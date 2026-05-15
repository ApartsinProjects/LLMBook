"""Book-wide audit: find tall atomic blocks that cannot split across pages.

A "reflow blocker" is a block-level HTML element that:
  1. Is CURRENTLY atomic (page-break-inside: avoid) in the EPUB build, AND
  2. Is taller than a typical Kindle page (>30 lines of content).

When such a block sits near the bottom of a page in EPUB, it jumps to the
next page and leaves a ghost gap.

Atomic determination is based on the rules collected in AUDIT_reflow.md:
  - `figure`, `.figure`, `.illustration`, `figure.epigraph` -> atomic
  - `.diagram-container`, `.figure-container` -> atomic
  - `.callout.key-takeaway` -> atomic (none in book today)
  - `.section-card`, `a.section-card` -> atomic
  - `.pathway-box`, `.fm-card`, `.pathway-card` -> atomic
  - `.chapter-header` -> atomic
  - `.author-card` -> FLOWING since v13.15 (legacy CSS overridden)
  - `.bib-entry-card`, `.bib-entry` -> FLOWING since v13.15
  - `.chapter-card`, `.chapter-card-header`, `.chapter-card-body` -> FLOWING
  - All `.callout.*` variants (except key-takeaway) -> FLOWING since v787
  - `.code-block-wrapper`, `pre` -> FLOWING since v787/v788
  - `.math-block`, `.katex-display` -> FLOWING (v13.16 fix)

Approximate height heuristics (line ~ 1 visible reflowed text line):
  - <table>: each <tr> ~ 1.2 lines -> flag tables >30 rows when wrapped
  - <pre>: each `\n` ~ 1 line -> flag <pre> >50 lines when wrapped
  - <figure>/.illustration/.diagram-container: tall if total textual content
    >12 lines (or SVG-only, if SVG viewBox height >> 1 page)
  - .callout.key-takeaway: tall if >4 lines
  - .section-card / .pathway-box / .fm-card / .pathway-card: tall if >8 lines
  - generic atomic block: tall if >30 lines

Output:
  - KDP/build/AUDIT_reflow_blockers.md - human report
  - KDP/build/AUDIT_reflow_blockers.json - structured data
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict, Counter

from bs4 import BeautifulSoup  # type: ignore

ROOT = Path(__file__).resolve().parents[2]  # E:/Projects/BookBlogsHome/LLMBook
SKIP_PARTS = (
    'node_modules', '/.git/', 'KDP/output', 'KDP/build', 'KDP/html2pub',
    'pagefind', 'temp_epub', 'source_fix_backups', 'venv', 'templates'
)


def should_skip(p: Path) -> bool:
    sp = str(p).replace('\\', '/') + '/'
    return any(s in sp for s in SKIP_PARTS)


# ----- Atomic-element catalogue ---------------------------------------------
# (key, css selector function, threshold, label, css reason)
# Each "selector_fn" takes a BS tag and returns True if it matches.

def _has_class(tag, *classes):
    cls = tag.get('class') or []
    return any(c in cls for c in classes)


ATOMIC_SPECS = [
    # Cards
    {
        'key': 'section_card',
        'match': lambda t: (t.name in ('a', 'div') and
                            _has_class(t, 'section-card')),
        'threshold': 8,
        'label': '.section-card / a.section-card',
        'css_rule': ('epub_overrides.css:2056-2079 display:flex + '
                     'page-break-inside:avoid'),
    },
    {
        'key': 'pathway_card',
        'match': lambda t: (t.name in ('div', 'a') and
                            _has_class(t, 'pathway-box', 'fm-card',
                                       'pathway-card')),
        'threshold': 8,
        'label': '.pathway-box / .fm-card / .pathway-card',
        'css_rule': 'epub_overrides.css:390-397 page-break-inside:avoid',
    },
    # Callouts (only key-takeaway is atomic after v787)
    {
        'key': 'callout_key_takeaway',
        'match': lambda t: (t.name in ('div', 'aside', 'section') and
                            _has_class(t, 'callout') and
                            _has_class(t, 'key-takeaway')),
        'threshold': 4,
        'label': '.callout.key-takeaway',
        'css_rule': ('epub_overrides.css:1061-1067, 1606-1613 '
                     'page-break-inside:avoid'),
    },
    # Figures
    {
        'key': 'figure_generic',
        'match': lambda t: (t.name == 'figure' and
                            not _has_class(t, 'diagram-container',
                                           'illustration', 'epigraph',
                                           'diagram')),
        'threshold': 12,
        'label': '<figure> (no specialized class)',
        'css_rule': ('epub_overrides.css:661-664 '
                     'figure {page-break-inside: avoid}'),
    },
    {
        'key': 'figure_illustration',
        'match': lambda t: (t.name in ('figure', 'div') and
                            _has_class(t, 'illustration')),
        'threshold': 12,
        'label': 'figure.illustration / .illustration',
        'css_rule': ('epub_overrides.css:661-664, 840-849 '
                     'page-break-inside:avoid'),
    },
    {
        'key': 'figure_class',
        'match': lambda t: (t.name == 'div' and _has_class(t, 'figure')),
        'threshold': 12,
        'label': 'div.figure',
        'css_rule': 'epub_overrides.css:840-849 page-break-inside:avoid',
    },
    {
        'key': 'diagram_container',
        'match': lambda t: (t.name in ('div', 'figure') and
                            _has_class(t, 'diagram-container')),
        'threshold': 12,
        'label': '.diagram-container',
        'css_rule': 'epub_overrides.css:840-849 page-break-inside:avoid',
    },
    {
        'key': 'figure_container',
        'match': lambda t: (t.name == 'div' and
                            _has_class(t, 'figure-container')),
        'threshold': 12,
        'label': '.figure-container',
        'css_rule': 'figure cascade rule via class match',
    },
    {
        'key': 'figure_diagram',
        'match': lambda t: (t.name == 'figure' and _has_class(t, 'diagram')),
        'threshold': 12,
        'label': '<figure class="diagram">',
        'css_rule': 'epub_overrides.css:661 figure {page-break-inside: avoid}',
    },
    {
        'key': 'epigraph',
        'match': lambda t: (t.name in ('figure', 'div', 'blockquote') and
                            _has_class(t, 'epigraph')),
        'threshold': 8,
        'label': '.epigraph (figure/div/blockquote)',
        'css_rule': ('figure cascade. v13.16 fix proposes flow; not yet '
                     'applied.'),
    },
    {
        'key': 'chapter_header',
        'match': lambda t: (t.name in ('div', 'header') and
                            _has_class(t, 'chapter-header')),
        'threshold': 12,
        'label': '.chapter-header',
        'css_rule': 'epub_overrides.css:1076-1084 page-break-inside:avoid',
    },
]


# ----- Height estimation ----------------------------------------------------
def text_lines(tag, kindle_chars_per_line: int = 70) -> int:
    """Estimate rendered line count from the visible text and structure of
    a tag. Excludes SVG payload (handled separately as a graphic)."""
    # Make a copy and remove SVGs and script/style.
    from copy import copy as _copy
    t2 = _copy(tag)
    for s in t2.find_all(['svg', 'script', 'style']):
        s.decompose()

    # Newlines inside <pre> count as visible lines.
    pre_lines = 0
    for pre in t2.find_all('pre'):
        pre_lines += pre.get_text().count('\n')

    # Plain text (without pre payload double-count)
    text = t2.get_text(separator=' ').strip()
    text = re.sub(r'\s+', ' ', text)
    line_count = max(0, (len(text) + kindle_chars_per_line - 1) //
                     kindle_chars_per_line) if text else 0

    # Block-level elements add structural lines.
    p_count = len(t2.find_all('p'))
    li_count = len(t2.find_all('li'))
    tr_count = len(t2.find_all('tr'))
    h_count = len(t2.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))

    # A paragraph is on average ~2 visible lines; headings ~1
    structural = p_count * 2 + h_count + max(0, li_count) + int(tr_count * 1.2)
    return max(line_count, structural) + pre_lines


def svg_lines(tag, kindle_page_lines: int = 30) -> int:
    """Estimate visual height of SVGs inside a tag, in 'lines'.
    A line ~= 24 CSS pixels. Cap each SVG at one Kindle page (90vh, ~30 lines)
    because epub_overrides.css limits image height to 90vh."""
    total = 0
    for svg in tag.find_all('svg'):
        vb = svg.get('viewBox') or svg.get('viewbox') or ''
        h = None
        if vb:
            parts = vb.split()
            if len(parts) == 4:
                try:
                    h = float(parts[3])
                except ValueError:
                    pass
        if h is None:
            try:
                h = float(svg.get('height', '0').rstrip('px'))
            except ValueError:
                h = 0
        if h > 0:
            total += min(kindle_page_lines, max(1, int(h / 24)))
    return total


def height_estimate(tag) -> int:
    return text_lines(tag) + svg_lines(tag)


# ----- Scan one file --------------------------------------------------------
def scan_file(p: Path) -> list:
    try:
        html = p.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return []
    rel = str(p.relative_to(ROOT)).replace('\\', '/')

    # Use the BS4 'html.parser' which is forgiving of mismatched divs.
    soup = BeautifulSoup(html, 'html.parser')
    findings = []

    # Precompute source positions via line search.
    # BeautifulSoup doesn't track source line numbers consistently, so we
    # re-find each match in the raw HTML to report the source line.
    def find_line(target_html: str) -> int:
        head = target_html[:60]
        idx = html.find(head)
        return html.count('\n', 0, idx) + 1 if idx >= 0 else 0

    for spec in ATOMIC_SPECS:
        for tag in soup.find_all(True):
            try:
                if not spec['match'](tag):
                    continue
            except Exception:
                continue
            h = height_estimate(tag)
            if h < spec['threshold']:
                continue
            # Build a short preview of textual content
            text = re.sub(r'\s+', ' ', tag.get_text()).strip()[:80]
            # The serialized outer HTML; we report its starting line.
            outer = str(tag)
            line = find_line(outer)
            findings.append({
                'file': rel,
                'line': line,
                'category': spec['key'],
                'label': spec['label'],
                'class': ' '.join(tag.get('class') or []),
                'tag': tag.name,
                'lines_est': h,
                'threshold': spec['threshold'],
                'css_rule': spec['css_rule'],
                'preview': text,
                'size_bytes': len(outer),
            })

    # Tables inside an atomic wrapper.
    for table in soup.find_all('table'):
        rows = len(table.find_all('tr'))
        if rows < 30:
            continue
        # Check ancestors for atomic wrapper class.
        wrapper = None
        for anc in table.parents:
            if anc.name == '[document]':
                break
            cls = anc.get('class') or []
            if anc.name == 'figure' and 'epigraph' not in cls:
                wrapper = anc
                break
            if any(c in cls for c in (
                'illustration', 'diagram-container', 'figure', 'figure-container',
                'diagram',
            )):
                wrapper = anc
                break
            if 'callout' in cls and 'key-takeaway' in cls:
                wrapper = anc
                break
        if wrapper is None:
            continue
        outer = str(table)
        line = find_line(outer)
        findings.append({
            'file': rel,
            'line': line,
            'category': 'table_in_atomic_wrapper',
            'label': f'<table> with {rows} rows inside atomic wrapper '
                     f'<{wrapper.name} class="{" ".join(wrapper.get("class") or [])}">',
            'class': ' '.join(table.get('class') or []),
            'tag': 'table',
            'lines_est': int(rows * 1.2),
            'threshold': 30,
            'css_rule': 'Inherited from atomic ancestor',
            'preview': re.sub(r'\s+', ' ', table.get_text())[:80],
            'size_bytes': len(outer),
        })

    # <pre> inside atomic wrapper.
    for pre in soup.find_all('pre'):
        text = pre.get_text()
        lines = text.count('\n')
        if lines < 50:
            continue
        wrapper = None
        for anc in pre.parents:
            if anc.name == '[document]':
                break
            cls = anc.get('class') or []
            if anc.name == 'figure' and 'epigraph' not in cls:
                wrapper = anc
                break
            if any(c in cls for c in (
                'illustration', 'diagram-container', 'figure',
                'figure-container', 'diagram',
            )):
                wrapper = anc
                break
            if 'callout' in cls and 'key-takeaway' in cls:
                wrapper = anc
                break
        if wrapper is None:
            continue
        outer = str(pre)
        line = find_line(outer)
        findings.append({
            'file': rel,
            'line': line,
            'category': 'pre_in_atomic_wrapper',
            'label': f'<pre> with {lines} lines inside atomic wrapper '
                     f'<{wrapper.name} class="{" ".join(wrapper.get("class") or [])}">',
            'class': '',
            'tag': 'pre',
            'lines_est': lines,
            'threshold': 50,
            'css_rule': 'Inherited from atomic ancestor',
            'preview': text[:80].replace('\n', ' '),
            'size_bytes': len(outer),
        })

    return findings


# ----- Main -----------------------------------------------------------------
def main():
    all_findings = []
    file_count = 0
    for p in ROOT.rglob('*.html'):
        if should_skip(p):
            continue
        file_count += 1
        all_findings.extend(scan_file(p))

    # Sort by estimated height descending.
    all_findings.sort(key=lambda f: -f['lines_est'])

    out_md = ROOT / 'KDP' / 'build' / 'AUDIT_reflow_blockers.md'
    out_json = ROOT / 'KDP' / 'build' / 'AUDIT_reflow_blockers.json'

    # Flag outliers: blocks with height >> expected (likely indicates a
    # source-HTML defect like a missing </div> or an `<h3none>` typo).
    # Defect signature: figure/diagram container has > 0 headings or > 1
    # callout inside it (real diagram containers have at most an SVG + a
    # single caption div).
    for f in all_findings:
        f['note'] = ''
        if (f['category'] in ('diagram_container', 'figure_container',
                              'figure_generic', 'figure_illustration',
                              'figure_class', 'figure_diagram')
                and f['lines_est'] > 60):
            f['note'] = ('LIKELY MALFORMED SOURCE HTML: container probably '
                         'has a missing </div> or invalid tag downstream, '
                         'which makes the atomic wrapper absorb all '
                         'following content. Check for `<h3none>`, missing '
                         '</div>, or stray `<` characters between this '
                         'opening tag and the next figure/section.')

    by_category = Counter(f['category'] for f in all_findings)
    by_file = Counter(f['file'] for f in all_findings)
    suspicious_count = sum(1 for f in all_findings if f.get('note'))
    height_dist = Counter()
    for f in all_findings:
        h = f['lines_est']
        if h < 13:
            bucket = '4-12'
        elif h < 31:
            bucket = '13-30'
        elif h < 61:
            bucket = '31-60'
        elif h < 101:
            bucket = '61-100'
        else:
            bucket = '100+'
        height_dist[bucket] += 1

    # Build markdown
    lines = []
    lines.append('# AUDIT: Reflow Blockers (Tall Atomic Blocks)')
    lines.append('')
    lines.append('Generated by `KDP/build/_audit_reflow_blockers.py` (BS4 parser).')
    lines.append('')
    lines.append(f'**Files scanned**: {file_count}')
    lines.append(f'**Total tall atomic blocks found**: {len(all_findings)}')
    lines.append(f'**Suspicious oversize blocks (likely malformed HTML)**: '
                 f'{suspicious_count}')
    lines.append('')
    lines.append('## Methodology')
    lines.append('')
    lines.append('"Atomic" = element cannot split across a page boundary in')
    lines.append('EPUB/Kindle. Determination follows the CSS audit in')
    lines.append('`AUDIT_reflow.md` (load order book.css then')
    lines.append('epub_overrides.css). A block is "tall" if its estimated')
    lines.append('rendered line count exceeds the per-category threshold.')
    lines.append('Heights are estimated from text length (~70 chars/line),')
    lines.append('`<p>` count, `<tr>` count, `<li>` count, `<pre>` newlines,')
    lines.append('and SVG viewBox height (capped at one Kindle page since')
    lines.append('epub_overrides.css limits images to 90vh).')
    lines.append('')
    lines.append('### Categories scanned')
    lines.append('')
    lines.append('| Category | Selector | Tall threshold | Atomic via |')
    lines.append('|---|---|---:|---|')
    for spec in ATOMIC_SPECS:
        lines.append(
            f'| `{spec["key"]}` | `{spec["label"]}` | '
            f'{spec["threshold"]} lines | {spec["css_rule"]} |'
        )
    lines.append('| `table_in_atomic_wrapper` | `<table>` inside atomic figure/illustration | 30 rows | Inherited |')
    lines.append('| `pre_in_atomic_wrapper` | `<pre>` inside atomic figure/illustration | 50 lines | Inherited |')
    lines.append('')

    lines.append('## Distribution by Category')
    lines.append('')
    lines.append('| Category | Count |')
    lines.append('|---|---:|')
    for cat, count in by_category.most_common():
        lines.append(f'| `{cat}` | {count} |')
    lines.append('')

    lines.append('## Distribution by Estimated Height')
    lines.append('')
    lines.append('| Lines | Count |')
    lines.append('|---|---:|')
    for bucket in ['4-12', '13-30', '31-60', '61-100', '100+']:
        if bucket in height_dist:
            lines.append(f'| {bucket} | {height_dist[bucket]} |')
    lines.append('')

    lines.append('## Top 10 Worst Offenders (by Estimated Height)')
    lines.append('')
    lines.append('| # | File | Line | Category | Est. height | Class | Preview | Suspicious? |')
    lines.append('|---:|---|---:|---|---:|---|---|---|')
    for i, f in enumerate(all_findings[:10], 1):
        cls = (f['class'] or '').replace('|', '\\|')[:40]
        prev = (f['preview'] or '').replace('|', '\\|')[:60]
        suspicious = 'YES' if f.get('note') else ''
        lines.append(
            f'| {i} | `{f["file"]}` | {f["line"]} | `{f["category"]}` | '
            f'{f["lines_est"]} | `{cls}` | {prev} | {suspicious} |'
        )
    lines.append('')
    if suspicious_count:
        lines.append(f'**{suspicious_count} blocks are flagged as likely '
                     'malformed source HTML.** When the container\'s rendered '
                     'height exceeds 100 lines, the most common cause is a '
                     'missing `</div>` or an invalid tag (e.g., `<h3none>`) '
                     'that the parser cannot close, causing the atomic '
                     'wrapper to absorb all downstream content.')
        lines.append('')

    lines.append('## Top 10 Files With Most Blockers')
    lines.append('')
    lines.append('| File | Blockers |')
    lines.append('|---|---:|')
    for fpath, count in by_file.most_common(10):
        lines.append(f'| `{fpath}` | {count} |')
    lines.append('')

    # Per-category detail
    lines.append('## Detail by Category')
    lines.append('')
    by_cat = defaultdict(list)
    for f in all_findings:
        by_cat[f['category']].append(f)
    for cat, items in sorted(by_cat.items(), key=lambda kv: -len(kv[1])):
        ex0 = items[0]
        lines.append(f'### `{cat}` ({len(items)} blocks)')
        lines.append('')
        lines.append(f'- Selector: `{ex0["label"]}`')
        lines.append(f'- Atomic via: {ex0["css_rule"]}')
        lines.append(f'- Threshold: > {ex0["threshold"]} lines')
        lines.append('')
        items.sort(key=lambda f: -f['lines_est'])
        lines.append('| File | Line | Est. height | Class | Preview |')
        lines.append('|---|---:|---:|---|---|')
        for f in items[:15]:
            cls = (f['class'] or '').replace('|', '\\|')[:40]
            prev = (f['preview'] or '').replace('|', '\\|')[:60]
            lines.append(
                f'| `{f["file"]}` | {f["line"]} | {f["lines_est"]} | '
                f'`{cls}` | {prev} |'
            )
        if len(items) > 15:
            lines.append('')
            lines.append(f'_..and {len(items) - 15} more in this category._')
        lines.append('')

    lines.append('## Recommended CSS Additions')
    lines.append('')
    lines.append('The existing `_fix_v13_16_reflow.css` already addresses the')
    lines.append('biggest patterns (`<figure>`, `.illustration`, `.figure`,')
    lines.append('`.diagram-container`, `.epigraph`, `.math-block`). Apply')
    lines.append('that file to neutralize most blockers. Additions:')
    lines.append('')
    lines.append('```css')
    lines.append('/* Cover .figure-container (used in part-7 and part-9) */')
    lines.append('.figure-container,')
    lines.append('div.figure-container {')
    lines.append('    page-break-inside: auto !important;')
    lines.append('    break-inside: auto !important;')
    lines.append('}')
    lines.append('')
    lines.append('/* Cover <figure class="diagram"> (used in module-30) */')
    lines.append('figure.diagram {')
    lines.append('    page-break-inside: auto !important;')
    lines.append('    break-inside: auto !important;')
    lines.append('}')
    lines.append('figure.diagram > svg,')
    lines.append('figure.diagram > img {')
    lines.append('    page-break-inside: avoid !important;')
    lines.append('    break-inside: avoid !important;')
    lines.append('}')
    lines.append('')
    lines.append('/* section-card, pathway-box, fm-card, pathway-card are')
    lines.append(' * meant to be small navigation cards. If they grow past')
    lines.append(' * 8 lines they cause page-jumps. Allow flow but glue the')
    lines.append(' * title to the first body element. */')
    lines.append('.section-card,')
    lines.append('a.section-card,')
    lines.append('.pathway-box,')
    lines.append('.fm-card,')
    lines.append('.pathway-card {')
    lines.append('    page-break-inside: auto !important;')
    lines.append('    break-inside: auto !important;')
    lines.append('}')
    lines.append('```')
    lines.append('')

    lines.append('## Blocks That SHOULD Stay Atomic')
    lines.append('')
    lines.append('- `.callout.key-takeaway` blocks under 4 lines remain')
    lines.append('  atomic (none currently exceed this in the book).')
    lines.append('- `.chapter-header` banners (small, intentional).')
    lines.append('- `<tr>` rows (already row-level atomic).')
    lines.append('- Single `<img>` / `<svg>` inside a figure (90vh capped).')
    lines.append('- Single `.katex-display` (one rendered formula).')
    lines.append('- `<figure>` wrappers when their TOTAL content (incl.')
    lines.append('  caption) fits within one Kindle page, regardless of how')
    lines.append('  tall the SVG is on the web - the 90vh cap protects them.')
    lines.append('')

    out_md.write_text('\n'.join(lines), encoding='utf-8')
    out_json.write_text(json.dumps({
        'file_count': file_count,
        'total_findings': len(all_findings),
        'by_category': dict(by_category),
        'by_file_top20': dict(by_file.most_common(20)),
        'top_offenders': all_findings[:50],
    }, indent=2), encoding='utf-8')

    print(f'Files scanned: {file_count}')
    print(f'Total tall atomic blocks: {len(all_findings)}')
    print(f'\nBy category:')
    for cat, count in by_category.most_common():
        print(f'  {cat:<30} {count}')
    print(f'\nTop 10 offenders by height:')
    for f in all_findings[:10]:
        print(f'  {f["lines_est"]:>4} lines | {f["category"]:<25} | '
              f'{f["file"]}:{f["line"]}')
    print(f'\nReport: {out_md}')
    print(f'JSON:   {out_json}')


if __name__ == '__main__':
    main()
