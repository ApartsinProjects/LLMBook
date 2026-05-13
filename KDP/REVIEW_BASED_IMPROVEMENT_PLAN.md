# Review-Based Improvement Plan

**Source:** synthesis of 7 critical reviews (research scientist, senior editor, freshness scout, skeptical reader, curriculum designer, staff engineer, structural architect)
**Target state:** transform from "advanced practitioner handbook with intellectual ambition" → serious conceptual reference / graduate-course textbook
**Date:** 2026-05-13
**Continuation of:** Waves 1–13 (already shipped). This plan is Waves 14–24.

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Convergent Diagnosis](#convergent-diagnosis)
- [Master Defect Inventory](#master-defect-inventory)
- [Wave Roadmap (14 → 24)](#wave-roadmap)
  - [Wave 14: Publication-Blocking Defects](#wave-14--publication-blocking-defects)
  - [Wave 15: Code Integrity Restoration](#wave-15--code-integrity-restoration)
  - [Wave 16: Conceptual Spine + Front-Matter](#wave-16--conceptual-spine--front-matter)
  - [Wave 17: The Six Cross-Chapter Bridges](#wave-17--the-six-cross-chapter-bridges)
  - [Wave 18: Master Reference Tables](#wave-18--master-reference-tables)
  - [Wave 19: Conceptual Diagrams](#wave-19--conceptual-diagrams)
  - [Wave 20: Freshness Updates (2026 currency)](#wave-20--freshness-updates-2026-currency)
  - [Wave 21: Production Engineering Hardening](#wave-21--production-engineering-hardening)
  - [Wave 22: Pedagogical Quality Pass](#wave-22--pedagogical-quality-pass)
  - [Wave 23: Structural Reorganization](#wave-23--structural-reorganization)
  - [Wave 24: Final Consistency + Build + Push](#wave-24--final-consistency--build--push)
- [Effort Estimate Summary](#effort-estimate-summary)
- [Success Criteria (Adoption-Ready Checklist)](#success-criteria-adoption-ready-checklist)

---

## Executive Summary

All 7 reviewers agree on the headline diagnosis: **the book has the content but lacks the spine.** Specifically:

1. **Local intellectual moments are excellent** — Bradley-Terry/Arrow's-impossibility in 16.1, statistical-physics in 6.3, Popper conjecture-refutation in 11.3, residual-stream interpretation in 4 — but they're isolated and never compose into a recurring conceptual framework the reader carries from chapter to chapter.
2. **Chapter numbering metadata is broken** in Part VI (publication-blocking per the senior editor and curriculum designer).
3. **Canonical "from-scratch" code in production chapters is unparseable Python** because of the v6.44 progressive over-indentation bug recurring (CircuitBreaker, TokenBucket, PromptRegistry, ABExperiment, FastAPI streaming, SecureAgentExecutor — all broken).
4. **Master comparison tables are absent** where practitioners need them most (model selection, RAG architecture, PEFT method, agent framework, alignment method).
5. **Chapter-21 RLHF, ch-18 RAG, and ch-11 prompting** read as competent but generic — readers who've read Anthropic's blog post or Hugging Face's RAG tutorial gain little.
6. **Freshness gaps for 2026 ship date**: Qwen3, Claude 4, DeepSeek-R1 4-stage pipeline, prefill/decode disaggregation, AG-UI protocol, structured-generation decision matrix, Lost-in-the-Middle, GraphRAG, FlashAttention-3, multi-token prediction, induction heads.
7. **Production engineering is concept-deep but runbook-shallow** — no incident post-mortem template, no SLO worksheet, no on-call rotation guidance, no per-tenant isolation patterns.
8. **Pedagogy** is uneven — Ch 4 has analysis-grade exercises, Ch 16 has recitation-grade exercises; capstone has no grading rubric; no intermediate projects between 60-min labs and 6-week capstone.

The book is **adoption-blocked** for graduate courses today (numbering, broken code, recitation exercises, no rubrics) and **adoption-borderline** for professional reference (production code broken, ROI chapter without causal-attribution, alignment chapter understates reward hacking).

---

## Convergent Diagnosis

| Reviewer | Headline | Score / Verdict |
|---|---|---|
| Research scientist | Adequate for practitioners, too shallow for grad course | Score not given; "deficits are systematic, not scattered" |
| Senior editor | "Well-resourced blog series bolted together" | Overall 3/5; "needs major revision" |
| Freshness scout | "Mostly current; 4 areas need substantive additions" | No score; specific gap list |
| Skeptical reader | "Most detailed where readers need it least, most superficial where practitioners are stuck" | "Not recommended as primary grad text; conditionally yes for professional reference" |
| Curriculum designer | "Numbering disaster + recitation exercises + no rubrics" | No score; multiple structural defects flagged |
| Staff engineer | "Broken canonical code; concept-deep, runbook-shallow" | 6/10 (would move to 8/10 if code fixed) |
| Structural architect | "Missing intellectual spine; needs 5 unifying theses" | "Needs reorganization at conceptual level; adequate at content level" |

**All 7 converge on:** the book has good content, good code (where not broken), good prose, and genuine intellectual moments — but lacks **a unifying conceptual framework, master reference tables, and consistent reference-quality treatment of the topics most-searched by practitioners.**

---

## Master Defect Inventory

| # | Defect | Severity | Source | Wave |
|---|---|---|---|---|
| D1 | Chapter numbering metadata broken (Part VI: 20.x labeled 22.x in `data-pagefind-meta`; module-31 "Part 10" displays without name; etc.) | **Publication-blocking** | Editor, Curriculum | W14 |
| D2 | Duplicate section entries in Ch 20 index (20.4 + 20.6 each appear twice) | Critical | Editor | W14 |
| D3 | `REPLACE-WITH-ASIN` and `ISBN: TBA` placeholders visible in landing-page source | Critical | Editor | W14 |
| D4 | 6+ canonical "from-scratch" code blocks unparseable Python (CircuitBreaker, TokenBucket, PromptRegistry, ABExperiment, FastAPI streaming, SecureAgentExecutor) | Critical | Staff engineer | W15 |
| D5 | Recitation-grade exercises in Ch 16 (Q: "describe the three stages of the RLHF pipeline"; A: rote summary) | High | Curriculum | W22 |
| D6 | No capstone grading rubric, no alternative tracks (A/B/C) | High | Curriculum | W22 |
| D7 | No intermediate projects between 60-min labs and 6-week capstone | High | Curriculum | W22 |
| D8 | Reading pathways too coarse — "skip math-heavy parts" but no per-section guidance | Medium | Curriculum | W22 |
| D9 | No master comparison tables (model selection, RAG architecture, PEFT, agents, alignment) | High | Editor, Skeptic, Architect | W18 |
| D10 | Missing intellectual spine — recurring principles not named or threaded across chapters | High | Architect | W16 |
| D11 | Goodhart's Law / proxy-failure framing not unified across ch 16/27/29/31 | High | Architect, Skeptic | W17 |
| D12 | "Two compute axes × two knowledge types" framework not stated | High | Architect | W16 |
| D13 | Generator-verifier asymmetry never named (recurs in best-of-N, RLHF, RAG faithfulness, reflection) | Medium | Architect | W17 |
| D14 | Few-shot prompting (ch 11) never cross-referenced to induction-heads mechanism (ch 31) | Medium | Architect, Researcher | W17 |
| D15 | Knowledge Storage Spectrum (parametric vs RAG vs long-context vs agent memory) never unified | High | Architect, Researcher | W17 |
| D16 | Alignment-verification gap not stated — capability outpacing verifiability is field's core problem | Medium | Architect | W17 |
| D17 | Qwen3 absent (released Apr 2026) | High | Freshness | W20 |
| D18 | Claude 4 thin coverage relative to its market position | Medium | Freshness | W20 |
| D19 | DeepSeek-R1 4-stage pipeline not described as coherent recipe | High | Freshness, Researcher | W20 |
| D20 | Prefill/decode disaggregation only mentioned in passing (Mooncake, Splitwise absent) | Medium | Freshness | W20 |
| D21 | AG-UI protocol absent from main chapters (third leg of MCP/A2A/AG-UI stack) | Medium | Freshness | W20 |
| D22 | Long-context vs RAG decision framework scattered, never quantified | High | Freshness, Researcher | W17 |
| D23 | Structured-generation decision matrix missing (Instructor/Outlines/BAML/JSON-mode) | Medium | Freshness | W18 |
| D24 | Vibe-coding treated as tool survey, not workflow design pattern | Medium | Freshness | W22 |
| D25 | Agent evaluation methodology missing (non-determinism, trajectory scoring, cost-weighted accuracy) | High | Freshness, Researcher | W17 |
| D26 | Lost-in-the-Middle (Liu 2023) absent from RAG chapter | High | Researcher | W20 |
| D27 | FlashAttention-3 + H100 numbers absent (chapter cites FA-2 / A100 numbers as if current) | Medium | Researcher | W20 |
| D28 | Multi-token prediction (Gloeckle 2024) absent | Medium | Researcher | W20 |
| D29 | Mamba/SSM dedicated treatment in ch 32 not findable | Medium | Researcher | W20 |
| D30 | Reward overoptimization not quantified (Gao 2022 missing) | Medium | Researcher | W20 |
| D31 | DPO/GRPO 2024 shift not in ch 16 foundational sections | Medium | Researcher | W20 |
| D32 | Process Reward Models (Lightman 2023) not connected to o1/o3 training | Medium | Researcher, Architect | W17 |
| D33 | Benchmark contamination not addressed in ch 27 | High | Researcher | W17 |
| D34 | Calibration not addressed in ch 27 | Medium | Researcher | W17 |
| D35 | Reasoning-model evaluation methodology (compute-accuracy curves) not in ch 27 | Medium | Researcher | W17 |
| D36 | Constitutional AI vs RLHF philosophical distinction mentioned but undeveloped | Low | Architect | W17 |
| D37 | Induction heads (Olsson 2022) absent from prompt engineering chapter | High | Architect, Researcher | W17 |
| D38 | Mechanistic interpretability foundational paper (Elhage 2021) not cited | Medium | Researcher | W20 |
| D39 | Scaling Monosemanticity / sparse autoencoders (Templeton 2024) absent | Low | Researcher | W20 |
| D40 | Burns 2023 Weak-to-Strong Generalization absent (most relevant paper for alignment-verification gap) | Medium | Researcher, Architect | W20 |
| D41 | Production code broken from v6.44 over-indentation regression: re-gate AST parsing in CI | Critical | Staff engineer | W15 |
| D42 | Prompt registry implementation is a 30-line JSON dump, not a real production pattern | High | Staff engineer | W21 |
| D43 | Capacity planning math missing (no worked example: "Llama-3.1-70B AWQ on H100 → tokens/sec → GPUs needed") | High | Staff engineer | W21 |
| D44 | Cost control with hard kill switches missing (no per-tenant budget caps, dynamic max_tokens clamping) | High | Staff engineer | W21 |
| D45 | Secrets/key management (rotation, scoped tenant keys, BYOK, leak detection) absent | High | Staff engineer | W21 |
| D46 | Audit logging w/ replay (immutable, signed, retained, redact-then-hash for PII) absent | High | Staff engineer | W21 |
| D47 | Eval-in-CI gating not connected to A/B testing | High | Staff engineer | W21 |
| D48 | Online drift detection / canary judging absent | Medium | Staff engineer | W21 |
| D49 | Tool idempotency for agent chapters is one paragraph; needs full pattern | Medium | Staff engineer | W21 |
| D50 | Multi-tenant isolation (noisy neighbor, per-tenant rate limits, per-tenant prompt overrides) absent | High | Staff engineer | W21 |
| D51 | Streaming backpressure end-to-end (client disconnect, abort-mid-generation, budget refunds) absent | Medium | Staff engineer | W21 |
| D52 | Privacy/data-residency in implementation chapters absent (no-train headers, EU-region endpoints) | Medium | Staff engineer | W21 |
| D53 | DR / model registry rollback runbook absent | Medium | Staff engineer | W21 |
| D54 | Shadow traffic pattern absent | Medium | Staff engineer | W21 |
| D55 | Canary deploy for prompts pattern missing | Medium | Staff engineer | W21 |
| D56 | Sandbox-then-execute two-model architecture pattern missing | Medium | Staff engineer | W21 |
| D57 | Tool-call dry-run/preview pattern missing | Medium | Staff engineer | W21 |
| D58 | "Prompt → eval → deploy" Git-PR canonical workflow missing | Medium | Staff engineer | W21 |
| D59 | Observability cardinality discipline missing | Low | Staff engineer | W21 |
| D60 | Embedding-migration dual-write pattern missing | Medium | Staff engineer | W21 |
| D61 | Type-safe prompt rendering pattern (Pydantic + Jinja strict-undefined) missing | Medium | Staff engineer | W21 |
| D62 | Agent budget-as-context pattern missing | Low | Staff engineer | W21 |
| D63 | Per-request cost attribution (tenant_id + feature_flag + prompt_version trace tags) missing | Low | Staff engineer | W21 |
| D64 | Audience claim is muddied (3 audiences claimed, only ML-engineer-building-LLM-apps is actually served) | High | Editor | W23 |
| D65 | Part VIII over-segmented (Eval/Observability + Production Engineering overlap) | Medium | Editor, Curriculum | W23 |
| D66 | Interpretability stranded in Part X "Frontiers" instead of Part II "Understanding LLMs" | Medium | Editor, Curriculum, Architect | W23 |
| D67 | Reasoning models discussed in 3 chapters (7, 8, 20.3) without scoping signals | Low | Curriculum | W22 |
| D68 | Epigraphs on every section page, not every chapter — too dense | Low | Editor | W22 |
| D69 | Marketing landing-page aesthetic (animating stars, CSS keyframe glows, particle Easter-egg) too SaaS-product, not textbook | Low | Editor | W23 |
| D70 | Named production failure cases absent (Air Canada chatbot, Chevy dealership ChatGPT, Bing Sydney) | High | Curriculum | W22 |
| D71 | "Common Misconception: function calling" callout in ch 21 talks down to its target reader | Low | Skeptic | W22 |
| D72 | "Closed-book / open-book exam" RAG metaphor exhausted — exists in dozens of secondary sources | Medium | Skeptic | W22 |
| D73 | "Talent-show" RLHF metaphor charming but misleading on reward hacking | Medium | Skeptic | W22 |
| D74 | ROI section uses textbook formula without addressing causal attribution challenge | High | Skeptic | W22 |
| D75 | Four-Pillar Readiness Framework structurally identical to McKinsey/Gartner without citation | Medium | Skeptic | W22 |
| D76 | DSPy described optimistically without naming "needs labeled training set + working eval function" precondition | Medium | Skeptic | W17 |

---

## Wave Roadmap

### Wave 14 — Publication-Blocking Defects

**Priority:** CRITICAL. Must ship before any course adoption.
**Defects addressed:** D1, D2, D3
**Estimated effort:** 4–6 hours

#### Deliverables
1. Reconcile chapter-numbering metadata across the entire book.
   - Sweep every `<title>`, `<h1>`, `<div class="chapter-label">`, `data-pagefind-meta="chapter:..."`, `data-pagefind-meta="part:..."` so they all reflect the canonical numbering (Chapter 0–34 with the directory names as the source of truth).
   - Particular hotspots: `module-21-ai-agents/*` (currently 22.x in metadata), `module-23-multi-agent-systems/*` (currently 20.x in metadata), `module-25-agent-safety-production/*`, `module-27-llm-applications/*`, `module-10-interpretability/*` ("Part 10" with no name), `module-34-idea-to-product/*`, `module-35-shipping-scaling/*`.
2. De-duplicate Chapter 21 index entries — confirm 20.4 and 20.6 each appear exactly once with their canonical title.
3. Replace `REPLACE-WITH-ASIN` and `ISBN: TBA` placeholders in `index.html`. If the ASIN is not yet assigned, hide the buy-now button entirely (don't render it).
4. Build a **`KDP/build/_v660_audit_chapter_metadata.py`** detector that:
   - Reads canonical chapter→title→number mapping from `BOOK_CONFIG.md`
   - Scans every section file for the four metadata locations above
   - Reports any file where any of the four conflicts with the canonical map
   - Returns exit code 1 on any defect

#### Success criteria
- Detector returns 0 defects book-wide
- Pagefind search results show consistent chapter numbers
- Landing page has no placeholder strings

---

### Wave 15 — Code Integrity Restoration

**Priority:** CRITICAL. Production chapters' canonical code currently does not parse.
**Defects addressed:** D4, D41
**Estimated effort:** 6–10 hours

#### Deliverables
1. Re-run `python_structure_audit.csv` (already exists per staff-engineer review) and process every flagged code block.
2. Specifically fix the named flagship examples:
   - `section-11.3.html` Code Fragment 11.3.3 (`CircuitBreaker`)
   - `section-29.4.html` Code Fragments 28.4.1, 28.4.2, 28.4.3 (`PromptRegistry`, `ABExperiment`, `FeedbackCollector`)
   - `section-29.3.html` (`TokenBucket`, `BackpressureQueue`)
   - `section-29.1.html` FastAPI chat endpoint (lines 154–180)
   - `section-25.1.html` `SecureAgentExecutor` (lines 75–113)
3. Build a **`KDP/build/_v661_validate_python_blocks.py`** that:
   - Extracts every `<pre><code class="lang-python">` block
   - Strips Pygments span tags
   - Calls `ast.parse()` on each
   - Reports every parse error with file:line context
   - Returns exit code 1 on any failure
4. Wire into pre-build CI alongside the other detectors (`_v651`, `_v653`, `_v654`, `_v655`, `_v660`).

#### Success criteria
- AST validator returns 0 errors across all Python blocks
- All 6 flagship "from-scratch" examples parse and run

---

### Wave 16 — Conceptual Spine + Front-Matter

**Priority:** HIGH. The book's biggest single weakness.
**Defects addressed:** D10, D12
**Estimated effort:** 1–2 weeks

#### Deliverables
1. **New front-matter document: `front-matter/conceptual-map.html`** — 2-page (≈ 1500 words) "Conceptual Map of This Book."
   - Names the **3 recurring tensions** that drive the field:
     - Expressiveness vs. learnability (architecture chapters)
     - Flexibility vs. controllability (alignment + safety chapters)
     - Knowledge breadth vs. knowledge currency (RAG + memory + fine-tuning chapters)
   - Names the **5 unifying theses** the book threads through subsequent chapters:
     - Compression-Communication tradeoff (LLM as learned compression)
     - Proxy Problem (Goodhart's Law as the field's central challenge)
     - Two compute axes (train-time × test-time) × two knowledge types (parametric × non-parametric)
     - Alignment as the gap between objective and intent
     - Modularity Hypothesis (emergent modular structure in attention heads, MoE experts, fine-tuning, RAG, agents)
   - Indicates which chapters develop each thesis. Diagram: a 5-row × 35-column grid showing where each thesis appears.
2. Add **"Conceptual Map" landing-page link** so readers see it before Chapter 0.
3. **Recurring callout type: `<div class="callout thesis-thread">`** — used in subsequent chapters to surface the relevant thesis when a section is an instance of one of the 5. Define CSS in `styles/book.css`.
4. **Update `BOOK_CONFIG.md`** — make the 3 tensions + 5 theses the canonical conceptual scaffold; subsequent waves cite back to it.
5. Implement the **"Two Scaling Axes"** framework formally in `section-6.3.html` (currently scattered) and reference it from `section-8.1.html` opening big-picture callout.

#### Success criteria
- Front-matter conceptual map page exists and is linked from landing page + every Part index
- The 5-thesis × 35-chapter grid figure exists
- At least 5 chapters add `<div class="callout thesis-thread">` boxes referencing the new framework

---

### Wave 17 — The Six Cross-Chapter Bridges

**Priority:** HIGH. These are the missing conceptual bridges identified by the architect + researcher.
**Defects addressed:** D11, D13, D14, D15, D16, D22, D25, D32, D33, D34, D35, D36, D37, D76
**Estimated effort:** 2–3 weeks

#### Bridge 1: Knowledge Storage Spectrum (D15, D22)
- New section `18.0` (or open of Part V): "The Knowledge Storage Spectrum" — 2-D framework (access latency × knowledge currency) placing parametric weights, RAG, agent memory, long-context window in distinct quadrants.
- Add quantitative RAG-vs-long-context decision section: cite Liu et al. 2023 "Lost in the Middle" + Nelson 2024 cross-document multi-hop results.
- Cross-reference forward from ch 14, 18, 20.

#### Bridge 2: The Proxy Problem (Goodhart's Law) (D11, D33)
- New big-picture callout opening `section-28.1.html` explicitly framing **Goodhart's Law** as the governing challenge of LLM evaluation.
- New "Proxy-Failure Taxonomy" callout (4 quadrants: distributional shift, overfitting the proxy, proxy insensitivity, proxy unfaithfulness).
- Cross-reference from ch 16 (reward hacking), ch 18 (citation hallucination), ch 27 (benchmark saturation), ch 31 (attention-not-causation), ch 32 (metric mirage).
- Add benchmark-contamination subsection citing Golchin/Surdeanu 2023, Yang 2023, Oren 2024.

#### Bridge 3: Generator-Verifier Asymmetry (D13, D32)
- New callout in `section-8.1.html` naming the principle ("verification is almost always cheaper than generation; this is the NP/coNP-shaped insight that explains best-of-N, reward models, reflection loops, and PRMs").
- Cross-reference forward to: section 11.3 (reflection), section 16.1 (reward models), section 18.9 (RAG faithfulness checking).
- Add Process Reward Models (PRM) section in ch 16.1 citing Lightman et al. 2023; explicitly connect to chain-of-thought training in DeepSeek-R1.

#### Bridge 4: Induction Heads Mechanistic Bridge (D14, D37)
- New "Why Few-Shot Works" callout in `section-12.1.html` (≈ 200 words), citing Olsson et al. 2022 induction heads + Xie et al. 2022 Bayesian-ICL.
- Cross-reference forward to `section-10.1.html` mechanistic-interpretability treatment of induction heads.
- Backward reference from ch 31 to "this is the mechanism behind the few-shot prompting in section 11.1."

#### Bridge 5: Alignment Verification Gap (D16)
- New callout in `chapter 31` introduction: as model capability grows, the tasks needing verification become harder for human evaluators.
- Forward reference from `section-16.1` (alignment) and `section-29.x` (safety).
- Cite Burns et al. 2023 "Weak-to-Strong Generalization" + Bowman 2022 "Measuring Progress on Scalable Oversight."

#### Bridge 6: Agent Evaluation Methodology (D25)
- Expand `section-20.4` from benchmark survey into two parts: 20.4.1 benchmarks (existing) + 20.4.2 building custom agent eval harnesses (non-determinism, trajectory scoring, cost-weighted accuracy, separating tool-call correctness from final-answer correctness).
- Add reasoning-model evaluation subsection in ch 27 with compute-accuracy curve methodology + calibration discussion (Kadavath 2022, Xiong 2024).

#### Side-fixes folded in
- D36: Constitutional AI vs RLHF distinction — add 200-word formal comparison in ch 16 referencing Bai et al. 2022.
- D76: DSPy as "needs labeled training set + working eval function" — add precondition note in ch 11.3.

#### Success criteria
- All 6 bridges exist as named, cross-referenced concepts
- Each appears in ≥ 3 chapters with explicit cross-references
- New callout type `<div class="callout thesis-thread">` used to mark each bridge instance

---

### Wave 18 — Master Reference Tables

**Priority:** HIGH. The single biggest move the book can make to become reference-quality (per editor + skeptic + architect).
**Defects addressed:** D9, D23
**Estimated effort:** 1 week

#### Deliverables — implement at minimum 15 tables:

| # | Table | Placement | Source review |
|---|---|---|---|
| T1 | Four-Tier Intervention Hierarchy (Prompt / RAG / Fine-tune / Pretrain × cost, time, generalization risk, when to use) | Part III opener | Architect |
| T2 | Knowledge Storage Decision (parametric / RAG / long-context / agent memory × latency, currency, verifiability) | Ch 18 | Architect, Researcher |
| T3 | Alignment Method Selection (SFT / DPO / RLHF / CAI / RLVR × annotation cost, compute, robustness, failure modes) | Ch 16 conclusion | Architect |
| T4 | Test-Time Compute Strategy Selector (task difficulty tier × strategy × N × verifier type × cost multiplier) | Ch 8 | Architect, Researcher |
| T5 | Model Provider Comparison (GPT-4o, o3, Claude 4, Gemini 2.5, Llama 3.3/4, Qwen3, DeepSeek-V3/R1, Mistral, Phi × context, pricing tier, modalities, tool support, thinking-toggle) | Ch 7 | Editor, Freshness |
| T6 | RAG Architecture Comparison (Naive / Advanced / Modular / Self-RAG / GraphRAG / Long-context × latency, freshness, setup complexity, when to use) | Ch 18 | Editor, Freshness |
| T7 | PEFT Method Comparison (Full FT / LoRA / QLoRA / DoRA / Prefix tuning / Prompt tuning / Adapters × params, memory, inference overhead, task coverage, hardware tier) | Ch 15 | Editor |
| T8 | Agent Framework Comparison (LangGraph / CrewAI / AutoGen / LlamaIndex Workflows / smolagents × architecture style, tool support, multi-agent, maturity) | Ch 20 | Editor |
| T9 | Decoding Strategy Decision (Greedy / Beam / Top-k / Top-p / Temperature / Repetition / Constrained × deterministic, diversity, structured-task quality, cost) | Ch 5 | Architect |
| T10 | Structured Generation Decision Matrix (Instructor / Outlines / BAML / JSON-mode / Tool-call schemas × Pydantic-first, latency, tokenizer-aware, stream-friendly) | Ch 10 or 11 | Freshness |
| T11 | Proxy Failure by Domain (training objective / reward model / RAG faithfulness metric / benchmark / attention × what it proxies, how it fails, mitigation) | Ch 27 | Architect |
| T12 | Positional Encoding Comparison (Sinusoidal / Learned / T5-relative / ALiBi / RoPE / YaRN × extrapolation, GPU efficiency, models, length-gen quality) | Ch 4.3 | Architect |
| T13 | MoE vs Dense Tradeoffs (param count / active params / training stability / expert collapse / inference memory / routing overhead) | Ch 6 | Architect |
| T14 | Benchmark Saturation Timeline (GLUE → SuperGLUE → BIG-Bench → MMLU → MATH → GPQA → ARC-AGI × release year, saturation date, what it measured, successor) | Ch 27 | Architect |
| T15 | Eval Metric Failure Modes (Perplexity / BLEU / ROUGE / BERTScore / LLM-as-Judge / Human × what it measures, gaming risk, correlation with human pref, recommended use) | Ch 27 | Architect |

#### Success criteria
- ≥ 15 master tables exist book-wide
- Each is referenced from at least one chapter index page so readers can find it as a reference
- Each table has a 1-sentence "How to use this" prefix

---

### Wave 19 — Conceptual Diagrams

**Priority:** HIGH. Visual aids that do pedagogical work, not decorative cartoons.
**Defects addressed:** complements Waves 16 + 17 + 18
**Estimated effort:** 1–2 weeks

#### Deliverables — implement at minimum 15 conceptual figures:

| # | Figure | Placement | Source |
|---|---|---|---|
| F1 | Four-Tier Intervention Hierarchy (pyramid) | Part III opener | Architect |
| F2 | Knowledge Storage Spectrum (2-D quadrant) | Ch 18 | Architect |
| F3 | Two Scaling Axes (train-time × test-time, with iso-performance curves + labeled real models) | Ch 6.3 | Architect |
| F4 | Goodhart's Law in LLMs (4-quadrant proxy-failure taxonomy with concrete examples) | Ch 27 | Architect |
| F5 | Alignment Verification Gap (capability vs verifiability over time, widening gap) | Ch 31 | Architect |
| F6 | Generator-Verifier Asymmetry (spectrum from creative to formal tasks) | Ch 8.1 | Architect |
| F7 | Transformer-as-Residual-Stream (unrolled, "highway" with read/process/write at each layer) | Ch 4.1 + Ch 31 | Architect |
| F8 | MoE Routing as Learned Modularity (dense vs sparse + expert specialization heatmap) | Ch 6 | Architect |
| F9 | Agent Decision Tree: When to Use an Agent (Chain → Workflow → Agent → Multi-Agent) | Ch 20 | Architect |
| F10 | Scaling Law Resolution (Kaplan vs Chinchilla vs Inference-Optimal, with real models as labeled points) | Ch 6.3 | Architect, Researcher |
| F11 | The ICL Mechanism: Induction Heads (2-layer transformer copy-and-complete circuit) | Ch 11.1 + Ch 31 | Architect |
| F12 | Chunking-Retrieval-Context Tradeoff (triangle diagram) | Ch 18 | Architect |
| F13 | Alignment Method Decision Matrix (visual companion to Table T3) | Ch 16 | Architect |
| F14 | LLM Evaluation Taxonomy with Failure Mode (tree, with each leaf annotated with its failure mode) | Ch 27 | Architect |
| F15 | Capability-Interpretability Gap Over Time (dual time series, projected to 2028) | Ch 31 | Architect |

#### Success criteria
- ≥ 15 new conceptual diagrams exist
- All are Mermaid or hand-crafted SVG (not Gemini cartoons) for pedagogical precision
- Each is sized correctly (max 1600px wide, ≤ 500 KB JPEG-converted) so the EPUB stays under KDP 50 MB

---

### Wave 20 — Freshness Updates (2026 currency)

**Priority:** HIGH. The book ships in mid-2026; multiple gaps would be noticed immediately.
**Defects addressed:** D17, D18, D19, D20, D21, D26, D27, D28, D29, D30, D31, D38, D39, D40
**Estimated effort:** 1–2 weeks

#### Deliverables (per chapter)

**Ch 4 (Transformer Architecture)**
- Add FlashAttention-3 + H100 numbers (D27): cite Shah et al. 2024, update "2-4× speedup" claim with FA-3-on-H100 numbers (740 vs 330 TFLOPS).

**Ch 6 (Pretraining + Scaling)**
- Add Sardana & Frankle 2023 "Beyond Chinchilla-Optimal" inference-aware scaling (already partially cited; needs full subsection).
- Add Llama 3 / FineWeb / DCLM data-quality literature.
- Add multi-token prediction (Gloeckle 2024) (D28).
- Add Henighan et al. 2020 cross-modal scaling laws.

**Ch 7 (Modern LLM Landscape)**
- Add Qwen3 (D17) with hybrid thinking-toggle architecture.
- Expand Claude 4 family treatment (D18).
- Update DeepSeek-V3/R1 model-card detail.
- Refresh model roster to mid-2026 reality.

**Ch 8 (Reasoning + Test-Time Compute)**
- Add OpenAI o3 / o4-mini technical-report references where public.
- Connect DeepSeek-R1 PRM training (link to Bridge 3 in Wave 17).

**Ch 9 (Inference Optimization)**
- Add prefill/decode disaggregation (D20): Mooncake, Splitwise, with architecture diagram + capacity-planning heuristic.

**Ch 11 (Prompt Engineering)**
- Add Olsson 2022 induction heads (D37, also covered in Wave 17 Bridge 4).
- Add Xie 2022 Bayesian-ICL.
- Add Zhou 2022 APE / automated prompt optimization in 11.3.

**Ch 13 (Synthetic Data)**
- Add DeepSeek-R1 4-stage pipeline as a coherent recipe (D19): cold-start SFT → RLVR → rejection-sampling SFT → final DPO.
- Add Microsoft Persona Hub (1B AI personas).
- Add FineWeb-Edu curriculum filtering.

**Ch 16 (Alignment)**
- Add Gao et al. 2022 reward overoptimization (D30).
- Add 2024 PPO → DPO/GRPO shift discussion (D31).
- Add PRM / Lightman 2023 (covered in Wave 17 Bridge 3).
- Add Constitutional AI formal connection to RLHF.
- Add Burns 2023 Weak-to-Strong Generalization callout (D40).

**Ch 18 (RAG)**
- Add Liu 2023 Lost-in-the-Middle (D26, also Wave 17 Bridge 1).
- Add GraphRAG full coverage (Edge et al. 2024).
- Add Self-RAG (Asai 2023).
- Add Anthropic contextual retrieval.
- Add late chunking.

**Ch 21 (Tool Use / Protocols)**
- Add AG-UI protocol section (D21) as third leg of MCP/A2A/AG-UI stack.
- Brief Schick et al. 2023 Toolformer reference.

**Ch 27 (Evaluation)**
- Add Braintrust as a leading commercial eval platform.
- Add benchmark contamination treatment (Wave 17 Bridge 2).
- Add agent-specific evaluation methodology (Wave 17 Bridge 6).
- Add reasoning-model evaluation methodology (Wave 17 Bridge 6).

**Ch 31 (Interpretability)**
- Add Elhage et al. 2021 mathematical framework for transformer circuits (D38).
- Add Templeton et al. 2024 Scaling Monosemanticity (D39).
- Add Marks & Tegmark 2023 linear representations of truth.

**Ch 32 (Emerging Architectures)**
- Verify or add Mamba/SSM dedicated section (D29).

**Across all chapters touched**
- Use citation pattern: `<a href="https://arxiv.org/abs/...">Author et al. Year</a>` or full bibliography card.

#### Success criteria
- Every flagged paper / model / benchmark cited at correct location
- Bibliography for each touched chapter includes the new references
- No model-roster section names dated 2023-only models (GPT-3, Claude 2, Llama 1/2) without acknowledging they are historical

---

### Wave 21 — Production Engineering Hardening

**Priority:** HIGH. Must close to move "production chapters" score from 6/10 to 8/10.
**Defects addressed:** D42–D63
**Estimated effort:** 2–3 weeks

#### Deliverables — group by chapter

**Ch 18 RAG (D43 + new section):**
- Add section 18.1.9 "Production Ingestion Pipelines": Airflow / Dagster / Temporal-driven re-indexing, embedding-model upgrade migrations (dual-write pattern), DLQ handling for failed parses, version-pinning embedding models.

**Ch 24 Agent Safety:**
- Expand idempotency for agent tools (D49) to a full pattern subsection: Stripe/Salesforce-style idempotency keys, dedup windows, tool-result cache keyed on (tool, normalized args, conversation_id).
- Add canary deploy for prompts pattern (D55).
- Add sandbox-then-execute two-model architecture (D56).
- Add tool-call dry-run / preview pattern (D57).
- Add agent budget-as-context pattern (D62).

**Ch 27 Eval:**
- Add eval-in-CI gating (D47): GitHub Actions / CI pattern that blocks deploy if eval regression > threshold.
- Add online drift detection / canary judging (D48).
- Add observability cardinality discipline (D59).
- Add per-request cost attribution (tenant_id + feature_flag + prompt_version trace tags) (D63).

**Ch 28 Production Engineering:**
- Replace toy `PromptRegistry` with production prompt registry (D42): Git-backed source of truth, review/approval workflow, environment-scoped (dev/staging/prod) rollouts, signing, link to eval gates. Compare PromptLayer / Langfuse / Helicone.
- Add capacity planning math (D43): worked example "Llama-3.1-70B AWQ on H100, p50 ITL = 25 ms, mean output = 200 tokens, target p95 latency = 8 s, concurrency = ?, GPUs = ?".
- Add cost control with hard kill switches (D44): per-tenant token caps, dynamic max_tokens clamping, Redis INCR budget-token counter pattern, PagerDuty integration.
- Add secrets / key management section (D45): rotation, scoped per-tenant keys, BYOK, leak detection.
- Add audit logging w/ replay (D46): immutable, signed, retained for compliance, redact-then-hash pattern for PII.
- Add multi-tenant isolation (D50): noisy-neighbor on shared GPU/vLLM, per-tenant rate limits, per-tenant prompt overrides.
- Add streaming backpressure end-to-end (D51): half-open connections, abort-mid-generation cost refunds.
- Add privacy / data-residency (D52): no-train headers per provider, EU-region endpoints, embedding-store residency.
- Add DR / model registry rollback runbook (D53): snapshot of (model_version + prompt_version + eval_score + traffic_split) at each deploy, one-command rollback.
- Add shadow traffic pattern (D54): 5% candidate model, judge-score comparison.
- Add prompt → eval → deploy Git PR canonical workflow (D58).
- Add embedding migration dual-write pattern (D60).
- Add type-safe prompt rendering (Pydantic + Jinja strict-undefined) (D61).

#### Success criteria
- Every D42-D63 has a named section or callout in the right chapter
- Each pattern has at least one runnable code example (validated by `_v661_validate_python_blocks.py`)
- Each chapter (18, 24, 27, 28) ends with a "Production Checklist" callout enumerating the patterns covered
- Per chapter, an "Incident Post-Mortem Template" + "First-30-Days-Post-Launch Runbook" + "SLO Worksheet" appendix or sidebar

---

### Wave 22 — Pedagogical Quality Pass

**Priority:** HIGH for graduate-course adoption.
**Defects addressed:** D5, D6, D7, D8, D24, D67, D68, D70, D71, D72, D73, D74, D75
**Estimated effort:** 2 weeks

#### Deliverables

**Exercise quality (D5)**
- Rewrite recitation-grade exercises in Ch 16 (and audit Ch 13, 18, 27, 30 for the same pattern) into analysis exercises matching the standard set in Ch 4.
- Specific examples (per curriculum review):
  - Replace Ex 16.1.1 ("describe the three stages of RLHF") with: "You design RLHF for customer service. Annotators have inter-annotator κ = 0.22. Analyze: (a) Should you proceed at this κ? (b) How would you redesign the labeling task to raise it? (c) What does low κ imply for reward-model generalization?"
  - Replace Ex 16.2.2 about ref_model frozen-copy with: "TRL's `model_adapter_name` exists to avoid materializing a second copy of weights. Describe two engineering approaches that achieve this and explain what TRL is doing under the hood."
  - Add cross-chapter synthesis exercise: "After PPO, you apply DPO. Why should DPO's reference model be the PPO-aligned model rather than the SFT model? What happens to the KL penalty term if you get this wrong?"

**Capstone (D6)**
- Add `capstone/rubric.html` with explicit grading rubric (5 dimensions: system integration 25%, evaluation quality 25%, technical depth 20%, limitations & honest analysis 15%, communication 15%).
- Add 3 alternative tracks: A (full stack with GPU access), B (API-only, no fine-tuning), C (research replication of one paper, e.g., SWE-bench agent / SELF-RAG / DPO).

**Intermediate projects (D7)**
- Add `front-matter/syllabi/intermediate-projects.html` with 3 projects:
  - P1 (after Part I): "Build & benchmark a character-level vs BPE tokenizer on a domain corpus. Profile vocab size, fertility, rare-word coverage. 2-page memo."
  - P2 (after Part III): "Design a prompt engineering pipeline for a classification task. Run an ablation across 5 templates, measure accuracy & token cost, produce a decision table for which template to use under a 100ms latency budget."
  - P3 (after Part V): "Build a RAG pipeline over a real document corpus. Implement RAGAS eval with ≥ 3 metrics. Diagnose one failure mode and implement a fix. 3-page technical analysis."

**Reading pathways (D8)**
- Update `front-matter/pathways/index.html` with per-section guidance:
  - "Engineer building AI products" pathway: "If you have used LLM APIs before, skip to Ch 10 directly; return to Ch 3-5 only when you need to debug model behavior."
  - "Researcher / grad student" pathway: add a "fast-forward to modern systems" variant — Ch 4 (sections 4.1, 4.2 only), Ch 6 (sections 6.1, 6.3 only), Ch 7 (all), then training + alignment.
- Each pathway lists time estimates per chapter.

**Chapter-level "you should now be able to" review (new)**
- Add `<div class="callout chapter-review">` to each chapter index page with 3-5 synthesis questions spanning multiple sections of the chapter.

**Production failure case studies (D70)**
- Add a recurring `<div class="callout war-story">` callout pattern.
- Populate with at least 5 named real-world incidents:
  - Air Canada chatbot liability ruling (RAG / hallucination → safety)
  - Chevy dealership ChatGPT incident (prompt injection → safety)
  - Bing Sydney 2023 behavior (alignment failure)
  - Amazon Alexa Prize controversies (safety)
  - $12,000 fintech API bill story (already in Ch 10.1; promote to canonical war-story format)
- Each cites a public source.

**Vibe-coding workflow (D24)**
- Expand section 23.4 from tool survey to workflow design. Add subsection on:
  - How to structure repos for agent-readiness
  - How to write effective CLAUDE.md / cursor-rules / .windsurfrules
  - How to review agent-generated diffs safely
  - How to integrate background agents into CI/CD without leaking secrets
  - OpenAI Codex CLI (April 2025) added to the tool survey.

**Reasoning models scoping (D67)**
- Add scoping signals: Ch 7 should say "landscape overview, details in Ch 8"; Ch 8 should be canonical deep treatment; Section 21.3 should explicitly say "applying what you learned in Ch 8" and limit itself to agent-specific configuration concerns (thinking budgets, when to call o3 vs faster model).

**Talent-show / closed-book metaphor revisit (D72, D73)**
- Either retire or qualify the exhausted metaphors:
  - RAG closed-book/open-book exam → keep but add "this metaphor breaks down because..."
  - RLHF talent-show → add "the metaphor obscures the central problem: reward hacking. The model learns what the reward model rewards, which drifts systematically from human preference."
- "Common Misconception: function calling" callout (D71) → reframe so it doesn't talk down to the audience.

**ROI causal-attribution (D74)**
- Expand Ch 30.3 to address the actually-hard problem of causal attribution: A/B testing design with holdout-group contamination challenges; the proxy metric problem when users route around the AI system; named real techniques for measuring LLM impact (synthetic control groups, regression discontinuity, instrumental variables).

**Readiness framework citations (D75)**
- Cite McKinsey AI Maturity Model + Gartner AI Readiness Framework + Google MLOps Maturity Model. Acknowledge what the book's Four-Pillar framework adds beyond them.

**Epigraph density (D68)**
- Reduce per-section epigraphs to per-chapter only.

#### Success criteria
- Ex quality audit: every chapter has at least 1 analysis-grade and 1 synthesis-grade exercise (no chapter ships with only recitation exercises)
- Capstone has explicit rubric + 3 tracks
- 3 intermediate projects exist + are linked from front-matter syllabus pages
- Reading pathways include per-section guidance
- ≥ 5 named war stories with public sources
- Section 24.4 has workflow-design subsection
- Section 21.3 + Ch 7 + Ch 8 have explicit scoping signals
- Per-chapter epigraph density: 1 epigraph per chapter (the chapter opener), not per section

---

### Wave 23 — Structural Reorganization

**Priority:** MEDIUM-HIGH. Risky to do until Waves 14-22 are done; do this last among content waves.
**Defects addressed:** D64, D65, D66, D69
**Estimated effort:** 1–2 weeks

#### Deliverables

**Audience commitment (D64)**
- Update `BOOK_CONFIG.md` + `front-matter/index.html`: declare primary audience as **"ML engineers building LLM applications who already know Python and basic ML."** Researchers and product leads are secondary; pathways guide them but the prose is calibrated to the primary.
- Rewrite landing-page subtitle to remove "for researchers and students" if not actually served at that level.

**Move Interpretability (D66)**
- Per BOOK_CONFIG.md proposed v3 structure, move ch 31 from Part X (Frontiers) into Part II (Understanding LLMs) right after pretraining/scaling. This is what every other reviewer (architect, editor, curriculum, researcher) called for.
- Renumber ch 31 (e.g., new ch 8a or ch 9a depending on Part II final size).
- Update all cross-references.
- Use this opportunity to weave the "what did the model learn?" thread through the new Part II.

**Sharpen Part VIII titles (D65)**
- Rename the over-segmented chapters:
  - Ch 27 "Evaluation and Observability" → "LLM Evaluation and Quality Metrics"
  - Ch 28 "Production Engineering" → "LLMOps and Deployment Engineering"
  - Add (if absent) a focused "Production Monitoring and Alerting" chapter, OR consolidate observability into ch 27 and rename appropriately.

**Landing page tone (D69)**
- Decide explicitly: keep the SaaS-product aesthetic (animating stars, particle Easter-egg) and accept it positions the book as "consumer product first," OR strip down to a textbook-publisher landing page (book cover + buy + ToC + Part-card grid).
- Recommendation per editor + architect: simplify. The current aesthetic undermines textbook positioning.

#### Success criteria
- Audience claim is consistent across landing page, front-matter, syllabi, and pathways
- Interpretability chapter is in Part II with all cross-references updated
- Part VIII chapter titles distinguish their scope without overlap
- Landing page tone matches "serious textbook" positioning

---

### Wave 24 — Final Consistency + Build + Push

**Priority:** Required after Waves 14-23.
**Estimated effort:** 2-3 days

#### Deliverables

**Run all detectors (now ≥ 7)**
- `_v651_audit_broken_img_refs.py` (broken `<img src>`)
- `_v653_check_broken_math.py` (KaTeX heuristic)
- `_v654_validate_math.cjs` (KaTeX render truth)
- `_v655_find_adjacent_figures.py` (figure stacking)
- `_v657_fix_orphan_figure_prose.py` (orphan prose)
- `_v660_audit_chapter_metadata.py` (numbering metadata) [new in W14]
- `_v661_validate_python_blocks.py` (AST parse) [new in W15]

All must report 0 defects.

**Cross-reference consistency pass**
- Every chapter that mentions the "proxy problem" cross-references ch 27 explicitly
- Every chapter that mentions parametric vs non-parametric knowledge cross-references ch 18's Knowledge Storage Spectrum
- Every chapter that mentions test-time compute cross-references ch 6.3 + ch 8.1 using the "Two Scaling Axes" vocabulary
- "Generator-verifier asymmetry" referenced in ch 8, 11.3, 16, 18.9
- Every Bridge from Wave 17 has its callouts in at least 3 chapters

**Build verification**
- Run `_v650_audit_mermaid_only.py` (mermaid integrity)
- Run `KDP/build/build_epub.py --max-image-side 1200 --jpeg-quality 80`
- Verify EPUB ≤ 50 MB (ideally ≤ 49 MB to stay clear of the KDP threshold)
- Run `epubcheck` 5.2.1 against EPUB 3.3 — must report 0 fatals / 0 errors / 0 warnings / 0 infos
- Rebuild Pagefind search index

**Final push**
- Push to `origin/main`
- Verify GitHub Pages at llmbook.apartsin.com renders updated content
- Update `KDP/output/` artifacts (EPUB) so what's shipped matches what's validated

**Update README + landing page**
- Add a "What's New in This Edition" section listing the 5 unifying theses + structural changes from W23
- Update the version to "Sixth Edition, 2026" if the book identifies itself by edition

#### Success criteria
- All 7+ detectors report 0 defects
- EPUB ≤ 50 MB
- EPUBCheck 0/0/0/0
- Pagefind rebuilt and search returns consistent chapter numbers
- GitHub Pages updated and verified

---

## Effort Estimate Summary

| Wave | Title | Est. effort | Type |
|---|---|---|---|
| 14 | Publication-Blocking Defects | 4–6 hours | Critical bugs |
| 15 | Code Integrity Restoration | 6–10 hours | Critical bugs |
| 16 | Conceptual Spine + Front-Matter | 1–2 weeks | New content (highest leverage) |
| 17 | The Six Cross-Chapter Bridges | 2–3 weeks | New content (highest leverage) |
| 18 | Master Reference Tables | 1 week | New content |
| 19 | Conceptual Diagrams | 1–2 weeks | New visuals |
| 20 | Freshness Updates | 1–2 weeks | Citations + small additions |
| 21 | Production Engineering Hardening | 2–3 weeks | New content (large) |
| 22 | Pedagogical Quality Pass | 2 weeks | Exercise + project + war-story rewrites |
| 23 | Structural Reorganization | 1–2 weeks | Risky moves; do last among content |
| 24 | Final Consistency + Build + Push | 2–3 days | Verification |
| **Total** | | **~13–17 weeks** | |

**If 1 engineer, full-time:** ≈ 4 months end-to-end
**If 2 engineers in parallel** (Waves can be parallelized in pairs after W14+W15): ≈ 2.5 months
**Minimum viable milestone (Waves 14-15-16-17):** ≈ 4-5 weeks → unblocks course adoption + closes the "missing intellectual spine" critique

## Recommended Execution Order

Two paths depending on what matters most:

**Path A: "Adoption-first" (recommended if grad-course pickup matters)**
W14 → W15 → W22 → W23 → W16 → W17 → W18 → W19 → W20 → W21 → W24
Reasoning: fix the publication blockers + numbering + code + recitation exercises + audience claim FIRST so a course instructor can adopt the book in its current shape. Then deepen.

**Path B: "Reference-first" (recommended if professional-handbook positioning matters)**
W14 → W15 → W16 → W17 → W18 → W19 → W21 → W20 → W22 → W23 → W24
Reasoning: fix blockers, then add the unifying conceptual spine + master tables + diagrams + production patterns. This is what makes the book a 5-year-shelf-life reference vs a 1-year tutorial.

---

## Success Criteria (Adoption-Ready Checklist)

After Waves 14–24 the book should pass each item:

- [ ] **Numbering consistency**: chapter numbers in `<title>`, `<h1>`, chapter-label, `data-pagefind-meta` all match
- [ ] **Code integrity**: `_v661_validate_python_blocks.py` reports 0 errors across all `<pre><code class="lang-python">` blocks
- [ ] **No publication blockers**: `REPLACE-WITH-ASIN`, `ISBN: TBA`, duplicate index entries all gone
- [ ] **Conceptual map exists** as front-matter document, linked from landing + every Part index
- [ ] **5 unifying theses** appear as recurring `<div class="callout thesis-thread">` callouts in ≥ 5 chapters each
- [ ] **6 cross-chapter bridges** (Knowledge Storage Spectrum, Goodhart's Law, Generator-Verifier Asymmetry, Induction Heads, Alignment Verification Gap, Agent Eval Methodology) exist with explicit cross-references in ≥ 3 chapters each
- [ ] **≥ 15 master comparison tables** exist; each is referenced from at least 1 chapter index page
- [ ] **≥ 15 conceptual diagrams** exist (Mermaid or SVG, not Gemini cartoons)
- [ ] **Freshness**: Qwen3, Claude 4 expanded, DeepSeek-R1 4-stage pipeline, prefill/decode disagg, AG-UI, Lost-in-the-Middle, FlashAttention-3, multi-token prediction all cited with full bibliography entries
- [ ] **Production patterns**: each of D42–D63 has a named section or callout
- [ ] **Capstone has rubric + 3 tracks**
- [ ] **3 intermediate projects** linked from front-matter syllabi
- [ ] **≥ 5 named war stories** with public sources
- [ ] **EPUB ≤ 50 MB**, EPUBCheck 0/0/0/0, all 7 detectors return 0
- [ ] **Cross-reference consistency**: proxy/parametric/test-time-compute vocabulary used uniformly with cross-refs

---

*End of plan. Review at the start of each wave; update defect status; mark wave complete when all its success criteria are met.*
