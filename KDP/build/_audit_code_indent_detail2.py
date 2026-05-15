"""Audit: detailed code-block indent/formatting issues (v2).

For every <pre><code> block under part-*, appendices/, front-matter/, capstone/,
categorize indent / whitespace / width problems that show up VISUALLY in the
rendered HTML, even when the underlying code parses fine.

Categories
----------
1. UNIFORM_OVER_INDENT      every non-empty line starts with >=4 spaces, AND the
                            block has >=3 non-empty lines. Looks like the whole
                            chunk was indented as if inside a <pre> paragraph.
2. INCONSISTENT_INDENT      tabs mixed with spaces inside the block, OR the
                            structural indent step (smallest non-zero indent
                            ignoring 16+ continuation alignment) is not a clean
                            multiple of 2 or 4. Usually a paste artifact.
3. PYTHON_NO_BODY_INDENT    a line that ends with ':' opens a block but the
                            following body has at least one line at indent
                            <= opener's indent before the block closes.
4. LEADING_BLANK            >=1 blank line(s) at the top of the block.
5. TRAILING_BLANK           >=2 blank line(s) at the bottom of the block (one
                            terminating newline is normal and ignored).
6. WIDE_LINE                a line exceeds 80 characters of source (horizontal
                            scroll risk on Kindle).
7. BASH_VISUAL_MISALIGN     a bash continuation ( ends in '\\' ) followed by a
                            line whose indent is < the previous line's indent.

Outputs
-------
- AUDIT_code_indent.md       markdown table, human-readable
- AUDIT_code_indent.json     same data, structured for downstream scripts
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
OUT_MD = ROOT / 'KDP' / 'build' / 'AUDIT_code_indent.md'
OUT_JSON = ROOT / 'KDP' / 'build' / 'AUDIT_code_indent.json'

INCLUDE_PREFIXES = ('part-', 'appendices', 'front-matter', 'capstone')
SKIP_FRAGMENTS = (
    'node_modules', '.git', 'KDP/output', 'KDP/build', 'KDP/html2pub',
    'pagefind', 'temp_epub', 'backup', 'source_fix_backups',
    'scripts/_exercise_payloads', 'agents/', 'templates/'
)

WIDE_THRESHOLD = 80
# Indents >= this are treated as visual-alignment continuation (e.g. aligned
# to an opening paren), not as structural code indent. We exclude them when
# checking the indent-step heuristic.
CONTINUATION_INDENT_FLOOR = 16


def in_scope(rel: str) -> bool:
    rel = rel.replace('\\', '/')
    if any(s in rel for s in SKIP_FRAGMENTS):
        return False
    top = rel.split('/', 1)[0]
    return top.startswith(INCLUDE_PREFIXES)


def get_lang(code_tag) -> str:
    for c in code_tag.get('class', []) or []:
        if c.startswith('language-'):
            return c[9:]
        if c.startswith('lang-'):
            return c[5:]
    return ''


def find_line_no(html: str, pre_tag_str: str, search_start: int = 0,
                 fallback_needles: list[str] | None = None):
    """Approximate line number in the source file for a <pre> tag.

    Tries successively shorter prefixes; if all fail, falls back to a list of
    short needles (e.g. the first <span> inside the <code>).
    """
    for n in (200, 120, 80, 50, 30):
        needle = pre_tag_str[:n]
        if not needle:
            continue
        idx = html.find(needle, search_start)
        if idx >= 0:
            return html.count('\n', 0, idx) + 1, idx + len(needle)
    if fallback_needles:
        for needle in fallback_needles:
            if not needle or len(needle) < 12:
                continue
            idx = html.find(needle, search_start)
            if idx >= 0:
                return html.count('\n', 0, idx) + 1, idx + len(needle)
    return -1, search_start


def leading_ws(line: str) -> tuple[int, int]:
    spaces = 0
    tabs = 0
    for ch in line:
        if ch == ' ':
            spaces += 1
        elif ch == '\t':
            tabs += 1
        else:
            break
    return spaces, tabs


def analyze(text: str, lang: str) -> list[dict]:
    issues = []
    if not text:
        return issues
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')

    # Drop the final empty element from the trailing newline so it does not
    # skew counts.
    if lines and lines[-1] == '':
        body_lines = lines[:-1]
    else:
        body_lines = lines[:]

    non_empty_idx = [i for i, l in enumerate(body_lines) if l.strip()]
    non_empty = [body_lines[i] for i in non_empty_idx]
    if not non_empty:
        return issues

    # ----------------------------------------------------------------- blanks
    leading_blank = non_empty_idx[0] if non_empty_idx else 0
    if leading_blank >= 1:
        issues.append({
            'type': 'LEADING_BLANK',
            'detail': f'{leading_blank} blank line(s) at top',
        })
    trailing_blank = 0
    for l in reversed(body_lines):
        if l.strip():
            break
        trailing_blank += 1
    if trailing_blank >= 2 and leading_blank < len(body_lines):
        issues.append({
            'type': 'TRAILING_BLANK',
            'detail': f'{trailing_blank} blank line(s) at bottom',
        })

    # ----------------------------------------------------- indent measurement
    indents_spaces = []
    indents_tabs = []
    has_tab_indent = False
    has_space_indent = False
    for l in non_empty:
        sp, tb = leading_ws(l)
        indents_spaces.append(sp)
        indents_tabs.append(tb)
        if tb > 0:
            has_tab_indent = True
        if sp > 0 and tb == 0:
            has_space_indent = True

    # ------------------------------------------------------ UNIFORM_OVER_INDENT
    if len(non_empty) >= 3 and min(indents_spaces) >= 4 and not has_tab_indent:
        issues.append({
            'type': 'UNIFORM_OVER_INDENT',
            'detail': f'all {len(non_empty)} non-empty lines start with >='
                      f'{min(indents_spaces)} spaces',
        })

    # ---------------------------------------------------- INCONSISTENT_INDENT
    if has_tab_indent and has_space_indent:
        issues.append({
            'type': 'INCONSISTENT_INDENT',
            'detail': 'tabs and space indents mixed in same block',
        })
    else:
        # Look at "structural" indents only (skip large continuation-aligned
        # ones). We collect distinct non-zero indent widths below the
        # continuation floor and check they are multiples of 2 or 4.
        if lang in ('python', 'py') and len(non_empty) >= 4:
            structural = sorted({i for i in indents_spaces
                                 if 0 < i < CONTINUATION_INDENT_FLOOR})
            if structural:
                ok_2 = all(i % 2 == 0 for i in structural)
                ok_4 = all(i % 4 == 0 for i in structural)
                # 1-space indents are the classic "broken" case (Python wants 4
                # but the paste lost depth so only one space survived).
                if 1 in structural or (not ok_2 and not ok_4):
                    issues.append({
                        'type': 'INCONSISTENT_INDENT',
                        'detail': f'structural indent widths suspect: '
                                  f'{structural}',
                    })

    # ---------------------------------------------------- PYTHON_NO_BODY_INDENT
    # Two sub-checks for python:
    # (a) line ends with ':' (def/class/if/...) and the very next non-empty
    #     line is at <= the opener's indent.
    # (b) After an opener at indent N, ANY subsequent body line is at indent
    #     <= N before we hit a new opener at indent N -- this catches the
    #     "docstring indented but rest of body flat" pattern.
    if lang in ('python', 'py'):
        opener_re = re.compile(
            r'^\s*(def |class |if |elif |else\s*:|for |while |try\s*:|except|'
            r'with |finally\s*:|async def )'
        )
        for k, l in enumerate(non_empty):
            stripped = l.rstrip()
            if not stripped.endswith(':'):
                continue
            if not opener_re.match(l):
                continue
            if l.strip().startswith('#'):
                continue
            this_indent = indents_spaces[k] + indents_tabs[k] * 4
            if k + 1 >= len(non_empty):
                continue
            next_indent = indents_spaces[k + 1] + indents_tabs[k + 1] * 4
            if next_indent <= this_indent:
                issues.append({
                    'type': 'PYTHON_NO_BODY_INDENT',
                    'detail': f'line opens block but next line not indented '
                              f'({this_indent} -> {next_indent}); '
                              f'opener: {l.strip()[:60]!r}',
                })
                break
            # Look ahead for body-fall-out: scan body lines while they remain
            # part of this block (until we hit a line whose indent is <= this
            # opener's indent and which is NOT a continuation alignment).
            saw_indented_body = False
            for j in range(k + 1, len(non_empty)):
                ind_j = indents_spaces[j] + indents_tabs[j] * 4
                if ind_j > this_indent:
                    saw_indented_body = True
                    continue
                # ind_j <= this_indent: this line closes the body
                if saw_indented_body and ind_j == this_indent and \
                        opener_re.match(non_empty[j]):
                    # Sibling opener at same level -- legitimate end of block
                    pass
                elif saw_indented_body and ind_j < this_indent:
                    # Dedented below opener -- legitimate end of block
                    pass
                elif saw_indented_body and ind_j == this_indent and \
                        not opener_re.match(non_empty[j]):
                    # Body fell back to opener's indent without dedenting --
                    # this is the broken pattern.
                    issues.append({
                        'type': 'PYTHON_NO_BODY_INDENT',
                        'detail': f'body of opener {l.strip()[:40]!r} drops '
                                  f'to opener indent at line '
                                  f'{non_empty_idx[j] + 1}',
                    })
                break
            else:
                continue
            # one report per block is enough
            if any(it['type'] == 'PYTHON_NO_BODY_INDENT' for it in issues):
                break

    # --------------------------------------------------------------- WIDE_LINE
    over = [(i, len(l)) for i, l in enumerate(body_lines) if len(l) > WIDE_THRESHOLD]
    if over:
        max_len = max(o[1] for o in over)
        issues.append({
            'type': 'WIDE_LINE',
            'detail': f'{len(over)} line(s) > {WIDE_THRESHOLD} chars (max {max_len})',
        })

    # ----------------------------------------------------- BASH_VISUAL_MISALIGN
    if lang in ('bash', 'sh', 'shell', 'zsh', 'console', 'shell-session'):
        for k in range(len(body_lines) - 1):
            cur = body_lines[k]
            nxt = body_lines[k + 1]
            if not cur.rstrip().endswith('\\'):
                continue
            if not nxt.strip():
                continue
            cur_sp, _ = leading_ws(cur)
            nxt_sp, _ = leading_ws(nxt)
            if nxt_sp < cur_sp:
                issues.append({
                    'type': 'BASH_VISUAL_MISALIGN',
                    'detail': f'continuation line indent ({nxt_sp}) < '
                              f'previous line indent ({cur_sp})',
                })
                break

    return issues


def first_line(text: str, n: int = 80) -> str:
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    for l in text.split('\n'):
        if l.strip():
            return l[:n]
    return ''


# ---------------------------------------------------------------------- driver
results = []
counts = {}
n_blocks_total = 0
n_blocks_with_issues = 0
files_seen = set()
files_with_issues_counter: dict[str, int] = {}

for p in sorted(ROOT.rglob('*.html')):
    rel = str(p.relative_to(ROOT)).replace('\\', '/')
    if not in_scope(rel):
        continue
    try:
        raw = p.read_text(encoding='utf-8')
    except Exception:
        continue
    try:
        soup = BeautifulSoup(raw, 'html.parser')
    except Exception:
        continue
    files_seen.add(rel)

    cursor = 0
    for pre in soup.find_all('pre'):
        code = pre.find('code')
        if not code:
            continue
        n_blocks_total += 1
        text = code.get_text()
        lang = get_lang(code)

        pre_str = str(pre)
        # Build fallback needles from the first descendant tag string
        fallbacks = []
        first_child = code.decode_contents()[:200] if code else ''
        if first_child:
            fallbacks.append(first_child[:80])
            fallbacks.append(first_child[:50])
        line_no, cursor = find_line_no(raw, pre_str, cursor,
                                       fallback_needles=fallbacks)

        issues = analyze(text, lang)
        if not issues:
            continue
        n_blocks_with_issues += 1
        files_with_issues_counter[rel] = files_with_issues_counter.get(rel, 0) + 1

        sample = first_line(text)
        n_lines = len([1 for l in text.split('\n') if l.strip()])
        for it in issues:
            counts[it['type']] = counts.get(it['type'], 0) + 1
            results.append({
                'file': rel,
                'line': line_no,
                'lang': lang,
                'type': it['type'],
                'detail': it['detail'],
                'sample': sample,
                'n_nonempty_lines': n_lines,
            })


summary = {
    'n_files_scanned': len(files_seen),
    'n_code_blocks_scanned': n_blocks_total,
    'n_code_blocks_with_issues': n_blocks_with_issues,
    'n_individual_issues': len(results),
    'counts_by_category': dict(sorted(counts.items(), key=lambda kv: -kv[1])),
    'top_files': sorted(files_with_issues_counter.items(),
                        key=lambda kv: -kv[1])[:20],
}
payload = {'summary': summary, 'issues': results}
OUT_JSON.write_text(json.dumps(payload, indent=2), encoding='utf-8')


def md_escape(s: str) -> str:
    return (s.replace('|', '\\|')
             .replace('\n', ' ')
             .replace('\r', ''))


md = []
md.append('# Code-block indent / formatting audit (detail2)')
md.append('')
md.append('Scope: `<pre><code>` blocks under `part-*`, `appendices/`, '
          '`front-matter/`, `capstone/`.')
md.append('')
md.append('## Summary')
md.append('')
md.append(f'- Files scanned: **{summary["n_files_scanned"]}**')
md.append(f'- Code blocks scanned: **{summary["n_code_blocks_scanned"]}**')
md.append(f'- Code blocks with at least one issue: '
          f'**{summary["n_code_blocks_with_issues"]}**')
md.append(f'- Individual issue rows: **{summary["n_individual_issues"]}**')
md.append('')
md.append('### Counts by category')
md.append('')
md.append('| Category | Count |')
md.append('|---|---|')
for k, v in summary['counts_by_category'].items():
    md.append(f'| `{k}` | {v} |')
md.append('')
md.append('### Top 20 files by issue count')
md.append('')
md.append('| File | Issues |')
md.append('|---|---|')
for f, n in summary['top_files']:
    md.append(f'| `{f}` | {n} |')
md.append('')

md.append('## Sample issues per category')
md.append('')
by_cat: dict[str, list] = {}
for r in results:
    by_cat.setdefault(r['type'], []).append(r)
for cat in summary['counts_by_category']:
    rows = by_cat.get(cat, [])
    md.append(f'### {cat}  ({len(rows)} total)')
    md.append('')
    md.append('| File | Approx line | Lang | Detail | First non-blank line |')
    md.append('|---|---|---|---|---|')
    for r in rows[:30]:
        md.append('| `{f}` | {ln} | `{lang}` | {det} | `{s}` |'.format(
            f=md_escape(r['file']),
            ln=r['line'],
            lang=md_escape(r['lang'] or '-'),
            det=md_escape(r['detail']),
            s=md_escape(r['sample']),
        ))
    md.append('')

md.append('## All issues (flat)')
md.append('')
md.append('| File | Approx line | Lang | Category | Detail | First line |')
md.append('|---|---|---|---|---|---|')
for r in results:
    md.append('| `{f}` | {ln} | `{lang}` | {cat} | {det} | `{s}` |'.format(
        f=md_escape(r['file']),
        ln=r['line'],
        lang=md_escape(r['lang'] or '-'),
        cat=r['type'],
        det=md_escape(r['detail']),
        s=md_escape(r['sample']),
    ))


OUT_MD.write_text('\n'.join(md), encoding='utf-8')

print('=== CODE INDENT AUDIT (detail2) ===')
print(f'Files scanned: {summary["n_files_scanned"]}')
print(f'Code blocks scanned: {summary["n_code_blocks_scanned"]}')
print(f'Code blocks with issues: {summary["n_code_blocks_with_issues"]}')
print(f'Individual issues: {summary["n_individual_issues"]}')
print()
print('Counts by category:')
for k, v in summary['counts_by_category'].items():
    print(f'  {k}: {v}')
print()
print('Top 10 files by issue count:')
for f, n in summary['top_files'][:10]:
    print(f'  {n:4d}  {f}')
print()
print(f'Wrote: {OUT_MD.relative_to(ROOT)}')
print(f'Wrote: {OUT_JSON.relative_to(ROOT)}')
