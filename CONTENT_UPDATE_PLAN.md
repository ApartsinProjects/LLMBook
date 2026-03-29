# Content Update Plan: Building Conversational AI using LLM and Agents

Generated: 2026-03-27 by Content Update Scout (Agent #20, Harper Quinn)
Consolidated from 4 parallel scout passes covering all 28 modules.

---

## Executive Summary

The book is broadly strong and current. Model names (GPT-4o, o3, o4-mini, Claude 4, Gemini 2.5), tools, and frameworks are up to date. Module 16's RLVR/GRPO coverage and Module 21's MCP coverage are exemplary. No entirely new parts are needed; all gaps are addressable through new sections, subsections, or paragraph-level additions.

**Biggest thematic gaps across the book:**
1. Reasoning models' impact on agents, RAG, and prompting
2. OpenAI Responses API (missing entirely)
3. Multimodal API inputs (images, audio, documents) in Module 9
4. Native speech-to-speech models
5. Vision-based document retrieval (ColPali/ColQwen)
6. All 10 appendices are empty placeholders

---

## TIER 1: Critical Additions (15 items)

These are essential for textbook credibility. Each represents a gap that readers or reviewers would immediately notice.

### New Sections to Create

| # | Location | Title | Scope | Justification |
|---|----------|-------|-------|---------------|
| 1 | Section 10.4 | Reasoning Models and Multimodal APIs | ~3000 words | OpenAI Responses API, reasoning model parameters across providers, multimodal content blocks (images, audio, documents). Biggest single gap in the book. |
| 2 | Section 11.5 | Prompting Reasoning and Multimodal Models | ~2000 words | How prompting changes for reasoning models (less explicit CoT needed), multimodal prompting patterns. |
| 3 | Section 13.7 | Synthetic Reasoning Data | ~2000 words | Generating chain-of-thought traces, verification-based filtering, the R1-style data pipeline. Bridges Modules 12 and 16. |
| 4 | Section 19.5 | Vision-Based Document Retrieval | ~2500 words | ColPali, ColQwen, visual embeddings that bypass OCR entirely. Paradigm shift in document retrieval. |
| 5 | Section 22.5 | Reasoning Models and Agent Architecture | ~2500 words | How o1/o3/Claude extended thinking change the agent loop, when to use reasoning vs. standard models as agent backbone. |
| 6 | Section 23.4 | Production Multi-Agent Systems | ~2500 words | Cost management, A2A in practice, testing multi-agent systems, scaling patterns. |
| 7 | Section 24.4 | Unified Multimodal Models and Omni-Architectures | ~2500 words | GPT-4o, Gemini 2.0, native cross-modal models, early vs. late fusion. |
| 8 | Section 27.8 | Arena-Style and Crowdsourced Evaluation | ~2000 words | Chatbot Arena / LMSYS methodology, Elo/Bradley-Terry, building your own evaluation arena. |
| 9 | Section 10.5 | Model Pruning and Sparsity | ~2500 words | Structured/unstructured pruning, SparseGPT, Wanda. One of four compression pillars, currently absent. |

### Expansions to Existing Sections

| # | Section | Addition | Scope |
|---|---------|----------|-------|
| 10 | 0.3 | torch.compile / PyTorch 2.x features, mixed precision training | ~1000 words |
| 11 | 4.1 | RMSNorm definition (referenced but never defined) | ~200 words |
| 12 | 13.4 | Anthropic Claude fine-tuning API, Together/Fireworks platforms | ~800 words |
| 13 | 26.8 | EU AI Act enforcement timeline (all phases now in force), EU AI Office, AI Pact | ~800 words |
| 14 | 27.5 | GPU table update (H200, Blackwell B100/B200, MI300X), API pricing refresh | ~500 words |
| 15 | 5.3 | Structured output via JSON schema / function calling patterns | ~800 words |

---

## TIER 2: Important Additions (20 items)

Strengthen completeness. Should be addressed in next revision pass.

| # | Section | Addition | Scope |
|---|---------|----------|-------|
| 16 | 19.1 | RAG vs. long context windows (when RAG still matters with 1M+ context) | ~1000 words |
| 17 | 20.5 | Native speech-to-speech models (GPT-4o Realtime, Gemini Live, Moshi) | ~1200 words |
| 18 | 21.2 | MCP ecosystem maturity (registries, OAuth, remote servers, security) | ~800 words |
| 19 | 25.3 | Agent evaluation benchmarks (SWE-bench, WebArena, OSWorld, AgentBench) | ~800 words |
| 20 | 25.1 | LLM-as-Judge advances (panel-of-judges, calibrated judges, domain-specific) | ~600 words |
| 21 | 6.6 | Ring Attention / sequence parallelism for long-context training | ~800 words |
| 22 | 6.3 | Post-Chinchilla scaling (inference-optimal training, Llama 3 15T tokens) | ~600 words |
| 23 | 7.1 | Benchmarking methodology (Chatbot Arena, contamination concerns) | ~800 words |
| 24 | 7.2 | Small Language Models (SLMs) as a trend (Phi-4, Gemma 3, Qwen 0.5B-3B) | ~600 words |
| 25 | 8.4 | Disaggregated inference (prefill/decode separation, Mooncake, Splitwise) | ~800 words |
| 26 | 14.2 | GaLore and rsLoRA methods | ~600 words |
| 27 | 16.2 | Online/iterative DPO, reward model overoptimization mitigation | ~600 words |
| 28 | 15.1 | Distillation licensing (OpenAI, Anthropic, Google output usage policies) | ~400 words |
| 29 | 17.2 | Scaled SAE results (Anthropic/OpenAI), automated interpretability | ~600 words |
| 30 | 19.3 | GraphRAG maturity (LightRAG, nano-GraphRAG alternatives) | ~600 words |
| 31 | 26.5 | Consolidated red teaming methodology (NIST AI Red Team, automated red teaming) | ~1000 words |
| 32 | 27.4 | Build-vs-buy economics update (open-weight quality, 2026/2027 cost landscape) | ~800 words |
| 33 | 26.3 | Production model routing/cascade (difficulty-based routing, cost-quality tradeoffs) | ~800 words |
| 34 | 2.3 | Tiktoken library (OpenAI tokenizer, cost estimation) | ~400 words |
| 35 | 4.1/4.2 | KV cache concept introduction (before full treatment in Module 8) | ~300 words |

---

## TIER 3: Nice to Have (18 items)

Rounds out coverage. Address when convenient.

| # | Section | Addition | Scope |
|---|---------|----------|-------|
| 36 | 0.3 | Distributed Data Parallel basics | ~400 words |
| 37 | 4.3 | Differential Attention (DIFF Transformer) | ~300 words |
| 38 | 4.3 | Update MoE notable models (DeepSeek-V3, Llama 4 Maverick) | ~200 words |
| 39 | 6.5 | Muon optimizer and newer optimizers | ~300 words |
| 40 | 6.6 | Expert parallelism for MoE training | ~400 words |
| 41 | 6.4 | Data quality > quantity (Phi / "Textbooks Are All You Need") | ~400 words |
| 42 | 6.1 | Update GPT series to include GPT-4o, o-series | ~200 words |
| 43 | 6.2 | Continual pre-training as a technique | ~400 words |
| 44 | 7.2 | AI model licensing landscape (Apache 2.0 vs. community licenses) | ~400 words |
| 45 | 8.1 | FP8 inference (Hopper TensorCores, H100 native) | ~300 words |
| 46 | 8.2 | Chunked prefill (now default in vLLM/SGLang) | ~300 words |
| 47 | 8.4 | Multi-LoRA serving | ~300 words |
| 48 | 18.4 | Late chunking (Jina AI) | ~300 words |
| 49 | 18.2 | Binary/scalar quantization for embeddings | ~300 words |
| 50 | 23.1 | AI-generated content detection (watermarking, C2PA) | ~500 words |
| 51 | 11.2 | Semantic caching as a hybrid pattern | ~400 words |
| 52 | 17.3 | Representation engineering for runtime control | ~400 words |
| 53 | 15.1 | Distillation for reasoning (chain-of-thought preservation) | ~400 words |

---

## Structural Suggestions

### 1. Split Module 26 (Recommended)
Module 26 has 11 sections spanning production engineering, security, ethics, regulation, and a research topic (unlearning). Consider splitting:
- **Module 26: Production Engineering and Operations** (current 26.1 to 26.4)
- **Module 27: Safety, Ethics, and Regulation** (current 26.5 to 26.11)
- **Module 28: LLM Strategy, Product Management and ROI** (current Module 27)

### 2. Build Appendices (Critical)
All 10 appendices exist as empty placeholder directories. Priority order:
1. **F: Glossary** (highest utility, referenced throughout)
2. **D: Environment Setup** (critical for reader onboarding)
3. **J: Datasets and Benchmarks** (high reference value)
4. **A: Mathematical Foundations** (fills prerequisite gaps)
5. **I: Prompt Templates** (high practical value)
6. **H: Model Cards** (quick reference)
7. **G: Hardware and Compute** (reference)
8. **B: ML Essentials** (overlap with Module 0)
9. **C: Python for LLM** (overlap with Module 0)
10. **E: Git Collaboration** (lowest priority)

Consider adding:
- **Appendix K: Regulatory Quick Reference** (practitioner cheat sheet for EU AI Act, GDPR)
- **Appendix L: Model Selection Decision Tree** (flowchart for choosing models by constraints)

### 3. "What's New" Living Section
Given field velocity, consider a dated "Recent Developments" appendix or webpage that tracks major post-publication developments.

---

## Topics Already Well Covered (Confirmed by Scout)

The following topics were checked and found to have adequate or strong coverage:
- MCP (Model Context Protocol): Section 22.2
- RLVR (Reinforcement Learning with Verifiable Rewards): Section 17.4
- Constitutional AI: Section 17.3
- Mixture of Experts architecture: Sections 4.3 and 7.2
- Reasoning models (o1, o3, DeepSeek R1): Section 7.3
- Data contamination: Sections 12.1, 25.1, 25.2
- AI coding assistants: Section 25.1
- Long context techniques: Section 14.7
- Open-weight model ecosystem: Section 7.2
- Structured/grammar-constrained generation: Section 5.3

---

## Estimated Total Effort

- **Tier 1 (Critical):** ~25,000 words across 9 new sections + 6 expansions
- **Tier 2 (Important):** ~14,000 words across 20 expansions
- **Tier 3 (Nice to have):** ~6,500 words across 18 small additions
- **Appendices:** ~50,000+ words for 10 appendices (substantial standalone effort)

**Total new content (excluding appendices):** ~45,500 words
**Total new sections to create:** 9
**Total existing sections to expand:** 44
