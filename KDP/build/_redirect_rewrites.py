"""One-shot script: rewrite cross-references from deleted sections to their
canonical replacements, then delete the duplicate/stub source files.

Run from project root:
    /c/Python314/python KDP/build/_redirect_rewrites.py

Idempotent — safe to re-run.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # project root

# Mapping: deleted section -> canonical replacement
# Format: (old_basename, new_basename, new_chapter_dir_relative_to_part)
REWRITES = [
    # Stubs (already self-redirect to these)
    ("section-29.5", "section-30.1", "module-30-observability-monitoring"),
    ("section-29.7", "section-30.3", "module-30-observability-monitoring"),
    # Real duplicates
    ("section-22.2", "section-22.7", "module-22-ai-agents"),       # Agent Memory dup -> larger
    ("section-29.8", "section-30.4", "module-30-observability-monitoring"),  # Arena-style dup
    ("section-35.7", "section-22.7", "module-22-ai-agents"),       # Agent memory misplaced in 35
]

# Files to delete
DELETE_FILES = [
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.5.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.7.html",
    "part-6-agentic-ai/module-22-ai-agents/section-22.2.html",
    "part-8-evaluation-production/module-29-evaluation-observability/section-29.8.html",
    "part-10-frontiers/module-35-ai-society/section-35.7.html",
]

EXCLUDE_DIRS = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


def relink(text: str, old: str, new: str) -> tuple[str, int]:
    """Replace href values that point to old.html with new.html.

    Matches:
        href="...section-22.2.html"
        href="...section-22.2.html#anchor"
        ../module-22-ai-agents/section-22.2.html
    Anchors and query strings preserved.
    """
    # href="...section-XX.Y.html..." (any path prefix)
    pattern = re.compile(rf'((?:href|src)="[^"]*?){re.escape(old)}\.html')
    new_text, n = pattern.subn(rf'\1{new}.html', text)
    return new_text, n


def main() -> int:
    n_files_changed = 0
    n_links_rewritten = 0

    # Walk all HTML in source (NOT in KDP/, _archive/, etc.)
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE_DIRS):
            continue
        # Skip the files we're about to delete (no point rewriting them)
        rel = p.relative_to(ROOT).as_posix()
        if rel in DELETE_FILES:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        original = text
        chapter_total = 0
        for old, new, _new_dir in REWRITES:
            text, n = relink(text, old, new)
            chapter_total += n
        if chapter_total > 0:
            p.write_text(text, encoding="utf-8")
            n_files_changed += 1
            n_links_rewritten += chapter_total
            print(f"  {chapter_total:>3}x  {rel}")

    print(f"\nRewrote {n_links_rewritten} links across {n_files_changed} files")

    # Delete the source files
    print("\nDeleting duplicate/stub source files:")
    for rel in DELETE_FILES:
        p = ROOT / rel
        if p.exists():
            p.unlink()
            print(f"  rm {rel}")
        else:
            print(f"  (already gone) {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
