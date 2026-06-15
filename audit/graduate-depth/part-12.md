# Graduate-Depth Audit: Part 12 (LLM Systems at Scale)

| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 57.1 | Compute Planning & Infrastructure | DEPTH-GAP | GPU-tier table and 12x cost vignette are concrete, but no derived sizing math; the "given model, latency, QPS, how many GPUs" promise is deferred to 57.2 and never closed here. Add a worked memory-budget + roofline-per-tier example. |
| 57.2 | Enterprise Integration Patterns | CATALOG-OK | Intentional pattern/vendor survey (gateway vs sidecar, five domains); no quantitative mechanism expected. |
| 57.3 | GPU Procurement & Spot-Reserved Economics | COURSE-READY | Tiered portfolio with real $/hr, spot eviction rates, a fully worked startup unit-economics example ($22K vs $70K). Lecturable on the economics alone. |
| 57.4 | Performance Benchmarking & Cross-Hardware | COURSE-READY | MLPerf scenarios, worked TTFT/TPOT/throughput run, KV-cache tiers with bandwidth/latency, chunked-prefill and CacheGen/InfiniGen mechanisms, all with numbers. |
| 58.1 | Beyond NVIDIA (Groq/Cerebras/etc.) | COURSE-READY | Derives batch-1 bandwidth-bound argument (140 GB/token at 1000 tok/s = 140 TB/s), under-the-hood wafer-scale/LPU mechanisms, self-check Q&A with roofline reasoning. |
| 58.2 | Decentralized Training (DeMo/DisTrO) | COURSE-READY | Per-step gradient-byte math (280 GB to 140 MB, 500-1000x), one DeMo step walked end-to-end, attestation threat model with the Sybil gap named. |
| 58.3 | Edge LLMs (MLX/Apple/Llama-Mobile) | COURSE-READY | Unified-memory vs discrete-VRAM derivation (why 32 GB beats 24 GB), QAT vs PTQ perplexity deltas, three-tier routing with latency/cost per tier, self-check. |
| 58.4 | FlashAttention-4 / Blackwell Kernels | COURSE-READY | Memory-hierarchy bandwidth tiers (HBM/SRAM/registers), asymmetric-pipelining mechanism tied to Blackwell SMs, kernel-availability gating case study with numbers. |
| 58.5 | Training-Inference Co-Design | COURSE-READY | Sardana inference-aware scaling derivation, MoE compute-vs-memory worked example (DeepSeek V4: 1.34 TB weights, 74 GFLOPs/token, 18x), runnable top-k router code. |
| 59.1 | Distributed Training Fundamentals | COURSE-READY | 18-bytes/param memory accounting, ring all-reduce bandwidth derivation (2(N-1)S/N -> 2S), interconnect tiers in GB/s, McCandlish critical-batch formula, full DDP loop. |
| 59.2 | ZeRO and FSDP | COURSE-READY | Per-stage bytes/param table (16 -> 16/N), Llama 70B/405B per-rank memory math with min-GPU counts, all-reduce = reduce-scatter + all-gather identity, meta-device init. |
| 59.3 | Megatron-LM and Tensor Parallelism | COURSE-READY | Column/row-parallel matmul algebra, worked 70B-on-8-H100 example (470 MB vs 3.7 GB intermediate, 0.6 ms all-reduce), from-scratch TP MLP with f/g autograd, NVLink-fanout limit derived. |
| 59.4 | Pipeline Parallelism & Hybrid | COURSE-READY | GPipe bubble formula (P-1)/M, interleaved and zero-bubble variants, full 3D-parallelism dimension-picking worked for 405B on 2048 GPUs, gradient-clipping all-reduce gotcha. |
| 59.5 | Production Training Infrastructure | COURSE-READY | MTBF table from real post-mortems, optimal checkpoint interval sqrt(2*C*tau) derived, MFU = 6PT/(N*peak) with roofline ceiling math, FP8 E4M3/E5M2 numerics. |
| 60.1 | Why Edge Deployment | DEPTH-GAP | Four-driver framing plus a blended-quality/cost break-even formula, but no hardware sizing math; "which model fits which device" is asserted via a matrix, not derived. Add a memory/token-budget derivation. |
| 60.2 | The Edge Framework Landscape | CATALOG-OK | Explicitly marked GIANT_SECTION catalog (six runtimes + GGUF quant levels + iMatrix); tool survey by design. |
| 60.3 | Hardware Constraints | DEPTH-GAP | Has battery (Wh, tokens/watt), thermal-throttle step function, and a memory-fit ceiling, but the model-fits-device claims stay rule-of-thumb; no KV-cache-vs-context memory derivation tying it together. Add the working-set arithmetic. |
| 61.1 | Platforms | CATALOG-OK | "Scale Tools of the Trade" chapter; intentional platform/vendor survey. Carries bonus bisection-bandwidth math, exceeding catalog bar. |
| 61.2 | Libraries and Frameworks | CATALOG-OK | Intentional library survey with stack-composition patterns; FlashAttention online-softmax recurrence callout adds bonus depth. |
| 61.3 | Datasets and Benchmarks | CATALOG-OK | Intentional corpora/benchmark/profiler catalog. |
| 61.4 | Models | CATALOG-OK | Intentional base/MoE/long-context/frontier checkpoint catalog. |
| 61.5 | External Reading and Communities | CATALOG-OK | Intentional venues/papers/communities index. |

## Summary
- COURSE-READY: 13 | DEPTH-GAP: 3 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 6
- Top sections most worth enriching:
  1. 57.1 (Compute Planning): close the sizing-math promise it makes itself; add a worked "model + latency + QPS -> GPU count" derivation (KV-cache memory + roofline per tier) instead of deferring it to 57.2.
  2. 60.3 (Hardware Constraints): add the explicit on-device working-set arithmetic (weights + KV-cache(context) + activations vs RAM budget) so the "3B fits, 8B does not" claims are derived, not asserted.
  3. 60.1 (Why Edge): supplement the cost break-even formula with a one-paragraph hardware sizing derivation so the use-case matrix has a mechanism behind it (currently the chapter's quantitative weight all lives in 60.3).
