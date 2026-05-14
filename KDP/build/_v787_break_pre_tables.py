"""v787: ROOT-CAUSE fix for code/table not splitting between pages.

Persistent problem visible in latest screenshots:
  - Long code fragment 0.2.2 clipped at the bottom of a page
  - Bad flow: code fragment is the only content of the right column,
    left column nearly empty
  - Tables don't flow page-to-page (forced atomic)
  - Code spills past callout border (inline <code> in TIP)
  - Big trailing empty space at bottom of callouts (e.g. optimizers
    box) and bibliography entry-cards

Why v785/v786 didn't fix this: 17 separate `page-break-inside: avoid`
rules exist in epub_overrides.css from earlier waves (v783, etc.) and
they shadow the auto rules. Most damaging for code rendering:

  Line 333-334:   .callout pre, .code-block-wrapper > pre  -> avoid
  Line 833-834:   .code-block-wrapper, .callout pre        -> avoid
  Line 1097-1099: headings (h1-h6 inside callouts)         -> inside avoid

This file APPENDS overriding rules with `!important` that explicitly
set `page-break-inside: auto` on every breakable container, in a block
that loads LAST so the cascade resolves in our favor.

Also:
  - Inline <code> word-break inside callouts (clip_grad_norm spillover)
  - Callouts: min-height:0 + height:auto so Kindle doesn't pad them
  - Bib-entry-card: tight bottom padding
  - Tables: thead/tbody display:table-row-group + per-row break-inside:
    avoid + table-level break-inside: auto
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
overrides = ROOT / 'KDP' / 'build' / 'epub_overrides.css'
s = overrides.read_text(encoding='utf-8')

NEW_BLOCK = '''
/* ============================================================
 * v787 ROOT-CAUSE: allow pre/tables/callouts to break across pages.
 * Loaded LAST so it overrides every prior `avoid` rule.
 * ============================================================ */

/* CODE BLOCKS: must allow page splits, including when nested inside a
 * callout. The earlier "avoid" rules caused clipping and bad flow. */
pre,
.code-block-wrapper,
.code-block-wrapper > pre,
.callout pre,
.callout > pre,
.callout .code-block-wrapper,
.callout.algorithm pre,
.callout.exercise pre,
.callout.library-shortcut pre,
.callout.numeric-example pre,
pre[class*="language-"],
pre.pygments-highlighted,
code[class*="language-"] {
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-column-break-inside: auto !important;
    -webkit-box-decoration-break: clone !important;
    box-decoration-break: clone !important;
    overflow-x: visible !important;
    overflow-y: visible !important;
    /* Long lines: wrap to fit Kindle column width so no clipping */
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}

/* Inline <code> inside callouts: prevent the long
 * "clip_grad_norm_(model.parameters(), max_norm=1.0)" spillover. */
.callout code,
.callout :not(pre) > code,
li code,
p code {
    word-wrap: break-word !important;
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
    white-space: normal !important;
    max-width: 100% !important;
}

/* TABLES: allow row-level breaks, never atomic. <thead> repeats on
 * each page fragment if Kindle honors it. */
table,
.complex-table,
.comparison-table,
table.complex-table,
table.comparison-table {
    page-break-inside: auto !important;
    break-inside: auto !important;
    table-layout: fixed !important;
    width: 100% !important;
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}
thead { display: table-header-group !important; }
tbody { display: table-row-group !important; }
tfoot { display: table-footer-group !important; }
/* Each ROW should stay together, but the table as a whole can break
 * between rows. */
tr {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}

/* CALLOUTS: must allow internal page breaks, no minimum height that
 * would create trailing empty space. The "optimizers" callout had a
 * huge empty bottom because Kindle inferred a min-height equal to
 * the column height. */
.callout,
.callout.tip,
.callout.note,
.callout.warning,
.callout.exercise,
.callout.algorithm,
.callout.fun-note,
.callout.research-frontier,
.callout.practical-example,
.callout.big-picture,
.callout.key-insight,
.callout.library-shortcut,
.callout.production-pattern,
.callout.postmortem,
.callout.thesis-thread,
.callout.numeric-example,
.callout.self-check,
.callout.looking-back,
.callout.cross-ref,
.callout.lab,
.callout.pathway {
    min-height: 0 !important;
    height: auto !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-box-decoration-break: clone !important;
    box-decoration-break: clone !important;
}
.callout > *:last-child,
.callout p:last-child,
.callout li:last-child,
.callout pre:last-child {
    margin-bottom: 0 !important;
}

/* BIBLIOGRAPHY entry-cards: trim trailing whitespace. The "PAPER"
 * pill at the bottom had a huge gap below it because the card had
 * fixed padding-bottom. */
.bib-entry,
.bib-entry-card {
    padding-bottom: 0.3em !important;
    margin-bottom: 0.3em !important;
}
.bib-entry .bib-tag,
.bib-entry-card .bib-tag,
.bib-entry > .badge,
.bib-entry-card > .badge {
    margin-bottom: 0 !important;
}

/* FIGURES (kept atomic for image+caption integrity) AND author cards
 * are still avoid; every other container is auto. */

/* Verify exception: chapter-header MUST stay whole (it's a small navy
 * band), key-takeaway is short and stays whole. */
.chapter-header,
.callout.key-takeaway,
figure,
.figure,
.author-card {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
'''

START = '/* ============================================================\n * v787 ROOT-CAUSE'

if START in s:
    idx = s.index(START)
    s = s[:idx].rstrip() + '\n' + NEW_BLOCK
    print('  [v787 block REPLACED in epub_overrides.css]')
else:
    s = s.rstrip() + '\n' + NEW_BLOCK
    print(f'  [v787 block ADDED to epub_overrides.css ({len(NEW_BLOCK)} chars)]')

overrides.write_text(s, encoding='utf-8')
