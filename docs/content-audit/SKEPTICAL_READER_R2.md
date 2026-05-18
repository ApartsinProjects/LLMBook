# Skeptical Reader R2 Report

Agent: 28-skeptical-reader (round 2)
Scope: non-frontier chapters in Parts 4-11 (modules 15-56)
Date: 2026-05-19

## Mandate

Read like a skeptical PhD student. Flag sentences that:
- State a finding as universal when it's distribution-specific.
- Generalize from a single paper to a domain.
- Use "proven" where the evidence is empirical, not mathematical.
- Make absolute claims ("always", "never", "all", "every", "eliminates", "guarantees").

Soften or counter-evidence each. Leave legitimately strong claims (Chinchilla ratios, technical specs) alone.

## Method

Sampled ~25 sections across the alignment / fine-tuning / PEFT / RAG / evaluation / safety chapters. For each, scanned for absolute claims about technique outcomes, and verified whether the literature supports the absolute framing. Targeted the highest-impact overclaims: claims that a working ML practitioner would read and walk away with a more confident view than the field warrants.

Most modules in scope already do a respectable job of hedging. Almost every "common misconception" callout already exists for the obvious overclaim ("RAG eliminates hallucination", "fine-tuning teaches new facts", "stronger judge = unbiased judge", "guardrails replace alignment", "federated learning means private"). The remaining overclaims tended to be in declarative prose around the same techniques.

## Edits Applied (8 overclaim softenings)

### 1. `part-4-training-adaptation/module-17-peft/index.html`

Was: PEFT methods solve full-FT memory cost while "achieving quality that rivals or matches full fine-tuning."
Now: "achieving quality that often rivals full fine-tuning on tasks close to the pretraining distribution" with explicit reference to Biderman et al. (2024), which shows LoRA still trails full fine-tuning on programming and math benchmarks demanding substantial behavioral change. Reader is now warned to test on their own task before assuming parity.

### 2. `part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.4.html` (RLVR section)

Was: "If you can write a function that grades the answer, you have a perfect reward signal... it is always exact."
Now: Reward is "exact relative to the verifier"; brittle verifiers (regex matching, flaky tests, buggy proof checkers) reintroduce noise and are themselves hackable.

### 3. Same file, RLVR Key Insight callout

Was: "In RLVR, the reward signal is free, exact, and infinitely scalable."
Now: Reward is "cheap to compute, exact relative to its verifier, and scales with available compute rather than human annotators." Added the second catch: the verifier becomes the proxy; DeepSeek-R1 and related work report models gaming weak unit-test suites or final-answer regexes.

### 4. `part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html`

Was: "The difference between [GPT-3 in 2020] and ChatGPT... is not bigger weights or more pretraining tokens: it is alignment... [aligned models] decline to help with the nerve agents."
Now: Alignment is "the most visible difference" but instruction tuning and continued pretraining contributed too; aligned models "usually decline" with explicit reference to jailbreak research (Chapter 47) showing refusals are "a strong default rather than a guarantee."

### 5. `part-4-training-adaptation/module-17-peft/section-17.2.html` (DoRA)

Was: "DoRA consistently outperforms LoRA by 1-3% across benchmarks when using the same rank and target modules."
Now: Original DoRA paper (Liu et al., 2024) "reports gains of 1-3% over LoRA across commonsense reasoning, visual-instruction, and image-text understanding tasks at matched rank and target modules"; "Independent replications find the gap is task-dependent and sometimes within noise; the safest claim is 'DoRA dominates LoRA on the original benchmark suite and is rarely worse,' not that it always wins."

### 6. `part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html` (Chain-of-Thought)

Two edits. The 18% to 79% GSM8K swing was previously attributed inconsistently (lines 55, 77, 84 had three different numbers). Standardized on Kojima et al. (2022)'s 17.7% to 78.7% for text-davinci-002, and added: "The gain depends on scale: Wei et al. (2022) report that CoT only emerges around ~60-100B parameters, and below that threshold it can hurt by letting smaller models talk themselves into worse answers." The second edit reframes the 18% to 57% PaLM number (which conflicted with the other two callouts on the same page) to match the canonical Kojima number with a note that PaLM 540B saw a similar (still-large) jump.

### 7. `part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1a.html` (RAG intro)

Was: "This simple idea yields enormous practical benefits: reduced hallucination, up-to-date information, domain-specific expertise, and full source attribution."
Now: "The promise is appealing (reduced hallucination, up-to-date information, domain-specific expertise, and the option of source attribution), but the gains are not automatic: a misconfigured RAG pipeline can increase hallucination by injecting irrelevant or contradictory passages, and citations themselves can be fabricated (see Section 32.4)."

### 8. `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1a.html` (hybrid search)

Was: "Hybrid search wins because dense and sparse retrievers fail in disjoint ways."
Now: "Hybrid search typically wins because dense and sparse retrievers fail in disjoint ways; for a corpus and query distribution where one mode dominates (e.g., pure semantic paraphrase or pure code-symbol lookup), the better single retriever can still beat a poorly-tuned fusion." Also softened the "embeddings are mathematically guaranteed to handle worst" framing to a less absolute "exactly the failure mode where embeddings are at their weakest."

### 9. `part-4-training-adaptation/module-15-synthetic-data/section-15.3.html` (LLM-as-judge correlation)

Was: "LLM-as-judge ... provides a reliable proxy that correlates well with human judgments (typically 0.7 to 0.85 Spearman correlation)."
Now: "a usable proxy with task-dependent agreement: per-example Spearman correlations with humans cluster in the 0.4 to 0.8 range across the surveys of Bavaresco et al. (2024) and Zheng et al. (2023), with the high end typically on style/helpfulness rubrics and the low end on factuality and complex reasoning." Reframed the value proposition: not that LLM judges match humans, but that they can be calibrated against a small held-out human-graded set.

## Findings Reviewed and Left Alone (well-hedged already)

- Section 18.5 (scalable oversight) explicitly says "none has fully solved the problem"; existing language is appropriately skeptical.
- Section 16.3 fine-tuning has the "fine-tuning does not reliably teach new facts" callout already.
- Section 32.1a already has "RAG Eliminates Hallucination" misconception callout.
- Section 46.1 has "Using a Stronger Model as Judge Eliminates Bias" misconception + "If Two Judges Agree" misconception.
- Section 48.1 explicitly states guardrails are not alignment, not evaluation, not policy.
- Section 50.3 has "Federated learning does not guarantee privacy by default" warning.
- Section 54.2 watermarking gives a sober "what survives and what kills it" robustness table.
- Section 12.2 already has a "CoT Always Improves Accuracy" misconception callout.
- Section 32.4 has "Citation Does Not Guarantee Faithfulness" warning with the concrete 90-days-from-30-days example.
- Section 17.1 LoRA chapter has "Higher Rank Does Not Always Mean Better Quality" and "LoRA Is Just Cheaper Full Fine-Tuning" misconception callouts.

## What Did Not Get Edited (and Why)

- Section 8.6 quiz answer asserts "more search always helps" for formal-verifier RL. The framing is reasonable in context (verifiable rewards do remove reward hacking as a search-budget bottleneck), but the absolute "always" is technically over-strong. Skipped: section 8 is Part 2, out of scope for this round.
- Section 18.1b has "Proven at largest scale (GPT-4, Claude)" and "Proven at large scale (DeepSeek-R1, 671B parameters)" in a table. "Proven at scale" is colloquial for "demonstrated empirically at scale," which is acceptable in a comparison table.
- Section 17.1 line 217: "Almost any behavior achievable through fine-tuning can also be achieved through sophisticated prompting." The "almost any" is already a hedge, and the surrounding paragraph is explicit that this is an economics-vs-capability framing, not a literal claim that prompting always suffices.
- Section 18.3 Constitutional AI already has the "Constitutional AI removes humans from alignment" misconception callout.

## Overall Assessment

The book's hedge density is already higher than typical LLM textbooks. Most of the absolute claims that survive into Parts 4-11 are either (a) inside "common misconception" callouts that explicitly correct them, or (b) in narrative prose where the surrounding context provides the qualification. The edits applied target the remaining cases where a reader could come away over-confident: PEFT-matches-full-FT, RLVR's "perfect" reward signal, CoT model-size dependence, DoRA's "consistent" win, RAG's "automatic" benefits, hybrid search as universal winner, and LLM-as-judge correlation as uniformly high.

Quality bar maintained: every softening is evidence-based (cites Biderman et al., Wei et al., Kojima et al., Liu et al., Bavaresco et al., DeepSeek-R1 reports), no generic "may" insertions, citations preserved.

Time spent: ~30 minutes.
