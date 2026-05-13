"""Validate every $...$ and $$...$$ math block book-wide using KaTeX.

Why: the heuristic checker (_v653) only catches a small known-bad pattern
class. KaTeX itself is the ground truth: if KaTeX cannot render a block,
it is broken regardless of whether our regex catches it.

Strategy: extract every math block from every shipped HTML file, hand it
to the `katex` Python wrapper (which calls the JS KaTeX renderer), and
report parser errors with file:line context.

Idempotent. Exit code 1 if any defect found.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

import katex

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/')

# Capture both display ($$...$$) and inline ($...$). Avoid pricing prose
# like '$5' by requiring at least one LaTeX-ish glyph.
DISPLAY_PATTERN = re.compile(r'\$\$([\s\S]+?)\$\$')
INLINE_PATTERN = re.compile(r'(?<!\$)\$([^$\n]{2,200}?)\$(?!\$)')


def is_likely_math(s: str) -> bool:
    """Heuristic to skip non-math dollars (currency, etc.)."""
    if '\\' in s:
        return True
    if any(c in s for c in '_^{}'):
        return True
    return False


def validate_block(expr: str, display: bool) -> str | None:
    """Return error message if KaTeX fails, else None."""
    # Decode common HTML entities that browsers handle for us
    expr_decoded = (expr.replace('&amp;', '&')
                       .replace('&lt;', '<')
                       .replace('&gt;', '>')
                       .replace('&nbsp;', ' '))
    try:
        katex.render(expr_decoded, display_mode=display, throw_on_error=True)
        return None
    except Exception as e:
        msg = str(e).split('\n')[0][:200]
        return msg


def main() -> int:
    total_blocks = 0
    total_errors = 0
    error_files = set()
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue

        rel = p.relative_to(ROOT)
        local_errors = []

        # Display blocks
        for m in DISPLAY_PATTERN.finditer(text):
            expr = m.group(1).strip()
            if not is_likely_math(expr):
                continue
            total_blocks += 1
            err = validate_block(expr, display=True)
            if err:
                line = text[: m.start()].count('\n') + 1
                local_errors.append((line, 'display', err, expr[:80]))

        # Strip display blocks before scanning inline so $$...$$ doesn't
        # double-count. Use temp text where displays are blanked.
        text_no_display = DISPLAY_PATTERN.sub(lambda _: '', text)
        for m in INLINE_PATTERN.finditer(text_no_display):
            expr = m.group(1).strip()
            if not is_likely_math(expr):
                continue
            total_blocks += 1
            err = validate_block(expr, display=False)
            if err:
                line = text_no_display[: m.start()].count('\n') + 1
                local_errors.append((line, 'inline', err, expr[:80]))

        if local_errors:
            error_files.add(rel)
            for line, kind, err, snippet in sorted(local_errors):
                print(f'{rel}:{line} [{kind}] {err}')
                print(f'    expr: {snippet!r}')
                total_errors += 1

    print()
    print(f'Validated {total_blocks} math blocks. Errors: {total_errors} across {len(error_files)} file(s).')
    return 1 if total_errors else 0


if __name__ == '__main__':
    sys.exit(main())
