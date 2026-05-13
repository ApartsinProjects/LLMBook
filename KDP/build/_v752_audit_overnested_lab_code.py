"""Detect Python code blocks where code that should be top-level has
been over-indented INTO a preceding function body.

Pattern (broken):
    def func(args):
        body
        return X
        # TODO comment        <-- now inside the function (unreachable)
        for x in items:        <-- inside function, but logically top-level
            X, y = [], []      <-- 1 level too deep
            for y in others:   <-- 2 levels too deep
                ...            <-- 3 levels too deep (and so on)

Signature: lines AFTER a `return X` (at indent N+4) at indent N+4 or
deeper, where the indent grows monotonically as block openers (for/if)
are added. The right Python would have the post-return code at indent
N (top-level).

This is the opposite of the v740/v741 flat-methods bug. Where flat-
methods had `def` at col 0 incorrectly, over-nest has top-level code
at col 4+ incorrectly.

Report-only.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

BLOCK_RE = re.compile(
    r'<pre[^>]*>\s*<code\s+class="[^"]*lang-python[^"]*">([\s\S]*?)</code>\s*</pre>',
    re.IGNORECASE)
SPAN_RE = re.compile(r'<span[^>]*>|</span>')
import html as _html


def extract_code(body: str) -> str:
    return _html.unescape(SPAN_RE.sub('', body))


def detect_overnest(code: str) -> int:
    """Return count of "post-return overnested" structures."""
    lines = code.split('\n')
    found = 0
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = re.match(r'^(\s*)def\s+\w+', line)
        if not m:
            i += 1
            continue
        def_indent = len(m.group(1))
        body_indent = def_indent + 4
        # Find the function's return statement at body_indent
        j = i + 1
        return_found = False
        while j < n:
            ln = lines[j]
            if not ln.strip():
                j += 1
                continue
            stripped_indent = len(ln) - len(ln.lstrip())
            if stripped_indent <= def_indent and ln.strip():
                # Function ended naturally
                break
            if re.match(r'^\s+return\s', ln) and stripped_indent == body_indent:
                return_found = True
                j += 1
                break
            j += 1
        if not return_found:
            i = j
            continue
        # Now look at lines after the return at body_indent or deeper
        # that show monotonic over-nesting. Specifically, find a `for`
        # or `if` at indent body_indent followed by content at
        # body_indent+4 followed by another `for`/`if` at body_indent+4
        # followed by content at body_indent+8. That cascade is the
        # signature.
        k = j
        deep_count = 0
        while k < n:
            ln = lines[k]
            if not ln.strip():
                k += 1
                continue
            stripped_indent = len(ln) - len(ln.lstrip())
            if stripped_indent <= def_indent and ln.strip():
                # We left the function scope; stop.
                break
            if stripped_indent >= body_indent + 8:
                deep_count += 1
            k += 1
        if deep_count >= 3:
            found += 1
        i = k if k > i else i + 1
    return found


def main() -> int:
    affected: list[tuple[str, int]] = []
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if 'lang-python' not in text:
            continue
        total = 0
        for m in BLOCK_RE.finditer(text):
            code = extract_code(m.group(1))
            total += detect_overnest(code)
        if total:
            affected.append((str(p.relative_to(ROOT)), total))

    print(f'Files with over-nested lab/script code: {len(affected)}')
    print(f'Suspect blocks total: {sum(n for _, n in affected)}')
    print()
    for f, n in sorted(affected, key=lambda kv: -kv[1])[:50]:
        print(f'  {n:3d}  {f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
