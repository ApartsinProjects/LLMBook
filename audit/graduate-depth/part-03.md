# Graduate-Depth Audit: Part 3 (Working with LLMs)

| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 11.1 | API Landscape & Architecture | COURSE-READY | |
| 11.2 | Structured Output & Tool Integration | COURSE-READY | |
| 11.3 | API Engineering Best Practices | COURSE-READY | |
| 11.4 | Reasoning Models & Multimodal APIs | COURSE-READY | |
| 12.1 | Foundational Prompt Design | COURSE-READY | |
| 12.2 | Chain-of-Thought & Reasoning | COURSE-READY | |
| 12.3 | Advanced Prompt Patterns | COURSE-READY | |
| 12.4 | Prompt Security & Optimization | COURSE-READY | |
| 12.5 | Automatic Prompt & Context Engineering | COURSE-READY | |
| 13.1 | LLM vs. Classical ML Decision | COURSE-READY | |
| 13.2 | LLM as Feature Extractor | COURSE-READY | |
| 13.3 | Hybrid Pipeline Patterns | COURSE-READY | |
| 13.4 | Cost-Performance Optimization | DEPTH-GAP | TCO/token-cost tooling is present, but the Pareto-frontier selection and confidence-threshold-vs-accuracy tradeoff are asserted, not derived; no worked frontier computation or break-even formula tying escalation rate to quality. |
| 13.5 | Dataset Engineering (pipelines) | COURSE-READY | |
| 13.6 | Quality Filtering & Data Mixing | DEPTH-GAP | The load-bearing mechanism (difficulty calibration via base-model logprob, and the data-mixing ratio choice) is described qualitatively; missing the scoring criterion math and any principled mixing-weight derivation, so the "drop trivial/chaotic, keep learnable" rule is a heuristic without a stated objective. |
| 14.1 | Platforms | CATALOG-OK | |
| 14.2 | Libraries & Frameworks | CATALOG-OK | |
| 14.3 | Datasets & Benchmarks | CATALOG-OK | |
| 14.4 | Models | CATALOG-OK | |
| 14.5 | External Reading & Communities | CATALOG-OK | |

## Summary
- COURSE-READY: 13 | DEPTH-GAP: 2 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 5
- Top sections to enrich:
  1. **13.4 Cost-Performance Optimization** - add a worked Pareto-frontier computation (quality vs cost per query for 3-4 model tiers on one shared eval) and a break-even formula linking escalation rate to blended cost, so the "find the best tradeoff" claim is derived rather than illustrated by a TCO calculator.
  2. **13.6 Quality Filtering & Data Mixing** - state the difficulty-calibration objective explicitly (what logprob band maximizes learning signal, and why both tails hurt) and give a principled data-mixing weight rule (e.g. temperature-based domain reweighting) instead of the qualitative refinery narrative; also fix the duplicated `<h1>`/section-number header carried over from 13.5.
  3. (Optional polish) **11.4** is COURSE-READY but the displayed Anthropic vision Code Fragment 11.4.4a pairs with a mismatched microservices "thinking" output block; the WHY content is intact, so this is an editorial caption fix, not a depth gap.

Note: Part 3 is inherently applied; the bar applied here is presence of the WHY (why a technique works, when it fails, supporting evidence). Modules 11, 12, and 13.1-13.3/13.5 consistently clear it with mechanism callouts (induction heads, CoT marginalization with scale thresholds, prompt-caching KV-prefill, comparative-advantage framing, confidence-calibration warnings) plus quantified evidence and named failure modes. Module 14 is a deliberate tools-of-the-trade survey (several files carry the GIANT_SECTION "catalog by design" marker) and is correctly scoped as CATALOG-OK.
