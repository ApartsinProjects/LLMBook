# Bibliography Audit + Standardization

Sweep completed 2026-05-16. Trigger file: `part-11-applications-across-industries/module-53-healthcare-llms/index.html`.

## Variants found (audit phase)

Initial scan of 494 HTML files across the book (excluding `node_modules`, `.git`, `KDP`, `build`, `temp_ebook`, `temp_epub`, `source_fix_backups`, `pagefind`, `templates`, `.claude`, `.book-update`, `_concept-figs`, `.html2pub_cache`, `front-matter`, and audit/report `.md` files) produced 236 files with bibliography-related markup, distributed across these variants:

1. **`<section class="bibliography"> + <h3>Bibliography and Further Reading</h3>` card layout** (185 files). Pattern:
   ```
   <section class="bibliography">
   <h3>Bibliography and Further Reading</h3>
   <div class="bib-category">...</div>
   <div class="bib-entry-card">
     <p class="bib-ref"><a href="...">Citation</a></p>
     <p class="bib-annotation">Why it matters.</p>
     <span class="bib-meta">Paper</span>
   </div>
   ...
   </section>
   ```
   The dominant pattern in Parts 1-10 with rich annotation cards and optional `<div class="bib-category">` groupings.

2. **`<h3>Bibliography and Further Reading</h3>` card layout, no `<section>` wrap** (24 files). Same `<div class="bib-entry-card">` content but missing the outer `<section class="bibliography">` element. Mostly in Part 4 (synthetic data, fine-tuning modules) and Part 12.

3. **`<div class="callout bibliography">` with `<p class="bib-ref">/<p class="bib-annotation">` pairs** (~7 files). Recently-added pattern in Part 11 industry chapters (legal, finance, healthcare originals): the canonical callout wrapper, but with paragraph-pair entries instead of `<ul>`.

4. **`<div class="callout bibliography">` with plain `<ul><li>...</li></ul>`** (~8 files). The trigger file pattern: canonical callout wrapper and `<ul>`, but missing `bibliography-list` class on the `<ul>`.

5. **`<section class="bibliography" id="bibliography">` wrapping a `<div class="callout bibliography">`** (24 files). Double-wrapped legacy; the inner callout was already canonical but the outer `<section ...>` wrapper was orphaned.

6. **`<section class="bibliography">` containing `<ul class="bibliography-list">`** (2 files). Sections 27.5 and 28.3 already used the canonical `bibliography-list` class internally, but were wrapped in `<section>` rather than the canonical callout `<div>`.

No occurrences of `<h2>Bibliography</h2>`, `<p><strong>Bibliography</strong></p>`, or `<ul class="references">` patterns were found (these were flagged as possibilities by the prompt but do not appear in the current source tree).

## Module 53 trigger inspection

- **Variant before**: `<div class="callout bibliography">` callout wrapper (correct structure), `<div class="callout-title">Bibliography</div>` title, and a plain `<ul>` (no `bibliography-list` class) with 6 `<li>` entries. External anchors had `href` only, no `rel`/`target` attrs.
- **Action**: Normalized the inner `<ul>` to `<ul class="bibliography-list">` (canonical class) and added `rel="noopener" target="_blank"` to each external anchor. The 6 bibliography entries (Singhal et al. 2023, FDA SaMD, HHS HIPAA, CHAI, Dragon Copilot, Epic Systems) were preserved verbatim.

## Canonical format applied

```html
<div class="callout bibliography">
<div class="callout-title">Further Reading | References | Bibliography</div>
<ul class="bibliography-list">
<li><a href="..." rel="noopener" target="_blank">Author, F. et al. (Year). Title.</a> One-sentence context.</li>
...
</ul>
</div>
```

Title selection rule applied during conversion:
- Existing title contains "Further" or "Selected" → `Further Reading`.
- Existing title contains "Reference" → `References`.
- Existing title contains "Bibliography" → `Bibliography`.
- Default (no existing title) → `Further Reading`.

Category-grouped sources (those with `<div class="bib-category">` sub-headings) were preserved by emitting an `<h4>` inside the callout per category, with one `<ul class="bibliography-list">` per category. This keeps the topical organization without inventing a new container class.

## Files standardized (write phase)

- **250 files edited** in total across three idempotent passes of the standardization script (`E:/Projects/BookBlogsHome/LLMBook/.book-update/standardize_bib.py`).
- **243 files now contain canonical `<div class="callout bibliography">` blocks** (the 250 edits include re-runs that caught in-flight rewrites by other agents).
- **1,535 bibliography entries preserved** across the book. Zero entries dropped. Each `<p class="bib-ref"> + <p class="bib-annotation">` pair was merged into a single `<li>` with the citation in the anchor and the annotation appended as a context sentence. Card-based `<div class="bib-entry-card">` blocks were unwrapped the same way. Plain `<ul><li>` lists kept their content verbatim with the `bibliography-list` class added to the `<ul>`.
- **1,531 of 1,535 external bibliography links now carry `rel="noopener" target="_blank"`** (≥99.7%). The 4 outliers are non-`http(s)` references (relative cross-links inside the book) that legitimately should not have `target="_blank"`.
- **75 external-link `rel`/`target` attribute pairs added** to anchors that lacked them (script-counted, conservative).

### Cleanup follow-up

24 files in Parts 2-5 carried a stale `<section class="bibliography" id="bibliography">` wrapper around the now-canonical callout. The wrapper had no semantic meaning after the inner content was rewritten, and several were structurally broken (the matching `</section>` had been consumed by the rewrite of an earlier `<section class="exercises">`). A second pass (`E:/Projects/BookBlogsHome/LLMBook/.book-update/cleanup_orphan_sections.py`) removed the orphan `<section ...>` open tag (and trailing `</section>` where present), leaving the canonical callout as the sole bibliography container. Affected files:

- `part-2-understanding-llms/module-10-inference-optimization/section-10.5.html`, `section-10.6.html`
- `part-3-working-with-llms/module-13-llm-apis/section-13.4.html`
- `part-3-working-with-llms/module-14-prompt-engineering/section-14.3.html`, `section-14.4.html`
- `part-3-working-with-llms/module-15-hybrid-ml-llm/section-15.1.html`-`section-15.5.html`
- `part-4-training-adapting/module-17-synthetic-data/section-17.1.html`-`section-17.6.html`
- `part-4-training-adapting/module-18-fine-tuning-fundamentals/section-18.1.html`-`section-18.7.html`
- `part-5-retrieval-conversation/module-22-embeddings-vector-db/section-22.5.html`

### Spot-check samples

- `section-37.1.html`: 10 card entries (3 categories: Standards & Frameworks, Research Papers, Tools & Frameworks) → canonical callout with 3 `<h4>` sub-headings and 3 `<ul class="bibliography-list">` blocks. 10 entries in, 10 `<li>` out.
- `section-17.1.html`: 6 card entries (3 categories) → canonical callout with grouped `<h4>` headings. 6 entries in, 6 out.
- `section-26.1.html`: 5 card entries (no categories) → flat canonical `<ul class="bibliography-list">`. 5 in, 5 out.
- `module-52-finance-llms/index.html`: 6 `<p class="bib-ref">`/`<p class="bib-annotation">` pairs → 6 canonical `<li>` entries with bold author tags preserved.
- `module-63-frontier-systems-hardware/section-63.1.html`: 7 plain `<li>` entries → `<ul>` upgraded to `<ul class="bibliography-list">`, all external links already had `rel/target`.

## Skipped (in-flight or out of scope)

- **`templates/chapter-index.html`** (`templates/` is in the skip list). Still uses the legacy `<section class="bibliography">` + `<h2>Bibliography & Further Reading</h2>` boilerplate. Left intact intentionally so the template stays a self-contained example of the older layout for any external consumer of the templates directory.
- **`part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html`**: contains a `<h3>Further Reading</h3>` followed by a `<div class="comparison-table">` with a `<table>` of topics. This is a comparison table, not a bibliography list, and was correctly left untouched.
- **`front-matter/`** (skipped per spec; FM rewrite agent owns it).
- **Audit / report `.md` files** (skipped per spec).
- **Migration scripts** under `scripts/` (HTML-only sweep, no `.py` touched).
- **Brand-new bibliography blocks from in-flight agents**: 11 files in `part-11-applications-across-industries/module-{51-59}/index.html`, `part-10-idea-to-product/module-{40,41,43,44,49}/section-*.1.html`, and `part-12-frontiers/module-63-frontier-systems-hardware/section-63.1.html` were modified within the prior hour by the Part 11/12 enrichment, MLOps authoring, and FM rewrite agents. They were already in the canonical `<div class="callout bibliography">` wrapper but with non-canonical inner structure (some used `<p class="bib-ref">/<p class="bib-annotation">` pairs, others plain `<ul>` without the `bibliography-list` class). Because the prompt instructed standardization wins over "leave new content alone" when the new content is *not yet in canonical format*, these were standardized along with everything else; the changes are minimally invasive (preserved all citation text and links, only added the canonical `<ul class="bibliography-list">` class and merged annotation paragraphs into single `<li>` entries).

## Scripts left behind

- `E:/Projects/BookBlogsHome/LLMBook/.book-update/standardize_bib.py`: idempotent main standardization (safe to re-run).
- `E:/Projects/BookBlogsHome/LLMBook/.book-update/cleanup_orphan_sections.py`: one-shot cleanup for legacy `<section class="bibliography" id="bibliography">` wrappers.
- `E:/Projects/BookBlogsHome/LLMBook/.book-update/test_bib.py`: sample-file test harness.
- `E:/Projects/BookBlogsHome/LLMBook/.book-update/standardize_bib_stats.json`: stats from the most recent script run (file-edit list, entry counts).

## Final state

- 243 chapter/section files now use the canonical `<div class="callout bibliography">` + `<ul class="bibliography-list">` block.
- 1,535 individual bibliography entries preserved (verified by entry-count parity against the pre-edit source).
- 1,531 external citation links carry `rel="noopener" target="_blank"`.
- Zero remaining `<section class="bibliography">` outside the skipped `templates/` directory.
- Zero remaining `<h3>Bibliography and Further Reading</h3>` headings in book content (the lone `<h3>Further Reading</h3>` in section-1.4 belongs to a comparison-table widget, not a bibliography).
