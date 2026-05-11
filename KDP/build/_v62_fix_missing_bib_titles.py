"""v6.2 follow-up: insert missing bibliography inner-title element.

Audit: 39 of 198 bibliographies lack the
  <div class="bibliography-title">References &amp; Further Reading</div>
element that the other 159 have. The user reported this as "empty
bibliography" in section-28.4 — the issue is that without the inner
title, the collapsible opens to a bare list and looks unfinished.

Fix: insert the canonical inner-title element immediately after
<section class="bibliography"> opens, in every affected file.

Idempotent: skips files that already have the inner title.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = {'agents', 'KDP', 'node_modules', 'scripts', '.git',
        'chapter_review', 'downloads', '_archive', '_lab_fragments',
        'templates'}

CANONICAL = '<div class="bibliography-title">References &amp; Further Reading</div>'

# Match: <details ... bibliography-collapsible ...> ... <section ... bibliography ...>
# We want to insert the inner title RIGHT AFTER <section class="bibliography">
# (or after the closing > of that tag, inside the section)
INSERT_PAT = re.compile(
    r'(<details[^>]*class="bibliography-collapsible"[^>]*>'
    r'(?:.|\n)*?'
    r'<section[^>]*class="bibliography"[^>]*>)\s*'
    r'(?!<div class="bibliography-title">)',
    re.IGNORECASE,
)


def fix(p: Path) -> bool:
    text = p.read_text(encoding='utf-8', errors='replace')
    if '<details' not in text or 'bibliography-collapsible' not in text:
        return False

    # Quick check: does it already have the inner title?
    # Find each bibliography-collapsible details block and check
    edits = []
    for m in re.finditer(
        r'<details[^>]*class="bibliography-collapsible"[^>]*>(.*?)</details>',
        text, re.DOTALL,
    ):
        body = m.group(1)
        if '<div class="bibliography-title">' in body:
            continue  # already has inner title
        # Find <section class="bibliography"> within this body
        sec_m = re.search(r'<section[^>]*class="bibliography"[^>]*>', body)
        if not sec_m:
            continue
        # m.start(1) is the absolute start of the body (right after the
        # <details ...> opening tag). sec_m.end() is the offset of the
        # closing > of <section> WITHIN the body. So absolute insert
        # position = m.start(1) + sec_m.end().
        insert_at = m.start(1) + sec_m.end()
        edits.append(insert_at)

    if not edits:
        return False

    # Apply in reverse to preserve offsets
    edits.sort(reverse=True)
    new_text = text
    for off in edits:
        new_text = new_text[:off] + '\n' + CANONICAL + new_text[off:]

    p.write_text(new_text, encoding='utf-8')
    return True


def main() -> int:
    fixed = 0
    for p in sorted(ROOT.rglob('*.html')):
        rel = p.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP:
            continue
        if fix(p):
            fixed += 1
            print(f'  + {rel}')
    print(f'\nInserted inner-title in {fixed} files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
