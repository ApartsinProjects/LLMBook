"""Detect malformed KaTeX/LaTeX patterns in book HTML.

Why: in section-16.1.html line 318 we shipped a `\\text{\\operatorname{clip}}`
construct that breaks KaTeX rendering (\\operatorname inside \\text is
invalid; \\operatorname already produces upright text). This script
guards against that and a handful of related regression classes so we
catch them before the next build.

Idempotent: produces a non-zero exit code if any defect is found, prints
file:line and the offending expression. Run as part of CI / pre-build.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

# Each rule: (pattern, label, hint)
RULES = [
    # \text{\operatorname{...}} or \text{\mathbb{...}}: nesting an upright-mode
    # macro inside \text{} is invalid KaTeX. \operatorname already produces
    # upright text; the outer \text{} should be removed.
    (
        re.compile(r'\\text\{\\(operatorname|mathbb|mathcal|mathrm|mathbf|mathit|mathsf|mathtt)\b'),
        'mis-nested upright macro',
        'remove the outer \\text{} since the inner macro is already upright',
    ),
    # \operatorname{\text{...}}: inverse mistake.
    (
        re.compile(r'\\operatorname\{\\text\b'),
        'inverse mis-nested upright macro',
        'use a single \\operatorname{name} or \\text{name}, not both',
    ),
    # Empty \text{}: usually a leftover artifact.
    (
        re.compile(r'\\text\{\s*\}'),
        'empty \\text{}',
        'remove the empty macro',
    ),
    # Unmatched \left or \right (very simple heuristic per math block).
    # We do this in a follow-up pass below so it can count both per block.
]


def check_balanced_left_right(text: str) -> list[tuple[int, str]]:
    """Find $$...$$ blocks where \\left count != \\right count."""
    findings = []
    # Iterate only over $$...$$ math blocks (display mode)
    for m in re.finditer(r'\$\$([\s\S]+?)\$\$', text):
        block = m.group(1)
        n_left = len(re.findall(r'\\left\b', block))
        n_right = len(re.findall(r'\\right\b', block))
        if n_left != n_right:
            line = text[: m.start()].count('\n') + 1
            findings.append((line, f'unbalanced \\left ({n_left}) vs \\right ({n_right})'))
    return findings


def main() -> int:
    total_defects = 0
    files_with_defects = 0
    for p in ROOT.rglob('*.html'):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue

        local = []
        for pat, label, hint in RULES:
            for m in pat.finditer(text):
                line = text[: m.start()].count('\n') + 1
                snippet = text[max(0, m.start() - 20) : m.end() + 30].replace('\n', ' ')
                local.append((line, f'{label}: ...{snippet}...  hint: {hint}'))

        for line, msg in check_balanced_left_right(text):
            local.append((line, msg))

        if local:
            files_with_defects += 1
            total_defects += len(local)
            rel = p.relative_to(ROOT)
            for line, msg in sorted(local):
                print(f'{rel}:{line}  {msg}')

    print()
    print(f'Found {total_defects} math defect(s) across {files_with_defects} file(s).')
    return 1 if total_defects else 0


if __name__ == '__main__':
    sys.exit(main())
