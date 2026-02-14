#!/usr/bin/env python3
"""
word_count.py

Counts distinct words and their frequency from a text file or from
multiple TC*.txt files inside a folder.

Usage:
    python word_count.py fileWithData.txt
    python word_count.py Data\\P3
"""

from __future__ import annotations

import os
import sys
import time
from typing import Dict, List, Tuple


def get_repo_root() -> str:
    """Return the repository root folder (parent of the script directory)."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def get_output_path() -> str:
    """Return the output path for WordCountResults.txt inside output/."""
    repo_root = get_repo_root()
    out_path = os.path.join(repo_root, "output", "WordCountResults.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    return out_path


def resolve_input_path(input_path: str) -> str:
    """Resolve a relative input path against the repository root."""
    if os.path.isabs(input_path):
        return input_path
    repo_root = get_repo_root()
    return os.path.join(repo_root, input_path)


def list_tc_files(folder_path: str) -> List[str]:
    """List and sort all TC*.txt files in the given folder."""
    files: List[str] = []
    for name in os.listdir(folder_path):
        lower = name.lower()
        if lower.startswith("tc") and lower.endswith(".txt"):
            files.append(os.path.join(folder_path, name))
    files.sort()
    return files


def read_words_from_file(path: str) -> Tuple[List[str], List[str]]:
    """
    Read words from a file.

    Words are separated by spaces.
    Empty lines are reported as errors and skipped.

    Returns:
        (words, errors)
    """
    words: List[str] = []
    errors: List[str] = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            line_number = 0
            for raw_line in file:
                line_number += 1
                line = raw_line.strip()

                if line == "":
                    errors.append(
                        f"{os.path.basename(path)} - Empty line at line {line_number}"
                    )
                    continue

                tokens = line.split(" ")
                for token in tokens:
                    if token != "":
                        words.append(token.lower())
    except OSError:
        errors.append(f"Error opening or reading file: {path}")

    return words, errors


def count_words(words: List[str]) -> Dict[str, int]:
    """Count word frequency using a basic dictionary + loops algorithm."""
    counts: Dict[str, int] = {}

    for word in words:
        if word in counts:
            counts[word] = counts[word] + 1
        else:
            counts[word] = 1

    return counts


def build_section(file_name: str, counts: Dict[str, int], elapsed: float) -> str:
    """Build a report section for one file."""
    section = (
        f"\n=== Results for {file_name} ===\n"
        "Word Count Results\n"
        "------------------\n"
    )

    for word, freq in counts.items():
        section += f"{word}: {freq}\n"

    section += f"Elapsed time (seconds): {elapsed}\n"
    return section


def write_results(result_path: str, text: str) -> None:
    """Write the final report text to a file."""
    with open(result_path, "w", encoding="utf-8") as file:
        file.write(text)


def print_counts_to_console(file_name: str, errors: List[str],
                            counts: Dict[str, int], elapsed: float) -> None:
    """Print a single file's results to the console."""
    print(f"\nFILE: {file_name}")
    for err in errors:
        print(f"ERROR: {err}")

    for word, freq in counts.items():
        print(f"{word} : {freq}")

    print(f"Elapsed time (seconds): {elapsed}")


def main() -> int:
    """Program entry point."""
    if len(sys.argv) < 2:
        print("Usage: python wordCount.py fileWithData.txt")
        print("   or: python wordCount.py Data\\P3")
        return 2

    input_path = resolve_input_path(sys.argv[1])
    output_path = get_output_path()

    total_start = time.perf_counter()
    report = ""

    if os.path.isdir(input_path):
        tc_files = list_tc_files(input_path)
        if not tc_files:
            print(f"ERROR: No TC*.txt files found in folder: {input_path}")
            return 1

        for file_path in tc_files:
            start = time.perf_counter()
            words, errors = read_words_from_file(file_path)
            counts = count_words(words)
            elapsed = time.perf_counter() - start

            print_counts_to_console(
                os.path.basename(file_path),
                errors,
                counts,
                elapsed,
            )
            report += build_section(os.path.basename(file_path), counts, elapsed)
    else:
        start = time.perf_counter()
        words, errors = read_words_from_file(input_path)
        counts = count_words(words)
        elapsed = time.perf_counter() - start

        print_counts_to_console(
            os.path.basename(input_path),
            errors,
            counts,
            elapsed,
        )
        report += build_section(os.path.basename(input_path), counts, elapsed)

    total_elapsed = time.perf_counter() - total_start
    report += f"\n=== Total elapsed time (seconds): {total_elapsed} ===\n"
    print(f"\n=== Total elapsed time (seconds): {total_elapsed} ===\n")

    write_results(output_path, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
