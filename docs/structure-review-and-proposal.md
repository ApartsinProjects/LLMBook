# Book Structure: Analysis and Proposed Restructure (v5)

**Status**: proposal, in development on branch `v2.0`. Production lives on `main` tagged `production-v1.0`.
**Generated**: 2026-05-17, post-appendix-renumbering.
**Revision history**:
  - v1 — initial: 13 parts → 13 parts, 87 → 78 chapters; mostly merge/dedupe.
  - v2 — split Part V into Retrieval+IE and Dialogue+Assistants.
  - v3 — split Part X into LLM @ Scale and LLMOps; move Multimodal to V.
  - v4 — move Agentic AI to Part VI; rename Part XII to LLMOps & Lifecycle Management.
  - **v5 (this version)** — deep section-level content analysis + content-level fixes added to the plan (not just structural moves). See section 5 (content findings) and section 7 (per-chapter intervention list).

**Current state on disk**: 13 parts, 87 chapters, 413 sections, 7 appendices, audit clean.

---

## 1. Editorial criteria

| Criterion | Target |
|---|---|
| **A. Separation of concerns** | One cohesive theme per part, one topic per chapter |
| **B. No duplication** | Each subject appears once in the ToC; cross-refs handle repetition |
| **C. Reasonable counts** | 5–7 chapters per part, 3–8 sections per chapter |
| **D. Consistent abstraction** | Sibling chapters cover comparable scope |
| **E. Reading order** | Model → patterns → quality → runtime → applied → frontier |
| **F. Content density** | Sections in the 5–60 KB body-text band; no stubs, no monsters |

---

## 2. Conceptual grouping of parts

The 15 parts cluster into 6 thematic blocks:

| Block | Parts | What it covers |
|---|---|---|
| **A. Models** | I–V | What an LLM is, how it works, how to train and adapt it, what modalities it covers |
| **B. Patterns on top of models** | VI–VIII | Agentic AI (foundational pattern), retrieval, dialogue — the application patterns. Agents come first because retrieval/dialogue use agent concepts. |
| **C. Quality** | IX–X | Evaluation, observability, safety, security, ethics |
| **D. Runtime** | XI–XII | Scale (compute/performance) and LLMOps (workflow/lifecycle) |
| **E. Applied** | XIII–XIV | Designing products and shipping into industries |
| **F. Future** | XV | Frontier research, theory, AGI |

---

## 3. Final per-part structure

| # | Part | Ch | What it contains |
|---|---|---:|---|
| **I** | **Foundations** | 7 | Math/ML/PyTorch, NLP basics, tokenization, attention, transformers, decoding, Foundations Tools |
| **II** | **Understanding LLMs** | 5 | Pre-training & scaling, modern landscape, reasoning, inference optimization, interpretability+Tools |
| **III** | **Working with LLMs** | 4 | APIs, prompt engineering, hybrid ML+LLM, Tools |
| **IV** | **LLM Training & Adaptation** | 5 | Synthetic data, SFT, PEFT, alignment, Tools |
| **V** | **Multimodal LLMs** *(moved earlier)* | 7 | VLM/Omni, image+video, audio, document/OCR, 3D/scenes, embodied AI/VLA/robotics, Tools |
| **VI** | **Agentic AI** *(moved up)* | 5 | Foundations, tools/MCP/A2A, multi-agent, specialized, Tools |
| **VII** | **Retrieval & Information Extraction** | 6 | Embeddings, **NER (promoted)**, RAG fundamentals, advanced RAG/KG, cross-modal RAG, Tools |
| **VIII** | **Dialogue & Conversational AI** | 5 | Architecture, memory, multi-turn, voice & realtime, Tools |
| **IX** | **Evaluation & Observability** | 4 | Quality metrics, specialized eval, online monitoring, Tools |
| **X** | **Safety, Security & Ethics** | 9 | Adversarial, guardrails, agent safety, privacy, bias/hallucination, regulation, provenance, frontier safety, Tools |
| **XI** | **LLM Systems at Scale** | 5 | Compute planning, distributed training, hardware, edge, Tools |
| **XII** | **LLMOps & Lifecycle Management** *(renamed)* | 5 | Gateways, orchestration, K8s, reliability/registry, Tools |
| **XIII** | **Designing LLM Products** | 7 | Ideation/strategy, PM, prototyping, MVP, economics, shipping, Tools |
| **XIV** | **Industry Applications** | 8 | Legal, finance, healthcare, education, cyber, gov, manuf+creative+rec (merged), Tools |
| **XV** | **Frontiers** | 4 | Architectures, theory, AGI trajectories, Tools |

**Totals**: 15 parts, **86 chapters**, ~370 sections target. Every part in 4–9 chapter band.

---

## 4. Section size distribution (current state)

```
Total: 413 sections, 10,168 KB body text
Average section: 24 KB
```

| Part | # Sec | Total | Avg | Min | Max | Verdict |
|---|---:|---:|---:|---:|---:|---|
| I (Foundations)   | 28 | 1111 KB | 39 KB |  4 KB |  66 KB | OK |
| II (Understanding)| 35 | 1367 KB | 39 KB |  3 KB |  65 KB | OK |
| III (Working)     | 20 |  682 KB | 34 KB |  2 KB |  79 KB | Has monster (15.5) |
| IV (Training)     | 31 | 1159 KB | 37 KB |  2 KB | 114 KB | Has monster (21.2) |
| V (Retrieval+CAI) | 24 |  885 KB | 36 KB |  2 KB |  75 KB | Has monster (25.2) |
| VI (Agents)       | 25 |  547 KB | 21 KB |  2 KB |  45 KB | OK |
| **VII (Multimodal)** | **66** | **1007 KB** | **15 KB** |  3 KB |  42 KB | **Thin avg → indicates over-splitting + Ch 31, Ch 41 duplicates** |
| VIII (Eval)       | 26 |  740 KB | 28 KB |  1 KB |  80 KB | Has monster (48.2) |
| IX (Safety)       | 36 |  777 KB | 21 KB |  1 KB |  86 KB | Has monster (49.1) + 4 single-sec ch |
| X (Operations)    | 15 |  342 KB | 22 KB |  6 KB |  41 KB | OK |
| XI (Designing)    | 35 |  680 KB | 19 KB |  1 KB |  51 KB | Has duplicate-content chapters |
| **XII (Industries)** | **49** | **487 KB** |  **9 KB** |  1 KB |  41 KB | **Thin avg → industry chapters under-developed** |
| XIII (Frontiers)  | 23 |  378 KB | 16 KB |  5 KB |  44 KB | OK |

**Key signals:**
- Parts VII and XII have anomalously thin section averages (15 KB and 9 KB) — duplicates and underdeveloped industry chapters
- Five "monster" sections (>75 KB) need splitting: 15.5, 21.2, 25.2, 48.2, 49.1
- 13 chapters have structural issues (oversized, undersized, or stub sections)

---

## 5. Content findings (section-level deep analysis)

### 5.1 Duplicate content (same topic in multiple places)

| Topic | Current locations | Action |
|---|---|---|
| **Reasoning models** | 8.3 (section), Ch 9 (whole chapter, same title), 10.6 (section), 13.4 (subset) | Drop 8.3; keep Ch 9 as canonical; tighten 10.6 to inference-only |
| **Test-time compute** | 8.3, 9.1, 9.5, 10.6 | Consolidate into Ch 9 only |
| **Embodied AI / VLA / Robotics** | Ch 39 (VLA), Ch 40 (Robotics), Ch 41.1+41.2+41.8 (aggregator duplicates) | Merge 39+40 + unique-from-41 into new V Ch 6 |
| **3D Gaussian Splatting** | Ch 36 (5 sec dedicated), 41.3+41.5 (duplicate) | Drop 41.3, 41.5; keep Ch 36 only |
| **World models** | 41.4 (unique), Ch 33 (video gen has overlap) | Keep 41.4 content, re-home in new V Ch 5 |
| **Audio/Speech/Voice** | Ch 32 (Audio gen), Ch 38 (Streaming), 24.5 (Voice Agents), 31.2 (overview duplicate) | Move 38.x → Dialogue Ch 4 (with 24.5); keep 32 as audio-gen; drop 31.2 |
| **Multimodal Reasoning** | 35.5, 41.7, 42.3, 42.4 | Consolidate in new VII Ch 5 (Cross-Modal RAG) |
| **Memory** | 10.2 (KV cache), 24.3 (Dialogue memory), 26.6 (Agent memory), 83.2 (Theory) | Each is distinct in scope; add cross-link table; no merge |
| **Code Generation** | 29.1 (Code Agents), 29.4 (Coding Workflows), 46.4 (Code Eval) | Consolidate 29.1+29.4; cross-link 46.4 |
| **Hardware** | 4.4 (GPU Foundations), 10.7 (Kernels), 61.x (Compute), 84 (Frontier Hardware) | Move Ch 84 → new XI Ch 3 (Hardware); keep 4.4 (foundations), 10.7 (kernel theory) |
| **Industry "X & LLMs" overview sections** | 73.6 (Finance), 74.6 (Healthcare), 76.6 (Cyber) — generic chapter overviews that duplicate the chapter | Delete all three; chapter index already serves this role |
| **Ch 79 "Education, Legal & Creative"** (sec 79.2) | Cross-cuts Education (Ch 75) and Legal (Ch 72) | Delete; topic belongs in respective domain chapters |
| **Ideation / Strategy / Product-Hypothesis** | Ch 63 (Ideation, 3 sec), Ch 65 (Strategy, 2 sec), Ch 68 (From Idea to Hypothesis, 7 sec) | Merge into one chapter, ~6 sections |

### 5.2 Quality issues by chapter

| Chapter | Issue | Fix |
|---|---|---|
| **Ch 7** (Pre-training) | 9 sections (over band); sec 7.6 (Distributed Training) and 7.8 (Production Training Systems) belong in new Part XI | Move 7.6 + 7.8 to new XI Ch 2; Ch 7 retains 7 sections |
| **Ch 15** (Hybrid ML+LLM) | 6 sec; sec 15.5 (NER) at 79 KB is monster, sec 15.6 (Dataset Engineering) loosely connected | Promote 15.5 → new VII Ch 2; 15.6 stays in 15 OR moves to IV (training data prep) |
| **Ch 21** (Training Tools) | Sec 21.2 is 114 KB monster — too many deep-dives merged in during ToT consolidation | Split into 21.2a (training frameworks: HuggingFace, Accelerate, PEFT, TRL) and 21.2b (experiment tracking: W&B, MLflow, hyperparameter opt) |
| **Ch 23** (RAG) | 9 sections (over band) | Split: 23.1–23.4 → new VII Ch 3 (RAG Fundamentals); 23.6–23.9 + 23.3 → new VII Ch 4 (Advanced RAG / KG) |
| **Ch 31** (Multimodal overview) | 4 sections, all overview-duplicates of Ch 32–35, Ch 37 | Delete chapter entirely |
| **Ch 41** (Embodied AI aggregator) | 8 sections, 6 of which duplicate Ch 36/39/40/42 | Extract 41.4 (World Models) → new V Ch 5; delete rest |
| **Ch 44** (Eval Foundations) | 11 sections (over band) | Split: 44.1–44.6 stay as Eval Foundations; 44.7–44.11 → new IX Ch 2 (Eval Methodology) |
| **Ch 45** (Testing Quality Gates orphan) | 1 section starting at 45.6 | Merge into Ch 44 |
| **Ch 47** (Online Eval) | 4 sections starting at 47.4 (broken numbering) | Renumber to 47.1–47.4 |
| **Ch 49** (Adversarial Security) | 2 sections; sec 49.1 is 86 KB monster | Split 49.1 into 3 sections (threats taxonomy, common attacks, attack-surface model); keep 49.2 |
| **Ch 52** (Privacy) | 2 sections | Expand: split 52.1 into privacy attacks (52.1) + differential privacy (52.2); rename 52.2 to 52.3 (Unlearning) |
| **Ch 53, 54, 58, 59** (Safety singletons) | 1 section each; Ch 59 starts at 59.5 | Merge into adjacent chapters per v3 plan (Bias+Hallucination, Environmental+Frontier-Safety) |
| **Ch 62** (Production Engineering) | 11 sections | Split into 4 chapters across new XI and XII per v3 plan |
| **Ch 65** (Strategy) | 2 sections | Merge with Ch 63 (Ideation) + Ch 68 (Hypothesis) per v3 plan |
| **Ch 68** (From Idea to Hypothesis) | 7 sections that duplicate Ch 63 scope | Merge into combined Ideation chapter |
| **Ch 70** (Shipping) | 6 sections; 70.5 "Application Architecture & Deployment" overlaps with Part X (Ops) | Move 70.5 → new XII (LLMOps); keep 70 product-focused |
| **Ch 72–78** (Industry chapters) | Some have stale ".6" overview sections that duplicate the chapter | Delete 73.6, 74.6, 76.6 (or merge their unique content into earlier sections) |
| **Ch 79** (Creative Industries) | 3 sections, one cross-cutting Education/Legal/Creative — duplicates | Drop 79.2; rebuild as Creative-only |

### 5.3 Content gaps (topics that deserve more / better treatment)

| Topic | Current treatment | Proposed |
|---|---|---|
| **Long context** | 18.7 (training), 44.9 (eval benchmarks) | Add a unified treatment in II Ch 1 (Pre-training & Scaling) section on "Long Context Foundations" |
| **Code agents** | 29.1 (Code Gen Agents), 29.4 (Workflows), 46.4 (Code Eval) | Consolidate into VI Ch 4 (Specialized Agents) sec on "Code Generation Agents: Models, Workflows, Evaluation" |
| **Cost / FinOps** | 15.4 (Cost-Performance), 69.1–69.3 (Economics), 71.x (Tools), 70.1 (Unit econ) | Strengthen XIII Ch 5 (Scaling Economics) as the canonical home; cross-link rest |
| **Tool use** | 27.1 (Function Calling), 27.2 (MCP), 27.4 (Custom Tools), 13.2 (Structured Output) | Strengthen VI Ch 2 (Tool Use Protocols); reduce 13.2 to API-level structured output only |
| **Evaluation** of new modalities | 35.5, 46.5 (Multimodal Eval), 26.4 (Agent Eval), 46.1 (RAG Eval) | All consolidate into IX Ch 2 (Specialized Evaluation) |

---

## 6. Branch & workflow status

```
main (production)
├── tag: production-v1.0
│       (audit-clean baseline: 13 parts, 87 chapters)
│
└── v2.0 (current development branch)
    └── work proceeds here through Phases 0-7
```

All commits from here forward land on `v2.0`. Once Phases 1–7 complete with audit-clean state, `v2.0` merges to `main` and we tag `production-v2.0`.

Phase 0 (templatization & manifests) is already complete on `v2.0`:
- `book_structure.yaml` refreshed (13 parts, 87 chapters, 413 sections)
- `book_structure.target.yaml` declares the v5 target (15 parts, 86 chapters)
- `scripts/structure_diff.py` shows the migration plan
- `scripts/_refresh_book_structure_yaml.py` closes the loop after each phase

---

## 7. Execution plan (per-phase, with chapter-level intervention list)

Each phase ends in audit-clean state (P0=P1=P2=P3=0, linear nav 100%, ToC matches disk).

### Phase 0 — Templatization & manifest setup ✅ *(done)*

### Phase 1 — Lossy deletions (re-home unique content first)
1. **Ch 31 (Multimodal overview)**: 4 sections deleted entirely; part-index already serves this role.
2. **Ch 41 (Embodied AI aggregator)**: extract 41.4 (World Models) and 41.7 (Multimodal Reasoning) as candidate sections for new homes; delete other 6 sections; delete shell.
3. **Ch 45 (Testing Quality Gates orphan)**: merge sec 45.6 into Ch 44.
4. **Industry overview sections**: delete 73.6 (Finance & Trading), 74.6 (Healthcare overview), 76.6 (Cyber overview), 79.2 (Education/Legal/Creative cross-cut).
5. **Section 8.3** (Reasoning & Test-Time Compute): delete (Ch 9 covers it canonically).

### Phase 2 — Monster section splits (quality fixes)
6. **Sec 15.5** (79 KB Structured Information Extraction): keep whole when promoting to new VII Ch 2, but split internally into 4 H2 subsections for readability.
7. **Sec 21.2** (114 KB Libraries): split into 21.2 (training frameworks: HuggingFace ecosystem) and 21.3 (experiment tracking: W&B / MLflow / HPO). 21.3 displaces current Datasets section to 21.4, etc.
8. **Sec 25.2** (75 KB Libraries): split into 25.2 (retrieval frameworks: LangChain core, document loaders) and 25.6 (orchestration: LlamaIndex, Haystack, DSPy).
9. **Sec 48.2** (80 KB Libraries): split into 48.2 (eval frameworks) and 48.6 (observability deep dives).
10. **Sec 49.1** (86 KB LLM Security Threats): split into 49.1 (threat taxonomy), 49.2 (common attack patterns), 49.3 (attack-surface modeling).

### Phase 3 — Sibling merges within parts
11. Part II: merge Ch 11 (Interpretability) + Ch 12 (Tools) → 1 chapter.
12. Part VII (current Multimodal): merge Ch 35 (VLM) + Ch 37 (Omni) → "Vision-Language and Omni Models".
13. Part VII: merge Ch 39 (VLA) + Ch 40 (Robotics) + extract from Ch 41 → "Embodied AI: VLA & Robotics".
14. Part IX (Safety): merge Ch 53 (Bias) + Ch 54 (Hallucination) → "Bias, Fairness, Hallucination & Truthfulness".
15. Part IX: merge Ch 56 (Watermarking) + Ch 57 (Transparency) → "Watermarking, Provenance & Transparency".
16. Part IX: merge Ch 58 (Environmental) + Ch 59 (Frontier Safety) → "Frontier Safety, Sustainability & Open Problems".
17. Part XI (Designing): merge Ch 63 (Ideation) + Ch 65 (Strategy) + Ch 68 (Hypothesis) → "Ideation, Strategy & Product Hypothesis".
18. Part XII (Industries): merge Ch 78 (Manufacturing) + Ch 79 (Creative) + Ch 80 (Recommendation) → "LLMs in Manufacturing, Creative & Recommendation".
19. Part VIII (Eval): merge Ch 44 (Eval Foundations) + Ch 45 (Testing) → consolidated; split into two chapters by content-clustering.

### Phase 4 — Cross-part content moves
20. Move sec 15.5 (NER, 79 KB) from Part III Ch 15 → new Part VII Ch 2 as full chapter.
21. Move sec 15.6 (Dataset Engineering) → Part IV Ch 16 (Synthetic Data) or as a new section in Part IV.
22. Move Part VII Ch 38 (Streaming Multimodal, 4 sec) → new Part VIII Ch 4 (Voice & Realtime).
23. Move Part VII Ch 42 (Cross-Modal RAG, 4 sec) → new Part VII Ch 5.
24. Move Part II sec 7.6 + 7.8 (Distributed Training Systems) → new Part XI Ch 2.
25. Move Part XIII Ch 84 (Frontier Hardware) → new Part XI Ch 3.
26. Move Part XI sec 70.5 (Application Architecture & Deployment) → new Part XII (LLMOps).

### Phase 5 — Part V split + Part X (Operations) split
27. Split old Part V into new V (Retrieval & IE, 6 ch) and new VI/VIII positions.
28. Promote Multimodal (old Part VII) to new Part V position.
29. Split old Ch 62 (11 sections) across new XI Ch 4 (Edge) and new XII Ch 1–4 (Gateways, Orchestration, Containers, Reliability).

### Phase 6 — Cascade renumbering
30. Run canonical renumbering: all chapters 0–85 contiguous, all sections X.1–X.N contiguous within each chapter.
31. Cross-file href rewrite (using `.__tmp__` pattern).
32. Rebuild toc.html, part indexes, chapter indexes, linear nav.

### Phase 7 — Manifest re-sync (close the loop)
33. Run `scripts/_refresh_book_structure_yaml.py` → `book_structure.yaml` matches new disk reality.
34. `git diff book_structure.yaml book_structure.target.yaml` should show **zero** semantic diff (success criterion).

### Audit gates between every phase
- P0 critical = 0
- P1 broken refs = 0
- P2 placeholders = 0
- P3 prose drift = 0
- Linear nav 100% coverage
- ToC matches disk

---

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Content loss during chapter merges | Two-pass: extract unique H2 subsections from the absorbed chapter, append into the absorber as new H2 blocks, only delete the shell after content moved. |
| Content duplication after merges | Phase 2 splits the monster sections that resulted from EARLIER merges; same pattern applies — extract distinct H2 subsections, redistribute. |
| Bookmark / search rot | Where chapters merge, new H2 anchor IDs preserve sensible anchors. Major moves get `<a id="old-X-Y">` aliases for backward compatibility. |
| Numbering cascade complexity | All in one pass at Phase 6 with `.__tmp__` intermediates (proven from the Parts 10–13 and Appendix C–G renumberings). |
| Industry chapter overview deletions | Each "X.6" section flagged for deletion is checked for unique content first; anything not already in earlier sections is preserved. |

---

## 9. Decision needed

Confirm the v5 plan and I execute Phases 1–7 in order with audit gates between phases. Estimated outcome:

- **13 parts → 15 parts** (+2 from splits; Multimodal reordered; Agents promoted)
- **87 chapters → 86 chapters** (≈ same total, much better distributed)
- **413 sections → ~360 sections** (-13% via dedup; quality fixes throughout)
- Every part in 4–9 chapter band, every chapter in 3–8 section band
- Five monster sections split into proportionate sub-sections
- Six duplicate aggregator sections eliminated
- NER promoted to chapter status, knowledge-graph arc contiguous
- Voice/realtime unified in Dialogue (no longer split with Multimodal)
- Hardware centralized in Part XI (no longer split across Part II, X, XIII, XV)
- Distributed training systems promoted to chapter status in Part XI
- Scale vs Ops separated by discipline; Production Engineering → LLMOps & Lifecycle Management
- Agents promoted to model-cluster-adjacent position so retrieval/dialogue can build on agent foundations
- Zero duplicated topics across the table of contents

All work lands on `v2.0`. Production remains live on `main` (`production-v1.0`) until merge.
