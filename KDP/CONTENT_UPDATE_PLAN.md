# Content Update Plan — what's missing from late 2025 / 2026

The book was assembled across many versions; the most recent topical refresh predates several major developments. This plan catalogs them and proposes where each should land.

## How to read this document

For each missing topic:
- **Significance**: why it matters
- **Where it should live**: chapter / section
- **What needs to be added**: new section, new subsection, callout, or just a bibliography entry
- **Effort**: small / medium / large

---

## Missing major developments (late 2025 → mid 2026)

### 1. Reasoning model proliferation beyond o1/o3 and DeepSeek-R1

What's missing:
- DeepSeek-R1 family details (R1, R1-Zero, R1-Distill series): the GRPO training recipe, the public release impact on closed-vs-open frontier perception
- Anthropic's Extended Thinking (Claude 3.7 Sonnet thinking mode, Claude 4.5 reasoning)
- Google's Gemini 2.5 Pro / Flash thinking
- xAI Grok 3/4 reasoning
- Quiet-STaR and self-taught reasoning approaches

Where: **Chapter 8 (Reasoning Models & Test-Time Compute)** — primary home. Add as section 8.7 "The Open-Source Reasoning Wave" or expand 8.2 with a 2025-2026 timeline.

Effort: **medium** (1 new section, ~2000 words, 1 timeline diagram).

### 2. Mixture-of-Experts at frontier scale

What's missing:
- DeepSeek-V3 (671B total / 37B active) architectural details
- Llama 4 / Llama 4.1 MoE (Maverick, Scout, Behemoth)
- Qwen 3 / 3.5 MoE
- Routing innovations: expert specialization, shared experts, Auxiliary-Loss-Free Load Balancing

Where: **Chapter 6 §6.3.7** (existing MoE section is brief; expand) AND **Chapter 7 (Modern LLM Landscape)**.

Effort: **medium** (~1500 words + diagram update).

### 3. Long context (1M+ tokens) and the post-100K-context regime

What's missing:
- Gemini 1.5/2.5 1M-2M token context, real-world failure modes (lost-in-the-middle, context fragmentation)
- Anthropic 1M context for Claude 4.6
- Long-context evaluation: RULER, BABILong, Needle-in-the-haystack maturity
- Streaming/incremental context strategies

Where: **Chapter 9 (Inference Optimization)** §9.2 KV-cache and §9.4 Serving, plus a new dedicated section.

Effort: **large** (new dedicated section ~2500 words, 2 figures: needle benchmark, KV memory growth).

### 4. Agent protocols (MCP maturity, A2A, AGNTCY)

What's missing:
- Model Context Protocol full ecosystem: server registry, security model, transport extensions (HTTP/streamable, OAuth)
- A2A (Agent-to-Agent) protocol (Google) for agent-agent communication
- IBM AGNTCY collective specification
- ACP (Agent Communication Protocol) by Cisco
- The protocol stack standardization wars

Where: **Chapter 23 (Tool Use, Function Calling & Protocols)** — already has §23.2 MCP and §23.3. Update §23.3 to compare A2A, ACP, AGNTCY, and MCP head-to-head.

Effort: **medium** (rewrite §23.3, ~2000 words, 1 protocol-comparison table, 1 architecture diagram).

### 5. Vibe coding and AI-pair-programming maturity

What's missing:
- Cursor 0.5+, Windsurf, Cline, Aider 2.x, Anthropic Claude Code, OpenAI Codex CLI
- The "spec-driven development" paradigm
- Claude Computer Use / Anthropic Browser Tools
- IDE integrations: tab-completion at the CoT/agent level (not just lines)
- Failure modes: phantom edits, context-window blowouts, repo amnesia

Where: **Chapter 25 §25.4 Code/Work Workflows and Agentic Coding** — exists but pre-2026. Refresh with current tooling landscape.

Effort: **medium** (~1500 word refresh, screenshots/diagrams update).

### 6. Multimodal generation: video, 3D, world models

What's missing:
- Sora 2, Veo 3, Kling 2, Runway Gen-4: production-grade text-to-video
- World models for robotics: Gemini Robotics, NVIDIA Cosmos, World Labs
- 3D / Gaussian splatting integration with LLMs
- Audio: ElevenLabs v3, OpenAI Realtime API, Suno 4

Where: **Chapter 27 (Multimodal Generation)** — needs a 2026 update sweep, especially §27.4 and §27.5.

Effort: **medium** (~2000 words across two sections, 1 timeline figure of video model releases).

### 7. Evaluation: AGI-tier benchmarks and the saturation problem

What's missing:
- ARC-AGI 2 (and ARC-AGI 3 if shipped), Humanity's Last Exam, FrontierMath
- The "post-MMLU" landscape: GPQA, BIG-Bench Extra Hard, MUSR
- LiveBench (continuously refreshed)
- Eval contamination / data-leak detection methods

Where: **Chapter 29 (Evaluation & Experiment Design)** — add a section "Frontier Benchmarks and the Saturation Problem".

Effort: **small** (~1500 words, 1 saturation chart).

### 8. Open-weights frontier closing the gap

What's missing:
- Llama 4 / Llama 4.1 release (April 2025) and ecosystem impact
- Mistral Large 3, Mixtral 8x22B v0.2
- Cohere Command R+, Command A
- Qwen 3 / Qwen 3 VL family
- Phi-4 (small/medium/multimodal)

Where: **Chapter 7 (Modern LLM Landscape)** — refresh §7.1-§7.4 with 2026 model releases.

Effort: **large** (substantial refresh of the landscape chapter; ~3000 words; landscape diagram redo).

### 9. RAG → agentic retrieval transition

What's missing:
- "Deep research" agents (Perplexity Deep Research, OpenAI Deep Research, Gemini Deep Research)
- Iterative retrieval / agentic RAG patterns
- HyDE, GraphRAG maturation
- Reranker market consolidation (Cohere Rerank 3, Jina Reranker v2)

Where: **Chapter 20 (RAG)** — extend §20.5+ with agentic retrieval patterns.

Effort: **medium** (~2000 words, 1 new section).

### 10. Safety & alignment: post-RLHF evolution

What's missing:
- Constitutional AI / Constitutional Classifiers maturity (Anthropic)
- Deliberative alignment (OpenAI)
- Process Reward Models (PRMs) at production scale
- Test-time alignment (best-of-N, rejection sampling for safety)
- Sleeper agents, sycophancy mitigation, alignment faking research

Where: **Chapter 17 (Alignment)** + **Chapter 32 (Safety, Ethics & Regulation)**.

Effort: **medium** (~2000 words split across both chapters).

### 11. LLM memory architectures

What's missing:
- MemGPT, Letta, Zep, memory-augmented agents
- Episodic vs semantic vs procedural memory in LLM agents
- Knowledge-graph + LLM hybrid memory

Where: **Chapter 22 (AI Agent Foundations)** §22.6 (already exists) and **Chapter 21 (Conversational AI)** §21.x.

Effort: **medium** (~1500 words, 1 memory-types diagram).

### 12. EU AI Act enforcement, and 2026 regulatory landscape

What's missing:
- Actual EU AI Act enforcement experience (it became enforceable in stages through 2025-2026)
- US executive orders / state-level AI laws (CA SB 1047 fallout, NY/IL/CO AI laws)
- China's Generative AI Measures enforcement
- UK AI Bill (2026)
- Voluntary commitments: Frontier Model Forum, AI Safety Institutes

Where: **Chapter 32 (Safety, Ethics & Regulation)** — §32.4-§32.10 needs 2026 refresh.

Effort: **medium** (~2500 words, regulatory-timeline diagram update).

### 13. Inference economics and unit cost collapse

What's missing:
- 90%+ price collapse from 2024 → 2026 (GPT-4o-mini, Gemini Flash, Claude Haiku)
- Provider tier economics: cached input pricing, prompt caching across providers
- The "cents-per-million-tokens" frontier
- Spot/batch pricing maturity (Anthropic Batch, OpenAI Batch with 50% discount)

Where: **Chapter 31 (Production Engineering)** + **Chapter 33 (Strategy & ROI)**.

Effort: **small** (~1000 words, 1 price-trajectory chart).

### 14. Test-time compute scaling laws (Hoffmann's reasoning equivalent)

What's missing:
- The "compute spend at inference" vs "compute spend at training" trade-off curves
- s1 / Distill-2-1B-style ultra-efficient reasoning
- Best-of-N scaling laws

Where: **Chapter 8 §8.5** (Compute-Optimal Inference) — extend with formal scaling-law treatment.

Effort: **small** (~1000 words, 1 chart).

### 15. Interpretability productionization

What's missing:
- Anthropic Sparse Autoencoders (SAEs) and Goodfire's commercialization
- Transluce / Constellation interpretability tools
- Production interpretability: attribution dashboards, debugging-by-circuits

Where: **Chapter 18 (Interpretability)** — refresh §18.3.

Effort: **small** (~800 words, 1 dashboard screenshot).

---

## Cross-cutting refreshes

- **Bibliography sweep**: every chapter needs ~5-10 new 2025-2026 citations.
- **Model price tables**: every chapter that quotes per-token pricing is stale (Apr 2024 prices). Build one canonical pricing table in `appendices/appendix-g-hardware-compute/` and link from chapters.
- **Tooling appendices** (K-V): refresh framework versions, especially LangChain (now 0.4+), LlamaIndex (now 0.13+), HuggingFace transformers (now 5.x).

---

## Execution order

Recommend this rollout sequence (each is one focused PR):

1. Chapter 7 landscape refresh (large, but foundational)
2. Chapter 8 reasoning models update + new §8.7
3. Chapter 23 protocol comparison update
4. Chapter 27 multimodal refresh
5. Chapter 25 §25.4 vibe coding update
6. Chapter 32 regulatory refresh
7. Cross-cutting bibliography + pricing-table pass
8. All others as time permits

Total estimated effort: **30-50 hours** of writing + ~10 hours of diagram regeneration + 5 hours of citation check.

This is a v7.0 milestone, not an inline patch.
