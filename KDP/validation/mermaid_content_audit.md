# Mermaid Figure Content Audit

**Scope:** All 167 `*.mmd` Mermaid sources under `part-*/` and `appendices/` of *Building Conversational AI with LLMs and Agents*.
**Focus:** Didactic value, informativeness, layout choice, technical correctness, label clarity. (NOT visual style/CSS.)
**Method:** For each figure, the `.mmd` source was read together with the surrounding HTML (caption + preceding paragraph + section title) and scored on five dimensions, 1-5 each (max 25). Figures grouped by recurring patterns to keep the report skim-able.

---

## Section 1. Executive summary

**Audited:** 167 Mermaid figures. 130 are referenced from a published `section-N.M.html`; **25 are orphans** (`.mmd` exists but never embedded in any HTML, only in the `md/` markdown sources). 12 of the 167 are obvious **near-duplicates** (the same diagram authored twice with slightly different labels - see Section 4.4).

**Diagram-type distribution:** **167 / 167 = 100% are `flowchart`.** Not a single `sequenceDiagram`, `classDiagram`, `stateDiagram`, `gantt`, `timeline`, `pie`, `quadrantChart`, `xychart-beta`, or `erDiagram` is used anywhere in the book. This is the single most important finding of the audit: the book treats Mermaid as a synonym for "flowchart with rounded boxes," and many concepts that would be served by other layouts (sequences of API calls, timelines of model releases, performance curves, comparison matrices, state machines, hierarchies) are forced into a left-to-right or top-to-bottom box-and-arrow shape. See Section 4 for the systemic recommendation.

**Category distribution (by total score):**

| Category | Count | % | Description |
|---|---|---|---|
| KEEP (22-25) | 28 | 17% | Strong figure, only visual polish needed |
| MINOR (18-21) | 71 | 42% | Solid concept, fix labels / tighten boxes |
| MAJOR (13-17) | 53 | 32% | Restructure: split panels, change layout, add detail |
| REPLACE (<=12) | 15 | 9% | Wrong diagram type or vacuous content; redesign |

**Top 5 worst offenders (full redesign needed):**

1. `part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.1.4-param-growth.mmd` - "exponential growth in model parameters" rendered as a 4-node flowchart. **This must be a log-scale line chart**, not a flowchart. The layout actively hides the exponential growth that is the entire point.
2. `part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.1.2-encoder-timeline.mmd` - timeline (BERT 2018 -> ModernBERT 2024) drawn as 5 boxes connected by arrows. **Use a horizontal timeline / `gantt`-style figure**; the temporal axis is invisible in the current rendering.
3. `part-3-working-with-llms/module-12-prompt-engineering/images/section-11.2-svg2.mmd` - "Tree of Thoughts" rendered as a single linear chain of 6 nodes ("N0 --> N1 --> N2 --> N3 --> N4 --> N5"). **A tree-of-thoughts figure that is not a tree is a contradiction.** Tree structure with branching, scores, and pruned branches is mandatory.
4. `part-3-working-with-llms/module-12-prompt-engineering/images/section-11.2-svg3.mmd` - "Decision flowchart for prompting techniques" implemented as a single linear chain N0 -> N1 -> ... -> N12 with all branches collapsed. Loses every "Yes/No" branch that defines a decision tree.
5. `part-2-understanding-llms/module-08-reasoning-test-time-compute/images/fig-8.1.2-performance-as-a-function-of-total-compute.mmd` - claims to show "performance as a function of total compute under three scaling strategies" but is three textual boxes labelled "Train-time", "Test-time", "Combined" with no axes, no curves, no comparison. Caption promises a chart; figure delivers a glossary.

**Top 5 templates worth emulating:**

1. `part-1-foundations/module-00-ml-pytorch-foundations/images/fig-0.2.2-perceptron.mmd` - perfect anatomical diagram: inputs, weights labeled on edges, summation, bias, activation, output. Each box self-explanatory; the math `z = Σwx + b` lives on the arrow where it belongs.
2. `part-1-foundations/module-03-sequence-models-attention/images/fig-3.3.2-scaled-dot-product.mmd` - faithful reproduction of the canonical Vaswani 2017 attention block, with tensor shapes `(n, dk)`, `(m, dv)` annotated on every node. This is what every architecture diagram in the book should look like.
3. `part-2-understanding-llms/module-09-inference-optimization/images/fig-9.2.4-three-attention-variants.mmd` - clean 3-panel comparison of MHA / MQA / GQA with consistent fields ("Q heads", "K/V heads", "KV cache size") in each panel. Readers can scan vertically to compare.
4. `part-1-foundations/module-00-ml-pytorch-foundations/images/fig-0.4.2-rl-loop.mmd` - the dog/LLM dual analogy on the same nodes is a brilliant pedagogical move; concrete and abstract on one canvas.
5. `part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.3.7-moe-layer.mmd` - 6 experts, top-2 routing, weights shown (`w=0.62`, `w=0.38`), skipped experts marked greyed, weighted-sum summation explicit. Concept comes through cleanly.

**Patterns observed:**

- **Module 0-5 (Part 1 Foundations) and Module 9 (Inference Optimization)** are the strongest: figures are anatomically correct, labels carry mathematical meaning, multi-panel comparisons use parallel structure.
- **Module 12 (Prompt Engineering) `section-11.2-*` and `section-11.3-*` figures** are the worst sub-cluster in the book - generic linear chains of `N0 -> N1 -> ... -> Nk` boxes with prose stuffed inside `<b>` tags. They appear to be auto-generated from text and never edited. 9 of the worst-15 figures are in this module.
- **Module 6, 7, 8** (Pretraining / Modern Landscape / Reasoning) repeatedly use flowcharts where time-series, log-scale charts, or tables would communicate better.
- **Architecture diagrams** (LSTM cell, MoE block, transformer block, RWKV/Mamba) are generally good but inconsistently include tensor shapes; only Module 3-4 figures annotate dimensions like `(n, d_model)`. Reader cannot reconstruct what flows through the wires in many later figures.
- **Decision trees and trees in general** are systematically mis-rendered as linear flows; the book lacks any true branching tree figure despite multiple opportunities (Tree of Thoughts, MCTS, decision flowcharts, taxonomy trees).
- **Comparison figures** (e.g., GPTQ vs AWQ, Kaplan vs Chinchilla) consistently use two adjacent subgraphs with bullet lists inside. This works but is often equivalent to a 2-column table; pick one mode and stick to it.
- **25 orphan `.mmd` files** are not embedded in any built HTML page. Either delete them or wire them in. Several appear to be earlier drafts later replaced (`fig-3.1.6-seq2seq.mmd` vs `fig-3.1.6-the-encoder-decoder-seq2seq...mmd`; `fig-1.1.2-nlp-eras.mmd`; `fig-4.3-s4-three-views.mmd`; etc.).

**Verdict:** Roughly **41% of the book's Mermaid figures are publication-ready or close to it**, but **the remaining 59% need at least label cleanup, and ~9% are fundamentally the wrong diagram type and require redesign with a different chart concept** (line chart, true tree, sequence diagram, timeline, table). The single highest-leverage intervention is to **stop using flowchart for everything that isn't a flow** and adopt 3-4 additional Mermaid diagram types (timeline, sequenceDiagram, branching trees, xychart-beta) where the concept demands them.

---

## Section 2. Per-chapter summary table

Mean scores below are out of 25.

| Module | Figs | Mean | KEEP | MINOR | MAJOR | REPLACE | Verdict |
|---|---|---|---|---|---|---|---|
| `appendix-l-langchain` | 7 | 17.6 | 0 | 5 | 2 | 0 | Solid simple architecture flows; near-duplicate `*.mmd` and `section-l.X-svg1.mmd` versions of same diagram should be deduped. |
| `appendix-o-llamaindex` | 3 | 16.3 | 0 | 2 | 1 | 0 | Ingestion pipeline reads well; index-comparison figure (`section-o.2-svg1`) needs labels for *what* makes each index different beyond two bullets per box. |
| `module-00-ml-pytorch` | 8 | 21.6 | 4 | 4 | 0 | 0 | Strongest module in the book. Perceptron, RL loop, training loop, RLHF mapping all near-template quality. |
| `module-01-foundations-nlp` | 15 | 18.7 | 1 | 9 | 4 | 1 | Mostly informative; `nlp-eras` should be a timeline; `nlp-tasks` is a thin classification with no detail; `bow-matrix` text-as-grid is a workaround for a real table. |
| `module-02-tokenization` | 9 | 18.4 | 1 | 5 | 3 | 0 | Byte-BPE figure (`fig-2.2.5-byte-level-bpe...`) is excellent; `multilingual-tokens` would benefit from a real bar chart. |
| `module-03-sequence-models-attention` | 8 | 19.5 | 2 | 5 | 1 | 0 | RNN/LSTM/seq2seq/attention all decently labeled; `vanishing-grad` is a glossary box with arrow rather than a curve. |
| `module-04-transformer-architecture` | 16 | 18.1 | 2 | 9 | 4 | 1 | Mixed: scaled dot-product, MHA, decoder-only block all good. `pos-encoding` and `causal-mask` figures use boxes to imitate heatmaps - real heatmap visuals needed. `fig-4.5.2-complexity` (TC0/NC1/AC0 hierarchy) is a single line of 4 boxes; should be a Venn or a containment hierarchy. |
| `module-05-decoding-text-generation` | 8 | 19.0 | 1 | 6 | 1 | 0 | `greedy` and `beam-search` figures are conceptually right but should show probability scores graphically (bars). `top-p-sampling` text values would benefit from grouped bar chart. |
| `module-06-pretraining-scaling-laws` | 14 | 16.3 | 1 | 6 | 5 | 2 | Several "timeline" and "growth" figures need to become real charts (`fig-6.1.2-encoder-timeline`, `fig-6.1.4-param-growth`, `fig-6.5.3-grokking`). MoE and DDP figures are good. |
| `module-07-modern-llm-landscape` | 11 | 16.9 | 1 | 5 | 4 | 1 | `frontier-ecosystem` (TIER 1/TIER 2 boxes) is essentially a table; `multilingual-performance-gap` should be a bar chart. Native-vs-bolt-on multimodal duplicates exist. |
| `module-08-reasoning-test-time-compute` | 5 | 15.0 | 0 | 2 | 2 | 1 | `fig-8.1.2-perf-vs-compute` and `fig-8.5.1-compute-optimal-frontier` both promise plots in caption; deliver bullet lists. Decision flowchart (`fig-8.4.1`) is one of only two correct decision-tree figures in the book. |
| `module-09-inference-optimization` | 11 | 19.4 | 3 | 6 | 2 | 0 | Together with module 0, the best technical-detail module. Figures actually visualize tradeoffs (PagedAttention, GQA, RadixAttention) rather than restating prose. |
| `module-19-interpretability` | 8 | 17.5 | 0 | 5 | 3 | 0 | Solid debugging-workflow figure (`fig-18.3.2`); `attention head types` is a flat 4-box list and could include mini-heatmap glyphs. `fig-18.4.2` "explanation methods on faithfulness vs cost" should be a 2-D scatter, not a chain. |
| `module-11-llm-apis` | 6 | 17.7 | 1 | 3 | 1 | 1 | `fig-11.1.5-request-response` is excellent. `section-10.3-svg1` and `section-10.5-svg1` are linear chains of 5 boxes that hide a clearly-tiered relationship. |
| `module-12-prompt-engineering` | 9 | 12.9 | 0 | 1 | 2 | 6 | **Worst module in the book.** All `section-11.2-*` and `section-11.3-*` figures are auto-generated linear chains. Tree of Thoughts is not a tree; decision flow is not branching; self-refine loop is fine but trivial. |
| `module-13-hybrid-ml-llm` | 1 | 20.0 | 0 | 1 | 0 | 0 | Refinery metaphor works well. |
| `module-16-peft` | 1 | 22.0 | 1 | 0 | 0 | 0 | Genuine decision tree for PEFT method choice; one of the best decision figures. |
| `module-21-rag` | 4 | 19.5 | 1 | 3 | 0 | 0 | Naive vs Advanced vs Modular RAG and GraphRAG figures are well-structured. |
| `module-22-conversational-ai` | 1 | 20.0 | 0 | 1 | 0 | 0 | Voice agent vs voice pipeline comparison is clear. |
| `module-23-ai-agents` | 2 | 21.0 | 1 | 1 | 0 | 0 | Tiered reasoning routing and 5-layer memory taxonomy are useful. |
| `module-26-specialized-agents` | 1 | 20.0 | 0 | 1 | 0 | 0 | Coding agent generations would be even better as a timeline. |
| `module-27-agent-safety-production` | 1 | 21.0 | 1 | 0 | 0 | 0 | Error recovery decision tree is an actual tree. |
| `module-29-llm-applications` | 1 | 14.0 | 0 | 0 | 1 | 0 | FIM diagram has only 4 nodes and obscures the key idea (`<PRE> prefix <SUF> suffix <MID>` token format). |
| `module-30-evaluation-observability` | 1 | 21.0 | 1 | 0 | 0 | 0 | Four-phase experiment design is well-structured. |
| `module-31-observability-monitoring` | 1 | 21.0 | 1 | 0 | 0 | 0 | OTel trace structure with attribute schemas is concrete and useful. |
| `module-10-production-engineering` | 5 | 19.0 | 1 | 3 | 1 | 0 | Saga compensation, durable execution recovery, retry taxonomy all readable. K8s stack figure is slightly busy but informative. |
| `module-33-safety-ethics-regulation` | 2 | 19.5 | 0 | 2 | 0 | 0 | Risk pyramid claim doesn't match implementation (linear chain) - could become a real triangle. |
| `module-34-strategy-product-roi` | 1 | 18.0 | 0 | 1 | 0 | 0 | Enterprise auth flow is reasonable; would be better as a sequence diagram. |
| `module-35-emerging-architectures` | 6 | 17.5 | 1 | 4 | 1 | 0 | Mamba/RWKV block diagrams are detailed; world-model figure is busy but accurate. Mostly orphans (not in HTML). |

---

## Section 3. Worst-50 detailed list (MAJOR + REPLACE)

Score columns: D=Didactic, I=Informativeness, V=Visualization choice, T=Technical correctness, L=Labels, **Σ**=Total.

### 3.1 REPLACE (15 figures, score ≤12) - need redesign with different concept

#### F1. `part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.1.4-param-growth.mmd`
- **Caption:** "Figure 6.1.4: The exponential growth in model parameters from GPT-1 to GPT-4, alongside BERT and T5 for reference."
- **Scores:** D=2 I=2 V=1 T=4 L=2 → **Σ=11**
- **Why:** A flowchart with arrows GPT-1 → GPT-2 → GPT-3 → GPT-4 hides exponential growth - the entire pedagogical point. Reference points (BERT, T5) appear as a separate disconnected subgraph instead of being plotted on the same axis.
- **Recommendation:** Replace with `xychart-beta` (or matplotlib SVG) - x-axis = release year, y-axis = parameter count (log scale), points labeled with model name. BERT 340M, T5 11B, GPT-1 117M, GPT-2 1.5B, GPT-3 175B - the visual slope IS the lesson.

#### F2. `part-2-understanding-llms/module-06-pretraining-scaling-laws/images/fig-6.1.2-encoder-timeline.mmd`
- **Caption:** "Figure 6.1.2: Timeline of encoder-only model evolution, showing key innovations at each step."
- **Scores:** D=3 I=3 V=1 T=4 L=3 → **Σ=14** (borderline MAJOR/REPLACE; counted as REPLACE for visualization choice)
- **Why:** A "timeline" with no time axis. Five boxes (BERT 2018 → RoBERTa 2019 → DeBERTa 2020 → DeBERTa V3 2021 → ModernBERT 2024) connected by arrows is a chronology disguised as a flow.
- **Recommendation:** Use Mermaid `timeline` syntax or a horizontal Gantt-like SVG with year axis. Place innovations as labels under each year tick.

#### F3-F4. `part-3-working-with-llms/module-12-prompt-engineering/images/section-11.2-svg2.mmd` (Tree of Thoughts) and `section-11.2-svg3.mmd` (decision flowchart)
- **Captions:** missing in HTML (orphans).
- **Scores:** ToT - D=2 I=2 V=1 T=2 L=1 → **Σ=8**. Decision flow - D=2 I=2 V=1 T=3 L=1 → **Σ=9**.
- **Why:** The Tree of Thoughts mmd is a single chain `N0 → N1 → N2 → N3 → N4 → N5`. There is literally no branching, so it cannot illustrate tree search. The "decision flowchart" likewise collapses Yes/No branches into a single line and stuffs both branch labels into adjacent prose nodes.
- **Recommendation:** Author both as actual `flowchart TD` with branching: ToT needs a root → 3 children → 9 grandchildren with score annotations and pruned-branch styling. Decision flowchart needs `Q1{...} -->|"Yes"| ...` with multiple terminal nodes (zero-shot, CoT, ReAct, self-consistency, step-back, reasoning-model). Compare with the one good decision tree in the book: `module-16-peft/images/peft-decision-flowchart.mmd`, and copy its structure.

#### F5-F8. Remaining `module-12-prompt-engineering/images/section-11.*-svg*.mmd` orphans (6 files: 11.1-svg1, 11.1-svg2, 11.2-svg1, 11.3-svg1, 11.3-svg2, 11.3-svg3)
- **Captions:** all missing (orphans, not embedded in HTML).
- **Scores:** all in 8-12 range.
- **Why:** Every one is a flat linear chain of `N0 → N1 → ... → Nk` boxes, with prose paragraphs encoded as bold + italic text *inside* boxes. They are essentially text rendered as boxes. They lack any visual structure that adds information beyond the surrounding paragraph.
- **Recommendation:** Each needs to be rewritten with a real diagram concept:
  - `11.1-svg1` (system message anatomy) → 2-column table or a labeled-template snippet, not a graph
  - `11.1-svg2` (5-component prompt structure) → a numbered vertical layout with each component as a labeled section, like an annotated form
  - `11.2-svg1` (Direct vs CoT) → 2-panel comparison with the math worked out side-by-side
  - `11.3-svg1` (self-refine loop) → simple 3-node cycle with feedback arrow (current structure is fine; just shorten labels)
  - `11.3-svg2` (model chaining pipeline) → already has subgraphs; salvageable as MAJOR fix
  - `11.3-svg3` (optimizer LLM history) → table of (prompt version, score) rows, NOT a chain

#### F9. `part-3-working-with-llms/module-11-llm-apis/images/section-10.3-svg1.mmd`
- **Orphan.** Five-level fallback chain rendered as `N0 → N1 → N2 → N3 → N4 → N5`.
- **Scores:** D=2 I=3 V=2 T=4 L=2 → **Σ=13** (REPLACE bordering on MAJOR).
- **Recommendation:** This is a tiered degradation hierarchy, not a sequence. Use a vertical bar with color gradient (best UX → worst UX) and arrows showing fallback transitions only when an upper tier fails. Or render as a numbered table with columns `Level | Trigger | UX Cost | Latency`.

#### F10. `part-3-working-with-llms/module-11-llm-apis/images/section-10.5-svg1.mmd`
- **Orphan.** "Dense → Prune → Quantize → Distill" pipeline.
- **Scores:** D=3 I=3 V=2 T=4 L=2 → **Σ=14**.
- **Recommendation:** Could become a horizontal stacked-bar chart showing memory at each stage (140 GB → 70 GB → 18 GB → recovered) so the compression is *visible*, not just stated.

#### F11. `part-2-understanding-llms/module-08-reasoning-test-time-compute/images/fig-8.1.2-performance-as-a-function-of-total-compute...mmd`
- **Caption:** "Performance as a function of total compute under three scaling strategies. ... test-time scaling (green) achieves higher accuracy per FLOP than simply using a larger model (purple)."
- **Scores:** D=3 I=2 V=1 T=4 L=2 → **Σ=12**.
- **Why:** Caption explicitly describes a chart with curves and crossover points; figure is three text boxes labeled "Train-time / Test-time / Combined" with arrows pointing at a NOTE. Readers cannot see the crossover.
- **Recommendation:** Replace with `xychart-beta` (line chart) - x = total FLOPs (log), y = accuracy, three curves. Mark crossover point. Use matplotlib if Mermaid xychart's styling is too limited.

#### F12. `part-2-understanding-llms/module-08-reasoning-test-time-compute/images/fig-8.5.1-compute-optimal-inference-frontier...mmd`
- **Caption:** "Compute-optimal inference frontier. On easy tasks (green), larger models are optimal. On hard tasks (red), smaller models with test-time compute scaling cross over and outperform larger models at matched total FLOPs."
- **Scores:** D=2 I=2 V=1 T=4 L=2 → **Σ=11**.
- **Why:** Same problem as F11 - caption describes a frontier curve with a crossover; figure is two text boxes plus a NOTE. The "frontier" is invisible.
- **Recommendation:** Same as F11 - real chart.

#### F13. `part-2-understanding-llms/module-08-reasoning-test-time-compute/images/fig-8.1.3-four-major-reasoning-architecture-approaches.mmd`
- **Caption:** "Four major reasoning architecture approaches compared..."
- **Scores:** D=2 I=2 V=2 T=4 L=2 → **Σ=12**.
- **Why:** Four approaches (Extended CoT, Hidden Thinking, Verifier-Guided, Tree Search) shown as a single linear chain `COT → HIDDEN → VERIFY → SEARCH`. The arrow direction implies progression, but they are distinct architectural choices, not stages.
- **Recommendation:** Render as a 2x2 matrix or a 4-quadrant layout indexed by (visible vs hidden reasoning) x (single-pass vs multi-sample). Or as 4 parallel side-by-side panels (no arrows) with a comparison row of properties beneath each.

#### F14. `part-1-foundations/module-04-transformer-architecture/images/fig-4.5.2-complexity.mmd`
- **Caption:** "The complexity class hierarchy. Fixed-depth Transformers with log-precision arithmetic correspond to TC^0..."
- **Scores:** D=3 I=2 V=2 T=4 L=2 → **Σ=13**.
- **Why:** P, NC1, TC0, AC0 rendered as a linear chain `P --- NC1 --- TC0 --- AC0`. This is a *containment* hierarchy (AC0 ⊆ TC0 ⊆ NC1 ⊆ P), not a sequence.
- **Recommendation:** Render as nested concentric boxes (Russian doll), or as a Venn-style containment with each class as a box inside the next, labels on the borders. The hierarchy IS the lesson.

#### F15. `part-2-understanding-llms/module-19-interpretability/images/fig-19.4.2-approximate-positioning-of-explanation-methods-on-faithfulness-vs-cost.mmd`
- **Caption:** "Approximate positioning of explanation methods on faithfulness vs. computational cost."
- **Scores:** D=2 I=2 V=1 T=4 L=2 → **Σ=11**.
- **Why:** Caption explicitly describes a 2-D scatter ("faithfulness vs cost"). Figure is a 1-D linear chain `RA → RO → GA → IG → LRP → SHAP` ordered by cost only. Faithfulness axis is invisible.
- **Recommendation:** Use `quadrantChart` (Mermaid supports this) or a matplotlib scatter with x = cost, y = faithfulness, 6 labeled points.

### 3.2 MAJOR (53 figures, score 13-17) - restructure but keep concept

These are grouped by recurring problem pattern; per-figure recommendations follow.

#### Group A: "Timeline rendered as flowchart" (8 figures)
Pattern: an evolution / chronology / generation sequence drawn as boxes-with-arrows. The reader can read the years from box labels but cannot see the time axis.

| File | Caption fragment | Σ | Recommended fix |
|---|---|---|---|
| `module-01-foundations-nlp/images/fig-1.4-evolution.mmd` | "evolution of text representation" | 16 | Use Mermaid `timeline` with eras (BoW/TF-IDF, Word2Vec, ELMo, Transformers) and put the "what it solved" annotation under each era. |
| `module-01/images/fig-1.1.2-nlp-eras.mmd` (orphan) | NLP eras 1950s-Present | 14 | Same: timeline with 4 eras. |
| `module-26-specialized-agents/images/fig-26.7.1-coding-agent-generations.mmd` | "Four generations of AI-assisted coding" | 17 | Timeline with year ranges 2021-22, 2023, 2024, 2025+. Already labels years in box titles - move them to the axis. |
| `module-06/images/fig-6.1.2-encoder-timeline.mmd` | encoder timeline | 14 | (REPLACE; see F2) |
| `module-06/images/fig-6.1.4-param-growth.mmd` | parameter growth | 11 | (REPLACE; see F1) |
| `module-08/images/fig-8.1.3-four-reasoning-architectures.mmd` | four arch. approaches | 12 | (REPLACE; see F13) |
| `module-07/images/fig-7.2.1-deepseek-v3.mmd` | "Four key architectural innovations" | 16 | Drop the chain `MLA → MOE → MTP → FP8` (these are concurrent innovations, not sequential). Use 2x2 grid. |
| `module-07/images/fig-7.3.4-mcts-for-language-reasoning.mmd` | MCTS tree | 17 | Add real branching - currently 3 branches with one promising and two stubs; make it a 3-deep tree with visit counts on every node. |

#### Group B: "Caption promises a chart, figure delivers prose-in-boxes" (10 figures)
Pattern: caption uses words like "performance", "frontier", "growth", "scatter", "curve", "tradeoff curve". Figure uses boxes.

| File | Caption fragment | Σ | Recommended fix |
|---|---|---|---|
| `module-08/images/fig-8.1.2-performance-as-a-function-of-total-compute...mmd` | three scaling strategies | 12 | (REPLACE; see F11) |
| `module-08/images/fig-8.5.1-compute-optimal-inference-frontier...mmd` | crossover frontier | 11 | (REPLACE; see F12) |
| `module-07/images/fig-7.4.3-illustrative-performance-gap-on-multilingual-qa...mmd` | "low-resource trail by 40+ pts" | 14 | Bar chart, not three subgraph boxes. |
| `module-02/images/fig-2.1.3-multilingual-tokens.mmd` | "context window usage by language" | 16 | Stacked horizontal bars (one per language) showing tokens consumed vs remaining; current 4-box chain shows the numbers but hides the proportion. |
| `module-04/images/fig-4.1.4-pos-encoding.mmd` | "Positional encoding heatmap" | 14 | Caption literally says "heatmap"; figure is two text boxes describing a heatmap. Use a real heatmap (matplotlib SVG) or remove the figure - prose suffices. |
| `module-04/images/fig-4.1.8-causal-mask.mmd` | "Causal attention mask (4 tokens)" | 16 | Render as a 4x4 grid (lower-triangular green, upper-triangular red), not as a column of "attend / block" text rows. Mermaid can't do this well; use SVG. |
| `module-05/images/fig-5.1.2-greedy.mmd` | "greedy vs better path" with probabilities | 17 | Probabilities (0.6 x 0.4 x 0.5) shown as text inside boxes; should be edge-weighted graph with bar-glyphs or thicker arrows for higher probability. |
| `module-05/images/fig-5.1.3-beam-search.mmd` | "beam search k=2" | 17 | Currently a 2-wide tree across 4 steps; would benefit from showing pruned beams (greyed) so the "best may not start with greediest" lesson is explicit. |
| `module-05/images/fig-5.2.3-top-p-sampling.mmd` | "nucleus expands when uncertain" | 17 | Two probability distributions shown as boxes with numbers; should be two bar charts side-by-side with the nucleus shaded. |
| `module-18/images/fig-19.4.2-explanation-methods.mmd` | faithfulness vs cost | 11 | (REPLACE; see F15) |

#### Group C: "Comparison rendered as parallel subgraphs that should be a table" (12 figures)
Pattern: 2-3 subgraphs side-by-side, each containing the same set of properties as bullet points. Reader has to scan back-and-forth to compare.

Affected: `fig-1.4.2-static-contextual` (Static vs Contextual), `fig-1.2.2-stem-lemma` (Stemming vs Lemmatization), `fig-2.3.4-tokenizer-landscape` (BBPE/WordPiece/Unigram), `fig-4.3.2-three-families` (encoder-only/decoder-only/encoder-decoder), `fig-4.3.4-pos-strategies` (4 positional encoding strategies), `fig-5.4.3-ar-vs-diffusion`, `fig-6.2.2-clm-mlm` (CLM vs MLM), `fig-6.3.4-scaling-laws` (Kaplan vs Chinchilla), `fig-7.1.2-frontier-ecosystem` (Tier 1 vs Tier 2 model providers), `fig-7.3.2-train-test-scaling` (Train-time vs Test-time), `fig-9.1.3-gptq-vs-awq`, `fig-19.2.4-no-superposition-vs-superposition`. Σ range 14-17.

**Recommendation:** Most of these would be more scannable as a comparison table with rows = property, columns = approach. Where the figures should remain visual, enforce parallel-vertical alignment (same property must appear at the same vertical position in each panel) and use small icon glyphs or color coding for shared properties (✓/✗, low/medium/high). Currently the subgraphs are all `direction TB` with text bullets in arbitrary order, which forces eye-darting.

If retained as Mermaid: add a horizontal comparison header (`subgraph PROPS["..."]`) below each panel column - e.g., for the encoder/decoder/encoder-decoder figure, ensure `attention type / models / tasks` appear in the same row of each panel.

#### Group D: "Architecture block lacks tensor shapes / dimensions" (7 figures)
Pattern: an architecture diagram (block of layers, attention variants, normalization choices) without `(n, d)`, `(b, h, n, d)`, or per-layer parameter annotations. Reader cannot tell what flows through the wires.

| File | Caption fragment | Σ | Fix |
|---|---|---|---|
| `module-04/images/fig-4.1.7-pre-post-ln.mmd` | Pre-LN vs Post-LN | 17 | Add "input shape (B,S,d_model)" entering and exiting each block. Indicate where shape changes (it doesn't, but say so). |
| `module-04/images/fig-4.3.6-pre-post-ln2.mmd` | Pre-Norm vs Post-Norm (duplicate of 4.1.7!) | 16 | This duplicates fig-4.1.7. Pick one and delete the other. |
| `module-04/images/fig-4.2.2-decoder-only.mmd` | "Decoder-only Transformer" | 17 | Add tensor shape annotations on the embedding output, between blocks, and at logits. |
| `module-06/images/fig-6.2.4-multi-token-pred.mmd` | multi-token prediction | 16 | Show shapes: backbone output is (B,S,d), each head projects to (B,S,vocab). |
| `module-09/images/fig-9.2.5-radixattention.mmd` | radix tree of KV prefixes | 16 | Add token counts per node so reader sees how much memory is shared. |
| `module-34/images/fig-34.3-mamba-block.mmd` (orphan) | Mamba block | 16 | Add d_state, d_conv, d_inner annotations on each branch. |
| `module-34/images/fig-34.3-rwkv-block.mmd` (orphan) | RWKV block | 15 | Add channel dimensions; clarify where time-mixing introduces O(1) inference cost. |

#### Group E: "Decision tree rendered as linear chain" (4 figures)
Already covered above (F3, F4, plus two listed in REPLACE). For completeness: Module 12's `section-11.2-svg3` and Module 8's `fig-8.4.1` are the two decision figures; the latter is already correctly branching and is one of only two well-formed decision trees in the book (the other being PEFT).

#### Group F: "Three-or-more-experts MoE/router with no per-expert detail" (3 figures)
- `module-06/images/fig-6.3.7-moe-layer.mmd` - Σ=22 (KEEP, baseline reference).
- `module-34/images/fig-34.2-switch-moe.mmd` (orphan) - Σ=17. Good but never embedded; embed it.
- `module-07/images/fig-7.2.1-deepseek-v3.mmd` MoE component - already in Group A.

#### Group G: Miscellaneous MAJOR fixes (9 figures)

| File | Σ | Issue and fix |
|---|---|---|
| `module-01/images/fig-1.1.4-nlp-tasks.mmd` | 17 | Two flat lists (Understanding/Generation) joined by a generic "LLMs can perform both". Add 1-2 example inputs/outputs per task to show what each task LOOKS like. |
| `module-01/images/fig-1.1.6-linguistic-layers.mmd` | 17 | 4 layers as a chain with `---` connectors. Use nested concentric boxes (pragmatics outermost) since these are layered, not sequential. |
| `module-01/images/fig-1.2.3-bow-matrix.mmd` (orphan) | 16 | A count matrix faked as text-in-boxes. Use an HTML table or a real grid SVG. |
| `module-01/images/fig-1.3.5-cosine-sim.mmd` | 17 | "King, queen 15deg cos=0.97" stated in box; should be a small unit-circle figure with the angle drawn. Mermaid can't do circles well; use matplotlib. |
| `module-04/images/fig-4.3.3-rope.mmd` | 16 | RoPE caption says "rotates each pair of dimensions"; figure has 3 text boxes inside a subgraph. Add a small rotation diagram (vector at pos 0 and pos 3). Matplotlib SVG. |
| `module-06/images/fig-6.5.3-grokking.mmd` | 15 | Grokking is a *curve* (train acc rises early, val acc plateaus then jumps). Three boxes can't capture that. Use a line chart with two curves and a big arrow marking "grokking moment". |
| `module-07/images/fig-7.3.3-orms-vs-prms.mmd` | 17 | Conceptually right (parallel chains for ORM and PRM); add a "where ORM gets stuck" arrow vs "where PRM diverges" annotation. |
| `module-09/images/fig-9.2.3-static-vs-continuous-batching.mmd` | 17 | Two text-block subgraphs. Should be a Gantt-style timeline showing 4 sequences, with idle boxes (white) in static and packed (filled) in continuous. |
| `module-32/images/fig-33.9.1-eu-ai-act-risk-tiers.mmd` | 17 | Caption says "PYRAMID" but figure is 4 chained boxes. Render as actual pyramid (trapezoids stacked). |

---

## Section 4. Patterns across the book

### 4.1 Concept categories where Mermaid flowchart works well

- **Pipelines / sequential data flow** (RAG ingestion, log-to-dataset refinery, OTel trace, durable execution recovery, training loop, GraphRAG indexing).
- **Anatomical block diagrams of single architectural units** when tensor shapes are annotated (perceptron, LSTM cell, scaled dot-product attention, decoder block, MoE layer).
- **Multi-stage feedback cycles** (self-refine, RL agent-environment loop, RLHF policy update).
- **Workflow with branching that ends at distinct terminal nodes** (PEFT decision tree, error-recovery decision tree, fig-8.4.1).

In all these cases the *flow* is the content, so a flowchart is the right tool.

### 4.2 Concept categories where Mermaid flowchart fails

- **Time series / growth curves / scaling curves.** These need axes and curves; flowchart cannot make growth visible. (Module 6, 7, 8 affected.)
- **Comparisons of N approaches across a fixed set of properties.** A table is cleaner; if visual, use parallel-aligned panels with a header row of properties.
- **Hierarchies of containment** (complexity classes, EU AI Act risk pyramid, attention-head taxonomies). Use nested boxes / Venn / pyramid.
- **2-D scatter / quadrant placements** (faithfulness-vs-cost, easy-vs-hard tasks). Use `quadrantChart` or matplotlib.
- **Heatmaps / matrices / attention masks.** Mermaid is the wrong tool; even ASCII grids look poor at print resolution.
- **Trees with branching and pruning.** Use a real flowchart with multiple children; never collapse into a chain.
- **Sequence-of-API-calls between components.** A `sequenceDiagram` with lifelines beats a flowchart.

### 4.3 Recurring labeling issues

1. **Boxes used as paragraph containers.** Many module-11 boxes hold full sentences in `<b>...<i>...</i></b>` formatting. Boxes should hold ≤ 5 words; longer text belongs in the caption or surrounding paragraph.
2. **Unicode escape soup.** `&Sigma;`, `&theta;`, `&#x4F60;`, `<br/>`, `&lt;`, `&gt;` appear inline. Renderers vary in support. Standardize on UTF-8 (`Σ`, `θ`, `你`, `<`, `>`) and use real `<br>` only when needed.
3. **Inconsistent emphasis convention.** Some figures use `**bold**` (Mermaid markdown), some use `<b>...</b>`, some use both. Pick one style per book.
4. **Math expressions as plain text.** `dL/da = 1.0`, `q . k`, `Σwx + b` appear as raw text where they should use the same KaTeX-rendered math used in the surrounding prose. Ensure consistency: either render figure math in a separate LaTeX/SVG step, or accept text-form throughout.
5. **Single-letter variables without legend.** RoPE figure uses `theta`, `pos=3` without saying what `theta` is in this figure (it's defined in the caption but not in the box).
6. **"NOTE" boxes as a crutch.** ~30 figures end with a `NOTE["..."]` box pointed at by an arrow. The note usually restates the caption or surrounding prose. Either remove (let the caption do its job) or convert to a true visual annotation (callout pointing at a specific element).

### 4.4 Recurring structural issues

- **Duplicate diagrams under different filenames.** Confirmed pairs include:
  - `appendices/appendix-l-langchain/images/agent-execution-loop.mmd` ≡ `section-l.5-svg1.mmd`
  - `appendix-l-langchain/lcel-chain-data-flow.mmd` ≡ `section-l.1-svg1.mmd`
  - `appendix-l-langchain/runnable-message-history.mmd` ≡ `section-l.2-svg1.mmd`
  - `appendix-o-llamaindex/ingestion-pipeline.mmd` ≡ `section-o.1-svg1.mmd`
  - `module-01/fig-1.3.6-fasttext-subword-decomposition*.mmd` ≡ `fig-1.3.6-fasttext.mmd`
  - `module-02/fig-2.2.5-byte-bpe.mmd` ≡ `fig-2.2.5-byte-level-bpe...mmd`
  - `module-03/fig-3.1.6-seq2seq.mmd` ≡ `fig-3.1.6-the-encoder-decoder-seq2seq...mmd`
  - `module-03/fig-3.2.4-gradient-attention.mmd` ≡ `fig-3.2.4-gradient-flow-through-attention...mmd`
  - `module-04/fig-4.1.7-pre-post-ln.mmd` ≡ `fig-4.3.6-pre-post-ln2.mmd`
  - `module-04/fig-4.1.7-residual-stream.mmd` ≡ `fig-4.1.9-residual-stream.mmd`
  - `module-06/fig-6.8.1-production-llm-training-architecture...mmd` ≡ `production-training-architecture.mmd`
  - `module-07/bolt-on-vs-native-multimodal.mmd` ≡ `fig-7.1.4-bolt-on-multimodal-architecture...mmd`
  - `module-07/reasoning-token-flow.mmd` ≡ `fig-7.1.3-reasoning-token-flow...mmd`

  In each pair, one is wired into the HTML (the `fig-N.M.K-...` long-name version) and the other is an unreferenced earlier draft. The orphans should be removed or merged.

- **25 orphan `.mmd` files** (no HTML reference): listed above plus all `module-11/section-11.*-svg*.mmd` (which appear in the markdown source `md/` but not the published `section-11.*.html`), plus `module-04/fig-4.3-s4-three-views.mmd`, `module-10/section-10.3-svg1.mmd`, `module-10/section-10.5-svg1.mmd`, `module-34/fig-34.2-*`, `fig-34.3-*`, `fig-34.4-*`, `scripts/mermaid/test_elk.mmd`. Either embed them or delete them; a stale .mmd is dead code.

- **Numbering drift between caption and filename.** E.g., `fig-1.1.4-nlp-tasks.mmd` is captioned as "Figure 1.1.5"; `fig-1.4-evolution.mmd` is captioned as "Figure 1.4.7"; `fig-3.1.3-vanishing-grad.mmd` is captioned "Figure 3.1.2"; `fig-4.1.4-pos-encoding.mmd` is captioned "Figure 4.1.3"; `fig-4.1.7-pre-post-ln.mmd` is captioned "Figure 4.1.7" but `fig-4.1.8-causal-mask.mmd` is captioned "Figure 4.1.5"; `fig-4.3.2-three-families.mmd` is captioned correctly while `fig-4.3.6-pre-post-ln2.mmd` is captioned... wait, this overlaps with the `diagram_audit.md` finding (`CAPTION_MISALIGN` × 95). The two audits agree.

- **Subgraph naming is inconsistent.** Some subgraphs use uppercase short codes (`MOE`, `KG`, `RAG`), others use full English (`Tree-Structured Verification`), others are blank labels (`subgraph ROW1[" "]`). Settle on a style.

---

## Section 5. Triage and next steps

### 5.1 Recommended fix order (highest reader-comprehension impact first)

**Tier 1 - replace these 15 figures before next print run** (~15 hours):
- All 6 `module-11/section-11.*-svg*.mmd` figures (Tree of Thoughts, decision flowchart, prompt anatomy, model chaining, etc.) - the worst-served chapter.
- 5 charts-pretending-to-be-flowcharts: `fig-6.1.4-param-growth`, `fig-6.1.2-encoder-timeline`, `fig-6.5.3-grokking`, `fig-8.1.2-perf-vs-compute`, `fig-8.5.1-frontier`.
- 3 hierarchy figures: `fig-4.5.2-complexity` (TC0/AC0), `fig-33.9.1-eu-ai-act-risk-tiers` (pyramid), `fig-1.1.6-linguistic-layers` (nested layers).
- 1 multi-axis comparison: `fig-19.4.2-explanation-methods`.

**Tier 2 - restructure these 53 MAJOR figures** (~25 hours):
- 8 timelines → use Mermaid `timeline` (cheap fix)
- 12 comparison-as-subgraphs → render as tables OR enforce parallel alignment (medium fix)
- 7 architecture diagrams → add tensor shape annotations (cheap fix)
- 10 chart-promised-by-caption → produce real charts in matplotlib (most expensive)
- 16 miscellaneous redesigns

**Tier 3 - cleanup** (~5 hours):
- Delete 13 confirmed duplicate `.mmd` files; embed or delete remaining 12 orphans.
- Fix 95 caption/filename misalignments (covered by `diagram_audit.md`).
- Standardize emphasis convention (`<b>` vs `**`) and Unicode handling.

### 5.2 Per-fix effort

| Fix type | Per-figure effort | Tooling |
|---|---|---|
| Label cleanup, MINOR | 5-10 min | Edit .mmd in place |
| Restructure within Mermaid (timeline, true tree, parallel alignment) | 20-40 min | Mermaid + careful authoring |
| Add tensor shapes / annotations | 10-15 min | Edit .mmd in place |
| Replace flowchart with `xychart-beta` or `quadrantChart` | 30-60 min | Mermaid v10+ syntax |
| Replace with matplotlib SVG | 60-90 min | New script per figure |
| LLM-generated SVG (line chart, heatmap, scatter) | 30-60 min including review | Code Interpreter / Claude with constraints |

**Total estimated effort for full audit-driven cleanup: ~45 hours of focused work.** The book is in publishable condition without these fixes; it would be substantially stronger with the Tier 1 + Tier 2 cleanups.

### 5.3 Recommended pipeline by figure category

| Figure category | Best authoring approach |
|---|---|
| Single-cell architecture / pipeline / cycle | Keep as Mermaid `flowchart` - already strong |
| Timeline / chronology | Mermaid `timeline` (built-in) - cheap upgrade |
| Decision tree | Mermaid `flowchart TD` with `Q1{...} -->|"Yes"| ...` syntax - already supported |
| Comparison of N approaches (≥3 properties) | HTML table embedded in section, NOT a figure |
| Comparison of N approaches (visual / spatial) | Mermaid with parallel-aligned subgraphs + property header |
| Sequence of API calls between actors | Mermaid `sequenceDiagram` (currently zero used) |
| 2-D scatter / quadrant | Mermaid `quadrantChart` or matplotlib |
| Time series / growth / scaling curves | Matplotlib SVG (Mermaid `xychart-beta` is too limited for log-scale) |
| Heatmap / mask / matrix grid | Matplotlib SVG (Mermaid cannot) |
| Containment hierarchy | Mermaid nested subgraphs OR pyramid SVG |
| Anatomical labelled diagram (perceptron-style with arrows + math) | Mermaid `flowchart` with shapes; or Inkscape SVG for higher fidelity |

The key change in production pipeline: **introduce matplotlib SVG generation for the ~12-18 figures that genuinely need a chart**, and **adopt Mermaid `timeline` and `quadrantChart`** for the ~10 figures that need time/2D-axis layouts but can stay in Mermaid.

---

*End of audit.*
