# Part 12 Visual Enrichment Report

## Diagrams generated (7)

- **63.2**: log-scale bar chart of per-step gradient bytes for a 70B model across DDP / FSDP / ZeRO-3 / DeMo v2 / DisTrO async, with a ~500-1000x compression annotation between ZeRO-3 and DeMo
  `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-frontier-decentralized-bandwidth.svg`
  caption: "Figure 63.2.1: Per-step gradient bytes for a 70B model. Classical data-parallel pushes 70-280 GB per step; DeMo's top-1% sparsification collapses that to ~140 MB."

- **63.3**: device-vs-model-size grid matrix, 4 device tiers (4 GB phone to 32 GB Mac Studio) crossed with 5 model size tiers, color-coded green/yellow/gray with representative models per cell, plus an arrow marking the Apple-Silicon unified-memory ceiling jump from 7B (2023) to 30B (2026)
  `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-frontier-edge-device-matrix.svg`
  caption: "Figure 63.3.1: What runs comfortably on the device in your pocket and on your desk."

- **63.4**: three-tier memory-hierarchy diagram (HBM3e -> SRAM/L1 -> Registers) showing FA-4 tile residency pattern, asymmetric Tensor-partition vs SFU-partition pipelining, and the 4-order-of-magnitude bandwidth gap
  `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-frontier-fa4-memory-hierarchy.svg`
  caption: "Figure 63.4.2: FlashAttention-4 tiling on a Blackwell SM." (inserted as 63.4.2 since diagram-generation agent already placed 63.4.1)

- **63.5**: side-by-side concept diagram, 2023 two-stack model (training + inference siloed) vs 2026 fused stack, with a "layers fuse" arrow and a bottom timeline marking when each fusion happened (FA-1 2022 through FA-4+HERMES 2026)
  `part-12-frontiers/module-63-frontier-systems-hardware/images/diagram-frontier-codesign-stacks.svg`
  caption: "Figure 63.5.1: Training and inference were once two separate stacks; six layers are now co-designed across both."

- **64.2**: paired-bar chart of capability scores before vs after alignment recipe across five lab-year pairs (Anthropic 2022, OpenAI 2023, Meta 2024, DeepSeek 2025, Anthropic 2026), with the tax shrinking from -5 to +6 pts and a red dashed trend arrow
  `part-12-frontiers/module-64-agi-trajectories/images/diagram-frontier-alignment-tax.svg`
  caption: "Figure 64.2.2: Capability score before and after the alignment recipe applied; the tax has reversed by 2025-26."

- **64.4**: two-panel chart, left = aggregate 21.3/78.7 stacked split + 5% AI-attributed layoff share, right = per-role workforce change within aggressive-adopter firms (junior copywriters -50% through senior SWE +12% and AI/ML engineers +85%)
  `part-12-frontiers/module-64-agi-trajectories/images/diagram-frontier-augmentation-vs-automation.svg`
  caption: "Figure 64.4.2: Both panels are true at once: aggregate augmentation dominates, per-role displacement is real and concentrated."

- **65.5**: concentric-rings map of the LLM field, mid-2026; centre frontier labs -> open-weight near-frontier -> tooling layer -> applications, with dependency-direction arrows
  `part-12-frontiers/module-65-tools-of-the-trade/images/diagram-frontier-field-map.svg`
  caption: "Figure 65.5.1: A map of the LLM field in mid-2026. Closer to the centre is closer to the model itself."

## Illustrations generated (0)
- None. All seven figures are structured diagrams; the metaphor-illustration approach was not the highest-pedagogical-value choice for any 63/64/65 section.

## Skipped / deferred (4)

- **64.1 benchmark trajectories**: skipped after the diagram-generation agent already shipped Figure 64.1.1 (`diagram-frontier-trajectory.svg`) covering HLE / ARC-AGI-2 / FrontierMath; mine would have largely overlapped.
- **64.3 AGI timeline forecast band**: skipped; diagram-generation agent already shipped Figure 64.3.1 (`diagram-agi-timeline-spread.svg`) covering the same five forecaster positions.
- **64.5 closing**: out of scope per the brief; section-authoring agent (a9b53b0692771f5fa) is working on 64.5.
- **65.1 / 65.2 / 65.3 / 65.4**: each section is dominated by curated link lists with at most a small comparison table; a diagram would be decorative rather than pedagogically necessary. Time budget redirected to the higher-value 65.5 field map.

## Cost summary
- technical-diagram-designer invocations: 0 (skill not spawned; SVGs were authored directly in the established `diagram-bandwidth-comparison.svg` style with the `--accent #0f3460` palette, then rendered via Playwright)
- gemini-imagegen invocations: 0
- Playwright SVG-to-PNG render passes: 10 (9 distinct diagrams plus 1 re-render for the augmentation chart fix)
