# Diagram Audit Report

_Generated from `KDP/validation/_raw/audit_full.json` (4,209 total issues across 473 files)._

## Summary

- **1,576** diagram/figure-related issues across **63** modules
- **222** HIGH (likely break the diagram or mislead the reader)
- **295** MEDIUM (degrade pedagogy / accessibility)
- **1,059** LOW (cosmetic / consistency)

## Issue counts by check

| Severity | Check | Count | What it means |
|----------|-------|-------|---------------|
| **HIGH** | `SVG_OVERLAP` | 150 | SVG text or shapes overlap (likely illegible) |
| **HIGH** | `DUP_FIGURE_NUM` | 41 | Two figures share the same number |
| **HIGH** | `SVG_TEXT_OVERFLOW` | 17 | SVG text extends past its container |
| **HIGH** | `BROKEN_FIGURE_REF` | 9 | Cross-reference points to a figure that doesn't exist |
| **HIGH** | `SVG_TEXT_CLIPPING` | 5 | SVG text is clipped by viewport/clip-path |
| **MEDIUM** | `CAPTION_MISALIGN` | 95 | Caption number doesn't match the figure it sits below |
| **MEDIUM** | `FIGURE_SEQUENCE` | 90 | Figure numbering out of sequence within chapter |
| **MEDIUM** | `GENERIC_SVG_LABEL` | 86 | SVG has generic/unhelpful label like 'Figure 1' instead of descriptive title |
| **MEDIUM** | `SVG_ARIA_TRUNCATED` | 17 | SVG <title>/<desc> appears truncated |
| **MEDIUM** | `SVG_PANEL_ASYM` | 6 | SVG multi-panel layout asymmetric / unbalanced |
| **MEDIUM** | `SVG_TITLE_TEXT` | 1 | SVG missing or weak <title> for accessibility |
| **LOW** | `MISSING_IMG_DIMS` | 733 | <img> tag lacks width/height (causes layout shift) |
| **LOW** | `MIXED_CAPTION_STYLE` | 326 | Caption formatting inconsistent across the chapter |

## Modules with the most diagram issues

| Module | Diagram issues |
|--------|----------------|
| `front-matter` | 101 |
| `part-8-evaluation-production/module-29-evaluation-observability` | 80 |
| `part-9-safety-strategy/module-32-safety-ethics-regulation` | 73 |
| `part-2-understanding-llms/module-06-pretraining-scaling-laws` | 70 |
| `part-8-evaluation-production/module-31-production-engineering` | 68 |
| `part-5-retrieval-conversation/module-20-rag` | 66 |
| `part-9-safety-strategy/module-33-strategy-product-roi` | 63 |
| `part-5-retrieval-conversation/module-19-embeddings-vector-db` | 62 |
| `part-2-understanding-llms/module-09-inference-optimization` | 52 |
| `part-1-foundations/module-04-transformer-architecture` | 48 |
| `part-4-training-adapting/module-13-synthetic-data` | 45 |
| `part-1-foundations/module-01-foundations-nlp-text-representation` | 43 |
| `part-1-foundations/module-02-tokenization-subword-models` | 42 |
| `part-2-understanding-llms/module-18-interpretability` | 40 |
| `part-3-working-with-llms/module-11-prompt-engineering` | 38 |

## HIGH-severity issues (fix before KDP submission)

These issues either break the diagram visually, mislead the reader, or break navigation. Address each before publishing.

### `BROKEN_FIGURE_REF` (9 occurrences)

_Cross-reference points to a figure that doesn't exist_

First 10 examples:

| File | Line | Detail |
|------|------|--------|
| `front-matter/section-fm.4.html` | 139 | 'Code Fragment 11.2.3' referenced in prose but no caption defines it |
| `front-matter/section-fm.4.html` | 140 | 'Figure 4.1.2' referenced in prose but no caption defines it |
| `part-11-idea-to-product/module-38-shipping-scaling/section-38.5.html` | 62 | 'Code Fragment 38.5.1' referenced in prose but no caption defines it |
| `part-11-idea-to-product/module-38-shipping-scaling/section-38.5.html` | 68 | 'Code Fragment 38.5.2' referenced in prose but no caption defines it |
| `part-11-idea-to-product/module-38-shipping-scaling/section-38.5.html` | 76 | 'Code Fragment 38.5.3' referenced in prose but no caption defines it |
| `part-11-idea-to-product/module-38-shipping-scaling/section-38.5.html` | 83 | 'Code Fragment 38.5.4' referenced in prose but no caption defines it |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` | 371 | 'Code Fragment 2.3.5' referenced in prose but no caption defines it |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` | 502 | 'Code Fragment 2.3.6' referenced in prose but no caption defines it |
| `part-1-foundations/module-02-tokenization-subword-models/section-2.3.html` | 626 | 'Code Fragment 2.3.7' referenced in prose but no caption defines it |

### `DUP_FIGURE_NUM` (41 occurrences)

_Two figures share the same number_

First 10 examples:

| File | Line | Detail |
|------|------|--------|
| `part-8-evaluation-production/module-29-evaluation-observability/section-29.11.html` | 168 | Duplicate "Code Fragment 29.11.2" on lines: 168, 202 |
| `part-8-evaluation-production/module-29-evaluation-observability/section-29.11.html` | 302 | Duplicate "Code Fragment 29.11.5" on lines: 302, 572 |
| `part-8-evaluation-production/module-29-evaluation-observability/section-29.11.html` | 572 | Duplicate "Code Fragment 29.11.7" on lines: 572, 666, 713 |
| `part-8-evaluation-production/module-29-evaluation-observability/section-29.12.html` | 150 | Duplicate "Code Fragment 29.12.2" on lines: 150, 252 |
| `part-8-evaluation-production/module-29-evaluation-observability/section-29.12.html` | 366 | Duplicate "Code Fragment 29.12.3" on lines: 366, 579 |
| `part-8-evaluation-production/module-29-evaluation-observability/section-29.12.html` | 366 | Duplicate "Code Fragment 29.12.5" on lines: 366, 579 |
| `part-8-evaluation-production/module-29-evaluation-observability/section-29.13.html` | 125 | Duplicate "Code Fragment 29.13.2" on lines: 125, 302 |
| `part-8-evaluation-production/module-29-evaluation-observability/section-29.13.html` | 302 | Duplicate "Code Fragment 29.13.5" on lines: 302, 570, 747 |
| `part-8-evaluation-production/module-29-evaluation-observability/section-29.14.html` | 153 | Duplicate "Code Fragment 29.14.2" on lines: 153, 248 |
| `part-8-evaluation-production/module-30-observability-monitoring/section-30.5.html` | 266 | Duplicate "Code Fragment 30.5.8" on lines: 266, 653 |
| ... | ... | _and 31 more_ |

### `SVG_OVERLAP` (150 occurrences)

_SVG text or shapes overlap (likely illegible)_

First 10 examples:

| File | Line | Detail |
|------|------|--------|
| `capstone/requirements.html` | 242 | Overlapping panels at y~8.0: [x=8.0,w=130.0] and [x=8.0,w=190.0] overlap by 130px |
| `capstone/requirements.html` | 242 | Overlapping panels at y~8.0: [x=8.0,w=190.0] and [x=8.0,w=190.0] overlap by 190px |
| `capstone/requirements.html` | 242 | Overlapping panels at y~8.0: [x=8.0,w=190.0] and [x=8.0,w=180.0] overlap by 190px |
| `capstone/requirements.html` | 242 | Overlapping panels at y~8.0: [x=8.0,w=180.0] and [x=8.0,w=200.0] overlap by 180px |
| `capstone/requirements.html` | 242 | Overlapping panels at y~8.0: [x=8.0,w=200.0] and [x=8.0,w=180.0] overlap by 200px |
| `capstone/requirements.html` | 242 | Overlapping panels at y~8.0: [x=8.0,w=180.0] and [x=8.0,w=200.0] overlap by 180px |
| `capstone/requirements.html` | 242 | Overlapping panels at y~8.0: [x=8.0,w=200.0] and [x=8.0,w=200.0] overlap by 200px |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html` | 72 | Overlapping panels at y~0.15: [x=6.0,w=190.0] and [x=6.0,w=190.0] overlap by 190px |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html` | 72 | Overlapping panels at y~50.0: [x=12.0,w=260.0] and [x=12.0,w=260.0] overlap by 260px |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html` | 72 | Overlapping panels at y~50.0: [x=12.0,w=260.0] and [x=12.0,w=260.0] overlap by 260px |
| ... | ... | _and 140 more_ |

### `SVG_TEXT_CLIPPING` (5 occurrences)

_SVG text is clipped by viewport/clip-path_

First 10 examples:

| File | Line | Detail |
|------|------|--------|
| `front-matter/pathways/index.html` | 185 | Text "AI" may be clipped: x=22.0 near right edge (28.0); y=22.0 near bottom edge (28.0) |
| `front-matter/pathways/index.html` | 203 | Text "UI" may be clipped: x=14.0 near left edge (0.0); x=14.0 near right edge (28.0); y=8.0 near top edge (0.0) |
| `front-matter/pathways/index.html` | 204 | Text "API" may be clipped: x=14.0 near left edge (0.0); x=14.0 near right edge (28.0); y=15.5 near bottom edge (28.0) |
| `front-matter/pathways/index.html` | 205 | Text "LLM" may be clipped: x=14.0 near left edge (0.0); x=14.0 near right edge (28.0); y=23.0 near bottom edge (28.0) |
| `front-matter/pathways/index.html` | 339 | Text "&gt;_" may be clipped: x=7.0 near left edge (0.0); y=16.0 near bottom edge (28.0) |

### `SVG_TEXT_OVERFLOW` (17 occurrences)

_SVG text extends past its container_

First 10 examples:

| File | Line | Detail |
|------|------|--------|
| `part-9-safety-strategy/module-33-strategy-product-roi/section-33.1.html` | 427 | Text "Tickets" overflows circle (r=18): est 42px vs 36px diameter (+17%) |
| `part-9-safety-strategy/module-33-strategy-product-roi/section-33.1.html` | 614 | Text "• Data pipeline setup" overflows circle (r=4): est 127px vs 8px diameter (+1488%) |
| `part-9-safety-strategy/module-33-strategy-product-roi/section-33.1.html` | 615 | Text "• Evaluation framework" overflows circle (r=4): est 133px vs 8px diameter (+1563%) |
| `part-9-safety-strategy/module-33-strategy-product-roi/section-33.1.html` | 617 | Text "• Governance basics" overflows circle (r=4): est 115px vs 8px diameter (+1336%) |
| `part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.1.html` | 409 | Text "128d" overflows circle (r=5): est 24px vs 10px diameter (+142%) |
| `part-5-retrieval-conversation/module-21-conversational-ai/section-21.1.html` | 129 | Text "• Task + chitchat" overflows circle (r=50): est 103px vs 100px diameter (+2%) |
| `part-5-retrieval-conversation/module-21-conversational-ai/section-21.1.html` | 134 | Text "virtual assistants, retail" overflows circle (r=50): est 157px vs 100px diameter (+57%) |
| `part-5-retrieval-conversation/module-21-conversational-ai/section-21.1.html` | 135 | Text "Structure: Medium" overflows circle (r=50): est 103px vs 100px diameter (+2%) |
| `part-5-retrieval-conversation/module-21-conversational-ai/section-21.1.html` | 140 | Text "• Freeform topics" overflows circle (r=50): est 103px vs 100px diameter (+2%) |
| `part-5-retrieval-conversation/module-21-conversational-ai/section-21.1.html` | 483 | Text "Response Generator (LLM)" overflows circle (r=50): est 158px vs 100px diameter (+58%) |
| ... | ... | _and 7 more_ |

## MEDIUM-severity issues (fix during quality polish)

Affect pedagogy and accessibility but won't block KDP. Prioritize the higher-volume ones.

### `CAPTION_MISALIGN` (95)

_Caption number doesn't match the figure it sits below_

First 5 examples:

| File | Line | Detail |
|------|------|--------|
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html` | 246 | Caption appears BEFORE code block at line 249 (should be after) |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.10.html` | 128 | Caption appears BEFORE code block at line 131 (should be after) |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.11.html` | 181 | Caption appears BEFORE code block at line 184 (should be after) |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.12.html` | 125 | Caption appears BEFORE code block at line 128 (should be after) |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.2.html` | 157 | Caption appears BEFORE code block at line 160 (should be after) |
| ... | ... | _and 90 more_ |

### `FIGURE_SEQUENCE` (90)

_Figure numbering out of sequence within chapter_

First 5 examples:

| File | Line | Detail |
|------|------|--------|
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html` | 1032 | Code Fragment 32.1.10 (line 1032) appears after Code Fragment 32.1.13 (line 970) |
| `part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.2.html` | 160 | Figure 19.2.2 (line 160) appears after Figure 19.2.3 (line 133) |
| `part-5-retrieval-conversation/module-20-rag/section-20.3.html` | 382 | Figure 20.3.4 (line 382) appears after Figure 20.3.4 (line 134) |
| `part-4-training-adapting/module-16-distillation-merging/section-16.1.html` | 606 | Figure 16.1.3 (line 606) appears after Figure 16.1.6 (line 305) |
| `part-4-training-adapting/module-16-distillation-merging/section-16.2.html` | 461 | Figure 16.2.4 (line 461) appears after Figure 16.2.5 (line 275) |
| ... | ... | _and 85 more_ |

### `GENERIC_SVG_LABEL` (86)

_SVG has generic/unhelpful label like 'Figure 1' instead of descriptive title_

First 5 examples:

| File | Line | Detail |
|------|------|--------|
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html` | 72 | Generic SVG aria-label: "Diagram" |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.1.html` | 344 | Generic SVG aria-label: "Diagram" |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.2.html` | 201 | Generic SVG aria-label: "Diagram" |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.2.html` | 279 | Generic SVG aria-label: "Diagram" |
| `part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.2.html` | 318 | Generic SVG aria-label: "Diagram" |
| ... | ... | _and 81 more_ |

### `SVG_ARIA_TRUNCATED` (17)

_SVG <title>/<desc> appears truncated_

First 5 examples:

| File | Line | Detail |
|------|------|--------|
| `capstone/requirements.html` | 242 | SVG aria-label appears truncated: "...owing how all 11 requirements integrate into a single system" |
| `part-9-safety-strategy/module-33-strategy-product-roi/section-33.1.html` | 607 | SVG aria-label appears truncated: "...ram: 6. Building an AI Roadmap (6 to 18 Months) Intermediate" |
| `part-8-evaluation-production/module-31-production-engineering/section-31.1.html` | 73 | SVG aria-label appears truncated: "...API layer) communicate through a well-defined service window" |
| `part-8-evaluation-production/module-31-production-engineering/section-31.1.html` | 240 | SVG aria-label appears truncated: "...ram: 2. Streaming Protocols: SSE and WebSockets Intermediate" |
| `part-7-multimodal-applications/module-27-multimodal/section-27.2.html` | 331 | SVG aria-label appears truncated: "...iagram: Architecture: Diffusion Transformers (DiT) for Video" |
| ... | ... | _and 12 more_ |

### `SVG_PANEL_ASYM` (6)

_SVG multi-panel layout asymmetric / unbalanced_

First 5 examples:

| File | Line | Detail |
|------|------|--------|
| `part-9-safety-strategy/module-33-strategy-product-roi/section-33.5.html` | 393 | Asymmetric panels at y~75: 650x60 vs 389x60 vs 116x60 (ratio 5.60x) |
| `part-9-safety-strategy/module-33-strategy-product-roi/section-33.5.html` | 498 | Asymmetric panels at y~75: 650x60 vs 389x60 vs 116x60 (ratio 5.60x) |
| `part-7-multimodal-applications/module-27-multimodal/section-27.1.html` | 256 | Asymmetric panels at y~20: 150x60 vs 200x60 (ratio 1.33x) |
| `part-7-multimodal-applications/module-27-multimodal/section-27.1.html` | 256 | Asymmetric panels at y~150: 150x60 vs 200x60 (ratio 1.33x) |
| `part-7-multimodal-applications/module-27-multimodal/section-27.3.html` | 126 | Asymmetric panels at y~40: 120x160 vs 160x170 (ratio 1.33x) |
| ... | ... | _and 1 more_ |

### `SVG_TITLE_TEXT` (1)

_SVG missing or weak <title> for accessibility_

First 5 examples:

| File | Line | Detail |
|------|------|--------|
| `part-4-training-adapting/module-15-peft/section-15.4.html` | 76 | SVG title text (redundant with caption): "Insertion Points by Method" |

## LOW-severity issues

- **`MISSING_IMG_DIMS`**: 733 occurrences. <img> tag lacks width/height (causes layout shift)
- **`MIXED_CAPTION_STYLE`**: 326 occurrences. Caption formatting inconsistent across the chapter

## Quick-win recommendations

Highest-leverage fixes:

1. **Add `width` / `height` attributes to all `<img>` tags** — 733 occurrences. Run `python scripts/find_missing_illustrations.py` or write a one-off script that adds dimensions from PIL.
2. **Renumber duplicate figures** — 41 `DUP_FIGURE_NUM` occurrences. Look at `scripts/fix_caption_numbering.py` and `scripts/fix_figure_sequence.py` (if they exist) and run.
3. **Fix SVG text overlaps** — 150 occurrences. The `scripts/audit_svg_overlaps.py` script identified them; the SVGs need manual repair (text repositioning) since the issue is visual.
4. **Replace generic SVG labels** — 86 occurrences. Many SVGs are titled simply 'Figure 1' or 'Diagram'; add descriptive labels for screen readers and EPUB nav.
5. **Fix figure-sequence + caption-misalign issues together** — 90 + 95 occurrences. These cascade: a misnumbered figure in section N.M shifts every reference downstream.

## Critical observations

From the agent's manual review of selected diagrams (transcript snippet):

> **RoPE diagram is non-functional**: A diagram about Rotary Position Embeddings consists of three text boxes that say 'pos=0: No rotation' and 'pos=3: Rotated by 3θ' with no actual rotation visualization. A diagram about ROTARY embeddings doesn't show any rotation.

Implication: even where the audit shows no automated issues, individual diagrams may be pedagogically broken. A human pass is needed for diagrams in math-heavy sections (Chapters 3-5: attention, Transformers, decoding).

## What this report does NOT cover

- **Factual correctness** of diagrams — the audit is structural; only a human can confirm whether an attention-pattern diagram correctly shows Q*K^T * V.
- **Pedagogical effectiveness** — whether each diagram earns its place in the chapter.
- **Raster image quality** — content of PNG/JPG figures was not opened and assessed.
- **Mermaid diagrams** — the audit ID list above doesn't include mermaid-specific checks; if mermaid is used, it would need a separate pass via `scripts/mermaid/`.

Run a sample manual review of 5-10 random diagrams from each part to validate the structural audit's findings reflect real visual quality.
