"""
Add a book-title-bar div as the first element after <body> in all HTML files
(excluding root index.html and toc.html). The bar links back to the root cover page.
Also reports what was changed.
"""

import os
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/LLMCourse")
BOOK_TITLE = "Building Conversational AI with LLMs and Agents"

# Files to exclude (root-level)
EXCLUDE = {"index.html", "toc.html"}

def get_relative_root(html_path: Path) -> str:
    """Return the relative path from html_path's directory to ROOT/index.html."""
    rel = html_path.parent.relative_to(ROOT)
    depth = len(rel.parts)
    if depth == 0:
        return "index.html"
    return "../" * depth + "index.html"

def make_bar(href: str) -> str:
    return (
        '<div class="book-title-bar">\n'
        f'    <a href="{href}">{BOOK_TITLE}</a>\n'
        '</div>\n'
    )

def process_file(path: Path) -> str | None:
    """Add book-title-bar if missing. Returns a status string or None if skipped."""
    text = path.read_text(encoding="utf-8", errors="replace")

    # Already has the bar
    if 'class="book-title-bar"' in text:
        return None

    # Find <body...> tag
    m = re.search(r"(<body[^>]*>)", text, re.IGNORECASE)
    if not m:
        return f"SKIP (no <body> tag): {path}"

    href = get_relative_root(path)
    bar_html = make_bar(href)

    # Insert right after <body...> (plus optional newline)
    insert_pos = m.end()
    # Skip a single newline if present
    if insert_pos < len(text) and text[insert_pos] == "\n":
        insert_pos += 1

    new_text = text[:insert_pos] + bar_html + text[insert_pos:]
    path.write_text(new_text, encoding="utf-8")
    return f"ADDED: {path.relative_to(ROOT)}"


def main():
    changed = []
    skipped = []
    already = []

    # Find all .html files under ROOT (excluding root-level excludes)
    for html_file in sorted(ROOT.rglob("*.html")):
        # Skip root-level excluded files
        rel = html_file.relative_to(ROOT)
        if str(rel) in EXCLUDE:
            skipped.append(f"EXCLUDE: {rel}")
            continue

        # Skip files not in subdirectories (other root-level html)
        # Actually, let's include all except the explicit excludes
        # But skip any non-content dirs
        parts = rel.parts
        if parts[0] in ("node_modules", ".git", "_lab_fragments", "styles"):
            continue

        result = process_file(html_file)
        if result is None:
            already.append(str(rel))
        elif result.startswith("ADDED"):
            changed.append(result)
        else:
            skipped.append(result)

    print(f"\n=== Book Title Bar Insertion Report ===")
    print(f"Files modified: {len(changed)}")
    print(f"Already had bar: {len(already)}")
    print(f"Skipped: {len(skipped)}")

    if changed:
        print(f"\nModified files:")
        for c in changed:
            print(f"  {c}")

    if already:
        print(f"\nAlready present in:")
        for a in already[:5]:
            print(f"  {a}")
        if len(already) > 5:
            print(f"  ... and {len(already) - 5} more")

    if skipped:
        print(f"\nSkipped:")
        for s in skipped:
            print(f"  {s}")


if __name__ == "__main__":
    main()
