# Human Editing Decisions

Items that require human judgment, not algorithmic resolution. After
many automated waves (the book went from 1668 audit issues to ~750),
what remains is mostly editorial: choices about voice, depth, lab vs.
no-lab, content trade-offs, and figure regeneration.

Most of these are NOT bugs. They are open authoring questions the
audit surfaced. The author should review and decide.

## 1. LAB_COVERAGE: which chapters genuinely need labs?

The audit currently flags 25 chapters as missing a hands-on lab.
Earlier tuning waved the exemption for tools-of-the-trade and
discussion-heavy chapters (ethics, regulation, frontier). The 25 that
remain split into three groups:

### Group A: Should have labs (engineering / build chapters)

These are practical chapters where a build-it lab is the natural fit.
A 30-90 minute hands-on lab should be added:

| Chapter | Suggested lab |
|---|---|
| Module 11 LLM APIs | Build a retry-with-jitter wrapper around OpenAI + Anthropic |
| Module 22 Vision-Language Models | Compare GPT-4o vs Claude Sonnet 4.7 on a 20-image VQA set |
| Module 33 Cross-Modal RAG | Build a multi-modal retriever over a small image+text corpus |
| Module 34 Structured IE / NER | Fine-tune a small extractor with instructor + GPT-4o-mini |
| Module 40 Voice / Realtime | Build a streaming voice agent with WebRTC + GPT-4o-Realtime |
| Module 43 Specialized Evaluation | Build a code-eval harness for HumanEval+ |
| Module 44 Online Eval / Observability | Wire Langfuse to a sample app and instrument a trace |
| Module 46 LLM-as-Judge | Run pairwise GPT-4 judge with position-swap on MT-Bench |
| Module 59 Distributed Training | Fine-tune a 1.5B model with FSDP on 2 GPUs |
| Module 60 Edge / On-Device | Run llama.cpp Q4_K_M on a laptop and measure tokens/sec |
| Module 62 Production Engineering Core | Build a request-router with timeout, retry, circuit-breaker |
| Module 63 AI Gateways | Stand up LiteLLM with cost limits and per-route routing |
| Module 64 Workflow Orchestration | Build a Temporal workflow that retries an agent step |
| Module 70 Shipping Products | Build a feature-flag-gated LLM rollout |

### Group B: Marginal — may want a lab but currently the chapter is fine without

These are application chapters (industry use cases) where a lab feels
forced. Decision: keep as discussion-only, or build an industry-domain
specific lab.

- Module 72 Legal LLMs
- Module 73 Finance LLMs
- Module 74 Healthcare LLMs
- Module 75 Education LLMs
- Module 76 Cybersecurity LLMs
- Module 77 Government LLMs
- Module 78 Manufacturing LLMs

If labs are added here, they should be industry-domain specific (e.g.
legal: "Annotate 50 contracts with GPT-4o + verify against attorney
gold standard"). Otherwise leave the FM.4-promise exemption.

### Group C: Already exempted or low-fit

- Module 6 Pretraining Scaling Laws — pre-existing exemption candidate
- Module 7 Modern LLM Landscape — survey chapter, lab feels forced

## 2. CALLOUT_ORDER: duplicate singletons needing manual reconciliation

33 files have TWO instances of a singleton callout type (two
key-takeaway, two self-check, two whats-next). An agent is in flight
to consolidate, but the decision of WHICH to keep depends on which
treatment is more substantive. The agent's heuristics:
  - More content (bullets, paragraphs) wins
  - Canonical position wins (key-takeaway between lab and self-check)
  - More descriptive title wins

Edge cases the author should review:
- When both versions cover different angles, the consolidation should
  MERGE bullet content, not drop one entirely.
- When one is in a sub-section context (e.g. lab-specific takeaway),
  the section-level takeaway should win.

## 3. GIANT_SECTION: which to split next

11 P1 + 32 P2 remain. Recent splits already handled the top 11.
Remaining P1 candidates (background split agent recommendation):

| Section | Lines | h2 | Recommendation |
|---|---:|---:|---|
| section-2.3 | 1054 | 9 | Split at "2.3.4 Multi-Head Attention" |
| section-7.1 | 673 | 13 | Split by vendor cluster (Anthropic/Google/Meta/Open-weight) |
| section-9.1 | 684 | 13 | Split at "Post-Training Quantization Algorithms" |
| section-9.4 | 861 | 14 | Split at "vLLM Deep Dive" |
| section-18.2 | 1024 | 8 | Split at "DPO Variants" (KTO/IPO/ORPO) |
| section-30.2 | 1005 | 7 | Split at "Multi-Agent Orchestration" |
| section-37.5 | 1146 | 9 | Split at "Persona Consistency" |
| section-19.3b | 1210 | 3 | UNSPLITTABLE along h2 (only 3 h2); requires sub-section restructuring |

P2 borderline candidates: most are catalog-style tools-of-the-trade
sections (61.3, 61.4, 61.5, 41.4, 41.5, 66.2) that legitimately have
many h2 entries with short bodies; the plugin tune already excluded
these from P1 but they still flag P2.

## 4. IMAGE_OPPORTUNITY: fun-note callouts to add

188 sections lack a fun-note callout. A fun-note is a short
comic/analogy/anecdote that adds personality. Wave 21D dispatches an
agent armed with `docs/content-audit/fun_note_context.json` (section
title, intro, subsection titles, top entities per section) so the agent
writes CONTEXT-AWARE fun-notes, not generic boilerplate.

Author decisions:
- Should every section have a fun-note? (Currently the audit suggests
  yes for non-reference sections.) Some technical sections may not
  benefit; the agent's judgment will surface candidates.
- Tone calibration: confident-and-sharp vs. self-deprecating
  vs. dry-academic. The Appendix-D rewrite set a "fun but confident"
  bar; agent should match.

## 5. MISSING_OUTPUT: code outputs to generate

63 code blocks flagged as missing output. An agent (Wave 21B) is
generating plausible outputs based on the surrounding prose and code
semantics. Author should verify:
- Numbers are in realistic ranges for the model/dataset described
- Tensor shapes match the inputs
- The agent didn't fabricate a result that contradicts the prose

## 6. SVG_TEXT_RIGHT_CLIP redesigns

19 SVG diagrams have text overflowing the right edge by >= 40px (too
much for the auto-viewBox-extend wave). An agent (Wave 21B) is
applying editorial fixes: reword, multi-line tspan, or font shrink.
Author should review each diagram for visual coherence.

## 7. Boilerplate-prose suspects (1351 candidates)

`scripts/boilerplate_detector.py` flags subsections with high list
density and low concrete-evidence. The top suspects:

| Section | Subsection | Issue |
|---|---|---|
| S41.4 | "Model evals vs product evals" | 158w, 62% list, 0.6 concrete/100w |
| S54.9 | "What to Log for an LLM System" | 176w, 89% list, 0.6 conc/100w |
| S6.7 | "Limitations of In-Context Learning" | 119w, 90% list, 0.8 conc/100w |
| S24.9 | "The Reference Pipeline" | 133w, 93% list, 0.8 conc/100w |
| S54.9 | "The Three Purposes of Logging" | 220w, 71% list, 0.5 conc/100w |
| S41.2 | "Memory architecture patterns in production" | 367w, 91% list, 0.5 conc/100w |
| S54.10 | "What Counts as an Explanation" | 189w, 68% list, 0.5 conc/100w |

These are "shopping lists without depth" candidates. The fix is
editorial: each bulleted item needs at least one supporting sentence
with a number, named system, or worked example. Wave 21D will dispatch
an agent to tackle the top 30.

## 8. v2.0 release decision

Audit count: 1668 -> ~750 = 55% reduction. Of the remaining 750:
- 409 are P3 informational (acceptable for v2.0 ship)
- ~340 are P0-P2 actionable
  - 63 MISSING_OUTPUT (Wave 21B agent in flight)
  - 33 CALLOUT_ORDER (Wave 21B agent in flight)
  - 43 GIANT_SECTION (most are catalog-style P2; 11 P1 candidates for next split)
  - 25 LAB_COVERAGE (Wave 21D agent will add 8-14 labs)
  - 19 SVG_TEXT_RIGHT_CLIP (Wave 21B agent in flight)
  - ~150 various smaller P1/P2

After the Wave 21B+21D agents land, expected to be ~400-500 issues, of
which most will be P3 informational. v2.0 ship-ready criterion (P0 = 0
and P1 < 30) should be met. No merge to main per directive.
