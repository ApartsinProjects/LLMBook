#!/usr/bin/env python3
"""Consolidate anecdote callouts to fun-note.

Replaces:
    <div class="callout anecdote">
with:
    <div class="callout fun-note">

Anecdote has no CSS styling; fun-note serves the same purpose
(lighthearted, memorable stories) with proper pink/magenta theme.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP_DIRS = {".git", "node_modules", "__pycache__", "_archive", "agents", "vendor"}


def main():
    fixed = 0
    for html_file in sorted(ROOT.rglob("*.html")):
        if any(s in html_file.parts for s in SKIP_DIRS):
            continue
        text = html_file.read_text(encoding="utf-8")
        if 'callout anecdote' not in text:
            continue
        new_text = text.replace(
            'class="callout anecdote"', 'class="callout fun-note"'
        )
        if new_text != text:
            html_file.write_text(new_text, encoding="utf-8")
            rel = html_file.relative_to(ROOT)
            print(f"Fixed: {rel}")
            fixed += 1

    print(f"\nConsolidated {fixed} files (anecdote -> fun-note)")


if __name__ == "__main__":
    main()
