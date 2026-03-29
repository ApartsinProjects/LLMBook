# Module 08: Inference Optimization & Efficient Serving
## 36-Agent Deep Review Report

**Date:** 2026-03-26
**Files reviewed:** index.html, section-10.1.html, section-10.2.html, section-10.3.html, section-10.4.html, chapter-plan.md

---

## Agent 00: Chapter Lead

**Overall assessment: STRONG**

The module is well-structured with a clear narrative arc: compress the model (8.1), optimize the memory (8.2), parallelize the computation (8.3), build the serving system (8.4). Each section builds on the previous. The chapter plan is thorough, with clear scope, learning objectives, prerequisites, and cross-references. Word count targets are reasonable (~17,700 words total). The four sections have consistent structure: Big Picture callout, prerequisite callout, explanatory text, code examples, diagrams, quiz, and key takeaways.

**No action items.**

---

## Agent 01: Curriculum Alignment

**Overall alignment: STRONG**

### Coverage Gaps
- NONE: All 8 learning objectives from the chapter plan are covered with appropriate depth.

### Scope Creep
- NONE: Content stays within the defined scope.

### Depth Calibration
- Section 10.1 (Intermediate): Appropriate. Math is accessible; code is practical.
- Section 10.2 (Advanced): Appropriate. KV cache formula, PagedAttention, GQA are well-covered.
- Section 10.3 (Advanced): Appropriate. The informal proof of correctness is a good addition.
- Section 10.4 (Intermediate): Appropriate. Practical survey with benchmarking.

### Prerequisite Alignment
- All sections have explicit prerequisite callouts referencing Module 04, 05, and 07.
- Section 10.1 references Section 0.2 (floating-point representation).

### Sequencing
- Forward reference from 8.1 to KV cache quantization in 8.2: present in chapter plan's areas for improvement but already addressed in Section 10.2, subsection 7.1.
- Section 10.3 note on knowledge distillation correctly references Section 7.3 (not a later module).

**No action items.**

---

## Agent 02: Deep Explanation

**Overall depth: STRONG**

### Strengths
1. GPTQ's Hessian explanation includes the update rule and intuitive explanation of error compensation.
2. The informal proof of speculative decoding correctness in Section 10.3 is excellent.
3. NF4's quantile-based design is explained with information-theoretic justification.
4. PagedAttention has a strong OS virtual memory analogy.

### Issues

1. **[TIER 2] Section 10.1, GPTQ subsection:** The chapter plan flags that the Hessian approximation (H = X^T X) could use a brief note for students without optimization background. The text says "the Hessian of the layer's squared error with respect to the weights, which equals X^T X" but does not explain why. Add one sentence: the Hessian captures how sensitive the output is to each weight, so weights with large Hessian values are "fragile" and should be quantized more carefully.

2. **[TIER 3] Section 10.2, TTT subsection:** The distinction between TTT and fine-tuning could be sharper. The text says "Unlike fine-tuning, which permanently updates model weights for reuse across many requests, TTT creates temporary weight updates for a single inference request." This is good but could benefit from an explicit contrast table or callout.

3. **[TIER 3] Section 10.4, TensorRT-LLM:** The section explains compilation and optimization but could briefly note what "kernel fusion" means for readers unfamiliar with GPU programming.

---

## Agent 03: Teaching Flow

**Overall flow: SMOOTH**

### Strengths
- Each section opens with a motivating Big Picture callout.
- Section 10.2 opens with "You quantized your model to 4-bit and slashed its memory footprint by 4x. But inference is still slow..." creating a natural bridge from 8.1.
- Section 10.3 bridges from 8.2's memory-bandwidth analysis.
- Section 10.4 explicitly ties together all three previous sections.

### Issues

1. **[TIER 2] Section 10.1 to 8.2 transition:** The end of Section 10.1 (takeaways) does not include a forward bridge to Section 10.2. The nav link exists but there is no "Now that we have compressed the weights, the next bottleneck is..." sentence.

2. **[TIER 3] Section 10.3 to 8.4 transition:** Similarly, the takeaways at the end of 8.3 do not preview 8.4.

---

## Agent 04: Student Advocate

**Clarity: MOSTLY CLEAR**
**Microlearning: WELL-STRUCTURED**

### Issues

1. **[TIER 2] Section 10.1, GPTQ update rule (line ~507-511):** The Hessian inverse notation [H^{-1}]_{jj} and [H^{-1}]_{jk} may be opaque to students without linear algebra beyond basics. Add a plain-language gloss after the formula.

2. **[TIER 3] Section 10.3, expected speedup formula:** The formula E[tokens] = (1 - alpha^{gamma+1})/(1 - alpha) appears without derivation. A one-sentence note on where it comes from (geometric series) would help.

3. **[TIER 3] Section 10.4:** The section covers 8 frameworks. Students may feel overwhelmed. The comparison table helps, but a decision flowchart ("If you need X, use Y") would be even better.

---

## Agent 05: Cognitive Load

**Overall: MANAGEABLE**

### Strengths
- Each section has multiple visual breaks (diagrams, code, tables, callouts).
- Quiz questions at the end of each section serve as checkpoints.
- Key Takeaways boxes consolidate learning.

### Issues

1. **[TIER 2] Section 10.4, frameworks survey (sections 2-8):** Seven frameworks in sequence (vLLM, SGLang, TGI, TensorRT-LLM, LMDeploy, Ollama/llama.cpp, Triton) is a lot. The comparison table at the end helps, but moving it earlier (before the individual descriptions) would let students build a mental framework first.

2. **[TIER 3] Section 10.1, data types table + NF4 + GPTQ + AWQ:** Sections 3-7 introduce many methods in sequence. The callouts and code examples provide relief, but a brief "roadmap" sentence at the start of Section 4 ("We will now examine three major PTQ algorithms...") would help.

---

## Agent 06: Example & Analogy

**Overall concreteness: VIVID**

### Strengths
- Section 10.1 opens with an image quantization analogy (24-bit to 8-bit color).
- Section 10.2 uses the OS virtual memory analogy for PagedAttention.
- Section 10.3 uses the "junior writer / senior editor" analogy.
- Section 10.4 has the "10% ML, 90% infrastructure" framing.
- The epigraphs are witty and set the right tone.

### Issues

1. **[TIER 3] Section 10.2, H2O eviction policy:** Mentioned briefly but no concrete example of which tokens would be evicted. A one-sentence example would help.

---

## Agent 07: Exercise Designer

**Overall: STRONG**

### Assessment
- Each section has a 5-question quiz with expandable answers.
- Section 10.1 has a "Modify and Observe" try-it exercise (GGUF comparison).
- Section 10.3 has a "Modify and Observe" exercise (changing gamma).
- Section 10.4 references a lab exercise (deploy vLLM and TGI side by side).

### Issues

1. **[TIER 3] Section 10.2:** No "Try It" exercise. A hands-on exercise to run the KV cache calculator with different model configs would reinforce the concept. The code is already there; a callout encouraging experimentation is all that is needed.

2. **[TIER 3] Section 10.1:** Quiz question 4 asks a calculation, but there is no standalone calculation exercise in the section body. The benchmark code (Example 4) is observational, not hands-on.

---

## Agent 08: Code Pedagogy

**Overall: EXCELLENT**

### Strengths
- All code blocks have clear comments and shown output.
- Progressive complexity: Section 10.1 goes from simple BitsAndBytesConfig to GPTQ to AWQ to benchmarking.
- Section 10.3 includes both a from-scratch implementation and the library API approach.
- Section 10.4 shows async benchmarking with realistic metrics.

### Issues

1. **[TIER 2] Section 10.3, Example 3 (from-scratch speculative decoding):** The code labels say "Example 3" but it should be labeled as the pedagogical from-scratch implementation, distinct from the HF library example (which is also labeled Example 3). Renumber to avoid confusion.

2. **[TIER 3] Section 10.1, Example 4 (benchmarking):** The `measure_perplexity` function has a subtle issue: `target_ids[:, :-1] = -100` masks all but the last token, which gives per-step loss, not true sliding-window perplexity. This is pedagogically fine for a rough comparison but should have a comment noting it is a simplified measurement.

---

## Agent 09: Visual Learning

**Overall: RICH**

### Visual Inventory
- Section 10.1: 2 SVG diagrams (quantization granularity, GPTQ vs AWQ)
- Section 10.2: 2 SVG diagrams (PagedAttention, continuous batching)
- Section 10.3: 2 SVG diagrams (speculative decoding workflow, EAGLE tree)
- Section 10.4: 2 SVG diagrams (serving stack, latency anatomy)
- Total: 8 SVG diagrams across 4 sections

### Assessment
- All diagrams have descriptive captions.
- Consistent color palette (blue, green, purple, orange from the book's CSS variables).
- Labels are legible and well-positioned.

### Issues

1. **[TIER 3] Section 10.2, MHA/MQA/GQA comparison:** The table is informative, but a visual diagram showing the head-sharing patterns would make the architectural differences more immediately clear.

---

## Agent 10: Misconception Analyst

**Overall risk: LOW**

### High-Risk Items

1. **[TIER 2] Section 10.3:** Students may think speculative decoding always speeds things up. The "When Speculative Decoding Hurts" warning is present but could be more prominent. Consider making it an explicit misconception callout rather than a warning box.

2. **[TIER 2] Section 10.1:** Students may confuse weight quantization with activation quantization. The text distinguishes them ("sometimes activations") but the distinction deserves a clearer callout, since the code examples all show weight-only quantization.

3. **[TIER 3] Section 10.2:** Students may confuse TTT with fine-tuning. The text addresses this but only in one paragraph. A "Common Misconception" callout would make the distinction stickier.

---

## Agent 11: Fact Integrity

**Overall reliability: HIGH**

### Issues

1. **[TIER 1] Section 10.1, line ~502:** States "GPTQ (Frantar et al., 2023)" but on line ~631 says "(Frantar et al., 2022)." The paper was published in 2022 (ICLR 2023 acceptance, but arXiv 2022). Standardize to 2022 for the arXiv date or 2023 for the publication venue, but be consistent.

2. **[TIER 2] Section 10.3:** States "H100 GPU with 3.35 TB/s memory bandwidth and 989 TFLOPS of FP16 compute." The H100 SXM5 has 3.35 TB/s HBM3 bandwidth and 989.4 TFLOPS of FP16 with sparsity (494.7 TFLOPS dense). The text should clarify "dense FP16" vs. "sparse FP16." The 989 figure is the sparsity-enabled number.

3. **[TIER 2] Section 10.4:** States TensorRT-LLM provides "30-50% higher throughput than vLLM at high concurrency." This was accurate in early 2025 benchmarks but the gap has narrowed as vLLM adopted more kernel optimizations. Add "as of early 2025" qualifier.

4. **[TIER 3] Section 10.2:** States DeepSeek Sparse Attention was "Introduced in DeepSeek V3.2." Verify this version number; DSA was described in the DeepSeek V3 technical report context. The term "V3.2" may not be an official release name.

---

## Agent 12: Terminology Keeper

**Overall: CONSISTENT (minor issues)**

### Issues

1. **[TIER 1] Section 10.3:** Uses both "M_q" for draft model and "M_p" for target model in the acceptance formula, but the text says "q(x) be the draft model's probability" and "p(x) be the target model's probability." This is reversed from the subscript notation (M_q for draft, M_p for target, but q = draft prob and p = target prob). This is standard in the literature but potentially confusing. Add a clarifying note.

2. **[TIER 2]** The chapter plan says to use "time to first token (TTFT)" on first mention. Section 10.4 introduces it correctly as "Time to First Token (TTFT)" but also uses "TPOT" which is expanded correctly. Good.

3. **[TIER 3]** Section 10.2 uses "key/value cache" in the index.html overview but "KV cache" consistently in the section itself. The chapter plan says to use "KV cache" with "key-value cache" only on first mention. Index.html should standardize.

---

## Agent 13: Cross-Reference

**Overall: WELL-CONNECTED**

### Strengths
- Section 10.1 references Section 0.2 and Module 04.
- Section 10.2 references Section 7.2 (GQA), Section 10.1 (quantization).
- Section 10.3 references Section 10.2, Section 5.1, Section 5.2, Section 7.3.
- Section 10.4 references all three previous sections and Section 5.1.

### Issues

1. **[TIER 2] Section 10.1:** Does not mention that quantization applies to KV caches too (not just weights). The chapter plan specifically flags this as a needed forward reference. Add a brief note: "We will see in Section 10.2 that quantization can also be applied to the KV cache, further reducing memory."

2. **[TIER 3] Section 10.2:** The GQA worked example correctly notes "GQA's architectural design and its role in models like Llama 3 were introduced in Section 7.2; here we focus on its memory optimization implications." Excellent.

---

## Agent 14: Narrative Continuity

**Overall: COHESIVE**

### Strengths
- The optimization cascade narrative (weight problem, memory wall, sequential bottleneck, putting it together) is clearly executed.
- Each section's opening references the previous section's conclusion.
- Epigraphs add personality and set tone consistently.

### Issues

1. **[TIER 2] Section 10.1 ending:** The takeaways list quantization methods but do not bridge to 8.2. Add a closing transition sentence.

2. **[TIER 2] Section 10.3 ending:** Similarly needs a bridge to 8.4.

---

## Agent 15: Style & Voice

**Overall: UNIFIED**

### Strengths
- Consistent authoritative-but-approachable tone throughout.
- Good use of "we" for shared exploration.
- Humor in epigraphs is well-calibrated.
- No condescending language detected ("simply," "obviously," etc.).

### Issues

1. **[TIER 1] Em dash in CSS:** All four section files contain `.epigraph cite::before { content: "\2014\00a0"; }` which renders an em dash before epigraph citations. This is a CSS rendering choice, not text content. However, per the strict rule against em dashes, consider replacing with a different visual separator in the CSS (e.g., a long hyphen entity or an en dash `\2013`).

2. **[TIER 3] Section 10.4:** Some sentences are long (35+ words), particularly in the TensorRT-LLM and Triton sections. Consider splitting for readability.

---

## Agent 16: Engagement Designer

**Overall: ENGAGING**

### Strengths
- Epigraphs are witty and memorable.
- "Try It" callouts in 8.1 and 8.3.
- Real benchmark numbers create concrete stakes.
- The from-scratch speculative decoding implementation is a highlight.

### Issues

1. **[TIER 3] Section 10.2:** No "Try It" or "Modify and Observe" callout. The section is somewhat denser than others in engagement elements.

2. **[TIER 3] Section 10.4:** The framework survey could benefit from a "Which framework should I pick?" decision-making exercise.

---

## Agent 17: Senior Editor

### Chapter Scorecard

| Dimension | Score (1-5) | Notes |
|-----------|-------------|-------|
| Wording | 4.5 | Clear, precise, professional |
| Structure | 4.5 | Consistent across sections |
| Figures | 4 | 8 SVGs, well-designed, could add 1-2 more |
| Exercises | 4 | Strong quizzes, could add more hands-on |
| Pedagogy | 5 | Excellent progression, analogies, proofs |
| Clarity | 4.5 | Minor notation issues |
| Market Quality | 4.5 | Modern, practical, competitive |
| **Overall** | **4.5** | |

### Publication Readiness: NEEDS MINOR REVISION

Top 3 improvements:
1. Fix GPTQ date inconsistency (TIER 1)
2. Add transition bridges at section endings (TIER 2)
3. Add forward reference from 8.1 to KV cache quantization (TIER 2)

---

## Agent 18: Research Scientist

**Overall depth: RICH**

### Strengths
- TTT and DeepSeek Sparse Attention coverage in 8.2 is forward-looking.
- EAGLE and Medusa treatment in 8.3 goes beyond surface level.
- The informal proof of speculative decoding correctness adds real rigor.

### Issues

1. **[TIER 3] Section 10.1:** Could mention the emerging field of 1-bit quantization (BitNet, 1.58-bit models). A brief "Research Frontier" callout would position this as a cutting-edge direction.

2. **[TIER 3] Section 10.3:** Could mention SpecInfer (Miao et al., 2024) as another tree-based approach, distinguishing it from EAGLE.

---

## Agent 19: Structural Architect

**Overall: WELL-STRUCTURED**

The four-section structure is logical and well-sequenced. No sections need to be moved, merged, or split. Internal consistency across sections is high (all follow: header, epigraph, Big Picture, prereqs, content, quiz, takeaways, nav).

### Issues

1. **[TIER 3] Section 10.4:** At ~5000 words covering 8 frameworks, this is the longest section. Consider whether LMDeploy and Triton could be condensed into a single "Other Frameworks" subsection rather than full subsections, since they receive less coverage than the top-tier frameworks.

---

## Agent 20: Content Update Scout

**Overall: MOSTLY CURRENT**

### Issues

1. **[TIER 2] Section 10.4:** Missing mention of MLX (Apple's ML framework for Apple Silicon). The chapter plan flags this. Worth a brief paragraph in or near the Ollama/llama.cpp section.

2. **[TIER 3] Section 10.1:** Could mention ExLlamaV2 as another popular quantization/inference tool, especially for GPTQ models.

3. **[TIER 3] Section 10.4:** Missing mention of cost optimization strategies (spot instances, auto-scaling). The chapter plan flags this as a gap. A brief "Note" callout would be appropriate.

---

## Agent 21: Self-Containment Verifier

**Overall: SELF-CONTAINED**

All prerequisite concepts are either explained locally or cross-referenced to earlier modules. The prerequisite callouts in each section are explicit and helpful.

### Issues

1. **[TIER 3] Section 10.3:** The acceptance/rejection sampling scheme assumes familiarity with uniform random variables and probability distributions. The prereq callout references Section 5.2 (sampling), which should cover this. Adequate.

---

## Agent 22: Title & Hook Architect

**Overall: COMPELLING THROUGHOUT**

### Assessment
- Chapter title "Inference Optimization & Efficient Serving" is clear and specific.
- Section titles are descriptive: "Model Quantization," "KV Cache & Memory Optimization," "Speculative Decoding," "Serving Infrastructure."
- All section openings use Big Picture callouts that immediately establish stakes.
- Epigraphs add personality.

### Issues

1. **[TIER 3]** Section titles could be slightly more action-oriented. "Model Quantization" could be "Compressing Model Weights with Quantization." However, the current titles are clear and the subtitles provide the action framing.

---

## Agent 23: Project Catalyst

**Overall: ADEQUATE**

### Strengths
- Section 10.1 has a GGUF comparison exercise.
- Section 10.3 has a from-scratch implementation.
- Section 10.4 references a lab exercise (deploy vLLM and TGI side by side).

### Issues

1. **[TIER 3] Section 10.2:** No project or build moment. Could add: "You Could Build This: A KV cache memory estimator that takes model architecture parameters and outputs memory requirements for different batch sizes and context lengths. Extend the code from Example 1 into a command-line tool."

---

## Agent 24: Aha-Moment Engineer

**Overall: RICH IN AHA MOMENTS**

### Existing Strong Moments
1. Section 10.1: NF4 quantile values listed explicitly; the "information-theoretically optimal" insight.
2. Section 10.2: The worked example showing MHA (68.7 GB) vs. GQA (17.2 GB) for a batch of 32.
3. Section 10.3: `torch.equal(out_standard, out_speculative)` returning True; the "Outputs match" moment.
4. Section 10.4: The benchmarking table showing throughput scaling from 48 to 894 tok/s with increasing concurrency.

### Issues

1. **[TIER 3] Section 10.1:** The FP16 vs. INT4 memory comparison (140 GB to 35 GB) is stated but could be made more dramatic with a "That means it goes from needing two A100 GPUs to fitting on a single consumer RTX 4090" framing.

---

## Agent 25: First-Page Converter

**Overall: CONVERTS**

All section openings follow the effective pattern: epigraph, Big Picture callout with concrete stakes, prerequisite callout. The Big Picture callouts in each section establish urgency and frame the problem clearly.

**No action items.**

---

## Agent 26: Visual Identity Director

**Overall: STRONG VISUAL IDENTITY**

### Strengths
- Consistent color palette across all sections (primary, accent, highlight).
- Consistent callout system (big-picture=purple, key-insight=green, note=blue, warning=yellow).
- Consistent code block styling (dark background, Consolas font).
- Consistent chapter navigation (top and bottom).
- SVG diagrams use the same font family (Segoe UI) and color scheme.

### Issues

1. **[TIER 3]** The `try-it` callout class styling is defined but used only in sections 8.1 and 8.3. Sections 8.2 and 8.4 could benefit from this callout type for consistency.

---

## Agent 27: Research Frontier Mapper

**Overall: FRONTIERS WELL-MAPPED**

### Strengths
- Section 10.2 has explicit "Research Frontiers" subsection covering TTT and DSA.
- Section 10.3 covers EAGLE-2, Medusa, LayerSkip, SPEED.
- Section 10.4 mentions emerging frameworks.

### Issues

1. **[TIER 3] Section 10.1:** No research frontier section. Could add a brief "Research Frontier" callout on 1-bit models (BitNet b1.58), sub-4-bit quantization, and mixed-precision quantization at the layer level.

---

## Agent 28: Demo & Simulation Designer

**Overall: NEEDS SLIGHTLY MORE INTERACTIVITY**

### Strengths
- Section 10.1: GGUF comparison try-it exercise.
- Section 10.3: gamma modification try-it exercise.
- Section 10.4: Comprehensive benchmarking script.

### Issues

1. **[TIER 3] Section 10.2:** No interactive demo. The KV cache calculator (Example 1) is already a good starting point; add a "Try It" callout encouraging students to modify the parameters.

---

## Agent 29: Memorability Designer

**Overall: HIGHLY MEMORABLE**

### Existing Strong Anchors
- "Quantization is like reducing color depth of an image" (8.1)
- "KV cache is the model's short-term memory" (8.2 epigraph)
- "Junior writer, senior editor" analogy (8.3)
- "10% ML, 90% infrastructure" (8.4 epigraph)
- "Lossless acceleration" phrase for speculative decoding

### Issues

1. **[TIER 3]** Consider adding a mnemonic for the four pillars of inference optimization: Quantize, Cache, Speculate, Serve.

---

## Agent 30: Skeptical Reader

**Overall: DISTINCTIVE AND MEMORABLE**

### What Makes This Chapter Stand Out
1. From-scratch speculative decoding implementation is rare in textbooks.
2. The informal proof of correctness is a differentiator.
3. Practical benchmarking code with realistic async patterns.
4. Coverage of TTT and DSA puts this ahead of most current textbooks.
5. GGUF format coverage (missing from many academic treatments).

### Issues

1. **[TIER 3] Section 10.4 framework survey:** The individual framework descriptions (vLLM, SGLang, TGI, etc.) risk reading like product documentation rather than textbook content. The comparison table helps, but the individual sections could include more comparative analysis within each description.

---

## Agent 31: Plain-Language Rewriter

**Overall: MOSTLY CLEAR**

### Issues

1. **[TIER 2] Section 10.1, line ~631:** "GPTQ processes weights one column at a time, using the Hessian information to (1) round each weight to the nearest quantized value, and (2) distribute the rounding error across not-yet-quantized columns to minimize the total loss increase." This 40-word sentence packs two ideas. Split.

2. **[TIER 3] Section 10.4, Triton paragraph:** "NVIDIA Triton Inference Server is a production-grade model serving platform designed for multi-model, multi-framework deployments" could be simplified.

---

## Agent 32: Sentence Flow

**Overall: MOSTLY SMOOTH**

The prose generally flows well. Sentence variety is good. The main concern is a few long sentences in technical descriptions.

### Issues

1. **[TIER 2] Section 10.2, TTT paragraph (line ~781):** A single sentence runs from "Instead of storing..." to "...next-token-prediction loss over the recent context." This is ~50 words. Split for readability.

2. **[TIER 3]** Some paragraphs in 8.4 framework descriptions have 4-5 sentences of similar length. Vary rhythm.

---

## Agent 33: Jargon Gatekeeper

**Overall: ACCESSIBLE**

### Strengths
- Key terms (quantization, KV cache, PagedAttention, TTFT, TPOT) are all defined on first use.
- Acronyms are expanded on first use.
- The terminology standards from the chapter plan are consistently followed.

### Issues

1. **[TIER 2] Section 10.1:** "Arithmetic intensity" is used in the first paragraph ("arithmetic intensity analysis") without definition. Add a brief inline gloss: "arithmetic intensity (the ratio of compute operations to memory accesses)."

2. **[TIER 3] Section 10.2:** "FlashAttention" is mentioned in the continuous batching section context without explanation. It is a well-known term but could use a one-phrase gloss for completeness.

---

## Agent 34: Micro-Chunking Editor

**Overall: WELL-CHUNKED**

### Strengths
- Sections use h2, h3, h4 hierarchy effectively.
- Code blocks and diagrams break up prose regularly.
- Callout boxes provide visual and cognitive breaks.

### Issues

1. **[TIER 3] Section 10.4, Benchmarking Methodology (section 10):** The latency/throughput metrics are presented in two h4-headed lists. Good structure. The following benchmarking code example is long (~80 lines). A brief signpost sentence before it would help.

---

## Agent 35: Reader Fatigue Detector

**Overall: MOSTLY ENGAGING**

### Energy Map
- Section 10.1: HIGH (good hook, varied content types, practical examples)
- Section 10.2: MEDIUM-HIGH (strong opening, good diagrams, but the compression techniques subsection is slightly denser)
- Section 10.3: HIGH (the proof, the from-scratch implementation, and the "Outputs match" moment maintain energy)
- Section 10.4: MEDIUM (framework survey can feel like a catalog; the benchmarking section restores engagement)

### Issues

1. **[TIER 2] Section 10.4, frameworks 2-8:** The sequential framework descriptions (SGLang, TGI, TensorRT-LLM, LMDeploy, Ollama, Triton) follow a repetitive pattern: description, features list, optional code. Moving the comparison table earlier would give readers a mental map before diving into details.

2. **[TIER 3] Section 10.2, KV cache compression (section 7):** Three compression techniques (quantization, H2O, sliding window, StreamingLLM) are listed quickly. The H2O and StreamingLLM descriptions could benefit from an additional sentence each.

---

## Consolidated Fix List

### TIER 1 (Must Fix)
1. **[8.1] GPTQ date inconsistency:** Standardize "Frantar et al., 2022" vs "2023" across the section.
2. **[8.3] Speculative decoding model notation clarification:** Add a note clarifying M_q/M_p subscript notation vs. q(x)/p(x) probability notation.
3. **[All sections] Epigraph CSS em dash:** Replace `\2014` with `\2013` (en dash) in epigraph cite::before CSS across all four section files.

### TIER 2 (Should Fix)
4. **[8.1] Add forward reference to KV cache quantization** at end of Section 10.1.
5. **[8.1] Add transition bridge** at end of 8.1 takeaways to preview 8.2.
6. **[8.3] Add transition bridge** at end of 8.3 takeaways to preview 8.4.
7. **[8.1] GPTQ Hessian gloss:** Add one sentence explaining why H captures weight sensitivity.
8. **[8.1] Arithmetic intensity definition:** Add inline gloss on first use.
9. **[8.3] H100 FP16 TFLOPS clarification:** Note whether 989 TFLOPS is dense or sparse.
10. **[8.4] TensorRT-LLM throughput claim:** Add time qualifier ("as of early 2025").
11. **[8.1] Split long GPTQ sentence** (line ~631).
12. **[8.2] Split long TTT sentence** (line ~781).
13. **[8.4] Move comparison table earlier** in the section, before individual framework descriptions.
14. **[8.4] Add MLX mention** near Ollama/llama.cpp section.
15. **[8.1] Weight vs. activation quantization clarification callout.**
16. **[8.2] Add "Try It" callout** for KV cache calculator.

### TIER 3 (Reasonable Improvements)
17. **[8.2] TTT vs fine-tuning misconception callout.**
18. **[8.2] H2O and StreamingLLM one-sentence expansions.**
19. **[8.3] Expected speedup formula derivation note.**
20. **[8.4] Kernel fusion brief definition.**
21. **[8.4] Add cost optimization note callout.**
22. **[8.2] DeepSeek Sparse Attention version verification note.**
23. **[index.html] Standardize "key/value" to "KV" in overview text.**
24. **[8.1] Add brief research frontier callout on 1-bit models.**

---

## Summary

Module 08 is a high-quality chapter with strong pedagogical design, clear narrative arc, excellent code examples, and good visual support. The main areas for improvement are minor: date inconsistency, a few missing transition bridges, some long sentences, and small clarification opportunities. The content is current, technically accurate (with minor qualifications needed), and distinctively better than standard textbook treatments through its from-scratch implementations, informal proofs, and coverage of cutting-edge techniques like TTT and EAGLE.

**Overall Grade: A-** (would be A after TIER 1+2 fixes)
