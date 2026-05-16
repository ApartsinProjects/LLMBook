"""Standardize tables book-wide.

Per the table-class audit, the book has:
- 223 tables with `class="complex-table"` (the dominant standard)
- 147 tables with no class (inherit global <table> rule, render the same)
- 12 tables with `class="data-table"` (4-sided grid borders — non-standard look)
- 11 tables with `class="psk-table"` (appendix problem-solution key — leave alone)
- 5 tables with `class="comparison-table"` (intentional gradient-title look — leave)

The audit also flagged:
- 2 tables with inline `style="..."` overrides — strip
- 1 table caption mislabeled `Figure 27.2.2 (Table)` — fix to `Table N.N.N`
- Several captions in section-28.12 say `Table 27.14.x` (wrong module)
- Several captions in section-29.9 say `Table 28.9.x` (wrong module)

This script:
  1. Converts every `class="data-table"` to `class="complex-table"`.
  2. Strips inline style="" attrs from those 12 converted tables.
  3. Fixes the `Figure 27.2.2 (Table)` mislabel to `Table 27.2.2`.
  4. Re-numbers section-28.12 captions from `Table 27.14.X` → `Table 28.12.X`.
  5. Re-numbers section-29.9 captions from `Table 28.9.X` → `Table 29.9.X`.

Idempotent. Skip KDP / .claude / build / temp_*.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}


def convert_datatable_to_complex(soup) -> int:
    """Change every <table class="data-table"> to class="complex-table".
    Also strip any inline style="" attribute on those tables."""
    n = 0
    for t in soup.find_all("table"):
        cls = t.get("class") or []
        if "data-table" in cls:
            new_cls = ["complex-table" if c == "data-table" else c for c in cls]
            # Remove duplicates while preserving order
            seen = set()
            final = []
            for c in new_cls:
                if c not in seen:
                    seen.add(c)
                    final.append(c)
            t["class"] = final
            if t.has_attr("style"):
                del t["style"]
            n += 1
    return n


def fix_figure_table_mislabel(text: str) -> tuple[str, int]:
    """Replace `Figure N.N.N (Table)` with `Table N.N.N`."""
    pat = re.compile(r"<strong>Figure\s+([\d.]+)\s*\(Table\)</strong>")
    new = pat.sub(r"<strong>Table \1</strong>", text)
    n = len(pat.findall(text))
    return new, n


def renumber_table_captions(text: str, from_prefix: str, to_prefix: str) -> tuple[str, int]:
    """Replace `Table <from_prefix>X` with `Table <to_prefix>X` inside table
    captions and table references. Conservative: only matches inside <caption>
    or after the literal token "Table " followed by the prefix."""
    pat = re.compile(rf"(\bTable\s+){re.escape(from_prefix)}(\d+)\b")
    n = len(pat.findall(text))
    new = pat.sub(rf"\g<1>{to_prefix}\g<2>", text)
    return new, n


def process_file(p: Path, dry_run: bool) -> tuple[int, list[str]]:
    text = p.read_text(encoding="utf-8")
    orig = text
    msgs: list[str] = []

    # Class conversion via BeautifulSoup
    if 'class="data-table"' in text or "class='data-table'" in text:
        soup = BeautifulSoup(text, "html.parser")
        n_cls = convert_datatable_to_complex(soup)
        if n_cls:
            text = str(soup)
            msgs.append(f"  converted {n_cls} data-table → complex-table")

    # Caption fixes via regex on raw HTML
    text, n_mis = fix_figure_table_mislabel(text)
    if n_mis:
        msgs.append(f"  fixed {n_mis} 'Figure N.N.N (Table)' → 'Table N.N.N'")

    # Section-28.12 mis-numbered captions
    if "section-28.12.html" in p.as_posix():
        text, n_re = renumber_table_captions(text, "27.14.", "28.12.")
        if n_re:
            msgs.append(f"  renumbered {n_re} 'Table 27.14.X' → 'Table 28.12.X'")

    # Section-29.9 mis-numbered captions
    if "section-29.9.html" in p.as_posix():
        text, n_re = renumber_table_captions(text, "28.9.", "29.9.")
        if n_re:
            msgs.append(f"  renumbered {n_re} 'Table 28.9.X' → 'Table 29.9.X'")

    if text == orig:
        return 0, []
    if not dry_run:
        p.write_text(text, encoding="utf-8")
    return len(msgs), msgs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total_files = 0
    total_msgs = 0
    for p in sorted(ROOT.rglob("*.html")):
        if set(p.parts) & SKIP_PARTS:
            continue
        n, msgs = process_file(p, args.dry_run)
        if n:
            total_files += 1
            total_msgs += n
            print(f"{p.relative_to(ROOT)}:")
            for m in msgs:
                print(m)
    print(f"\nTOTAL: {total_msgs} edits across {total_files} files")
    if args.dry_run:
        print("(dry run; nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
