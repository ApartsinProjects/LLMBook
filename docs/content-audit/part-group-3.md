# Content Audit — Parts 9-12

This audit covers `part-9-llm-evaluation-observability/` (modules 42-46), `part-10-llm-security-runtime-safety/` (modules 47-51), `part-11-llm-ethics-trust-governance/` (modules 52-56), and `part-12-llm-systems-at-scale/` (modules 57-61).

Numbering note: the post-restructure scheme is **part N -> module M -> chapter M -> section M.x** (module-and-chapter share the same numeric label). Older labels (Part VIII/IX/X, Chapter 44/49/57/63, etc.) appear throughout the source and are flagged below as stale.

A repeating background problem across all four parts: `section-desc` spans across most chapter indexes still say "A comprehensive chapter from the Building Conversational AI textbook." (or "A chapter from..."). Each one needs to be replaced with a real one-line summary of the section. I call this out per-chapter only where there is something else to add; for the cleanup itself, **every chapter except 43, 44, 46, 54 (partial), 56, 59, 61 has this pattern across every section card**. The default boilerplate is a wholesale find-and-replace target.

---

## Part 9: LLM Evaluation & Observability

### Part-level index (`part-9-llm-evaluation-observability/index.html`)

- **Part title**: Header shows "Part VIII: Evaluation of LLM-Based Systems" (lines 8, 24-25); meta description starts "Part VIII: Evaluation & Production" (line 7). **PROPOSE** "Part IX: LLM Evaluation & Observability" to match `toc.html` line 426 ("Part IX · LLM Evaluation & Observability") and the directory's actual ordinal.
- **Subtitle**: line 26 "Rigorous evaluation, observability infrastructure, and production engineering for LLM systems at scale" — keep, but drop "production engineering" (Part 13 owns that now).
- **Part overview** (lines 37-41) says "Chapters: 3 (Chapters 34, 35, and 36)" — **stale**. Should say "Chapters 42-46 (five chapters)".
- **Big Picture** (line 45): generic. **PROPOSE** "Part IX covers the discipline that separates 'demo works' from 'product ships': how to measure LLM quality (Chapter 42), how to evaluate specialized systems like RAG and agents (Chapter 43), how to run production traffic through online monitoring (Chapter 44), how to use LLM judges reliably (Chapter 46), and the eval/observability toolbox (Chapter 45)."
- **Chapter cards** (lines 47-128) are broken:
  - Cards labeled "Chapter 44" (module-42), "Chapter 45" (module-42 monolith), "Chapter 46" (module-43), "Chapter 47" (module-44), "Chapter 48" (module-45), plus a final duplicate "Chapter 46" card (module-46). All chapter numbers in this index are stale by **+2** from the canonical numbering in `toc.html` and in each module's own index.
  - Chapter 44 card lists sections "44.1-44.11" but link targets are `section-42.1.html` through `section-42.9.html` (file names are 42.x), and several entries duplicate the same target file (`section-42.9.html` appears twice as 44.9, 44.10, 44.11). Section 44.8 LLM-as-Judge links to `module-46-llm-as-judge-automated-evaluation/index.html` (correct destination, wrong number).
  - The "Chapter 45 Testing and Evaluation-Driven Quality Gates" card contains a single entry "45.6 Structured-Output Validity Testing" — this is a fossil; no separate chapter 45 with that body exists.
  - Chapter 48 (Tools) card lists 13 sections, several of which are fragment anchors into the same two files (`section-45.1.html` and `section-45.2.html`) — duplicated.
  - The duplicate trailing Chapter 46 card (lines 118-129) does correctly list module-46 sections 46.1-46.5.
- **Fix in one pass**: regenerate this part-index from a single source of truth that matches `toc.html` + each module-index. Remove all references to the old "Chapter 34/35/36/44/45/46/47/48" sequence.

### Chapter 42: LLM Evaluation & Quality Metrics

`part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html`

- **Title**: KEEP "LLM Evaluation & Quality Metrics".
- **Breadcrumb / part label** (line 24): "Part VIII: Evaluation of LLM-Based Systems" — stale. **PROPOSE** "Part IX: LLM Evaluation & Observability".
- **Looking Back callout** (line 38): mentions ten topics including LLM-as-judge and OpenTelemetry as if all in one chapter. Now that LLM-as-Judge moved to Chapter 46 and OpenTelemetry to its own section, rewrite to say: "Chapter 42 is the eval foundations chapter: metrics (perplexity, BLEU, BERTScore), benchmarks (MMLU, HumanEval, MT-Bench), experimental design and statistical rigor, the testing pyramid for LLM applications, observability and tracing, OpenTelemetry, drift detection, reproducibility, and long-context benchmarks. LLM-as-Judge is now a chapter of its own (Chapter 46); specialized eval (RAG, agents, multimodal) is Chapter 43; online monitoring is Chapter 44."
- **Section descriptions**: Every section card has the placeholder `A comprehensive chapter from the Building Conversational AI textbook.` except 42.5 which already has a real description. **All ten** need real descriptions. Proposed wording:
  - 42.1 "Perplexity, BLEU/ROUGE/BERTScore, LLM-as-judge as a baseline pattern, and the major benchmarks (MMLU, HumanEval, MT-Bench, Chatbot Arena)."
  - 42.2 "Bootstrap CIs, paired tests, ablation design, effect-size reporting, and how benchmark contamination distorts every published score."
  - 42.3 "The LLM testing pyramid: deterministic unit tests with mocked responses, assertion-based integration tests, red-team and prompt-injection tests, and CI integration."
  - 42.4 "Concept drift, model drift, embedding drift, prompt drift; what to alert on and what triggers retraining."
  - 42.5 KEEP (already specific).
  - 42.6 "LLM-specific tracing with LangSmith, Langfuse, Phoenix, and OpenTelemetry; spans, traces, and replay-based debugging for non-deterministic systems."
  - 42.7 "Why LLM experiments are harder to reproduce than ML experiments and the prompt-versioning, config, and container patterns that make them reproducible."
  - 42.8 "Needle-in-a-Haystack, RULER, LongBench v2; context-window extension methods (YaRN, NTK-aware scaling) and the gap between claimed and effective context."
  - 42.9 "GenAI Semantic Conventions, auto-instrumentation libraries, custom span attributes for LLM-specific telemetry."
  - 42.10 "Experimental design for LLM papers, contamination as a publication-validity threat, reproducibility expectations from major venues."
  - 42.11 "JSON-schema compliance, function-calling spec compliance, semantic vs syntactic validity; the eval-as-CI hookup for structured output."
- **Ordering issue**: section 42.6 (Observability) is currently placed AFTER 42.5 (Quality Gates), which references "from Section 42.6" the previous-tense observability material. This reads cleanly only if 42.6 comes BEFORE 42.5. **PROPOSE reorder** to: 42.1 Fundamentals -> 42.2 Stats -> 42.3 Testing -> 42.6 Observability & Tracing -> 42.9 OpenTelemetry -> 42.4 Monitoring & Drift Detection -> 42.7 Reproducibility -> 42.5 Quality Gates -> 42.8 Long-Context Benchmarks -> 42.10 Research Methodology -> 42.11 Structured-Output Validity. (Or, more conservatively: move 42.6 and 42.9 to slots 4 and 5, leaving everything else in current order.)
- **Section file numbering inconsistencies**: file `section-42.10.html` carries `<title>Section 42.9: Research Methodology...</title>` and `Section 42.9` in page-current (lines 7-8, 31); file `section-42.11.html` carries `<title>Section 42.9: Structured-Output Validity Testing</title>` and `Section 42.9` in page-current (lines 7-8, 37). Two different files both call themselves Section 42.9 in their own `<title>`/`<div class="page-current">`. Filenames are 42.10 and 42.11 respectively; the index card-list also lists only ten entries (42.1-42.9 plus a duplicate 42.9). **Fix**: update titles, page-current divs, descriptions, and the chapter index to use 42.10 and 42.11; add the 42.11 entry to the index.
- **What's Next** (line 154) links to `index.html` (self) with stale title "Chapter 55". Rewrite to point to Chapter 43 (Specialized Evaluation).
- **Chapter-nav** (lines 156-159): previous "Chapter 43", up "Part VIII", next "Chapter 45" — stale. Should be prev Chapter 41 (the last chapter of Part 8), up "Part IX", next "Chapter 43".

#### Sections, section-by-section

- **42.1 LLM Evaluation Fundamentals**:
  - H1 KEEP.
  - All H2 ids use prefix `34-1-`, the visible numbers say `44.1.1`, `44.1.2`, ... The file is Section 42.1, so subsections should be 42.1.1, 42.1.2, ... Same pattern in every section of this module.
  - **Code Fragment / Figure** captions (lines 146, 204, 322, 393, 464, 511, 575, 689, 786, ...) all say `44.1.x`. Should be `42.1.x`.
  - **Thesis-thread** callout (line 79) references "Chapter 42.2, Chapter 20, Chapter 23.9, Chapter 43" — these conflate chapter and section numbers. Should be "Section 42.2", "Chapter 20", "Section 32.9" (or current RAG numbering), and "Chapter 43 (Specialized Evaluation)".
- **42.2 Experimental Design & Statistical Rigor**:
  - H2 ids prefix `34-2-`, visible numbers `44.2.x` — same stale pattern.
- **42.3 Testing LLM Applications**:
  - H2 ids prefix `34-3-`, visible `44.3.x` — same.
  - Prerequisite paragraph (line 50, "Section 26.1") fine.
- **42.4 LLM-Specific Monitoring & Drift Detection**:
  - H2 only shows `44.4.5 Retraining and Intervention Triggers` plus an Exercises H2 — possibly the section is truncated or earlier H2s use different headings. Need a closer look in editing pass.
  - Big-picture references "Section 42.6" as if it precedes (and link is to `module-44-online-eval-observability/section-44.4.html` — wrong file). Resolve along with the reorder.
- **42.5 Evaluation-Driven Quality Gates**:
  - Big-picture (line 47) mentions "evaluate RAG and agent systems" as if same chapter — but that material is now in Chapter 43. Rewrite as "Sections 42.1-42.3 covered metrics, stats, and testing; this section closes the loop by turning those measurements into pre-deployment, post-deployment, and continuous gates."
- **42.6 Observability & Tracing**:
  - Big-picture (line 38): "production engineering patterns from Section 13.3 introduced the logging and monitoring foundations that observability extends" — fine if 13.3 still discusses logging; check on a later pass.
  - Line 42 prerequisite paragraph: "This section requires the evaluation foundations from Section 42.6 and observability concepts from Section 42.7" — self-reference to its own number (42.6) and a forward reference to 42.7 that reads backward. Rewrite.
  - "What's Next" (line 545) says next is "Section 42.7: LLM Experiment Reproducibility" but the linked file is `section-42.4.html`. Mismatch.
- **42.7 LLM Experiment Reproducibility**:
  - H2 ids `34-7-`, visible `44.7.x`.
  - Big-picture (line 38) links to "Section 42.4" through Section 42.4 (looks like a stale forward/back reference). Verify.
- **42.8 Long-Context Benchmarks**:
  - H1 KEEP.
  - H2 ids `34-9-`, visible `44.9.x`. Stale.
- **42.9 OpenTelemetry for LLM Applications**:
  - H2 ids `34-10-`, visible `44.10.x`. Stale.
  - Tail paragraph references "deployment patterns in Section 45.1" — should be Section 48 or the actual Part-13/14 home of the deployment material.
- **42.10 Research Methodology for LLM Papers** (file `section-42.10.html`):
  - As noted above, the file self-identifies as "Section 42.9" — fix title/meta/page-current.
  - Big-picture (line 45) lists three prerequisites all linking to `section-42.1.html`, but the visible link text says "Section 42.7: LLM Experiment Reproducibility" and "Section 42.1: Evaluation Harness Ecosystems". Fix link targets to match the link text.
  - "What Comes Next" (line 678) links to `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html` and labels it "Section 42.9: LLM Performance Benchmarking and Cross-Hardware Portability" — the linked section is actually Section 57.4 (benchmarking), but it's being framed as if it's the next chapter-internal section. Rewrite to either drop the cross-part jump or label it correctly: "Section 57.4 (Part 12) covers hardware benchmarking."
  - Nav next (line 723) points to 42.11 which is "Structured-Output Validity Testing" — fine, but the chapter index doesn't list 42.11.
- **42.11 Structured-Output Validity Testing** (file `section-42.11.html`):
  - File self-identifies as Section 42.9; fix.
  - Nav next (line 308) points to `section-42.12.html` which doesn't exist. Remove the next-link or point it to Chapter 43 entry.

#### Home fit / consolidation for Chapter 42

- Chapter 42 currently subsumes both eval-design topics (42.1-42.3, 42.7, 42.8, 42.10, 42.11) and observability topics (42.4, 42.6, 42.9). The chapter is wide. With Chapter 44 owning online-eval / observability / monitoring, sections 42.4 (Drift Detection), 42.6 (Observability & Tracing), and 42.9 (OpenTelemetry) sit awkwardly in 42. **Consolidation candidate**: move 42.4, 42.6, 42.9 into Chapter 44, leaving Chapter 42 as pure "offline / pre-launch eval foundations". 42.5 (Quality Gates) sits naturally between the two and can stay where it lives in the reading order regardless of chapter assignment.

### Chapter 43: Specialized Evaluation: RAG, Agents, Multimodal, Long-Context

`part-9-llm-evaluation-observability/module-43-specialized-evaluation/index.html`

- **Title**: KEEP. Clear and accurate.
- **Breadcrumb** (line 23): "Part VIII" — stale.
- **Big Picture** (line 30): "Evaluation methodologies for the 2026 frontier..." — concise but slightly marketing-speak. **PROPOSE** "Generic eval (Chapter 42) doesn't cover the cases that matter most in production. This chapter is the four specialized eval verticals: RAG (faithfulness vs groundedness, Ragas, BEIR), agents (trajectory eval, AgentBench, SWE-Bench, GAIA, τ-bench), simulation-based eval for conversational systems, code generation (pass@k, HumanEval+, LiveCodeBench), and multimodal eval."
- **Section descriptions**:
  - 43.1 KEEP (real description).
  - 43.2 KEEP (truncated mid-word "che" — finish to "...harness, scoring, and contamination checks").
  - 43.3 placeholder. **PROPOSE** "Why static benchmarks fail for conversational agents; τ-bench, τ²-bench, and MM-τ-p2 as user-simulator harnesses; how to write a simulator that doesn't collapse."
  - 43.4 placeholder. **PROPOSE** "pass@k metric, HumanEval and HumanEval+, MBPP, SWE-Bench and SWE-Bench Verified, LiveCodeBench and the contamination-scaling problem."
  - 43.5 placeholder. **PROPOSE** "Vision-language eval (MMMU, VLM-Bench), audio-generation eval, video-generation eval, multimodal RAG eval, cross-modal grounding."
- **Section ordering**: 43.1 (RAG) -> 43.2 (Agentic) -> 43.3 (Simulation) -> 43.4 (Code) -> 43.5 (Multimodal). Simulation-based eval (43.3) is really a subtype of agent eval (43.2) — they're in adjacent slots which is fine. **PROPOSE** ordering: keep as-is, or pull 43.4 (Code) directly after 43.1 (RAG) since pass@k is closer to ground-truth grading than trajectory eval is. Minor.
- **Stale refs in sections**: every H2 in 43.1-43.5 uses visible number `46.x.y` (e.g., `46.1.1`, `46.2.1`...). Sections live in module-43; should be 43.x.y.
- **Chapter-nav** at bottom of index (lines 62, 64) shows prev "Chapter 45", up "Part VIII", next "Chapter 47" — stale; should be prev Chapter 42, up Part IX, next Chapter 44.

### Chapter 44: Online Evaluation, Observability, and Production Monitoring

`part-9-llm-evaluation-observability/module-44-online-eval-observability/index.html`

- **Title**: clear but long. **KEEP** for now; consider shortening to "Online Evaluation and Production Monitoring" since the observability material currently lives in Chapter 42 (see consolidation note above). Final title depends on whether you move 42.6 / 42.9 into this chapter.
- **Big Picture** (line 30): concise but flat. **PROPOSE** "Pre-launch eval (Chapter 42) tells you whether the system works today. Online eval is the discipline of knowing whether it still works tomorrow, after the provider silently updates the model, after the user mix shifts, after the cost curve crosses a threshold."
- **Section descriptions**:
  - 44.4 KEEP (good).
  - 44.5 KEEP (good).
  - 44.6 KEEP (good).
  - 44.7 placeholder. **PROPOSE** "Braintrust, Latitude, Laminar as eval-as-product platforms; the eval-first workflow (experiment, score, compare, iterate); the platform-vs-build decision."
- **Section numbering oddity**: sections are 44.4, 44.5, 44.6, 44.7 — there is NO 44.1, 44.2, 44.3. The 44.1/2/3 slots appear to have been merged into Chapter 42 (or never created). The visible H2 numbering inside 44.4 says `47.4.x`, in 44.7 says `47.7.x` — this is leftover from a numbering where this content was sections 47.4-47.7. **PROPOSE**: renumber sections to 44.1-44.4 (no skipped numbers), or accept that the chapter starts at 44.4 and explain why in the index (preferred: renumber).
- **Stale H2 numbering**: all H2 ids and labels in 44.4-44.7 prefix with `37-x-y` ids and visible `47.x.y` numbers.
- **Chapter-nav** (lines 57, 59): "Chapter 46" prev (should be Chapter 43), "Part VIII" up (should be Part IX), "Chapter 48" next (should be Chapter 45 or 46 — Tools is currently Chapter 45 in toc.html).
- **Stale prose ref**: `section-44.6.html` line 34 says "(which Section 59.2 recommends)" — Section 59.2 is "ZeRO and FSDP" (Part 12), which is unrelated to model-version pinning. Wrong cross-reference; trace to original intent (probably old Section 45.something about model-pinning) and fix.

### Chapter 45: Tools of the Trade: Eval & Production Stack

`part-9-llm-evaluation-observability/module-45-tools-of-the-trade/index.html`

- **Title**: KEEP. Could trim "& Production Stack" since Part 13 owns production now, but the chapter still bundles serving tools (vLLM, TGI, SGLang) so the dual scope is defensible — **PROPOSE** rename to "Tools of the Trade: Eval & Observability Stack" and shift the serving-stack content to Part 13's Tools chapter, OR keep title and accept dual scope.
- **Breadcrumb** line 22: "Part VIII" — stale.
- **Big Picture** (line 35) is concrete and useful — KEEP.
- **Section descriptions**: all five sections say "A chapter from the Building Conversational AI textbook." Each needs a real one-liner:
  - 45.1 "Hosted eval platforms (LangSmith, Braintrust, Vellum) and self-hosted serving platforms (vLLM, TGI, SGLang, Triton)."
  - 45.2 "Eval libraries (lm-evaluation-harness, HELM, OpenAI Evals, Inspect AI, promptfoo, DeepEval), serving SDKs, and OpenTelemetry instrumentation."
  - 45.3 "Standard eval datasets and benchmarks (MMLU, HumanEval, MT-Bench, Chatbot Arena, BIG-Bench, HELM scenarios)."
  - 45.4 "Judge models (Prometheus, Prometheus-2, JudgeLM) and production-serving model picks."
  - 45.5 "Foundational eval and serving papers, active research groups, communities, and conferences."
- **Section ordering**: standard Tools template (Platforms / Libraries / Datasets / Models / External Reading) — KEEP.
- **Stale H2 numbering**: every section uses visible `48.x.y` (old Chapter 48 numbering) instead of `45.x.y`. Sections also each contain a SECOND H2 with `id="45-1-..."` (e.g., 45.1 has `<h2 id="45-1-inference-scaling-and-load-balancing">Inference Scaling and Load Balancing</h2>` at the end) — these look like content stubs spliced in from another chapter to satisfy the cross-references in part-9 index lines 105-113. **Investigation needed**: verify each appended H2 has body content vs being an empty anchor.
- **Chapter-nav** (lines 76-78): "Chapter 47" prev, "Part VIII" up, "Chapter 49" next — stale; should be prev 44, up Part IX, next 46.
- **What Comes Next** (line 73): "Part IX turns to safety..." — should be "Part X turns to safety..."

### Chapter 46: LLM-as-Judge & Automated Evaluation

`part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/index.html`

- **Title**: KEEP. Clear, accurate.
- **Big Picture** (line 26): good — KEEP.
- **Section descriptions**: **ALL FIVE say "Promoted and expanded from old section 42.8."** — these are clearly placeholder breadcrumbs from the restructure. Replacements:
  - 46.1 "Why grading is often easier than generating; cost and latency trade-offs; the cases where LLM-as-Judge is the right tool and the cases where it isn't."
  - 46.2 "Position bias (judges prefer first-presented answers), length bias, verbosity bias, self-preference, and how each one shows up in production."
  - 46.3 "Symmetric-swap eval to neutralize position bias; length-control eval (AlpacaEval LC); verbosity penalties; chain-of-thought scoring (G-Eval) for transparency."
  - 46.4 "Prometheus and Prometheus 2 (rubric-trained), JudgeLM (distilled from GPT-4); training-data construction, swap augmentation, reference-guided judging."
  - 46.5 "Multi-judge ensembles (vote, average, debate), production patterns (caching, sampling, escalation), and meta-evaluation against human panels."
- **Section ordering**: Why -> Biases -> Debiasing -> Training -> Ensembles. Logical. KEEP.
- **Home fit / consolidation**: This chapter was just promoted from old 42.8 and is currently very thin (sections are 44-126 lines each; 46.4 is 44 lines). Each section contains only ONE H2 from the original monster section (44.8.1 through 44.8.5). **Concerns:**
  - As a freestanding chapter, this material is undercooked. Each section should grow to 3-6 subsections to merit its own page.
  - The H2 inside each section is still numbered `44.8.x` (stale).
  - 46.4 (Training Judge Models) is essentially one paragraph plus a warning callout. Either expand to 4-5x current size or merge 46.4 into 46.5.
  - Section descriptions in the index don't describe the content, they describe the restructure history. Already flagged.
- **Stale refs**:
  - All section H2 ids are `34-8-y` and visible labels `44.8.y`.
  - 46.4 line 32 references "the meta-evaluation methods in Section 7 below" — "Section 7" doesn't exist; should be "Section 46.5" (the ensembles & production-patterns section) or removed if 46.5 doesn't actually cover meta-eval methods.

#### Part 9 consolidation summary

Three structural recommendations for Part 9 (in priority order):
1. Renumber every visible subsection inside every section file to match the section's own number (currently 42.1 contains `44.1.x` H2s, etc.).
2. Resolve the section-42.10 / 42.11 duplicate-numbering bug and add 42.11 to the chapter index.
3. Decide whether observability-related sections (42.4, 42.6, 42.9) belong in Chapter 42 or Chapter 44 and move them once. Currently Chapter 44 has no sections 44.1-44.3 because those slots are conceptually filled by 42.4/42.6/42.9.

---

## Part 10: LLM Security & Runtime Safety

### Part-level index (`part-10-llm-security-runtime-safety/index.html`)

- **Part title**: KEEP "Part X: LLM Security & Runtime Safety". Clear.
- **Subtitle / Big Picture** (lines 25, 28): both say "Adversarial threats, guardrails, agent safety, privacy, security tooling." — the literal same sentence. **PROPOSE** new Big Picture: "Part X is the *runtime* safety part: the threats that show up when an attacker takes a real swing at a deployed LLM and the defenses that catch them. Chapter 47 maps the adversarial threat surface; Chapter 48 covers input/output guardrails and content filtering; Chapter 49 covers tool-using agents and sandboxing; Chapter 50 covers privacy attacks and data protection. Chapter 51 is the toolbox. Part 11 covers the slower-moving questions: fairness, regulation, environmental impact, transparency."
- **Chapter cards**: empty `<div class="chapter-card-list"><!-- Chapter cards added by rebuild script --></div>` — the rebuild script never ran, so the part index lists no chapters at all. **Critical fix**.

### Chapter 47: Adversarial Security and Red Teaming

`part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/index.html`

- **Title (H1, line 25)**: KEEP "Adversarial Security and Red Teaming".
- **Meta title (line 8)**: "Chapter 47: Safety, Ethics & Regulation" — stale and wrong (that's old combined chapter). Fix to match H1.
- **Breadcrumb** (line 24): "Part IX: LLM Safety, Security, and Ethics" — stale. Should be "Part X: LLM Security & Runtime Safety".
- **Figure caption** (line 34): "Figure 49.0.1" — wrong number; should be 47.0.1.
- **Looking Back callout** (line 38): "Parts III-VIII built and operated LLM systems. Part IX zooms out to..." — Part IX in the old map was the safety-ethics-regulation combo. Now this chapter is in Part X. Rewrite Looking Back to: "Part IX (the previous part) measured LLM quality. Part X turns to the question of whether the system survives a deliberate attack. This chapter is the threat map: adversarial attacks, jailbreaks, prompt-injection taxonomies, and red-teaming as an engineering discipline."
- **Chapter Overview** (lines 41-57): refers to "Chapter 45", "Chapter 20", "Chapter 31" with old numbering and lists topics that span the entire old Part IX (bias, model cards, environmental impact, EU AI Act, federated learning, machine unlearning, licensing). Most of these now live in Part 11. Rewrite to focus only on Chapter 47's actual two sections (47.1 threats, 47.2 red-teaming).
- **Big Picture** (line 61): generic for old combined chapter. **PROPOSE** "Adversaries treat your LLM as an attack surface. Section 47.1 catalogs the threat families (OWASP LLM Top 10, MITRE ATLAS, prompt-injection variants). Section 47.2 covers red-teaming as an engineering practice: PyRIT, Garak, HarmBench, JailbreakBench, and how to wire automated red-team runs into CI."
- **Learning Objectives** (lines 65-79): nine of the thirteen objectives are about content that has been moved out of this chapter (bias, EU AI Act, model cards, environmental impact, differential privacy, federated learning, machine unlearning, licensing). Trim to the four that apply to 47.1/47.2.
- **Prerequisites** (lines 83-88): "Chapter 45 Production Engineering and Operations" — now Chapter 62. "Chapter 14 Prompt Engineering" — now Chapter 12. "Chapter 44 Evaluation and Observability" — now Chapter 42. "Chapter 20 Alignment, RLHF, and DPO" — still 20. Update all four numbers.
- **Section descriptions**: both 47.1 and 47.2 say "A comprehensive chapter from the Building Conversational AI textbook." Replace:
  - 47.1 "OWASP Top 10 for LLM apps, MITRE ATLAS threat categories, prompt-injection variants (direct, indirect via retrieved content, multi-turn), jailbreaks, and the layered-defense baseline."
  - 47.2 "PyRIT and Garak as automated red-team toolkits; HarmBench and JailbreakBench as benchmark suites; manual playbooks; CI integration; multimodal red-teaming."
- **What's Next** (line 105): links to module 49 ("Chapter 50: Agent Safety & Security") — but Chapter 48 (Guardrails) is the next chapter in Part 10. Fix to point to module 48.
- **Chapter-nav** (lines 108-110): "Chapter 48", "Part IX", "Chapter 50" — all stale.
- **47.1 LLM Security Threats**:
  - File `section-47.1.html`. H1 KEEP. The grep output for H2s on 47.1 shows only Exercises and What-Comes-Next H2s, but the file has 1300+ lines — most H2s likely have non-standard IDs. The visible numbering in Code Fragment captions is `49.1.x` (lines 185, 251, ...) — stale.
  - Line 227 says "A redaction layer scans text for emails, phone numbers, SSNs, and other sensitive patterns, replacing them with placeholders before the data reaches the model... Code Fragment 49.1.4 below..." — but next captioned Code Fragment is `49.1.2`. So prose says fragment 49.1.4 but the labeled fragment is 49.1.2. Mismatch in numbering.
- **47.2 Red Teaming Frameworks**:
  - H1 KEEP.
  - Visible H2 numbering `49.8.x` — stale. Should be 47.2.x.
  - Line 42: "Section 14.4" (old prompt-injection numbering) — confirm whether the current Chapter 12 (Prompt Engineering) has section 12.4 with prompt injection.
  - Line 42: "Section 45.3" — the link target is `part-13-llmops-lifecycle/module-62-production-engineering-core/section-62.1.html` and the link text says "Section 45.3". Mismatch. Either text or target is stale.
  - Line 679: "Section 47.9: EU AI Act Compliance in Practice" — but the link target is `section-47.1.html`. EU AI Act material was moved to Chapter 53 (Part 11). Update text and target.
  - Nav prev `section-47.1.html` correct; nav next links to 48.1 correct.

### Chapter 48: Guardrails and Runtime Safety

`part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/index.html`

- **Title (H1)**: KEEP "Guardrails and Runtime Safety".
- **Meta / title bar** (line 8): "Chapter 40: Guardrails and Runtime Safety" — wrong number (was 40 in some draft). Fix to 48.
- **Page H1 header element** "Chapter 40" in pagefind meta injection (line 24) — stale.
- **Breadcrumb** (line 20): "Part IX: LLM Safety, Security, and Ethics" — stale.
- **Big Picture** (line 27): generic. **PROPOSE** "Guardrails are the runtime *layer* of safety: they don't change the model, they add fast filters before and after every model call. This chapter covers input guardrails (prompt-injection detection, PII redaction with Microsoft Presidio), output guardrails (Llama Guard, NeMo Guardrails, ShieldGemma, Guardrails AI), policy DSLs and constrained decoding as safety mechanisms, and multimodal guardrails for image, audio, and video content."
- **Section descriptions**: every section says "A comprehensive chapter from..."
  - 48.1 "What guardrails are vs alignment vs policy; the three layers (input, output, tool-call); cost/latency budgets; the lifecycle of a guardrail."
  - 48.2 "Threat model at the input stage; Prompt Guard 2 and regex baselines; multilingual and encoding attacks; PII redaction with Microsoft Presidio; topic and policy classification."
  - 48.3 "Llama Guard 3 (open-source standard), NeMo Guardrails and Colang DSL, ShieldGemma (model-size trade-offs), Guardrails AI (Pydantic-native), and the integrated deployment."
  - 48.4 "Outlines and Guidance for constrained decoding; NeMo Colang as a policy DSL; Pydantic schemas as safety contracts; when constrained decoding is the *wrong* tool."
  - 48.5 "Image content classification (hosted APIs), image-prompt-injection as a defense layer, audio/video streaming pipelines, cross-modal policy consistency."
- **Section ordering**: KEEP. What guardrails are -> input -> output -> constrained -> multimodal is a clean buildup.
- **Stale refs** in 48.1:
  - Line 55: "Sophisticated jailbreaks (covered in Section 49.1)" — but link is to `module-47-adversarial-security-red-team/section-47.1.html`. Wrong text (49.1 -> 47.1).
  - Line 57: "Section 57.1" — link to `module-54-watermarking-provenance/section-54.6.html`. The Model Cards section is now in Chapter 54 (provenance), not Section 57.1. Update text.
  - Line 112: three cross-refs at end of paragraph all stale ("Section 51.1", "Section 52.2", "Section 81.2"). Should be "Section 49.1", "Section 50.1", and "Section 51.2".
- **Chapter-nav** (lines 59-61): "Chapter 49 / Part IX / Chapter 51" — stale.

### Chapter 49: Agent Safety & Security

`part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/index.html`

- **Title (H1)**: KEEP "Agent Safety & Security".
- **Breadcrumb** (line 22): "Part IX: LLM Safety, Security, and Ethics" — stale.
- **Big Picture** (lines 30-33): mostly good. References "Chapter 49 covered safety and regulation for LLMs that talk" — but Chapter 49 IS this chapter. Two paragraphs in, line 31 says "Chapter 49 covers safety and security for LLMs that act." So the same chapter is contrasted with itself. The intent is clearly: "Chapter 47/48 covered safety for LLMs that talk; Chapter 49 covers safety for LLMs that act." Fix the chapter numbers in both sentences.
- **What Comes Next** (line 64): "Chapter 60 consolidates the Part IX safety toolchain" — should be "Chapter 51 consolidates the Part X safety toolchain".
- **Section descriptions**: all four placeholder.
  - 49.1 "Agent threat model, prompt-injection vectors specific to tool-using agents (indirect injection via retrieved documents, tool-output injection), defense-in-depth design."
  - 49.2 "Docker and container-based isolation, gVisor and Firecracker for stronger isolation, resource limits, and abuse-prevention patterns."
  - 49.3 "The b3 benchmark, τ-bench under simulated user pressure, safe-tool design (principle-of-least-authority APIs), and the methodology of agent security benchmarks."
  - 49.4 "SBOM generation with Syft, vulnerability scanning with Trivy, image signing with Cosign, the SLSA framework, and CI hardening for agent sandbox images."
- **Section ordering**: 49.1 threat model -> 49.2 sandboxing -> 49.3 benchmarks -> 49.4 supply chain. Logical. KEEP.
- **Stale refs**: every section's H2 numbering visible labels use `51.x.y` prefix (49.1 = `51.1.x`, 49.2 = `51.2.x`, 49.3 = `51.6.x` — note the gap, was old section 51.6 not 51.3, suggests these were 3 different sections in an old monster chapter), 49.4 = `51.7.x`. Renumber.

### Chapter 50: Privacy and Data Protection

`part-10-llm-security-runtime-safety/module-50-privacy-data-protection/index.html`

- **Title**: KEEP "Privacy and Data Protection".
- **Breadcrumb** (line 20): "Part IX" — stale.
- **Big Picture** (line 27) is short; **PROPOSE** "Even a model that refuses every harmful prompt can still leak training data, betray membership inference, and serve as an information-extraction channel. This chapter covers privacy attacks (training-data extraction, membership inference, contextual-integrity violations), differential privacy as the math-backed defense, and machine unlearning for the right-to-be-forgotten / copyright-removal use case."
- **Section descriptions**: both placeholder.
  - 50.1 "Training-data extraction attacks, membership inference, differential privacy for fine-tuning, contextual-integrity and PII leakage, defense-in-depth."
  - 50.2 "Why unlearn (GDPR right-to-be-forgotten, copyright removal, safety alignment), gradient-ascent and task-vector methods, and how to evaluate unlearning quality."
- **Section count**: only 2 sections. Reasonable for a 2-topic chapter, but if you want symmetry with neighboring chapters, consider adding a federated-learning section (currently mentioned in the breadcrumb of Chapter 47's overview as content that exists in this part but no longer has a home).
- **Stale H2 numbering**: 50.1 = `52.2.x`, 50.2 = `52.5.x`. Renumber.
- **Chapter-nav** (lines 44-46): "Chapter 51 / Part IX / Chapter 53" — stale.

### Chapter 51: Tools of the Trade: Safety & Guardrails Stack

`part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/index.html`

- **Title**: KEEP.
- **Breadcrumb** (line 22): "Part IX" — stale.
- **Big Picture** (line 35): concrete, useful — KEEP.
- **Section descriptions**: all five say "A chapter from the Building Conversational AI textbook." Replace:
  - 51.1 "Moderation APIs (OpenAI, Azure Content Safety, AWS Comprehend Toxicity), hosted red-team platforms (HiddenLayer, Lakera), governance platforms."
  - 51.2 "Guardrails frameworks (NeMo Guardrails, Guardrails AI, Llama Guard, ShieldGemma), red-team libraries (Garak, PyRIT), privacy-preserving training (Opacus, TF Privacy)."
  - 51.3 "Harmful-output benchmarks (AdvBench, HarmBench, JailbreakBench), bias and fairness datasets, truthfulness benchmarks (TruthfulQA, HaluEval)."
  - 51.4 "Safety classifier models (Llama Guard, ShieldGemma, Prompt Guard) and constitutional / reward models for safety."
  - 51.5 "Foundational safety papers and reports, active research groups (METR, Apollo, Redwood), communities and venues."
- **Stale H2 numbering**: every section uses `60.x.y` prefix.
- **What Comes Next** (line 73): "Part X turns to the product side..." — should be "Part XI turns to the slower governance questions..."
- **Chapter-nav** (lines 76-78): "Chapter 59 / Part IX / Chapter 61" — stale. Chapter 59 was old "Frontier Safety", which no longer exists in this position. Should be prev 50, up Part X, next 52.

---

## Part 11: LLM Ethics, Trust & Governance

### Part-level index (`part-11-llm-ethics-trust-governance/index.html`)

- **Part title**: KEEP "Part XI: LLM Ethics, Trust & Governance".
- **Part Overview / Big Picture**: literal duplicate sentences ("Bias and hallucination, provenance and transparency, regulation and compliance, frontier safety.") at lines 25 and 28. Also, "hallucination" is mentioned but the only hallucination section is hidden as 52.2 (orphaned from Chapter 52's index, see below) — content scope statement is loose.
- **PROPOSE** Big Picture: "Part XI covers the slow-moving non-runtime questions: bias and fairness (Chapter 52), regulatory frameworks and compliance (Chapter 53), watermarking and provenance for synthetic media plus the transparency-documentation stack of model cards / datasheets / system cards (Chapter 54), environmental impact and Green AI (Chapter 55), and the responsible-AI tools that knit it all together (Chapter 56). Where Part X was about defending the system *today*, Part XI is about the institutional commitments that determine whether the system is *allowed to exist next year*."
- **Chapter cards**: the `<div class="chapter-card-list">` is empty (rebuild-script comment). Only Chapter 56 has a manually-added trailing card. Same fix needed as Part 10's index.

### Chapter 52: Bias, Fairness, and Disparate Impact

`part-11-llm-ethics-trust-governance/module-52-bias-fairness/index.html`

- **Title**: KEEP.
- **Breadcrumb** (line 20): "Part IX: LLM Safety, Security, and Ethics" — stale.
- **Chapter Overview** (lines 30-32) is good — KEEP.
- **Big Picture** (line 35): generic. **PROPOSE** "LLMs trained on internet text inherit the unequal distributions of that text. This chapter covers the sources of LLM bias (data, training, alignment, deployment), measurement (CrowS-Pairs, BBQ, demographic-parity probes), cross-cultural NLP and pluralistic alignment, model cards as documentation, and the mitigation patterns (counterfactual augmentation, distributional alignment) that move models toward fairer behavior."
- **Section count**: chapter index lists ONE section (52.1), but `section-52.2.html` exists (H1 "Why LLMs Hallucinate and How to Catch Them"). **Critical**: either add 52.2 to the index, or move 52.2 to a Hallucination chapter / section elsewhere. Hallucination is technically a *truthfulness* issue, not a *bias/fairness* issue — it does not belong in a fairness chapter. **PROPOSE** either:
  - Promote 52.2 to a new Chapter "Hallucination and Truthfulness" sitting between 52 and 53 (matches the chapter-nav forward-link in 52's own nav which says "Chapter 54: Hallucination and Truthfulness"), OR
  - Merge 52.2 into Chapter 54 (provenance / detection-of-synthetic-content has overlap with hallucination detection).
- **Section descriptions**: 52.1 placeholder.
  - 52.1 "Sources of bias across the LLM lifecycle (data, training, RLHF, deployment); measurement with CrowS-Pairs, BBQ, demographic-parity probes; model cards and datasheets; cross-cultural NLP and pluralistic alignment; mitigation patterns."
- **Section 52.1 internal issues**:
  - File has two `<div class="callout big-picture">` opens; only one expected per section. Duplicate Big Picture suggests a merge of two sub-sections.
  - File has TWO H2 with id `37-3-1-` (different titles: "Sources of Bias" and "Cultural Bias in LLMs") — duplicate `id` attributes.
  - All Figure / Code Fragment captions labeled `53.1.x` AND a stretch labeled `49.10.x` (lines 365, 426, 456, 524) — this is a merge of an old 49.10 section into 53.1, with stale numbering on both halves.
- **Chapter-nav** (lines 47-49): "Chapter 52 / Part IX / Chapter 54" — first should be Chapter 51, middle Part XI, third 53.

### Chapter 53: Regulation, Compliance, and Governance

`part-11-llm-ethics-trust-governance/module-53-regulation-compliance/index.html`

- **Title**: KEEP.
- **Breadcrumb** (line 20): "Part IX" — stale.
- **Big Picture** (line 27): concise label list. **PROPOSE** "Regulation of AI moved from theoretical to operational between 2023 and 2026. This chapter covers the global landscape (EU AI Act, GDPR, US executive orders, sector-specific regs in healthcare and finance), the EU AI Act in practice (risk tiers, GPAI obligations, conformity assessment), enterprise risk governance (NIST AI RMF, ISO 42001, SR 11-7), and the LLM-specific intersections with licensing, IP, and privacy law."
- **Section descriptions**: all four placeholder.
  - 53.1 "EU AI Act risk tiers, GDPR for LLM systems, sector-specific regulations (healthcare, finance, public sector)."
  - 53.2 "Risk classification, GPAI obligations, automated compliance checking, conformity assessment, implementation milestones."
  - 53.3 "Comparing NIST AI RMF / ISO 42001 / SR 11-7; model-inventory practices and risk classification at the organization level."
  - 53.4 "Model-license taxonomy (Apache 2.0, OpenRAIL, Llama Community License), differential privacy for LLM training, IP ownership of LLM outputs."
- **Section ordering**: 53.1 landscape -> 53.2 EU AI Act drill-down -> 53.3 enterprise risk governance -> 53.4 licensing/IP/privacy. Reasonable. Some teams would put licensing first (since it's the constraint most engineers hit first) but the current order is fine.
- **Stale refs**:
  - Section 53.1 line 42: "Section 49.3" / "Section 14.3" — stale. Bias is Section 52.1; prompt-injection defenses are Section 12.4 (current Prompt Engineering chapter).
  - Section 53.1 line 127: "Section 44.6" — link target `module-42-evaluation-foundations/section-42.6.html`. The link text and link target are now disconnected (text says 44.6, file is 42.6).
  - Section 53.1 nav prev (line 375): "Section 52.2 Why LLMs Hallucinate" — the file exists but is not exposed in Chapter 52's index. Coordinate with the 52.2-disposition decision above.
  - Section 53.4 line 38: "Section 8.2" link target `module-07-modern-llm-landscape/section-7.2.html`. Mismatched numbering.
  - Section 53.4 line 42: "Section 49.5" / "Section 18.1" / "Section 7.1" — stale.
  - All section H2 numbering visible `55.x.y` (53.1 = 55.1.x, 53.2 = 55.2.x, 53.3 = 55.5.x, 53.4 = 55.7.x). Renumber.
- **Chapter-nav** (lines 53-55): "Chapter 54 / Part IX / Chapter 56" — stale.

### Chapter 54: Watermarking, Provenance, and Deepfake Defense

`part-11-llm-ethics-trust-governance/module-54-watermarking-provenance/index.html`

- **Title**: clear but no longer accurate. **PROPOSE** rename to "Provenance, Transparency, and Documentation" or "Provenance and Documentation: Watermarks, Model Cards, System Cards". Reason: the chapter currently contains TEN sections, only five of which are about provenance/deepfakes (54.1-54.5). Sections 54.6-54.10 cover Model Cards, Datasheets, System Cards, Audit Trails, and Explainability — all transparency/documentation topics that belong with provenance under the umbrella concept of "verifiable claims about AI artifacts." The title needs to reflect both halves.
- **Meta description** (line 7): "Chapter 46" — stale chapter number.
- **Breadcrumb** (line 20): "Part IX" / "Chapter 46" — stale.
- **Big Picture** (line 27): too narrow. **PROPOSE** "How do you tell synthetic from real content (54.1-54.5: watermarks, C2PA, deepfake detection)? And how do you document the AI artifacts well enough that downstream consumers can trust them (54.6-54.10: model cards, datasheets, system cards, audit trails, explainability for high-stakes decisions)? Both halves share a single theme: verifiable claims about AI."
- **Section count in index vs filesystem**: index lists 5 sections (54.1-54.5); filesystem has 10 (54.1-54.10). The Provenance and Documentation sections (54.6-54.10) are orphaned from the index. **Critical fix**: add 54.6 through 54.10 to the index. Alternatively, split into Chapter 54 (Provenance, 5 sections) and a new Chapter "Transparency and Documentation" (5 sections). The chapter-nav of 54.7 already calls itself "Chapter 57: Transparency, Documentation, and Auditability" — that title is a survivor from a pre-restructure split, and reusing it is one defensible option.
- **Section descriptions**:
  - 54.1 placeholder. **PROPOSE** "Why provenance broke when generation got cheap; five mission-critical domains (news, art, science, evidence, identity); cooperative vs adversarial generators; the 2026 policy landscape."
  - 54.2 placeholder. **PROPOSE** "The Kirchenbauer green-list watermark, SynthID-Text (Google) tournament sampling, robustness analysis (what survives paraphrase, what doesn't), and practical deployment."
  - 54.3 placeholder. **PROPOSE** "C2PA manifests, c2patool pipelines, SynthID-Image pixel-domain watermarking, Adobe Content Credentials, the publisher workflow from camera to CDN, and video provenance."
  - 54.4 placeholder. **PROPOSE** "GAN-vs-diffusion fingerprints, video temporal artifacts as decisive signals, audio detection (formants and breath), the detector half-life arms race."
  - 54.5 placeholder. **PROPOSE** "The imperceptibility-robustness trade-off, paraphrase as a text-watermark removal attack, regeneration as image attack, C2PA stripping, and the realistic role of provenance technology."
  - 54.6 (in filesystem, not index). **PROPOSE** "Model cards anatomy, real examples (Llama 3.1, Claude 3.5/3.7 Sonnet), procurement workflows, failure modes and anti-patterns."
  - 54.7 (in filesystem, not index). **PROPOSE** "Datasheets for datasets, seven canonical sections, C4 and The Pile as worked examples, Hugging Face dataset cards, Google Know Your Data, completeness audits."
  - 54.8 (in filesystem, not index). **PROPOSE** "Model card vs system card, OpenAI and Anthropic system-card formats, Google's Frontier Safety Framework, what system cards leave out, regulatory use."
  - 54.9 (in filesystem, not index). **PROPOSE** "Three purposes of logging, what to log for an LLM system, retention policies by regime, tamper-resistance (write-once, hash-chained), insider-threat access controls."
  - 54.10 (in filesystem, not index). **PROPOSE** "LIME, SHAP, attention visualization (useful but misleading), mechanistic interpretability for high-stakes decisions, the right-to-explanation under EU AI Act, system architectures for shipping explanations."
- **Section ordering**: 54.1 (why) -> 54.2 (text) -> 54.3 (image/video) -> 54.4 (detection) -> 54.5 (limitations) is a clean buildup for the provenance half. Adding the transparency half: keep 54.6-54.10 grouped together, ordered model card -> datasheet -> system card -> audit trails -> explainability. If kept as one chapter, the natural flow is provenance-first then documentation-second; if split, see above.
- **Stale refs in 54.6-54.10**: each carries breadcrumb "Chapter 57: Transparency, Documentation, and Auditability" (e.g., 54.7 line 27) — fix the breadcrumb to match wherever the sections end up.
- **Stale prose refs**:
  - 54.7 line 158: "Section 57.3 moves up the abstraction ladder..." — Section 57.3 in the new numbering is GPU Procurement Strategy. Should read "Section 54.8 moves up..."
  - 54.10 line 110: "Hooked into the audit-logging pipeline from Section 57.4" — Section 57.4 is hardware benchmarking. Should be "Section 54.9".
  - 54.10 nav next (line 155): jumps to `module-55-environmental-sustainability/section-55.1.html` — fine, but the back-link should also be sane.
- **Chapter-nav** (lines 59-61): "Chapter 55 / Part IX / Chapter 57" — stale.

### Chapter 55: Environmental Impact and Sustainability

`part-11-llm-ethics-trust-governance/module-55-environmental-sustainability/index.html`

- **Title**: KEEP.
- **Breadcrumb** (line 20): "Part IX" — stale.
- **Chapter Overview** (line 31): good — KEEP.
- **Big Picture** (line 35): label list. **PROPOSE** "Training a frontier model emits hundreds of tons of CO2 equivalent. Inference at scale emits more, every day. This chapter covers the carbon-accounting frameworks (CodeCarbon, ML CO2 Impact Calculator), the engineering choices that cut emissions (model size, hardware, batching, regional energy mix), and the regulatory pressure (EU AI Act energy disclosures) that's moving Green AI from optional to required."
- **Section count**: index lists 1 section (55.1), filesystem has 2 (55.1, 55.2). 55.2 is "AI Governance and Open Problems" — clearly orphaned from Chapter 55. It does not belong in an environmental chapter. **PROPOSE** either:
  - Move 55.2 to Chapter 53 (Regulation/Compliance/Governance) as a new closing section.
  - Spin it out into a new "Frontier Safety and Open Problems" chapter (the chapter-nav next link in 55 currently calls it "Chapter 59: Frontier Safety and Open Problems" — that's a pre-restructure ghost we can revive deliberately if there's enough content).
  - Delete if redundant.
- **Section descriptions**: 55.1 placeholder.
  - 55.1 "Training carbon footprint, training efficiency metrics, strategies for reducing footprint, carbon-tracking tools (CodeCarbon, eco2AI, Carbontracker), the rebound effect, the EU AI Act energy disclosure regime, and a practical Green AI checklist."
  - 55.2 IF kept: "AI governance frameworks at the open-problem layer..." — but recommend move.
- **Stale H2 numbering**: 55.1 uses `58.1.x` visible labels.
- **Stale prose refs in 55.1**:
  - Line 51: "Section 7.1" / "Section 49.3" / "Section 49.9" all stale. Section 49.x doesn't have bias or AI Act material anymore.
  - Line 200: "Section 45.1" — should be Section 9.x (inference optimization) or 48.x (production tools).
  - Lines 603-606: "Section 19.5" / "Section 10.2" / "Section 45.1" — verify current numbering.
  - Line 614: "Section 49.9" — should be Section 53.2 (EU AI Act in practice).
  - Line 633: "Section 44.3" — should be Section 42.3.
- **Chapter-nav** (lines 47-49): "Chapter 57 / Part IX / Chapter 59" — stale.

### Chapter 56: Responsible AI Tools of the Trade

`part-11-llm-ethics-trust-governance/module-56-responsible-ai-tools/index.html`

- **Title**: KEEP. Chapter is brand-new, skeletal, as expected.
- **Big Picture** (line 26): KEEP (decent description of scope, even if the sections themselves are empty).
- **Section descriptions**: real one-liners — KEEP, but as the sections fill in, these can become more specific. For now they describe the *intent* not the content.
- **Section count**: 5 sections, all stubs (~55 lines each). Each section has 3-4 empty H2 placeholders (Commercial Platforms, Open-Source Platforms, Selection Criteria) and a 3-entry bibliography that reuses the generic "Karpathy State of GPT" / "HuggingFace OpenLLM Leaderboard" / "Anthropic Building Effective Agents" boilerplate. **Critical content-gap**: this chapter currently has no useful content.
- **Section 56.4** has **two** `<div class="callout big-picture">` opens (duplicate Big Picture block). Same template error appears in other 56.x files: file is templated but not authored.
- **What this chapter should cover** (to flesh out): platforms (Fiddler, Credo AI, Holistic AI, IBM watsonx.governance), libraries (Fairlearn, AIF360, IBM AI Explainability 360, SHAP, LIME, Captum), datasets/benchmarks (BBQ, BOLD, StereoSet, RealToxicityPrompts, CivilComments), bias-detection models (Toxicity / Perspective API, Detoxify, hate-speech classifiers), external reading (Algorithmic Justice League, AI Now Institute, FAccT conference, Mozilla AI).
- **Chapter-nav**: bottom shows only an `up` link to Part XI. No prev/next. Add prev (Chapter 55) and next (Chapter 57 in Part 12).
- **Section 56.x nav backlinks** (e.g., `section-56.1.html` line 48) point to `module-55-environmental-sustainability/section-55.2.html` (the orphaned AI Governance & Open Problems section). If 55.2 gets moved, fix this nav.

---

## Part 12: LLM Systems at Scale

### Part-level index (`part-12-llm-systems-at-scale/index.html`)

- **Part title**: KEEP "Part XII: LLM Systems at Scale".
- **Big Picture / Part Overview**: duplicate sentences again ("Compute planning, distributed training systems, hardware and chip diversity, edge and on-device LLMs.").
- **PROPOSE** Big Picture: "Part XII covers the systems-engineering layer behind frontier LLM work: how to plan compute capacity (Chapter 57), how to use non-NVIDIA silicon, decentralized training, and edge runtimes (Chapter 58), how distributed training actually works (Chapter 59), how on-device LLMs ship (Chapter 60), and the scale toolbox (Chapter 61). Where Part 13 will cover the LLMOps lifecycle (gateways, routing, registry), this part covers the lower-level systems substrate."
- **Chapter cards**: `<div class="chapter-card-list"><!-- Chapter cards added by rebuild script --></div>` is empty. Three trailing manually-added cards exist (Chapter 60 / 59 / 61 — note the wrong order!): the displayed chapters jump 60, 59, 61. Also Chapter 57 and 58 are entirely missing from the part index. **Critical fix**: regenerate part index with all five chapter cards in 57-58-59-60-61 order.

### Chapter 57: Compute Planning & Infrastructure

`part-12-llm-systems-at-scale/module-57-compute-planning/index.html`

- **Title**: KEEP "Compute Planning & Infrastructure".
- **Breadcrumb** (line 22): "Part X: LLM Operations and Production Infrastructure" — stale.
- **Big Picture** (lines 31-32): mostly good but pretends Chapter 57 is the start of a part about MVP-to-scale. **PROPOSE** "Once the prototype works, capacity planning becomes the dominant cost question. This chapter covers GPU tier selection (H100 / H200 / Blackwell GB200 / Trainium2 / TPU v5p), the canonical inference stacks (vLLM 0.6+, NVIDIA TensorRT-LLM, SGLang), enterprise-integration patterns, GPU procurement strategy (spot vs reserved economics), and how to benchmark LLM performance across hardware."
- **Section descriptions**: all four placeholder.
  - 57.1 "Three workload categories (training, fine-tune, inference), 2026 GPU tiers, comparing GPU options, capacity-planning timeline."
  - 57.2 "Five integration domains (auth, observability, data, compliance, billing), two reference architectures (centralized gateway, federated services), pattern comparison."
  - 57.3 "Four procurement tiers (on-demand, spot, reserved, committed-use), spot economics for LLM workloads, reserved-capacity playbook, comparing venues."
  - 57.4 "MLPerf training and inference suites, inference benchmarking (TTFT/TPOT/throughput), cross-hardware portability, advanced inference scheduling, KV cache as distributed resource."
- **Section ordering**: 57.1 sizing -> 57.2 integration -> 57.3 procurement -> 57.4 benchmarking. Reasonable. Some teams would put benchmarking (57.4) before procurement (57.3) since benchmark results drive procurement decisions. Worth a swap.
- **Stale H2 numbering**: 57.1-57.3 use `50.x.y` visible labels (was Chapter 50 in old numbering); 57.4 uses `61.4.x` (was Chapter 61).
- **Stale prose**:
  - "What Comes Next" (line 59): "Section 57.1" link self-references (pointing to its own section 57.1 as "the next concrete topic"); then "Chapter 68: Scaling Economics: Unit Costs & ROI" link target `part-14-designing-llm-agent-products/module-69-llm-economics/index.html`. Verify the destination still exists and the chapter number.
- **Chapter-nav** (lines 62-64): "Chapter 60 / Part X / Chapter 62" — stale; prev should be 56 (Tools of Trade), up Part XII, next 58.

### Chapter 58: Frontier Systems & Hardware

`part-12-llm-systems-at-scale/module-58-frontier-systems-hardware/index.html`

- **Title**: KEEP "Frontier Systems & Hardware".
- **Breadcrumb** (line 22): "Part XII: Frontiers" — stale; should be "Part XII: LLM Systems at Scale".
- **Big Picture** (line 35): excellent, content-rich, anchored to dated industry events — KEEP.
- **Section descriptions**: all five placeholder.
  - 58.1 "Cerebras CS-3 (wafer-scale), Groq LPU now inside NVIDIA Vera Rubin, Tenstorrent RISC-V chiplet, AMD MI355X second-source, and the 2026 silicon-market consolidation story."
  - 58.2 "DeMo algorithmic core (bandwidth 1000-10000x lower), DisTrO toolkit, Nous Psyche internet-scale training; what 2027 has to settle."
  - 58.3 "MLX (Apple's tensor framework), Apple Intelligence foundation models, Llama-Mobile and the small-open frontier, runtime comparison."
  - 58.4 "Why each GPU generation rewrites the attention kernel, algorithm/kernel pipelining co-design for Blackwell, the wider inference-kernel ecosystem, non-NVIDIA silicon implications."
  - 58.5 "Inference-aware scaling laws, MoE as the canonical co-design case, speculative decoding and draft-model patterns, multi-stage inference pipelines."
- **Section ordering**: 58.1 silicon -> 58.2 decentralized -> 58.3 edge -> 58.4 kernels -> 58.5 co-design. Mixed organization: 58.1 and 58.4 are both about silicon details; 58.2 and 58.3 are both about deployment-location choices. **PROPOSE** reorder: 58.1 silicon -> 58.4 kernels -> 58.5 co-design (silicon group) -> 58.2 decentralized -> 58.3 edge (deployment-location group). Or keep current order if the existing prose builds in the current sequence — verify.
- **Stale H2 numbering**: all five sections use `63.x.y` visible labels.
- **Stale prose**:
  - "What Comes Next" (line 75): "Chapter 64 closes Part XII..." — Chapter 64 is in Part 13 now. The "this whole part has been building toward" reference is to AGI Trajectories, which is in Part 16. Update.
  - Chapter-nav (lines 78, 80): prev "Chapter 83: Frontier Theory & Cognition", next "Chapter 85: AGI Trajectories" — both in Part 16. So this chapter currently navs to Part 16 instead of to the rest of Part 12. **Critical**: prev should be Chapter 57, next should be Chapter 59.

### Chapter 59: Distributed Training Systems

`part-12-llm-systems-at-scale/module-59-distributed-training-systems/index.html`

- **Title**: KEEP "Distributed Training Systems".
- **Meta description** (line 6): "Chapter 59: Distributed Training Systems. Tools of the trade reference." — wrong description (this is not a Tools chapter). Fix to: "Parallelism strategies, memory-efficient training (ZeRO/FSDP), and production training infrastructure."
- **Big Picture** (line 26): good — KEEP.
- **Section descriptions**: REAL one-liners (5 of 5) — KEEP.
- **Section count**: 5 sections — all skeletal (55 lines each, ~3 paragraphs of body, 3-entry bibliography that reuses the same ZeRO / Megatron-LM / FSDP citations across every section). **Critical content-gap**: this is one of the gap-fill chapters and currently has effectively no content. Same skeleton as Chapter 56 and 61.
- **Section 59.1** has **two** `<div class="callout big-picture">` opens.
- **Section ordering**: 59.1 fundamentals -> 59.2 ZeRO/FSDP -> 59.3 Megatron/tensor -> 59.4 pipeline/hybrid -> 59.5 production. Logical; KEEP.
- **Chapter-nav**: only an `up` link. Add prev (Chapter 58) and next (Chapter 60).
- **What Comes Next**: absent. Add one.

### Chapter 60: Edge & On-Device LLMs

`part-12-llm-systems-at-scale/module-60-edge-on-device-llms/index.html`

- **Title**: KEEP "Edge & On-Device LLMs".
- **Meta description** (line 6): "Chapter 60: Edge & On-Device LLMs. Production LLM systems engineering." — generic; replace with "Running LLMs on consumer hardware: llama.cpp, Ollama, MLX, ExecuTorch, mobile constraints."
- **Big Picture** (line 26): KEEP (good).
- **Section descriptions**: 60.1 placeholder ("Promoted from old Ch 62 monster.") — **the most blatant restructure-artifact in this part group**.
  - 60.1 **PROPOSE** "Why edge deployment matters; llama.cpp as universal C/C++ inference; Ollama for developer-friendly local model management; MLX for Apple Silicon; ExecuTorch for PyTorch on mobile; battery and thermal constraints."
- **Section count**: 1 section. The chapter is essentially a single oversized section. Consider splitting 60.1's six H2s into 3-4 sections (e.g., one for runtimes — llama.cpp/Ollama/MLX/ExecuTorch — and one for constraints/optimization). Currently the chapter and the section are functionally the same artifact.
- **Stale H2 numbering**: 60.1 uses `53.5.x` visible labels (it was Section 53.5 in old numbering, suggesting it sat in an old Chapter 53 — confirmed: this is content "moved as cross-part from old LLMOps Ch 62" per user-provided context).
- **Cross-cut**: Chapter 60 (Edge) has substantial overlap with Section 58.3 (Edge LLMs: MLX, Apple Intelligence, Llama-Mobile). MLX is covered in BOTH 58.3 and 60.1. Decide which is the canonical home and cross-reference from the other. **PROPOSE** 58.3 covers "the high-level edge ecosystem and where the frontier is" while 60.1 covers "how to actually deploy: build, quantize, ship". Then have 58.3 close with "see Chapter 60 for the deployment playbook" and 60.1 open with "see Section 58.3 for the broader edge ecosystem context."
- **Chapter-nav**: only `up` link. Add prev (Chapter 59) and next (Chapter 61).

### Chapter 61: Scale Tools of the Trade

`part-12-llm-systems-at-scale/module-61-scale-tools/index.html`

- **Title**: KEEP "Scale Tools of the Trade". (Could trim to "Tools of the Trade: Systems at Scale" for parallelism with Chapters 45/51/56 — minor.)
- **Big Picture** (line 26): KEEP — concrete and useful.
- **Section descriptions**: REAL one-liners (5 of 5) — KEEP, but they describe intent rather than authored content (sections are stubs).
- **Section count**: 5 stub sections, each 55 lines (same template as Chapter 56 and 59). Each section is empty H2s plus 3-entry placeholder bibliography. **Critical content-gap**: needs authoring like Ch 56 and 59.
- **Section 61.x nav backlinks** (e.g., `section-61.1.html`) point to `module-60-edge-on-device-llms/section-60.1.html` — fine.
- **Chapter-nav**: only `up` link. Add prev (Chapter 60). No "next" needed (end of part) or add "next" pointing to Part 13's first chapter (62).
- **What Comes Next**: absent. Add one pointing to Part 13.

---

## Cross-cutting findings (apply across Parts 9-12)

1. **Old-number H2 prefix everywhere.** Every subsection visible label inside every section file uses the OLD chapter number, not the current one. Examples: file `section-42.1.html` has H2s `44.1.1`, `44.1.2`, ... A global find-and-replace based on `(file's current chapter number).x.y` is needed. Same problem in Code Fragment captions and Figure captions. This is the single highest-impact cosmetic bug.
2. **Stale "Section N.M" cross-references in body prose.** Body paragraphs and prerequisite lists frequently use old section numbers in the visible link text while the `href` already points to the renamed file. Most prevalent in Parts 9-11. Each file needs a sweep for `Section [0-9]+\.[0-9]+` strings against the actual destination file's current section number.
3. **Stale breadcrumbs / nav part labels.** Most module index files and many section files have breadcrumb text "Part VIII", "Part IX: LLM Safety, Security, and Ethics", "Part X: LLM Operations and Production Infrastructure", "Part XII: Frontiers" — all old part names. They need to be updated to match the new part titles in `toc.html`.
4. **Chapter cards missing from part indexes.** Parts 10, 11, and 12 part-level indexes all show `<div class="chapter-card-list"><!-- Chapter cards added by rebuild script --></div>` with no cards. Part 9 has a card list that's full but with stale chapter numbers and a duplicate Chapter 46 card. The rebuild script that's supposed to populate these has not run successfully against the current structure.
5. **Empty/skeletal chapters needing authoring**: Chapter 56 (Responsible AI Tools), Chapter 59 (Distributed Training Systems), Chapter 61 (Scale Tools). All three are gap-fill chapters from the restructure with the same 55-line stub template (empty H2s + placeholder bibliography). They list real-sounding section titles but contain no substantive content yet.
6. **Section orphaning / misplacement issues**:
   - `section-52.2.html` (Why LLMs Hallucinate) exists but is missing from Chapter 52's index. Doesn't belong in the bias chapter regardless.
   - `section-55.2.html` (AI Governance and Open Problems) exists but is missing from Chapter 55's index. Doesn't belong in the environmental chapter.
   - `section-54.6.html` through `section-54.10.html` exist but are missing from Chapter 54's index. These are Transparency/Documentation topics that should either (a) be added to Chapter 54 with a rename of Chapter 54, or (b) split into a new chapter.
7. **Title-vs-filename mismatches.** `section-42.10.html` has `<title>Section 42.9: Research Methodology...</title>`; `section-42.11.html` has `<title>Section 42.9: Structured-Output Validity Testing</title>`. Two files both claim "Section 42.9" in their visible title.
8. **Duplicate chapter cards on toc-style indexes.** Part 9 index has Chapter 46 listed twice (once as the mis-numbered LLM-as-Judge slot at sec-num 44.8 inside the Chapter 44 card, and once as a standalone trailing Chapter 46 card). Part 11 index has Chapter 56 manually appended after the empty chapter-card-list.
9. **Old "Promoted from..." restructure artifacts in two places**: `module-46-llm-as-judge-automated-evaluation/index.html` (five `section-desc` spans say "Promoted and expanded from old section 42.8") and `module-60-edge-on-device-llms/index.html` (one `section-desc` says "Promoted from old Ch 62 monster."). These need real one-line descriptions.
10. **Generic placeholder description**: `A comprehensive chapter from the Building Conversational AI textbook.` (and the variant `A chapter from the Building Conversational AI textbook.`) appears in nearly every section card across Chapters 42, 43, 44, 45, 47-51, 52, 53, 54.1-54.5, 55, 57, 58. This is the default boilerplate for unfilled descriptions and the user explicitly called this out. Every one needs a real one-liner.

## Top-priority fixes (if forced to pick five)

1. **Renumber every visible subsection / figure / code-fragment caption** to match the current chapter/section number (kill all `44.x.y`, `47.x.y`, `49.x.y`, `50.x.y`, `51.x.y`, `52.x.y`, `53.x.y`, `55.x.y`, `58.x.y`, `60.x.y`, `61.x.y`, `63.x.y` H2 labels across the four parts).
2. **Resolve section-orphans**: add `section-52.2`, `section-55.2`, `section-54.6` through `section-54.10` to their chapter indexes (or move them). Fix `section-42.10` / `section-42.11` self-titles.
3. **Repopulate part-level chapter cards** for Parts 10, 11, 12 (and fix Part 9's broken card list).
4. **Replace all placeholder `section-desc`** values with real one-liners. Same for the Ch 46 "Promoted from..." spans and the Ch 60 "Promoted from old Ch 62 monster" span.
5. **Update every breadcrumb / part-label / chapter-nav prev-next** in section and chapter files (Parts VIII/IX/X labels, old chapter numbers in nav, wrong destinations like Ch 58's nav going to Part 16).
