"""Find and fix callouts trapped inside <header class="chapter-header">.

Pattern (broken):
    <header class="chapter-header">
        ...
        <h1>Title</h1>
        <aside class="callout ...">...</aside>    <-- BUG: inside header
    </header>
    <main>...

Fix: move every <aside class="callout ..."> block that appears AFTER
<h1>...</h1> but BEFORE </header> into the start of <main>, right
after the pagefind-meta-injected spans.

Idempotent: only moves if the callout is actually inside the header.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

HEADER_RE = re.compile(
    r'(<header\s+class="chapter-header">)([\s\S]*?)(</header>)',
    re.IGNORECASE)
# Strict aside-callout match: <aside class="callout..."> ... </aside>
# The closing tag must be </aside>, not </div>.
ASIDE_CALLOUT_RE = re.compile(
    r'<aside\s+class="callout[^"]*"[^>]*>[\s\S]*?</aside>',
    re.IGNORECASE)
H1_RE = re.compile(r'<h1[^>]*>[\s\S]*?</h1>', re.IGNORECASE)
MAIN_INSERT_RE = re.compile(
    r'(<main[^>]*>(?:\s*<span[^>]*>[^<]*</span>)*)',
    re.IGNORECASE)


def main() -> int:
    fix = '--fix' in sys.argv
    files_touched = 0
    callouts_moved = 0
    affected_files: list[str] = []
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if 'chapter-header' not in text or 'aside' not in text:
            continue

        hm = HEADER_RE.search(text)
        if not hm:
            continue
        header_open, header_inner, header_close = hm.group(1), hm.group(2), hm.group(3)
        h1m = H1_RE.search(header_inner)
        if not h1m:
            continue
        after_h1 = header_inner[h1m.end():]
        callouts = ASIDE_CALLOUT_RE.findall(after_h1)
        if not callouts:
            continue

        # Remove callouts from after_h1
        new_after_h1 = ASIDE_CALLOUT_RE.sub('', after_h1)
        # Normalize trailing whitespace
        new_after_h1 = re.sub(r'\n\s*\n+', '\n', new_after_h1).rstrip() + '\n'
        new_header_inner = header_inner[:h1m.end()] + '\n' + new_after_h1
        new_header = f'{header_open}{new_header_inner}{header_close}'

        # Insert callouts after <main> + pagefind spans
        new_text = text.replace(hm.group(0), new_header, 1)
        m2 = MAIN_INSERT_RE.search(new_text)
        if not m2:
            continue
        ins = m2.end()
        moved_block = '\n' + '\n'.join(callouts) + '\n'
        new_text = new_text[:ins] + moved_block + new_text[ins:]

        files_touched += 1
        callouts_moved += len(callouts)
        affected_files.append(str(p.relative_to(ROOT)))
        if fix and new_text != text:
            p.write_text(new_text, encoding='utf-8')

    mode = 'APPLIED' if fix else 'DRY-RUN'
    print(f'[{mode}] Files touched: {files_touched}')
    print(f'        Callouts moved out of <header>: {callouts_moved}')
    for f in affected_files:
        print(f'  - {f}')
    if not fix:
        print('\nRe-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
