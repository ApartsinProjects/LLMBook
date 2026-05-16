# Diagram Generation Report

Date: 2026-05-16. Cap was 15 diagrams; 15 shipped.

## Generated diagrams (15)

1. `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-bandwidth-comparison.{svg,png}` | section-63.1.html, after the comparison table | Figure 63.1.1 | Log-scale bar chart of A100 / H100 / MI355X / B200 / Groq LPU / Cerebras CS-3 effective memory bandwidth.
2. `part-3-working-with-llms/module-16-tools-of-the-trade/images/diagram-price-quality-pareto.{svg,png}` | section-16.4.html, after the table | Figure 16.4.1 | Price vs LM Arena Elo scatter with dashed Pareto frontier through eight mid-2026 models.
3. `part-10-idea-to-product/module-42-strategy-prioritization/images/diagram-build-vs-buy-tree.{svg,png}` | section-42.2.html, before the comparison table | Figure 42.2.1 | Five-question decision tree (Q1 differentiation, Q2 sovereignty, Q3 refresh, Q4 utilization, Q5 IP) with six endpoints.
4. `part-10-idea-to-product/module-46-compute-planning/images/diagram-gpu-bandwidth.{svg,png}` | section-46.1.html, after the GPU table | Figure 46.1.1 | Bar chart of L40S / A100 / H100 / H200 / MI355X / B200 bandwidth, colored by workload sweet spot.
5. `part-10-idea-to-product/module-47-scaling-economics/images/diagram-utilization-breakeven.{svg,png}` | section-47.2.html, after the cost table | Figure 47.2.1 | Cost-per-1M-tokens vs utilization curve crossing the flat OpenRouter line at ~80%.
6. `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-flashattention-timeline.{svg,png}` | section-63.4.html, after sect 63.4.1 intro | Figure 63.4.1 | Horizontal timeline of FA-1 (A100) -> FA-2 -> FA-3 -> FA-4 (Blackwell), each paired with the hardware change driving it.
7. `part-12-frontiers/module-64-agi-trajectories/images/diagram-agi-timeline-spread.{svg,png}` | section-64.3.html, after the timeline table | Figure 64.3.1 | Horizontal bar chart of Amodei / Hassabis / Metaculus / Polymarket / 80kHours AGI forecasts with median and 25-75% intervals.
8. `part-12-frontiers/module-64-agi-trajectories/images/diagram-frontier-trajectory.{svg,png}` | section-64.1.html, after the benchmark table | Figure 64.1.1 | Three-line chart of HLE, ARC-AGI-2, FrontierMath scores from Jan 2025 to May 2026 with 90% expert baseline.
9. `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-demo-sparse-gradient.{svg,png}` | section-63.2.html, after table | Figure 63.2.2 (parallel agent already used 63.2.1) | Three-step DeMo sequence (local momentum -> sparse sync -> global merge) plus bandwidth comparison DDP/FSDP/DiLoCo/DeMo.
10. `part-12-frontiers/module-64-agi-trajectories/images/diagram-alignment-stack.{svg,png}` | section-64.2.html, after practical-example | Figure 64.2.1 | Three-layer defense (RLHF -> Constitution/SAE -> output classifier) with three attack arrows (jailbreak, prompt injection, unsafe completion).
11. `part-12-frontiers/module-64-agi-trajectories/images/diagram-augmentation-fork.{svg,png}` | section-64.4.html, after labor data table | Figure 64.4.1 | 2025 measured 78.7/21.3 augmentation/automation split forking to 2027 Scenario A (72/28) vs Scenario B (52/48); three arbitrating indicators listed.
12. `part-10-idea-to-product/module-47-scaling-economics/images/diagram-cost-stack.{svg,png}` | section-47.1.html, after sect 47.1.2 prose | Figure 47.1.1 | Stacked bar (50% inference / 30% orchestration / 20% integration) plus per-layer explanation and pseudo-formula breakdown.
13. `appendices/appendix-f-agent-frameworks/images/diagram-framework-selection.{svg,png}` | section-f.1.html, before the selection comparison table | Figure F.1.1 | Decision tree splitting single vs multi-agent then typing / open-weight / state / code-execution / .NET to seven endpoints (PydanticAI, smolagents, OpenAI SDK, LangGraph, AutoGen, Semantic Kernel, CrewAI).
14. `appendices/appendix-d-langchain/images/diagram-rag-pipeline.{svg,png}` | section-d.3.html, opening "Putting It All Together" | Figure D.3.2 | Two-lane RAG pipeline (offline ingest: loader -> splitter -> embed -> vector store; online query: embed -> retrieve -> rerank -> compress -> generate) with failure-points and build-sequence callouts.
15. `part-1-foundations/module-04-transformer-architecture/images/diagram-transformer-anatomy.{svg,png}` | module-04 index.html, after the big-picture callout | Figure 4.0.2 | Seven-stage transformer anatomy (tokens -> embedding -> position -> N-block (attn + MLP) -> final LN -> head -> sample) with tensor shapes and 7B parameter breakdown.

## Deferred / skipped (4)

- VLA architecture + 3D Gaussian Splatting + world-model rollout (part-7 ch 32): destination is being authored by section-authoring agent (a9b53b06...); audit explicitly told this writer to wait. Deferred to a follow-up pass once Ch 32 is non-stub.
- Attribution graph for interpretability (section-62.3.html): destination is in part-12 frontier-theory; cost cap reached. Defer.
- Top-level book map for toc.html or front-matter: a dependency diagram already lives at front-matter/fm-what-this-book-covers.html (Figure FM.3.1). Skipped to avoid duplication; the transformer-anatomy diagram (#15) used the cross-cutting slot instead, since it sits in every later chapter's prerequisites.
- Alignment-thesis unifying diagram (part-7 index): part-7/module-32 is still being authored by the section agent; deferred to avoid conflict.

## Notes

- All SVGs use the established book palette (#1a4078 data, #1f7a3a model, #722f8a control, #d4b96a store, #b3401b warning, #1a1a2e text) with no gradients, no drop shadows.
- All `<figure class="diagram">` blocks reference the `.svg` (modern readers); the matching `.png` (rasterized via resvg_py at 1400 px) ships alongside for legacy fallbacks.
- One numbering collision (63.2) resolved by bumping the DeMo sequence figure to 63.2.2 because the parallel Frontier-update agent shipped a bandwidth bar chart as 63.2.1 mid-task.
- Helper scripts created: `scripts/rasterize_diagram.py`, `scripts/clean_svg_comments.py` (strips invalid `--` inside XML comments).
