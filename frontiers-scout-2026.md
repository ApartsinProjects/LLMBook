# Frontiers of LLMs, 2026-2027: Scouting Report

Prepared for the closing "Frontiers" Part of an LLM textbook. Citations are real URLs surfaced via web search in May 2026. Each chapter follows the same template: ~5-8 most-cited papers, 3-5 named systems/models/benchmarks, 1-2 production stories, 1-2 representative blog/talk/podcast items, and 2-3 specific open questions where 2026 did not close the book.

---

## Chapter 1: Frontier Architectures & Scaling

Post-transformer architectures, MoE at trillion-parameter scale, 1-bit weight quantization, the emergent-abilities controversy, and where Chinchilla-style scaling laws are being pushed.

### Most-cited 2024-2026 papers
1. Mamba-3: Improved Sequence Modeling using State Space Principles (ICLR 2026). https://arxiv.org/abs/2603.15569 and https://openreview.net/forum?id=HwCvaJOiCj
2. RWKV-7 "Goose" with Expressive Dynamic State Evolution (March 2025). https://arxiv.org/abs/2503.14456
3. DeepSeek-V3 Technical Report (Dec 2024), the foundation of the V4 line. https://arxiv.org/abs/2412.19437
4. BitNet b1.58 (original): The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits. https://arxiv.org/abs/2402.17764
5. BitNet b1.58 2B4T Technical Report (April 2025): first open-source, native 1-bit LLM at the 2B scale. https://arxiv.org/abs/2504.12285
6. 1-bit AI Infra Part 1.1: Fast and Lossless BitNet b1.58 Inference on CPUs (bitnet.cpp). https://arxiv.org/abs/2410.16144
7. Beyond Chinchilla-Optimal: Accounting for Inference in LM Scaling Laws (Sardana et al., 2024). https://arxiv.org/abs/2401.00448
8. A Survey of RWKV (Jan 2025), with comparisons to RetNet, Mamba, and Hyena. https://arxiv.org/abs/2412.14847

### Named systems / models / benchmarks (2025-2026)
- DeepSeek V4 (April 2026): Compressed Sparse Attention (CSA), 1M-token context, trained on 32T+ tokens. https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond and https://particula.tech/blog/deepseek-v4-qwen-open-source-ai-disruption
- Qwen3-235B-A22B (April 2025): 128 experts, top-8 routing, "hybrid reasoning" mode toggle. https://friendli.ai/blog/moe-models-comparison
- BitNet b1.58 2B4T + bitnet.cpp inference framework. https://github.com/microsoft/BitNet
- Liquid AI LFM2.5-350M (April 2026): set a new data-to-parameter ratio record of 80,000:1 (350M params, 28T tokens). https://callsphere.ai/blog/transformer-alternatives-mamba-rwkv-state-space-models-2026
- Qwen3-0.6B (April 2025): 60,000:1 tokens-to-parameters ratio, still the densest small-text model.

### Production / deployment stories
- DeepSeek + Qwen combined market share: from ~1% global AI market share (Jan 2025) to ~15% (Jan 2026), entirely on open-weight MoE families. https://particula.tech/blog/deepseek-v4-qwen-open-source-ai-disruption
- Microsoft's bitnet.cpp deployment: 2.37x to 6.17x x86 CPU speedups and 1.37x to 5.07x ARM CPU speedups for ternary-weight inference, opening genuine CPU-only LLM serving. https://arxiv.org/abs/2410.16144

### Blog / talk / podcast
- Sebastian Raschka, "The Big LLM Architecture Comparison". https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison
- Cameron R. Wolfe, "Scaling Laws for LLMs: From GPT-3 to o3" (Substack). https://cameronrwolfe.substack.com/p/llm-scaling-laws

### Open questions 2026 did NOT settle
1. Whether hybrid SSM/Attention or pure SSM (Mamba-3 MIMO) wins at the 70B+ scale: published Mamba-3 numbers stop at 1.5B and the trillion-token frontier remains transformer-MoE.
2. Whether 1.58-bit weights survive the move from base pretraining to long RL post-training without de-quantization (BitNet b1.58 2B4T pretrains in 1.58 bits but post-training stability at frontier scale is unverified).
3. Whether "emergent abilities" reflect a true phase change in model behavior or are an artifact of metric discontinuity (post-Schaeffer et al. critique, still unresolved as 2026 reasoning models scale test-time compute rather than parameters).

---

## Chapter 2: Frontier Theory & Cognition

Computational-complexity theory of transformers, memory as a first-class primitive, mech-interp at production scale, and when behavior crosses into agency.

### Most-cited 2024-2026 papers
1. Exact Expressive Power of Transformers with Padding (ICLR 2025/26): TC0 upper and lower bound proof. https://openreview.net/forum?id=O1abxStFcy
2. Circuit Complexity Bounds for RoPE-based Transformer Architecture (EMNLP 2025). https://aclanthology.org/2025.emnlp-main.561.pdf
3. Pause Tokens Strictly Increase the Expressivity of Constant-Depth Transformers. https://openreview.net/forum?id=eG5oh8l1WZ
4. Lower Bounds for Chain-of-Thought Reasoning in Hard-Attention Transformers (Feb 2025). https://arxiv.org/abs/2502.02393
5. How Numerical Precision Affects Arithmetical Reasoning Capacity (ACL 2025). https://aclanthology.org/2025.findings-acl.3.pdf
6. A-Mem: Agentic Memory for LLM Agents (Feb 2025). https://arxiv.org/abs/2502.12110
7. Memory for Autonomous LLM Agents: Mechanisms, Evaluation, Emerging Frontiers (March 2026 survey). https://arxiv.org/abs/2603.07670
8. Associative memory inspires improvements for in-context learning (Aug 2025). https://arxiv.org/abs/2412.15113
9. On the Emergence of Induction Heads for In-Context Learning (Musat, Nov 2025). https://arxiv.org/abs/2511.01033

### Named systems / models / benchmarks (2025-2026)
- A-Mem (Xu et al. 2025): semantic-network memory for LLM agents. https://arxiv.org/pdf/2502.12110
- HeLa-Mem (April 2026): Hebbian associative memory for agents. https://arxiv.org/html/2604.16839v1
- CALM (Continual Associative Learning, Nov 2025) preprint pipeline. https://www.preprints.org/manuscript/202511.0430
- Anthropic's Cross-Layer Transcoders (CLTs) for circuit tracing (March 2025): full replacement model of MLPs by sparse, human-readable features. https://medium.com/@adnanmasood/mechanistic-interpretability-explained-circuits-sparse-autoencoders-causal-tracing-and-ai-88ecc8d70b72
- Anthropic's 34M-feature SAE on Claude 3 Sonnet (Scaling Monosemanticity, base for circuit-tracing line). https://learnmechinterp.com/topics/scaling-monosemanticity/

### Production / deployment stories
- Golden Gate Claude (May 2024 -> 24-hour public deploy): first production-scale SAE feature-clamp demo, drove the entire 2025 wave of feature-steering work in safety teams. https://venturebeat.com/ai/anthropic-tricked-claude-into-thinking-it-was-the-golden-gate-bridge-and-other-glimpses-into-the-mysterious-ai-brain
- Humberd et al. (2026, Journal of Management Studies): first peer-reviewed application of agency theory to LLMs as organizational agents, kicked off enterprise governance discussion. https://onlinelibrary.wiley.com/doi/10.1111/joms.13274

### Blog / talk / podcast
- Anthropic Research: "Labor market impacts of AI" (links agency theory to deployed Claude usage). https://www.anthropic.com/research/labor-market-impacts
- "Mechanistic Interpretability Explained: Circuits, Sparse Autoencoders, Causal Tracing, and AI Safety" (April 2026, Adnan Masood). https://medium.com/@adnanmasood/mechanistic-interpretability-explained-circuits-sparse-autoencoders-causal-tracing-and-ai-88ecc8d70b72

### Open questions 2026 did NOT settle
1. Whether SAEs actually carve the model at the joints, or merely produce convenient post-hoc projections: two 2025 papers (Karvonen et al.; Wu et al.) show SAEs underperform simple baselines on concept probing and steering. https://arxiv.org/html/2506.23845v1
2. Whether the TC0 ceiling is binding in practice: chain-of-thought, pause tokens, and looped inference push transformers above TC0 in theory, but no benchmark cleanly separates a "TC0-only" from an "above-TC0" task at frontier model scale.
3. Whether long-horizon memory should live in weights (continual learning), context (1M+ token windows), or external stores (A-Mem-style graphs). The 2026 survey (Memory for Autonomous LLM Agents) explicitly catalogues all five families without naming a winner.

---

## Chapter 3: Frontier Systems & Hardware

Non-NVIDIA silicon, decentralized training, specialized inference kernels, edge deployment, and training-inference co-design.

### Most-cited 2024-2026 papers
1. FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling (March 2026). https://arxiv.org/abs/2603.05451 and https://www.together.ai/blog/flashattention-4
2. DeMo: Decoupled Momentum Optimization (Bowen Peng, Diederik Kingma et al., 2024; v2 Oct 2025), the algorithmic core of decentralized training. https://github.com/NousResearch/DisTrO
3. Challenges and Research Directions for LLM Inference Hardware (Jan 2026 survey). https://arxiv.org/abs/2601.05047
4. Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective (multi-revision through 2025). https://arxiv.org/html/2410.04466v4
5. HERMES: Understanding and Optimizing Multi-Stage AI Inference Pipelines (MIT 2025). https://people.csail.mit.edu/suvinay/pubs/2025.hermes.arxiv.pdf
6. A Review on Edge Large Language Models: Design, Execution, and Applications (ACM Computing Surveys 2025). https://dl.acm.org/doi/full/10.1145/3719664
7. Apple ML Research: Native LLM and MLLM Inference at Scale on Apple Silicon (Jan 2026). https://machinelearning.apple.com/research/iclr-2026

### Named systems / models / benchmarks (2025-2026)
- Cerebras CS-3 wafer-scale system; OpenAI signed a 750 MW, $10B+ supply deal in Jan 2026. https://www.cerebras.ai/blog/cerebras-cs-3-vs-groq-lpu and https://markmancapitalinsight.substack.com/p/cerebras-cbrs-everything-you-need
- Groq LPU (acquired by NVIDIA, Dec 2025, $20B). NVIDIA Vera Rubin "LPX" racks integrate Groq LPUs for inference. https://www.theregister.com/2026/03/16/nvidia_lpx_groq_3/ and https://kbssidhu.substack.com/p/nvidias-20-billion-groq-deal-how
- Tenstorrent (Jim Keller, RISC-V chiplet, $700M raised Dec 2024). https://aimultiple.com/ai-chip-makers
- AMD Instinct MI355X (~6 TBps HBM bandwidth); AWS Trainium 2 GA Dec 2024; Trainium 4 expected late 2026. https://introl.com/blog/ai-accelerators-beyond-gpus-tpu-trainium-gaudi-cerebras
- Nous Research Psyche Network on Solana (Jan 2025), built on DeMo/DisTrO. https://nousresearch.com/nous-psyche/

### Production / deployment stories
- OpenAI -> Cerebras 750 MW deal (Jan 2026): first hyperscaler commitment to wafer-scale silicon as a primary inference fabric. https://markmancapitalinsight.substack.com/p/cerebras-cbrs-everything-you-need
- Apple WWDC 2025 + Ollama switching to MLX as its Apple Silicon inference engine (March 2026): MLX becomes the de facto on-device runtime; ~3B-param Foundation Models ship in iOS via the new framework. https://dev.to/arshtechpro/wwdc-2025-explore-llm-on-apple-silicon-with-mlx-1if7 and https://machinelearning.apple.com/research/apple-foundation-models-2025-updates

### Blog / talk / podcast
- Modal Labs, "We reverse-engineered Flash Attention 4". https://modal.com/blog/reverse-engineer-flash-attention-4
- Chakra Research, "The Third Epoch of AI: Decentralizing the Training Stack" (overview of DeMo, DisTrO, Psyche). https://www.chakra.dev/research/the-third-epoch-of-ai-decentralizing-the-training-stack

### Open questions 2026 did NOT settle
1. Whether decentralized training can produce a frontier model competitive with a centralized hyperscaler run: DeMo v2 hits 1000-10000x bandwidth reduction, but the largest fully-decentralized Psyche run as of 2026 is still mid-size and below GPT-4-class.
2. Whether MoE routing can be made energy-efficient on heterogeneous edge hardware (3D analog-in-memory vs. chiplet-MoE vs. wafer-scale all argue for different topologies, no consensus).
3. Whether the NVIDIA-Groq consolidation forecloses an inference-silicon ecosystem or accelerates it (Cerebras IPO, AMD MI355 ramp, and the AWS Trainium roadmap are the natural test cases through 2027).

---

## Chapter 4: AGI Trajectories & Open Questions

Capability evals, alignment at the frontier, AGI timelines, economic implications, what 2026 actually settled.

### Most-cited 2024-2026 papers
1. Humanity's Last Exam (Phan et al., Jan 2025): 2,500-question multimodal expert benchmark. https://arxiv.org/abs/2501.14249
2. ARC-AGI-2: A New Challenge for Frontier AI Reasoning Systems (Chollet et al., May 2025). https://arxiv.org/abs/2505.11831
3. FrontierMath: A Benchmark for Evaluating Advanced Mathematical Reasoning in AI (Glazer et al., Epoch AI, multi-revision through 2025). https://arxiv.org/html/2411.04872v7
4. Redefining Superalignment: From Weak-to-Strong to Human-AI Co-Alignment (April-June 2025, v5). https://arxiv.org/abs/2504.17404
5. C3AI: Crafting and Evaluating Constitutions for Constitutional AI (ACM Web Conference 2025). https://dl.acm.org/doi/10.1145/3696410.3714705
6. ARC-AGI-3 Technical Report (early 2026): interactive-reasoning benchmark, first format change since 2019. https://arcprize.org/media/ARC_AGI_3_Technical_Report.pdf
7. The AI Skills Shift: Mapping Skill Obsolescence, Emergence, and Transition Pathways in the LLM Era (April 2026). https://arxiv.org/html/2604.06906v1

### Named systems / models / benchmarks (2025-2026)
- HLE (Humanity's Last Exam): top model Gemini 3.1 Pro Preview at 44.7%, GPT-5.5 (xhigh) 44.3%, GPT-5.5 (high) 43.0%. https://agi.safe.ai/ and https://artificialanalysis.ai/evaluations/humanitys-last-exam
- ARC-AGI-2: 24% top Kaggle score for $0.20/task (ARC Prize 2025). https://arcprize.org/blog/arc-prize-2025-results-analysis
- FrontierMath Tier 4 (June 2025): 50 problems; best single-run score 29%, "ever-solved" rate >40% on Tier 1-3 by GPT-5.2 / Claude Opus 4.6. https://epoch.ai/benchmarks/frontiermath-tier-4
- ARC-AGI-3 (planned early 2026): interactive-reasoning successor.
- Anthropic Claude 4 family (2025): explicit agentic targeting, computer use, long-horizon reasoning.

### Production / deployment stories
- Anthropic "Labor market impacts of AI" project: by Dec 2025, 35.9% of U.S. workers used generative AI; ~55K layoffs attributed to AI out of 1.17M total in 2025 (~5%). https://www.anthropic.com/research/labor-market-impacts
- WEF Future of Jobs Report 2025: projects 92M jobs displaced and 170M created by 2030, net +78M. https://www.cio.com/article/4142784/job-disruption-by-ai-remains-limited-and-traditional-metrics-may-be-missing-the-real-impact-2.html

### Blog / talk / podcast
- 80,000 Hours, "What the hell happened with AGI timelines in 2025?" https://80000hours.substack.com/p/what-the-hell-happened-with-agi-timelines
- LessWrong, "A visualization of changing AGI timelines, 2023-2026". https://www.lesswrong.com/posts/Tc5AbEpbFFdNx5nkP/a-visualization-of-changing-agi-timelines-2023-2026
- Stanford HAI, "Stanford AI Experts Predict What Will Happen in 2026". https://hai.stanford.edu/news/stanford-ai-experts-predict-what-will-happen-in-2026

### Open questions 2026 did NOT settle
1. The AGI date itself: Metaculus median has compressed to March 30, 2028, but the 25%/50% probability spread (2029 / 2033) reflects real disagreement; Amodei publicly anchors 2026-27, Hassabis still says ~2030, Polymarket gives only 9% to 2027. https://www.metaculus.com/questions/5121/when-will-the-first-general-ai-system-be-devised-tested-and-publicly-announced/
2. Whether weak-to-strong alignment generalizes to genuinely super-human capabilities: the April 2025 v5 paper claims w2s closes 20-30% of the reasoning gap, but argues no method certifies alignment for true ASI.
3. Whether economic disruption follows the augmentation trajectory (78.7% of Anthropic-measured AI interactions are augmentation, not automation) or whether 2026-27 reasoning agents flip the curve toward displacement; 2.5%-7% U.S. employment-at-risk estimates remain unreconciled.

---

### Cross-cutting notes for the textbook author

- 2026 frontier discourse is dominated by three vectors: post-transformer architectures finally producing benchmark-competitive 3B models (Mamba-3, RWKV-7), MoE swallowing the open-weight market (DeepSeek V4, Qwen3), and test-time compute / reasoning replacing parameter scaling as the headline scaling axis (HLE, FrontierMath, ARC-AGI-2/3 leaderboards).
- The "scaling wall" framing is in retreat; the new wall is inference cost, which drives the Cerebras / Groq / BitNet / FlashAttention-4 cluster of work into one connected story.
- Interpretability has graduated from toy circuits to production-scale feature steering (Golden Gate Claude, CLTs), but the field is openly admitting in late-2025 papers that SAE-vs-baseline gains are smaller than hoped.
- 2027 is positioned to settle: (a) whether non-NVIDIA inference silicon survives the post-Groq consolidation, (b) whether decentralized training crosses the GPT-4 threshold, (c) whether ARC-AGI-3 falls to interactive-reasoning agents, and (d) where on the 2027-2033 spectrum the AGI timeline actually lands.
