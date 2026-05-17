# Wave 25: diagram audit (new chapters)

Audit date: 2026-05-17. Scope: Chapter 36 (5 sections), Chapter 41 (5), Chapter 56 (5), Chapter 59 (5), Chapter 61 (5), plus Wave-17i consolidation sections 24.6, 24.13, 26.6, 27.5, 29.1, 29.4, 35.2, 35.3, 37.3. Reference quality bar: section-3.1.html (`Figure 3.1.5`, residual stream), section-26.6.html (memory taxonomy figure), section-44.5.html (drift detection, but note this section has no diagrams in current source so the actual benchmark is 3.1.5 and the 59.1 SVGs).

Inventory of inline SVGs (counts per file):

| Chapter | Section | SVG count |
|---|---|---|
| 36 | 36.1-36.5 | 0 in every section |
| 41 | 41.1 | 1 |
| 41 | 41.2 | 1 |
| 41 | 41.3 | 1 |
| 41 | 41.4 | 1 |
| 41 | 41.5 | 0 |
| 56 | 56.1 | 1 |
| 56 | 56.2-56.5 | 0 in each |
| 59 | 59.1 | 2 |
| 59 | 59.2 | 1 |
| 59 | 59.3 | 1 |
| 59 | 59.4 | 2 |
| 59 | 59.5 | 1 |
| 61 | 61.1-61.5 | 1 in each (5 total) |
| Wave 17i | 24.6, 24.13, 26.6, 27.5, 29.1, 29.4, 35.3 | 0 inline SVGs (PNG illustrations only) |
| Wave 17i | 35.2 | 1 |
| Wave 17i | 37.3 | 2 |

## Top remaining issues (prioritized)

1. **Chapter 36 (Retrieval Tools): five sections, zero diagrams.** The chapter is the densest "tools of the trade" chapter in Part 7 and shouldn't be all prose plus tables. The biggest gap is **section-36.1.5 "A decision tree"** — currently a 9-bullet prose list that begs to be an SVG decision tree (5 to 7 boxes). Same shape gap in 36.2.7 (orchestration framework comparison) and 36.4.6 (embedder selection). The 36.3 benchmarks section needs at least one diagram comparing benchmark scope.

2. **Chapter 41 SVGs use a non-book color palette and font family (Georgia, not sans-serif).** All four Chapter 41 SVGs (`section-41.1.html`, `.2`, `.3`, `.4`) use `font-family="Georgia, serif"` and a palette of `#1a2b5c, #2f6b3a, #5d3c8c, #b87000, #a73838` which is *close* to the book palette (navy/green/purple/amber/red) but the hex values diverge from book.css. They also use `#f7f7f2` cream background instead of white. **Plus**, none of the four uses a `<figcaption><strong>Figure N.M.K</strong>: ...</figcaption>` outside the SVG; the title is baked inside as `<text>`. This breaks figure-numbering consistency with the rest of the book.

3. **Chapter 56 (Responsible AI Tools): one section out of five has a diagram (56.1), four sections have none.** Same Georgia/non-palette issue as Chapter 41 (the SVG was clearly authored from the same template). Sections 56.2 (libraries), 56.3 (benchmarks), 56.4, and 56.5 have no diagrams in a chapter where a "responsible AI stack" map and a "fairness library decision matrix" would carry real pedagogical weight.

4. **Chapter 61 (Scale Tools): every section uses the same "tile-map" SVG pattern.** All five 61.x SVGs are six-rectangles-in-2x3-grid platform maps with the same colors (`#1a2b5c, #2f6b3a, #5d3c8c, #b87000, #a73838, #666`) and same `#f7f7f2` background. They are repetitive, share the Georgia-serif issue, and have no figcaption pattern. The visual identity reads as "filler diagram" rather than "earned diagram". The most acute repetition issue is between 61.1, 61.2, and 61.3 which are nearly visually indistinguishable at a glance — three "platform stack" maps with rectangles of identical shape.

5. **Chapter 59 figure 59.5.1 (training stack) is a five-layer rainbow.** Uses five distinct row colors including dark red `#9a2828` and purple `#5f2a8a` that are not in the rest of the book's diagrams. Layers-by-color is OK semantically, but the colors should at least come from the book palette (navy / green / purple / amber / red) consistently.

6. **Figure 59.2.1 (ZeRO stages) has 20 sub-boxes** across four stage panels. This is reasonable as a **memory bar chart by stage** (it's a column comparison, not a flow diagram) but it pushes against the "≤8 boxes" guideline. Could be split into 1 conceptual diagram (4 stages × 1 stacked-bar) plus a separate table-style "what is sharded" summary if rebuilt; as-is it remains defensible because the visual rhythm is regular.

7. **Figure 59.4.1 (GPipe vs 1F1B) has 60+ Gantt cells** but Gantt charts are the canonical convention for pipeline-schedule diagrams and the cell count is necessary to show the bubble. KEEP. Don't decompose.

8. **section-37.3.html SVGs use a third color palette** (`#3498db / #8e44ad / #27ae60 / #f39c12 / #1a1a2e` — a flat-design / Material palette) which is yet again different from both the Chapter 41/56/61 family AND from Chapter 59's. This is a Wave-17i carry-over; consider re-skinning to match either Ch 59 or book.css.

9. **section-37.3.html Figure 37.3.3 caption has a markup bug**: `<strong><strong>Figure 37.3.3</strong>` — nested `<strong>` tags. Visible at line 499 of `section-37.3.html`.

10. **section-35.2.html GraphRAG SVG has cluttered/duplicate edge labels.** Lines 99-110 of `section-35.2.html` add a `data-annotation-line` overlay (line 108) that is not labeled; combined with multiple `<text>` labels at similar coordinates the visual is busier than its content requires. Six nodes plus six labeled edges is at the upper end of comfortable; the dashed annotation line could be removed.

## Per-chapter findings

### Chapter 36 — Retrieval Tools (`part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/`)

- **section-36.1**: 0 inline SVGs, 1 comparison table (12-row platform comparison, well-built). PROPOSE adding a **platform selection decision tree** SVG to replace or complement section 36.1.5's 9-bullet prose decision tree. 5-6 boxes max: "Already on Postgres + <50M vectors? → pgvector" / "Need to ship fast, no infra team? → Pinecone or Chroma" / "Multi-tenant SaaS, many cold tenants? → Turbopuffer" / "Heavy filtering? → Qdrant or Vespa" / "Already on ES/OS? → native vector field" / "Billion-scale on-prem? → Milvus or Vespa". Use book palette navy boxes with green decision diamonds.

- **section-36.2**: 0 inline SVGs, 1 comparison table (orchestration frameworks). PROPOSE a small **"thinnest viable stack" diagram** to illustrate section 36.2.8: 4-5 boxes showing the recommended minimal layer stack (embedder, vector DB, retriever orchestration, eval). Reuse the layered-stack pattern from Chapter 59 figure 59.5.1 but pruned to ≤5 layers and the book palette.

- **section-36.3**: 0 inline SVGs, 1 large comparison table (benchmarks). PROPOSE a **scope-versus-realism scatter** sketched diagram: x-axis "task scope" (single fact, multi-doc synthesis), y-axis "contamination resistance" (high to low). Plot BEIR, MS MARCO, MTEB, RAGTruth, NaturalBenchRAG. 6-8 dots, axes labeled. This makes section 36.3.7 ("contamination-resistant benchmarks") visual instead of prose.

- **section-36.4**: 0 inline SVGs, 1 comparison table (embedders). PROPOSE a **dimensionality-vs-quality trade curve** sketched on standard axes for section 36.4.7 (Matryoshka). 3-4 model labels plotted; dashed line showing the Matryoshka projection trajectory.

- **section-36.5**: 0 inline SVGs, mostly link lists. Lower priority — section 36.5 is a "tools of the trade" reading/community list and prose plus a comparison table is fine. Optional: a tiny **"weekly cadence wheel"** illustrating the 36.5.9 reading cadence.

### Chapter 41 — Conversational AI Tools (`part-8-conversational-ai-with-llms/module-41-conv-ai-tools/`)

- **section-41.1, "Conversational AI platform landscape" SVG (lines 92-126)**: 2x3 grid of 6 platform-category tiles plus a cross-axis annotation. RE-SKIN. Issues: (a) uses Georgia serif font instead of book sans-serif; (b) palette `#1a2b5c, #2f6b3a, #5d3c8c, #b87000, #a73838` is close-but-not-equal to the book palette; (c) tile #6 ("Persona stores") repeats the navy color of tile #1, which is visually misleading because they aren't more closely related than the others; (d) no `<figcaption><strong>Figure 41.1.x</strong>` outside the SVG, so this diagram has no figure number in the running text. KEEP the content/structure (6 tiles + cross-axis is a fine landscape map), but recolor to book palette and add a proper figcaption.

- **section-41.2, "Choosing a chat orchestration framework" SVG (lines 230-263)**: same template as 41.1, same six-color-tile layout. Same issues (Georgia font, off-palette, no figcaption). RE-SKIN. The content (6 framework tiles + bottom-recommendation banner) is a legitimate decision aid; the visual treatment needs to match the book.

- **section-41.3, "Conversational AI evaluation pyramid" SVG (lines 223-244)**: pyramid of 5 trapezoid tiers. Same palette/font issue. The pyramid form is a strong choice for "broad cheap → narrow expensive" eval layers. KEEP the structure; RE-SKIN to book palette. Add figcaption.

- **section-41.4, "Picking a chat model: four axes" SVG (lines 154-180)**: 2x2 grid of axis tiles + recommendation banner. Same template family. RE-SKIN. The 2x2 form fits the content ("four axes") well; what's missing is positioning model families *on* the axes — the current diagram lists the axes but doesn't show comparative position of (say) Claude vs GPT vs Llama. Optional enhancement: show one or two example placements per axis to make the diagram earn its space.

- **section-41.5**: 0 inline SVGs. Low priority — this is a community/reading list section like 36.5.

### Chapter 56 — Responsible AI Tools (`part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/`)

- **section-56.1, "Responsible AI platform landscape" SVG (lines 77-111)**: same Georgia-font / off-palette / no-figcaption template family as Chapter 41. 2x3 tile map: governance suites, hyperscaler bundles, observatories, LLM safety runtimes, privacy-GRC hybrids, open-source stacks. RE-SKIN. Structure is fine; visuals don't match the book.

- **section-56.2**: 0 inline SVGs. PROPOSE a **stack diagram** for section 56.2.8 ("a canonical 2026 responsible AI stack"). 5 layers: data preprocessing (fairness slicing) → training-time (DP-SGD, debiasing) → eval (HELM, lm-eval-harness, BBQ) → runtime guard (Lakera, NeMo Guardrails) → governance registry (Credo, Holistic). Use the same layered-stack template as Chapter 59 figure 59.5.1 but recolored to the book palette and trimmed to 5 boxes.

- **section-56.3**: 0 inline SVGs. PROPOSE a **benchmark-coverage matrix** for section 56.3.7: rows = harm categories (bias, toxicity, hallucination, privacy, multi-dim aggregated); columns = leading benchmarks; cells filled in where covered. This is naturally a small chart, not a flow diagram. Alternative: a **funnel** showing the evaluation cascade (bias benchmarks → toxicity → hallucination → privacy → aggregated dashboards).

- **section-56.4**: 0 inline SVGs. Lower priority — this is a "models for RAI" section that is mostly model lists.

- **section-56.5**: 0 inline SVGs. Low priority — reading and community list.

### Chapter 59 — Distributed Training Systems (`part-12-llm-systems-at-scale/module-59-distributed-training-systems/`)

This chapter has the closest-to-book-quality diagrams in the audited set, and **all six SVGs use the same visual language** (the navy/green/amber palette of `#1a4078 / #1f7a3a / #a67c1a` with light-tinted backgrounds), which gives the chapter strong visual identity.

- **section-59.1 Figure 59.1.1 "Three Axes of Parallelism" SVG (lines 57-157)**: KEEP. 3-panel comparison (Data / Pipeline / Tensor parallel) with consistent palette, clear GPU box layouts, ≤3-word labels per box, and a clean per-panel "Comm: ..." summary line. This is a model diagram for the chapter and is one of the strongest in the audit. Caption explains the takeaway ("Production training composes all three"). Reference quality.

- **section-59.1 Figure 59.1.2 "Interconnect hierarchy" SVG (lines 209-269)**: KEEP. Three tier panels (Tier 1 NVLink / Tier 2 InfiniBand / Tier 3 spine) with the same palette as 59.1.1. Bandwidth annotations are concrete and useful. Strong diagram.

- **section-59.2 Figure 59.2.1 "ZeRO Stages" SVG (lines 64-147)**: KEEP with note. 4-column memory bar chart (Stage 0 / 1 / 2 / 3) with 5 stacked component bars per stage = 20 cells. This is a *bar chart by stage*, not a 20-box flow diagram, so the cell count is appropriate to its function. Color uses 5 monochromatic blues for the memory components which is clean. Bottom comm-cost legend is useful. Caption explains the dashed/solid box convention. Defensible. If revisited later, could split into one diagram per stage (4 small diagrams) but the current single comparative chart works.

- **section-59.3 Figure 59.3.1 "Tensor-Parallel MLP" SVG (lines 65-158)**: KEEP. LR flow from X → column-parallel W1 → GELU → row-parallel W2 → Y with f/g communication labels and bottom "two all-reduces per block" annotation. Uses the navy/amber/green palette consistently (color-codes the column/row directions). 8-9 boxes counting the small f/g arrow markers, but the visual is uncluttered because the boxes are spatially separated. Good diagram.

- **section-59.4 Figure 59.4.1 "GPipe vs 1F1B" SVG (lines 52-230)**: KEEP. 4-row × 14-or-16-column Gantt comparing pipeline schedules. Cell count is high but Gantt is the canonical convention for this content; cell count is *required* to show the bubble visually. Color use is restrained (green for F, amber for B, gray for idle). The two-stack comparison communicates the bubble shrinkage clearly. Reference quality for chapter.

- **section-59.4 Figure 59.4.2 "3D Parallelism" SVG (lines 270-340)**: KEEP. Three panels (TP / PP / DP) using the same navy/green/amber palette as 59.1.1 and showing what each axis runs across. The bottom "rule of thumb" callout reinforces the takeaway. Consistent with chapter language. Good.

- **section-59.5 Figure 59.5.1 "Production Training Stack" SVG (lines 148-210)**: REVIEW. 5-row layered stack: Framework / Distributed primitives / Orchestration / Observability / Storage. Uses 5 distinct row colors including dark red `#9a2828` and purple `#5f2a8a` that don't appear elsewhere in the chapter. This breaks the chapter's visual identity. PROPOSE re-skinning to use only the 3-color (navy/green/amber) palette plus one additional accent (purple from book.css `#6a1b9a`), and reusing the same light-tint background pattern as the other Ch 59 diagrams.

### Chapter 61 — Scale Tools (`part-12-llm-systems-at-scale/module-61-scale-tools/`)

All five 61.x SVGs follow the same template (cream background, Georgia serif, 5-6 color tile maps with `#1a2b5c / #2f6b3a / #5d3c8c / #b87000 / #a73838 / #666`). The chapter's diagrams have a unified visual language but it doesn't match the rest of the book (and is identical to the Chapter 41 + 56.1 templates, which were probably authored together).

- **section-61.1, "LLM training platform stack (2026)" SVG (lines 92-119)**: RE-SKIN. 6 tiles (Hyperscaler, Specialized GPU, In-house, Scheduler, Storage, Framework + Observability bottom). Same template-family issues. Structure is fine. No figcaption outside the SVG.

- **section-61.2, "LLM training library stack (2026)" SVG (lines 103-124)**: RE-SKIN. 5-row layered stack (High-level recipes / Foundation distributed / Optimization kernels / Communication / Orchestration). This is a competent layered architecture diagram; only visual issues. NOTE: this and Chapter 59 figure 59.5.1 are the same shape (5-row layered stack) with overlapping content; consider cross-referencing them or merging the visual.

- **section-61.3, "LLM data and benchmark stack (2026)" SVG (lines 96-130)**: RE-SKIN. 2x3 tile grid + bottom annotation. Same template issues. Structure works.

- **section-61.4, "LLM model landscape (mid-2026)" SVG (lines 187-222)**: RE-SKIN. 2x3 tile grid + bottom selection-axes annotation. Same template issues. PROPOSE a stronger version that plots model families on a parameter-count × license axis instead of grouping them into category tiles. The 2x3 form here is the weakest fit — a scatter or quadrant would communicate more.

- **section-61.5, "Reading and community landscape" SVG (lines 142-176)**: RE-SKIN. 2x3 tile grid + bottom cadence banner. Lower priority because section 61.5 is meta-reading; the diagram is supplementary.

### Wave 17i consolidation-touched sections

- **section-24.6.html (`part-5-multimodal-llms/module-24-vla-models/`)**: 0 inline SVGs. Has 1 comparison table and prose. The "dexterity ceiling" table (section 24.6.2) and "language understanding cliff" (24.6.4) prose are candidates for a small **capability-ladder** SVG (5 rungs, frontier above tool-use line). Lower priority.

- **section-24.13.html (`part-5-multimodal-llms/module-24-vla-models/`)**: 0 inline SVGs but 3 figcaption-labeled tables (Figure 24.13.2 / 24.13.3 are tables labeled as figures, which is an inconsistency — they're tabular, not visual). Section is heavy on data. The cumulative-gap-closing diagram and the deployment-stages cost breakdown would both benefit from being actual diagrams (bar chart or stacked-effect chart) rather than tables-labeled-as-figures.

- **section-26.6.html (`part-6-agentic-ai/module-26-ai-agents/`)**: 0 inline SVGs but 1 PNG illustration `images/memory-taxonomy-five-layers.png`. Caption explains the layered model well. The PNG is referenced as `Figure 26.6.1`. NO INLINE SVG to audit. Note: this section was cited in the prompt as a reference for "Memory architecture" diagram convention — the actual diagram is a PNG illustration, not an SVG. The reference benchmark for SVG diagrams should really be 3.1.5 + 59.1.1 + 59.1.2.

- **section-27.5.html (`part-6-agentic-ai/module-27-tool-use-protocols/`)**: 0 inline SVGs but 1 PNG illustration `images/ch23-agentic-rag-librarian.png` (a narrative illustration, not a technical diagram). PROPOSE adding a small technical diagram showing the agent → retrieval-tool → vector-store → response loop with retry edges, in book palette. Currently the section explains the agent-side retrieval pattern in prose and code only.

- **section-29.1.html (`part-6-agentic-ai/module-29-specialized-agents/`)**: 0 inline SVGs but 2 PNG illustrations. Figure 29.1.1 (the specialist agent team) and Figure 29.1.2 (the self-debugging loop) are both narrative illustrations rather than technical diagrams. The self-debugging loop especially deserves a small SVG showing write → run → observe error → reason → fix → repeat with the iteration-budget exit edge.

- **section-29.4.html (`part-6-agentic-ai/module-29-specialized-agents/`)**: 0 inline SVGs. Comparison table for agentic-coding platforms is present. Section is mostly prose plus a single table; could benefit from a small **agency-vs-developer-control** quadrant diagram (Claude Code / Cursor / Windsurf / Devin positioned by autonomy axis).

- **section-35.2.html (`part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/`)**: 1 inline SVG ("knowledge graph example", lines 81-116). REVIEW. 6 colored nodes (Einstein/Ulm/Relativity/Physics/Nobel/ETH) with 6 labeled edges. Uses circle nodes with distinct colors per node, which is visually busy compared with the book convention of consistent semantic colors (different colors should mean different *categories*, not different *instances*). The dashed `data-annotation-line` overlay (line 108) is unlabeled and adds visual noise. PROPOSE recoloring nodes by entity type (person / place / concept / award / institution) rather than per instance, and removing the spare dashed line.

- **section-35.3.html (`part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/`)**: 0 inline SVGs. Section explains the Microsoft GraphRAG pipeline (community detection, summarization, hierarchical query) in prose plus a table. PROPOSE adding a **GraphRAG pipeline LR flow** SVG: documents → entity extraction → graph construction → community detection → community summaries → query answer. 6 boxes, top-down or LR. This is exactly the type of pipeline that needs a diagram.

- **section-37.3.html (`part-8-conversational-ai-with-llms/module-37-conversational-ai/`)**: 2 inline SVGs.

  - Figure 37.3.2 "Memory architecture overview" (lines 83-125): KEEP with re-skin. 5 boxes (Context Window / Short-Term / Long-Term / Session Store / User Profile) plus dashed connectors. Uses a *third* palette (`#3498db / #8e44ad / #27ae60 / #f39c12 / #1a1a2e` — Material-design flat colors). Structure is clean and educational. The palette difference from Chapter 59's navy/green/amber and from Chapter 41/56/61's tile palette is jarring across the book.

  - Figure 37.3.3 "MemGPT / Letta architecture" (lines 454-498): KEEP with re-skin. 1 controller box + 3 tier boxes (Working / Archival / Recall) + 5 function-call labels. Cleanly shows the controller invoking memory functions. Same palette issue. BUG: nested `<strong><strong>` in the caption at line 499.

## Cross-cutting suggestions

### Visual identity should converge on the book palette across all chapters

The audit found at least **three distinct color palettes** in current diagrams:

- **"Book / Ch 59 palette"**: navy `#1a4078 / #0d3b66`, green `#1f7a3a / #2e7d32`, amber `#a67c1a / #e65100`, purple `#6a1b9a / #4a148c`, with light tints (`#eef4fa`, `#ecf6ee`, `#fef3e0`). Used in Chapter 59 and the Chapter 3 reference figure 3.1.5. **This is the book's de-facto palette and what the user's prompt describes.**

- **"Tile-map template palette"** (Ch 41 + Ch 56.1 + Ch 61): `#1a2b5c, #2f6b3a, #5d3c8c, #b87000, #a73838, #666` with cream `#f7f7f2` background and Georgia serif font. **Looks like one author/wave produced all 10 of these from the same template; should be re-skinned in bulk.**

- **"Material flat palette"** (Ch 37.3): `#3498db, #8e44ad, #27ae60, #f39c12, #1a1a2e`. **Probably a Wave-17i carry-over; should be re-skinned for cross-chapter consistency.**

A bulk re-skin pass (palette + font-family + figcaption-outside-SVG) on the 10 tile-map SVGs in Ch 41/56/61 would be the highest-leverage single improvement.

### Figcaption discipline

Diagrams that follow the book convention have `<figcaption><strong>Figure N.M.K</strong>: takeaway sentence.</figcaption>` *outside* the SVG, and an in-SVG title is optional (an internal `<title>` for a11y is fine, but the bold "Figure N.M.K" label and the takeaway sentence belong in the figcaption). The 10 tile-map SVGs in Ch 41/56/61 break this: they have an in-SVG `<title>` and an in-SVG `<text>` heading but no figcaption with a figure number. This means these 10 SVGs cannot be referenced as "Figure 41.1.1" etc. in the running text. **Recommendation**: add a `<figcaption>` to each so the figure-numbering scheme is restored.

### Gaps where a small diagram would replace prose

- **section-36.1.5** decision tree → SVG (6 decision boxes)
- **section-36.4.7** Matryoshka quality/dim tradeoff → small line chart
- **section-56.2.8** "canonical 2026 RAI stack" → 5-layer stack diagram
- **section-35.3** Microsoft GraphRAG pipeline → 6-box LR pipeline
- **section-29.1.1** the self-debugging loop → 4-box cycle with retry edge

### Diagrams that should be merged

- Chapter 59 figure 59.5.1 ("Production training stack") and Chapter 61 section-61.2 SVG ("LLM training library stack") have **substantially overlapping content** (frameworks layer, distributed primitives, orchestration). They could be one canonical diagram referenced from both chapters, or visually differentiated so the duplication is intentional and clear.

### Diagrams that should be split (already noted)

- Figure 59.2.1 (ZeRO stages) is dense (20 cells across 4 stages) but is a bar chart and the bar chart form is appropriate. Optionally splittable into 4 small diagrams + 1 communication-cost table but **not required**.

## Reference-quality benchmark (for future audits)

The top three diagrams to use as quality bar going forward:

1. `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html`, **Figure 3.1.5** (residual stream branch-and-merge). Uses book palette, ≤3-word labels, 8 elements counting both sub-layers + plus-nodes + endpoints, in-diagram reading guide, takeaway-sentence figcaption.

2. `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.1.html`, **Figure 59.1.1** (three axes of parallelism). Three side-by-side panels using navy/green/amber, GPU boxes ≤3 words each, per-panel comm summary, takeaway-sentence figcaption.

3. `part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.1.html`, **Figure 59.1.2** (interconnect hierarchy). Three tier panels with concrete bandwidth annotations.

Diagrams that match this quality bar are clear at a glance, use the book palette consistently, and pair with a figcaption that states what to take away rather than what is depicted.
