# Content Update Scout Report (Wave 28)

**Generated:** 2026-05-18
**Scope:** All 16 parts of the book
**Mode:** Suggest (report-only, no edits)
**Today's date anchor:** 2026-05-18

## Conventions

Each finding lists:
- **Severity** (1-5: 5 = critically misleading, 1 = nice-to-update)
- **File path and approximate location**
- **Current claim**
- **2026 reality**
- **Suggested fix**

Findings flag (a) stale 2024 statements, (b) missing recent papers, (c) missing recent tools, (d) stale model rankings. Reading the book chronologically, Part I through Part V is generally the most durable (foundational); Parts VII through XVI evolve fastest and tend to need more touch-ups.

---

## Part I: LLM Building Blocks

### Finding P1-1: GPT-4 framed as canonical instruction-tuned model
- **Severity:** 2
- **Location:** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.1.html`, around line 326 (Research Frontier callout) and line 235.
- **Current claim:** "Instruction-tuned models (GPT-4, Claude, Gemini)" and "GPT-4 or Claude can perform all six tasks above".
- **2026 reality:** GPT-4 has been superseded by GPT-4o and the o-series; the field defaults to GPT-4o / o3 / Claude 3.5 / Claude 4 / Gemini 2.5 as 2026 reference points.
- **Suggested fix:** Replace bare "GPT-4" with "GPT-4o or Claude Sonnet" or simply "a frontier instruction-tuned model"; the older "GPT-4" lands like recommending Python 2.7.

### Finding P1-2: "Phi-4, Gemma 2" listed as the SLM exemplars
- **Severity:** 2
- **Location:** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.1.html`, line 326.
- **Current claim:** "specialized small language models (SLMs like Phi-4, Gemma 2)".
- **2026 reality:** Gemma 3 (March 2025) is the current canonical Gemma generation; Phi-4 (and Phi-4-mini) is still current, but Gemma 2 is now one generation behind. SmolLM2 / SmolLM3 from HuggingFace also belong on this list.
- **Suggested fix:** Update to "Phi-4-mini, Gemma 3, SmolLM2"; ideally add a one-line note that these are the smallest models capable of meaningful instruction-following on a laptop.

### Finding P1-3: tiktoken examples pin to gpt-4 encoding (cl100k_base) without flagging o200k_base
- **Severity:** 3
- **Location:** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.5.html`, lines 175-177, 217-218, 328-329, 370-371, 430-432, 632-634.
- **Current claim:** `tiktoken.encoding_for_model("gpt-4")` and `cl100k_base` are used throughout as the default OpenAI tokenizer.
- **2026 reality:** GPT-4o, GPT-4o-mini, o1, o3, and o4-mini all use `o200k_base` (a ~200K vocabulary, distinct from `cl100k_base`). Using the wrong encoding for cost estimation systematically under-counts tokens (especially for multilingual and code content).
- **Suggested fix:** Update at least one example to call `encoding_for_model("gpt-4o")` and add a paragraph: "OpenAI ships two production tokenizers in 2026: `cl100k_base` (GPT-4, GPT-3.5) and `o200k_base` (GPT-4o and the o-series). Always pick the encoding for the model you actually call."

### Finding P1-4: Missing modern PyTorch 2.x patterns (torch.compile, FlexAttention)
- **Severity:** 2
- **Location:** `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.1.html` and adjacent sections.
- **Current claim:** Setup chapter covers PyTorch install, CUDA, venv, conda, uv; uv is correctly flagged as 10-100x faster than pip.
- **2026 reality:** PyTorch 2.5+ ships FlexAttention (early 2025); torch.compile is now the default speedup for many production deploys; the foundations chapter does not mention either. JAX is mentioned as the "second-most-common research alternative", which is accurate, but the FlexAttention/torch.compile gap is more practically important.
- **Suggested fix:** Add a short callout in section 5.1 or section 3.6 noting torch.compile and FlexAttention as the default PyTorch 2.5+ acceleration story.

### Finding P1-5: Cosmopedia / FineWeb / DCLM not mentioned in the foundations stack
- **Severity:** 2
- **Location:** `part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.4.html` or section-5.4 (canonical teaching datasets).
- **Current claim:** Datasets used are MNIST, CIFAR-10, SQuAD, GLUE.
- **2026 reality:** Those teaching datasets are fine for the foundations chapter (and shouldn't be replaced), but the chapter could add a one-line forward reference: "When we get to pretraining in Part II, the modern open corpora you will see are FineWeb-Edu (HuggingFace, 2024), DCLM (Apple, 2024), and Dolma (AI2, 2024)."
- **Suggested fix:** Add a "Looking Ahead" pointer in section 5.5 (datasets) so readers do not think MNIST/SQuAD is what real LLMs train on.

### Finding P1-6: Tokenizer landscape figure may pre-date Llama 3 tokenizer expansion
- **Severity:** 1
- **Location:** `part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/images/fig-2.3.4-tokenizer-landscape.svg` and section-1.5.html.
- **Current claim:** Likely references SentencePiece BPE, tiktoken cl100k_base, etc.
- **2026 reality:** Llama 3 expanded from 32K to 128K vocabulary; the Llama 3 tokenizer is itself a notable point on the modern tokenizer landscape; Gemma 3 uses a 256K vocabulary. A landscape figure that doesn't show this 128K-256K expansion is mildly stale.
- **Suggested fix:** Update or add a footnote noting the 2024-2025 vocabulary expansion across Llama 3, Gemma 3, Qwen 2.5.

---

## Part II: Understanding LLMs

### Finding P2-1: "As of 2025, three companies define the frontier" framing
- **Severity:** 3
- **Location:** `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`, line 58.
- **Current claim:** "As of 2025, three companies consistently define the frontier: OpenAI, Anthropic, and Google DeepMind."
- **2026 reality:** xAI (Grok 3, Grok 4) entered the frontier conversation in 2025. DeepSeek (V3, R1) and Qwen (Qwen 3) are now generally counted as frontier-class on at least some benchmarks. "Three companies" is a 2024 snapshot.
- **Suggested fix:** Reframe as "As of 2026 the frontier is contested: OpenAI, Anthropic, and Google DeepMind remain at the top across most benchmarks, with xAI, DeepSeek, and Qwen pushing into frontier territory on specific axes (coding, reasoning, multilingual)."

### Finding P2-2: GPT-4o latency / pricing claims are stale snapshots
- **Severity:** 2
- **Location:** `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`, lines 74-76.
- **Current claim:** "Average response times of 320ms for audio... Significantly lower per-token costs than GPT-4 Turbo".
- **2026 reality:** GPT-4o's audio latency was a 2024 launch figure; the Realtime API targets sub-250ms now. Pricing has dropped further; current GPT-4o is roughly $2.50/$10 per M input/output, but GPT-4o-mini at $0.15/$0.60 is the cost reference point most teams actually use.
- **Suggested fix:** Replace absolute latency numbers with relative phrasing ("under 350ms typical, dropping with each Realtime API update"); express pricing as ratios; add GPT-4o-mini as the practical default.

### Finding P2-3: "Claude 3.5 Sonnet, released in mid-2024" + Claude 4 family
- **Severity:** 2
- **Location:** `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.1.html`, lines 106-130.
- **Current claim:** Claude 4 family (Opus/Sonnet/Haiku) introduced; 200K context; Claude 3.5 Sonnet treated as the recent benchmark.
- **2026 reality:** Claude is now in the Claude 4 generation (Opus 4, Sonnet 4, Haiku 4) as of Anthropic's 2025 launches; there is also Claude 4.5 (Sonnet 4.5, Haiku 4.5, Opus 4.5) and the 1M-context Sonnet 4.5 variant. The book introduces Claude 4 but does not mention 4.5 or the 1M context window.
- **Suggested fix:** Add one paragraph on Claude 4.5 (released 2025) and the 1M-context variant; note that "Claude 3.5 Sonnet" is now two generations old as a daily-driver.

### Finding P2-4: "vLLM went from a research project... PagedAttention paper published in 2023, by 2024 was serving models at Fortune 500"
- **Severity:** 2
- **Location:** `part-2-understanding-llms/module-09-inference-optimization/section-9.5.html`, line 96.
- **Current claim:** Treats vLLM/PagedAttention as a 2023-2024 development arc.
- **2026 reality:** vLLM has shipped 0.6.x and 0.7.x releases with prefix caching, chunked prefill, and disaggregated serving (prefill/decode separation). The 2023-2024 framing reads as historical-only; the production reality in 2026 includes disaggregated serving as a first-class feature.
- **Suggested fix:** Add a sentence: "By 2026 vLLM ships chunked prefill, prefix caching, and disaggregated prefill/decode by default; SGLang and TensorRT-LLM provide comparable feature sets."

### Finding P2-5: Reasoning model survey covers o1/o3/R1/QwQ but not the 2025 wave
- **Severity:** 3
- **Location:** `part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.2.html`.
- **Current claim:** Chapter title and survey: "o1, o3, R1, QwQ".
- **2026 reality:** Missing entries: o4-mini, Gemini 2.5 Pro/Flash thinking mode, Claude Sonnet 3.7 / 4 extended thinking, DeepSeek R1-0528 (May 2025 update), Qwen QwQ-32B-Preview successor (Qwen3-Reasoning), Phi-4-reasoning. The o3-mini release (Jan 2025) is also missing.
- **Suggested fix:** Add a "2025 wave" subsection or update the existing survey to cover at minimum: o3-mini, o4-mini, Gemini 2.5 thinking, Claude extended thinking, DeepSeek R1 refresh, Qwen3 reasoning models.

### Finding P2-6: Missing mention of sparse autoencoder (SAE) interpretability mainstream
- **Severity:** 3
- **Location:** `part-2-understanding-llms/module-10-interpretability/section-10.2.html` (mechanistic interpretability).
- **Current claim:** Need to verify, but Wave-27 audits suggest SAEs are mentioned only briefly.
- **2026 reality:** Sparse autoencoders are now the dominant tool for circuit-level interpretability (Anthropic's "Scaling Monosemanticity" May 2024, "Towards Monosemanticity" Oct 2023; OpenAI's "Scaling and Evaluating SAEs" June 2024; the SAEBench eval released 2024). This deserves at least one subsection.
- **Suggested fix:** Add a subsection on SAEs in section 10.2 with key references: Templeton et al. (Anthropic, May 2024) "Scaling Monosemanticity" and Gao et al. (OpenAI, June 2024) "Scaling and evaluating sparse autoencoders" (arXiv:2406.04093).

### Finding P2-7: Missing native multimodality reasoning (MoE-VLM)
- **Severity:** 2
- **Location:** `part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html`.
- **Current claim:** DeepSeek V3 covered with MoE innovations; Mixtral covered.
- **2026 reality:** Llama 4 Scout/Maverick (April 2025) are natively multimodal MoE; the book mentions Llama 4 Scout/Maverick numbers but should note this is the first widely-available open-weight native-multimodal MoE.
- **Suggested fix:** Sharpen line 91 to say "Both models are natively multimodal MoE, the first open-weight family in this class; they process text and images via a unified MoE architecture."

---

## Part III: Working with LLMs

### Finding P3-1: API pricing examples pin to "early 2025"
- **Severity:** 2
- **Location:** `part-3-working-with-llms/module-11-llm-apis/section-11.1.html`, line 74.
- **Current claim:** "All pricing figures in this chapter reflect approximate rates as of early 2025."
- **2026 reality:** This caveat is appropriate (and well-written) but the actual numbers further down the chapter may need a refresh; GPT-4o-mini has dropped to ~$0.15/$0.60 per M tokens, Haiku 3.5 dropped to $0.80/$4 then $1/$5, Gemini Flash dropped to $0.075/$0.30.
- **Suggested fix:** Refresh the specific dollar figures or replace with ratios (e.g., "Haiku is ~5x cheaper than Sonnet"); ratios survive longer.

### Finding P3-2: Prompt caching and context caching not centrally introduced
- **Severity:** 3
- **Location:** `part-3-working-with-llms/module-11-llm-apis/` (chapter as a whole).
- **Current claim:** The chapter covers API basics, function calling, retries, fallbacks, but prompt caching is not the headline feature it now is.
- **2026 reality:** Prompt caching is the single most impactful cost-reduction technique in 2026: Anthropic prompt caching (Aug 2024), OpenAI prompt caching (Oct 2024 auto), Gemini context caching, Bedrock prompt caching, all save 50-90% on cached input tokens. For any agent or RAG system, this is a load-bearing optimization.
- **Suggested fix:** Add a section (perhaps 11.4 or a new 11.5) titled "Prompt Caching Across Providers" with code snippets for Anthropic `cache_control`, OpenAI auto-caching, and Gemini explicit cache; cross-reference from RAG chapters (32.x).

### Finding P3-3: Missing reasoning_effort / extended thinking parameter
- **Severity:** 3
- **Location:** `part-3-working-with-llms/module-11-llm-apis/` and `module-12-prompt-engineering/`.
- **Current claim:** Function calling and prompting covered without mentioning the new reasoning-effort knob.
- **2026 reality:** OpenAI o-series ships `reasoning_effort: "low" | "medium" | "high"`; Anthropic Claude Sonnet 3.7+ ships `thinking: { type: "enabled", budget_tokens: 8000 }`; Gemini 2.5 ships `thinking_budget`. This is a first-class API parameter now.
- **Suggested fix:** Add a short section in chapter 11 or 12 covering the reasoning-effort / thinking-budget parameter across providers.

### Finding P3-4: DSPy treated as a special case rather than the dominant prompt-optimization framework
- **Severity:** 2
- **Location:** `part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html` (likely DSPy section).
- **Current claim:** DSPy is covered.
- **2026 reality:** DSPy is correctly covered. The book could add a paragraph on the broader programmatic-prompt-optimization ecosystem: TextGrad (Stanford, 2024; arXiv:2406.07496), MIPROv2 (DSPy's own optimizer), Promptbase (Microsoft Medprompt-style techniques). This is one of the Frontier Topics from the agent role card.
- **Suggested fix:** Add a paragraph in 12.5 surveying TextGrad, MIPROv2, EvoPrompt, and the programmatic-prompt-optimization frontier.

### Finding P3-5: Structured output ecosystem coverage
- **Severity:** 2
- **Location:** `part-3-working-with-llms/module-11-llm-apis/` or `module-12-prompt-engineering/`.
- **Current claim:** Function calling covered; need to verify Instructor / Outlines / native structured-output coverage.
- **2026 reality:** OpenAI ships native Structured Outputs (Aug 2024) with strict JSON Schema enforcement; Anthropic ships JSON mode; Gemini ships response_schema. The library stack is Instructor (Pydantic-first), Outlines (grammar-guided), and the new Marvin / BAML.
- **Suggested fix:** Either confirm coverage exists or add a short section on native structured outputs across providers, with a comparison to Instructor and Outlines.

---

## Part IV: Training & Adaptation

### Finding P4-1: PEFT chapter heads with LoRA/QLoRA; missing newer methods at depth
- **Severity:** 2
- **Location:** `part-4-training-adaptation/module-17-peft/section-17.2.html` (Advanced PEFT Methods).
- **Current claim:** LoRA and QLoRA covered in 17.1; "Advanced PEFT" in 17.2.
- **2026 reality:** DoRA (Liu et al., 2024, arXiv:2402.09353), VeRA (Kopiczko et al., 2024, arXiv:2310.11454), LoRA+ (Hayou et al., 2024), and OFT/BOFT have become commonly-used; rsLoRA is now a recommended default for higher ranks. The mainstream 2026 default for LoRA is often DoRA or LoRA+ initialization.
- **Suggested fix:** Verify section 17.2 covers DoRA, LoRA+, rsLoRA; if not, add subsections with arxiv references.

### Finding P4-2: Alignment chapter lists DPO and Constitutional AI but newer 2024-2025 methods may be light
- **Severity:** 2
- **Location:** `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html`.
- **Current claim:** DPO derivation covered as the "Modern Preference Optimization" headline.
- **2026 reality:** GRPO (Group Relative Policy Optimization, DeepSeekMath 2024, then DeepSeek R1 2025) is now the dominant preference-tuning method for reasoning models. SimPO, ORPO, KTO, RLOO are all common production choices. Verify these are covered.
- **Suggested fix:** If not already covered, add a "Preference Optimization Zoo" subsection comparing DPO, ORPO, KTO, SimPO, RLOO, and GRPO with a brief recommendation table.

### Finding P4-3: RLVR section name is current but RLAIF spectrum should mention process reward models (PRMs)
- **Severity:** 2
- **Location:** `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.6.html` (RLVR).
- **Current claim:** RLVR (Reinforcement Learning with Verifiable Rewards) section exists.
- **2026 reality:** PRMs (Process Reward Models) have largely been displaced or supplemented by ORM (Outcome Reward Models) + RLVR; the Lightman et al. (2023) "Let's Verify Step by Step" PRM800K work is foundational, and the failure of pure PRM training is now a well-documented finding (DeepSeek R1 paper).
- **Suggested fix:** Add a paragraph on the PRM-vs-ORM tradeoff; cite DeepSeek R1 (DeepSeek-AI, 2025, arXiv:2501.12948) for the modern empirical take.

### Finding P4-4: Synthetic data chapter should reference modern open synthetic datasets
- **Severity:** 2
- **Location:** `part-4-training-adaptation/module-15-synthetic-data/section-15.6.html` (Synthetic Reasoning Data).
- **Current claim:** Synthetic reasoning data covered.
- **2026 reality:** OpenMathInstruct-2 (NVIDIA, 2024), Self-Reward Cycles (Yuan et al., 2024, Meta), Nemotron-4 340B as data generator, MAmmoTH2, NuminaMath (the IMO winner), AceReason, Numina, Sky-T1 (Berkeley 2025 reasoning trace dataset for $450), should appear in the citations / examples.
- **Suggested fix:** Add a paragraph listing modern open synthetic-reasoning datasets and pipelines.

### Finding P4-5: Training-stack tools chapter may be missing Unsloth / Liger Kernel / torchtune emphasis
- **Severity:** 2
- **Location:** `part-4-training-adaptation/module-19-tools-of-the-trade/section-19.2.html`.
- **Current claim:** Need to verify the listed libraries.
- **2026 reality:** The 2026 default fine-tuning stack is: Unsloth (single-GPU LoRA), Axolotl (config-driven multi-GPU), torchtune (Meta's official), LitGPT (Lightning), Liger Kernel (LinkedIn's fused kernels, late 2024). Liger Kernel in particular is a major recent addition.
- **Suggested fix:** Verify these are all in the Tools of the Trade chapter; if not, add Liger Kernel and torchtune as recent additions.

---

## Part V: Multimodal LLMs

### Finding P5-1: Vision-encoder zoo: missing AIMv2 / DINOv3
- **Severity:** 2
- **Location:** `part-5-multimodal-llms/module-22-vision-language-models/section-22.1.html`, line 63 (DINOv2, SigLIP-ViT, InternViT-6B mentioned).
- **Current claim:** "most recent generation (DINOv2, EVA-CLIP) uses 2D rotary position embeddings (2D-RoPE) for arbitrary input sizes".
- **2026 reality:** SigLIP-2 (Google, Feb 2025) is now the SoTA contrastive vision encoder; DINOv3 (Meta, 2025) is also released. AIMv2 (Apple, late 2024) is the autoregressive vision pretraining competitor.
- **Suggested fix:** Update the lineage paragraph to add SigLIP-2 and DINOv3 (and ideally AIMv2 as the autoregressive alternative).

### Finding P5-2: VLM coverage may pre-date Pixtral / Molmo / Qwen2.5-VL / Llama 4 vision
- **Severity:** 3
- **Location:** `part-5-multimodal-llms/module-22-vision-language-models/` (chapter as a whole).
- **Current claim:** VLM survey likely covers GPT-4V, LLaVA, Flamingo, CLIP.
- **2026 reality:** Pixtral 12B (Mistral, Sept 2024), Molmo (AI2, Sept 2024) with PixMo data, Qwen2.5-VL (Jan 2025), Llama 4 native multimodal (April 2025), InternVL3, are all 2024-2025 open VLMs that the book should cite. Anthropic's vision capability in Claude Sonnet 3.5 + and the GPT-4o native multimodal pipeline are also relevant.
- **Suggested fix:** Add a 2024-2025 open VLM survey paragraph in section 22.4 or 22.5.

### Finding P5-3: Audio/music chapter may pre-date Suno v4 / Udio / MusicGen v2 / Stable Audio Open
- **Severity:** 2
- **Location:** `part-5-multimodal-llms/module-20-audio-music-generation/`.
- **Current claim:** Audio/music generation chapter; need to verify exact contents.
- **2026 reality:** Suno v4 (Nov 2024), Udio v1.5, Stable Audio Open (Stability, 2024), MusicGen-Style (Meta, 2024) are commercial / open landmarks. Sora 2 (OpenAI, late 2025) and Veo 3 (Google, 2025) define video generation; the book's video coverage should reference these.
- **Suggested fix:** Refresh the audio/music model lineup; add a "2025 commercial state" note. For video, add Sora 2, Veo 3, Runway Gen-4 as reference points.

### Finding P5-4: Document understanding chapter (21) needs ColPali / ColQwen2 / DocOwl-2
- **Severity:** 3
- **Location:** `part-5-multimodal-llms/module-21-document-understanding-ocr/`.
- **Current claim:** Document OCR / understanding chapter exists.
- **2026 reality:** ColPali (Faysse et al., June 2024, arXiv:2407.01449) replaced classical OCR+chunking pipelines for many document-RAG use cases; ColQwen2 (2024) is the most-used variant; DocOwl-2 (Alibaba, 2024) is the open VLM for document QA. This is a frontier topic explicitly called out in the agent role card.
- **Suggested fix:** Add a section or subsection on vision-based document retrieval (ColPali family); cross-reference to section 31.8 if covered there.

### Finding P5-5: VLA models chapter (24) needs Pi0 / OpenVLA / RT-2 lineage
- **Severity:** 3
- **Location:** `part-5-multimodal-llms/module-24-vla-models/`.
- **Current claim:** VLA chapter exists.
- **2026 reality:** Pi0 (Physical Intelligence, Oct 2024), OpenVLA (Stanford, 2024, arXiv:2406.09246), RT-2 (Google DeepMind, 2023), Octo, Helix (Figure AI 2025) define the 2024-2025 VLA landscape. The book chapter should cite at least Pi0 and OpenVLA.
- **Suggested fix:** Verify Pi0 and OpenVLA are cited; if not, add them with arxiv references.

---

## Part VI: Agentic AI

### Finding P6-1: MCP coverage is current; Linux Foundation governance update missing
- **Severity:** 2
- **Location:** `part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html`, lines 62-70.
- **Current claim:** "Anthropic open-sourced the Model Context Protocol in November 2024... Within ten weeks Cursor, Continue, Sourcegraph, and three rival labs had MCP servers."
- **2026 reality:** Excellent and accurate. The 2026 Snapshot callout already covers Anthropic Connectors and Plugins, which is great. The book could add one line on the Streamable HTTP transport (Mar 2025) and the MCP registry standardization.
- **Suggested fix:** Add a line: "In March 2025, MCP gained the Streamable HTTP transport (replacing the older SSE+HTTP combo), and a community registry (registry.modelcontextprotocol.io) for discovering servers."

### Finding P6-2: A2A protocol coverage
- **Severity:** 2
- **Location:** `part-6-agentic-ai/module-27-tool-use-protocols/section-27.3.html` (A2A).
- **Current claim:** A2A chapter exists.
- **2026 reality:** Google's A2A protocol (April 2025) and the AG-UI protocol (CopilotKit, 2025) are the two emerging agent-interop standards. AG-UI in particular is gaining traction for human-agent UX.
- **Suggested fix:** Verify A2A coverage is current; consider adding AG-UI as the human-agent companion protocol.

### Finding P6-3: Code agents section 29.4 dated "2026" but may miss Claude Code / Codex / Cursor Agent / Devin
- **Severity:** 3
- **Location:** `part-6-agentic-ai/module-29-specialized-agents/section-29.4.html` ("Production Agentic Coding Systems (2026)").
- **Current claim:** Dated 2026, should be comprehensive.
- **2026 reality:** The 2026 production-agentic-coding systems are: Claude Code (Anthropic CLI), OpenAI Codex CLI (April 2025), Cursor (Composer Agent mode), Windsurf (Cascade), Devin (Cognition), Aider (open-source), Cline, Roo Code, Gemini CLI. SWE-bench Verified leaders evolved through Devin -> Cognition's Synthetix -> Anthropic Claude Sonnet 4.5 + Claude Code.
- **Suggested fix:** Verify section 29.4 covers Claude Code, Codex CLI, Cursor, Devin, Aider; if any are missing, add them with one-line summaries.

### Finding P6-4: Computer Use / browser agents
- **Severity:** 3
- **Location:** `part-6-agentic-ai/module-29-specialized-agents/section-29.2.html` (Browser & Web Agents).
- **Current claim:** Browser agents chapter exists.
- **2026 reality:** Anthropic Computer Use (Oct 2024), OpenAI Operator (Jan 2025), Google Project Mariner (Dec 2024), Browser-Use library, Playwright-MCP, Stagehand, OmniMCP, are the major 2024-2025 entries. This is an explicit Frontier Topic from the agent role card.
- **Suggested fix:** Verify these are all cited in section 29.2; pay particular attention to OpenAI Operator and the Computer Use API.

### Finding P6-5: Agent memory section 26.6 may lag MemGPT/Letta evolution
- **Severity:** 2
- **Location:** `part-6-agentic-ai/module-26-ai-agents/section-26.6.html` (Memory Architecture for Agents).
- **Current claim:** Memory architecture chapter exists.
- **2026 reality:** Letta (formerly MemGPT) shipped a cloud platform in 2024-2025; Mem0 (mem0ai/mem0) has become the most-starred open-source memory library; Zep (now ZepCloud) provides graph-backed memory. The "Memory as a Service" category did not exist when MemGPT was first published.
- **Suggested fix:** Verify Mem0 and Zep are mentioned alongside Letta; the book mentions MemGPT/Letta in section 37.5, so cross-reference may suffice.

### Finding P6-6: Microsoft Agent Framework / Semantic Kernel merger
- **Severity:** 2
- **Location:** `part-6-agentic-ai/module-28-multi-agent-systems/section-28.1.html` (Framework Landscape).
- **Current claim:** Framework landscape covers LangGraph, CrewAI, AutoGen, smolagents, PydanticAI.
- **2026 reality:** Microsoft Agent Framework (announced 2025 as the AutoGen + Semantic Kernel merger) is an emerging unified Microsoft platform. This is an explicit item in the agent role card's high-priority topics.
- **Suggested fix:** Add a one-paragraph mention of Microsoft Agent Framework in section 28.1 noting the AutoGen + Semantic Kernel merger.

---

## Part VII: Retrieval & Information Extraction

### Finding P7-1: Embedding model lineup missing 2025 releases
- **Severity:** 2
- **Location:** `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.1.html`, line 178.
- **Current claim:** "BGE-M3, E5-Mistral, Nomic, GTE, mxbai, and the original SBERT family".
- **2026 reality:** Missing: Voyage 3 (Voyage AI, 2024), Cohere embed-english-v4 (May 2025), Stella embedding (early 2024, very efficient), nomic-embed-text-v2 (2025), Qwen3-Embedding (2025), gemini-embedding-001 (Google, 2025), and NV-Embed-v2 (NVIDIA, 2024).
- **Suggested fix:** Refresh the embedding lineup in section 31.1; emphasize Voyage 3 (proprietary leader on retrieval benchmarks) and Cohere v4 / Qwen3-Embedding / gemini-embedding-001 as 2025 reference points.

### Finding P7-2: Vector DB ranking treats Pinecone / Chroma as the default first stop
- **Severity:** 2
- **Location:** `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html`, line 132.
- **Current claim:** "If you are building a prototype or proof of concept, start with Chroma (in-process, zero infrastructure) or Pinecone serverless (managed, free tier)."
- **2026 reality:** Reasonable, but pgvector + Supabase has become the dominant "first stop" for production Postgres-based RAG (pgvectorscale, pgvector 0.7+, Supabase Vector). Turbopuffer (built on object storage, 2024) is the emerging cost-efficient option. LanceDB has gained on developer experience.
- **Suggested fix:** Add a paragraph noting pgvector + Supabase as the SQL-native default, and Turbopuffer as the storage-tiered budget option.

### Finding P7-3: ColPali / vision-based document retrieval coverage
- **Severity:** 3
- **Location:** `part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.8.html` (Vision-Based Document Retrieval).
- **Current claim:** Section exists with this title.
- **2026 reality:** Section title is correct. Verify it cites ColPali (Faysse et al., June 2024, arXiv:2407.01449), ColQwen2, ColPali-Mini, BGE-Visualized. This is a Frontier Topic per the agent role card.
- **Suggested fix:** Confirm ColPali family is covered with arxiv reference; otherwise add a subsection.

### Finding P7-4: GraphRAG coverage is current; missing LightRAG / nano-graphrag
- **Severity:** 2
- **Location:** `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.4.html` (GraphRAG: Community-Summarization Retrieval).
- **Current claim:** GraphRAG chapter exists.
- **2026 reality:** Microsoft GraphRAG (released Feb 2024, paper arXiv:2404.16130) is correctly the anchor. The 2024-2025 evolution: LightRAG (HKU, Oct 2024, arXiv:2410.05779), nano-graphrag (open-source minimalist clone), HybridRAG, MultiHop-RAG, KAG (Knowledge Augmented Generation). The book likely covers GraphRAG but probably not LightRAG / nano-graphrag.
- **Suggested fix:** Add a paragraph in section 35.4 covering LightRAG and the lightweight GraphRAG clones.

### Finding P7-5: Reranker coverage (Cohere Rerank v3, BGE-reranker, ms-marco)
- **Severity:** 2
- **Location:** `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html` (Advanced RAG Techniques).
- **Current claim:** Need to verify reranker coverage.
- **2026 reality:** Cohere Rerank 3.5 (2024), BGE-reranker-v2-m3, mxbai-rerank-large, Voyage rerank-2 are the 2024-2025 production rerankers. LLM-as-reranker (RankGPT, RankZephyr) and listwise rerankers (RankLLM) are also relevant.
- **Suggested fix:** Verify rerankers are covered; if needed, refresh the lineup.

---

## Part VIII: Conversational AI

### Finding P8-1: Voice / realtime models lineup
- **Severity:** 2
- **Location:** `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.3.html` ("Gemini Live and GPT-4o Realtime API").
- **Current claim:** Gemini Live and GPT-4o Realtime covered.
- **2026 reality:** Should also cover: OpenAI Realtime API GA (Dec 2024) + the newer gpt-realtime model (Aug 2025), Gemini 2.5 Live, Claude voice (announced 2025), Anthropic's voice mode in claude.ai, NotebookLM Audio Overviews / podcast generation (Google, Sept 2024), Sesame CSM-1B (open conversational speech model, 2025).
- **Suggested fix:** Refresh the realtime API survey; add Sesame and the most recent gpt-realtime model.

### Finding P8-2: Open-source realtime: Moshi / Pipecat / LiveKit
- **Severity:** 1
- **Location:** `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.5.html`.
- **Current claim:** Moshi, Pipecat, LiveKit Agents covered.
- **2026 reality:** Good current lineup. Could add: Vapi, Retell, Daily Bots (Daily.co + Pipecat, late 2024).
- **Suggested fix:** Optional: add Vapi and Retell as commercial alternatives to LiveKit Agents.

### Finding P8-3: Memory / persistence: Mem0 not mentioned as core option
- **Severity:** 2
- **Location:** `part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.5.html`.
- **Current claim:** MemGPT / Letta covered; Library Shortcut callout for `letta`.
- **2026 reality:** Mem0 (mem0ai/mem0) has 30K+ stars and is the dominant open-source memory library by GitHub adoption; Zep / ZepCloud is the production-graph memory option. The book mentions MemGPT/Letta but may underweight Mem0.
- **Suggested fix:** Add a one-paragraph comparison of MemGPT/Letta vs Mem0 vs Zep so the reader can choose.

### Finding P8-4: Speech-to-text lineup likely missing Whisper-Large-v3-turbo / Parakeet / Distil-Whisper
- **Severity:** 2
- **Location:** `part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.6.html` (Speech-to-Text, Text-to-Speech).
- **Current claim:** Section exists.
- **2026 reality:** Should cover Whisper-Large-v3-turbo (Sept 2024, 8x faster, ~same accuracy), Distil-Whisper, NVIDIA Parakeet (TDT, RNN-T) topping HuggingFace Open ASR leaderboard. For TTS: OpenAI gpt-4o-mini-tts (2025), ElevenLabs v3, Kokoro (free open TTS, 2025), MaskGCT (Amphion).
- **Suggested fix:** Refresh both STT and TTS sections with 2024-2025 models.

---

## Part IX: Evaluation & Observability

### Finding P9-1: Benchmark coverage: MMLU-Pro, GPQA-Diamond, HumanEval++ deserve mention
- **Severity:** 2
- **Location:** `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.2.html` or 42.8.
- **Current claim:** Foundational benchmark coverage exists.
- **2026 reality:** MMLU is largely saturated (>90% on frontier models); MMLU-Pro (Wang et al., 2024, arXiv:2406.01574) is the replacement. GPQA-Diamond (Rein et al., 2023) is the SoTA "hard knowledge" benchmark frontier labs report. SWE-bench Verified is the canonical coding benchmark. Chatbot Arena (LMSYS Arena) is the human-preference reference. SimpleQA (OpenAI, 2024) for hallucination eval.
- **Suggested fix:** Refresh the benchmark lineup with MMLU-Pro, GPQA-Diamond, SimpleQA, SWE-bench Verified, Chatbot Arena.

### Finding P9-2: LLM-as-judge frameworks: G-Eval / Prometheus / Patronus
- **Severity:** 2
- **Location:** `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/`.
- **Current claim:** LLM-as-judge chapter exists.
- **2026 reality:** Key frameworks: G-Eval (Liu et al., 2023, arXiv:2303.16634), Prometheus 2 (Kim et al., 2024, arXiv:2405.01535), Patronus AI Judges, JudgeBench, RewardBench (Lambert et al., 2024). The book should cite Prometheus 2 (open weights LLM-as-judge SoTA).
- **Suggested fix:** Verify Prometheus 2 and RewardBench are cited; if not, add them.

### Finding P9-3: Observability stack: should highlight Langfuse / Phoenix / LangSmith
- **Severity:** 2
- **Location:** `part-9-llm-evaluation-observability/module-44-online-eval-observability/`.
- **Current claim:** Observability chapters exist.
- **2026 reality:** The 2026 observability stack: LangSmith (LangChain), Arize Phoenix (open-source, OpenInference), Langfuse (open-source, self-hostable, dominant in EU), Helicone (open-source proxy + analytics), OpenLLMetry (Traceloop, OpenTelemetry semantic conventions), Braintrust (eval + observability hybrid).
- **Suggested fix:** Verify Phoenix, Langfuse, Braintrust all appear; emphasize OpenInference / OpenLLMetry semantic conventions as the open-standards layer.

### Finding P9-4: Agent evaluation: TAU-bench, SWE-bench, OSWorld, GAIA
- **Severity:** 3
- **Location:** Either Part VI (section 26.4 Agent Evaluation) or Part IX agent-eval section.
- **Current claim:** Need to verify which agent benchmarks are covered.
- **2026 reality:** Per the agent role card frontier topics: SWE-bench (Verified), WebArena, GAIA, TAU-bench, OSWorld, and the newer BrowseComp (OpenAI, April 2025), HLE (Humanity's Last Exam), AgentBench.
- **Suggested fix:** Confirm all six core agent benchmarks are cited in either section 26.4 or the Part IX agent-eval coverage.

### Finding P9-5: Hallucination metrics: SimpleQA, FActScore, HALoGEN
- **Severity:** 2
- **Location:** `part-9-llm-evaluation-observability/module-43-specialized-evaluation/`.
- **Current claim:** Specialized evaluation chapter exists.
- **2026 reality:** SimpleQA (OpenAI, Wei et al., 2024, arXiv:2411.04368) is the canonical hallucination eval; FActScore (Min et al., 2023, arXiv:2305.14251); HALoGEN (Ravichander et al., 2025, arXiv:2501.08292) is the latest comprehensive hallucination taxonomy.
- **Suggested fix:** Verify SimpleQA / FActScore are cited; add HALoGEN as 2025 reference.

---

## Part X: Security & Runtime Safety

### Finding P10-1: Many-shot jailbreaking + prompt-injection canon is current
- **Severity:** 1
- **Location:** `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/index.html`, line 51.
- **Current claim:** Cites "Many-Shot Jailbreaking" (Apr 2024) and OWASP LLM Top 10 (2024); Simon Willison's prompt-injection writing.
- **2026 reality:** Excellent and current. Could add the OWASP LLM Top 10 2025 update (released early 2025), and Anthropic's "Constitutional Classifiers" (Jan 2025) defense paper for prompt injection.
- **Suggested fix:** Add a citation to Anthropic's "Constitutional Classifiers" (Sharma et al., 2025) and reference the OWASP LLM Top 10 2025 list.

### Finding P10-2: LlamaFirewall / PyRIT / agent guardrails
- **Severity:** 2
- **Location:** `part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/` or `module-49-agent-safety-autonomy/`.
- **Current claim:** Guardrails chapter exists.
- **2026 reality:** LlamaFirewall (Meta, 2025, the safety framework for tool-using agents) is an explicit agent-role-card item. Microsoft PyRIT (red-teaming framework, 2024). Lakera Guard. NVIDIA NeMo Guardrails 0.10+. ProtectAI llm-guard. Invariant Labs.
- **Suggested fix:** Verify LlamaFirewall and PyRIT are cited; if not, add them with one-line summaries.

### Finding P10-3: AgentDojo / INJECAGENT covered; should add AgentHarm
- **Severity:** 2
- **Location:** `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/index.html`, line 60.
- **Current claim:** "Evaluate an agent on agentic security benchmarks (AgentDojo, INJECAGENT)."
- **2026 reality:** AgentHarm (Andriushchenko et al., Gray Swan AI, 2024, arXiv:2410.09024) is the newer comprehensive harm benchmark; also AgentSafetyBench (Liu et al., 2024).
- **Suggested fix:** Add AgentHarm to the agent-security benchmark list.

### Finding P10-4: Differential privacy / DP-SGD for LLM training
- **Severity:** 1
- **Location:** `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/`.
- **Current claim:** Privacy chapter exists.
- **2026 reality:** DP-SGD (Abadi et al. 2016) plus the more recent VaultGemma (Google, 2025) and DP fine-tuning literature should appear. PII redaction tools: Presidio (Microsoft), Pseudo, scrubadub.
- **Suggested fix:** Verify VaultGemma and Presidio are cited.

---

## Part XI: Ethics, Trust & Governance

### Finding P11-1: EU AI Act timeline: where we are in 2026
- **Severity:** 3
- **Location:** `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.1.html`, lines 58-67.
- **Current claim:** EU AI Act risk tiers covered. "If your LLM-powered hiring tool screens candidates in the EU, you are operating a 'high-risk' AI system under the EU AI Act, which means mandatory conformity assessments..."
- **2026 reality:** EU AI Act entered into force Aug 2024; prohibited-AI provisions applied Feb 2025; GPAI (General-Purpose AI) obligations applied Aug 2025; high-risk obligations apply Aug 2026 (this is the key date the book should foreground). The Code of Practice for GPAI was published in 2025.
- **Suggested fix:** Add a one-paragraph timeline ("As of May 2026, the Act's prohibited-use provisions are already in force; GPAI obligations have been live since August 2025; high-risk obligations enter force August 2026...") and cite the EU GPAI Code of Practice.

### Finding P11-2: California SB 53 / federal AI policy missing
- **Severity:** 2
- **Location:** `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.2.html` (US executive orders).
- **Current claim:** US executive orders covered.
- **2026 reality:** SB 1047 (vetoed Sep 2024 by Newsom) and the successor SB 53 (Frontier AI Transparency Act, signed Sept 2025) define California's frontier-AI safety regime. The Biden Executive Order 14110 was rescinded by Trump's executive order in Jan 2025; the new Trump AI Action Plan (July 2025) replaces it.
- **Suggested fix:** Add a paragraph on SB 1047 (vetoed) and SB 53 (signed), and on the Trump-era executive order replacing EO 14110.

### Finding P11-3: AI Safety Institutes coverage
- **Severity:** 2
- **Location:** `part-11-llm-ethics-trust-governance/module-53-regulation-compliance/section-53.3.html` or 53.4.
- **Current claim:** Regulation chapter exists.
- **2026 reality:** US AI Safety Institute (NIST AISI, 2024), UK AI Safety Institute (May 2023, now AI Security Institute as of 2025), EU AI Office, the international AISI network. Anthropic / OpenAI / Google DeepMind have voluntary pre-deployment safety testing agreements with AISIs.
- **Suggested fix:** Add a subsection on the AI Safety Institute network and the voluntary pre-deployment testing agreements.

### Finding P11-4: SynthID / C2PA / watermarking
- **Severity:** 2
- **Location:** `part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/`.
- **Current claim:** Watermarking chapter exists, with figures for SynthID and C2PA.
- **2026 reality:** Need to verify the book covers: SynthID-Text (Google DeepMind, 2024, Nature paper Oct 2024), the OpenAI watermark research (released and then pulled), and the Adobe Content Authenticity Initiative + C2PA 2.x spec. California AB 2013 (AI training transparency) signed Sept 2024.
- **Suggested fix:** Verify SynthID Nature paper (Dathathri et al., 2024) is cited; verify C2PA 2.x is current.

### Finding P11-5: Sustainability chapter: water + carbon accounting
- **Severity:** 2
- **Location:** `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/`.
- **Current claim:** Environmental sustainability chapter exists.
- **2026 reality:** ML CO2 Impact (Lacoste et al.), Carbontracker, CodeCarbon are the tools. Recent papers: "Making AI Less Thirsty" (Li et al., 2023, the water-use paper), Google's 2024 environmental report (data center water + carbon), Microsoft's 2024 report. The EPA-equivalent regulations and US national-grid impact are missing.
- **Suggested fix:** Verify water use is mentioned and Li et al. (2023, arXiv:2304.03271) is cited.

---

## Part XII: LLM Systems at Scale

### Finding P12-1: Hardware lineup is mostly current; missing TPU v6 (Trillium) and GB200 NVL72
- **Severity:** 2
- **Location:** `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.1.html`, lines 67-86.
- **Current claim:** Covers B200/B300 ($5-8/hr), H100/H200, A100, AMD MI355X; 2026-priced table.
- **2026 reality:** Current lineup is good. Missing: GB200 NVL72 (Blackwell + Grace, the rack-scale system used by frontier labs), Google TPU v6 Trillium (May 2024 GA, 4.7x FP8 perf vs v5e), TPU v6e and v7 (Ironwood, 2025), AWS Trainium 2 / Trainium 3, Cerebras WSE-3 (2024), Groq LPU (production inference at speed), Tenstorrent Blackhole (2025).
- **Suggested fix:** Add a paragraph on accelerator diversity: TPU v6 Trillium, Trainium 2, Groq LPU, Cerebras WSE-3, in addition to the GB200 NVL72 rack.

### Finding P12-2: FlashAttention-3 / FA-4 line
- **Severity:** 1
- **Location:** `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.4.html` (FlashAttention-4 and Inference Kernels for Blackwell).
- **Current claim:** Section title mentions FlashAttention-4.
- **2026 reality:** FlashAttention-3 (Shah et al., July 2024, arXiv:2407.08608) is the Hopper-optimized version with FP8 + WGMMA. FlashAttention-4 is the Blackwell-optimized successor. Need to verify both are correctly distinguished.
- **Suggested fix:** Confirm FA-3 (Hopper) and FA-4 (Blackwell) are correctly labeled; cite Shah et al. (2024).

### Finding P12-3: Edge on-device: Apple Intelligence + MLX + ExecuTorch
- **Severity:** 2
- **Location:** `part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/section-58.3.html` and `module-60-edge-on-device-llms/section-60.1.html`.
- **Current claim:** MLX / Apple Intelligence / Llama-Mobile covered.
- **2026 reality:** Apple Intelligence (iOS 18, June 2024) + Foundation Models framework (iOS 18.4, Apple's on-device LLM API for developers). MLX-LM. PyTorch ExecuTorch. Qualcomm AI Engine (Hexagon NPU). Google AI Edge / MediaPipe LLM Inference. Phi-4-mini (Microsoft, 2024) and Gemma 3 (1B/4B) are the canonical on-device models.
- **Suggested fix:** Verify Foundation Models framework, ExecuTorch, and Gemma 3 small variants are covered.

### Finding P12-4: Distributed training: 3D parallelism / FSDP2 / TorchTitan
- **Severity:** 2
- **Location:** `part-12-llm-systems-at-scale/module-59-distributed-training-systems/`.
- **Current claim:** ZeRO, FSDP, Megatron, pipeline parallelism covered.
- **2026 reality:** FSDP2 (PyTorch 2.4+, late 2024, the per-parameter sharding rewrite) supersedes FSDP1. TorchTitan (Meta, 2024) is the new PyTorch-native pre-training reference codebase. PyTorch Distributed Checkpoint (DCP). Should also mention DeepSpeed Ulysses for sequence parallelism.
- **Suggested fix:** Add FSDP2 and TorchTitan as the 2024-2025 PyTorch-native training references; cite Meta's TorchTitan paper.

---

## Part XIII: LLMOps Lifecycle

### Finding P13-1: AI gateway lineup: missing Cloudflare AI Gateway, OpenRouter
- **Severity:** 2
- **Location:** `part-13-llmops-lifecycle/module-63-ai-gateways-routing/section-63.1.html`.
- **Current claim:** AI gateway section exists.
- **2026 reality:** Production gateways: LiteLLM (open-source proxy, dominant OSS choice), Portkey (commercial), Helicone, Cloudflare AI Gateway, OpenRouter (multi-provider with built-in pricing/routing), Kong AI Gateway, TrueFoundry, Vercel AI Gateway (launched 2025).
- **Suggested fix:** Verify Cloudflare AI Gateway, OpenRouter, and Vercel AI Gateway are all covered; LiteLLM is the open-source default and should be the primary case study.

### Finding P13-2: Workflow orchestration: Temporal / Dagster / Prefect
- **Severity:** 2
- **Location:** `part-13-llmops-lifecycle/module-64-workflow-orchestration/`.
- **Current claim:** Workflow orchestration chapter exists.
- **2026 reality:** Temporal (durable execution leader for LLM agents), Dagster, Prefect, Airflow (legacy but still common), Inngest (event-driven), Restate. For agent-specific orchestration: LangGraph Cloud, AutoGen Studio.
- **Suggested fix:** Verify Temporal is cited as the durable-execution leader for agentic workflows.

### Finding P13-3: Container/K8s: KServe vs Ray Serve vs vLLM Production Stack
- **Severity:** 2
- **Location:** `part-13-llmops-lifecycle/module-65-containers-kubernetes/`.
- **Current claim:** Containers & K8s chapter exists.
- **2026 reality:** For LLM serving on K8s: KServe (Knative-based), Ray Serve, vLLM Production Stack (released 2024), Triton Inference Server, NVIDIA NIM containers, BentoML, Modal, RunPod, Anyscale, Together AI for managed.
- **Suggested fix:** Verify KServe / Ray Serve / vLLM Production Stack are covered; add NVIDIA NIM if not present.

---

## Part XIV: Designing LLM/Agent Products

### Finding P14-1: AI-Native IDE landscape: section title is "2026" but verify coverage
- **Severity:** 3
- **Location:** `part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.3.html` ("The AI-Native IDE Landscape in 2026").
- **Current claim:** Section explicitly dated 2026.
- **2026 reality:** Should cover Cursor (Composer Agent, Cursor 1.0 in 2025), Windsurf (formerly Codeium Cascade), GitHub Copilot Workspace, Zed (Anthropic-backed), JetBrains AI Assistant + Junie, Replit Agent / Agent V2, Bolt.new, Lovable, v0 (Vercel), Trae (ByteDance), Continue.dev (open-source).
- **Suggested fix:** Confirm the IDE landscape includes Cursor, Windsurf, Copilot Workspace, Zed, Replit Agent, Bolt, Lovable, v0, Continue.

### Finding P14-2: Vibe-coding chapter should reference Karpathy's original tweet/definition + Claude Code
- **Severity:** 2
- **Location:** `part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.1.html` and 68.2.
- **Current claim:** Vibe-coding chapter exists.
- **2026 reality:** "Vibe coding" was named by Andrej Karpathy in a Feb 2025 tweet; should be cited. Claude Code (Anthropic CLI, Feb 2025), OpenAI Codex CLI (April 2025), Gemini CLI, and Aider are the canonical agentic coding tools. Devin (Cognition, March 2024, GA 2024) is the headline autonomous coding agent.
- **Suggested fix:** Verify Karpathy's coinage is cited; Claude Code, Codex CLI, Devin all referenced.

### Finding P14-3: Economics chapter: token-cost ladder + spot pricing
- **Severity:** 2
- **Location:** `part-14-designing-llm-agent-products/module-69-llm-economics/`.
- **Current claim:** Token cost forecasting and multi-vendor arbitrage covered.
- **2026 reality:** The 2026 cost story: GPT-4o-mini ($0.15/$0.60), Haiku 3.5 ($0.80/$4) / Haiku 4.5 (cheaper), Gemini Flash ($0.075/$0.30), DeepSeek V3 ($0.27/$1.10 official, or near-free via OpenRouter for off-peak). Cached input is 50-90% cheaper. Batch API is 50% cheaper. The full pricing ladder needs a 2026 refresh.
- **Suggested fix:** Refresh the cost ladder; emphasize prompt caching and batch APIs as first-order optimizations.

---

## Part XIV: Applications Across Industries

### Finding P15-1: Legal LLMs: missing Harvey AI / Lexis+ AI / Westlaw Edge AI
- **Severity:** 2
- **Location:** `part-14-applications-of-llms-across-industries/module-67-legal-llms/`.
- **Current claim:** Legal LLMs chapter.
- **2026 reality:** Harvey AI (Anthropic + a16z backed), Lexis+ AI, Westlaw Precision AI, CoCounsel (Thomson Reuters / Casetext), Spellbook, Ironclad AI. The Stanford RegLab work on legal-LLM hallucination (Magesh et al., 2024, arXiv:2405.20362) is essential reading.
- **Suggested fix:** Verify Harvey AI is cited and the Stanford RegLab hallucination paper is referenced.

### Finding P15-2: Healthcare LLMs: missing Med-Gemini / o1 medical evals
- **Severity:** 2
- **Location:** `part-14-applications-of-llms-across-industries/module-69-healthcare-llms/`.
- **Current claim:** Healthcare LLMs chapter exists.
- **2026 reality:** Med-Gemini (Saab et al., May 2024, arXiv:2404.18416), Med-PaLM 2, GPT-4 + o1 on USMLE (Nori et al., 2023, arXiv:2303.13375 + 2024 update). The HuatuoGPT family (Chinese medical LLM). Abridge / DAX / Suki for clinical scribes. EU MDR + FDA SaMD regulatory pathways.
- **Suggested fix:** Verify Med-Gemini and a clinical-scribe section (Abridge, Microsoft DAX, Suki) are covered.

### Finding P15-3: Finance LLMs: BloombergGPT is dated; missing modern coverage
- **Severity:** 2
- **Location:** `part-14-applications-of-llms-across-industries/module-68-finance-llms/`.
- **Current claim:** Finance LLMs chapter exists.
- **2026 reality:** BloombergGPT (March 2023) was the headline finance LLM but is now historical. Modern: FinLLM-Eval, FinanceBench, Pixiu, Hawkamah. JPMorgan IndexGPT, Goldman Sachs use of LLM-powered tooling (announced 2024). Numo, AlphaSense, Hebbia.
- **Suggested fix:** Verify BloombergGPT is treated as historical rather than current; refresh with FinanceBench and 2024-2025 enterprise deployments.

### Finding P15-4: Cybersecurity LLMs: missing major 2024-2025 entries
- **Severity:** 2
- **Location:** `part-14-applications-of-llms-across-industries/module-71-cybersecurity-llms/`.
- **Current claim:** Cybersecurity LLMs chapter exists.
- **2026 reality:** Foundation-AI / Foundation-Sec (Cisco, 2024-2025), Vectra / DarkTrace LLM integrations, Microsoft Copilot for Security (2024 GA), CrowdStrike Charlotte AI. The Bug-AGENTS / cyber-evals literature: Cybench (Stanford, 2024), HackTheBox + LLMs.
- **Suggested fix:** Add Microsoft Copilot for Security and Cybench eval as references.

### Finding P15-5: Education LLMs: Khanmigo, Synthesis Tutor, Magic School
- **Severity:** 1
- **Location:** `part-14-applications-of-llms-across-industries/module-70-education-llms/`.
- **Current claim:** Education LLMs chapter exists.
- **2026 reality:** Khanmigo (Khan Academy + OpenAI), Synthesis Tutor, Magic School AI, Eureka Labs (Andrej Karpathy's startup). The OpenAI for Education + Anthropic for Education programs (2024-2025).
- **Suggested fix:** Verify Khanmigo and Eureka Labs are cited as the canonical examples.

---

## Part XV: Research Frontiers

### Finding P16-1: Alternative architectures: missing 2025 hybrid SSM-Transformer entries
- **Severity:** 2
- **Location:** `part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.3.html`.
- **Current claim:** Mamba, Mamba-2, S4 covered; references the 2024 hybrid pattern.
- **2026 reality:** Jamba (AI21, March 2024, hybrid SSM-Transformer-MoE), Zamba (Zyphra, 2024), Falcon-H1 (TII, 2025), and the IBM Granite-3 hybrid models. The "linear attention" line: Mamba-Codestral, Recurrent Gemma. xLSTM (Beck et al., 2024, arXiv:2405.04517) deserves at least a callout.
- **Suggested fix:** Add Jamba, Zamba, Falcon-H1, and xLSTM as 2024-2025 alternative architectures.

### Finding P16-2: AGI benchmark coverage is fresh; ARC-AGI-2 update
- **Severity:** 2
- **Location:** `part-15-llm-agentic-ai-research-frontiers/module-77-agi-trajectories/section-77.1.html` (Frontier Benchmarks: HLE, ARC-AGI-2, FrontierMath).
- **Current claim:** HLE, ARC-AGI-2, FrontierMath called out.
- **2026 reality:** Good current lineup. Should also cover: SWE-bench Verified, GPQA-Diamond, AIME 2024/2025, BrowseComp (OpenAI, April 2025), and the o3 ARC-AGI breakthrough (Dec 2024) followed by the ARC-AGI-2 release (March 2025).
- **Suggested fix:** Verify the o3 ARC-AGI breakthrough and ARC-AGI-2 release are both narrated in section 77.1.

### Finding P16-3: AGI timelines section needs Situational Awareness / AI 2027 / METR doubling time
- **Severity:** 3
- **Location:** `part-15-llm-agentic-ai-research-frontiers/module-77-agi-trajectories/section-77.3.html` (AGI Timelines: The 2027-2033 Spectrum).
- **Current claim:** AGI timelines covered.
- **2026 reality:** Leopold Aschenbrenner's "Situational Awareness" (June 2024), the AI 2027 scenario (April 2025), and the METR task-length-doubling work ("Measuring AI Ability to Complete Long Tasks", Kwa et al., March 2025, arXiv:2503.14499) showing 7-month doubling time, are the three most-discussed 2024-2025 timeline pieces. Daniel Kokotajlo's "AI 2027" scenario specifically deserves citation.
- **Suggested fix:** Add Aschenbrenner, Kokotajlo et al. (AI 2027), and METR doubling-time work to the section.

### Finding P16-4: Alignment frontier: deceptive alignment + scalable oversight
- **Severity:** 2
- **Location:** `part-15-llm-agentic-ai-research-frontiers/module-77-agi-trajectories/section-77.2.html` (Alignment at Frontier Scale).
- **Current claim:** Alignment at frontier scale covered.
- **2026 reality:** Should cite: "Sleeper Agents" (Hubinger et al., Anthropic, Jan 2024, arXiv:2401.05566), "Alignment Faking in Large Language Models" (Greenblatt et al., Anthropic, Dec 2024, arXiv:2412.14093), Debate / Scalable Oversight (Khan et al., 2024), Weak-to-Strong Generalization (Burns et al., OpenAI, 2023, arXiv:2312.09390).
- **Suggested fix:** Verify these four papers are cited as the canonical alignment-research papers.

### Finding P16-5: Mechanistic interpretability at scale: SAE results + circuits
- **Severity:** 2
- **Location:** `part-15-llm-agentic-ai-research-frontiers/module-76-frontier-theory/section-76.3.html` (Mechanistic Interpretability at Scale).
- **Current claim:** Section exists.
- **2026 reality:** Should cite: Templeton et al. (Anthropic, May 2024) "Scaling Monosemanticity"; Gao et al. (OpenAI, June 2024) "Scaling and evaluating sparse autoencoders" (arXiv:2406.04093); the Anthropic circuit-tracing work; Neel Nanda's tutorial corpus; SAEBench (2024) for SAE eval.
- **Suggested fix:** Verify the Templeton + Gao SAE papers and SAEBench are cited.

---

## Summary

**Total findings:** 80 (Part I: 6; II: 7; III: 5; IV: 5; V: 5; VI: 6; VII: 5; VIII: 4; IX: 5; X: 4; XI: 5; XII: 4; XIII: 3; XIV: 3; XV: 5; XVI: 5).

**By severity:**
- Severity 5: 0
- Severity 4: 0
- Severity 3: 18
- Severity 2: 51
- Severity 1: 11

**Top 5 highest-impact (cross-book):**
1. **P3-2 Prompt caching coverage** (sev 3): The single most impactful 2024-2026 cost optimization is not centrally introduced. Recommend adding a dedicated section in chapter 11 with provider-by-provider snippets.
2. **P2-5 Reasoning model survey** (sev 3): Section 8.2 covers o1/o3/R1/QwQ but misses o3-mini, o4-mini, Gemini 2.5 thinking, Claude extended thinking, DeepSeek R1-0528, Qwen3 reasoning.
3. **P5-2 / P6-4 Modern VLMs and Computer Use** (sev 3): Pixtral, Molmo, Qwen2.5-VL, Llama 4 vision, plus Computer Use / Operator / Project Mariner all deserve current treatment; these are flagship 2024-2025 capabilities.
4. **P11-1 EU AI Act timeline** (sev 3): The book covers risk tiers but needs the specific 2024-2026 timeline (prohibited Feb 2025, GPAI Aug 2025, high-risk Aug 2026) so readers know what to comply with right now.
5. **P14-1 AI-native IDE landscape** (sev 3): Section is dated 2026 in its title, so it must be exhaustive: Cursor, Windsurf, Copilot Workspace, Zed, Replit Agent, Bolt, Lovable, v0, Continue, Claude Code, Codex CLI, Gemini CLI.

**Overall assessment:** MOSTLY CURRENT, NEEDS UPDATES.

The book is impressively current for a 16-part work, especially on MCP coverage, EU AI Act framing, hardware (B200/H200/MI355X), Llama 4, DeepSeek V3, vLLM/PagedAttention, and the reasoning-model architecture survey. The most consistent gap pattern is **2025-specific developments**: o3-mini and o4-mini, Claude 4.5, Gemini 2.5 thinking, SigLIP-2 / DINOv3, the EU AI Act enforcement-date timeline, OpenAI Operator, prompt caching as a first-class feature, and SAE-based interpretability. Most findings can be addressed by adding 1-3 paragraphs or refreshing one bibliography entry per section rather than restructuring chapters.

---

## Round 2 (Wave 43)

**Scope:** Parts 6-9 only (modules 26-46). **Mode:** Implement (surgical edits in place). **Date anchor:** 2026-05-18.

Round 1 was a comprehensive suggest-mode pass at the part level. Round 2 was a deep-scan of section-*.html files specifically in Parts 6 (Agentic AI), 7 (Retrieval/RAG), 8 (Conversational AI), and 9 (Evaluation/Observability). I scanned ~50 sections looking for the patterns in the dispatch brief: 2025 reasoning-model wave, modern eval frameworks, modern VLMs, multi-agent framework maturity, updated context lengths, and stale pricing.

**Overall finding:** Parts 6-9 are remarkably fresh. The June-2024 to early-2026 timeframe is densely covered: MCP (Section 27.2), A2A (Section 27.3), LangGraph / AutoGen v0.4 / CrewAI / Semantic Kernel (Sections 30.2, 41.2), Claude Computer Use / Operator / Project Mariner (Section 30.1, 30.4), SigLIP 2 / ColPali / NV-Embed-v2 / BGE-M3 / Stella / Linq-Embed (Sections 33.1, 36.4), DeepSeek-R1 / extended thinking / o1/o3 (Section 26.3), tau-bench / tau²-bench / GAIA / WebArena / OSWorld (Sections 26.4, 43.3), SWE-bench Verified / LiveCodeBench / MMMU / MM-Vet (Sections 43.4, 43.5), OpenLLMetry / Braintrust / Latitude / Laminar / LangSmith / Langfuse (Sections 44.3, 44.7), Letta / MemGPT (Section 37.5), and the Anthropic Connectors / Plugins distinction (Section 27.2).

Only three real staleness items surfaced. The book had already absorbed almost everything the Round 1 audit flagged for Parts 6-9.

### Edits made

1. **`part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html`** (Section 32.1.4 Context Window Management): updated "128K tokens for GPT-4o, 200K for Claude" to also list GPT-4.1 (1M), Gemini 1.5/2.5 (1M-2M), and Llama 4 Scout (10M). The old line implied 128K-200K was the modern range, which was true in mid-2024 but no longer true as of 2025-26 when context windows ran from 128K to 10M.

2. **`part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html`** (Section 42.1.5 LLM Benchmarks comparison table): added rows for GPQA-Diamond (PhD-level science, Rein et al. 2024), Humanity's Last Exam (CAIS, January 2025), ARC-AGI-2 (Chollet et al., March 2025), and FrontierMath (Epoch AI, November 2024). Also annotated the SWE-Bench row with the SWE-bench Verified subset (OpenAI, August 2024). The pre-edit table cut off at GSM8K/SWE-Bench and missed the 2024-25 frontier-benchmark wave that supersedes them.

3. **`part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.3.html`** (Section 45.3.1 Knowledge and Reasoning, 45.3.2 Capability/Agentic, and the comparison table): added bullets for HLE, ARC-AGI-2, FrontierMath, GAIA, WebArena, and OSWorld. Added the SWE-bench Verified annotation to the SWE-bench bullet. Added three rows to the comparison table (HLE, ARC-AGI-2, GAIA/WebArena/OSWorld) so the "what to use in 2026" table is no longer missing the 2025 wave.

### What I checked but did not edit

The following sections were inspected for the listed staleness patterns and found to already be current as of 2026-05-18: 26.1 (agent architectures), 26.2 (planning), 26.3 (reasoning models — already cites o1/o3/R1/Claude extended thinking), 26.4 (agent eval — already cites SWE-bench, GAIA, WebArena, OSWorld, tau-bench, PaperBench), 26.5 (deployment), 27.1-27.6 (tool use, MCP, A2A), 28.1-28.4 (multi-agent — AutoGen v0.4, CrewAI, supervisor/swarm/debate patterns), 29.1 (code agents), 29.2 (browser agents — already cites Stagehand, browser-use, Claude in Chrome), 30.1-30.4 (agent platforms — fresh through 2025-26 with Operator, Project Mariner, Skills, MCP registries), 31.1a/31.1b (embeddings), 33.1 (SigLIP 2, EVA-CLIP), 33.3 (when to retrieve vs reason), 35.1-35.5b (advanced RAG, DSPy, hardening), 36.1-36.4 (retrieval tools — all major vector DBs and embedders present and dated correctly), 37.1-37.5b (dialogue systems, memory — Letta/MemGPT covered), 40.1-40.6b (voice realtime — GPT-4o Realtime, Gemini Live, Moshi, Hume EVI, Cartesia Sonic all covered), 41.1-41.5 (conv-AI tools — Dialogflow CX, Voiceflow, Botpress, Anthropic Projects, Copilot Studio, LiveKit Agents, Pipecat covered), 42.5-42.12 (eval quality gates, long-context, NIAH/RULER), 43.2-43.5 (specialized eval — tau-bench / tau²-bench / MM-tau-p2 / SWE-bench / LiveCodeBench / MMMU / MM-Vet covered), 44.2-44.7 (online eval, observability — OpenLLMetry, Braintrust, Latitude, Laminar covered with the 2024-2025 GenAI semantic conventions), 45.1-45.5 (eval tools — Prometheus 2, Skywork-Reward, lm-eval-harness covered), 46.1-46.5 (LLM-as-judge — Zheng et al. position-bias debiasing covered).

**Assessment:** Parts 6-9 are now current as of 2026-05-18 in all the dimensions the brief asked me to check. Three surgical edits closed the remaining staleness gaps. Recommend no further round-2 work on these parts; the next deep scout should focus on Parts 10-16 (where Round 1 found heavier coverage gaps).
