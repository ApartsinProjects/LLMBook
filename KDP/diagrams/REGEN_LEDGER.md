# Diagram Regeneration Ledger

**Purpose**: Survive session compaction. Any future session can read this file and resume autonomous regeneration without losing context.

**Updated**: 2026-05-10 (sweep COMPLETE)

---

## Current state

- **Total Mermaid figures in book**: 167
- **Redesigned to high-quality SVG**: **168 SVGs in dir** (some figures had multiple variants merged into one canonical SVG)
- **Remaining genuine figures**: 0
- **Status**: ✅ **COMPLETE — 100%**

## Final tally

| Round | Figures | Method | Wallclock |
|---|---|---|---|
| Prior session | 23 | sequential hand-design | several hours |
| Round 4 | 5 | sequential | ~15 min |
| Round 5 (sequential batches) | 24 | sequential | ~60 min |
| Round 1 parallel | 15 | 3 subagents × 5 | ~5 min |
| Round 2 parallel | 15 | 3 subagents × 5 | ~5 min |
| Round 3 parallel | 15 | 3 subagents × 5 | ~5 min |
| Round 4 parallel | 15 | 3 subagents × 5 | ~5 min |
| Round 5 parallel | 15 | 3 subagents × 5 | ~5 min |
| Round 6 parallel | 15 | 3 subagents × 5 | ~5 min |
| Round 7 parallel | 15 | 3 subagents × 5 | ~5 min |
| Round 8 final | 11 | 2 subagents × 5+6 | ~5 min |
| **TOTAL** | **168** | | |

Verifier: 0 errors across all 171 SVGs (24 cosmetic warnings on density / palette interpolation, all expected).

## Last batch: 15 figures via 3 parallel subagents

All 15 verified (0 errors), rasterized, wired into HTML. Backups in `KDP/build/source_fix_backups/diagram_replace_*/`.

### Parallel A — module 0 + 6 (training fundamentals)
- ✅ fig-0.4.4-rl-llm-mapping (RL→RLHF mapping table)
- ✅ fig-6.2.2-clm-mlm (causal vs masked LM, two-lane)
- ✅ fig-6.3.4-scaling-laws (Kaplan vs Chinchilla)
- ✅ fig-6.6.3-ddp (data-parallel sharding + all-reduce)
- ✅ fig-6.6.4-pipeline-parallel (1F1B Gantt schedule)

### Parallel B — module 6 + 7 (data, MoE, reasoning)
- ✅ fig-6.4.3-data-pipeline (100TB→3TB data filtering stages)
- ✅ fig-6.3.7-moe-layer (top-2 routing, 6 experts)
- ✅ fig-7.1.3-reasoning-token-flow (thinking vs answer tokens)
- ✅ bolt-on-vs-native-multimodal (adapter vs unified-token)
- ✅ fig-7.3.2-train-test-scaling (capex vs marginal cost shapes)

### Parallel C — module 4 (transformer internals)
- ✅ fig-4.1.7-residual-stream (highway with attn/FFN read+write)
- ✅ fig-4.3.3-rope (rotation panels at positions 0/3/5)
- ✅ fig-4.3.5-head-behaviors (4 panels: syntactic/local/induction/positional)
- ✅ fig-4.4.2-gpu-memory (inverted pyramid: registers→SMEM→L2→HBM)
- ✅ fig-4.1.2-cross-entropy (H(P) + KL → CE → exp → perplexity)

### Throughput observations
- Sequential batch of 5: ~12-15 min main-agent work
- Parallel 3×5 batch: 15 figures in ~4 min wallclock (subagent design) + 30 sec wiring
- **Speedup ≈ 4×** with parallel-batch protocol

## How to resume in a new session

```bash
# 1. Confirm what's done by listing rendered SVGs
ls "E:/Projects/BookBlogsHome/LLMBook/KDP/diagrams/svg/"*.svg | wc -l

# 2. Read this file's "Done" section to see redesigned figures
# 3. Pick next batch from the "Next up" section below
# 4. For each figure: read .mmd source, design SVG using technical-diagram-designer skill,
#    verify, rasterize, wire to HTML (see "Wiring recipe" below)
```

## Skill usage requirements

Use **technical-diagram-designer** skill at `~/.claude/skills/technical-diagram-designer/`. v1.4.

Key conventions:
- **Canonical palette**: data=`#1a4078`, model=`#1f7a3a`, orchestration=`#722f8a`, store=`#7a5e1a`, warning=`#b3401b`
- **Font sizes**: title 22-28, section 14-18, body 12-13, small 11 (NEVER below 11)
- **R9**: output structured "## Diagram Plan" before SVG (decision-tree branch, pattern, aspect, alternatives, sketch)
- **R10**: pre-flight checks (sub-11px fonts, off-palette colors)
- **Use `chart_helpers.py`** for heatmaps, bar charts, log axes — don't hand-write 100s of `<rect>`

## Wiring recipe (per batch of 5)

```python
import sys, shutil, time
sys.path.insert(0, 'E:/Projects/BookBlogsHome/LLMBook/KDP/build')
from generate_diagram_svg import rasterize_svg
from pathlib import Path

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')
SVG_DIR = ROOT / 'KDP/diagrams/svg'

# 1. Auto-fix: bumps sub-11px fonts, expands hex shortcuts, normalizes black strokes
# Run: python verify_svg.py + auto_fix_svg.py on SVG_DIR

# 2. Rasterize each new SVG
for src_name, dst_rel in BATCH_ITEMS:
    s = SVG_DIR / f'{src_name}.svg'
    rasterize_svg(s, s.with_suffix('.png'), max_width=1400)

# 3. Wire: copy PNG over the in-book filename (preserves <img src=>)
backup = ROOT / f'KDP/build/source_fix_backups/diagram_replace_{time.strftime("%Y%m%d_%H%M%S")}'
for src_name, dst_rel in BATCH_ITEMS:
    sp = SVG_DIR / f'{src_name}.png'
    dp = ROOT / f'{dst_rel}.png'
    if dp.exists():
        b = backup / f'{dst_rel}.png'
        b.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dp, b)
    shutil.copy2(sp, dp)
    shutil.copy2(SVG_DIR / f'{src_name}.svg', ROOT / f'{dst_rel}.svg')
```

---

## Done (52 figures)

### Prior sessions (23)
- fig-16.1.3-lora-decomposition, fig-17.1.2a-rlhf-ppo-step, fig-17.1.2b-rlhf-three-stage
- fig-19.4.2-explainability-2d, fig-2.2-bpe-overview, fig-21.1.3-rag-pipeline
- fig-21.3.4-graphrag-pipeline, fig-28.1.3-ddpm-process, fig-4.2.2-decoder-only_v1
- fig-4.5.2-complexity, fig-6.1.2-encoder-timeline, fig-6.1.4-param-growth
- fig-8.1.2-perf-vs-compute, fig-8.1.3-four-reasoning-architectures
- fig-8.5.1-compute-optimal-frontier, section-10.3-fallback-staircase
- section-10.5-compression-pipeline, section-11.2-prompting-strategy-decision
- section-11.2-tree-of-thoughts, fig-2.1.3-multilingual-tokens
- fig-4.1.4-pos-encoding-heatmap (later regenerated via codegen)
- section-11.1-prompt-anatomy, fig-1.4-evolution-timeline

### Batch 4 (5)
- fig-4.1.4-pos-encoding-heatmap (regenerated true PE values)
- fig-0.1.2-gradient-descent
- fig-0.1.4-bias-variance
- fig-0.2.2-perceptron

### Batch 5 (4)
- fig-0.2.4-backprop, fig-0.3.3-comp-graph, fig-0.3.5-training-loop, fig-0.4.2-rl-loop

### Batch 6 (5)
- fig-1.1.2-nlp-eras, fig-1.2.1-nlp-pipeline, fig-1.3.1-skipgram, fig-1.3.5-cosine-sim, fig-1.4.2-static-contextual

### Batch 7 (5)
- fig-3.3.2-scaled-dot-product, fig-3.3.3-multi-head, fig-2.1.2-vocab-spectrum, fig-3.1.3-vanishing-grad, fig-3.1.6-seq2seq

### Batch 8 (5)
- fig-4.1.8-causal-mask, fig-4.4.3-flash-attention, fig-5.1.3-beam-search, fig-5.2.3-top-p-sampling, fig-5.3.3-speculative

### Batch 9 (5)
- fig-9.2.3-continuous-batching, fig-11.2.4-function-calling-loop, fig-11.1.5-api-request-response, fig-9.4.3-prefill-decode, fig-11.2.2-structured-output-levels

### Batch 10 (5)
- fig-20.2-advanced-rag-paradigms, fig-21.8.1-rag-ingestion-pipeline, fig-23.4.1-tiered-reasoning, memory-taxonomy-five-layers, agent-execution-loop

---

## Next up — Tier B priority queue

Pick 5 from this ordered list per batch. Cross out as completed.

### Module 0 (foundations) — remaining
- [ ] fig-0.4.4-how-rl-concepts-map-to-llm-training (RL-to-LLM mapping)

### Module 1-3 (NLP, sequences) — remaining
- [ ] fig-1.1.4-nlp-tasks, fig-1.1.6-linguistic-layers, fig-1.2.2-stem-lemma, fig-1.2.3-bow-matrix, fig-1.2.4-tfidf
- [ ] fig-1.3.6-fasttext-subword, fig-1.4.3-elmo
- [ ] fig-2.1.5-token-artifacts, fig-2.2.4-unigram, fig-2.2.5-byte-bpe, fig-2.3.2-chat-template, fig-2.3.3-multimodal-tokens, fig-2.3.4-tokenizer-landscape
- [ ] fig-3.1.5-lstm-cell, fig-3.2.4-gradient-attention

### Module 4 (transformers) — remaining
- [ ] fig-4.1.2-cross-entropy, fig-4.1.7-pre-post-ln, fig-4.1.7-residual-stream, fig-4.1.9-residual-stream
- [ ] fig-4.3-s4-three-views, fig-4.3.2-three-families, fig-4.3.3-rope, fig-4.3.4-pos-strategies, fig-4.3.5-head-behaviors, fig-4.3.6-pre-post-ln2
- [ ] fig-4.4.2-gpu-memory

### Module 5 (decoding) — remaining
- [ ] fig-5.1.2-greedy, fig-5.3.2-contrastive, fig-5.4.2-diffusion

### Module 6 (model design) — all remaining
- [ ] All `module-06-*` figures (4 total)

### Module 7-8 — all remaining
- [ ] All `module-07-*` and `module-08-*` figures (~15 total)

### Module 9 (inference opt) — remaining
- [ ] fig-9.1.2-quantization-granularity, fig-9.1.3-gptq, fig-9.2.2-pagedattention
- [ ] fig-9.2.4-mha-mqa-gqa, fig-9.2.5-radixattention, fig-9.3.2-speculative
- [ ] fig-9.3.3-tree-verification, fig-9.4.2-serving-stack, fig-9.5.1-2-4-sparsity

### Module 11-11 (APIs, prompting) — remaining
- [ ] fig-11.1.2-llm-api-ecosystem, fig-12.6.1-dspy-optimization-loop
- [ ] section-11.1-svg1, svg2; section-11.2-svg1, svg2, svg3; section-11.3-svg1, svg2, svg3

### Module 13-19 — many remaining
See `KDP/build/_remaining_diagrams.txt` for the full list grouped by part.

### Tier D (appendices) — leave Mermaid OR bulk-normalize
- [ ] LangChain / LlamaIndex appendix figures (~10) — low ROI, current Mermaid is acceptable

---

## Parallel-batch protocol

To run N=3 batches in parallel via subagents:

1. Main agent picks 15 figures from "Next up" (split into 3 groups of 5)
2. Spawn 3 subagents in parallel, each with self-contained brief:
   - Skill location: `~/.claude/skills/technical-diagram-designer/`
   - List of 5 .mmd source paths to read
   - Output: 5 SVG files in `KDP/diagrams/svg/`
   - Quality bar: must pass `verify_svg.py` (0 errors)
3. Wait for all 3 to complete
4. Main agent runs auto_fix + rasterize + HTML wire (sequential, 1-2 min)
5. Update this ledger: cross off completed, mark batch done

Subagent brief template stored at: `KDP/diagrams/_subagent_brief.md` (TODO: write this)
