# Architecture Diagram Opportunities Audit

**Date**: 2026-05-19
**Mode**: READ-ONLY scout (no diagrams generated, no figures added)
**Scope**: 938 `section-*.html` files across 15 parts (v2.0)
**Goal**: Identify where a MODEL ARCHITECTURE or FLOW diagram would unlock comprehension, with redraw-from-source planning

---

## 1. Executive Summary

### Coverage snapshot

The book is already heavily illustrated. Quick counts of unique `Figure N.M.K` references per part:

| Part | Sections | Unique figures | Density |
|---|---:|---:|---:|
| Part 1 (Building Blocks) | 35 | 105 | **3.0** |
| Part 2 (Understanding LLMs) | 39 | 74 | 1.9 |
| Part 3 (Working with LLMs) | 20 | 48 | 2.4 |
| Part 4 (Training & Adaptation) | 44 | 61 | 1.4 |
| Part 5 (Multimodal LLMs) | 46 | 58 | 1.3 |
| Part 6 (Agentic AI) | 26 | 41 | 1.6 |
| Part 7 (Retrieval & IE) | 34 | 75 | 2.2 |
| Part 8 (Conversational AI) | 18 | 31 | 1.7 |
| Part 9 (Eval & Observability) | 33 | 42 | 1.3 |
| Part 10 (Security & Safety) | 22 | 34 | 1.5 |
| Part 11 (Ethics & Governance) | 25 | 42 | 1.7 |
| Part 12 (Systems at Scale) | 22 | 37 | 1.7 |
| Part 13 (LLMOps) | 16 | 24 | 1.5 |
| Part 14 (Industry Applications) | 45 | 46 | 1.0 |
| Part 15 (Frontiers) | 18 | 21 | 1.2 |

**Total**: ~937 sections, ~739 unique figures (incl. cartoon illustrations + technical SVGs).

### High-value gaps found

- **Architecture diagrams missing where prose carries the full mental-model load**: 26 high-impact opportunities (see Top 40 below).
- **Flow/sequence diagrams that would replace ordered bullet lists**: 14 candidates.
- **Architectural variants comparison panels missing where prose only enumerates differences**: 8 candidates.

### Why this audit differs from `UNIMPLEMENTED_VISUALS.md`

The May 2026 unimplemented-visuals scan tracked "sections with zero figures." This audit takes a different cut: sections that **have figures** but lack a **precise canonical architecture diagram** that would lock the concept in the reader's mind. A "cartoon embedding-space-party" image (Fig 31.1.1) is decorative, not architectural. The reader needs *both*, but the architectural one is where comprehension is unlocked, and several of those are still missing.

### What's covered well already (don't duplicate)

- **Transformer fundamentals** (3.1a-3.6): exemplary. The residual stream, scaled dot-product attention, multi-head attention, RoPE/ALiBi, FlashAttention, complexity classes — all illustrated. **Reference quality**.
- **Inference optimization** (9.1-9.7): KV cache, PagedAttention, MHA/MQA/GQA, RadixAttention, speculative decoding, structured sparsity — all illustrated.
- **RLHF/DPO/Constitutional AI/RLVR** (18.1-18.4): every paradigm has a flow diagram.
- **PEFT** (17.1-17.7): LoRA, DoRA, soft-prompt methods, distillation, task arithmetic — all illustrated.
- **Distributed training** (59.1-59.5): three axes of parallelism, interconnect hierarchy, ZeRO, GPipe-vs-1F1B, 3D parallelism — reference quality.
- **Agent foundations** (26.1-26.6): agent loop, planning strategies, multi-tier reasoning, memory taxonomy, production architecture — well covered.
- **Multi-agent topologies** (28.1-28.4): foundational + advanced topologies illustrated.

---

## 2. Top 40 Recommendations (Ranked by pedagogical impact × current gap severity)

### Tier S: book-critical architecture gaps (rank 1-10)

These sections lack the *one* diagram that would make the concept click. Highest pedagogical leverage.

| # | Section | Concept | Source diagram to redraw | Detail | Complexity | Priority |
|---:|---|---|---|---|---|---|
| 1 | `part-5-multimodal-llms/module-22-vision-language-models/section-22.3.html` | **BLIP-2 / Q-Former cross-attention architecture** | Li et al. (2023) "BLIP-2", arXiv:2301.12597 Fig 2. Cross-attention from N learned query tokens to ViT patch features. | Vision encoder (frozen) → Q-Former (32 query tokens + cross-attention) → LLM. Show queries, keys, values; the learned-queries→patch-features attention. | Medium (10 boxes, 2 cross-attention arrows) | **HIGH** |
| 2 | `part-5-multimodal-llms/module-22-vision-language-models/section-22.7.html` | **Flamingo Perceiver Resampler + gated cross-attention** | Alayrac et al. (2022) "Flamingo: a Visual Language Model for Few-Shot Learning", arXiv:2204.14198 Fig 3. | Resampler block (vision features → 64 latent queries via cross-attention) + gated cross-attention layer interleaved into frozen LLM. Show the tanh-gate. | Medium (8-9 boxes, 1 cross-attention, 1 gate symbol) | **HIGH** |
| 3 | `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html` | **ColBERT late-interaction MaxSim** | Khattab & Zaharia (2020) "ColBERT", arXiv:2004.12832 Fig 1. | Per-token query embeddings × per-token doc embeddings → similarity matrix → row-wise max → sum. Contrast against bi-encoder dot product. | Medium (12 elements: 2 token-embed strips + 1 matrix + max arrows + sum) | **HIGH** |
| 4 | `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.6.html` | **IVF + Product Quantization detailed compute path** (Figure 31.6.2 covers PQ shape; section 31.6 lacks an IVF-PQ combined search-path diagram showing coarse quantizer → PQ refine) | Jegou et al. (2011) "Product Quantization for Nearest Neighbor Search" Fig 1, plus Faiss IVF-PQ docs. | Query → IVF coarse quantizer (chooses nlist clusters) → PQ-encoded residual table lookup → ranking. | Medium (8 elements, codebook insets) | **HIGH** |
| 5 | `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html` | **Mamba selective scan block** | Gu & Dao (2023) "Mamba", arXiv:2312.00752 Fig 3. | x_t → linear projections (Δ, B, C) → discretization → state-space scan (h_t) → output. Show the *selective* part (input-dependent Δ, B, C). | Medium (10 elements: 4 projections, scan box, gates) | **HIGH** |
| 6 | `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html` | **MoE expert parallelism with all-to-all dispatch** | Lepikhin et al. GShard (2020) arXiv:2006.16668 Fig 3, OR DeepSeek-V3 tech report fig. | 4 GPUs, each holding 2 of 8 experts. Router on each GPU; all-to-all dispatch; expert compute; all-to-all combine. | Complex (4 GPU columns × 4 stages = 16 elements + crossing arrows) | **HIGH** |
| 7 | `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.2.html` | **Modern GPU memory & compute hierarchy** | NVIDIA H100 whitepaper Fig 3 OR Hennessy & Patterson 6th ed. ch. 4. | Tensor cores, SM (streaming multiprocessor), L1/L2 cache, HBM3, NVLink, NVSwitch. Show bandwidths at each tier. | Medium (8 tiers + bandwidth annotations) | **HIGH** |
| 8 | `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.6.html` | **GRPO (Group Relative Policy Optimization)** | DeepSeekMath paper (Shao et al. 2024) arXiv:2402.03300 Fig 4, OR DeepSeek-R1 tech report. | Prompt → sample G completions → verifier rewards → group-normalize → policy gradient. Highlight: no critic network needed. | Medium (8 elements: prompt box, 4 completions, verifier, normalizer, gradient arrow) | **HIGH** |
| 9 | `part-2-understanding-llms/module-09-inference-optimization/section-9.7.html` | **vLLM internal architecture / continuous batching scheduler** | Kwon et al. (2023) "Efficient Memory Management for LLM Serving with PagedAttention", SOSP 2023, Fig 5. | Scheduler queue → block manager → KV cache pool (page table) → CUDA kernels. Show how PagedAttention plugs in. | Complex (6 components + page-table inset) | **HIGH** |
| 10 | `part-5-multimodal-llms/module-23-3d-generation-neural-scenes/section-23.1.html` | **NeRF / Gaussian Splatting pipeline** | Mildenhall et al. (2020) NeRF Fig 2, OR Kerbl et al. (2023) 3D Gaussian Splatting Fig 1. | Multi-view images → ray sampling → MLP / Gaussian primitives → volume rendering → novel view. | Medium (7-8 elements, ray-sample inset) | **HIGH** |

### Tier A: high-value architecture diagrams (rank 11-25)

| # | Section | Concept | Source diagram to redraw | Detail | Complexity | Priority |
|---:|---|---|---|---|---|---|
| 11 | `part-5-multimodal-llms/module-21-document-understanding-ocr/section-21.3.html` | **Generic VLM-for-documents pipeline** (no diagram currently) | Compose from LayoutLMv3 paper (Huang et al. 2022) + Qwen-VL doc tech report. | Document image → tile partition → vision encoder per tile → projection → LLM with text query → structured-JSON output. | Medium (8-9 boxes, LR flow) | **HIGH** |
| 12 | `part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.4.html` | **Provider API fine-tuning lifecycle vs. self-hosted lifecycle** | Hugging Face fine-tuning blog post + OpenAI fine-tuning docs. | Two parallel swim-lanes: (a) upload → API validates → managed training → managed inference, (b) data prep → local trainer → eval → deploy. | Medium (2 swim-lanes × 5 steps each) | MEDIUM-HIGH |
| 13 | `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.3.html` | **RLVR training loop with verifier feedback** | DeepSeek-R1 Fig 1 (training pipeline). | Policy generates → verifier (regex / unit test / proof checker) → 0/1 reward → policy gradient. Contrast with RLHF reward-model arrow. | Medium (8 elements; can reuse Fig 18.6.2 layout but specialize) | MEDIUM-HIGH |
| 14 | `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.8.html` | **Vector database internal architecture** (Fig 31.8.2 exists but is a high-level box; deserves a more detailed redraw) | Pinecone tech doc OR Milvus architecture diagram (open docs). | Query path: client → router → query node → segment manager → ANN index (per shard) → result aggregator. Show write path separately. | Complex (10+ components, two paths) | MEDIUM-HIGH |
| 15 | `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.6.html` | **Hybrid retrieval pipeline (BM25 + dense + reranker)** | Lin et al. (2021) "Pretrained Transformers for Text Ranking" survey Fig 3.x. | Query → dual paths (BM25 / dense ANN) → score fusion (RRF or weighted) → reranker (cross-encoder) → top-k. | Medium (8 boxes, 2 parallel paths converging) | MEDIUM-HIGH |
| 16 | `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html` | **Self-RAG decision diagram** (Self-RAG referenced but not diagrammed; CRAG is) | Asai et al. (2023) "Self-RAG" arXiv:2310.11511 Fig 1. | Prompt → retrieve? token → conditional retrieval → utility critic tokens → score selection. Show the special tokens flow. | Medium (10 elements including decision diamonds) | MEDIUM-HIGH |
| 17 | `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html` | **RAG-Fusion / multi-query reranking with RRF** | Adapted from RAG-Fusion blog post (LangChain blog, 2023). | Original query → LLM generates 3 paraphrases → each retrieves top-k → reciprocal rank fusion → final top-k. | Medium (8 elements, fan-out fan-in) | MEDIUM |
| 18 | `part-5-multimodal-llms/module-22-vision-language-models/section-22.5.html` | **MLLM evaluation pipeline (MMMU + MM-Vet judge architecture)** | Per Yu et al. MM-Vet paper Fig 2. | Image+question → VLM → free-form answer → GPT-4-judge prompt with capability rubric → per-capability scores. | Medium (7 elements, scoring rubric inset) | MEDIUM |
| 19 | `part-2-understanding-llms/module-09-inference-optimization/section-9.8.html` | **Disaggregated serving (prefill-decode split)** — Figure 9.8.1 shows prefill/decode latency but no disaggregated-pool architecture diagram | DistServe paper (Zhong et al. 2024) Fig 3, OR Splitwise paper (Patel et al. 2024). | Prefill GPU pool (high-FLOPS) ↔ decode GPU pool (high-memory-bandwidth) connected by KV cache transfer. | Medium (2 GPU pools + transfer arrow + scheduler) | MEDIUM-HIGH |
| 20 | `part-2-understanding-llms/module-09-inference-optimization/section-9.9.html` | **GPU sparse-matrix multiplication kernel** for 2:4 sparsity | NVIDIA Ampere whitepaper Fig 11. | Dense weight × activation → 2:4 mask + index → sparse compute → output. Show 50% FLOP reduction with metadata sidecar. | Medium (8 elements + matrix insets) | MEDIUM |
| 21 | `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.5.html` | **RAG with citation verification (NLI loop)** | Currently Fig 32.5.1 only sketches the loop; an expanded version showing entailment scoring per claim would help. | Generated answer → claim-extractor → for each claim: NLI(claim, source) → confidence → flag-or-keep. | Medium (8 elements, per-claim inner loop) | MEDIUM |
| 22 | `part-6-agentic-ai/module-27-tool-use-protocols/section-27.5.html` | **Agentic RAG retrieval-as-tool loop** | Compose from CRAG paper Fig 2 + ReAct paper Fig 1. | Agent decides "search?" → retrieval tool → results → grade utility → loop or answer. | Medium (7 elements, decision diamond) | MEDIUM |
| 23 | `part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html` | **Whisper encoder-decoder architecture** | Radford et al. (2022) "Robust Speech Recognition via Large-Scale Weak Supervision" Fig 1. | Audio → 80-mel spectrogram → encoder transformer → cross-attention from decoder transformer that emits text+special tokens. | Medium (8 elements, includes cross-attention arrows) | MEDIUM |
| 24 | `part-5-multimodal-llms/module-20-audio-music-generation/section-20.1.html` | **Modern TTS architecture (parallel non-autoregressive)** | Kim et al. (2020) "Glow-TTS" Fig 1 OR VITS paper. | Text → phoneme encoder → duration predictor + monotonic alignment → mel-spectrogram (or codec) → vocoder. | Medium (9 elements) | MEDIUM |
| 25 | `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.3.html` | **NVL72 / GB200 rack-scale topology** | NVIDIA GB200 NVL72 architecture whitepaper Fig 2-3. | Rack: 18 compute trays, 9 NVSwitch trays, NVLink5 mesh. Show the all-to-all topology vs. legacy 8-GPU server. | Medium (rack diagram with 27 nodes, simplified) | MEDIUM |

### Tier B: useful additions (rank 26-40)

| # | Section | Concept | Source diagram to redraw | Detail | Complexity | Priority |
|---:|---|---|---|---|---|---|
| 26 | `part-6-agentic-ai/module-29-specialized-agents/section-29.1.html` | **Code-agent self-debugging loop** (already has cartoon illustration Fig 29.1.2; needs precise SVG variant — noted in `wave25_diagrams.md` too) | Compose from Reflexion paper Fig 1 + AutoGPT loop. | Write → run tests → parse failures → reason about cause → patch → repeat, with iteration-budget exit. | Simple (5-6 boxes, cycle arrow) | MEDIUM |
| 27 | `part-1-llm-building-blocks/module-03-transformer-architecture/section-3.7.html` | **RoPE 2D rotation in attention** (Fig 3.7.3 is conceptual; a more precise vector-rotation visualization would help) | Su et al. (2021) "RoFormer" Fig 1. | Q, K vectors split into 2D pairs → rotated by θ_pos → dot product preserves relative angle. Show two positions. | Medium (vector-pair pair diagram, 2 positions, rotation arrows) | MEDIUM |
| 28 | `part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.3.html` | **Speculative decoding tree-verification** (already covered in section 9.4, but section 4.3 on decoding lacks architectural anchor) | Leviathan et al. (2023) "Fast Inference from Transformers via Speculative Decoding" Fig 1 OR Medusa paper. | Draft model emits γ tokens → target model verifies in parallel → accept prefix → resample on first reject. | Simple-Medium (8 elements, parallel verification arrows) | MEDIUM |
| 29 | `part-4-training-adaptation/module-17-peft/section-17.1.html` | **LoRA forward + backward path** (Fig 17.1.1 is cartoon; a precise matrix-decomposition diagram would help) | Hu et al. (2022) "LoRA" arXiv:2106.09685 Fig 1. | W (frozen, d×k) + α·BA (B: d×r, A: r×k) ; show low-rank decomposition explicitly. | Simple (matrix shapes, frozen vs trainable shading) | MEDIUM |
| 30 | `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html` | **LLM-as-judge pipeline with calibration** | Compose from Zheng et al. (2023) MT-Bench paper Fig 1 + chatbot arena. | Candidate response → judge LLM with rubric → score → calibrate against gold pairs → final metric. | Medium (7-8 elements + calibration sidecar) | MEDIUM |
| 31 | `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.4.html` | **Prompt injection attack vector flow** (security chapters tend to have story illustrations rather than architecture) | Compose from Greshake et al. (2023) "Not what you've signed up for" Fig 2. | Attacker website ← LLM browses → exfiltrates payload → injected instructions → agent acts on attacker behalf. | Simple (5 actors + numbered arrows) | MEDIUM |
| 32 | `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.3.html` | **Sandbox / capability-bounded execution** | Compose from open standards (gVisor, Firecracker docs). | Agent → sandbox boundary (syscall filter, network-policy, fs-rootfs) → resources. Show what crosses the boundary. | Medium (7-8 elements, boundary highlight) | MEDIUM |
| 33 | `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.3.html` | **Model serving infra (load balancer + autoscaler + replica pool)** | Compose from Kubernetes/k-serve docs. | Client → load balancer → autoscaler decides → replica pool (each replica has model+KV cache+queue). | Medium (8 elements) | MEDIUM |
| 34 | `part-13-llmops-lifecycle/module-64-workflow-orchestration/section-64.3.html` | **Agent workflow orchestrator (LangGraph-style)** | Compose from LangGraph or Temporal docs. | State graph: nodes (steps) + edges (transitions) + checkpoints + retry policies. | Medium (DAG diagram with 6-8 nodes) | MEDIUM |
| 35 | `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/section-54.1.html` | **Generative watermark embedding + verification** | Compose from Kirchenbauer et al. (2023) "A Watermark for Large Language Models" Fig 2. | Encoder: hash(prev tokens) → green/red list → biased sampling. Verifier: same hash → fraction of green → p-value. | Medium (encoder + verifier swim lanes) | MEDIUM |
| 36 | `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.2.html` | **Mixture of Depths / hybrid SSM+attention block** | Compose from Jamba paper (Lieber et al. 2024) Fig 2 + Mixture-of-Depths paper. | Block layout: 7 SSM layers + 1 attention layer pattern (Jamba); show the periodicity. | Medium (block diagram, 8 layers) | MEDIUM |
| 37 | `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.2.html` | **Realtime audio LLM full-duplex architecture** | Compose from OpenAI Realtime API docs + Moshi paper (Défossez et al. 2024) Fig 1. | Input audio stream → codec encoder → LLM (interleaved audio+text tokens) → codec decoder → output audio stream. Show concurrent input+output. | Medium (7-8 elements, 2 streams) | MEDIUM |
| 38 | `part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html` | **NER architectures comparison** | Compose from CoNLL benchmarks survey diagrams. | BiLSTM-CRF (legacy) vs encoder+span-classifier vs LLM-extractor — three side-by-side panels. | Medium (3 panels × 4-5 boxes) | MEDIUM |
| 39 | `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.1.html` | **Bias measurement & mitigation pipeline** | Compose from BBQ benchmark paper + Counterfactual Fairness paper. | Data → bias diagnostic (per group score) → mitigation step (reweighting / debiasing / counterfactual) → re-evaluate. | Medium (6-7 elements, feedback loop) | MEDIUM |
| 40 | `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.1.html` | **Total cost of ownership flow for LLM training** | Compose from Chinchilla follow-ups + cloud cost calculators. | Inputs (compute hours, storage, network, eng-time) → cost breakdown → optimization knobs. | Simple-Medium (sankey or stacked bar concept) | LOW-MEDIUM |

---

## 3. Patterns: Which kinds of concepts benefit most from architecture diagrams

Looking across the 40 candidates above and the existing ~739 figures, the book's diagram economy shows clear patterns:

### Architecture diagrams (static block layouts) work best for

- **Model architectures**: ViT, CLIP, Q-Former, Flamingo, Mamba block, Whisper. The reader needs to see "what reads from what" and "what is frozen vs trained" in one glance. **The book has these for Transformer/RLHF/PEFT but not for several VLM connectors (Q-Former, Resampler) — the biggest gap.**
- **System architectures**: vLLM internals, vector DB internals, NVL72 rack. Components + cardinality + dataflow. **Several gaps here in the systems chapters.**
- **Memory/compute hierarchies**: GPU memory tiers, KV-cache layouts, sparse-matrix layout. **Section 58.2 (frontier hardware) lacks a unified diagram.**

### Flow diagrams (sequential pipelines) work best for

- **Training pipelines**: RLHF, DPO, Constitutional AI, GRPO, RLVR. **All except GRPO already diagrammed.**
- **Retrieval pipelines**: RAG ingestion, hybrid retrieval, CRAG, Self-RAG, RAG-Fusion. **CRAG done; Self-RAG and RAG-Fusion still prose-only.**
- **Inference paths**: prefill vs decode, speculative-decoding tree, disaggregated serving. **Disaggregated serving (9.7) is a clear gap.**
- **Agent loops**: ReAct, Reflexion, planning, multi-agent topologies. **All diagrammed.**

### Comparison diagrams (side-by-side panels) work best for

- **Architectural variants**: encoder-only / decoder-only / encoder-decoder; MHA / MQA / GQA; CLIP vs SigLIP; LLaVA vs BLIP-2 vs Flamingo. **First three are done; the VLM connector comparison is a clear gap (see #2 above).**
- **Training-vs-inference contrasts**: dense vs MoE FLOPs; standard vs reasoning models. **Reasoning panels done well (Fig 8.1.3).**

### Sequence diagrams (numbered-step interactions) work best for

- **Protocol interactions**: MCP, A2A, function-calling loops. **All done.**
- **Attack vector flows**: prompt injection, prompt leak, side channels. **Security chapters have story illustrations but few precise architecture sequences. This is a soft gap.**

### Where diagrams should NOT be added

- "Tools of the trade" reading-list sections (per `ILLUSTRATOR_R2.md` convention).
- Sections where prose summarizes well-known math (entropy, cross-entropy formulae). These are math, not architecture.
- "Why X matters" framing sections. A cartoon illustration carries more pedagogical value than a precise diagram of an abstract concept.

---

## 4. IP-safety notes

The redraw policy: **same essential structural information, different visual style**. This is sound; copyright protects creative expression, not factual content of a diagram. Reference diagrams I would treat with extra caution:

### Safe to redraw (any reasonable reinterpretation is fine)

- **Mamba selective scan** (#5): the canonical figure is conceptual, structural, and the relevant content is the equations. A redraw with book palette is safe.
- **HNSW** (#4): Malkov & Yashunin figure is geometric/topological; the structural concept is in the public domain.
- **MoE routing** (#6): GShard / DeepSeek diagrams show the same abstract routing pattern in many forms; safe to redraw.
- **ColBERT MaxSim** (#3): the figure is essentially a matrix-product schematic; pure math.
- **NVL72 rack** (#25): NVIDIA whitepapers are technical reference; rack topologies are factual. A simplified redraw is fine.
- **Vector DB internals** (#14): components and dataflow are common across vendors (Pinecone, Milvus, Qdrant, Vespa); a "canonical vector DB" diagram synthesized from open docs is safe.

### Redraw with care (figure has distinctive visual treatment)

- **BLIP-2 Q-Former** (#1): the Salesforce Fig 2 has a very specific visual style (boxed sections, query-token vectors). **Redraw using book palette and the structural information ONLY**: query tokens, cross-attention from queries to vision features, separate vision-language objectives. Don't reuse colors, font, or border treatments.
- **Flamingo** (#2): DeepMind Fig 3 has a recognizable "gated cross-attention" symbol. Use a different gate-symbol convention (e.g., a *gated-merge* node rather than DeepMind's tanh-gate triangle). State "Inspired by Alayrac et al. (2022)" in the caption.
- **Whisper** (#23): OpenAI's Whisper diagram has a distinctive cross-attention layout. Redraw with generic encoder-decoder layout + clear cross-attention arrows; cite source.

### Potentially closer to source than typical (extra caution)

- **NeRF** (#10): Mildenhall et al. Fig 2 is iconic; many redraws have appeared in textbooks and survey papers, suggesting fair-use precedent. Still, use a different ray-sampling visualization (e.g., 3 rays through 5 points rather than NeRF's 16 points). Cite original.
- **PagedAttention** (#9): the vLLM Fig 5 page-table visualization is distinctive. Redraw with a generic page-table convention (similar to OS textbook page-table diagrams) and cite Kwon et al.

### Avoid copying outright (these are tempting but risky)

- The exact 2:4 sparsity visualization from NVIDIA Ampere whitepaper (#20) has a specific color/shading scheme that should be replaced.
- DeepSeek-V3 architecture diagrams have a distinctive layout; redraw at a more abstract level (do not reproduce the specific layer arrangement verbatim).

### General redraw rules to enforce

1. **No logos, brand assets, or product names as visual elements** (text labels are fine if factual).
2. **Use the book's navy/green/amber/purple palette** consistently (per `wave25_diagrams.md` reference standards).
3. **Replace serif fonts with the book's sans-serif** (System UI / Segoe UI / equivalent).
4. **Caption discipline**: every redraw says "Inspired by [Author, year]" or "Synthesized from [open docs]". Caption-sentence states the takeaway.
5. **Box / arrow / label count ≤ 12 boxes** unless the concept genuinely requires more (per Chapter 59 reference standard).
6. **Internal sub-structures abstracted away** when not load-bearing for the pedagogy (e.g., don't show every attention head in a multi-head block — show one head + "× N heads" note).
7. **Each diagram has a `<figcaption><strong>Figure N.M.K</strong>` *outside* the SVG**, not baked into the SVG as `<text>` (per `wave25_diagrams.md` style audit).

---

## 5. Suggested implementation order

If the team works through this list sequentially, optimal grouping is:

1. **Sprint 1 (multimodal architecture gap)**: #1 Q-Former, #2 Flamingo Resampler, #11 VLM-for-documents pipeline, #18 MLLM eval pipeline. All four sit in Chapter 22-23 and would unify the multimodal-connector visual story.
2. **Sprint 2 (retrieval architectures)**: #3 ColBERT MaxSim, #4 HNSW, #14 vector DB internals, #15 hybrid retrieval, #16 Self-RAG, #17 RAG-Fusion. Six diagrams that turn Chapter 31-35 from "RAG is a flow of boxes" into "I understand each retrieval-architecture's mechanism."
3. **Sprint 3 (foundational architecture detail)**: #5 Mamba, #6 MoE all-to-all, #27 RoPE rotation, #29 LoRA matrix decomposition. Foundation Chapter 3 + Chapter 6 + Chapter 17 close their last architecture-detail gaps.
4. **Sprint 4 (systems and inference)**: #7 GPU hierarchy, #9 vLLM internals, #19 disaggregated serving, #20 2:4 sparsity, #25 NVL72 rack. Chapter 9, 57-58 systems story becomes complete.
5. **Sprint 5 (training paradigm completeness)**: #8 GRPO, #13 RLVR loop. Final two training-paradigm gaps in Chapter 18.
6. **Sprint 6 (lower priority, opportunistic)**: 26-40. Mostly secondary value; tackle as time permits.

Each sprint is 4-6 SVG diagrams at the book's quality bar (≤12 boxes, book palette, takeaway-sentence figcaption). At ~30-45 minutes per diagram if reusing the Chapter 59 template family, a sprint is ~3-4 hours of focused work.

---

## 6. What I deliberately did *not* include

To stay within the requested ~30-50 recommendation budget, I left out:

- **Cartoon "illustration" opportunities** (these belong in a separate "fun-note / opener illustration" pass per the existing audits).
- **Re-skin requests** for the 10 tile-map SVGs in Ch 41/56/61 (already exhaustively documented in `wave25_diagrams.md`).
- **Plot/chart improvements** (matplotlib-style scaling-law plots, benchmark comparison bar charts). These belong in a separate "quantitative figure" pass.
- **Industry-specific pipeline diagrams** in Part 14 (manufacturing, legal, healthcare). Each industry chapter could use one or two, but the impact-per-diagram is much lower than the foundational-architecture gaps above.
- **Section openers / hero images**. The book already has a strong illustrations layer; this audit targets architecture-and-flow diagrams specifically.

---

## 7. Methodology notes (for next auditor)

- Read each of the 40 candidate sections directly.
- Cross-referenced with `UNIMPLEMENTED_VISUALS.md` (May 2026) to avoid duplicating the 9 truly-empty sections (those are already tracked there; mostly low-priority tools-of-the-trade catalog sections).
- Cross-referenced with `wave25_diagrams.md` (May 2026) to avoid duplicating the 10 tile-map re-skin opportunities (those are visual-identity fixes, not architecture-content gaps).
- Cross-referenced with `VISUAL_LEARNING.md` and `ILLUSTRATOR_R2.md` to confirm those passes did not already land the diagrams in this list.
- Quality bar: `section-3.1.html` Figure 3.1.5 (residual stream branch-and-merge), `section-59.1.html` Figure 59.1.1 (three axes of parallelism), and `section-59.1.html` Figure 59.1.2 (interconnect hierarchy) per `wave25_diagrams.md`'s reference triad.
