# Regenerated Diagram Review

Generated 2026-05-10 via Imagen 4 (`imagen-4.0-generate-001`), 4 variants per figure.
Source PNGs were NOT replaced. Pick the best variant manually and copy it over the
original under each module's `images/` directory if you want to promote it.

Generation script: `KDP/build/regenerate_diagram.py`

---

## 1. Figure 4.2.2 - Decoder-Only Transformer

- **Source HTML**: `part-1-foundations/module-04-transformer-architecture/section-4.2.html` (line 87)
- **Original PNG**: `part-1-foundations/module-04-transformer-architecture/images/fig-4.2.2-decoder-only.png`
- **Concept**: vertical stack of decoder-only Transformer (Token+Pos Embedding -> N x [LN -> Causal Self-Attn -> +residual -> LN -> FFN -> +residual] -> Final LN -> Linear -> Softmax). Residuals MUST be curved bypass arrows, not boxes. Show ghost block to indicate "x N" repetition.
- **Aspect**: portrait 3:4
- **Variants**:
  - [v1](fig-4.2.2-decoder-only_v20260510-111948_1.png) - mostly garbled meta-text from prompt; reject
  - [v2](fig-4.2.2-decoder-only_v20260510-111948_2.png) - clean vertical flow, ghost stacking visible, residual loops shown
  - [v3](fig-4.2.2-decoder-only_v20260510-111948_3.png) - clean, has ghost stacks, residual loops labelled, full top-to-softmax flow
  - [v4](fig-4.2.2-decoder-only_v20260510-111948_4.png) - inverted flow, FFN above attention; reject
- **Recommendation: v3.** Best label fidelity ("Causal Multi-Head Self-Attention", "Feed-Forward Network (MLP)", residual add curves), shows the ghost-block stacking with "N x" tag, and has the full Linear/Softmax/Next-Token Probabilities tail intact. Minor typo ("Transforcure") in title - crop the title or relabel in post.

---

## 2. Figure 4.1.5 - Pre-LN vs Post-LN Comparison

- **Source HTML**: `part-1-foundations/module-04-transformer-architecture/section-4.1.html` (caption at line 778; note: image filename in the HTML is currently mislabelled as `fig-4.1.8-causal-mask.png` - separate cleanup task)
- **Target output filename**: `fig-4.1.5-pre-post-ln.png`
- **Concept**: side-by-side blocks. Post-LN: x -> Sublayer -> +residual -> LN. Pre-LN: x -> LN -> Sublayer -> +residual (residual bypasses both LN and sublayer). Show formulas LN(x+Sublayer(x)) vs x+Sublayer(LN(x)).
- **Aspect**: landscape 4:3
- **Variants**:
  - [v1](fig-4.1.5-pre-post-ln_v20260510-112029_1.png) - clean two columns, but Pre-LN side has garbled "B0H BOTH" placeholder; the formula LN(x+Sublayer(x)) appears only on left
  - [v2](fig-4.1.5-pre-post-ln_v20260510-112029_2.png) - has two sub-layer boxes per side (incorrect topology); reject
  - [v3](fig-4.1.5-pre-post-ln_v20260510-112029_3.png) - cleanest: two symmetric mini-stacks, both formulas present at bottom, residual loops drawn correctly
  - [v4](fig-4.1.5-pre-post-ln_v20260510-112029_4.png) - duplicates sub-layer; topology wrong; reject
- **Recommendation: v3.** Both formulas captioned, correct single-sublayer-per-side topology, clear residual bypass arc on each side. Ghost divider strip in the middle is unnecessary but unobtrusive.

---

## 3. Figure 3.1.5 - LSTM Cell Internals

- **Source HTML**: `part-1-foundations/module-03-sequence-models-attention/section-3.1.html` (line 300)
- **Original PNG**: `part-1-foundations/module-03-sequence-models-attention/images/fig-3.1.5-the-lstm-cell-the-cell-state-green-line-at-top-acts-as-a.png`
- **Concept**: single LSTM cell with cell-state highway at top (green), three sigmoid gates (forget, input, output), tanh candidate, pointwise multiply/add ops, h_(t-1)/x_t inputs left, h_t/C_t outputs right.
- **Aspect**: landscape 4:3
- **Variants**:
  - [v1](fig-3.1.5-lstm-cell_v20260510-112107_1.png) - has all three gates, tanh, cell-state highway across top, x_t/h_t inputs/outputs labelled
  - [v2](fig-3.1.5-lstm-cell_v20260510-112107_2.png) - too schematic, gates degenerate to summation symbols
  - [v3](fig-3.1.5-lstm-cell_v20260510-112107_3.png) - has all gates but layout messy; "Cell LSTM cell" title typo
  - [v4](fig-3.1.5-lstm-cell_v20260510-112107_4.png) - simpler but loses the forget/input separation
- **Recommendation: v1.** Best classic Olah-style LSTM rendering: green cell-state highway across the top with C_(t-1) -> C_t flow, sigmoid + tanh units, pointwise ops drawn as small circles, all input/output labels present and correctly placed. Some label crowding around the input gate but readable on Kindle.

---

## 4. Figure 3.3.3 - Multi-Head Attention

- **Source HTML**: `part-1-foundations/module-03-sequence-models-attention/section-3.3.html` (line 349)
- **Original PNG**: `part-1-foundations/module-03-sequence-models-attention/images/fig-3.3.3-multi-head.png`
- **Concept**: input X -> 4 parallel heads, each with W^Q_i / W^K_i / W^V_i projections -> Scaled Dot-Product Attention per head -> Concat -> W^O -> output.
- **Aspect**: portrait 3:4
- **Variants**:
  - [v1](fig-3.3.3-multi-head_v20260510-112142_1.png) - 4 heads as labelled rows, 4 attention boxes, Concat bar, W^O on top, output labelled
  - [v2](fig-3.3.3-multi-head_v20260510-112142_2.png) - flow inverted (input top, output... unclear); reject
  - [v3](fig-3.3.3-multi-head_v20260510-112142_3.png) - heads labelled but no attention boxes shown; collapses too much
  - [v4](fig-3.3.3-multi-head_v20260510-112142_4.png) - flow direction inverted again; reject
- **Recommendation: v1.** Only variant that shows the full pipeline correctly: input X at bottom, 4 head rows with separate Q/K/V projection boxes, 4 Scaled Dot-Product Attention blocks, Concat bar, W^O projection, Output(d_model) at top. Heading "Multi-head attention h=4 heads" is correct. Some label fuzziness on the W^Q/W^K/W^V column headers but legible.

---

## 5. Figure 35.10.1 - Domain Tokenization Pipeline

- **Source HTML**: `part-10-frontiers/module-35-emerging-architectures/section-35.10.html` (line 62)
- **Original PNG**: `part-10-frontiers/module-35-emerging-architectures/images/fig-34.10-domain-tokenization.png` (currently 8049 x 1224, 6.58 aspect - unreadable on Kindle)
- **Concept**: three lanes (Proteins / Molecules / DNA-RNA), 4 stages per lane (Raw Input -> Pre-tokenization -> BPE/Unigram Training [shared] -> Merge with Base LM Vocab [shared]).
- **Aspect**: portrait 3:4
- **Variants**:
  - [v1](fig-34.10-domain-tokenization_v20260510-112233_1.png) - 3 lanes with example sequences, pre-tokenization rules per lane, shared BPE band, merged output box
  - [v2](fig-34.10-domain-tokenization_v20260510-112233_2.png) - cuts off after Stage 2; incomplete
  - [v3](fig-34.10-domain-tokenization_v20260510-112233_3.png) - collapses to a single column; lanes lost
  - [v4](fig-34.10-domain-tokenization_v20260510-112233_4.png) - 3 lanes but stage labels duplicated/jumbled
- **Recommendation: v1.** Only variant that completes the full 4-stage pipeline AND keeps the 3-lane comparison. Shows raw input examples (MGSSHHHH..., CC(=O)c1ccccc1, ATGGCCAAGTAA), per-lane pre-tokenization rules, and a unified merge box at the bottom. Some "Stage 1/Stage 3" mis-numbering in label text - relabel in post or accept.

---

## Summary

| Figure | Recommended | Notes |
|---|---|---|
| fig-4.2.2-decoder-only | v3 | Title typo "Transforcure" - crop or overlay |
| fig-4.1.5-pre-post-ln | v3 | Both formulas present, clean topology |
| fig-3.1.5-lstm-cell | v1 | Classic Olah-style; minor crowding |
| fig-3.3.3-multi-head | v1 | Only variant with complete pipeline |
| fig-34.10-domain-tokenization | v1 | Stage numbering needs minor relabel |

Imagen 4 reliably nails layout/topology but consistently misspells small portions of dense label text. For all 5 recommended variants, treat the model output as a "structurally correct draft" and either accept minor typos for v1/v3 publication or do a quick text-overlay pass in Affinity/Figma before promoting.

To promote a variant, copy it over the source PNG, e.g.:

```bash
cp KDP/diagrams/regenerated/fig-4.2.2-decoder-only_v20260510-111948_3.png \
   part-1-foundations/module-04-transformer-architecture/images/fig-4.2.2-decoder-only.png
```

---

## Copyright-flagged redraws (2026-05-10)

This batch redraws the seven third-party diagrams flagged in `KDP/validation/copyright_audit.md` Section 2. Goal: produce conceptually equivalent originals so the book no longer relies on Raschka, NVIDIA, Lambert/HF, Huyen, Lilian Weng, or Edge et al. artwork. Output PNGs are NOT promoted into source `images/` directories yet; pick the recommended variant and copy it over after a final visual review.

All seven were generated via `KDP/build/regenerate_diagram.py` with Imagen 4 (`imagen-4.0-generate-001`), n=4. Prompt files saved alongside variants as `*_prompt.txt`.

### 1. Figure 16.1.3 - LoRA weight decomposition (replaces `lora-weights-raschka.png`)

- **Source HTML**: `part-4-training-adapting/module-16-peft/section-16.1.html` line 91
- **Original attribution**: "Source: Sebastian Raschka, 2023. *Parameter-Efficient LLM Finetuning With Low-Rank Adaptation (LoRA)*" (sebastianraschka.com blog).
- **Concept**: Frozen pretrained matrix W (d x k) in parallel with low-rank update Delta-W = B . A where B is d x r and A is r x k, with r much smaller than d, k. Output: h = Wx + BAx.
- **Prompt file**: `fig-16.1.3-lora-decomposition_v20260510-113935_prompt.txt`
- **Variants**: [v1](fig-16.1.3-lora-decomposition_v20260510-113935_1.png), [v2](fig-16.1.3-lora-decomposition_v20260510-113935_2.png), [v3](fig-16.1.3-lora-decomposition_v20260510-113935_3.png), [v4](fig-16.1.3-lora-decomposition_v20260510-113935_4.png)
- **Recommendation: v4.** Cleanest topology: frozen W with lock icon on the left, parallel B.A path on the right, explicit "+" merge node, dimension labels d x k / d x r / r x k correctly placed, "rank r << d, k" annotation, and the `h = Wx + BAx` equation rendered crisply at the bottom. v2 is a viable backup but slightly busier.
- **Equivalence**: Conveys exactly the same low-rank-bypass idea as the Raschka original; safe swap, no narrative change in the surrounding text.

### 2. Figure 2.2.x - BPE training overview (replaces `raschka-bpe-overview.jpg`)

- **Source location**: `raschka-bpe-overview.jpg` lives under `part-1-foundations/module-02-tokenization-subword-models/images/` but the audit-flagged image is currently **orphaned** (no `<img>` reference in the live HTML). Treat this redraw as a drop-in replacement asset for any future BPE figure or as a safe override if the file is ever re-referenced.
- **Original attribution**: filename indicates Sebastian Raschka source; jpg format inconsistent with the otherwise PNG-only directory.
- **Concept**: BPE training loop, starting from character/byte tokens, count adjacent-pair frequencies, merge most-frequent pair, repeat until vocabulary size reached.
- **Prompt file**: `fig-2.2-bpe-overview_v20260510-114010_prompt.txt`
- **Variants**: [v1](fig-2.2-bpe-overview_v20260510-114010_1.png), [v2](fig-2.2-bpe-overview_v20260510-114010_2.png), [v3](fig-2.2-bpe-overview_v20260510-114010_3.png), [v4](fig-2.2-bpe-overview_v20260510-114010_4.png)
- **Recommendation: v2.** All four numbered stages visible (Initialize, Count pairs, Merge most frequent pair, Repeat), clear character tiles for `l o w e r n s t`, frequency table on the right with readable pair counts, and visible merge of `l + o` to `lo`. Minor typo in stage 4 caption ("uneed", "voculary"); fix in post via overlay.
- **Equivalence**: Same algorithmic flow as the Raschka diagram, plus an explicit frequency table the original lacked. Safe swap.

### 3. Figure 21.1.3 - RAG pipeline (replaces `rag-pipeline-nvidia.png`)

- **Source HTML**: `part-5-retrieval-conversation/module-21-rag/section-21.1.html` line 105
- **Original attribution**: "Source: NVIDIA, 2023. *RAG 101: Demystifying Retrieval-Augmented Generation Pipelines*" (NVIDIA Developer Blog).
- **Concept**: Two-lane RAG architecture: offline ingestion (Documents, Chunker, Embedding Model, Vector DB) and online query (Query, Embedding Model, Retriever, Top-k, Prompt Builder, LLM, Answer), sharing the central Vector DB.
- **Prompt file**: `fig-21.1.3-rag-pipeline_v20260510-114050_prompt.txt`
- **Variants**: [v1](fig-21.1.3-rag-pipeline_v20260510-114050_1.png), [v2](fig-21.1.3-rag-pipeline_v20260510-114050_2.png), [v3](fig-21.1.3-rag-pipeline_v20260510-114050_3.png), [v4](fig-21.1.3-rag-pipeline_v20260510-114050_4.png)
- **Recommendation: v3.** Both lanes drawn, all eight nodes labelled correctly (Documents, Chunker, Embedding Model, Vector Database for ingestion; User Query, Retriever, Embedding Model, Top-k Chunks, Prompt Builder, LLM, Answer for query). Distinct teal/amber lane backgrounds. Note: the query lane in v3 reads slightly right-to-left after Retriever; if that bothers an editor, v2 is a simpler fallback (no LLM box rendered, would need overlay).
- **Equivalence**: Architecturally identical to the NVIDIA diagram, same two lanes, same nodes, same shared vector store. Safe swap.

### 4. Figure 17.1.2a - RLHF PPO step (replaces `hf-rlhf-training.png`)

- **Source HTML**: `part-4-training-adapting/module-18-alignment-rlhf-dpo/section-18.1.html` line 85
- **Original attribution**: "Source: Lambert et al., *Illustrating RLHF*, Hugging Face Blog, 2023" (CC-BY per HF policy, but the audit recommends a clean redraw to avoid downstream verification).
- **Concept**: PPO optimization step: Policy LM generates response from prompt; Reward Model scores; frozen Reference LM contributes log-probs for KL penalty; combined `r - beta . KL` signal feeds PPO gradient update back to Policy LM.
- **Prompt file**: `fig-17.1.2a-rlhf-rl-step_v20260510-114153_prompt.txt`
- **Variants**: [v1](fig-17.1.2a-rlhf-rl-step_v20260510-114153_1.png), [v2](fig-17.1.2a-rlhf-rl-step_v20260510-114153_2.png), [v3](fig-17.1.2a-rlhf-rl-step_v20260510-114153_3.png), [v4](fig-17.1.2a-rlhf-rl-step_v20260510-114153_4.png)
- **Recommendation: v1.** Only variant where all four required components (Policy LM, Reward Model, Reference LM, KL Penalty) are correctly rendered with the `r - beta . KL` combination feeding gradient updates. v2/v4 leak Mermaid/style metadata into the rendered text and v3 has a duplicated "PPO" title and garbled labels.
- **Equivalence**: Captures the same PPO loop as the Lambert diagram. Needs a manual relabel pass (a few labels are slightly garbled, e.g., "Impolate") before publication.

### 5. Figure 17.1.2b - RLHF three-stage pipeline (replaces `huyenchip-rlhf-pipeline.png`)

- **Source HTML**: `part-4-training-adapting/module-18-alignment-rlhf-dpo/section-18.1.html` line 89
- **Original attribution**: "Source: Chip Huyen, *RLHF: Reinforcement Learning from Human Feedback*, 2023" (huyenchip.com personal blog, no license).
- **Concept**: Three-stage RLHF training pipeline: (1) SFT on instruction-response demos, (2) Reward Model training on human-ranked pairs, (3) PPO using the SFT model as policy init and the reward model as reward signal.
- **Prompt file**: `fig-17.1.2b-rlhf-three-stage_v20260510-114233_prompt.txt`
- **Variants**: [v1](fig-17.1.2b-rlhf-three-stage_v20260510-114233_1.png), [v2](fig-17.1.2b-rlhf-three-stage_v20260510-114233_2.png), [v3](fig-17.1.2b-rlhf-three-stage_v20260510-114233_3.png), [v4](fig-17.1.2b-rlhf-three-stage_v20260510-114233_4.png)
- **Recommendation: v4.** All three stages clearly numbered top-to-bottom with distinct teal/amber/navy bands, model artifacts (Pretrained Base LM, SFT Model, Reward Model, Aligned LM) flow correctly between stages, and the PPO loop arrow at the bottom is visible. Some auxiliary text needs touch-up ("Scorip" should be "Score").
- **Equivalence**: Same three-stage decomposition as Huyen's diagram. Safe swap after a label cleanup pass.

### 6. Figure 28.1.3 - Diffusion forward/reverse process (replaces `ddpm-forward-reverse-process.png`)

- **Source HTML**: `part-7-multimodal-applications/module-28-multimodal/section-28.1.html` line 69
- **Original attribution**: "Diagram from Lilian Weng, lilianweng.github.io" (personal blog, no license).
- **Concept**: DDPM Markov chain. Forward `q(x_t | x_{t-1})` adds Gaussian noise from x_0 to x_T; reverse `p_theta(x_{t-1} | x_t)` denoises step-by-step using a learned network epsilon_theta.
- **Prompt file**: `fig-28.1.3-ddpm-process_v20260510-114324_prompt.txt`
- **Variants**: [v1](fig-28.1.3-ddpm-process_v20260510-114324_1.png), [v2](fig-28.1.3-ddpm-process_v20260510-114324_2.png), [v3](fig-28.1.3-ddpm-process_v20260510-114324_3.png), [v4](fig-28.1.3-ddpm-process_v20260510-114324_4.png)
- **Recommendation: v4.** Clearest two-arrow Markov chain: forward arrow (top, navy) with sharp teapot becoming progressively noisier thumbnails ending in static; reverse arrow (bottom, teal) labelled "learned denoiser" goes the other direction with epsilon_theta icons between steps. Both `q(...)` and `p_theta(...)` formulas rendered. v1 is also viable if a different subject illustration is preferred.
- **Equivalence**: Functionally identical to the Lilian Weng figure (forward chain + reverse chain + noise schedule notation). Safe swap.

### 7. Figure 21.3.4 - GraphRAG pipeline (replaces `fig-20.3-graphrag-pipeline.png`)

- **Source HTML**: `part-5-retrieval-conversation/module-21-rag/section-21.3.html` line 311
- **Original attribution**: "Source: Edge et al., *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*, 2024" (arXiv 2404.16130).
- **Concept**: Two-phase GraphRAG architecture. (A) indexing: Documents, LLM entity/relation extraction, Knowledge Graph, Leiden community detection, LLM community summaries. (B) query: User Query, Router, Local Search (entity neighbors) for specific questions or Global Search (map-reduce over community summaries) for broad questions, Response.
- **Prompt file**: `fig-21.3.4-graphrag-pipeline_v20260510-114413_prompt.txt`
- **Variants**: [v1](fig-21.3.4-graphrag-pipeline_v20260510-114413_1.png), [v2](fig-21.3.4-graphrag-pipeline_v20260510-114413_2.png), [v3](fig-21.3.4-graphrag-pipeline_v20260510-114413_3.png), [v4](fig-21.3.4-graphrag-pipeline_v20260510-114413_4.png)
- **Recommendation: v4.** Best of the batch: Phase A and Phase B are clearly separated bands (teal / amber), all five indexing stages are present, and the query phase shows both Local Search and Global Search lanes converging on Response with a Router diamond. Labels are crisp and almost typo-free.
- **Equivalence**: Faithful redraw of the Edge et al. two-phase pipeline. Safe swap.

### Summary table

| # | Figure | Recommended | Legal review | Touch-up needed |
|---|---|---|---|---|
| 1 | LoRA decomposition (15.1.3) | v4 | Pass as-is | None |
| 2 | BPE overview (2.2) | v2 | Pass as-is | Minor: 2 typos in stage 4 caption |
| 3 | RAG pipeline (20.1.3) | v3 | Pass as-is | Optional: query lane direction |
| 4 | RLHF PPO step (17.1.2a) | v1 | Pass after touch-up | Required: a few label words garbled |
| 5 | RLHF three-stage (17.1.2b) | v4 | Pass as-is | Minor: "Scorip" -> "Score" |
| 6 | DDPM diffusion (27.1.3) | v4 | Pass as-is | None |
| 7 | GraphRAG pipeline (20.3.4) | v4 | Pass as-is | None |

### Promotion checklist

To promote a variant, copy it over the source image (filenames retained so the source HTML keeps working unchanged):

    cp KDP/diagrams/regenerated/fig-16.1.3-lora-decomposition_v20260510-113935_4.png \
       part-4-training-adapting/module-16-peft/images/lora-weights-raschka.png

    cp KDP/diagrams/regenerated/fig-2.2-bpe-overview_v20260510-114010_2.png \
       part-1-foundations/module-02-tokenization-subword-models/images/raschka-bpe-overview.jpg

    cp KDP/diagrams/regenerated/fig-21.1.3-rag-pipeline_v20260510-114050_3.png \
       part-5-retrieval-conversation/module-21-rag/images/rag-pipeline-nvidia.png

    cp KDP/diagrams/regenerated/fig-17.1.2a-rlhf-rl-step_v20260510-114153_1.png \
       part-4-training-adapting/module-18-alignment-rlhf-dpo/images/hf-rlhf-training.png

    cp KDP/diagrams/regenerated/fig-17.1.2b-rlhf-three-stage_v20260510-114233_4.png \
       part-4-training-adapting/module-18-alignment-rlhf-dpo/images/huyenchip-rlhf-pipeline.png

    cp KDP/diagrams/regenerated/fig-28.1.3-ddpm-process_v20260510-114324_4.png \
       part-7-multimodal-applications/module-28-multimodal/images/ddpm-forward-reverse-process.png

    cp KDP/diagrams/regenerated/fig-21.3.4-graphrag-pipeline_v20260510-114413_4.png \
       part-5-retrieval-conversation/module-21-rag/images/fig-20.3-graphrag-pipeline.png

Once promoted, also update the `figcaption` / `diagram-caption` HTML in each section to remove the "Source: ..." attribution lines and the cited URLs, since the figures will then be original work by the authors.

### Label-quality notes

Imagen 4 continues to garble dense small text. For this batch:

- **Pass-without-touch-up**: GraphRAG (v4), LoRA (v4), Diffusion (v4), RLHF three-stage (v4 with one-letter fix), RAG (v3) - labels are correct enough to publish as-is.
- **Touch-up required**: RLHF PPO (v1) - all structural elements correct, only label text needs fixing in Affinity / Figma overlay pass.
- **Already orphaned**: BPE (v2) - the source image is not currently referenced in any HTML, so promotion is optional; if added back, expect a one-pass overlay touch-up.
