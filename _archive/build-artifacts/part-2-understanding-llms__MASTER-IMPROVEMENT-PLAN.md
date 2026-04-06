# Part II Master Improvement Plan

**Modules:** 06 (Pre-training & Scaling Laws), 07 (Modern LLM Landscape), 08 (Inference Optimization)
**Sections reviewed:** 15 HTML files (6.1 through 6.7, 7.1 through 7.4, 8.1 through 8.4)
**Source reports:** 5 review phases consolidated
**Date:** 2026-03-26

---

## Executive Summary

Five review phases examined all 15 sections of Part II across planning, building, structure/self-containment, engagement/clarity/integrity, and frontier/challenge dimensions. This plan de-duplicates 160+ raw findings into 63 unique action items, organized into three priority tiers.

**Key patterns across reports:**

1. **Cross-references are entirely absent.** No section HTML file links back to prerequisite material from Part I or earlier Part II sections. This is the single most frequently flagged issue (raised in 4 of 5 reports).
2. **Module 07 has the weakest code coverage.** Section 7.1 has zero code. Sections 7.2, 7.3, and 7.4 have code but no output blocks. This was flagged independently by 3 reports.
3. **Two promised lab implementations are missing.** The speculative decoding from-scratch lab (8.3) and the quality filtering code example (6.4) are called out in the chapter plans but absent from the HTML.
4. **Several frontier topics are absent.** Synthetic data for pretraining, knowledge distillation, GGUF format, WSD learning rate schedule, and Mamba/SSMs are missing despite coverage in reference courses (Stanford CS336, CMU ANLP, Berkeley CS294).
5. **Active learning design is weak.** No "modify and observe" exercises exist. Module 07 quizzes are all recall/comprehension level.

**Tier summary:**

| Tier | Count | Description |
|------|-------|-------------|
| TIER 1: BLOCKING | 15 | Must fix before next release; missing promised content, broken self-containment, structural inconsistencies |
| TIER 2: HIGH | 25 | Significant gaps in depth, coverage, or pedagogy |
| TIER 3: MEDIUM | 23 | Enhancements that improve quality, polish, and competitiveness |

---

## TIER 1: BLOCKING (15 items)

These items represent missing promised content, broken self-containment, or structural issues that undermine the reader's ability to follow the material.

### T1-01. Add cross-references to prerequisite modules in all 15 section HTML files
- **Module:** ALL
- **Reports:** Phase 1 (#27), Phase 3 (#1), Phase 4 (#7)
- **Details:** Zero sections contain inline references to prerequisite material. Section 10.2 (KV Cache) assumes attention knowledge from Module 04 with no pointer. Section 7.3 mentions Chinchilla scaling laws but never points to Section 6.3. Section 6.6 (Distributed Training) references tensor operations with no pointer to Module 00 (PyTorch foundations).
- **Fix:** Add brief parenthetical references at first use of prerequisite concepts throughout all 15 sections. Minimum: one cross-reference per section to Part I material and one to earlier Part II material where applicable.

### T1-02. Add from-scratch speculative decoding implementation to Section 10.3
- **Module:** 08
- **Reports:** Phase 1 (#1), Phase 3 (#10), Phase 4 (#1)
- **Details:** The syllabus and chapter plan promise a lab implementing the draft-verify-resample loop. The section only shows the Hugging Face `assistant_model` API and a Medusa simulation. Students cannot understand acceptance/rejection sampling from an API call alone.
- **Fix:** Add a 30-line pedagogical implementation using two GPT-2 models (small draft, larger target) with the full accept/reject/resample loop.

### T1-03. Add mathematical proof of lossless distribution preservation to Section 10.3
- **Module:** 08
- **Reports:** Phase 1 (#2), Phase 3 (#29), Phase 4 (#2)
- **Details:** The Key Insight callout states speculative decoding is "lossless" but the probability argument is never shown. The acceptance criterion min(1, q(x)/p(x)) is given without explaining why it preserves the target distribution.
- **Fix:** Add an informal proof showing that accepted + resampled tokens together recover the target distribution.

### T1-04. Add code examples and output blocks to all Module 07 sections
- **Module:** 07
- **Reports:** Phase 2 (#1, #2, #6), Phase 4 (#5, #6)
- **Details:** Section 7.1 has zero code. Sections 7.2, 7.3, and 7.4 have code but no output blocks. Module 07 is the only module with zero code output blocks.
- **Fix:** (a) Add at least one API call example to Section 7.1. (b) Add `code-output` blocks to all existing code in 7.2, 7.3, and 7.4.

### T1-05. Add WSD (Warmup-Stable-Decay) learning rate schedule to Section 6.5
- **Module:** 06
- **Reports:** Phase 1 (#4), Phase 3 (#11), Phase 4 (#4), Phase 5 (#12)
- **Details:** WSD is now used by Llama 3, DeepSeek V3, and other models discussed in Module 07. Students will encounter WSD references in Module 07 with no prior explanation.
- **Fix:** Add a subsection between cosine decay and gradient accumulation covering the three-phase schedule, its rationale, and its advantage for continued pretraining.

### T1-06. Add quality filtering code example to Section 6.4
- **Module:** 06
- **Reports:** Phase 1 (#5), Phase 3 (#13), Phase 4 (#12)
- **Details:** The section describes heuristic, perplexity-based, and classifier-based filtering conceptually but provides no code. MinHash deduplication and domain mixing have code examples, but the most commonly needed pipeline step (filtering) does not.
- **Fix:** Add a minimal code example demonstrating heuristic quality filtering (length thresholds, language detection, symbol ratios) applied to sample documents.

### T1-07. Add worked numerical example for MLA dimensionality to Section 7.2
- **Module:** 07
- **Reports:** Phase 1 (#3), Phase 3 (#16), Phase 4 (#3)
- **Details:** Students are told MLA achieves "93% cache reduction" but the calculation path is never shown. The jump from concept to code leaves the compression claim unverifiable.
- **Fix:** Add: "Standard MHA for 128 heads with d_head=128 caches 128 x 128 = 16,384 values per layer per token. MLA compresses to a 512-dim latent, storing only 512 values: 512/16,384 = 3.1%, a 97% reduction."

### T1-08. Normalize CSS format across all 15 section files
- **Module:** ALL
- **Reports:** Phase 1 (#25), Phase 3 (#2), Phase 4 (#13)
- **Details:** Three distinct CSS formatting patterns exist: Section 6.1 (308 lines, expanded), Sections 6.2-6.7 (~91 lines, compressed), Module 07 (~282 lines, expanded variant), Module 08 (~308 lines, expanded). All render identically but maintenance requires different approaches per file.
- **Fix:** Normalize all 15 sections to a single CSS format. Consider extracting shared CSS into a separate stylesheet file.

### T1-09. Standardize footer text across all index pages and add footers to section pages
- **Module:** ALL
- **Reports:** Phase 3 (#3, #12), Phase 4 (#14)
- **Details:** Three different footer strings across index pages. Zero section pages have footers.
- **Fix:** Choose a single footer format and apply to all 3 index pages and all 15 section pages.

### T1-10. Add tensor parallelism worked matrix example to Section 6.6
- **Module:** 06
- **Reports:** Phase 1 (#7), Phase 3 (#18), Phase 4 (#8)
- **Details:** Column vs. row splitting is described verbally but no matrix multiplication shows how work distributes across devices. Students without distributed-systems background will struggle.
- **Fix:** Add a small worked example: a weight matrix split column-wise across 2 GPUs, showing local partial products and the all-reduce combination step.

### T1-11. Add MCTS scaffolding example to Section 7.3
- **Module:** 07
- **Reports:** Phase 1 (#8), Phase 3 (#6), Phase 4 (#11)
- **Details:** The section moves directly from best-of-N sampling to full MCTS for language with no intermediate example. Students without game-AI background will struggle.
- **Fix:** Add a simplified 3-4 sentence analogy (e.g., everyday decision reasoning) and a toy "MCTS for choosing the best next sentence" example before the full treatment.

### T1-12. Add synthetic data coverage to Section 6.4
- **Module:** 06
- **Reports:** Phase 5 (#2)
- **Details:** Synthetic data for pretraining is covered by Stanford CS336, CMU ANLP, and Berkeley CS294. Phi-3 and Phi-4 were trained substantially on synthetic textbook-quality data. The "data wall" discussion should address this as the leading mitigation strategy.
- **Fix:** Add a new subsection after "Data Pruning and Influence Functions" covering model-generated synthetic data, its use in Phi-3/4, and quality control strategies.

### T1-13. Add distillation coverage spanning Sections 7.3 and 8.3
- **Module:** 07, 08
- **Reports:** Phase 5 (#3)
- **Details:** Knowledge distillation appears in pretraining (teacher-student), post-training (distilling reasoning traces, as DeepSeek-R1 demonstrated), and inference (draft models). All reference courses cover this, but Part II does not.
- **Fix:** Add a "Paper Spotlight" on the DeepSeek-R1 distillation pipeline in Section 7.3, and a cross-reference noting the connection to draft models in Section 10.3.

### T1-14. Update Section 7.1 for model staleness and add evaluation framework
- **Module:** 07
- **Reports:** Phase 5 (#1), Phase 1 (#18)
- **Details:** The section references "as of early 2025" but does not mention more recent models. More importantly, it lacks a framework for evaluating new releases, making it a catalog with a short shelf life.
- **Fix:** (a) Add a "Where This Leads Next" sidebar acknowledging rapid evolution and providing a framework for evaluating new model releases. (b) Add "last updated" notes to all pricing and capability tables.

### T1-15. Add "modify and observe" active learning exercises
- **Module:** ALL
- **Reports:** Phase 2 (#8), Phase 4 (#15)
- **Details:** All exercises across all 15 sections are quiz questions with hidden answers. No prompts ask the learner to change a parameter and observe the result. This is a significant gap in active learning design.
- **Fix:** Add at least one "modify and observe" exercise per module (3 total minimum). Good candidates: 6.3 (change scaling law parameters), 8.1 (change quantization bits and compare output), 8.3 (change draft model size and observe acceptance rate).

---

## TIER 2: HIGH (25 items)

These items represent significant gaps in depth, coverage, or pedagogy that should be addressed soon after blocking issues.

### T2-01. Add GGUF format discussion to Section 10.1
- **Module:** 08
- **Reports:** Phase 1 (#9), Phase 3 (#23), Phase 4 (#16), Phase 5 (#8)
- **Details:** GGUF is the dominant format for local inference (llama.cpp, Ollama). Section 10.4 references it but Section 10.1 never explains the format or its mixed-precision k-quant strategy.

### T2-02. Add GQA memory savings worked calculation to Section 10.2
- **Module:** 08
- **Reports:** Phase 1 (#6), Phase 4 (#17)
- **Details:** The MHA vs. MQA vs. GQA table lacks concrete numbers. A Llama 3 8B example showing GB of KV cache at 4K context under MHA vs. GQA would make the architectural choice tangible.

### T2-03. Add GRPO algorithm explanation to Section 7.3
- **Module:** 07
- **Reports:** Phase 1 (#11), Phase 3 (#20), Phase 4 (#18)
- **Details:** DeepSeek-R1 is discussed as a key result, but the GRPO algorithm enabling emergent reasoning is never named or explained.

### T2-04. Add GQA/MLA cross-references between Sections 7.2 and 8.2
- **Module:** 07, 08
- **Reports:** Phase 1 (#27), Phase 3 (#4), Phase 4 (#19)
- **Details:** Both sections independently explain GQA and MLA. Neither acknowledges the other.
- **Fix:** In 7.2: "We return to GQA's memory implications in Section 10.2." In 8.2: "GQA architecture details were introduced in Section 7.2; here we focus on memory savings."

### T2-05. Upgrade Module 07 quiz questions to higher Bloom's levels
- **Module:** 07
- **Reports:** Phase 2 (#3), Phase 4 (#9)
- **Details:** All Module 07 quizzes are recall/comprehension (Bloom's levels 1-2). No application, analysis, or evaluation questions exist.
- **Fix:** Add at least one decision-making exercise per section (e.g., "Given these constraints, which model family would you recommend and why?").

### T2-06. Add cosine decay + WSD visualization SVG to Section 6.5
- **Module:** 06
- **Reports:** Phase 2 (#4), Phase 4 (#10)
- **Details:** The section covers five optimizer topics but only grokking gets a diagram. A learning rate schedule comparison visualization is strongly needed.

### T2-07. Add TTT (Test-Time Training) expanded explanation to Section 10.2
- **Module:** 08
- **Reports:** Phase 1 (#10), Phase 3 (#25), Phase 4 (#26)
- **Details:** TTT is described in one paragraph. Students may confuse it with fine-tuning. The key distinction (temporary inference-time weight updates that are discarded after generation) is not clearly stated.

### T2-08. Add PaLM, BLOOM, and Falcon entries to Section 6.1
- **Module:** 06
- **Reports:** Phase 1 (#13), Phase 4 (#24)
- **Details:** Three landmark models are absent from the survey. PaLM (Pathways, 540B scale), BLOOM (first multilingual open-science LLM), and Falcon (open training data value).

### T2-09. Add Gemma model family discussion to Section 7.2
- **Module:** 07
- **Reports:** Phase 1 (#14), Phase 4 (#28)
- **Details:** Google's Gemma 2 and Gemma 3 are competitive open-weight models mentioned on the module index page but not discussed in the section text.

### T2-10. Expand data-constrained scaling discussion in Section 6.3
- **Module:** 06
- **Reports:** Phase 1 (#12), Phase 3 (#21), Phase 4 (#21)
- **Details:** The Muennighoff et al. finding (up to 4 epochs of data repetition with minimal degradation) is mentioned in a single paragraph. Practical guidance on when to repeat vs. augment vs. synthesize is missing.

### T2-11. Add TensorRT-LLM code example to Section 10.4
- **Module:** 08
- **Reports:** Phase 1 (#16), Phase 3 (#15), Phase 4 (#27)
- **Details:** vLLM, TGI, and Ollama all have runnable examples. TensorRT-LLM, positioned as the highest-throughput option, has only a descriptive paragraph.

### T2-12. Add "data wall" Open Problem callout to Section 6.3 or 6.4
- **Module:** 06
- **Reports:** Phase 5 (#5)
- **Details:** The broader concern that high-quality text data may be exhausted by 2026-2028 deserves a dedicated callout covering Epoch AI projections, legal challenges, and the synthetic data response.

### T2-13. Add muP (maximal update parametrization) Paper Spotlight to Section 6.5
- **Module:** 06
- **Reports:** Phase 5 (#6)
- **Details:** Hyperparameter transfer across model scales is a critical practical problem. Stanford CS336 covers muP. A Paper Spotlight sidebar would add practitioner value.

### T2-14. Add reasoning model hallucination discussion to Section 7.3
- **Module:** 07
- **Reports:** Phase 1 (#23), Phase 4 (#29)
- **Details:** Reasoning traces can make hallucinations either more transparent (visible errors) or more convincing (coherent but incorrect chains). This practical consideration is absent.

### T2-15. Add KV cache quantization subsection to Section 10.2
- **Module:** 08
- **Reports:** Phase 5 (#13)
- **Details:** KV cache quantization (INT4/INT8 for cached keys/values) is standard in production serving. vLLM supports it natively. This is distinct from weight quantization and extends Section 10.1.

### T2-16. Add Mamba/SSM "Where This Leads Next" sidebar to Section 6.2 or 7.2
- **Module:** 06 or 07
- **Reports:** Phase 5 (#11)
- **Details:** Mamba, RWKV, and hybrid architectures (Jamba) are covered by Berkeley CS294 and Stanford CS336. A forward-looking callout positioning these as alternatives to attention would strengthen competitiveness.

### T2-17. Add model licensing details to Section 7.2
- **Module:** 07
- **Reports:** Phase 1 (#15), Phase 4 (#32)
- **Details:** The section distinguishes open-source from open-weight but does not explain Llama's 700M MAU restriction, Apache 2.0, or other practical licensing differences critical for production.

### T2-18. Add GPTQ Hessian explanation to Section 10.1
- **Module:** 08
- **Reports:** Phase 1 (#17)
- **Details:** GPTQ is described as "Hessian-based optimal rounding" but the Hessian's role (second-order sensitivity of loss to weight perturbations) is not explained.

### T2-19. Add lab exercises to Sections 7.1 and 7.4
- **Module:** 07
- **Reports:** Phase 1 (#20), Phase 3 (#19, #27)
- **Details:** Sections 7.2 and 7.3 have labs; 7.1 and 7.4 do not. The chapter plan recommends an API comparison lab (7.1) and a multilingual evaluation lab (7.4).

### T2-20. Add second SVG diagram to Section 6.7 (ICL theory)
- **Module:** 06
- **Reports:** Phase 2 (#9), Phase 4 (#25)
- **Details:** The section has four distinct theoretical frameworks but only one diagram. The task vector concept and implicit gradient descent view both deserve visual support.

### T2-21. Expand Section 6.6 with sequence parallelism and context parallelism
- **Module:** 06
- **Reports:** Phase 1 (#19), Phase 3 (#30), Phase 4 (#35), Phase 5 (#10)
- **Details:** With 128K+ context models now standard, ring attention and sequence parallelism are increasingly relevant. The chapter plan flags this gap.

### T2-22. Add self-speculative decoding mention to Section 10.3
- **Module:** 08
- **Reports:** Phase 5 (#17)
- **Details:** LayerSkip, SPEED, and similar "draft-free" approaches eliminate the need for a separate draft model. These are notable extensions of the speculative decoding concept.

### T2-23. Add SGLang expanded coverage and verify LMDeploy in Section 10.4
- **Module:** 08
- **Reports:** Phase 5 (#9)
- **Details:** SGLang has emerged as a strong vLLM competitor in 2025, particularly for structured output. RadixAttention deserves at least a paragraph.

### T2-24. Add acceptance/rejection sampling probability distribution SVG to Section 10.3
- **Module:** 08
- **Reports:** Phase 2 (#7)
- **Details:** A visual showing overlapping draft vs. target distributions with the min(1, p/q) acceptance criterion would make the math intuitive.

### T2-25. Add DeepSeek V3 FP8 training and Qwen 2.5 coverage to Section 7.2
- **Module:** 07
- **Reports:** Phase 5 (#4)
- **Details:** DeepSeek V3's FP8 training connects directly to Module 08's quantization discussion. Qwen 2.5's multilingual performance connects to Section 7.4.

---

## TIER 3: MEDIUM (23 items)

These items improve quality, polish, and competitiveness with reference courses.

### T3-01. Add quantization analogy (color depth reduction) to Section 10.1
- **Module:** 08
- **Reports:** Phase 2 (#10), Phase 4 (#37)

### T3-02. Add parallelism analogy (assembly line vs. task division) to Section 6.6
- **Module:** 06
- **Reports:** Phase 2 (#5), Phase 4 (#40)

### T3-03. Add MinHash LSH analogy (Shazam fingerprinting) to Section 6.4
- **Module:** 06
- **Reports:** Phase 2 (#11)

### T3-04. Connect grokking to double descent and regularization in Section 6.5
- **Module:** 06
- **Reports:** Phase 1 (#22), Phase 3 (#24), Phase 4 (#23)

### T3-05. Add tokenization efficiency bar chart SVG to Section 7.4
- **Module:** 07
- **Reports:** Phase 2 (#13), Phase 4 (#39)

### T3-06. Add "last updated" notes to Section 7.1 pricing tables
- **Module:** 07
- **Reports:** Phase 1 (#28), Phase 3 (#14), Phase 4 (#22)

### T3-07. Standardize quiz question counts across modules
- **Module:** ALL
- **Reports:** Phase 3 (#9, #22), Phase 4 (#36)

### T3-08. Standardize Module 06 index page order (prereqs before sections)
- **Module:** 06
- **Reports:** Phase 3 (#17), Phase 4 (#31)

### T3-09. Refine Module 08 prerequisite to be section-specific
- **Module:** 08
- **Reports:** Phase 3 (#28)

### T3-10. Add FLOPs vs. FLOPS inline note to Section 6.3
- **Module:** 06
- **Reports:** Phase 3 (#26), Phase 4 (#30)

### T3-11. Improve Section 10.2 opening hook
- **Module:** 08
- **Reports:** Phase 4 (#34)
- **Fix:** Start with: "You quantized your model to 4-bit, but inference is still slow. Why? The KV cache is now the bottleneck."

### T3-12. Add ORM vs. PRM worked example to Section 7.3
- **Module:** 07
- **Reports:** Phase 2 (#20)

### T3-13. Promote R1-Zero emergent reasoning to Key Insight callout in Section 7.3
- **Module:** 07
- **Reports:** Phase 4 (missed aha-moment #1 for Module 07)

### T3-14. Promote MoE economics to Key Insight callout in Section 7.2
- **Module:** 07
- **Reports:** Phase 4 (missed aha-moment #2 for Module 07)

### T3-15. Add "optimizer is bigger than model" aha-moment callout to Section 6.5
- **Module:** 06
- **Reports:** Phase 4 (missed aha-moment #1 for Module 06)

### T3-16. Add "97% of internet data is filtered out" aha-moment callout to Section 6.4
- **Module:** 06
- **Reports:** Phase 4 (missed aha-moment #2 for Module 06)

### T3-17. Elevate "tokenization tax" to Key Insight callout in Section 7.4
- **Module:** 07
- **Reports:** Phase 4 (missed aha-moment #3 for Module 07)

### T3-18. Add Section 7.3 to 7.4 transition paragraph
- **Module:** 07
- **Reports:** Phase 1 (module flow note)

### T3-19. Add forward pointer from Section 6.3 to inference-time scaling in 7.3
- **Module:** 06
- **Reports:** Phase 5 (#18)

### T3-20. Add Paper Spotlight on FineWeb to Section 6.4
- **Module:** 06
- **Reports:** Phase 5 (#16)

### T3-21. Add Open Problem on ICL failure modes to Section 6.7
- **Module:** 06
- **Reports:** Phase 5 (#15)

### T3-22. Add MTP DeepSeek V3 validation reference to Section 6.2
- **Module:** 06
- **Reports:** Phase 5 (#23)

### T3-23. Add cost optimization and auto-scaling discussion to Section 10.4
- **Module:** 08
- **Reports:** Phase 1 (#29), Phase 4 (#38)

---

## Counts by Tier and Module

| Module | TIER 1 (Blocking) | TIER 2 (High) | TIER 3 (Medium) | Total |
|--------|-------------------|---------------|-----------------|-------|
| Module 06 | 5 (T1-05, T1-06, T1-10, T1-12, T1-15*) | 8 (T2-08, T2-10, T2-12, T2-13, T2-16*, T2-20, T2-21, T2-06) | 9 (T3-02, T3-03, T3-04, T3-08, T3-10, T3-15, T3-16, T3-19, T3-20, T3-21, T3-22) | 22 |
| Module 07 | 5 (T1-04, T1-07, T1-11, T1-13*, T1-14) | 8 (T2-03, T2-04*, T2-05, T2-09, T2-14, T2-17, T2-19, T2-25) | 5 (T3-05, T3-06, T3-12, T3-13, T3-14, T3-17, T3-18) | 18 |
| Module 08 | 3 (T1-02, T1-03, T1-13*) | 9 (T2-01, T2-02, T2-04*, T2-07, T2-11, T2-15, T2-22, T2-23, T2-24) | 3 (T3-01, T3-11, T3-23) | 15 |
| Cross-module | 4 (T1-01, T1-08, T1-09, T1-15*) | 1 (T2-16*) | 3 (T3-07, T3-09, T3-10) | 8 |
| **TOTAL** | **15** | **25** | **23** | **63** |

*Items marked with * span multiple modules.

---

## Conflict Resolutions

1. **Quiz question count:** Phase 3 reports Module 06 has 5 questions per section while Phase 2 reports 4. Phase 4 reports varying counts. Resolution: audit actual HTML and standardize to 5 per section across all modules.

2. **Section 7.3 length:** Phase 1 and Phase 3 both suggest splitting or trimming. Phase 4 rates the section's content as strong. Resolution: do NOT split; instead trim the MCTS subsection to a high-level overview with a pointer to the full treatment in an appendix or further reading section.

3. **PRMs/ORMs:** Phase 5 (#14) says PRM/ORM coverage is missing from Section 7.3. Phase 4 and Phase 2 reference existing PRM/ORM diagrams and discussion. Resolution: the content exists but needs a worked example (Tier 3, T3-12). Phase 5 may have missed it due to the section's density. No new section needed.

4. **CSS extraction:** Phase 3 recommends a separate shared stylesheet. Phase 4 recommends normalizing in-file CSS. Resolution: normalize first (T1-08), and consider extraction as a follow-up maintenance improvement. Extraction changes the build/serving approach and should be evaluated separately.

5. **Section 7.1 code:** Phase 2 (#1, #6) and Phase 4 (#5) agree this section needs code. Phase 5 (#21) suggests adding a decision framework rather than code. Resolution: do both. Add an API call example AND a decision matrix. These complement each other.
