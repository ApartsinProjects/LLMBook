# Graduate-Depth Audit: Book-Wide Master Report

Every leaf section of the book was audited for whether it has enough depth to
anchor a graduate-course unit using the book as the only source. The bar
(graduate-course-basis): the core mechanism is derived or faithfully sketched
(not just a recipe or API call), assumptions and failure modes are stated, a
worked example or numeric trace is present where the topic is mathematical or
algorithmic, and the section is self-contained enough to lecture from.

Per-section verdict tables live in `part-01.md` through `part-15.md` in this
directory.

## Scope

- 15 parts, 462 leaf sections judged (appendices and front matter excluded).
- Verdicts: COURSE-READY, DEPTH-GAP, NOT-SELF-CONTAINED, CATALOG-OK
  (the last for intentional tools-of-the-trade catalogs and indices, which are
  not held to the derivation bar).

## Results

| Part | Course-ready | Depth-gap | Not-self-contained | Catalog-ok |
|---|---|---|---|---|
| 1 LLM Building Blocks | 32 | 0 | 0 | 6 |
| 2 Understanding LLMs | 33 | 3 | 0 | 7 |
| 3 Working with LLMs | 13 | 2 | 0 | 5 |
| 4 Training & Adaptation | 24 | 4 | 0 | 16 |
| 5 Multimodal LLMs | 33 | 3 | 0 | 16 |
| 6 Agentic AI | 20 | 2 | 0 | 7 |
| 7 Retrieval & IE | 28 | 1 | 0 | 7 |
| 8 Conversational AI | 18 | 2 | 0 | 5 |
| 9 Evaluation & Observability | 25 | 0 | 1 | 5 |
| 10 Security & Runtime Safety | 17 | 1 | 0 | 5 |
| 11 Ethics, Trust & Governance | 19 | 1 | 0 | 5 |
| 12 Systems at Scale | 13 | 3 | 0 | 6 |
| 13 LLMOps Lifecycle | 16 | 0 | 0 | 1 |
| 14 Applications Across Industries | 28 | 1 | 0 | 9 |
| 15 Research Frontiers | 12 | 1 | 0 | 6 |
| **Total** | **331** | **24** | **1** | **106** |

- COURSE-READY rate among non-catalog sections: 331 / 356 = 93% before fixes.
- After fixes: all 24 DEPTH-GAP and the 1 NOT-SELF-CONTAINED section closed, so
  every non-catalog section is now COURSE-READY.

## Gaps found and closed (all fixed)

Each fix added the load-bearing mechanism the section was missing, written to the
Deep-Explanation and Code-Pedagogy house-style contracts. Commits: 26d0db8 (batch 1,
Parts 2/3/4/15), de24cd2 (batch 2, Parts 5/6), fe6681f (batch 3, Parts 7/8/10/11),
and the final batch (Parts 9/12/14).

| Section | Gap | Fix |
|---|---|---|
| 7.1 | native vs bolt-on multimodal fusion | attention/loss argument for joint-sequence fusion |
| 7.2a | architectural inference asserted | worked MoE active-fraction estimate from latency/price + code |
| 8.4 | reasoning-model prompting heuristic | internalized-controller principle derived |
| 13.4 | cost tradeoff illustrated, not derived | Pareto dominance test + cascade break-even formula + code |
| 13.6 | data mixing qualitative (+ dup header) | difficulty-calibration objective + temperature reweighting rule |
| 15.4 | active learning not reproducible | entropy acquisition function + stopping criterion + code |
| 15.5 | weak supervision asserted | Snorkel label-model derivation from agreement statistics |
| 16.5 | contrastive loss narrated | InfoNCE/NT-Xent + triplet + in-batch negatives + code |
| 16.7 | RoPE context-extension named | PI/NTK/YaRN scaling derivation for long-context fine-tuning |
| 20.4 | source separation named | SI-SDR objective + mask/band-split math |
| 20.9 | frame interpolation listed | optical-flow warping + RIFE/FILM losses |
| 23.5 | relighting described | inverse-rendering optimization + ambiguity + learned prior |
| 27.3 | A2A protocol narrated | task-lifecycle Algorithm box + JSON-RPC trace |
| 29.3 | research agent narrated | plan-execute-reflect loop + credibility/gap scoring |
| 35.7 | production RAG listed | DSPy compilation trace + corpus-poisoning attack/defense |
| 37.4 | dialogue mechanics in elided code | topic-stack push/pop algorithm + clarification-confidence rule |
| 39.6 | voice pipeline = vendor table | streaming-finalization mechanism recap + cross-ref |
| 42.4 | drift monitoring forwarded out | inline three-drift recap + KL covariate-shift signal |
| 42.8 | YaRN temperature stated | entropy-growth rationale (residual) |
| 43.5 | generation metrics named | FID Frechet formula + KID note (residual) |
| 50.3 | FL privacy threat named | gradient-inversion (DLG/iDLG) derivation + skeleton |
| 53.4 | DP not tied to a budget | formal (epsilon,delta)-DP + Gaussian calibration + cross-ref |
| 57.1 | capacity sizing deferred | model+latency+QPS to GPU-count derivation + code |
| 60.1 | edge use-case matrix | sizing-mechanism callout tying to 60.3 |
| 60.3 | on-device fit asserted | working-set RAM arithmetic, 3B vs 8B worked |
| 73.6 | creative tools survey | brand-consistency-drift production case through the eval loop |
| 77.5 | epilogue, not analytical | framed four-measurable-open-problems research-frontier block |

Also fixed as incidental bugs during the sweep: 11.4 vision code-output/caption
mismatch; 13.6 duplicated 13.5 header; 73.10 What's-Next pointing back instead of
to Chapter 74.

## Strongest parts (no gaps)

- Part 1 (LLM Building Blocks), Part 13 (LLMOps Lifecycle): every non-catalog
  section already COURSE-READY.
- Part 9 (Evaluation): only a self-containment forward-reference, now recapped.

## Out-of-scope follow-ups noted (publication QA, not depth)

These were surfaced by auditors but are link/label hygiene, not depth gaps, so
they were not fixed in this sweep:

- Part 14 stale cross-reference text from an earlier numbering scheme: 67.5
  ("Section 74.2"), 68.5 ("Section 69.1" and a bare "4," bullet), 72.5 (bare
  "4," bullet), 73.8/73.9 ("Section 75.x" references and meta tags).
- A "Section 49.10" cross-reference in module-50 whose target does not exist in
  module-49.

A publication-QA pass (or the existing audit plugins for broken xrefs) should
sweep these.

## Method

15 background subagents, one per part, each reading every section in its part and
writing a per-section verdict table. Fixes were applied by per-part editor
subagents following the Deep-Explanation and Code-Pedagogy agent contracts, then
verified XML-well-formed with no em dashes before commit. Concurrency was
throttled to avoid server-side rate limiting.
