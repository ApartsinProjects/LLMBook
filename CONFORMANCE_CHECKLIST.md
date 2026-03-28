# Conformance Checklist

This is the single source of truth for ALL formatting, structural, and content requirements
across every HTML file in the book. The Controller Agent reads this file before
every sweep to know exactly what to check and fix.

**Maintained by**: Controller Agent + Meta Agent + user directives
**Last updated**: 2026-03-28

---

## A. Header Structure

Every `section-*.html` file:
- [ ] `.chapter-header` contains three elements in this exact order (top to bottom):
  1. `.part-label` (top): Part name, hyperlink to **part index** (`../index.html`)
  2. `.module-label` (middle): Module number, hyperlink to **module index** (`index.html`)
  3. `h1` (bottom): Section title
- [ ] Order is: Part → Module → Section title (hierarchy from broadest to most specific)
- [ ] All three use consistent font family (inherit from header)
- [ ] Part label: `<div class="part-label"><a href="../index.html">Part N: Name</a></div>`
- [ ] Module label: `<div class="module-label"><a href="index.html">Module XX: Title</a></div>`
- [ ] Section title: `<h1>Section Title</h1>`
- [ ] Link colors: part label `rgba(255,255,255,0.85)`, module label `rgba(255,255,255,0.7)`
- [ ] Both links present, no inline styles except color and text-decoration on the `<a>` tags
- [ ] Canonical HTML:
```html
<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part N: Name</a></div>
    <div class="module-label"><a href="index.html" style="color: rgba(255,255,255,0.7); text-decoration: none;">Module XX: Title</a></div>
    <h1>Section Title</h1>
</header>
```

Every `index.html` (module level):
- [ ] Header links to book ToC (`../../index.html`) and part index (`../index.html`)
- [ ] Lists all section files that actually exist on disk (no broken links, no missing sections)
- [ ] Section titles match the actual `<h1>` in each corresponding section file
- [ ] Contains a brief description and annotated chapter listing with hyperlinks

## B. Epigraph

- [ ] Present in every section file, immediately after `.chapter-header` inside `.content`
- [ ] Uses `<blockquote class="epigraph">` with CSS class (no inline styles)
- [ ] Attribution format: `<cite>A [Adjective] AI Agent</cite>` (e.g., "A Weary AI Agent", "A Philosophical AI Agent")
- [ ] Attribution must NOT use character names (e.g., NOT "Cautious Gradient")
- [ ] Content is relevant to the chapter topic, not generic filler
- [ ] Maximum one epigraph per file (idempotency guard)
- [ ] Canonical CSS present in `<style>` block:

```css
.epigraph {
    max-width: 600px;
    margin: 2rem auto 2.5rem;
    padding: 1.2rem 1.5rem;
    border-left: 4px solid var(--highlight, #e94560);
    background: linear-gradient(135deg, rgba(233,69,96,0.04), rgba(15,52,96,0.04));
    border-radius: 0 8px 8px 0;
    font-style: italic;
    font-size: 1.05rem;
    line-height: 1.6;
    color: var(--text, #1a1a2e);
}
.epigraph cite {
    display: block; text-align: right; font-style: normal;
    font-size: 0.9rem; color: var(--highlight, #e94560); font-weight: 600;
}
.epigraph cite::before { content: "\2014\00a0"; }
```

## C. Prerequisites

- [ ] Present in every section file, after epigraph, before first content heading
- [ ] Uses `<div class="prerequisites">` with CSS class (no inline styles)
- [ ] Written as **flowing prose** with inline `<a href>` links (NEVER bulleted `<ul>/<li>` lists)
- [ ] Links use correct relative paths to earlier sections (same-part: `../module-XX/section-X.Y.html`, different-part: `../../part-N/module-XX/section-X.Y.html`)
- [ ] Contains `<h3>Prerequisites</h3>` followed by one or two `<p>` paragraphs
- [ ] Canonical CSS present in `<style>` block:

```css
.prerequisites {
    max-width: 600px;
    margin: 1.5rem auto 2rem;
    padding: 1.2rem 1.5rem;
    background: linear-gradient(135deg, rgba(15,52,96,0.04), rgba(233,69,96,0.02));
    border: 1px solid rgba(15,52,96,0.12);
    border-radius: 8px;
    font-size: 0.95rem;
    line-height: 1.6;
}
.prerequisites h3::before { content: "\1F4CB\00a0"; }
.prerequisites a {
    color: var(--highlight, #e94560);
    text-decoration: none;
    border-bottom: 1px dotted var(--highlight, #e94560);
}
```

## D. Callout Boxes

- [ ] Only 7 canonical class names are used:
  1. `big-picture` (purple: `#f3e5f5` / `#f0e6ff`, border `#8e44ad`)
  2. `key-insight` (green: `#e8f5e9`, border `#27ae60`)
  3. `note` (blue: `#e8f4fd`, border `#3498db`)
  4. `warning` (amber: `#fef9e7` / `#fff8e1`, border `#f39c12`)
  5. `practical-example` (light grey: `#f5f5f5`, border `#78909c`)
  6. `fun-note` (pink/yellow: pink gradient, gold border)
  7. `research-frontier` (teal: `#e0f2f1` / `#e0f7fa`, border `#00897b`)
- [ ] No variant names such as: `callout-note`, `callout-insight`, `callout-warning`, `callout-error`, `callout-big-picture`
- [ ] CSS definitions for all 7 types present in every file's `<style>` block
- [ ] At least 1 `key-insight` (mental model) per section file
- [ ] At least 1 `practical-example` per section file
- [ ] Maximum 5 to 6 callout boxes per section (avoid overloading the page)
- [ ] Every callout box is referenced or connected to surrounding prose text
- [ ] Each callout type has a visually distinct background, icon, and border color
- [ ] Canonical callout-title icons (HTML entities in the `.callout-title` div):
  1. `big-picture`: `&#9733; Big Picture` (★ star)
  2. `key-insight`: `&#128161; Key Insight` (💡 lightbulb)
  3. `note`: `&#128221; Note` (📝 memo)
  4. `warning`: `&#9888; Warning` (⚠ warning sign)
  5. `practical-example`: `&#x1F3D7;&#xFE0F; Application Example` (🏗️ construction)
  6. `fun-note`: `&#127914; Fun Fact` (🎪 circus tent)
  7. `research-frontier`: `&#128300; Research Frontier` (🔬 microscope)
- [ ] Icon must appear as the first character(s) in the `.callout-title` text, followed by a space and the title word(s)

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

- [ ] `<div class="whats-next">` present in every section file
- [ ] Positioned after Research Frontier, before Bibliography
- [ ] Uses CSS class definition (NO inline `style=` attribute on the div)
- [ ] Contains a transition sentence describing the next topic
- [ ] Contains a hyperlink to the next section in reading order
- [ ] Canonical CSS in `<style>` block:

```css
.whats-next {
    background: linear-gradient(135deg, #e3f2fd, #e8eaf6);
    border: 1px solid #90caf9;
    border-radius: 10px;
    padding: 1.5rem 1.8rem;
    margin: 2rem 0;
}
.whats-next h3 { color: #1565c0; margin-bottom: 0.8rem; }
```

## H. Bibliography

- [ ] `<section class="bibliography">` present as last content element (before nav footer)
- [ ] Uses card-based format with `.bib-entry-card` (NOT old `<ol class="bib-list">` format)
- [ ] At least 3 entries per section file, each with 2 to 3 sentence annotations
- [ ] Annotations explain: what the reference contains, why it is relevant, who should read it
- [ ] Real, clickable URLs (arXiv, ACL Anthology, GitHub, official docs)
- [ ] Maximum one bibliography per file (idempotency guard)
- [ ] CSS definitions in `<style>` block for: `.bibliography`, `.bibliography-title`, `.bib-entry-card`, `.bib-ref`, `.bib-annotation`, `.bib-meta`

## I. Navigation Footer

- [ ] Prev/Next links present pointing to correct adjacent sections
- [ ] "Up" link pointing to module `index.html`
- [ ] Links are correct and bidirectional (section A's "next" matches section B's "prev")
- [ ] No duplicate navigation bars (old `<nav class="chapter-nav">` removed)

## J. CSS Completeness

Every file's `<style>` block must contain definitions for:
- [ ] CSS custom properties (`:root` block with `--primary`, `--accent`, `--highlight`, `--bg`, `--text`)
- [ ] `.epigraph` (and sub-selectors: `cite`, `cite::before`)
- [ ] `.prerequisites` (and sub-selectors: `h3::before`, `a`)
- [ ] `.whats-next` (and sub-selectors: `h3`)
- [ ] `.bibliography` (and sub-selectors: `.bibliography-title`, `.bib-entry-card`, `.bib-ref`, `.bib-annotation`)
- [ ] `.code-caption`
- [ ] All 7 `.callout` variants (big-picture, key-insight, note, warning, practical-example, fun-note, research-frontier)
- [ ] `.lab` (if the file contains a lab section)
- [ ] `.diagram-container` and `.diagram-caption` (if the file contains diagrams)

No recurring element should use inline `style=` when a CSS class exists for it.

## K. Responsive CSS

- [ ] Media query for 1024px (tablet): content max-width 100%, reduced padding, SVG scaling
- [ ] Media query for 768px (iPad Mini): smaller fonts, scrollable tables/code blocks, adjusted callout boxes
- [ ] Media query for 480px (mobile): tighter padding, full-width epigraph/prerequisites

## L. Cross-References

- [ ] At least 3 cross-module hyperlinks per section file
- [ ] Links use correct relative paths:
  - Same part: `../module-XX/section-X.Y.html`
  - Different part: `../../part-N/module-XX/section-X.Y.html`
- [ ] No broken hrefs (all targets exist on disk)
- [ ] Progressive depth concepts linked with context-differentiating language (see section U)
- [ ] Big Picture boxes contain backward-facing links to previous chapters where the concept was introduced

## M. Content Width Rules

- [ ] `.content` container: `max-width: 820px`
- [ ] `.epigraph`: `max-width: 600px` (intentionally narrower, centered)
- [ ] `.prerequisites`: `max-width: 600px` (intentionally narrower, centered)
- [ ] Everything else inherits from `.content` (no separate conflicting max-width)
- [ ] No sections appear visually wider or narrower than expected due to rogue inline styles

## N. Style Rules

- [ ] No em dashes (the character U+2014) anywhere in text
- [ ] No double dashes (`--`) used as punctuation in prose
- [ ] No "syllabus" or "course" when referring to the book (use "book", "chapter", "module", "section")
- [ ] No placeholder text ("TODO", "TBD", "Lorem ipsum", "[placeholder]")
- [ ] No patronizing phrases ("Great job!", "Congratulations!", "Well done!")
- [ ] All claims have intuitive or formal justification (no unjustified assertions)
- [ ] Acronyms and proper nouns in prerequisites and prose are correctly capitalized (e.g., "LLM APIs" not "llm apis", "PyTorch" not "pytorch")
- [ ] Prerequisites text reads as natural, complete prose (no truncated sentences, garbled text, or broken HTML entities)
- [ ] Every concept answers: what it is, why it matters, how it works, when to use it
- [ ] Text is justified with auto-hyphens (`text-align: justify; hyphens: auto;`)

## O. Figures and Tables

- [ ] Every figure has a caption with section-aligned numbering: `Figure [Section].[Seq]` (e.g., Figure 3.2.1)
- [ ] Every table is introduced in preceding prose text
- [ ] Every diagram wrapped in `<div class="diagram-container">`
- [ ] All images have meaningful alt text (not empty, not "image")
- [ ] SVGs use book color palette (`#1a1a2e`, `#0f3460`, `#e94560`, `#f8f9fa`)
- [ ] SVG coordinate correctness verified (y=0 is top of viewport; minima at high y values, maxima at low y values)
- [ ] Every figure is referenced in surrounding prose text before it appears

## P. Element Ordering (within each section file)

Mandatory order in every section file:
1. Chapter header (`.chapter-header` with module-label, h1, subtitle)
2. Epigraph (immediately after header, inside `.content`)
3. Prerequisites (immediately after epigraph)
4. Section content (prose, callouts, code, figures, exercises, labs)
5. Research Frontier (`.callout.research-frontier`, after all content)
6. What's Next (`.whats-next`, after Research Frontier)
7. Bibliography (`<section class="bibliography">`, last before nav footer)
8. Navigation footer (prev/next/up links)

## Q. Illustrations

- [ ] Chapter opener illustration in every module `index.html` (Gemini-generated PNG in `images/` subfolder)
- [ ] Illustrations wrapped in `<figure class="illustration">` with `<figcaption>`
- [ ] Inline SVG diagrams wrapped in `<div class="diagram-container">`
- [ ] Illustration style: Kurzgesagt-inspired flat vector art (bright, educational, slightly humorous)
- [ ] 5 to 8 illustrations per module across all section files
- [ ] Illustration types include: algorithm-as-scene, architecture-as-building, concept-as-character, system-as-ecosystem, analogy, mental-model

## R. Mental Models

- [ ] At least 1 `key-insight` callout (mental model, analogy, or "aha moment") per section file
- [ ] Mental model explains the concept using a concrete analogy, comparison, or visualization
- [ ] Mental model is placed near the concept it illuminates, not relegated to the end

## S. Fun Notes

- [ ] Maximum 1 to 2 `fun-note` callouts per section (quality over quantity)
- [ ] Humor is in good taste: witty analogy, self-aware aside, absurdist comparison, understatement, playful personification, or relatable frustration
- [ ] Not patronizing, forced, or cringeworthy
- [ ] Related to the section content (not random)

## T. Inline Style Elimination

- [ ] No `style=` attributes on elements where a CSS class exists for that purpose
- [ ] Specifically check: epigraph, prerequisites, whats-next, callout boxes, bibliography, code-caption, lab
- [ ] Header link colors may use inline style for `color` on `<a>` tags (acceptable exception)

## U. Progressive Depth Cross-Linking

The following concepts appear in multiple chapters at different depth levels. Each occurrence must include a cross-reference link with context-differentiating language:

| Concept | Locations | Context Differences |
|---------|-----------|---------------------|
| Attention | Section 3.2, Section 4.1, Section 8.3 | intuition, multi-head detail, optimization |
| GQA (Grouped Query Attention) | Section 4.2, Section 7.1, Section 8.2 | mechanism, model usage, efficiency |
| MoE (Mixture of Experts) | Section 7.1, Section 8.4 | architecture, inference optimization |
| Embeddings | Section 1.3, Section 18.1, Section 18.2 | word2vec, semantic search, vector DBs |
| Catastrophic forgetting | Section 13.2, Section 14.1 | full fine-tuning, PEFT motivation |
| Temperature | Section 5.1, Section 9.2 | decoding theory, API parameter |
| Tokenization | Section 2.1, Section 2.2, Section 2.3 | concept, BPE, sentencepiece |
| Prompt injection | Section 10.3, Section 26.3 | attack patterns, production defense |
| RLHF/DPO | Section 16.1, Section 16.2, Section 16.3 | theory, RLHF practice, DPO alternative |

Link phrasing must differentiate context: "for the intuitive introduction, see Section 3.2" vs. "for multi-head implementation details, see Section 4.1".

## V. Index/ToC Synchronization

Three levels of index must stay synchronized:

**Book-level** (`index.html`):
- [ ] Lists all 7 parts with links to part index pages
- [ ] Lists all modules (currently 28+) with links to module index pages
- [ ] Module titles match actual `<h1>` in module index files
- [ ] Writing Team link reflects current agent count

**Part-level** (`part-*/index.html`):
- [ ] Lists all modules within that part with links to module index pages
- [ ] Each module card lists all section files with hyperlinks
- [ ] Section titles match actual `<h1>` in section files
- [ ] Links to adjacent part index pages and back to book index

**Module-level** (`part-*/module-*/index.html`):
- [ ] Lists all section files that exist on disk
- [ ] Section titles match actual `<h1>` in section files
- [ ] Contains chapter opener illustration
- [ ] Contains epigraph and description
- [ ] Links back to part index and book index

## W. Agent Team HTML (`team.html`)

- [ ] Reflects current pipeline state (agent count, phase count)
- [ ] Each agent card includes: avatar, name, role title, 3 to 5 sentence description
- [ ] Pipeline workflow table references agents by `#NN Name (Role)` format
- [ ] Stats bar matches actual agent/phase counts
- [ ] "Back to Book Home" link (not "Back to Course Home")
- [ ] All avatar images exist in `agents/avatars/` directory

## X. Labs

- [ ] Labs (when present) placed after exercises, before Research Frontier
- [ ] Uses `<div class="lab">` with CSS class
- [ ] Structure: Objective, What You'll Practice, Setup, Guided Steps (with TODOs and hints), Expected Output, Stretch Goals, Solution
- [ ] 1 to 2 labs per module, 30 to 90 minutes each
- [ ] Idempotency guard: check for existing `class="lab"` before adding
- [ ] Lab CSS definitions in `<style>` block for: `.lab`, `.lab-meta`, `.lab-step`, `.lab-expected`, `.lab-stretch`, `.lab-solution`

---

## Book-Specific Requirements

These items are specific to the current book ("Building Conversational AI using LLM and Agents") rather than generic formatting rules.

### Module 26/27/28 Split Structure

Module 26 was split into three modules:
- [ ] Module 26: Production Engineering (sections 26.1 to 26.4)
- [ ] Module 27: Safety, Ethics, and Regulation (formerly sections 26.5 to 26.11, renumbered as 27.1 to 27.7)
- [ ] Module 28: Strategy, Product, and ROI (formerly old Module 27, renumbered as 28.1 to 28.5)
- [ ] All internal cross-references updated to reflect renumbering
- [ ] Part 7 index page reflects the three-module structure

### Content Update Plan Tiers

All tiers from `CONTENT_UPDATE_PLAN.md` should be addressed:
- [ ] Tier 1 (Essential Now): 9 new sections created, 6 critical expansions completed
- [ ] Tier 2 (Useful Soon): 20 important additions integrated
- [ ] Tier 3 (Nice to Have): 18 additions integrated where appropriate

### New Sections Created

These sections were created to fill content gaps:
- [ ] Section 8.5: Model Pruning and Sparsity
- [ ] Section 9.4: Reasoning Models and Multimodal APIs
- [ ] Section 10.5: Prompting Reasoning and Multimodal Models
- [ ] Section 12.7: Synthetic Reasoning Data
- [ ] Section 18.5: Vision-Based Document Retrieval (ColPali, ColQwen)
- [ ] Section 21.5: Reasoning Models and Agent Architecture (MCP ecosystem)
- [ ] Section 22.4: Multi-Agent Communication Patterns
- [ ] Section 23.4: Document AI
- [ ] Section 25.8: Advanced Evaluation Methods

### Tech Stack Currency

The Content Update Scout should verify coverage of:
- [ ] Current Python libraries: vLLM, SGLang, Unsloth, CrewAI, LangChain, LangGraph, LlamaIndex, DSPy, Outlines, instructor
- [ ] Current models: DeepSeek-R1, Llama 4, Phi-4, Gemini 2.x, Claude 3.x/4.x, GPT-4o/o1/o3
- [ ] Protocols and standards: MCP (Model Context Protocol), A2A (Agent-to-Agent)
- [ ] Disaggregated inference, speculative decoding, PagedAttention

### Badge System

- [ ] Difficulty badges: Basic (green), Intermediate (yellow), Advanced (red)
- [ ] Focus badges: Fundamentals, Engineering, Research, Lab
- [ ] Badges synchronized across main index, part index, and module index pages

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
| 2026-03-28 | Header order changed: Part (top) → Module (middle) → Section title (bottom). Renamed `.subtitle` to `.part-label`. Consistent fonts. | User directive: "Part should be first" |
