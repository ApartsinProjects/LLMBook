"""Rename 6 part titles to LLM/Agent-inclusive wording, book-wide.

Slug directories (`part-4-training-adapting/`, etc.) and filenames are
NOT renamed — URL stability matters. Only displayed text changes.

Decisions:
  Part 4:  Training and Adapting            -> LLM Training and Adaptation
  Part 5:  Retrieval and Conversation       -> Retrieval and Conversation with LLMs and Agents
  Part 8:  Evaluation and Production        -> Evaluation of LLM-Based Systems
  Part 9:  Safety, Security & Ethics        -> LLM Safety, Security, and Ethics
  Part 10: Idea to Product                  -> Building LLM and Agent Products
  Part 11: Applications Across Industries   -> LLM Applications Across Industries

The renamer walks every HTML/MD/YAML/JSON file (skipping vendor / build
artifacts / URL-bearing slugs) and rewrites the literal text in:
  <title>, meta description, h1, h2, page headings, breadcrumbs,
  pagefind-meta values, TOC entries, prose cross-references, alt text.

The `&amp;` HTML-encoded form for Part 9 is also handled.

Idempotent: re-runs find no old strings.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update", "vendor"}

# (old_text, new_text) pairs. Order matters: more-specific first.
RENAMES = [
    # Part 9 HTML-encoded form (must come BEFORE the plain-text form
    # to avoid double-rewrite via the plain form's substring match).
    ("Safety, Security &amp; Ethics", "LLM Safety, Security, and Ethics"),
    ("Safety, Security & Ethics", "LLM Safety, Security, and Ethics"),
    # Part 4
    ("Training and Adapting", "LLM Training and Adaptation"),
    # Part 5
    ("Retrieval and Conversation", "Retrieval and Conversation with LLMs and Agents"),
    # Part 8
    ("Evaluation and Production", "Evaluation of LLM-Based Systems"),
    # Part 10
    ("Idea to Product", "Building LLM and Agent Products"),
    # Part 11
    ("Applications Across Industries", "LLM Applications Across Industries"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    counts: dict[str, int] = {old: 0 for old, _ in RENAMES}
    files_edited = 0
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        if set(p.parts) & SKIP_PARTS:
            continue
        if p.suffix not in (".html", ".md", ".yaml", ".yml", ".json"):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        orig = text
        for old, new in RENAMES:
            if old in text:
                n = text.count(old)
                text = text.replace(old, new)
                counts[old] += n
        if text != orig:
            files_edited += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Files edited: {files_edited}")
    print("Per-rename counts:")
    for old, _ in RENAMES:
        print(f"  {counts[old]:5d}  {old!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
