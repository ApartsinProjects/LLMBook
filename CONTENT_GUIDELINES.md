# Content Guidelines

Style guide for generating clean, audit-passing HTML content.
Every rule below corresponds to an automated audit check. Following these rules
ensures content passes on the first run.

---

## 1. HTML Structure

### 1.1 Heading Hierarchy (HEADING_HIERARCHY, P2)

Never skip heading levels. Each heading must be at most one level deeper than the previous.

```html
<!-- DO -->
<h1>Chapter Title</h1>
<h2>First Section</h2>
<h3>Subsection</h3>

<!-- DON'T -->
<h1>Chapter Title</h1>
<h3>Subsection</h3>   <!-- skipped h2 -->
```

### 1.2 Consecutive Headings (CONSECUTIVE_HEADINGS, P2)

Always place at least one paragraph or content element between two headings.

```html
<!-- DO -->
<h2>Attention Mechanism</h2>
<p>The attention mechanism allows a model to focus on relevant parts of the input.</p>
<h3>Self-Attention</h3>

<!-- DON'T -->
<h2>Attention Mechanism</h2>
<h3>Self-Attention</h3>  <!-- nothing between them -->
```

### 1.3 Mixed Heading Numbering (HEADING_NUM_MIX, P2)

Within a single file, either number all h2 headings or none of them. Do not mix.

```html
<!-- DO (all numbered) -->
<h2>1. Tokenization</h2>
<h2>2. Embedding</h2>
<h2>3. Encoding</h2>

<!-- DON'T (mixed) -->
<h2>1. Tokenization</h2>
<h2>Embedding</h2>         <!-- unnumbered among numbered -->
<h2>3. Encoding</h2>
```

### 1.4 Orphan Tags Between Header and Main (ORPHAN_TAG_BEFORE_MAIN, P1)

No stray closing tags (e.g. `</div>`) should appear between `</header>` and `<main>`.

```html
<!-- DO -->
</header>
<main>

<!-- DON'T -->
</header>
</div>          <!-- orphan tag -->
<main>
```

### 1.5 Orphan Content Outside Main (ORPHAN_CONTENT, P1)

Structural elements (epigraph, prerequisites, callouts) must be inside `<main>`, not
between `</header>` and `<main>`.

```html
<!-- DO -->
<main>
  <div class="epigraph">...</div>
  <div class="prerequisites">...</div>

<!-- DON'T -->
</header>
<div class="epigraph">...</div>   <!-- outside <main> -->
<main>
```

### 1.6 Unclosed Paragraph Tags (UNCLOSED_P_TAG, UNCLOSED_P_IN_DIV, UNCLOSED_PREREQ_P; P1)

Always close `<p>` tags explicitly. Never let a `</div>` implicitly close a `<p>`.

```html
<!-- DO -->
<div class="prerequisites">
  <p>You should be familiar with Python basics.</p>
</div>

<!-- DON'T -->
<div class="prerequisites">
  <p>You should be familiar with Python basics.
</div>   <!-- </p> is missing; </div> closes it implicitly -->
```

Also, never open a `<p>` and then start a block-level element (div, figure, table, pre)
without closing the paragraph first.

### 1.7 Skip-to-Content Link (MISSING_SKIP_LINK, P2)

Include a skip link near the top of `<body>` for accessibility.

```html
<!-- DO -->
<body>
  <a href="#content" class="skip-link">Skip to content</a>
  <header>...</header>
  <main id="content">
```

### 1.8 Meta Description (MISSING_META_DESC, P1)

Every page must have a `<meta name="description">` tag in `<head>`.

```html
<!-- DO -->
<head>
  <meta name="description" content="Learn how transformer attention mechanisms work.">
</head>

<!-- DON'T: omitting the meta description entirely -->
```

### 1.9 Title Format (TITLE_FORMAT, P1)

Page titles must not be empty. Use "with" not "using" before "LLMs". Use plural "LLMs"
not singular "LLM" in the title.

```html
<!-- DO -->
<title>Attention Mechanisms | Building Conversational AI with LLMs and Agents</title>

<!-- DON'T -->
<title>Attention Mechanisms | Building Conversational AI using LLM</title>
```

### 1.10 Unescaped Ampersands in Titles (UNESCAPED_AMPERSAND_TITLE, P1)

Always use `&amp;` for ampersands inside `<title>` tags.

```html
<!-- DO -->
<title>Retrieval &amp; Generation</title>

<!-- DON'T -->
<title>Retrieval & Generation</title>
```

### 1.11 Part Label Format (PART_LABEL_FORMAT, P1)

Part labels must use Arabic numerals matching the directory name. No Roman numerals.

```html
<!-- DO (in directory part-3-*/) -->
<div class="part-label">Part 3: Advanced Topics</div>

<!-- DON'T -->
<div class="part-label">Part III: Advanced Topics</div>
```

### 1.12 Chapter Label Format (CHAPTER_LABEL_ON_ANCHOR, CHAPTER_LABEL_NO_TITLE; P2)

Do not duplicate `class="chapter-label"` on both the outer `<div>` and the inner `<a>`.
Always include the chapter title after the number.

```html
<!-- DO -->
<div class="chapter-label">
  <a href="section-18.1.html">Chapter 18: Prompt Engineering</a>
</div>

<!-- DON'T -->
<div class="chapter-label">
  <a class="chapter-label" href="section-18.1.html">Chapter 18</a>
</div>
```

### 1.13 Excessive Blank Lines (EXCESSIVE_BLANKS, P2)

Never have three or more consecutive blank lines. Use one blank line to separate blocks.

### 1.14 Footer Placement (FOOTER_PLACEMENT, P1)

Place `<footer>` consistently across all files. Follow the majority pattern (inside
or outside `<main>`) used across the project.

### 1.15 Hardcoded Styles (HARDCODED_STYLE, P2)

Use CSS variables from the design system, not hardcoded hex colors, inside `<style>` blocks.

```css
/* DO */
background: var(--primary);

/* DON'T */
background: #1a1a2e;
```

### 1.16 External Link Attributes (EXT_LINK_ATTRS, P2)

External links (https://) must include `target="_blank"` and `rel="noopener"`.

```html
<!-- DO -->
<a href="https://arxiv.org/abs/1706.03762" target="_blank" rel="noopener">
  Attention Is All You Need
</a>

<!-- DON'T -->
<a href="https://arxiv.org/abs/1706.03762">Attention Is All You Need</a>
```

---

## 2. Tables

### 2.1 Tables Must Have Thead (TABLE_NO_THEAD, P2)

Every `<table>` must contain a `<thead>` section with column headers.

```html
<!-- DO -->
<table>
  <thead>
    <tr><th scope="col">Model</th><th scope="col">Parameters</th></tr>
  </thead>
  <tbody>
    <tr><td>GPT-4</td><td>~1.8T</td></tr>
  </tbody>
</table>

<!-- DON'T -->
<table>
  <tr><td>Model</td><td>Parameters</td></tr>
  <tr><td>GPT-4</td><td>~1.8T</td></tr>
</table>
```

### 2.2 Th Scope Required (MISSING_TH_SCOPE, P2)

Every `<th>` element must have a `scope` attribute (`"col"` or `"row"`).

```html
<!-- DO -->
<th scope="col">Metric</th>
<th scope="row">BLEU Score</th>

<!-- DON'T -->
<th>Metric</th>
```

### 2.3 Correct Th Scope (WRONG_TH_SCOPE, P1/P2; TH_SCOPE_MISMATCH, P2)

Use `scope="col"` for column headers in `<thead>` or the first row of a table.
Use `scope="row"` only for row headers (the first cell of a data row).

```html
<!-- DO -->
<thead>
  <tr>
    <th scope="col">Model</th>
    <th scope="col">Accuracy</th>
  </tr>
</thead>
<tbody>
  <tr>
    <th scope="row">BERT</th>
    <td>92.3%</td>
  </tr>
</tbody>

<!-- DON'T -->
<thead>
  <tr>
    <th scope="row">Model</th>    <!-- wrong: column header using scope="row" -->
    <th scope="row">Accuracy</th>
  </tr>
</thead>
```

### 2.4 Image Dimensions (MISSING_IMG_DIMS, P2)

Every `<img>` tag must include both `width` and `height` attributes to prevent
layout shift.

```html
<!-- DO -->
<img src="diagram.png" alt="Architecture" width="800" height="450">

<!-- DON'T -->
<img src="diagram.png" alt="Architecture">
```

---

## 3. Figures and Captions

### 3.1 No Duplicate Figure Numbers (DUP_FIGURE_NUM, P0)

Each Figure, Table, Listing, or Code Fragment number must appear exactly once
in caption elements within a file.

```html
<!-- DO -->
<figcaption><strong>Figure 5.2.1</strong>: Encoder block.</figcaption>
<figcaption><strong>Figure 5.2.2</strong>: Decoder block.</figcaption>

<!-- DON'T -->
<figcaption><strong>Figure 5.2.1</strong>: Encoder block.</figcaption>
<figcaption><strong>Figure 5.2.1</strong>: Decoder block.</figcaption>  <!-- duplicate -->
```

### 3.2 Sequential Figure Numbering (FIGURE_SEQUENCE, P1)

Figure and Code Fragment captions must appear in ascending sequential order.
Start numbering at 1 (not 0).

```html
<!-- DO -->
<figcaption><strong>Figure 12.3.1</strong>: Step one.</figcaption>
<!-- ... content ... -->
<figcaption><strong>Figure 12.3.2</strong>: Step two.</figcaption>

<!-- DON'T -->
<figcaption><strong>Figure 12.3.2</strong>: Step two.</figcaption>
<figcaption><strong>Figure 12.3.1</strong>: Step one.</figcaption>  <!-- out of order -->
```

### 3.3 No Broken Figure References (BROKEN_FIGURE_REF, P1)

Every "Figure X.Y.Z" or "Code Fragment X.Y.Z" mentioned in prose must have a
matching caption in the same file.

```html
<!-- DO -->
<p>As shown in Figure 7.1.2, the loss decreases over epochs.</p>
<!-- later in same file: -->
<figcaption><strong>Figure 7.1.2</strong>: Training loss curve.</figcaption>

<!-- DON'T -->
<p>As shown in Figure 7.1.5, the loss decreases.</p>
<!-- no caption for 7.1.5 exists anywhere in the file -->
```

### 3.4 Consistent Caption Styles (MIXED_CAPTION_STYLE, P2)

Within a single file, use one caption element type. Do not mix `<figcaption>`,
`<div class="diagram-caption">`, and `<div class="code-caption">` for the same
kind of content.

- Use `<figcaption>` for `<figure>` elements.
- Use `<div class="code-caption">` for code blocks.
- Use `<div class="diagram-caption">` for standalone SVG diagrams.

---

## 4. Code Blocks

### 4.1 Language Class Required (CODE_NO_LANGUAGE, P2)

Every `<pre><code>` block must specify a `language-*` class for Prism.js highlighting.

```html
<!-- DO -->
<pre><code class="language-python">
import torch
model = torch.nn.Linear(768, 512)
</code></pre>

<!-- DON'T -->
<pre><code>
import torch
model = torch.nn.Linear(768, 512)
</code></pre>
```

Common classes: `language-python`, `language-javascript`, `language-bash`,
`language-json`, `language-yaml`, `language-html`, `language-css`, `language-sql`.

### 4.2 No Manual Highlight Spans (MANUAL_HIGHLIGHT_SPANS, P1)

Never add hand-rolled syntax highlighting spans inside `<code>` blocks.
Prism.js handles highlighting automatically based on the language class.

```html
<!-- DO -->
<pre><code class="language-python">
def forward(self, x):
    return self.linear(x)
</code></pre>

<!-- DON'T -->
<pre><code class="language-python">
<span class="kw">def</span> <span class="fn">forward</span>(self, x):
    <span class="kw">return</span> self.linear(x)
</code></pre>
```

### 4.3 No Inline Color Styles in Code (INLINE_STYLE_IN_CODE, P2)

Never use `<span style="color: #...">` inside code blocks. Let Prism handle colors.

```html
<!-- DO -->
<pre><code class="language-python">x = torch.tensor([1, 2, 3])</code></pre>

<!-- DON'T -->
<pre><code><span style="color: #569cd6">x</span> = torch.tensor([1, 2, 3])</code></pre>
```

### 4.4 Intro Paragraph Before Code (BARE_CODE_AFTER_HEADING, P1)

Never place a `<pre><code>` block immediately after a heading. Always write at least
one explanatory paragraph between the heading and the code.

```html
<!-- DO -->
<h3>Computing Attention Scores</h3>
<p>The attention score between query and key vectors is computed as a scaled dot product.</p>
<pre><code class="language-python">
scores = torch.matmul(Q, K.T) / math.sqrt(d_k)
</code></pre>

<!-- DON'T -->
<h3>Computing Attention Scores</h3>
<pre><code class="language-python">
scores = torch.matmul(Q, K.T) / math.sqrt(d_k)
</code></pre>
```

### 4.5 Explain Non-Obvious Imports (UNEXPLAINED_IMPORT, P2)

If a code block imports a library that is not part of the standard library or the
common ML/LLM ecosystem, mention it in the surrounding prose within 50 lines.

Well-known libraries that need no explanation include: numpy, torch, pandas,
matplotlib, sklearn, openai, anthropic, transformers, langchain, pydantic, fastapi,
chromadb, tiktoken, and similar ecosystem staples.

```html
<!-- DO -->
<p>We use the <code>outlines</code> library for structured generation.</p>
<pre><code class="language-python">
import outlines
</code></pre>

<!-- DON'T (no mention of "outlines" in nearby prose) -->
<pre><code class="language-python">
import outlines
</code></pre>
```

### 4.6 Code Fragment Numbering (CODE_FRAG_NUM, P1)

Code Fragment numbers must follow the pattern `X.Y.Z` (three numeric segments,
no letter suffixes). They must appear in sequential order.

```html
<!-- DO -->
<div class="code-caption"><strong>Code Fragment 9.3.1:</strong> Tokenizer setup</div>
<div class="code-caption"><strong>Code Fragment 9.3.2:</strong> Encoding text</div>

<!-- DON'T -->
<div class="code-caption"><strong>Code Fragment 9.3.1a:</strong> Tokenizer setup</div>
```

---

## 5. SVG Diagrams

### 5.1 No Redundant Title Text (SVG_TITLE_TEXT, P0)

Do not embed a bold, large title `<text>` element at the top of an SVG if a
`<figcaption>` or caption `<div>` already provides the title below it.

```html
<!-- DO -->
<figure>
  <svg viewBox="0 0 800 400" aria-label="Multi-head attention data flow.">
    <!-- diagram content, no title text element -->
  </svg>
  <figcaption><strong>Figure 6.1.1</strong>: Multi-head attention data flow.</figcaption>
</figure>

<!-- DON'T -->
<svg viewBox="0 0 800 400">
  <text x="400" y="30" font-size="16" font-weight="bold">
    Multi-head Attention Data Flow    <!-- redundant with caption below -->
  </text>
  <!-- ... -->
</svg>
<figcaption><strong>Figure 6.1.1</strong>: Multi-head attention data flow.</figcaption>
```

### 5.2 Text Clipping (SVG_TEXT_CLIPPING, P2)

Ensure all `<text>` elements have coordinates safely inside the viewBox boundaries.
Keep at least 15 units of margin from each edge.

```html
<!-- DO (viewBox is "0 0 800 400") -->
<text x="50" y="30">Safe label</text>

<!-- DON'T -->
<text x="795" y="395">Clipped label</text>  <!-- too close to right and bottom edge -->
```

### 5.3 Text Overflow in Shapes (SVG_TEXT_OVERFLOW, P2)

Text placed inside circles or rectangles must fit within the shape. Estimate the
rendered width (character count * font-size * 0.6) and compare to the container.

### 5.4 Descriptive Aria Labels (GENERIC_SVG_LABEL, P2)

SVG `aria-label` must describe the diagram content, not just say "Diagram" or
"Figure 1".

```html
<!-- DO -->
<svg aria-label="Comparison of BERT and GPT pre-training objectives showing masked language modeling versus autoregressive prediction.">

<!-- DON'T -->
<svg aria-label="Diagram">
<svg aria-label="Figure 1">
<svg aria-label="">
```

### 5.5 Non-Truncated Aria Labels (SVG_ARIA_TRUNCATED, P2)

Aria labels must be complete sentences. They must not end with a preposition,
comma, or trailing article ("the", "a", "and", etc.).

```html
<!-- DO -->
<svg aria-label="Encoder-decoder architecture with cross-attention between layers.">

<!-- DON'T -->
<svg aria-label="Encoder-decoder architecture with cross-attention between the">
```

### 5.6 Panel Symmetry (SVG_PANEL_ASYM, P2)

When an SVG uses side-by-side panels (rectangles at the same y position),
keep their widths within a 1.3x ratio of each other for visual balance.

---

## 6. Math (KaTeX)

### 6.1 No Triple Dollar Signs (TRIPLE_DOLLAR_MATH, P1)

Never write `$$$`. This is a malformed delimiter. Use `$$` for display math and `$`
for inline math, always separated by whitespace or line breaks.

```html
<!-- DO -->
<p>The loss is $L = -\log p(y|x)$.</p>

$$
L = -\sum_{i} y_i \log \hat{y}_i
$$

<!-- DON'T -->
<p>The loss is $L = -\log p(y|x)$$$   <!-- triple dollar -->
L = -\sum_{i} y_i \log \hat{y}_i
$$</p>
```

### 6.2 No Prose Titles Inside Math Blocks (MATH_PROSE_MIXING, P1)

Do not place English-language titles or prose descriptions inside `$$...$$` blocks
using `\textbf{}`. Titles belong in HTML headings or caption elements.

```html
<!-- DO -->
<h3>Cross-Entropy Loss</h3>
$$
L = -\sum_{i} y_i \log \hat{y}_i
$$

<!-- DON'T -->
$$
\textbf{Cross-Entropy Loss} \\
L = -\sum_{i} y_i \log \hat{y}_i
$$
```

### 6.3 Load KaTeX Only When Needed (UNUSED_VENDOR, P1)

Only include KaTeX CSS/JS on pages that contain `$` or `$$` math expressions.
Only include Prism CSS/JS on pages that contain `<pre>` code blocks.

---

## 7. Navigation

### 7.1 TOC Link Target (TOC_LINK_TARGET, P1)

The header TOC link must point to `toc.html`, not `index.html`.

```html
<!-- DO -->
<a href="../toc.html" class="toc-link">Table of Contents</a>

<!-- DON'T -->
<a href="../index.html" class="toc-link">Table of Contents</a>
```

### 7.2 Broken Cross-References (BROKEN_XREF, P0)

Every relative `href` must point to a file that exists on disk. Verify paths
before committing.

```html
<!-- DO -->
<a href="section-5.2.html">next section</a>  <!-- file exists -->

<!-- DON'T -->
<a href="section-5.20.html">next section</a>  <!-- file does not exist -->
```

### 7.3 No Truncated Nav Text (TRUNCATED_NAV, P2)

Navigation link text must not end with an ellipsis. Write the full title.

```html
<!-- DO -->
<a href="section-12.1.html">Transformer Architecture</a>

<!-- DON'T -->
<a href="section-12.1.html">Transformer Arch...</a>
```

---

## 8. Content Quality

### 8.1 No Placeholder Content (PLACEHOLDER_CONTENT, P1)

Published pages must not contain any of these phrases inside `<main>`:
`TODO`, `FIXME`, `TBD`, `placeholder`, `Content pending`, `will be produced`,
`will be generated`, `coming soon`.

### 8.2 No Vague Headings (VAGUE_HEADING, P1)

Headings must be specific enough to stand on their own. Avoid generic titles.

| DON'T | DO |
|---|---|
| "The Algorithm" | "The BERT Masked Language Model Algorithm" |
| "How It Works" | "How Multi-Head Attention Works" |
| "Implementation" | "Implementing the RAG Pipeline" |
| "Example" | "Example: Summarizing Legal Documents" |
| "Overview" | "Overview of Retrieval-Augmented Generation" |
| "Results" | "Results of Fine-Tuning on SQuAD 2.0" |
| "Putting It All Together" | "Putting It All Together: End-to-End Chatbot" |

### 8.3 No Empty Sections (EMPTY_SECTION, P1)

Section files must have at least 100 non-whitespace characters of content inside
`<main>`. Do not commit stub pages.

### 8.4 Section Ordering (SECTION_ORDER, P1)

Structural elements within a section file must follow this order (top to bottom):

1. Epigraph
2. Prerequisites
3. Big-picture callout
4. Body content (headings, paragraphs, code, figures)
5. What's-next
6. Bibliography
7. Chapter nav
8. Footer

Rules:
- Prerequisites must appear before the big-picture callout.
- The big-picture callout must be within the first 100 lines after `<main>`.
- No callouts or headings after the bibliography (except nav/footer).
- What's-next must appear before the bibliography.

### 8.5 Decision Frameworks After Content (DECISION_FRAMEWORK_EARLY, P1)

Summary tables ("Decision Framework", "Method Comparison", "When to Use",
"Choosing Between") must appear after the content they compare, not in the
first 20% of the file.

### 8.6 No Decorative Code Blocks (DECORATIVE_CODE, P1)

Code blocks must teach an engineering concept, not encode a decision tree, lookup
table, or classification taxonomy. If the logic is a simple mapping from inputs to
categories, use an HTML table instead. Code is appropriate when it demonstrates an
API, algorithm, data pipeline, or technique the reader will adapt in their own work.

```html
<!-- DO: use a table for classification/taxonomy -->
<table>
  <thead><tr><th scope="col">Risk Tier</th><th scope="col">Criteria</th><th scope="col">Examples</th></tr></thead>
  <tbody>
    <tr><td>High</td><td>Annex III domain + automated decisions</td><td>Resume screener</td></tr>
    <tr><td>Minimal</td><td>Internal tool, no rights impact</td><td>Code assistant</td></tr>
  </tbody>
</table>

<!-- DON'T: encode the same thing as Python -->
<pre><code class="language-python">
class RiskTier(Enum):
    HIGH = "high"
    MINIMAL = "minimal"

def classify(app):
    if app.domain in HIGH_RISK_DOMAINS:
        return RiskTier.HIGH
    return RiskTier.MINIMAL
</code></pre>
```

Signals that a code block is decorative (2+ in non-engineering chapters triggers the audit):
- Enum class with 3+ string-valued members
- Dict literal with 3+ keys mapping to string lists
- @dataclass with all-string fields and no computation
- if/elif chain with 3+ branches returning enum/string values

### 8.7 Callout Type Consistency (CALLOUT_TYPE_MISMATCH, P2)

The callout CSS class must match its title text. For example, a callout with
title "Fun Fact" must use class `callout fun-note`, not `callout hands-on`.

| Title Text | Required Class |
|---|---|
| Fun Fact | `callout fun-note` |
| Hands-On | `callout hands-on` |
| Key Insight | `callout key-insight` |
| Big Picture | `callout big-picture` |
| Warning / Caution | `callout warning` |
| Algorithm | `callout algorithm` |
| Library Shortcut | `callout library-shortcut` |

---

## 9. Vendor and Asset Paths

### 9.1 Consistent Vendor Prefixes (VENDOR_PATH_PREFIX, P3)

Within a single file, use one consistent prefix for vendor assets. Do not mix
`./vendor/`, `vendor/`, and `../vendor/` in the same file.

```html
<!-- DO (pick one prefix, use it everywhere) -->
<link href="../vendor/katex/katex.min.css" rel="stylesheet">
<script src="../vendor/prism/prism.min.js"></script>

<!-- DON'T -->
<link href="./vendor/katex/katex.min.css" rel="stylesheet">
<script src="../vendor/prism/prism.min.js"></script>  <!-- different prefix -->
```

---

## Quick Reference: Priority Levels

| Priority | Meaning | Action |
|---|---|---|
| P0 | Broken content (dead links, duplicate numbers, redundant SVG titles) | Fix before any commit |
| P1 | Structural or accessibility issues (missing tags, bad scope, placeholders) | Fix in current session |
| P2 | Polish and consistency (missing dims, generic labels, style mixing) | Fix when editing the file |
| P3 | Minor style nits (vendor path prefix inconsistency) | Fix opportunistically |
