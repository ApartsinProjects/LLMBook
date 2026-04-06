"""
Fix chapter-nav and footer across all section/index files.

Issues:
1. 3-way nav (prev/up/next) has redundant "up" link (chapter index already in header)
2. First sections have prev == up (both point to index.html)
3. Inconsistent footer: 77 files have 3-line WAVE 7 footer, 168 have 1-line original

Fix:
- Remove the "up" link from all chapter-nav blocks (2-link prev/next only)
- CSS already handles 2-child layout (grid auto-fills)
- Standardize all footers to the simple 1-line format
"""

import re
import glob
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

stats = {
    "up_removed": 0,
    "footer_standardized": 0,
    "total_scanned": 0,
    "total_changed": 0,
}

SIMPLE_FOOTER_SECTION = '<footer><p>Fifth Edition, 2026 &middot; <a href="{root}/toc.html">Contents</a></p></footer>'

# Match the 3-line WAVE 7 footer
WAVE7_FOOTER_RE = re.compile(
    r'<footer>\s*'
    r'<p class="footer-title">.*?</p>\s*'
    r'<p>.*?</p>\s*'
    r'<p class="footer-updated">.*?</p>\s*'
    r'</footer>',
    re.DOTALL
)


def get_root_path(filepath: Path) -> str:
    rel = filepath.relative_to(BOOK_ROOT)
    depth = len(rel.parts) - 1
    if depth == 0:
        return "."
    return "/".join([".."] * depth)


def fix_file(filepath: Path):
    content = filepath.read_text(encoding="utf-8")
    original = content
    stats["total_scanned"] += 1
    root = get_root_path(filepath)

    # 1. Remove "up" link from chapter-nav
    # Pattern: <a class="up" href="...">...</a> with surrounding whitespace
    up_pattern = re.compile(r'\s*<a class="up" href="[^"]*">[^<]*</a>\s*')
    if 'class="up"' in content:
        content = up_pattern.sub('\n', content)
        stats["up_removed"] += 1

    # 2. Standardize footer
    simple_footer = SIMPLE_FOOTER_SECTION.format(root=root)

    # Replace 3-line WAVE 7 footer
    if 'footer-title' in content:
        content = WAVE7_FOOTER_RE.sub(simple_footer, content)
        stats["footer_standardized"] += 1
    # Also fix any existing simple footer with wrong root path
    # (leave correct ones alone)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        stats["total_changed"] += 1
        return True
    return False


def main():
    patterns = [
        "part-*/module-*/section-*.html",
        "part-*/module-*/index.html",
        "part-*/index.html",
        "appendices/appendix-*/section-*.html",
        "appendices/appendix-*/index.html",
        "front-matter/*.html",
    ]

    all_files = []
    for pattern in patterns:
        all_files.extend(BOOK_ROOT.glob(pattern))
    all_files = sorted(set(all_files))

    print(f"Scanning {len(all_files)} files...")

    for f in all_files:
        changed = fix_file(f)
        if changed:
            print(f"  FIXED: {f.relative_to(BOOK_ROOT)}")

    print(f"\n=== Summary ===")
    print(f"Total scanned: {stats['total_scanned']}")
    print(f"Total changed: {stats['total_changed']}")
    print(f"Up links removed: {stats['up_removed']}")
    print(f"Footers standardized: {stats['footer_standardized']}")

    # Verification
    print(f"\n=== Verification ===")
    remaining_up = 0
    remaining_wave7 = 0
    for f in all_files:
        content = f.read_text(encoding="utf-8")
        if 'class="up"' in content and 'chapter-nav' in content:
            remaining_up += 1
        if 'footer-title' in content:
            remaining_wave7 += 1

    print(f"Remaining 'up' links in chapter-nav: {remaining_up}")
    print(f"Remaining 3-line footers: {remaining_wave7}")


if __name__ == "__main__":
    main()
