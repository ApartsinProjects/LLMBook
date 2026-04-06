#!/usr/bin/env python3
"""
Fix part and chapter labels in section files.
Rewrites <div class="part-label"> and <div class="chapter-label"> to match
the actual part/chapter derived from the directory structure.

Dry-run by default. Pass --apply to write changes.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from book_utils import (
    BOOK_ROOT, read_file, find_section_files,
    part_num_from_dirname, chapter_num_from_dirname,
    extract_part_label, extract_chapter_label,
)


def main():
    apply = "--apply" in sys.argv

    if apply:
        print("MODE: APPLY (writing changes)")
    else:
        print("MODE: DRY RUN (pass --apply to write)")

    section_files = find_section_files()
    total_changed = 0

    for fpath in section_files:
        fpath = Path(fpath)
        html = read_file(fpath)
        changed = False
        new_html = html

        part_num = part_num_from_dirname(fpath)
        ch_num = chapter_num_from_dirname(fpath)

        # Fix part label
        if part_num is not None:
            part_label = extract_part_label(html)
            if part_label:
                pl_match = re.search(r"(\d+)", part_label)
                if pl_match and int(pl_match.group(1)) != part_num:
                    # Replace the number in the part label
                    old_div = re.search(
                        r'(<div\s+class="part-label"[^>]*>)(.*?)(</div>)',
                        new_html, re.DOTALL
                    )
                    if old_div:
                        inner = old_div.group(2)
                        new_inner = re.sub(r"\d+", str(part_num), inner, count=1)
                        new_html = (
                            new_html[:old_div.start(2)]
                            + new_inner
                            + new_html[old_div.end(2):]
                        )
                        changed = True
                        print(f"  [PART] {fpath.relative_to(BOOK_ROOT)}: "
                              f"{part_label} -> Part {part_num}")

        # Fix chapter label
        if ch_num is not None:
            ch_label = extract_chapter_label(html)
            if ch_label:
                cl_match = re.search(r"Chapter\s+(\d+)", ch_label)
                if cl_match and int(cl_match.group(1)) != ch_num:
                    old_div = re.search(
                        r'(<div\s+class="chapter-label"[^>]*>)(.*?)(</div>)',
                        new_html, re.DOTALL
                    )
                    if old_div:
                        inner = old_div.group(2)
                        new_inner = re.sub(
                            r"Chapter\s+\d+",
                            f"Chapter {ch_num}",
                            inner, count=1
                        )
                        new_html = (
                            new_html[:old_div.start(2)]
                            + new_inner
                            + new_html[old_div.end(2):]
                        )
                        changed = True
                        print(f"  [CH]   {fpath.relative_to(BOOK_ROOT)}: "
                              f"{ch_label} -> Chapter {ch_num}")

        if changed:
            total_changed += 1
            if apply:
                fpath.write_text(new_html, encoding="utf-8")

    print(f"\n  Total: {total_changed} files {'updated' if apply else 'would change'}")


if __name__ == "__main__":
    main()
