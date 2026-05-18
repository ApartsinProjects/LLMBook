# Code Caption Audit, Round 2 (Parts 8-12)

**Agent:** 40-code-caption-agent (round 2)
**Scope:** Parts 8 to 12 (modules 37-60). Wave-1 (R1) covered Parts 1-7.
**Date:** 2026-05-19.

## Summary

Reviewed approximately 25 section files in Parts 8 to 12. Added or improved 39 code-block captions across 11 section files. Two recurring failure modes dominated the wave: stub captions of the form "Implementation of foo" and Algorithm-callout pseudocode blocks with no caption at all. Both have been replaced with 2-sentence captions that name specific functions, parameters, or output behaviour visible in the code.

## Files touched and per-file work

### Part 8 (Conversational AI)
- No changes this wave; the section files audited (37.x, 40.x, 41.x) already had specific captions on every code block from the wave-1 pass.

### Part 9 (LLM Evaluation & Observability)
- `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.1.html`
  - Replaced 4 stub captions (`Implementation of compute_perplexity_and_bpb`, `llm_judge_evaluate`, `compute_inter_annotator_agreement`, `run_mmlu_sample`) with specific 2-sentence captions.
  - Fixed a mis-attributed caption: the EvalHarness code block had a caption describing DeepEval.
  - Added 3 new captions for DeepEval, lm-eval-harness, and the production DeepEval blocks.
- `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.2.html`
  - Replaced 6 stub captions (`bootstrap_ci`, `mcnemar_test`, `paired_bootstrap_test`, `get_eval_seeds`, `AblationConfig`, perturbation contamination test) with specific captions referencing the actual statistical tests (paired bootstrap p-value, McNemar discordant pairs, etc.).
- `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.3.html`
  - Improved 3 weak captions (42.3.1, 42.3.3, 42.3.4) to reference the SentimentAnalyzer mocks, PromptInjectionTestSuite categories, and the promptfooconfig.yaml assertion types.
- `part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html`
  - Added 3 new captions for the BLEU-N, ROUGE-N, and sequence-perplexity algorithm pseudocode blocks.

### Part 10 (LLM Security & Runtime Safety)
- `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1a.html`
  - Added 4 new captions (LLM Guard library shortcut, 3-layer injection detection algorithm, Presidio library shortcut).
  - Replaced 2 stub captions (`Implementation of sanitize_input`, `Implementation of redact`) with specific descriptions of the regex labels and the `[TYPE_REDACTED]` placeholder logic.
- `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1b.html`
  - Added 2 captions for the GCG and FGSM/PGD algorithm pseudocode blocks.
  - Replaced 5 weak captions (47.1.3 through 47.1.8) with specific captions referencing LlamaGuard category codes, the four-layer safety stack, and the red-team test outcomes.
- `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.2.html`
  - Added 1 caption for the automated red-teaming pipeline algorithm.
  - Replaced 3 weak captions (47.2.1 PyRIT, 47.2.3 tool-use, 47.2.4 adversarial library) with captions that reference specific scorers, dataclasses, and example attacks.
- `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.1.html`
  - Added 3 new captions for the COST-CONTROLLED-AGENT-LOOP and REACT-WITH-GUARDRAILS algorithm blocks plus the NeMo Guardrails library shortcut.
  - Replaced the generic `SecureAgentExecutor` caption with one that names the five defense layers.
- `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.3.html`
  - Replaced the stub `Implementing least-privilege tool wrappers` caption with one that names the constraint types (range, allowlist, blocklist, context-required).
- `part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/section-49.4.html`
  - Replaced the misleading `!/usr/bin/env bash` caption with one describing the Syft + Python pipe that counts SBOM packages by ecosystem.
- `part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.1.html`
  - Fixed a duplicate-caption bug: Code Fragment 50.1.2 carried the same text as 50.1.1. Rewrote 50.1.1 (memorization detection), 50.1.2 (PrivacyConfig pipeline), 50.1.3 (loss-threshold MIA), 50.1.4 (Opacus DP-SGD), 50.1.5 (PII scrubbing), and 50.1.6 (canary-dataset lab) with specific descriptions.
  - Added 2 new captions (shadow-model MIA algorithm and Presidio library shortcut).

### Part 11 (LLM Ethics, Trust & Governance)
- `part-11-llm-ethics-trust-governance/module-52-bias-fairness/section-52.1.html`
  - Added 4 new captions (group-fairness audit algorithm, toxicity disparity pipeline, DeepEval ToxicityMetric, HuggingFace Evaluate toxicity).
  - Replaced 1 stub (`Implementation of bias_probe`) with a caption that explains the templated, temperature-0 probe.
- `part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/section-55.1.html`
  - Added 3 new captions (Sardana inference-aware scaling algorithm, CodeCarbon library shortcut, efficiency metrics block).

### Part 12 (LLM Systems at Scale)
- `part-12-llm-systems-at-scale/module-60-edge-on-device-llms/section-60.1.html`
  - Replaced 1 truncated caption (60.1.6 about MLX) with a complete 2-sentence caption that includes the gotcha about Intel Mac fallback.

## Patterns observed

1. **The "Implementation of foo" stub.** This caption pattern appeared in roughly half the audited sections, especially in Part 9 sections 42.1, 42.2, and 42.3. It usually masked a generic auto-generated comment that survived earlier passes.
2. **Algorithm pseudocode without captions.** Multiple Algorithm callout boxes (GCG, FGSM/PGD, Shadow-MIA, BLEU-N, ROUGE-N, perplexity, cost-controlled loop, ReAct-with-guardrails, group fairness audit) had pseudocode `<pre>` blocks with no caption. These blocks are substantive (20+ lines each), so I added captions using fractional numbering (47.1.0, 50.1.3b, etc.) to avoid renumbering the existing per-section sequence.
3. **Duplicate caption text.** Two sibling code blocks in section 50.1 carried identical caption text. Fixed by rewriting both captions to reference the distinct code content.
4. **Mis-attributed captions.** Section 42.1's EvalHarness block was captioned as if it described DeepEval (the *following* block); fixed.

## Limitations

- Did not renumber existing captions to a strict 1..N sequence; instead added fractional suffixes (e.g., 47.1.0, 50.1.3b, 55.1.1c) when inserting captions before/after existing numbered blocks. A full renumbering pass would touch unrelated text and add risk for little benefit.
- Skipped one-line bash command blocks inside callouts (e.g., setup steps in section 60.1) per the agent role's "1 to 3 lines of pseudocode or a command" exclusion.
- Some sections in Parts 8 and 12 already had high-quality captions from R1 and did not need work; the budget was spent on the highest-delta sections in Parts 9 to 11.

## Caption count

Approximate totals across the wave:
- Captions added (no caption existed): 19
- Captions rewritten (stub or wrong content): 20
- Total improvements: 39 across 11 files.
