# Chapter Plan: Module 05, Decoding Strategies & Text Generation

## Scope

**What this chapter covers:**
This chapter is the bridge between a trained language model and the text it actually produces. It covers the full landscape of decoding algorithms, from the simplest deterministic methods through stochastic sampling, advanced techniques, and the emerging paradigm of diffusion-based language generation. Students learn not only the mechanics of each method but also when and why to choose one over another.

**What this chapter does NOT cover:**
- Training or fine-tuning language models (covered in Part II, Modules 06 and 08)
- The internal architecture of the Transformer (covered in Module 04)
- Prompt engineering or in-context learning (covered in Part III)
- Evaluation metrics for generated text beyond what is needed to motivate decoding choices (covered in Module 10)
- Reinforcement Learning from Human Feedback, except brief mention in the context of TraceRL for diffusion models (RLHF is covered in Module 08)

## Learning Objectives

1. Implement greedy decoding and beam search from scratch; explain their strengths and failure modes
2. Apply temperature scaling, top-k, top-p, and min-p sampling; visualize how each reshapes the token probability distribution
3. Explain repetition penalties, frequency penalties, and presence penalties, and when each is appropriate
4. Describe contrastive decoding, speculative decoding, and minimum Bayes risk decoding at both a conceptual and algorithmic level
5. Use grammar-constrained decoding to enforce structured output (JSON, XML) at the logit level
6. Explain the principles behind text watermarking and its implications for AI safety
7. Articulate how diffusion-based language models differ from autoregressive generation, including their advantages and current limitations

## Prerequisites

Students should have completed:
- **Module 00 (Mathematical Foundations):** Probability distributions, softmax, log-probabilities, entropy
- **Module 01 (NLP Fundamentals):** Tokenization, vocabulary, language model basics
- **Module 03 (Sequence Models & Attention):** Understanding of autoregressive generation and the attention mechanism
- **Module 04 (Transformer Architecture):** Decoder blocks, autoregressive masking, the forward pass of a decoder-only model
- **PyTorch basics:** Tensor operations, softmax, sampling from distributions

## Chapter Structure

### Section 5.1: Deterministic Decoding Strategies (~3,500 words)
**Level:** Intermediate | **Focus:** Engineering + Lab

- **Key concepts:**
  - The decoding problem (bridging model probabilities to generated text)
  - Greedy decoding: algorithm, strengths, failure modes (repetition loops, missed global optima)
  - Beam search: intuition, algorithm in detail, beam width trade-offs
  - Length normalization and length penalty
  - Constrained beam search (lexical constraints)
  - When to use deterministic decoding (translation, summarization, factual QA)

- **Diagrams needed:**
  - Figure 5.1: Greedy decoding search tree showing a locally optimal but globally suboptimal path
  - Figure 5.2: Beam search tree with beam width = 3, showing how multiple hypotheses are maintained

- **Code examples:**
  - Greedy decoding from scratch using raw logits (PyTorch)
  - Beam search implementation with score tracking
  - Lab: comparing greedy vs. beam search on a summarization task using HuggingFace

- **Exercises:** 3 quiz questions (multiple choice / short answer) plus 1 hands-on lab

---

### Section 5.2: Stochastic Sampling Methods (~3,500 words)
**Level:** Intermediate | **Focus:** Engineering + Lab

- **Key concepts:**
  - Pure random (ancestral) sampling and why it produces low-quality output
  - Temperature scaling: the math, intuition, and effect on distribution shape
  - Top-k sampling: truncate to k most likely tokens, then renormalize
  - Nucleus (top-p) sampling: dynamic vocabulary cutoff based on cumulative probability
  - Min-p sampling: a newer alternative that scales the threshold relative to the top token
  - Typical sampling (brief coverage)
  - Repetition penalty, frequency penalty, and presence penalty: formulas and use cases
  - Combining sampling methods: the typical temperature + top-p + min-p pipeline

- **Diagrams needed:**
  - Figure 5.3: Temperature effect on token probability distribution (already present as SVG)
  - Figure 5.4: Top-k vs. top-p truncation visualized on the same distribution

- **Code examples:**
  - Temperature scaling implementation
  - Top-k and top-p sampling functions
  - Min-p sampling function
  - Lab: interactive visualization of how each parameter reshapes distributions

- **Exercises:** 3 quiz questions plus 1 hands-on lab

---

### Section 5.3: Advanced Decoding & Structured Generation (~3,200 words)
**Level:** Advanced | **Focus:** Engineering

- **Key concepts:**
  - Contrastive decoding: expert minus amateur, plausibility filter, when it helps
  - Speculative decoding: using a small draft model to propose tokens, verified by the large model; guarantees identical output distribution
  - Grammar-constrained decoding: finite-state machines / pushdown automata applied to logit masking; JSON schema enforcement
  - Tools and libraries: Outlines, Guidance, llama.cpp grammars, vLLM structured output
  - Watermarking generated text: the Kirchenbauer et al. (2023) green/red list method; detection and implications for AI safety
  - Minimum Bayes Risk (MBR) decoding: sample many candidates, score pairwise, select the one closest to all others

- **Diagrams needed:**
  - Figure 5.5: Contrastive decoding (expert minus amateur probabilities)
  - Figure 5.6: Speculative decoding pipeline (draft, verify, accept/reject)
  - Grammar-constrained decoding state machine diagram

- **Code examples:**
  - Contrastive decoding implementation
  - Speculative decoding pseudocode / simplified implementation
  - Grammar-constrained JSON generation with Outlines (conceptual)
  - Watermarking: simplified green/red list demonstration
  - MBR decoding with ROUGE as the utility metric

- **Exercises:** 3 quiz questions

---

### Section 5.4: Diffusion-Based Language Models (~3,500 words)
**Level:** Advanced | **Focus:** Research

- **Key concepts:**
  - From continuous to discrete diffusion: why Gaussian noise does not work for text
  - Absorbing diffusion (mask corruption) vs. uniform diffusion (random replacement)
  - Forward process (corrupt) and reverse process (denoise)
  - Key models: MDLM, SEDD, LLaDA, Dream
  - Parallel generation: the speed advantage of unmasking multiple tokens per step
  - Gemini Diffusion: industry-scale diffusion LM and its reported performance
  - Advantages: parallelism, bidirectional context, flexible length, infilling
  - Limitations: quality gap for complex reasoning, lack of KV-cache equivalent, training costs
  - TraceRL: applying reinforcement learning to diffusion LLMs for reasoning tasks
  - The road ahead: hybrid architectures, scaling, and open questions

- **Diagrams needed:**
  - Figure 5.7: Discrete diffusion forward/reverse process (already present as SVG)
  - Figure 5.8: Parallel generation timeline comparing autoregressive vs. diffusion
  - Table comparing key diffusion LM models (MDLM, SEDD, LLaDA, Dream, Gemini Diffusion)

- **Code examples:**
  - Simplified discrete diffusion training loop (conceptual PyTorch)
  - Confidence-based parallel unmasking strategy
  - Comparison timing pseudocode (autoregressive vs. diffusion)

- **Exercises:** 3 quiz questions (conceptual and research-oriented)

---

## Terminology Standards

| Term | Usage Standard |
|------|---------------|
| **Decoding** | The process of selecting tokens from a model's output distribution to produce text. Not "inference" (which is broader). |
| **Logits** | The raw, unnormalized scores output by the model before softmax. Always plural. |
| **Beam width** (not "beam size") | The number of hypotheses maintained at each step of beam search. |
| **Temperature** | A scalar T that divides logits before softmax. Always written as T in math, "temperature" in prose. |
| **Nucleus sampling** | The formal name. Use "top-p sampling" as the parenthetical synonym on first mention, then either form freely. |
| **Min-p** | Always hyphenated. |
| **Speculative decoding** | Not "assisted generation" (though HuggingFace uses that term). Mention the HuggingFace name as an alias. |
| **Diffusion LM** / **Diffusion language model** | Preferred over "diffusion LLM" since these models are not yet at the "large" scale of autoregressive LLMs. |
| **Autoregressive** | One word, no hyphen. |
| **[MASK] token** | Use brackets and monospace when referring to the mask token in diffusion models. |

## Cross-References

### Builds on:
- **Module 00 (Mathematical Foundations):** Probability, softmax, entropy, KL divergence
- **Module 01 (NLP Fundamentals):** Tokenization, vocabulary, perplexity
- **Module 02 (Embeddings):** Token representations that feed into the decoder
- **Module 03 (Attention):** Autoregressive masking, the attention mechanism
- **Module 04 (Transformer Architecture):** Decoder blocks, the forward pass, KV cache (referenced in speculative decoding and diffusion LM limitations)

### Referenced by:
- **Module 06 (Pretraining & Scaling Laws):** Training objectives that produce the distributions we decode from
- **Module 07 (Tokenization Deep Dive):** Vocabulary size affects all sampling methods
- **Module 08 (RLHF & Alignment):** Alignment changes the distribution; decoding strategies interact with RLHF-tuned models
- **Module 10 (Evaluation):** Metrics like BLEU, ROUGE, and BERTScore that appear in MBR decoding
- **Module 14 (Inference & Serving):** Speculative decoding and KV cache optimizations at serving time
- **Part III (Prompt Engineering):** Practical guidance on temperature and sampling parameter selection

## Estimated Total Word Count

~13,700 words across the four sections, plus the index page. This places the chapter comfortably within the 8,000 to 15,000 word target.

## Narrative Arc

The chapter follows a clear progression:

1. **Start simple:** Greedy decoding is the easiest algorithm to understand and implement. It sets the stage by making the decoding problem concrete.
2. **Reveal the limitation:** Greedy search gets stuck in local optima. Beam search partially solves this, but both methods produce deterministic, often repetitive output.
3. **Introduce randomness:** Stochastic sampling methods let us control the quality/diversity trade-off. Temperature, top-k, top-p, and min-p each offer a different control knob.
4. **Go deeper:** Advanced techniques like contrastive decoding, speculative decoding, structured generation, and watermarking address specific real-world challenges.
5. **Look forward:** Diffusion-based language models challenge the entire autoregressive assumption and point toward the future of text generation.

This arc moves from foundational to frontier, from deterministic to stochastic, and from sequential to parallel, giving students both practical engineering skills and research-level understanding.
