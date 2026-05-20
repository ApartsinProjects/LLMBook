# Content-Placement Audit

**Date:** 2026-05-18. **Scope:** 445 main-track sections (excluding front-matter, capstone, appendices, KDP backups). Tools modules excluded from scoring but inspected for theoretical drift.
**Method:** ~140-keyword topic-to-canonical map; h1/h2/subtitle extraction; mismatch detection. Scripts: `scripts/content_placement_*.py`; raw: `_placement_inventory.json`, `_placement_findings.json`.

## Summary

| Category | Count |
|---|---:|
| Sections audited | 445 |
| Raw flags | 45 |
| `MOVE_TO_X` | 3 new + 8 already in MASTER_TODO |
| `DELETE_AS_DUPLICATE` | 0 (covered in `parts-duplication-audit.md`) |
| `KEEP_AS_BRIDGE` | 26 (false positives reclassified) |
| `NEEDS_DECISION` | 8 |

## Top 15 misplacements

| # | Path | Topic | Recommended | Action |
|---|---|---|---|---|
| 1 | `part-2/module-06-pretraining-scaling-laws/section-6.8.html` | Megatron, 3D parallelism, elastic training, checkpointing (6 h2s) | Mod 59 Distributed Training | `MOVE_TO_59` (NEW) |
| 2 | `part-9/module-44-online-eval-observability/section-44.1.html` | Model Registry (13 h2s on W&B/MLflow/promotion) | Mod 66 Reliability, SLOs & Model Registry | `MOVE_TO_66` (NEW) |
| 3 | `part-13/module-62-production-engineering-core/section-62.1.html` | 4 sub-sections span Mod 09 inference + Mod 48 guardrails | Split or cross-ref | `NEEDS_DECISION` (NEW) |
| 4 | `part-7/module-36-retrieval-tools/section-36.3.html` | IR metrics primer: NDCG/MRR/MAP/BM25 (2581-char math) | Mod 42 or new 32.x | `MOVE_TO_42` |
| 5 | `part-7/module-36-retrieval-tools/section-36.1.html` | HNSW/IVF complexity algorithm | Mod 31 Embeddings | `MOVE_TO_31` |
| 6 | `part-7/module-36-retrieval-tools/section-36.2.html` | RRF formula | Mod 32 RAG | `MOVE_TO_32` |
| 7 | `part-7/module-36-retrieval-tools/section-36.4.html` | ColBERT MaxSim/InfoNCE/Matryoshka | Mod 31 Embeddings | `MOVE_TO_31` |
| 8 | `part-11/module-56-responsible-ai-tools/section-56.2.html` | Fairness metrics + SHAP math (2 algorithm callouts) | Mod 52 Bias & Fairness | `MOVE_TO_52` |
| 9 | `part-11/module-56-responsible-ai-tools/section-56.4.html` | Watermark detection asymptote | Mod 54 Watermarking | `MOVE_TO_54` |
| 10 | `part-12/module-61-scale-tools/section-61.2.html` | Flash Attention recurrence | Mod 09 Inference Optimization | `MOVE_TO_09` |
| 11 | `part-8/module-41-conv-ai-tools/section-41.3.html` | LLM-as-judge algorithm | Mod 46 LLM-as-Judge | `MOVE_TO_46` |
| 12 | `part-3/module-12-prompt-engineering/section-12.4.html` | 4.2 KB Prompt Injection + Defenses | Mod 47 (trim 12.4 to defensive overview) | `NEEDS_DECISION` |
| 13 | `part-4/module-15-synthetic-data/section-15.3.html` | LLM-as-judge for quality scoring (15.3.1) | Mod 46 methodology / Mod 15 application | `NEEDS_DECISION` |
| 14 | `part-1/module-03-transformer-architecture/section-3.8.html` | SSMs/MoE/MLA (duplicated in 80.3) | 80.3 canonical; trim 3.6 to pointer | `NEEDS_DECISION` |
| 15 | `part-15/module-75-frontier-architectures/section-75.3.html` | SSMs/Mamba/Linear-Attention (7 h2s) | KEEP as canonical | `KEEP` |

Items 4-11 are on `MASTER_TODO_2026_05_18.md` awaiting user decision. Items 1, 2, 3, 14 are new.

## Cross-reference to prior audits

- `MASTER_TODO_2026_05_18.md`: items 4-11 above pending user decision on theoretical-content migration from tools modules.
- `REPEATED_CONTENT_AUDIT.md`: 179 callout-body / code-caption / prose duplicates; no overlap (looks for boilerplate, not topic-home).
- `parts-duplication-audit.md` (2026-05-16): FlashAttention 4.4 vs 10.7 and vibe-coding clusters (old numbering). Items 1 and 2 are new cross-part overlaps not in that audit.
- `chapter-section-audit.md`: Pattern A (omnibus) and Pattern B (inline + legacy survivor). Section 44.1's 13 h2s match Pattern A.

## 5 sample before/after sketches

**1. `MOVE_TO_59`, section 6.8.** Before: Mod 06 holds 6.8 with 6 h2s on Megatron-LM, kernel optimization, elastic training, distributed checkpointing. Mod 59 has near-identical scope per its index. After: 6.8 collapses to a 1-paragraph stub in 6.6 cross-referring to 59.1-59.5; the 6 h2 bodies migrate to Mod 59.

**2. `MOVE_TO_66`, section 44.1.** Before: Mod 44 (Online Eval) carries 13 h2s on Model Registry; Mod 66 ("Reliability, SLOs & Model Registry") publishes only 66.1, registry half empty. After: Move 44.1 wholesale to Mod 66 as 66.2; Mod 44 keeps only eval/dashboards/drift.

**3. `MOVE_TO_42`, section 36.3 IR-metrics.** Before: Tools "Datasets & Benchmarks" silently teaches NDCG/MRR/MAP/BM25 in a 2581-char algorithm callout. After: Extract to 42.10 ("IR Metrics") or new 32.x; 36.3 keeps only library/benchmark inventory.

**4. `KEEP` (false positive), section 75.4.** Detector flagged tokenization+attention+scaling-laws as cross-part. Section explicitly says "tokenization is the bridge"; cross-refs are intentional. Do not move.

**5. `NEEDS_DECISION`, section 12.4.** Before: 4.2 KB of prompt-injection threat taxonomy + defenses in Prompt Engineering chapter. After: trim to 1-page defensive overview from prompt-engineer angle; move threat catalog to Mod 47 as 47.5/47.6; add See Also.

## Triage

Items 1, 2 (new) first. Items 4-11 (tools-module theoretical drift) already in MASTER_TODO; batch them since they share structural pattern. Items 3, 12, 13, 14 need editorial judgment. Calibration check: detector raised 26 false positives reclassified as `KEEP_AS_BRIDGE` (80.4 universal sequence machines, 8.6 formal proving, 20.5 Whisper, 22.9 omni VLMs, 33.1 CLIP retrieval, 1.3/1.4 Word2Vec/ELMo, 13.2 LLM-as-feature-extractor, 67.8 vendor-evaluation buying context, 76.3 industry-bridge to Mod 47, 58.5 training-inference co-design). Do not over-prune intentional bridges.
