# Visual Learning Designer Pass (Cycle 3.2)

Agent: 09-visual-learning (scope Parts 5-9 section files, non-catalog only)
Date: 2026-05-19

## Scope and approach

Surveyed 96 section files across Parts 5-9 (multimodal, agentic AI, retrieval/RAG, conversational AI, evaluation/observability) and filtered out tools-of-the-trade reference modules per the brief. Targeted sections where dense conceptual prose described compare/contrast structures, sequential pipelines, hierarchies, or numeric magnitudes without any inline SVG figure. Added 11 publication-quality inline SVGs and 1 comparison table where the prose-only treatment was leaving information on the floor for visual learners.

Inventory script used: Python over the part-{5-9}/module-*/section-*.html tree, computing per-section paragraph count, SVG count, figure count, and table count. Targets were prioritized by `paragraphs >= 6 AND svgs == 0 AND figures <= 1`. From that pool, the final picks were sections containing N-way compare/contrast prose or risk/flow logic that a single static image could not replicate.

All SVGs use the R2 palette specified in the agent brief (#3a73a8 blue, #d97706 amber, #047857 green, #b91c1c red, #4a5568 secondary text) with `viewBox`, `role="img"`, `aria-label`, Segoe UI fonts, gradients via opacity layering, and drop shadows via `feDropShadow`. Captions are full sentences (not labels) and reference what the reader should notice. Figure numbers were chosen by scanning existing `Figure X.Y.N` references in each section and picking the next free slot.

## Visuals added

| # | Section | Figure | Visual type | What it shows |
|---|---------|--------|-------------|---------------|
| 1 | `part-7/module-35/section-35.4.html` (RAG Ingestion) | Fig 35.4.2 | 3-panel comparison | Fixed-window vs semantic vs structure-aware chunking on the same document with two sections and one table. Highlights how fixed-window can split a table mid-cell, while structure-aware treats the table as atomic. |
| 2 | `part-6/module-26/section-26.3.html` (Reasoning agents) | Fig 26.3.2 | 3-panel comparison | Think-then-Act vs Planner+Executor vs Adaptive Depth reasoning-agent architectures. Shows the cost-vs-capability trade for each. |
| 3 | `part-6/module-28/section-28.2.html` (Multi-agent topologies) | Fig 28.2.2 | 3-panel topology | Swarm, debate, and hierarchical topologies. Complements the existing foundational-3 figure with the advanced-3. |
| 4 | `part-6/module-28/section-28.2.html` (Multi-agent topologies) | Table 28.2.1 | Pattern selection table | 6 patterns x 6 criteria cheat sheet for picking supervisor / pipeline / mesh / swarm / debate / hierarchical. |
| 5 | `part-6/module-27/section-27.2.html` (MCP) | Fig 27.2.2 | Architecture diagram | MCP host containing LLM + N clients, connected via JSON-RPC over stdio/HTTP/SSE to N MCP servers (PostgreSQL, Filesystem, GitHub) each exposing Tools/Resources/Prompts. |
| 6 | `part-6/module-28/section-28.3.html` (HITL) | Fig 28.3.3 | Flowchart | Risk-routed approval flow: classify risk -> low (auto-execute) / medium (execute_and_log) / high (request_approval -> Slack -> approve|reject). |
| 7 | `part-8/module-40/section-40.1.html` (Voice agents) | Fig 40.1.2 | Stacked bar chart | Sequential (900 ms) vs streaming (280 ms first audio) voice-pipeline latency, with the 500 ms target line marked. |
| 8 | `part-9/module-42/section-42.10.html` (Research methodology) | Fig 42.10.2 | Horizontal scale | Cohen's kappa Landis-Koch bands (None/Slight/Fair/Moderate/Substantial/Almost perfect) with the publication floor (kappa >= 0.6) marked as a dashed line. |
| 9 | `part-9/module-43/section-43.5.html` (Multimodal eval) | Fig 43.5.2 | 2D matrix | Modality matrix with input modalities on rows (text/image/audio/video) and outputs on columns. Each cell labels the canonical eval regime and benchmark family. Rare cells are grayed out. |
| 10 | `part-7/module-33/section-33.4.html` (Multimodal production) | Fig 33.4.2 | 3-panel comparison | Three multimodal product shapes: conversational assistant, document QA, visual search. Each panel shows the model stack, latency budget, and use cases. |
| 11 | `part-7/module-34/section-34.2.html` (NER throughput) | Fig 34.2.1 | Log-scale bar chart | spaCy (10,000 docs/sec) vs REBEL fine-tuned (100 docs/sec) vs LLM API (1 doc/sec) on a logarithmic axis. Makes the 10,000x throughput gap visually obvious. |

Total added: 11 SVG figures + 1 comparison table = 12 visual elements across 9 section files.

## Quality bar checks

For each added visual:

- `viewBox` set with sane width/height; SVG flexes responsively via `style="max-width:100%;height:auto;"`
- `role="img"` and `aria-label` present with descriptive content (not just "diagram")
- Caption is a full sentence that tells the reader what to notice, not just what the figure is
- Each visual sits inside a `<figure class="illustration">` wrapper
- Each visual has a unique filter ID (`ch354shadow`, `rp263shadow`, etc.) to avoid SVG ID collisions when multiple figures share a page
- Each visual conveys information the surrounding prose does not (e.g., the kappa-scale visual gives a magnitude intuition that the Landis-Koch number list cannot)
- Numbers in the visuals (latency budgets, throughput, kappa thresholds) match the numbers in the prose

## Sections deliberately left alone

These sections came up in the candidate pool but were skipped:

- All `tools-of-the-trade` and section-X.5 reading-list modules (per brief)
- Sections with 2+ existing figures (e.g., 22.4 frontier VLMs, 22.6 pipeline vs native, 22.8 any-to-any, 23.1 3D Gaussian splatting, 26.1 agent foundations, 26.4 agent eval, 28.3 HITL except adding the risk-routing flowchart, 35.3 GraphRAG, 37.5b memory consolidation, 40.1 except adding the latency chart, 43.5 except adding the matrix)
- Sections that are pure curriculum lists or bibliography (per brief)
- Section 28.3.2 added the risk-routing flow even though the section already had 2 figures, because the existing figures are conceptual illustrations rather than the actual routing flow described in the LangGraph code; the new SVG matches the algorithmic structure directly

## Style consistency note

The added SVGs follow the R2 palette specified in the agent brief, which differs from the book's established internal palette (#3498db, #27ae60, etc., documented in `VISUAL_IDENTITY_R2.md`). The visual-identity director agent (#25) is expected to harmonize these in a separate pass; figure semantics, captions, sizing, and aria-labels are stable and should survive any palette retune.

## Verification

All 9 modified files load without HTML parse errors (each `<figure>` block contains balanced tags). Caption text is consistent with the figure-numbering scheme in each section. Cross-references are not needed for these inserts because each visual is introduced by surrounding prose that already named the concepts (chunking strategies, reasoning patterns, etc.).
