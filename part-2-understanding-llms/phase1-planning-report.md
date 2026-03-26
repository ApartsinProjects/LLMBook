# Part II Planning Review: Modules 06, 07, 08

## Overview

Three planning perspectives evaluated all 15 HTML sections and 3 chapter plans across Part II. Module 06 (Pre-training, Scaling Laws & Data Curation) has 7 sections. Module 07 (Modern LLM Landscape) has 4 sections. Module 08 (Inference Optimization) has 4 sections.

**Module flow ratings:**
- Module 06: SMOOTH. The narrative arc from landmark models to training objectives to scaling to data to optimizers to distributed training to ICL theory is logical and well-connected.
- Module 07: ADEQUATE. The progression from closed-source to open-weight to reasoning to multilingual is sound, but the jump from reasoning models (7.3) to multilingual LLMs (7.4) feels abrupt; a bridging sentence or transition paragraph is needed.
- Module 08: SMOOTH. The cascade from quantization to KV cache to speculative decoding to serving infrastructure follows the natural optimization pipeline clearly.

---

## Top 30 Findings (Ranked by Priority)

### Critical (Would Confuse or Mislead Students)

**1. [Module 08, Section 8.3] No from-scratch speculative decoding implementation.**
The section describes the draft-verify-resample loop mathematically and shows the Hugging Face `assistant_model` API, but never walks through the core algorithm manually. The chapter plan promises this, and the syllabus lists it as a lab. Students cannot deeply understand acceptance/rejection sampling from an API call alone. Add a 30-line pedagogical implementation with a toy model.

**2. [Module 08, Section 8.3] Mathematical proof of distribution preservation is missing.**
The Key Insight callout states that speculative decoding is "lossless," but the probability argument is never shown. Students are asked to accept this crucial guarantee on faith. Even an informal walkthrough (showing that accepted + resampled tokens together recover the target distribution) would prevent misconceptions.

**3. [Module 07, Section 7.2] MLA explanation lacks mathematical intuition.**
The section jumps from high-level KV compression concept to code without showing a concrete dimensionality example. A worked calculation (e.g., "Standard MHA for 128 heads with d_head=128 caches 128 x 128 = 16,384 dims; MLA compresses to 512 dims, a 32x reduction") would make the claimed 93% savings verifiable.

**4. [Module 06, Section 6.5] WSD (warmup-stable-decay) learning rate schedule is absent.**
The section covers warmup + cosine decay but omits WSD, which is now used by Llama 3, DeepSeek V3, and other recent models. Since these models are discussed in Module 07, students will encounter WSD references with no prior explanation. Add at minimum a subsection with the three-phase schedule and its rationale (enables learning rate restarts and continued pre-training).

**5. [Module 06, Section 6.4] No code example for quality filtering.**
The section describes heuristic, perplexity-based, and classifier-based filtering conceptually but provides no code. The chapter plan itself flags this gap. A minimal example (even pseudocode showing length/character-ratio heuristics applied to a sample document) would complete the pipeline story that starts with MinHash code.

### High Priority (Significant Gaps in Depth or Coverage)

**6. [Module 08, Section 8.2] GQA memory savings not demonstrated numerically.**
The MHA vs. MQA vs. GQA table lists qualitative differences, but no worked calculation shows the concrete memory difference. A calculation such as "Llama 3 8B with 8 KV heads (GQA) uses X GB KV cache at 4K context vs. Y GB with full 32 KV heads (MHA)" would make the architectural choice tangible.

**7. [Module 06, Section 6.6] Tensor parallelism math is abstract.**
Column vs. row splitting is described verbally but no matrix multiplication example is shown. A small 4x4 matrix split across 2 GPUs, showing how partial products are computed and combined, would clarify the concept for students without distributed-systems background.

**8. [Module 07, Section 7.3] MCTS section is dense and lacks scaffolding.**
The section moves directly from best-of-N sampling to full MCTS for language with no intermediate example. Students without game-AI background will struggle. A simple "MCTS for choosing the best next sentence" toy example before the full treatment would help.

**9. [Module 08, Section 8.1] GGUF format not discussed.**
GGUF is the dominant quantization format for local inference (llama.cpp, Ollama), which Section 8.4 extensively covers. Students using Ollama in Section 8.4 will encounter GGUF models immediately. Section 8.1 should explain GGUF's mixed-precision approach (different bit widths for attention vs. feed-forward layers).

**10. [Module 08, Section 8.2] TTT (Test-Time Training) explanation is too brief.**
TTT is a genuinely novel concept that students could easily confuse with standard fine-tuning. The current two-paragraph treatment does not adequately distinguish TTT (which happens during inference, compressing context into temporary weight updates) from continued pre-training. A diagram showing the inference-time weight update loop would help.

**11. [Module 07, Section 7.3] DeepSeek-R1 GRPO training algorithm not explained.**
The section describes the R1 training pipeline at a high level (pure RL, then SFT, then RL again) but never names or explains GRPO (Group Relative Policy Optimization), which is the specific algorithm that enables emergent reasoning. Since R1 is discussed as a landmark result, a brief outline of GRPO's mechanism would strengthen the section.

**12. [Module 06, Section 6.3] Data-constrained scaling section is underdeveloped.**
The Muennighoff et al. finding about data repetition (up to 4 epochs with minimal degradation) is mentioned in a single paragraph. Given that data scarcity is a growing concern for the field, this deserves expansion: the effective-data formula is shown but not contextualized with practical guidance on when to repeat vs. augment vs. synthesize data.

### Medium Priority (Content Completeness and Structural Issues)

**13. [Module 06, Section 6.1] PaLM, BLOOM, and Falcon absent from landmark survey.**
The chapter plan identifies this gap. PaLM introduced the Pathways system and demonstrated 540B-scale training. BLOOM was the first large-scale multilingual open-science model. Falcon demonstrated the value of open training data. These deserve at least table entries and brief mentions.

**14. [Module 07, Section 7.2] Gemma model family missing.**
Despite Google's Gemma 2 and Gemma 3 being competitive open-weight models (and mentioned in the module index page), they receive no dedicated discussion. A brief subsection or expanded table entry is warranted.

**15. [Module 07, Section 7.2] Model licensing discussion is shallow.**
The section distinguishes open-source from open-weight but does not explain the practical licensing differences (Llama community license restrictions for 700M+ MAU companies, Apache 2.0, etc.). For production deployments, this is critical information.

**16. [Module 08, Section 8.4] TensorRT-LLM has no code example.**
Unlike vLLM, TGI, and Ollama, which all have runnable examples, TensorRT-LLM is described only textually. Even a Docker-based deployment snippet would improve parity across the framework comparison.

**17. [Module 08, Section 8.1] GPTQ Hessian explanation is insufficient.**
The section describes GPTQ as "Hessian-based optimal rounding" but does not explain what the Hessian captures (second-order sensitivity of loss to weight perturbations). Students without optimization background will not understand why this approach outperforms naive rounding.

**18. [Module 07, Section 7.1] No discussion of model deprecation and versioning.**
Students should understand that frontier models are moving targets: GPT-4 Turbo was replaced by GPT-4o, pricing changes frequently, and older model versions get deprecated. A brief note on how to stay current and plan for model transitions would be practical.

**19. [Module 06, Section 6.6] Sequence parallelism and context parallelism absent.**
For long-context training (ring attention, sequence parallelism), these techniques are increasingly important. The chapter plan flags this gap. A brief mention and forward reference to Module 08 would suffice.

**20. [Module 07, Section 7.4] No hands-on lab exercise.**
Sections 7.2 and 7.3 have explicit labs, but 7.4 has none. A lab evaluating a multilingual model's tokenization efficiency across languages, or demonstrating vocabulary extension, would strengthen this section. The chapter plan also identifies this gap.

**21. [Module 08, Section 8.2] H2O eviction policy mentioned but not explained.**
The section lists H2O (Heavy-Hitter Oracle), sliding window attention, and StreamingLLM as KV cache compression techniques but does not explain when each is appropriate or the quality tradeoffs. Students need at least a brief comparison to make informed choices.

**22. [Module 06, Section 6.5] Grokking not connected to double descent or regularization theory.**
Grokking is introduced and explained, but the connection to the broader double-descent phenomenon and the role of regularization in enabling the transition from memorization to generalization is not drawn explicitly. Students may not understand why grokking matters beyond being an interesting curiosity.

**23. [Module 07, Section 7.3] Hallucination behavior of reasoning models not discussed.**
Reasoning traces can make hallucinations either more transparent (the student can see where the reasoning went wrong) or more convincing (a coherent but incorrect chain of thought). This practical consideration is absent.

**24. [Module 07, Section 7.4] Vocabulary extension initialization not fully explained.**
The code example shows random initialization with scaling but does not explain why this works or what alternatives exist (e.g., initializing new token embeddings from the mean of their subword components). Students will wonder why random initialization does not destroy model performance.

### Lower Priority (Polish and Consistency)

**25. [Module 06, Section 6.1] CSS format inconsistency.**
Section 6.1 uses an expanded multi-line CSS style (300+ lines), while Sections 6.2 through 6.7 use a compressed single-line CSS format. This does not affect rendering but makes maintenance harder. Standardize to the compressed format used by the majority.

**26. [Module 07] Section length imbalance.**
Section 7.3 (949 lines) and 7.4 (888 lines) are significantly longer than 7.1 (674 lines). This creates uneven reading time. Consider whether 7.3 or 7.4 could be split or trimmed.

**27. [Module 08] Redundancy with Module 07 on GQA and MLA.**
Section 8.2 discusses GQA and MLA, which are also covered in Section 7.2 (DeepSeek V3 deep dive). The overlap is intentional (architecture in 7.2, memory optimization in 8.2) but should be explicitly acknowledged with a cross-reference callout to avoid student confusion.

**28. [Module 07, Section 7.1] Pricing and capability data will become outdated.**
Section 7.1 contains specific pricing numbers and capability claims that will age quickly. Adding a "last updated: [date]" note to the comparison tables and structuring them for easy updates would improve maintainability.

**29. [Module 08, Section 8.4] Cost optimization and auto-scaling not covered.**
The section covers the serving stack thoroughly but does not discuss cost optimization strategies: spot instances, model caching across cold starts, auto-scaling policies, or the economics of self-hosted vs. API inference. These are important for production deployment decisions.

**30. [Module 08, Section 8.4] Apple Silicon / MLX inference absent.**
Given the growing number of developers using MacBooks, the lack of any mention of the MLX framework or Apple Silicon inference is a practical gap. A brief note under the local inference section (alongside Ollama) would help.

---

## Module-Level Summaries

### Module 06: Pre-training, Scaling Laws & Data Curation

**Curriculum alignment:** Strong. All 7 learning objectives are addressed. The progression from landmark models to training objectives to scaling laws to data curation to optimizers to distributed training to ICL theory covers the promised scope comprehensively. The one notable omission is the WSD learning rate schedule (finding #4).

**Deep explanation quality:** Generally excellent. Mathematical formulations are provided for all key concepts (CLM/MLM loss, scaling law equations, Adam update rules, influence functions). The scaling laws section does a particularly good job of answering WHAT (power law relationships), WHY (empirical discovery), HOW (curve fitting code), and WHEN (Kaplan vs. Chinchilla vs. over-training regimes). Weak spots: tensor parallelism math (#7), data-constrained scaling (#12), and the grokking-regularization connection (#22).

**Teaching flow:** SMOOTH. Each section builds naturally on the previous one. The "Big Picture" callouts at the start of each section effectively frame why the topic matters. Quizzes at the end of each section reinforce learning. The narrative arc from "what exists" to "how it works" to "what makes it possible" is well-executed.

### Module 07: Modern LLM Landscape

**Curriculum alignment:** Good with gaps. The four-section structure covers closed-source, open-weight, reasoning, and multilingual dimensions well. Key gaps: Gemma models (#14), model licensing nuances (#15), GRPO algorithm (#11), and reasoning model hallucination behavior (#23). The DeepSeek V3 deep dive in 7.2 is a highlight.

**Deep explanation quality:** Mixed. The MLA explanation needs mathematical grounding (#3). The MCTS treatment needs scaffolding (#8). The reasoning model section (7.3) is the strongest in terms of depth, with clear explanations of best-of-N sampling, PRM vs. ORM, and compute-optimal inference. The multilingual section (7.4) provides solid conceptual coverage but would benefit from a lab exercise (#20).

**Teaching flow:** ADEQUATE. The progression from closed-source to open-weight is natural (opacity to transparency). The jump from reasoning models (7.3) to multilingual LLMs (7.4) is the weakest transition; a bridging paragraph explaining that "having surveyed cutting-edge capabilities, we now ask: who benefits from these advances?" would improve the flow.

### Module 08: Inference Optimization

**Curriculum alignment:** Strong. All 8 learning objectives are addressed. The four-pillar structure (quantization, KV cache, speculative decoding, serving) covers the promised scope. The most significant gap is the missing from-scratch speculative decoding implementation (#1), which the syllabus promises as a lab exercise.

**Deep explanation quality:** Good overall. Quantization mathematics are thorough (absmax, zero-point, per-group, NF4). KV cache memory formulas with worked calculator code are excellent. The speculative decoding section explains the concept well but fails to prove its key guarantee (#2). The serving infrastructure section provides the best practical coverage in the module, with runnable code for vLLM, TGI, and Ollama.

**Teaching flow:** SMOOTH. The optimization cascade (compress weights, optimize memory, parallelize decoding, deploy serving system) creates a coherent journey. Each section motivates the next: quantization reduces model size, revealing KV cache as the next bottleneck; KV cache optimization reveals the sequential decoding bottleneck; speculative decoding breaks that bottleneck; serving infrastructure puts everything together. The forward reference from 8.1 (quantization) to 8.2 (KV cache quantization) could be strengthened.
