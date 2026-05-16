# Tools-of-the-Trade Enrichment Resume Report (2026-05-16)

## Summary

Audit of three remaining Tools chapters (modules 6, 12, 16) found that the Tools prose-deepening agent (ae6c8d07e9ae3ffdc) and the prior currency-upgrade agent had already landed essentially every audit recommendation across the 15 section files. Verified each audit bullet against on-disk content; layered only the remaining drift fixes.

## Module 06 (Part I Foundations)

- Sections 6.1-6.5: all audit bullets already landed by prior agents. Verified: uv + pixi + MLX + ZeroGPU + Modal Notebooks + Colab GPU lottery anti-rec (6.1); torch.compile reduce-overhead + torch.export + polars + numpy<2 anti-rec + transformer-engine (6.2); TinyStories + Cosmopedia v2 + FineWeb paper + BIG-bench Lite + contamination warning (6.3); ModernBERT + Pythia-14M/31M + SmolLM2/Qwen3/Llama-3.2/Gemma-3 + max-seq/vocab columns (6.4); Maxime Labonne + HF NLP Course + CS336 + 3Blue1Brown + Bluesky + Transformer Circuits successor link (6.5).
- index.html: upgraded `pip install` library-shortcut to `uv pip install` with explanatory note (cross-cutting pattern 7).

## Module 12 (Part II Understanding LLMs)

- Sections 12.1-12.5: all audit bullets already landed. Verified: SGLang + TensorWave + SambaNova + MLX + BitNet CPU + vast.ai verified hosts + egress anti-rec (12.1); outlines + nnsight 0.4 + NDIF + SAELens with Gao 2024 paper + Lindsey 2024 crosscoders + garak/EasyJailbreak + transformers v5 + tiktoken encoding_for_model + speculative decoding + prefix caching + attention sinks + uv pin set (12.2); FineWeb-2 + SmolLM3 + Nemotron-CC + DataComp-LM + LiveCodeBench + ZeroEval + reasoning benchmark suite + SimpleQA + HLE + DeepSeek-V3 cost case study (12.3); GPT-5 + Claude Opus 4.5 + Gemini 2.5 Pro + Grok 3/4 + Llama 4 family + Qwen3 + DeepSeek-V3.1/R1 + Kimi K2 + GLM-4.5/4.6 + GPT-OSS + Apertus + Phi-4 + BitNet + hybrid-reasoning-toggles key-insight + BitsAndBytesConfig modern code + DeepSeek-R1 / GRPO case study (12.4); Karpathy GPT-2 video + 2025 Anthropic mech-interp survey + AI Safety Fundamentals + Lilian Weng newer posts + Bluesky shift (12.5).
- index.html: replaced speculative "GPT-5.5 / Claude Opus 4.6 / Gemini 3.1 / Llama-4 / DeepSeek-V4" with verified May 2026 names (GPT-5 family, Claude Opus 4.5, Gemini 2.5 Pro, Llama 4 Scout/Maverick, DeepSeek-V3.1/R1). Upgraded `pip install` to `uv pip install` with note.

## Module 16 (Part III Working with LLMs)

- Section 16.1: complete (no longer a TODO scaffold). All three first-party providers + Bedrock + Azure + Together + Replicate + Fireworks + LM Studio + Ollama + Msty already landed with per-vendor anti-recommendations.
- Section 16.2: complete. DSPy + pydantic-ai + BAML + mirascope + marvin + SGLang + LMCache + vLLM v1 + speculative decoding + prefix caching + best-of-N + MCP cross-reference + LiteLLM error-swallowing anti-rec + uv pin set + streaming variant in code example all landed.
- Section 16.3: complete. WildBench + MMLU-Pro + IFEval + SimpleBench + Arena-Hard v2 + BFCL v3 + tau-bench v2 + AlpacaEval supersedence note + LLM-judge bias paper (Li 2024) + SWE-bench harness anti-rec all landed.
- Section 16.4: hybrid-reasoning-toggles key-insight + GPT-5/Claude 4.5/Gemini 2.5/Grok 4 + o3/o4-mini cheap reasoning + Stargate+R1 cost anchor + cheap-tier agentic-failure anti-rec + prompt caching three-provider note all landed. Fixed model-name drift: figure 16.4.1 alt text replaced "GPT-5.5/DeepSeek-V4/Gemini 3.1 Pro/Claude Opus 4.6" with "GPT-5/DeepSeek-V3.1/Gemini 2.5 Pro/Claude Opus 4.5"; "5.5" baseline in cheap-tier list replaced with "GPT-5 flagship"; "Gemini 3 Flash" replaced with "Gemini 2.5 Flash and Gemini 2.5 Flash-Lite".
- Section 16.5: complete. Simon Willison llm CLI + Anthropic Engineering blog + Hamel Husain evals + Latent Space + OpenAI Devday + Cursor/Claude Code/Aider docs all landed.
- index.html: filled in the "TODO author this" What-Comes-Next callout with Part IV outline (DPO/GRPO/DeepSeek-R1 lineage transition).
- diagram-price-quality-pareto.svg: corrected 6 speculative labels (Gemini 3 Flash, Llama-4-70B, DeepSeek-V4, Gemini 3.1 Pro, GPT-5.5, Claude Opus 4.6) and one routing-pattern note.

## Model-name corrections summary

- GPT-5.5 -> GPT-5 (or "GPT-5 flagship" where comparative)
- Claude Opus 4.6 -> Claude Opus 4.5
- Gemini 3.1 Pro -> Gemini 2.5 Pro
- Gemini 3 Flash -> Gemini 2.5 Flash (with Gemini 2.5 Flash-Lite as the cheap sibling)
- DeepSeek-V4 -> DeepSeek-V3.1 / R1
- Llama-4-70B (in SVG) -> Llama 3.3 70B (the actual May 2026 70B-class workhorse; Llama 4 family ships as Scout/Maverick MoE, not a 70B dense)

## Anti-recommendations confirmed present

- vast.ai nvidia-smi verification (12.1); LiteLLM error-swallowing (16.2); SWE-bench harness sensitivity (16.3); cheap-tier agentic compounding failure (16.4); cloud-free-tier checkpoint warning + Colab GPU lottery (6.1); numpy<2 pin (6.2); contamination universality (12.3, 6.3).

## Files modified

- E:/Projects/BookBlogsHome/LLMBook/part-1-foundations/module-06-tools-of-the-trade/index.html
- E:/Projects/BookBlogsHome/LLMBook/part-2-understanding-llms/module-12-tools-of-the-trade/index.html
- E:/Projects/BookBlogsHome/LLMBook/part-3-working-with-llms/module-16-tools-of-the-trade/index.html
- E:/Projects/BookBlogsHome/LLMBook/part-3-working-with-llms/module-16-tools-of-the-trade/section-16.4.html
- E:/Projects/BookBlogsHome/LLMBook/part-3-working-with-llms/module-16-tools-of-the-trade/images/diagram-price-quality-pareto.svg

## No double-edits with prose-deepening agent

Confirmed by reading each section file fully; the prose agent's annotations sit on the same `<li>` items the audit targeted, but the currency drift was confined to the figure alt text, the SVG labels, two prose sentences in 16.4, and the index.html "Big Picture" callout in module 12. None of those were prose-deepening targets.
