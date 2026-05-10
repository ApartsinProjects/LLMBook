# Image / Caption Alignment Audit

**Scope**: 470 HTML files under `part-*/`, `appendices/`, `front-matter/`, `capstone/`.
**Method**: Line-based extraction of `<img src="...fig-N.M[.K]...">` tags and `<strong>Figure N.M[.K]</strong>` captions, paired by line proximity (img usually one line above caption inside `<div class="diagram-container">` or `<figure class="illustration">`). For each pair, compared (a) the figure number embedded in the img filename, (b) the figure number in the caption, (c) the topic overlap between alt-text and caption-text.

**Headline**: Two distinct bug classes were found. The user-reported "4.13 / 4.14" issue (i.e. Figures 4.1.3 and 4.1.4 in `part-1-foundations/module-04-transformer-architecture/section-4.1.html`) is the most severe class: an IMG block is **physically misplaced one slot earlier than its intended caption**, so the caption description and the image content do not match. The same reader-visible bug exists in 7 other sections. A second, milder class (caption number does not match img filename, but content matches) exists in 10 more sections; the reader sees the correct image with the correct caption, only the auto-generated filename is one number off.

---

## 1. Root cause for Figure 4.1.3 / 4.1.4 (the user-reported issue)

**File**: `part-1-foundations/module-04-transformer-architecture/section-4.1.html`

**Observed misalignment** (lines 347-348, 429-430, 777-778):

| line | img src                          | img alt                       | caption number  | caption text                                    | reader sees |
|------|----------------------------------|-------------------------------|-----------------|-------------------------------------------------|-------------|
| 347  | `fig-4.1.4-pos-encoding.png`     | "Positional encoding..."      | "Figure 4.1.3"  | "encoder-decoder Transformer..."                | wrong image |
| 429  | `fig-4.1.7-pre-post-ln.png`      | "Post-LN/Pre-LN..."           | "Figure 4.1.4"  | "row=position, column=dimension (positional)"   | wrong image |
| 777  | `fig-4.1.8-causal-mask.png`      | "Causal triangular mask..."   | "Figure 4.1.5"  | "Post-LN (left) ... Pre-LN (right)..."          | wrong image |
| 957  | `fig-4.1.7-residual-stream.png`  | "Residual stream..."          | "Figure 4.1.7"  | "residual stream perspective"                   | OK          |

**What actually happened**: at some point the prose for section-4.1 introduced a new "Figure 4.1.3" (encoder-decoder Transformer description) without producing a `fig-4.1.3-encoder-decoder.png` image file. The image directory does not contain any `fig-4.1.3-*.png`. Every subsequent IMG container then shows the image meant for the *next* caption position:

- caption 4.1.3 (encoder-decoder) gets shown the positional-encoding image (intended for 4.1.4)
- caption 4.1.4 (positional encoding) gets shown the pre/post-LN image (intended for 4.1.5)
- caption 4.1.5 (pre/post-LN) gets shown the causal-mask image (which has no caption of its own anywhere; section "10. The Causal Mask" at line ~825 has no figure)

There is also a **filename collision**: both `fig-4.1.7-pre-post-ln.png` and `fig-4.1.7-residual-stream.png` claim figure number 4.1.7. The pre/post-LN file is misnamed from an older numbering scheme; the residual-stream file is the correct 4.1.7.

**Fix recommendation (manual, not auto-applied)**:
1. Move the `<div class="diagram-container">` at line 347 down to replace the one at line 429 (so caption 4.1.4 displays `fig-4.1.4-pos-encoding.png`).
2. Move the diagram block at line 429 down to replace the one at line 777 (so caption 4.1.5 displays `fig-4.1.7-pre-post-ln.png`; ideally also rename the asset to `fig-4.1.5-pre-post-ln.png`, but renaming is out of scope).
3. Move the causal-mask diagram block (line 777) into Section 10 (around the prose at lines 825-839) and add a "Figure 4.1.8" caption for it.
4. For caption 4.1.3 (encoder-decoder), either (a) generate a `fig-4.1.3-encoder-decoder.png` asset, or (b) remove the `<img>` tag and demote the caption to a paragraph.

---

## 2. Inventory of similar misalignments across the book

Audit produced 26 issues across 14 files: 18 image/caption number mismatches, 7 caption-number-out-of-order, 1 image without any caption.

### 2A. Reader-visible content mismatches (8 cases)
**The displayed image content does NOT match the caption description.** Highest priority. Same root cause as Section 4.1.

| file | img line | img file (content)                            | caption (description)                                    |
|------|---------:|-----------------------------------------------|----------------------------------------------------------|
| part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html | 146 | `fig-1.3.5-cosine-sim.png` (cosine similarity) | "Figure 1.3.2: Skip-gram neural network"                 |
| part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html | 277 | `fig-1.3.6-fasttext.png` (FastText)            | "Figure 1.3.5: cosine similarity geometric intuition"    |
| part-1-foundations/module-02-tokenization-subword-models/section-2.2.html         | 140 | `fig-2.2.4-unigram.png` (Unigram/Viterbi)      | "Figure 2.2.2: BPE iterative merging"                    |
| part-1-foundations/module-02-tokenization-subword-models/section-2.2.html         | 483 | `fig-2.2.5-byte-bpe.png` (byte-level BPE)      | "Figure 2.2.4: Unigram model / Viterbi"                  |
| part-1-foundations/module-03-sequence-models-attention/section-3.1.html           | 265 | `fig-3.1.6-seq2seq.png` (encoder-decoder)      | "Figure 3.1.3: gradient magnitude vs time step"          |
| part-1-foundations/module-04-transformer-architecture/section-4.1.html            | 429 | `fig-4.1.7-pre-post-ln.png` (pre/post LN)      | "Figure 4.1.4: positional encoding row/column"           |
| part-1-foundations/module-04-transformer-architecture/section-4.1.html            | 777 | `fig-4.1.8-causal-mask.png` (causal mask)      | "Figure 4.1.5: Pre-LN / Post-LN"                         |
| part-1-foundations/module-05-decoding-text-generation/section-5.2.html            |  93 | `fig-5.2.3-top-p.png` (top-p sampling)         | "Figure 5.2.2: temperature softmax peakiness"            |

### 2B. Filename-only mismatches (10 cases)
**Reader sees the correct image with the correct caption text; only the IMG src filename has a stale figure number.** These are not visible bugs but break automated cross-checking and asset-management tooling.

| file | img line | situation |
|------|---------:|-----------|
| part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html | 262 | filename says 1.1.4, caption is "Figure 1.1.5" (NLP tasks). Topic matches both. |
| part-1-foundations/module-01-foundations-nlp-text-representation/section-1.1.html | 319 | filename says 1.1.6, caption is "Figure 1.1.7" (linguistic layers). Topic matches both. |
| part-1-foundations/module-01-foundations-nlp-text-representation/section-1.4.html | 303 | filename `fig-1.4-evolution.png` (no third digit), caption "Figure 1.4.7". |
| part-1-foundations/module-03-sequence-models-attention/section-3.1.html           |  98 | filename says 3.1.3 (vanishing-grad), caption "Figure 3.1.2: RNN unrolled". Borderline: alt and caption are about different visual artifacts but both explain RNN dynamics. |
| part-1-foundations/module-03-sequence-models-attention/section-3.2.html           | 125 | filename says 3.2.4 (gradient-attention), caption "Figure 3.2.2: Bahdanau additive". Borderline: both attention-related. |
| part-1-foundations/module-04-transformer-architecture/section-4.1.html            | 347 | filename says 4.1.4 (pos-encoding), caption "Figure 4.1.3: encoder-decoder". The IMG content is positional-encoding (wrong), but the *caption* is in the right slot. See section 1 above. |
| part-10-frontiers/module-34-emerging-architectures/section-34.10.html             |  62 | filename `fig-34.10-domain-tokenization.png` (no third digit), caption "Figure 34.10.1". |
| part-5-retrieval-conversation/module-20-rag/section-20.3.html                     | 311 | filename `fig-20.3-graphrag-pipeline.png` (no third digit), caption "Figure 20.3.4". |
| part-8-evaluation-production/module-31-production-engineering/section-31.6.html   | 438 | filename says 31.6.4, caption "Figure 31.6.3" (Retry strategy). Topic matches both; image filename is swapped with the next entry. |
| part-8-evaluation-production/module-31-production-engineering/section-31.6.html   | 531 | filename says 31.6.3, caption "Figure 31.6.4" (Saga). Image filename is swapped with the previous entry. |

### 2C. Caption out of source-order (7 cases)
Captions monotonically increase in most files, but a few sections renumber backwards mid-document. Cross-references (e.g. "as shown in Figure 16.1.5") rely on the existing numbers, so blind renumbering would break them.

| file | situation |
|------|-----------|
| part-2-understanding-llms/module-09-inference-optimization/section-9.2.html | sequence is 9.2.2, 9.2.4, 9.2.5, 9.2.3 (the 9.2.3 caption appears AFTER 9.2.5). |
| part-4-training-adapting/module-16-distillation-merging/section-16.1.html   | sequence is 16.1.1, 16.1.2, 16.1.5, 16.1.6, 16.1.3, 16.1.4. Two prose cross-references depend on the existing numbering ("As Figure 16.1.5 illustrates" L105, "Figure 16.1.6 contrasts" L213). |
| part-4-training-adapting/module-16-distillation-merging/section-16.2.html   | caption "16.2.4" appears AFTER caption "16.2.5". |
| part-4-training-adapting/module-16-distillation-merging/section-16.3.html   | sequence is 16.3.3, 16.3.1, ..., 16.3.5, 16.3.2 (two backwards jumps). |
| part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.2.html | "19.2.2" appears AFTER "19.2.3". |

### 2D. Image without nearby caption (1 case)
| file | img line | filename |
|------|---------:|----------|
| part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html | 175 | `fig-8.1.3-the-four-major-reasoning-architecture-approaches-compared-...` followed by an SVG/HTML diagram with its own caption rather than a `<div class="diagram-caption">`. False positive on closer inspection (the caption is rendered as part of the SVG/HTML below). |

---

## 3. Patterns / systemic root causes

1. **AI illustration insertion broke the running figure index.** Starting in Module 1, an AI-generated `<figure class="illustration">` was added between every existing Mermaid diagram. The captions on the Mermaid diagrams were renumbered to follow the new joint sequence (`1.1.5` instead of `1.1.4`), but **the IMG src filenames were not renamed**. Net effect: caption numbers and filenames diverge by exactly 1 in those files.

2. **Missing source images cause downstream displacement.** In Section 4.1, the AI-illustration step *also* introduced a new caption (`Figure 4.1.3` for the encoder-decoder description) without producing a corresponding image. Because the existing `<div class="diagram-container">` blocks were not reordered, every subsequent IMG block now sits one slot earlier than its intended caption. Same shape of bug in sections 1.3, 2.2, 3.1, 4.1, 5.2, 31.6 (each contains 1-2 displaced diagrams).

3. **Hand-edits broke caption order in the distillation chapter (Module 16).** Sections 16.1, 16.2, 16.3 each have figures captioned in a non-monotonic order. This is the only chapter where this concentration of out-of-order captions occurs and looks like a manual edit (likely cut/paste of section blocks during a content reorganisation). Cross-references in prose still point at the existing numbers, so a renumbering pass needs to also update prose references.

4. **Two-digit short filenames.** A handful of "section-summary" style images use only `fig-N.M-name.png` (no third digit), e.g. `fig-1.4-evolution.png`, `fig-20.3-graphrag-pipeline.png`, `fig-34.10-domain-tokenization.png`. These trip the auto-validator because the caption uses the full three-digit `N.M.K` form. Reader-visible behavior is correct.

**Worst chapters by misalignment count**
1. `part-1-foundations/module-04-transformer-architecture/section-4.1.html` — 3 displaced diagrams (the user-reported one), missing source image, filename collision.
2. `part-4-training-adapting/module-16-distillation-merging/` — 5 caption-out-of-order issues spread across sections 16.1, 16.2, 16.3, with prose cross-references that complicate renumbering.
3. `part-1-foundations/module-01-foundations-nlp-text-representation/` (sections 1.1, 1.3, 1.4) — 5 issues, two of them content-level (section 1.3).

---

## 4. Mechanical fixes applied

**Zero fixes were applied.** Every candidate fix failed at least one safety check:

- For Class 2A (content mismatches): the safe fix is to move IMG `<div>` blocks between DOM positions, which is structural surgery and risks altering the page layout. Requires human judgment about where each image belongs.
- For Class 2B (filename-only mismatches): renaming the caption number to match the filename would either (a) create duplicate caption numbers in the same file (sections 1.1, 1.4, 31.6) or (b) silently demote a three-digit caption to a two-digit one (sections 1.4, 20.3, 34.10), both of which break the table of contents and figure index. Renaming the IMG filename would require modifying image files (out of scope for this task).
- For Class 2C (out of order): renumbering captions would break in-prose cross-references, which were not in scope to update.

A read-only copy of the audit is preserved here as the source of truth.

---

## 5. Manual review queue

The following items need a human to make the call. Listed in priority order (reader-visible bugs first).

### High priority (reader sees the wrong image)
1. **`part-1-foundations/module-04-transformer-architecture/section-4.1.html`** — perform the four-step structural fix described in section 1 above. The user explicitly reported this file.
2. **`part-1-foundations/module-01-foundations-nlp-text-representation/section-1.3.html` lines 146 and 277** — Skip-gram caption (1.3.2) is showing a cosine-similarity image; cosine-similarity caption (1.3.5) is showing a FastText image. Two diagrams are swapped/displaced.
3. **`part-1-foundations/module-02-tokenization-subword-models/section-2.2.html` lines 140 and 483** — BPE caption (2.2.2) is showing a Unigram image; Unigram caption (2.2.4) is showing a byte-BPE image.
4. **`part-1-foundations/module-03-sequence-models-attention/section-3.1.html` line 265** — caption 3.1.3 (gradient magnitude) is showing the seq2seq encoder-decoder image. Decide whether to move the image or rewrite the caption.
5. **`part-1-foundations/module-05-decoding-text-generation/section-5.2.html` line 93** — temperature caption (5.2.2) is displaying a top-p sampling image.

### Medium priority (numbering inconsistency, no reader-visible content bug)
6. Sections 1.1, 1.4, 3.1 (line 98), 3.2, 20.3, 31.6, 34.10 — decide on a single source of truth: either rename images to match captions (preferred, requires asset rename) or accept the divergence permanently and silence the auditor.

### Lower priority (out-of-order captions)
7. Section 16.1, 16.2, 16.3 (Module 16 distillation) — renumber captions in source-order AND update the in-prose references ("Figure 16.1.5 illustrates...", "Figure 16.1.6 contrasts...") to the new numbers.
8. Section 9.2, 19.2 — single backwards jumps that can be renumbered if no prose references depend on them (verify per-file).

### Notes
- `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html` line 175 was flagged but is a likely false positive (the `<svg>` diagram below the IMG carries its own caption inline). Verify and dismiss.
- The "missing IMG without a caption" reports from a more aggressive earlier audit pass (e.g. `fig-4.1.7-residual-stream.png` at line 957 of section 4.1) are all benign: they are the second image of a figure pair where one block is HTML/SVG-rendered and the other is PNG-rendered. The current line-proximity audit no longer flags these.
