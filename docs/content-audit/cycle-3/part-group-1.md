# Cycle 3 Audit — Parts 1-4

Scope: `part-1-llm-building-blocks/` (modules 00-05), `part-2-understanding-llms/` (modules 06-10), `part-3-working-with-llms/` (modules 11-14), `part-4-training-adaptation/` (modules 15-19). Read-only audit between cycle 2 (which described drift across body refs, figure captions, H2 numbering, breadcrumbs, and inflated tools chapter-nav blocks) and the cycle 3 starting state after waves 17a-h landed.

## Resolved since cycle 2

- **Wave 17c (H2 / H3 visible-numbering)** verified working: section-body H2 IDs and visible text now agree everywhere we sampled (Part 1 modules 2/3/4 sections, Part 2 module-07 section-7.1, Part 3 module-14 section-14.1, Part 4 module-15 section-15.1, module-19 section-19.2). The cycle-2 dual-numbering pattern (`id="14-1-1"` rendered as "16.1.1") is gone for normal subsection h2s. Stragglers documented under "Remaining" below.
- **Wave 17c (figure caption sync)** mostly working: section-2.1 figures now read "Figure 2.1.1", "Figure 2.1.2"; section-3.1 figures read "Figure 3.1.1" through "3.1.6"; section-15.1 H2s read "15.1.X". The chapter-opener `<figcaption>` figures in module index files (e.g. "Figure 3.0.1", "Figure 5.0.1", "Figure 7.0.1") are still off, but the section bodies are clean.
- **Wave 17d (in-prose visible labels)** verified for body files where a `Section N.M` / `Chapter N` label sits adjacent to its `href`: section-13.5 hyperlinks now read "Section 15.1", "Chapter 18", "Section 11.1" with matching targets; section-12.4 hyperlinks read "Section 11.1", "Section 52.1" with matching targets. The cycle-2-dominant body drift ("Chapter 22", "Chapter 23", "Section 20.1" etc.) is largely cleared for hyperlinks that the sweep could resolve via href.
- **Wave 17e (module-index sections-list rebuild)** verified for module-10: sections 10.5-10.9 are now LISTED in `<ul class="sections-list">` of the module-10 index (cycle-2 said they were missing). Module-01 index now lists sections 1.5-1.7 (tokenization).
- **Wave 17g (chapter-nav rebuild)** verified for module-index files: prev/next chapter labels now use unpadded current numbers ("Chapter 0", "Chapter 1", ..., "Chapter 19") and target the correct neighbouring chapter. Module-01's prior self-pointing "Next Chapter" link is gone. Module-08 prereq labels now read "Chapter 3", "Chapter 4", "Chapter 6", "Chapter 7" (cycle-2 said they were "Chapter 04/05/06/08").
- **Wave 16 PEFT rename** propagated to the module-17 chapter index (`<title>` and h1 both read "Parameter-Efficient Fine-Tuning, Distillation & Model Merging").
- Cycle 2 #5 partially: module-10 sections 10.5-10.9 are now discoverable from the chapter index (Wave 17e), so the cycle-2 discoverability complaint is closed even though the content still claims to be Chapter 12 (see below).

## Remaining issues (priority order)

### P1. Tools-of-the-Trade misplaced/inflated content unchanged

- **Part 2 Tools content still lives as module-10 sections 10.5-10.9 with `<a href="index.html">Chapter 12: Tools of the Trade: Models &amp; Tokenizers</a>` breadcrumbs and `<meta data-pagefind-meta="chapter:Chapter 12: ...">` injection.** Every section file 10.5 through 10.9 still pagefind-indexes as Chapter 12 while physically being Chapter 10 sections. Confirmed in `section-10.5.html` line 23,27 and `section-10.6.html` line 23,27. Cycle 2 #5 still open.
- **section-10.6 still has 5 `<nav class="chapter-nav">` blocks** with mid-content navs at lines 78, 321, 572, 845, 1092; four say `<span class="nav-num">Chapter 12</span>`. section-10.8 still has 2 chapter-nav blocks. Cycle 2 #11 unchanged.
- **section-5.1 still has 7 `chapter-nav` blocks** (lines 57, 130, 165, 231, 274, 356, 487) with nav-num labels "Section 5.7" through "Section 5.17" and `href="section-5.1.html#6-1-..."` self-pointing anchors using the OLD "6-1-" prefix. Visible chapter labels are "Chapter 5" inside the navs but the first nav still uses `<span class="nav-num">Chapter 05</span>` (zero-padded). The h2 IDs were rewritten to `5-1-X` by Wave 17c, but the `href="#6-1-..."` anchors point into nonexistent IDs.
- **section-5.2 still has 8 `chapter-nav` blocks**; cycle 2 #4 unchanged.
- **section-14.2 still has 3 `chapter-nav` blocks** with anchor-deep self-pointing hrefs.
- **section-19.2 still has 10 `chapter-nav` blocks** (lines 72, 377, 723, 1048, 1138, 1331, 1538, 1803, 1928, 2229) with nav-num labels "Section 19.5" through "Section 22.1" (the last one even spills into Part 7) and `href="section-19.2.html#21-2-..."` / `href="section-19.3.html#21-3-..."` self-pointing anchors using the OLD "21-2-" / "21-3-" prefix. section-19.3 still has 5 such blocks. Cycle 2 #4 unchanged.

### P2. Tokenization (Chapter 2) still inside module-01

- Sections 1.5/1.6/1.7 are now LISTED in the module-01 chapter index (Wave 17e progress), but the section files themselves still carry `Chapter 2: Tokenization and Subword Models` breadcrumbs and meta description (e.g. section-1.6.html, section-1.7.html). The section card descriptions in module-01/index.html lines 110, 115 still read "You should have read Section 2.1: Why Tokenization Matters" and "you understand BPE and other subword algorithms from Section 2.2 and the tokenization fundamentals from Section 2.1", pointing into legacy Section 2.X labels for what is now 1.5/1.6.
- Cycle 2 #6 partially resolved (discoverability) but identity (breadcrumb / page-current / metadata) still broken.

### P3. Module-index `<title>` and `<meta description>` zero-padding / off-by-one

Twelve module indexes still carry the OLD numbering scheme in the `<title>` and `<meta name="description">`:

- module-00: `<title>Chapter 00:</title>` (breadcrumb "Chapter 0")
- module-01: `<title>Chapter 01:</title>` (breadcrumb "Chapter 1")
- module-02: `<title>Chapter 03:</title>` (breadcrumb "Chapter 2"), meta "Chapter 03:"
- module-03: `<title>Chapter 04:</title>` (breadcrumb "Chapter 3"), meta "Chapter 04:"
- module-04: `<title>Chapter 05:</title>` (breadcrumb "Chapter 4"), meta "Chapter 05:"
- module-06: `<title>Chapter 06:</title>` (breadcrumb "Chapter 6")
- module-07: `<title>Chapter 07:</title>` (breadcrumb "Chapter 7")
- module-08: `<title>Chapter 08:</title>` (breadcrumb "Chapter 8")
- Module-05/09/10/11/12/13/14/15/16/17/18/19 titles ARE now unpadded ("Chapter 5", "Chapter 9", ...). The zero-padded straggler set is the cycle-2 P8 set minus modules 5 and 9 (which were fixed).

### P4. Part-overview prose stale chapter ranges

All four part-index files still cite the OLD chapter ranges in the `<div class="part-overview">` prose:

- Part I: "Chapters: 7 (Chapters 0 through 6) ... closes with Chapter 6: Tools of the Trade" — should be "Chapters: 6 (Chapters 0 through 5)" closing with Chapter 5.
- Part II: "Chapters: 6 (Chapters 7 through 12)" — should be "Chapters: 5 (Chapters 6 through 10)".
- Part III: "Chapters: 4 (Chapters 13 through 16)" — should be "Chapters: 4 (Chapters 11 through 14)".
- Part IV: "Chapters: 5 (Chapters 17 through 21)" — should be "Chapters: 5 (Chapters 15 through 19)".

Cycle 2 #7 unchanged. The chapter-card grids themselves are correct; only the surrounding prose lags.

### P5. Module-17 section-file breadcrumbs lag the Wave 16 rename

All 7 module-17 section files (`section-17.1.html` through `section-17.7.html`) still link to `index.html` with the OLD label `Chapter 17: Parameter-Efficient Fine-Tuning (PEFT)`. The chapter index itself has the new title "Parameter-Efficient Fine-Tuning, Distillation & Model Merging" but the section breadcrumbs were not updated. Cycle 2 #12 unchanged.

### P6. Section-6.9 duplicate not de-duped

- `part-2-understanding-llms/index.html` chapter-6 card: section-6.9 listed twice in the `<ul class="section-list">` (two adjacent `<li>` entries on lines 56-57).
- `part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html`: section-6.9 listed once in `<ul class="sections-list">` (line 122-126) and again in a free-floating `<div class="section-grid">` immediately after the ul (lines 128-133).

Cycle 2 #10 unchanged.

### P7. Figure / Table / Listing numbers in module-index chapter openers are still off

Almost every chapter index has a `<figcaption>` for `images/chapter-opener.png` whose number lags the current chapter. Examples observed:

- module-02 chapter-opener `<strong>Figure 3.0.1</strong>` (real Chapter 2)
- module-03 `<strong>Figure 4.0.1</strong>` + diagram `<strong>Figure 4.0.2</strong>` (real Chapter 3)
- module-04 `<strong>Figure 5.0.1</strong>` (real Chapter 4)
- module-06 `<strong>Figure 7.0.1</strong>` (real Chapter 6)
- module-07 `<strong>Figure 8.0.1</strong>` (real Chapter 7)
- module-09 `<strong>Figure 10.0.1</strong>` (real Chapter 9)
- module-10 `<strong>Figure 11.0.1</strong>` (real Chapter 10)
- module-11 `<strong>Figure 13.0.1</strong>` (real Chapter 11)
- module-12 `<strong>Figure 14.0.1</strong>` (real Chapter 12)
- module-13 `<strong>Figure 15.0.1</strong>` (real Chapter 13)
- module-15 `<strong>Figure 17.0.1</strong>` (real Chapter 15)
- module-16 `<strong>Figure 18.0.1</strong>` (real Chapter 16)
- module-17 `<strong>Figure 19.0.1</strong>` (real Chapter 17)
- module-18 `<strong>Figure 20.0.1</strong>` (real Chapter 18)

Wave 17c covered section-body figures but skipped chapter-opener figures inside the module index files. Same off-by-1 / off-by-2 pattern as before.

### P8. In-prose / non-href chapter mentions still stale

Wave 17d resolved most label-vs-href mismatches, but the sweep was anchored to href targets. Non-href body prose ("Chapter 18 introduces fine-tuning", "Chapter 20: Alignment", "Chapter 04 Transformer Architecture", etc.) was not touched. Examples:

- module-00 (Chapter 0) chapter overview: "NLP fundamentals (Chapter 01)", "Transformer architecture (Chapter 04)", "Chapter 20: Alignment, RLHF & DPO", "Chapter 18: Fine-Tuning Fundamentals". Real: 1, 3, 18, 16.
- module-02 looking-back: "You now have tokens (Chapter 2) and you know how to embed them (Chapter 1)" — Chapter 2 IS this chapter (self-reference) and tokens are in Chapter 1.
- module-03 looking-back: "Chapter 3 introduces attention" — self-reference (Chapter 3 IS this chapter, attention is Chapter 2). Big-picture: "Chapter 11: Interpretability" — real Chapter 10.
- module-04 looking-back: "You built a Transformer in Chapter 4" — self-reference (this IS Chapter 4, Transformer is Chapter 3).
- module-05 What's Next: "Chapter 12 closes Part II with its own Tools of the Trade chapter" — real Chapter 10 closes Part II.
- module-06 overview: "Transformer architecture (Chapter 04)" → real 3. Learning Objectives: "Chapter 18: Fine-Tuning" → real 16.
- module-07 looking-back: "Chapter 7 told you how LLMs are trained" — self-reference (Chapter 7 IS this chapter; pretraining is Chapter 6).
- module-09 looking-back: "Chapter 7 (Modern LLM Landscape)" → real 7 is Modern, but the sentence introduces pretraining (Ch 6). "Chapter 8 (Reasoning)" → real 8. "Chapter 9" → self-reference.
- module-09 section-9.6 prose: `<a href="index.html">Chapter 11: Inference Optimization &amp; Efficient Serving</a>` — visible "Chapter 11" but href is to this chapter (which IS Chapter 9). Mismatch label, correct href.
- module-10 big-picture: "Chapters 17 and 32" (real 18 alignment, real 47 safety).
- module-10 prereqs: "Chapter 4: Embeddings and Representation Learning" — Chapter 4 is Decoding, not Embeddings (Embeddings/text is Ch 1).
- module-12 looking-back: "You can call an API (Chapter 13)" — real 11.
- module-12 big-picture: "RAG systems (Chapter 23), agents (Chapter 26), and evaluation (Chapter 34)" — chapter numbers may still be valid in the global TOC (Part 7+) but visible-only references like these were not resolved.
- module-13 overview: "Chapter 23 on RAG" — visible label only, may still be valid global number.
- module-14 What Comes Next: "Chapter 21 closes Part IV" — real Chapter 19 closes Part IV.
- module-15 overview: "Chapter 06" → real 6 (correct), "RLHF, covered in Chapter 20" → real 18, "Chapter 14's prompt engineering" → real 12, "Chapter 18" fine-tuning → real 16, "Chapter 20" alignment → real 18.
- module-15 big-picture: "Chapters 14 and 15 ... Chapter 20" → real 16/17/18.
- module-16 looking-back: "data (Chapter 17)" — Chapter 17 is PEFT, data is Chapter 15.
- module-16 big-picture: "Chapter 19" PEFT → real 17, "Chapter 20" alignment → real 18.
- module-17 looking-back: "Chapter 18 introduces fine-tuning" — real 16.
- module-18 looking-back: "Fine-tuning (Chapter 18) and PEFT (Chapter 19)" — real 16/17.
- module-18 big-picture: "Chapter 37" → real 47.
- module-19 What Comes Next: "Part V turns to retrieval... Chapter 25 closes Part V" — Part V in current numbering is Multimodal LLMs; retrieval is Part 7.
- section-5.1 body: "Chapter 50.2 (Vibe-Coding with LLMs)" — likely real 68.2 in part-15.

This class of issue is dominated by **stale visible numbers in prose without an accompanying href**, which Wave 17d's href-anchored sweep could not resolve.

### P9. `concept-link title="..."` and code-fragment caption stragglers

- `module-09/index.html` line 74: `title="Section Q.4: Quantization for Serving (GPTQ, AWQ, GGUF)"` while the href target uses anchor `#12-4-quantization-for-serving` and lives in `module-10/section-10.8.html`. Both the "Q.4" label and the "12-4" anchor are pre-renumbering artifacts.
- `module-09/index.html` line 42 looking-back: `title="Section Q.2: Text Generation Inference (TGI)"`, `title="Section Q.3: SGLang: Structured Generation and RadixAttention"` — same stale-label class.
- section-3.1 (Chapter 3 transformer) has section-body table titles with stale numerical em-prefixes inside `<em>` tags:
  - Line 500: `<em>8.1 Pre-LN vs. Post-LN ...</em>` inside a Table 3.1.1 title.
  - Line 863: `<em>13. Putting It All Together ...</em>` inside a Table 3.1.2 title.
- section-3.1 has straggler code-fragment caption suffix variants Wave 17c missed:
  - Line 417: `<strong>Code Fragment 4.1.5a:</strong>`
  - Line 664: `<strong>Code Fragment 4.1.6a:</strong>`
  - Line 680: `<strong>Code Fragment 4.1.5c:</strong>`
  The siblings without suffixes (e.g. Code Fragment 3.1.5, 3.1.6) ARE updated; only the "a/b/c" suffix variants slipped through the regex.
- Caption-vs-filename mismatch unresolved: section-2.1 line 106 uses `<img src="images/fig-3.1.7-rnn-unrolled.png">` while the caption now reads "Figure 2.1.2". The image filename retains the old number; this is cosmetic but inconsistent with the rest of the book.

### P10. Mid-content section-nav anchor-prefix mismatch

In each inflated Tools section, the embedded mid-content `<nav class="chapter-nav">` blocks point at anchors using the OLD prefix:

- section-5.1 / section-5.2 (Part 1 module-05): `href="section-5.1.html#6-1-..."`, `href="section-5.2.html#6-2-..."` (old "6-" because Tools used to be Chapter 6).
- section-10.6 / section-10.8 (Part 2 module-10): `href="section-10.6.html#12-2-..."`, `href="section-10.8.html#12-4-..."` (old "12-" because Tools used to be Chapter 12).
- section-14.2 (Part 3 module-14): `href="section-14.2.html#16-2-..."` (old "16-").
- section-19.2 / section-19.3 (Part 4 module-19): `href="section-19.2.html#21-2-..."`, `href="section-19.3.html#21-3-..."` (old "21-").

Because Wave 17c rewrote the in-document h2 IDs to the new prefix (`5-1-`, `10-6-`, `14-2-`, `19-2-`), every one of these href anchors now points at a non-existent ID. The mid-content prev/next chains are broken navigation, not just cosmetic.

### P11. `nav-num` zero-padding stragglers in section files

Every Part-1 section file's main chapter-nav still uses zero-padded chapter labels in the bottom nav: `<span class="nav-num">Chapter 00</span>`, `Chapter 01`, `Chapter 02`, etc. Confirmed in section-0.1.html line 532, section-5.1.html line 59, etc. Affected: 28 section files in Part 1; sample checks in Part 2-4 show the pattern stops at module-09 (Chapter 9 reads "Chapter 09" in section-9.6 line 347). Wave 17g rebuilt the module-index navs but not the section-bottom navs.

### P12. Cross-part / appendix anchor breakage

A few cross-part references still embed the OLD anchor prefix and now miss:

- section-5.1.html line 442: `href=".../module-14-tools-of-the-trade/section-14.1.html#16-1-api-keys-and-secrets-management"` — the new anchor would be `#14-1-...`. Same on line 459.
- `module-19/index.html` line 41: `href=".../section-19.3.html#21-3-pyspark-for-llm-data-pipelines"` (visible "Appendix L") — stale "21-3-" prefix.

Both fall under the same root cause as P10 (anchor prefixes not rewritten when section h2 IDs were renumbered).

## Suggested cycle 4 actions

1. **Rewrite `<title>` and `<meta name="description">` in the 8 remaining Part 1 and Part 2 chapter indexes** (modules 00/01/02/03/04/06/07/08) to use unpadded chapter numbers matching the breadcrumb. Single regex pass per file, scoped to `<title>` and `<meta content="Chapter \d+:`.

2. **Fix the four `<div class="part-overview">` prose blocks** in `part-1-llm-building-blocks/index.html`, `part-2-understanding-llms/index.html`, `part-3-working-with-llms/index.html`, `part-4-training-adaptation/index.html` to cite the correct chapter ranges. Quick string replacement (less than 5 lines per file).

3. **Renumber the 14 chapter-opener `<figcaption>` figures in module indexes** to match the new chapter number (Figure 5.0.1 → 4.0.1, etc.). Path-derived: read `module-XX-…/index.html`, find `<strong>Figure A.0.B</strong>`, rewrite A to the chapter number. About 14 figures total in Parts 1-4.

4. **Resolve the Tools-of-the-Trade misplaced content (P1) decisively.** Two options:
   - **(a) Move sections 10.5-10.9 out of module-10 into a new module-NN-tools-of-the-trade folder under Part 2, give them their own chapter index and add a chapter card to the Part-2 index.** This matches the structure used in Parts 1 (Tools = Chapter 5 / module-05), 3 (Tools = Chapter 14 / module-14), 4 (Tools = Chapter 19 / module-19). It requires renaming hrefs that point in but the result is a clean Part 2 structure with 6 chapters (6-11) — though that pushes downstream chapter numbers further if applied beyond Part 2.
   - **(b) Keep the content inside module-10 but rebrand the breadcrumbs from "Chapter 12: Tools of the Trade: Models & Tokenizers" to "Chapter 10: Interpretability & Mechanistic Understanding"** and dedupe the inflated chapter-nav blocks. This treats sections 10.5-10.9 as additional sections of the interpretability chapter (Tools of the Trade subsumed). Lighter touch.

   Either way: (i) drop the duplicate / inflated `<nav class="chapter-nav">` blocks inside sections 10.5-10.9 down to one per file, (ii) rewrite `href="#12-X-..."` anchors to current `#10-X-...` IDs.

5. **Resolve the tokenization location (P2).** Same fork as #4: either lift sections 1.5-1.7 into their own module-NN-tokenization folder as Chapter 2 (pushing the rest of Part 1 forward) or rebrand the breadcrumbs from "Chapter 2: Tokenization and Subword Models" to "Chapter 1: Foundations of NLP & Text Representation". Whichever path, fix the section-card descs in `module-01/index.html` lines 110, 115 that reference "Section 2.1" / "Section 2.2" pointing at section-1.5/1.6.

6. **De-inflate the Tools sections (P1):** `section-5.1`, `section-5.2`, `section-10.6`, `section-10.8`, `section-14.2`, `section-19.2`, `section-19.3`. Each has 2-10 mid-content `<nav class="chapter-nav">` blocks; replace with a single bottom-of-page chapter-nav, drop the self-pointing `<a href="section-X.Y.html#prefix-..">` chains, and let the `<section class="tot-subsection">` wrappers stand on their own. Same pass: rewrite `href="...#OLD-..."` anchors in section bodies to the current h2 IDs.

7. **Propagate Wave 16 rename** to all 7 `section-17.X.html` files: change the breadcrumb `<a href="index.html">Chapter 17: Parameter-Efficient Fine-Tuning (PEFT)</a>` to match the new title. Single regex pass.

8. **De-duplicate section-6.9** in `part-2-understanding-llms/index.html` (drop the second `<li>` on line 57) and `module-06/index.html` (drop the `<div class="section-grid">` block on lines 128-133).

9. **Non-href in-prose chapter/section reference sweep (P8).** Wave 17d resolved href-anchored cases. A second pass is needed for prose that mentions "Chapter N" / "Section N.M" without an accompanying hyperlink: this includes looking-back, big-picture, overview, learning-objectives, and What's Next paragraphs in every module index, plus stragglers in section bodies (e.g. section-5.1 "Chapter 50.2", section-12.4 "Section 15.4"). Probably needs an authored mapping table from OLD-numbering to NEW-numbering (and to global numbering for cross-part references like "Chapter 23 RAG" → "Chapter 32" or wherever RAG now sits), then a manual or LLM-mediated rewrite per file.

10. **Concept-link `title="..."` cleanup.** The "Section Q.4: Quantization for Serving (GPTQ, AWQ, GGUF)" / "Section Q.2: TGI" / "Section Q.3: SGLang" tooltips in `module-09/index.html` and similar concept-link tooltips elsewhere still embed legacy letter-prefixed labels. Sweep all `title="Section [A-Z]\.\d"` and `title="Section \d{2,}\."` attributes against href targets.

11. **section-body `nav-num` zero-padding sweep (P11).** 28+ Part-1 section files have `<span class="nav-num">Chapter 0\d</span>` in the bottom chapter-nav. Wave 17g rebuilt module-index navs but missed the section-bottom navs.

12. **Caption-vs-filename drift (P9).** Image filenames like `fig-3.1.7-rnn-unrolled.png` (referenced from section-2.1 with caption "Figure 2.1.2") encode the old number. Either rename files and rewrite `<img src=...>` or accept the asset-layer drift and only fix captions (current state). Recommend leaving filenames alone unless a rebuild is happening for other reasons.

13. **section-3.1 table title em-prefix and code-fragment suffix stragglers.** Manual fix: rewrite the `<em>` text inside the Table 3.1.1 / Table 3.1.2 titles (strip the "8.1" / "13." legacy prefixes), and renumber Code Fragments 4.1.5a / 4.1.5c / 4.1.6a to the 3.1.X scheme. Less than 10 lines edited.
