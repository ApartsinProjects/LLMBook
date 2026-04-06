#!/usr/bin/env python3
"""Detect section numbering drift: filename vs heading, part/chapter labels, missing sections."""

import re
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from book_utils import (
    BOOK_ROOT, DriftReport, read_file, extract_h1,
    extract_part_label, extract_chapter_label,
    section_num_from_filename, chapter_num_from_dirname, part_num_from_dirname,
    find_section_files,
)


def main():
    report = DriftReport("SECTION NUMBERING CONSISTENCY")
    section_files = find_section_files()

    # Group by chapter directory
    by_chapter = defaultdict(list)

    for fpath in section_files:
        fpath = Path(fpath)
        html = read_file(fpath)

        sec_num = section_num_from_filename(fpath)
        ch_num = chapter_num_from_dirname(fpath)
        part_num = part_num_from_dirname(fpath)
        h1 = extract_h1(html)

        # Track for gap detection
        if ch_num is not None:
            by_chapter[ch_num].append((sec_num, fpath))

        # Check h1 contains correct section number
        if h1 and sec_num:
            # Extract number from h1
            h1_num_match = re.match(r"^([\d]+\.[\d.]+)", h1)
            if h1_num_match:
                h1_num = h1_num_match.group(1).rstrip(".")
                file_num = sec_num.rstrip(".")
                if h1_num != file_num:
                    report.warn(
                        fpath,
                        f"Filename/heading number mismatch",
                        expected=f"Filename: {file_num}",
                        actual=f"Heading: {h1_num}",
                    )

        # Check part label
        if part_num is not None:
            part_label = extract_part_label(html)
            if part_label:
                # Extract number from label
                pl_match = re.search(r"(\d+)", part_label)
                if pl_match:
                    label_part = int(pl_match.group(1))
                    if label_part != part_num:
                        report.error(
                            fpath,
                            f"Part label mismatch",
                            expected=f"Part {part_num}",
                            actual=f"Part label says: {part_label}",
                        )

        # Check chapter label
        if ch_num is not None:
            ch_label = extract_chapter_label(html)
            if ch_label:
                cl_match = re.search(r"Chapter\s+(\d+)", ch_label)
                if cl_match:
                    label_ch = int(cl_match.group(1))
                    if label_ch != ch_num:
                        report.warn(
                            fpath,
                            f"Chapter label mismatch",
                            expected=f"Chapter {ch_num}",
                            actual=f"Label says: {ch_label}",
                        )

    # Check for missing sections (gaps in numbering within each chapter)
    for ch_num, sections in sorted(by_chapter.items()):
        # Extract the sub-number (e.g., "9.2" -> 2)
        sub_nums = []
        for sec_num, fpath in sections:
            parts = sec_num.split(".")
            if len(parts) >= 2 and parts[1].isdigit():
                sub_nums.append(int(parts[1]))

        if sub_nums:
            sub_nums_sorted = sorted(set(sub_nums))
            expected_range = range(sub_nums_sorted[0], sub_nums_sorted[-1] + 1)
            missing = [n for n in expected_range if n not in sub_nums_sorted]
            for m in missing:
                report.warn(
                    BOOK_ROOT,
                    f"Chapter {ch_num}: missing section {ch_num}.{m} "
                    f"(have {', '.join(f'{ch_num}.{n}' for n in sub_nums_sorted)})",
                )

    report.print_report()


if __name__ == "__main__":
    main()
