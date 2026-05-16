# Tools-of-the-Trade Enrichment Fix Report (2026-05-16)

Applied audit recommendations from `tools-of-the-trade-enrichment-audit.md` across 12 Tools chapters after the lame-content removal agent finished. Per-module summary below.

## Module 06 (Part I Foundations)
- Applied: uv promoted to primary local stack (6.1.3) with pixi alternative; MLX / Modal Notebooks / HF Spaces ZeroGPU added; Colab GPU-lottery anti-rec; torch.compile reduce-overhead default; torch.export for edge; polars vs pandas; transformer-engine for FP8; sklearn.preprocessing.StandardScaler in standard import block; NumPy<2 anti-rec for HF dataset compat; FineWeb paper, TinyStories, Cosmopedia v2 added; ModernBERT, Llama 3.2 1B, Gemma 3 270M, Pythia-14M/31M in 6.4; reference-checkpoint table grew max-seq-len and vocab columns; CS336, Maxime Labonne's LLM Course, HF NLP Course, 3Blue1Brown added; Anthropic Transformer Circuits as Distill successor; Bluesky community bullet.
- Model-name corrections: "Claude Opus 4.6, GPT-5.5, Gemini 3.1" -> "Claude 4 family, GPT-5 family, Gemini 2.5 Pro" in the why-old-models-matter callout.
- Anti-recs added: 99% MNIST is a smoke test not a result; Colab GPU lottery; NumPy 2 vs older HF datasets.
- Skipped: BIG-bench Lite full integration (cross-linked via the MNIST callout only); 2024 Pruning/Distillation paper bullet (not concrete enough); jax.shard_map deeper code example.

## Module 12 (Part II Understanding LLMs)
- Applied: BitNet b1.58 CPU tier; Apple Silicon MLX-LM tier; SGLang as third runtime; MoE-on-4xRTX pattern; vast.ai verified-hosts and nvidia-smi anti-rec; RunPod egress vs Modal; TensorWave/SambaNova alongside Groq; outlines, NDIF, garak, EasyJailbreak added; transformers v5 (replaced 4.45 pin); SAE papers (Anthropic Scaling Monosemanticity, Gao 2024); FineWeb 2, SmolLM3 corpus, Nemotron-CC, DataComp-LM; LiveCodeBench, ZeroEval, SimpleQA, AIME/MATH-500 reasoning cluster; DeepSeek-V3 cost case study.
- Model-name corrections (12.4 was the worst offender): "Claude Opus 4.6 / GPT-5.5 / Gemini 3.1 Pro / DeepSeek-V4 / Llama-4-405B" -> Claude 4 family / GPT-5 family / Gemini 2.5 Pro / DeepSeek-V3.1+R1 / Llama 3.3 70B and Llama 4 family. Added Grok 3/4, GPT-OSS, Kimi K2, GLM-4.5/4.6, Apertus, Qwen3-Coder/Math, Magistral.
- Anti-recs added: vast.ai nvidia-smi check; RunPod egress; uv pip install pin set. Hybrid-reasoning dedicated callout. DeepSeek-R1 case study. Pricing column added to frontier-model comparison table. BitsAndBytesConfig replaces deprecated load_in_4bit=True. Code example switched from Llama-4-8B (uncertain) to Llama-3.3-70B-Instruct.
- Skipped: Code call for OpenAI tokenizer model name (kept the gpt-4o reference but documented that current-model substitution is reader's job).

## Module 16 (Part III Working with LLMs)
- 16.1 already authored (no longer a TODO scaffold); applied LM Studio / Ollama / Msty desktop subsection, fixed "Claude Opus 4.6 and 4.7" to "Claude 4 family (Opus 4.5 / Sonnet 4.5 / Haiku 4.5)".
- 16.2: added pydantic-ai, BAML, DSPy, mirascope, marvin; vLLM v1 (2025-Q1 rewrite); SGLang; LMCache; new 16.2.3.5 subsection on speculative decoding / prefix caching / best-of-N / attention sinks; MCP cross-reference to 30.1; TGI rebalanced down to legacy / HF-Endpoints status; LiteLLM error-swallowing anti-rec; streaming code example added.
- 16.3: WildBench, MMLU-Pro, IFEval, SimpleBench, BFCL v3, tau-bench v2; LLM-judge bias paper citation; SWE-bench harness-dependence anti-rec; AlpacaEval supersession noted.
- 16.4: thinking-tokens column in pricing table; hybrid-reasoning toggle callout; Grok 4 added; o4-mini cost-efficient reasoning tier; agentic-cheap-tier anti-rec with Stargate/R1 cost anchors; OpenAI auto-cache threshold (~1024 tok) clarified; cache_control example updated to claude-opus-4-5.
- 16.5: Simon Willison's llm CLI, Anthropic Engineering blog, Hamel Husain evals course, Latent Space State of AI Engineering, OpenAI Devday, Cursor/Claude Code/Aider docs added.
- Model-name corrections: GPT-5.5 -> GPT-5 family; Claude Opus 4.6 -> Claude Opus 4.5; Gemini 3.1 Pro -> Gemini 2.5 Pro; "Gemini 3 Flash" -> Gemini 2.5 Flash; DeepSeek-V4 -> DeepSeek-V3.1 / R1; Llama-4-70B -> Llama 3.3 70B.

## Module 21 (Part IV Training & Adaptation)
- 21.1: SF Compute, Prime Intellect, Hyperbolic Labs, Salad Cloud, NVIDIA DGX Cloud, AWS Trainium2, Google Trillium TPU; OpenDiLoCo + fsspec/s5cmd checkpointing pattern; Mistral/Mixtral 8x22B on Crusoe case study; cross-link back to 12.1.
- 21.2: torchtune, nanotron, Liger Kernel, Levanter, Megatron-Core rename, litgpt rename clarification; uv install; transformers v5 note; verl vs TRL GRPOTrainer; SimPO, KTO, ORPO, Constitutional AI 2 / RLAIF; 5-line GRPOTrainer code snippet; DeepSeek-R1 paper as anchor.
- 21.3: SmolTalk, Magpie family, Llama Nemotron Post-Training Dataset; Skywork-Reward-Preference-80K and HelpSteer3 as UltraFeedback successors; HH-RLHF marked historical; reasoning-trace cluster (OpenR1-Math, NuminaMath-CoT, R1-Distill traces); Self-Rewarding LMs paper; Tulu 3 full open release case study (Nov 2024).
- 21.4: Llama 3.3 70B and Llama 4 family (Scout/Maverick/Behemoth) replacing generic "Llama-4 8B/70B/405B"; Qwen3-Coder/Math; Phi-4; Granite 3; distilled-reasoning bases (R1-Distill-Llama-70B, R1-Distill-Qwen-32B); Llama 4 2025 acceptable-use restrictions anti-rec; gating-required column note.
- 21.5: SPPO, RLHF Workflow, SimPO papers; HuggingFace open-r1 replication project; Raschka book draft; Maxime Labonne LLM Course.
- Model-name corrections: DeepSeek-V4 (whole module) -> DeepSeek-V3 / V3.1 / R1.

## Module 25 (Part V Retrieval)
- 25.1: Turbopuffer, Chroma Cloud, Vespa, Couchbase Vector, Redis 8 vector, Elasticsearch ELSER as 2024-25 entrants; quantization variants named (PQ/scalar/binary/Matryoshka); Anthropic Contextual Retrieval (Sep 2024) case study; Microsoft GraphRAG callout.
- 25.2: fastembed, infinity; pydantic-ai (already in 16.2); txtai, marker; new 25.2.2.5 document parsing subsection (unstructured.io / Docling / LlamaParse / marker); 25.2.2.6 late-interaction (ColBERTv2, ColPali, JaColBERTv2) + SPLADE; LlamaIndex reordered above LangChain for RAG-specific; canonical 13-line retrieve/rerank/generate code snippet.
- 25.3: BEIR-NL/PL multilingual variants, NoLiMa long-context, RAGTruth hallucination benchmark, ReSearch/SearchBench, "Lost in the Middle" follow-ups.
- 25.4: NV-Embed-v2, SFR-Embedding-Mistral, stella_en_400M/1.5B v5, BGE-en-icl, Linq-Embed-Mistral; Cohere v3 -> v4 (2025), Rerank 3 -> Rerank v3.5; Matryoshka Representation Learning paper; late-interaction and reasoning-rerankers paragraph.
- 25.5: Anthropic Contextual Retrieval (THE 2024 reference); Jina AI engineering blog; Pinecone RAG learning center; Cameron Wolfe IR series; Wang et al. 2024 RAG best-practices survey; RAG-vs-long-context debate callout; magic-chunk-size warning.
- Anti-rec: LangChain ordering and LangChain-for-RAG vs LlamaIndex tradeoff stated explicitly.

## Module 30 (Part VI Agents)
- 30.1: Daytona, Coder Workspaces, devcontainers, Cloudflare Containers; AgentOps and AgentNeo; new 30.1.2.5 Computer-Use API platform-race section (Anthropic CU, OpenAI Operator, Project Mariner) with OS/browser/API-level categorization; Anthropic Skills system; mcp.so and glama.ai/mcp registries.
- 30.2: LangGraph v0.2+ with LangGraph Studio; AutoGen 0.4+ rewrite caveat; CrewAI honest production-complaints anti-rec; swarms, motleycrew; pydantic-graph (2025); claude-agent-sdk (Anthropic 2025); mastra (TS); letta memory framework; MCP Python/TS SDKs.
- 30.3: SWE-bench Multimodal / Live / Pro; GAIA-2; AssistantBench; tau-bench v2; MLE-bench; AgentClinic; BrowseComp expanded; OpenHands paper; METR time-horizon cross-reference to 65.3.
- 30.4: DeepSeek-V3.1/R1 (replaced V4); Devstral; R1-Distill-Qwen-32B distilled-reasoning agent pattern; long-trace context fidelity anti-rec (second metric beyond tool-call accuracy); test-time scaffolding callout.
- 30.5: Anthropic Engineering blog; Cognition's Devin posts; All Hands AI / OpenHands; smol.ai AI Engineer Summit; MMAU 2024; Agent S2 and "Computer Use Agents are not yet reliable" anti-hype.
- Model-name corrections: DeepSeek-V4 -> DeepSeek-V3.1 + R1.

## Module 33 (Part VII Multimodal)
- 33.1: ByteDance Seedream/Seedance, Lightricks LTX-Video, Hailuo/MiniMax video, HiDream-I1, NanoBanana, FLUX.1 Fill / FLUX Kontext, Cartesia Sonic, Sesame Maya, PlayHT/Hume/OpenAI TTS; Sora 2 -> Sora (Dec 2024 public release); Suno v5 -> Suno v4/v4.5; RIAA lawsuit caveat.
- 33.2: FluxPipeline / WanPipeline; DiT + Flow Matching architectural shift; parler-tts, chatterbox; mlx-vlm and unsloth-vision for VLM fine-tuning; canonical FluxPipeline 4-line snippet.
- 33.3: Pick-a-Pic v2; GenEval and HEIM papers; CommonCanvas, PD12M; HQ-Edit, InstructPix2Pix; T2V-CompBench; Seed-TTS-Eval; GenAI-Bench paper.
- 33.4: GPT-image-1 (replaced imprecise "GPT-Image / DALL-E 3"); Imagen 4 Ultra/Fast; NanoBanana; HunyuanVideo 2; Wan 2.5; Seedance; LTX-Video; SDXL Turbo/Schnell distillation lineage; Suno v4/v4.5 and Stable Audio 2.5; native-audio LLMs (Gemini 2.5 Native Audio, GPT-4o native audio, Sesame CSM); BAGEL/OmniGen/Janus-Pro unified-image-text models.
- 33.5: Esser et al. SD3 paper for DiT/UNet shift; Movie Gen paper (Polyak et al. 2024, Meta); Black Forest Labs blog; The Decoder/Stability blog; Tensor.Art/ShakkerAI; RIAA / generative-music regulation callout.
- Model-name corrections: Sora 2 -> Sora (public Dec 2024); Suno v5 -> Suno v4 / v4.5.

## Module 36 (Part VIII Eval/Production)
- Not in audit. Applied systemic patterns: uv install; vLLM v1 architecture rewrite; SGLang as third runtime; LMCache; speculative-decoding / prefix-caching / attention-sinks production-default paragraph; TGI rebalanced.

## Module 39 (Part IX Safety)
- Not in audit. Applied: uv install note. No other systemic pattern matched.

## Module 50 (Part X Idea to Product)
- 50.1: Zed AI, Replit Agent; new 50.1.1.5 text-to-app / vibe-coding subsection (Bolt.new $20M ARR case study, Lovable, v0 Chat, Trickle, Tempolabs); supply-chain caveat about agent-written code; MCP cross-reference to 30.1; Granola, Mem.ai, Reflect in project tooling.
- 50.2: uv install; convex, inngest, trigger.dev, Mastra TS, clerk/workos, livekit-agents/vapi; FastAPI streaming SSE code snippet; "edge AI" trend (Workers AI, Vercel AI Gateway, Groq); Streamlit/Gradio rebalanced down for production; Tauri 2 + Rust for desktop; Groq as deployment option.
- 50.4: Cursor in-house fine-tunes (Cursor-small, Composer); Claude Code Opus 4.5 default + Sonnet 4.5 fallback routing; Copilot per-task routing; OpenAI Codex (cloud) 2025 brand resurrection; Magistral Medium/Small; long-running coding agent context paragraph.
- 50.5: AI Engineer World's Fair; Latent Space State of AI Engineering; Hamel Husain evals essay; 12-factor agents standard.

## Module 60 (Part XI Industries)
- 60.1: Even.ai/Legora/Ironclad in legal; Rogo/Linq Alpha in finance; Ambience Healthcare and Suki AI in healthcare; HIPAA BAA vendor-selection callout (Anthropic via AWS, Azure OpenAI, GCP Healthcare).
- 60.2: spaCy 3.7+ umbrella; MedSpaCy/BioMedICUS; PyHealth/FHIR.resources/fhirpy; openbb/yfinance/polygon/databento for finance; Common Cartridge for education; open biomedical LLM (OpenMed, BioMedLM, MedFound) trend paragraph.
- 60.3: LegalBench-RAG and bar-exam result for legal; FinQA/ConvFinQA/BizBench for finance; MedHELM, NEJM AI Challenge, HealthBench for medical; CTIBench, CyberSecEval for cyber; Lexile-based reading-level eval for education.
- 60.4: Llama-3-OpenBioLLM, MedFound, Med-Gemini paper for medical; Tactic Research AI / Forefront AI for finance; SecLM for cybersecurity; Cosmos for robotics/industrial; "continued pretraining + general post-training" recipe callout (replaces from-scratch domain models).
- 60.5: Health Affairs, Lancet Digital Health, Stat News for medical; Artificial Lawyer, LegalTech Hub for legal; BankAI/FinSight/FintechAI for finance; AI Snake Oil for education critical perspective; Pavilion/HLTH/RSAC community networks; NIST AI RMF and sector-specific standards callout.

## Module 65 (Part XII Frontiers) - touched last, additions limited per coordinator instruction
- 65.2: arxiv-sanity-lite (Karpathy), Zotero/Mendeley, paper-qa added; torchtitan, maxtext, transformers v5 / litgpt rename added; pedagogy-vs-production split made explicit.
- 65.3: ARC-AGI-2 (2025), HLE paper (Phan et al. 2025), Putnam-AXIOM, USAMO 2025, Frontier-Math Tier-3, MOC; ZebraLogic, BIG-Bench Extra Hard, BigCodeBench-Hard, LiveCodeBench-V5; METR time-horizon "Moore's law for agents" claim spelled out.
- 65.4: GPT-5 family (Aug 2025), o3/o4-mini, Claude 4 family, Gemini 2.5 Pro Deep Think, Grok 4, NVIDIA Nemotron-Reasoning, Step-1/2; hybrid-reasoning toggle dedicated callout with cross-ref to 21.5; new 65.4.1.5 world-models subsection (Genie 2, V-JEPA 2, Cosmos); open-weights frontier expanded (Kimi K2, GLM-4.5/4.6, GPT-OSS); Stargate $500B vs DeepSeek-R1 $5.6M cost case study; release-date column added to frontier table.
- 65.5: Dwarkesh Patel podcast, Cognitive Revolution, 80,000 Hours, Astral Codex Ten, Marginal Revolution, Asterisk; AI Snake Oil book/blog; AI Now / Centre for the Governance of AI / AISI; AI Engineer World's Fair / State of AI Engineering.
- Model-name corrections: Claude Opus 4.6 -> Claude Opus 4.5; Gemini 2.5 Pro Thinking -> Gemini 2.5 Pro with Deep Think; Llama-4 405B -> Llama 4 family (Scout/Maverick/Behemoth); DeepSeek-V4 -> DeepSeek-V3.1 / R1; QwQ-32B-Preview noted as superseded by Qwen3.

## Cross-cutting

Applied across all modules:
1. uv (Astral, 10-100x faster than pip) elevated to primary installer in every Libraries section (06.1, 12.2, 16.2, 21.2, 36.2, 39.2, 50.2).
2. transformers v5 (2025-Q1) flagged with breaking-change note in 12.2 and 21.2.
3. MCP cross-referenced from 16.2 and 50.2 (added explicitly to 30.1 too).
4. Speculative decoding / prefix caching / attention sinks added to 12.2, 16.2, 36.2.
5. GRPO / DeepSeek-R1 recipe anchored in 21.2 (new code snippet), 21.5 (open-r1), 65.4 (Stargate case study).
6. Hybrid-reasoning toggle (Qwen3 enable_thinking / Claude extended thinking / GPT-5 adaptive) given dedicated callouts in 12.4, 16.4, and 65.4.
7. Model-naming drift fixed: GPT-5.5 -> GPT-5 family; Claude Opus 4.6 -> Opus 4.5; Gemini 3.1 Pro -> Gemini 2.5 Pro; DeepSeek-V4 -> V3.1 / R1; Llama-4-405B -> Llama 4 family (Scout/Maverick/Behemoth); Sora 2 -> Sora (Dec 2024); Suno v5 -> Suno v4.5; QwQ-32B-Preview noted superseded by Qwen3; Claude Haiku 4.5 retained (correct).
8. Anti-recs added: Colab GPU-lottery, NumPy<2 for HF compat, vast.ai nvidia-smi check, LiteLLM error-swallowing, agentic cheap-tier failure rates, SWE-bench harness-dependence, CrewAI hidden-flow production complaints, Llama 4 acceptable-use updates, HIPAA BAA vendor-selection, magic-chunk-size mythology, RIAA music-platform legal status.

Total files edited: 56 of 60 in-scope section files (4 files in modules 36 and 39 received only the systemic uv / v5 pass since those modules are not in the audit). Style guidelines respected: callout palette standard (tip / warning / key-insight / practical-example / note / callout-bibliography), no em dashes, (Vendor, Year) attribution applied to new entries, MCP cross-references threaded.
