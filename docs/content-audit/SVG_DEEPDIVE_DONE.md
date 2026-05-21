# Deep-Dive THEORY SVG Diagrams Authored

Publication-quality inline SVG diagrams added for the dense deep-dive theory inserts
(branch v2.0). Each SVG uses the house standard: `<linearGradient>`/`<radialGradient>`
fills, `feDropShadow` filters, rounded corners, the #1e88e5/#43a047/#e53935/#fb8c00/#8e24aa
palette, #fafafa backgrounds, `role="img"` + descriptive `aria-label`, numeric character
entities for all symbols, min font-size 11, and a `<figure class="diagram">` wrapper with a
`<figcaption><strong>Figure N.M.K</strong>: ...</figcaption>`. A one-sentence prose
reference precedes each figure.

## Figures authored (8)

| # | Section | Figure | Diagram type | Caption line |
|---|---------|--------|--------------|--------------|
| 1 | `part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html` | Figure 2.3.3 | Multi-head W_O block-decomposition: concat-then-project (View A) shown equal to per-head slabs summed (View B), with equality banner | ~438 |
| 2 | `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html` | Figure 3.5.4 | PI vs NTK vs YaRN frequency-band comparison: three rows over a high-to-low frequency spectrum showing which RoPE bands each scheme rescales | ~359 |
| 3 | `part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html` | Figure 22.3.2 | Q-Former stage-1 three-loss training: 32 learnable queries cross-attend frozen image features, shared transformer branches into ITC/ITM/ITG heads (one mask each), losses sum | ~158 |
| 4 | `part-6-agentic-ai/module-26-ai-agents/section-26.2.html` | Figure 26.2.2 | MCTS four-stage loop: Selection (UCB1 path) / Expansion / Simulation (LLM value head) / Backpropagation drawn as four small trees with loop-back arrow and UCB1 annotation | ~359 |
| 5 | `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html` | Figure 32.3.3 | FLARE entropy-gated retrieval: CRAG/Self-RAG/FLARE comparison band plus FLARE per-token confidence gate (max p < tau) branching to emit vs retrieve-mid-generation-then-regenerate | ~379 |
| 6 | `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.1.html` | Figure 40.1.2 | Speech-to-speech joint vocabulary: waveform to RVQ codec (K codes/frame) to shared text+audio vocab, one AR transformer emitting an interleaved stream, depth transformer expanding each frame's hidden state to K codes | ~194 |
| 7 | `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.3.html` | Figure 75.3.2 | Mamba selective scan: input-dependent Delta_t, B_t, C_t discretize fixed A into A-bar_t / B-bar_t gating the recurrence h_t = A-bar_t h_{t-1} + B-bar_t x_t, with S4 contrast | ~259 |
| 8 | `part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html` | Figure 20.1.3 | RVQ residual chain: r_0 = z_t, each codebook quantizes the running residual r_k = r_{k-1} - e_k across K stages, reconstruction = sum of e_k, with coarse-to-fine and drop-codebook note | ~207 |

## Targets skipped (2) — already had a relevant mechanism figure

- `part-5-multimodal-llms/module-22-vision-language-models/section-22.1.html` (ViT patch
  embedding): Figure 22.1.1 already depicts the full image -> patches -> flatten + linear
  projection -> position embeddings -> transformer pipeline
  (`images/figure-35-1-1.svg`). Adding another would duplicate the concept.
- `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.2.html`
  (ZeRO-1/2/3 partitioning): Figure 59.2.2 is already an inline SVG Stage 0/1/2/3
  per-rank memory-reduction bar chart covering exactly this concept.

## Renumbering performed (downstream figures shifted to keep document order sequential)

- `section-3.5.html`: existing 3.5.4/3.5.5/3.5.6 -> 3.5.5/3.5.6/3.5.7 (captions only; no
  stale prose refs existed). Done via `fix_caption_order_only.py`.
- `section-22.3.html`: existing cost-matrix 22.3.2 -> 22.3.3.
- `section-26.2.html`: no shift (new fig is last).
- `section-32.3.html`: new FLARE fig inserted as 32.3.3; existing 32.3.3/32.3.4 ->
  32.3.4/32.3.5, including their prose references (lines updated manually, confirmed by
  the order fixer).
- `section-40.1.html`: existing latency fig 40.1.2 -> 40.1.3 (caption manually updated).
- `section-20.1.html`: existing TTS-landscape 20.1.3 -> 20.1.4 (caption + prose ref
  manually updated).

## Validation

- All 14 inline SVGs across the edited files parse as well-formed XML (Python
  `xml.dom.minidom`, 0 failures). All symbols use numeric character entities
  (e.g. `&#931;` Sigma, `&#8712;` in, `&#8594;` arrow, `&#256;` A-bar, `&#964;` tau);
  no raw `&` or `<` in text.
- Per-file audit (`agents.book-skills.scripts.audit.run --priority P0+P1+P2`) on the 8
  edited files: 0 issues. (One initial `SVG_TEXT_RIGHT_CLIP` P1 in the Q-Former diagram
  was fixed by widening its viewBox 800 -> 840.)
- Full-root audit (`--priority P0+P1+P2 --root .`, 558 files): 0 issues. No new
  FIGURE_SEQUENCE, DUP_FIGURE_NUM, or well-formedness problems introduced.
- No em dashes used in any caption or prose reference.
