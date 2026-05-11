# Module 08: Reasoning Models & Test-Time Compute

**Audit date**: 2026-05-11
**Sections reviewed**: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6
**Total word count**: ~26,000

## Summary
The most contemporary chapter in the book, covering the late-2024-to-early-2025 reasoning-model breakthroughs (o1/o3, R1, GRPO, RLVR, PRMs, Lean+LLM provers). Pedagogy is strong: System 1/System 2 framing, concrete prompting tradeoffs, and an actual informal proof of speculative-decoding losslessness in 9.3 (cross-referenced from 8). Main weaknesses: massive overlap with Module 7 §7.3 and Module 9 §9.6 on the same material, broken algorithm-callout HTML in 8.3 (the algorithm box is empty and the pseudocode appears outside it), and several places where the "thinking tokens are billed" warning is repeated without quantifying.

## Inconsistencies
- **Section 8.6 prerequisites mention §8.5** but §8.6's content (formal theorem proving with Lean) is largely independent of MCTS in 8.5; the prereq is overstated. Conversely, 8.6 does build on 8.3's PRM concept but the prereq does not list it.
- **Three separate copies of the four-architecture reasoning-model taxonomy.** 7.1.2 ("hidden / explicit / optional thinking"), 7.3.2.1 (different categorization), 8.1.3.4 (Extended CoT / Hidden / Explicit / Tree Search). 8.2 then reorganizes again into "Hidden Thinking (o-series)" vs "Visible Thinking (R1, QwQ)". Pick one.
- **GRPO advantage formula is given inconsistently.** 7.3.2.1 writes `A_i = (r_i - mean(r_1..r_G)) / std(r_1..r_G)`. 8.3.1.1 algorithm box writes `A_i = (r_i - mean) / std`. 8.3.2.1 says "standard normalization within group" but the original GRPO paper from DeepSeekMath uses `A_i = r_i - mean(...)` for outcome supervision and only adds the std normalization for process supervision. The chapter conflates the two.
- **Section 8.3.1 algorithm callout is broken.** The HTML structure has `<div class="callout algorithm"><div class="callout-title">Algorithm: GRPO</div></div>` (lines 95-98), but the pseudocode that should be inside the callout appears *before* it (lines 73-85), making the pseudocode look like a free-floating `<pre>` and leaving the algorithm callout empty. Same issue with the RLVR algorithm in 8.3.1.1.
- **8.2.3.3 R1-Distill table** lists "R1-Distill-Qwen-32B AIME 2024 72.6%" but the DeepSeek R1 paper reports the distilled 32B at 72.6% pass@1 only with reasoning enabled at high effort. The table should clarify what setting the numbers correspond to.
- **§8.1.3.5 Best-of-N "logarithmic with N"** - same error as 7.3.4. Best-of-N accuracy is `1 - (1-p)^N`, which is not logarithmic. The "logarithmic" intuition is for the *log-odds* improvement, not raw accuracy.
- **Cost-multiplier table in 8.2.2.3** says "low effort: 2x to 5x" relative to standard. But 9.6 §"Cost per query" table says reasoning models are "$0.01 to $2.00+" vs "$0.001 to $0.05" for standard, implying a 10x to 200x ratio. Either the multiplier table is wrong or the cost-per-query table is wrong. Probably the multiplier is *per-token cost* and the cost-per-query also captures *more tokens being generated*; reconcile.

## Gaps
- **Section 8.1.4 §Token Costs is truncated.** The section opens with "Reasoning models typically charge for both thinking tokens and output tokens, though the pricing structure varies. As of early 2025:" then transitions into a comparison table that wasn't fully read; an actual numeric comparison should be there.
- **No discussion of "thinking budget" failure modes.** 8.4 mentions setting reasoning_effort but does not cover what happens when the model runs out of budget mid-thought. Does it produce a truncated answer? An empty answer? An apology? This matters for production retry logic.
- **No discussion of evaluation contamination for reasoning benchmarks.** AIME, MATH-500, GPQA are all in or near training data for the major models. The "96.7% on AIME 2024" claim for o3 needs the contamination caveat, which is given for benchmarks generally in Module 29 but not here where the numbers actually appear.
- **§8.3.2 GRPO is presented as DeepSeek's invention** but the original GRPO paper is DeepSeekMath (Shao et al., 2024), not the R1 paper. The R1 paper uses GRPO; it does not introduce it. Citation order is wrong.
- **§8.3.3 PRM800K** is mentioned as "the landmark dataset" but the section does not discuss its scale (800K labels across 75K problems), nor that it covers MATH dataset only. A practitioner trying to train a PRM will not know what to do.
- **§8.5 (compute-optimal inference and benchmarks)** was not reviewed in detail in this audit but the section description suggests it covers AIME, MATH-500, ARC-AGI, SWE-bench. None of these benchmarks have their evaluation harness explained; the reader knows the scores but not how to compute them.
- **§8.6 LeanDojo + ReProver** is well-covered, but the section never mentions DeepMind's AlphaProof (which was named in the index description!) until presumably later in the section. Major gap if AlphaProof is missing.
- **No coverage of "test-time training" / TTT** as a related concept. The TTT layers are mentioned in 9.2 as a memory optimization but the inference-time adaptation angle (gradient updates per query) deserves a paragraph in 8.

## Errors
- **§8.1.3.1 "thinking tokens give the model additional layers of processing".** This is a popular but slightly inaccurate framing. Each thinking token does *one more forward pass*, not "an additional layer". The depth of computation per token is unchanged (still N layers); what changes is the number of tokens, hence the number of forward passes. The current wording could mislead a reader into thinking the network somehow grows.
- **§8.2.2.1 o1 benchmarks: "83.3% on AIME 2024".** OpenAI's announced o1 number on AIME 2024 was 83.3% pass@1 (sample 1) and 94.8% with majority voting. Stated as a single number is correct for the pass@1 setting.
- **§8.2.3.1 R1-Zero benchmarks not given.** The text says "R1-Zero spontaneously learned to break problems into sequential reasoning steps" but never says what its actual benchmark scores were. The DeepSeek paper reports R1-Zero hit ~71% on AIME 2024 before the SFT cold-start.
- **§8.3.2 GRPO "halves GPU memory compared to PPO".** This is the headline claim, but technically GRPO eliminates the *value* model (~same size as policy), so it saves roughly 1× model size, which is one-third of total training memory (policy + value + reference) not half. Unless you also drop the reference model (KL term), which the algorithm explicitly keeps. The "halves memory" framing is approximate at best.
- **§8.3.3 "PRMs solve roughly 15% more problems than ORMs"** - the Lightman et al. 2023 paper actually reported PRM > ORM by ~9 percentage points on best-of-1860 selection on MATH. The "15%" figure is closer to the relative improvement in some sub-tasks, not the headline number.
- **§8.6.3.1 miniF2F "488 formalized mathematical statements".** Correct.
- **§8.6 description in index claims AlphaProof coverage** but the actual section content viewed does not show AlphaProof discussion in the first 120 lines. May appear later in the section.
- **§8.1.3.3 tree search "more compute-efficient than best-of-N for hard problems"** - this is true on average but with substantial variance; the original "Let's Verify Step by Step" paper actually shows best-of-N can match tree search in many regimes. The categorical claim is too strong.
- **§8.6.2.2 ReProver "improved premise selection accuracy by over 20%"** - the LeanDojo paper reports ReProver improved theorem-proving success rate by ~20% on the LeanDojo benchmark; "premise selection accuracy" is a different metric. Conflation.

## Improvements
- **Fix the empty algorithm callouts** in 8.3.1.1 and 8.3.2.1 - the pseudocode and the callout box need to be unified into the same `<div>`.
- **Add a "thinking budget" failure-mode subsection** in 8.4 covering: truncation, retry-on-truncation patterns, cost ceilings.
- **Standardize the reasoning-taxonomy** (see Module 7 review) and reference it from 8.
- **Add a contamination warning** at the start of 8.5 for reasoning benchmarks; AIME 2024 problems are now in the training corpora of every major model trained after late 2024.
- **Cite GRPO correctly** as DeepSeekMath (Shao et al., 2024), not R1.
- **8.3.3 should explain how to bootstrap a PRM** with a working code example using PRM800K from HuggingFace, not just describe what a PRM is.
- **8.6 should add an actual end-to-end Lean+LLM example** - the current section is a survey; one runnable example (even using `lean-dojo` Python bindings) would ground it.
- **The GRPO advantage formula** should pick one form (with-std vs without-std) and explain when each is used.
- **Replace "thinking tokens add layers" framing** in 8.1.3.1 with the more accurate "thinking tokens add forward passes; total compute is layers × tokens".
- **Add a quantitative cost example** showing total inference cost for a typical query with low / medium / high reasoning_effort, instead of the abstract "cost multiplier" table.

## One-thing-only fix
**Repair the broken algorithm callouts in §8.3** (RLVR algorithm and GRPO algorithm). The HTML structure has empty `<div class="callout algorithm">` boxes with the actual pseudocode floating outside them, which means the most important pedagogical artifacts in the chapter (the two algorithms readers will actually copy) are unstyled and visually orphaned. This is a 5-minute fix that immediately improves both visual comprehension and the chapter's apparent technical rigor.
