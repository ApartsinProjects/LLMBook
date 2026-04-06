# Chapter Plan: Module 04, The Transformer Architecture

## Scope

This is the central module of the entire course and the single most important chapter in Part I: Foundations. It covers the Transformer architecture end to end: conceptual understanding, hands-on implementation, the landscape of architectural variants, the GPU hardware that makes Transformers practical, and the theoretical limits of what Transformers can compute.

**In scope:**
- Complete walkthrough of the original "Attention Is All You Need" architecture
- Every building block: positional encoding, multi-head attention, feed-forward networks, residual connections, layer normalization, causal masking, weight initialization
- A from-scratch PyTorch implementation of a decoder-only Transformer (~300 lines)
- The three architectural families (encoder-only, decoder-only, encoder-decoder) and when to use each
- Efficient attention variants: sparse attention, linear attention, FlashAttention, MQA, GQA
- Post-Transformer alternatives and extensions: Mamba/SSMs, RWKV, Mixture-of-Experts, Gated Attention, Multi-head Latent Attention (MLA)
- GPU architecture fundamentals: SMs, memory hierarchy, roofline model, Triton programming
- Expressiveness theory: universal approximation, circuit complexity (TC0), limitations, chain-of-thought

**Not in scope (covered elsewhere):**
- Attention mechanism derivation from first principles (Module 03)
- Tokenization and vocabulary construction (Module 02)
- Decoding strategies, sampling, and beam search (Module 05)
- Distributed training and parallelism strategies (Module 08)
- Pre-training and fine-tuning procedures (Modules 07 and 09)
- Scaling laws (Module 06)

## Learning Objectives

1. Walk through the original Transformer paper and explain every component from positional encodings to output probabilities
2. Implement a complete decoder-only Transformer in ~300 lines of PyTorch, training it on a small dataset
3. Compare encoder-only, decoder-only, and encoder-decoder architectures with concrete use cases
4. Explain efficient attention mechanisms (linear attention, sparse attention, FlashAttention) and their tradeoffs
5. Describe State Space Models (SSMs/Mamba), Mixture-of-Experts (MoE), RWKV, Gated Attention, and Multi-head Latent Attention
6. Understand GPU architecture (SMs, memory hierarchy, bandwidth) and write a basic Triton kernel
7. State the universal approximation and computational complexity results for Transformers, and explain how chain-of-thought reasoning extends their power

## Prerequisites

Students should be comfortable with the following before starting this module:

- **Module 00 (ML Foundations):** PyTorch tensors, autograd, nn.Module, training loops, loss functions, optimizers
- **Module 01 (Language Representations):** Word embeddings, vector spaces, similarity measures
- **Module 02 (Tokenization):** How text becomes integer token IDs, vocabulary construction, BPE/SentencePiece
- **Module 03 (Sequence Models and Attention):** Dot-product attention, multi-head attention, KV caches, the motivation for replacing RNNs with attention
- **Math prerequisites:** Matrix multiplication, softmax, norms, basic probability, logarithms

Bridging needed: Section 4.1 opens by recapping multi-head attention from Module 03 before extending it to the full Transformer context. Section 4.4 assumes basic familiarity with computer memory concepts (caches, bandwidth) but teaches GPU specifics from scratch.

## Chapter Structure

### Section 4.1: Transformer Architecture Deep Dive (~4,500 words)
**Level:** Intermediate | **Type:** Fundamentals

- **Key concepts:**
  - Historical context of "Attention Is All You Need" (2017)
  - High-level encoder-decoder architecture overview
  - Token embeddings and embedding scaling
  - Sinusoidal positional encoding (derivation, intuition, frequency interpretation)
  - Learned positional embeddings
  - Scaled dot-product attention (recap from Module 03, reframed for Transformer context)
  - Multi-head attention: projection matrices, parallel heads, concatenation
  - Position-wise feed-forward network (two-layer MLP with ReLU/GELU)
  - Residual connections and the information-theoretic view
  - Layer normalization: Pre-LN vs. Post-LN tradeoffs
  - Weight initialization strategies (Xavier, scaled init for depth)
  - Causal mask for decoder self-attention
  - Complete forward pass walkthrough
  - Information flow through the residual stream
  - Parameter count formulas and example calculations

- **Diagrams needed:**
  1. Full Transformer architecture (encoder-decoder block diagram)
  2. Sinusoidal positional encoding heatmap (position vs. dimension)
  3. Multi-head attention data flow
  4. Pre-LN vs. Post-LN comparison
  5. Residual stream information flow
  6. Complete forward pass sequence

- **Code examples:**
  1. Sinusoidal positional encoding implementation (PyTorch)
  2. Positional encoding visualization snippet

- **Exercises:** 5 comprehension questions (quiz format with hidden answers)

### Section 4.2: Build a Transformer from Scratch (~4,000 words)
**Level:** Intermediate | **Type:** Engineering Lab

- **Key concepts:**
  - Design decisions for a decoder-only (GPT-style) model
  - Configuration dataclass for hyperparameters
  - Causal self-attention module: Q/K/V projections, masking, dropout
  - Feed-forward network module with GELU activation
  - Transformer block: attention + FFN + residual + LayerNorm
  - Full model assembly: embedding, N blocks, final LayerNorm, output projection
  - Weight tying between embedding and output projection
  - Character-level language modeling as a training task
  - Dataset preparation and batching
  - Training loop with learning rate scheduling (cosine warmup)
  - Shape tracking through every layer
  - Common bugs: mask shape errors, forgotten transpose, incorrect dimension ordering
  - Experiments to try: varying depth, width, context length, activation functions

- **Diagrams needed:**
  1. Model architecture schematic with tensor shapes annotated at every stage
  2. Training loss curve example

- **Code examples:**
  1. Configuration dataclass
  2. CausalSelfAttention class (~40 lines)
  3. FeedForward class (~15 lines)
  4. TransformerBlock class (~20 lines)
  5. GPTModel class (~50 lines)
  6. Dataset and DataLoader setup
  7. Training loop with logging
  8. Text generation / sampling function

- **Exercises:** 5 comprehension questions plus 4 suggested coding experiments

### Section 4.3: Transformer Variants and Efficiency (~4,000 words)
**Level:** Advanced | **Type:** Fundamentals (Survey)

- **Key concepts:**
  - Three architectural families: encoder-only (BERT), decoder-only (GPT), encoder-decoder (T5)
  - Positional encoding variants: RoPE (Rotary Position Embedding), ALiBi
  - Sparse attention patterns (local windows, strided, BigBird)
  - Linear attention (kernel-based approximations)
  - FlashAttention: tiling, IO-awareness, memory savings (high-level; algorithmic details in 4.4)
  - Multi-Query Attention (MQA) and Grouped-Query Attention (GQA)
  - State Space Models: S4 foundations, Mamba selective state spaces, Mamba-2 and the connection to attention
  - RWKV: linear attention reformulated as an RNN
  - Mixture-of-Experts: architecture, routing, load balancing, expert parallelism
  - Notable MoE models (Mixtral, Switch Transformer, DeepSeek)
  - Gated Linear Units and SwiGLU activation
  - Gated Attention Units
  - Multi-Head Latent Attention (MLA): low-rank key-value compression (DeepSeek-V2/V3)
  - Modern LLM recipe table: which components real models combine

- **Diagrams needed:**
  1. Three architectural families comparison (encoder-only, decoder-only, encoder-decoder)
  2. RoPE rotation visualization
  3. Sparse attention pattern diagrams
  4. FlashAttention tiling schematic (conceptual)
  5. MoE routing diagram
  6. MLA compression flow

- **Code examples:**
  1. RoPE implementation snippet
  2. GQA pseudocode
  3. Top-k gating for MoE (pseudocode)

- **Exercises:** 5 comprehension questions

### Section 4.4: GPU Fundamentals and Systems (~3,500 words)
**Level:** Advanced | **Type:** Engineering Lab

- **Key concepts:**
  - Why GPU architecture knowledge matters for LLM practitioners
  - Streaming Multiprocessors: CUDA cores, Tensor Cores, warp schedulers
  - Memory hierarchy: registers, shared memory/L1, L2 cache, HBM (bandwidth and latency at each level)
  - Compute-bound vs. memory-bound operations
  - The roofline model: arithmetic intensity, bandwidth ceiling, compute ceiling
  - Classifying Transformer operations on the roofline (matmuls vs. elementwise vs. reductions)
  - FlashAttention algorithm in detail: the tiling approach, online softmax, block-by-block accumulation
  - Introduction to Triton: programming model, block pointers, @triton.jit
  - Lab: vector addition in Triton
  - Lab: fused softmax kernel in Triton
  - Key GPU metrics: TFLOPS, memory bandwidth, utilization
  - Mixed precision training (FP16, BF16, FP8)
  - Memory budgeting: model parameters, optimizer states, activations, KV cache

- **Diagrams needed:**
  1. GPU memory hierarchy pyramid (registers through HBM)
  2. Roofline model plot with Transformer operations placed on it
  3. FlashAttention tiling visualization (outer loop over KV blocks, inner loop over Q blocks)
  4. Triton programming model schematic

- **Code examples:**
  1. Triton vector addition kernel
  2. Triton fused softmax kernel (~40 lines)
  3. Memory budget calculation example

- **Exercises:** 5 comprehension questions

### Section 4.5: Transformer Expressiveness Theory (~2,500 words)
**Level:** Advanced | **Type:** Fundamentals (Research-Oriented)

- **Key concepts:**
  - Universal approximation theorem for sequence-to-sequence functions (Yun et al., 2020)
  - Role of the FFN in universal approximation (attention alone is linear over values)
  - Transformers as circuit complexity models: connection to TC0 (threshold circuits of constant depth)
  - Log-precision assumption and its implications
  - Limitations of fixed-depth Transformers: inherently sequential computation, counting, state tracking
  - Graph reasoning difficulties
  - Chain-of-thought as additional computation steps (extending effective depth)
  - Why CoT helps on hard problems: converting parallel computation to serial
  - Implications for LLM design and prompting strategies
  - Open research questions: optimal depth vs. width, implicit chain-of-thought, learned computation graphs

- **Diagrams needed:**
  1. TC0 circuit depth illustration
  2. Chain-of-thought extending computation diagram (fixed-depth limitation vs. CoT workaround)

- **Code examples:** None (purely theoretical section)

- **Exercises:** 4 comprehension questions

## Terminology Standards

The following terms should be used consistently throughout the chapter:

| Term | Usage |
|------|-------|
| Transformer | Capitalized when referring to the architecture. Lowercase "transformer" only in non-technical contexts. |
| attention head | Lowercase. Not "Attention Head." |
| multi-head attention | Lowercase, hyphenated "multi-head." |
| feed-forward network (FFN) | Hyphenate "feed-forward." Abbreviation "FFN" after first use in each section. |
| residual connection | Not "skip connection" (use "residual connection" as the primary term; mention "skip connection" as a synonym once). |
| layer normalization (LayerNorm) | Spell out on first use, then "LayerNorm" is acceptable. |
| Pre-LN / Post-LN | Hyphenated with capital LN. |
| causal mask | Lowercase. Not "autoregressive mask." |
| KV cache | No hyphen. Stands for "key-value cache." |
| Streaming Multiprocessor (SM) | Capitalized. Abbreviation "SM" after first use. |
| High Bandwidth Memory (HBM) | Capitalized. Abbreviation "HBM" after first use. |
| roofline model | Lowercase. |
| FlashAttention | One word, capital F and A. |
| Mixture-of-Experts (MoE) | Hyphenated. Abbreviation "MoE" after first use. |
| State Space Model (SSM) | Capitalized. Abbreviation "SSM" after first use. |
| chain-of-thought (CoT) | Lowercase, hyphenated. Abbreviation "CoT" after first use. |
| RoPE | All caps except lowercase "o." Stands for "Rotary Position Embedding." |
| GQA / MQA | Grouped-Query Attention / Multi-Query Attention. |
| MLA | Multi-Head Latent Attention. |
| GELU / SwiGLU | Activation function names. Keep as written. |

## Cross-References

### Builds on:
- **Module 00 (ML Foundations):** PyTorch basics, training loops, loss functions, backpropagation
- **Module 01 (Language Representations):** Embedding spaces, word vectors, semantic similarity
- **Module 02 (Tokenization):** Token IDs, vocabulary, subword algorithms (BPE, SentencePiece)
- **Module 03 (Sequence Models and Attention):** Dot-product attention, multi-head attention, KV caches, motivation for leaving RNNs behind

### Referenced by:
- **Module 05 (Decoding and Text Generation):** Uses the Transformer forward pass as its starting point; extends with sampling strategies, temperature, top-k/top-p, beam search
- **Module 06 (Scaling Laws):** Relates model size (parameter counts from 4.1) to training compute and loss
- **Module 07 (Pre-training at Scale):** Assumes full understanding of the architecture; covers data pipelines, distributed training of the model built here
- **Module 08 (Distributed Systems):** Extends GPU knowledge from 4.4 to multi-GPU and multi-node parallelism (tensor parallel, pipeline parallel, FSDP)
- **Module 09 (Fine-tuning and Alignment):** Modifies the Transformer with LoRA adapters, prompt tuning; assumes fluency with the architecture
- **Module 10 (Inference and Serving):** Builds on KV cache, MQA/GQA, and GPU systems knowledge for efficient serving
- **Part II onwards:** Nearly every module references Module 04 as the architectural foundation

## Estimated Total Length

~18,500 words across all five sections. This is the largest module in the course, reflecting its central importance. Expected study time: 12 to 16 hours including the two labs (4.2 and 4.4).

## Production Notes

- Sections 4.1 and 4.2 are the core and should be polished to the highest standard. Every student will read these.
- Section 4.3 is a survey and should be comprehensive but not exhaustive. Each variant gets enough depth to understand the core idea and tradeoffs, with citations for readers who want more.
- Section 4.4 is a systems section that bridges theory and practice. The Triton labs are optional stretch goals but should be runnable.
- Section 4.5 is for advanced/research-oriented readers. It should be rigorous but accessible, avoiding unnecessary formalism. The practical takeaway (why CoT works) should be crystal clear even if the complexity theory details are skimmed.
