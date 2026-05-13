"""Audit unescaped $ characters in prose that KaTeX auto-render will
interpret as inline math delimiters, mangling the text between them.

Pattern: a literal $ sign next to a digit (e.g., $50, $1.2B, $90,000)
that is NOT preceded by a backslash, AND not inside a math context.

Two failure modes:
  D1 (HIGH-IMPACT): pairs of unescaped $ around prose containing letters;
      everything between is rendered as math (italic single-letter vars,
      no spaces, no readability).
  D2 (LOW-IMPACT): single unescaped $ at the end of a paragraph; KaTeX
      may or may not pair it with another $ later in the doc.

Reports per-file findings.

The fix: replace `$50` with `\\$50`, or with `&dollar;50`, or with
$50</code> wrapping in <code>...</code> if it's not prose.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

# A $ followed by a digit, not preceded by a backslash
DOLLAR_AMOUNT = re.compile(r'(?<!\\)(?<!\$)\$(\d[\d,]*\.?\d*[KMB]?)')


def main() -> int:
    n_files = 0
    n_dollars = 0
    by_file: dict[str, list[tuple[int, str]]] = {}
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        # Strip protected zones: <script>, <style>, <pre>, <code>,
        # <table> headers that already use $ for currency in raw text...
        # but we keep prose context.
        text_scan = re.sub(r'<script\b[\s\S]*?</script>', ' ', text,
                           flags=re.IGNORECASE)
        text_scan = re.sub(r'<style\b[\s\S]*?</style>', ' ', text_scan,
                           flags=re.IGNORECASE)
        text_scan = re.sub(r'<pre\b[\s\S]*?</pre>', ' ', text_scan,
                           flags=re.IGNORECASE)
        text_scan = re.sub(r'<code\b[\s\S]*?</code>', ' ', text_scan,
                           flags=re.IGNORECASE)
        # Don't double-count $$display math$$ blocks
        text_scan = re.sub(r'\$\$[\s\S]*?\$\$', ' ', text_scan)

        file_hits: list[tuple[int, str]] = []
        for m in DOLLAR_AMOUNT.finditer(text_scan):
            line = text_scan.count('\n', 0, m.start()) + 1
            file_hits.append((line, f'${m.group(1)}'))
        if file_hits:
            n_files += 1
            n_dollars += len(file_hits)
            by_file[str(p.relative_to(ROOT))] = file_hits
    print(f'Files with unescaped $-amounts in prose: {n_files}')
    print(f'Total occurrences: {n_dollars}')
    for fp in sorted(by_file.keys()):
        hits = by_file[fp]
        print(f'\n{fp}: {len(hits)} occurrences')
        for line, amount in hits[:10]:
            print(f'  L{line:<5} {amount}')
        if len(hits) > 10:
            print(f'  ... and {len(hits)-10} more')
    return 0


if __name__ == '__main__':
    sys.exit(main())
