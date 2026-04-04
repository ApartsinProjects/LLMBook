"""Fix known broken cross-reference links across the book."""
import re
from pathlib import Path

BOOK_ROOT = Path(r"E:\Projects\LLMCourse")
SKIP = {"vendor", "node_modules", ".git", "deprecated", "__pycache__", "templates"}

# Mapping: old broken href pattern -> replacement
REPLACEMENTS = [
    # module-26-production-safety-ethics was renamed to module-27-safety-ethics-regulation
    (
        "part-7-production-strategy/module-26-production-safety-ethics/index.html",
        "part-7-production-strategy/module-27-safety-ethics-regulation/index.html",
    ),
    (
        "part-7-production-strategy/module-26-production-safety-ethics/section-26.1.html",
        "part-7-production-strategy/module-27-safety-ethics-regulation/section-27.1.html",
    ),
    (
        "part-7-production-strategy/module-26-production-safety-ethics/section-26.3.html",
        "part-7-production-strategy/module-27-safety-ethics-regulation/section-27.3.html",
    ),
    (
        "part-7-production-strategy/module-26-production-safety-ethics/section-26.8.html",
        "part-7-production-strategy/module-27-safety-ethics-regulation/section-27.7.html",
    ),
    # module-13-synthetic-data is in part-4, not part-3
    (
        "part-3-working-with-llms/module-13-synthetic-data/index.html",
        "part-4-training-adapting/module-13-synthetic-data/index.html",
    ),
]


def find_html_files():
    for f in BOOK_ROOT.rglob("*.html"):
        if not any(s in f.parts for s in SKIP):
            yield f


def fix_file(filepath):
    html = filepath.read_text(encoding="utf-8", errors="replace")
    original = html
    changes = []

    for old, new in REPLACEMENTS:
        if old in html:
            html = html.replace(old, new)
            changes.append(f"  {old} -> {new}")

    # Fix section-8.5 sibling link to module-09 (wrong relative path)
    if "module-08" in str(filepath):
        bad = '../module-09-llm-apis/index.html'
        good = '../../part-3-working-with-llms/module-09-llm-apis/index.html'
        if bad in html:
            html = html.replace(bad, good)
            changes.append(f"  {bad} -> {good}")

    if html != original:
        filepath.write_text(html, encoding="utf-8")
        return changes
    return []


def main():
    total_files = 0
    total_fixes = 0

    for filepath in find_html_files():
        changes = fix_file(filepath)
        if changes:
            rel = filepath.relative_to(BOOK_ROOT)
            print(f"{rel}:")
            for c in changes:
                print(c)
            total_files += 1
            total_fixes += len(changes)

    print(f"\nFixed {total_fixes} broken links in {total_files} files.")

    # Note: appendix ../index.html links need appendices/index.html to be created
    print("\nNote: 9 appendix index pages link to ../index.html (appendices landing page).")
    print("These need an appendices/index.html file to be created.")


if __name__ == "__main__":
    main()
