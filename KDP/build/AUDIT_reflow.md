# AUDIT: Reflow / Atomic Element Analysis (EPUB/Kindle)

Date: 2026-05-15
Scope: `styles/book.css` (3,526 lines), `KDP/build/epub_overrides.css` (3,336 lines), inline `<style>` in `front-matter/about-authors.html`.

## Methodology

Atomic = element cannot split across page boundary in EPUB/Kindle. Triggers searched:
- `display:flex`, `display:grid`, `display:table` on block-level containers
- `page-break-inside: avoid` / `break-inside: avoid`
- `position: absolute|fixed`
- `float: left|right` (with width)

The EPUB load order is **`book.css` then `epub_overrides.css`**, so the override file (loaded LAST, !important everywhere) is the effective specification for the EPUB build. The base `book.css` web rules are largely neutralized for the EPUB.

## Per-Element Analysis

| Element class | Type | Atomic in EPUB? | Made atomic by | Recommend | Notes |
|---|---|---|---|---|---|
| `.callout` (base) | callout | **FLOWING** (correctly) | `epub_overrides.css:1551–1578, 2024–2050` set `page-break-inside: auto !important` + `box-decoration-break: slice`. v789/v790 explicitly forces `display: block`. | Keep flowing | This is the result of v787/v788/v789/v790 sequence after the user reported empty page-bottoms behind tall callouts. |
| `.callout.key-takeaway` | callout | **ATOMIC** | `epub_overrides.css:1061–1067, 1081–1084, 1606–1613` `page-break-inside: avoid !important` | Keep atomic | Always 1-3 lines. Intentional. |
| `.callout.exercise` | callout (tall) | **FLOWING** | Same as base callout | Keep flowing | Often contains long solution `<details>`. v788/v789 explicitly broke it. |
| `.callout.algorithm` | callout (tall) | **FLOWING** | Same as base | Keep flowing | Has pseudocode `<pre>` inside; needs to flow. |
| `.callout.self-check` | callout | **FLOWING** | Same as base | Keep flowing | Quiz blocks can be tall. |
| `.callout.lab` | callout (tall) | **FLOWING** | Same as base | Keep flowing | Multi-step labs. |
| `.callout.looking-back`, `.cross-ref`, `.postmortem`, `.production-pattern`, `.thesis-thread`, `.numeric-example`, `.big-picture`, `.key-insight`, `.note`, `.warning`, `.practical-example`, `.fun-note`, `.research-frontier`, `.tip`, `.library-shortcut` | callout | **FLOWING** | Same as base | Keep flowing | All inherit the v787 fix. |
| `.author-card` | card | **FLOWING** (since v13.15) | `epub_overrides.css:3262–3290` strips all box decoration, sets `page-break-inside: auto`. Old `.author-card { page-break-inside: avoid }` at lines 162, 186, 224, 792, 847, 1082, 1419 is OVERRIDDEN by the later v13.15 block. | Keep flowing | Inline `<style>` in `about-authors.html` sets `display: flex` but `epub_overrides.css:3267` forces `display: block !important`. |
| `.bib-entry-card`, `.bib-entry` | card | **FLOWING** | `epub_overrides.css:3090–3094` `page-break-inside: auto !important` (overrides v786's earlier `avoid` at line 1314) | Keep flowing | Long annotations now flow naturally. |
| `.bib-category` | header | **ATOMIC** (`break-after: avoid`) | `epub_overrides.css:3078–3088` `page-break-after: avoid` + adjacent rule for first entry | Keep | Category title stays glued to its first entry. Correct. |
| `.chapter-card`, `.chapter-card-header`, `.chapter-card-body` | card | **FLOWING** | No `break-inside: avoid` rule anywhere in `epub_overrides.css`. No `display:flex/grid` either. Pure block layout. | Keep flowing | Index-page cards. |
| `.section-card`, `a.section-card` | card | **ATOMIC** | `epub_overrides.css:2056–2079` `display: flex !important; page-break-inside: avoid !important` | Keep atomic | Each card is small (badge + title + 1-line desc). Atomic is correct. |
| `.comparison-table` (wrapper div) | table wrapper | **FLOWING** (since v13.14) | `epub_overrides.css:3194–3208` `display: block !important; page-break-inside: auto !important` (overrides v792's `display: table` which had made it atomic). Inner `<table>` keeps `display: table`. | Keep flowing | Critical fix; previously caused page-jumps. |
| `.comparison-table-title` | header | **ATOMIC** | `epub_overrides.css:2312–2318` `break-after: avoid-column !important` (binds title to table) | Keep | Correct: keeps title with table. |
| `.complex-table` | table | **FLOWING** | `epub_overrides.css:2632–2642, 3201–3208` `page-break-inside: auto !important` | Keep flowing | Rows still atomic. |
| `.diagram-container` | figure | **ATOMIC** | `epub_overrides.css:840–849` `page-break-inside: avoid !important` (under "PAGE-BREAK CONTROL" v783 block) | **Recommend MAKE FLOWING** | Diagrams with very tall SVGs (>1 page) cause page-jumps. The v13.9 fix capped images at `90vh` but the WRAPPER `.diagram-container` is still atomic. With cap intact, atomic is fine; if cap fails, atomic causes ghost pages. **LOW priority.** |
| `.illustration`, `figure.illustration` | figure | **ATOMIC** | `epub_overrides.css:661–664, 840–849, 1076–1084, 1601–1613` `page-break-inside: avoid !important` (figure, .figure, .author-card all in same rule) | **Recommend MAKE FLOWING** for figures with long captions | A figure with a long multi-paragraph caption + tall SVG can exceed page height. **MEDIUM priority** if any such figure exists. With v13.9's 90vh image cap most are safe. |
| `figure` (raw) | figure | **ATOMIC** | Same as `.illustration` | Same recommendation | |
| `.epigraph`, `blockquote.epigraph`, `figure.epigraph` | callout-like | **FLOWING** | No `break-inside` rule. The earlier `figure { page-break-inside: avoid }` block at line 661 targets `figure.epigraph` as a side effect → mildly atomic. | **MAKE FLOWING** explicitly | Long epigraphs (multi-paragraph quotes from a 9th edition Wave A) become atomic via the `figure` rule. **HIGH priority.** Excluded explicitly in proposed fix. |
| `.whats-next`, `div.whats-next`, `.callout.whats-next` | callout | **FLOWING** | `epub_overrides.css:1246–1257` `page-break-inside: auto !important` | Keep flowing | Correctly fixed in v786. |
| `.prereqs`, `.prerequisites`, `.objectives`, `.overview` | callout-like | **FLOWING** | No `break-inside: avoid` rule. Plain `padding/margin` only. | Keep flowing | Correct. |
| `.takeaways` | callout-like | **FLOWING** | No `break-inside: avoid` in override. The base `book.css:2107` styles it but no atomic property. | Keep flowing | Correct. |
| `.code-block-wrapper`, `pre`, `.callout pre` | code | **FLOWING** (since v787/v788) | `epub_overrides.css:1483–1508, 1645–1688` `page-break-inside: auto !important` + `box-decoration-break: slice` | Keep flowing | The v787/v788 chain explicitly broke the v783 avoid rule for code. |
| `.code-collapse`, `.exercises-container`, `.lab-collapse`, `.scenario-collapse`, `.bib-collapse`, `.selfcheck-collapse`, `.output-collapse` | `<details>` wrapper | mixed | `epub_overrides.css:1127–1130` `details { page-break-inside: avoid !important }` for `.exercises-container > details`. Generic `<details>` has no rule. | Keep | Short summaries are fine; inner long content is broken by sub-rules. |
| `tr`, `thead`, `tbody`, `tfoot` | table row | **ATOMIC** | `epub_overrides.css:1543–1545, 1703–1708, 2304–2308, 2644–2651` `page-break-inside: avoid !important` | Keep atomic | Half-rows look broken. Correct. |
| `.chapter-header` | header banner | **ATOMIC** | `epub_overrides.css:1076–1084, 1606–1613` `page-break-inside: avoid !important` | Keep atomic | Small navy band, intentional. |
| `.header-nav`, `.chapter-nav`, `.header-search`, `.toc-toggle`, `.toc-link`, `.book-title-link`, `.toc-icon`, `.author-links`, `body > footer` | site chrome | `display: none` | `epub_overrides.css:59–64, 1153–1183, 1622–1634` `display: none !important` | n/a | Hidden in EPUB. |
| `.wisdom-council-grid`, `.toc-grid`, `.chapter-cards`, `.dense-part`, `.course-grid`, `.intro-sections`, `.pathway-grid`, `.pathway-diagram`, `.pathway-row`, `.fm-cards`, `.fm-grid`, `.cards-grid` | grid wrapper | **FLOWING** | `epub_overrides.css:200–202, 381–388` `display: block !important` (single column) | Keep | Grid stripped, children flow. |
| `.pathway-box`, `.fm-card`, `.pathway-card` | card | **ATOMIC** | `epub_overrides.css:390–397` `page-break-inside: avoid` | Keep atomic | Small cards (one short label). |
| `.math-block`, `.katex-display` | math | **FLOWING** | `epub_overrides.css:1742–1763` `min-height: 0`, no `break-inside: avoid` since v789. (book.css `:625` `page-break-inside: avoid` is overridden) | Keep flowing | Caveat: `book.css` line 625 sets `avoid` but the later v789/v801 rules don't include `break-inside`, so the base rule may still apply through cascade. **LOW priority.** |
| `.takeaway-next` | sticky note | unspecified | No atomic rule | Keep flowing | Small block. |
| `.dataset-card`, `.model-card`, `.template-card` | small card | unspecified | No `break-inside: avoid` rule in either file | Keep flowing | Correct. |
| `.lab-step` | sub-card | **FLOWING** | `epub_overrides.css:1929–1942` `display: block !important; height: auto !important` | Keep flowing | v789 fix. |

## Inline `<style>` in `front-matter/about-authors.html`

Sets `.author-card { display: flex }` (atomic in some readers). Overridden by `epub_overrides.css:3267 display: block !important` for EPUB build. Web-only impact; safe.

## Summary

- **Total block-level element classes analyzed**: 60+
- **Atomic (page-break-inside: avoid) in EPUB**: ~15 classes (`.callout.key-takeaway`, `.section-card`, `tr/thead/tbody`, `.chapter-header`, `figure`, `.figure`, `.illustration`, `.diagram-container`, `.pathway-box`, `.fm-card`, `.pathway-card`, `.bib-category` (break-after), `.comparison-table-title` (break-after), `details` inside `.exercises-container`).
- **Flowing (page-break-inside: auto)**: ~30 classes — all callouts, code, tables, author cards, bib entries, what's-next, prereqs, objectives, overview, takeaways, math, chapter/lesson cards.
- **Incorrectly atomic (should-flow but doesn't)**: 2 — `figure.epigraph` (via `figure` rule), `.illustration` with tall captions. Plus 1 possibly stale: `.math-block` (if book.css cascade still bites).

## Top 5 Problematic Elements

1. **`figure.epigraph`** (HIGH): atomic because the generic `figure { page-break-inside: avoid }` at `epub_overrides.css:661` catches it. Long multi-paragraph epigraphs jump to next page. **Fix**: explicit `figure.epigraph, .epigraph { break-inside: auto }`.
2. **`.illustration`** with multi-paragraph `figcaption` (MEDIUM): same root cause. When `figcaption` is long, the figure exceeds page height. **Fix**: allow break, keep image+first-paragraph-of-caption glued via `figcaption { page-break-before: avoid }`.
3. **`.diagram-container`** (LOW): atomic and contains potentially tall SVG. v13.9 caps to 90vh, so usually fine. Add `break-inside: auto` defensively.
4. **`.math-block`** (LOW): `book.css:625` says `avoid`; `epub_overrides.css` does NOT override break-inside for `.math-block` explicitly, so the base rule may apply via cascade. Long aligned-equation blocks may jump.
5. **Inline `<style>` `.author-card { display: flex }`** in `about-authors.html` (LOW, EPUB-safe but web-relevant): atomic in browsers. Already overridden for EPUB.

## Recommended CSS Fix Priority List

1. (HIGH) Explicitly allow break on `figure.epigraph`, `.epigraph`, `blockquote.epigraph`.
2. (MED) Add `break-inside: auto` to `.illustration` and tighten so only the `<img>` (already capped at 90vh) stays atomic, but the `figcaption` flows.
3. (LOW) Add `break-inside: auto` to `.math-block` to nullify the inherited `book.css:625` rule.
4. (LOW) Add `break-inside: auto` to `.diagram-container`, since the inner `<img>`/`<svg>` are already 90vh-capped.

Proposed CSS in `_fix_v13_16_reflow.css`.
