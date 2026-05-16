# Part 12 Comprehensive Enrichment Report

Date: 2026-05-16. Coverage: modules 63, 64, 65. Approach: full callout palette per brief, no diagram duplication (other agent had ~11 diagrams in flight; all kept as-is, hero openers wired).

## Callouts added per section

| Section | pathway | big-picture | key-insight (Mental Model) | practical-example (Real-World) | warning | tip | fun-note | research-frontier | thesis-thread | key-takeaway | self-check | bibliography | looking-back |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 63.1 Beyond NVIDIA | + | + | + (interconnect dominates) | + (Cerebras/OpenAI $10B+) | + (pflops misleading) | + (vendor-neutral dashboards) | | | | + | + | + | |
| 63.2 Decentralized Training | + | + | + (DeMo as steganography) | + (Nous Psyche 1B run) | + (not yet frontier parity) | | + (DGC 2017 ancestor) | + | | + | + | + | |
| 63.3 Edge LLMs | + | + | (existing reframed) | + (Apple Intelligence routing) | | + 2x (cloud-vs-edge, QAT) | | | | + | + | + | |
| 63.4 FlashAttention-4 | + | + | + (memory hierarchy is bottleneck) | + (DeepSeek V4 CSA lag) | + 2x (Blackwell-specific, kernel gating) | | | | | + | + | + | |
| 63.5 Co-Design | + | + | (existing kept) | + (Anthropic Computer Use cascade) | (existing kept) | | | | + | + | + | + | |
| 64.1 Frontier Benchmarks | + | + | + (emergence is threshold-crossing) | + (DeepSeek-R1 emergence) | (existing kept) | (existing kept) | + (Gemini 2.5 Project Euler) | | | + | + | + | |
| 64.2 Alignment | + | + | + (alignment tax shrinking) | + (CAI vs DPO vs GRPO compared) | (existing kept) | | | + | | + | + | + | |
| 64.3 AGI Timelines | + | + | (existing kept) | | + (definition shopping) | (existing kept) | | | | + | + | + | |
| 64.4 Economic | + | + | (existing kept) | + (augmentation in SWE teams) | (existing kept) | + (review-location test) | | | | + | + | + | |
| 64.5 Closing essay | | | (existing kept) | | | | | | | | | + (foundational refs) | + (three theses) |
| 65.1 Platforms | + | + | + (rigor-vs-recency tradeoff) | | | | | | | + | | + | |
| 65.2 Libraries | + | + | | | | + (start small, then graduate) | | | | | | + | |
| 65.3 Benchmarks | + | + | | + (SWE-bench Verified 2026) | + (saturated not solved) | | | | | + | | + | |
| 65.4 Models | + | + | (existing kept) | + (vLLM 2025 inflection) | + (stars are vanity) | | | | | + | | + | |
| 65.5 External Reading | + | + | + (half-life of tool lists) | | | + 2x (lurk first; three papers) | | | | + | | + (bullet list converted) | |

## Illustrations / heroes

- Module 63 chapter-opener.png: already on disk (May 16 10:04); WIRED into module-63 index.html.
- Module 64 chapter-opener.png: already on disk (May 16 10:04); WIRED into module-64 index.html.
- Module 65 chapter-opener.png: already on disk (May 16 10:04); WIRED into module-65 index.html.
- No new gemini-imagegen calls were needed. Existing diagrams already cover the conceptual surface (bandwidth-comparison, demo-sparse-gradient, edge-device-matrix, flashattention-timeline, fa4-memory-hierarchy, codesign-stacks, frontier-trajectory, alignment-tax, alignment-stack, agi-timeline-spread, augmentation-vs-automation, augmentation-fork, field-map). The diagram agent had wired most of these in parallel; I added callouts AROUND them rather than duplicating.

## Files edited (15 total)

- part-12-frontiers/module-63-frontier-systems-hardware/index.html (hero wire-in)
- part-12-frontiers/module-63-frontier-systems-hardware/section-63.1.html
- part-12-frontiers/module-63-frontier-systems-hardware/section-63.2.html
- part-12-frontiers/module-63-frontier-systems-hardware/section-63.3.html
- part-12-frontiers/module-63-frontier-systems-hardware/section-63.4.html
- part-12-frontiers/module-63-frontier-systems-hardware/section-63.5.html
- part-12-frontiers/module-64-agi-trajectories/index.html (hero wire-in)
- part-12-frontiers/module-64-agi-trajectories/section-64.1.html
- part-12-frontiers/module-64-agi-trajectories/section-64.2.html
- part-12-frontiers/module-64-agi-trajectories/section-64.3.html
- part-12-frontiers/module-64-agi-trajectories/section-64.4.html
- part-12-frontiers/module-64-agi-trajectories/section-64.5.html
- part-12-frontiers/module-65-tools-of-the-trade/index.html (hero wire-in)
- part-12-frontiers/module-65-tools-of-the-trade/section-65.1.html
- part-12-frontiers/module-65-tools-of-the-trade/section-65.2.html
- part-12-frontiers/module-65-tools-of-the-trade/section-65.3.html
- part-12-frontiers/module-65-tools-of-the-trade/section-65.4.html (also removed duplicate chapter-nav block)
- part-12-frontiers/module-65-tools-of-the-trade/section-65.5.html

## Coordination notes

- The Part-12 diagram agent (a3aedf6c363b1debe) inserted `diagram-frontier-*.svg` figures into 63.2, 63.3, 63.5, 64.2, 64.4, 65.5 during this task; my edits worked around all in-flight figure inserts and several "file modified since read" retries succeeded after re-reads. No half-inserted figure blocks were observed at final state.
- All callouts use canonical class names (`pathway`, `big-picture`, `key-insight`, `practical-example`, `warning`, `tip`, `fun-note`, `research-frontier`, `thesis-thread`, `key-takeaway`, `self-check`, `bibliography`, `looking-back`, `note`). No `fun-fact` or `why-it-matters` used.
- Section-64.5 retains BOTH looking-back callouts (existing "softmax through-line" + new "three theses"); they read complementary rather than duplicative.
- Section 65.4 had a duplicate broken `<nav class="chapter-nav">` block at the bottom; removed as part of the enrichment.
