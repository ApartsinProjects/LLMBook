# Mermaid Diagram Audit — Highlights

**Scope**: all 168 Mermaid `.mmd` source files in chapters 0-34.
**Method**: automated text analysis of the .mmd structure + label content.
Visual inspection was attempted via parallel sub-agents but the per-session
image limit (2000 px aggregate) was hit at scale; that audit is reserved
for spot-checking the most-defective cases.

**Full report**: `KDP/validation/mermaid_diagram_audit.csv` (168 rows).

## Summary

| Recommended action | Count | What it means |
|---|---|---|
| KEEP | 98 | Hits at least one "useful Mermaid" criterion (architecture, branching, named tools, structured grouping) and has no defects. |
| FIX | 43 | Content is fine but publishing quality flags fired (long labels, too many nodes, edge-bundle). Regenerate with terser labels or split into sub-diagrams. |
| DROP | 19 | Low didactic value: pure step-list / trivial / prose-redundancy. Per the v6.48 Diagram Policy these are candidates to remove. |
| REWORK-AS-Gemini | 5 | Contains metaphor / analogy keywords — would land better as a Gemini illustration. |
| REWORK-AS-matplotlib | 3 | Contains 3+ quantitative tokens (% / GB / tokens-per-sec / etc.) — would land better as a matplotlib chart. |

## Per-axis distribution

| Axis | Value | Count |
|---|---|---|
| A. Didactic value | HIGH | 28 |
|   | MEDIUM | 121 |
|   | LOW | 19 |
| B. Type fit | CORRECT | 160 |
|   | WRONG-should-be-Gemini | 5 |
|   | WRONG-should-be-matplotlib | 3 |
| C. Publishing quality | OK | 113 |
|   | DEFECT | 55 |

## Most actionable items

### REWORK-AS-matplotlib (3 — high-impact, clear case)

These flowcharts contain enough quantitative content that a real chart
would teach more:

- `fig-2.1.3-multilingual-tokens.mmd` — multilingual token-cost
  comparison. Should be a horizontal bar chart of token-per-char by
  language with the cost-multiplier on a secondary axis.
- `fig-32.9.1-tool-orchestration-economy.mmd` — tool-call cost
  breakdown. Should be a stacked-bar / pareto chart of cost components.
- `section-11.3-svg2.mmd` — prompt-optimization score trajectory.
  Should be a simple line chart of score-over-iterations.

### REWORK-AS-Gemini (5 — concept illustrations)

These would benefit from warm-cartoon framing rather than box-and-arrow
formality:

- `fig-32.4.2-world-model-architecture.mmd`
- `fig-34.4-world-model.mmd`
- `fig-18.8.1-rag-ingestion-pipeline.mmd`
- `fig-25.6.1-robot-cloud-edge-hierarchy.mmd`
- `fig-28.9.1-k8s-llm-stack.mmd`

### DROP candidates (19)

These are pure step-lists with no named tools, no numbers, no
branching, and < 9 nodes. Each is essentially the prose drawn as boxes.
Top of the list:

| File | Pattern |
|---|---|
| `fig-0.3.3-comp-graph` | PyTorch autograd graph — but reader sees only "x → MulBackward → AddBackward" |
| `fig-0.3.5-training-loop` | "data → forward → loss → backward → step" — pure prose echo |
| `fig-0.4.2-rl-loop` | < 3 nodes; trivial |
| `fig-1.4.5-elmo-layers` | "layer 0 → layer 1 → layer 2" — replaces prose |
| `fig-3.1.3-vanishing-grad` | Step-by-step gradient flow narration |
| `fig-4.1.9-residual-stream` | < 3 nodes; trivial |
| `fig-4.5.2-complexity` | Sequential complexity-class hierarchy |
| `fig-31.1.3-logit-lens` | "Layer 0 → 4 → 8 → 11" — but: each layer has a concrete prediction (the/France/Paris/Paris) which my heuristic missed. **Re-review before dropping.** |
| `fig-34.1.1-token-to-dollar-pipeline` | "User → App → Tokenizer → API → Billing → Invoice" — but the per-step cost formulas matter. **Re-review.** |

**Caveat**: the auto-classifier weighs my "named-entity" list heavily;
it doesn't recognize all PyTorch / interpretability internals. Two
candidates (`fig-31.1.3-logit-lens` showing concrete model predictions
per layer, and `fig-34.1.1-token-to-dollar-pipeline` showing cost
formulas) are likely false-positives — review the actual image before
dropping. Apply v6.48 Policy criteria: a worked-example with concrete
values DOES carry weight.

### FIX (43 — wrap-risk / cramped)

Mostly captions with > 50 chars per node label — these wrap or clip on
narrow screens. Regenerate with terser labels (split into sub-labels,
move long text to captions). Top offenders:

- `fig-1.1.2-nlp-eras` (4 labels > 50 chars)
- `fig-1.1.6-linguistic-layers` (2)
- `fig-1.3.2-skipgram-network` (2)
- `fig-2.1.2-vocab-spectrum` (2)
- ... plus 39 more in the CSV.

## Next steps

1. **Action the 3 REWORK-AS-matplotlib first** — they're high-impact and
   the existing matplotlib generator pipeline is well-trodden.
2. **Manual review of the 19 DROP candidates** against the v6.48 Diagram
   Policy. Expect 10-12 actual drops; 7-9 false positives where the
   classifier missed structural value.
3. **Action the 5 REWORK-AS-Gemini** when bandwidth allows; less urgent
   than the matplotlib reworks.
4. **Batch the 43 FIX cases** by regenerating Mermaid with terser node
   labels. Use the same `scripts/mermaid/generate_mermaid_diagrams.py`
   pipeline that produced them.

The 98 KEEP figures need no action.
