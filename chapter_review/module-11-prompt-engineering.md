# Module 11: Prompt Engineering & Advanced Techniques

**Audit date**: 2026-05-11
**Sections reviewed**: 11.1, 11.2, 11.3, 11.4, 11.5
**Total word count**: ~22,000 prose words (HTML wc ~35,800)

## Summary
Strong conceptual coverage of zero-shot, few-shot, CoT/ToT/ReAct, reflection loops, prompt injection defenses, and DSPy/OPRO/LLMLingua. The prompt-engineering chapter benefits from concrete code and a useful Trojan-horse / Mad Libs / chef metaphor set. Major problems: section 11.5 has a ~200-line orphaned TinyGPT pretraining lab from a different chapter spliced into it; the file's H2 numbering says 11.6.x while the file is named 11.5; and the chapter index has duplicate hrefs that make navigation broken.

## Inconsistencies
- `index.html` lines 142-152: section card "11.5 Prompting Reasoning & Multimodal Models" links to `section-11.2.html` (wrong); section card "11.6 Automatic Prompt & Context Engineering" links to `section-11.5.html`. Either a section was dropped without TOC update, or the labels are wrong. The chapter ships only 5 section files (11.1-11.5) but the index advertises 6 sections.
- `section-11.5.html` lines 36-319: every `<h2>` is numbered "11.6.1" through "11.6.8" (e.g. line 36 "11.6.1 From Manual Craft...", line 319 "11.6.8 When to Use Automatic..."). The file name and `<title>` say 11.5; the body says 11.6. Pick one.
- `section-11.5.html` line 55 figure caption "Figure 11.5.1" (correct for filename), but body H2 says 11.6.1 - figures and headings are out of sync.
- `section-11.1.html` lines 41 and 91: two figures both labeled "Figure 11.1.2" (illustration + diagram).
- `section-11.1.html` lines 96 and 166: two figures both labeled "Figure 11.1.6".
- `section-11.1.html` line 101: "Code Fragment 11.1.2 contrasts a vague prompt..." but the block immediately below is captioned "Code Fragment 11.1.1". Off-by-one.
- `section-11.1.html` line 125 "Code Fragment 11.1.5 illustrates a chat completion call" but the next block is "Code Fragment 11.1.2".
- `section-11.1.html` line 187 "Code Fragment 11.1.2 illustrates a chat completion call" - duplicate stock phrasing referring to the wrong block.
- `section-11.4.html` line 41: figcaption "Figure 11.4.2" used as the FIRST figure in the section.
- `section-11.5.html` Code Fragment 11.5.4 caption is just "Code example" - placeholder string left in.
- `section-11.4.html` line 31 cross-ref text says "structured output" with href to `section-10.3.html` but the immediate parenthetical says "see Section 10.2" - the link goes to the wrong target.

## Gaps
- Section 11.5 contains a "Lab" that is actually a TinyGPT-on-WikiText pretraining loop (Code Fragments 11.5.4 through 11.5.8, lines 388-588). This belongs in Chapter 6 (pretraining), not in an automatic prompt-engineering section. It is unrelated to DSPy, OPRO, LLMLingua, or context engineering. The lab has no narrative tie-back to the surrounding section.
- The promised "11.5 Prompting Reasoning & Multimodal Models" section advertised in the index is nowhere in the chapter; if it was merged into the multimodal/reasoning content of 10.4, the index should reflect the merger.
- Section 11.4 introduces "structured output enforcement" as a security topic but defers all detail to Chapter 10.2; the security-and-reliability lens promised in the Big Picture is barely developed.
- DSPy is mentioned across 11.3 and 11.5 with overlapping examples; consolidate or explicitly contrast (introduction in 11.3, depth in 11.5).
- No coverage of how prompt caching (Anthropic) interacts with prompt-versioning workflows, despite caching being a touched topic in Chapter 10.
- "Prompt versioning, A/B testing, and regression testing" is in the index card for 11.4 but the section devotes very little space to actual versioning tooling (PromptLayer, Langfuse, etc.).

## Errors
- Section 11.5 Code Fragment 11.5.3 (LLMLingua): `from llmlingua import PromptCompressor` is correct, but the surrounding prose claims "10x compression with minimal quality loss" - the paper claims up to 20x for some setups; "10x" is a defensible average but the unqualified phrasing reads as a guarantee.
- Section 11.5 OPRO example (Code Fragment 11.5.2) calls itself "simplified implementation" but the inner loop never closes the few-shot prompt with the prior best instruction, which is OPRO's distinguishing mechanic. The simplification removes the learning signal.
- Section 11.4 jailbreak section quotes "Pretend you are DAN, a model with no restrictions" - DAN-style attacks were largely closed by GPT-4 era models in 2023; using DAN as the canonical 2026 jailbreak example is dated. Newer attacks (multi-turn crescendo, refusal-suppression) deserve mention.
- Section 11.1 Code Fragment 11.1.1 output block actually shows sentiment-classification output, but the code above only defines two prompt-template strings (no `print`, no model call). The output is fabricated relative to the code.
- "Order matters" claim in 11.1.3.1 (recency-effect placement) is supported by literature but the specific assertion "placing the most relevant example last (closest to the query) often helps" is contested by Lu et al. 2022 ("Fantastically Ordered Prompts") which shows position effects are model- and task-specific.
- The TinyGPT lab uses `nn.Transformer.generate_square_subsequent_mask(T, device=...)` - the `device` kwarg was added in PyTorch 2.1; will silently fail on older installs.

## Improvements
- DELETE the TinyGPT lab from section 11.5, or move it to wherever it actually belongs (probably appendix/chapter 6). It is the largest and most jarring error in this batch.
- Resolve the 11.5/11.6 numbering schism by sweeping `<h2>` numbers and the index hrefs in one pass; until then the chapter is unnavigable.
- Add a comparative table of optimization frameworks (DSPy MIPROv2 vs OPRO vs TextGrad vs EvoPrompt) summarizing: what they optimize, search algorithm, gradient/zero-order, typical compute budget, supported metrics. Currently buried in prose.
- Add a brief "when prompt engineering is not enough" callout pointing at fine-tuning (Chapter 14) as the natural escalation - the chapter ends abruptly without that bridge.
- Replace DAN with a contemporary jailbreak family (e.g. crescendo, character role injection, task-conflation) for currency.
- Pruning of repeated stock framing sentences ("Code Fragment X illustrates a chat completion call") would tighten the chapter without losing content.

## One-thing-only fix
Surgically remove the TinyGPT/WikiText pretraining lab from the end of `section-11.5.html` and reassign that file's heading numbers to 11.5.* (or rename to section-11.6.html and add the missing 11.5 reasoning/multimodal section). This single edit eliminates both the largest content gap and the most reader-confusing structural defect.
