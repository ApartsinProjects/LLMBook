# Module 06: Pre-training, Scaling Laws & Data Curation
## 36-Agent Deep Review Report

**Date:** 2026-03-26
**Scope:** index.html, section-6.1 through section-6.7
**Reviewed against:** chapter-plan.md and 36 agent definitions (00 through 35)

---

## Agent 00: Chapter Lead

**Overall assessment:** The module is the largest in Part II with seven well-scoped sections covering the full pre-training lifecycle. The chapter plan is thorough and the narrative arc (historical survey to math foundations to engineering to theory) is sound.

**Issues:**
1. The chapter-plan.md identifies six content gaps that remain partially unaddressed (see Agent 01 for details).
2. No Mistral or Llama 3 entries in the Section 6.1 comparison table despite being mentioned in the takeaways.

---

## Agent 01: Curriculum Alignment

**Coverage Gaps:**
1. Section 6.1: Mistral is mentioned in takeaways but absent from the landmark models table. Add a row for Mistral 7B (2023).
2. Section 6.1: Llama 3 is not mentioned despite being a major 2024 landmark (405B parameters, 15T tokens).
3. Section 6.5: The Key Takeaways bullet says "Warmup + cosine decay is the universal learning rate schedule" but the section now covers WSD too. Update the takeaway to reflect WSD.
4. Section 6.6: No mention of sequence parallelism or context parallelism (ring attention). At minimum, a brief note is warranted.
5. Section 6.2: Quiz has only 4 questions; plan calls for 5.

**Scope Creep:** None identified. All content is within scope.

**Depth Mismatches:** None significant. Advanced sections are appropriately tagged.

**Summary:** STRONG (minor gaps in model coverage and one outdated takeaway)

---

## Agent 02: Deep Explanation

**Unjustified Claims:**
1. Section 6.5: "LION matches or exceeds AdamW on many vision and language tasks" lacks specifics. Add: "on ImageNet classification and GPT-2 scale language modeling benchmarks (Chen et al., 2023)."
   Priority: LOW
2. Section 6.3: "Multi-token prediction effectively shifts the loss curve downward" is vague. Specify: "Meta (2024) reported that MTP with 4 heads improved downstream accuracy by 1 to 3 points on code benchmarks for models above 7B parameters."
   Priority: MEDIUM

**Missing Intuition:**
1. Section 6.6: Tensor parallelism column vs. row splitting is described but the worked example callout is excellent; no further changes needed.
2. Section 6.3: The 6ND compute approximation is explained well in the quiz answer but should also be briefly explained in the main text before first use.
   Priority: MEDIUM

**Summary:** Explanations are generally deep and well-motivated. Minor gaps noted above.

---

## Agent 03: Teaching Flow

**Concept Ordering:** Excellent. Each section builds on the prior: models, objectives, scaling, data, optimizers, distributed training, ICL theory.

**Pacing:** Good overall. Section 6.6 is the densest section but is broken well with diagrams and code.

**Missing Transitions:**
1. Between Section 6.4 and 6.5: The transition from data curation to optimizers could be smoother. Add a bridge sentence at the end of 6.4's takeaways or the beginning of 6.5.
   Priority: LOW (the prereq callout in 6.5 partially serves this role)

**Summary:** SMOOTH

---

## Agent 04: Student Advocate

**Confusion Points:**
1. Section 6.3: The math block for Chinchilla L(N,D) uses Greek letters without defining them inline. While alpha and beta are explained in the following paragraph, E, A, B are introduced only as "constants" which may confuse students.
   Priority: LOW (the subsequent text clarifies)

**Microlearning Structure:**
1. Section 6.2 quiz has only 4 questions while other sections have 5. Add a fifth question.
   Priority: MEDIUM
2. Section 6.4: Two consecutive "Key Insight" callouts (quality filtering section) feel redundant. Merge or differentiate them.
   Priority: MEDIUM

**Delayed Examples:** No issues. All sections introduce examples early.

**Summary:** MOSTLY CLEAR, WELL-STRUCTURED

---

## Agent 05: Cognitive Load

**Overloaded Sections:** None. Sections are well-chunked with visual breaks.

**Missing Visual Relief:** All sections have adequate diagrams, code, and callout boxes.

**Missing Checkpoints:** None significant. All sections end with quizzes and takeaway boxes.

**Summary:** MANAGEABLE

---

## Agent 06: Example and Analogy

**Missing Examples:**
1. Section 6.6: The tensor parallelism worked example in the callout is good. No gaps.

**Analogy Quality:**
1. Section 6.6: The "factory" analogy for parallelism strategies is excellent and covers all four types.
2. Section 6.4: The "humanity's attic" epigraph is memorable. No changes needed.

**Summary:** Examples and analogies are strong throughout.

---

## Agent 07: Exercise Designer

**Issues:**
1. Section 6.2: Only 4 quiz questions (all other sections have 5). Add a 5th question about Prefix LM or UL2.
   Priority: MEDIUM
2. No hands-on coding exercises beyond the inline code examples and labs. The chapter plan mentions lab exercises for 6.3, 6.4, and 6.6, which are present inline.

**Summary:** Adequate quiz coverage with one gap in Section 6.2.

---

## Agent 08: Code Pedagogy

**Issues:**
1. All code examples are well-commented, show output, and focus on one concept at a time.
2. Section 6.4: The quality filtering code example is a good addition that addresses the chapter-plan's identified gap.
3. Section 6.7: The task vector extraction code has an appropriate warning about requiring model downloads.

**Summary:** Code pedagogy is strong.

---

## Agent 09: Visual Learning

**Diagrams present:** 12 SVG diagrams across all sections. All are properly captioned with Figure numbers.

**Issues:**
1. All diagrams use consistent font families (Segoe UI for labels, Georgia for body text).
2. Color usage is consistent across sections.

**Summary:** Visual learning is well-served.

---

## Agent 10: Misconception Analyst

**Potential Misconceptions Addressed:**
1. Section 6.3: FLOPs vs. FLOPS confusion is addressed in a dedicated callout. Excellent.
2. Section 6.3: Emergence debate (Schaeffer et al.) is covered with diagram.
3. Section 6.5: L2 regularization vs. weight decay distinction is explained.

**Missing Misconception Coverage:**
1. Section 6.6: Students may confuse FSDP with DDP. The quiz question covers this well.

**Summary:** Misconceptions are well-addressed.

---

## Agent 11: Fact Integrity

**Issues:**
1. Section 6.1: GPT-4 is listed as "est. 1T+" parameters in the SVG diagram. This is speculative. Consider changing to "Undisclosed" to match the table below.
   Priority: MEDIUM
2. Section 6.1: ALBERT description says "70% fewer parameters than BERT-Large." The original paper claims different efficiency ratios depending on configuration. The statement is acceptable as a general claim.
   Priority: LOW
3. Section 6.3: Schaeffer et al. is cited as "(2024)" in Section 6.1 but as "(2023)" in Section 6.3. The paper was published in 2023 (NeurIPS 2023). Correct the Section 6.1 reference.
   Priority: HIGH

**Summary:** One date inconsistency needs correction.

---

## Agent 12: Terminology Keeper

**Issues:**
1. Section 6.5 takeaway says "Warmup + cosine decay is the universal learning rate schedule" but the section itself now covers WSD prominently. This is inconsistent.
   Priority: HIGH
2. "LLaMA" vs "Llama": Section 6.3 uses "LLaMA" (original branding) while index.html uses "Llama 2" and "Llama 3". Standardize to "Llama" (current Meta branding) throughout.
   Priority: MEDIUM
3. "pre-training" is correctly hyphenated throughout. Good.
4. "fine-tuning" is correctly hyphenated. Good.

**Summary:** Minor inconsistencies in model naming conventions.

---

## Agent 13: Cross-Reference

**Missing Forward References:**
1. Section 6.1: No forward reference to Section 6.4 when discussing Falcon's RefinedWeb. Add.
   Priority: LOW

**Missing Prerequisite References:** None. All sections have proper prereq callouts.

**Summary:** WELL-CONNECTED

---

## Agent 14: Narrative Continuity

**Opening:** Each section has a well-crafted epigraph and Big Picture callout. Tone is consistent and engaging.

**Transitions:** Mostly smooth. The prereq callouts at the start of each section serve as informal transitions.

**Closing:** All sections end with Key Takeaways boxes. Section 6.7 closes the module well by connecting back to practical implications.

**Summary:** COHESIVE

---

## Agent 15: Style and Voice

**Em Dash Audit:**
1. CSS `epigraph cite::before` uses Unicode \2014 (em dash) in all 7 section files. This is a CSS presentation element, not content text. However, per the strict rule, consider changing to a different visual separator.
   Priority: MEDIUM

**Tone:** Consistent semi-formal, authoritative but approachable voice throughout.

**Passive Voice:** Minimal. Writing is predominantly active.

**Summary:** UNIFIED (one CSS em dash pattern to address)

---

## Agent 16: Engagement Designer

**Epigraphs:** Every section has a witty, on-theme epigraph. These are excellent engagement hooks.

**Monotonous Stretches:** None identified. Good variety of prose, code, diagrams, callouts, and tables.

**Summary:** ENGAGING

---

## Agent 17: Senior Editor

### Chapter Scorecard

| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Wording | 4.5 | Clear, precise prose throughout |
| Structure | 5 | Seven well-organized sections with consistent template |
| Figures | 4.5 | 12 SVGs, all captioned, consistent style |
| Exercises | 4 | Good quizzes; Section 6.2 needs one more question |
| Pedagogy | 5 | Strong "why before how" approach |
| Clarity | 4.5 | Explanations are deep and accessible |
| Market Quality | 4.5 | Competitive with top resources |
| **Overall** | **4.5** | |

**Publication Readiness:** READY (minor revisions)

---

## Agent 18: Research Scientist

**Depth Opportunities:**
1. Section 6.5: muP (Maximal Update Parametrization) Paper Spotlight is already present. Good.
2. Section 6.7: The implicit gradient descent treatment is thorough with code demonstration.

**Unsettled Science Handled Well:**
1. Emergence debate in 6.3 properly qualified.
2. Mesa-optimization in 6.7 properly flagged as speculative.

**Missing Frontier Content:**
1. Section 6.6: No mention of sequence parallelism or ring attention for long-context training. Add a brief note.
   Priority: MEDIUM

**Summary:** RICH

---

## Agent 19: Structural Architect

**Structure:** Clean, consistent template across all sections (nav, header, epigraph, big-picture, prereq, content, quiz, takeaways, nav, footer).

**Issues:**
1. Section 6.1 uses expanded CSS while 6.2 through 6.7 use compressed single-line CSS. This is a maintenance concern, not a rendering issue.
   Priority: LOW (cosmetic)

**Summary:** WELL-STRUCTURED

---

## Agent 20: Content Update Scout

**Missing Topics (Essential Now):**
1. Section 6.1: Llama 3 (2024) with 405B parameters and 15T tokens. Major open-weight milestone.
   Priority: HIGH
2. Section 6.1: Mistral 7B should be in the comparison table.
   Priority: MEDIUM

**Outdated Content:**
1. Section 6.5 takeaway about "universal" cosine decay schedule is outdated now that WSD is covered.
   Priority: HIGH

**Summary:** MOSTLY CURRENT

---

## Agent 21: Self-Containment Verifier

**Assessment:** All sections have proper prerequisite callouts referencing earlier modules. Mathematical prerequisites are explained inline.

**Summary:** SELF-CONTAINED

---

## Agent 22: Title and Hook Architect

**Assessment:** Section titles are clear and descriptive. Epigraphs provide excellent hooks. Subtitles are informative.

**Minor suggestion:** Section 6.7's subtitle could be more intriguing.

**Summary:** COMPELLING

---

## Agent 23: Project Catalyst

**Assessment:** Lab exercises are present inline in Sections 6.3, 6.4, and 6.6. Code examples are practical and buildable.

**Summary:** ADEQUATE

---

## Agent 24: Aha-Moment Engineer

**Assessment:** Multiple well-placed Key Insight callouts throughout. The "your optimizer is bigger than your model" insight in 6.5 is particularly effective.

**Summary:** Strong aha-moments present.

---

## Agent 25: First-Page Converter

**Assessment:** All sections open with engaging epigraphs followed by Big Picture callouts that explain "why this matters." Section openings are strong.

**Summary:** Strong first-page hooks across all sections.

---

## Agent 26: Visual Identity Director

**Assessment:** Consistent visual design across all sections. Color scheme, typography, and layout are uniform.

**Issue:** Section 6.1 has expanded CSS formatting while other sections use compressed format. Not a visual issue but a code consistency issue.

**Summary:** Consistent visual identity.

---

## Agent 27: Research Frontier Mapper

**Frontiers Covered:**
1. Section 6.3: Inference-time scaling (o1/o3, DeepSeek-R1) referenced with forward pointer.
2. Section 6.2: Alternative architectures (Mamba, RWKV) mentioned.
3. Section 6.4: Data wall and synthetic data discussed.
4. Section 6.6: FP8 training (DeepSeek V3) covered.

**Missing:**
1. Section 6.6: Sequence parallelism / ring attention for long-context training.
   Priority: MEDIUM

**Summary:** Good frontier coverage.

---

## Agent 28: Demo/Simulation Designer

**Assessment:** Code demos are present in all sections with realistic outputs. The scaling law curve-fitting lab in 6.3 is particularly effective.

**Summary:** Good demo coverage.

---

## Agent 29: Memorability Designer

**Assessment:** Epigraphs are memorable and quotable. Key insights are well-framed. The "97% of the internet is not worth training on" statistic in 6.4 is sticky.

**Summary:** High memorability.

---

## Agent 30: Skeptical Reader

**Issues:**
1. Section 6.1: GPT-4 "est. 1T+" in diagram is speculative and should be qualified.
   Priority: MEDIUM
2. Section 6.3: The 6ND approximation is stated but the derivation of the factor 6 appears only in the quiz answer, not in the main text.
   Priority: MEDIUM

**Summary:** Claims are generally well-supported.

---

## Agent 31: Plain Language Rewriter

**Assessment:** Writing is accessible throughout. Technical terms are defined on first use. Sentences are clear.

**Summary:** CLEAR

---

## Agent 32: Sentence Flow Smoother

**Assessment:** Good sentence variety. No monotonous stretches. Transitions are smooth.

**Summary:** SMOOTH

---

## Agent 33: Jargon Gatekeeper

**Assessment:** All major terms are defined on first use. Acronyms are expanded.

**Summary:** WELL-GUARDED

---

## Agent 34: Micro-Chunking Editor

**Assessment:** Sections are well-chunked with subsections, callouts, and visual breaks every few paragraphs.

**Summary:** WELL-CHUNKED

---

## Agent 35: Reader Fatigue Detector

**Assessment:** Good pacing throughout. Dense sections (6.5, 6.6) are broken up with code examples and diagrams. Epigraphs provide tonal relief.

**Summary:** LOW FATIGUE RISK

---

## Consolidated Fix List

### TIER 1 (Must Fix)
| # | File | Issue | Fix |
|---|------|-------|-----|
| 1 | section-6.1.html | Schaeffer et al. cited as "(2024)" but paper is 2023 | Change "2024" to "2023" |
| 2 | section-6.5.html | Takeaway says cosine decay is "universal" but section now covers WSD | Update takeaway to include WSD |
| 3 | section-6.1.html | Missing Llama 3 and Mistral from comparison table | Add table rows |
| 4 | section-6.3.html | "LLaMA" should be "Llama" per current Meta branding | Standardize naming |

### TIER 2 (Should Fix)
| # | File | Issue | Fix |
|---|------|-------|-----|
| 5 | section-6.2.html | Only 4 quiz questions (plan calls for 5) | Add 5th question about Prefix LM or UL2 |
| 6 | section-6.1.html | GPT-4 "est. 1T+" in SVG is speculative | Change to "Undisclosed" |
| 7 | section-6.4.html | Two consecutive Key Insight callouts are redundant | Merge into one |
| 8 | section-6.6.html | No mention of sequence/context parallelism | Add brief note |
| 9 | section-6.3.html | 6ND approximation derivation only in quiz answer | Add brief inline explanation |
| 10 | all section files | CSS epigraph cite::before uses em dash (\2014) | Replace with a different separator |

### TIER 3 (Nice to Have)
| # | File | Issue | Fix |
|---|------|-------|-----|
| 11 | section-6.1.html | No forward reference to 6.4 when mentioning Falcon's RefinedWeb | Add cross-reference |
| 12 | section-6.5.html | LION claim lacks specifics | Add benchmark reference |
| 13 | section-6.3.html | MTP scaling benefit claim is vague | Add specific numbers |
