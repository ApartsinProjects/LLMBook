# Book v4 Restructuring Plan

**Date:** 2026-03-28
**Current state:** 7 parts, 29 chapters (modules 0-28), ~141 section HTML files, 10 appendices
**Book title:** Building Conversational AI using LLM and Agents

---

## 1. Executive Summary

**Recommendation: Evolutionary restructuring (Option B below), not a 4-pillar revolution.**

The current 7-part structure is pedagogically sound and follows a natural learning progression. A 4-pillar reorg would break this progression and force awkward placement decisions. Instead, the recommended approach is:

1. **Keep 7 parts** with minor boundary adjustments (rename Part VII, rebalance Part IV)
2. **Expand to 32 chapters** by adding 3 new chapters (Reasoning, Data Engineering, AGI/Frontier Capstone)
3. **Promote 2 sections** to full chapter status (Information Extraction from 11.5; Reasoning from 7.3)
4. **Do NOT split agents into 4 chapters** (current 2-chapter treatment is well-structured)
5. **Relocate Interpretability** from Part IV to Part II (better conceptual fit)

Net result: 7 parts, 32 chapters, ~155 sections. Minimal file moves; maximum content coherence.

---

## 2. Task 1: Evaluation of the 4-Pillar Structure

### Proposed 4-Pillar Model

| Pillar | Content |
|--------|---------|
| **Representation** | Ch 0-4, 18 (embeddings), 17 (interpretability) |
| **Generation** | Ch 5-8, 12-16 (training, alignment) |
| **Retrieval + Reasoning** | Ch 20-22, 10 (prompting), 11 (hybrid) |
| **Deployment + Safety** | Ch 10, 25-28, 23-24 (applications) |

### Assessment: NOT RECOMMENDED

**Pros:**
- Intellectually elegant; maps well to a research taxonomy
- Each pillar has a clear conceptual identity
- Good for reference use (jump to the pillar you need)

**Cons (decisive):**
- **Breaks the learning progression.** The current structure takes students from "what is NLP?" to "deploy a production agent." The 4-pillar model would require students to jump between pillars (e.g., you need embeddings from Pillar 1 before RAG in Pillar 3, but they are in different parts)
- **Awkward placement problems.** Where does Prompt Engineering go? It touches Representation (understanding tokens), Generation (controlling output), and Retrieval (query formulation). Where do LLM APIs go? They are used in all four pillars.
- **Unbalanced sizes.** "Generation" pillar would have ~14 chapters; "Representation" would have ~7. The imbalance undermines the structural elegance.
- **Massive migration cost.** Nearly every chapter would need renumbering, directory moves, and cross-reference updates. The ~500+ internal hyperlinks would all break.
- **Not how practitioners learn.** Engineers typically progress linearly from foundations to deployment, not by switching between conceptual pillars.

**Verdict:** The 4-pillar model works well as a mental framework (consider adding a "Four Pillars" diagram to the introduction) but not as a book structure. Keep the current linear progression.

---

## 3. Task 2: Evaluation of New Chapter Proposals

### 3a. Information Extraction Chapter

**Current state:** Section 13.5 (IE with LLMs) inside Ch 13 (Hybrid ML+LLM). Contains NER, relation extraction, event extraction, coreference, structured output.

**Recommendation: Keep as a section; do NOT promote to standalone chapter.**

| Factor | Assessment |
|--------|------------|
| Content depth | 11.5 is already substantial (7 bullet points, a lab) |
| Standalone coherence | IE is a task, not an architectural concept; it fits naturally as a "case study" within the hybrid chapter |
| Reader demand | Most readers will use LLM-based IE via prompt engineering, not build IE pipelines from scratch |
| Competitive positioning | Stanford CS336 and CMU ANLP do not have standalone IE chapters |
| Expansion opportunity | Could expand 11.5 into 11.5 + 11.6 (splitting classical IE from LLM-based IE) if needed |

**Action:** Expand 11.5 content if desired, but keep it within Ch 13. Add a cross-reference from Ch 1.1 (NLP task taxonomy) to 11.5.

---

### 3b. Agent Chapter Expansion (2 to 4 chapters)

**Current state:** Ch 22 (AI Agents, 5 sections: foundations, tools, planning, code agents, reasoning) + Ch 23 (Multi-Agent, 4 sections: frameworks, patterns, workflows, production).

**Recommendation: Do NOT split into 4 chapters.**

| Factor | Assessment |
|--------|------------|
| Current coverage | Ch 22 and 22 together have 9 sections; this is already comprehensive |
| Topic boundaries | Planning, tools, and memory are deeply intertwined in practice; separating them creates artificial boundaries |
| Memory coverage | Already well-covered in 20.3 (Memory and Context Management) and 21.1 (agent memory data structures). A standalone "Memory" chapter would be thin. |
| Multi-agent | Already a standalone chapter (22); no split needed |
| Industry trend | Agent frameworks (LangGraph, CrewAI) treat tool-use, planning, and memory as integrated concepts, not separate modules |

**Action:** Keep the 2-chapter structure. If content grows, add sections within existing chapters rather than splitting.

---

### 3c. Data Engineering Chapter

**Current state:** Data curation is split between Ch 6.4 (pre-training data curation) and Ch 13 (synthetic data generation, 7 sections).

**Recommendation: Create a new chapter, but via PROMOTION rather than new content.**

The proposal has merit because data engineering for LLMs is a distinct skill set that deserves first-class treatment. However, the content already exists; it just needs consolidation.

**Proposed new chapter: "Data Engineering for LLMs"**
- Relocate Ch 6.4 (Data Curation at Scale) as the foundation
- Relocate Ch 13.4 (Quality Assurance and Data Curation)
- Relocate Ch 13.5 (LLM-Assisted Labeling)
- Relocate Ch 13.6 (Weak Supervision)
- Add new section: Data Pipelines and Versioning (content currently scattered in 18.4 and 25.7)

**Tradeoff:** This breaks the clean narrative of Ch 6 (pretraining story) and Ch 13 (synthetic data story). The compromise is to keep the content where it is but add a "Data Engineering Track" reading guide in the introduction that links 6.4, 12.4, 12.5, 12.6, and 18.4 as a cross-chapter learning path.

**Final recommendation:** Add a reading path guide rather than physically restructuring. The current placement optimizes for the linear reader; a reading path serves the reference reader.

---

### 3d. Reasoning and Test-Time Compute Chapter

**Current state:** Section 7.3 (Reasoning and Test-Time Compute) in Ch 7 (Modern LLM Landscape), plus 16.4 (RLVR), 21.5 (Reasoning Models and Agent Architecture), 10.5 (Prompting Reasoning Models).

**Recommendation: PROMOTE to standalone chapter. This is the strongest candidate for expansion.**

**Justification:**
- Reasoning models (o1, o3, R1, QwQ) represent a paradigm shift in LLM capabilities
- Test-time compute scaling is arguably the most important development since the original scaling laws
- Currently scattered across 4 chapters (7.3, 10.5, 16.4, 21.5), which fragments a coherent topic
- A standalone chapter would consolidate: architectures, training (RLVR/GRPO), prompting strategies, agent integration, and compute-optimal inference
- Competitive positioning: this would be a differentiator vs. existing textbooks

**Proposed chapter: "Reasoning Models and Test-Time Compute"**
1. The test-time compute paradigm (from 7.3)
2. Reasoning model architectures: o1, o3, R1, QwQ (from 7.3)
3. Training reasoning models: RLVR, GRPO, process reward models (consolidate from 16.4)
4. Prompting and using reasoning models (from 10.5)
5. Monte Carlo Tree Search and search-based reasoning (from 7.3 and 21.3)
6. Compute-optimal inference: when to think longer vs. use a bigger model
7. Reasoning in agents: extended thinking for planning and tool use (from 21.5)

**Placement:** Part II (Understanding LLMs) as the new Ch 10, pushing Inference Optimization to Ch 10.

---

### 3e. AGI/Frontier Capstone Chapter

**Current state:** No dedicated treatment. Frontier topics are scattered (emergent abilities in 6.3, alignment in 16.3, governance in 27.5).

**Recommendation: ADD as the final chapter (Ch 31 or equivalent) in Part VII.**

**Justification:**
- The book currently ends on "Strategy, Product Management, and ROI," which is anticlimactic for a technical textbook
- A capstone "frontier" chapter would provide intellectual closure and forward-looking perspective
- Topics: emergent abilities debate, alignment research frontiers, AI governance, open problems in LLM research, the path to AGI (if any), societal implications
- This chapter should be explicitly marked as speculative/opinion and dated (acknowledge rapid obsolescence)

**Proposed chapter: "Frontiers: Open Problems, Alignment, and the Road Ahead"**
1. Emergent abilities: real or mirage? (expand from 6.3)
2. Scaling frontiers: what comes after current scaling laws
3. Alignment research frontiers: scalable oversight, interpretability-based alignment
4. AI governance: international coordination, compute governance, open-source vs. closed
5. Open problems in LLM research (compositionality, planning, world models, grounding)
6. Societal impact: labor markets, education, creative industries, inequality

**Placement:** Final chapter of the book, after Part VII.

---

## 4. Task 3: Content Gap Analysis (Recent Additions)

### Recently Added Sections

| Section | Current Location | Structural Promotion? |
|---------|-----------------|----------------------|
| **8.5: Model Pruning and Sparsity** | Ch 10 (Inference Optimization) | No. Fits well as a section within inference optimization. |
| **24.7: Robotics, Embodied AI, Scientific Discovery** | Ch 25 (Applications) | No. Applications chapter is the right place for vertical surveys. |
| **7.4: Multilingual and Cross-Cultural LLMs** | Ch 7 (Modern LLM Landscape) | No. Good as a section. Could expand to 2 sections if multilingual content grows. |
| **4.3: SSM/Mamba content** | Ch 4 (Transformer Variants) | **Consider.** SSMs are becoming a distinct architectural family. If Mamba/RWKV/Jamba content exceeds ~3000 words, consider splitting 4.3 into two sections: "Efficient Attention Variants" (Flash, MQA, GQA, MLA) and "Alternative Architectures" (SSMs, RWKV, hybrid). But do not promote to a standalone chapter yet. |
| **13.7: Long Context** | Ch 14 (Fine-Tuning) | No. Fits well within fine-tuning fundamentals. |
| **9.4: Reasoning Models and Multimodal APIs** | Ch 10 (LLM APIs) | Relocate to the proposed Reasoning chapter (API usage of reasoning models). Keep a brief pointer in Ch 10. |
| **10.5: Prompting Reasoning Models** | Ch 11 (Prompt Engineering) | Relocate to the proposed Reasoning chapter. Keep a brief pointer in Ch 11. |
| **12.7: Synthetic Reasoning Data** | Ch 13 (Synthetic Data) | Relocate to the proposed Reasoning chapter (training data for reasoning models). Keep a brief pointer in Ch 13. |
| **18.5: Vision-Based Document Retrieval** | Ch 19 (Embeddings) | No. Good as a section. |
| **21.5: Reasoning Models and Agent Architecture** | Ch 22 (AI Agents) | Relocate to the proposed Reasoning chapter. Keep a brief pointer in Ch 22. |
| **22.4: Production Multi-Agent Systems** | Ch 23 (Multi-Agent) | No. Good fit in the multi-agent chapter. |
| **23.4: Unified Multimodal Models** | Ch 24 (Multimodal) | No. Good fit. |
| **25.8: Arena-Style Evaluation** | Ch 27 (Evaluation) | No. Good fit. |

**Key insight:** The Reasoning topic is the one area where structural promotion is clearly warranted. Four different chapters (7, 10, 12, 21) each have a reasoning-related section that would benefit from consolidation.

---

## 5. Task 4: Chapter Count Decision

### Option Analysis

| Option | Count | Pros | Cons |
|--------|-------|------|------|
| **A: Keep 29** | 29 | No migration cost | Misses reasoning consolidation opportunity |
| **B: Expand to 31** | 31 | Adds Reasoning + AGI chapters; minimal disruption | Slightly more content to maintain |
| **C: Expand to 32-35** | 32-35 | Also adds Data Engineering, splits agents | Diminishing returns; splitting agents is counterproductive |
| **D: Compress to 25** | 25 | Tighter book | Would require merging healthy chapters; loss of granularity |

**Recommendation: Option B (31 chapters)**

Add:
1. **Ch 10 (new): Reasoning Models and Test-Time Compute** (consolidate from 7.3, 10.5, 12.7, 16.4, 21.5)
2. **Ch 32 (new): Frontiers: Open Problems, Alignment, and the Road Ahead** (new content + expanded 6.3 emergent abilities)

Relocate:
3. **Interpretability (current Ch 19)** from Part IV to Part II (it is about understanding models, not training them)

This gives us 31 chapters (29 existing minus ~4 sections relocated to the new Reasoning chapter, plus 2 new chapters, with Interpretability relocated but not deleted).

---

## 6. Task 5: Proposed Part Boundaries

### Recommended Structure (v4)

```
Part I: Foundations (6 chapters, Ch 0-5)
  Unchanged. The onramp from ML basics through transformers and decoding.

Part II: Understanding LLMs (5 chapters, Ch 6-10)
  Ch 6: Pre-training, Scaling Laws, Data Curation
  Ch 7: Modern LLM Landscape and Model Internals
  Ch 10: [NEW] Reasoning Models and Test-Time Compute
  Ch 10: Inference Optimization and Efficient Serving (renumbered from old Ch 10)
  Ch 11: [RELOCATED] Interpretability and Mechanistic Understanding (from old Ch 19)

Part III: Working with LLMs (3 chapters, Ch 13-13)
  Ch 13: Working with LLM APIs (renumbered from old Ch 10)
  Ch 13: Prompt Engineering and Advanced Techniques (renumbered from old Ch 11)
  Ch 14: Hybrid ML+LLM Architectures (renumbered from old Ch 13)

Part IV: Training and Adapting (5 chapters, Ch 15-18)
  Ch 15: Synthetic Data Generation (renumbered from old Ch 13)
  Ch 16: Fine-Tuning Fundamentals (renumbered from old Ch 14)
  Ch 17: Parameter-Efficient Fine-Tuning (renumbered from old Ch 15)
  Ch 19: Knowledge Distillation and Model Merging (renumbered from old Ch 16)
  Ch 19: Alignment: RLHF, DPO, Preference Tuning (renumbered from old Ch 17)

Part V: Retrieval and Conversation (3 chapters, Ch 20-21)
  Ch 20: Embeddings, Vector Databases, Semantic Search (renumbered from old Ch 19)
  Ch 22: Retrieval-Augmented Generation (renumbered from old Ch 20)
  Ch 22: Building Conversational AI Systems (renumbered from old Ch 22)

Part VI: Agents and Applications (5 chapters, Ch 23-26)
  Ch 23: AI Agents: Tool Use, Planning, Reasoning (renumbered from old Ch 22)
  Ch 24: Multi-Agent Systems (renumbered from old Ch 23)
  Ch 25: Multimodal Generation (renumbered from old Ch 24)
  Ch 27: LLM Applications (renumbered from old Ch 25)
  Ch 27: Evaluation, Experiment Design, Observability (renumbered from old Ch 27)

Part VII: Production, Safety, and Strategy (5 chapters, Ch 28-31)
  Ch 28: Production Engineering and Operations (renumbered from old Ch 27)
  Ch 29: Safety, Ethics, and Regulation (renumbered from old Ch 28)
  Ch 29: LLM Strategy, Product Management, ROI (renumbered from old Ch 29)
  Ch 29: [NEW] Frontiers: Open Problems, Alignment, and the Road Ahead
```

### Balance Check

| Part | Chapters | Sections (est.) | Focus |
|------|----------|-----------------|-------|
| I: Foundations | 6 | 23 | Theory + implementation basics |
| II: Understanding LLMs | 5 | 25 | How LLMs work at depth |
| III: Working with LLMs | 3 | 14 | Practical API/prompt skills |
| IV: Training | 5 | 24 | Adaptation techniques |
| V: Retrieval | 3 | 16 | RAG and conversation |
| VI: Agents | 5 | 28 | Applications and evaluation |
| VII: Production | 4 | ~20 | Deployment and strategy |
| **Total** | **31** | **~150** | |

Parts III and V are smaller (3 chapters each) but this reflects their scope. Each part remains self-contained and readable independently.

---

## 7. Task 6: Migration Plan

### IMPORTANT CAVEAT

The restructuring proposed above involves renumbering nearly every chapter (8-28 become 9-29+). This is a high-cost operation. There are two implementation strategies:

### Strategy A: Full Renumber (Recommended if doing a major release)

**Phase 1: Create the new Reasoning chapter**
1. Create directory: `part-2-understanding-llms/module-10-reasoning-test-time-compute/`
2. Create new files:
   - `index.html` (chapter index)
   - `section-10.1.html` through `section-10.7.html`
3. Content migration:
   - Move 7.3 content to new 8.1 + 8.2 (paradigm + architectures)
   - Move 16.4 RLVR content to new 8.3 (training reasoning models)
   - Move 10.5 content to new 8.4 (prompting reasoning models)
   - Move 12.7 content to new 8.5 (synthetic reasoning data)
   - Move 21.5 content to new 8.6 (reasoning in agents)
   - Write new 8.7 (compute-optimal inference; expand from 7.3 subsection)
4. Add stub pointers in the source chapters (7.3, 10.5, 12.7, 16.4, 21.5) redirecting to the new chapter

**Phase 2: Relocate Interpretability**
1. Move `part-4-training-adapting/module-19-interpretability/` to `part-2-understanding-llms/module-12-interpretability/`
2. Update all cross-references pointing to old Ch 19

**Phase 3: Create AGI/Frontier capstone chapter**
1. Create directory: `part-7-production-strategy/module-30-frontiers/`
2. Create new files: `index.html`, `section-29.1.html` through `section-29.6.html`
3. Mostly new content; expand emergent abilities discussion from 6.3

**Phase 4: Renumber all chapters**
This is the most labor-intensive step. Every module directory would need renaming, and every cross-reference in ~150 HTML files would need updating.

**Estimated effort:** 4-6 hours with scripted assistance
**Risk:** High. Any missed cross-reference creates a broken link.

### Strategy B: Additive Only (Recommended for incremental approach)

Do NOT renumber existing chapters. Instead:

1. Add the Reasoning chapter as **module-07b** or insert it at a new number
2. Add the Frontier chapter as **module-29**
3. Keep Interpretability where it is (Ch 19) but add a note in Part II linking to it
4. Update the index.html to reorder the visual presentation without changing file paths

**Estimated effort:** 2-3 hours
**Risk:** Low. No existing links break. The chapter numbers become non-sequential (0-7, 7b, 8, 9, 10, 11, 12-16, 17, 18-28, 29), which is cosmetically ugly but functionally fine.

### Recommended: Strategy B now, Strategy A for a future "v4.0 release"

Implement the additive changes now to get the content benefits immediately. Schedule the full renumber for a dedicated release when you can run automated link-checking.

---

## 8. Detailed File Operations (Strategy B)

### New Files to Create

```
part-2-understanding-llms/module-08-reasoning-test-time-compute/
  index.html
  section-8.1.html  (Test-time compute paradigm)
  section-8.2.html  (Reasoning model architectures)
  section-8.3.html  (Training: RLVR and GRPO)
  section-8.4.html  (Prompting reasoning models)
  section-8.5.html  (Search-based reasoning: MCTS, AlphaProof)
  section-8.6.html  (Compute-optimal inference)
  section-8.7.html  (Reasoning in agents)

part-7-production-strategy/module-30-frontiers/
  index.html
  section-29.1.html  (Emergent abilities debate)
  section-29.2.html  (Scaling frontiers)
  section-29.3.html  (Alignment research frontiers)
  section-29.4.html  (AI governance and compute governance)
  section-29.5.html  (Open problems)
  section-29.6.html  (Societal impact)
```

### Sections to Consolidate (content moves to Reasoning chapter)

| Source | Content | Destination | Source Treatment |
|--------|---------|-------------|-----------------|
| 7.3 (Reasoning and Test-Time Compute) | Full section | 7b.1 + 7b.2 + 7b.5 + 7b.6 | Replace with 2-paragraph summary + link to 7b |
| 10.5 (Prompting Reasoning Models) | Full section | 7b.4 | Replace with 1-paragraph summary + link to 7b |
| 12.7 (Synthetic Reasoning Data) | Full section | 7b.3 (partial) | Replace with 1-paragraph summary + link to 7b |
| 16.4 (RLVR) | Partial (GRPO details) | 7b.3 | Keep RLVR in 16.4 but add cross-ref to 7b.3 for deeper treatment |
| 21.5 (Reasoning Models and Agent Architecture) | Full section | 7b.7 | Replace with 1-paragraph summary + link to 7b |

### Cross-References to Update

After creating the Reasoning chapter, update these references:
- `index.html`: Add new chapter entry between Ch 7 and Ch 10
- Ch 7 index: Link to the new Reasoning chapter
- Ch 10.4: Update reference to reasoning model content
- Ch 17 index: Add cross-reference to Reasoning chapter for RLVR context
- Ch 22 index: Add cross-reference to Reasoning chapter for agent reasoning

After creating the Frontier chapter:
- `index.html`: Add new chapter entry at the end of Part VII
- Ch 6.3: Add forward reference to Frontier chapter for emergent abilities
- Ch 17.3: Add forward reference for alignment research frontiers

---

## 9. Risk Assessment

### High Risk
- **Broken cross-references.** The book has ~500+ internal hyperlinks. Any restructuring that moves files will break links. Mitigation: Run a link-checker script after any migration.
- **Disrupted reading flow.** Removing content from existing chapters (7.3, 10.5, etc.) could leave those chapters feeling incomplete. Mitigation: Always leave a summary paragraph and link.

### Medium Risk
- **Content duplication.** The Reasoning chapter consolidates content from 5 sources. There is risk of duplicating material rather than cleanly relocating it. Mitigation: One author should own the migration.
- **Scope creep.** The Frontier capstone chapter could expand indefinitely. Mitigation: Cap it at 6 sections and explicitly mark it as "perspective" not "reference."

### Low Risk
- **Chapter count.** 31 chapters is well within norms for technical textbooks (Jurafsky and Martin has 28; Bishop has 13 long ones; Goodfellow has 20).
- **Reader confusion from additive numbering.** Using "7b" is unusual but readers will adapt.

---

## 10. Decision Points for the Author

These decisions require human judgment and cannot be resolved by structural analysis alone:

### Decision 1: Full renumber vs. additive approach
- Full renumber gives cleaner aesthetics but costs 4-6 hours and risks breaking links
- Additive approach is safer but results in non-sequential numbering
- **Recommendation:** Additive now, full renumber at a planned release milestone

### Decision 2: Interpretability relocation
- Moving Ch 19 (Interpretability) from Part IV to Part II makes conceptual sense (it is about understanding, not training)
- However, the prerequisite chain works: readers need to understand training (Part IV context) before mechanistic interpretability techniques
- **Recommendation:** Keep it in Part IV for now. The prerequisite argument is stronger than the taxonomic argument.

### Decision 3: Data Engineering reading path vs. new chapter
- A "Data Engineering for LLMs" chapter would consolidate 6.4, 12.4-12.6, and 18.4
- But this breaks the narrative flow of the existing chapters
- **Recommendation:** Add a "Reading Paths" section to the book introduction instead. Define 4-5 paths (e.g., "Data Engineering Track," "Agent Builder Track," "Researcher Track") that cross-reference chapters.

### Decision 4: Reasoning chapter depth
- The proposed Reasoning chapter could be 7 sections (comprehensive) or 4 sections (focused)
- 7 sections risks being the largest chapter in the book
- 4 sections means some content stays distributed
- **Recommendation:** Start with 5 sections (paradigm, architectures, training, prompting, agents). Add search-based reasoning and compute-optimal inference only if they have enough unique content to justify standalone sections.

### Decision 5: Frontier capstone tone
- Should this be a neutral survey of open problems, or include opinionated perspectives?
- Neutral is safer for a textbook; opinionated is more engaging
- **Recommendation:** Primarily neutral survey with clearly labeled "author perspective" sidebars for opinions. Date-stamp the chapter prominently.

### Decision 6: Part VII naming
- Current: "Production and Strategy"
- The directory is `part-7-production-strategy` but the git status shows files in both `module-28-production-safety-ethics` and `module-29-strategy-product-roi`
- The index.html shows Ch 27 as "Production Engineering," Ch 28 as "Safety, Ethics, Regulation," Ch 29 as "Strategy, Product, ROI"
- **Recommendation:** Rename Part VII to "Production, Safety, and Strategy" to better reflect its actual 3-chapter scope (4 with the new Frontier chapter).

---

## 11. Current vs. Proposed Structure Comparison

### Current Structure (v3)

```
Part I: Foundations (6 ch, 0-5)
Part II: Understanding LLMs (3 ch, 6-8)
Part III: Working with LLMs (3 ch, 9-11)
Part IV: Training and Adapting (6 ch, 12-17)
Part V: Retrieval and Conversation (3 ch, 18-20)
Part VI: Agents and Applications (5 ch, 21-25)
Part VII: Production and Strategy (3 ch, 26-28)
Total: 29 chapters
```

### Proposed Structure (v4)

```
Part I: Foundations (6 ch, 0-5) [UNCHANGED]
Part II: Understanding LLMs (4 ch, 6-8 + 7b) [+1 Reasoning chapter]
Part III: Working with LLMs (3 ch, 9-11) [UNCHANGED]
Part IV: Training and Adapting (6 ch, 12-17) [UNCHANGED]
Part V: Retrieval and Conversation (3 ch, 18-20) [UNCHANGED]
Part VI: Agents and Applications (5 ch, 21-25) [UNCHANGED]
Part VII: Production, Safety, and Strategy (4 ch, 26-29) [+1 Frontier chapter]
Total: 31 chapters
```

### Changes Summary

| Change | Type | Impact |
|--------|------|--------|
| Add Reasoning chapter (7b) | New chapter | Consolidates content from 5 existing sections |
| Add Frontier capstone (29) | New chapter | Entirely new content |
| Slim 7.3, 10.5, 12.7, 21.5 | Section demotion | Replaced with summaries + links |
| Add reading paths to intro | Navigation | New section in index.html |
| Rename Part VII | Cosmetic | Label change only |

---

## 12. Appendix: Section Count by Chapter (Current)

For reference, the current section counts per chapter:

| Chapter | Sections | Assessment |
|---------|----------|------------|
| 0: ML Foundations | 4 | Appropriate |
| 1: NLP Foundations | 4 | Appropriate |
| 2: Tokenization | 3 | Appropriate |
| 3: Attention | 3 | Appropriate |
| 4: Transformer | 5 | Heavy; 4.3 could split |
| 5: Decoding | 4 | Appropriate |
| 6: Pre-training | 7 | Heavy; justified by scope |
| 7: LLM Landscape | 4 | Will become 3 after Reasoning extraction |
| 8: Inference | 6 | Heavy; justified by scope |
| 9: APIs | 4 | Appropriate |
| 10: Prompting | 5 | Will become 4 after Reasoning extraction |
| 11: Hybrid ML+LLM | 5 | Appropriate |
| 12: Synthetic Data | 7 | Heavy; will become 6 after Reasoning extraction |
| 13: Fine-Tuning | 7 | Heavy; justified by scope |
| 14: PEFT | 3 | Could be expanded (only 3 sections for a critical topic) |
| 15: Distillation | 3 | Appropriate |
| 16: Alignment | 4 | Appropriate |
| 17: Interpretability | 4 | Appropriate |
| 18: Embeddings | 5 | Appropriate |
| 19: RAG | 6 | Appropriate |
| 20: Conversational AI | 5 | Appropriate |
| 21: Agents | 5 | Will become 4 after Reasoning extraction |
| 22: Multi-Agent | 4 | Appropriate |
| 23: Multimodal | 4 | Appropriate |
| 24: Applications | 7 | Heavy; justified by breadth |
| 25: Evaluation | 8 | Heaviest chapter; consider splitting into "Evaluation" and "Observability" |
| 26: Production | 4 | Appropriate |
| 27: Safety | 7 | Appropriate for the breadth of topics |
| 28: Strategy | 5 | Appropriate |

### Notable Imbalances
- **Ch 27 (8 sections)** is the heaviest chapter. Consider splitting into "Evaluation and Testing" (25.1-25.4) and "Observability and Monitoring" (25.5-25.8) if the book expands further.
- **Ch 15 (3 sections)** is light for such an important topic (LoRA is one of the most-used techniques). Consider adding a section on "LoRA in Practice: Debugging, Hyperparameter Selection, and Common Pitfalls."

---

## 13. Implementation Priority

1. **Immediate (this release):** Create the Reasoning chapter (7b) by consolidating existing content. This is the highest-value, lowest-risk change.
2. **Next release:** Create the Frontier capstone chapter (29). This requires new content authoring.
3. **Future release:** Full renumbering to clean up chapter sequence. Run automated link-checking.
4. **Deferred:** Reading paths in introduction (nice-to-have, not blocking).
5. **Not recommended:** 4-pillar restructure, agent chapter split, IE standalone chapter, Data Engineering standalone chapter.
