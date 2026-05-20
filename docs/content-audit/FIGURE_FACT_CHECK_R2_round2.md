# Figure Fact-Check Round 2 (Round 2 pass)

Agent: 39-figure-fact-checker (R2 run 2)
Branch: v2.0
Date: 2026-05-19
Scope: spot-check of ~40 figures across the book, focused on R2 illustrator output (29 new figures in modules 25, 26-28, 30, 32, 35, 36, 37, 42-46), plus tables/bar/heat plots in eval/scaling/cost sections and a sweep of fact-dense industry chapters (Parts 14, 15, 16) that the first R2 pass did not cover.

## Method
1. Pulled the 29-figure illustrator R2 list from `docs/content-audit/ILLUSTRATOR_R2.md` and confirmed which had not been checked in the first R2 pass (`FIGURE_FACT_CHECK_R2.md`).
2. For each candidate, opened the SVG content, the figcaption, the aria-label, and the surrounding prose. Triangulated counts, percentages, named entities, and structural claims.
3. Also spot-checked older fact-dense figures in Parts 12-16 not covered in R1.
4. Only fixed claims where one of {caption, alt/aria-label, SVG content, prose} disagreed with the others. Did not regenerate any SVGs; all fixes are caption / alt-text / aria-label edits.

## Fixes Applied

### 1. Section 28.4 - Figure 28.4.1 (Four-layer testing pyramid)
- BEFORE: caption said "A healthy suite has hundreds of unit tests at the base and only a handful of chaos drills at the peak."
- ISSUE: the SVG count column actually labels Unit tests as "~thousands", Integration tests as "~hundreds", Scenario tests as "~50 to 200", and Chaos as "~5 to 20". The caption collapsed unit tests to "hundreds", contradicting the SVG.
- AFTER: caption now reads "thousands of unit tests at the base, hundreds of integration tests, dozens of scenario tests, and only a handful (5 to 20) of chaos drills at the peak."
- File: `part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html`

### 2. Section 35.7 - Figure 35.6.1 aria-label (Compound AI pipeline)
- BEFORE: aria-label said "Compound AI pipeline with six stages: query rewriter, retriever, reranker, generator, verifier, and router".
- ISSUE: the SVG shows five swappable stages (query rewriter, retriever, reranker, generator, verifier) feeding into an Output box, with the router branching beneath the main flow as a separate routing element, not a sixth stage in sequence.
- AFTER: aria-label now reads "Compound AI pipeline with five swappable stages (query rewriter, retriever, reranker, generator, verifier) feeding an output, with a router branching beneath the main flow".
- File: `part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.7.html`

### 3. Section 46.2 - Figure 46.2.1 (G-Eval argmax annotation)
- BEFORE: SVG annotation said "discards p(4) = 0.40".
- ISSUE: the figure's own formula and caption use the probability distribution p1=0.05, p2=0.20, p3=0.35, p4=0.32, p5=0.08 (which sums to 1.0 and gives the displayed score of 3.18). The argmax panel claimed p(4)=0.40, contradicting the formula's p(4)=0.32.
- AFTER: annotation now reads "discards p(4) = 0.32", consistent with the formula and the bar heights.
- File: `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html`

### 4. Section 30.4 - Figure 30.4.1 aria-label (Agent benchmark families)
- BEFORE: aria-label said "Five-cell grid of agent benchmark families".
- ISSUE: the SVG actually shows six cells (Software engineering, Browser/web, Tool-use mechanics, Customer service, General assistants, Computer use); the caption and prose both say "six families".
- AFTER: aria-label now reads "Six-cell grid of agent benchmark families: software engineering, browser/web, tool-use mechanics, customer service, general assistants, and computer use".
- File: `part-6-agentic-ai/module-30-tools-of-the-trade/section-30.4.html`

### 5. Section 30.5 - Figure 30.5.1 aria-label (What agents need from a model)
- BEFORE: aria-label said "Radar-style comparison of four model qualities important for agents: tool-call accuracy, long-trace coherence, reasoning, and multimodal grounding".
- ISSUE: the SVG is not a radar chart, it is three rectangular panels. The first panel covers tool-call reliability plus reasoning depth, the second covers long-trace coherence plus context window plus code specialty, and the third lists how agent workloads differ from chat. No multimodal-grounding axis appears anywhere in the SVG.
- AFTER: aria-label now reads "Three-panel summary of what agents need from a model: tool-call reliability (with reasoning depth), long-trace coherence (with context window and code specialty), and how agent workloads differ from chat".
- File: `part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html`

### 6. Section 67.3 - Figure 67.3.1 aria-label (Legal compliance rules)
- BEFORE: aria-label and title element said "Five legal-LLM compliance rules and how three jurisdictions diverge".
- ISSUE: the figure actually shows FOUR jurisdictions (California 2023, Florida 2024 Op 24-1, Texas 2024, EU AI Act 2024/1689). The caption already says "four jurisdictions"; only the SVG title and aria-label were wrong.
- AFTER: both aria-label and the `<title>` element now say "four jurisdictions".
- File: `part-14-applications-of-llms-across-industries/module-67-legal-llms/section-67.3.html`

### 7. Section 72.3 - Figure 72.3.1 SVG title (Federal frameworks)
- BEFORE: SVG title text said "Eight overlapping frameworks for US federal LLM deployments".
- ISSUE: the SVG actually draws only seven framework boxes (numbered 1-7), and the figcaption itself says "seven overlapping frameworks ... with NIST AI RMF as the cross-cutting voluntary baseline". The prose mentions eight, but NIST AI RMF (item 8) is treated as cross-cutting rather than drawn as a box. Caption and SVG drawing are consistent at seven boxes plus NIST as overlay; only the SVG title disagreed.
- AFTER: SVG title now reads "Seven overlapping frameworks for US federal LLM deployments (plus NIST AI RMF as voluntary baseline)".
- File: `part-14-applications-of-llms-across-industries/module-72-government-llms/section-72.3.html`

## Verified Without Changes

The following R2 figures were spot-checked and caption/SVG/prose triangulation passed:

- Figure 26.2.1 (Planning spectrum): three planning strategies (ReAct, Plan-and-Execute, Tree Search) match caption; compute-cost labels per panel are consistent.
- Figure 26.4.1 (Pareto frontier): 4 frontier points (52%, 68%, 84%, 93%) and 2 dominated orange points; the (62%, $0.75) point is correctly dominated by Premium (84%, $0.55).
- Figure 27.6.1 (Tool-economy control loop): meta-planner, tool router, registry, budget tracker, result cache, executor with search/compute/paid-API sub-tools, synthesizer; matches caption.
- Figure 32.5.1 (Citation pipeline): three-panel pipeline with retrieved sources, generation with inline cites, NLI/quote-match verifier catching 90-day citation hallucination; numbers in panel match caption (NLI=0.94, NLI=0.91).
- Figure 36.1.1 (Vector platform 2x2 quadrant): all four quadrants correctly populated with the named engines per the prose deep-dives.
- Figure 36.3.1 (Retrieval benchmark pyramid): four tiers (Classical IR, BEIR cross-domain, MTEB embedding leaderboards, end-to-end RAG); caption matches.
- Figure 36.4.1 (Three retrieval architectures): bi-encoder, cross-encoder, ColBERT late-interaction; caption matches.
- Figure 37.5.1 (Memory consolidation): four-step consolidator (merge duplicates, resolve conflicts, importance score, decay + archive) producing canonical store with PostgreSQL/MongoDB resolved conflict and three coffee mentions merged.
- Figure 42.4.1 (Covariate shift bell curves): P_validation vs P_production curves shifted right; KL marginal note correct.
- Figure 42.8.1 (NIAH heatmap): 6x7 grid with red lost-in-middle zone in middle depth at long contexts; caption stays in the spirit of the SVG (red is centered near 50% depth, which is within the caption's "25 to 50 percent depth" range when reading the upper edge of the dark cells).
- Figure 42.9.1 (OpenTelemetry stack): Application -> OTel Collector -> Backends matches caption.
- Figure 42.11.1 (Four-tier validity stack): syntactic, schema-compliant, semantic, behavioral; matches caption.
- Figure 43.4.1 (pass@k bars): Model A 29%/59%/72% and Model B 90%/94%/96% bar heights are proportional; the 30-point gap heuristic in the footer is generic guidance, not a per-figure claim.
- Figure 44.2.1 (Dashboard four-family grid): quality / safety / operational / behavioral panels match caption.
- Figure 44.3.1 (Three observability pillars): metrics, traces, logs with classical-vs-LLM rows; matches caption.
- Figure 44.4.1 (Eval-in-prod loop): production traffic -> sample -> label -> merge -> deploy decision -> re-run eval cycle.
- Figure 44.6.1 (Four-layer model rotation): concentric abstraction / eval suite / second source / runbook; caption matches.
- Figure 44.7.1 (Eval-as-CI vs eval-as-product): CI gate panel + 4-stage product loop (Experiment-Score-Compare-Iterate).
- Figure 46.3.1 (Three debiasing axes): position swap, length control, rubric anchoring; 4-axis rubric correctly inside the rubric panel (not the same as the 3 debiasing axes).
- Figure 46.4.1 (Swap augmentation): r_1 vs r_2 with y=1, then r_2 vs r_1 with y=2 (still r_1 wins); position-flip rates 15-25% vs 2-5% match caption.
- Figure 46.5.1 (Three-judge ensemble): GPT-4 (A), Claude (A), Prometheus (B); majority A wins 2/3; matches caption.
- Figure 25.1.1 (Multimodal platform 2x3 grid): closed API vs open weights x image/video/audio rows; matches caption.
- Figure 30.1.1 (Six-layer agent stack): UI / A2A / runtime / MCP / sandbox / observability layers; matches caption.
- Figure 30.2.1 (Four multi-agent topologies): hierarchical, peer/debate, pipeline, competitive; SVG panels match caption.
- Figure 52.3.1 (Web vs speaker share): English 60% web / 12% speakers, Mandarin <2% web / 13% speakers, Hindi <0.1% / 8%, Bengali <0.1% / 4%, Swahili <0.05% / 2%; bar widths consistent with the labeled percentages within rounding.
- Figure 58.3.2 (Apple Intelligence three-tier routing): 70-85% on-device, 10-25% Private Cloud Compute, 3-7% partner; the partner-tier "consent + escalate" annotation is consistent with the caption claim.
- Figure 66.2.1 (Champion-challenger gates): four assertion gates with 0.923/0.971/412 ms/+0.005 values all match the caption.
- Figure 67.3.1 (Seven LLM capabilities log-cost bar chart): seven capabilities mapping to Table 67.3.1 cost columns; SaaS plan dashed lines at $9, $50, $500/month consistent with the prose.
- Figure 67.4.1 (Four risk tiers): T1 PM / T2 Eng lead / T3 Business VP / T4 Legal+Compliance+VP owners; cumulative guardrail layers; matches caption.
- Figure 67.5.4 (LLM product iteration cycle): four stages (evaluate, tune, A/B test, ship); caption matches.
- Figure 67.10.2 (Five role patterns): drafter, classifier, router, researcher, verifier mapped to autonomy gradient; matches caption.
- Figure 67.13.1 (Five-stage Prototype Playbook ladder): four gates between stages; gate criteria match (5+ inputs OK / cite sources / 80% task done / regression green).
- Figure 67.4.1 (Verified-RAG five layers): layer 5 (citation verification) is the legal-specific addition; matches caption.
- Figure 68.3.1 (Five regulatory tracks): SR 11-7 / EU AI Act / FINRA 24-09 / DORA / CFPB tracks each map to the artifact the caption names.
- Figure 70.2.1 (AI-detection error rates): FP 4-9% native, 8-18% non-native, FN >50% paraphrased; preponderance 51% and clear-and-convincing 75-85% reference lines; cost arithmetic (5000 students * 4% FP * $5-15K = $1-3M/year) checks out.
- Figure 75.2.1 (Three scaling axes): GPT-3.5 / GPT-4 / GPT-5 progression, CommonCrawl / FineWeb 15T / Llama-3 15T data points, direct / o1-R1 / o3 test-time points; consistent with prose.
- Figure 40.2.2 (Latency budget table): row sums for pipeline (800-2400 ms) and native (320-1100 ms) are within rounding of additive sums; the caption explicitly notes ASR finalization plus streamable output as the savings driver, and the key-insight callout right after clarifies that the "Total end-to-end" row accounts for stage overlap rather than naive summation.

## Notes on Scope

- Did not flag the Section 67.13.1 ladder's stale "Ch 18, 19" / "Ch 21, 22" / "Ch 28" / "Ch 29" labels because those are a v1->v2 chapter-renumbering artifact rather than a fact-check issue; flagged to the chapter-numbering / cross-reference agent's lane.
- Did not regenerate any SVGs; all fixes are SVG-internal text (titles, annotations) or surrounding caption / aria-label edits that bring the figure's metadata in line with what the figure already shows.
- The R1 fact-check fixes and the first R2 pass (`FIGURE_FACT_CHECK_R2.md`) remain valid and were not revisited.

## Suggested Follow-Up

- Figure 67.13.1's chapter labels (Ch 11, 12 / Ch 18, 19 / Ch 21, 22 / Ch 28 / Ch 29) are v1 numbering; the linked anchors in the same section already point to v2 modules. A cross-reference pass should rewrite the in-figure labels to match (likely Ch 12 / Ch 31-32 / Ch 32-35 / Ch 42 / Ch 62 in v2 numbering). Flagged for the cross-reference / renumbering agent.
- Figure 72.3.1 still has the asymmetry that NIST AI RMF is the eighth listed framework in prose but is drawn outside the seven-box grid. Caption and title now match, but a future illustrator pass could either drop the eighth list item or add an eighth box to fully reconcile.
