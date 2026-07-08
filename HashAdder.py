#!/usr/bin/env python3
"""
HashAdder - Python Hash Calculator

Calculates common cryptographic hashes for a file, useful for verifying
file integrity or comparing against known-good hashes (e.g. malware
signature checks, download verification).
"""

import argparse
import hashlib
import sys
from pathlib import Path

# Algorithms to calculate. Easy to add/remove entries here.
ALGORITHMS = ["md5", "sha1", "sha256", "sha512"]

CHUNK_SIZE = 65536  # 64KB - read large files in chunks instead of all at once


def calculate_hashes(file_path: Path, algorithms=None) -> dict:
    """
    Calculate one or more hash digests for a file.

    Reads the file in chunks so it works on large files without
    loading the whole thing into memory.
    """
    if algorithms is None:
        algorithms = ALGORITHMS

    hashers = {name: hashlib.new(name) for name in algorithms}

    with open(file_path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            for hasher in hashers.values():
                hasher.update(chunk)

    return {name: hasher.hexdigest() for name, hasher in hashers.items()}


def format_results(file_path: Path, hashes: dict) -> str:
    lines = [
        f"File: {file_path}",
        f"Size: {file_path.stat().st_size:,} bytes",
        "-" * 50,
    ]
    for name, digest in hashes.items():
        lines.append(f"{name.upper():<8}: {digest}")
    return "\n".join(lines)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate cryptographic hashes for a file."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to the file to hash. If omitted, you'll be prompted.",
    )
    parser.add_argument(
        "-a", "--algorithms",
        nargs="+",
        choices=ALGORITHMS,
        default=None,
        help=f"Specific algorithms to run (default: all of {ALGORITHMS}).",
    )
    parser.add_argument(
        "-c", "--compare",
        metavar="HASH",
        help="Compare the computed hash(es) against this value and report a match.",
    )
    return parser.parse_args()


def main():
    print("HashAdder Python Hash Calculator\n")
    args = parse_args()

    file_input = args.file or input("Enter file path: ").strip().strip('"')
    file_path = Path(file_input)

    if not file_path.exists():
        print(f"Error: '{file_path}' does not exist.")
        sys.exit(1)
    if not file_path.is_file():
        print(f"Error: '{file_path}' is not a file.")
        sys.exit(1)

    try:
        hashes = calculate_hashes(file_path, args.algorithms)
    except PermissionError:
        print(f"Error: permission denied reading '{file_path}'.")
        sys.exit(1)
    except OSError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    print(format_results(file_path, hashes))

    if args.compare:
        target = args.compare.lower().strip()
        match = next((name for name, digest in hashes.items() if digest == target), None)
        print("-" * 50)
        if match:
            print(f"MATCH: computed {match.upper()} matches the provided hash.")
        else:
            print("NO MATCH: provided hash does not match any computed digest.")


if __name__ == "__main__":
    main()
