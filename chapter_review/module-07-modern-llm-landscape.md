# Module 07: The Modern LLM Landscape

**Audit date**: 2026-05-11
**Sections reviewed**: 7.1, 7.2, 7.3, 7.4
**Total word count**: ~22,000

## Summary
A timely and well-organized survey of frontier closed-source models, open-weight families, the emerging reasoning-model paradigm, and multilingual/cross-cultural concerns. Strong didactic touches: each section opens with the right level of context and the practical-example callouts are concrete. Weaknesses: substantial overlap with Module 8 (the entire reasoning section 7.3 is essentially a preview of Module 8) and Module 9 §9.6, several factual claims that will date quickly without footnoting, and architectural attribution that is repeatedly hedged as "inferred" without methodology.

## Inconsistencies
- **7.1 vs 7.2 vs 7.3 architectural details overlap.** DeepSeek V3 architecture (MLA, FP8, auxiliary-loss-free MoE, MTP) is covered in 7.2.4 in detail, then re-introduced in 7.3 (DeepSeek-R1 builds on V3) without explicitly linking back. The MoE architecture overview also exists in 6.3.7. Three separate places to learn about DeepSeek's MoE.
- **GPT-4o "context window: 128K input, 16K output".** 7.1.2 lists 128K input, 16K output. OpenAI's docs say up to 16,384 max output tokens for GPT-4o, but max-output for `gpt-4o-2024-08-06` is 16,384, while some variants cap at 4,096. Stated as a single number is misleading.
- **Pricing snapshot.** Claude 4 Opus listed at $15/$75 per million tokens (input/output) in 7.1.9. Anthropic's actual Claude Opus 4.x pricing is $15/$75 - matches. But "Claude 3.5 Sonnet $3/$15" is the older Sonnet 3.5 price; the chapter mixes Claude generations (Sonnet 3.5, Opus 4) inconsistently in the same table.
- **"Reasoning model" definition drift.** 7.1.2 §"Reasoning Model Architectures" introduces three categories (hidden, explicit, optional thinking). 7.3 then introduces a different taxonomy (extended CoT, hidden, explicit, tree search). Module 8 §8.1.3.4 introduces yet a third version of the same taxonomy with the same four categories. Pick one taxonomy and reference it.
- **Llama numbering ambiguity.** 7.2.2 §Llama 4 says "Llama 4 Scout uses 16 experts with 17B active parameters out of 109B total, while Llama 4 Maverick scales to 128 experts with 17B active out of 400B total." These are correct as of early 2025. But 6.1 table earlier in the book lists Llama 3 at "8B / 70B / 405B" with no Llama 4 row. The chapter-overview also says Llama is the catalyst but never defines what "Llama 3.1" vs "Llama 3.1 Instruct" vs "Llama 3.1 405B-Instruct" means.
- **Section 7.3 cross-references Section 8.1 but Section 8.1 cross-references 7.3.** Both sections claim to be the "definitive" treatment of test-time compute. They share many sub-figures (Snell et al. plot, the four-architecture taxonomy). A reader following links will go in circles.
- **§7.2.4 calls MLA a "97% reduction in per-token KV cache storage (512 / 16,384 = 3.1%)".** 1 - 0.031 = 96.9%, fine. But §9.2 calls it "97% saving" and the original DeepSeek paper reports ~93.3% reduction relative to standard MHA at the same model size (the 97% number is comparing to the dense KV without any sharing). Number depends on baseline; needs explicit baseline.

## Gaps
- **No definition of "frontier" model.** 7.1.1 uses the term "as the most capable AI systems available at any given time" which is circular. A more useful definition (e.g., "models within 1 generation of the SOTA on at least 3 of the standard benchmarks: MMLU, GPQA, SWE-bench, AIME") would help.
- **Pricing/capability tables have no "snapshot date" footnote on each entry.** A reader in 6 months will get confused. The "Pricing as of early 2025" warning in 7.1.9 only covers the pricing example, not the capability tables in 7.1.2 / 7.1.4 / 7.1.5.
- **MQA/GQA/MLA decision tree.** 7.1.6 lists which models use which attention variants, but does not give a table of "if you have these constraints, choose this variant." The decision criterion is implicit.
- **Cohere Command R+** is mentioned in 7.1.8 with one paragraph and disappears entirely. The Cohere model line (Command R, Command R+, Command R7B, Aya) is much richer; the brief mention undersells it.
- **Aya appears in the bibliography** (Ustun et al., 2024) but is never discussed in 7.4 §"Adapting English-Centric Models" which is exactly where it belongs.
- **No discussion of "open-source" data licenses.** 7.2.1 distinguishes open-weight from open-source but does not mention that many open-weight models (Llama, Mistral) restrict commercial use beyond a threshold or for specific applications. The compliance-conscious reader needs this.
- **§7.3 promises "compute-optimal inference framework" but only sketches the Snell et al. result.** No actual formulas, no graph showing the tradeoff curves, just text. A figure showing "for difficulty class D, compute budget B, optimal allocation is (model size, samples)" would land the concept.
- **§7.4 lacks a discussion of what "low-resource" means quantitatively.** "Some languages have fewer than 10,000 sentences" is mentioned, but no specific cutoff is given. The Joshi et al. (2020) language tier classification (Class 0 to Class 5) would be the natural reference and is missing.

## Errors
- **7.1.2 GPT-4o latency: "320ms for audio".** OpenAI announced 232ms average for audio responses (320ms was an earlier estimate from internal testing). Either is defensible but the source should be footnoted.
- **7.1.5 "GPT-4V (the vision-capable predecessor to GPT-4o)".** GPT-4V was the first vision-capable GPT-4, but GPT-4 Turbo with Vision came between V and 4o; the lineage is not strictly linear.
- **7.1.6 attention table.** Llama family is listed as "GQA". Llama 3 actually uses GQA with 8 KV heads for the 70B and 405B; the 8B uses GQA with 8 KV heads as well. Mistral 7B is listed with "GQA + Sliding Window Attention (SWA)". Mistral 7B does use SWA but only for the original 7B; later Mistral models (Mistral Nemo, Mistral Large 2) dropped SWA. Stated as "Mistral 7B / Large" the row conflates two architectures.
- **7.2.4.1 MLA 128 attention heads × d_head=128 = 16,384.** Correct for DeepSeek V3 (MHA-equivalent). But the MLA compresses to 512-dim latent + 64-dim decoupled rope key, total 576 per token, not 512. The 97% number is approximately correct (576/16,384 ≈ 3.5%) but the latent dim cited is slightly off.
- **7.2.4.3 auxiliary-loss-free routing.** "The bias terms b are not learned through backprop... Instead, they are adjusted dynamically based on observed load statistics." Correct. But the formula `gate(x) = softmax(W_g · x + b)` should clarify that the bias is added *before* top-K selection but *not* used in the weighted output (DeepSeek's paper: only the bias-augmented score is used for routing decisions, not for the output mixture). This nuance is missing.
- **7.2.5 Qwen 2.5 "0.5B to 72B parameters".** The 32B Qwen 2.5 is also released; the table jumps from 14B to 72B implicitly.
- **7.2.6 Phi-3 Medium "Approaches GPT-4o mini capability".** This was Microsoft's marketing; independent benchmarks (LMSYS) had Phi-3 Medium below Llama 3 8B on average, well below GPT-4o mini. Should be hedged.
- **7.3.2.2 R1-Zero "trained a model called R1-Zero using only reinforcement learning on the base DeepSeek-V3 model".** R1-Zero was trained on DeepSeek-V3-Base (the pre-trained checkpoint), not the released DeepSeek-V3 Instruct. The distinction matters because the Instruct version had already undergone post-training.
- **7.3.4 Best-of-N "performance scales logarithmically with N".** The accuracy follows `1 - (1-p)^N`, which is *not* logarithmic in N - it asymptotes to 1. The marginal gain (derivative) decreases roughly as `(1-p)^N · log(1/(1-p))`, which is exponentially decaying, not logarithmic. The text in 7.3.4 contradicts itself: the formula in 8.1.3.5 (`1-(1-p)^N`) is correct. Fix the "logarithmic" language.
- **7.4.2 tokenization table.** "Khmer 43 tokens for 'อาคาศกฎาศกุช ល្អនៅថ្ងៃនេះ។'" - the actual Khmer text would tokenize to 30-50 tokens depending on tokenizer; the example is plausible but the Llama 3 tokenizer is multilingual-aware so the actual ratio may be better than shown. Verify against current tokenizer.
- **7.4.3 cultural-bias code fragment** is rendered as `lang-json` but the content is Python with comments - so the syntax highlighting is wrong. Lines 159-190 show garbled token rendering ("# Demo<kc>nstrat</kc>i<kc>n</kc>g cul<kc>tural</kc> bias..."). This is a Prism syntax-highlighting failure due to wrong language tag.
- **7.1 model-comparison table mixes Gemini 2.5 Pro and Gemini Ultra.** Gemini Ultra was the original frontier tier; Gemini 2.5 Pro replaced it in 2025. Listing both as current tiers (with 1M context for both) is anachronistic.

## Improvements
- **Consolidate the test-time compute coverage.** 7.3 should be a 3-paragraph teaser pointing to Module 8, not a 4,000-word duplicate.
- **Add a "snapshot as of YYYY-MM" badge** to every model-pricing and capability table.
- **Fix the syntax-highlighting bug** in 7.4.3 (change `lang-json` to `lang-python` and re-render).
- **Standardize the reasoning-model taxonomy** - currently three slightly different taxonomies in 7.1.2, 7.3.2.1, 8.1.3.4. Pick one and reference it.
- **Add a decision flowchart for attention variant selection** in 7.1.6 (input length, batch size, hardware → MHA / GQA / MQA / MLA).
- **Aya (cited in references) should appear in 7.4.5 §Cross-Lingual Instruction Tuning** as the canonical example.
- **The Constitutional AI section 7.1.3** is excellent; consider promoting it from a sub-subsection to a full callout box and linking from Module 17.
- **The "needle in a haystack" key-insight** is great pedagogy; cite Greg Kamradt's original benchmark by name and date.
- **Add a "model selection cookbook" sidebar** at the end of 7.1: given (use case, budget, latency, privacy), recommend a tier. Currently the practical-example boxes do this implicitly across 4 sections.

## One-thing-only fix
**Merge or definitively split the test-time-compute coverage**. Currently 7.3 (this chapter), 8.1-8.6 (Module 8), and 9.6 (Module 9) all give significant coverage of reasoning models, with substantial duplication of taxonomies, examples, and even the same Snell et al. citation. Decide that Module 8 owns the conceptual content, 9.6 owns the inference-serving angle, and 7.3 is a 3-paragraph teaser pointing to both. The current sprawl is the single biggest reader-facing problem in this part of the book.
