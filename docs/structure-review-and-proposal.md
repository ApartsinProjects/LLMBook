# Book Structure: Analysis and Proposed Restructure

**Status**: proposal, awaiting review.
**Generated**: 2026-05-17, post-appendix-renumbering.
**Revised**: 2026-05-17 to split current Part V into two parts (Retrieval & Information Extraction; Dialogue & Assistants) and to give NER / structured extraction a prominent home.
**Current state**: 13 parts, 87 chapters, 413 sections, 7 appendices.
**Audit**: P0=P1=P2=P3=0; linear nav 413/413; ToC clean.

The book is structurally healthy at the link-integrity level. The remaining issues are **editorial**: chapter counts per part are uneven, several chapters carry overlapping or duplicated content, and a handful of chapters sit at a different abstraction level from their siblings.

---

## 1. Evaluation criteria

Four tests, each applied to every chapter and every part.

| Criterion | Target |
|---|---|
| **A. Separation of concerns** | Each part covers one cohesive theme; each chapter covers one topic. |
| **B. No duplication** | The same subject appears at most once in the table of contents; cross-references substitute for repetition. |
| **C. Reasonable counts** | 5–7 chapters per part, 3–8 sections per chapter. Avoid 1-section chapters and 10+-section chapters. |
| **D. Consistent abstraction** | Sibling chapters cover comparable scope. Avoid hyper-specific neighbors of broad chapters. |

---

## 2. Current state — per-part audit

### Imbalanced chapter counts

| Part | Title | Chapters | Verdict |
|---|---|---:|---|
| I | Foundations | 7 | OK |
| II | Understanding LLMs | 6 | OK |
| III | Working with LLMs | 4 | thin |
| IV | LLM Training and Adaptation | 5 | OK |
| V | Retrieval and Conversation | 4 | thin |
| VI | Agentic AI | 5 | OK |
| **VII** | **Multimodal Generation** | **13** | **way too many** |
| VIII | Evaluation of LLM-Based Systems | 5 | OK, 1 broken chapter |
| **IX** | **LLM Safety, Security, and Ethics** | **12** | **way too many, 4 chapters with 1 section** |
| **X** | **LLM Operations** | **2** | **way too few, one 11-section chapter** |
| **XI** | **Designing LLM-Based Products** | **9** | **slightly over** |
| XII | Applications Across Industries | 10 | slightly over |
| XIII | Frontiers | 5 | OK |

### Chapters with broken / extreme section counts

| Location | Sections | Issue |
|---|---:|---|
| Part II Ch 7 (Pre-training) | 9 | over the 3–8 band |
| Part V Ch 23 (RAG) | 9 | over |
| Part VII Ch 41 (Embodied AI) | 8 | over, **and** content overlaps Ch 36/39/40 |
| Part VIII Ch 44 (LLM Evaluation) | 11 | way over |
| Part VIII Ch 45 (Testing Quality Gates) | 1 (starts at 45.6!) | broken |
| Part VIII Ch 47 (Online Eval) | 4 (starts at 47.4!) | broken numbering |
| Part IX Ch 49 (Adversarial) | 2 | thin |
| Part IX Ch 52 (Privacy) | 2 | thin |
| Part IX Ch 53 (Bias) | 1 | thin |
| Part IX Ch 54 (Hallucination) | 1 | thin |
| Part IX Ch 58 (Environmental) | 1 | thin |
| Part IX Ch 59 (Frontier Safety) | 1 (starts at 59.5!) | broken |
| Part X Ch 62 (Production Engineering) | 11 | way over |
| Part XI Ch 65 (Strategy) | 2 | thin |

---

## 3. Duplication audit

### Reasoning models — appears 5+ times

- Part II Ch 8 section 8.3 "Reasoning Models & Test-Time Compute"
- Part II Ch 9 entire chapter "Reasoning Models & Test-Time Compute" (overlaps 8.3)
- Part II Ch 10 section 10.6 "Test-Time Compute & Reasoning Models"
- Part VII Ch 41 has "Multimodal Reasoning" sections
- Part VII Ch 42 "Cross-Modal Reasoning and Multimodal RAG"

**Fix**: drop section 8.3, keep dedicated Ch 9; tighten 10.6 to inference-side concerns only.

### Embodied AI / Robotics — Part VII Ch 39, 40, 41 all overlap

- Ch 39: VLA Models (6 sections)
- Ch 40: LLM-Powered Robotics (7 sections)
- Ch 41: Embodied AI, World Models & Multimodal Reasoning (8 sections, **explicitly named after 39 + 40 + 36 content**: section 41.1 is VLA, 41.2 is robotics, 41.3 is 3D Gaussian Splatting (duplicate of Ch 36), 41.4 is world models, 41.8 is "Robotics, Embodied AI...")

**Fix**: Ch 41 is an aggregator chapter that duplicates downstream content. Delete Ch 41 outright. Keep its unique sections (41.4 World Models, 41.7 Multimodal Reasoning) and re-home them.

### Multimodal Ch 31 — pure overview duplicate

Ch 31 has 4 sections that summarize Ch 32 (Audio), Ch 33 (Video), Ch 34 (Document), Ch 35 (VLM), Ch 37 (Omni). It is a "table of contents written as a chapter."

**Fix**: delete Ch 31; the part-index page already provides the overview.

### 3D Gaussian Splatting — twice in Part VII

- Ch 36 (5 sections, dedicated chapter)
- Ch 41 section 41.3 (duplicate)

**Fix**: Ch 41 deletion above resolves this.

### Audio / Speech — split across three chapters

- Ch 32 (Audio and Music Generation): TTS, voice cloning, music
- Ch 38 (Streaming and Real-Time Multimodal): Gemini Live, GPT-4o Realtime, Moshi
- Ch 31.2 (overview, duplicate)

**Fix**: merge Ch 38 into Ch 32; Ch 32 becomes "Audio: Generation and Streaming."

### Vision-Language Models — split across chapters

- Ch 35 (VLM): ViT, CLIP, LLaVA, GPT-4V
- Ch 37 (Unified Multimodal and Omni Models): GPT-4o, Gemini, Chameleon

**Fix**: merge Ch 37 into Ch 35; Ch 35 becomes "Vision-Language and Omni Models."

### Pre-training systems — split across Parts II and IV

Part II Ch 7 covers:
- 7.6 Distributed Training at Scale
- 7.8 Production LLM Training Systems

These are training-engineering topics that overlap with Part IV Ch 19.3 (Training Platforms & Tools) and the Tools of the Trade content.

**Fix**: keep 7.6 and 7.8 where they are (they are about base-model training, not adaptation); cross-link from Part IV.

### GPU / Hardware — spread thinly

- Part I Ch 4.4 "GPU Fundamentals & Systems"
- Part II Ch 10.4 "Serving Infrastructure"
- Part II Ch 10.7 "GPU Kernel Programming"
- Part X Ch 61 "Compute Planning"
- Part XIII Ch 84 "Frontier Systems & Hardware"

Each serves a different purpose (foundations → serving → planning → frontier), so this is not duplication, but the cross-links between them are weak.

**Fix**: explicit "see also" call-outs at the top of each, no structural change.

---

## 4. Abstraction-level inconsistencies

### Part IX Safety — thin specialty chapters next to wide guardrails

- Ch 50 Guardrails (5 sec, broad)
- Ch 53 Bias (1 sec)
- Ch 54 Hallucination (1 sec)
- Ch 58 Environmental (1 sec)
- Ch 59 Frontier Safety (1 sec, broken numbering)

The 1-section chapters need to be either expanded to 3–5 sections or merged with adjacent chapters.

### Part XI Designing Products — overlapping product phases

- Ch 63 Ideation (3 sec)
- Ch 65 Strategy (2 sec)
- Ch 68 From Idea to Product Hypothesis (7 sec, **named the same as Ch 63**)

Ch 68's H1 is literally "From Idea to Product Hypothesis" — that is exactly Ch 63's job. These are the same chapter that got authored twice.

**Fix**: collapse Ch 63 + Ch 65 + Ch 68 into "Ideation, Strategy & Product Hypothesis" (5–6 sections).

### Part X LLM Operations — one chapter does everything

- Ch 61 Compute Planning (4 sec)
- Ch 62 Production Engineering for LLM Systems (11 sec)

Ch 62 covers scaling, LLMOps, gateways, orchestration, edge, reliability, Docker (4 sec), Kubernetes. Each of those is a chapter-sized topic in its own right.

**Fix**: split Ch 62 into 4 chapters (see proposal).

---

## 5. Proposed structure

Total: **13 parts → 13 parts** (no parts added or removed), **87 chapters → 74 chapters**, **413 sections → ~340 sections** (after deduplication). Each part now sits in the 5–7 chapter band except Part XII (applications inherently span many industries — kept at 8).

### Part I — Foundations *(7 ch, unchanged)*
1. ML and PyTorch Foundations
2. Foundations of NLP & Text Representation
3. Tokenization and Subword Models
4. Sequence Models & the Attention Mechanism
5. The Transformer Architecture
6. Decoding Strategies & Text Generation
7. Tools of the Trade: Foundations Stack

### Part II — Understanding LLMs *(5 ch, was 6)*
1. Pre-training, Scaling Laws & Data Curation *(was Ch 7)*
2. Modern LLM Landscape & Model Internals *(was Ch 8, drop sec 8.3)*
3. Reasoning Models & Test-Time Compute *(was Ch 9, absorbs old 8.3)*
4. Inference Optimization & Efficient Serving *(was Ch 10)*
5. Interpretability & Mechanistic Understanding + Tools *(merge old Ch 11 + Ch 12)*

### Part III — Working with LLMs *(4 ch, unchanged count)*
1. Working with LLM APIs
2. Prompt Engineering & Advanced Techniques
3. Hybrid ML+LLM Architectures & Decision Frameworks *(15.1–15.4; 15.5 and 15.6 move to new Part V)*
4. Tools of the Trade: LLM API Stack

> Note: 4 chapters is below the 5–7 target band but acceptable — Part III is a deliberately compact "first foray" before training (IV), retrieval (V), and dialogue (VI) split the workload. The chapter on Hybrid ML+LLM is the linkable Application Patterns reference.

### Part IV — LLM Training and Adaptation *(5 ch, unchanged)*
1. Synthetic Data Generation & LLM Simulation
2. Fine-Tuning Fundamentals
3. Parameter-Efficient Fine-Tuning (PEFT)
4. Alignment: RLHF, DPO & Preference Tuning
5. Tools of the Trade: Training Stack

### Part V — Retrieval and Information Extraction *(5 ch, was 4)* **SPLIT FROM OLD PART V**
1. Embeddings, Vector Databases & Semantic Search *(was Ch 22)*
2. Structured Information Extraction & NER *(was Part III sec 15.5; now a full chapter)*
3. RAG Fundamentals *(was 23.1–23.5)*
4. Advanced RAG: Knowledge Graphs, Ingestion & Attribution *(was 23.3, 23.6–23.9)*
5. Tools of the Trade: Retrieval & Extraction Stack

> The current 23.3 (RAG with Knowledge Graphs) and 23.7 (GraphRAG) merge into one Advanced-RAG chapter so the knowledge-graph thread is contiguous; NER → graph construction → graph-augmented retrieval reads as one arc.

### Part VI — Dialogue and Assistants *(5 ch, new)* **SPLIT FROM OLD PART V**
1. Dialogue System Architecture & Personas *(was 24.1 + 24.2)*
2. Memory & Context Management *(was 24.3)*
3. Multi-Turn Conversation Flows *(was 24.4)*
4. Voice & Realtime Multimodal Assistants *(was 24.5 + current Part VII Ch 38 streaming sections)*
5. Tools of the Trade: Conversational AI Stack

> The 4 streaming sections currently in Part VII Ch 38 (Gemini Live, GPT-4o Realtime, Moshi/Pipecat/LiveKit, audio-latency engineering) belong with Voice Agents — they describe the same product category from the realtime-API side. Moving them here clears Part VII (Multimodal) of an off-theme chapter and unifies the voice-assistant story.

### Part VII — Agentic AI *(5 ch, was VI, unchanged content)*
1. AI Agent Foundations
2. Tool Use, Function Calling & Protocols
3. Multi-Agent Systems
4. Specialized Agents
5. Tools of the Trade: Agent Stack

### Part VIII — Multimodal Generation *(7 ch, was VII with 13)* **biggest restructure**
1. Vision-Language and Omni Models *(merges Ch 35 + 37)*
2. Image & Video Generation *(was Ch 33; image generation pulled out of merged sources)*
3. Audio & Music Generation *(was Ch 32, minus the 4 streaming sections moved to Part VI)*
4. Document Understanding and OCR *(was Ch 34)*
5. 3D Generation, World Models & Neural Scenes *(merges Ch 36 + unique parts of 41)*
6. Embodied AI: VLA Models & LLM-Powered Robotics *(merges Ch 39 + 40 + 41)*
7. Cross-Modal Reasoning & Multimodal RAG *(was Ch 42)*
8. Tools of the Trade: Multimodal Stack

**Deletions**: Ch 31 (overview duplicate), Ch 38 (4 sections moved to new Part VI Ch 4), Ch 41 (aggregator duplicate).

### Part IX — Evaluation of LLM-Based Systems *(4 ch, was VIII with 5)*
1. LLM Evaluation Fundamentals & Quality Metrics *(was Ch 44, split into 6 sections)*
2. Specialized Evaluation: RAG, Agents, Multimodal *(absorbs old Ch 45 single section + Ch 46)*
3. Online Evaluation, Observability & Production Monitoring *(was Ch 47, renumber sections to start at .1)*
4. Tools of the Trade: Eval & Production Stack

**Deletions**: Ch 45 was an orphan with one section (45.6 only) — merge into Ch 44.
**Repair**: Ch 47 starts at section 47.4 — renumber to 47.1–47.4.

### Part X — LLM Safety, Security, and Ethics *(8 ch, was IX with 12)*
1. Adversarial Security and Red Teaming *(was Ch 49)*
2. Guardrails and Runtime Safety *(was Ch 50)*
3. Agent Safety & Sandboxing *(was Ch 51)*
4. Privacy, Data Protection & Unlearning *(was Ch 52)*
5. Bias, Fairness, Hallucination & Truthfulness *(merges Ch 53 + 54)*
6. Regulation, Compliance, and Governance *(was Ch 55)*
7. Watermarking, Provenance & Transparency *(merges Ch 56 + 57)*
8. Frontier Safety, Sustainability & Open Problems *(merges Ch 58 + 59)*
9. Tools of the Trade: Safety & Guardrails Stack

**Deletions**: 4 one-section chapters (53, 54, 58, 59) absorbed by neighboring chapters.

### Part XI — LLM Operations and Production Infrastructure *(5 ch, was X with 2)* **expansion**
1. Compute Planning & Hardware Procurement *(was Ch 61)*
2. Scaling, Reliability & SLOs *(was 62.1, 62.2, 62.6)*
3. AI Gateways, Routing & Workflow Orchestration *(was 62.3, 62.4)*
4. Containers, Kubernetes & Edge Deployment *(was 62.5, 62.7–62.11)*
5. Tools of the Trade: Operations Stack *(new, broken out from Tools of the Trade context)*

### Part XII — Designing LLM-Based Products *(7 ch, was XI with 9)*
1. Ideation, Strategy & Product Hypothesis *(merges Ch 63 + 65 + 68)*
2. LLM Product Management *(was Ch 64)*
3. Prototyping via Vibe-Coding *(was Ch 66)*
4. Building the MVP *(was Ch 67)*
5. Scaling Economics: Unit Costs & ROI *(was Ch 69)*
6. Shipping and Scaling AI Products *(was Ch 70)*
7. Tools of the Trade: Idea-to-Product Toolkit

**Merge**: three near-duplicate chapters about "ideation / strategy / product hypothesis" collapsed into one.

### Part XIII — Applications Across Industries *(8 ch, was XII with 10)*
1. LLMs in Legal Practice
2. LLMs in Finance
3. LLMs in Healthcare & Biomedical
4. LLMs in Education
5. LLMs in Cybersecurity
6. LLMs in Government & Public Sector
7. LLMs in Manufacturing, Creative & Recommendation *(merges Ch 78 + 79 + 80)*
8. Tools of the Trade: Industry Solution Stack

### Part XIV — Frontiers *(5 ch, was XIII)*
1. Frontier Architectures & Scaling
2. Frontier Theory & Cognition
3. Frontier Systems & Hardware
4. AGI Trajectories & Open Questions
5. Tools of the Trade: Frontier Research Stack

---

## 6. Summary of structural changes

The split of old Part V into two parts (V Retrieval & Information Extraction + VI Dialogue & Assistants) takes the book from 13 parts to 14. All other parts shift +1 in their Roman-numeral label from the old VI (Agentic AI) onward.

| New # | Part | Old # | Chapters before | Chapters after | Net |
|---:|---|---:|---:|---:|---:|
| I    | Foundations | I | 7 | 7 | 0 |
| II   | Understanding LLMs | II | 6 | 5 | -1 |
| III  | Working with LLMs | III | 4 | 4 | 0 (15.5/15.6 move out) |
| IV   | LLM Training and Adaptation | IV | 5 | 5 | 0 |
| **V**    | **Retrieval & Information Extraction** | — (new) | — | **5** | **+5 (split)** |
| **VI**   | **Dialogue and Assistants** | — (new) | — | **5** | **+5 (split)** |
| —    | (old V Retrieval and Conversation) | V | 4 | — | -4 (split out) |
| VII  | Agentic AI | VI | 5 | 5 | 0 |
| **VIII** | **Multimodal Generation** | VII | **13** | **7** | **-6** |
| IX   | Evaluation of LLM-Based Systems | VIII | 5 | 4 | -1 |
| **X**    | **LLM Safety, Security, and Ethics** | IX | **12** | **9** | **-3** |
| **XI**   | **LLM Operations** | X | **2** | **5** | **+3** |
| **XII**  | **Designing LLM-Based Products** | XI | **9** | **7** | **-2** |
| XIII | Applications Across Industries | XII | 10 | 8 | -2 |
| XIV  | Frontiers | XIII | 5 | 5 | 0 |
| **TOTAL** | | | **87** | **81** | **-6** |

All 14 parts now sit in the 4–9 chapter band (target: 5–7). Notable boundary cases:

- **Part III (4 chapters)** — deliberately compact "first foray" before the deeper parts split the workload.
- **Part IX (4 chapters)** — Evaluation breaks cleanly into 4 cohesive topics; further splitting would dilute.
- **Part VIII (7 chapters), Part XII (7), Part XIII (8)** — at the top of the band; each chapter is a distinct stakeholder context or modality.

### Where NER / structured extraction lives

In the new structure, NER and structured information extraction are no longer buried inside a hybrid-architecture chapter — they have a full chapter in the new Part V:

  - **Part V Ch 2: Structured Information Extraction & NER** *(was section 15.5)*

This pairs naturally with the surrounding chapters: Vector retrieval (V.1) handles unstructured-to-similarity; NER (V.2) handles unstructured-to-structured; RAG (V.3, V.4) handles retrieval-as-context-for-generation; knowledge-graph construction is part of V.4 (Advanced RAG).

---

## 7. Execution plan

Each step is independently reversible and ends in an integrity-clean state.

### Phase 1: deletions (lossy)
Delete the three duplicate-aggregator chapters. Content unique to them gets re-homed first.

1. **Ch 31 (Multimodal Generation overview)** — delete; part-index already serves this role.
2. **Ch 41 (Embodied AI aggregator)** — extract unique content (41.4 World Models, 41.7 Multimodal Reasoning Frontier topics) and re-home in Ch 36 / Ch 42; delete shell.
3. **Ch 45 (Testing Quality Gates orphan)** — merge single section (45.6) into Ch 44.

### Phase 2: merges within parts
Combine sibling chapters that share topical scope.

4. Part II: merge Ch 11 + Ch 12 (Interpretability + Tools)
5. Part VII (Multimodal): merge Ch 35 + Ch 37 (VLM + Omni → Vision-Language and Omni Models)
6. Part VII: merge Ch 39 + Ch 40 (VLA + Robotics → Embodied AI)
7. Part IX (Safety): merge Ch 53 + Ch 54 (Bias + Hallucination → Bias, Fairness, Hallucination & Truthfulness)
8. Part IX: merge Ch 56 + Ch 57 (Watermarking + Transparency → Watermarking, Provenance & Transparency)
9. Part IX: merge Ch 58 + Ch 59 (Environmental + Frontier Safety → Frontier Safety, Sustainability & Open Problems)
10. Part XI: merge Ch 63 + Ch 65 + Ch 68 → Ideation, Strategy & Product Hypothesis
11. Part XII: merge Ch 78 + Ch 79 + Ch 80 → LLMs in Manufacturing, Creative & Recommendation

### Phase 3: Part V split — **biggest structural change**

12. Move Part III sec 15.5 (Structured Information Extraction) into a new chapter inside the new Part V.
13. Move Part VII Ch 38 (Streaming Multimodal — 4 sections) into a new chapter inside the new Part VI (combined with current 24.5 Voice Agents).
14. Split old Part V into:
    - New Part V — Retrieval and Information Extraction (5 chapters: Embeddings, NER, RAG Fundamentals, Advanced RAG, Tools)
    - New Part VI — Dialogue and Assistants (5 chapters: Architecture, Memory, Multi-Turn, Voice & Realtime, Tools)
15. Split old Ch 23 (9 sections) across the new Part V Ch 3 (RAG Fundamentals) and Ch 4 (Advanced RAG including knowledge graphs).

### Phase 4: other splits and renumbering

16. Part X (Operations): split Ch 62 (11 sections) into 3 chapters (Scaling/Reliability, Gateways/Orchestration, Containers/K8s/Edge).
17. Part VIII (Eval): renumber Ch 47 sections from 47.4–47.7 to 47.1–47.4.

### Phase 5: book-wide renumbering cascade

After all deletions / merges / splits / Part V split, run the canonical renumbering cascade so the chapter sequence is 0–N with no gaps. Part numbering shifts: old VI–XIII become VII–XIV.

Mechanics (same as the Parts 10–13 renumbering pattern):

- `.__tmp__` intermediate renames to avoid collisions
- in-file metadata rewrite (title, meta, breadcrumb, page-current, pagefind-meta, anchor IDs, body refs)
- cross-file href rewrite across the entire book
- regenerate toc.html, part indexes, chapter indexes
- rebuild linear nav chain

### Phase 6: audit gates

After every phase: P0 = P1 = P2 = P3 = 0, linear nav 100% coverage, toc.html matches disk.

---

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Content loss when merging chapters | Two-pass approach: extract unique H2 subsections from the merged chapter, append into the absorber chapter as new H2 blocks, then delete only the shell. |
| Broken cross-references | After each phase, run the integrity audit; a single script handles slug rewrites and section-number rewrites across the book. |
| Reader bookmark / search rot | Where chapters are merged, the new file's H2 subsection IDs preserve a sensible anchor for old anchor links (we add aliases like `id="old-X-Y-..."`). |
| Numbering cascade complexity | All in one pass with `.__tmp__` intermediates (proven pattern from the Parts 10–13 renumbering and the appendix renumbering). |

---

## 9. Open questions for the editor

1. **Part VIII Ch 44 (11 sections)** — keep as a deliberately big "foundations of evaluation" chapter, or split? Recommendation: **split into 2 chapters** (44 Fundamentals + 44b Methodology) so the band is consistent.
2. **Part XII industry chapters at 5–6 sections each** — consider trimming the per-industry "Vendors and Further Reading" template-fifth section into the Tools of the Trade chapter? Recommendation: **keep**, since the industry-specific vendor list is a key practitioner reference.
3. **Should Ch 0 (ML and PyTorch Foundations) move to a `prerequisites/` location** outside Parts entirely, akin to Appendices A/B? It sits at chapter 0 awkwardly. Recommendation: **leave at 0** for now; revisit in next major edition.

---

## 10. Decision needed

Confirm the proposed structure (or veto specific items) and I execute Phases 1–6 in order with audit gates between phases. Estimated outcome:

- **13 parts → 14 parts** (old V splits into V Retrieval+IE and VI Dialogue+Assistants)
- **87 chapters → ~81 chapters** (-6)
- **413 sections → ~370 sections** (-10%)
- Every part in 4–9 chapter band, every chapter in 3–8 section band
- NER / structured extraction gets a full chapter (Part V Ch 2), no longer buried in a hybrid-architecture chapter
- Realtime voice/streaming unifies with Voice Agents in Part VI Ch 4, no longer split between Conversation and Multimodal
- Knowledge graphs become a contiguous arc in Part V (NER → graph construction → graph-augmented retrieval)
- Zero duplicated topics across the table of contents
