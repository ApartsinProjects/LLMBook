# Anomalous Styling / Typesetting Audit

Scope: new chapters Ch 34, 36, 41, 46, 56, 59, 61 plus Wave 17i consolidated sections (24.6, 24.13, 26.6, 27.5, 29.1, 29.4, 35.2, 35.3, 37.3).

Reference canonical section template: `agents/book-skills/templates/section-template.html` and the CONTENT_GUIDELINES.md rules (P0/P1/P2 severity).

The canonical structural order inside `<main>` is:
1. Epigraph (`<blockquote class="epigraph">`)
2. Prerequisites (`<div class="prerequisites">`)
3. Big-picture callout (`<div class="callout big-picture">`)
4. Body (headings `<h2>N.M.K Title</h2>`, content)
5. What's-next / chapter-end content
6. Bibliography
7. Closing `</main>`
8. Chapter-nav (`<nav class="chapter-nav">`)
9. Footer (`<footer>`)

Section-numbering canonical form for headings: `<h2 id="...">N.M.K Title</h2>` where `K` is the sub-sub-section number (e.g. `<h2>34.1.1 The Information Extraction Landscape</h2>`).

Severity: P0 = broken content; P1 = structural / accessibility; P2 = polish; P3 = nit.

---

## High-impact anomalies (likely already on the engineering team's radar)

### Pattern A: missing big-picture callout at top of section

| File | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html`:27 | P1 | Section opens directly into `<h2 id="34-1-1-the-information-extraction-landscape">34.1.1 The Information Extraction Landscape</h2>` with no big-picture callout above. The big-picture callout is structural per template. | Add `<div class="callout big-picture">` between `</span></span></span></main>` opening and the first `<h2>`. |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html`:27 | P1 | Same pattern, jumps directly into `<h2>34.2.2 Classical IE with spaCy</h2>` with no big-picture. | Same fix. |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html`:27 | P1 | Same pattern. Opens directly into `34.3.4 Hybrid IE Architectures`. | Same fix. |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.4.html`:27 | P1 | Same pattern. Opens directly into `34.4.5 Production Deployment Patterns`. | Same fix. |
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.5.html`:27 | P1 | Same pattern. Opens directly into `34.5.7 Coreference Resolution`. | Same fix. |

### Pattern B: missing epigraph (all of Ch 34 and Ch 46 sections)

| File | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html`:26 | P2 | No `<blockquote class="epigraph">` at section open. Compare to 35.2 which has one. | Add an epigraph with agent-avatar attribution before the big-picture callout. |
| Same for `section-34.2.html`, `section-34.3.html`, `section-34.4.html`, `section-34.5.html` | P2 | Same. | Same fix. |
| `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html`:24 | P2 | No epigraph. | Same fix. |
| Same for `section-46.2.html`, `section-46.3.html`, `section-46.4.html`, `section-46.5.html` | P2 | Same. | Same fix. |
| `part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.1.html`:25 | P2 | No epigraph. | Same fix. |
| Same for `section-56.2.html` through `section-56.5.html` | P2 | Same. | Same fix. |
| `part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.1.html`:23 | P2 | No epigraph. | Same fix. |
| Same for `section-36.2.html` through `section-36.5.html` | P2 | Same. | Same fix. |
| `part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.1.html`:27 | P2 | No epigraph. | Same fix. |
| Same for `section-41.2.html` through `section-41.5.html` | P2 | Same. | Same fix. |
| `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.1.html`:36 | P2 | No epigraph. | Same fix. |
| Same for `section-59.2.html` through `section-59.5.html` | P2 | Same. | Same fix. |
| `part-12-llm-systems-at-scale/module-61-scale-tools/section-61.1.html`:23 | P2 | No epigraph. | Same fix. |
| Same for `section-61.2.html` through `section-61.5.html` | P2 | Same. | Same fix. |

### Pattern C: non-canonical opening h2 numbering (e.g. starting at .2 or .4 not .1)

| File | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| `module-34-structured-information-extraction-ner/section-34.2.html`:27 | P1 | First `<h2>` is `34.2.2 Classical IE with spaCy` (starts at .2 not .1). Suggests prior consolidation deleted a leading `34.2.1` that introduced the section. | Renumber starting from `34.2.1` (or restore a `34.2.1` intro subsection). |
| `module-34-structured-information-extraction-ner/section-34.3.html`:27 | P1 | First `<h2>` is `34.3.4 Hybrid IE Architectures` (starts at .4). | Same fix. |
| `module-34-structured-information-extraction-ner/section-34.4.html`:27 | P1 | First `<h2>` is `34.4.5 Production Deployment Patterns` (starts at .5). | Same fix. |
| `module-34-structured-information-extraction-ner/section-34.5.html`:27 | P1 | First `<h2>` is `34.5.7 Coreference Resolution` (starts at .7). | Same fix. |
| `module-46-llm-as-judge-automated-evaluation/section-46.1.html`:25 | P1 | First `<h2>` is `46.1.1 Judge Bias Taxonomy` (looks OK in number but flows into Production Pattern P9 immediately - misaligned with section title "Why LLM-as-Judge Matters"). | Verify alignment of h2 title with section title. |
| `module-46-llm-as-judge-automated-evaluation/section-46.2.html`:25 | P1 | First `<h2>` is `46.2.2 G-Eval` (starts at .2). | Same fix. |
| `module-46-llm-as-judge-automated-evaluation/section-46.3.html`:25 | P1 | First `<h2>` is `46.3.3 Prometheus and Prometheus 2` (starts at .3). | Same fix. |
| `module-46-llm-as-judge-automated-evaluation/section-46.4.html`:25 | P1 | First `<h2>` is `46.4.4 JudgeLM` (starts at .4). | Same fix. |
| `module-46-llm-as-judge-automated-evaluation/section-46.5.html`:25 | P1 | First `<h2>` is `46.5.5 AlpacaEval` (starts at .5). | Same fix. |

This is the strongest signal that Ch 34 and Ch 46 were stitched from larger sections during consolidation and the numbering was never re-normalized. **Recommended: P1 high-priority renumber pass.**

### Pattern D: malformed pagefind-meta-injected span (Ch 46)

| File | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| `module-46-llm-as-judge-automated-evaluation/section-46.1.html`:24 | P0 | Span tag is malformed: `<span class="pagefind-meta-injected" f: LLM-as-Judge &amp; Automated Evaluation" hidden=""></span>` - the `data-pagefind-meta="chapter:Chapter 46:` prefix has been dropped. The `f:` looks like a truncated `chapter:` attribute. | Repair to `<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 46: LLM-as-Judge &amp; Automated Evaluation" hidden=""></span>`. |
| `module-46-llm-as-judge-automated-evaluation/section-46.2.html`:24 | P0 | Same malformed span. | Same fix. |
| `module-46-llm-as-judge-automated-evaluation/section-46.3.html`:24 | P0 | Same malformed span. | Same fix. |
| `module-46-llm-as-judge-automated-evaluation/section-46.4.html`:24 | P0 | Same malformed span. | Same fix. |
| `module-46-llm-as-judge-automated-evaluation/section-46.5.html`:24 | P0 | Same malformed span. | Same fix. |

This is a broken-content issue (P0). It silently breaks Pagefind search faceting for all of Chapter 46.

### Pattern E: chapter-nav location and `</main>` ordering inconsistency

The canonical pattern (in Ch 34 sections) is: `</main>` then `<nav class="chapter-nav">` then `<footer>`. Some new chapter sections invert this.

| File | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| `module-36-retrieval-tools/section-36.1.html`:264-273 | P1 | Has `<nav class="section-nav"></nav>` then `<nav class="chapter-nav">` INSIDE `<main>` (closes `</main>` at line 270), then `<footer>` outside. Compare with Ch 34 which has `</main>` first. | Either standardize the whole book on "nav inside main" or "nav outside main"; per FOOTER_PLACEMENT (CONTENT_GUIDELINES sec 1.14) the majority pattern wins. The majority of new chapter sections in 36, 41, 56, 59, 61 all place chapter-nav INSIDE `<main>`. The older Ch 34 places it OUTSIDE `<main>`. **Recommendation**: pick one and audit-fix the other. |
| All `section-36.*.html` | P1 | Same pattern (chapter-nav inside main). | Same. |
| All `section-41.*.html` | P1 | Same pattern. | Same. |
| All `section-56.*.html` | P1 | Same pattern. | Same. |
| All `section-59.*.html` | P1 | Same pattern. | Same. |
| All `section-61.*.html` | P1 | Same pattern. | Same. |
| All `section-34.*.html` | P1 | Chapter-nav OUTSIDE `</main>` (older canonical pattern). | Same. |
| All `section-46.*.html` | P1 | Chapter-nav OUTSIDE `</main>`. | Same. |

This is the single biggest cross-chapter structural inconsistency. Once a pattern is picked, an automated pass can normalize all sections.

### Pattern F: bibliography format inconsistency

Three distinct bibliography formats are in active use across the new chapters:

1. **`<div class="bib-entries"> + <div class="bib-entry-card"> + <div class="bib-ref">`** - the canonical 2026 format. Used by Ch 36, 41, 56.
2. **`<section class="bibliography"> + <h2>Bibliography</h2> + <ol>`** - simpler format. Used by Ch 59.
3. **Inline mentions only, no Bibliography section** - used by Ch 34, 46.

| File | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| All `section-34.*.html` | P1 | No Bibliography section at the end. The cite-style references are inline only (e.g. "Tobin et al., 2017, arXiv:1703.06907"). | Add a `<div class="bib-entries">` Bibliography section before `</main>` for each subsection, listing the cited papers. |
| All `section-46.*.html` | P1 | No Bibliography section. | Same fix. |
| `section-59.1.html` line 280, `section-59.3.html` line 339, `section-59.4.html` line 393, `section-59.5.html` line 281 | P2 | Uses `<section class="bibliography"><h2>Bibliography</h2><ol>` format. Different from Ch 36/41/56's `<div class="bib-entries">` card format. | Standardize to `<div class="bib-entries">` format for consistent CSS styling. |
| `section-59.2.html` | P2 | Verify; likely same format as 59.1. | Same. |

### Pattern G: non-canonical h2 ID-versus-text format

Canonical: `<h2 id="34-1-1-the-information-extraction-landscape">34.1.1 The Information Extraction Landscape</h2>` (kebab-case ID with numeric dashes; text starts with `N.M.K`).

| File | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| `module-36-retrieval-tools/section-36.1.html`:30 | P2 | `<h2 id="36-1-1-serverless-and-hosted-vector-databases">36.1.1 Serverless and hosted vector databases</h2>` - heading text uses lowercase "S" / "h" in the title body. Compare to Ch 34's title-case `34.1.1 The Information Extraction Landscape`. | Either standardize Ch 36 to title-case or document a per-chapter style. Recommendation: title-case. |
| All `section-36.*.html`, `section-41.*.html`, `section-56.*.html`, `section-61.*.html` h2 headings | P2 | Use sentence-case in headings. | Standardize. |
| All `section-34.*.html`, `section-46.*.html`, `section-59.*.html` h2 headings | P2 | Use Title-Case in headings. | Standardize. |

This is the second-biggest visible inconsistency. Sentence-case is fine if used everywhere, but mixed is jarring.

### Pattern H: prerequisites block missing or partial

| File | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| All `section-34.*.html` | P1 | No `<div class="prerequisites">` block. Template requires it for the first section in a chapter. | Add prerequisites at least to `section-34.1.html` (the first section in the chapter). |
| All `section-36.*.html` | P1 | Same. | Add to `section-36.1.html`. |
| All `section-41.*.html` | P1 | Same. | Add to `section-41.1.html`. |
| All `section-46.*.html` | P1 | Same. | Add to `section-46.1.html`. |
| All `section-56.*.html` | P1 | Same. | Add to `section-56.1.html`. |
| All `section-59.*.html` | P1 | Same. | Add to `section-59.1.html`. |
| All `section-61.*.html` | P1 | Same. | Add to `section-61.1.html`. |
| `module-26-ai-agents/section-26.6.html` line 38-41 | OK | Has `<div class="prerequisites">`. | None. |
| `module-27-tool-use-protocols/section-27.5.html` line 40-43 | OK | Has prerequisites. | None. |
| `module-29-specialized-agents/section-29.1.html` line 40-43 | OK | Has prerequisites. | None. |
| `module-29-specialized-agents/section-29.4.html` line 40-43 | OK | Has prerequisites. | None. |
| `module-35-advanced-rag/section-35.2.html` line 40-43 | OK | Has prerequisites. | None. |
| `module-37-conversational-ai/section-37.3.html` line 39-42 | OK | Has prerequisites. | None. |
| `module-24-vla-models/section-24.6.html` | P2 | Verify; appears not to have prerequisites block. | Add if missing. |
| `module-24-vla-models/section-24.13.html` | P2 | Verify; appears not to have prerequisites block. | Add if missing. |

---

## Specific anomalies (file:line indexed)

### Section 34.1 (`section-34.1.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 36 | P2 | `<div class="comparison-table-title"><strong>Table 34.1.1</strong>:</strong> <em>1.1 Classical IE vs. LLM-Based IE (as of 2026).</em></div>` - has stray extra `</strong>` closing tag after the colon, and the table caption begins with "1.1" (artifact of consolidation; should read "Table 34.1.1: Classical IE..."). | Repair to: `<div class="comparison-table-title"><strong>Table 34.1.1</strong>: <em>Classical IE vs. LLM-Based IE (as of 2026).</em></div>`. (P0 actually - this is malformed HTML.) |
| 37 | P2 | `<table>` has no `class` attribute and no `<thead>`. Per CONTENT_GUIDELINES 2.1 every table must have `<thead>`. Rows are plain `<tr><th scope="col">...</th>...</tr>`. | Wrap header row in `<thead>` and add `class="complex-table"` if intended. |
| 53 | P2 | SVG opens `<svg aria-label="Diagram" ...>` - generic aria-label per CONTENT_GUIDELINES 5.4. | Replace with descriptive aria-label like `"IE pipeline comparison: classical NER versus LLM-based extraction"`. |
| 130 | P2 | `<main>` closes here; `<nav class="chapter-nav">` is OUTSIDE main. See Pattern E above. | Standardize. |
| Missing | P2 | No Bibliography section. See Pattern F. | Add. |

### Section 34.2 (`section-34.2.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 27 | P1 | Opens with `<h2>34.2.2 Classical IE with spaCy</h2>` (skips 34.2.1). | Renumber. |
| 32 | P2 | "Code Fragment 34.2.10" referenced in prose but actual caption (line 82) is `Code Fragment 34.2.1`. Section uses 34.2.1 - 34.2.5 captions. Per CONTENT_GUIDELINES 3.3 BROKEN_FIGURE_REF. | Replace "34.2.10" prose references with the correct code fragment number. |
| 34-66 | P2 | The `<pre><code class="pygments-highlighted lang-python">` class uses `lang-python` rather than the CONTENT_GUIDELINES-mandated `language-python`. CONTENT_GUIDELINES 4.1 specifies `language-*` classes. | Replace `lang-python` with `language-python` throughout. (Note: this affects almost every code block across all new chapters - sweeping change.) |
| 36-37 | P2 | Embedded `comparison-table` with `<table class="complex-table">` but inside the `comparison-table` wrapper. Some Ch 34 tables use this pattern, others use a bare `<table>` with no class. | Standardize. |
| 84 | P1 | "Code Fragment 34.2.10" - broken figure reference (see above). | Same. |
| 207 | P0 | "Output" code block shows `confidence=0.96 span="competes with OpenAI's ChatGPT"` followed by an unclosed `</div>` pattern after the `<pre>` ends but before `<div class="code-caption">`. Verify the wrapper closes properly. | Audit. |
| 211 | P2 | `<div class="comparison-table-title"><strong>Table 34.2.2:</strong> <em>Dimension Comparison (as of 2026).</em></div>` - title is generic "Dimension Comparison" (per CONTENT_GUIDELINES 8.2 VAGUE_HEADING - applies to captions too). | Replace with a descriptive title like "Stanford OpenIE vs REBEL vs LLM-Based Open IE". |

### Section 34.3 (`section-34.3.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 27 | P1 | Opens with `<h2>34.3.4 Hybrid IE Architectures</h2>` (skips 34.3.1, 34.3.2, 34.3.3). | Renumber. |
| 29 | P2 | Reference to "Figure 34.3.2" appears before any "Figure 34.3.1" caption exists. Per CONTENT_GUIDELINES 3.2 FIGURE_SEQUENCE - must start at .1. | Renumber figure to 34.3.1. |
| 32 | P2 | SVG aria-label is `"Diagram: Hybrid IE Architectures"` - acceptable but Generic per 5.4. | Replace with a descriptive sentence. |
| 99 | P1 | "Code Fragment 0" referenced in prose ("The following implementation (Code Fragment 0) shows this approach in practice"). Code Fragment 0 does not exist. | Fix to "Code Fragment 34.3.6" or whichever is the actual caption. |
| 100 | P1 | "Code Fragment 34.3.10" referenced in prose, actual caption is `34.3.6`. BROKEN_FIGURE_REF. | Fix. |
| 217 | P2 | Caption is `Code Fragment 34.3.6` but is the only code fragment in 34.3; numbering should likely be `34.3.1`. | Renumber. |

### Section 34.4 (`section-34.4.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 27 | P1 | Opens with `<h2>34.4.5 Production Deployment Patterns</h2>` (skips 1-4). | Renumber. |
| 44 | P2 | "Figure 34.4.3" referenced; only one figure in section, should be 34.4.1. FIGURE_SEQUENCE. | Renumber to 34.4.1. |

### Section 34.5 (`section-34.5.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 27 | P1 | Opens with `<h2>34.5.7 Coreference Resolution</h2>` (skips 1-6). | Renumber. |
| 43 | P2 | "Table 34.5.3" but should be 34.5.1 (FIGURE_SEQUENCE). | Renumber. |
| 115 | P0 | The "Output" of Code Fragment 34.5.7 has an embedded `<a>` link to interpretability section: `brought fresh perspectives on <a href="../../part-2-understanding-llms/module-10-interpretability/section-10.1.html">interpretability</a>`. Code output should be a fixed string; embedding HTML links inside a `<pre>`-rendered output is unusual and likely a copy-paste accident. | Strip the `<a>` from the output text. |
| 119 | P2 | Code Fragment caption is "34.5.7" but is the only one in section; should be 34.5.1. | Renumber. |

---

### Section 36.1 (`section-36.1.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 22 | P2 | Title element: `<title>Section 36.1: Platforms | Building Conversational AI with LLMs and Agents</title>` - has trailing book title. Compare to Ch 34 which omits the book title in `<title>`. Either is fine but choose one and apply across the book. | Standardize. |
| 70 | P2 | Inline code uses `<code class="pygments-highlighted lang-python">` (lang-python again). | Change to `language-python` per CONTENT_GUIDELINES 4.1. |
| 70-86 | P2 | Code block (Weaviate hybrid query) has NO `<div class="code-caption">` element. Other code in same chapter has captions. | Add caption "Code Fragment 36.1.1: Weaviate hybrid query example" or similar. |
| 264 | P2 | Empty `<nav class="section-nav"></nav>` element. If unused, remove; otherwise populate. | Remove or populate. |
| 265 | P1 | `<nav class="chapter-nav">` inside `<main>`. See Pattern E. | Standardize. |

### Section 36.2 (`section-36.2.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 46-54 | P2 | Inline code block with no `<div class="code-caption">`. | Add. |
| 104-124 | P2 | Same. | Add. |
| 241 | P2 | Empty `<nav class="section-nav"></nav>`. | Remove or populate. |
| 242 | P1 | Chapter-nav inside main. | Standardize per Pattern E. |

### Section 36.3 (`section-36.3.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 218 | P2 | Empty `<nav class="section-nav"></nav>`. | Remove or populate. |
| 219 | P1 | Chapter-nav inside main. | Standardize. |

### Section 36.4 (`section-36.4.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 244-271 | P2 | sentence-transformers fine-tune code block - no `<div class="code-caption">`. | Add. |
| 296 | P2 | Empty `<nav class="section-nav"></nav>`. | Remove or populate. |
| 297 | P1 | Chapter-nav inside main. | Standardize. |

### Section 36.5 (`section-36.5.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| (verify) | P1 | Likely same pattern: chapter-nav inside main. | Standardize. |

---

### Section 41.1 (`section-41.1.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 19 | P2 | Page-breadcrumb shows `<span class="bc-current">Chapter 41</span>` rather than `<a href="index.html">Chapter 41</a>` - last item is current page so this is intentional, but compare to other sections where last breadcrumb is the section number not the chapter. The breadcrumb depth is inconsistent: Ch 36 breadcrumbs go Part > Chapter > Section, but Ch 41 stops at Part > Chapter. | Standardize breadcrumb depth (3 levels: Part > Chapter > Section). |
| 23 | P2 | `<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part VIII: Conversational AI with LLMs</a><span class="bc-sep">›</span><a href="index.html">Chapter 41</a></div>` - missing "Section 41.1" as third breadcrumb item. | Add. |
| 92-126 | P2 | SVG is inline as a styled block element; works but bigger SVGs in Ch 34 use a `<div class="diagram-container">` wrapper. Standardize. | Wrap. |
| 211 | P1 | `</main>` is after `<footer>` line 211. Reverse order: `<footer>` should come AFTER `</main>`. Per HTML semantics and CONTENT_GUIDELINES 1.14 FOOTER_PLACEMENT. | Move `</main>` before `<footer>`. |

### Section 41.2 (`section-41.2.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 295 | P1 | Same `</main>` after `<footer>` inversion as 41.1. | Move. |
| 230-263 | P2 | SVG used as a wide-screen "framework selection" map; might be better as a clean visual diagram via the technical-diagram-designer skill. | Optional re-design. |

### Section 41.3 (`section-41.3.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| (verify) | P1 | Likely same `</main>` after `<footer>` inversion. | Move. |

### Section 41.4, 41.5 (`section-41.4.html`, `section-41.5.html`)
Same likely pattern - `</main>` after `<footer>`. Verify and move.

---

### Section 46.1 (`section-46.1.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 24 | P0 | Malformed `pagefind-meta-injected` span (see Pattern D). | Repair. |
| 25 | P1 | First `<h2>` is `46.1.1 Judge Bias Taxonomy`. But the section title is "Why LLM-as-Judge Matters" - inconsistent. | Reconcile h1 vs first h2. |
| 26 | P2 | `<div class="callout production-pattern">` - "production-pattern" is a non-canonical callout class. Verify in book.css; expected pattern is `<div class="callout key-insight">` or similar from the canon. | Verify or rename. |
| 40-94 | P2 | Code block uses `pygments-highlighted lang-python` (not `language-python`). | Same as Pattern in Ch 34. |
| 104-110 | P2 | DeepEval `library-shortcut` callout - the code block inside it does NOT use `<div class="code-caption">`. | Add. |

### Section 46.2-46.5
Same patterns as 46.1 - malformed pagefind span (Pattern D), `lang-python` vs `language-python`, missing code captions in inline-with-callout snippets.

---

### Section 56.1 (`section-56.1.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 7 | P2 | `<title>Section 56.1: Platforms | Building Conversational AI with LLMs and Agents</title>` - title is fine but the description meta on line 6 ends with a `.` while title does not. Minor consistency. | Standardize. |
| 77 | P2 | SVG uses `font-family="Georgia, serif"` inline style. Per CONTENT_GUIDELINES 1.15 HARDCODED_STYLE, avoid hardcoded fonts in SVG; use CSS class. | Move to CSS class. |
| 89-105 | P2 | SVG fill colors hardcoded (`fill="#1a2b5c"`, `fill="#2f6b3a"`). Per HARDCODED_STYLE these should be CSS vars. | Use var(--primary-dark), var(--success), etc. |
| 198 | P1 | `</main>` then `<footer>` - check the order is canonical (footer outside main). Looking at structure: ends at 200 with `</body>`. Verify. | Audit. |

### Section 56.2-56.5
Same SVG-color hardcoded patterns. P2 cleanup.

---

### Section 59.1 (`section-59.1.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 36 | P2 | `<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter 59: Distributed Training Systems" hidden=""></span>` - only one pagefind span; other chapters have two (one for part, one for chapter). | Add the part-level span. |
| 38 | P2 | Inline `<div class="math-block">$$M_{\text{state}} = 70 \times 10^{9} \cdot 18 \text{ bytes}...$$</div>` - uses display math inside a div; works but compare to other math-using sections that use just `$$...$$` directly inside `<p>`. Standardize. | Optional. |
| 58 | P2 | SVG inline styles `style="font-family: 'Segoe UI', sans-serif; max-width: 100%; height: auto;"` - per HARDCODED_STYLE move to CSS. | CSS class. |
| 63-90 | P2 | SVG inline fill colors hardcoded. | CSS vars. |
| 281+ | P2 | Bibliography uses `<section class="bibliography"><h2>Bibliography</h2><ol>` format instead of `<div class="bib-entries">` cards. See Pattern F. | Standardize. |

### Section 59.2-59.5
Same: hardcoded SVG styles (P2), bibliography format (P2 / Pattern F), pagefind only one span (P2).

---

### Section 61.1 (`section-61.1.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 24 | P2 | Only one pagefind-meta-injected span (chapter level), missing the part-level. | Add. |
| 92-125 | P2 | SVG hardcoded inline style + hardcoded fill colors. | CSS. |

### Section 61.2-61.5
Same patterns.

---

### Section 24.6 (`section-24.6.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 27 | P2 | Missing prerequisites block. | Add. |
| 27 | P2 | No part-level pagefind span; only chapter-level. | Add. |
| 70-94 | P2 | Code block uses `lang-python` not `language-python`. | Fix. |
| 95 | P2 | Code Fragment caption appears OUTSIDE `<div class="code-block-wrapper">` (or the wrapper is absent). Compare canonical pattern. | Wrap. |

### Section 24.13 (`section-24.13.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 27 | P2 | No prerequisites block. | Add. |
| 55-? | P2 | Code uses `lang-python` not `language-python`. | Fix. |

### Section 26.6 (`section-26.6.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 30-33 | OK | Has proper epigraph with agent avatar. | None. |
| 38-41 | OK | Has prerequisites. | None. |
| 56 | P2 | `<figure class="illustration">` with `<img alt="Five-layer agent memory taxonomy with Working Memory at center, surrounded by Episodic, Semantic, Profile, and Retrieval memories" src="images/memory-taxonomy-five-layers.png"/>` - missing width and height attributes. Per CONTENT_GUIDELINES 2.4 MISSING_IMG_DIMS. | Add `width` and `height`. |
| 63+ | P2 | Code block uses `lang-python` not `language-python`. | Fix. |

### Section 27.5 (`section-27.5.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 45 | P2 | `<img alt="..." src="images/ch23-agentic-rag-librarian.png"/>` - filename uses "ch23" but section is 27.5. Historical filename, but worth tracking. Missing width/height. | Add dims (P2). Filename rename optional. |
| 58+ | P2 | Code blocks `lang-python`. | Fix. |

### Section 29.1 (`section-29.1.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 45 | P2 | `<img alt="..." src="images/ch25-opener-specialist-robots.png"/>` - filename "ch25" but section 29.1. Historical. Missing dims. | Same. |
| 49 | P2 | Exercise callout has title "Exercise 24.1.1: (Hands-On Lab)" - the "24.1.1" looks like a stale id from a previous chapter location. | Renumber to "29.1.1". |

### Section 29.4 (`section-29.4.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 42 | P2 | Prerequisites paragraph contains `<a class="prereq-link" href="...">` - "prereq-link" class is used; consistent with Wave 17i pattern. Verify it is documented. | Document. |

### Section 35.2 (`section-35.2.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 44, 45 | P2 | `<img alt="Islands connected by bridges..." src="images/knowledge-graph-islands.png"/>` - missing width/height. | Add. |
| 50 | P2 | `<img alt="A small knowledge graph illustrating the entity-relationship structure." aria-describedby="fig-19-3-2-knowledge-graph-example-desc" src="images/fig-19.3.2-knowledge-graph-example.png"/>` - filename uses "19.3.2" but section is 35.2. Stale figure-numbering from a previous location. Also missing width/height. | Rename / dims. |
| 73 | P0 | Markup error: `</div>` followed by figure orphan: `</p> </div>` then `<figure>` then `</figure>` then `<text>` indicating `shows how a knowledge graph encodes entities and relationships.` floating outside any structural container. The figure caption fragment is orphaned. Likely a half-completed sentence broken by figure insertion. | Repair the paragraph/figure structure. |

### Section 35.3 (`section-35.3.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 11-19 | OK | Uses KaTeX (justifiable for the math in this section). | None. |
| Verify | P2 | Probably missing prerequisites complete-link block; check. | Audit. |

### Section 37.3 (`section-37.3.html`)
| Line | Severity | Anomaly | Expected canonical form |
|---|---|---|---|
| 33 | P2 | `<blockquote class="epigraph"><p>Memory is what turns a sequence of isolated exchanges into a genuine relationship.</p> <span class="agent-avatar-inline">...` - the agent-avatar-inline span is on the same line as the closing `</p>`. Minor whitespace nit. | Reformat. |
| 44 | P2 | Image missing dims. | Add. |

---

## Cross-cutting issues (apply across all new chapters)

### Issue 1: `lang-python` vs `language-python`

Every code block in the new chapters uses `<code class="pygments-highlighted lang-python">` rather than `<code class="language-python">`. Per CONTENT_GUIDELINES 4.1, the Prism.js class is `language-python` (and friends). The `lang-*` shorthand is non-canonical.

**Severity**: P2.

**Scope**: every code block in Ch 34, 36, 41, 46, 56, 59, 61 and Wave 17i sections.

**Fix**: a single global find-replace `lang-python` -> `language-python` (and `lang-bash`, `lang-yaml`, `lang-json` likewise).

### Issue 2: Smart quotes vs straight quotes

CONTENT_GUIDELINES does not enforce one or the other but consistency matters. Spot-checks:

- `section-34.2.html` line 33: uses straight quote in caption.
- `section-36.1.html` line 41 (Pinecone Serverless): uses straight quotes throughout.
- `section-37.3.html` line 33: uses smart quote variants in epigraph in some files.

**Severity**: P3.

**Fix**: a smart-quotes vs straight-quotes pass once direction is chosen.

### Issue 3: Missing `width` and `height` on `<img>` elements

Every figure-illustration `<img>` across Wave 17i sections is missing the width/height attributes required by CONTENT_GUIDELINES 2.4 MISSING_IMG_DIMS.

**Severity**: P2.

**Scope**: 26.6, 27.5, 29.1, 29.4, 35.2, 35.3, 37.3 illustrations and the diagram-container images in 34, 36, 56.

### Issue 4: Generic SVG aria-labels

Per CONTENT_GUIDELINES 5.4 GENERIC_SVG_LABEL, SVGs should have descriptive aria-labels, not "Diagram" or "Figure 1".

**Examples**:
- `section-34.1.html` line 53: `aria-label="Diagram"`.
- `section-34.3.html` line 32: `aria-label="Diagram: Hybrid IE Architectures"` (slightly better but still terse).
- `section-34.4.html` line 47: `aria-label="Diagram: End-to-End Example: Financial Event Extraction"`.

**Severity**: P2.

**Fix**: per-SVG; replace with a descriptive sentence.

### Issue 5: Non-canonical callout classes

Audit each callout-class usage:

- `production-pattern` (in Ch 46) - not in the canonical 15-callout type list per book template. Verify CSS exists or rename.
- `practical-example` (Ch 34, 41, 56) - in use across chapters; appears canonical.
- `big-picture`, `key-insight`, `warning`, `tip`, `note`, `fun-note`, `library-shortcut`, `exercise`, `self-check` - all canonical.

**Severity**: P2.

**Fix**: confirm `production-pattern` is in book.css; rename to `key-insight` if not.

### Issue 6: Inline `style="..."` overrides in SVG and divs

Per CONTENT_GUIDELINES 1.15 HARDCODED_STYLE.

**Examples**:
- `section-26.6.html` line 32: `<span class="agent-avatar-inline" style="background-color: #16a085;">` - hardcoded color.
- `section-27.5.html` line 34: similar.
- All Ch 56, 59, 61 SVGs have hardcoded `font-family="Georgia, serif"` and hardcoded fill hex codes.

**Severity**: P2.

**Fix**: move to CSS classes. The agent-avatar-inline can take a `data-color="teal"` or similar attribute with the color in CSS.

### Issue 7: Code captions inside `library-shortcut` callouts

When a code block is INSIDE a `library-shortcut` callout, it lacks a `code-caption`. Compare to standalone code blocks in the same file that DO have captions.

**Examples**: section-46.1.html lines 103-110, section-46.2.html lines 95-104, section-32.1.html shows the canonical pattern (caption follows the code).

**Severity**: P2.

**Fix**: add captions or document the rule that library-shortcut code blocks omit captions.

---

## Summary Counts

| Severity | Cross-cutting issues | Specific anomalies | Estimated impact |
|---|---|---|---|
| P0 (broken) | 1 (Ch 46 pagefind spans) + 1 (Ch 35.2 paragraph orphan) + 1 (Ch 34.1 stray closing tag) | 3 individual lines | Affects Pagefind search + HTML validation. **Fix first.** |
| P1 (structural) | Section ordering: chapter-nav placement, missing big-picture, h2 numbering starting at .2/.4/.5/.7, broken Code Fragment refs, missing Prerequisites, missing Bibliography | ~30 individual lines across 34, 46 | Affects all of Ch 34 and Ch 46; significant. |
| P2 (polish) | `lang-python` -> `language-python`, image dims, generic SVG aria-labels, hardcoded SVG styles, missing code captions in library-shortcuts | ~80 individual lines, but mostly bulk find-replace fixable | A few hours of automation. |
| P3 (nit) | Smart vs straight quotes, breadcrumb depth | Sweeping | Optional. |

## Highest-priority fixes (top 10 if you only ship a few)

1. **Repair the malformed pagefind-meta span in all Ch 46 sections** (P0; breaks search). 5 files.
2. **Renumber the leading `<h2>` in all Ch 34 and Ch 46 sections to start at .1**, then renumber dependent figure/code/table references (P1; numerous broken refs). 10 files.
3. **Fix the Ch 34.1 stray `</strong>` closing tag and Code Fragment number "34.2.10" / "34.3.10" / "Code Fragment 0" broken refs** (P0/P1).
4. **Standardize chapter-nav placement**: either inside or outside `</main>`, pick one, apply globally (P1, ~30 files).
5. **Repair the Ch 41 `</main>` after `<footer>` inversion** (P1, 5 files).
6. **Add big-picture callouts to all Ch 34 sections** (P1, 5 files).
7. **Add prerequisites blocks at least to the first section of each new chapter (34.1, 36.1, 41.1, 46.1, 56.1, 59.1, 61.1)** (P1, 7 files).
8. **Add Bibliography sections to Ch 34 and Ch 46** (P1, 10 files).
9. **Global find-replace `lang-python` -> `language-python`** (P2, sweeping, ~50 files).
10. **Repair the Ch 35.2 paragraph/figure orphan around line 73** (P0, 1 file).

Items 1, 3, 5, 6, 7 should be safe to automate. Items 2 (renumbering) requires careful per-file decisions about whether to insert missing 34.1.1, 34.2.1, etc. or to renumber existing content.
