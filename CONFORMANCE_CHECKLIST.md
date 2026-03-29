# Conformance Checklist

This is the single source of truth for ALL formatting, structural, and content requirements
across every HTML file in the book. The Controller Agent reads this file before
every sweep to know exactly what to check and fix.

**Maintained by**: Controller Agent + Meta Agent + user directives
**Last updated**: 2026-03-29 (v3: callout system update, non-standard box ban, CSS icon delivery)

---

## A. Header Structure

Every `section-*.html` file:
- [ ] `.chapter-header` contains three elements in this exact order (top to bottom):
  1. `.part-label` (top): Part name, hyperlink to **part index** (`../index.html`)
  2. `.chapter-label` (middle): Chapter number, hyperlink to **chapter index** (`index.html`)
  3. `h1` (bottom): Section title
- [ ] Order is: Part → Chapter → Section title (hierarchy from broadest to most specific)
- [ ] All three use consistent font family (inherit from header)
- [ ] Part label: `<div class="part-label"><a href="../index.html">Part N: Name</a></div>`
- [ ] Chapter label: `<div class="chapter-label"><a href="index.html">Chapter XX: Title</a></div>`
- [ ] Section title: `<h1>Section Title</h1>`
- [ ] Link colors: part label `rgba(255,255,255,0.85)`, chapter label `rgba(255,255,255,0.7)`
- [ ] Class name is `.part-label` (NOT the deprecated `.subtitle`). Files with `class="subtitle"` must be updated.
- [ ] Both links present, no inline styles except color and text-decoration on the `<a>` tags
- [ ] Canonical HTML:
```html
<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part N: Name</a></div>
    <div class="chapter-label"><a href="index.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Chapter XX: Title</a></div>
    <h1>Section Title</h1>
</header>
```

Every `index.html` (chapter level):
- [ ] Header contains `<nav class="header-nav">` as first child with book title link and ToC icon
- [ ] Header links to book ToC (`../../index.html`) and part index (`../index.html`)
- [ ] Lists all section files that actually exist on disk (no broken links, no missing sections)
- [ ] Section titles match the actual `<h1>` in each corresponding section file
- [ ] Contains a brief description and annotated chapter listing with hyperlinks
- [ ] No standalone `<div class="book-title-bar">` (replaced by `.header-nav` inside header)
- [ ] No badges on section listings (no difficulty/focus badges)
- [ ] No `practical-example` callouts on chapter index pages
- [ ] No callout boxes nested inside `<li>` elements
- [ ] No `<a>` tags nested inside `<a class="section-card">` (invalid HTML; strip inner links to plain text)
- [ ] Section cards `<span class="section-desc">` must NOT contain `<a>` tags (they are inside an `<a class="section-card">` parent; nested anchors break the card layout)

### A2. Chapter Index Content Order

Mandatory element order for every `part-*/module-*/index.html`:
1. `<header class="chapter-header">` (header-nav, part-label, h1)
2. `<blockquote class="epigraph">` (inside `.content`)
3. `<figure class="illustration">` (chapter opener image)
4. `<div class="callout big-picture">` (**MANDATORY**: why this chapter matters in the book's arc)
5. `<div class="overview">` (Chapter Overview with cross-references)
6. `<div class="prereqs">` (Prerequisites: what the reader needs; items linked to appendix sections where relevant)
7. `<div class="objectives">` (Learning Objectives: what the reader will learn)
8. `<h2>Sections</h2>` + `<ul class="sections-list">` (section cards)
9. `<div class="callout fun-note">` (optional, max 1 after sections)
10. `<div class="whats-next">` (link to **next chapter**, not a section)
11. `<nav class="chapter-nav">` (prev/next chapter links)
12. `<footer>` (book title and edition)

**NOTE**: No bibliography on chapter index pages. Bibliographies belong only on section pages.

### A3. Part Index Content Order

Mandatory element order for every `part-*/index.html`:
1. `<header class="chapter-header">` (header-nav, h1, chapter-subtitle)
2. `<div class="part-overview">` (Part Overview with cross-references)
3. `<div class="callout big-picture">` (**MANDATORY**: why this part matters in the book's arc)
4. `<div class="chapter-card">` blocks (one per chapter, with section lists)
5. `<div class="whats-next">` (link to **next part**, not a chapter)
6. `<footer>` (book title and edition)

**NOTE**: No bibliography on part index pages.

### A4. Header Navigation Bar

All pages (section, chapter index, part index, appendix) must have:
- [ ] `<nav class="header-nav">` as first child inside `<header class="chapter-header">`
- [ ] Book title link → **cover page** (`index.html`): `<a href="[path-to-root]/index.html" class="book-title-link">`
- [ ] ToC link → **table of contents** (`toc.html`): `<a href="[path-to-root]/toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>`
- [ ] CRITICAL: The two links point to DIFFERENT pages. Book title = cover (`index.html`), menu = ToC (`toc.html`)
- [ ] Correct relative path based on file depth:
  - Root files: `index.html` / `toc.html`
  - Front matter files: `../index.html` / `../toc.html`
  - Part index: `../index.html` / `../toc.html`
  - Chapter index / section files: `../../index.html` / `../../toc.html`
  - Appendix files: `../../index.html` / `../../toc.html`

### A5. File Naming Convention

- [ ] Section files use `section-N.M.html` with NO leading zeros (e.g., `section-0.1.html` not `section-00.1.html`)
- [ ] Chapter index pages are always `index.html` inside `module-*` directories
- [ ] Part index pages are always `index.html` inside `part-*` directories

## B. Epigraph

- [ ] Present in every section file and chapter index file, immediately after `.chapter-header` inside `.content`
- [ ] Uses `<blockquote class="epigraph">` with CSS class (no inline styles)
- [ ] **Full width** within `.content` container (same width as other callout boxes)
- [ ] `margin-inline-start: 0` to override browser default blockquote indentation
- [ ] Attribution format: `<cite>A [Adjective] AI Agent</cite>` (e.g., "A Weary AI Agent", "A Philosophical AI Agent")
- [ ] Attribution must NOT use character names (e.g., NOT "Cautious Gradient")
- [ ] Content is relevant to the chapter topic, not generic filler
- [ ] Maximum one epigraph per file (idempotency guard)
- [ ] CSS defined in `styles/book.css` (single source of truth, not inline)

## C. Prerequisites

### C1. Section-level prerequisites
- [ ] Present in every section file, after epigraph, before first content heading
- [ ] Uses `<div class="prerequisites">` with CSS class (no inline styles)
- [ ] Written as **flowing prose** with inline `<a href>` links (NEVER bulleted `<ul>/<li>` lists)
- [ ] Links use correct relative paths to earlier sections
- [ ] Contains `<h3>Prerequisites</h3>` followed by one or two `<p>` paragraphs

### C2. Chapter-level prerequisites
- [ ] Present on every chapter index page (`module-*/index.html`)
- [ ] Uses `<div class="prereqs">` with bulleted `<ul>/<li>` lists (chapter level uses lists, section level uses prose)
- [ ] **Appendix linking**: Each prerequisite item should link to the relevant appendix section where readers can review:
  - "Linear algebra" → `appendix-a/section-a.1.html`
  - "Probability" → `appendix-a/section-a.2.html`
  - "Calculus" → `appendix-a/section-a.3.html`
  - "Python proficiency" → `appendix-c/index.html`
  - "Environment setup" → `appendix-d/index.html`
  - "Neural networks" → `appendix-b/section-b.2.html`
  - "PyTorch" → `module-00/section-0.3.html`
  - "Transformer basics" → `module-04/index.html`
- [ ] CSS defined in `styles/book.css` (single source of truth)

## D. Callout Boxes

- [ ] All 11 canonical class names are recognized:
  1. `big-picture` (purple: `#f3e5f5` / `#f0e6ff`, border `#8e44ad`)
  2. `key-insight` (green: `#e8f5e9`, border `#27ae60`)
  3. `note` (blue: `#e8f4fd`, border `#3498db`)
  4. `warning` (amber: `#fef9e7` / `#fff8e1`, border `#f39c12`)
  5. `practical-example` (light grey: `#f5f5f5`, border `#78909c`)
  6. `fun-note` (pink/yellow: pink gradient, gold border)
  7. `research-frontier` (teal: `#e0f2f1` / `#e0f7fa`, border `#00897b`)
  8. `algorithm` (indigo: `#e8eaf6`, border `#3f51b5`)
  9. `tip` (cyan: `#e0f7fa`, border `#00acc1`)
  10. `exercise` (orange: `#fff3e0`, border `#fb8c00`)
  11. `key-takeaway` (deep green: `#e8f5e9`, border `#2e7d32`)
- [ ] No non-standard box classes (tip-box, highlight-box, info-box, note-box, example-box, alert, notice, important, caution). All content boxes must use `<div class="callout TYPE">` format.
- [ ] No variant names such as: `callout-note`, `callout-insight`, `callout-warning`, `callout-error`, `callout-big-picture`
- [ ] CSS definitions for all 11 types present in `styles/book.css` (single source of truth)
- [ ] At least 1 `key-insight` (mental model) per section file
- [ ] At least 1 `practical-example` per section file
- [ ] Maximum 5 to 6 callout boxes per section (avoid overloading the page)
- [ ] Every callout box is referenced or connected to surrounding prose text
- [ ] Each callout type has a visually distinct background, icon, and border color
- [ ] **Icon delivery**: Icons are delivered via CSS `::before` pseudo-elements with PNG images (defined in `styles/book.css`), NOT inline HTML entities in the title text. The `.callout-title` text should contain ONLY the title words (e.g., "Big Picture", "Key Insight"), with no emoji or entity prefixes.
- [ ] **Callout title case**: Titles use sentence case (not ALL CAPS). CSS `text-transform: uppercase` has been removed from `.callout-title`.
- [ ] **Callout title typography**: All callout titles share identical typography: `font-family: 'Segoe UI', system-ui, sans-serif; font-size: 0.95rem; font-weight: 700; letter-spacing: 0.3px`

## E. Code Blocks and Captions

Three mandatory elements for every code block:

### E1. Caption Below Each Code Block
- [ ] Every `<pre>` code block has a `<div class="code-caption">` immediately after it
- [ ] Caption starts with bold label: `<strong>Code Fragment X:</strong>` where X is a running number (1, 2, 3...) within the section
- [ ] After the label, 2 to 3 descriptive sentences explaining: what the code demonstrates, why it matters, and what the reader should notice
- [ ] Captions MUST be specific to the actual code content (not generic templates)
- [ ] BANNED generic captions: "Making an API call to the language model provider", "Loading a pretrained model and tokenizer", "Configuration setup for the pipeline", "These libraries provide the core functionality" or any caption that could apply to any code block without modification
- [ ] Each caption must reference specific variables, functions, outputs, or concepts visible in the code
- [ ] Example: `<div class="code-caption"><strong>Code Fragment 3:</strong> This snippet demonstrates beam search decoding with a beam width of 5. Notice how the algorithm maintains multiple candidate sequences simultaneously, pruning lower-probability paths at each step. The temperature parameter controls how aggressively the model explores alternative completions.</div>`
- [ ] Code caption is positioned BELOW the `<pre>` block (after `</pre>` or after `.code-output`), NEVER above it
- [ ] Anti-pattern to scan for: `<div class="code-caption">` immediately followed (within 5 lines) by `<pre>`. This means the caption is above the code and must be moved below.
- [ ] No two code captions in the same file have identical text. Each caption must reference at least one specific element from its code block.
- [ ] Uses `.code-caption` CSS class (no inline styles)

### E2. Opening Comments Inside Each Code Block
- [ ] Every code block starts with 2 to 3 comment lines describing what the code does
- [ ] Comments use the language's comment syntax (# for Python, // for JS, etc.)
- [ ] Comments describe the purpose and key operations, not line-by-line narration
- [ ] BANNED generic comments: "Import X and supporting dependencies", "These libraries provide the core functionality for this example" or any comment that could apply to any code block. Opening comments must state what THIS specific code does.
- [ ] Example:
  ```python
  # Beam search decoding: maintain top-k candidate sequences
  # at each step, expanding and pruning by cumulative log-probability.
  # Returns the highest-scoring complete sequence.
  def beam_search(model, input_ids, beam_width=5, max_length=50):
  ```

### E3. Prose Reference Before Each Code Block
- [ ] Every code block is introduced in the preceding prose paragraph
- [ ] The reference describes what the code will show and why it is relevant
- [ ] Use natural phrasing such as: "The following snippet demonstrates...", "Below, we implement...", "Consider the following approach to...", "Code Fragment 3 shows how..."
- [ ] Do NOT just drop a code block without any preceding text introducing it

### E4. General Code Quality
- [ ] Code has informative inline comments (not cluttering, but pedagogically helpful)
- [ ] Code uses current, stable libraries and tools
- [ ] Numbering is sequential within each section file (Code Fragment 1, 2, 3... restarting per file)
- [ ] Canonical CSS:

```css
.code-caption {
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    color: #555;
    text-align: center;
    margin-top: 0.3rem;
    margin-bottom: 1.8rem;
    padding: 0 1rem;
    line-height: 1.5;
    font-style: italic;
}
```

## F. Research Frontier

- [ ] `.callout.research-frontier` present in every section file
- [ ] Positioned after all main content, before What's Next
- [ ] Contains current (2024 to 2026) research directions, not placeholder text
- [ ] References specific papers, tools, or active research areas
- [ ] CSS: teal/green gradient background (`#e0f2f1` / `#e0f7fa`), `#00897b` border

## G. What's Next

- [ ] `<div class="whats-next">` present on every page (section, chapter index, part index)
- [ ] Uses CSS class definition (NO inline `style=` attribute on the div)
- [ ] Contains a transition sentence describing the next topic
- [ ] Contains a hyperlink to the appropriate next item
- [ ] **Hierarchy rule (MANDATORY)**:
  - **Section pages** → link to the **next section** in the same chapter (or chapter index if last section)
  - **Chapter index pages** → link to the **next chapter** (or next part if last chapter in part)
  - **Part index pages** → link to the **next part** (or conclusion/appendices if last part)
  - NEVER cross levels: a chapter page must NOT link to a section; a part page must NOT link to a chapter
- [ ] Canonical CSS defined in `styles/book.css` (single source of truth):

```css
.whats-next {
    background: linear-gradient(135deg, #e3f2fd, #e8eaf6);
    border: 1px solid #90caf9;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin: 1.5rem 0;
}
.whats-next h3 { color: #1565c0; margin-bottom: 0.8rem; }
.whats-next p:last-child { margin-bottom: 0; }
```

- [ ] What's Next title uses same typography as callout titles: `font-family: 'Segoe UI', system-ui, sans-serif; font-size: 0.95rem; font-weight: 700; letter-spacing: 0.3px`

## H. Bibliography

- [ ] Bibliography title uses same typography as callout titles (sentence case, no uppercase transform)
- [ ] **Section pages ONLY**: `<section class="bibliography">` present as last content element (before nav footer)
- [ ] **Chapter index pages**: NO bibliography (removed; references belong on section pages)
- [ ] **Part index pages**: NO bibliography
- [ ] Uses card-based format with `.bib-entry-card` (NOT old `<ol class="bib-list">` format)
- [ ] At least 3 entries per section file, each with 2 to 3 sentence annotations
- [ ] Annotations explain: what the reference contains, why it is relevant, who should read it
- [ ] Real, clickable URLs (arXiv, ACL Anthology, GitHub, official docs)
- [ ] Maximum one bibliography per file (idempotency guard)
- [ ] CSS definitions in `styles/book.css` for: `.bibliography`, `.bibliography-title`, `.bib-entry-card`, `.bib-ref`, `.bib-annotation`, `.bib-meta`

## I. Navigation Footer

- [ ] Prev/Next links present pointing to correct adjacent sections
- [ ] "Up" link pointing to chapter `index.html`
- [ ] Links are correct and bidirectional (section A's "next" matches section B's "prev")
- [ ] No duplicate navigation bars (old `<nav class="chapter-nav">` removed)

## J. CSS Completeness

### Shared Stylesheet (Target State)
All HTML files should link to the shared stylesheet `styles/book.css` instead of embedding inline `<style>` blocks:
```html
<link rel="stylesheet" href="../../styles/book.css">
```
The relative path depth depends on the file's location:
- Section files (`part-*/module-*/section-*.html`): `../../styles/book.css`
- Chapter index files (`part-*/module-*/index.html`): `../../styles/book.css`
- Part index files (`part-*/index.html`): `../styles/book.css`
- Book root files (`index.html`, `team.html`): `styles/book.css`
- Appendix files (`appendices/appendix-*/index.html`): `../../styles/book.css`

The shared stylesheet (`styles/book.css`) is the **single source of truth** for all CSS definitions. It contains:
- [ ] CSS custom properties (`:root` block with `--primary`, `--accent`, `--highlight`, `--bg`, `--text`)
- [ ] `.header-nav` (book title link + ToC icon, replaces `.book-title-bar`)
- [ ] `.epigraph` (and sub-selectors: `cite`, `cite::before`)
- [ ] `.prerequisites` (and sub-selectors: `h3::before`, `a`)
- [ ] `.whats-next` (and sub-selectors: `h3`)
- [ ] `.bibliography` (and sub-selectors: `.bibliography-title`, `.bib-entry-card`, `.bib-ref`, `.bib-annotation`)
- [ ] `.code-caption`
- [ ] All 11 `.callout` variants (big-picture, key-insight, note, warning, practical-example, fun-note, research-frontier, algorithm, tip, exercise, key-takeaway)
- [ ] `.lab` (and sub-selectors)
- [ ] `.diagram-container` and `.diagram-caption`
- [ ] `.content a` visible link styling (underline with subtle color, hover highlight)
- [ ] `.sections-list` and `.section-card` (chapter index page section listings)
- [ ] `.chapter-card` (part index page chapter listings)
- [ ] `.chapter-header` with `.part-label`, `.chapter-label`, `h1`
- [ ] Responsive media queries (1024px, 768px, 480px)
- [ ] Print styles

### Current State (Migration in Progress)
Files may still contain inline `<style>` blocks. During migration:
- [ ] Replace inline `<style>` with `<link rel="stylesheet" href="[path]/styles/book.css">`
- [ ] Verify no visual regressions after removing inline CSS
- [ ] Keep only page-specific CSS overrides in a minimal inline `<style>` block (rare; most pages need no overrides)

No recurring element should use inline `style=` when a CSS class exists for it.

## K. Responsive CSS

All responsive rules are defined in `styles/book.css`. Files using the shared stylesheet inherit these automatically:
- [ ] Media query for 1024px (tablet): content max-width 100%, reduced padding, SVG scaling
- [ ] Media query for 768px (iPad Mini): smaller fonts, scrollable tables/code blocks, adjusted callout boxes
- [ ] Media query for 480px (mobile): tighter padding, full-width epigraph/prerequisites

## L. Non-Standard Content Boxes

- [ ] All styled content boxes must use the standard callout system (`<div class="callout TYPE">`). The following non-standard classes are **BANNED** and must be converted to an appropriate callout type: `tip-box`, `highlight-box`, `info-box`, `note-box`, `example-box`, `alert`, `notice`, `important`, `caution`
- [ ] Inline-styled divs with `background-color` used for emphasis or callout purposes should be converted to the appropriate standard callout type
- [ ] Bold-prefix patterns like `<p><strong>Note:</strong>` outside callouts should be wrapped in an appropriate callout (e.g., `<div class="callout note">`)
- [ ] Any custom-styled box that visually resembles a callout must use the standard callout markup and one of the 11 canonical class names from Section D

## M. Cross-References

- [ ] At least 3 cross-chapter hyperlinks per section file
- [ ] Links use correct relative paths:
  - Same part: `../module-XX/section-X.Y.html`
  - Different part: `../../part-N/module-XX/section-X.Y.html`
- [ ] No broken hrefs (all targets exist on disk)
- [ ] Progressive depth concepts linked with context-differentiating language (see section V)
- [ ] Big Picture boxes contain backward-facing links to previous chapters where the concept was introduced

## N. Content Width Rules

- [ ] `.content` container: `max-width: 820px`
- [ ] `.epigraph`: full width within `.content` (uses `margin-inline-start: 0` to override blockquote default)
- [ ] `.prerequisites` / `.prereqs`: full width within `.content`
- [ ] All callout boxes: full width within `.content`
- [ ] **ToC page** (`toc.html`): `body.index-page .container` uses `max-width: 820px` (same as content pages)
- [ ] Everything else inherits from `.content` (no separate conflicting max-width)
- [ ] No sections appear visually wider or narrower than expected due to rogue inline styles

## O. Style Rules

- [ ] No em dashes (the character U+2014) anywhere in text
- [ ] No double dashes (`--`) used as punctuation in prose
- [ ] No "syllabus" or "course" when referring to the book (use "book", "part", "chapter", "section")
- [ ] No "module" when referring to book structure (use "chapter" instead; "module" is only for software/code modules)
- [ ] No placeholder text ("TODO", "TBD", "Lorem ipsum", "[placeholder]")
- [ ] No patronizing phrases ("Great job!", "Congratulations!", "Well done!")
- [ ] All claims have intuitive or formal justification (no unjustified assertions)
- [ ] Acronyms and proper nouns in prerequisites and prose are correctly capitalized (e.g., "LLM APIs" not "llm apis", "PyTorch" not "pytorch")
- [ ] Prerequisites text reads as natural, complete prose (no truncated sentences, garbled text, or broken HTML entities)
- [ ] Every concept answers: what it is, why it matters, how it works, when to use it
- [ ] Text is justified with auto-hyphens (`text-align: justify; hyphens: auto;`)

## P. Figures and Tables

- [ ] Every figure has a caption with section-aligned numbering: `Figure [Section].[Seq]` (e.g., Figure 3.2.1)
- [ ] Every table is introduced in preceding prose text
- [ ] Every diagram wrapped in `<div class="diagram-container">`
- [ ] All images have meaningful alt text (not empty, not "image")
- [ ] SVGs use book color palette (`#1a1a2e`, `#0f3460`, `#e94560`, `#f8f9fa`)
- [ ] SVG coordinate correctness verified (y=0 is top of viewport; minima at high y values, maxima at low y values)
- [ ] Every figure is referenced in surrounding prose text before it appears

## Q. Element Ordering (within each section file)

Mandatory order in every section file:
1. Chapter header (`.chapter-header` with chapter-label, h1, part-label)
2. Epigraph (immediately after header, inside `.content`)
3. Prerequisites (immediately after epigraph)
4. Section content (prose, callouts, code, figures, exercises, labs)
5. Research Frontier (`.callout.research-frontier`, after all content)
6. What's Next (`.whats-next`, after Research Frontier)
7. Bibliography (`<section class="bibliography">`, last before nav footer)
8. Navigation footer (prev/next/up links)

## R. Illustrations

- [ ] Chapter opener illustration in every chapter `index.html` (Gemini-generated PNG in `images/` subfolder)
- [ ] Illustrations wrapped in `<figure class="illustration">` with `<figcaption>`
- [ ] Inline SVG diagrams wrapped in `<div class="diagram-container">`
- [ ] Illustration style: Kurzgesagt-inspired flat vector art (bright, educational, slightly humorous)
- [ ] 5 to 8 illustrations per chapter across all section files
- [ ] No duplicate illustrations: each illustration in a section file must depict a DIFFERENT concept. Two images about the same concept (e.g., two sandbox images, two training loop images) are duplicates; remove the weaker one.
- [ ] Illustration types include: algorithm-as-scene, architecture-as-building, concept-as-character, system-as-ecosystem, analogy, mental-model

## S. Mental Models

- [ ] At least 1 `key-insight` callout (mental model, analogy, or "aha moment") per section file
- [ ] Mental model explains the concept using a concrete analogy, comparison, or visualization
- [ ] Mental model is placed near the concept it illuminates, not relegated to the end

## T. Fun Notes

- [ ] Maximum 1 to 2 `fun-note` callouts per section (quality over quantity)
- [ ] Humor is in good taste: witty analogy, self-aware aside, absurdist comparison, understatement, playful personification, or relatable frustration
- [ ] Not patronizing, forced, or cringeworthy
- [ ] Related to the section content (not random)

## U. Inline Style Elimination

- [ ] No `style=` attributes on elements where a CSS class exists for that purpose
- [ ] Specifically check: epigraph, prerequisites, whats-next, callout boxes, bibliography, code-caption, lab
- [ ] Header link colors may use inline style for `color` on `<a>` tags (acceptable exception)

## V. Progressive Depth Cross-Linking

The following concepts appear in multiple chapters at different depth levels. Each occurrence must include a cross-reference link with context-differentiating language:

| Concept | Locations | Context Differences |
|---------|-----------|---------------------|
| Attention | Section 3.2, Section 4.1, Section 10.3 | intuition, multi-head detail, optimization |
| GQA (Grouped Query Attention) | Section 4.2, Section 7.1, Section 10.2 | mechanism, model usage, efficiency |
| MoE (Mixture of Experts) | Section 7.1, Section 10.4 | architecture, inference optimization |
| Embeddings | Section 1.3, Section 19.1, Section 19.2 | word2vec, semantic search, vector DBs |
| Catastrophic forgetting | Section 14.2, Section 15.1 | full fine-tuning, PEFT motivation |
| Temperature | Section 5.1, Section 10.2 | decoding theory, API parameter |
| Tokenization | Section 2.1, Section 2.2, Section 2.3 | concept, BPE, sentencepiece |
| Prompt injection | Section 11.3, Section 27.3 | attack patterns, production defense |
| RLHF/DPO | Section 17.1, Section 17.2, Section 17.3 | theory, RLHF practice, DPO alternative |

Link phrasing must differentiate context: "for the intuitive introduction, see Section 3.2" vs. "for multi-head implementation details, see Section 4.1".

## W. Index/ToC Synchronization

Three levels of index must stay synchronized:

**Cover page** (`index.html`): Animated cover page. No ToC content. Links to `toc.html`.

**Table of Contents** (`toc.html`):
- [ ] Lists all 10 parts with links to part index pages
- [ ] Lists all 36 chapters with links to chapter index pages
- [ ] Lists all 10 appendices with links
- [ ] Lists Front Matter with links
- [ ] **Short ToC** (default): compact grid, no badges, no legend, no Lab indicators
- [ ] **Detailed ToC**: expandable chapter cards, collapsed by default, no badge-group spans
- [ ] No `<div class="legend">` block (removed)
- [ ] No `<span class="badge">` or `<span class="badge-group">` anywhere
- [ ] No `<strong>Lab:</strong>` lines in lesson-topics
- [ ] Uses `body.index-page .container` with `max-width: 820px`
- [ ] Overview/Detailed toggle with JS `showToc()` function
- [ ] Chapter titles match actual `<h1>` in chapter index files
- [ ] Writing Team link reflects current agent count (42)

**Part-level** (`part-*/index.html`):
- [ ] Lists all chapters within that part with links to chapter index pages
- [ ] Each chapter card lists all section files with hyperlinks
- [ ] Section titles match actual `<h1>` in section files
- [ ] Has big-picture callout and what's-next (to next part)

**Chapter-level** (`part-*/module-*/index.html`):
- [ ] Lists all section files that exist on disk
- [ ] Section titles match actual `<h1>` in section files
- [ ] Contains chapter opener illustration
- [ ] Contains epigraph, overview, big-picture, prereqs (linked to appendices), objectives
- [ ] Has what's-next (to next chapter)
- [ ] No bibliography (bibliographies only on section pages)

## X. Agent Team HTML (`team.html`)

- [ ] Reflects current pipeline state (agent count, phase count)
- [ ] Each agent card includes: avatar, name, role title, 3 to 5 sentence description
- [ ] Pipeline workflow table references agents by `#NN Name (Role)` format
- [ ] Stats bar matches actual agent/phase counts
- [ ] "Back to Book Home" link (not "Back to Course Home")
- [ ] All avatar images exist in `agents/avatars/` directory

## Y. Front Matter Structure

The front matter lives in `front-matter/` at the root level and follows the same standards as any chapter:
- [ ] `front-matter/index.html` (Front Matter index, standard chapter index layout)
- [ ] `front-matter/section-fm.1.html` (Introduction: what this book is, who it's for)
- [ ] `front-matter/section-fm.2.html` (Reading Pathways: reader profiles with links to relevant chapters)
- [ ] `front-matter/section-fm.3.html` (Course Syllabi: university course outlines linking to chapters)
- [ ] `front-matter/section-fm.4.html` (How to Use This Book: conventions, callouts, labs)
- [ ] Each section follows standard section page layout (header-nav, chapter-header, content, what's-next, nav, footer)
- [ ] Pathways use `<div class="callout pathway">` for each reader profile
- [ ] Course syllabi link to specific chapter sequences
- [ ] Appears in `toc.html` like any other part (with section items in short ToC, expandable card in detailed ToC)
- [ ] Relative paths from front-matter/: `../styles/book.css`, `../index.html`, `../toc.html`

## Z. Labs

- [ ] Labs (when present) placed after exercises, before Research Frontier
- [ ] Uses `<div class="lab">` with CSS class
- [ ] Structure: Objective, What You'll Practice, Setup, Guided Steps (with TODOs and hints), Expected Output, Stretch Goals, Solution
- [ ] 1 to 2 labs per chapter, 30 to 90 minutes each
- [ ] Idempotency guard: check for existing `class="lab"` before adding
- [ ] Lab CSS definitions in `<style>` block for: `.lab`, `.lab-meta`, `.lab-step`, `.lab-expected`, `.lab-stretch`, `.lab-solution`

---

## Book-Specific Requirements

These items are specific to the current book ("Building Conversational AI using LLM and Agents") rather than generic formatting rules.

### Chapter 25/27/28 Split Structure

Chapter 25 was split into three chapters:
- [ ] Chapter 27: Production Engineering (sections 26.1 to 26.4)
- [ ] Chapter 27: Safety, Ethics, and Regulation (formerly sections 26.5 to 26.11, renumbered as 27.1 to 27.7)
- [ ] Chapter 28: Strategy, Product, and ROI (formerly old Chapter 27, renumbered as 28.1 to 28.5)
- [ ] All internal cross-references updated to reflect renumbering
- [ ] Part 7 index page reflects the three-chapter structure

### Content Update Plan Tiers

All tiers from `CONTENT_UPDATE_PLAN.md` should be addressed:
- [ ] Tier 1 (Essential Now): 9 new sections created, 6 critical expansions completed
- [ ] Tier 2 (Useful Soon): 20 important additions integrated
- [ ] Tier 3 (Nice to Have): 18 additions integrated where appropriate

### New Sections Created

These sections were created to fill content gaps:
- [ ] Section 10.5: Model Pruning and Sparsity
- [ ] Section 10.4: Reasoning Models and Multimodal APIs
- [ ] Section 11.5: Prompting Reasoning and Multimodal Models
- [ ] Section 13.7: Synthetic Reasoning Data
- [ ] Section 19.5: Vision-Based Document Retrieval (ColPali, ColQwen)
- [ ] Section 22.5: Reasoning Models and Agent Architecture (MCP ecosystem)
- [ ] Section 23.4: Multi-Agent Communication Patterns
- [ ] Section 24.4: Document AI
- [ ] Section 27.8: Advanced Evaluation Methods

### Tech Stack Currency

The Content Update Scout should verify coverage of:
- [ ] Current Python libraries: vLLM, SGLang, Unsloth, CrewAI, LangChain, LangGraph, LlamaIndex, DSPy, Outlines, instructor
- [ ] Current models: DeepSeek-R1, Llama 4, Phi-4, Gemini 2.x, Claude 3.x/4.x, GPT-4o/o1/o3
- [ ] Protocols and standards: MCP (Model Context Protocol), A2A (Agent-to-Agent)
- [ ] Disaggregated inference, speculative decoding, PagedAttention

### Badge System (Index Pages)

- [ ] Difficulty badges: Basic (green), Intermediate (yellow), Advanced (red)
- [ ] Focus badges: Fundamentals, Engineering, Research, Lab
- [ ] Badges synchronized across main index, part index, and chapter index pages

### Level Badges (Section Files)

- [ ] Every h2 heading in section files includes a `<span class="level-badge [level]">[LEVEL]</span>` where [level] is one of: basic, intermediate, advanced, research
- [ ] Every section file contains a `.level-legend` div after prerequisites, before first content heading
- [ ] Level-legend contains exactly 4 items: BASIC, INTERMEDIATE, ADVANCED, RESEARCH
- [ ] Level-legend uses the canonical HTML:
  ```html
  <div class="level-legend">
    <div class="level-legend-item"><span class="level-badge basic">BASIC</span> Foundational concepts</div>
    <div class="level-legend-item"><span class="level-badge intermediate">INTERMEDIATE</span> Core skills</div>
    <div class="level-legend-item"><span class="level-badge advanced">ADVANCED</span> Deep expertise</div>
    <div class="level-legend-item"><span class="level-badge research">RESEARCH</span> Cutting edge</div>
  </div>
  ```
- [ ] CSS definitions for `.level-badge`, `.level-badge.basic`, `.level-badge.intermediate`, `.level-badge.advanced`, `.level-badge.research`, `.level-legend` present in styles/book.css
- [ ] Badge distribution: at least 1 basic and 1 intermediate heading per section file; research headings optional
- [ ] Cross-chapter links use `class="cross-ref"` on the `<a>` tag for automated audit

### Self-Study Learning Pathways (introduction.html)

- [ ] introduction.html contains at least 10 named learning pathways
- [ ] Each pathway lists a sequence of sections with focus/skip/skim guidance
- [ ] Pathways cover diverse audiences (researcher, engineer, PM, career changer, etc.)
- [ ] No broken links in pathway section references

### Book Color Palette

- [ ] Primary: `#1a1a2e`
- [ ] Accent: `#0f3460`
- [ ] Highlight: `#e94560`
- [ ] Background: `#f8f9fa` / `#fafafa`
- [ ] Text: `#2d3436`
- [ ] Text light: `#555`

### Typography

- [ ] Body font: Georgia, 'Times New Roman', serif
- [ ] UI elements font: 'Segoe UI', system-ui, sans-serif
- [ ] Body font-size: 17px
- [ ] Line-height: 1.85
- [ ] Text justified with auto-hyphens

---

## Idempotency Rules

All editor agents must check before adding content:

| Element | Check For | Max Allowed | Behavior on Re-Run |
|---------|-----------|-------------|---------------------|
| Cross-references | `href=` links | 8 to 20 | Fix/improve, add only if below 8 |
| Illustrations | `class="illustration"` | 5 to 8 | Replace weak, add only if below 5 |
| Epigraph | `class="epigraph"` | 1 | Replace or keep; never add second |
| Practical Examples | `class="callout practical-example"` | 3 to 6 | Replace weak, add only if below 3 |
| Fun Notes | `class="callout fun-note"` | 1 to 2 | Replace weak, add only if below 1 |
| Bibliography | `class="bibliography"` | 1 | Replace or keep; never add second |
| Exercises | `class="exercise"` or `<h3>Exercise` | 8 to 15 | Add only if below 8 |
| Visual elements | `<svg`, `<figure`, `<img` | 10 to 20 | Add only if below 10 |
| Engagement elements | callout boxes, hooks, challenges | 6 to 10 | Add only if below 6 |
| Research sidebars | Paper Spotlight, Open Question, Research Frontier | 5 to 8 | Add only if below 5 |
| Labs | `class="lab"` | 1 to 2 | Add only if below 1 |

---

## Change Log

| Date | Change | Source |
|------|--------|--------|
| 2026-03-27 | Initial checklist created from accumulated requirements | User directives across multiple sessions |
| 2026-03-27 | Added header navigation links requirement (module label + part subtitle as hyperlinks) | User request |
| 2026-03-27 | Added code caption requirement (2 to 3 descriptive sentences after every code block) | User request |
| 2026-03-27 | Added responsive CSS requirement (iPad 1024/768/480 breakpoints) | User request |
| 2026-03-27 | Added width consistency rules (820px content, 600px epigraph/prereqs) | User observation |
| 2026-03-27 | Added inline style elimination rule (use CSS classes, not style=) | User observation |
| 2026-03-27 | Comprehensive rewrite: elicited all requirements from full conversation history (12,462 lines, 133 user messages) via Meta Agent (Agent 41) | Conversation transcript analysis |
| 2026-03-27 | Added: 7 canonical callout types (was 6, added research-frontier), epigraph attribution rules, prerequisites prose format, bibliography card format, figure/code numbering alignment, progressive depth cross-linking table, idempotency rules, element ordering, lab requirements, book-specific sections (Module 26 split, content tiers, tech stack, badge system, color palette, typography) | Extracted from user directives MSG 0 through MSG 133 |
| 2026-03-27 | Added canonical callout-title icons: 7 specific HTML entity icons for each callout type (star, lightbulb, memo, warning, construction, circus tent, microscope) | User request for icon consistency |
| 2026-03-28 | Added BANNED generic captions/comments to Section E (anti-template rules) | User observation: code fragment agents applied generic boilerplate |
| 2026-03-28 | Added acronym capitalization and prerequisites quality rules to Section N | User observation: "llm apis" instead of "LLM APIs" |
| 2026-03-28 | SKILL.md: Added mandatory post-generation quality pass (all agents must run on new content) | User directive: every new chapter/section gets full workflow |
| 2026-03-28 | SKILL.md: Added Resume Incomplete Work Protocol for auto-restart after usage limits | User directive: prevent lost work from session breaks |
| 2026-03-28 | Header order changed: Part (top) → Chapter (middle) → Section title (bottom). Renamed `.subtitle` to `.part-label`. Consistent fonts. | User directive: "Part should be first" |
| 2026-03-28 | Renamed "Module" to "Chapter" throughout. Book hierarchy: Part → Chapter → Section. CSS class `.module-label` → `.chapter-label`. | User directive: "part->chapter->section" |
| 2026-03-28 | Section J rewritten: shared stylesheet `styles/book.css` as single source of truth, replacing per-file inline `<style>` blocks. Migration path documented. Section K updated to reference shared CSS. | User directive: single CSS for all pages |
| 2026-03-28 | Meta Agent audit: Added caption position verification (BELOW not above) and caption uniqueness rule to Section E1. Added `.subtitle` deprecation note to Section A. Updated 7 agent skill files with self-check protocol, uniqueness enforcement, and class migration rules. | Meta Agent #41 full book audit |
