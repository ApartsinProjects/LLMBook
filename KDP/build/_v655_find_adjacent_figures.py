"""Detect figure-stacking defects: two figures back-to-back with no prose.

Why: section-17.3.html shipped two <figure class="illustration"> blocks
adjacent with no intervening prose / heading / callout / list. The
second image (metadata-filtering-bouncer) belongs deeper in the section
where metadata filtering is actually discussed, but the illustration-
insertion script batched it next to the chapter opener instead.

This script flags every place in the book where two <figure> or
<div class="diagram-container"> blocks are separated by only whitespace,
indicating the second one is mis-placed and probably belongs deeper in
the section.

Idempotent. Exit code 1 if any defect found.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

# Pattern: a closing </figure> or </div> (diagram-container) followed by
# only whitespace and then an opening <figure or <div class="diagram-
# container". Means there is NO prose (<p>, <h2>, <h3>, <ul>, <div
# class="callout">, <table>) between them.
ADJACENT_PATTERN = re.compile(
    r'(?:</figure>|<!-- end diagram -->\s*</div>)\s*\n\s*'
    r'(?:<figure[^>]*>|<div class="diagram-container">)',
    re.MULTILINE,
)

# Simpler version that catches both orderings
SIMPLE_FIG_FIG = re.compile(
    r'</figure>\s*\n\s*<figure',
    re.MULTILINE,
)
SIMPLE_DIAG_DIAG = re.compile(
    r'</div>\s*\n\s*<div class="diagram-container">',
    re.MULTILINE,
)


def main() -> int:
    total_defects = 0
    files_with_defects = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue

        rel = p.relative_to(ROOT)
        local = []

        for m in SIMPLE_FIG_FIG.finditer(text):
            line = text[: m.start()].count('\n') + 1
            local.append((line, 'figure-figure', 'two <figure> blocks back-to-back'))

        # Catch </figure> followed by <div class="diagram-container">
        for m in re.finditer(r'</figure>\s*\n\s*<div class="diagram-container">', text):
            line = text[: m.start()].count('\n') + 1
            local.append((line, 'figure-diagram', '<figure> immediately followed by <div diagram>'))

        # Catch </div diagram> followed by <figure>
        for m in re.finditer(r'</div>\s*\n\s*<figure', text):
            line = text[: m.start()].count('\n') + 1
            # Only count if the closing div is a diagram-container.
            # Look back ~200 chars for the matching open.
            head = text[max(0, m.start() - 500): m.start()]
            if 'diagram-container' in head and head.rfind('diagram-container') > head.rfind('</div>'):
                local.append((line, 'diagram-figure', '<div diagram> immediately followed by <figure>'))

        if local:
            files_with_defects += 1
            for line, kind, msg in sorted(local):
                print(f'{rel}:{line}  [{kind}] {msg}')
                total_defects += 1

    print()
    print(f'Found {total_defects} adjacent-figure defect(s) across {files_with_defects} file(s).')
    return 1 if total_defects else 0


if __name__ == '__main__':
    sys.exit(main())
