# Part I: Foundations, Curriculum Alignment Report

**Reviewer:** Curriculum Alignment Agent
**Date:** 2026-03-26
**Scope:** All 6 modules in Part I (Modules 00 through 05)
**Method:** Cross-referenced each chapter plan and every HTML section against the master syllabus (index.html), checking for coverage, depth, sequencing, prerequisite handling, and scope creep.

---

## Module 00: ML & PyTorch Foundations

### Coverage Assessment

All four syllabus sections are delivered as complete HTML files:

- **Section 0.1** covers features, supervised learning, loss functions, gradient descent (SGD, mini-batch), overfitting/underfitting, regularization (L1, L2, dropout), bias-variance tradeoff, cross-validation, and model selection. **Full coverage.**
- **Section 0.2** covers perceptrons, MLPs, activation functions, backpropagation, batch normalization, dropout, weight initialization, a CNN overview, and training best practices (LR scheduling, early stopping, gradient clipping). **Full coverage.**
- **Section 0.3** is a comprehensive PyTorch tutorial: tensors, autograd, nn.Module, Dataset/DataLoader, training loops, saving/loading models, debugging (hooks, profiling), and a FashionMNIST lab. **Full coverage.**
- **Section 0.4** covers the RL framework (agent, environment, state, action, reward), policies, value functions, Bellman equation, policy gradients, PPO, and the explicit bridge to LLM training (RLHF). **Full coverage.**

### Depth Assessment

All sections are tagged Basic in the syllabus and deliver at that level. The content assumes only Python and basic math; no prior ML experience is required. The depth is appropriate: concepts are explained with analogies and worked examples before formalisms.

One minor over-depth observation: Section 0.2's CNN overview and Section 0.4's PPO discussion go slightly beyond what is strictly needed for later modules. However, both are clearly scoped as "overview" material and do not demand deep understanding, so this is acceptable scope enrichment rather than scope creep.

### Sequencing Issues

None. The progression from ML basics (0.1) to deep learning (0.2) to PyTorch hands-on (0.3) to RL (0.4) is logical. Section 0.4 correctly forward-references Module 16 for RLHF/DPO.

### Gaps Found

1. **No explicit "course roadmap" in Module 00.** The syllabus description for Module 01, Section 1.1 lists "Course roadmap and project overview" as a topic. It might be more natural in Module 00's index page. Currently, Module 00's index page does not provide a bird's-eye view of the full course arc.
2. **NumPy coverage is implicit.** The chapter plan for Module 01 lists "Familiarity with NumPy" as a prerequisite from Module 00. Section 0.3 uses NumPy in passing but does not offer a dedicated NumPy refresher. This is a minor gap since the audience is assumed to have Python experience.

### Recommendations (priority-ordered)

1. **[Low]** Add a brief "What Lies Ahead" paragraph to the Module 00 index page to orient students to the full Part I arc.
2. **[Low]** Add 2 to 3 NumPy examples in Section 0.3 (array creation, slicing, broadcasting) before the PyTorch tensor section, since later modules use NumPy directly (e.g., Section 1.3 uses numpy for cosine similarity).

**Overall Alignment: STRONG**

---

## Module 01: Foundations of NLP & Text Representation

### Coverage Assessment

All four sections map directly to their syllabus entries:

- **Section 1.1** covers the four eras of NLP, the core NLP task taxonomy, and why language is hard. **Mostly covered.** The syllabus lists an extremely detailed task taxonomy (8 sub-categories: text classification, sequence labeling, text generation, QA, information extraction, semantic tasks, conversational AI, plus "how LLMs are changing each task"). The delivered section covers six core tasks at a higher level and does not break out all sub-categories individually. The sub-items like "event detection," "slot filling," and "natural language inference" are not explicitly named.
- **Section 1.2** covers preprocessing (Unicode normalization, stop words, stemming, lemmatization), BoW, TF-IDF, n-grams, and one-hot encoding. **Partial gap.** The syllabus specifies "TF-IDF in depth: term frequency saturation, inverse document frequency weighting, document length normalization, vector space model for retrieval." The delivered section covers the standard TF-IDF formula and a worked example but does not address TF saturation (BM25-style sublinear TF), document length normalization, or the vector space model for retrieval.
- **Section 1.3** covers the distributional hypothesis, Word2Vec (CBOW, Skip-gram, negative sampling), GloVe, FastText, cosine similarity, word analogies, t-SNE, and UMAP. **Full coverage.**
- **Section 1.4** covers the polysemy problem, ELMo, contextual embeddings with BERT code, the pre-train/fine-tune paradigm, and forward references. **Full coverage.**

### Depth Assessment

Sections 1.1 through 1.3 are tagged Basic and deliver at that level. Section 1.4 is tagged Intermediate, which is appropriate since it assumes understanding of LSTMs (introduced conceptually here, formalized in Module 03). The GloVe section is notably lighter than Word2Vec (concept + one code snippet vs. full architecture walkthrough + training lab). The chapter plan itself flags this imbalance.

### Sequencing Issues

1. **Section 1.1 does not explicitly bridge from Module 00.** The chapter plan notes this gap. There is no sentence like "In Module 00 you built neural networks; now we apply them to language." This is a minor but real orientation issue for students arriving from Module 00.
2. **Section 1.4 uses BERT code** to demonstrate contextual embeddings rather than ELMo code. This is a practical choice (ELMo libraries are deprecated), but the section should note more prominently that BERT is formally covered in Module 04/Part II.

### Gaps Found

1. **Syllabus topic gap: detailed NLP task taxonomy.** The syllabus promises sub-categories (relation extraction, event detection, slot filling, extractive vs. abstractive summarization, open-domain QA, NLI, etc.) that are not individually covered.
2. **Syllabus topic gap: TF-IDF depth.** Term frequency saturation, document length normalization, and the vector space model for retrieval are absent.
3. **Exercise distribution.** All exercises are consolidated in Section 1.4. Sections 1.1, 1.2, and 1.3 have only inline quick-checks. This is flagged in the chapter plan itself.

### Recommendations (priority-ordered)

1. **[Medium]** Expand Section 1.2's TF-IDF coverage to include sublinear TF scaling (the `1 + log(tf)` variant), document length normalization, and a brief mention of the vector space model for retrieval. This is explicitly promised in the syllabus.
2. **[Medium]** Expand Section 1.1's NLP task taxonomy to mention (even briefly) the sub-categories the syllabus lists: slot filling, relation extraction, NLI, extractive vs. abstractive summarization.
3. **[Low]** Add 1 to 2 short exercises at the end of Sections 1.1, 1.2, and 1.3 instead of concentrating all exercises in Section 1.4.
4. **[Low]** Add a one-sentence bridge from Module 00 at the start of Section 1.1.
5. **[Low]** Balance GloVe coverage with a brief worked example of the co-occurrence matrix or a code snippet comparing GloVe and Word2Vec analogy performance.

**Overall Alignment: ADEQUATE** (two syllabus promises are under-delivered)

---

## Module 02: Tokenization & Subword Models

### Coverage Assessment

All three sections deliver their syllabus topics:

- **Section 2.1** covers the vocabulary tradeoff, context window impact, multilingual "token tax," cost arithmetic, and tokenization artifacts (inconsistent splitting, arithmetic failures, trailing spaces, code tokenization). **Full coverage.**
- **Section 2.2** covers BPE (algorithm, merge table, encoding), WordPiece (likelihood-based merging, MaxMatch), Unigram (top-down pruning, Viterbi decoding), byte-level BPE, ByT5, and MegaByte. A full BPE from-scratch lab is included. **Full coverage.** Minor note: the syllabus mentions "merge tree data structure" and "O(n log n) encoding complexity" in its detailed BPE internals; the section covers the merge table but does not explicitly formalize it as a "merge tree" or state the complexity bound.
- **Section 2.3** covers special tokens, ChatML and Llama 3 chat templates, `apply_chat_template`, multilingual fertility analysis lab, multimodal tokenization (image patches, audio codecs), API cost estimation, and a head-to-head tokenizer comparison lab. **Full coverage.**

### Depth Assessment

Section 2.1 is tagged Basic and delivers appropriately. Sections 2.2 and 2.3 are tagged Intermediate, which is correct. The BPE from-scratch lab is well-calibrated for the audience. The Unigram/Viterbi section is the densest part and may benefit from a more explicit step-by-step walkthrough for readers unfamiliar with dynamic programming.

### Sequencing Issues

None. The progression from "why tokenization matters" to "algorithms" to "practical usage" is logical. Forward references to Module 03 (token embeddings as input to attention) and Module 04 (embedding layers sized to vocabulary) are present in the chapter plan.

### Gaps Found

1. **Syllabus detail gap: BPE merge tree and complexity.** The syllabus explicitly states "merge tree data structure maps byte sequences to token IDs with O(n log(n)) encoding complexity." The delivered Section 2.2 describes the merge table but does not formalize the tree structure or state the complexity bound.
2. **Syllabus detail gap: "Comparing tokenizers" tools.** The syllabus lists "tiktoken (Rust/Python, fast), Hugging Face tokenizers (Rust core), SentencePiece (C++)" as a comparison topic in Section 2.2. The delivered section focuses on the algorithms rather than the library ecosystem comparison. The head-to-head lab in Section 2.3 partially covers this, but a brief "library landscape" paragraph in Section 2.2 would close the gap.

### Recommendations (priority-ordered)

1. **[Medium]** Add a brief subsection or callout in Section 2.2 explaining the merge tree data structure and stating the encoding complexity bound, as promised in the syllabus.
2. **[Low]** Add a 2 to 3 paragraph "Tokenizer Libraries" subsection in Section 2.2 comparing tiktoken, Hugging Face tokenizers, and SentencePiece as implementations.
3. **[Low]** Consider adding a diagram or step-by-step numeric example for Viterbi decoding in the Unigram section to make it more accessible to students without dynamic programming background.

**Overall Alignment: STRONG** (minor detail gaps, nothing structural)

---

## Module 03: Sequence Models & the Attention Mechanism

### Coverage Assessment

All three sections are fully delivered:

- **Section 3.1** covers the sequence modeling problem, vanilla RNN cell, BPTT, vanishing/exploding gradients, LSTM, GRU, bidirectional RNNs, the encoder-decoder architecture, the information bottleneck, the parallelism problem, and a seq2seq translation model. **Full coverage.** The section even adds "The Parallelism Problem" (Section 7) which, while not in the syllabus, provides good motivation for attention.
- **Section 3.2** covers the "where to look" intuition, Bahdanau additive attention, Luong dot-product attention, attention as soft alignment, attention as a differentiable dictionary lookup, backpropagation through attention (Jacobian of softmax, gradient flow through context vector), and integration into seq2seq. **Full coverage.**
- **Section 3.3** covers Q/K/V abstraction, scaled dot-product attention, why scale by sqrt(d_k), softmax temperature, self-attention vs. cross-attention, causal masking, multi-head attention, the MultiHeadSelfAttention lab, and O(n^2) complexity analysis. **Full coverage.**

### Depth Assessment

Section 3.1 is tagged Basic and delivers at that level. Sections 3.2 and 3.3 are tagged Intermediate with Lab components, which is appropriate. The backpropagation through attention subsection in 3.2 (Jacobian of softmax, gradient flow) is on the higher end of intermediate but matches the syllabus's explicit request for this content.

### Sequencing Issues

1. **Section 3.1's "Parallelism Problem" (subsection 7)** is not in the syllabus but is valuable. It is clearly scope enrichment, not scope creep, since it motivates why attention (and later, Transformers) replaced RNNs.
2. **Cross-reference to Module 01 is well handled.** Section 3.1 bridges from Module 01 by showing how embedding vectors become x_t inputs to the RNN.

### Gaps Found

No significant gaps found. All syllabus topics are covered at appropriate depth.

### Recommendations (priority-ordered)

1. **[Low]** The exercises are all quiz-format (self-check questions). Consider adding one small coding exercise per section (e.g., "modify the LSTM cell code to remove the forget gate and observe the effect on gradient flow").
2. **[Low]** The chapter plan mentions verifying the MultiHeadSelfAttention implementation against PyTorch's `nn.MultiheadAttention`. The delivered section does not include this verification step. Adding a brief comparison code block would strengthen the lab.

**Overall Alignment: STRONG**

---

## Module 04: The Transformer Architecture

### Coverage Assessment

All five sections are fully delivered and represent the largest module in Part I:

- **Section 4.1** covers the original paper context, high-level architecture, token embeddings, sinusoidal positional encoding, learned positional embeddings, multi-head attention (recap from Module 03), FFN with GELU/SwiGLU, residual connections, layer normalization (Pre-LN vs. Post-LN), weight initialization, causal mask, complete forward pass, residual stream information flow, and parameter count formulas. **Mostly covered.** See gaps below.
- **Section 4.2** is a from-scratch decoder-only Transformer lab with configuration dataclass, CausalSelfAttention, FeedForward (with SwiGLU variant), TransformerBlock, GPTModel, data preparation, training loop, shape tracking, and debugging tips. **Full coverage.**
- **Section 4.3** covers encoder-only/decoder-only/encoder-decoder families, RoPE, ALiBi, sparse attention, linear attention, FlashAttention, MQA, GQA, S4, Mamba, Mamba-2, RWKV, MoE (routing, load balancing, notable models), GLU/SwiGLU, Gated Attention Units, MLA, and a "Modern LLM Recipes" comparison table. **Full coverage** of a massive topic list.
- **Section 4.4** covers GPU architecture (SMs, memory hierarchy), roofline model, FlashAttention algorithm (tiling, online softmax), Triton introduction with vector addition and fused softmax labs, GPU metrics, mixed precision, and memory budgeting. **Full coverage.**
- **Section 4.5** covers universal approximation, TC^0 circuit complexity, Transformer limitations (sequential computation, counting, graph reasoning), chain-of-thought extending computation, and open questions. **Full coverage.**

### Depth Assessment

Section 4.1 is tagged Intermediate, Section 4.2 is Intermediate/Lab, Section 4.3 is Advanced, Section 4.4 is Advanced/Lab, and Section 4.5 is Advanced/Research. Depth levels are well-calibrated. The module is ambitious (estimated 18,500 words) but earns its length as the central module of the course.

### Sequencing Issues

1. **Section 4.1 discusses RoPE briefly** (mentioning it as a "modern approach") but the full RoPE treatment is in Section 4.3. This is appropriate since 4.1 focuses on the original architecture.
2. **Section 4.2's implementation uses learned positional embeddings** (`nn.Embedding`) rather than RoPE, while the syllabus for Section 4.2 says "Token embeddings + RoPE positional encoding." This is a mismatch between the syllabus promise and the delivered content. The lab uses the simpler learned embeddings for pedagogical clarity, which is reasonable, but the syllabus should be updated to match, or the lab should be updated to use RoPE.

### Gaps Found

1. **Syllabus topic gap: Section 4.1 missing information theory block.** The syllabus promises a dedicated information theory subsection covering "entropy as the theoretical lower bound on compression; cross-entropy loss is an upper bound on true entropy; perplexity = 2^(cross-entropy); KL divergence; mutual information." The delivered section has a brief "information-theoretic view" callout in the residual connections subsection but does not deliver the full information theory treatment. This is a significant gap.
2. **Syllabus topic gap: Section 4.1 missing loss function coverage.** The syllabus lists "Loss function: cross-entropy for next-token prediction, label smoothing, auxiliary losses." These are not covered in 4.1 (cross-entropy appears in 4.2's training loop but without the theoretical framing).
3. **Syllabus topic gap: Section 4.1 missing activation function ablation.** The syllabus lists "Activation functions: ReLU to GELU to SwiGLU: ablation evidence and why SwiGLU wins." Section 4.1 mentions SwiGLU in a callout but does not provide ablation evidence or a comparison.
4. **Syllabus vs. content mismatch: Section 4.2 positional encoding.** See sequencing issues above.
5. **Syllabus topic gap: Section 4.3 missing encoder-decoder deep dive.** The syllabus promises "Encoder-decoder deep dive: cross-attention mechanism, T5 text-to-text framework, BART denoising pre-training, seq2seq fine-tuning" in detail. Section 4.3 covers encoder-decoder at a survey level (brief subsection) without this deep dive.

### Recommendations (priority-ordered)

1. **[High]** Add a dedicated information theory subsection to Section 4.1 covering entropy, cross-entropy, perplexity, KL divergence, and mutual information as the syllabus promises. These concepts are foundational and referenced throughout later modules.
2. **[High]** Add a loss function subsection to Section 4.1 covering cross-entropy for next-token prediction, label smoothing, and auxiliary losses.
3. **[Medium]** Either update Section 4.2's implementation to use RoPE (with a code snippet and explanation) or update the syllabus to say "learned positional embeddings" to match reality. If the former, include the RoPE code alongside the learned embeddings so students see both.
4. **[Medium]** Expand the activation function coverage in Section 4.1 with a brief comparison table (ReLU vs. GELU vs. SwiGLU) including reported ablation results.
5. **[Medium]** Expand Section 4.3's encoder-decoder coverage to at least briefly discuss the T5 text-to-text framework and BART denoising objectives, since these are explicitly listed in the syllabus.
6. **[Low]** Add the "computational complexity" research-tagged content from the syllabus (Fine-Grained Complexity, SETH implications) as a brief mention in Section 4.3 or 4.5.

**Overall Alignment: ADEQUATE** (information theory and loss function gaps are notable; several syllabus promises are under-delivered)

---

## Module 05: Decoding Strategies & Text Generation

### Coverage Assessment

All four sections are fully delivered:

- **Section 5.1** covers the decoding problem, greedy decoding (algorithm, strengths, failure modes), beam search (algorithm, beam width tradeoffs), length normalization, constrained beam search, when to use deterministic decoding, and a greedy-vs-beam lab. **Full coverage.**
- **Section 5.2** covers pure random sampling, temperature scaling, top-k, top-p (nucleus), min-p, typical sampling, repetition/frequency/presence penalties, combining methods, and a visualization lab. **Full coverage.**
- **Section 5.3** covers contrastive decoding, speculative decoding, grammar-constrained decoding (FSMs, JSON schema, Outlines/Guidance/llama.cpp/vLLM), watermarking (green/red list method), and MBR decoding. **Mostly covered.** See gaps below.
- **Section 5.4** covers discrete diffusion (absorbing vs. uniform), key models (MDLM, SEDD, LLaDA, Dream), parallel generation, Gemini Diffusion, advantages/limitations, TraceRL, and the road ahead. **Full coverage.**

### Depth Assessment

Sections 5.1 and 5.2 are tagged Intermediate, which is appropriate. Section 5.3 is tagged Advanced, and Section 5.4 is Advanced/Research. Depth calibration is good throughout.

### Sequencing Issues

1. **Speculative decoding is intentionally scoped as an introduction** with a forward reference to Module 08 (Inference Optimization) for full depth. This is a good design choice.
2. **Prerequisites are well handled.** The chapter assumes Module 04's decoder forward pass and autoregressive masking, which are available.

### Gaps Found

1. **Syllabus topic gap: Classifier-free guidance for language models.** The syllabus explicitly lists "Classifier-free guidance for language models" as a research-tagged topic in Section 5.3. This is absent from the delivered HTML.
2. **Syllabus topic gap: Eta sampling.** The syllabus lists "Typical decoding and eta sampling" for Section 5.2. The delivered section covers typical sampling but does not mention eta sampling.
3. **Minor: Speculative decoding code.** The chapter plan calls for "pseudocode / simplified implementation." The delivered section provides a conceptual explanation with a diagram but the actual code implementation appears to be a simplified pseudocode block rather than a full runnable implementation. This matches the chapter plan's intent but is lighter than some other labs.

### Recommendations (priority-ordered)

1. **[Medium]** Add a subsection on classifier-free guidance for language models in Section 5.3. This is a research-tagged topic explicitly listed in the syllabus.
2. **[Low]** Add a brief paragraph on eta sampling in Section 5.2 (it can be treated as a variant of typical sampling with additional filtering).
3. **[Low]** Consider adding a runnable speculative decoding demo (even a simplified one with a small draft model) to make the concept more concrete.

**Overall Alignment: STRONG** (one missing syllabus topic, otherwise comprehensive)

---

## Cross-Module Summary: Part I Systemic Issues

### 1. Information Theory Gap (High Priority)

The syllabus promises a substantial information theory block in Module 04, Section 4.1 (entropy, cross-entropy, perplexity, KL divergence, mutual information). This is not delivered. These concepts are referenced throughout Part II and beyond (scaling laws use perplexity, evaluation uses cross-entropy, alignment uses KL divergence). This is the single most impactful gap in Part I.

**Recommendation:** Add a dedicated subsection in Section 4.1 or create a new short subsection in Module 00 as mathematical background.

### 2. Syllabus Detail Inflation

The syllabus (index.html) contains more detailed sub-topics than the chapter plans, especially for Modules 01 and 04. For example, the syllabus lists extremely granular NLP task sub-categories (slot filling, event detection, NLI) and deep TF-IDF internals (saturation, length normalization) that are not reflected in the chapter plans or delivered content. This suggests the syllabus was expanded after the content was written, or aspirational detail was added without corresponding content updates.

**Recommendation:** Audit the syllabus against delivered content module by module and either (a) add the missing content or (b) simplify the syllabus to match what is actually delivered. Consistency between promise and delivery is critical for student trust.

### 3. Exercise Distribution Pattern

Multiple modules concentrate exercises at the end of the final section rather than distributing them across sections. This pattern appears in Modules 01, 03, and 04. Modules 02 and 05 do better, with check-your-understanding quizzes at the end of each section.

**Recommendation:** Standardize on the Module 02/05 pattern: each section gets its own quiz block. This reinforces learning before students move to the next topic.

### 4. Prerequisite Bridging Inconsistency

Some modules bridge well from their predecessors (Module 03 explicitly references Module 01 embeddings), while others skip the bridge (Module 01 does not reference Module 00). A consistent opening paragraph referencing prior modules would improve the learning flow.

**Recommendation:** Add a one to two sentence bridge at the top of each module's first section referencing what students learned in the previous module and how it connects.

### 5. CSS Styling Inconsistency (Minor)

Module 00's four sections use three different CSS styling approaches (Section 0.1 uses a chapter-header gradient style; Sections 0.2 through 0.4 use a simpler nav-bar style). This does not affect content but creates visual inconsistency.

**Recommendation:** Standardize the CSS template across all sections in Module 00.

### 6. Section 4.2 Positional Encoding Mismatch

The syllabus says Section 4.2's lab uses "Token embeddings + RoPE positional encoding," but the delivered code uses learned positional embeddings (`nn.Embedding`). This is a factual mismatch between promise and delivery.

**Recommendation:** Either update the lab to implement RoPE or update the syllabus to say "learned positional embeddings."

### Priority Summary

| Priority | Issue | Modules Affected |
|----------|-------|-----------------|
| High | Information theory subsection missing from 4.1 | 04 |
| High | Loss function coverage missing from 4.1 | 04 |
| Medium | Syllabus vs. content detail mismatches | 01, 02, 04, 05 |
| Medium | Classifier-free guidance missing from 5.3 | 05 |
| Medium | Section 4.2 positional encoding mismatch | 04 |
| Low | Exercise distribution across sections | 01, 03, 04 |
| Low | Prerequisite bridging inconsistency | 00, 01 |
| Low | CSS styling inconsistency in Module 00 | 00 |
