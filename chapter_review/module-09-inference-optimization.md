# Module 09: Inference Optimization

**Audit date**: 2026-05-11
**Sections reviewed**: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7
**Total word count**: ~32,000

## Summary
The most engineering-dense and immediately practical chapter in Part 2. Excellent coverage of quantization (with worked round-trip examples), KV cache memory math (a memorable "more than the model itself" insight), speculative decoding with an actual lossless-distribution proof, structured/unstructured pruning including 2:4 sparsity, and serving frameworks. Standout sections: 9.2 (KV cache math), 9.3 (speculative decoding proof). Main weaknesses: §9.6 substantially duplicates Module 8 (test-time compute), §9.7 GPU-kernel content was not reviewed but appears advanced and may need a "skip on first read" badge, and the Library Shortcut callouts are inconsistent in coverage (vLLM gets multiple, TGI gets one). Several factual claims about hardware (H100 TFLOPS) sometimes mix sparse and dense numbers.

## Inconsistencies
- **§9.6 duplicates Module 8.** §9.6 reads as a 4,000-word recap of Module 8: thinking tokens, PRMs, MCTS, best-of-N, compute-optimal scaling. The "Big Picture" callout even acknowledges this and points to Chapter 08, but then proceeds anyway. Either the section should be a 1-page bridge or it should be merged into Module 8 with a single cross-reference.
- **GPU bandwidth/TFLOPS numbers.** 9.1.1 says "On an A100 with 2 TB/s memory bandwidth"; A100 is actually 1.55 TB/s (40GB) or 2.0 TB/s (80GB SXM4). The 2 TB/s figure is for the 80GB SXM4 only. 9.3.1 says "On an H100 GPU with 3.35 TB/s memory bandwidth and 989 TFLOPS of FP16 compute". H100 SXM5 has 3.35 TB/s HBM3 bandwidth (correct), but 989 TFLOPS is the *sparse* FP16 number; dense is ~756 TFLOPS. 9.2.2 says "the H100 has 3958 TFLOPS of FP8 compute but only 3.35 TB/s of HBM bandwidth" - 3958 TFLOPS is the *sparse* FP8 number. Mixing sparse and dense is a recurring issue.
- **§9.1.4 GPTQ vs §9.5.5 SparseGPT** both reference Frantar et al. but with different years (2022 for GPTQ, 2023 for SparseGPT). Correct, but the chapter should highlight that they share an algorithm framework explicitly (which §9.5.5.1 does, but only briefly).
- **NF4 levels list.** §9.1.3.1 lists 16 NF4 values starting "{−1.0, −0.6962, ..., 0.7230, 1.0}". 16 values listed - correct. But the values are quantile-based with a slight asymmetry that is not explained (NF4 is asymmetric; the 16 levels include both 0 and an asymmetric distribution around it because the input weight distribution itself is asymmetric for some layers). Worth a sentence.
- **§9.2.1 KV cache table** uses Llama 3.1 8B/70B/405B with `kv_heads=8` for all three. Llama 3.1 8B actually uses 8 KV heads (correct), 70B uses 8 KV heads (correct), 405B uses 8 KV heads (correct). All consistent ✓.
- **§9.3.1 "Theoretical maximum throughput is approximately 1,675 tokens/second for a 1B model"** on H100 - 3.35 TB/s / 2 GB (1B FP16) = 1,675 tok/s ✓. But the 989 TFLOPS comparison should use dense (756 TFLOPS) or be flagged as sparse.
- **Speculative decoding draft model framing.** §9.3.3 says draft models "often produced via knowledge distillation from the target model". §9.3.3.1 then says "Llama 3.1 8B as a draft for Llama 3.1 70B" - 8B is *not* distilled from 70B; they share a tokenizer and were both trained from scratch. The "via distillation" claim is generally true for purpose-built draft models, not for "use a smaller model from the same family".

## Gaps
- **No coverage of FP4 and MXFP4** (Microscaling FP4) which is the cutting-edge format on Blackwell and is mentioned only in passing in §6.8 of Module 6. By 2026 this should be a sub-section in 9.1.
- **No coverage of weight + activation quantization.** §9.1 covers weight-only quantization (GPTQ, AWQ, NF4) extensively but only mentions activation quantization (W8A8, SmoothQuant, ZeroQuant) in passing in the data-types table. SmoothQuant is the production standard for INT8 weight + INT8 activation and deserves a section.
- **§9.4 (serving frameworks) was not reviewed in detail** but the index promises vLLM, SGLang, TGI, TensorRT-LLM, LMDeploy, Ollama, llama.cpp, Triton. That's 8 frameworks; if each gets a paragraph, the section is shallow. Recommend depth on top 3 (vLLM, SGLang, TensorRT-LLM) and a comparison table for the others.
- **§9.5 missing Sheared LLaMA / LLM-Pruner** - the academically prominent structured-pruning approaches for LLMs are not mentioned. Wanda and SparseGPT cover the unstructured side; the structured side needs LLM-Pruner / Sheared LLaMA.
- **§9.5.4 NVIDIA 2:4 sparsity** is well-explained but no benchmarks given. What's the actual end-to-end speedup on a real model? The "nearly 2x" claim is theoretical; production speedups are typically 1.3-1.6x due to other bottlenecks.
- **Continuous batching is mentioned** in §9.2's index description but the actual section content I reviewed (lines 30-150) does not yet introduce it. May appear later. If not, this is a major gap (continuous batching is the second-most-important serving optimization after PagedAttention).
- **No discussion of streaming / SSE for token-by-token delivery** - this is part of "serving infrastructure" but may be in §9.4 (not reviewed in detail).
- **MoE serving is barely mentioned** in §9.2 / §9.4. Expert parallelism for MoE inference (different from training) has different characteristics and deserves a sub-section.

## Errors
- **§9.1.1 A100 memory bandwidth "2 TB/s".** A100 80GB SXM is 2.0 TB/s; A100 40GB PCIe is 1.55 TB/s. The chapter does not specify which.
- **§9.1 fun-fact claims "most models barely notice the difference between 16-bit and 4-bit weights".** Generally true for >7B models and >=4-bit; for <3B models, the gap to 4-bit can be substantial (3-6% perplexity increase). The "barely notice" framing is too strong without size qualifier.
- **§9.1.2.1 absmax example.** The output shows `Quantized: [48, -79, 16, 127, -32]` from `X = [0.3, -0.5, 0.1, 0.8, -0.2]` with scale `0.8/127 ≈ 0.0063`. Round(0.3/0.0063) = 47.6 → 48 ✓; Round(-0.5/0.0063) = -79.4 → -79 ✓. The numbers check out.
- **§9.1.7a vLLM FP8 code uses `quantization="fp8"` and `dtype="float16"`.** vLLM's actual API uses `quantization="fp8"` which is correct, but `dtype="float16"` should probably be `dtype="bfloat16"` for H100 (where BF16 is preferred for non-quantized ops). FP16 works but BF16 is the recommended default. Minor.
- **§9.2.1 KV cache formula** `2 × L × n_kv × s × d_h × dtype_size` ✓. But the *per-layer* explanation should mention that this assumes K and V are separately stored (true for MHA/GQA, NOT for MLA where they share a latent vector).
- **§9.2 PagedAttention practical example "concurrent serving capacity increased from 24 to 58"**. 2.4x improvement is plausible but the original vLLM paper reported up to 2-4x throughput improvement; the specific number depends on workload. As an anonymized case study this is fine.
- **§9.3.2 acceptance probability formula** `min(1, p(x)/q(x))` ✓. The proof of distribution preservation is one of the cleanest in the book. Minor: the "informal proof" is actually rigorous.
- **§9.3.3.2 self-speculative claim "self-speculative decoding uses the target model itself with some layers skipped".** This conflates two distinct techniques: (a) layer-skipping speculation (Draft & Verify, Zhang et al., 2023) and (b) auxiliary-head speculation (Medusa, EAGLE, DeepSeek MTP). They have very different cost/quality profiles. The chapter mostly covers (b) under "Medusa" and "EAGLE" but introduces (a) here without distinguishing them.
- **§9.3.5 Medusa heads "single linear layer each".** The original Medusa paper uses MLP heads (Linear → SiLU → Linear), not single linear layers. The code fragment in 9.3.5 shows the correct two-layer MLP, but the prose contradicts it.
- **§9.5.4.2 ASP `mask_calculator="m4n2_1d"` notation.** The ASP library uses `m4n2_1d` to mean "4 elements per group, 2 zeros, 1D pattern" - correct API. ✓
- **§9.6.1 "doubling model size requires roughly doubling both training compute and serving costs".** Doubling parameters with same data → 2× memory, 2× FLOPs/token → 2× serving cost ✓. But training cost scales with N×D, and Chinchilla says D should also double, so training cost goes 4× when N doubles, not 2×. The "roughly doubling" claim about training is wrong by a factor of 2.
- **§9.6.4.2 MCTS phases (selection, expansion, simulation, backpropagation)** correct. But "A PRM provides the value estimates at each node, replacing the random rollouts used in traditional MCTS" - traditional MCTS uses rollouts, but neural-network-guided MCTS (AlphaGo Zero) uses a value head instead. The chapter contrasts PRM-MCTS with "traditional MCTS" but the relevant comparison is to AlphaZero's value head.
- **§9.7 was not reviewed** - cannot verify GPU kernel content.

## Improvements
- **Disambiguate sparse vs dense TFLOPS** every time hardware FLOPS are quoted. A two-line standardization at the start of the chapter would help.
- **Add a SmoothQuant / W8A8 sub-section in §9.1.** Weight-only quant is well-covered; weight+activation needs equal treatment.
- **Add an MXFP4 / Blackwell sub-section** for forward-looking coverage.
- **Add Sheared LLaMA / LLM-Pruner** as the structured-pruning representatives for LLMs in §9.5.3.
- **Reduce §9.6 to 1-2 pages of bridging content.** It currently duplicates the much fuller treatment in Module 8.
- **Add real-world 2:4 sparsity benchmark numbers** in §9.5.4 (e.g., the SparseGPT + 2:4 results from the Frantar 2023 paper showed ~1.3-1.6x speedup on real models, not the theoretical 2x).
- **§9.3.3 should distinguish layer-skipping speculation (Draft & Verify) from auxiliary-head speculation (Medusa, EAGLE)** as separate strategies with separate trade-offs.
- **Add a continuous-batching subsection in §9.2** (or wherever it currently lives) - it is one of the two foundational serving optimizations.
- **§9.4 should pick top 3 frameworks for depth** (vLLM, SGLang, TensorRT-LLM) and provide a feature-comparison table for the rest.

## One-thing-only fix
**Reduce §9.6 to a 1-page bridge to Module 8.** Currently §9.6 is ~5,000 words covering reasoning models, PRMs, ORMs, MCTS, best-of-N, and compute-optimal inference - all of which are covered in much greater depth in Module 8. The current arrangement asks the reader to learn the same material twice, with subtly different framings. Cut §9.6 down to a single page that says "test-time compute is now an inference optimization concern; for the full treatment see Chapter 8; here is the inference-serving angle (extra KV cache pressure, mixed-mode batching) that is unique to this chapter." That would also free up space to deepen §9.4 (serving frameworks) and §9.5 (pruning), both of which feel rushed in their current form.
