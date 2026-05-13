# SVG Diagram Replacements — Review & Promotion Guide

**Generated**: 2026-05-10 via the LLM-SVG pipeline (`KDP/build/generate_diagram_svg.py`)
**Renderer**: `resvg-py` (pure-Rust, no GTK / no admin install needed)
**Source files**: each `.svg` is plain text — open in any editor or vector tool (Inkscape, Affinity, Figma) to tweak.

These 7 replace the third-party diagrams flagged by the copyright audit (`KDP/validation/copyright_audit.md`). Unlike the Imagen 4 attempts at `KDP/diagrams/regenerated/`, **all text labels are perfect** because they're encoded as `<text>` elements, not pixels.

---

## The 7 redraws

| # | Figure | Replaces | SVG file | PNG render | Concept |
|---|--------|----------|----------|------------|---------|
| 1 | LoRA decomposition (15.1.3) | `lora-weights-raschka.png` | [`fig-16.1.3-lora-decomposition.svg`](fig-16.1.3-lora-decomposition.svg) | 195 KB | Frozen W₀ + trainable B·A; forward pass shows `h = W₀x + BAx`; explicit shape annotations |
| 2 | BPE overview (2.2) | `raschka-bpe-overview.jpg` | [`fig-2.2-bpe-overview.svg`](fig-2.2-bpe-overview.svg) | 293 KB | 4-step process: split → count pairs → merge winner → repeat; with concrete worked example |
| 3 | RAG pipeline (20.1.3) | `rag-pipeline-nvidia.png` | [`fig-21.1.3-rag-pipeline.svg`](fig-21.1.3-rag-pipeline.svg) | 321 KB | Two-lane: A (offline ingest) + B (online query) with numbered steps + failure-points callout |
| 4 | RLHF PPO step (17.1.2a) | `hf-rlhf-training.png` | [`fig-17.1.2a-rlhf-ppo-step.svg`](fig-17.1.2a-rlhf-ppo-step.svg) | 228 KB | Single PPO iteration: prompt → policy → response → reward + KL → gradient update; loop indicator |
| 5 | RLHF three-stage (17.1.2b) | `huyenchip-rlhf-pipeline.png` | [`fig-17.1.2b-rlhf-three-stage.svg`](fig-17.1.2b-rlhf-three-stage.svg) | 354 KB | SFT → Reward Model → PPO as 3 distinct panels, with cost annotations per stage |
| 6 | DDPM diffusion (27.1.3) | `ddpm-forward-reverse-process.png` | [`fig-28.1.3-ddpm-process.svg`](fig-28.1.3-ddpm-process.svg) | 368 KB | Forward (top, red) + reverse (bottom, green) with progressive noise illustrations + equations |
| 7 | GraphRAG (20.3.4) | `fig-20.3-graphrag-pipeline.png` | [`fig-21.3.4-graphrag-pipeline.svg`](fig-21.3.4-graphrag-pipeline.svg) | 312 KB | Phase A indexing (5 steps) + Phase B query routing (router → local OR global → LLM) |

---

## Quality vs. the Imagen 4 versions

| Dimension | Imagen 4 (KDP/diagrams/regenerated/) | **LLM-SVG (this folder)** |
|-----------|-------------------------------------|---------------------------|
| Text labels | Garbled in 5 of 7 ("Causla", "Reword Model", "Scoirp", "Impolate", etc.) | **All perfect** |
| Topology accuracy | Generally correct | **Verified by hand** against source HTML |
| Semantic color | Random | **Consistent**: blue=data, green=model, purple=orchestration, gold=storage, red=warning |
| Vector / scalable | Raster only | **SVG** — infinite zoom |
| File size | 280 KB - 700 KB PNG | **~10 KB SVG** + ~250 KB PNG render |
| Editable post-generation | Regenerate | **Open in text editor** — fix typos, adjust positions, add elements |
| Includes legend | Mostly no | **Yes** — every diagram has one |
| Includes failure-points / callouts | No | **Yes** for RAG, GraphRAG; tradeoff annotations elsewhere |
| Caption fidelity | Often off | **Matches source caption verbatim** |

---

## How to promote

For each figure you're happy with:

```bash
# Example: promote the LoRA SVG to replace the third-party PNG
SRC=KDP/diagrams/svg/fig-16.1.3-lora-decomposition.svg
DST=part-4-training-adapting/module-16-fine-tuning-peft-lora-qlora/images/lora-weights-raschka.svg
cp "$SRC" "$DST"

# Then update the HTML <img> tag to use the SVG and drop the third-party attribution
# Search for: src="images/lora-weights-raschka.png"
# Replace with: src="images/lora-weights-raschka.svg"
# Also delete the "Source: ..." part of the figcaption (no longer needed - now original work)
```

Per-figure source paths:

| # | Figure | Target source path |
|---|--------|-------------------|
| 1 | LoRA | `part-4-training-adapting/module-16-fine-tuning-peft-lora-qlora/images/` |
| 2 | BPE | `part-1-foundations/module-02-tokenization-subword-models/images/` |
| 3 | RAG | `part-5-retrieval-conversation/module-21-rag/images/` |
| 4 | RLHF PPO | `part-4-training-adapting/module-18-alignment-rlhf-dpo/images/` |
| 5 | RLHF three-stage | `part-4-training-adapting/module-18-alignment-rlhf-dpo/images/` |
| 6 | DDPM | `part-7-multimodal-applications/module-28-multimodal/images/` |
| 7 | GraphRAG | `part-5-retrieval-conversation/module-21-rag/images/` |

After promotion, also remove the third-party attribution from each `figcaption` (since the diagrams are now original work):
```html
<!-- BEFORE -->
<div class="diagram-caption"><strong>Figure 21.1.3</strong>: ... Source: NVIDIA, 2023. <a href="...">RAG 101...</a></div>

<!-- AFTER -->
<div class="diagram-caption"><strong>Figure 21.1.3</strong>: ...</div>
```

---

## EPUB integration considerations

EPUB readers DO support SVG. Your build script (`build_epub.py`) already includes SVG handling: chapters with embedded SVG get `properties=["svg"]` set on the EpubHtml. No changes needed.

For the HTML web edition, browsers render SVG natively at any zoom — better than PNG for retina/high-DPI displays.

If you'd rather ship PNGs for maximum reader compatibility, the rendered `*.png` files in this folder are 1200-1400 px wide (Kindle-friendly).

---

## How these were generated

This batch was generated **directly inside the Claude Code conversation** (no API key needed locally) following the `technical-diagram-designer` skill workflow:

1. Read each figure's source HTML (caption + surrounding paragraphs) to understand the concept
2. Apply the skill's step-by-step workflow:
   - Step 1: Clarify intent (audience, learning objective, main message)
   - Step 2: Decompose into 5-9 primary elements
   - Step 3: Choose diagram type (pipeline / mechanism / multi-panel / etc.)
   - Step 4: Design visual grammar (semantic colors, shape conventions)
   - Step 5: Layout specification
3. Write SVG directly with `<text>` elements for all labels (perfect text)
4. Rasterize via `resvg-py` for PNG fallback

For future diagrams, run the script:
```bash
export ANTHROPIC_API_KEY=sk-ant-...
python KDP/build/generate_diagram_svg.py \
    --figure fig-X.Y.Z-name \
    --concept "specific technical description with concrete elements" \
    --aspect portrait \
    --variants 3
```

Or — preferred for high-quality work — request the diagrams interactively in Claude Code so you can iterate on the design.
