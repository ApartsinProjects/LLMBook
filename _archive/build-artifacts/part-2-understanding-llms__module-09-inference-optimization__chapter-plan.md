# Chapter Plan: Module 08 - Inference Optimization & Efficient Serving

## Scope

**What this chapter covers:** The four pillars of making LLM inference fast and affordable: quantization (reducing weight precision with GPTQ, AWQ, bitsandbytes); KV cache and memory optimization (PagedAttention, GQA, prefix caching, continuous batching); speculative decoding (draft-verify paradigm, EAGLE, Medusa, token tree verification); and serving infrastructure (vLLM, SGLang, TGI, TensorRT-LLM, Ollama/llama.cpp, benchmarking methodology). Each section combines mathematical foundations with hands-on implementation.

**What this chapter does NOT cover:** Model training optimization or distributed training (Module 06, Section 6.6), model architecture design or pre-training (Module 06), fine-tuning for efficiency (Module 14, QLoRA), knowledge distillation as a compression technique (Module 15), or model deployment in production environments beyond the serving infrastructure itself (Module 26). While quantization-aware training is mentioned, the full treatment of training-time techniques belongs to earlier modules.

**Target audience:** Students who understand the Transformer architecture (Module 04), decoding strategies (Module 05), and the modern model landscape (Module 07, especially Llama, Mistral, and DeepSeek architectures). Students should be comfortable with GPU memory concepts and have basic experience with PyTorch and Hugging Face.

**Target length:** ~16,000 to 19,000 words across four sections.

---

## Learning Objectives

1. Explain the mathematics of absmax, zero-point, and per-group quantization; apply GPTQ, AWQ, and bitsandbytes to compress a 7B model to 4-bit.
2. Calculate KV cache memory requirements and explain how PagedAttention eliminates fragmentation.
3. Compare MHA, MQA, and GQA architectures and their effect on memory and throughput.
4. Describe prefix caching, continuous batching, TTT layers, and DeepSeek Sparse Attention.
5. Implement speculative decoding with rejection sampling and explain why it preserves the target distribution.
6. Compare EAGLE and Medusa approaches to self-speculative decoding.
7. Deploy and benchmark inference servers using vLLM, SGLang, TGI, and TensorRT-LLM.
8. Profile and optimize end-to-end latency (TTFT and TPS) under realistic workloads.

---

## Prerequisites

- Module 04 (Transformer Architecture): attention mechanism, multi-head attention, KV computation in self-attention
- Module 05 (Decoding Strategies): autoregressive generation, sampling methods, temperature, nucleus sampling
- Module 07 (Modern LLM Landscape): Llama, Mistral, DeepSeek architecture details, GQA, MoE
- Basic familiarity with GPU memory hierarchy and CUDA concepts (memory bandwidth, compute units, occupancy)
- Python, PyTorch, and Hugging Face Transformers library

---

## Detailed Section Structure

### Section 10.1: Model Quantization

**Key concepts:**
- Why inference is expensive: memory bandwidth bottleneck, arithmetic intensity analysis
- Quantization mathematics:
  - Absmax (symmetric) quantization: q = round(x / max|x| * (2^(n-1) - 1)), dequantization formula
  - Zero-point (asymmetric) quantization: shift + scale, useful when weight distributions are not centered
  - Granularity: per-tensor (coarsest), per-channel (moderate), per-group (finest, 32-128 elements)
- Data types: INT8, INT4, FP8 (E4M3 for forward, E5M2 for gradients), NF4 (normal-float, quantile-based, optimal for normally-distributed weights)
- Post-training quantization algorithms:
  - GPTQ: layer-wise Hessian-based optimal rounding, column-by-column quantization with error compensation
  - AWQ: activation-aware weight quantization, protecting salient channels that carry important activations
- Quantization in practice with bitsandbytes: 4-bit NF4 loading, double quantization for QLoRA
- GPTQ quantization with AutoGPTQ: calibration dataset, layer-by-layer processing
- AWQ quantization with autoawq: activation-aware channel scaling
- Calibration strategies: min/max, percentile, MSE-minimizing, cross-entropy-minimizing
- Quality degradation analysis: perplexity vs. bit width, task-specific sensitivity, outlier features
- Quantization-aware training: simulated quantization, straight-through estimator

**Diagrams present:**
- SVG: Quantization granularity visualization (per-tensor vs. per-channel vs. per-group)
- SVG: AWQ salient channel protection (how activation-aware scaling works)

**Code examples:**
- Loading a model in 4-bit NF4 with bitsandbytes (BitsAndBytesConfig, memory measurement)
- Quantizing a model with GPTQ (AutoGPTQ, calibration dataset, layer-wise quantization)
- Quantizing with AWQ (autoawq library, activation-aware scaling)
- Benchmarking quantization quality (perplexity, tokens/sec, memory across methods)

**Exercises:**
- Quiz: 5 questions on quantization math, NF4 advantages, GPTQ vs. AWQ tradeoffs, calibration

**Callouts:** Big Picture (opening), Key Insight (NF4 optimality, quality vs. speed frontier), Note (double quantization), Warning (outlier features causing quality degradation)

---

### Section 10.2: KV Cache & Memory Optimization

**Key concepts:**
- The KV cache explained: storing key/value tensors to avoid recomputation during autoregressive generation
- KV cache memory formula: 2 * layers * heads * seq_len * head_dim * dtype_size * batch_size
- Why inference is memory-bandwidth-bound: low arithmetic intensity during token generation
- PagedAttention: virtual memory analogy, block tables mapping logical to physical GPU memory, eliminating fragmentation, enabling memory sharing across sequences
- MHA vs. MQA vs. GQA: multi-head (full KV per head), multi-query (single shared KV), grouped-query (compromise, Llama 2/3 default)
- Prefix caching and RadixAttention: tree-based caching for shared prefixes, automatic prefix matching across requests
- Continuous batching: dynamically adding/removing sequences mid-batch, iteration-level scheduling vs. request-level
- KV cache compression techniques: INT8/INT4 quantization of cached values, H2O eviction (Heavy-Hitter Oracle), sliding window attention, StreamingLLM (attention sinks)
- Research frontiers:
  - Test-Time Training (TTT): compressing long context into model weights via next-token prediction at inference; 35x speedup over full attention at 2M context
  - DeepSeek Sparse Attention (DSA): hierarchical two-stage sparse attention, ~70% cost reduction for long contexts

**Diagrams present:**
- SVG: PagedAttention block table mapping (logical sequence to physical GPU blocks)
- SVG: Continuous batching timeline (requests entering and leaving a running batch)

**Code examples:**
- KV cache size calculator for various models (Llama 3 8B, 70B, 405B at different context lengths and batch sizes)
- Prefix caching demonstration with vLLM (cold vs. warm request latency)
- Profiling KV cache memory in vLLM (block sizes, utilization rates)

**Exercises:**
- Quiz: 5 questions on KV cache sizing, PagedAttention benefits, MQA/GQA tradeoffs, continuous batching

**Tables:**
- MHA vs. MQA vs. GQA comparison (KV heads, cache size, throughput, models using each)

**Callouts:** Big Picture (opening), Warning (KV cache can dominate memory), Key Insight (continuous batching throughput gains), Note (research vs. production readiness of TTT and DSA)

---

### Section 10.3: Speculative Decoding

**Key concepts:**
- The core principle: draft gamma tokens with a fast model, verify all gamma in one forward pass of the target model
- Mathematical guarantee: acceptance/rejection sampling preserves the target distribution exactly
- Acceptance criterion: accept draft token x with probability min(1, q(x)/p(x)) where q is target, p is draft
- Rejection and resampling: when rejected, sample from the adjusted distribution max(0, q(x) - p(x)) / sum
- Expected speedup analysis: E[accepted] = gamma * alpha / (1 - alpha) where alpha is acceptance rate
- Draft model strategies:
  - Separate small model: Llama-68M drafting for Llama-70B
  - Self-speculative (layer skipping): using a subset of the target model's own layers
  - N-gram lookup: drafting from prompt context via n-gram matching
  - Retrieval-based drafting: using retrieved text as draft candidates
- EAGLE (Efficient Autoregressive LLM Generation): feature-level autoregression predicting hidden states instead of tokens; tree-structured verification for parallel candidate evaluation
- Medusa: multiple prediction heads on top of the target model, each head predicts k-th future token independently; tree attention masks for batched verification
- Token tree verification: batched verification of multiple candidate branches in a single forward pass
- When speculative decoding helps vs. hurts: acceptance rate thresholds, latency-sensitive vs. throughput-sensitive workloads

**Diagrams present:**
- SVG: Speculative decoding workflow (draft, verify, accept/reject, resample)
- SVG: EAGLE tree-structured verification (branching candidates, parallel verification)

**Code examples:**
- Expected speedup computation for various acceptance rates and draft lengths
- Medusa-style multi-head prediction simulation (multiple heads, top-k per head)
- Speculative decoding with Hugging Face Transformers (assistant_model parameter)

**Exercises:**
- Quiz: 5 questions on acceptance probability, speedup conditions, EAGLE vs. Medusa, draft model selection

**Tables:**
- Draft model strategies comparison (method, memory overhead, acceptance rate, best for)
- Best vs. poor scenarios for speculative decoding

**Callouts:** Big Picture (opening), Key Insight (lossless acceleration guarantee, identical outputs), Warning (when speculative decoding hurts), Note (Medusa vs. EAGLE tradeoffs)

---

### Section 10.4: Serving Infrastructure

**Key concepts:**
- The serving stack: model loading, request scheduling, batching, inference engine, API layer
- vLLM: PagedAttention, continuous batching, OpenAI-compatible API, tensor parallelism; the de facto standard for research and production
- SGLang: RadixAttention for automatic prefix caching, constrained decoding, optimized for structured generation; advantages over vLLM for prefix-heavy workloads
- TGI (Text Generation Inference): Hugging Face's inference server, Docker-native, token streaming, watermarking, production-ready with monitoring
- TensorRT-LLM: NVIDIA's inference engine with hardware-level GPU optimization, FP8/INT4 kernel fusion, 30-50% higher throughput than vLLM at high concurrency
- LMDeploy: inference engine with TurboMind backend, competitive quantization support
- Ollama and llama.cpp: local inference, GGUF format, CPU/GPU hybrid, consumer hardware
- Triton Inference Server: NVIDIA's general-purpose inference server, model ensembles, dynamic batching
- Framework comparison across dimensions: throughput, latency, ease of use, quantization support, model compatibility
- Benchmarking methodology:
  - Latency metrics: TTFT (time to first token), TPOT (time per output token), end-to-end latency
  - Throughput metrics: tokens per second, requests per second, concurrent users
  - The latency-throughput tradeoff: higher concurrency improves throughput but increases per-request latency

**Diagrams present:**
- SVG: Serving stack layers (request to response flow)
- SVG: Benchmarking visualization (latency vs. concurrency curves)

**Code examples:**
- Launch vLLM server and benchmark throughput (server startup, concurrent request benchmark, metrics collection)
- Deploy TGI with Docker and query it (docker run, curl API, streaming)
- Local inference with Ollama (model pull, API interaction, benchmarking)
- Comprehensive benchmarking script (sweep concurrency levels, measure TTFT/TPOT/throughput)

**Exercises:**
- Quiz: 5 questions on framework selection, benchmarking methodology, latency-throughput tradeoffs

**Lab exercise:** Deploy vLLM and TGI side by side; benchmark throughput and latency under load at multiple concurrency levels

**Tables:**
- Framework comparison matrix (vLLM, SGLang, TGI, TensorRT-LLM, LMDeploy, Ollama, llama.cpp, Triton with features)

**Callouts:** Big Picture (opening), Note (choosing between vLLM and SGLang), Key Insight (local vs. cloud tradeoffs, latency-throughput tradeoff), Warning (benchmarking pitfalls)

---

## Areas for Improvement

### Content Gaps
1. **Section 10.1:** No discussion of GGUF format and its mixed-precision quantization strategy (different bit widths for different layers). This is the dominant format for local inference via llama.cpp and Ollama, and students will encounter it immediately in practice.
2. **Section 10.1:** Missing coverage of dynamic quantization (quantizing activations on the fly during inference) vs. static quantization (precomputing activation scales). This distinction matters for deployment decisions.
3. **Section 10.2:** No worked example demonstrating the memory savings of GQA over MHA numerically. A concrete calculation (e.g., "Llama 3 8B with GQA uses X GB KV cache vs. Y GB with full MHA") would make the comparison tangible.
4. **Section 10.2:** The H2O eviction policy and sliding window attention compression are mentioned but not explained in detail. Students need to understand when each technique is appropriate and the quality tradeoffs.
5. **Section 10.3:** No from-scratch implementation of speculative decoding. The section references the Hugging Face `assistant_model` API but does not walk through the draft-verify-resample loop manually. A pedagogical implementation (even on a toy model) would dramatically improve understanding.
6. **Section 10.3:** Missing discussion of speculative decoding in the MoE context. With MoE models like Mixtral and DeepSeek V3 becoming prevalent, students should understand how expert routing interacts with speculative verification.
7. **Section 10.4:** No coverage of model serving on Apple Silicon (MLX framework). Given the growing number of developers using MacBooks, this is a practical gap.
8. **Section 10.4:** Missing discussion of cost optimization strategies: spot instances, auto-scaling, model caching across cold starts, and the economics of self-hosted vs. API-based inference.

### Weak Explanations
1. **Section 10.1:** The GPTQ algorithm description is at the right level of detail, but the Hessian computation and its approximation are glossed over. A brief note explaining that the Hessian captures weight sensitivity (second-order information) would help students who lack optimization background.
2. **Section 10.2:** The TTT (Test-Time Training) explanation is too brief for such a novel concept. Students may confuse it with fine-tuning. A clearer distinction (TTT happens during inference, not as a separate training step) and a simple diagram would help.
3. **Section 10.3:** The mathematical proof that speculative decoding preserves the target distribution is not shown. While the Key Insight callout states this guarantee, walking through the probability argument (even informally) would satisfy curious students and prevent misconceptions.
4. **Section 10.4:** The TensorRT-LLM section lacks a code example. Unlike vLLM, TGI, and Ollama, there is no runnable example. Even a Docker-based deployment example would improve parity.

### Structural Issues
1. **Section ordering tension:** Section 10.1 (quantization) and 8.2 (KV cache) could arguably be read in either order, but the current ordering works because quantization concepts (data types, precision) are referenced in KV cache compression. However, a brief forward reference in 8.1 noting that quantization applies to KV caches too (not just weights) would strengthen the connection.
2. **Lab distribution:** Sections 8.1 and 8.4 have the strongest lab exercises. Section 10.2's lab is described in the syllabus but is less prominent in the content. Section 10.3's lab (implementing speculative decoding from scratch) is referenced in the syllabus but the section content only shows the Hugging Face API approach.
3. **Redundancy with Module 07:** Section 10.2 discusses GQA and MLA, which are also covered in Section 7.2 (DeepSeek V3 deep dive). The overlap is intentional (different perspective: architecture in 7.2, memory optimization in 8.2) but should be explicitly acknowledged to avoid confusion.

---

## Terminology Standards

| Term | Standard Usage | Avoid |
|------|---------------|-------|
| Quantization | "quantization" (lowercase) | "Quantization" (capitalize only at sentence start) |
| Post-training quantization / PTQ | "post-training quantization (PTQ)" on first mention | "weight-only quantization" (subset of PTQ) |
| KV cache | "KV cache" (uppercase K, V) | "key-value cache" (use only on first mention) |
| PagedAttention | "PagedAttention" (one word, camel case) as coined by vLLM | "Paged Attention" or "paged attention" |
| TTFT | "time to first token (TTFT)" on first mention | "first-token latency" (use only as informal synonym) |
| TPOT | "time per output token (TPOT)" on first mention | "inter-token latency" (use only as informal synonym) |
| TPS | "tokens per second (TPS)" on first mention | "tok/s" (use only in tables/code output) |
| GQA | "Grouped-Query Attention (GQA)" on first mention | "grouped query attention" (capitalize as proper noun) |
| MQA | "Multi-Query Attention (MQA)" on first mention | "multi query attention" |
| GPTQ | "GPTQ" (all caps, no expansion needed; name is well-established) | "GPT Quantization" (incorrect expansion) |
| AWQ | "Activation-Aware Weight Quantization (AWQ)" on first mention | "activation aware quantization" |
| NF4 | "NF4 (Normal Float 4-bit)" on first mention | "normal float" alone (always include "4-bit") |
| Speculative decoding | "speculative decoding" (lowercase) | "Speculative Decoding" (capitalize only at sentence start) |
| Draft model / target model | "draft model" and "target model" | "small model" / "large model" (imprecise) |
| vLLM | "vLLM" (lowercase v, uppercase LLM) | "VLLM" or "Vllm" |
| SGLang | "SGLang" (capital S, G, L) | "sglang" or "SgLang" |

---

## Cross-References

### Upstream (prerequisites from earlier modules)
- Module 00 (ML & PyTorch Foundations): GPU concepts, training loops, tensor operations
- Module 04 (Transformer Architecture): self-attention computation, KV pairs in attention, multi-head attention (essential for understanding KV cache and quantization targets)
- Module 05 (Decoding Strategies): autoregressive generation loop, sampling methods (the baseline that speculative decoding improves upon)
- Module 06 (Pre-training): mixed precision training (FP16/BF16/FP8 from Section 6.6 directly informs quantization), distributed training (tensor parallelism reappears in serving)
- Module 07 (Modern LLM Landscape): GQA in Llama (Section 7.2), MLA in DeepSeek V3 (Section 7.2), MoE routing (relevant to serving efficiency)

### Downstream (modules that build on this one)
- Module 09 (Working with LLM APIs): serving infrastructure from Section 10.4 is what backs the APIs students learn to use
- Module 14 (PEFT): QLoRA combines NF4 quantization (Section 10.1) with LoRA fine-tuning
- Module 15 (Knowledge Distillation): distillation as alternative to quantization for model compression
- Module 19 (RAG): retrieval-augmented generation depends on fast inference for the generation component
- Module 20 (Conversational AI): multi-turn conversation serving depends on prefix caching (Section 10.2) and continuous batching
- Module 26 (Production Deployment): serving infrastructure from Section 10.4 is the foundation for production systems

---

## Estimated Total Word Count

| Section | Estimated Words |
|---------|----------------|
| 8.1 Model Quantization | ~4,500 |
| 8.2 KV Cache & Memory Optimization | ~4,200 |
| 8.3 Speculative Decoding | ~4,000 |
| 8.4 Serving Infrastructure | ~5,000 |
| **Total** | **~17,700** |

(Estimates based on HTML content line counts, excluding CSS/boilerplate, code blocks counted at reduced weight.)

---

## Narrative Arc

The module tells the story of making LLM inference practical, following the natural flow of optimization from the model itself outward to the serving system.

**The weight problem (Section 10.1):** We open with the blunt reality: a 70B-parameter model at full precision requires over 140 GB of GPU memory. Quantization is the first and most impactful optimization, because it directly shrinks the model. Students learn the mathematics behind compression (how to map a float to 4 bits without destroying the model) and gain hands-on experience quantizing real models. The section establishes the fundamental tradeoff between precision and efficiency that runs through the entire module.

**The memory wall (Section 10.2):** With weights compressed, the next bottleneck reveals itself: the KV cache. Every generated token adds to a growing memory burden, and naive management wastes GPU memory through fragmentation. PagedAttention solves this elegantly by borrowing ideas from operating systems. Students learn to calculate cache sizes, understand why inference is memory-bandwidth-bound (not compute-bound), and see how architectural choices like GQA and techniques like prefix caching unlock dramatically higher throughput.

**Breaking the sequential bottleneck (Section 10.3):** Even with a small model and efficient memory, autoregressive decoding is inherently sequential: one token at a time. Speculative decoding breaks this bottleneck by drafting multiple tokens cheaply and verifying them in parallel. The mathematical guarantee (identical outputs to the unoptimized model) makes this technique uniquely appealing. Students implement the draft-verify loop and explore advanced variants like EAGLE and Medusa.

**Putting it all together (Section 10.4):** The final section assembles all previous optimizations into production-ready serving systems. Students deploy real inference servers, benchmark them under load, and learn to measure what matters (TTFT, TPS, throughput at various concurrency levels). The section closes with the latency-throughput tradeoff, teaching students that optimization is always about choosing the right point on a curve for their specific use case.

The overall arc follows the natural optimization cascade: compress the model, optimize the memory, parallelize the computation, and build the serving system. Each section both builds on the previous one and motivates the next, creating a coherent journey from raw model weights to a production inference endpoint.
