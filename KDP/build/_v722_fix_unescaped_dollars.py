"""Fix unescaped $-amounts in prose by replacing `$N` with `\\$N`.

The replacement runs ONLY in prose context. Protected zones (preserved
as-is):
  - <script>, <style>, <pre>, <code> blocks
  - $$...$$  display math blocks
  - $...$    inline math (rare but possible)

The fixer rewrites the file in-place. Idempotent: re-running on a
fixed file does nothing because `\\$N` no longer matches the `(?<!\\)$N`
pattern.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

DOLLAR_AMOUNT = re.compile(r'(?<!\\)(?<!\$)\$(\d[\d,]*\.?\d*[KMB]?)')


# Tokenizer that preserves protected zones unchanged
ZONE_PATTERNS = [
    (re.compile(r'<script\b[\s\S]*?</script>', re.IGNORECASE), 'script'),
    (re.compile(r'<style\b[\s\S]*?</style>', re.IGNORECASE), 'style'),
    (re.compile(r'<pre\b[\s\S]*?</pre>', re.IGNORECASE), 'pre'),
    (re.compile(r'<code\b[\s\S]*?</code>', re.IGNORECASE), 'code'),
    (re.compile(r'\$\$[\s\S]*?\$\$'), 'display-math'),
    # Inline math: only protect $...$ pairs whose body looks math-like
    # (starts with a backslash command or a known math token). This
    # avoids protecting prose between two prose-dollar amounts.
    (re.compile(r'(?<!\$)\$(?=\\[a-zA-Z]|[a-zA-Z]_|[a-zA-Z]\^)[^\$\n]{0,80}\$(?!\$)'),
     'inline-math'),
]


def split_into_zones(text: str) -> list[tuple[str, bool]]:
    """Return list of (chunk, is_protected). Protected chunks are NOT
    modified by the fixer."""
    # Find all protected spans in document order; weave with unprotected.
    spans: list[tuple[int, int]] = []
    for pat, _name in ZONE_PATTERNS:
        for m in pat.finditer(text):
            spans.append((m.start(), m.end()))
    # Resolve overlaps by keeping outermost.
    spans.sort()
    merged: list[tuple[int, int]] = []
    for s, e in spans:
        if merged and s < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    # Build chunks
    out: list[tuple[str, bool]] = []
    cur = 0
    for s, e in merged:
        if cur < s:
            out.append((text[cur:s], False))
        out.append((text[s:e], True))
        cur = e
    if cur < len(text):
        out.append((text[cur:], False))
    return out


def fix_prose(text: str) -> str:
    return DOLLAR_AMOUNT.sub(lambda m: '\\$' + m.group(1), text)


def main() -> int:
    fix = '--fix' in sys.argv
    n_files = 0
    n_fixes = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        zones = split_into_zones(text)
        new_parts: list[str] = []
        local = 0
        for chunk, protected in zones:
            if protected:
                new_parts.append(chunk)
            else:
                fixed = fix_prose(chunk)
                local += len(DOLLAR_AMOUNT.findall(chunk))
                new_parts.append(fixed)
        new_text = ''.join(new_parts)
        if local:
            n_files += 1
            n_fixes += local
            if fix and new_text != text:
                p.write_text(new_text, encoding='utf-8')

    print(f'Files {"fixed" if fix else "needing fix"}: {n_files}')
    print(f'Total $-amounts escaped: {n_fixes}')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
