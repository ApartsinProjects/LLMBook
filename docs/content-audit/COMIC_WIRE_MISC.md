# Comic Wiring Report: Chapters 24, 26, 27, 29, 56, 59, 61

Scope: the 15 cartoon-comic JPEGs from `.book-update/comic-manifest.jsonl` whose
`chap_sec` begins with 24., 26., 27., 29., 56., 59., or 61. All images were
pre-generated and on disk; this task wired each into its section as a
`<figure class="illustration">` with a screen-reader `alt` and a metaphor-to-lesson
`figcaption`. Images were not modified or regenerated.

Date: 2026-05-20. Branch: v2.0.

## Summary

- Wired: 15 / 15
- Skipped (missing image): 0
- Audit (P0+P1+P2, 12 touched files): 0 issues. No FIGURE_SEQUENCE,
  DUP_FIGURE_NUM, BROKEN_FIGURE_REF, or MISSING_IMG_DIMS.
- `scripts/fix_caption_order_only.py` run on every touched file: 0 reorders
  needed (figure numbering already sequential in document order).
- All 15 images carry `width="1024" height="1024"`.

## Key finding: most comics were already half-wired under draft filenames

11 of the 15 comics were already placed in their sections during an earlier
session, but pointing at ad-hoc draft filenames (e.g. `comic-dexterity-ceiling.jpg`)
rather than the canonical manifest filenames (e.g. `comic-24.6-88-vla-limitations.jpg`).
Both the draft and the canonical JPEGs exist on disk. To wire the manifest's
canonical assets without creating duplicate same-joke figures (which would crowd
the sections, against the task's placement guidance), the existing `<img src>` was
repointed to the canonical filename at the same anchor and the `alt` text refreshed.
The superseded draft JPEGs were left on disk untouched (not referenced anywhere now).

4 comics were genuinely new figures inserted at a fresh anchor with a new prose
reference: 29.4-103, 56.2-64, 59.3-78, and 29.1-101 (the last replaced a cold PNG
diagram of the identical self-debug loop at the same anchor).

## Per-comic disposition

| chap_sec | num | filename (canonical) | section file | figure | action |
|----------|-----|----------------------|--------------|--------|--------|
| 24.6  | 88  | comic-24.6-88-vla-limitations.jpg | part-5-multimodal-llms/module-24-vla-models/section-24.6.html | Fig 24.6.1 | repointed from draft `comic-dexterity-ceiling.jpg` (anchor: 24.6.2 Dexterity Ceiling) |
| 24.6  | 89  | comic-24.6-89-vla-limitations.jpg | part-5-multimodal-llms/module-24-vla-models/section-24.6.html | Fig 24.6.2 | repointed from draft `comic-nested-safety-vests.jpg` (anchor: 24.6.3 Safety Story) |
| 24.13 | 91  | comic-24.13-91-sim-to-real-gap.jpg | part-5-multimodal-llms/module-24-vla-models/section-24.13.html | Fig 24.13.1 | repointed from draft `comic-domain-randomization-globe.jpg` (anchor: 24.13.2 Domain Randomization) |
| 26.6  | 94  | comic-26.6-94-memory-architecture-for-agents.jpg | part-6-agentic-ai/module-26-ai-agents/section-26.6.html | Fig 26.6.1 | repointed from draft `comic-dialogue-vs-process-memory.jpg` (anchor: dialogue-vs-process key insight) |
| 27.5  | 98  | comic-27.5-98-retrieval-as-a-tool-call.jpg | part-6-agentic-ai/module-27-tool-use-protocols/section-27.5.html | Fig 27.5.2 | repointed from draft `comic-crag-stamps.jpg` (anchor: 27.5.3 corrective grading) |
| 29.1  | 101 | comic-29.1-101-code-generation-agents.jpg | part-6-agentic-ai/module-29-specialized-agents/section-29.1.html | Fig 29.1.2 | replaced cold PNG `ch25-code-agent-debug-loop.png` (same self-debug-loop anchor; avoids crowding) |
| 29.4  | 103 | comic-29.4-103-production-agentic-coding-systems.jpg | part-6-agentic-ai/module-29-specialized-agents/section-29.4.html | Fig 29.4.2 | NEW figure inserted after the vendor-landscape Table 29.4.1, with prose ref |
| 56.1  | 60  | comic-56.1-60-platforms.jpg | part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.1.html | Fig 56.1.1 | repointed from draft `comic-venn-buyers.jpg` (anchor: 56.1.1 governance platforms) |
| 56.2  | 63  | comic-56.2-63-libraries-and-frameworks.jpg | part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.2.html | Fig 56.2.1 | repointed from draft `comic-fairness-scales.jpg` (anchor: 56.2.1 fairness libraries) |
| 56.2  | 64  | comic-56.2-64-libraries-and-frameworks.jpg | part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/section-56.2.html | Fig 56.2.2 | NEW figure inserted after 56.2.5 watermarking list, with prose ref |
| 59.1  | 70  | comic-59.1-70-distributed-training-fundamentals.jpg | part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.1.html | Fig 59.1.1 | repointed from draft `comic-three-parallelism-kitchens.jpg` (anchor: 59.1.2 Three Axes) |
| 59.2  | 72  | comic-59.2-72-zero-and-fsdp.jpg | part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.2.html | Fig 59.2.1 | repointed from draft `comic-zero-mountain-climbers.jpg` (anchor: 59.2.2 ZeRO Progression) |
| 59.3  | 75  | comic-59.3-75-tensor-parallelism.jpg | part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.3.html | Fig 59.3.1 | repointed from draft `comic-infiniband-strain.jpg` (anchor: tensor-parallel interconnect ceiling) |
| 59.3  | 78  | comic-59.3-78-tensor-parallelism.jpg | part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.3.html | Fig 59.3.3 | NEW figure inserted after 59.3.7 "When Tensor Parallelism Breaks", with prose ref (ops/observability theme; no 59.5 section exists in this file) |
| 61.1  | 81  | comic-61.1-81-platforms.jpg | part-12-llm-systems-at-scale/module-61-scale-tools/section-61.1.html | Fig 61.1.1 | repointed from draft `comic-ethernet-vs-infiniband.jpg` (anchor: InfiniBand-premium key insight) |

## Notes

- Placement deviations from the manifest's literal anchor: for the 11 repointed
  comics, the figure was kept at the anchor an earlier session had already chosen
  (typically the section/subsection head), which is an equivalent home for the same
  joke and avoided moving + re-crowding. For num 78 the manifest named "59.5
  Operations and observability", but section-59.3.html has no such subsection, so
  the checkpoint-resilience comic went under 59.3.7 ("When Tensor Parallelism
  Breaks"), the closest failure/recovery anchor in that file.
- No em dashes used in any added alt text, caption, or prose.
- Superseded draft JPEGs still on disk (now unreferenced): comic-dexterity-ceiling.jpg,
  comic-nested-safety-vests.jpg, comic-domain-randomization-globe.jpg,
  comic-dialogue-vs-process-memory.jpg, comic-crag-stamps.jpg, comic-self-debug-strip.jpg
  (never wired), ch25-code-agent-debug-loop.png, comic-venn-buyers.jpg,
  comic-fairness-scales.jpg, comic-three-parallelism-kitchens.jpg,
  comic-zero-mountain-climbers.jpg, comic-infiniband-strain.jpg,
  comic-3am-checkpoint.jpg (never wired), comic-ethernet-vs-infiniband.jpg.
  Left in place per the "do not modify or regenerate images" rule; a separate
  cleanup pass could prune them.
