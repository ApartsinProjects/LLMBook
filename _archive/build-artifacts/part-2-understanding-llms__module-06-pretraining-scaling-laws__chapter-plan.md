# Chapter Plan: Module 06 - Pre-training, Scaling Laws & Data Curation

## Scope

**What this chapter covers:** The full lifecycle of training a large language model, from data collection through optimization to convergence. Specifically: the landmark models that defined the field (BERT, GPT series, T5); the pre-training objectives that teach models language (causal LM, masked LM, span corruption, fill-in-the-middle, multi-token prediction); the scaling laws that predict performance as a function of compute, parameters, and data (Kaplan, Chinchilla, over-training regimes); data curation pipelines (web crawling, deduplication, quality filtering, domain mixing, toxicity removal); optimizer internals and training dynamics (Adam, AdamW, Adafactor, learning rate schedules, gradient accumulation, instabilities); distributed training infrastructure (DDP, FSDP, ZeRO, tensor parallelism, pipeline parallelism, mixed precision, gradient checkpointing); and the theoretical foundations of in-context learning (meta-learning, implicit gradient descent, task vectors, mesa-optimization).

**What this chapter does NOT cover:** Fine-tuning and alignment (Module 13, 16), inference optimization and serving (Module 08), specific API usage for closed-source models (Module 09), prompt engineering (Module 10), or RLHF/DPO preference tuning (Module 16). While landmark models are surveyed, the detailed architecture deep dives for modern open-weight models belong to Module 07. Tokenization is covered in Module 02 and is assumed knowledge here.

**Target audience:** Students who have completed Part I (Modules 00 through 05) and understand the Transformer architecture, attention mechanisms, tokenization, and basic PyTorch training loops.

**Target length:** ~18,000 to 22,000 words across seven sections (the largest module in Part II by section count).

---

## Learning Objectives

1. Trace the evolution from BERT to GPT-4, identifying the key architectural and training decisions that defined each era.
2. Compare and implement pre-training objectives: causal LM, masked LM, span corruption, fill-in-the-middle, and multi-token prediction.
3. Apply Kaplan and Chinchilla scaling laws to estimate optimal model size and data requirements for a given compute budget.
4. Design a data curation pipeline with deduplication, quality filtering, and domain mixing.
5. Explain how Adam, AdamW, and Adafactor work, and select appropriate learning rate schedules for large-scale training.
6. Distinguish between DDP, FSDP, ZeRO, tensor parallelism, and pipeline parallelism, and select the right strategy for a given hardware setup.
7. Discuss leading theories of in-context learning: meta-learning, implicit gradient descent, and task vectors.

---

## Prerequisites

- Solid understanding of the Transformer architecture (Module 04): self-attention, multi-head attention, feed-forward layers, positional encodings
- Familiarity with attention mechanisms (Module 03): dot-product attention, cross-attention
- Basic PyTorch proficiency (Module 00): training loops, autograd, nn.Module, optimizers
- Understanding of tokenization and subword models (Module 02): BPE, SentencePiece, vocabulary construction
- Comfort with basic probability and information theory: cross-entropy, perplexity, KL divergence
- Familiarity with decoding strategies (Module 05): autoregressive generation, sampling methods

---

## Detailed Section Structure

### Section 6.1: The Landmark Models

**Key concepts:**
- BERT and bidirectional understanding: MLM + NSP objectives, BERT-base vs. BERT-large
- BERT variants: RoBERTa (removed NSP, dynamic masking), DeBERTa (disentangled attention), ALBERT (parameter sharing)
- GPT series evolution: GPT-1 (transfer learning proof), GPT-2 (zero-shot emergence), GPT-3 (in-context learning revolution), InstructGPT/ChatGPT (alignment), GPT-4 (multimodal)
- T5 and the text-to-text framework: every NLP task as text generation
- Emergence and scaling: in-context learning, chain-of-thought reasoning
- The open-weight movement: democratization of access

**Diagrams present:**
- SVG: BERT architecture family tree (BERT, RoBERTa, DeBERTa, ALBERT with key differences)
- SVG: GPT series timeline with parameter counts and key milestones

**Code examples:**
- Loading and using BERT for masked language modeling (Hugging Face pipeline)
- GPT-2 zero-shot text generation

**Exercises:**
- Quiz: 5+ check-your-understanding questions covering model comparisons, architectural choices, and emergence

**Callouts:** Big Picture (opening), Key Insight (in-context learning), Note (T5 flexibility), Warning (emergence debate)

**Comparison table:** Model landscape (BERT, GPT-2, GPT-3, T5, Llama 2, Llama 3, Mistral) with params, training data, objective, and key innovation

---

### Section 6.2: Pre-training Objectives & Paradigms

**Key concepts:**
- Causal Language Modeling (CLM): mathematical formulation, shifted labels, why every token gives a gradient signal, train-test alignment
- Masked Language Modeling (MLM): 15% masking strategy, bidirectional context, strengths for understanding tasks, sample efficiency limitations
- Span Corruption and Denoising: T5 approach, variable-length spans, UL2 mixture of denoisers
- Prefix Language Modeling: bidirectional prefix with causal suffix
- Fill-in-the-Middle (FIM): PSM/SPM transformations for code completion, how FIM enables infilling without architectural changes
- Multi-Token Prediction: shared trunk with N independent heads, improved sample efficiency, connection to speculative decoding

**Diagrams present:**
- SVG: CLM vs. MLM side-by-side (attention masks, training signals)
- SVG: Multi-token prediction architecture (shared trunk, multiple heads)

**Code examples:**
- Causal LM loss from scratch (shifted logits, cross-entropy, perplexity)
- T5 span corruption simulation (sentinel tokens, input/target pairs)
- Fill-in-the-Middle transformation (prefix-suffix-middle rearrangement)
- Multi-token prediction conceptual implementation

**Exercises:**
- Quiz: 5 questions on objective selection, train-test mismatch, FIM mechanics

**Comparison table:** Pre-training objectives (CLM, MLM, Span, Prefix, FIM, MTP) with directionality, signal density, generation capability, and example models

---

### Section 6.3: Scaling Laws & Compute-Optimal Training

**Key concepts:**
- Power law foundation: L(x) = a * x^(-alpha) + L_infinity, log-log linearity, irreducible loss
- Kaplan scaling laws (2020): loss vs. N, D, C; exponents alpha_N, alpha_D, alpha_C; compute-optimal recipe favoring larger models
- Chinchilla scaling laws (2022): equal scaling of parameters and tokens; L(N,D) = E + A/N^alpha + B/D^beta; 20 tokens per parameter rule
- Beyond Chinchilla: over-training for inference efficiency (Llama approach), trading training compute for smaller, faster models
- Data-constrained scaling: repeating data, epoch-based training, diminishing returns
- Emergent capabilities and phase transitions: the metric mirage hypothesis (Schaeffer et al.)
- Multi-token prediction and its interaction with scaling

**Diagrams present:**
- SVG: Kaplan vs. Chinchilla compute budget allocation (bar chart comparison)
- SVG: Emergent abilities, smooth vs. sharp transitions

**Code examples:**
- Fitting power law curves to mini-model training runs (NumPy, SciPy curve_fit)
- Computing Chinchilla-optimal allocation for a given FLOP budget

**Exercises:**
- Quiz: 5 questions on scaling law application, Chinchilla vs. Kaplan, over-training rationale

**Summary table:** Scaling regimes (Kaplan, Chinchilla, Over-training, Data-constrained) with strategy, ratio, and example models

---

### Section 6.4: Data Curation at Scale

**Key concepts:**
- Pre-training data sources: Common Crawl, The Pile, RedPajama, FineWeb, DCLM, C4, RefinedWeb
- The data curation pipeline: crawl, extract, deduplicate, filter, mix, package
- Text extraction: HTML parsing, boilerplate removal (trafilatura, resiliparse)
- Deduplication: exact (URL/hash), near-duplicate (MinHash/LSH), substring-level (suffix arrays)
- Quality filtering: heuristic rules (length, language, symbol ratios), perplexity-based (KenLM), classifier-based (fastText quality scorer)
- Data mixing: domain proportions, their impact on capabilities, DoReMi-style optimization
- Toxicity and PII removal: content classifiers, regex-based PII detection, tension between safety and capability
- Data pruning and influence functions: TRAK, datamodels, membership inference, connection to copyright litigation

**Diagrams present:**
- SVG: End-to-end data curation pipeline (flow diagram with stages)

**Code examples:**
- MinHash near-duplicate detection (building shingles, hashing, Jaccard estimation)
- Domain mixing with weighted sampling

**Exercises:**
- Quiz: 5 questions on deduplication techniques, quality filtering tradeoffs, data mixing

**Tables:**
- Pre-training data sources (name, size, composition, license)
- Major open datasets comparison (FineWeb, DCLM, RedPajama, The Pile)

---

### Section 6.5: Optimizers & Training Dynamics

**Key concepts:**
- SGD limitations for Transformer training: sensitivity to learning rate, slow convergence
- Adam: first and second moment estimation, bias correction, memory cost (2x model params for states)
- AdamW: decoupled weight decay, why L2 regularization differs from weight decay in adaptive optimizers
- Memory-efficient alternatives: Adafactor (factored second moments), 8-bit Adam (quantized states), LION (sign-based updates)
- Learning rate schedules: warmup (preventing early divergence), cosine decay, cosine with restarts, WSD schedule
- Gradient accumulation: simulating large batch sizes, interaction with learning rate
- Training dynamics: loss landscape geometry, sharp vs. flat minima, the grokking phenomenon
- Training instabilities: loss spikes (root causes), gradient clipping, z-loss regularization

**Diagrams present:**
- SVG: Grokking phenomenon (training loss vs. test accuracy over time)

**Code examples:**
- Adam optimizer internals (manual moment computation)
- Cosine decay learning rate schedule with warmup

**Exercises:**
- Quiz: 5 questions on optimizer selection, warmup rationale, grokking

**Comparison table:** Optimizers (SGD, Adam, AdamW, Adafactor, 8-bit Adam, LION) with memory, speed, stability, and typical use cases

---

### Section 6.6: Distributed Training at Scale

**Key concepts:**
- Communication primitives: all-reduce, all-gather, reduce-scatter; ring vs. tree topologies
- Data Parallelism (DDP): replicated model, gradient all-reduce, synchronized SGD
- FSDP and ZeRO: parameter sharding, ZeRO stages (1: optimizer states, 2: +gradients, 3: +parameters)
- Tensor parallelism: column and row splitting of linear layers, all-reduce placement
- Pipeline parallelism: micro-batching, 1F1B schedule, pipeline bubble overhead
- Mixed precision: FP16 (requires loss scaling), BF16 (range preserved), FP8 (Hopper GPUs, DeepSeek V3 demonstration)
- Gradient checkpointing: recomputing activations to trade compute for memory
- Combining parallelism strategies: 3D parallelism in practice

**Diagrams present:**
- SVG: DDP workflow (replicate, forward, backward, all-reduce)
- SVG: Pipeline parallelism micro-batch schedule (1F1B with bubble visualization)

**Code examples:**
- DDP training with PyTorch (init_process_group, DistributedDataParallel)
- FSDP training setup (auto_wrap_policy, ShardingStrategy)
- Gradient checkpointing activation savings measurement

**Exercises:**
- Quiz: 5 questions on parallelism strategy selection, ZeRO stages, mixed precision tradeoffs

**Tables:**
- Communication primitives (operation, description, use case)
- Mixed precision data types (FP32, FP16, BF16, FP8 with range, precision, use case)

---

### Section 6.7: In-Context Learning Theory

**Key concepts:**
- The mystery of ICL: learning from prompt examples without gradient updates
- Bayesian inference interpretation (Xie et al. 2022): ICL as posterior inference over latent concepts
- Implicit gradient descent (Akyurek et al. 2023, Von Oswald et al. 2023): attention layers performing optimization steps on in-context data
- Task vectors: how demonstrations shift internal representations toward task-relevant subspaces
- Mesa-optimization: whether transformers learn internal optimization algorithms
- Practical implications: why prompt design, example selection, and ordering matter
- Limitations: distribution shift, complex reasoning, long-context degradation
- Connection to few-shot prompting practice

**Diagrams present:**
- SVG: ICL theories comparison (Bayesian, gradient descent, task vectors as three pathways)

**Code examples:**
- Few-shot classification example
- Conceptual demonstration of task vector extraction (hidden state differences)

**Exercises:**
- Quiz: 5 questions on ICL theories, practical implications, failure modes

**Table:** ICL theory comparison (theory, mechanism, evidence, limitations)

---

## Areas for Improvement

### Content Gaps
1. **Section 6.1:** No mention of PaLM, Falcon, or Bloom in the landmark models survey. These represent important milestones (PaLM for Pathways system, Falcon for open training data, Bloom for multilingual open science). A brief subsection or expanded table entry would improve coverage.
2. **Section 6.3:** The connection between scaling laws and inference cost is mentioned but not developed quantitatively. A worked example showing how over-training changes the cost-per-token at inference time would strengthen the practical value.
3. **Section 6.4:** No code example for quality filtering (heuristic or perplexity-based). The section describes these conceptually but the lab exercise references FineWeb tools without demonstrating them. A minimal filtering pipeline code example would complete the hands-on story.
4. **Section 6.5:** The WSD (warmup-stable-decay) learning rate schedule, used by recent models including Llama 3 and DeepSeek V3, is not mentioned. This is now arguably more important than cosine decay for practitioners.
5. **Section 6.6:** No discussion of sequence parallelism or context parallelism for long-context training. These are increasingly important (e.g., ring attention) and should be at least mentioned.
6. **Section 6.7:** No concrete experiment reproducing ICL-as-gradient-descent results. The code shows task vector extraction conceptually, but a minimal experiment training a small transformer on synthetic tasks and demonstrating the ICL gradient-descent correspondence would be highly valuable pedagogically.

### Weak Explanations
1. **Section 6.3:** The data-constrained scaling section is brief. It mentions repeating data but does not explain the Muennighoff et al. (2023) finding that up to 4 epochs of repetition has minimal degradation, or the value of data augmentation in this regime.
2. **Section 6.5:** Grokking is introduced but the connection to regularization and double descent is not drawn explicitly. Students may not understand why grokking matters for LLM training.
3. **Section 6.6:** Tensor parallelism is described abstractly (column vs. row splitting) but the actual math showing how matrix multiplication distributes across devices is not shown. A small worked example would clarify.

### Structural Issues
1. **CSS inconsistency:** Section 6.1 uses an expanded CSS style while sections 6.2 through 6.7 use a compressed single-line CSS format. This does not affect rendering but makes maintenance harder.
2. **Lab placement:** The lab exercises in sections 6.3, 6.4, and 6.6 are inline within the main content. A consistent "Lab" subsection at the end of each section (as done in Module 08 sections) would improve navigability.

---

## Terminology Standards

| Term | Standard Usage | Avoid |
|------|---------------|-------|
| Pre-training | "pre-training" (hyphenated) | "pretraining", "pre training" |
| Fine-tuning | "fine-tuning" (hyphenated) | "finetuning", "fine tuning" |
| Causal LM / CLM | "causal language modeling" or "CLM" | "autoregressive LM" (use only as synonym on first mention) |
| Masked LM / MLM | "masked language modeling" or "MLM" | "cloze task" (use only as historical note) |
| In-context learning / ICL | "in-context learning" or "ICL" | "few-shot learning" (not interchangeable; ICL includes zero-shot) |
| Scaling law | "scaling law" (lowercase) | "Scaling Law" (capitalize only in proper names like "Chinchilla scaling laws") |
| FLOP / FLOPs | "FLOPs" for floating-point operations (plural) | "FLOPS" (floating-point operations per second) |
| KV cache | "KV cache" (uppercase K, V) | "key-value cache" (use only on first mention for clarity) |
| Data parallelism / DDP | "data parallelism" or "DDP" | "DP" alone (ambiguous) |
| FSDP | "Fully Sharded Data Parallelism (FSDP)" on first mention | "ZeRO Stage 3" (related but not identical) |
| BF16 / FP16 | "BF16" and "FP16" (all caps) | "bfloat16" (use only on first explanation) |

---

## Cross-References

### Upstream (prerequisites from earlier modules)
- Module 00 (ML & PyTorch Foundations): training loops, gradient descent, optimizers, loss functions
- Module 02 (Tokenization): BPE, SentencePiece, vocabulary construction (referenced in data curation)
- Module 03 (Sequence Models & Attention): dot-product attention, cross-attention (foundation for Transformer)
- Module 04 (Transformer Architecture): self-attention, multi-head attention, feed-forward layers, positional encodings (core architecture assumed throughout)
- Module 05 (Decoding & Text Generation): autoregressive generation, sampling (referenced in CLM discussion)

### Downstream (modules that build on this one)
- Module 07 (Modern LLM Landscape): directly extends Section 6.1's model survey; references scaling laws and data curation decisions
- Module 08 (Inference Optimization): quantization and KV cache assume understanding of model architecture and precision formats from Section 6.6
- Module 13 (Fine-Tuning Fundamentals): pre-training objectives and optimizer knowledge are prerequisites
- Module 14 (PEFT): LoRA and adapter methods assume understanding of weight matrices and training dynamics
- Module 15 (Knowledge Distillation): scaling law understanding helps frame when distillation is preferable to training
- Module 16 (Alignment: RLHF, DPO): builds on InstructGPT discussion from Section 6.1
- Module 17 (Interpretability): in-context learning theory (Section 6.7) connects directly to mechanistic interpretability

---

## Estimated Total Word Count

| Section | Estimated Words |
|---------|----------------|
| 6.1 The Landmark Models | ~3,500 |
| 6.2 Pre-training Objectives | ~3,200 |
| 6.3 Scaling Laws | ~2,800 |
| 6.4 Data Curation | ~2,800 |
| 6.5 Optimizers & Training Dynamics | ~2,400 |
| 6.6 Distributed Training | ~3,000 |
| 6.7 In-Context Learning Theory | ~2,600 |
| **Total** | **~20,300** |

(Estimates based on HTML content line counts, excluding CSS/boilerplate, code blocks counted at reduced weight.)

---

## Narrative Arc

The module follows the journey of building a large language model from the ground up, organized as a progression from "what exists" to "how it works" to "what makes it possible."

**Opening hook (Section 6.1):** We begin with the landmarks, the models that changed the field. Students meet BERT, GPT, and T5 as characters in a story of escalating ambition. The question is established: how did we get from 110M parameters to hundreds of billions, and what did that unlock?

**The training recipe (Sections 6.2 and 6.3):** With the landscape in mind, we zoom into the two critical decisions: what objective to train on, and how much of everything (parameters, data, compute) to use. Section 6.2 gives students the ability to read any model paper and understand its training objective. Section 6.3 gives them the quantitative framework for understanding why models are the sizes they are.

**The raw materials (Section 6.4):** Data is the fuel. This section grounds the abstract scaling curves in the messy reality of web crawling, deduplication, and quality filtering. Students learn that data curation is as important as architecture design.

**The engine room (Sections 6.5 and 6.6):** With the recipe and raw materials in hand, we descend into the engineering of actually running the training. Optimizers determine whether training converges at all. Distributed training determines whether it finishes in a reasonable time. Together, these sections bridge theory and practice.

**The mystery (Section 6.7):** The module closes by returning to one of the most fascinating open questions: how do models learn from examples in the prompt without any weight updates? This section ties the pre-training story back to the practical capabilities that make LLMs useful, and sets the stage for Module 07's exploration of the modern model landscape and Module 10's treatment of prompt engineering.

The overall arc moves from historical survey to mathematical foundations to practical engineering to theoretical frontiers, giving students both the conceptual framework and the hands-on skills to understand modern LLM training.
