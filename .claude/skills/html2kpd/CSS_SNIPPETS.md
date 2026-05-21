# Reusable CSS patterns for Kindle / KPF

Copy-paste these snippets into the project's `epub_overrides.css`. Each
fixes a specific class of Kindle layout bug that surfaces during KPV
qualitychecks or visual inspection.

## Table flow (split across pages)

Without this, long tables stay atomic and leave half the previous page
empty. Wrapper must be `display: block`; inner `<table>` stays `display:
table` for correct tabular layout.

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
.comparison-table > table,
table.complex-table {
    display: table !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
}
```

## Wide tables (>= 6 columns, sometimes >= 4)

```css
table.complex-table {
    font-size: 0.78em !important;
    line-height: 1.35 !important;
}
table.complex-table th,
table.complex-table td {
    padding: 0.25em 0.4em !important;
    word-break: break-word !important;
}
```

## Author bio cards (drop the box, float the photo)

The web design (border, background, padding, photo beside text via flex)
fails on Kindle in three ways: Kindle Paperwhite strips backgrounds; flex
falls back to block on older Kindles; the box creates an atomic boundary
the renderer refuses to break across pages. Best pattern: strip ALL box
decoration, float the photo.

```css
.author-card,
.about-authors .author-card,
.about-the-authors .author-card,
.author-cards .author-card,
div.author-card {
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
    display: block !important;
    margin: 0.2em 1em 0.4em 0 !important;
    border: 1px solid #ccc !important;
    border-radius: 4px !important;
    box-shadow: none !important;
    width: 120px !important;
    max-width: 30% !important;
    height: auto !important;
    flex: none !important;
}
.author-card .author-info {
    display: block !important;
    flex: none !important;
    width: auto !important;
    min-width: 0 !important;
}
.author-card h3 {
    margin: 0 0 0.2em 0 !important;
    padding: 0 !important;
    font-size: 1.15em !important;
    line-height: 1.25 !important;
    page-break-after: avoid !important;
}
.author-card p {
    margin: 0 0 0.6em 0 !important;
    line-height: 1.5 !important;
    text-align: justify !important;
}
.author-card::after {
    content: "" !important;
    display: block !important;
    clear: both !important;
    height: 0 !important;
}
```

## Section card layout (badge + title row)

`min-width: 12em` on the title forces it onto a new line below the badge
when the row is narrower than badge + 12em + padding. Use `min-width: 4em`
and `flex: 1 1 0`.

```css
.section-card,
a.section-card,
li > a.section-card,
.section-grid > a.section-card {
    display: -webkit-flex !important;
    display: flex !important;
    -webkit-flex-direction: row !important;
    flex-direction: row !important;
    -webkit-flex-wrap: wrap !important;
    flex-wrap: wrap !important;
    -webkit-align-items: flex-start !important;
    align-items: flex-start !important;
    padding: 0.7em 0.9em !important;
    margin: 0 0 0.5em 0 !important;
    background: #ffffff !important;
    border: 1px solid #d0d7de !important;
    border-left: 4px solid #1a4078 !important;
    border-radius: 0 4px 4px 0 !important;
    text-decoration: none !important;
    color: inherit !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
}
.section-card .section-num,
a.section-card .section-num {
    display: inline-block !important;
    font-size: 0.8em !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    background: #1a4078 !important;
    padding: 0.25em 0.55em !important;
    border-radius: 4px !important;
    min-width: 2em !important;
    text-align: center !important;
    -webkit-flex-shrink: 0 !important;
    flex-shrink: 0 !important;
    margin: 0 0.5em 0.2em 0 !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
    vertical-align: top !important;
    line-height: 1.3 !important;
}
.section-card .section-title,
a.section-card .section-title {
    font-weight: 700 !important;
    color: #1a4078 !important;
    font-size: 1em !important;
    -webkit-flex: 1 1 0 !important;
    flex: 1 1 0 !important;
    min-width: 4em !important;
    line-height: 1.3 !important;
}
.section-card .section-desc,
a.section-card .section-desc {
    display: block !important;
    -webkit-flex-basis: 100% !important;
    flex-basis: 100% !important;
    width: 100% !important;
    margin-top: 0.3em !important;
    color: #455a64 !important;
    font-size: 0.92em !important;
    line-height: 1.45 !important;
}
```

## Display math centering

```css
.math-block,
div.math-block,
.math-display,
div.math-display {
    text-align: center !important;
    padding: 0.4em 0.7em !important;
    margin: 0.5em 0 !important;
    page-break-inside: avoid;
}
.math-block > span,
.math-block > .katex,
.math-block > .katex-display,
.math-block > .katex-rendered,
.math-block > math {
    display: inline-block !important;
    margin: 0 auto !important;
    text-align: left !important;
    max-width: 100% !important;
}
math[display="block"] {
    display: inline-block !important;
    margin: 0 auto !important;
    text-align: left !important;
    vertical-align: middle !important;
}
```

## Inline math (reset block-level baseline)

The global rule that pads `.katex-rendered` for display math also lifts
inline math above baseline. Split inline vs display.

```css
.katex-rendered:not(.katex-display),
span.katex-rendered:not(.katex-display),
span.katex.katex-rendered:not(.katex-display),
.katex:not(.katex-display),
math:not([display="block"]) {
    display: inline !important;
    margin: 0 !important;
    padding: 0 !important;
    vertical-align: baseline !important;
    line-height: inherit !important;
    font-size: 1em !important;
}
.katex-rendered:not(.katex-display) > *,
math:not([display="block"]) > * {
    vertical-align: baseline !important;
    line-height: inherit !important;
}
```

## Inline-math HTML replacement (when MathML is too block-y)

For the `<span class="inline-math"><sub>i</sub></span>` replacement:

```css
span.inline-math {
    display: inline !important;
    white-space: nowrap !important;
    vertical-align: baseline !important;
    font-family: "Cambria Math", "Times New Roman", serif !important;
    font-style: italic !important;
}
span.inline-math sub,
span.inline-math sup {
    font-style: normal !important;
    font-size: 0.75em !important;
    line-height: 0 !important;
}
span.inline-math sub { vertical-align: sub !important; }
span.inline-math sup { vertical-align: super !important; }
```

## Suppress tooltip pseudo-elements

Book CSS often uses `::after { content: attr(title); opacity: 0 }` for
hover tooltips. Kindle ignores opacity, so the tooltip text renders
always-on.

```css
.callout .callout-title::after,
.callout-title::after,
.prereqs h3::after,
.prerequisites h3::after,
.objectives h3::after,
.comparison-table-title::after,
.exercise-type::after,
[title]::after {
    content: none !important;
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0 !important;
    width: 0 !important;
    background: transparent !important;
    color: transparent !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
    position: static !important;
    border: none !important;
}
```

## Suppress decorative Unicode icons (tofu prevention)

```css
.comparison-table-title::before,
.complex-table-title::before,
.callout.thesis-thread::before,
.callout.postmortem .callout-title::before,
.exercises-container > summary.exercises-summary::before,
.epigraph cite::before {
    content: none !important;
    display: none !important;
}
```

## Callouts that flow across pages

Override `overflow: hidden` and `break-inside: avoid` that web design uses.

```css
.callout,
.code-block-wrapper,
.code-block-wrapper > pre,
pre {
    overflow: visible !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-box-decoration-break: clone !important;
    box-decoration-break: clone !important;
    widows: 2 !important;
    orphans: 2 !important;
}

/* Suppress print-media break-inside:avoid the web stylesheet may declare */
@media print {
    .callout, pre, .code-block-wrapper {
        break-inside: auto !important;
        page-break-inside: auto !important;
    }
}
```

## Callout visual identity (defense in depth)

Kindle Paperwhite (e-ink) strips background-color. So use FOUR independent
markers: thick solid border, extra-thick left border, background tint (only
seen on color readers), and a leading unicode symbol prefix.

```css
.callout {
    border: 2px solid #444 !important;
    border-left-width: 8px !important;
    padding: 0.7em 0.9em !important;
    margin: 1em 0 !important;
    background: #fafafa !important;
    border-radius: 0 4px 4px 0 !important;
}
.callout-title {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95em !important;
    margin: 0 0 0.4em 0 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    display: block !important;
    text-align: left !important;
}
/* Suppress icon ::before that may load PNG (often fails to bundle) */
.callout .callout-title::before {
    content: none !important;
    display: none !important;
    background: none !important;
}
/* Per-type unicode symbol prefixes (always visible, no font dependency) */
.callout.big-picture       .callout-title::before { content: "■ "; }
.callout.key-insight       .callout-title::before { content: "★ "; }
.callout.warning           .callout-title::before { content: "▲ "; }
.callout.note              .callout-title::before { content: "▸ "; }
.callout.tip               .callout-title::before { content: "✓ "; }
.callout.practical-example .callout-title::before { content: "❯ "; }
.callout.research-frontier .callout-title::before { content: "◆ "; }
.callout.algorithm         .callout-title::before { content: "§ "; }
.callout.exercise          .callout-title::before { content: "? "; }
/* Per-type colors. Border-left and title color are always-visible. */
.callout.big-picture       { background: #eef4fa !important; border-color: #2a6dba !important; border-left-color: #2a6dba !important; }
.callout.key-insight       { background: #ecf6ee !important; border-color: #1f7a3a !important; border-left-color: #1f7a3a !important; }
.callout.warning           { background: #fdeee8 !important; border-color: #b3401b !important; border-left-color: #b3401b !important; }
.callout.note              { background: #f4f4f4 !important; border-color: #555 !important; border-left-color: #555 !important; }
.callout.tip               { background: #ecf6ef !important; border-color: #237549 !important; border-left-color: #237549 !important; }
.callout.exercise          { background: #fafafa !important; border-color: #444 !important; border-left-color: #444 !important; border-style: dashed !important; border-left-style: solid !important; }
```

## Bibliography styles

```css
.bib-entry-card,
.bib-entry {
    margin: 0.7em 0 !important;
    padding: 0.5em 0.8em !important;
    border-left: 3px solid #aaa !important;
    background: #fafafa !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
}
.bib-ref { font-size: 0.95em !important; }
.bib-annotation { font-size: 0.88em !important; color: #444 !important; margin-top: 0.3em !important; }

/* Heading + first entry must stay together */
.bib-category {
    page-break-after: avoid !important;
    break-after: avoid !important;
}
.bib-category + .bib-entry-card,
.bib-category + .bib-entry {
    page-break-before: avoid !important;
    break-before: avoid !important;
}
```

## Code blocks (light theme for Kindle)

Kindle strips dark backgrounds; many code highlight themes are designed
for dark bg. Force light bg + dark default text so syntax-highlight
tokens are readable.

```css
pre,
pre.pygments-highlighted,
pre[class*="language-"],
.callout pre,
.code-block-wrapper > pre {
    background: #f6f8fa !important;
    background-color: #f6f8fa !important;
    color: #24292f !important;
    border: 1px solid #d1d5da !important;
    padding: 0.7em 0.9em !important;
    border-radius: 4px !important;
    line-height: 1.45 !important;
    font-size: 0.88em !important;
    overflow-x: auto !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
    -webkit-box-decoration-break: clone !important;
    box-decoration-break: clone !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}
pre code, pre.pygments-highlighted code {
    background: transparent !important;
    color: inherit !important;
    padding: 0 !important;
}
:not(pre) > code {
    background: #f3f4f6 !important;
    color: #1f2937 !important;
    padding: 0.1em 0.3em !important;
    border-radius: 3px !important;
    font-size: 0.92em !important;
}
```

## Pygments token colors (light bg)

```css
.highlight, .codehilite { background: transparent !important; }
.highlight .k,  .codehilite .k,
.highlight .kd, .codehilite .kd,
.highlight .kn, .codehilite .kn,
.highlight .kp, .codehilite .kp,
.highlight .kr, .codehilite .kr,
.highlight .kt, .codehilite .kt    { color: #007020 !important; font-weight: bold !important; }
.highlight .s,  .codehilite .s,
.highlight .s1, .codehilite .s1,
.highlight .s2, .codehilite .s2    { color: #4070a0 !important; }
.highlight .c,  .codehilite .c,
.highlight .c1, .codehilite .c1    { color: #808080 !important; font-style: italic !important; }
.highlight .n,  .codehilite .n     { color: #000 !important; }
.highlight .nb, .codehilite .nb    { color: #007020 !important; }
.highlight .nc, .codehilite .nc,
.highlight .nf, .codehilite .nf    { color: #06287e !important; font-weight: bold !important; }
.highlight .nn, .codehilite .nn    { color: #0e84b5 !important; font-weight: bold !important; }
.highlight .o,  .codehilite .o     { color: #666 !important; }
.highlight .p,  .codehilite .p     { color: #555 !important; }
.highlight .m,  .codehilite .m,
.highlight .mi, .codehilite .mi    { color: #208050 !important; }
```

## Image dimensions

```css
/* Generic cap so no image blows out the column */
img {
    max-width: 100% !important;
    height: auto !important;
}

/* Tall images: cap height so they fit one page */
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

/* Inline SVG diagrams: same bounds */
figure.illustration svg,
.diagram-container svg,
.figure svg,
figure svg {
    max-width: 100% !important;
    max-height: 90vh !important;
    width: 100% !important;
    height: auto !important;
    display: block !important;
}
```

## Pathway / front-matter cards: force single column

Web grid `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`
keeps 2 columns at 600px viewport, cramping cards. Force single column.

```css
.pathway-diagram,
.pathway-row,
.fm-cards,
.fm-grid,
.cards-grid,
.pathway-grid {
    display: block !important;
    grid-template-columns: 1fr !important;
}
.pathway-box,
.fm-card,
.pathway-card {
    width: 100% !important;
    max-width: 100% !important;
    margin-bottom: 1em !important;
    page-break-inside: avoid;
}
```

## Headings (reduce top margin for inner pages)

Web design uses `h2 { margin: 3rem 0 1.5rem }` for chapter-scroll
reading. For paginated EPUB, the 3rem top margin pushes content way
down when an h2 lands at the start of a continuation page.

```css
h2 { margin-top: 1.2rem !important; }
h3 { margin-top: 0.9rem !important; }
h4 { margin-top: 0.7rem !important; }
body > main.content > h2:first-child,
body > main.content > h3:first-child,
body > main.content > h4:first-child {
    margin-top: 0 !important;
}
```

## Chapter header (defense in depth)

Background + bold border + per-element color so the header survives
Kindle's background-stripping.

```css
.chapter-header {
    background: #1a1a2e !important;
    background-color: #1a1a2e !important;
    color: #ffffff !important;
    padding: 0.6em 1em 0.8em !important;
    margin: 0 0 1.2em 0 !important;
    border-radius: 0 0 4px 4px;
    border-top: 6px solid #1a1a2e !important;
    border-bottom: 1px solid #c9d3df !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}
.chapter-header,
.chapter-header h1,
.chapter-header h2,
.chapter-header h3,
.chapter-header a {
    color: #ffffff !important;
}
```

## Suppress site chrome

```css
.chapter-nav, .header-nav, .toc-toggle,
.toc-link, .book-title-link, .toc-icon,
.author-links,
.bg-motes, #stars-canvas, .glow-ring {
    display: none !important;
}
```

## Reset animations (Kindle has no animation support anyway)

```css
* {
    animation: none !important;
    transition: none !important;
}
```
