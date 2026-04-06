# Part II Review: Structure and Self-Containment Report

**Modules reviewed:** 06 (7 sections), 07 (4 sections), 08 (4 sections) = 15 sections total
**Date:** 2026-03-26

---

## Methodology

Two review passes were performed on all 15 HTML section files, 3 index pages, and 3 chapter plans:

- **Agent 1 (Structural Refactoring Architect):** Examined section ordering, template consistency (headers, quizzes, takeaways, navigation), CSS uniformity, section length balance, lab distribution, and cross-module duplication.
- **Agent 2 (Self-Containment Verifier):** Checked prerequisite references, forward-dependency assumptions, cross-reference presence and accuracy, undefined jargon, and whether a reader can follow each section using only material the book has provided up to that point.

---

## Top 30 Findings (ranked by priority)

### 1. BLOCKING: No explicit cross-references to prerequisite modules in any section HTML

**Agent:** Self-Containment Verifier
**Location:** All 15 sections
**Details:** None of the 15 section HTML files contain textual references to prerequisite modules (e.g., "as covered in Module 04" or "see Section 6.3"). The chapter plans define upstream dependencies, and the index pages list prerequisites, but the actual section content never links back. A reader entering Section 10.2 (KV Cache) has no pointer to Module 04 (Transformer Architecture) for the attention mechanism fundamentals that KV caching depends on. Similarly, Section 7.3 (Reasoning Models) references Kaplan and Chinchilla by name but never points the reader to Section 6.3 where those scaling laws were explained in detail.
**Fix:** Add brief parenthetical or inline references at first use of prerequisite concepts, e.g., "the key-value pairs computed during self-attention (see Module 04, Section 4.X)."

---

### 2. BLOCKING: CSS format inconsistency across the three modules

**Agent:** Structural Refactoring Architect
**Location:** Module 06 (sections 6.1 vs 6.2-6.7), Module 07 (all sections), Module 08 (all sections)
**Details:** Three distinct CSS sizing patterns exist:
- Section 6.1: 308 CSS lines (expanded, multi-line declarations)
- Sections 6.2 through 6.7: ~91 CSS lines (compressed, single-line declarations)
- Module 07 sections: ~282 CSS lines (expanded, slightly different from 6.1 and 8.x)
- Module 08 sections: 308 CSS lines (expanded, matching 6.1)

This creates maintenance difficulty. A styling change must be applied differently depending on the file. All three variants render the same visual output but diverge in formatting.
**Fix:** Normalize all 15 sections to a single CSS format. Consider extracting shared CSS into a separate stylesheet file.

---

### 3. BLOCKING: Footer text inconsistent across module index pages

**Agent:** Structural Refactoring Architect
**Location:** Module 06 index, Module 07 index, Module 08 index
**Details:** Three different footer strings:
- Module 06: "Building Conversational AI using LLM and Agents" (no copyright)
- Module 07: "LLM Course (c) 2025." (different title, has copyright)
- Module 08: "(c) 2025 Building Conversational AI using LLM and Agents." (combined)

Section HTML files have no footer element at all.
**Fix:** Standardize all index footers to a single format. Add a consistent footer to section pages as well.

---

### 4. IMPORTANT: GQA/MLA content duplication between Section 7.2 and Section 10.2

**Agent:** Structural Refactoring Architect
**Location:** Section 7.2 (Open-Source Models) and Section 10.2 (KV Cache & Memory Optimization)
**Details:** Both sections independently explain GQA (Grouped-Query Attention) and MLA (Multi-head Latent Attention). Section 7.2 covers them from an architecture perspective (how DeepSeek V3 works), and Section 10.2 covers them from a memory optimization perspective (how they reduce KV cache size). The overlap is conceptually justified, but neither section acknowledges or cross-references the other. Readers going through linearly will encounter near-duplicate explanations without understanding this is intentional.
**Fix:** Add a brief cross-reference in each section. In 7.2: "We return to GQA's memory implications in Section 10.2." In 8.2: "GQA architecture details were introduced in Section 7.2; here we focus on the memory savings."

---

### 5. IMPORTANT: Section 10.2 assumes KV cache knowledge without grounding in Module 04

**Agent:** Self-Containment Verifier
**Location:** Section 10.2, lines 337-348
**Details:** Section 10.2 opens by explaining the KV cache formula but assumes the reader already understands that attention computes queries, keys, and values, and that these grow linearly with sequence length. This is correct per the prerequisite chain (Module 04 covers attention), but a single sentence referencing where this was taught would help readers who jump directly to Module 08.
**Fix:** Add at opening: "Recall from Module 04 that each attention layer computes query, key, and value projections for every token."

---

### 6. IMPORTANT: Section 7.3 uses MCTS without prerequisite coverage

**Agent:** Self-Containment Verifier
**Location:** Section 7.3, subsection 5 (Monte Carlo Tree Search)
**Details:** MCTS is introduced and explained from scratch in Section 7.3. This is good. However, the explanation is dense (approximately 100 lines of combined text and SVG) and assumes comfort with tree search concepts (selection, expansion, simulation, backpropagation). The chapter plan itself notes this may be challenging for students without game-AI background. No simplified analogy or warm-up example is provided before the language-generation application.
**Fix:** Add a 3-4 sentence simplified analogy (e.g., decision trees in everyday reasoning) before diving into the four-phase MCTS cycle.

---

### 7. IMPORTANT: Module 06 section 6.1 has different nav link count from other sections

**Agent:** Structural Refactoring Architect
**Location:** Section 6.1 navigation bars
**Details:** Section 6.1 has 7 navigation-related elements (top nav + bottom nav with different styling), while sections 6.4 through 6.7 have 6 each. The difference is in the CSS: section 6.1 includes an explicit `.chapter-nav-bottom` block definition spread across more lines, while sections 6.2 through 6.7 define it in a single compressed line. Functionally identical, but structurally divergent.
**Fix:** Normalize alongside the CSS fix in Finding #2.

---

### 8. IMPORTANT: Section 7.3 is the longest section at 949 lines; length imbalance

**Agent:** Structural Refactoring Architect
**Location:** Section 7.3 (Reasoning Models & Test-Time Compute)
**Details:** Section lengths range from 416 lines (6.5) to 957 lines (8.4), with Section 7.3 at 949 lines. The sections in Module 07 have the widest variance: 7.1 (674), 7.2 (800), 7.3 (949), 7.4 (888). Section 7.3 covers six major topics (inference-time scaling, CoT at scale, PRMs/ORMs, best-of-N, MCTS, compute-optimal inference) plus a lab. Consider splitting MCTS into its own section or making it an appendix.
**Fix:** Either split Section 7.3 into "7.3a Reasoning Models" and "7.3b Search and Verification" or trim the MCTS explanation to a high-level overview with a pointer to further reading.

---

### 9. IMPORTANT: Quiz question counts differ between modules

**Agent:** Structural Refactoring Architect
**Location:** All sections
**Details:** Module 06 sections have 5 questions each (except 6.1, which has 6). Module 07 sections have 6 questions each. Module 08 sections have 5 questions each. The inconsistency is minor but breaks the uniform template.
**Fix:** Standardize to 5 questions per section across all modules (or 6 if preferred).

---

### 10. IMPORTANT: Section 10.3 (Speculative Decoding) lacks a from-scratch implementation

**Agent:** Self-Containment Verifier
**Location:** Section 10.3, subsection 6 (Practical Implementation)
**Details:** The chapter plan and section index card promise a lab where students "implement speculative decoding from scratch." However, the actual section content shows only the Hugging Face `assistant_model` API approach and a Medusa simulation. The draft-verify-resample loop, which is the core pedagogical goal, is only described mathematically, not implemented in code. Students cannot reproduce the algorithm themselves.
**Fix:** Add a minimal speculative decoding implementation using two GPT-2 models (one small draft, one larger target) with the full accept/reject/resample loop.

---

### 11. IMPORTANT: Section 6.5 omits the WSD learning rate schedule

**Agent:** Self-Containment Verifier
**Location:** Section 6.5, subsection 5 (Learning Rate Schedules)
**Details:** The chapter plan flags this gap: the Warmup-Stable-Decay (WSD) schedule used by Llama 3 and DeepSeek V3 is not mentioned. The section covers warmup + cosine decay only. Since Module 07 discusses Llama 3 and DeepSeek V3 architecture, students who read Section 7.2 will encounter models whose training schedule was never explained.
**Fix:** Add a brief subsection on WSD between cosine decay and gradient accumulation.

---

### 12. IMPORTANT: No section HTML files contain a `<footer>` element

**Agent:** Structural Refactoring Architect
**Location:** All 15 section HTML files
**Details:** All index pages have footers, but none of the section pages do. The section pages end with the bottom navigation bar and then close the `</body>` tag. This is a template inconsistency.
**Fix:** Add a consistent footer to all section pages matching the index page footer format.

---

### 13. IMPORTANT: Section 6.4 (Data Curation) lacks a quality filtering code example

**Agent:** Self-Containment Verifier
**Location:** Section 6.4, subsection 5 (Quality Filtering)
**Details:** The section describes heuristic and perplexity-based quality filtering conceptually but provides no code example. The code examples cover MinHash deduplication and domain mixing but skip filtering, which is the most commonly needed skill for students building data pipelines.
**Fix:** Add a minimal code example demonstrating heuristic quality filtering (length, language detection, symbol ratios).

---

### 14. IMPORTANT: Section 7.1 contains time-sensitive pricing data without a "last updated" note

**Agent:** Self-Containment Verifier
**Location:** Section 7.1 (Closed-Source Frontier Models)
**Details:** The section includes specific pricing per million tokens for GPT-4o, Claude, Gemini, and others. These prices change frequently (sometimes monthly). The SVG diagram notes "Landscape as of early 2025" but the pricing tables have no such caveat. Students may treat these as current prices when they are likely outdated.
**Fix:** Add a "Pricing as of [date]; check provider websites for current rates" note above or below each pricing table.

---

### 15. IMPORTANT: Section 10.4 has no TensorRT-LLM code example

**Agent:** Self-Containment Verifier
**Location:** Section 10.4, subsection 5 (TensorRT-LLM)
**Details:** vLLM, TGI, and Ollama each have runnable code examples (server launch, API calls, benchmarking). TensorRT-LLM has only a descriptive paragraph. Since TensorRT-LLM is positioned as the highest-throughput option (30-50% over vLLM), the lack of a concrete example makes it harder for students to evaluate or try it.
**Fix:** Add a Docker-based deployment example for TensorRT-LLM, similar to the TGI docker example.

---

### 16. IMPORTANT: Section 7.2 MLA explanation lacks a worked numerical example

**Agent:** Self-Containment Verifier
**Location:** Section 7.2, subsection 4.1 (Multi-head Latent Attention)
**Details:** The chapter plan flags this: the MLA explanation jumps from concept to code without showing the dimensionality math. Students are told MLA achieves "93% cache reduction" but the path from (e.g.) 128-dim KV to 16-dim latent to 93% compression is not shown concretely.
**Fix:** Add a brief worked example: "For 128 KV heads with head_dim=128, standard cache stores 128 x 128 = 16,384 values per layer per token. MLA compresses to a 512-dim latent, storing only 512 values. Compression: 512/16,384 = 3.1%, a 97% reduction."

---

### 17. IMPORTANT: Module 07 index page has prereqs before sections list (different order from 06 and 08)

**Agent:** Structural Refactoring Architect
**Location:** Module 07 index.html, lines 193-201
**Details:** Module 06 index: Overview, Objectives, Sections, Prerequisites. Module 07 index: Overview, Objectives, Prerequisites, Sections. Module 08 index: Overview, Objectives, Prerequisites, Sections. Module 07 and 08 match each other but differ from Module 06, where prerequisites come after the sections list.
**Fix:** Move Module 06 prerequisites before the sections list to match Modules 07 and 08.

---

### 18. IMPORTANT: Section 6.6 (Distributed Training) lacks tensor parallelism math

**Agent:** Self-Containment Verifier
**Location:** Section 6.6, subsection 4 (Tensor Parallelism)
**Details:** The chapter plan notes that tensor parallelism is described abstractly (column vs. row splitting) but the actual matrix multiplication showing how work distributes across devices is not shown. Students who have not seen this before may struggle to visualize how a single linear layer is split across GPUs.
**Fix:** Add a small worked example: "A weight matrix W of shape [4096, 4096] is split column-wise across 4 GPUs, each holding W_i of shape [4096, 1024]. Each GPU computes Y_i = X * W_i locally, then an all-reduce gathers the full output."

---

### 19. OPTIONAL: Sections 7.1 and 7.4 lack dedicated lab exercises

**Agent:** Structural Refactoring Architect
**Location:** Section 7.1 (Closed-Source Frontier) and Section 7.4 (Multilingual)
**Details:** Sections 7.2 and 7.3 have explicit lab sections. Sections 7.1 and 7.4 do not. The chapter plan acknowledges this gap and suggests a guided API comparison lab for 7.1 and a multilingual evaluation lab for 7.4.
**Fix:** Add a lab exercise to each: (7.1) compare API responses from two providers on the same prompt; (7.4) evaluate a multilingual model on a set of languages and compare tokenization efficiency.

---

### 20. OPTIONAL: Section 7.3 does not explain the GRPO algorithm used to train DeepSeek-R1

**Agent:** Self-Containment Verifier
**Location:** Section 7.3, subsection 2 (Chain-of-Thought at Scale)
**Details:** DeepSeek-R1 is discussed as a key reasoning model, and its training process (RL-trained chain-of-thought) is mentioned. But the GRPO (Group Relative Policy Optimization) algorithm that makes R1's training work is not described. Students interested in reproducing or understanding reasoning model training have no starting point.
**Fix:** Add a brief paragraph explaining GRPO at a high level: reward computation, group-relative scoring, and how it differs from PPO.

---

### 21. OPTIONAL: Section 6.3 data-constrained scaling discussion is thin

**Agent:** Self-Containment Verifier
**Location:** Section 6.3, subsection 5 (Data-Constrained Scaling)
**Details:** The section mentions repeating data but does not cite the Muennighoff et al. (2023) finding that up to 4 epochs of repetition causes minimal degradation. This is a practically important result for teams with limited data budgets.
**Fix:** Add 2-3 sentences summarizing the data repetition findings and their practical implications.

---

### 22. OPTIONAL: Section 6.1 quiz has 6 questions; all other Module 06 sections have 5

**Agent:** Structural Refactoring Architect
**Location:** Section 6.1 quiz
**Details:** Minor template inconsistency. Section 6.1 has 6 quiz questions while sections 6.2 through 6.7 have 5 each.
**Fix:** Either remove one question from 6.1 or add one to each of 6.2 through 6.7.

---

### 23. OPTIONAL: Section 10.1 does not cover GGUF format

**Agent:** Self-Containment Verifier
**Location:** Section 10.1 (Model Quantization)
**Details:** GGUF is the dominant format for local inference with llama.cpp and Ollama (covered in Section 10.4). But Section 10.1, which covers quantization in depth, never mentions GGUF or its mixed-precision strategy (different bit widths for different layers). Students arrive at Section 10.4 encountering GGUF without understanding how it relates to the quantization methods they just learned.
**Fix:** Add a brief subsection in 8.1 on GGUF format and how it applies quantization at varying granularity across layers.

---

### 24. OPTIONAL: Section 6.5 grokking explanation lacks connection to double descent

**Agent:** Self-Containment Verifier
**Location:** Section 6.5, subsection 7 (Training Dynamics)
**Details:** Grokking is introduced but the connection to regularization and double descent is not drawn. Students may not understand why grokking matters for LLM training decisions (e.g., justifying longer training with weight decay).
**Fix:** Add 2-3 sentences connecting grokking to regularization theory and the double descent phenomenon.

---

### 25. OPTIONAL: Section 10.2 TTT (Test-Time Training) explanation is too brief

**Agent:** Self-Containment Verifier
**Location:** Section 10.2, subsection 8 (Research Frontiers)
**Details:** TTT is described in one paragraph. Students may confuse it with fine-tuning, since both involve weight updates. The key distinction (TTT happens during inference, compresses context into temporary weights, and is discarded after the request) is not clearly stated.
**Fix:** Expand with a comparison: "Unlike fine-tuning, which permanently updates weights, TTT creates temporary weights for a single request, compressing long-context information. These weights are discarded after generation completes."

---

### 26. OPTIONAL: Scaling law terms (FLOPs vs FLOPS) not consistently used

**Agent:** Self-Containment Verifier
**Location:** Section 6.3 and cross-referencing chapter plan terminology table
**Details:** The terminology table specifies "FLOPs" (floating-point operations, plural) vs. "FLOPS" (operations per second). In Section 6.3 and Section 10.3, the term "FLOPs" is used correctly. However, the chapter plan's careful distinction is not surfaced in the section text, meaning students may remain confused about the difference.
**Fix:** Add a brief inline note on first use in Section 6.3: "FLOPs (floating-point operations; not to be confused with FLOPS, which measures operations per second)."

---

### 27. OPTIONAL: Section 7.4 has no lab exercise (confirmed by index badge mismatch)

**Agent:** Structural Refactoring Architect
**Location:** Module 07 index.html and Section 7.4
**Details:** The Module 07 index page does NOT show a Lab badge for Section 7.4 (correct, since there is no lab). However, the chapter plan recommends adding one. Sections 7.2 and 7.3 have Lab badges; 7.1 and 7.4 do not. This creates uneven hands-on experience across the module.
**Fix:** Same as Finding #19; add a lab to Section 7.4.

---

### 28. OPTIONAL: Module 08 prerequisite lists Module 07 but Module 07 is not strictly required for 8.1

**Agent:** Self-Containment Verifier
**Location:** Module 08 index prerequisites
**Details:** Module 08 lists Module 07 as a prerequisite, referencing "Llama, Mistral, DeepSeek architecture details, GQA, MoE." However, Section 10.1 (Quantization) and Section 10.3 (Speculative Decoding) can be understood without Module 07 knowledge. Only Section 10.2 (KV Cache, GQA discussion) truly requires Module 07. Listing Module 07 as a blanket prerequisite may discourage students who want to jump directly to inference optimization.
**Fix:** Refine the prerequisite to: "Module 07 recommended for Sections 8.2 and 8.4; Sections 8.1 and 8.3 can be read with Module 04 and 05 knowledge alone."

---

### 29. OPTIONAL: Section 10.3 mathematical proof of lossless speculative decoding is absent

**Agent:** Self-Containment Verifier
**Location:** Section 10.3, subsection 2 (Acceptance and Rejection Sampling)
**Details:** The Key Insight callout states that speculative decoding preserves the target distribution, but the probability argument is not shown. The acceptance criterion formula is given (min(1, q(x)/p(x))), but why this specific formula guarantees distributional equivalence is not explained. Curious students have no way to verify the claim from the text alone.
**Fix:** Add a brief informal proof: "For any token x, the probability of accepting and keeping x is p(x) * min(1, q(x)/p(x)). When q(x) >= p(x), this equals p(x) * 1 = p(x). When q(x) < p(x), the rejected probability mass is redistributed via resampling from max(0, q(x) - p(x)), which adds back exactly the missing probability. The net distribution is thus q(x) exactly."

---

### 30. OPTIONAL: Section 6.6 omits sequence parallelism and context parallelism

**Agent:** Self-Containment Verifier
**Location:** Section 6.6 (Distributed Training)
**Details:** The chapter plan flags this: sequence parallelism (for long-context training) and context parallelism (ring attention) are not discussed. With long-context models becoming standard (128K+ context for Llama 3, 1M for Gemini), these techniques are increasingly relevant.
**Fix:** Add a brief "Beyond Data and Model Parallelism" subsection mentioning sequence parallelism and ring attention, with pointers to the original papers.

---

## Summary Statistics

| Metric | Module 06 | Module 07 | Module 08 |
|--------|-----------|-----------|-----------|
| Sections | 7 | 4 | 4 |
| Line range | 416-722 | 674-949 | 790-957 |
| CSS style | Mixed (6.1 expanded, rest compressed) | Expanded (~282 lines) | Expanded (~308 lines) |
| Quiz questions | 5-6 per section | 6 per section | 5 per section |
| Big Picture callout | All present | All present | All present |
| Key Takeaways | All present | All present | All present |
| Footer (section pages) | None | None | None |
| Footer (index pages) | Variant A | Variant B | Variant C |
| Cross-refs to prereqs | Zero | Zero | Zero |
| Lab exercises | 6.3, 6.4, 6.6 | 7.2, 7.3 | 8.1, 8.3, 8.4 |

## Severity Distribution

| Severity | Count |
|----------|-------|
| BLOCKING | 3 |
| IMPORTANT | 15 |
| OPTIONAL | 12 |
