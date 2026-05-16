# Diagram complexity audit

Total SVGs scanned: **178**. Score combines size, line count, rect count, text count, long-text count, and canvas size. Score >= 4 flags as overly complex.

Overly-complex (score>=4): **93**


## Top 30 over-complex diagrams

| Rank | Score | Size | Lines | Rect | Text | Long | Canvas | Path | Recommendation |
|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 1 | 13 | 22605 | 300 | 260 | 54 | 2 | 1200x850 | `part-1-foundations/module-04-transformer-architecture/images/fig-4.1.4-pos-encoding.svg` | merge boxes; drop annotations |
| 2 | 12 | 11806 | 162 | 28 | 65 | 19 | 1300x760 | `part-2-understanding-llms/module-10-inference-optimization/images/fig-9.5.1-the-2-4-structured-sparsity-pattern-every-group-of-4-weight.svg` | merge boxes; shorten labels; drop annotations |
| 3 | 12 | 10434 | 151 | 22 | 53 | 18 | 1300x760 | `part-1-foundations/module-02-tokenization-subword-models/images/fig-2.2.5-byte-bpe.svg` | merge boxes; shorten labels; drop annotations |
| 4 | 11 | 15327 | 223 | 80 | 56 | 4 | 1300x700 | `part-2-understanding-llms/module-11-interpretability/images/fig-10.1.2-common-attention-head-types-observed-across-transformer-mode.svg` | merge boxes; drop annotations |
| 5 | 11 | 12348 | 186 | 19 | 75 | 11 | 1300x760 | `part-2-understanding-llms/module-10-inference-optimization/images/fig-9.2.2-pagedattention-maps-logical-kv-cache-blocks-to-non-contiguou.svg` | merge boxes; shorten labels; drop annotations |
| 6 | 11 | 12189 | 162 | 13 | 64 | 11 | 1400x880 | `part-7-multimodal-generation/module-32-embodied-world-models/images/diagram-32-5-1.svg` | merge boxes; shorten labels; drop annotations |
| 7 | 11 | 11675 | 157 | 10 | 71 | 12 | 1400x1100 | `appendices/appendix-f-agent-frameworks/images/diagram-framework-selection.svg` | shorten labels; shrink canvas; drop annotations |
| 8 | 10 | 11979 | 171 | 29 | 72 | 7 | 1400x820 | `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-frontier-edge-device-matrix.svg` | merge boxes; drop annotations |
| 9 | 9 | 10250 | 135 | 13 | 49 | 16 | 1400x1180 | `part-1-foundations/module-04-transformer-architecture/images/diagram-transformer-anatomy.svg` | merge boxes; shorten labels; shrink canvas; drop annotations |
| 10 | 8 | 11422 | 178 | 14 | 84 | 5 | 1300x760 | `part-3-working-with-llms/module-15-hybrid-ml-llm/images/fig-13.8.1-log-to-dataset-pipeline.svg` | merge boxes; drop annotations |
| 11 | 8 | 11202 | 158 | 18 | 53 | 5 | 1300x720 | `part-2-understanding-llms/module-07-pretraining-scaling-laws/images/fig-6.8.1-production-llm-training-architecture-data-flows-from-object.svg` | merge boxes; drop annotations |
| 12 | 8 | 11160 | 146 | 17 | 53 | 14 | 1400x880 | `part-7-multimodal-generation/module-32-embodied-world-models/images/diagram-32-3-1.svg` | merge boxes; shorten labels; drop annotations |
| 13 | 8 | 11125 | 159 | 18 | 55 | 10 | 1400x820 | `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-frontier-codesign-stacks.svg` | merge boxes; drop annotations |
| 14 | 8 | 10868 | 168 | 15 | 67 | 7 | 1300x760 | `part-3-working-with-llms/module-14-prompt-engineering/images/fig-12.6.1-dspy-optimization-loop.svg` | merge boxes; drop annotations |
| 15 | 8 | 10745 | 160 | 68 | 39 | 3 | 1300x700 | `part-2-understanding-llms/module-10-inference-optimization/images/fig-9.2.4-the-three-attention-variants-compared-side-by-side-mha-stor.svg` | merge boxes; drop annotations |
| 16 | 8 | 10601 | 150 | 30 | 49 | 12 | 1400x820 | `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-frontier-fa4-memory-hierarchy.svg` | merge boxes; shorten labels; drop annotations |
| 17 | 8 | 10449 | 151 | 33 | 49 | 8 | 1300x700 | `part-1-foundations/module-05-decoding-text-generation/images/fig-5.4.2-diffusion.svg` | merge boxes; drop annotations |
| 18 | 8 | 10371 | 126 | 62 | 53 | 3 | 1100x540 | `part-2-understanding-llms/module-07-pretraining-scaling-laws/images/fig-6.6.4-pipeline.svg` | merge boxes; drop annotations |
| 19 | 8 | 9350 | 159 | 29 | 48 | 3 | 1300x700 | `part-1-foundations/module-04-transformer-architecture/images/fig-4.3.4-pos-strategies.svg` | merge boxes; drop annotations |
| 20 | 8 | 9227 | 140 | 15 | 51 | 14 | 1400x820 | `part-12-frontiers/module-64-agi-trajectories/images/diagram-frontier-augmentation-vs-automation.svg` | merge boxes; shorten labels; drop annotations |
| 21 | 8 | 7857 | 110 | 23 | 44 | 17 | 1300x700 | `part-2-understanding-llms/module-10-inference-optimization/images/fig-9.1.3-gptq-compensates-for-rounding-errors-across-columns-using-th.svg` | merge boxes; shorten labels; drop annotations |
| 22 | 7 | 10129 | 165 | 52 | 30 | 4 | 1300x700 | `part-2-understanding-llms/module-10-inference-optimization/images/fig-9.1.2-quantization-granularity-levels-per-group-quantization-bot.svg` | merge boxes |
| 23 | 6 | 155371 | 4789 | 2 | 0 | 0 | 1083x398 | `part-2-understanding-llms/module-07-pretraining-scaling-laws/images/fig-6.5.1-sgd-vs-adam.svg` | minor tidy |
| 24 | 6 | 127037 | 3672 | 1 | 0 | 0 | 1023x435 | `part-2-understanding-llms/module-07-pretraining-scaling-laws/images/fig-6.4.3-curation-funnel.svg` | minor tidy |
| 25 | 6 | 113248 | 3391 | 1 | 0 | 0 | 663x429 | `part-2-understanding-llms/module-07-pretraining-scaling-laws/images/fig-6.3.3-chinchilla-vs-kaplan.svg` | minor tidy |
| 26 | 6 | 107983 | 3507 | 3 | 0 | 0 | 780x366 | `part-1-foundations/module-05-decoding-text-generation/images/fig-5.2.4-temperature.svg` | minor tidy |
| 27 | 6 | 106566 | 3282 | 1 | 0 | 0 | 717x386 | `part-4-training-adapting/module-17-synthetic-data/images/fig-14.1.2-annotation-cost.svg` | minor tidy |
| 28 | 6 | 99856 | 3077 | 3 | 0 | 0 | 921x353 | `part-2-understanding-llms/module-07-pretraining-scaling-laws/images/fig-6.3.2-power-law.svg` | minor tidy |
| 29 | 6 | 79662 | 2805 | 1 | 0 | 0 | 674x402 | `part-2-understanding-llms/module-08-modern-llm-landscape/images/fig-7.4.3-multilingual-gap.svg` | minor tidy |
| 30 | 6 | 61636 | 2143 | 1 | 0 | 0 | 643x374 | `part-2-understanding-llms/module-07-pretraining-scaling-laws/images/fig-6.5.2-lr-schedules.svg` | minor tidy |

## Simplified in this pass (11)

Top 10 from the original audit (pre-rewrite) plus one user-flagged extra.
Each was rewritten with <= 8 primary boxes, <= 3-word labels inside boxes,
single directional flow, canvas <= 1100x600. Long explanatory text moved to
figure captions or surrounding prose. Same filename and `<title>`, so existing
`<img src=>` and `<figcaption>` references keep working.

The post-simplification audit table above is freshly regenerated; you can see
the simplified files have dropped (or fallen far) from the leaderboard.

1. `diagram-32-6-1.svg` (user-flagged, multimodal edit taxonomy) - was rank 30 score 7
2. `diagram-32-7-1.svg` (user-flagged, cross-modal embedding) - was rank 16 score 10
3. `diagram-32-4-1.svg` (three world-model paradigms) - was rank 7 score 12
4. `fig-8.1.3-four-reasoning-architectures.svg` - was rank 1 score 16
5. `fig-5.4.3-ar-vs-diffusion.svg` - was rank 2 score 14, now score 6
6. `fig-2.3.4-tokenizer-landscape.svg` - was rank 3 score 14
7. `fig-6.6.4-pipeline.svg` - was rank 5 score 13, now score 8 (grid stays but prose slimmed)
8. `fig-2.1.5-token-artifacts.svg` - was rank 6 score 12
9. `fig-28.13.1-experiment-design-flow.svg` - was rank 8 score 12
10. `fig-2.2.4-unigram.svg` - was rank 9 score 12
11. `fig-30.9.1-eu-ai-act-risk-tiers.svg` - was rank 18 score 10

## Skipped (grid signature is the point)

- `fig-4.1.4-pos-encoding.svg` (positional encoding heatmap grid)
- `fig-9.5.1-2-4-structured-sparsity.svg` (sparsity pattern grid)
- `fig-10.1.2-attention-head-types.svg` (attention matrix signatures)
- `fig-9.2.4-attention-variants.svg` (per-variant grids)

Score 6 entries with 0 rects/texts (rank 23-30 above) are matplotlib-generated
plots, not box diagrams. Their score reflects raw file size, not visual
complexity, so they need a different treatment if revisited.

PNG sidecars to be regenerated by the next build pass.
