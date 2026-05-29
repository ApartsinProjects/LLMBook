"""
Author missing or non-canonical figure/table captions across the book.

This is the figure/table analogue of ``_author_code_captions.py``. The goal is
that every figure-tier element (an ``<img>``/``<figure>``, a ``<table>``, or a
code listing) carries a caption with the standard prefix:

    <strong>Figure N.M.K:</strong> One-sentence explanation.
    <strong>Table N.M.K:</strong>  One-sentence explanation.
    <strong>Listing N.M.K:</strong> One-sentence explanation.

The dominant wrappers (observed from a book-wide audit) are kept as-is:

  - ``<figure class="illustration"><img/><figcaption>...</figcaption></figure>``
    for figures and figure-wrapped tables (already 100% caption-prefixed).
  - ``<div class="diagram-container"><img/><div class="diagram-caption">...</div></div>``
    for technical diagrams (already 100% caption-prefixed).
  - ``<div class="comparison-table"><div class="comparison-table-title">...</div><table>...</table></div>``
    for comparison/data tables. The title-div is the de facto caption but
    342 of 342 instances lack a "Table N.M.K:" prefix. This script adds the
    prefix while preserving the existing descriptive text.
  - Plain ``<table>...</table>`` not wrapped in any caption-bearing container
    (24 truly-naked tables in main content). The script inserts a
    ``<caption><strong>Table N.M.K:</strong> Text.</caption>`` as the first
    child of the ``<table>``.

Skip rules
----------
  * ``<figure class="illustration chapter-opener">`` and any other figure
    classed as a chapter/part opener (decorative hero).
  * Author photos, agent avatars (small inline icons).
  * ``<table>`` inside callouts (note/warning/practical-example/etc.).
  * ``<table>`` inside a ``<figure>`` that already has ``<figcaption>``.
  * ``<table>`` inside a ``<div class="diagram-container">`` already
    captioned upstream.
  * Anything already carrying a "Table N.M.K:" / "Figure N.M.K:" prefix.

Numbering
---------
Per-section, per-kind. Tables and figures have independent K sequences. The
script reads existing "Table N.M.K:" prefixes in the file and continues the
sequence (max + 1). For the comparison-table batch this means the first
table-title in section 4.1 becomes "Table 4.1.1", the second "Table 4.1.2",
and so on, in document order.

Caption text
------------
Per element:
  * comparison-table-title: keep existing descriptive text. We only PREPEND
    the "<strong>Table N.M.K:</strong> " marker; the human-written title is
    preserved untouched. No <em> wrapping (matches the dominant pattern).
  * Naked tables: synthesise from preceding ``<p>`` first sentence, or from
    a preceding heading, or from the column headers, or a generic fallback.

The script is idempotent: a second invocation reports zero changes.

Usage
-----
    python _author_figtab_captions.py            # dry run (default)
    python _author_figtab_captions.py --apply    # write changes
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {
    'node_modules', '.git', 'KDP', 'build', 'temp_ebook', 'temp_epub',
    'source_fix_backups', 'pagefind', 'templates', '.claude',
    '.book-update', 'vendor', 'scripts', 'docs', 'styles',
    '.html2epub_cache', '_concept-figs', 'agents', 'tmp_whats_next',
    'images', 'downloads',
}

TAG_RE = re.compile(r'<[^>]+>')

# Callout div classes whose internal tables are skipped.
CALLOUT_CLASSES = [
    'callout note',
    'callout warning',
    'callout tip',
    'callout pitfall',
    'callout deep-dive',
    'callout fun-note',
    'callout algorithm',
    'callout library-shortcut',
    'callout production-pattern',
    'callout practical-example',
    'callout case-study',
    'callout decision',
    'callout exercise',
    'callout opinion',
    'callout history',
    'callout philosophy',
    'callout takeaway',
    'callout big-idea',
    'callout reflection',
    'callout side-quest',
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def strip_tags(html: str) -> str:
    return TAG_RE.sub('', html).strip()


def section_prefix(stem: str, parent: str = '') -> str | None:
    m = re.match(r'section-(\d+)\.(\d+)$', stem)
    if m:
        return f'{m.group(1)}.{m.group(2)}'
    m = re.match(r'section-([a-z])\.(\d+)$', stem)
    if m:
        return f'{m.group(1)}.{m.group(2)}'
    # Module/appendix index pages: derive prefix from parent folder.
    if stem == 'index' and parent:
        # module-NN-... -> 'N.0' (strip leading zero)
        m = re.match(r'module-(\d+)-', parent)
        if m:
            return f'{int(m.group(1))}.0'
        # appendix-X-... -> 'X.0' (lowercase to match section convention)
        m = re.match(r'appendix-([a-z])-', parent)
        if m:
            return f'{m.group(1)}.0'
    return None


def trim_sentence(text: str, max_words: int = 28) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    m = re.search(r'([.!?])\s', text + ' ')
    if m:
        text = text[: m.start() + 1]
    # Strip a trailing colon that often appears in lead-in sentences like
    # "Our model has these hyperparameters:".
    text = text.rstrip().rstrip(':').rstrip()
    words = text.split(' ')
    if len(words) > max_words:
        head = ' '.join(words[:max_words])
        chosen = None
        for break_char in (';', ','):
            idx = head.rfind(break_char)
            if idx > len(head) // 2:
                chosen = head[:idx] + '.'
                break
        text = chosen if chosen else head.rstrip(',;:') + '.'
    if text and text[-1] not in '.!?':
        text += '.'
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


# ---------------------------------------------------------------------------
# Span/container utilities
# ---------------------------------------------------------------------------


def div_spans(text: str, opener: str) -> list[tuple[int, int]]:
    """Return [(start, end_after_closing_div)] for every container that
    starts with the literal ``opener`` (e.g. ``<div class="comparison-table">``)
    and is closed by a matching ``</div>``. Handles nesting."""
    spans: list[tuple[int, int]] = []
    i = 0
    while True:
        j = text.find(opener, i)
        if j == -1:
            break
        depth = 0
        pos = j
        end = -1
        while pos < len(text):
            if text[pos:pos + 4] == '<div':
                depth += 1
                pos += 4
            elif text[pos:pos + 6] == '</div>':
                depth -= 1
                pos += 6
                if depth == 0:
                    end = pos
                    break
            else:
                pos += 1
        if end == -1:
            i = j + 1
            continue
        spans.append((j, end))
        i = end
    return spans


def figure_spans(text: str) -> list[tuple[int, int, bool]]:
    """Return [(start, end, has_figcaption)] for every <figure> element."""
    spans = []
    for m in re.finditer(r'<figure\b[^>]*>(.*?)</figure>', text, re.DOTALL):
        spans.append((m.start(), m.end(), '<figcaption' in m.group(1)))
    return spans


def in_any(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(s <= pos < e for s, e in spans)


def in_any3(pos: int, spans: list[tuple[int, int, bool]]) -> bool:
    return any(s <= pos < e for s, e, _ in spans)


def callout_spans(text: str) -> list[tuple[int, int]]:
    spans = []
    for cls in CALLOUT_CLASSES:
        spans.extend(div_spans(text, f'<div class="{cls}"'))
    return spans


# ---------------------------------------------------------------------------
# Caption-text heuristics
# ---------------------------------------------------------------------------


def preceding_paragraph_text(content: str, pos: int) -> str | None:
    """Return plain text of the immediately-preceding <p> if any."""
    look_start = max(0, pos - 4000)
    look = content[look_start:pos]
    p_end = look.rfind('</p>')
    if p_end == -1:
        return None
    p_start = look.rfind('<p', 0, p_end)
    if p_start == -1:
        return None
    # Reject if there's substantial real text between </p> and pos.
    after_p = look[p_end + 4:]
    if len(strip_tags(after_p)) > 80:
        return None
    return strip_tags(look[p_start:p_end + 4])


def preceding_heading_text(content: str, pos: int) -> str | None:
    """Return the closest preceding h2/h3 text."""
    look = content[max(0, pos - 4000):pos]
    h_match = None
    for m in re.finditer(r'<h[23][^>]*>(.*?)</h[23]>', look, re.DOTALL):
        h_match = m
    if h_match:
        return strip_tags(h_match.group(1))
    return None


def caption_from_table_headers(table_html: str) -> str | None:
    """Build a caption from <th> column headers."""
    headers = re.findall(r'<th[^>]*>(.*?)</th>', table_html, re.DOTALL)
    headers = [strip_tags(h) for h in headers if strip_tags(h)]
    if not headers:
        return None
    headers = headers[:4]
    if len(headers) == 1:
        return trim_sentence(f'Table of {headers[0].lower()} values.', max_words=20)
    joined = ', '.join(headers[:-1]) + f' and {headers[-1]}'
    return trim_sentence(f'Comparison of {joined.lower()}.', max_words=20)


def caption_text_for_table(content: str, table_start: int, table_html: str,
                           h1: str) -> str:
    """Best-effort one-sentence caption for a naked table."""
    # If an h3 (or h2) sits IMMEDIATELY before the table (no intervening
    # paragraph), prefer the heading text — it usually labels the table.
    pre_window = content[max(0, table_start - 600):table_start]
    last_h = None
    last_p = None
    for m in re.finditer(r'<h[23][^>]*>(.*?)</h[23]>', pre_window, re.DOTALL):
        last_h = m
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', pre_window, re.DOTALL):
        last_p = m
    if last_h and (last_p is None or last_h.end() > last_p.end()):
        head_text = strip_tags(last_h.group(1))
        if head_text:
            return trim_sentence(f'{head_text}.', max_words=20)
    para = preceding_paragraph_text(content, table_start)
    if para:
        # Reject prompts/discourse openers like "Step 1:" or short fragments.
        first_word = para.split(' ', 1)[0].lower().rstrip('.,:;')
        if first_word in {'this', 'these', 'that', 'those', 'we', 'you',
                          'it', 'they', 'there'}:
            para = None
    if para:
        first = trim_sentence(para, max_words=22)
        if first and len(first) > 25:
            return first
    head = preceding_heading_text(content, table_start)
    if head:
        return trim_sentence(f'{head}.', max_words=20)
    fromcols = caption_from_table_headers(table_html)
    if fromcols:
        return fromcols
    topic = re.sub(r'^[Ss]ection\s+[\d.a-z]+:\s*', '', h1).strip() or 'this section'
    if topic and topic[0].isupper():
        topic = topic[0].lower() + topic[1:]
    return trim_sentence(f'Reference table for {topic}.', max_words=20)


# ---------------------------------------------------------------------------
# Per-file processing
# ---------------------------------------------------------------------------


def h1_title(content: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if not m:
        return ''
    return strip_tags(m.group(1))


def next_seq(content: str, kind: str, prefix: str) -> int:
    """Return next available K for ``kind`` ('Figure' or 'Table') in section
    ``prefix``. Reads <strong>Kind P.K:</strong> occurrences."""
    pat = re.compile(rf'\b{re.escape(kind)}\s+{re.escape(prefix)}\.(\d+)\b')
    nums = [int(n) for n in pat.findall(content)]
    return (max(nums) if nums else 0) + 1


def process_file(path: Path, apply: bool) -> dict:
    """Run all caption authoring rules on the file. Returns a stats dict."""
    prefix = section_prefix(path.stem, path.parent.name)
    stats = {
        'comparison_table_renamed': 0,
        'naked_table_captioned': 0,
        'figure_skipped_opener': 0,
        'diagram_skipped_already_captioned': 0,
    }
    if prefix is None:
        return stats
    try:
        content = path.read_text(encoding='utf-8')
    except Exception:
        return stats

    h1 = h1_title(content)

    # Pre-compute spans we need.
    callouts = callout_spans(content)
    cmp_spans = div_spans(content, '<div class="comparison-table">')
    figs = figure_spans(content)
    diag_spans = div_spans(content, '<div class="diagram-container">')

    # Build a list of (insert/replace operations) to apply in reverse order.
    edits: list[tuple[int, int, str]] = []

    # ---- 1) comparison-table titles --------------------------------------
    # Each <div class="comparison-table-title">...</div> inside a
    # comparison-table container that doesn't already start with
    # "Table N.M.K:" gets the prefix prepended. comparison-tables that lack
    # any title at all receive a fresh, synthesised title prepended at the
    # top of the container.
    table_seq = next_seq(content, 'Table', prefix)
    title_re = re.compile(
        r'<div class="comparison-table-title">(.*?)</div>',
        re.DOTALL,
    )
    cmp_handled = set()
    for m in title_re.finditer(content):
        tstart = m.start()
        owner = None
        for cs, ce in cmp_spans:
            if cs <= tstart < ce:
                owner = (cs, ce)
                break
        if owner is None:
            continue
        cmp_handled.add(owner)
        inner = m.group(1).strip()
        inner_text = strip_tags(inner)
        # Already prefixed? Detect <strong>Table N.M.K:</strong> or plain
        # "Table N.M.K:" at the start.
        if re.match(r'^\s*(?:<strong>)?\s*Table\s+[\w.]+', inner_text):
            continue
        # Compute the new K and inject.
        k = table_seq
        table_seq += 1
        # Use the user-specified canonical shape with italic body wrap.
        # The descriptive title text becomes the explanation.
        body = inner.strip()
        # Trim hard if the title contains the literal text "(as of YYYY)"
        # we keep it; otherwise the body is left verbatim.
        if not body.endswith(('.', '!', '?')):
            body_with_period = body + '.'
        else:
            body_with_period = body
        new_inner = (
            f'<strong>Table {prefix}.{k}:</strong> '
            f'<em>{body_with_period}</em>'
        )
        new_div = f'<div class="comparison-table-title">{new_inner}</div>'
        edits.append((m.start(), m.end(), new_div))
        stats['comparison_table_renamed'] += 1

    # comparison-tables without any title at all: synthesise one.
    for cs, ce in cmp_spans:
        if (cs, ce) in cmp_handled:
            continue
        # Find inner table
        inner_html = content[cs:ce]
        if '<div class="comparison-table-title">' in inner_html:
            continue  # had a title but our regex missed it (unlikely)
        # Find the first <table>
        tm = re.search(r'<table\b[^>]*>(.*?)</table>', inner_html, re.DOTALL)
        if not tm:
            continue
        # Synthesise caption text from preceding paragraph or table headers.
        text = caption_text_for_table(content, cs, tm.group(0), h1)
        k = table_seq
        table_seq += 1
        title_div = (
            f'<div class="comparison-table-title">'
            f'<strong>Table {prefix}.{k}:</strong> '
            f'<em>{text}</em></div>\n'
        )
        # Insert just after the opening <div class="comparison-table">
        open_tag = '<div class="comparison-table">'
        opener_end = cs + len(open_tag)
        insert_pos = opener_end
        # Move past any trailing newline after the opener.
        if content[insert_pos:insert_pos + 1] == '\n':
            insert_pos += 1
        edits.append((insert_pos, insert_pos, title_div))
        stats['comparison_table_renamed'] += 1

    # ---- 1b) repair malformed table <caption> elements -------------------
    # Some tables already carry a <caption> but with an empty <strong></strong>
    # prefix (a known typo pattern) or a "Figure N (Table)" non-standard
    # prefix. Rewrite these to canonical form.
    for m in re.finditer(
        r'<caption([^>]*)>(.*?)</caption>',
        content,
        re.DOTALL,
    ):
        attrs = m.group(1)
        cap_body = m.group(2).strip()
        cap_text = strip_tags(cap_body)
        # Skip captions that already carry a canonical "Table N.M.K:" prefix.
        if re.match(r'^\s*Table\s+[\w.]+\s*:', cap_text):
            continue
        # Find the parent <table> to make sure we're actually inside one
        # (not, say, a <figcaption> with caption inside, which doesn't exist).
        table_open = content.rfind('<table', 0, m.start())
        if table_open == -1:
            continue
        # The caption must be a direct child (within 200 chars of the table).
        if m.start() - table_open > 400:
            continue
        # Skip if inside a comparison-table (handled above) or a callout.
        if in_any(table_open, cmp_spans):
            continue
        if in_any(table_open, callouts):
            continue
        # Detect empty <strong></strong> prefix or "Figure N (Table)" prefix.
        empty_strong = re.match(r'^\s*<strong>\s*</strong>\s*:?\s*', cap_body)
        figure_table_prefix = re.match(
            r'^\s*<strong>\s*Figure\s+[\w.]+\s*\(Table\)\s*:?\s*</strong>\s*:?\s*',
            cap_body,
        )
        if not (empty_strong or figure_table_prefix):
            continue
        # Strip the broken prefix and any leading colon.
        if empty_strong:
            body_after = cap_body[empty_strong.end():].lstrip()
        else:
            body_after = cap_body[figure_table_prefix.end():].lstrip()
        body_after = body_after.lstrip(':').lstrip()
        # Wrap a fresh body — preserving any embedded HTML.
        if body_after and not body_after.endswith(('.', '!', '?')):
            body_after = body_after + '.'
        k = table_seq
        table_seq += 1
        new_cap = (
            f'<caption{attrs}><strong>Table {prefix}.{k}:</strong> '
            f'<em>{body_after}</em></caption>'
        )
        edits.append((m.start(), m.end(), new_cap))
        stats['naked_table_captioned'] += 1

    # ---- 2) naked tables --------------------------------------------------
    for m in re.finditer(r'<table\b[^>]*>(.*?)</table>', content, re.DOTALL):
        tstart = m.start()
        body = m.group(1)
        if '<caption' in body:
            continue
        # In a figure that already has figcaption?
        if any(s <= tstart < e for s, e, has_fc in figs if has_fc):
            continue
        # In a figure that has no figcaption? (would need other treatment)
        if any(s <= tstart < e for s, e, has_fc in figs if not has_fc):
            continue
        # In a comparison-table (handled above)
        if in_any(tstart, cmp_spans):
            continue
        # In a diagram-container that already has its own caption upstream?
        if in_any(tstart, diag_spans):
            continue
        # In a callout? skip.
        if in_any(tstart, callouts):
            continue
        # OK — author a caption.
        text = caption_text_for_table(content, tstart, m.group(0), h1)
        k = table_seq
        table_seq += 1
        caption_html = (
            f'<caption><strong>Table {prefix}.{k}:</strong> '
            f'<em>{text}</em></caption>\n'
        )
        # Insert caption as first child of the <table>. We need to find the
        # offset right after the opening <table ...> tag.
        gt = content.find('>', tstart)
        if gt == -1 or gt > m.end():
            continue
        insert_pos = gt + 1
        # Preserve newline after the opening tag if present.
        edits.append((insert_pos, insert_pos, '\n' + caption_html))
        stats['naked_table_captioned'] += 1

    # ---- 3) figures without figcaption (chapter openers) -----------------
    for s, e, has_fc in figs:
        if has_fc:
            continue
        # Only skip-counted; we don't add captions to opener art.
        snippet = content[s:e]
        if 'chapter-opener' in snippet or 'part-opener' in snippet:
            stats['figure_skipped_opener'] += 1
            continue
        # Otherwise: still skip (we have no signal for content imgs in this
        # book, and the audit shows zero non-opener uncaptioned figures).

    # ---- 4) diagram-containers without their own caption -----------------
    for ds, de in diag_spans:
        inner = content[ds:de]
        if 'class="diagram-caption"' in inner or '<figcaption' in inner:
            continue
        # Check if parent figure already has figcaption.
        parent_fig = any(fs <= ds and de <= fe and has_fc
                         for fs, fe, has_fc in figs)
        if parent_fig:
            stats['diagram_skipped_already_captioned'] += 1
            continue
        # No parent caption: in the book this combination is currently
        # absent. We do nothing to avoid bogus captions on edge cases.

    if not edits:
        return stats

    if apply:
        # Apply in reverse order.
        new_content = content
        for ins_start, ins_end, html in sorted(edits, key=lambda x: x[0],
                                               reverse=True):
            new_content = new_content[:ins_start] + html + new_content[ins_end:]
        path.write_text(new_content, encoding='utf-8')

    return stats


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def iter_html_files(root: Path):
    for path in root.rglob('*.html'):
        parts = set(path.parts)
        if parts & SKIP_DIRS:
            continue
        yield path


def main() -> int:
    apply = '--apply' in sys.argv
    files = sorted(iter_html_files(BOOK_ROOT))

    totals = {
        'comparison_table_renamed': 0,
        'naked_table_captioned': 0,
        'figure_skipped_opener': 0,
        'diagram_skipped_already_captioned': 0,
    }
    files_touched: list[tuple[str, dict]] = []

    for path in files:
        if section_prefix(path.stem, path.parent.name) is None:
            continue
        stats = process_file(path, apply)
        for k, v in stats.items():
            totals[k] += v
        change_count = stats['comparison_table_renamed'] + stats['naked_table_captioned']
        if change_count:
            rel = str(path.relative_to(BOOK_ROOT)).replace('\\', '/')
            files_touched.append((rel, dict(stats)))

    mode = 'APPLIED' if apply else 'DRY RUN'
    print(f'=== Figure/Table caption author ({mode}) ===')
    print(f'HTML files scanned (section-style): '
          f'{sum(1 for p in files if section_prefix(p.stem, p.parent.name))}')
    print(f'Files modified: {len(files_touched)}')
    for k, v in totals.items():
        print(f'  {k}: {v}')

    if files_touched:
        print()
        print('Files touched (counts: cmp-table-renamed, naked-table-caps):')
        for rel, st in sorted(files_touched,
                              key=lambda x: -(x[1]['comparison_table_renamed']
                                              + x[1]['naked_table_captioned']))[:30]:
            print(f"  {st['comparison_table_renamed']:3d} cmp  "
                  f"{st['naked_table_captioned']:2d} naked  {rel}")
        if len(files_touched) > 30:
            print(f'  ... +{len(files_touched) - 30} more files')

    if not apply and (totals['comparison_table_renamed']
                      or totals['naked_table_captioned']):
        print('\nRe-run with --apply to write changes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
