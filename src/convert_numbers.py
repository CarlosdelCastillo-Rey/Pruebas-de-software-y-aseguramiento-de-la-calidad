#!/usr/bin/env python3
"""
convertNumbers.py

Read numbers from a file (or multiple TC*.txt files in a folder) and convert
each integer to binary and hexadecimal using basic algorithms (no bin/hex).

Usage:
    python convertNumbers.py fileWithData.txt
    python convertNumbers.py <folder_with_TC_files>
"""

from __future__ import annotations

import os
import sys
import time
from typing import List, Tuple


HEX_DIGITS = "0123456789ABCDEF"


def get_results_file_path() -> str:
    """
    Build the absolute path for the results file.

    Returns:
        Full path to output/ConvertionResults.txt
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    results_path = os.path.join(repo_root, "output", "ConvertionResults.txt")
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    return results_path


def resolve_input_path(input_path: str) -> str:
    """
    Resolve a relative input path against the repository root so it works
    even when running from inside src/.
    """
    if os.path.isabs(input_path):
        return input_path

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    return os.path.join(repo_root, input_path)


def list_tc_files(folder_path: str) -> List[str]:
    """List and sort TC*.txt files in a folder."""
    files: List[str] = []
    for name in os.listdir(folder_path):
        lower = name.lower()
        if lower.startswith("tc") and lower.endswith(".txt"):
            files.append(os.path.join(folder_path, name))
    files.sort()
    return files


def parse_integers_from_file(path: str) -> Tuple[List[int], List[str]]:
    """
    Parse integer values from a file.

    Accepts tokens separated by whitespace and/or commas.
    Invalid tokens are reported and skipped.
    """
    numbers: List[int] = []
    errors: List[str] = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            line_no = 0
            for raw_line in file:
                line_no += 1
                line = raw_line.strip()
                if not line:
                    continue

                comma_parts = line.split(",")
                tokens: List[str] = []
                for part in comma_parts:
                    tokens.extend(part.split())

                for token in tokens:
                    token_stripped = token.strip()
                    if not token_stripped:
                        continue

                    if not is_valid_integer_token(token_stripped):
                        errors.append(
                            f"{os.path.basename(path)} - line {line_no}: "
                            f"'{token_stripped}' skipped"
                        )
                        continue

                    try:
                        numbers.append(int(token_stripped))
                    except ValueError:
                        errors.append(
                            f"{os.path.basename(path)} - line {line_no}: "
                            f"'{token_stripped}' skipped"
                        )
    except FileNotFoundError:
        errors.append(f"File not found: {path}")
    except OSError as exc:
        errors.append(f"Could not read file '{path}': {exc}")

    return numbers, errors


def is_valid_integer_token(token: str) -> bool:
    """
    Check if token represents a valid base-10 integer (no decimals).
    Accepts: "10", "-3", "+7"
    Rejects: "3.14", "1e3", "abc"
    """
    if token in ("+", "-"):
        return False

    start = 1 if token[0] in "+-" else 0
    if start >= len(token):
        return False

    for ch in token[start:]:
        if ch < "0" or ch > "9":
            return False

    return True


def to_binary_str(number: int) -> str:
    """Convert an integer to binary string using repeated division."""
    if number == 0:
        return "0"

    sign = ""
    n = number
    if n < 0:
        sign = "-"
        n = -n

    bits: List[str] = []
    while n > 0:
        remainder = n % 2
        bits.append("1" if remainder == 1 else "0")
        n //= 2

    bits.reverse()
    return sign + "".join(bits)


def to_hex_str(number: int) -> str:
    """Convert an integer to hexadecimal string using repeated division."""
    if number == 0:
        return "0"

    sign = ""
    n = number
    if n < 0:
        sign = "-"
        n = -n

    digits: List[str] = []
    while n > 0:
        remainder = n % 16
        digits.append(HEX_DIGITS[remainder])
        n //= 16

    digits.reverse()
    return sign + "".join(digits)


def build_section(source_label: str, rows: List[str], elapsed_seconds: float) -> str:
    """Build one report section for a single input file."""
    header = (
        f"\n=== Results for {source_label} ===\n"
        "Conversion Results\n"
        "------------------\n"
        "Decimal\tBinary\tHexadecimal\n"
        "-------\t------\t-----------\n"
    )
    body = "\n".join(rows) + ("\n" if rows else "")
    footer = f"Elapsed time (seconds): {elapsed_seconds}\n"
    return header + body + footer


def write_results(path: str, text: str) -> None:
    """Write results text to a file."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def convert_file(file_path: str) -> Tuple[str, List[str], float]:
    """
    Convert numbers from a single file.

    Returns:
        (section_text, errors, elapsed_seconds)
    """
    start = time.perf_counter()

    numbers, errors = parse_integers_from_file(file_path)
    rows: List[str] = []

    for num in numbers:
        bin_str = to_binary_str(num)
        hex_str = to_hex_str(num)
        rows.append(f"{num}\t{bin_str}\t{hex_str}")

    elapsed = time.perf_counter() - start
    section = build_section(os.path.basename(file_path), rows, elapsed)
    return section, errors, elapsed


def main() -> int:
    """Program entry point."""
    if len(sys.argv) < 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        print("   or: python convertNumbers.py <folder_with_TC_files>")
        return 2

    input_arg = resolve_input_path(sys.argv[1])
    results_path = get_results_file_path()

    total_start = time.perf_counter()
    full_report = ""
    all_errors: List[str] = []

    if os.path.isdir(input_arg):
        tc_files = list_tc_files(input_arg)
        if not tc_files:
            print(f"ERROR: No TC*.txt files found in folder: {input_arg}")
            return 1

        for file_path in tc_files:
            section, errors, _ = convert_file(file_path)
            full_report += section
            all_errors.extend(errors)
    else:
        section, errors, _ = convert_file(input_arg)
        full_report += section
        all_errors.extend(errors)

    for err in all_errors:
        print(f"ERROR: {err}")

    total_elapsed = time.perf_counter() - total_start
    full_report += f"\n=== Total elapsed time (seconds): {total_elapsed} ===\n"

    print(full_report, end="")
    write_results(results_path, full_report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
