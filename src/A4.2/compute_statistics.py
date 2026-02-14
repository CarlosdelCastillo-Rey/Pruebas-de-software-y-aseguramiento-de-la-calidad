#!/usr/bin/env python3
"""
compute_statistics.py

Compute descriptive statistics (mean, median, mode, variance and standard
deviation) from numeric data in text files.

Usage:
    python compute_statistics.py fileWithData.txt
    python compute_statistics.py <folder_with_TC_files>
"""

from __future__ import annotations

import os
import sys
import time
import math
from typing import List, Tuple, Optional


def get_results_file_path() -> str:
    """
    Build the absolute path for the results file.

    Returns:
        Full path to output/StatisticsResults.txt
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    results_path = os.path.join(
        repo_root,
        "output",
        "StatisticsResults.txt",
    )

    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    return results_path


def parse_numbers_from_file(path: str) -> Tuple[List[float], List[str]]:
    """
    Parse numeric values from a file.

    Invalid data is reported and skipped.
    """
    numbers: List[float] = []
    errors: List[str] = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            line_no = 0
            for raw_line in file:
                line_no += 1
                line = raw_line.strip()

                if not line:
                    continue

                parts = line.split(",")
                tokens: List[str] = []
                for part in parts:
                    tokens.extend(part.split())

                for token in tokens:
                    try:
                        numbers.append(float(token))
                    except ValueError:
                        errors.append(
                            f"{os.path.basename(path)} - line {line_no}: "
                            f"'{token}' skipped"
                        )
    except FileNotFoundError:
        errors.append(f"File not found: {path}")
    except OSError as exc:
        errors.append(f"Could not read file '{path}': {exc}")

    return numbers, errors


def compute_mean(values: List[float]) -> float:
    """Compute arithmetic mean."""
    total = 0.0
    count = 0
    for value in values:
        total += value
        count += 1
    return total / count


def compute_median(sorted_values: List[float]) -> float:
    """Compute median."""
    size = len(sorted_values)
    mid = size // 2
    if size % 2 == 1:
        return sorted_values[mid]
    return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0


def compute_mode(sorted_values: List[float]) -> Optional[List[float]]:
    """Compute mode(s)."""
    if not sorted_values:
        return None

    max_count = 1
    current = 1
    modes: List[float] = []

    for i in range(1, len(sorted_values)):
        if sorted_values[i] == sorted_values[i - 1]:
            current += 1
        else:
            if current > max_count:
                max_count = current
                modes = [sorted_values[i - 1]]
            elif current == max_count and current > 1:
                modes.append(sorted_values[i - 1])
            current = 1

    if current > max_count:
        modes = [sorted_values[-1]]
    elif current == max_count and current > 1:
        modes.append(sorted_values[-1])

    if max_count == 1:
        return None

    return modes


def compute_population_variance(values: List[float], mean: float) -> float:
    """Compute population variance."""
    total = 0.0
    count = 0
    for value in values:
        diff = value - mean
        total += diff * diff
        count += 1
    return total / count


def format_modes(modes: Optional[List[float]]) -> str:
    """Format mode output."""
    if modes is None:
        return "No mode"
    return ", ".join(str(m) for m in modes)


def list_tc_files(folder: str) -> List[str]:
    """Return sorted list of TC*.txt files."""
    files: List[str] = []
    for name in os.listdir(folder):
        if name.lower().startswith("tc") and name.lower().endswith(".txt"):
            files.append(os.path.join(folder, name))
    files.sort()
    return files


def compute_statistics_for_file(path: str) -> Tuple[str, List[str]]:
    """Compute statistics for one file."""
    start = time.perf_counter()
    numbers, errors = parse_numbers_from_file(path)
    elapsed = time.perf_counter() - start

    header = (
        f"\n=== Results for {os.path.basename(path)} ===\n"
        "Descriptive Statistics Results\n"
        "-------------------------------\n"
    )

    if not numbers:
        section = (
            header
            + "No valid numeric data found. No statistics computed.\n"
            + f"Elapsed time (seconds): {elapsed}\n"
        )
        return section, errors

    sorted_numbers = sorted(numbers)

    mean_val = compute_mean(numbers)
    median_val = compute_median(sorted_numbers)
    mode_val = compute_mode(sorted_numbers)
    variance_val = compute_population_variance(numbers, mean_val)
    std_dev_val = math.sqrt(variance_val)

    section = (
        header
        + f"Count: {len(numbers)}\n"
        + f"Mean: {mean_val}\n"
        + f"Median: {median_val}\n"
        + f"Mode: {format_modes(mode_val)}\n"
        + f"Variance (population): {variance_val}\n"
        + f"Standard Deviation (population): {std_dev_val}\n"
        + f"Elapsed time (seconds): {elapsed}\n"
    )

    return section, errors


def write_results(path: str, text: str) -> None:
    """Write results to file."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def main() -> int:
    """Program entry point."""
    if len(sys.argv) < 2:
        print("Usage: python compute_statistics.py <file|folder>")
        return 2

    input_path = sys.argv[1]
    results_path = get_results_file_path()

    start_total = time.perf_counter()

    report: List[str] = []
    all_errors: List[str] = []

    if os.path.isdir(input_path):
        files = list_tc_files(input_path)
        if not files:
            print("ERROR: No TC*.txt files found.")
            return 1
        for file_path in files:
            section, errors = compute_statistics_for_file(file_path)
            report.append(section)
            all_errors.extend(errors)
    else:
        section, errors = compute_statistics_for_file(input_path)
        report.append(section)
        all_errors.extend(errors)

    for error in all_errors:
        print(f"ERROR: {error}")

    total_elapsed = time.perf_counter() - start_total
    footer = f"\n=== Total elapsed time (seconds): {total_elapsed} ===\n"

    final_report = "".join(report) + footer

    print(final_report, end="")
    write_results(results_path, final_report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
