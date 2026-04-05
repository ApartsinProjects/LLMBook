#!/usr/bin/env python3
"""Detect caption numbering drift: wrong chapter prefix, gaps, duplicates."""

import re
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from book_utils import (
    BOOK_ROOT, DriftReport, read_file, extract_captions,
    section_num_from_filename, chapter_num_from_dirname, find_section_files,
)


def main():
    report = DriftReport("CAPTION NUMBERING (Figure/Table/Code/Exercise)")
    section_files = find_section_files()

    for fpath in section_files:
        fpath = Path(fpath)
        html = read_file(fpath)
        captions = extract_captions(html)

        if not captions:
            continue

        sec_num = section_num_from_filename(fpath)
        ch_num = chapter_num_from_dirname(fpath)

        # Group captions by type
        by_type = defaultdict(list)
        for kind, num_str, pos in captions:
            by_type[kind].append((num_str, pos))

        for kind, entries in by_type.items():
            seen_numbers = []
            for num_str, pos in entries:
                # Parse the caption number: could be "9.1", "9.2.1", "h.3.1", etc.
                parts = num_str.split(".")

                # Check chapter prefix matches
                if ch_num is not None and parts[0].isdigit():
                    caption_ch = int(parts[0])
                    if caption_ch != ch_num:
                        report.error(
                            fpath,
                            f"{kind} {num_str}: wrong chapter prefix",
                            expected=f"Chapter {ch_num}",
                            actual=f"Chapter {caption_ch}",
                        )

                seen_numbers.append(num_str)

            # Check for duplicates
            for i, num in enumerate(seen_numbers):
                if seen_numbers.count(num) > 1 and seen_numbers.index(num) == i:
                    report.error(fpath, f"Duplicate {kind} {num}")

            # Check for sequential gaps (only for simple X.Y patterns)
            seq_nums = []
            for num in seen_numbers:
                parts = num.split(".")
                if len(parts) >= 2 and parts[-1].isdigit():
                    seq_nums.append(int(parts[-1]))

            if seq_nums:
                for i in range(len(seq_nums) - 1):
                    if seq_nums[i + 1] != seq_nums[i] + 1:
                        # Allow restart at 1 (different sub-section)
                        if seq_nums[i + 1] != 1:
                            report.warn(
                                fpath,
                                f"{kind} numbering gap: {seen_numbers[i]} followed by {seen_numbers[i+1]}",
                            )

    report.print_report()


if __name__ == "__main__":
    main()
