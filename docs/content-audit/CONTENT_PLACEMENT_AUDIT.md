# Content-Placement Audit

**Date:** 2026-05-18.
**Scope:** 445 main-track section files across 83 chapters in 16 parts. Front-matter, capstone, appendices, and `tools-of-the-trade` modules excluded for misplacement scoring, but tools modules are inspected for theoretical drift (signal 1).
**Method:** Build a topic-keyword to canonical-chapter map (~140 keywords), extract h1/h2/subtitle from every section, flag mismatches. Auxiliary scripts under `scripts/content_placement_*.py`; raw findings in `_placement_inventory.json` + `_placement_findings.json`.

## Summary stats

| Action category | Count | Notes |
|---|---:|---|
| Total sections audited | 445 | Excludes KDP backups, front-matter, capstone, appendices. |
| Sections flagged | 45 | After heuristic detection. |
| `MOVE_TO_X` (high-confidence move) | 8 | Cross-part contamination with strong canonical home. |
| `DELETE_AS_DUPLICATE_OF_X` | 0 | Pure duplicates already covered in `parts-duplication-audit.md`. |
| `KEEP_AS_BRIDGE` (intentional cross-ref) | 26 | Reviewed and re-classified from the 36 raw cross-part hits. |
| `NEEDS_DECISION` | 11 | Theoretical content in tools-of-trade modules + 3 borderline cases. |

The detector also produced 36 raw "cross-part" topic hits. Manual review reclassified 26 as `KEEP_AS_BRIDGE` (e.g., 80.3 SSMs in Frontier Architectures, 80.4 LLMs-as-universal-sequence-machines, 8.6 formal proving, 33.1 CLIP for multimodal retrieval, 20.5 Whisper, 22.9 omni VLMs). The 10 with strong claim are listed below.

## Top 15 highest-confidence misplacements

| # | Section path | Topic | Current home | Recommended home | Action |
|---|---|---|---|---|---|
| 1 | `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.8.html` | Megatron-LM, 3D parallelism, elastic training, distributed checkpointing | Mod 06 (Pre-training & Scaling Laws) | Mod 59 (Distributed Training Systems) | `MOVE_TO_59` |
| 2 | `part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.1.html` | Model Registry (13 h2 subsections on W&B/MLflow/promotion stages) | Mod 44 (Online Eval & Observability) | Mod 66 (Reliability, SLOs & Model Registry) | `MOVE_TO_66` |
| 3 | `part-7-.../module-36-retrieval-tools/section-36.3.html` | IR metrics primer (NDCG, MRR, MAP, BM25 derivations, 2581-char math block) | Mod 36 (Retrieval Tools — TOTT) | Mod 42 (Evaluation Foundations) or new section 32.x | `MOVE_TO_42` (already on MASTER_TODO) |
| 4 | `part-7-.../module-36-retrieval-tools/section-36.1.html` | Vector-index complexity (HNSW/IVF formal analysis in algorithm callout) | Mod 36 (TOTT) | Mod 31 (Embeddings, Vector DBs) | `MOVE_TO_31` (MASTER_TODO) |
| 5 | `part-7-.../module-36-retrieval-tools/section-36.2.html` | RRF formula derivation inside algorithm callout | Mod 36 (TOTT) | Mod 32 (RAG Fundamentals) | `MOVE_TO_32` (MASTER_TODO) |
| 6 | `part-7-.../module-36-retrieval-tools/section-36.4.html` | ColBERT MaxSim / InfoNCE / Matryoshka math | Mod 36 (TOTT) | Mod 31 (Embeddings, late-interaction) | `MOVE_TO_31` (MASTER_TODO) |
| 7 | `part-11-.../module-56-responsible-ai-tools/section-56.2.html` | Fairness metrics derivations + SHAP math (2 algorithm callouts) | Mod 56 (TOTT) | Mod 52 (Bias, Fairness, Disparate Impact) | `MOVE_TO_52` (MASTER_TODO) |
| 8 | `part-11-.../module-56-responsible-ai-tools/section-56.4.html` | Watermark detection asymptote derivation | Mod 56 (TOTT) | Mod 54 (Watermarking & Provenance) | `MOVE_TO_54` (MASTER_TODO) |
| 9 | `part-12-.../module-61-scale-tools/section-61.2.html` | Flash Attention recurrence algorithm callout | Mod 61 (TOTT) | Mod 09 (Inference Optimization) | `MOVE_TO_09` (MASTER_TODO) |
| 10 | `part-8-.../module-41-conv-ai-tools/section-41.3.html` | LLM-as-judge algorithm in datasets-and-benchmarks section | Mod 41 (TOTT) | Mod 46 (LLM-as-Judge) | `MOVE_TO_46` (MASTER_TODO) |
| 11 | `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.1.html` | Latency optimization details cover same ground as Mod 09 inference-opt + Mod 48 guardrails; 4 sub-sections (62.1.1 Latency, 62.1.2 Backpressure, 62.1.3 Production Guardrails, 62.1.4 Memory) span 3 canonical homes | Mod 62 | NEEDS triage: split or cross-ref | `NEEDS_DECISION` |
| 12 | `part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html` | 4.2 KB of Prompt Injection Attacks + Defense Patterns | Mod 12 (Prompt Engineering) | Mod 47 (Adversarial Security & Red Team) | `NEEDS_DECISION` (defense-from-prompt-engineer angle could justify keeping a 1-page summary + xref) |
| 13 | `part-4-training-adaptation/module-15-synthetic-data/section-15.3.html` | LLM-as-Judge for quality scoring (15.3.1) | Mod 15 (Synthetic Data) | Mod 46 (LLM-as-Judge) for methodology; Mod 15 retains the application angle | `NEEDS_DECISION` |
| 14 | `part-16-.../module-80-frontier-architectures/section-80.3.html` | SSMs / Mamba / Linear-Attention (substantive 7 h2s, also covered briefly in 3.6) | Mod 80 (Frontier Arch) — canonical | Mod 3 (Transformer Variants) — too brief there | `KEEP` 80.3 as canonical; trim 3.6 to be a pointer (READ-ONLY noted) |
| 15 | `part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.4.html` | vLLM in Docker, TGI in Docker (deep-dive into specific serving libs) | Mod 65 (Containers) | KEEP — containerization is the angle | `KEEP_AS_BRIDGE` |

Items 3-10 are already on `MASTER_TODO_2026_05_18.md` ("11 algorithm/key-insight callouts in tools-of-the-trade modules"). Listed here for completeness because the user asked for one consolidated triage view. Item 1, 2, and 11 are new findings from this audit.

## Cross-reference to prior audits (avoid duplicate effort)

- `MASTER_TODO_2026_05_18.md` already tracks items 3-10 above as "11 algorithm/key-insight callouts in tools-of-the-trade modules" needing user decision.
- `REPEATED_CONTENT_AUDIT.md` covers callout-body / code-caption / prose-paragraph duplicates (179 blocks). No overlap with this audit; that one looks for boilerplate, this one looks for topic-home mismatches.
- `parts-duplication-audit.md` (2026-05-16) identifies stale-numbered leftovers + concept-duplication clusters (FlashAttention 4.4 vs 10.7, vibe-coding M43 vs M45). Those remain valid; this audit confirms 6.8 vs 59 and 44.1 vs 66 as the two new cross-part overlaps in the v2.0 layout.
- `chapter-section-audit.md` documents Pattern A (single omnibus) and Pattern B (inline content + legacy survivor). Items 11 and 12 in my list above may benefit from Pattern-A-style splits.

## 5 sample before/after sketches

### Sample 1 — Move 6.8 to Module 59
- **Before:** Section 6.8 lives in Mod 06 (Pre-training & Scaling Laws). 6 h2s on Megatron-LM, kernel optimization, elastic training, distributed checkpointing, streaming datasets. Module 59 (Distributed Training Systems) has near-identical scope per its index ("3 orthogonal axes of parallelism, ZeRO/FSDP, Megatron, pipeline scheduling").
- **After:** 6.8 becomes a 1-paragraph stub in 6.6 ("Distributed Training, briefly"): "Megatron-LM and the full production-systems story are covered in detail in Section 59.1-59.5." Move the 6 h2 bodies into Mod 59 (likely 59.2/59.3/59.4 new subsections). Update cross-refs from Mod 06 to point at Mod 59.

### Sample 2 — Move 44.1 to Module 66
- **Before:** Section 44.1 in Mod 44 (Online Eval & Observability) has 13 h2 subsections on Model Registry (W&B, MLflow, promotion, aliases, validation gates, lifecycle stages). Module 66 is titled "Reliability, SLOs & Model Registry" but currently has only 66.1 published, covering reliability patterns. The registry half of 66's title is empty.
- **After:** Move 44.1 wholesale to Mod 66 as 66.2 ("Model Registry & Deployment Workflows"). Keep a 1-paragraph note in 44.0 / 44.x explaining where the registry workflow lives. Mod 44 then focuses purely on online eval, dashboards, drift, and observability.

### Sample 3 — Migrate 36.3 IR-metrics primer to Module 42 or new 32.x
- **Before:** Inside a tools-of-the-trade "Datasets & Benchmarks" section, an algorithm callout silently teaches NDCG, MRR, MAP, Recall@k, BM25 with full math derivations (2581 chars). Tools modules are reference catalogs, not the place to introduce formal metrics.
- **After:** Extract the algorithm callout into a new top-level section (proposed: 42.10 "Information-Retrieval Metrics" or a 32.x "Evaluating Retrieval Quality"). 36.3 then contains only library/benchmark inventory and cross-links to the new home.

### Sample 4 — Keep 80.4 as bridge (DO NOT MOVE)
- **Before:** Section 80.4 ("Beyond Text: LLMs as Universal Sequence Machines") in Mod 80 (Frontier Architectures) mentions tokenization, attention, scaling laws (canonical homes: Mod 01, 02, 06). The detector flagged this as cross-part.
- **After:** Verified intentional. The section explicitly builds the bridge: "tokenization is the bridge between a new domain and the entire LLM ecosystem." Keep with the existing cross-refs to Mod 01/02/06. Note: this is exactly the kind of false positive we should not chase.

### Sample 5 — Cross-ref or trim 12.4 prompt-injection content
- **Before:** Section 12.4 in Mod 12 (Prompt Engineering) has 4.2 KB of "Prompt Injection Attacks" + "Defense Patterns" (sections 12.4.1, 12.4.2). Mod 47 (Adversarial Security & Red Team) is the canonical home for adversarial-security threat modeling.
- **After:** Replace 12.4.1-12.4.2 bodies with a 1-page "Prompt-engineering defensive patterns" overview that pulls only the defensive techniques relevant to a prompt-engineer audience (delimiter hygiene, output schema validation). Move the threat taxonomy + attack catalog to Mod 47 as 47.5 or 47.6. Insert See Also callout in 12.4 pointing at Mod 47.

## Notes on detection methodology

- Misplacement signals: theoretical-in-tools (algorithm/proof callouts inside the 14 tools-of-the-trade modules), topic-path-mismatch (h1/h2 keyword matches a canonical chapter in a different part), library-deep-dive-in-main (>=3 library-shortcut callouts + library name in h1 within a non-tools chapter).
- False-positive sources caught and filtered: keyword "discovery" matching "Problem-Discovery"; "embeddings" matching foundational Word2Vec content; "scaling law" matching "inference-aware scaling laws" in 58.5 (legitimate co-design topic).
- Inventory files: `docs/content-audit/_placement_inventory.json` (module scopes + 445 section summaries) and `docs/content-audit/_placement_findings.json` (raw heuristic hits).

## Triage recommendation

Highest impact items 1 (6.8 to 59) and 2 (44.1 to 66) are new findings. Address those first. Items 3-10 are already in the MASTER_TODO backlog awaiting user decision; if the user wants to act on tools-module theoretical content, take all 8 in a single coordinated migration since they are structurally identical. Items 11-13 need editorial judgment on whether to trim+cross-ref or full-move. Items 14-15 are the calibration check: confirm we are not over-pruning intentional bridge sections.
