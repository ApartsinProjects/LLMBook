"""9th edition follow-up: detect `<div class="lab">` (or class="lab ...")
blocks that never balance their closing </div>. The visual symptom is
that everything after the unclosed lab gets rendered nested inside the
lab box, including callouts, exercises, bibliography, and chapter-nav.

For each affected file, we report the line where the lab opened and the
line where the open-div counter passes the lab's closing point (or
"never closes" if the depth stays positive to end of file).

This is the same family of bug as v692/v703 (premature </main>) but for
inner block-level containers.

Read-only audit; reports per-file findings.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

DIV_OPEN = re.compile(r'<div\b', re.IGNORECASE)
DIV_CLOSE = re.compile(r'</div\s*>', re.IGNORECASE)
LAB_OPEN = re.compile(r'<div\s+class="lab(?:\s+[^"]*)?"[^>]*>', re.IGNORECASE)
# Also catch other commonly-misclosed container blocks
CALLOUT_OPEN = re.compile(r'<div\s+class="callout\b[^"]*"[^>]*>', re.IGNORECASE)


def audit_file(text: str, container_pat: re.Pattern, name: str
               ) -> list[tuple[int, int | None]]:
    """For each match of container_pat in text, return (open_line,
    close_line_or_None). close_line_or_None is None if the container
    never balances within the file."""
    results: list[tuple[int, int | None]] = []
    # Tokenize: list of (offset, kind) where kind in {'open', 'close',
    # 'container'}.
    events: list[tuple[int, str]] = []
    for m in DIV_OPEN.finditer(text):
        events.append((m.start(), 'open'))
    for m in DIV_CLOSE.finditer(text):
        events.append((m.start(), 'close'))
    container_starts = {m.start() for m in container_pat.finditer(text)}
    events.sort()

    # Walk events; whenever we hit a 'container' position (which is also
    # in 'open'), push a marker; track depth.
    stack: list[int] = []  # offsets of container opens still awaiting close
    depth = 0
    for off, kind in events:
        if kind == 'open':
            depth += 1
            if off in container_starts:
                stack.append((off, depth))  # remember depth-after-open
        else:  # close
            # If the top of our container-stack was at this depth, this
            # close balances it.
            if stack and stack[-1][1] == depth:
                open_off, _ = stack.pop()
                open_line = text.count('\n', 0, open_off) + 1
                close_line = text.count('\n', 0, off) + 1
                results.append((open_line, close_line))
            depth -= 1
    # Anything left on the stack never closed.
    for open_off, _ in stack:
        open_line = text.count('\n', 0, open_off) + 1
        results.append((open_line, None))
    return results


def main() -> int:
    n_files_bad = 0
    n_unclosed_total = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if '<div class="lab"' not in text and 'class="lab ' not in text:
            continue
        results = audit_file(text, LAB_OPEN, 'lab')
        unclosed = [r for r in results if r[1] is None]
        if unclosed:
            n_files_bad += 1
            n_unclosed_total += len(unclosed)
            for open_line, _ in unclosed:
                print(f'  {p.relative_to(ROOT)}:L{open_line} <div class="lab"> never closes')
    print(f'\nFiles with unclosed lab blocks: {n_files_bad}')
    print(f'Total unclosed lab openings: {n_unclosed_total}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
