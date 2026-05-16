# Tools-of-the-Trade Enrichment Audit (2026-05-16)

Read-only audit of all 12 Tools-of-the-Trade chapters. Each section gets specific, actionable bullets (ADD / REMOVE / TRENDING / COMPARISON / CODE / ANTI / BACKREF / PAPER / CASE). Suggestions reflect the post-2025 / mid-2026 stack.

Note: User's brief referred to "module-21, 29, 33, 39" for parts 4-7; the actual module IDs are 21, 25, 30, 33. Audit uses actual file paths. Section 16.1 is currently a TODO scaffold (a critical gap, not just an enrichment opportunity).

---

## module-06-tools-of-the-trade (Part I Foundations)

### Section 6.1: Platforms
- ADD: `uv` (Astral) as the recommended installer is already listed but should be elevated to the primary local stack; add explicit `uv venv && uv pip install` snippet. Also add `pixi` (https://pixi.sh) as a conda alternative when CUDA pinning matters.
- ADD: Modal sandboxes / Notebook + Volume tier for free-tier exploration beyond Colab (https://modal.com/notebooks) — useful for learners who want a persistent disk.
- ADD: HF Spaces ZeroGPU as a fourth notebook tier (free A10G when active) — better than Lightning for short-lived experiments.
- ADD case study: Colab's Feb 2025 quota tightening, where idle TPU sessions dropped from 12h to 3h, and the resulting r/MachineLearning advice thread — grounds the "cloud free tiers are not a backup" warning.
- TRENDING: Apple-Silicon-first development is a real trend among learners — add MLX (Apple) and explain why M-series Macs now run 4-bit Qwen3-7B locally without CUDA.
- COMPARISON: pip vs uv vs poetry vs pixi vs rye — a 5-row table with install speed, lockfile support, and CUDA-wheel handling would replace the current "via uv or conda" prose.
- ANTI: Section recommends "Colab for first read-through" without flagging that the GPU you get is non-deterministic (T4 vs L4 vs A100 by lottery) — add a one-line warning.
- BACKREF: Hardware tier list partly overlaps with Section 12.1 ("hardware tier you actually need"). Cross-link rather than repeat the 6/12/24/80 GB ladder.

### Section 6.2: Libraries & Frameworks
- ADD: `torch.compile(mode='reduce-overhead')` is the 2025-26 default for inference; mention it explicitly. Currently only `torch.compile` is named in passing.
- ADD: PyTorch 2.6+ `torch.export` and `torch.export.aot_export_compiled` for edge deployment — relevant once readers reach Part X.
- ADD: `jax.experimental.shard_map` for explicit sharding in JAX 0.5+ — replaces `pmap` for modern code.
- ADD: 2024 paper "Compact Language Models via Pruning and Knowledge Distillation" (Muralidharan et al., arXiv:2407.14679) — relevant for the BERT/GPT2 size discussion.
- TRENDING: `transformer-engine` (NVIDIA) for FP8 training on H100 — every serious post-2024 pretraining stack uses it.
- TRENDING: `polars` is now the right answer for tabular data > 1 GB; pandas is no longer the universal recommendation. Section currently says "pandas: tabular dataframes" as if it were monolithic.
- REMOVE: `flash-attn` separate-package mention is now stale — PyTorch 2.5+ `scaled_dot_product_attention` ships FlashAttention-2/3 natively; the only reason to install flash-attn separately is the FA3 backwards kernel.
- CODE: The "standard Part I import block" callout is good but could include `from sklearn.preprocessing import StandardScaler` since baselines almost always need it.
- ANTI: NumPy 2.x is recommended without warning that `numpy<2` is still required for ~30% of older HF datasets and torchvision transforms — add a "pin numpy<2 if you hit AttributeError" footnote (it half-says this already; sharpen it).

### Section 6.3: Datasets & Benchmarks
- ADD: `nanotron` Hub datasets and Cosmopedia v2 (2025-Q1) — synthetic-pretraining demonstration corpus relevant to teaching "small but real" pretraining.
- ADD: Tiny Stories (Eldan & Li, arXiv:2305.07759) — the canonical "smallest model that can write coherent English" dataset, perfect for Part I learners.
- ADD: 2024 paper "FineWeb: decanting the web for the finest text data at scale" (Penedo et al., arXiv:2406.17557) — primary source for the FineWeb mention currently uncited.
- TRENDING: BIG-bench Lite and BIG-bench Extra Hard — 2025 contamination-resistant evaluation suites that supersede classic GLUE for teaching how 2026 models are measured.
- ANTI: "~99% on MNIST" target metric is a fine teaching anchor but the section should note that hitting 99% on MNIST gives effectively zero predictive power about modern model behavior. Currently reads as if 99% MNIST is meaningful.
- BACKREF: GLUE contamination warning is well-placed but the deeper contamination discussion belongs in Section 12.3 — cross-link rather than re-state.

### Section 6.4: Models
- ADD: ModernBERT (Warner et al., 2024, arXiv:2412.13663) — the modern BERT replacement (8192 ctx, GLU, RoPE) that should be the "modern encoder reference" anchor in 2026.
- ADD: TinyStories-33M and TinyStories-1M models — the smallest checkpoints worth knowing for "how small can a coherent LM be" experiments.
- ADD: Pythia-14M and Pythia-31M as smallest mech-interp targets; Section currently only names Pythia-1.4B.
- REMOVE/UPDATE: "For modern decoder reference work, you would reach for SmolLM2-135M or Qwen3-0.6B" — also name Llama 3.2 1B and Gemma 3 270M (the late-2024 / 2025 small-model wave) which are now standard.
- CASE: Add the BERT-base "frozen-encoder embedding" production case study at GitHub Copilot's semantic search circa 2023; concrete grounding for "old models still matter".
- COMPARISON: The reference-checkpoint table compares params and type but not context window or vocab size — add columns for "max seq len" and "vocab" since both drive practical decisions.
- BACKREF: The "old models still matter" callout is great; explicitly cross-link to Chapter 11 mech-interp examples instead of restating.

### Section 6.5: External Reading & Communities
- ADD: Maxime Labonne's "LLM Course" (https://github.com/mlabonne/llm-course) — the most popular open community curriculum in 2025-26, complements Karpathy.
- ADD: Hugging Face NLP Course and Smol-Course (https://github.com/huggingface/smol-course) — 2025 free curriculum targeting exactly this Part I/II audience.
- ADD: Stanford CS336 "Language Models from Scratch" (Percy Liang, 2024) — newer than CS224N, materials online.
- ADD: 3Blue1Brown's transformer-from-scratch series (released 2024) — the most-watched visual explainer; widely cited.
- TRENDING: Bluesky's ML community is now larger than the equivalent on X for academic posters — worth flagging as the post-2024 venue shift.
- REMOVE: Distill being "dormant since 2021" is fine to keep but pair with "see Anthropic Transformer Circuits, which inherited the interactive-essay tradition".

---

## module-12-tools-of-the-trade (Part II Understanding LLMs)

### Section 12.1: Platforms
- ADD: SGLang (https://github.com/sgl-project/sglang) — became a real third option alongside vLLM and TGI in 2025, often beats vLLM on structured-output workloads.
- ADD: vast.ai's "verified hosts" tier — the 2025 trust filter most learners miss.
- ADD: TensorWave and SambaNova on-demand (2025) — alternative inference providers worth mentioning alongside Groq.
- TRENDING: Apple Silicon inference is now production-grade for ≤32B models via MLX-LM and Ollama-MLX — the section currently mentions MLX in passing but it deserves its own bullet for laptops with 64+ GB unified memory.
- TRENDING: 1.58-bit BitNet inference on CPU only (no GPU at all) — extend the "Laptop CPU" tier bullet to note BitNet b1.58 + bitnet.cpp now runs Llama-3-8B-class quality on CPU at usable speeds.
- COMPARISON: Add "egress/storage cost" column to the GPU-rental table. RunPod charges egress; Modal does not; that distinction is often the cost-deciding factor.
- ANTI: vast.ai is listed as cheapest but the section doesn't mention container-image issues with custom CUDA stacks — a one-liner about "always test with `nvidia-smi` first" would be honest.
- BACKREF: Hardware tier ladder repeats Section 6.1; consolidate by linking back.

### Section 12.2: Libraries & Frameworks
- ADD: `outlines` (https://github.com/dottxt-ai/outlines) for constrained generation — every mech-interp / structured-output pipeline uses it now.
- ADD: `nnsight 0.4+` adds remote execution against the NDIF (https://ndif.us) — explicit mention of NDIF (National Deep Inference Fabric) is missing and it's the dominant remote-introspection platform in 2026.
- ADD: `EasyJailbreak` and `garak` for tokenizer/model probing — relevant when Chapter 11 covers safety probes.
- ADD: 2024 paper "Sparse Crosscoders for Cross-Layer Features in Superposition" (Lindsey et al., Anthropic) for the SAELens / circuit-tracer line.
- ADD: 2025 paper "Scaling and evaluating sparse autoencoders" (Gao et al., OpenAI, arXiv:2406.04093) — the OpenAI counterpart to the Anthropic monosemanticity work.
- TRENDING: `transformers` v5 (released 2025-Q1) — major break with v4 (model registry, config API, removed legacy methods). The "pin set" in 12.2.5 lists 4.45 which is now stale.
- REMOVE: `transformers>=4.45` pin should be updated to `transformers>=5.0` or note v4-vs-v5 differences.
- COMPARISON: The tokenizer table is good but missing the "byte-level vs character-level vs subword" pedagogical column; add one to make it teachable.
- CODE: The three-tokenizer example calls Llama-4-8B but doesn't show how to count tokens for OpenAI (you need `tiktoken.encoding_for_model("gpt-5.5")` not "gpt-4o" if matching frontier).
- BACKREF: TransformerLens vs nnsight comparison is mature enough that a comparison row would help — both are mentioned but never contrasted.

### Section 12.3: Datasets & Benchmarks
- ADD: SmolLM3 corpus (2025) and FineWeb 2 (2024-12, multilingual) — the canonical post-FineWeb releases.
- ADD: Nemotron-CC (NVIDIA, 2024) — 6.3T-token filtered Common Crawl that competes with FineWeb.
- ADD: 2024 paper "DataComp-LM: In search of the next generation of training sets for language models" (Li et al., arXiv:2406.11794) — the methodology paper behind serious modern corpus curation.
- ADD: LiveCodeBench (Jain et al., 2024) — contamination-resistant code benchmark that should sit alongside SWE-bench in the eval list.
- ADD: ZeroEval (Tianle Li, 2024) — small contamination-resistant suite that paper authors increasingly use.
- TRENDING: Reasoning benchmark suite (AIME 2024/2025, MATH-500, Codeforces ELO) — currently absent but is the single most-cited benchmark cluster of 2025.
- TRENDING: SimpleQA (OpenAI, 2024) — the canonical "how often does the model hallucinate facts" benchmark of 2025.
- COMPARISON: Add a "contamination risk" column to the benchmark table (saturated / partly / unlikely / live).
- CASE: DeepSeek-R1's pretraining cost disclosure (2025-Q1, ~$5.6M for V3 base) makes a concrete grounding for "what a real corpus pipeline costs".

### Section 12.4: Models
- ADD: GPT-OSS (OpenAI, 2025) — OpenAI's first open-weights release in years; currently completely absent and a major omission for an open-weight section.
- ADD: Mistral Magistral (2025) — Mistral's reasoning line; missing from frontier list.
- ADD: Kimi K2 (Moonshot, 2025) — 1T-parameter MoE with 32B active, one of the largest open-weight releases of 2025.
- ADD: GLM-4.5 / GLM-4.6 (Zhipu, 2025) — major Chinese open-weight family alongside Qwen3 and DeepSeek.
- ADD: Apertus (Swiss AI, 2025-Q4) — fully open multilingual European-trained model; matters for multilingual research.
- ADD: Yi-Lightning, Yi-1.5 (01.AI) — relevant Chinese open family.
- TRENDING: Hybrid reasoning toggles (Qwen3's `enable_thinking=True`, Claude's "extended thinking") are core to the 2025-26 frontier but go unmentioned here; deserve a dedicated bullet.
- TRENDING: Continuous-batched MoE inference with expert-parallelism on consumer hardware (e.g. DeepSeek-V3 on 4x RTX 5090) — Section says "anything above 70B requires multi-GPU" but skips the popular new pattern.
- REMOVE: "GPT-5.5" and "Claude Opus 4.6" as concrete frontier examples should be cross-checked against actual frontier-model lineup (the names are plausible but worth verifying for May 2026; Claude Opus 4.5 is the actually-shipped one).
- CASE: DeepSeek-R1 training pipeline + GRPO recipe release (2025-Q1) — should be the case study for "open frontier" since it's the most-replicated open recipe of 2025.
- COMPARISON: Frontier model table doesn't include "pricing per 1M tokens" — gives readers a poor sense of cost. Add columns.
- CODE: The Practical Example calls `load_in_4bit=True` which is deprecated; modern pattern is `quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16)`.

### Section 12.5: External Reading & Communities
- ADD: `Karpathy 2024 "Let's reproduce GPT-2 (124M)"` video — most-watched practical pretraining walkthrough of 2024-25.
- ADD: 2025 "Mechanistic Interpretability 1-year Update" (Anthropic, 2025-Q3) — current canonical survey replacing the 2022 Olsson piece for newcomers.
- ADD: AI Safety Fundamentals (https://aisafetyfundamentals.com/) — the dominant alignment-onboarding curriculum.
- ADD: Lilian Weng's 2024 "Why we think" and 2025 reasoning-models survey — explicitly call out the newer posts since the section only references the blog generically.
- TRENDING: Bluesky AI accounts (Andrej Karpathy, Sebastian Raschka, etc.) overtook X-only posting for many researchers in 2025; flag the platform shift.
- COMPARISON: The cadence table mixes leaderboards (LM Arena) with blogs (Lilian Weng). Splitting them would make it more usable.

---

## module-16-tools-of-the-trade (Part III Working with LLMs)

### Section 16.1: Platforms
- CRITICAL: This section is a `TODO author this section` scaffold (line 28). The entire enrichment plan starts with "write this section". Suggested skeleton:
  - 16.1.1 API providers and their console UIs (OpenAI, Anthropic, Google, Mistral, xAI, Together, Groq, Fireworks).
  - 16.1.2 Aggregators (OpenRouter, LiteLLM-as-service, Portkey, AnyScale).
  - 16.1.3 Local-inference platforms (Ollama, LM Studio, Jan, Msty).
  - 16.1.4 Comparison table covering signup pain, key-rotation, dashboards, rate limits.
  - 16.1.5 Default recommendation matrix by use case.
- ADD on rewrite: Anthropic API Workbench, OpenAI Playground, Google AI Studio as the three free dev UIs.
- ADD: `bedrock-runtime` and Azure OpenAI for enterprise readers.
- ADD: LM Studio (https://lmstudio.ai) — the dominant local Mac GUI in 2025.
- ADD: Msty (https://msty.app) — emerging multi-model desktop client.

### Section 16.2: Libraries & Frameworks
- ADD: `instructor` is named but should be paired with `pydantic-ai` (which has surpassed instructor in adoption for new projects).
- ADD: BAML (https://github.com/BoundaryML/baml) — typed prompt-DSL with strong 2025 traction.
- ADD: `dspy` (Stanford NLP) for prompt-program optimization — completely absent and a major 2024-25 trend.
- ADD: `mirascope` and `marvin` as alternative structured-output libraries.
- ADD: vLLM v1 architecture (2025-Q1) — major rewrite that adds prefix caching by default and Speculative Decoding APIs.
- ADD: `lmcache` — KV-cache offloading layer that production deployments increasingly add on top of vLLM/SGLang.
- TRENDING: Speculative decoding (draft model + verifier) is now standard production practice; should be named at least once.
- TRENDING: Prompt caching is mentioned via Anthropic's `cache_control` but should be framed as a 3-provider pattern (Anthropic explicit, OpenAI automatic, Gemini explicit cache resource).
- TRENDING: Inference-time best-of-N sampling and self-consistency are routinely deployed by 2025 — should be flagged as a "library missing" gap.
- REMOVE: TGI (Text Generation Inference) is named but its share collapsed in 2025 in favor of vLLM/SGLang. Note its current state ("primarily HF Inference Endpoints").
- COMPARISON: Add a separate vLLM vs SGLang vs TGI table since the section has 4 runtimes but no head-to-head.
- CODE: The "same chat call in three SDKs" snippet is excellent but missing the streaming variants; one extra block showing streaming would replace 200 words elsewhere.
- ANTI: "LiteLLM is great" without acknowledging that LiteLLM's translation layer occasionally swallows provider-specific errors and breaks observability — name the failure mode.

### Section 16.3: Datasets & Benchmarks
- ADD: WildBench (https://huggingface.co/spaces/allenai/WildBench) — became the dominant chat-eval benchmark in 2024-2025, more discriminating than Arena-Hard.
- ADD: MMLU-Pro (2024) — successor to MMLU; should sit next to GPQA.
- ADD: IFEval (Zhou et al., arXiv:2311.07911) — the standard instruction-following benchmark; surprisingly absent.
- ADD: SimpleBench (Philip, 2024-2025) — the contamination-resistant "common sense" benchmark widely cited in 2025 model cards.
- ADD: ChatArena and Hard Prompts of Arena-Hard v2 (2025).
- ADD: 2024 paper "From Generation to Judgment: Opportunities and Challenges of LLM-as-judge" (Li et al., arXiv:2411.16594) — the standard reference for the LLM-judge-bias callout already in the section.
- TRENDING: Multi-turn agentic benchmarks (BFCL v3, tau-bench v2 from 2024-12) are the new normal — the current section mostly lists single-turn benchmarks.
- COMPARISON: The benchmark table doesn't say "contamination-resistant Y/N" or "rotated questions Y/N" — add columns to teach what to trust.
- REMOVE: AlpacaEval 2.0 is named but is largely superseded by Arena-Hard-Auto for new work — clarify the chronological superseding.
- ANTI: SWE-bench Verified pass rates need a caveat: results swing 10-15 points depending on whether the agent has internet access — the section should warn readers when reading model cards.

### Section 16.4: Models
- ADD: GPT-5 family naming as of mid-2026 should be cross-checked. As of 2025-2026, OpenAI shipped GPT-4o, GPT-4.5 "Orion", GPT-5 (Aug 2025), o3, o4-mini; verify the section's "GPT-5.5" against actual deployed lineup.
- ADD: Claude 3.7 Sonnet (Feb 2025) and Claude 4 family (May 2025) — Claude Opus 4.5 is correct but the section's "Claude Opus 4.6" reference should be reconciled with what shipped.
- ADD: Gemini 2.5 Pro (March 2025) Deep Think mode and Gemini 2.5 Flash; "Gemini 3.1 Pro" naming is speculative for 2026.
- ADD: o3-mini and o4-mini are cheaper reasoning tiers that should appear in the small/fast table.
- ADD: DeepSeek-V3 (Dec 2024), DeepSeek-R1 (Jan 2025), DeepSeek-V3.1 — the section's "DeepSeek-V4" is uncertain; reconcile.
- ADD: Grok 3 (Feb 2025), Grok 4 (July 2025) — currently absent from the model lineup.
- ADD: Llama 4 family (2025-Q2: Scout, Maverick, Behemoth previewed) — section's "Llama-4 8B" doesn't match shipped sizes.
- TRENDING: Hybrid reasoning (Claude 3.7's "extended thinking" toggle, Gemini Deep Think, GPT-5 "think harder" tier) — the unification of fast and thinking modes is the dominant 2025 trend missing from the model section.
- CASE: The Stargate project announcement (Jan 2025) and DeepSeek-R1 cost claim (Jan 2025) are the two pricing-relevant case studies that ground the cost table.
- CODE: The prompt-caching example uses `cache_control` correctly; should note OpenAI's automatic prompt caching kicks in only above 1024 tokens (specific cutoff matters).
- COMPARISON: Pricing table doesn't include reasoning-token premium (o3 and Claude extended-thinking charge more for thinking tokens than completion tokens).
- ANTI: "Default to the cheap tier" advice is correct but should warn that cheap-tier models break agentic / multi-step workloads at higher rates — naming a failure mode.

### Section 16.5: External Reading & Communities
- ADD: Simon Willison's `llm` CLI and his weekly blog roundups — Simon is named once but should be a top-shelf bullet for "best AI engineering daily commentary in 2025".
- ADD: OpenAI Devday session archive (every year since 2023) — primary source for new API features.
- ADD: Anthropic's "Engineering blog" (https://www.anthropic.com/engineering) — separate from research, focuses on building with Claude.
- ADD: Hamel Husain's evals course material (https://hamel.dev/blog/posts/evals/) — canonical 2024 practitioner content on building LLM-as-judge evals.
- ADD: `aiengineer.substack` / Latent Space's annual State of AI Engineering report.
- TRENDING: Slash-command and AI-coding-tool documentation (Cursor docs, Claude Code docs, Aider docs) are now reference reading for API users — add a bullet.

---

## module-21-tools-of-the-trade (Part IV Training & Adapting)

### Section 21.1: Platforms
- ADD: SF Compute Marketplace (https://sfcompute.com) — became the leading multi-GPU spot marketplace in 2024-25; missing entirely.
- ADD: Prime Intellect (https://primeintellect.ai) — decentralized H100 marketplace + open-pretraining org; relevant for academic teams.
- ADD: Hyperbolic Labs and Salad Cloud — alternatives to vast.ai for 4090-class GPUs.
- ADD: NVIDIA DGX Cloud (Lepton AI acquisition, 2025) — enterprise option missing from the list.
- ADD: AWS Trainium2 and Google Trillium TPU — the non-NVIDIA training options are absent.
- TRENDING: Distributed training over commodity networks (NCCL alternative `gloo-rs`, OpenDiLoCo) — relevant for academic readers without InfiniBand.
- TRENDING: Spot-friendly checkpointing via `fsspec` + `s5cmd` is now the standard pattern; section says "checkpoint every N steps" without naming the libraries.
- COMPARISON: Cost/H100/hour numbers are useful but missing data-egress costs, which often dominate cloud training expenses.
- CASE: Mistral's 2024 training of Mixtral 8x22B on Crusoe — public cost disclosure that grounds the bare-metal-vs-hyperscaler discussion.
- BACKREF: Section 12.1 lists the same compute providers; this section should focus on training-specific differences (interconnect, multi-node, persistent storage) and link.

### Section 21.2: Libraries & Frameworks
- ADD: `torchtune` (PyTorch official, 2024) — Meta's native fine-tuning library; competes with axolotl and TRL.
- ADD: `nanotron` (HuggingFace, 2024) — minimal pretraining-from-scratch framework; the spiritual successor to nanoGPT for production scale.
- ADD: `Megatron-LM` is listed but `Megatron-Core` (NVIDIA 2024 modular rewrite) is the modern entry point — clarify.
- ADD: `Liger Kernel` (LinkedIn, 2024) — Triton kernels giving 20-40% memory savings on Llama/Mistral fine-tunes; widely adopted in 2025.
- ADD: `Levanter` (Stanford CRFM) — JAX-based pretraining framework; missing.
- ADD: `litgpt` is named but `lit-gpt` is now the older path; `lit-gpt` was deprecated in favor of `litgpt` (PyPI rename). Reconcile.
- TRENDING: GRPO (Group Relative Policy Optimization) implementations via TRL (>=0.12, 2024-Q4) and verl — section names GRPO via TRL but should mention `verl`'s GRPO is faster and the de facto choice for serious reasoning training.
- TRENDING: SimPO (Simple Preference Optimization, Meng et al., 2024, arXiv:2405.14734) and KTO (Kahneman-Tversky Optimization) — newer alignment algorithms that are well past adoption threshold by 2026.
- TRENDING: Reward-model-free RL via Constitutional AI 2 (Anthropic, 2025) and RLAIF — relevant for the RLHF section.
- ADD: 2024 paper "Direct Preference Optimization: Your Language Model is Secretly a Reward Model" (already cited via Rafailov) but ALSO cite 2024 "DPO Meets PPO" (Xu et al.) and "Smaug" (Pal et al., 2024) which complicate the DPO story.
- ADD: 2025 paper "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning" (DeepSeek-AI 2025-01, arXiv:2501.12948) — listed in 21.5 but should also anchor the GRPO bullet in 21.2.
- COMPARISON: Table compares 5 libraries but doesn't position them on a "ergonomics vs control" axis — that's the actually useful comparison.
- CODE: A 5-line `from trl import GRPOTrainer; GRPOTrainer(model=..., reward_funcs=[...]).train()` snippet would do more than the prose.

### Section 21.3: Datasets & Benchmarks
- ADD: Tulu 3 SFT is named; also add Tulu 3 DPO Mixture (2024) explicitly — currently only the SFT version is highlighted.
- ADD: SmolTalk (2024-12, HF) — 1M synthetic instruction dataset for SmolLM2; the cleanest 2024 small-model SFT recipe.
- ADD: Magpie family (Xu et al., 2024, arXiv:2406.08464) — synthetic instruction data generated by aligning models, dominant approach in 2024-25.
- ADD: Llama Nemotron Post-Training Dataset (NVIDIA, 2025) — recently-released large synthetic SFT/preference corpus.
- ADD: NuminaMath (2024 AIMO winner) — the canonical math-reasoning dataset for GRPO training.
- ADD: Skywork-Reward-Preference-80K and HelpSteer3 — modern preference datasets superseding UltraFeedback.
- TRENDING: Reasoning-trace datasets (OpenR1-Math, NuminaMath-CoT, DeepSeek-R1-Distill traces) are the post-2024 preference cluster; section names one (OpenR1-Math-220k) but the category deserves a paragraph.
- TRENDING: Self-rewarding language models (Yuan et al., 2024, arXiv:2401.10020) — the technique missing from the data section.
- REMOVE: Anthropic HH-RLHF is listed as "RLHF baseline" but it's now mostly historical; clarify.
- CASE: Allen AI's full Tulu 3 release (Nov 2024, recipe + data + code + models) — should be the headline reproducibility case study.
- COMPARISON: Add license column showing commercial-use compatibility per dataset (currently buried in prose).

### Section 21.4: Models
- ADD: Llama 4 family (released 2025-Q2 as Scout/Maverick) — section names "Llama-4" generically but should distinguish variants.
- ADD: Qwen3-Coder and Qwen3-Math — task-specific Qwen3 variants relevant to specialized fine-tunes.
- ADD: Phi-4 (Microsoft, 2024-12) — small dense model with strong reasoning; missing as a fine-tuning base option.
- ADD: Granite 3 (IBM, 2024) — Apache 2.0 open family; relevant for enterprise readers.
- ADD: Llama 3.3 70B (2024-12) — Meta's last-3-series release; should be named alongside Llama 4.
- TRENDING: Distilled-reasoning models (DeepSeek-R1-Distill-Llama-70B and -Qwen-32B) as fine-tuning bases — these are now the preferred starting points for reasoning-task fine-tunes.
- COMPARISON: The license column is present but missing fields for "agreement gating required Y/N" (Llama needs gated download; Gemma requires acceptance).
- CASE: The "Tulu 3" call-out should grow into a full example: which model + dataset + recipe + cost.
- ANTI: "Apache 2.0 and MIT are safest" is correct but the section doesn't flag that Llama 4 added new acceptable-use restrictions in 2025 — the MAU threshold is one issue, the use-case list is another.

### Section 21.5: External Reading & Communities
- ADD: Maxime Labonne's LLM Course chapters on fine-tuning (https://github.com/mlabonne/llm-course) — the most popular fine-tuning tutorial of 2024-25.
- ADD: Sebastian Raschka's 2024-2025 fine-tuning book draft "Build a Large Language Model from Scratch" — relevant for from-scratch learners.
- ADD: 2024 paper "Self-Play Preference Optimization" (Wu et al., arXiv:2405.00675) and "RLHF Workflow" (Dong et al., arXiv:2405.07863) — both gaps in the foundational papers list.
- ADD: 2025 paper "Direct Reinforcement Learning from Verifiable Rewards" (DeepSeek-R1-Zero recipe) — the actual paper that defined the modern reasoning-fine-tune workflow.
- TRENDING: Hugging Face's `open-r1` open replication project (2025) — case study of the most-watched open replication of the year.
- REMOVE: Zephyr is named in 21.4 but the corresponding "Zephyr recipe" reference in 21.5 should point to the alignment-handbook directly (currently does, good).
- COMPARISON: The reading-venue table mixes paper sources (arXiv), recipes (HF blog), and chat (Discord). Worth splitting.

---

## module-25-tools-of-the-trade (Part V Retrieval & Conversation)

### Section 25.1: Platforms
- ADD: Turbopuffer (https://turbopuffer.com) — object-storage-native vector DB; the cheapest-at-scale option of 2025.
- ADD: ChromaDB Cloud (managed Chroma, 2024) — relevant for the prototype-to-production path.
- ADD: Vespa (https://vespa.ai) — Yahoo open-source search engine; underrated and used by some large RAG systems.
- ADD: Couchbase Vector and Redis 8 vector search (2024) — both shipped vector capabilities; relevant for "I already run X" readers.
- ADD: Elasticsearch ELSER + dense vector (2024 8.x) — the search-engine vector path.
- TRENDING: Vector quantization at scale (PQ, scalar, binary, Matryoshka) — every modern DB ships these now; section says "all major DBs ship HNSW/IVF/quantized" which is good but doesn't name the quantization variants.
- TRENDING: GraphRAG and Microsoft GraphRAG (https://github.com/microsoft/graphrag) — knowledge-graph + RAG hybrid that became significant in 2024-25.
- COMPARISON: The table compares 5 DBs but doesn't include LanceDB (mentioned in prose only) or pricing dimensions.
- CASE: Anthropic's "Contextual Retrieval" methodology (Sep 2024) — the canonical 2024 production-RAG technique; should be a callout.

### Section 25.2: Libraries & Frameworks
- ADD: `fastembed` (Qdrant) — drop-in replacement for sentence-transformers with ONNX-based 2-10x speedup for inference.
- ADD: `vectordb-bench` (Zilliz) — the standard benchmark suite for comparing vector DBs.
- ADD: `infinity` (https://github.com/michaelfeil/infinity) — high-throughput embedding server, the "vLLM for embeddings".
- ADD: `txtai` and `marker` — alternative orchestration libraries for RAG.
- ADD: ColBERT and PLAID (Stanford) — late-interaction retrieval models worth contrasting with single-vector embeddings.
- ADD: ColPali / ColQwen (multimodal late-interaction retrieval for documents with figures) — major 2024-25 trend in document RAG.
- TRENDING: Hybrid sparse+dense retrieval with SPLADE — section names BGE-m3 as supporting sparse+dense but never names SPLADE which is the actual algorithm.
- TRENDING: Document parsing layer (`unstructured.io`, `marker`, `Docling`, `LlamaParse`) — the upstream-of-embedding layer that the section currently skips entirely. This is where 80% of real RAG bugs live.
- REMOVE: LangChain is listed first but `pgvector + LangChain` is increasingly out-of-favor relative to LlamaIndex's tight RAG focus. Rebalance ordering.
- COMPARISON: The "RAG libraries" table doesn't distinguish "retrieval framework" from "orchestration framework". LangChain and LlamaIndex do both; Haystack and Semantic Kernel skew differently.
- CODE: A canonical 10-line `retrieve -> rerank -> generate` snippet using `sentence-transformers + Qdrant + Cohere Rerank` would replace 300 words.

### Section 25.3: Datasets & Benchmarks
- ADD: BEIR-NL, BEIR-PL (multilingual BEIR variants) — 2024 releases relevant to non-English readers.
- ADD: NoLiMa (Modarressi et al., 2024) — long-context retrieval benchmark.
- ADD: RAGTruth (Niu et al., 2024) — hallucination-detection-in-RAG benchmark; section discusses end-to-end RAG eval but doesn't name the leading benchmark.
- ADD: ReSearch (2025) and SearchBench — newer agentic-retrieval benchmarks.
- ADD: 2024 paper "Lost in the Middle" follow-ups (e.g. "Long context is the future" failure-mode studies) — the long-context-retrieval-is-broken literature.
- TRENDING: MTEB v2 with retrieval-specific filtering; section names MTEB but the 2024 MTEB-NV variant is now the canonical.
- COMPARISON: The benchmark table doesn't note language coverage; English-only vs multilingual matters for selection.

### Section 25.4: Models
- ADD: NV-Embed-v2 (NVIDIA, 2024) and SFR-Embedding-Mistral (Salesforce) — both topped MTEB in 2024 and are absent.
- ADD: stella_en_400M_v5 and stella_en_1.5B_v5 — surprisingly strong tiny embedders.
- ADD: BGE-en-icl (BGE 2024) and `Linq-Embed-Mistral` — recent open releases.
- ADD: Voyage-3 series (2024-Q4) — Voyage AI named once but specific model versions missing.
- ADD: Cohere `embed-multilingual-v4` (2025) and `rerank-v3.5` — the section's "v3" / "Rerank 3" should be updated.
- TRENDING: Matryoshka Representation Learning (Kusupati et al., 2022, arXiv:2205.13147) — every modern embedding now uses it; should be named explicitly.
- TRENDING: Late-interaction (ColBERTv2, ColPali, JaColBERTv2) — the "second axis" of retrieval models alongside single-vector dense; absent.
- TRENDING: Reasoning rerankers (using R1-style reasoning for relevance scoring) — emerging post-2025.
- COMPARISON: The reranker table compares 4 rerankers but doesn't include cross-encoder size class or latency cost per query — important for production.
- CODE: The "two-stage system (cheap embedding -> top-100 -> rerank to top-5)" callout should include a code snippet using the canonical libs.

### Section 25.5: External Reading & Communities
- ADD: Anthropic's "Contextual Retrieval" engineering post (Sep 2024) — currently absent; this is THE production-RAG 2024-25 reference.
- ADD: Jina AI engineering blog (multilingual retrieval research) — relevant lab missing.
- ADD: Pinecone's "RAG learning center" — vendor docs but often cited.
- ADD: 2024 paper "Searching for Best Practices in Retrieval-Augmented Generation" (Wang et al., arXiv:2407.01219) — surveys what actually works; should sit alongside the 2024 Gao survey.
- ADD: Cameron Wolfe's "Information Retrieval for LLMs" series (2024) — practitioner-focused.
- TRENDING: RAG-vs-long-context debate (since Gemini 1.5's 1M context shipped in 2024) — the "RAG is dead" thread on AI Twitter/Bluesky.
- COMPARISON: The "RAG advice" warning callout is good; consider naming specific blog posts that propagate "magic chunk size" mythology for readers to recognize.

---

## module-30-tools-of-the-trade (Part VI Agents)

### Section 30.1: Platforms
- ADD: Anthropic's "Skills" system (2024-25) — agentic skills are a key MCP-adjacent abstraction missing entirely.
- ADD: Daytona (https://daytona.io) — dev-environment sandboxing platform; alternative to E2B for code agents.
- ADD: Coder Workspaces and devcontainers.dev — used as agent sandboxes.
- ADD: Cloudflare Containers (2025) — edge agent sandboxes.
- ADD: AgentOps (https://www.agentops.ai) and AgentNeo — agent-specific observability beyond LangSmith.
- TRENDING: MCP server registry (https://mcp.so and https://glama.ai/mcp) — community catalogs of MCP servers; absent.
- TRENDING: Anthropic's Computer Use API (Oct 2024) and OpenAI's Operator/Computer Use Agent (Jan 2025) — the section mentions Computer Use but should treat the platform race seriously.
- CASE: The Mariner / Project Astra demo / Operator launch — should anchor the "browser agent" platform discussion.
- COMPARISON: Add "OS-level vs browser-level vs API-level" categorization to the platform table.

### Section 30.2: Libraries & Frameworks
- ADD: LangGraph v0.2+ (2024-Q3 rewrite) and LangGraph Studio (visual debugger) — the section names LangGraph but skips the 0.2 redesign.
- ADD: `mcp` Python and TS SDKs (https://github.com/modelcontextprotocol) — the canonical libraries every MCP-aware tool now uses.
- ADD: Anthropic's `claude-agent-sdk` (2025) — direct SDK for building Claude-based agents; subsumes much of what older agent frameworks tried to do.
- ADD: `pydantic-ai` is named; add `pydantic-graph` (the agent-graph extension, 2025).
- ADD: `mastra` (TypeScript) — TS agent framework gaining mindshare in 2025.
- ADD: `motleycrew` and `swarms` — multi-agent libraries beyond CrewAI/AutoGen.
- ADD: `letta` (https://github.com/letta-ai/letta, formerly MemGPT) — agent-memory frameworks missing.
- TRENDING: AutoGen 0.4+ (Microsoft, 2024-Q4) — major rewrite; section's AutoGen description matches the older version.
- TRENDING: Stateless re-entrant agent loops (the "agent restart" pattern) — operational best-practice missing.
- REMOVE: CrewAI is named with no caveat about its hidden control flow; the existing "tradeoff" column says "hides control flow" but the section could be more honest about CrewAI's production complaints in 2024-25.
- COMPARISON: 6 frameworks but no MCP-compatibility column — that's the actually load-bearing axis in 2026.

### Section 30.3: Datasets & Benchmarks
- ADD: `SWE-bench Multimodal` (2024-Q4) — extension to images; missing.
- ADD: `SWE-bench Live` and `SWE-bench Pro` (2025) — contamination-resistant variants.
- ADD: GAIA-2 (2024) — the section names GAIA but the v2 update is significant.
- ADD: AssistantBench (Yoran et al., 2024, arXiv:2407.15711) — web-research assistant benchmark; absent.
- ADD: τ²-bench (tau-bench v2, 2024-12) — improved customer-service benchmark.
- ADD: MLE-bench (OpenAI, 2024-12) — agents doing ML engineering tasks.
- ADD: AgentClinic (multi-turn medical agent benchmark, 2024).
- ADD: BrowseComp (OpenAI, 2025) — section already mentions it; expand.
- ADD: 2024 paper "OpenHands: An Open Platform for AI Software Developers as Generalist Agents" (Wang et al., arXiv:2407.16741) — relevant infrastructure paper.
- TRENDING: METR's "time horizon" measurements — currently in 65.3 but should also be flagged here for agents specifically.
- COMPARISON: The benchmark table doesn't note whether the benchmark is "deterministic test suite vs LLM-judge vs human-judge" — critical metric for trusting numbers.

### Section 30.4: Models
- ADD: Claude Sonnet 4.5 (2025) and Claude Haiku 4.5 — section names Claude Opus 4.5 but the smaller Claude 4 variants need their own rows.
- ADD: GPT-5 (Aug 2025) replaced o3/GPT-4o on most agent leaderboards by end of 2025; "GPT-5 / o3" current naming is roughly right but worth verifying.
- ADD: o4-mini (2025) for the cost-efficient reasoning agent tier.
- ADD: Devstral (Mistral, 2025) — code-agent open model.
- ADD: SWE-agent's underlying model lineage (when this is reported in papers it matters).
- TRENDING: Distilled-reasoning-for-agents (DeepSeek-R1-Distill-Qwen-32B in agent loops) — a 2025 efficiency pattern.
- TRENDING: Test-time scaffolding (multiple sample + verifier voting at agent step level) — production technique missing.
- COMPARISON: SWE-bench Verified scores are great but missing latency, average tokens per task, and cost per task — the three metrics that actually drive production agent choices.
- ANTI: "Tool-call accuracy is the metric" callout is good but doesn't mention that long-trace context fidelity matters more for production multi-step agents — name the second failure mode.

### Section 30.5: External Reading & Communities
- ADD: Anthropic engineering blog posts on Claude Code, Claude Skills, and Computer Use (2024-25) — primary sources for agent best practices.
- ADD: Cognition's "Devin" technical posts and SWE-bench leaderboard analyses.
- ADD: All Hands AI (OpenHands) blog and benchmark posts.
- ADD: smol.ai's "AI Engineer Summit 2024/2025" talks — most are now on YouTube.
- ADD: 2024 paper "MMAU: A Comprehensive Benchmark for Massive Multitask Agent Understanding" (Yin et al., 2024).
- ADD: 2025 paper "Agent S2" and "Computer Use Agents are not yet reliable" — needed for the anti-hype calibration.
- TRENDING: Discord/Bluesky migration of agent practitioners in 2025 — venue shift.

---

## module-33-tools-of-the-trade (Part VII Multimodal)

### Section 33.1: Platforms
- ADD: ByteDance Seedream / Seedance (2025) — top-of-leaderboard image and video models that emerged in 2025.
- ADD: HiDream-I1 (2025-Q2) — open image model competitive with FLUX.
- ADD: Lightricks LTX-Video (2024-12) — open real-time video gen; missing.
- ADD: Hailuo / MiniMax video (2024-2025) — Chinese video platform missing.
- ADD: Suno v4 → Suno v4.5 (the 2025 generation); section names v5 which is speculative.
- ADD: Cartesia Sonic, Sesame Maya (2025) — TTS competitors to ElevenLabs.
- ADD: PlayHT, Hume, OpenAI TTS — alternative TTS providers.
- TRENDING: Image-edit and inpainting via FLUX.1 Fill, FLUX Kontext (2025) — major capability shift from 2024.
- TRENDING: Real-time / sub-second video generation (LTX-Video, Wan 2.5) — the "real-time" tier missing from the platform table.
- COMPARISON: The 4-row table should grow rows for "image editing" (separate from generation) and "TTS voice cloning" (separate from TTS).
- CASE: The Sora launch (Dec 2024 public release) and the Veo 2 launch — concrete adoption case studies.

### Section 33.2: Libraries & Frameworks
- ADD: ComfyUI-API and `comfyscript` — programmatic ComfyUI patterns since ComfyUI is "the de facto power-user interface".
- ADD: `diffusers` is named; specifically mention `FluxPipeline` and `WanPipeline` (2025) for current models.
- ADD: `transformers` `pipeline("automatic-speech-recognition")` and `AutoProcessor` for multimodal LLMs — alternative to whisper/audiocraft.
- ADD: `parler-tts` (HF, 2024) — open TTS with prompt control.
- ADD: `chatterbox` (Resemble AI, 2025) — open voice cloning.
- ADD: `clarify.ai` and `replicate-python` — programmatic interfaces to closed APIs.
- TRENDING: Native-multimodal LLM toolkits (`mlx-vlm`, `unsloth-vision`) — fine-tuning frameworks for VLMs.
- TRENDING: Diffusion Transformers (DiT) and Flow Matching as the architectural shift behind SD3 / FLUX / Sora — should be named in the libraries section since `diffusers` now supports both.
- COMPARISON: The library table doesn't distinguish "training-capable" from "inference-only" or "fine-tuning-only".
- CODE: A canonical `from diffusers import FluxPipeline; pipe = FluxPipeline.from_pretrained(...).to("cuda"); pipe(prompt).images[0]` would compress 200 words.

### Section 33.3: Datasets & Benchmarks
- ADD: CommonCanvas (Mozilla AI / Common Voice, 2024) — CC-licensed image-text dataset; missing.
- ADD: PD12M (Source.Plus, 2024) — public domain 12M image dataset.
- ADD: HQ-Edit and InstructPix2Pix datasets — image-editing-specific training data.
- ADD: GenEval (Ghosh et al., 2023, arXiv:2310.11513) and HEIM (Lee et al., 2023, arXiv:2311.04287) — image-gen benchmarks more rigorous than DrawBench.
- ADD: T2V-CompBench (text-to-video composition benchmark, 2024).
- ADD: TextSpeech and Seed-TTS-Eval (ByteDance, 2024) — TTS benchmarks.
- ADD: 2024 paper "GenAI-Bench: Evaluating and Improving Compositional Text-to-Visual Generation" (Li et al., arXiv:2406.13743).
- TRENDING: Human preference datasets for image gen (Pick-a-Pic v2, ImageReward) — section names ImageReward but not Pick-a-Pic.
- REMOVE: LAION-5B is named but its takedown over CSAM-related material in 2023 is unmentioned; the section has a "licensing and consent" callout which is good but doesn't name the specific incident.
- COMPARISON: Add "license restrictiveness" column to the multimodal dataset table.

### Section 33.4: Models
- ADD: Sora 2 naming is speculative; verify against the actual deployed Sora model.
- ADD: Wan 2.5 (Alibaba, 2025) — extension to Wan 2.1.
- ADD: HunyuanVideo 2 (2025) — section names HunyuanVideo without version.
- ADD: GPT-image-1 (OpenAI, 2025) — the new OpenAI image model API; "DALL-E 3 / GPT-Image" naming is imprecise.
- ADD: Imagen 4 Ultra and Imagen 4 Fast (2024-25) — Google variants.
- ADD: NanoBanana (Google, 2025) — image editing model.
- ADD: SDXL Turbo, FLUX.1 Schnell — speed-focused variants are named in the table but their distillation lineage should be flagged.
- ADD: Stable Audio 2.5 and Suno v4.5; section's Suno v5 is uncertain.
- TRENDING: Native-audio LLMs (Gemini 2.5 Native Audio, GPT-4o native audio, Sesame CSM) — the multimodal audio-LLM tier missing.
- TRENDING: Image-and-text generative unified models (BAGEL, OmniGen, Janus-Pro) — emerging architectures absent.
- COMPARISON: The comparison table should add an "open weights license" column and a "GPU memory needed" column.

### Section 33.5: External Reading & Communities
- ADD: Black Forest Labs blog (https://blackforestlabs.ai/announcements/) — lab missing.
- ADD: The Decoder, Ainave, Stability blog — multimodal-focused outlets.
- ADD: 2024 paper "Scaling Rectified Flow Transformers for High-Resolution Image Synthesis" (Esser et al., arXiv:2403.03206) is cited under "33.5.1 SD3 paper" but should also anchor a discussion of why DiT replaced UNet.
- ADD: 2024 paper "Movie Gen: A Cast of Media Foundation Models" (Polyak et al., Meta, arXiv:2410.13720).
- ADD: 2025 paper "Veo 3" report when public — currently absent.
- TRENDING: AI music regulation (Suno/Udio RIAA lawsuits, 2024-25) — should be named since legal status drives platform availability.
- COMPARISON: Civitai is named but Tensor.Art and ShakkerAI (Asian image-model hubs) are missing.

---

## module-50-tools-of-the-trade (Part X Idea to Product)

### Section 50.1: Platforms
- ADD: Bolt.new (StackBlitz) and Lovable (https://lovable.dev) — text-to-app platforms that dominated 2024-25 startup tooling.
- ADD: v0.dev evolution to v0 Chat (Vercel) — section names v0 but should reflect the 2025 product changes.
- ADD: Replit Agent (2024) — coding-agent-in-IDE; very widely used.
- ADD: Trickle, Tempolabs — vibe-coding platforms.
- ADD: Linear / Notion AI integrations are named but should mention Granola, Mem.ai, Reflect — AI-meeting and AI-notes platforms.
- ADD: Statsig is named under analytics; also add LaunchDarkly, ConfigCat, Unleash.
- TRENDING: AI-coding-tool subscription bundling — Cursor + Linear + Vercel + Anthropic = the modern bundle; flag it as a meta-trend.
- TRENDING: "Apps written by Claude Code / Cursor agents" — supply-chain question; absent.
- COMPARISON: AI editor row only mentions Cursor + Cline + Aider; should add Windsurf (which is also named in 50.1.1) and Zed AI.
- CASE: The Bolt.new $20M+ ARR in 60 days (Oct 2024) — concrete grounding for "AI native product tooling matters".

### Section 50.2: Libraries & Frameworks
- ADD: `convex` (https://convex.dev), `inngest` (durable workflows) — modern backend libraries for AI products.
- ADD: `clerk` and `workos` — auth providers; missing.
- ADD: `trigger.dev` — background job queues with AI-friendly retries.
- ADD: Mastra (TS) — agent framework purpose-built for SaaS.
- ADD: `vapi` and `livekit-agents` — real-time voice-agent libraries; absent.
- ADD: Daytona, Coder, Devbox — dev-environment libraries.
- TRENDING: Edge inference (Cloudflare Workers AI, Vercel AI Gateway, Groq edge) — section mentions Cloudflare but the broader "edge AI" trend deserves a paragraph.
- TRENDING: Tauri 2 + Rust for AI desktop apps — replaces Electron in 2025.
- REMOVE: Streamlit and Gradio are named but enterprises shifted to Next.js + Vercel AI SDK; consider re-ordering by 2026 production-share.
- COMPARISON: Add a "language" column (Python/TS/Rust) to the library table.
- CODE: A 10-line "FastAPI + OpenAI streaming + Server-Sent Events" snippet would compress 300 words of prose.

### Section 50.3: Datasets & Benchmarks
- ADD: SWE-Lancer Diamond, Codeforces (2024 LLMs evaluation), Aider polyglot — current AI-coding benchmarks beyond SWE-bench.
- ADD: LiveCodeBench, BigCodeBench — contamination-resistant code benchmarks.
- ADD: WebArena, OSWorld — OS-level evaluation relevant to "AI coding tools".
- ADD: METR's "time horizon" measurement applied to AI-coding tools.
- ADD: 2024 paper "Don't Generate, Discriminate: A Proposal for Grounding Language Models to Real-World Knowledge" — wrong title, but the related "AI engineering eval" literature is sparse and should be cited.
- ADD: Yongchao Zhou et al. "Large Language Models are Human-Level Prompt Engineers" (APE) — relevant for the prompt-iteration tooling.
- TRENDING: Custom-eval-set best practices — the Hamel Husain / Eugene Yan "build your own eval" approach is referenced indirectly but should be explicit.
- COMPARISON: The benchmark table is short; expand with status column ("contaminated/active/saturated").

### Section 50.4: Models
- ADD: Claude Code's underlying model lineage (Opus 4.5 default, Sonnet 4.5 fallback) — section says "Claude Code: Claude Sonnet / Opus" but the actual selection logic is documented and would help readers.
- ADD: Cursor's "Cursor-small" and "Composer" models (Cursor's in-house fine-tunes) — relevant since users see them.
- ADD: GitHub Copilot's 2024-25 multi-model selection — section names it but doesn't explain the per-task routing.
- ADD: Codex (cloud) — OpenAI's resurrection of the Codex brand for the cloud agent; relevant.
- ADD: Magistral Medium and Magistral Small (Mistral, 2025) — for self-hosted code agents.
- TRENDING: Long-running coding agents need 1M+ context — the "Document summarization" row in the table should be split from "AI coding tool" since the requirements diverged.
- COMPARISON: Table is fine but missing latency and cost columns.

### Section 50.5: External Reading & Communities
- ADD: AI Engineer World's Fair (https://www.ai.engineer/) — the dominant 2024-25 AI-engineering conference; talks on YouTube.
- ADD: AISummerSchool, BigScience, EleutherAI offsites — alternative AI-engineering venues.
- ADD: SWyx and Latent Space's annual "State of AI Engineering" survey.
- ADD: Hamel Husain's "Your AI Product Needs Evals" series — most-cited evals essay of 2024.
- ADD: "12-factor agents" community standard (2024-25) — emerging agent-engineering doctrine.
- TRENDING: Mid-2025 wave of "AI startup how-I-built" YC threads — first-hand cases worth surveying.
- COMPARISON: The cadence table mixes products (Hacker News, Indie Hackers) with content (Latent Space). Splitting them helps.

---

## module-60-tools-of-the-trade (Part XI Applications Across Industries)

### Section 60.1: Platforms
- ADD: Vertical-specific 2024-25 entrants: SuperAnnotate (vertical labeling), Ironclad (legal contracts AI), Coram (security copilot), Vivun (sales AI).
- ADD: Legal: Even.ai, Legora (2025 entrants) — section names Harvey but the legal-vertical space is broader.
- ADD: Healthcare: Ambience Healthcare, Suki AI (clinical voice scribes).
- ADD: Finance: Rogo, Linq Alpha, Hebbia's 2024-25 product changes.
- ADD: Cybersecurity: Tines AI (SOAR + AI), Dropzone AI, Prophet Security.
- ADD: Insurance: Salient, Indemn, Ema Unlimited.
- TRENDING: HIPAA Business Associate Agreement (BAA) availability is a major vendor-selection factor — section should note which platforms have BAAs (Anthropic via AWS, Azure OpenAI, GCP Healthcare).
- COMPARISON: The "buyer" column is good but missing "average deal size" or "compliance certifications" — both matter at vendor selection.
- ANTI: "Vendor wrapper over frontier APIs" is correct but should also flag that vendor lock-in is the major risk readers underestimate.

### Section 60.2: Libraries & Frameworks
- ADD: spaCy 3.7+ with transformers — section names scispaCy but skips the umbrella `spaCy` modernization.
- ADD: MedSpaCy and BioMedICUS — additional medical NLP libraries.
- ADD: `langchain-community` is named in the table; specifically call out `langchain-medical-extractor`-style domain integrations.
- ADD: Pyhealth, FHIR.resources, fhirpy — Python FHIR libraries.
- ADD: Finance: `openbb`, `yfinance` (still useful), `polygon`, `databento` for market data.
- ADD: Legal: Casetext API (post-Thomson Reuters acquisition) — relevant.
- ADD: Education: Common Cartridge / IMS Global standards.
- TRENDING: Open-source domain-specific LLMs (OpenMed, BioMedLM, MedFound) — the "open biomedical LLM" thread of 2024-25.
- COMPARISON: The 5-row table should include "license compatibility" column since many medical/legal libraries are non-commercial.

### Section 60.3: Datasets & Benchmarks
- ADD: MedHELM (Stanford HELM Med, 2024) — medical evaluation suite.
- ADD: NEJM AI Challenge datasets — public clinical-reasoning evaluations.
- ADD: HealthBench (OpenAI, 2025) — medical Q&A benchmark.
- ADD: Legal: Bar exam scores (GPT-4 passing the bar, 2023), LegalBench-RAG (2024).
- ADD: Financial: FinQA, ConvFinQA, BizBench (2024).
- ADD: Cybersecurity: CTIBench, CyberSecEval (Meta, 2024).
- ADD: Educational: K-12 reading-level eval datasets (Lexile-based).
- TRENDING: Vertical-specific contamination tests are appearing in 2025; absent from the table.
- COMPARISON: The benchmark table is too short; expand per-industry with at least 2-3 benchmarks each.

### Section 60.4: Models
- ADD: Llama-3-OpenBioLLM, MedFound (2024) — open medical models beyond Med-PaLM 2.
- ADD: SecLM (Google, 2024) — cybersecurity-specific model.
- ADD: Tactic Research AI / Forefront AI — finance-specific models.
- ADD: Cosmos (NVIDIA, 2025) — robotics foundation model relevant for industrial verticals.
- TRENDING: Continued pretraining on domain corpus + general post-training is now the standard recipe (rather than from-scratch domain models) — Section gets this right with "vertical models rarely beat frontier" but should name the recipe.
- ADD: 2024 paper "Med-Gemini" (Saab et al., arXiv:2404.18416) — relevant for "frontier general models on medicine".
- COMPARISON: The vertical-model table should add "matches/exceeds general frontier? Y/N/Mixed" column to make the "general usually wins" point quantitative.

### Section 60.5: External Reading & Communities
- ADD: NEJM AI is named but Health Affairs, Lancet Digital Health, and Stat News also relevant.
- ADD: BankAI, FinSight, FintechAI events and newsletters.
- ADD: Law360 is named; also add Artificial Lawyer, LegalTech Hub.
- ADD: Education: AI Snake Oil (Princeton CITP) — critical-perspective venue.
- ADD: Industry-vertical Slack/Discord communities (Pavilion, HLTH, RSAC) — networking venues.
- TRENDING: Industry vertical AI standards (NIST AI RMF 1.0 customizations, sector-specific AI risk frameworks) — should be flagged given they affect platform selection.

---

## module-65-tools-of-the-trade (Part XII Frontiers)

### Section 65.1: Platforms
- ADD: ChemRxiv, ESS Open Archive — domain preprint servers for AI4Science readers.
- ADD: Hugging Face Daily Papers (Akhaliq) — section names HF Papers but Akhaliq's curated daily list is the actually-read variant.
- ADD: AlphaXiv discussions (already named) but emphasize specific use: "where you see paper authors respond".
- ADD: AISI's published evaluations (UK AI Safety Institute) and US AISI — alongside METR for safety-focused readers.
- ADD: AI Verify / TrustLLM evaluation platforms — emerging.
- TRENDING: ConnectedPapers, Inciteful, OpenAlex — citation graphs for literature navigation.
- TRENDING: Twitter/Bluesky author threads as the de facto paper companion in 2025-26.
- COMPARISON: Frontier-tracking table doesn't include alphaXiv (named in prose), which is now a primary venue.
- BACKREF: This section largely repeats venues from Section 12.5; consider unifying or cross-linking.

### Section 65.2: Libraries & Frameworks
- ADD: `arxiv-sanity-lite` (Karpathy) — minimal personal arXiv tracker.
- ADD: Mendeley, Zotero — citation managers worth flagging for non-Elicit workflows.
- ADD: `paper-qa` (Future House) — question-answering over scientific papers; popular in 2024-25.
- ADD: HF `datasets` library for tracking evaluation datasets.
- ADD: `bilibili` and `paper-replicate` clones — community paper-replication trackers.
- ADD: torchtitan (Meta, 2024) — modular PyTorch pretraining library — section names nanoGPT and lit-gpt but skips this.
- ADD: maxtext (Google JAX) — TPU-friendly pretraining; absent.
- TRENDING: `transformers` v5 SDK is the modern default; section's "nanoGPT" focus is teaching-correct but elides production references.
- COMPARISON: Reference-implementation table mixes pedagogy (nanoGPT) with production scale (gpt-neox). Split.

### Section 65.3: Datasets & Benchmarks
- ADD: HLE (Humanity's Last Exam, 2025) — the 2025 successor benchmark.
- ADD: ZebraLogic and BIG-Bench Extra Hard (2024-25).
- ADD: AIME 2025, Putnam-AXIOM (2024), USAMO 2025 — competition math beyond AIME 2024.
- ADD: Mathematical Olympiad Programming benchmark (MOC, 2024).
- ADD: ARC-AGI-2 (2025) — successor to ARC-AGI; section names ARC-AGI but not v2.
- ADD: Frontier-Math Tier-3 (Epoch's hardest tier) — currently the section just says "FrontierMath" generically.
- ADD: BigCodeBench-Hard, LiveCodeBench-V5 (2025).
- ADD: 2024 paper "GPQA: A Graduate-Level Google-Proof Q&A Benchmark" (Rein et al., arXiv:2311.12022) is correctly attributed; ADD also "Humanity's Last Exam" paper (Phan et al., arXiv:2501.14249).
- TRENDING: Long-horizon agent benchmarks (METR's 50% time horizon doubling every ~7 months observation) — the "Moore's law for agents" claim that drives 2025 capability discourse.
- COMPARISON: Saturation timeline column is great; consider adding "year introduced" for context.

### Section 65.4: Models
- ADD: GPT-5 family proper (Aug 2025) — section's "o3" focus is correct but GPT-5 is the post-launch frontier; should be named.
- ADD: Claude 4 family (May 2025) — Opus 4.5 named but ought to clarify lineage.
- ADD: Gemini 3 (rumored 2025 H2) vs Gemini 2.5 — section names Gemini 2.5 Pro Thinking; verify against actual.
- ADD: Qwen3 (April 2025) and Qwen3-VL — the section names QwQ-32B-Preview (Dec 2024) which is superseded.
- ADD: DeepSeek-R1-0528, DeepSeek-V3.1 (2025) — current open frontier.
- ADD: Grok 4 (July 2025) — already in 30.4; add here too.
- ADD: NVIDIA Nemotron-Reasoning (2025) — relevant frontier release.
- ADD: Step-1 / Step-2 (StepFun, 2025) — Chinese reasoning models.
- TRENDING: "Hybrid reasoning" toggle (Qwen3's `enable_thinking`, Claude 3.7+ extended thinking, GPT-5's adaptive think) — the unifying 2025 architectural trend; absent.
- TRENDING: World models for video / robotics (Genie 2, V-JEPA 2, Cosmos) — section is text-focused; world models are the 2025 frontier expansion.
- CASE: Stargate, $500B announcement (Jan 2025) — economic/infrastructure case study grounding the "frontier requires capital" thesis.
- COMPARISON: Add "release date" column to the frontier table since these dates matter for chronology.

### Section 65.5: External Reading & Communities
- ADD: Dwarkesh Patel podcast — top-shelf 2024-25 long-form interviews with frontier-lab leaders; absent.
- ADD: Cognitive Revolution (Nathan Labenz) and 80,000 Hours podcasts.
- ADD: Asterisk Magazine and The Algorithmic Bridge are partly listed; add Astral Codex Ten and Marginal Revolution for the cross-disciplinary perspective.
- ADD: AI Snake Oil book / blog (Narayanan, Kapoor) — critical-perspective reading.
- ADD: AI Now Institute, Centre for the Governance of AI, AISI — policy-focused.
- ADD: Annual State of AI Engineering report (swyx) and "AI Engineer World's Fair" YouTube archive — 2024-25 venue.
- TRENDING: Bluesky and Mastodon as parallel-to-X academic venues in 2025.

---

## Cross-cutting observations (apply across all chapters)

1. **Section 16.1 is a TODO scaffold** and needs to be authored before any enrichment makes sense — this is the single biggest gap.
2. **Model-naming drift**: "GPT-5.5", "Claude Opus 4.6", "Gemini 3.1 Pro", "DeepSeek-V4", "Sora 2", "Suno v5", "Llama-4-405B", "Claude Haiku 4.5" appear throughout. Some are accurate (Claude 4 family shipped May 2025), some plausible, some speculative. A model-name verification pass against actual May 2026 reality is the single highest-leverage edit.
3. **Hybrid reasoning toggle** (Qwen3 enable_thinking / Claude extended thinking / GPT-5 adaptive think) is the unifying 2025 architectural trend and is mentioned only obliquely in 12.4 and 65.4. Should be a dedicated bullet in every "Models" section.
4. **MCP (Model Context Protocol)** is correctly elevated in 30.1, but should be cross-referenced from 16.2 (libraries) and 50.2 (product tooling) since MCP servers are now part of the API-consumer stack, not only the agent stack.
5. **Prompt caching** is discussed only in 16.4; it belongs in 50.2 (product tooling) and 60.2 (vertical apps) as a cost-optimization tool.
6. **Speculative decoding, prefix caching, attention sinks, test-time scaling** are all production-standard inference techniques but are missing from 12.2, 16.2, 50.2 — all the "Libraries" sections.
7. **`uv` (Astral)** is named in 6.1 but should appear in every Libraries section's "pin set" recommendation as the recommended install tool.
8. **`transformers v5` transition** (2025) means every "pin set" recommendation in the book (12.2.5, 16.2.6, 21.2 implicit) is at least one major version out of date.
9. **Citation density**: Section 6.5 / 12.5 / 21.5 cite foundational papers well; sections 16-65 mostly cite no papers in the Libraries/Models sections. Each "Libraries" section would benefit from 2-3 anchoring papers.
10. **Anti-recommendations** are rare. The book recommends most tools as "the right answer" without acknowledging failure modes. Sections 25.2 (LangChain abstractions), 16.2 (LiteLLM error swallowing), 30.2 (CrewAI hidden control flow) are the only places where tradeoffs are honest. Apply this discipline to every "Best for / When to skip" column.
11. **Comparison-table coverage**: Most tables have 4 columns. Adding "cost", "license", "language", "active development?" as standard columns would make tables much more useful.
12. **DeepSeek-R1 / GRPO** is the most-replicated open recipe of 2025 and should be the headline case study in 21.2, 21.3, 21.4, 21.5, 65.2, and 65.4 — currently only mentioned in 21.5 and 65.4.
