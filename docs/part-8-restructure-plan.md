# Part 8 Restructure Plan — Evaluation-Only Refocus + Chapter 35 Migration to Part 10

**Author**: Architecture planning pass, 2026-05-16
**Status**: DESIGN (no files moved yet)

---

## Section A — Current State Map

Word counts are plain-text after HTML stripping. Destination "P8/Eval" = stays evaluation-focused in Part 8; "P10/Prod" = moves to Part 10 production engineering; "Split" = section's content gets divided across multiple destinations.

### Chapter 34 — LLM Evaluation & Quality Metrics (12 sections, ~63,732 words)

| Sec | Title | Words | Topic family | Proposed destination |
|-----|-------|------:|--------------|----------------------|
| 34.1 | LLM Evaluation Fundamentals | 6,816 | Intrinsic + reference metrics, LLM-as-judge intro, human eval, standard benchmarks | P8 Ch34 (Foundations) |
| 34.2 | Experimental Design & Statistical Rigor | 5,971 | Bootstrap CI, paired tests, effect sizes, ablations, contamination | P8 Ch34 (Foundations) |
| 34.3 | Testing LLM Applications | 5,045 | Unit/integration tests, red-team, promptfoo, security regression | P8 Ch35 (Testing & Quality Gates) |
| 34.4 | LLM-Specific Monitoring & Drift Detection | 2,314 | Drift, covariate shift, intervention triggers (stub-like; only 34.4.5 visible) | P8 Ch37 (Online Eval & Production Monitoring) — and consolidate w/ overlapping Part 10 §49.x |
| 34.5 | Evaluation-Driven Quality Gates | 4,909 | Quality gates, regression testing, golden sets, CI integration | P8 Ch35 (Testing & Quality Gates) |
| 34.6 | Observability & Tracing | 4,149 | Tracing concepts, Langfuse, LangSmith, alerting | P8 Ch37 (Online Eval & Production Monitoring) |
| 34.7 | LLM Experiment Reproducibility | 4,160 | Hydra, DVC, MLflow, W&B, Docker | P8 Ch34 (Foundations) — appended to experiment-design grouping |
| 34.8 | LLM-as-Judge: Reliability, Debiasing, Training Judge Models | 6,255 | Bias taxonomy, G-Eval, Prometheus, JudgeLM, meta-eval | P8 Ch34 (Foundations) — adjacent to 34.1's judge intro |
| 34.9 | Long-Context Benchmarks and Context Extension | 6,260 | NIAH, RULER, LongBench, RoPE/YaRN, position interpolation | P8 Ch36 (Specialized Eval: Long-Context & Capability) |
| 34.10 | OpenTelemetry for LLM Applications | 4,597 | OTel, OpenLLMetry, trace propagation, dashboards (note: lab is MLflow — mislabeled, move lab to 34.7's destination) | P8 Ch37 (Online Eval & Production Monitoring) |
| 34.11 | Research Methodology for LLM Papers | 8,000 | Experiment design, reproducibility, baselines, human eval IAA, p-hacking | P8 Ch34 (Foundations) — but section is over-broad; trim overlap with 34.2 / 34.7 |
| 34.12 | LLM Performance Benchmarking & Cross-Hardware Portability | 6,256 | MLPerf, TTFT/TPOT, TPU/ROCm/Gaudi, Sarathi-Serve, KV-cache | **P10/Prod (relocate to Part 10 Ch46 Compute Planning)** — this is hardware/serving perf, not eval quality |

### Chapter 35 — LLMOps & Deployment Engineering (9 sections, ~45,492 words)

| Sec | Title | Words | Topic family | Proposed destination |
|-----|-------|------:|--------------|----------------------|
| 35.1 | Application Architecture & Deployment | 4,132 | FastAPI, LitServe, Docker, AWS Bedrock, GCP Vertex, Modal | P10 Ch48 (Shipping & Deploying) |
| 35.2 | Frontend & User Interfaces | 4,029 | Gradio, Streamlit, Chainlit, Vercel AI SDK | P10 Ch48 (Shipping & Deploying) |
| 35.3 | Scaling, Performance & Production Guardrails | 4,967 | Latency, rate limiting, queues, NeMo Guardrails, Llama Guard, ShieldGemma | **Split**: scaling/latency -> P10 Ch48; guardrails -> Part 9 (Safety) Ch37 or Ch38; production memory -> P10 Ch48 |
| 35.4 | LLMOps & Continuous Improvement | 4,168 | Prompt versioning, A/B testing, online eval, data flywheels, model registry | **Split**: LLMOps process -> new P10 Ch (Production Engineering); online-eval pieces -> P8 Ch37 |
| 35.5 | AI Gateways and Model Routing | 4,447 | LiteLLM, Portkey, semantic routing, fallback chains, semantic cache, budget | P10 Ch48 (Shipping & Deploying) — or its own section in the new P10 Production Engineering chapter |
| 35.6 | Workflow Orchestration & Durable Execution | 6,344 | Temporal, Inngest, LangGraph persistence, retries, idempotency | P10 new "Production Engineering" chapter |
| 35.7 | Edge & On-Device LLM Deployment | 4,607 | llama.cpp, Ollama, MLX, ExecuTorch, GGUF, mobile constraints | P10 new "Production Engineering" chapter |
| 35.8 | Reliability Engineering for LLM Applications | 6,325 | Failure taxonomy, circuit breakers, SLOs, chaos engineering | P10 new "Production Engineering" chapter |
| 35.9 | Kubernetes-Native LLM Operations | 6,473 | Kueue, Volcano, KServe, MIG, autoscaling, scale-to-zero | P10 new "Production Engineering" chapter |

### Chapter 36 — Tools of the Trade: Eval & Production Stack (5 sections, kept)

| 36.1–36.5 | Platforms / Libraries / Datasets / Models / External Reading | small | Reference appendix | **Split**: split into eval-only tools (P8) and production-only tools (merge into P10 Ch50 Tools toolkit). |

---

## Section B — Proposed New Part 8 Structure

**Title (unchanged)**: Part VIII — Evaluation of LLM-Based Systems
**Subtitle (new)**: "Rigorous evaluation of LLM systems: from intrinsic metrics through agentic and online evaluation."

**Target chapter count**: 5 chapters (4 substantive + 1 Tools of the Trade). Total sections ~28–32.

### Chapter 34 — Foundations of LLM Evaluation (renumbered, retitled)

Source for sections: 34.1, 34.2, 34.7, 34.8, 34.11 (trimmed)

1. **34.1** LLM Evaluation Fundamentals — Metrics & Benchmarks *(from old 34.1)*
2. **34.2** Experimental Design & Statistical Rigor *(from old 34.2)*
3. **34.3** LLM-as-Judge: Reliability, Debiasing & Training Judge Models *(from old 34.8)*
4. **34.4** Reproducibility: Configs, Tracking & Containers *(from old 34.7 + the misplaced MLflow lab from old 34.10)*
5. **34.5** Research Methodology for LLM Papers *(from old 34.11, trimmed: extract overlapping content already covered in 34.2/34.4)*
6. **34.6** Human Evaluation Methodology & Inter-Annotator Agreement *(promoted from buried 34.11.5; expanded with annotation codebook + human-rater study patterns; pulls in `human-labeling` skill content)*

**Rationale**: Today, judge-model and human-eval material is buried as a sub-section of 34.11. Both are first-class evaluation topics in 2026 and warrant their own section. The misplaced "Lab: End-to-End MLOps Pipeline with MLflow" inside 34.10 belongs with reproducibility/tracking content.

### Chapter 35 — Testing & Evaluation-Driven Quality Gates (new chapter, mostly from existing material)

Source for sections: 34.3, 34.5, plus new red-team-eval content

1. **35.1** The LLM Testing Pyramid: Unit, Integration, Regression *(from old 34.3.1–34.3.3)*
2. **35.2** Adversarial Testing & Red Teaming for Evaluation *(from old 34.3.4 + 34.3.6 + new content from `red-teaming` scout)*
3. **35.3** Evaluation-Driven Quality Gates & Golden Sets *(from old 34.5)*
4. **35.4** CI/CD Integration: promptfoo & Assertion-Based Eval *(from old 34.3.5)*
5. **35.5** Security Regression Testing & OWASP LLM Top 10 *(from old 34.3.6, expanded)*
6. **35.6** Structured-Output Validity Testing *(NEW — JSON Schema match, JSON-mode, function-calling spec compliance; gap identified)*

**Rationale**: "Testing" and "quality gates" are conceptually a unit — both are *automated, pre-deployment* validation. They deserve their own chapter, distinct from intrinsic-metric eval. Section 35.6 fills a documented 2026 gap (production structured outputs are everywhere; eval coverage is thin).

### Chapter 36 — Specialized Evaluation: RAG, Agents, Multimodal & Long-Context (NEW chapter — biggest delta)

Source: scouted content + existing 34.9

1. **36.1** RAG Evaluation: Ragas, BEIR, Faithfulness & Groundedness *(NEW; covers Ragas 6–12 metric expansion, retrieval/generation/end-to-end layers, faithfulness vs groundedness)*
2. **36.2** Agentic Evaluation: AgentBench, SWE-Bench, GAIA, τ-bench *(NEW; covers tool-use, multi-step trajectories, dual-control settings)*
3. **36.3** Simulation-Based Evaluation: τ-bench & MM-τ-p2 *(NEW; dialogue agents w/ simulated users, database-state goal comparison)*
4. **36.4** Code-Generation Evaluation: HumanEval, MBPP, SWE-Bench Verified, LiveCodeBench *(NEW; pass@k metrics, decontamination, real-GitHub-issue benchmarks)*
5. **36.5** Multimodal Evaluation: Vision-Language, Audio, Video *(NEW; CLIPScore, VQA-style benchmarks, perceptual quality)*
6. **36.6** Long-Context Benchmarks & Context Extension Methods *(from old 34.9 — kept intact)*

**Rationale**: 2026 frontier eval *is* this chapter. The current chapter 34 has roughly 80% of its body weight on general-purpose eval (perplexity, BLEU, MMLU) and almost no agentic / RAG-specific / multimodal coverage. This is the largest content gap.

### Chapter 37 — Online Evaluation, Observability & Production Monitoring (new chapter, eval-of-production focus)

Source: 34.4, 34.6, 34.10, 35.4 (online-eval pieces)

1. **37.1** LLM Tracing Concepts & Distributed Spans *(from old 34.6.1)*
2. **37.2** Observability Platforms: Langfuse, LangSmith, Phoenix, Helicone *(from old 34.6.2–34.6.4 + scouted 2026 landscape updates: Datadog LLM Obs, Honeycomb, Laminar)*
3. **37.3** OpenTelemetry for LLM Applications *(from old 34.10, minus the misplaced MLflow lab)*
4. **37.4** Online Evaluation & Feedback Loops *(from old 35.4.3 + new content)*
5. **37.5** A/B Testing & Online Experimentation *(from old 35.4.2)*
6. **37.6** Drift Detection: Five Flavors & Their Responses *(from old 34.4, consolidated with Part 10's existing 49.2)*
7. **37.7** Eval-as-Product: Braintrust, Latitude, eval-first workflows *(NEW; from scout — closes the gap)*

**Rationale**: Online evaluation is *evaluation*, not production engineering. By grouping tracing + drift + online experiments here, we keep Part 8 cohesive and stop the duplication with Part 10 Ch 49. The current section 48.4 in Part 10 still references "35.4.1" — a legacy artifact confirming previous reshuffling left fingerprints — this restructure resolves that.

### Chapter 38 — Tools of the Trade: Evaluation Stack (renumbered from 36)

Source: 36.1–36.5 (eval-only subset)

1. **38.1** Eval Platforms: HELM, lm-evaluation-harness, Inspect AI, Braintrust, Phoenix
2. **38.2** Eval Libraries & Frameworks: Ragas, DeepEval, TruLens, promptfoo, G-Eval
3. **38.3** Eval Datasets & Benchmarks: MMLU, MMLU-Pro, GPQA, SWE-Bench, τ-bench, AgentBench, RULER
4. **38.4** Judge Models & Specialized Eval Models: Prometheus 2, JudgeLM, GPT-4 judge profiles
5. **38.5** External Reading & Communities

**Result**: Part 8 = 5 chapters (34–38), ~28–32 sections, evaluation-only.

---

## Section C — Proposed Part 10 Absorption of Chapter 35

### Recommendation: **HYBRID — promote chapter 35 into a new standalone Part 10 chapter for the "infrastructure-heavy" half, and distribute the rest into existing Part 10 chapters.**

The reason a pure renumber-and-drop-in does not work: Part 10's existing module-48 (Shipping & Deploying) already covers app architecture, multi-provider strategy, and post-launch monitoring. A 9-section module-35 dropped in beside it would create heavy overlap with 48.1–48.4 and 49.1–49.3. A pure absorb-into-existing also doesn't work: the K8s + edge + reliability material is a coherent unit that deserves its own chapter, not splinters.

### Distribution

| Old Section | New destination | Disposition |
|-------------|-----------------|-------------|
| 35.1 App Architecture & Deployment | Part 10 **Ch 48** (Shipping & Deploying) — new sections 48.5/48.6 | Merge: existing Ch 48 has shipping but lacks the FastAPI/LitServe/cloud detail |
| 35.2 Frontend & User Interfaces | Part 10 **Ch 48** new section 48.7 | Move intact |
| 35.3 Scaling, Perf & Guardrails | **Split 3 ways**: (a) latency/queues/backpressure -> P10 new Ch 49 "Production Engineering" §49.1; (b) Guardrails (NeMo, Llama Guard, ShieldGemma) -> **Part 9** Ch 38 (or new section in 37); (c) production memory patterns -> P10 Ch 48 (memory as feature) |
| 35.4 LLMOps & Continuous Improvement | **Split**: prompt versioning + model registry -> P10 new Ch 49 §49.2; A/B testing + online-eval + data flywheels -> **P8 Ch 37** (online evaluation) |
| 35.5 AI Gateways & Model Routing | P10 new Ch 49 §49.3 | Move intact |
| 35.6 Workflow Orchestration & Durable Execution | P10 new Ch 49 §49.4 | Move intact |
| 35.7 Edge & On-Device Deployment | P10 new Ch 49 §49.5 | Move intact |
| 35.8 Reliability Engineering | P10 new Ch 49 §49.6 | Move intact |
| 35.9 Kubernetes-Native LLM Ops | P10 new Ch 49 §49.7 | Move intact |
| 34.12 LLM Perf Benchmarking & Cross-HW | P10 **Ch 46** (Compute Planning) — new §46.3 | Move from old 34.12; serving perf belongs with compute planning |

### New Part 10 chapter to create: **Chapter 49 — Production Engineering for LLM Systems**

(Title is unambiguous and aligns with author's intent. Replaces existing "module-49-post-launch-monitoring" — see renumbering below for how the existing Ch 49 monitoring content folds in.)

**Sections**:

1. **49.1** Scaling, Latency & Queue Management *(from old 35.3 partial)*
2. **49.2** LLMOps: Prompt Versioning, Model Registry & Continuous Improvement *(from old 35.4 partial)*
3. **49.3** AI Gateways & Model Routing *(from old 35.5)*
4. **49.4** Workflow Orchestration & Durable Execution *(from old 35.6)*
5. **49.5** Edge & On-Device LLM Deployment *(from old 35.7)*
6. **49.6** Reliability Engineering *(from old 35.8)*
7. **49.7** Kubernetes-Native LLM Operations *(from old 35.9)*

### What happens to the *existing* P10 Ch 49 (Post-Launch Monitoring)

The existing module-49-post-launch-monitoring is small (3 sections, all of which overlap with the proposed P8 Ch 37 "Online Evaluation & Production Monitoring"). **Recommendation**: dissolve it. Its 3 sections (49.1 Post-Launch Monitoring, 49.2 Drift Detection, 49.3 Model-Rotation Strategy) all move to **P8 Ch 37** since they are *evaluation* of production traffic. This also resolves the long-standing duplication: section 48.4 ("Post-Launch Monitoring & Iteration") still has 35.4.1 anchors visible, and the standalone 49.x sections cover the same ground.

The freed "49" slot is reused for the new Production Engineering chapter.

---

## Section D — Renumbering Scheme

Author convention: chapter numbers are stable across the book and editions persist on the URL slug, so renumbering must touch directory names, file slugs, internal anchors, `book_structure.yaml`, `toc.html`, and every cross-link.

### Part 8 chapter numbering — before / after

| Before | After | Action |
|--------|-------|--------|
| Ch 34 LLM Evaluation & Quality Metrics (12 secs) | **Ch 34 Foundations of LLM Evaluation (6 secs)** | RENUMBER sections; new title |
| Ch 35 LLMOps & Deployment Engineering (9 secs) | **(GONE — moved to Part 10)** | REMOVE from Part 8 |
| Ch 36 Tools of the Trade: Eval & Production Stack (5 secs) | **Ch 38 Tools of the Trade: Evaluation Stack (5 secs)** | RENUMBER 36 -> 38; retitle |
| — | **Ch 35 Testing & Evaluation-Driven Quality Gates (6 secs)** | NEW chapter — populated from 34.3 + 34.5 |
| — | **Ch 36 Specialized Evaluation: RAG, Agents, Multimodal & Long-Context (6 secs)** | NEW chapter — populated from 34.9 + scouted content |
| — | **Ch 37 Online Evaluation, Observability & Production Monitoring (7 secs)** | NEW chapter — populated from 34.4, 34.6, 34.10, 35.4 partial, P10 49.1–49.3 |

### Part 9 chapter numbers — unchanged

Ch 37 Safety, Ethics & Regulation, Ch 38 Agent Safety & Security, Ch 39 Tools of the Trade.

**Conflict**: New Part 8 chapters 35, 36, 37, 38 collide with existing Part 9 Ch 37, 38, 39. **Resolution**: Part 9 renumbers up to 39, 40, 41 — OR — Part 8 uses new ranges 34, 34A, 34B (not author-friendly). **Recommendation**: renumber Part 9 chapters and shift Part 10 chapters up by 3.

### Full target numbering after restructure

| Part | Old Ch # | Old Title | New Ch # | New Title |
|------|---------|-----------|---------|-----------|
| 8 | 34 | LLM Evaluation & Quality Metrics | 34 | Foundations of LLM Evaluation |
| 8 | — | — | 35 | Testing & Evaluation-Driven Quality Gates |
| 8 | — | — | 36 | Specialized Evaluation: RAG, Agents, Multimodal, Long-Context |
| 8 | — | — | 37 | Online Evaluation, Observability & Production Monitoring |
| 8 | 36 | Tools of the Trade: Eval & Prod Stack | 38 | Tools of the Trade: Evaluation Stack |
| 9 | 37 | Safety, Ethics & Regulation | 39 | (unchanged title) |
| 9 | 38 | Agent Safety & Security | 40 | (unchanged title) |
| 9 | 39 | Tools of the Trade: Safety Stack | 41 | (unchanged title) |
| 10 | 40 | Ideation | 42 | (unchanged title) |
| 10 | 41 | Product Management | 43 | (unchanged title) |
| 10 | 42 | Strategy & Use Case Prioritization | 44 | (unchanged title) |
| 10 | 43 | Vibe-Coding | 45 | (unchanged title) |
| 10 | 44 | MVP | 46 | (unchanged title) |
| 10 | 45 | Prototype to Production | 47 | (unchanged title) |
| 10 | 46 | Compute Planning | 48 | Compute Planning & Inference Benchmarking *(absorbs old 34.12)* |
| 10 | 47 | Scaling Economics | 49 | (unchanged title) |
| 10 | 48 | Shipping & Deploying | 50 | Shipping & Deploying *(absorbs old 35.1, 35.2, parts of 35.3)* |
| 10 | 49 | Post-Launch Monitoring | — | **DISSOLVED — content moves to P8 Ch 37** |
| 10 | — | — | 51 | **Production Engineering for LLM Systems** *(NEW; from old 35.3–35.9)* |
| 10 | 50 | Tools of the Trade: Idea-to-Product | 52 | Tools of the Trade: Idea-to-Product & Production Stack *(absorbs old 36 production-tool entries)* |

Total chapters: Part 8 = 5 (was 3). Part 9 = 3 (numbers shift). Part 10 = 11 (was 11; net zero, but one dissolved + one added). Total book chapters before: 50. After: 52.

### Directory & slug renames

```
part-8-evaluation-production/
  module-34-evaluation-observability/            -> module-34-evaluation-foundations/
  module-35-production-engineering/              -> (DELETED; content distributed)
  module-36-tools-of-the-trade/                  -> module-38-tools-of-the-trade/
  + module-35-testing-quality-gates/             [NEW]
  + module-36-specialized-evaluation/            [NEW]
  + module-37-online-eval-observability/         [NEW]

part-9-safety-security-ethics/
  module-37-safety-ethics-regulation/            -> module-39-safety-ethics-regulation/
  module-38-agent-safety-security/               -> module-40-agent-safety-security/
  module-39-tools-of-the-trade/                  -> module-41-tools-of-the-trade/

part-10-idea-to-product/
  module-40-ideation/                            -> module-42-ideation/
  module-41-product-management/                  -> module-43-product-management/
  module-42-strategy-prioritization/             -> module-44-strategy-prioritization/
  module-43-vibe-coding/                         -> module-45-vibe-coding/
  module-44-mvp/                                 -> module-46-mvp/
  module-45-prototype-to-production/             -> module-47-prototype-to-production/
  module-46-compute-planning/                    -> module-48-compute-planning/
  module-47-scaling-economics/                   -> module-49-scaling-economics/
  module-48-shipping-deploying/                  -> module-50-shipping-deploying/
  module-49-post-launch-monitoring/              -> (DELETED; content -> P8 Ch37)
  + module-51-production-engineering/            [NEW]
  module-50-tools-of-the-trade/                  -> module-52-tools-of-the-trade/
```

### Section file renames

For each renumbered chapter, every `section-XX.Y.html` becomes `section-NN.Y.html`. Anchors of form `#34.5.2` become `#34.5.2` (numbering of *foundations* stays anchored at 34) but for split sections (e.g., old 34.3 -> new 35.1) anchors become `#35.1.1`. A redirect map JSON should be generated for legacy URLs.

---

## Section E — Migration Script Outline

The migration is large (≈40 file moves, hundreds of anchor rewrites, dozens of cross-link updates). Recommend a **multi-phase Python pipeline** rather than a single monolith. Each phase is idempotent and produces a verifiable artifact.

```
scripts/restructure_part8/
├── 00_validate_preconditions.py
│      • Confirms git tree is clean
│      • Snapshots book_structure.yaml, toc.html, every chapter index.html
│      • Builds a graph: section -> {incoming-links, outgoing-links, anchors}
│      • Writes baseline-state.json (used by 90_verify_outcome.py)
│
├── 10_build_migration_map.py
│      • Reads docs/part-8-restructure-plan.md (Section D table) — or hardcoded dict
│      • Produces migration-map.json with entries:
│           {old_path, new_path, old_anchor_prefix, new_anchor_prefix,
│            split_into?: [target_paths_with_h-range], action: move|split|delete|new}
│      • Validates: every source section accounted for, no duplicate destinations,
│        no anchor collisions, every new file has a defined source or 'new' flag
│
├── 20_move_and_rename_dirs.py
│      • Performs git mv on module directories (preserves history)
│      • Renames section-XX.Y.html within each moved module
│      • Skip-creates new directories for NEW chapters
│      • Does NOT yet touch file contents
│
├── 30_split_sections.py
│      • For each 'split' entry in the migration map:
│         - Parse source HTML
│         - Walk h2/h3 boundaries
│         - Extract subtree by heading range
│         - Write extracted subtree into target file using the section template
│      • For 34.3 -> {35.1, 35.2, 35.4, 35.5}: split by 34.3.1..34.3.6 anchors
│      • For 35.3 -> {49.1, 38.x guardrails, 50.x memory}: split by 35.3.1..35.3.4
│      • For 35.4 -> {49.2, 37.4, 37.5}: split by 35.4.1..35.4.4
│
├── 40_rewrite_section_anchors.py
│      • For each section, walk every h2/h3/h4 with id attr
│      • Apply prefix transform per migration map
│      • Build anchor-rename.json (old_full_anchor -> new_full_anchor) for use
│        in 50_rewrite_cross_links
│
├── 50_rewrite_cross_links.py
│      • Walks ALL HTML files in book (not just touched ones)
│      • For each <a href> matching old path or old anchor, rewrite
│      • Logs every rewrite to cross-link-rewrite-log.csv
│      • Issues a warning for any href that points to a deleted section without
│        a redirect target
│
├── 60_create_new_chapter_skeletons.py
│      • For new chapters 35, 36, 37 in Part 8 and 51 in Part 10:
│         - Create module-NN-slug/index.html using existing index.html as template
│         - Populate Section list from migration-map.json
│         - Stub sections that need NEW content (36.1 RAG eval, 36.2 Agentic, etc.)
│           with a one-paragraph placeholder + TODO comment
│
├── 70_regenerate_yaml_and_toc.py
│      • Rewrites book_structure.yaml from migration-map.json
│      • Regenerates toc.html from yaml using existing toc-build script (if any)
│      • Regenerates each part's index.html chapter-card list
│
├── 80_generate_redirect_map.py
│      • Writes downloads/legacy-url-redirects.json
│      • Maps every old URL to new URL for use by hosting redirect rules
│      • Includes anchor-level redirects for hash fragments
│
├── 90_verify_outcome.py
│      • Reloads baseline-state.json
│      • Confirms: zero dangling cross-links, every old section has a new home,
│        no duplicate IDs across the book, toc.html parses cleanly, every
│        chapter index has nav links to siblings, every section has prev/next
│      • Builds final-state.json and a diff report
│
└── README.md
       • Explains: run order is 00 -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> 70
         -> 80 -> 90. Stop on first failure. Resume by deleting later
         artifacts and re-running.
```

**Estimated runtime**: 30–60 seconds for the full pipeline (the bulk is anchor-rewrite traversal across ~600 HTML files).

**Manual-content phase (after script runs)**: the script creates **stub** sections for new content. These need human/agent authoring (use `book-skills`):

- 36.1 RAG eval (deep-dive Ragas)
- 36.2 Agentic evaluation (AgentBench/SWE-Bench/GAIA)
- 36.3 Simulation eval (τ-bench)
- 36.4 Code-gen eval
- 36.5 Multimodal eval
- 37.7 Eval-as-product (Braintrust/Latitude)
- 35.6 Structured-output validity testing

---

## Section F — Risks & Open Questions

### Content gaps to fill (in priority order)

1. **RAG evaluation depth (36.1)** — Current ch 34 has near-zero RAG-specific eval. 2026 frameworks ship 6–12 metrics per pipeline; the chapter needs Ragas faithfulness vs. groundedness disambiguation, BEIR-style retrieval metrics (MRR, hit@k), and end-to-end metrics (answer correctness, refusal calibration).
2. **Agentic eval (36.2)** — AgentBench, SWE-Bench Verified, GAIA, WebArena, OSWorld, τ-bench, ARC-AGI-2, MCP Atlas, Tool-Decathlon, Harbor, Exgentic. All 2024+ benchmarks, none in current text. This is the single biggest editorial debt.
3. **Eval-as-product platforms (37.7)** — Braintrust, Latitude, Laminar. The "eval-first" workflow is a distinct 2026 product category not currently surveyed.
4. **Simulation-based eval (36.3)** — τ-bench's database-state goal comparison is a methodological innovation worth its own section.
5. **Structured-output validity (35.6)** — JSON-Schema compliance, function-calling spec match, OpenAI/Anthropic tool-use eval. Adjacent to RAG eval, also missing.
6. **Multimodal eval (36.5)** — Currently zero coverage. Vision-language benchmarks, audio gen eval, video gen eval.

### Deferred decisions

- **Should guardrails (35.3 partial) go to Part 9 Safety or stay in P10 Production Engineering?** Argument for Part 9: Llama Guard / NeMo Guardrails / ShieldGemma are *safety* systems. Argument for P10: they're operational primitives. **Recommendation**: Move to Part 9 (renumbered Ch 39 or 40), cross-link from P10.
- **Should the new P10 chapter be "Production Engineering" (one chapter) or "LLM Infrastructure & Reliability" (split into two)?** With 7 sections it's defensible as one chapter, but a future scout pass for K8s+GPU content could justify a split.
- **What happens to old chapter 35's epigraph and chapter-opener illustration?** Recommendation: keep both with the new P10 Ch 51 to preserve continuity for readers who bookmarked.
- **Inter-Annotator Agreement section (proposed 34.6)** — How much depth? Cohen's kappa, Fleiss' kappa, Krippendorff's alpha all warrant treatment. The book has a `human-labeling` skill that captures this; a section should be a curated extraction.
- **Long-context (36.6)** — Stays in specialized eval, but the *context-extension methods* sub-content (RoPE/YaRN/PI) is really architecture, not eval. Consider relocating those subsections to a Part 4 transformer chapter and keeping only the *benchmarks* (NIAH, RULER, LongBench) in 36.6.

### Risk mitigation

- **Cross-link breakage**: phase 50 of the migration script must rewrite every link in the book, not just Part 8/10. Build a complete pre/post snapshot and assert zero dangling refs.
- **URL stability**: KDP / EPUB / web all reference URLs. Phase 80 generates a redirect map; the hosting layer must apply it.
- **Search index (pagefind)**: rebuild after restructure. Confirm pagefind-meta `chapter:` values still match new titles.
- **Capstone & appendices**: appendices may reference Part 8/10 sections. Phase 50 catches these automatically, but spot-check appendices A, G, K.
- **Visual identity**: chapter-opener images live in each module's `images/` dir. When we `git mv` modules, images move with them. New chapters need new chapter-opener.png (use `gemini-imagegen`).

### Validation checklist (post-migration)

- [ ] `python scripts/restructure_part8/90_verify_outcome.py` reports zero failures.
- [ ] `pagefind` rebuild produces same or larger index size (none lost).
- [ ] All exercises and labs in moved sections still execute.
- [ ] Bibliography refs in moved sections still resolve.
- [ ] `book_structure.yaml` validates against schema (if any).
- [ ] Pathway maps (`Learning Pathways`) in front-matter updated.
- [ ] CLAUDE.md and BOOK_CONFIG.md mention of "Part 8 = eval + prod" updated.

---

## Notes for the implementer

- **Mode**: This was a read-only planning pass. No file in the repo has been modified.
- **Line count**: ~310 lines (well under the 500-line cap).

### Critical Files for Implementation

- `E:/Projects/BookBlogsHome/LLMBook/book_structure.yaml`
- `E:/Projects/BookBlogsHome/LLMBook/toc.html`
- `E:/Projects/BookBlogsHome/LLMBook/part-8-evaluation-production/index.html`
- `E:/Projects/BookBlogsHome/LLMBook/part-10-idea-to-product/index.html`
- `E:/Projects/BookBlogsHome/LLMBook/part-8-evaluation-production/module-34-evaluation-observability/index.html`

**Sources** (web scouting for Section B/F new content):

- [A Survey on Evaluation of LLM-based Agents (2025)](https://arxiv.org/html/2503.16416v2)
- [Evaluation and Benchmarking of LLM Agents: A Survey (2025)](https://arxiv.org/html/2507.21504v1)
- [Top 7 Benchmarks That Matter for Agentic Reasoning (MarkTechPost, 2026)](https://www.marktechpost.com/2026/04/26/top-7-benchmarks-that-actually-matter-for-agentic-reasoning-in-large-language-models/)
- [LangSmith vs Arize vs Braintrust — Definitive 2026 Comparison](https://anudeepsri.medium.com/langsmith-vs-arize-vs-braintrust-e397e4728a76)
- [Top 6 Agent Observability Platforms 2026 (Laminar)](https://laminar.sh/article/2026-04-23-top-6-agent-observability-platforms)
- [Ragas — List of Available Metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- [RAGAS, TruLens, DeepEval: LLM Evaluation Frameworks 2026 (Atlan)](https://atlan.com/know/llm-evaluation-frameworks-compared/)
- [τ-bench: A Benchmark for Tool-Agent-User Interaction (arXiv 2406.12045)](https://arxiv.org/abs/2406.12045)
- [τ2-Bench: Evaluating Conversational Agents in Dual-Control (2025)](https://arxiv.org/pdf/2506.07982)
- [MM-tau-p2: Persona-Adaptive Multi-Modal Agent Evaluation](https://arxiv.org/html/2603.09643v3)
- [What is RAG Evaluation? Frameworks, Metrics, and Gates in 2026 (FutureAGI)](https://futureagi.com/blog/what-is-rag-evaluation-2026)
