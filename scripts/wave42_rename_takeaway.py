"""Wave 42: rename non-canonical class='callout takeaway' to canonical
class='callout key-takeaway' across the book.

The audit's CANONICAL_TYPES expects 'key-takeaway'. Some early sections used
the shorter 'takeaway'. Rename in place.
"""
from pathlib import Path

REPO_ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

count = 0
for fp in REPO_ROOT.rglob("section-*.html"):
    text = fp.read_text(encoding="utf-8")
    if 'class="callout takeaway"' not in text:
        continue
    new = text.replace('class="callout takeaway"', 'class="callout key-takeaway"')
    if new != text:
        fp.write_text(new, encoding="utf-8")
        count += 1

print(f"Renamed in {count} files")
