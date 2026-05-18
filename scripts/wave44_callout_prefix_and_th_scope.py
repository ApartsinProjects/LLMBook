"""Wave 44: Two mechanical sweeps.

1. PSEUDO_CALLOUT residual: add "callout " prefix to bare <div class="lab"> /
   <div class="exercise"> so they become <div class="callout lab"> /
   <div class="callout exercise"> as per canonical form. (47 + 4 issues.)

2. MISSING_TH_SCOPE: add scope="col" to bare <th> cells in the first <tr>
   of a table (header row). 53 issues.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'source_fix_backups',
        'pagefind', '.book-update', 'vendor', '.claude', '_archive',
        'agents', 'templates', 'docs', 'scripts'}

# --- Sweep 1: callout prefix ---
# Match <div class="lab"> or <div class="exercise"> (bare, no "callout " prefix)
BARE_CALLOUT_RE = re.compile(
    r'<div\s+class="(lab|exercise)"([^>]*)>',
    re.IGNORECASE,
)

# --- Sweep 2: th scope ---
# We need to find <table>...<thead><tr><th>...</th>...</tr></thead>...</table>
# OR <table>...<tr><th>...</th>...</tr>... (first tr is header)
# And add scope="col" to any <th> in that header row that doesn't have scope.
TABLE_RE = re.compile(r'<table\b[^>]*>(.*?)</table>', re.DOTALL | re.IGNORECASE)
THEAD_RE = re.compile(r'<thead\b[^>]*>(.*?)</thead>', re.DOTALL | re.IGNORECASE)
TR_RE = re.compile(r'<tr\b[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
TH_TAG_RE = re.compile(r'<th\b([^>]*)>', re.IGNORECASE)


def fix_callout_prefix(text: str) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        cls = m.group(1)
        rest = m.group(2)
        return f'<div class="callout {cls}"{rest}>'

    return BARE_CALLOUT_RE.sub(repl, text), n


def fix_th_scope_in_header(header_tr_inner: str) -> tuple[str, int]:
    """Add scope='col' to every <th> in this header row that lacks it."""
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        attrs = m.group(1)
        if 'scope=' in attrs.lower():
            return m.group()
        n += 1
        return f'<th scope="col"{attrs}>'

    return TH_TAG_RE.sub(repl, header_tr_inner), n


def fix_th_scope(text: str) -> tuple[str, int]:
    total = 0

    def replace_table(m: re.Match) -> str:
        nonlocal total
        inner = m.group(1)
        # If there's a <thead>, fix all <th> inside the first <tr> of thead
        thead_m = THEAD_RE.search(inner)
        if thead_m:
            thead_inner = thead_m.group(1)
            tr_m = TR_RE.search(thead_inner)
            if tr_m:
                old_tr = tr_m.group()
                new_tr_inner, n = fix_th_scope_in_header(tr_m.group(1))
                if n > 0:
                    total += n
                    new_thead_inner = (
                        thead_inner[:tr_m.start()]
                        + f'<tr>{new_tr_inner}</tr>'
                        + thead_inner[tr_m.end():]
                    )
                    new_inner = (
                        inner[:thead_m.start()]
                        + f'<thead>{new_thead_inner}</thead>'
                        + inner[thead_m.end():]
                    )
                    return m.group().replace(inner, new_inner, 1)
            return m.group()
        # No thead — first <tr> is header if it contains only <th>
        tr_m = TR_RE.search(inner)
        if tr_m:
            tr_inner = tr_m.group(1)
            if re.search(r'<th\b', tr_inner, re.IGNORECASE) and not re.search(r'<td\b', tr_inner, re.IGNORECASE):
                new_tr_inner, n = fix_th_scope_in_header(tr_inner)
                if n > 0:
                    total += n
                    new_inner = (
                        inner[:tr_m.start()]
                        + f'<tr>{new_tr_inner}</tr>'
                        + inner[tr_m.end():]
                    )
                    return m.group().replace(inner, new_inner, 1)
        return m.group()

    new_text = TABLE_RE.sub(replace_table, text)
    return new_text, total


def main():
    n_callout = 0
    n_scope = 0
    files_callout = 0
    files_scope = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        text, c1 = fix_callout_prefix(text)
        text, c2 = fix_th_scope(text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            if c1: files_callout += 1
            if c2: files_scope += 1
            n_callout += c1
            n_scope += c2
    print(f'Bare callouts prefixed: {n_callout} across {files_callout} files')
    print(f'<th> scope added: {n_scope} across {files_scope} files')


if __name__ == '__main__':
    main()
