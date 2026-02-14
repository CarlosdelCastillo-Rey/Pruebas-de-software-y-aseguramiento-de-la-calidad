"""
compute_sales.py

Usage:
    python compute_sales.py <base_folder_with_TC_folders>
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd


OUTPUT_FILENAME = "SalesResults.txt"


def load_json_file(file_path: Path) -> Any:
    """Load and parse a JSON file."""
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def to_dataframe_catalogue(data: Any) -> pd.DataFrame:
    """Convert product catalogue JSON to a DataFrame."""
    df = pd.DataFrame(data)

    if "title" not in df.columns or "price" not in df.columns:
        raise ValueError(
            "Catalogue JSON must contain 'title' and 'price' fields."
        )

    df = df[["title", "price"]].copy()
    df["title"] = df["title"].astype(str).str.strip().str.lower()
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    return df


def to_dataframe_sales(data: Any) -> pd.DataFrame:
    """Convert sales JSON to a DataFrame."""
    df = pd.DataFrame(data)

    col_map: Dict[str, str] = {}
    for col in df.columns:
        lower = col.lower()
        if lower == "product":
            col_map[col] = "product"
        elif lower == "quantity":
            col_map[col] = "quantity"

    df = df.rename(columns=col_map)

    if "product" not in df.columns or "quantity" not in df.columns:
        raise ValueError(
            "Sales JSON must contain product and quantity fields."
        )

    df = df[["product", "quantity"]].copy()
    df["product"] = df["product"].astype(str).str.strip().str.lower()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    return df


def clean_data(
    df_catalogue: pd.DataFrame,
    df_sales: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, pd.DataFrame]]:
    """Validate and clean catalogue and sales data, returning errors found."""
    errors: Dict[str, pd.DataFrame] = {}

    price_nan = df_catalogue["price"].isna()
    if price_nan.any():
        errors["catalogue_price_not_numeric"] = df_catalogue[price_nan].copy()

    price_non_pos = df_catalogue["price"] <= 0
    if price_non_pos.any():
        errors["catalogue_price_non_positive"] = df_catalogue[
            price_non_pos
        ].copy()

    df_catalogue_clean = df_catalogue[~(price_nan | price_non_pos)].copy()

    qty_nan = df_sales["quantity"].isna()
    if qty_nan.any():
        errors["sales_quantity_not_numeric"] = df_sales[qty_nan].copy()

    qty_non_pos = df_sales["quantity"] <= 0
    if qty_non_pos.any():
        errors["sales_quantity_non_positive"] = df_sales[qty_non_pos].copy()

    df_sales_clean = df_sales[~(qty_nan | qty_non_pos)].copy()

    return df_catalogue_clean, df_sales_clean, errors


def compute_totals(
    df_catalogue: pd.DataFrame,
    df_sales: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Compute total cost per product and identify missing catalogue items."""
    sales_sum = df_sales.groupby("product", as_index=False)["quantity"].sum()

    merged = sales_sum.merge(
        df_catalogue,
        left_on="product",
        right_on="title",
        how="left",
    )

    missing = merged[merged["price"].isna()].copy()
    found = merged[~merged["price"].isna()].copy()

    if found.empty:
        found_df = pd.DataFrame(
            columns=["product", "quantity", "price", "total_cost"]
        )
    else:
        found_df = found[["product", "quantity", "price"]].copy()
        found_df["total_cost"] = found_df["quantity"] * found_df["price"]
        found_df = found_df.sort_values(by="total_cost", ascending=False)

    if missing.empty:
        missing_df = pd.DataFrame(columns=["product", "quantity"])
    else:
        missing_df = missing[["product", "quantity"]].copy()
        missing_df = missing_df.sort_values(by="quantity", ascending=False)

    return found_df, missing_df


def format_report(
    tc_name: str,
    detail: pd.DataFrame,
    missing: pd.DataFrame,
    errors: Dict[str, pd.DataFrame],
    elapsed_seconds: float,
) -> str:
    """Build a human-readable report for a single test case."""
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append(f"TC: {tc_name}")
    lines.append("=" * 80)
    lines.append("")

    if detail.empty:
        lines.append("RESULT:")
        lines.append(
            "No valid sales could be computed after cleaning and matching."
        )
        lines.append("")
        total_cost = 0.0
    else:
        lines.append("RESULT (per product):")
        lines.append(detail.to_string(index=False))
        lines.append("")
        total_cost = float(detail["total_cost"].sum())

    lines.append(f"TOTAL COST: {total_cost:.2f}")
    lines.append("")

    if not missing.empty:
        lines.append("WARNING: Sales products missing from catalogue:")
        lines.append(missing.to_string(index=False))
        lines.append("")

    if errors:
        lines.append("INVALID RECORDS:")
        for name, df_err in errors.items():
            lines.append("-" * 80)
            lines.append(f"{name} ({len(df_err)} rows)")
            lines.append(df_err.to_string(index=False))
            lines.append("")
    else:
        lines.append("No invalid records were found.")
        lines.append("")

    lines.append(f"TIME ELAPSED (seconds): {elapsed_seconds:.6f}")
    lines.append("=" * 80)
    lines.append("")

    return "\n".join(lines)


def print_errors_to_console(tc_name: str, errors:
                            Dict[str, pd.DataFrame]) -> None:
    """Print invalid records to the console, keeping execution running."""
    if not errors:
        return

    print(f"\nINVALID DATA FOUND in {tc_name} (execution continues):")
    for name, df_err in errors.items():
        print("-" * 80)
        print(f"{name} ({len(df_err)} rows)")
        print(df_err.head(20).to_string(index=False))
        if len(df_err) > 20:
            remaining = len(df_err) - 20
            print(f"... ({remaining} more rows)")


def load_base_catalogue(base_folder: Path) -> pd.DataFrame:
    """Load base product catalogue from TC1."""
    tc1_folder = base_folder / "TC1"
    if not tc1_folder.exists() or not tc1_folder.is_dir():
        raise FileNotFoundError(
            "TC1 folder not found inside the base folder."
        )

    product_files = list(tc1_folder.glob("*ProductList*.json"))
    if not product_files:
        raise FileNotFoundError(
            "ProductList file not found inside TC1."
        )

    data = load_json_file(product_files[0])
    return to_dataframe_catalogue(data)


def process_tc(tc_folder: Path, df_catalogue_base: pd.DataFrame) -> str:
    """Process a single TC folder using the base catalogue."""
    tc_name = tc_folder.name
    sales_files = list(tc_folder.glob("*Sales*.json"))

    if not sales_files:
        return (
            "=" * 80
            + "\n"
            + f"TC: {tc_name}\n"
            + "=" * 80
            + "\n\n"
            + "ERROR: Missing Sales file.\n\n"
        )

    start = time.perf_counter()

    try:
        sales_data = load_json_file(sales_files[0])
        df_sales = to_dataframe_sales(sales_data)

        df_cat_clean, df_sales_clean, errors = clean_data(
            df_catalogue_base.copy(),
            df_sales,
        )

        print_errors_to_console(tc_name, errors)

        detail, missing = compute_totals(df_cat_clean, df_sales_clean)

        elapsed = time.perf_counter() - start
        return format_report(tc_name, detail, missing, errors, elapsed)

    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        return (
            "=" * 80
            + "\n"
            + f"TC: {tc_name}\n"
            + "=" * 80
            + "\n\n"
            + f"ERROR processing {tc_name}: {exc}\n\n"
        )


def build_output_path(base_folder: Path) -> Path:
    """Build output path inside Output/A5.2."""
    repo_root = base_folder.parent.parent
    output_dir = repo_root / "Output" / "A5.2"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / OUTPUT_FILENAME


def main(argv: List[str]) -> int:
    """Program entry point."""
    exit_code = 0

    if len(argv) != 2:
        print("Usage: python compute_sales.py <base_folder_with_TC_folders>")
        return 1

    base_folder = Path(argv[1]).resolve()
    if not base_folder.exists() or not base_folder.is_dir():
        print(f"ERROR: Folder not found: {base_folder}")
        return 1

    try:
        output_path = build_output_path(base_folder)
    except OSError as exc:
        print(f"ERROR: Could not prepare output folder: {exc}")
        return 1

    try:
        df_catalogue_base = load_base_catalogue(base_folder)
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(f"ERROR loading base catalogue from TC1: {exc}")
        return 1

    tc_folders = [p for p in sorted(base_folder.iterdir()) if p.is_dir()]
    if not tc_folders:
        print("ERROR: No TC folders found inside the base folder.")
        return 1

    all_reports: List[str] = []
    for tc_folder in tc_folders:
        report = process_tc(tc_folder, df_catalogue_base)
        print(report)
        all_reports.append(report)

    try:
        output_path.write_text("\n".join(all_reports), encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: Could not write output file '{output_path}': {exc}")
        exit_code = 1

    if exit_code == 0:
        print(f"All TC processed. Results saved to: {output_path}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
