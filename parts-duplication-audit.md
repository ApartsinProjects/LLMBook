# Cross-Part Duplication Audit

Audit date: 2026-05-16. Scope: 286 non-Tools-of-the-Trade section HTML files across the 12 parts of the LLMBook. Read-only audit; no files modified.

## Summary

- Sections scanned: 286 (Tools-of-the-Trade modules 06, 12, 16, 21, 25, 30, 33, 36, 39, 50, 60, 65 excluded).
- **In-part literal duplicates (same module, same title)**: 6 confirmed pairs (modules 46, 47).
- **Cross-part literal duplicates (same h1/title in different parts)**: 2 confirmed (Post-Launch Monitoring 48.4 vs 49.1; What 2026 Settled 33.11 vs 64.5).
- **Stale-numbered leftover files** (filename does not match its h1/title or content uses obsolete chapter numbers): 14 files identified.
- **Concept-duplication clusters with no canonical anchor**: 5 (FlashAttention; Cost / unit economics; ROI; Production observability; Agent observability).
- **Concept-duplication clusters that are healthy (single canonical with backrefs)**: 7 (Attention math, Tokenization, RAG, Hallucination, RLHF/DPO, MCP, LLM-as-judge).
- **Named-case-without-canonical references**: 0 cases of the "Air Canada chatbot" pattern within `part-*/module-*/section-*.html`; Air Canada is correctly anchored in `appendices/appendix-u-war-stories/`. DeepSeek-R1 is mentioned in 30+ files but each appearance is a passing model reference, not a duplicated training case study.
- **Recommended canonical placements**: 9 (see "Recommended consolidations" below).

The most serious finding is structural, not topical: **Modules 46, 47, 48 (Part X) contain near-literal duplicate section files** (two files per topic in M46/M47, plus a 48.5/48.6 pair orphaned from M48's index). These appear to be content imports from old chapter 31/33/34/35 that were never reconciled with the new numbering, and they continue to drive cost / ROI / observability concept duplication with Part VIII. Part XI module-58 and -59 contain analogous leftover files with old chapter-27 numbering.

---

## Concept clusters

### Healthy backref patterns

**Attention math** (HEALTHY).
Canonical: Sections 3.2 ("Attention Mechanism"), 3.3 ("Scaled Dot-Product & Multi-Head Attention"), 4.1-4.3 (Part I). Module 04 is the deepest treatment.
Also discussed: 7.2/7.6 (Part II pretraining objectives, brief), 32.3 (cross-attention in 3D Gaussian splatting), 61.3 (alternative architectures: Mamba, RWKV vs attention).
Verdict: Healthy. Later mentions are short and use the standard "Section X.Y" backref.
Fix: None required. Verify the section-32.3 cross-attention paragraph backrefs to Section 4.2 (currently it does not).

**Tokenization / BPE** (HEALTHY).
Canonical: Sections 2.1, 2.2, 2.3 (Module 02). Each ~90 mentions.
Also discussed: 61.4 ("Beyond Text: LLMs as Universal Sequence Machines") covers domain-specific tokenization (genomics, proteins, time-series). Different scope; not duplicative.
Verdict: Healthy by topic distinction.
Fix: None.

**RAG pipeline** (HEALTHY).
Canonical: Module 23 (Sections 23.1-23.9), with 23.1 as the architectural entry point.
Also discussed: 262 sections mention RAG in passing. Spot-checked sections 45.5, 52.7, 53.7, all link back to 23.1 explicitly.
Verdict: Healthy: RAG is treated as an architectural primitive and most mentions explicitly link to Chapter 23.
Fix: One internal duplication: Sections **23.3 ("RAG with Knowledge Graphs") and 23.7 ("GraphRAG: Knowledge Graph-Augmented Retrieval")** cover the same topic and the book has flagged this with "Related coverage" callouts in both files. Either fold 23.3 into 23.7 (keep 23.7 as the deep treatment) or rebrand 23.3 as a one-page intro that only references 23.7.

**Hallucination** (HEALTHY-MOSTLY).
Canonical (grounding side): Section 23.1 introduces RAG-as-hallucination-mitigation; full coverage in 37.2 ("Why LLMs Hallucinate and How to Catch Them"). Canonical (detection side): Section 34.1 and 34.6 (Eval & Observability).
Also discussed: 50+ sections, each in context.
Verdict: Each downstream section uses the term contextually (failure mode in healthcare 53.2, legal 51.1-51.5, etc.) without re-teaching the concept. Healthy.
Fix: None. Confirm that section 37.2 is unambiguously labelled as the "why hallucinations happen" canonical, not just one of several treatments.

**RLHF / DPO / Alignment** (HEALTHY).
Canonical: Module 20 (Sections 20.1-20.5). Section 20.1 owns RLHF, 20.2 owns DPO, 20.3 owns Constitutional AI, 20.4 owns RLVR.
Also discussed: 9.3 (RLVR / GRPO in reasoning models, with backref), 37.1, 37.2, 37.3 (alignment as safety lens), 64.2 (frontier-scale alignment).
Verdict: Healthy. Each external mention is in context (reasoning, safety, frontier) and not re-teaching the core algorithms.
Fix: None. Verify section 64.2 explicitly cites 20.2 for the DPO loss derivation.

**MCP (Model Context Protocol)** (HEALTHY).
Canonical: Section 27.2 ("Model Context Protocol (MCP)").
Also discussed: 13.1-13.3 (API patterns mentioning MCP), 26.1, 26.4 (agent architectures using MCP).
Verdict: Healthy. 27.2 owns the protocol; other sections only mention it as a tool.
Fix: None.

**LLM-as-judge / Eval methodology** (HEALTHY).
Canonical: Section 34.8 ("LLM-as-Judge: Reliability, Debiasing, and Training Judge Models"). 18 mentions in this single section.
Also discussed: 17.1-17.7 (synthetic data quality assessment via judge), 23.x (RAG evaluation), 49.1-49.2 (drift detection), 53.7, 59.1.
Verdict: Healthy. Downstream uses are application-specific and reference 34.8.
Fix: Confirm `production-pattern P9: LLM Judge with Periodic Human Calibration` (only in 34.8) is referenced from at least 49.1 and 53.7.

### Duplication-flagged clusters

**FlashAttention** (DUPLICATION).
Canonical candidate: Section 10.7 ("GPU Kernel Programming for LLM Optimization"), 18 mentions plus the implementation in Triton.
Also discussed:
- Section 4.4 ("GPU Fundamentals & Systems"), 29 mentions, full algorithm walkthrough, including the "Under the Hood: Why FlashAttention Doesn't Materialize N×N" callout and "4.4.4 The FlashAttention Algorithm" header.
- Section 4.3 (13 mentions, GQA / MQA in context of variant attention).
- Section 63.4 ("FlashAttention-4 and Inference Kernels for Blackwell"), 18 mentions, frontier-specific.
- Section 63.5 (training-inference co-design, 2 mentions in context).
Verdict: DUPLICATION between 4.4 and 10.7. Both teach the algorithm in full. 4.4 is the foundations layer (block-tiling + online softmax); 10.7 is the kernel-level layer (Triton implementation). 63.4 is the frontier (Blackwell-specific FA4). The boundary is muddled.
Fix: Make 4.4 introduce the algorithm at high level and explicitly defer the implementation to 10.7 ("for the Triton implementation, see Section 10.7"). Make 10.7's opening explicitly say "this section assumes 4.4's algorithmic background and dives into the kernel". 63.4 should backref both.

**Compute Planning / GPU Selection / Inference Cost** (DUPLICATION, IN-PART AND CROSS-PART).
Canonical candidate: Section 46.1 ("LLM Compute Planning & Infrastructure"), the cleanest 2026-era treatment.
Duplicates in the same module:
- **Section 46.3 has the same title as 46.1** ("LLM Compute Planning & Infrastructure") and covers the same topic (GPU selection, cloud vs on-prem). 46.3's body headers use stale "31.5.x" numbering. The module-46 index lists both 46.1 and 46.3 with identical titles.
- **Section 46.4 has the same title as 46.2** ("Enterprise Integration Patterns for LLM Systems"). 46.4's body headers use stale "31.6.x" numbering. Listed twice in the module-46 index.
Cross-part overlap:
- Section 10.4 (Part II, Inference Optimization, "Serving Infrastructure") covers vLLM, TGI, batch scheduling.
- Section 10.5 (Part II, "Model Pruning & Sparsity") and 10.6 ("Test-Time Compute") touch cost.
- Section 35.1, 35.3, 35.5, 35.9 (Part VIII, Production Engineering) cover deployment / GPU management again.
- Section 63.1 (Part XII, "Beyond NVIDIA: Groq, Cerebras...") and 63.3, 63.5 (frontier hardware) cover the same GPU comparison forward-looking.
Verdict: DUPLICATION. Module 46 contains its own internal duplication AND duplicates content already in Part II Module 10 and Part VIII Module 35. The 46.3 and 46.4 files are clearly imports from old chapter 31 that were not reconciled.
Fix: (a) Delete or merge 46.3 into 46.1 (keep the 46.1 file; 46.3 has stale headings and is older content). (b) Same for 46.4 -> 46.2. (c) After deletion, renumber sections so module-46 has clean 46.1-46.4 instead of 46.1, 46.2, 46.3 (orphan), 46.4 (orphan). (d) Section 46.1 should backref Section 10.4 for inference-serving specifics and Section 35.9 for Kubernetes-native GPU management.

**ROI / Unit Economics** (DUPLICATION, IN-PART AND CROSS-PART).
Canonical candidate: Section 47.1 ("ROI Measurement & Value Attribution"), the cleanest 2026 treatment.
Duplicates in the same module:
- **Section 47.3 has the same title as 47.1** ("ROI Measurement & Value Attribution"). 47.3 has 146 mentions of ROI (vs 47.1's 14) but uses old "31.3.x" headings.
- **Section 47.4 has the same title as 47.2** ("Economic Design of LLM Systems"). 47.4 uses old "31.7.x" headings.
Cross-part overlap:
- Section 15.4 (Part III, "Cost-Performance Optimization at Scale") covers the same model-tier-and-routing decision tree.
- Section 35.4 (Part VIII LLMOps) implicitly overlaps cost monitoring.
- Section 47.2 explicitly backrefs section 47.3 even though they are duplicate-title (an internal contradiction).
- Conflicting numbers: section 47.1 says inference is 40-70% of per-request cost; section 47.2 says inference is "50%" in the cost-stack diagram. The two sections are using different baselines without saying so.
Verdict: DUPLICATION. Module 47 also has internal duplication AND cross-references the unwell duplicate.
Fix: (a) Delete 47.3 / merge into 47.1 (keep 47.1 as the modern 2026 treatment; 47.3 is the longer but stale-numbered older version). (b) Same for 47.4 -> 47.2. (c) Reconcile the inference-cost percentage (40-70% vs 50%) to one number based on current 2026 data. (d) Section 47.1 should backref Section 15.4 for the cost-per-token / model-tier math.

**Production Observability / Cost Control** (DUPLICATION, IN-PART AND CROSS-PART).
Canonical candidate: Section 35.4 ("LLMOps & Continuous Improvement") + 34.6 ("Observability & Tracing") + 34.10 ("OpenTelemetry for LLM Applications") in Part VIII.
Duplicates in Part X:
- **Section 48.5 ("Production Observability & Cost Control")** uses old "25.3.x" headings and Production Pattern P2. The module-48 index does NOT list section 48.5 (it ends at 48.4), so this file is orphaned but still rendered. Content overlaps 34.6 and 35.4.
- **Section 48.6 ("Error Recovery, Resilience & Graceful Degradation")** similarly orphaned in module-48 index; overlaps 35.8 ("Reliability Engineering for LLM Applications").
- **Section 48.4 ("Post-Launch Monitoring and Iteration")** has the SAME title as Section 49.1, and uses "35.4.x" headers showing it was copied from Part VIII Section 35.4. The module-49 chapter is titled "Post-Launch Monitoring" so 48.4 is redundant with the entire chapter 49.
Cross-part:
- Section 49.2 ("Drift Detection in Production") overlaps Section 34.4 ("LLM-Specific Monitoring & Drift Detection") canonically.
- Section 49.3 ("Model-Rotation Strategy") is new content not present elsewhere; legitimate.
Verdict: DUPLICATION. Section 48.4 is a 1:1 copy of old Chapter 35.4 from Part VIII and clashes with the entire Chapter 49. Sections 48.5 and 48.6 are orphans (not linked from index) that still ship in the build.
Fix: (a) Delete 48.4; its content already exists in 35.4 + 49.1. (b) Delete 48.5; its content exists in 34.6 + 35.4. (c) Delete 48.6; its content exists in 35.8. (d) Update the toc/index page to reflect that module-48 has only 48.1-48.3 as proper sections. (e) Update Section 23.1's stale reference "Production Pattern P2 in Chapter 35's LLMOps coverage" to point at the canonical P2 location (which is currently in 48.5; should be moved to 34.6 or 35.4).

**Agent Cost Control / Observability** (DUPLICATION).
Canonical candidate: Section 27.6 ("Efficient Multi-Tool Orchestration and Tool Economy") for agent cost, Section 28.x for agent coordination cost.
Duplicates:
- Section 48.5 references "Part VI" and includes Production Pattern P2: Token Budget Caps; but agent-specific token budgeting also appears in 27.6 ("Tool Economy") and 47.4 (Production Pattern P6: Per-User Token Budget Caps).
Verdict: SCATTERED. P2 (Token Budget Caps), P6 (Per-User Token Budget Caps), and unnamed budget patterns in 27.6 are inconsistently numbered and located.
Fix: Promote a single canonical "Token Budget" pattern (probably P2 living in Section 35.x or 34.x), have 27.6 and 47.4 reference it.

---

## In-part literal duplicates (same module, same title, NOT a Tools-of-Trade)

| Module | Pair | Status |
|---|---|---|
| M46 (Part X) | section-46.1.html and section-46.3.html, title "LLM Compute Planning & Infrastructure" | DUPLICATE. 46.3 has stale "31.5.x" headers. |
| M46 (Part X) | section-46.2.html and section-46.4.html, title "Enterprise Integration Patterns for LLM Systems" | DUPLICATE. 46.4 has stale "31.6.x" headers. |
| M47 (Part X) | section-47.1.html and section-47.3.html, title "ROI Measurement & Value Attribution" | DUPLICATE. 47.3 has stale "31.3.x" headers. |
| M47 (Part X) | section-47.2.html and section-47.4.html, title "Economic Design of LLM Systems" | DUPLICATE. 47.4 has stale "31.7.x" headers. |
| M48 (Part X) | section-48.4.html "Post-Launch Monitoring and Iteration" duplicates the entire content of M49 chapter 49 | CROSS-MODULE DUPLICATE. |
| M48 (Part X) | section-48.5.html "Production Observability & Cost Control" not in module-48 index (orphan) | ORPHAN, DUPLICATE of P8 M34/M35. |
| M48 (Part X) | section-48.6.html "Error Recovery, Resilience & Graceful Degradation" not in module-48 index (orphan) | ORPHAN, DUPLICATE of 35.8. |

## Cross-part literal duplicates (same title, different parts)

| Part / Section | Title | Duplicates |
|---|---|---|
| P12 M61 section-33.11.html | "33.11 What 2026 Settled (and What Remains Open)" | P12 M64 section-64.5.html title "What 2026 Settled (and What Remains Open)" |
| P10 M48 section-48.4.html | "Post-Launch Monitoring and Iteration" | P10 M49 section-49.1.html same title |

## Stale-numbered leftover files

These files exist in the new chapter directories but have filenames and/or H1/H2 headings using old chapter numbering (pre-renumbering era). Their content is either a strict duplicate of canonical content (the items above) or stale "Catch-all" sections that mix topics already split into the new chapters.

| File path | File-stem # | Title # | Reading H2 # | Issue |
|---|---|---|---|---|
| `part-12-frontiers/module-61-frontier-architectures/section-33.11.html` | 33.11 | "Section 33.11" | "33.11 What 2026 Settled..." | Old chapter 33 leftover; duplicates 64.5 |
| `part-12-frontiers/module-61-frontier-architectures/section-33.4.html` | 33.4 | "Section 33.4: World Models" | n/a (clean H2) | Old chapter 33 leftover; content already moved to Section 32.4 (whose title explicitly says "from old 33.4") |
| `part-12-frontiers/module-61-frontier-architectures/section-61.4.html` | 61.4 | "Section 61.10" | "33.10.x" | Filename = 61.4 but title and headers say 61.10/33.10 |
| `part-12-frontiers/module-62-frontier-theory/section-62.1.html` | 62.1 | "Section 62.5" | n/a | Filename / title mismatch |
| `part-12-frontiers/module-62-frontier-theory/section-62.2.html` | 62.2 | "Section 62.6" | n/a | Filename / title mismatch |
| `part-12-frontiers/module-62-frontier-theory/section-62.3.html` | 62.3 | "Section 62.7" | n/a | Filename / title mismatch |
| `part-12-frontiers/module-62-frontier-theory/section-62.4.html` | 62.4 | "Section 62.8" | n/a | Filename / title mismatch |
| `part-12-frontiers/module-64-agi-trajectories/section-64.5.html` | 64.5 | "Section 64.5: 33.11 What 2026 Settled..." | "64.5.x" | Title still has the old "33.11" prefix |
| `part-11-applications-across-industries/module-52-finance-llms/section-52.7.html` | 52.7 | "Section 52.2: LLMs in Finance & Trading" | "27.2.x" | Filename, title, and headers all inconsistent; content is old chapter 27 leftover |
| `part-11-applications-across-industries/module-53-healthcare-llms/section-53.7.html` | 53.7 | "Section 53.3: Healthcare & Biomedical AI" | "27.3.x" | Same as 52.7 pattern |
| `part-11-applications-across-industries/module-55-cybersecurity-llms/section-55.7.html` | 55.7 | "Section 55.5: Cybersecurity & LLMs" | n/a | Same pattern |
| `part-11-applications-across-industries/module-58-creative-industries/section-58.2.html` | 58.2 | "Section 58.6: Education, Legal & Creative Industries" | "27.6.x" | Mixes Education (M54), Legal (M51), and Creative (M58) topics |
| `part-11-applications-across-industries/module-59-recommendation-search/section-59.2.html` | 59.2 | "Section 59.4: LLM-Powered Recommendation & Search" | "27.4.x" | Old chapter 27 leftover |
| `part-6-agentic-ai/module-28-multi-agent-systems/section-28.6.html` | 28.6 | "Section 28.5: Testing Multi-Agent Systems" | "25.5.x" | Filename = 28.6 but title and headers use old 28.5 / 25.5 numbering |
| `part-9-safety-security-ethics/module-38-agent-safety-security/section-38.3.html` | 38.3 | "Section 38.6: Agentic Security Benchmarks..." | n/a | Filename / title mismatch |
| `part-9-safety-security-ethics/module-38-agent-safety-security/section-38.4.html` | 38.4 | "Section 38.7: Supply-Chain Security..." | n/a | Same pattern |
| `part-10-idea-to-product/module-43-vibe-coding/section-43.2.html` | 43.2 | "Section 43.2: Vibe-Coding & AI-Assisted Software Engineering" | "27.1.x" | H2 headers use old chapter 27 |
| `part-10-idea-to-product/module-44-mvp/section-44.x.html` | mostly clean | clean | varies | not duplicated, but unchecked |
| `part-10-idea-to-product/module-45-prototype-to-production/section-45.1.html through 45.7.html` | 45.1-45.7 | clean titles | "34.x.x" for all | All H2 headers use old chapter 34 numbering (Production Engineering's previous home) |
| `part-10-idea-to-product/module-42-strategy-prioritization/section-42.3.html` | 42.3 | "Section 42.1: LLM Strategy & Use Case Prioritization" | n/a | DUPLICATE TITLE with 42.1 |
| `part-10-idea-to-product/module-42-strategy-prioritization/section-42.4.html` | 42.4 | "Section 42.4: LLM Vendor Evaluation & Build vs. Buy" | n/a | DUPLICATE TITLE with 42.2 ("LLM Vendor Evaluation & Build vs. Buy") |

## Named-case reuse

Searched for "Air Canada", "DeepSeek-R1 training", and similar named cases.

- **Air Canada chatbot incident**: zero hits inside `part-*/module-*/section-*.html`. The case is correctly anchored in `appendices/appendix-u-war-stories/`. No backref / duplication issue.
- **DeepSeek-R1 training case**: appears in 30+ files but each appearance is a model citation, not a re-teaching of the GRPO training recipe. Canonical teaching is in Section 20.4 ("RLVR") and Section 9.3 ("Training Reasoning Models"). Other mentions correctly reference these.
- **"text-embedding-ada-002 -> v3 silent embedding swap" postmortem**: lives only in Section 23.1. Healthy.
- **"Out-of-Date Policy Bot" postmortem**: lives only in Section 23.1. Healthy.

No named-case-without-canonical pattern detected.

## Cross-part topic leakage (specific concerns)

1. **Cost-optimization material in Part II inference-opt overlaps with Part VIII production-eng and Part X compute-planning**. Currently each of these has its own "cost decomposition" with slightly different breakdowns (40-70% / 50% / etc., model-tier vs gateway-tier accounting). The reader sees the same topic 3-4 times with no canonical anchor.

2. **Agent observability + production observability + post-launch monitoring** overlap. Section 27.6, 28.5, 34.6, 35.4, 48.5, 49.1, 49.2 all touch the same telemetry / drift / cost-monitoring story. Section 48.5 is the worst offender (orphaned and old).

3. **Vibe Coding** appears in Module 43 (Sections 43.1, 43.2, 43.3) AND in Module 45 (Section 45.4, 20 mentions, with H2 headers "34.5.1 What Is Vibe Coding?"). Module 45 should not be re-teaching vibe coding.

4. **Safety/Hallucination/Compliance** appear in Part IX, Part VI (agent safety), Part X (post-launch monitoring), AND each Part XI industry chapter. The Part XI industry sections correctly use the pattern "see Section 37.x for the canonical treatment" in most places, but the Part X module-48 / 49 sections re-teach safety concepts without backrefs.

5. **Eval frameworks**: Part VIII (34.1-34.12) is canonical. Part XII section 64.1 ("Frontier Benchmarks") is the new-benchmarks layer (HLE, ARC-AGI-2, FrontierMath). Industry-specific eval lives in Part XI per chapter (e.g., 51.4 verified-RAG architecture for legal eval, 53.5 healthcare vendors). This split is healthy.

## Recommended consolidations

1. **Module 46: collapse 46.1+46.3 and 46.2+46.4**. Keep 46.1 and 46.2 (modern 2026 content). Delete 46.3 and 46.4 (stale "31.x" headers). Renumber subsequent if needed. Update module-46/index.html to list only 4 sections, not 4 with duplicates.

2. **Module 47: collapse 47.1+47.3 and 47.2+47.4**. Keep 47.1 and 47.2. Delete 47.3 and 47.4. Reconcile the conflicting inference-cost percentage (40-70% in 47.1 vs 50% in 47.2's cost-stack diagram).

3. **Module 48: delete 48.4, 48.5, 48.6**. 48.4 duplicates the entire Chapter 49 ("Post-Launch Monitoring"). 48.5 and 48.6 are orphaned (not in module-48 index); their content already lives in Sections 34.6, 35.4, 35.8. Update Section 23.1's "Production Pattern P2 in Chapter 35's LLMOps coverage" reference to point at the new canonical P2 location (probably Section 34.6 or 35.4).

4. **Module 42: collapse 42.1+42.3 and 42.2+42.4**. Same pattern as Modules 46/47.

5. **Module 23: collapse 23.3 (RAG with KGs) into 23.7 (GraphRAG)**. Keep 23.7 as the canonical deep treatment; reduce 23.3 to a one-page intro or remove entirely.

6. **Module 61: delete `section-33.11.html` and `section-33.4.html`** files. They are leftover old-chapter-33 imports. Section 32.4 already explicitly notes it inherits content "from old 33.4"; Section 64.5 is the new home of the "What 2026 Settled" piece. Rename file `section-61.4.html` so the filename matches its actual title (which says "Section 61.10"; either renumber the title to 61.4 or rename file to section-61.10.html).

7. **Module 62: fix file-vs-title numbering**. Files section-62.1, 62.2, 62.3, 62.4 have titles "Section 62.5, 62.6, 62.7, 62.8" - either rename the files or fix the titles. The H1/H2 headings are clean so the fix is one-line per file.

8. **Module 38: fix file-vs-title numbering**. section-38.3.html title says "Section 38.6"; section-38.4.html title says "Section 38.7". Same fix as Module 62.

9. **Part XI .7 files (52.7, 53.7, 55.7, 58.2, 59.2)**: delete or merge into the canonical .1-.5 sections of their chapters. They are old chapter-27 imports. Each retains H2 numbering like "27.2.1 Financial NLP..." that exposes its origin.

10. **Module 45 (Prototype to Production): renumber all H2 headers from "34.x.x" to "45.x.x"** to remove old-chapter-34 leftover numbering. The h1 titles are clean. Also remove Section 45.4's "What Is Vibe Coding?" treatment (or trim it to a one-liner) since Module 43 owns vibe coding.

11. **FlashAttention canonical placement**: Move the algorithm walkthrough from Section 4.4 to Section 10.7. Keep Section 4.4 as a one-paragraph "memory-hierarchy view" with a backref to 10.7. Section 63.4 (FlashAttention-4 Blackwell) backrefs both. This removes the dual-treatment.

12. **Token Budget Cap Production Pattern numbering**: Currently P2 (in 48.5, orphan) and P6 (in 47.4, also orphan-numbering). Consolidate to one canonical P2 location (recommend Section 34.6 or 35.4), and update Sections 23.1, 27.6, and 47.4 to backref the canonical.

---

## Notes on audit method

- Tools-of-the-Trade modules (06, 12, 16, 21, 25, 30, 33, 36, 39, 50, 60, 65) excluded as designed-to-be-redundant catalogs.
- Concept matching used inclusive regex: e.g., "RAG|retrieval-augmented|retrieval.augmented" for RAG.
- "Duplicate" judgement based on (a) identical or near-identical h1/title, (b) overlapping H2 structure, (c) substantial content overlap (>30% of section bytes), or (d) explicit "Related coverage" callouts the book itself adds.
- "Canonical" judgement based on which section has the deepest treatment (longest, most-citations) AND best fits the part's pedagogical role.
- Inspected file count: 286 main sections + 22 module index pages + key cross-references in `appendices/` and `front-matter/`.

The audit did NOT consider:
- Appendices (which are designed to be parallel reference shelves).
- Tools-of-the-Trade modules (designed to be redundant).
- Capstone exercises (which legitimately re-use concepts).
- The `_concept-figs/`, `images/`, `KDP/build/`, and `temp_epub/` directories.
