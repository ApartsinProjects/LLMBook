# Content Duplicates Audit

Read-only audit of repeated / near-duplicate prose across LLMBook sections.
Generated: 2026-05-19 17:47:45 (branch: v2.0)

## Executive Summary

- **Sections indexed**: 386
  (skipped 57 sections under `tools-of-the-trade` / appendices)
- **Total prose shingles** (~3-sentence windows): 38158
- **Average shingles / section**: 98.9
- **Candidate section-pair flags**: 30
  - HIGH severity (likely copy-paste): 9
  - MED severity (significant overlap): 7
  - LOW severity (thematic overlap): 14

**Where duplication concentrates**:

- `section-N.Ma.html` <-> `section-N.Mb.html` **split-sibling pairs**:
  16 of 30 flagged pairs.
  These are sections that were split in half during the v2.0 length
  rebalance and share the original intro/recap prose.
- Cross-module candidates: 2.

**Headline finding**: prose duplication is *structurally localised*. Almost all
high-overlap pairs are the planned `a`/`b` split-section siblings, which
intentionally share a Big-Picture / setup paragraph. There is no evidence of
substantial copy-paste across unrelated parts of the book.

**Methodology** (read-only):

1. Walked all `part-*/module-*/section-*.html` files.
2. Stripped HTML, code blocks, captions, callouts, epigraphs, bibliographies,
   prerequisites/what-comes-next boilerplate, math/figures.
3. Extracted only `<p>` prose >= 60 chars.
4. Tokenised into ~3-sentence shingles (25-180 tokens each).
5. Hashed each shingle (sha1, 16 hex chars).
6. **Exact hits**: shingles whose sha1 appears in 2+ sections.
7. **Near-dups**: TF-IDF cosine (1-2 grams, stop-words removed) >= 0.30
   plus per-shingle token-set Jaccard >= 0.7.
8. Ranked by a severity score combining exact-hit count, longest run of
   consecutive duplicates, near-dup count, cosine score, and a cross-part bonus.
9. Filtered out boilerplate fragments ("This section assumes...", "Big
   Picture" callouts, etc.) to keep signal on real prose duplication.

**Skipped (per audit spec):**

- `module-*-tools-of-the-trade/*` (intentionally repeats short library blurbs)
- `part-12-appendices/*` (bibliographies, glossary, reading lists)
- Within-page boilerplate (`.prerequisites`, `.what-comes-next`,
  `.learning-goals`, `.epigraph`, `.bibliography`, `.reading-list`,
  `.author-card`, `.agent-card`, code blocks, figure captions, tables, math)

## Top 30 Candidate Section Pairs

Ranked by severity (exact-hit count + longest-run weight + cosine + cross-part bonus).
Each row: severity bucket, both file paths, key metrics, example duplicate shingle,
and a recommendation.

Legend:

- **exact**: identical sha1 shingles shared (after boilerplate filter)
- **run**: longest consecutive run of duplicate shingles in section A order
- **near**: token-set Jaccard >= 0.7 shingle pairs (sampled)
- **J**: section-level shingle Jaccard
- **cos**: TF-IDF cosine between the full prose of both sections
- **xp**: cross-part flag (TRUE = different Parts -- more suspicious)

### 1. [HIGH] part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html  vs  part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html

- **severity**: 295.87  | **exact**: 48  | **run**: 45  | **near**: 56  | **J**: 0.193  | **cos**: 0.587  | **xp**: False
- **recommendation**: MERGE-OR-EXTRACT
- **example duplicate shingle**:

  > Beta too low: the model exploits reward model weaknesses, producing adversarial outputs that score high on the reward model but are not actually helpful (reward hacking). Typical beta: 0.01 to 0.2. Describe the reward hacking problem in RLHF.
- **best near-dup pair** (Jaccard 1.00):

  - A> RLHF is the technique that turned GPT-3 into ChatGPT. A pretrained language model can generate fluent text, but it has no notion of helpfulness, safety, or user intent. RLHF introduces human judgment into the training loop: annotators compare model outputs, those comparisons train a reward model, and reinforcement learning steers the policy toward higher-reward behavior.
  - B> RLHF is the technique that turned GPT-3 into ChatGPT. A pretrained language model can generate fluent text, but it has no notion of helpfulness, safety, or user intent. RLHF introduces human judgment into the training loop: annotators compare model outputs, those comparisons train a reward model, and reinforcement learning steers the policy toward higher-reward behavior.

### 2. [HIGH] part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.6.html  vs  part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.7.html

- **severity**: 269.13  | **exact**: 43  | **run**: 40  | **near**: 53  | **J**: 0.267  | **cos**: 0.713  | **xp**: False
- **recommendation**: MERGE-OR-EXTRACT
- **example duplicate shingle**:

  > Actions: acknowledge the frustration ("I understand this is frustrating"), simplify the response, offer to escalate to a human agent, and reduce response verbosity. Explain how native speech-to-speech models (like GPT-4o voice) differ from the traditional STT-LLM-TTS pipeline. What advantages do they offer in terms of latency and expressiveness?
- **best near-dup pair** (Jaccard 1.00):

  - A> Voice is the most natural human interface, and multimodal AI is making it programmable. The convergence of high-quality speech recognition ( Whisper , Deepgram), expressive text-to-speech (ElevenLabs, Cartesia), and real-time orchestration frameworks (LiveKit, Pipecat) has made it possible to build voice-first conversational AI that feels responsive and natural. Combined with v...
  - B> Voice is the most natural human interface, and multimodal AI is making it programmable. The convergence of high-quality speech recognition ( Whisper , Deepgram), expressive text-to-speech (ElevenLabs, Cartesia), and real-time orchestration frameworks (LiveKit, Pipecat) has made it possible to build voice-first conversational AI that feels responsive and natural. Combined with v...

### 3. [HIGH] part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html  vs  part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.6.html

- **severity**: 239.01  | **exact**: 38  | **run**: 36  | **near**: 46  | **J**: 0.229  | **cos**: 0.701  | **xp**: False
- **recommendation**: MERGE-OR-EXTRACT
- **example duplicate shingle**:

  > Build an IVF index with 256 clusters on 500,000 random vectors. Measure recall@10 and query time as you sweep nprobe from 1 to 128. Plot the recall/latency tradeoff curve.
- **best near-dup pair** (Jaccard 1.00):

  - A> Finding the most similar vectors in a collection of millions is a computational challenge that brute-force search cannot solve at scale. Approximate Nearest Neighbor (ANN) algorithms trade a small amount of accuracy for dramatic speedups, enabling sub-millisecond search over billions of vectors. Understanding the internals of HNSW, IVF, and Product Quantization is essential for...
  - B> Finding the most similar vectors in a collection of millions is a computational challenge that brute-force search cannot solve at scale. Approximate Nearest Neighbor (ANN) algorithms trade a small amount of accuracy for dramatic speedups, enabling sub-millisecond search over billions of vectors. Understanding the internals of HNSW, IVF, and Product Quantization is essential for...

### 4. [HIGH] part-2-understanding-llms/module-09-inference-optimization/section-9.1.html  vs  part-2-understanding-llms/module-09-inference-optimization/section-9.3.html

- **severity**: 51.29  | **exact**: 9  | **run**: 6  | **near**: 9  | **J**: 0.036  | **cos**: 0.329  | **xp**: False
- **recommendation**: MERGE-OR-EXTRACT
- **example duplicate shingle**:

  > That exceeds the capacity of even the largest single GPU (the A100 has 80 GB, the H100 has 80 GB). Quantization compresses weights from 16-bit or 32-bit floating point down to 8-bit, 4-bit, or even lower precision integers. A 4-bit quantized 70B model fits in roughly 35 GB, making it servable on a single GPU.
- **best near-dup pair** (Jaccard 1.00):

  - A> Why quantize? A 70B-parameter model stored in FP16 requires approximately 140 GB of GPU memory just for the weights. That exceeds the capacity of even the largest single GPU (the A100 has 80 GB, the H100 has 80 GB).
  - B> Why quantize? A 70B-parameter model stored in FP16 requires approximately 140 GB of GPU memory just for the weights. That exceeds the capacity of even the largest single GPU (the A100 has 80 GB, the H100 has 80 GB).

### 5. [HIGH] part-4-training-adaptation/module-17-peft/section-17.5.html  vs  part-4-training-adaptation/module-17-peft/section-17.7.html

- **severity**: 38.04  | **exact**: 6  | **run**: 4  | **near**: 8  | **J**: 0.027  | **cos**: 0.404  | **xp**: False
- **recommendation**: MERGE-OR-EXTRACT
- **example duplicate shingle**:

  > Knowledge distillation is the art of making small models behave like large ones. A 70B-parameter teacher model contains vast knowledge but is expensive to serve. By training a smaller student model to mimic the teacher's output distribution (not just its final answers), the student can inherit much of the teacher's capability at a fraction of the inference cost.
- **best near-dup pair** (Jaccard 1.00):

  - A> Knowledge distillation is the art of making small models behave like large ones. A 70B-parameter teacher model contains vast knowledge but is expensive to serve. By training a smaller student model to mimic the teacher's output distribution (not just its final answers), the student can inherit much of the teacher's capability at a fraction of the inference cost.
  - B> Knowledge distillation is the art of making small models behave like large ones. A 70B-parameter teacher model contains vast knowledge but is expensive to serve. By training a smaller student model to mimic the teacher's output distribution (not just its final answers), the student can inherit much of the teacher's capability at a fraction of the inference cost.

### 6. [HIGH] part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.7.html  vs  part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.8.html

- **severity**: 34.78  | **exact**: 5  | **run**: 3  | **near**: 10  | **J**: 0.027  | **cos**: 0.378  | **xp**: False
- **recommendation**: CONSOLIDATE
- **example duplicate shingle**:

  > Chat template standardization is an ongoing challenge. Different model families (Llama, Mistral, ChatML, Claude) use different special token conventions. Multimodal tokenization (handling images, audio, and video alongside text) is a rapidly evolving area, with models like GPT-4o and Gemini 2.0 using vision encoders that produce "visual tokens" interleaved with text tokens.
- **best near-dup pair** (Jaccard 1.00):

  - A> Tokenizer fertility is a fairness issue. Users of languages that tokenize inefficiently pay more per API call, get less context per request, and experience slower inference. Building on the BPE and Unigram algorithms from Section 1.6 , fertility differences arise directly from how training corpora shape the merge rules.
  - B> Tokenizer fertility is a fairness issue. Users of languages that tokenize inefficiently pay more per API call, get less context per request, and experience slower inference. Building on the BPE and Unigram algorithms from Section 1.6 , fertility differences arise directly from how training corpora shape the merge rules.

### 7. [HIGH] part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.5.html  vs  part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.6.html

- **severity**: 28.55  | **exact**: 4  | **run**: 4  | **near**: 5  | **J**: 0.021  | **cos**: 0.355  | **xp**: False
- **recommendation**: CONSOLIDATE
- **example duplicate shingle**:

  > The key insight is mathematical: the optimal policy under the RLHF objective has a closed-form relationship with the reward function. This can be implemented efficiently using parameter-efficient methods like LoRA . This means you can reparameterize the reward model loss directly in terms of the policy, training the language model on preference pairs using a simple classification-like objective.
- **best near-dup pair** (Jaccard 1.00):

  - A> DPO achieves RLHF-level alignment without reinforcement learning. The key insight is mathematical: the optimal policy under the RLHF objective has a closed-form relationship with the reward function. This can be implemented efficiently using parameter-efficient methods like LoRA .
  - B> DPO achieves RLHF-level alignment without reinforcement learning. The key insight is mathematical: the optimal policy under the RLHF objective has a closed-form relationship with the reward function. This can be implemented efficiently using parameter-efficient methods like LoRA .

### 8. [HIGH] part-2-understanding-llms/module-09-inference-optimization/section-9.7.html  vs  part-2-understanding-llms/module-09-inference-optimization/section-9.8.html

- **severity**: 27.0  | **exact**: 4  | **run**: 4  | **near**: 7  | **J**: 0.018  | **cos**: 0.0  | **xp**: False
- **recommendation**: CONSOLIDATE
- **example duplicate shingle**:

  > A trained model is just a collection of tensors on disk. Turning it into a responsive, scalable API requires specialized serving infrastructure that handles continuous batching, KV cache management, request scheduling, model parallelism, and hardware-specific kernel optimization. For production deployment patterns and safety considerations, see Chapter 47 .
- **best near-dup pair** (Jaccard 1.00):

  - A> From model weights to production endpoint. A trained model is just a collection of tensors on disk. Turning it into a responsive, scalable API requires specialized serving infrastructure that handles continuous batching, KV cache management, request scheduling, model parallelism, and hardware-specific kernel optimization.
  - B> From model weights to production endpoint. A trained model is just a collection of tensors on disk. Turning it into a responsive, scalable API requires specialized serving infrastructure that handles continuous batching, KV cache management, request scheduling, model parallelism, and hardware-specific kernel optimization.

### 9. [HIGH] part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html  vs  part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.4.html

- **severity**: 24.0  | **exact**: 4  | **run**: 4  | **near**: 4  | **J**: 0.019  | **cos**: 0.0  | **xp**: False
- **recommendation**: CONSOLIDATE
- **example duplicate shingle**:

  > In Section 2.2 , we used attention to let a decoder peek at encoder states. The Transformer (Vaswani et al., 2017) takes this much further. It introduces the query/key/value (Q/K/V) abstraction, scales the dot products by √ for numerical stability, runs multiple attention "heads" in parallel, and applies attention not just between encoder and decoder but also within a single sequence (self-attention).
- **best near-dup pair** (Jaccard 1.00):

  - A> From seq2seq attention to the Transformer's attention. In Section 2.2 , we used attention to let a decoder peek at encoder states. The Transformer (Vaswani et al., 2017) takes this much further.
  - B> From seq2seq attention to the Transformer's attention. In Section 2.2 , we used attention to let a decoder peek at encoder states. The Transformer (Vaswani et al., 2017) takes this much further.

### 10. [MED] part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.5.html  vs  part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.6.html

- **severity**: 23.24  | **exact**: 3  | **run**: 2  | **near**: 7  | **J**: 0.019  | **cos**: 0.324  | **xp**: False
- **recommendation**: CONSOLIDATE
- **example duplicate shingle**:

  > Enterprise data is a goldmine that most teams leave buried. Every production LLM system generates logs: user queries, model responses, latency traces, tool invocations, and feedback signals. These raw artifacts contain exactly the signal needed for fine-tuning, evaluation, and preference alignment, but only if you can transform them into properly formatted, validated, and balanced datasets.
- **best near-dup pair** (Jaccard 1.00):

  - A> Enterprise data is a goldmine that most teams leave buried. Every production LLM system generates logs: user queries, model responses, latency traces, tool invocations, and feedback signals. These raw artifacts contain exactly the signal needed for fine-tuning, evaluation, and preference alignment, but only if you can transform them into properly formatted, validated, and balan...
  - B> Enterprise data is a goldmine that most teams leave buried. Every production LLM system generates logs: user queries, model responses, latency traces, tool invocations, and feedback signals. These raw artifacts contain exactly the signal needed for fine-tuning, evaluation, and preference alignment, but only if you can transform them into properly formatted, validated, and balan...

### 11. [MED] part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html  vs  part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html

- **severity**: 21.02  | **exact**: 3  | **run**: 3  | **near**: 3  | **J**: 0.016  | **cos**: 0.302  | **xp**: False
- **recommendation**: CONSOLIDATE
- **example duplicate shingle**:

  > It costs one extra LLM call (use a cheap, fast model) and requires no changes to your index or embeddings. Step-back prompting (Zheng et al., 2023) generates a more abstract or general version of the query before retrieval. For example, the query "What was the GDP growth rate of Japan in Q3 2024?" might be stepped back to "What are the recent economic trends in Japan?" The broader query retrieves documents that provide necessary background context, which is then combined with results from the specific query. compares these three query transformation strategies.
- **best near-dup pair** (Jaccard 1.00):

  - A> Multi-query expansion is the single easiest advanced technique to implement and typically boosts recall by 10 to 20%. If you only have time for one improvement to your naive RAG pipeline, start here. It costs one extra LLM call (use a cheap, fast model) and requires no changes to your index or embeddings.
  - B> Multi-query expansion is the single easiest advanced technique to implement and typically boosts recall by 10 to 20%. If you only have time for one improvement to your naive RAG pipeline, start here. It costs one extra LLM call (use a cheap, fast model) and requires no changes to your index or embeddings.

### 12. [MED] part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html  vs  part-1-llm-building-blocks/module-03-transformer-architecture/section-3.6.html

- **severity**: 21.0  | **exact**: 4  | **run**: 2  | **near**: 5  | **J**: 0.016  | **cos**: 0.0  | **xp**: False
- **recommendation**: CONSOLIDATE
- **example duplicate shingle**:

  > This section is a coding lab. By the end you will have a working character-level language model built on a decoder-only Transformer. Every line of code is explained.
- **best near-dup pair** (Jaccard 1.00):

  - A> Reading about attention heads and layer normalization is one thing; implementing them is another. This hands-on lab translates the architecture from Section 3.1 into working PyTorch code, building a character-level language model step by step. By the end, you will have internalized how data flows through embeddings, multi-head attention, and feed-forward layers.
  - B> Reading about attention heads and layer normalization is one thing; implementing them is another. This hands-on lab translates the architecture from Section 3.1 into working PyTorch code, building a character-level language model step by step. By the end, you will have internalized how data flows through embeddings, multi-head attention, and feed-forward layers.

### 13. [MED] part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html  vs  part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html

- **severity**: 18.0  | **exact**: 3  | **run**: 3  | **near**: 3  | **J**: 0.011  | **cos**: 0.0  | **xp**: False
- **recommendation**: CONSOLIDATE
- **example duplicate shingle**:

  > The Transformer's core insight is that attention alone, applied across all pairs of positions simultaneously, can capture dependencies of arbitrary range without the vanishing gradient problem that plagues RNNs. As we saw in Section 2.3 , multi-head self-attention provides the mechanism; this section assembles it into a complete architecture. The cost is quadratic in sequence length, a tradeoff that later sections of this module will address.
- **best near-dup pair** (Jaccard 1.00):

  - A> The first sub-section is an information-theory primer (entropy, cross-entropy, KL divergence). If you already know these or just want the transformer mechanics, skip to Scaled Dot-Product Attention. The Transformer's core insight is that attention alone, applied across all pairs of positions simultaneously, can capture dependencies of arbitrary range without the vanishing gradi...
  - B> The first sub-section is an information-theory primer (entropy, cross-entropy, KL divergence). If you already know these or just want the transformer mechanics, skip to Scaled Dot-Product Attention. The Transformer's core insight is that attention alone, applied across all pairs of positions simultaneously, can capture dependencies of arbitrary range without the vanishing gradi...

### 14. [MED] part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.2.html  vs  part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.4.html

- **severity**: 13.65  | **exact**: 1  | **run**: 1  | **near**: 5  | **J**: 0.006  | **cos**: 0.365  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **example duplicate shingle**:

  > In Temporal, state lives in the Temporal server's event history, and your workers are stateless. In LangGraph, state lives in the checkpointer database, and your application server manages the graph execution. In Inngest, state lives in Inngest's managed platform, and your function code is stateless.
- **best near-dup pair** (Jaccard 1.00):

  - A> In Temporal, state lives in the Temporal server's event history, and your workers are stateless. In LangGraph, state lives in the checkpointer database, and your application server manages the graph execution. In Inngest, state lives in Inngest's managed platform, and your function code is stateless.
  - B> In Temporal, state lives in the Temporal server's event history, and your workers are stateless. In LangGraph, state lives in the checkpointer database, and your application server manages the graph execution. In Inngest, state lives in Inngest's managed platform, and your function code is stateless.

### 15. [MED] part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html  vs  part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html

- **severity**: 12.0  | **exact**: 2  | **run**: 2  | **near**: 2  | **J**: 0.008  | **cos**: 0.0  | **xp**: False
- **recommendation**: CONSOLIDATE
- **example duplicate shingle**:

  > Although their weights and training details remain proprietary, frontier closed-source models set the benchmark for what is possible with large language models. Understanding their capabilities, architectural hints, and positioning helps practitioners choose the right tool for each task, anticipate where the field is headed, and recognize the gap (or lack thereof) between proprietary and open alternatives. Building on the historical model lineage from Section 6.1 , this section maps the landscape as of early 2025, with notes on rapidly evolving developments.
- **best near-dup pair** (Jaccard 1.00):

  - A> Why study closed-source models? Although their weights and training details remain proprietary, frontier closed-source models set the benchmark for what is possible with large language models. Understanding their capabilities, architectural hints, and positioning helps practitioners choose the right tool for each task, anticipate where the field is headed, and recognize the gap...
  - B> Why study closed-source models? Although their weights and training details remain proprietary, frontier closed-source models set the benchmark for what is possible with large language models. Understanding their capabilities, architectural hints, and positioning helps practitioners choose the right tool for each task, anticipate where the field is headed, and recognize the gap...

### 16. [MED] part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.5.html  vs  part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.6.html

- **severity**: 9.0  | **exact**: 1  | **run**: 1  | **near**: 4  | **J**: 0.006  | **cos**: 0.0  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **example duplicate shingle**:

  > Short-term memory (covered in Section 37.3 ) keeps the current conversation coherent. Long-term memory is what lets a system carry knowledge across sessions, weeks, and months: vector stores that retrieve old context by meaning, user profiles that accumulate stable preferences, self-managing architectures like MemGPT/Letta where the LLM itself decides what to remember, and memory-as-a-service platforms that package all of this behind an API. This section ties those pieces together, compares them, shows how to consolidate and evaluate them, and closes with a hands-on lab that wires short-term a...
- **best near-dup pair** (Jaccard 1.00):

  - A> Short-term memory (covered in Section 37.3 ) keeps the current conversation coherent. Long-term memory is what lets a system carry knowledge across sessions, weeks, and months: vector stores that retrieve old context by meaning, user profiles that accumulate stable preferences, self-managing architectures like MemGPT/Letta where the LLM itself decides what to remember, and memo...
  - B> Short-term memory (covered in Section 37.3 ) keeps the current conversation coherent. Long-term memory is what lets a system carry knowledge across sessions, weeks, and months: vector stores that retrieve old context by meaning, user profiles that accumulate stable preferences, self-managing architectures like MemGPT/Letta where the LLM itself decides what to remember, and memo...

### 17. [LOW] part-15-llm-agentic-ai-research-frontiers/module-76-frontier-theory/section-76.3.html  vs  part-2-understanding-llms/module-10-interpretability/section-10.2.html

- **severity**: 8.52  | **exact**: 0  | **run**: 0  | **near**: 0  | **J**: 0.0  | **cos**: 0.352  | **xp**: True
- **recommendation**: KEEP-BOTH (likely intentional)

### 18. [LOW] part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html  vs  part-2-understanding-llms/module-09-inference-optimization/section-9.9.html

- **severity**: 8.27  | **exact**: 0  | **run**: 0  | **near**: 0  | **J**: 0.0  | **cos**: 0.327  | **xp**: True
- **recommendation**: KEEP-BOTH (likely intentional)
- **best near-dup pair** (Jaccard 0.45):

  - A> Writing GPU kernels in CUDA requires managing threads, warps, shared memory, synchronization, and memory coalescing at a low level. Triton (developed at OpenAI) provides a higher-level abstraction: you write kernels in a Python-like language that operates on blocks of data rather than individual threads. Triton handles the complex details of thread mapping, shared memory manage...
  - B> Triton, developed by OpenAI, lets you write GPU kernels in Python with a programming model centered on block-level operations . Unlike CUDA, where you think in terms of individual threads, Triton operates on tiles (blocks) of data. The compiler handles thread scheduling, memory coalescing, and shared memory management automatically.

### 19. [LOW] part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html  vs  part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.5.html

- **severity**: 6.67  | **exact**: 0  | **run**: 0  | **near**: 3  | **J**: 0.0  | **cos**: 0.367  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **best near-dup pair** (Jaccard 0.97):

  - A> An eval suite that is not refreshed with production samples becomes stale within weeks. Schedule a recurring task (weekly for high-traffic products, monthly for lower-traffic ones) to sample 50 to 100 production interactions, label them for quality, and merge them into your golden set. This single practice prevents the most common failure mode in production AI: a green eval das...
  - B> An eval suite that is not refreshed with production samples becomes stale within weeks. Schedule a recurring task (weekly for high-traffic products, monthly for lower-traffic ones) to sample 50 to 100 production interactions, label them for quality, and merge them into your golden set. This single practice prevents the most common failure mode: a green eval dashboard that no lo...

### 20. [LOW] part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html  vs  part-1-llm-building-blocks/module-03-transformer-architecture/section-3.7.html

- **severity**: 6.0  | **exact**: 1  | **run**: 1  | **near**: 1  | **J**: 0.003  | **cos**: 0.0  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **example duplicate shingle**:

  > This section dives deeper into a topic that is not strictly required for the rest of the book. Readers who are time-constrained can skim or skip on first pass and return when they need the specific details. The next section assumes only what was covered in the earlier sections of this chapter.
- **best near-dup pair** (Jaccard 1.00):

  - A> This section dives deeper into a topic that is not strictly required for the rest of the book. Readers who are time-constrained can skim or skip on first pass and return when they need the specific details. The next section assumes only what was covered in the earlier sections of this chapter.
  - B> This section dives deeper into a topic that is not strictly required for the rest of the book. Readers who are time-constrained can skim or skip on first pass and return when they need the specific details. The next section assumes only what was covered in the earlier sections of this chapter.

### 21. [LOW] part-1-llm-building-blocks/module-03-transformer-architecture/section-3.7.html  vs  part-1-llm-building-blocks/module-03-transformer-architecture/section-3.7.html

- **severity**: 6.0  | **exact**: 1  | **run**: 1  | **near**: 1  | **J**: 0.002  | **cos**: 0.0  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **example duplicate shingle**:

  > This section dives deeper into a topic that is not strictly required for the rest of the book. Readers who are time-constrained can skim or skip on first pass and return when they need the specific details. The next section assumes only what was covered in the earlier sections of this chapter.
- **best near-dup pair** (Jaccard 1.00):

  - A> This section dives deeper into a topic that is not strictly required for the rest of the book. Readers who are time-constrained can skim or skip on first pass and return when they need the specific details. The next section assumes only what was covered in the earlier sections of this chapter.
  - B> This section dives deeper into a topic that is not strictly required for the rest of the book. Readers who are time-constrained can skim or skip on first pass and return when they need the specific details. The next section assumes only what was covered in the earlier sections of this chapter.

### 22. [LOW] part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.3.html  vs  part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.5.html

- **severity**: 6.0  | **exact**: 1  | **run**: 1  | **near**: 1  | **J**: 0.005  | **cos**: 0.0  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **example duplicate shingle**:

  > PyTorch is the language we will use to build, train, and understand LLMs throughout this book. Every transformer layer, every attention head, and every training loop in the chapters ahead will be expressed in PyTorch. Investing time here pays compound interest in every module that follows.
- **best near-dup pair** (Jaccard 1.00):

  - A> PyTorch is the language we will use to build, train, and understand LLMs throughout this book. Every transformer layer, every attention head, and every training loop in the chapters ahead will be expressed in PyTorch. Investing time here pays compound interest in every module that follows.
  - B> PyTorch is the language we will use to build, train, and understand LLMs throughout this book. Every transformer layer, every attention head, and every training loop in the chapters ahead will be expressed in PyTorch. Investing time here pays compound interest in every module that follows.

### 23. [LOW] part-1-llm-building-blocks/module-03-transformer-architecture/section-3.7.html  vs  part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html

- **severity**: 6.0  | **exact**: 1  | **run**: 1  | **near**: 1  | **J**: 0.002  | **cos**: 0.0  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **example duplicate shingle**:

  > This section dives deeper into a topic that is not strictly required for the rest of the book. Readers who are time-constrained can skim or skip on first pass and return when they need the specific details. The next section assumes only what was covered in the earlier sections of this chapter.
- **best near-dup pair** (Jaccard 1.00):

  - A> This section dives deeper into a topic that is not strictly required for the rest of the book. Readers who are time-constrained can skim or skip on first pass and return when they need the specific details. The next section assumes only what was covered in the earlier sections of this chapter.
  - B> This section dives deeper into a topic that is not strictly required for the rest of the book. Readers who are time-constrained can skim or skip on first pass and return when they need the specific details. The next section assumes only what was covered in the earlier sections of this chapter.

### 24. [LOW] part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.6.html  vs  part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.7.html

- **severity**: 4.27  | **exact**: 0  | **run**: 0  | **near**: 0  | **J**: 0.0  | **cos**: 0.427  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **best near-dup pair** (Jaccard 0.64):

  - A> Suno 's v5 model produces complete songs (with vocals, instrumentation, and lyrics) from a text prompt in under 60 seconds. The output is good enough that the platform crossed 100 million users in its first 18 months and generated a serious lawsuit from the RIAA over training data provenance. Udio competes in the same space with slightly different aesthetic defaults.
  - B> Suno v5 produces complete songs (vocals, instrumentation, lyrics) from a text prompt in under 60 seconds, with quality good enough that the platform crossed 100 million users in its first 18 months. Udio competes in the same space with slightly different aesthetic defaults. Both companies were sued by the RIAA in 2024 over training-data provenance, with the major labels allegin...

### 25. [LOW] part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.10.html  vs  part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.8.html

- **severity**: 3.41  | **exact**: 0  | **run**: 0  | **near**: 0  | **J**: 0.0  | **cos**: 0.341  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)

### 26. [LOW] part-14-applications-of-llms-across-industries/module-69-healthcare-llms/section-69.1.html  vs  part-14-applications-of-llms-across-industries/module-69-healthcare-llms/section-69.5.html

- **severity**: 3.11  | **exact**: 0  | **run**: 0  | **near**: 0  | **J**: 0.0  | **cos**: 0.311  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)

### 27. [LOW] part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.4.html  vs  part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5.html

- **severity**: 3.1  | **exact**: 0  | **run**: 0  | **near**: 0  | **J**: 0.0  | **cos**: 0.31  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **best near-dup pair** (Jaccard 0.48):

  - A> GraphRAG's indexing phase is significantly more expensive than standard RAG because it requires LLM calls for every chunk (entity extraction), every entity pair (relation validation), and every community (summary generation). For a corpus of 10,000 documents, indexing can cost $50 to $500 in LLM API calls depending on the model and chunk count. However, this is a one-time cost,...
  - B> GraphRAG's community summaries pre-compute corpus-level understanding at index time, making it possible to answer "What are the main themes?" without retrieving every document. The trade-off is indexing cost: because every chunk requires LLM calls for entity extraction and every community requires a summary, indexing a 10,000-document corpus can cost $50 to $500 in API fees. Th...

### 28. [LOW] part-14-applications-of-llms-across-industries/module-70-education-llms/section-70.1.html  vs  part-14-applications-of-llms-across-industries/module-70-education-llms/section-70.5.html

- **severity**: 3.06  | **exact**: 0  | **run**: 0  | **near**: 0  | **J**: 0.0  | **cos**: 0.306  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)

### 29. [LOW] part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.1.html  vs  part-14-applications-of-llms-across-industries/module-73-manufacturing-llms/section-73.5.html

- **severity**: 3.02  | **exact**: 0  | **run**: 0  | **near**: 0  | **J**: 0.0  | **cos**: 0.302  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)
- **best near-dup pair** (Jaccard 0.45):

  - A> Siemens Industrial Copilot is the most-cited reference for an industrial-OEM-shipped maintenance copilot. The product integrates with Siemens TIA Portal and the broader factory-automation stack, with retrieval over Siemens equipment documentation and customer-specific configurations. Foxconn's Foxbrain , a proprietary in-house LLM announced in 2025 and built on a fine-tuned Lla...
  - B> Several other large Asian and European manufacturers have followed with comparable in-house programs through 2025 and 2026. The Siemens Industrial Copilot is the most-cited reference for an industrial-OEM-shipped maintenance copilot. Siemens integrated the copilot with TIA Portal, the company's engineering and automation environment, with retrieval over Siemens equipment docume...

### 30. [LOW] part-4-training-adaptation/module-17-peft/section-17.1.html  vs  part-4-training-adaptation/module-17-peft/section-17.2.html

- **severity**: 3.01  | **exact**: 0  | **run**: 0  | **near**: 0  | **J**: 0.0  | **cos**: 0.301  | **xp**: False
- **recommendation**: KEEP-BOTH (likely intentional)

## Cross-Module Watch-List (loose threshold, cosine >= 0.25)

Pairs from **different modules** with moderate prose similarity. The strict
threshold above misses these because they don't share exact shingles, but they
are listed here in case any are genuine duplication rather than thematic overlap.
Most are expected (e.g. an *Inference Optimization* section that touches on the
*Transformer Architecture* section it builds on).

| cos | Section A | Section B |
|-----|-----------|-----------|
| 0.352 | `part-15-llm-agentic-ai-research-frontiers/module-76-frontier-theory/section-76.3.html` | `part-2-understanding-llms/module-10-interpretability/section-10.2.html` |
| 0.327 | `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html` | `part-2-understanding-llms/module-09-inference-optimization/section-9.9.html` |
| 0.276 | `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html` | `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.3.html` |
| 0.268 | `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html` | `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.8.html` |
| 0.266 | `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.3.html` | `part-5-multimodal-llms/module-22-vision-language-models/section-22.4.html` |
| 0.255 | `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.4.html` | `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.4.html` |
| 0.251 | `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html` | `part-2-understanding-llms/module-09-inference-optimization/section-9.8.html` |

## Frequently Reused Boilerplate (filtered out, FYI)

Shingles matching at least 2 templated phrases. These are intentional and were
excluded from the duplicate ranking, but listed here so you can confirm the
templates are consistent and trim them if any are accidentally bloated.

_(none detected -- boilerplate filter could be tuned if needed)_

## Files

- This report: `docs/content-audit/CONTENT_DUPLICATES.md`
- Full shingle index: `docs/content-audit/_content_shingles.jsonl` (38158 rows)
- All scored pairs: `docs/content-audit/_content_pairs.jsonl` (30 rows)

Schema for `_content_shingles.jsonl`:

```json
{"section": "part-1-llm-building-blocks/module-00-.../section-0.1.html",
 "shingle_index": 0,
 "hash": "a1b2c3...",
 "text": "Three-sentence window of prose."}
```

Schema for `_content_pairs.jsonl`:

```json
{"section_a": "...", "section_b": "...",
 "exact_shingles": 3, "near_dup_shingles": 5, "longest_run": 2,
 "jaccard": 0.12, "cosine": 0.68, "cross_part": true,
 "severity": 27.5, "example": "..."}
```

To re-run: `python docs/content-audit/_audit_duplicates.py`
