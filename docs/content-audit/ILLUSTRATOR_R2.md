# Illustrator R2 Report

Cycle 3, round 2 of the 31-illustrator agent. Inline SVG figures added to
sections that the IMAGE_OPPORTUNITY audit flagged as missing any figure or
diagram. All figures follow the book's established visual style: viewBox-based,
`role="img"` with descriptive `aria-label`, Segoe UI typography, established
palette (steel blue #3a73a8, slate gray #4a5568, accent orange #d97706, success
green #047857, accent red #b91c1c), 8px corner radii on rounded rects.

Total figures added: 29 sections.

## Figures added (per section)

1. **part-6-agentic-ai/module-26-ai-agents/section-26.2.html** (Figure 26.2.1):
   Three-panel comparison of ReAct loop, plan-and-execute, and tree-search
   planning strategies, with relative compute cost labels.

2. **part-6-agentic-ai/module-26-ai-agents/section-26.4.html** (Figure 26.4.1):
   Scatter plot of agent accuracy vs dollar cost showing the Pareto frontier
   and labeled "dominated" points to justify cost-weighted scoring.

3. **part-6-agentic-ai/module-27-tool-use-protocols/section-27.6.html**
   (Figure 27.6.1): Tool-economy control loop diagram: user request, meta
   planner, router, registry, budget tracker, cache, executor, tools, and
   synthesizer.

4. **part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html**
   (Figure 28.4.1): Four-layer testing pyramid for agent systems (unit,
   integration, scenario, chaos) with per-layer cost and count annotations.

5. **part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.5.html**
   (Figure 32.5.1): Citation pipeline showing retrieved sources, generation
   with inline cites, and NLI / quote-match verifier catching citation
   hallucinations.

6. **part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.7.html**
   (Figure 35.6.1): Compound AI / RAG pipeline as six swappable boxes
   (query rewriter, retriever, reranker, generator, verifier, output) with a
   router across the top.

7. **part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.1.html**
   (Figure 36.1.1): 2x2 quadrant of 2026 vector platforms (managed vs
   self-hosted on horizontal, hybrid vs vector-first on vertical) listing
   the major engines per cell.

8. **part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.4.html**
   (Figure 42.4.1): Two overlapping bell curves visualizing covariate shift
   between validation and production distributions, with the KL marginal
   noted underneath.

9. **part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.8.html**
   (Figure 42.8.1): 7x6 needle-in-a-haystack heatmap with greens at edges and
   a red "lost-in-middle" zone around 25-50% depth at long contexts.

10. **part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.9.html**
    (Figure 42.9.1): OpenTelemetry stack diagram: app SDK auto-instrumentors
    -> OTel collector with GenAI conventions -> swappable backends.

11. **part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.11.html**
    (Figure 42.11.1): Four-tier structured-output validity stack (syntactic,
    schema-compliant, semantic, behavioral) with cheap-to-expensive labels.

12. **part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.4.html**
    (Figure 43.4.1): Bar chart of pass@1, pass@10, pass@100 for two
    hypothetical models showing when scaling test-time sampling pays off.

13. **part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.2.html**
    (Figure 44.2.1): Dashboard grid showing the four metric families
    (quality, safety, operational, behavioral) with example widgets.

14. **part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html**
    (Figure 44.3.1): Three-column comparison of metrics, traces, and logs
    pillars with classical vs LLM additions in each.

15. **part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html**
    (Figure 44.4.1): Cyclic eval-in-prod loop: production traffic -> sample
    -> label -> merge into golden set -> re-eval -> deploy decision.

16. **part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.6.html**
    (Figure 44.6.1): Concentric four-layer model-rotation strategy
    (abstraction, eval suite, second source, runbook) protecting the app.

17. **part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.7.html**
    (Figure 44.7.1): Side-by-side eval-as-CI (linear gate) vs eval-as-product
    (experiment-score-compare-iterate loop).

18. **part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html**
    (Figure 46.2.1): Probability histograms over 1-5 score tokens for argmax
    vs G-Eval probability-weighted scoring, showing the 3 vs 3.18
    discretization gap.

19. **part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.3.html**
    (Figure 46.3.1): Three debiasing axes (position swap, length control,
    rubric anchoring) drawn as three panels.

20. **part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.4.html**
    (Figure 46.4.1): Swap augmentation diagram: one labeled pair becomes two
    training examples in opposite orders, dropping position-flip rate.

21. **part-6-agentic-ai/module-30-tools-of-the-trade/section-30.1.html**
    (Figure 30.1.1): Six-layer agent platform stack from UI to observability
    (AG-UI, A2A, runtime, MCP, sandboxes, observability).

22. **part-6-agentic-ai/module-30-tools-of-the-trade/section-30.4.html**
    (Figure 30.4.1): Six-cell grid of agent benchmark families (SWE, browser,
    tool-use, customer service, general assistants, computer use).

23. **part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html**
    (Figure 30.5.1): Three-panel summary of what agents need from a model
    (tool-call reliability, long-trace coherence, reasoning) vs chat.

24. **part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.1.html**
    (Figure 25.1.1): 2x3 grid of multimodal platforms by modality
    (image/video/audio) and access pattern (closed API vs open weights).

25. **part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.3.html**
    (Figure 36.3.1): Four-tier benchmark pyramid for retrieval (classical IR,
    BEIR, MTEB, end-to-end RAG) with per-tier risks.

26. **part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.4.html**
    (Figure 36.4.1): Three retrieval-model architectures side-by-side
    (bi-encoder, cross-encoder, ColBERT late-interaction) with their score
    functions and pros/cons.

27. **part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.5.html**
    (Figure 46.5.1): Three-judge ensemble that majority-votes on a comparison,
    showing how partly-uncorrelated biases cancel in the aggregate verdict.

28. **part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.6.html**
    (Figure 37.5.1): Memory consolidation pipeline: raw memory log -> four-step
    consolidator (merge, resolve, score, decay) -> compact canonical store.

29. **part-6-agentic-ai/module-30-tools-of-the-trade/section-30.3.html**
    (Figure 30.2.1): Four multi-agent topology patterns side by side
    (hierarchical, peer / debate, pipeline, competitive) with named framework
    and primary failure mode per cell.

## Sections skipped (intentionally)

- Tools-of-the-trade external-reading lists (sections 19.6, 30.5, 36.5, 41.5,
  45.5) are intended as text-heavy bibliographies. No figure benefit.
- HuggingFace library deep-dive sections (19.6, 19.8, 19.9, 19.10, 19.11,
  19.12, 19.13, 19.14) are API walk-throughs; figures would be filler.
- Multimodal tools-of-trade catalogs 25.2 through 25.5 (libraries, datasets,
  models, readings) are catalogs without a single conceptual frame.
- Fun-note callout suggestions on 1.7a, 13.5b, 18.1b, 31.2b, 40.6b, 70.3b
  (these sections already have hero figures and the audit flag is for adding
  fun-note callouts, not figures, which is out of scope for the
  illustrator).
- Section 45.2 (eval libraries deep dive) is similar to 19.X library
  catalogs; would dilute rather than help.

## Style notes for visual-identity reviewer

- Palette uses #3a73a8 (steel blue) for primary, #d97706 (amber/orange)
  for accent / warning, #047857 (green) for positive/success, #b91c1c
  (red) for fail/risk, #4a5568 (slate) for arrows and neutral text,
  #2d3748 for dark labels, #718096 for muted/italic notes.
- All `<defs><marker id="arrow-*">` IDs are unique per file (arrow-planning,
  arrow-tools, arrow-cite, arrow-drift, arrow-evalprod, arrow-evalp,
  arrow-otel, arrow-compound, arrow-swap, arrow-embed) to avoid clashes if
  multiple figures from this batch land on one page.
- All figures use `style="max-width:100%;height:auto;display:block;margin:1.5rem auto;"`
  inline; book.css may want to absorb that into `.illustration figure svg`.
- All `<text>` elements use either Segoe UI (matching existing book figures)
  or default sans-serif inherited from the SVG `font-family` declaration on
  the SVG root.
- Figure numbers chosen by scanning each file's existing `Figure X.Y.N`
  numbers and using the next free integer; references in the figcaption
  match.

## Audit verification

Re-running `agents/book-skills/scripts/audit/run.py --checks IMAGE_OPPORTUNITY`
will show fewer flagged sections after this pass. The fun-note suggestions
that remain are out of scope (fun-injector role, not illustrator).
