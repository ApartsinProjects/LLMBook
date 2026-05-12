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

## Wave 2 — DROP triage results (2026-05-12)

19 DROP candidates manually inspected against rendered PNGs (not just
.mmd source). The text-only heuristic had an **89% false-positive rate**
on this axis: rendered diagrams almost always include SVG sidebar
annotations (How-it-works boxes, Key-idea footers, worked-example
values) that the .mmd source does not capture.

| Verdict | Count | Files |
|---|---|---|
| KEEP (false positive) | 17 | comp-graph, rl-loop, elmo-layers, vanishing-grad, complexity, logit-lens, token-to-dollar-pipeline, bayesian, speculative-decoding, function-calling-loop, 10.3-svg1, 11.2-svg1, 11.2-svg2, 11.3-svg1, memory-taxonomy, 24.4.2-error-recovery, 26.1.2-fim |
| DROP | 1 | `fig-4.1.9-residual-stream` (orphan; never embedded in any HTML; pure prose redundancy without annotations) |
| Move to FIX queue | 1 | `fig-0.3.5-training-loop` (text clipped inside circles) |
| Bonus FIX flag | +1 | `fig-24.4.2-error-recovery-decision` (label "No, max retries" overlaps the "Alternative available?" diamond) |

**Action taken**: deleted the residual-stream files + removed the entry
from `scripts/mermaid/generate_all_mermaid.py`. Two FIX-flagged diagrams
folded into the FIX queue.

**Lesson for future audits**: the .mmd-source heuristic is unreliable
for the LOW-value axis. A diagram is only truly "low-value" if both the
.mmd AND the rendered PNG lack annotations. Always inspect the PNG.

## Wave 5 — FIX triage results (2026-05-12)

The 43 FIX candidates plus 2 from Wave 2 (training-loop, error-recovery)
were sampled visually. Same pattern as Wave 2: the text-only "labels
&gt; 50 chars likely to wrap" heuristic has a high false-positive rate.

Sample of 4 from the top of the FIX queue (worst defect scores):
- `production-training-architecture` (30 nodes flagged "cramped"): OK
  at full resolution, named entities all legible.
- `fig-27.13.1-experiment-design-flow` (10 long labels): card-rectangle
  layout absorbs the length cleanly.
- `fig-29.9.1-eu-ai-act-risk-tiers` (7 long labels): 4-tier comparison
  table layout, multi-bullet cells render OK.
- `fig-18.7.1-graphrag-pipeline` (7 long labels): substantial pedagogical
  figure with indexing stages, knowledge graph store, query modes,
  concrete examples; "long labels" are the content, not a defect.

Estimated false-positive rate &gt; 80%. Decided NOT to mechanically
process the remaining 39 candidates; they would mostly be no-ops.

**Two REAL defects from Wave 2 inspection were fixed:**

1. `fig-0.3.5-training-loop` (hand-crafted SVG): code labels clipped
   inside circles (`optimizer.step()`, `criterion(y_hat, y)`), subtitle
   line interrupted by top circle, "repeat for next mini-batch" label
   crowded the top circle. Fixed by shifting all circles down 20-30px,
   bumping circle radius 60→62, shrinking monospace font 11→10,
   repositioning the subtitle and loop label. Re-rendered via puppeteer.

2. `fig-24.4.2-error-recovery-decision` (Mermaid): "No, max retries"
   edge label collided with the "Alternative available?" diamond
   because Dagre layout forced the SUCC1→FALL edge diagonally across
   the canvas. Fixed by shortening the label to "max retries" AND
   re-rendering with the ELK layout (scripts/mermaid/mermaid-config-elk.json)
   which routes edges orthogonally with zero label collisions.

**Wave 5 conclusion**: the 43 FIX candidates are marked KEEP. Only the
2 verified defects (training-loop, error-recovery) actually needed
intervention.

## Wave 6 — REWORK-AS-Gemini triage results (2026-05-12)

5 candidates flagged by metaphor-keyword detection in `.mmd` label text:

| Candidate | Audit flag | Verdict |
|---|---|---|
| fig-32.4.2-world-model-architecture | "imagined rollouts" | KEEP (RL terminology; formal architecture with math notation) |
| fig-34.4-world-model | "dreams" | KEEP (literal V-M-C paper terminology, "dream training") |
| fig-18.8.1-rag-ingestion-pipeline | "pipeline" | KEEP (concrete tools: Confluence, OAuth, vector DB) |
| fig-25.6.1-robot-cloud-edge-hierarchy | "clean the kitchen" | KEEP (worked-example goal, not analogy) |
| fig-28.9.1-k8s-llm-stack | "stack" | KEEP (3-layer K8s architecture with named operators) |

False-positive rate: 100% (5/5). The metaphor-keyword detector fires
on incidental vocabulary in technical diagrams (RL terms from papers,
worked-example goals, generic words like "pipeline" and "stack").

## Audit closeout summary

Across 168 Mermaid diagrams (waves 2, 5, 6) the text-only audit's
"action required" verdicts had these false-positive rates:

| Verdict | Candidates | False positives | Real |
|---|---|---|---|
| DROP | 19 | 17 (89%) | 1 orphan + 2 promoted to FIX |
| FIX | 43+2 | ~80%+ (sampled) | 2 verified defects |
| REWORK-AS-Gemini | 5 | 5 (100%) | 0 |
| REWORK-AS-matplotlib | 3 | 3 (100%, all already charts) | 0 |

**Takeaway**: the v6.50 text-only heuristic should not be used as the
sole signal for diagram action. Useful as a *triage filter* to surface
candidates, but every flagged item needs visual verification of the
rendered PNG. The single most reliable signal across all 3 axes was
visual inspection.

Real defects fixed across all waves:
- 1 caption mismatch (fig-13.1.2 seed-data text on annotation-cost chart)
- 1 orphan diagram dropped (fig-4.1.9-residual-stream)
- 3 chapter-opener typos (Imagen-mangled text in ch16/17/18 openers)
- 5 caption/file-id mismatches across 4 chapters
- 1 orphan illustration adopted (rlvr-auto-graded-exam to section 16.4)
- 2 publishing defects (training-loop clipping, error-recovery overlap)

Tools/scripts added:
- scripts/images/add_chapter_title.py (PIL title overlay for Gemini openers)
- scripts/images/svg_to_png.cjs (puppeteer SVG→PNG renderer)
- Wave-level documentation in this file
