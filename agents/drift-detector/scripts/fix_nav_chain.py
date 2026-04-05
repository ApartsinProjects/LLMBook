#!/usr/bin/env python3
"""
Fix navigation chain: rewrite prev/next links so they form a correct
bidirectional sequence within each chapter/module directory.

Dry-run by default. Pass --apply to write changes.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from book_utils import BOOK_ROOT, read_file, find_section_files


def _section_sort_key(fpath):
    """Sort key for section files: extract numeric parts from filename."""
    name = Path(fpath).stem  # section-9.2
    m = re.match(r"section-(.+)", name)
    if not m:
        return (0, 0, name)
    num_str = m.group(1)
    parts = num_str.split(".")
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            nums.append(ord(p[0]) if p else 0)
    return tuple(nums)


def fix_chapter_nav(module_dir, apply=False):
    """Fix nav links for all section files in a module directory."""
    sections = sorted(Path(module_dir).glob("section-*.html"), key=_section_sort_key)
    if not sections:
        return []

    changes = []
    index_path = Path(module_dir) / "index.html"
    up_href = "index.html" if index_path.exists() else "../index.html"

    for i, fpath in enumerate(sections):
        html = read_file(fpath)

        # Determine correct prev/next
        if i == 0:
            prev_href = up_href
        else:
            prev_href = sections[i - 1].name

        if i == len(sections) - 1:
            next_href = None  # Will need manual connection to next chapter
        else:
            next_href = sections[i + 1].name

        # Find existing nav block
        nav_match = re.search(
            r'(<nav\s+class="chapter-nav">)(.*?)(</nav>)',
            html, re.DOTALL
        )
        if not nav_match:
            changes.append((fpath, "SKIP", "No chapter-nav found"))
            continue

        nav_inner = nav_match.group(2)

        # Update prev link
        new_nav = nav_inner
        if prev_href:
            new_nav = re.sub(
                r'(<a\s+href=")[^"]*("\s+class="prev")',
                rf'\g<1>{prev_href}\2',
                new_nav,
            )
            # Also handle class before href
            new_nav = re.sub(
                r'(<a\s+class="prev"\s+href=")[^"]*(")',
                rf'\g<1>{prev_href}\2',
                new_nav,
            )

        # Update next link
        if next_href:
            new_nav = re.sub(
                r'(<a\s+href=")[^"]*("\s+class="next")',
                rf'\g<1>{next_href}\2',
                new_nav,
            )
            new_nav = re.sub(
                r'(<a\s+class="next"\s+href=")[^"]*(")',
                rf'\g<1>{next_href}\2',
                new_nav,
            )

        # Update up link
        new_nav = re.sub(
            r'(<a\s+href=")[^"]*("\s+class="up")',
            rf'\g<1>{up_href}\2',
            new_nav,
        )
        new_nav = re.sub(
            r'(<a\s+class="up"\s+href=")[^"]*(")',
            rf'\g<1>{up_href}\2',
            new_nav,
        )

        if new_nav != nav_inner:
            new_html = html[:nav_match.start(2)] + new_nav + html[nav_match.end(2):]
            changes.append((fpath, "CHANGED", f"prev={prev_href}, next={next_href}"))
            if apply:
                fpath.write_text(new_html, encoding="utf-8")
        else:
            changes.append((fpath, "OK", "No changes needed"))

    return changes


def main():
    apply = "--apply" in sys.argv

    if apply:
        print("MODE: APPLY (writing changes)")
    else:
        print("MODE: DRY RUN (pass --apply to write)")

    # Find all module directories
    module_dirs = set()
    for fpath in find_section_files():
        module_dirs.add(Path(fpath).parent)

    total_changed = 0
    for mdir in sorted(module_dirs):
        changes = fix_chapter_nav(mdir, apply=apply)
        changed = [c for c in changes if c[1] == "CHANGED"]
        if changed:
            print(f"\n  {mdir.relative_to(BOOK_ROOT)}:")
            for fpath, status, detail in changes:
                if status == "CHANGED":
                    print(f"    [{status}] {fpath.name}: {detail}")
                    total_changed += 1

    print(f"\n  Total: {total_changed} files {'updated' if apply else 'would change'}")


if __name__ == "__main__":
    main()
