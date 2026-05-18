# Scientific Depth Opportunities (Task B Audit)

Scan of ~30 main-content sections across Parts I-XVI looking for opportunities to add scientific depth: numbered Algorithm callouts, neural-architecture tensor diagrams, and explicit processing-step formalizations. The list below is review-only; no HTML edits in this pass. Authoring the actual Algorithm callouts is a separate task. Sections are grouped by topic area and each opportunity is one line.

## 1. Transformer Architecture and Attention (Part I, Chapter 3)

- Section 3.1.5 (Scaled Dot-Product Attention): needs Algorithm callout for the full per-head forward pass (Q, K, V projections; QK^T scaled by sqrt(d_k); softmax; attention @ V; output projection) with explicit tensor shapes at each step.
- Section 3.1.6 (Position-Wise FFN): needs Algorithm callout for the two-layer FFN (W1, GELU/SwiGLU, W2) with shape annotations [B, T, d_model] to [B, T, 4*d_model] to [B, T, d_model].
- Section 3.1.8 (Layer Normalization): needs Algorithm callout contrasting LayerNorm vs RMSNorm step-by-step (mean, variance, scale, shift vs RMS-only).
- Section 3.1.11 (The Complete Forward Pass): needs Algorithm callout for the full decoder-block forward pass (pre-norm, attention, residual, pre-norm, FFN, residual) with shapes.
- Section 3.3.2 (Positional Encoding Variants): needs Algorithm callout for RoPE rotation per pair (cos/sin matrix construction, complex-rotation form) and a separate one for ALiBi bias slope schedule.
- Section 3.3.3 (Efficient Attention Mechanisms): needs Algorithm callout for Sliding-Window Attention and Sink-Token Attention masking patterns (boundary indices, mask construction).

## 2. Decoding and Sampling (Part I, Chapter 4)

- Section 4.2.4 (Nucleus / Top-p Sampling): needs Algorithm callout for top-p selection: sort logits, compute cumulative-softmax, find cutoff index where cumulative probability crosses p, renormalize, sample.
- Section 4.2.5 (Min-p Sampling): needs Algorithm callout for min-p: compute max_prob, threshold = min_p * max_prob, keep tokens above threshold, renormalize, sample.
- Section 4.2.7 (Repetition / Frequency / Presence Penalty): needs Algorithm callout showing how each penalty modifies logits given a count vector over generated tokens.

## 3. Inference Optimization (Part II, Chapter 9)

- Section 9.1.4 (Post-Training Quantization Algorithms): needs Algorithm callout for GPTQ Hessian-based weight update (block iteration, error compensation across columns) and a separate one for AWQ activation-aware scaling.
- Section 9.2.3 (PagedAttention): needs Algorithm callout for the block-table lookup that maps logical KV positions to physical pages, with the allocation/eviction step on sequence growth.
- Section 9.2.4 (MHA, MQA, GQA Architectural Deep Dive): needs neural-architecture tensor diagram (or pseudocode) showing the three variants side-by-side with Q-head count, KV-head count, and grouping factor explicit in the tensor shapes.
- Section 9.3.2 (Speculative Decoding, Acceptance and Rejection Sampling): needs Algorithm callout for the rejection-sampling acceptance criterion (draft p, target q, accept with probability min(1, q/p), resample on rejection) with the proof sketch that the marginal matches the target.
- Section 9.3.4 (EAGLE): needs neural-architecture diagram of the feature-level draft head (last hidden state to draft head to token logits) showing where it taps the target model.
- Section 9.3.5 (Medusa): needs Algorithm callout for the tree-attention verification across the multi-head proposal set.
- Section 9.6.4 (Search at Inference Time): needs Algorithm callout for beam search and a separate one for Monte Carlo Tree Search over reasoning steps with a process reward signal.

## 4. Training and Alignment (Part IV, Chapters 17-18)

- Section 17.2.1 (DoRA): needs Algorithm callout for the weight-decomposed update: decompose W = m * (V / ||V||), train m (magnitude) and LoRA(V) (direction) separately, recombine at inference.
- Section 17.2.9 (GaLore): needs Algorithm callout for the gradient low-rank projection: compute gradient G, project to low-rank via SVD or random projection, update in low-rank space, periodically re-orthogonalize.
- Section 17.2.10 (rsLoRA): needs Algorithm callout showing the rank-stabilized scaling factor alpha/sqrt(r) vs alpha/r and why it stabilizes gradients at high rank.
- Section 18.2 (PPO for RLHF): needs Algorithm callout for the PPO clipped surrogate objective with KL penalty to reference model, advantage normalization, and the rollout-update loop.
- Section 18.2 (DPO): needs Algorithm callout contrasting DPO's closed-form preference loss against PPO's two-stage reward-then-policy procedure, with explicit terms (log-prob ratio, beta scaling, sigmoid).
- Section 8.3.2 (GRPO): needs Algorithm callout for the group-relative advantage computation (sample N completions, compute per-completion reward, normalize within the group, update with PPO-style clip).

## 5. Vector Search and Retrieval (Part VII, Chapter 31)

- Section 31.2.2 (HNSW): needs Algorithm callout for the multi-layer greedy search (entry-point selection, level descent, per-level candidate expansion with priority queue, beam parameter ef).
- Section 31.2.3 (IVF): needs Algorithm callout for the two-stage search: (a) coarse quantizer over centroids selects nprobe lists, (b) exhaustive search within selected lists.
- Section 31.2.4 (Product Quantization): needs Algorithm callout showing the codebook training (k-means per subvector) and the lookup-table-based distance computation at query time.
- Section 31.3.6 (Reciprocal Rank Fusion): needs Algorithm callout for the RRF score combination: sum over retrievers of 1/(k + rank_i(doc)), then re-rank.

## 6. Agentic AI and Reasoning (Part VI, Chapter 26 and Part II, Chapter 8)

- Section 26.1.3 (ReAct Framework): needs Algorithm callout for the ReAct loop: while not done, sample Thought, sample Action, execute tool, observe, append to context, repeat; with halt-condition and max-step guard.
- Section 26.2.1 (From Simple Loops to Strategic Planning): needs Algorithm callout for the Plan-and-Execute pattern: decompose query into subgoals, execute each via sub-agent, aggregate.
- Section 26.2.2 (Tree of Thoughts and LATS): needs Algorithm callout for ToT search: expand thought tree breadth-first, score with self-evaluation, prune low-scoring branches, return best leaf.
- Section 26.2.3 (Reflection and Self-Correction): needs Algorithm callout for the Reflexion loop: attempt, critique, revise with critique in context, retry, exit on success or max-retries.
- Section 8.1.3 (Mechanisms of Test-Time Compute): needs Algorithm callout for self-consistency: sample N reasoning traces with temperature > 0, extract answers, majority-vote, return mode.

## 7. Distributed Training and Inference (Part XII)

- Section 59.1 (Data Parallel All-Reduce): needs neural-architecture diagram of ring all-reduce: scatter-reduce phase plus all-gather phase, with per-step tensor sizes.
- Section 59.2 (ZeRO Stage 3 / FSDP Full-Shard): needs Algorithm callout for the per-layer forward pass: all-gather parameters from peers, compute, reshard, free; mirrored for backward.
- Section 59.3 (Megatron Tensor Parallel): needs neural-architecture diagram of column-parallel plus row-parallel matmul pairs around the MLP block, with the two implied all-reduces.
- Section 59.4 (Pipeline Parallelism, 1F1B): needs Algorithm callout for the 1F1B schedule: warmup phase (P-1 forward), steady-state phase (alternating forward/backward), cooldown phase.

## 8. Multimodal and Document Understanding (Part V)

- Section 22.1 (ViT Patch Tokenization): needs neural-architecture diagram of patch embedding: image [B, 3, H, W] to conv2d kernel=P stride=P to flatten to [B, (H/P)*(W/P), d_model], with CLS token prepend.
- Section 22.2 (CLIP Contrastive Pretraining): needs Algorithm callout for the symmetric InfoNCE loss: image-to-text softmax and text-to-image softmax, average, with batch-size sensitivity discussion.
- Section 22.3 (LLaVA Connector): needs neural-architecture diagram of the connector: vision encoder output [B, num_patches, d_vision] to MLP/projection to [B, num_patches, d_llm] inserted into the prompt token sequence.
- Section 21.1.2 (TrOCR): needs neural-architecture diagram of the vision-encoder plus text-decoder cross-attention layout, with patch sequence on encoder side and token sequence on decoder side.

## Notes on Authoring Priority

If only a subset can be authored in a follow-up pass, the highest-leverage opportunities are:

1. Section 3.1.5 (attention forward pass): foundational; missing the canonical algorithm is unusual for a textbook.
2. Section 9.3.2 (speculative decoding rejection sampling): the proof-and-algorithm pairing is the cleanest didactic moment in inference optimization.
3. Section 18.2 (DPO vs PPO): the contrast is what makes alignment intelligible; an Algorithm callout side-by-side is high-impact.
4. Sections 31.2.2 to 31.2.4 (HNSW, IVF, PQ): three foundational algorithms in the same section, currently described in prose only.
5. Section 26.1.3 (ReAct): the canonical agentic loop deserves a numbered Algorithm callout since the book references it everywhere.

All other opportunities are valuable but secondary to those five.
