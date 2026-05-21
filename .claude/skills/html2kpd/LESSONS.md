# Lessons learned: HTML to KPF

Extracted from many KPV-iteration cycles (versions 6.10 through 13.15) on
production technical books. Each lesson is a specific failure mode that
cost hours to diagnose, with the production fix.

## Math rendering

### 1. Render math as MathML, not KaTeX HTML

KaTeX has two output modes:

- `htmlAndMathml` (default): emits both HTML (with `<span class="strut">`,
  `vlist`, `pstrut`, `mspace` — ~400 empty layout spans per chapter) AND
  MathML, with CSS hiding one.
- `mathml`: emits only `<math>...</math>` with no layout helpers.

For Kindle, force `output: 'mathml'`. The HTML mode creates visible tofu
boxes (Kindle paints empty inline spans with `height:` styles as visible
rectangles) AND ignores inline `vertical-align`, so inline math floats
above the surrounding baseline. The MathML path is structurally clean.

Also: strip `<annotation>` tags after KaTeX renders. KaTeX puts raw TeX
inside `<annotation encoding="application/x-tex">` as a fallback. If Kindle
falls back from MathML to text, this would display "(x_1, x_2, T)" inline.

Declare `properties="mathml"` on chapter manifest items (epubcheck OPF-014).

### 2. Math dot alignment: replace U+22C5 with U+00D7

KaTeX emits U+22C5 DOT OPERATOR for `\cdot`. EPUB reader fonts often render
this glyph at baseline, looking like a period. U+00B7 MIDDLE DOT helps in
some fonts but not all. The most reliable fix is U+00D7 MULTIPLICATION SIGN
which is in Latin-1 and is positioned correctly in every font (it is a 2D
cross at middle).

Mathematical equivalence: `a · b = a × b` for scalar multiplication. Chain
rule, gradients, dot product all use × commonly in textbooks.

Apply to all `<mo>`, `<mi>`, `<mn>`, `<mtext>` elements containing the dot.

### 3. Empty `<p style="text-align:center">` wrapper around math-block

Pattern in source HTML:

```html
<p style="text-align: center; margin: 1em 0;">
  <div class="math-block">...</div>
</p>
```

HTML5 parser auto-closes the `<p>` before the `<div>` (because `<p>` cannot
contain block elements). Result: the opening `<p style=...>` becomes a
standalone empty paragraph above the math, and the closing `</p>` becomes
orphaned text after the math (rendered as visible `</p>` literally in some
readers).

Fix: pre-build regex pass to strip `<p style="...text-align..."\s*>` that
directly precedes `<div class="math-block">`, and the matching `</p>` that
follows `</div>`.

### 4. KaTeX msub/msup with function-application invisible char

When `\max`/`\min`/`\sup`/`\inf` is used as a subscript (e.g. `D_{\max}`),
KaTeX emits a trailing `<mo>&#x2061;</mo>` (function application, invisible)
INSIDE the `<msub>`. This violates the MathML schema (msub takes exactly
2 children) and triggers epubcheck RSC-005.

Strip invisible operators (U+2061..U+2064) when they appear as direct `mo`
children of `msub`/`msup`/`msubsup`.

### 5. Empty mtable columnspacing triggers RSC-005

`\begin{aligned}` emits `<mtable columnspacing="">` (empty value) which
fails epubcheck RSC-005 (`columnspacing` must match the mathlength regex).

Strip empty-string layout attributes:

```python
for attr in ('columnspacing', 'rowspacing', 'columnalign', 'rowalign'):
    v = mtable.get(attr)
    if v is not None and not v.strip():
        del mtable[attr]
```

### 6. Multi-line display math needs `\begin{aligned}` wrap

`$$ ... \\\\ ... \\\\ ... $$` blocks render as one wide MathML expression
(KaTeX treats `\\\\` as a hint, not a forced break). Auto-wrap at the
renderer:

```python
if r'\\' in tex and not has_aligned_env(tex):
    tex = r'\begin{aligned}' + insert_amp_before_eq(tex) + r'\end{aligned}'
```

Apply the same rewrite to source HTML so web KaTeX (auto-render) benefits.

### 7. Inline MathML breaks line flow; selectively convert to HTML sub/sup

Some EPUB readers (Calibre, Apple Books KFX) treat inline `<math>` elements
as block-level, forcing inline math like `p_i` onto its own line. For
simple inline patterns convert to plain HTML:

```
<math><mrow><mi>K</mi></mrow></math>                  -> K
<math><mrow><msub><mi>x</mi><mi>i</mi></msub></mrow></math>  -> x<sub>i</sub>
<math><mrow><msup>...</msup></mrow></math>            -> x<sup>2</sup>
<math><mrow><msubsup>...</msubsup></mrow></math>      -> x<sub>i</sub><sup>2</sup>
```

Walk inside `<mrow>`. Accept `<mi>`/`<mn>`/`<mo>`/`<ms>`/`<mtext>` as token
leaves; recursively handle `<msub>`/`<msup>`/`<msubsup>`/`<mfrac>` (as
`a/b`)/`<msqrt>` (as `√x`). Bail to MathML if the pattern is more complex.

The replacement is `<span class="inline-math">` with HTML `<sub>`/`<sup>`.
CSS makes it render at proper baseline with italic font.

### 8. Strip `<semantics>` wrappers

KaTeX MathML wraps content in `<semantics>` (alternative-representation
container). Once you have stripped `<annotation>`, `<semantics>` contains
only one `<mrow>` child. Some EPUB readers render `<semantics>` as block.
Unwrap it: move children up into `<math>` directly.

### 9. .vlist-s spans paint as visible tofu

KaTeX inserts `<span class="vlist-s">&#x200b;</span>` (ZWSP) for vertical
alignment. CSS `visibility: hidden` is ignored by Kindle. Stripping just
the ZWSP is not enough either, because the now-empty `<span class="vlist-s">`
is `display:table-cell; min-width:2px` and Kindle paints that 2px cell as
a tiny visible square.

Final fix: `decompose()` every `.vlist-s` span entirely. Their only purpose
was web vertical alignment which Kindle does not honor anyway. Run AFTER
`math_render.render()` so KaTeX does not re-add them.

## Tables

### 10. Tables must flow: `display: block` on the wrapper

A common bug pattern: an early CSS revision set `.comparison-table {
display: table }` on the WRAPPER div, making it atomic. CSS `display:
table` cannot split across pages. Long comparison tables get pushed to a
fresh page, leaving half the previous page empty.

Fix: wrapper divs go back to `display: block`. Only the inner `<table>`
elements stay `display: table` (correct tabular layout). Combined with
`break-inside: auto`, tables can flow.

```css
div.comparison-table,
div.complex-table-wrap,
div.table-wide-wrap {
    display: block !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
}
table,
.complex-table,
.comparison-table > table {
    display: table !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
}
```

### 11. Wide tables: 6+ cols overflow Kindle (sometimes 4+)

In a 600px Kindle column, a 6-column table needs 100px per column including
padding and borders. Anything narrower wraps every cell to multi-line.

Production heuristic: tag tables with >=4 cols as "wide" and wrap in a
`.table-wide-wrap` div. Apply CSS to reduce font size to 0.78em and tighten
padding to 0.25em 0.4em on wide tables.

For >=6 cols, consider rotating the table layout or splitting into multiple
narrower tables in source.

### 12. Tables with images / code blocks inside

Audit for `<table>` containing `<img>` or `<pre>`. These almost always
overflow Kindle width because the image/code has its own width constraint
that competes with table cell width.

Fix in source: extract the image/code BELOW the table with a caption "see
table above"; reference it inline.

### 13. Tables with rowspan/colspan

Kindle's renderer supports rowspan/colspan but renders quirks: merged
cells sometimes get drawn outside the table border, or text overflows on
narrow viewports. Audit and prefer "flat" tables where possible.

### 14. Math inside table cells

Math inside `<td>` reflows oddly: inline math may break to a new line in
the middle of a sentence within a cell, or MathML may render as block
forcing the cell to expand vertically.

Audit for `<span class="math">` or `<div class="math-block">` inside any
`<table>`. Either move the math outside the table, or convert to a simple
HTML expression (e.g. `K=128` instead of `<math><mi>K</mi><mo>=</mo>...`).

## Navigation

### 15. Navigation chains break after section renumbering

Every time sections are moved or merged, the `<nav class="chapter-nav">`
block in each section becomes stale. Common patterns:

- `28.2.next` -> 28.1 (loop)
- `28.3.next` -> 28.6 (skip)
- `28.6.next` -> 28.4 (backwards)
- `28.9.next` -> module-29 (skips 28.10-12)
- `T.1.prev` -> ../appendix-s/section-s.5 (cross-module backwards)

Fix: rebuild chains sequentially based on actual file numerical order.
`section-N.1.html: prev=index.html, next=section-N.2.html`. For the last
section, next points to the next module's index.html (computed from
sibling-dir order, with letter-length sort for appendices so `a < b < ...
< z < aa < ab < ...`).

Audit: for each `<nav>`, check (a) prev/next/up target files exist; (b)
reciprocity (A.next = B implies B.prev = A).

### 16. Cross-part/cross-appendix transitions

When module 28 (last in part-7) reaches its last section, the next link
should point to part-8/module-29/index.html. After cross-part moves, these
get stale.

For appendix sequences, use length-then-lex sort: `appendix-a`,
`appendix-b`, ..., `appendix-z`, `appendix-aa`, `appendix-ab`. NEVER
plain lex sort (which would put `appendix-aa` before `appendix-b`).

## Index cards (chapter overview pages)

### 17. Phantom cards: duplicate hrefs in `<a class="section-card">` lists

After section consolidation, `module-XX/index.html` keeps OLD cards
pointing to the NEW (consolidated) files. Result: multiple cards with the
same href but different titles. The reader sees three "Section 28.1" cards
each labeled differently, all opening the same page.

Fix: for each href group in cards, keep only ONE card: the one whose
title matches the actual target file's `<h1>`. If no match, keep first and
log.

Dedup by RESOLVED href, not raw href. `./section-28.6` and
`../module-28/section-28.6` resolve to the same file.

### 18. Trailing `<div class="section-grid">` cards

Some modules have a supplementary `<div class="section-grid">` at the
bottom of `index.html` with cards that mostly duplicate the main
`<ul class="sections-list">`. Consolidate: for each grid card, if its
resolved href is already in the main list, drop the grid card; otherwise
move it into the main list, wrapped in `<li>`.

### 19. Sort section cards after dedup

Parse `<span class="section-num">28.3</span>` text. Sort by `(chapter,
section)` tuple. Handle alpha prefixes: "S.4" -> `(0, 4)`; "AB.5" ->
`(0, 5)`. Reorder `<li>` children in `<ul>` accordingly.

### 20. Normalize hrefs (drop `../module-XX/` self-prefix)

When a card in `module-28/index.html` points to `../module-28/section-28.6`,
strip the prefix to `section-28.6`. Cosmetic but reduces noise in diffs
and makes hrefs more portable.

## Section card layout

### 21. `min-width: 12em` on `.section-title` breaks the wrap

The section card is `<a class="section-card"><span class="section-num">S.1</span>
<span class="section-title">vLLM Production Serving</span></a>`. If
`.section-title { min-width: 12em }` forces the title element to be at
least 12em wide, and the row width is less than `2em (badge) + 12em (title)
+ padding`, the title wraps to a new line BELOW the badge:

```
S.1
vLLM Production Serving
```

instead of:

```
S.1 vLLM Production Serving
```

Fix: `min-width: 4em` and `flex: 1 1 0` (was `1 1 auto`) so the title
shrinks to fit alongside the badge with internal text wrap.

## Author bio cards

### 22. Drop the box decoration entirely on Kindle

Author cards designed for the web (border, background, padding, photo
beside text via flex) often look bad on Kindle:

- Kindle Paperwhite strips background colors.
- Flex layout falls back to block on older Kindles, so the photo and
  bio stack vertically with awkward spacing.
- The box decoration creates a visual "atomic boundary" that some
  renderers refuse to break across pages, even with `page-break-inside:
  auto`. The bio gets trapped on one page while the photo is alone on
  the previous page.

Best pattern: strip ALL box decoration in EPUB CSS. Display as plain text
flow with the photo floated left:

```css
.author-card {
    display: block !important;
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0.6em 0 1.5em 0 !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
    overflow: visible !important;
}
.author-card .author-photo,
.author-card > img:first-child {
    float: left !important;
    margin: 0.2em 1em 0.4em 0 !important;
    width: 120px !important;
    max-width: 30% !important;
    height: auto !important;
}
.author-card::after {
    content: "" !important;
    display: block !important;
    clear: both !important;
}
```

This guarantees the bio appears immediately after the heading and splits
naturally at paragraph boundaries.

## Code blocks

### 23. Strip leading/trailing blank lines in `<pre><code>`

Source HTML often has:

```html
<pre><code>
import re
class X:
    ...
</code></pre>
```

The first newline after `<code>` renders as a blank line at the top of the
code block, making it look "over-indented" / having visible whitespace.

Build-time fix: walk every `<code>` block. If the first child is a
`NavigableString` starting with whitespace ending in `\n`, strip the
leading whitespace through and including `\n`. Same for trailing. Preserves
internal indentation.

Works on plain `<code>` blocks AND Pygments-highlighted blocks (where the
first/last child may be a NavigableString containing just `\n`).

### 24. Pygments lang-X vs language-X prefix

Source HTML may use either convention (`<code class="language-python">` or
`<code class="lang-python">`). Auto-detect by trying BOTH prefixes when
matching Pygments lexers. Some books accumulate both conventions over years.

Bug pattern: skipping `lang-*` and only handling `language-*` silently
leaves entire sections un-highlighted (e.g. section 0.3.7.1 stays as plain
gray text instead of syntax-highlighted Python).

### 25. Don't over-dedent code blocks

A feature that "removes common leading whitespace" sounds nice but breaks
KPV in subtle ways. The text manipulation can introduce invisible
whitespace nodes that mismatch the surrounding XHTML structure, producing
E21018 errors.

Production decision: leave the dedent hook DISABLED. If a code block has
"too much indent" because it was extracted from a deeply nested function,
fix it at the source-HTML level, not in the build pipeline.

### 26. Wide code blocks (>100 char lines)

Kindle's narrow column overflows on long code lines. Options:

(a) `pre { white-space: pre-wrap }` to force wrap. Breaks code formatting
    (Python indentation becomes meaningless when continuation lines start
    at column 0).
(b) Source-edit the widest blocks to add line continuations (`\` for
    Python, backslash-newline for shell).
(c) Accept horizontal-scroll behavior (most Kindle readers do not provide
    horizontal scroll, so this means clipping).

For >100-char lines audit and pick (b) selectively for the worst offenders.

## CSS sanitization (post-build)

### 27. The Kindle CSS sanitizer must REPLACE, not DELETE

KDP's CSS parser rejects many modern properties. Approach: don't delete
declarations (breaks CSS syntax); replace VALUES with safe defaults.

Rules:
- `\d+(\.\d+)?rem` -> `\1em` (root font-size is null in many KFX contexts,
  resolving rem to "nullem" — replacing the unit makes value compute from
  local font-size, which Kindle handles)
- `nullem` / `nanem` / `undefinedem` -> `0`
- `min-content` / `max-content` / `fit-content` -> `auto`
- `box-shadow: ...` (any prefix) -> drop the declaration entirely (leaving
  `box-shadow: none` still triggers KDP's "unsupported" warning)
- `gap: ...` / `row-gap` / `column-gap` -> drop the declaration
- `min(...)` / `max(...)` / `clamp(...)` -> keep first argument
- `transition` / `transform` / `filter` / `animation` -> set value to `none`
- Negative margins on tables -> `0`
- `caption-side: ...` -> drop entirely

After replacement, collapse stray `;;` and `{;`. CSS-only — running this on
HTML mangles entity references like `&quot;}` -> `&quot}` causing fatal
RSC-016.

### 28. HTML `<details>/<summary>` -> div shim

Kindle does not support disclosure widgets. Pre-build pass:

```
<details>...</details>  -> <div class="details-shim">...</div>
<summary>X</summary>    -> <p class="details-title"><strong>X</strong></p>
```

Add CSS: `.details-shim { border: 1px solid #ccc; padding: 0.5em; }`.

The shim renders content always-expanded (since Kindle has no disclosure).
Acceptable tradeoff.

## Image format

### 29. PNG to JPEG for binary-alpha PNGs

Many "RGBA" PNGs from matplotlib / Mermaid have alpha=255 everywhere
(opaque on white background). The pipeline trusts color-mode tags and
ships these as PNG when JPEG is fine. Saves ~50% size.

Detection: `Image.open(path).getchannel('A').getextrema() == (255, 255)`.
If true, flatten and re-encode as JPEG.

### 30. OPF rewrite after PNG to JPG conversion

When the post-processor renames `foo.png` -> `foo.jpg`, it must update
BOTH the `<item href>` AND the `media-type` attribute in `content.opf`.

CRITICAL gotcha: OPF references are RELATIVE (e.g. `styles/icons/foo.jpg`)
but ZIP entries are ABSOLUTE (e.g. `EPUB/styles/icons/foo.jpg`). Build the
rename map keyed by the OPF-relative form, OR try both forms when matching.

Without this, every converted file emits an OPF-029 mismatch error in
EPUBCheck.

### 31. SVG viewBox must be camelCase

SVG spec requires camelCase `viewBox`. Browsers parsing HTML5 in lenient
mode accept lowercase `viewbox`, but XHTML parsers (which EPUB uses) and
Kindle's strict renderer ignore the misnamed attribute, falling back to
SVG intrinsic size (300x150 default) instead of rendering at full width.

Visible symptom: diagrams clipped from below or sized at the SVG default.

Fix at build time:

```python
for svg in soup.find_all('svg'):
    if svg.has_attr('viewbox') and not svg.has_attr('viewBox'):
        svg['viewBox'] = svg['viewbox']
        del svg['viewbox']
```

Also source-rewrite `viewbox=` -> `viewBox=` to fix the input.

### 32. Strip `style` from `<img>` (E21018)

`<img style="height: auto; max-width: 100%">` trips Kindle Previewer's
enhanced-Mobi parser. Strip ALL inline `style` from `<img>` at build time;
size via class-level CSS.

### 33. Decode HTML entities in `alt` attribute values

`<img alt="A -&gt; B">` survives EPUBCheck but trips KPV's E21018 parser.
The entity-encoded `>` inside an attribute value is parsed strictly. Fix:
replace `->` with Unicode `→` before serialization. The Unicode form is
parsed correctly.

## Self-closing non-void elements

### 34. `<span class="x"/>` breaks Kindle's parser

ebooklib re-parses chapter HTML and serializes via lxml in XML mode, which
writes empty non-void elements as self-closing: `<span class="x"/>`.
Kindle's HTML5 parser interprets `<span/>` as opening-only, swallowing
subsequent text.

Visible symptom: tofu (■) at end of math formulas, missing close-parens,
garbled inline content.

Post-write XHTML pass: regex expand for the non-void element list:
`span|div|p|a|td|th|li|strong|em|b|i|sub|sup|small|code|pre`.

Critical regex bug to avoid: `<(span|...|i)([^>]*)/>` matches `<img/>` as
`<i + mg.../>`. Use the `\s` requirement: `<(span|...|i)(\s[^>]*|)/>`.

Run on chapter HTML files only, NOT OPF/NCX (which legitimately use
self-closing on `<item/>` etc.).

### 35. Entity stripping by html-minifier-terser

epub-optimizer's html-minifier-terser strips trailing `;` from named
entities: `&apos;` -> `&apos`, `&quot;` -> `&quot`. This is valid HTML5
(parsers tolerate it) but breaks XML.

Run a post-optimizer entity-repair pass:

```python
fix_re = re.compile(r"&(apos|quot|lt|gt|nbsp|copy|reg|trade)(?=[^;a-zA-Z0-9])")
text = fix_re.sub(lambda m: f"&{m.group(1)};", text)
```

`&amp;` is intentionally excluded because it is a prefix of many valid
entity names.

## CSS layout for Kindle

### 36. Overflow: hidden traps Kindle pagination

Web design uses `overflow: hidden` on `.code-block-wrapper`, `.callout`,
`.comparison-table` for rounded-corner clipping. Kindle treats this as
"must fit on one page" — long blocks get pushed to a fresh page leaving
half the previous page empty.

EPUB CSS override: `overflow: visible !important` + `page-break-inside:
auto !important` + `box-decoration-break: clone` so border and background
repaint cleanly across page fragments.

ALSO override the `@media print { .callout { break-inside: avoid } }` rule
the web stylesheet may declare — Kindle's KFX converter honors print media
at conversion time.

### 37. Tooltip pseudo-elements leak as visible text

Book CSS attaches hover tooltips via:

```css
.callout .callout-title::after {
    content: attr(title);
    background: #333;
    color: #fff;
    opacity: 0;
    position: absolute;
}
```

In a browser, opacity hides it until hover. Kindle ignores `opacity` AND
has no `:hover`, so the dark gray tooltip text renders ALWAYS-ON as a
black bar after the title.

Suppress every such tooltip pseudo-element. Common carriers:
- `.callout .callout-title::after`
- `.prereqs h3::after`, `.prerequisites h3::after`
- `.objectives h3::after`
- `.comparison-table-title::after`
- `.exercise-type::after`
- `[title]::after` (defensive)

Force `content: none !important; display: none !important; visibility:
hidden !important; opacity: 0 !important; height: 0 !important; width: 0
!important;`.

### 38. Decorative Unicode icons render as tofu

book.css adds decorative glyphs (U+2696 SCALES, U+26A0 WARNING, etc.)
before various titles via `::before content: "..."`. Many EPUB readers'
bundled fonts lack these glyphs and render them as tofu boxes / "##" /
replacement chars.

Pattern: suppress `::before { content: ... }` on:
- `.comparison-table-title::before`
- `.complex-table-title::before`
- `.callout.thesis-thread::before`
- `.callout.postmortem .callout-title::before`
- `.epigraph cite::before`

The icons are decorative; losing them does not affect comprehension.

### 39. Tall images need max-height to fit one page

Some figures are very tall (e.g. 1299x2151 = 1.66x aspect). With
`max-width: 100%` and aspect-ratio preservation, these expand to a height
greater than page height, causing the bottom to clip at the page boundary
or push to next page leaving empty space.

Cap height at 90vh:

```css
figure.illustration img,
.diagram-container img,
.figure img,
figure img {
    max-height: 90vh !important;
    max-width: 100% !important;
    width: auto !important;
    height: auto !important;
    object-fit: contain !important;
}
```

Also apply to inline `<svg>` (else they overflow narrow EPUB columns).

### 40. Bibliography heading-with-first-card

`.bib-category` heading must stay with its first `.bib-entry-card`.
Otherwise (when the card moves to next page due to `break-inside: avoid`),
the heading is left alone above empty space.

```css
.bib-category {
    page-break-after: avoid !important;
    break-after: avoid !important;
}
.bib-category + .bib-entry-card,
.bib-category + .bib-entry {
    page-break-before: avoid !important;
    break-before: avoid !important;
}
.bib-entry-card,
.bib-entry {
    page-break-inside: auto !important;
    break-inside: auto !important;
}
```

## Section number references

### 41. Stale "Section X.Y" labels after renumber

`section-30.1.html` shows internal TOC labels "32.1.1 through 32.1.12"
because the file was renumbered from 32.1 -> 30.1 but the internal
subsection labels were not updated.

Visible to reader: TOC shows "**32.1.1** OWASP Top 10..." when the section
is actually 30.1.1.

Fix: regex find-and-replace in the file, `32.1.` -> `30.1.` (both in id
attributes and visible text).

Audit pattern: for each `section-N.M.html`, find all `<strong>X.Y.Z</strong>`.
If dominant X.Y prefix does not match file's N.M, flag.

### 42. Stale inline "Section X.Y" references

After cross-ref restructuring, dead `<a>Section X.Y</a>` accumulate where
the original author wrote a domain noun. Bulk-unwrap these but PROTECT
chrome (`h1`, TOC, nav, sidebar, section-card) and intentional preceding
contexts: "see/in/from/of/cf./under/via/covered in/discussed in/introduced
in/presented in/detailed in/explained in/described in/defined in/including
/earlier/later".

The 21-word intentional-preceding regex tuned over multiple audit rounds
correctly preserves intentional uses while unwrapping broken ones.

### 43. Filename-lookup xref repair

When a section/module is moved or merged, ALL inbound `<a href>` paths
silently break. Don't maintain a redirect map by hand. Build a
`{filename: actual_disk_path}` index, then walk every href, resolve it
relative to its parent dir, check if it exists, and if not look up the
filename in the index. The unique-filename hit rate is ~95%; the rest are
truly deleted (and should be unwrapped to plain text).

## Build sequencing

### 44. PYTHONPATH for project plugins is non-negotiable

When invoking `python -m html2pub` from project root, the project's
`_html2pub_hooks.py` is NOT importable unless its directory is on
`PYTHONPATH`. The "[warn] No module named '_html2pub_hooks'" can be
silently swallowed in batch output, leaving every project hook a no-op
without anyone noticing.

Two fixes:
1. `publish.py` sets `PYTHONPATH=KDP/build` before invoking.
2. `builder.py` HARD-FAILS when the hook cannot load (instead of warning).

### 45. Hook order: math_render BEFORE post_process_html

The project hook cleans up KaTeX artifacts (ZWSP, vlist-s spans, etc.)
that only exist AFTER math_render has run. Reverse order = no-op cleanup.

### 46. Metadata sync between yaml and toml

If the project keeps publication metadata in BOTH `KDP/metadata/metadata.yaml`
AND `html2pub.toml`, they drift. KDP detects the wrong edition or stale
publication date.

Pre-build check: verify `publication_date`, `identifier`, `edition`,
`rights` match between the two files. Hard-fail on drift.

## Pagefind integration (web-only)

### 47. `data-pagefind-meta` must live INSIDE indexed body

Common bug: putting `data-pagefind-meta="part"` on a `.part-label` div
inside `<header class="chapter-header">` while the header is in Pagefind's
`exclude_selectors`. Pagefind drops the whole subtree and the metadata
never reaches the index.

Fix: inject hidden `<span data-pagefind-meta="part:..." hidden>` spans
inside `<main class="content">` where indexing is active.

### 48. Pagefind UI escapes HTML in result.meta.title

Only its own internal `<mark>` highlights survive. If you want a custom
prefix on each result, use plain text with a unicode separator (e.g.
`[Part 2 › Ch 6] Title`), NOT a styled `<span>`. The `<span>` ships as
visible markup like `<span class==>`.

## Image recompression cache (v14.1)

### 49. Content-addressed cache for MozJPEG / OxiPNG

Recompressing every image on every build wastes 60-180 seconds when most
images are unchanged across rebuilds. Add a SHA-256 content-addressed
cache:

```python
CACHE_ROOT = Path.home() / "Tools" / "img-tools" / "cache" / "recompress"
ARGS_FINGERPRINT = hashlib.sha256(
    ("mozjpeg|" + "|".join(MOZJPEG_ARGS)).encode()
).hexdigest()[:8]

def cache_key(input_bytes: bytes, fmt: str) -> str:
    h = hashlib.sha256(input_bytes).hexdigest()
    return f'{h}.{ARGS_FINGERPRINT}.{fmt}'
```

Key safety properties:
- Hash is of INPUT bytes — filename-independent. Renaming an image
  doesn't invalidate.
- Tool-args fingerprint appended to key — changing MozJPEG quality
  from 82 to 78 invalidates all cached JPEGs automatically.
- Output is byte-for-byte the optimized result; restore by writing
  cache bytes back to disk.
- Best-effort cache write — failure (disk full, permissions) doesn't
  break the build.

Track hit/miss stats and report them:

```
cache:   145 hits / 12 miss (92% hit; jpg=86/8, png=59/4)
```

92% hit on a steady-state book saves ~90s per build.

## Reflow CSS (v13.16)

### 50. Figure/illustration wrappers atomic by default

The generic `figure { page-break-inside: avoid }` cascade makes all
figures atomic. For multi-paragraph epigraphs wrapped as
`<figure class="epigraph">`, this causes page jumps when the quote
exceeds page height.

Strategy: WRAPPER FLOWS, INNER STAYS ATOMIC.

```css
.epigraph, blockquote.epigraph, figure.epigraph,
.illustration, figure.illustration, figure,
.diagram-container, .math-block {
    page-break-inside: auto !important;
    break-inside: auto !important;
    box-decoration-break: slice !important;
}
.illustration > img, .illustration > svg,
figure > img, figure > svg,
.diagram-container > img, .diagram-container > svg {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
figcaption {
    page-break-before: avoid !important;
    page-break-inside: auto !important;
}
.katex-display, math[display="block"] {
    page-break-inside: avoid !important;
}
```

Logic: image / SVG / single rendered formula stays whole (capped at
90vh so it always fits). The surrounding figure wrapper allows page
breaks so multi-paragraph content above + below splits naturally.

## Code block whitespace at build time vs source

### 51. Strip leading/trailing blanks via build hook

238 source code blocks had a leading `\n` after `<code class="...">` —
this renders as a visible blank line at the top of every `<pre>`. Three
options:

1. **Source fix** (manual): edit every file to remove the newline.
   Survives rebuilds. Touches 238 files in the diff.
2. **Build hook** (automatic): post-process the HTML at build time.
   Source unchanged; only the EPUB output is clean.
3. **Both**: source fix removes the visual artifact in browser too,
   build hook catches any new instances introduced later.

Production: option 3. Source fix via surgical regex (NOT BeautifulSoup
— it re-quotes attributes everywhere) targeting only the bytes after
`<code\b[^>]*>`:

```python
PATTERN_LEADING = re.compile(r'(<code\b[^>]*>)(\s*\n)+', re.DOTALL)
PATTERN_C1_SPAN = re.compile(
    r'(<code\b[^>]*>)<span class="c1"></span>\n', re.DOTALL
)
```

Two patterns because Pygments sometimes emits `<span class="c1"></span>`
as the first child of `<code>` for blocks that start with a blank
"comment line".

Build hook for catch-all:

```python
def strip_code_block_whitespace(soup):
    for code in soup.find_all('code'):
        first = list(code.children)[:1]
        if first and isinstance(first[0], NavigableString):
            s = str(first[0]).lstrip(' \t\n\r')
            if not s:
                first[0].extract()
            else:
                first[0].replace_with(NavigableString(s))
```

## Audit scripts for ongoing quality

### 52. Re-runnable audit scripts catch regressions

Each fix lesson above should ship with an audit script that detects the
issue. Production set:

- `audit_navigation.py` — prev/next chain integrity, reciprocity
- `audit_phantom_cards.py` — duplicate hrefs in index pages
- `audit_math_kpv.py` — math-in-p, math-in-table, deeply-nested mfrac
- `audit_tables_kpv.py` — wide tables, unwrapped tables, math-in-cells
- `audit_code_indent.py` — leading blank, over/under indent, wide lines
- `audit_stale_refs.py` — Section X.Y where X.Y doesn't exist
- `audit_bibliography.py` — heading consistency, markup pattern
- `audit_reflow.py` — atomic elements that should flow
- `audit_consolidation.py` — duplicated values across files
- `audit_toc_navigation.py` — ToC entries match source files

Run all on every build OR every PR. The 30 seconds total they take is
worth catching the 60 minutes spent debugging "why is this card weird".

### 53. KPV `-convert` CLI is unusable from subprocess on Windows

`Kindle Previewer 3.exe -convert <epub> -output <kpf> -qualitychecks` is
NOT a working headless CLI. It silently returns rc=0 in 100-200 ms while
doing nothing whenever the launching shell is not a foreground interactive
desktop session. This affects:

- Python `subprocess.run([kpv, '-convert', ...])`
- Python `subprocess.run(['cmd', '/c', kpv, '-convert', ...])`
- Python `subprocess.Popen(..., DETACHED_PROCESS)`
- PowerShell `& "kpv" -convert ...`
- PowerShell `Start-Process -FilePath kpv -Wait` (`-Wait` only blocks on the
  parent GUI exe which exits in 140 ms regardless of conversion progress)
- .NET `System.Diagnostics.Process.Start()` with `UseShellExecute=false`
- The `kindlepreviewer.bat` launcher at `%APPDATA%\Amazon\` (same exe call)

The KPV main process is a Qt5/QtWebEngine GUI binary that detects whether
it has a real foreground console (TTY-attached stdin, console buffer, input
focus). Without those, it forks the persistent `KPR_NCD.exe` daemon, exits
rc=0, and never spawns the actual `kindlegen.exe` + `Server_KRF4.exe`
workers that build the KPF. There is no flag, no env var, and no Windows
manifest tweak that bypasses this. The manifest is `asInvoker`, so the
PermissionError [WinError 5] that some Python configs hit is a cmdline
quoting issue, not UAC: but fixing the quoting only changes "loud failure"
into "silent rc=0 with no output".

Specifically:

- No KPF is produced.
- No qualitychecks CSV is produced.
- No log file is produced.
- `%LOCALAPPDATA%/Amazon/Kindle Previewer 3/workspace/` does NOT exist;
  the docs that mention it are wrong. KPV writes the KPF alongside the
  input EPUB and the qualitychecks log as `<epub-stem>-conversionLog.csv`
  in the same directory, but ONLY when conversion actually ran.
- `KPR_NCD.exe` running after a "successful" call is meaningless - it is
  the system-tray daemon and auto-spawns whether or not conversion ran.

What DOES work from subprocess:

- `kindlegen.exe` at `lib/fc/bin/kindlegen.exe` works headlessly and
  writes `<epub-stem>.mobi`. This is the legacy MOBI compiler (V2.9, 2015)
  and does NOT understand MathML (emits `W29007: Rejected unknown tag:
  <math>...<mfrac>...<mi>...<mo>` for every math element). Useful only for
  MOBI scaffold validation, NOT for KPF or modern Kindle rendering.

What DOES work for KPF:

- The user opens a foreground cmd.exe or PowerShell window on their own
  desktop and runs the same command. The GUI window appears, conversion
  takes 30-180 s, KPF lands alongside the EPUB, qualitychecks CSV lands
  alongside as `<stem>-conversionLog.csv`.
- The user double-clicks the EPUB in Explorer.
- The bisect harness at `_kp_bisect.py` worked on 2026-05-11 specifically
  because the user was at the desktop while it ran. Re-running it from
  Claude later produced empty results.

Workflow guidance for automation:

- Build EPUB-only artifacts in CI/scripts. Skip KPV step.
- Print a clear "MANUAL STEP NEEDED" gate at the end of automated builds
  with the exact command for the user to run.
- DO NOT treat KPV's rc=0 as success. Check that `<epub>.kpf` exists AND
  is larger than ~50 KB AND has mtime > start time.
- Detect non-interactive context early (e.g. check `os.environ.get(
  'SESSIONNAME', '') == 'Console'` and `sys.stdin.isatty()`) and skip the
  KPV step entirely rather than pretending it worked.

Investigation log: `KDP/build/KPV_CLI_ANALYSIS.md` (2026-05-15).

### 54. KDP ingestion uses different fixed-layout detection than kindlegen

KDP's web upload pipeline rejected a reflowable EPUB with: "This content
is a fixed format eBook. Updating a reflowable eBook with a fixed format
eBook is not supported." But the same EPUB:

- `<meta property="rendition:layout">reflowable</meta>` in OPF (correct)
- No per-spine `properties="rendition:layout-pre-paginated"`
- No `<meta name="viewport" content="width=..., height=...">` in any XHTML
- kindlegen run with `-verbose` explicitly says `fixed-layout "false"`
- epubcheck 5.1: 0 FATAL / 0 ERROR / 0 WARNING

KDP's web-side heuristic differs from kindlegen's. Known KDP fixed-layout
triggers that are NOT epubcheck or kindlegen errors:

- `cover.xhtml` whose `<body>` contains only an `<img>` (no text, no
  paragraph). KDP may classify the cover spine item as fixed-layout and
  propagate that to the entire book.
- High image-to-text ratio.
- SVG-only XHTML pages anywhere in the spine.
- Large XHTML files (>200 KB compressed) when the surrounding chapters
  are tiny.

What works for diagnosis:

- Run `kindlegen.exe <book.epub> -c2 -verbose -o test.mobi`. The first
  100 lines of output declare `Info(prcgen):I1047: Added metadata
  fixed-layout "false"` if kindlegen agrees the book is reflowable.
- Watch the kindlegen output for `Info(prcgen):I1052: Kindle support
  cover images but does not support cover HTML. Hence using the cover
  image specified and suppressing cover HTML in content.` This is a HINT
  that the cover.xhtml has structure that KDP may dislike.
- The KDP ingestion log is NOT user-visible. Only the web UI's red error
  banner. There is no `-debug` flag for KDP's pipeline.

Mitigation for the cover-as-fixed-layout heuristic: keep cover.xhtml
image-only (it gets stripped by Kindle anyway per I1052), but ensure
the EPUB's OPF and spine clearly mark it as the navigation cover, not
as content. Use the cover JPEG as `<meta name="cover" content="cover-img"/>`
in OPF metadata, and consider not including cover.xhtml in the spine at
all (mark `<itemref idref="cover" linear="no"/>` or omit it entirely if
the EPUB toolchain allows).

---

## L-KPV-CLI. Kindle Previewer 3 headless conversion: argument order + console (2026-05-21)

**The silent-failure trap**: running
`"Kindle Previewer 3.exe" -convert input.epub -output out.kpf -qualitychecks`
exits rc=0 in ~2s and produces NOTHING (no KPF, empty workspace). It looks like
"CLI not supported" but it's just wrong syntax.

**Correct syntax** (input first; `-convert` bare; `-output` is a FOLDER):
```
"Kindle Previewer 3.exe" <input.epub> -convert -output <OUTPUT_FOLDER> -qualitychecks
```
Verified working headlessly. Produces `<out>/KPF/<name>.kpf`,
`<out>/Logs/<name>_log.csv`, `<out>/Logs/<name>_QualityReport.csv`,
`<out>/Summary_Log.csv`. Gate on `Summary_Log.csv` `Error Count`.

**Console gotcha**: do NOT launch via Git Bash/MSYS -- the exe is a Windows
console-subsystem app and the worker `KPR_NCD.exe` can hang at ~0% CPU with no
real console (prints nothing). Use PowerShell `Start-Process -Wait -NoNewWindow`,
`cmd.exe /c`, or a direct Python `subprocess.run` (not through a bash shim).
Kill stale `KPR_NCD.exe` at the start of each run (a ghost worker from a prior
bad launch wedges the next one). CLI exists since KPV v3.32; keep KPV current
(~3.82.x had conversion regressions). A PATH wrapper `kindlepreviewer.bat` is
installed under `%APPDATA%\Amazon\`. `scripts/kpv_convert.py` implements all of
this (corrected 2026-05-21).

**KindleGen is dead** (retired 2020; KDP rejects MOBI). The engine is folded into
KPV3 (`KPR_NCD.exe`), no standalone `kindlegen.exe`. For automation: EPUBCheck-clean
EPUB -> KPV3 headless `-convert -qualitychecks` -> parse Summary_Log.csv -> upload
EPUB (or KPF) to KDP. EPUB upload (Amazon converts to KFX server-side) is a fully
supported fallback. AZW3 (Calibre) is NOT accepted by the KDP web uploader.

---

## L-MATH-PNG. Math: ship PNG, not MathML; and don't let CSS force-`display` MathML (2026-05-21)

**MathML on Kindle is unreliable** -- it renders only under Enhanced Typesetting,
which is silently disqualified by **>25 SVGs**, inline-block tables, fixed layout,
>300 HTML files, or >30MB/file; and even when ET is on, it "renders in Kindle
Previewer but breaks on devices" (documented). For a math-heavy book, **render
equations to PNG** (de-facto STEM-on-Kindle standard).

**CSS bug that broke MathML even in good readers**: `epub_overrides.css` forced
`display:inline !important` on `math, mrow, mi, mn, mo, ...` (plus `math *{overflow}`),
which overrides the UA MathML layout -- `<mfrac>`/`<msub>` stay block while siblings
go inline, so equations stack vertically (confirmed in Thorium/Chromium: 171px broken
vs 45px when removed). NEVER force `display` on `m*` elements; style only `.katex`/
`.math-block` wrappers.

**Automated PNG pipeline** (KaTeX + Playwright; see math2epub LESSONS L13):
`math_render.py` stamps `data-tex` -> build writes `.book-update/math-manifest.json`
-> `scripts/build_math_png_cache.py` renders each LaTeX (KaTeX HTML in Chromium,
3x scale, tight bbox, pngquant) keyed by `sha1(tex|display)` -> `builder.py`
`replace_mathml_with_png()` swaps remaining MathML for `<img>`, adding PNG bytes
straight to `images.bundled_bytes` (bypass `_reencode` so they stay crisp PNG, not
JPEG). Keep simple inline math as `<sub>/<sup>` (scales, matches body). Size via
logical width/height ATTRS (= px/scale) -- Kindle honors width/height attrs but
ignores CSS max-width/height on `<img>`. Result: 0 `<math>`, 293 PNGs ~2.7MB,
EPUBCheck 0 errors.

---

## L-TOC-NUM. Number the EPUB ToC from breadcrumb/page-current, not <h1> (2026-05-21)

The EPUB nav (ToC) is built from each chapter's `<h1>`. If the source keeps section
numbers OUT of `<h1>` (here: in `<div class="page-breadcrumb">`="... Chapter 0" and
`<div class="page-current">`="Section 0.1"), the ToC shows bare titles. Fix: a
post_process hook (`number_headings`) prepends the authored number to `<h1>` ->
"0.1 Title", "Chapter 0: Title", "Appendix A: Title", "A.1 Title". **Gotcha**: merge
the number INTO the first text node, don't `insert(0, NavigableString("0.1 "))` -- the
nav title comes from `h1.get_text(strip=True)`, which strips each node's whitespace
before concatenating, giving "0.1Title". Also don't skip titles by a bare leading
digit (e.g. "3D Generation" must still get its number); only skip real "X.Y "/"Part "
prefixes.

---

## L-SVG-CASE. ebooklib lowercases ALL camelCase SVG attributes on write (2026-05-21)

Symptom: every inline-SVG diagram "not rendered" in Kindle -- the diagram collapses
to a vertical stack of unpositioned `<text>` labels (looks like raw text), and all
arrowheads disappear. EPUBCheck passes (0 errors) and the diagrams look perfect in
Chromium, so it's easy to misdiagnose as an Enhanced-Typesetting/KF8 problem. It is
NOT: it's malformed SVG.

Root cause: SVG attribute names are camelCase (`viewBox`, `refX`, `refY`,
`markerWidth`, `markerHeight`, `markerUnits`, `preserveAspectRatio`, `gradientUnits`,
`stdDeviation`, ...). XHTML/XML is case-SENSITIVE, so a lowercased `viewbox` is simply
an unknown attribute and the SVG has no coordinate system (collapses); lowercased
marker attrs drop every arrowhead. The html2pub `fix_svg_viewbox` post_process hook
DOES restore `viewBox` in the BeautifulSoup tree, and `str(soup)` preserves it -- but
**ebooklib re-parses each chapter's XHTML through lxml's HTML mode when it writes the
EPUB**, and lxml-HTML lowercases every attribute name. So the hook's fix is silently
undone in BOTH the raw and optimized EPUB (raw.epub already shows lowercase).

Diagnosis trick: `zipfile`-scan the built EPUB's xhtml for `viewbox=` vs `viewBox=`.
Our book: 408 `viewbox=` / 0 `viewBox=` after build, despite the hook running (proven
because OTHER hook effects -- numbered `<h1>`, stripped `<img style>` -- WERE present).

Fix: do it on the FINAL EPUB bytes, after ebooklib, in the ZIP-rewrite sanitizer
(`_sanitize_kindle_css.py`). Scope to `<svg>...</svg>` blocks (so escaped
`&lt;svg viewbox=` inside code samples is untouched) and restore the canonical casing
for the whole camelCase attribute set, not just viewBox:
```python
SVG_CAMEL_ATTRS = {"viewbox":"viewBox","refx":"refX","refy":"refY",
  "markerwidth":"markerWidth","markerheight":"markerHeight","markerunits":"markerUnits",
  "preserveaspectratio":"preserveAspectRatio","gradientunits":"gradientUnits",
  "gradienttransform":"gradientTransform","stddeviation":"stdDeviation", ...}
# for each <svg..</svg> block: re.sub(r'(\s)(name)=', camelCase, block)
```
Lesson: any HTML attribute whose canonical form is camelCase (SVG, and MathML's
`definitionURL`) cannot survive an lxml-HTML round-trip. Fix it as a string pass on
the final serialized bytes, never in the parsed tree.

---

## L-DEEP-AUDIT. Validators pass clean; reader-facing issues remain (2026-05-21)

EPUBCheck (0 errors) AND Kindle Previewer qualitychecks (0 errors, 0 quality
issues) can BOTH pass while real problems ship. Add a deep audit
(`scripts/audit_epub_quality.py` + `scripts/deep_scan_epub.py`) over the FINAL
EPUB. Two generalizable issues it caught that no validator did:

1. **Code-OUTPUT blocks leak a blank first/last line.** Output is authored as
   `<div class="code-output">...<pre>\n{...}\n</pre></div>` - a BARE `<pre>` with
   no nested `<code>`. The `strip_code_block_whitespace` hook only walked
   `<code>` elements, so 40 output blocks rendered with a visible blank line top
   and bottom. Fix: also strip leading/trailing whitespace NavigableString
   children of `<pre>` that contain no `<code>` (handle `\r\n` too - 1602 pre
   blocks had CRLF).

2. **Prerequisites box caused an h1->h3 heading skip (379x).** Every section is
   `<h1>title</h1> ... <h3 id="prerequisites">Prerequisites</h3> ... <h2>first
   subsection</h2>` - the prereqs h3 appears before the first h2 => h1->h3 skip
   (accessibility/structure warning). Fix: promote the prereqs heading to `<h2>`
   (it's the page's first top-level section) and change `.prereqs h3` /
   `.prerequisites h3` CSS selectors -> `h2`. 0 skips after.

Audit false positives worth pre-filtering so "0 warnings" stays meaningful:
- CODE-LONG (line >88 chars) is benign when `pre{white-space:pre-wrap}` wraps it.
- TABLE-WIDE (>=5 cols) is benign when already in `.table-wide-wrap`/`.complex-table`.
- INLINE-STY on SVG-internal elements (`<stop stop-color>`, `<rect fill>`) is
  valid SVG, not CSS Kindle strips - skip anything with an `<svg>` ancestor.
- empty `<td>` is a legitimate blank cell.

Wire the audit into publish.py as a gate (`step_quality_audit`, fails on
ERROR-level only). DAISY ACE is a good additional accessibility checker if you
install `@daisy/ace`.
