"""v4.0: Add a book-wide 'as of 2026' note + targeted table footnotes.

  1. Add a one-paragraph editorial note in front-matter/about-book.html
     declaring the freshness assumption.
  2. Auto-add `(as of 2026)` after model-comparison table titles
     ('Comparison of X', 'X Models', etc.) where they're missing.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


def add_book_wide_note() -> None:
    p = ROOT / "front-matter/about-book.html"
    if not p.exists():
        print("  [skip] about-book.html missing")
        return
    text = p.read_text(encoding="utf-8", errors="replace")
    if "as of late 2025" in text:
        print("  [skip] book-wide date note already present")
        return
    # Insert after first <p> in <main>
    note = (
        '\n<aside class="callout note book-freshness">\n'
        '<div class="callout-title">A note on freshness</div>\n'
        '<p>All model versions, benchmark scores, pricing, and API details '
        'referenced in this book reflect the state of the field as of late 2025 '
        'and early 2026 unless explicitly noted. The agentic-AI ecosystem moves '
        'fast; expect specific model identifiers (GPT-4o, Claude 3.5 Sonnet, '
        'o1/o3, Gemini 2.0, etc.) to be superseded within months. Concepts and '
        'patterns survive longer than version numbers.</p>\n'
        '</aside>\n'
    )
    text = re.sub(r'(<main[^>]*>(?:[^<]|<(?!p\s))*?<p[^>]*>[^<]*</p>\s*)',
                   r'\1' + note, text, count=1, flags=re.DOTALL)
    p.write_text(text, encoding="utf-8")
    print("  added book-wide freshness note to about-book.html")


def add_table_footnotes() -> None:
    """Add (as of 2026) suffix to comparison-table titles that lack a date."""
    n_files = 0
    n_added = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        try:
            if p.stat().st_size > 5_000_000: continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        original = text
        # Look for <div class="comparison-table-title">X</div> where X doesn't have a date
        def _add(m: re.Match) -> str:
            nonlocal n_added
            inner = m.group(1).strip()
            if any(kw in inner.lower() for kw in ("as of", "circa", "2025", "2026", "2024")):
                return m.group(0)
            n_added += 1
            return m.group(0).replace(inner, f"{inner} (as of 2026)")
        text = re.sub(
            r'<div\s+class="comparison-table-title"[^>]*>([^<]+)</div>',
            _add, text,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"  added 'as of 2026' to {n_added} comparison-table titles in {n_files} files")


def main() -> int:
    add_book_wide_note()
    add_table_footnotes()
    return 0


if __name__ == "__main__":
    sys.exit(main())
