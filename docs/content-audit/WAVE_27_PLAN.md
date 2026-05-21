# Wave 27+: Multi-Agent Book Enrichment Plan

**State at start:** 1668 → 261 audit issues (84.4% reduction). 26 commits on v2.0.

## Reframing: nothing is non-actionable

What I called "non-actionable" earlier was actually "deferred":

| Category | Was called | Actually |
|---|---|---|
| 223 P3 IMAGE_OPPORTUNITY | "needs illustration commissions" | Generate context-aware images via Gemini + technical-diagram-designer skills (wave 27) |
| 32 P2 GIANT_SECTION catalogs | "canonical for catalogs" | Could split for better navigation (wave 38) |
| 4 P1 GIANT_SECTION | "unsplittable" | Editorial decision; could be split with sub-section restructuring (wave 38) |
| 2 CALLOUT_ORDER section-1.4 | "needs editorial restructure" | Manual: pick canonical ending, merge/delete (wave 37) |

All 261 remaining issues are addressable. The plan below works through them.

## Agent inventory

42 specialist agents available in `agents/book-skills/agents/`. Each focuses on a single book-quality dimension. Running all 42 on all 577 sections would cost $10-50K. Targeted dispatch (each agent only on the sections where its specialty matters most) drops the cost to roughly $300-500 total.

Each wave below dispatches one or more agents at a specific section subset surfaced by the detectors built in earlier waves (dedup_detector, boilerplate_detector, concept_depth_detector, xref_graph, fun_note_prep, editing_leftover_detector, prereq_audit).

## Wave 27: Image generation (223 sections)

**Agent**: 31-illustrator + gemini-imagegen / technical-diagram-designer skills
**Target**: 223 sections flagged with "no figure or diagram"
**Cost**: ~$50-100 (Gemini 2.5 Flash Image is cheap, batches of 25)

Per-section approach (avoid the 93 boilerplate-figure failure of round 18):
- Read section title + big-picture intro + top 3 named entities (from dedup_detector)
- Decide: technical diagram (LayoutLM workflow, embedding space, training loop) vs comic/analogy (fun-note style, character + insight) vs reference chart (model comparison, benchmark table-as-figure)
- Generate prompt that's SPECIFIC ("LoRA fine-tuning architecture with rank-r adapter matrices A and B injected into a frozen W_0 weight matrix, gradients flowing only through A and B") — never just the section title
- Verify rendered output, reject if it has the boilerplate "three-panel overview" template

Batches of 25 per dispatch, run sequentially to avoid Gemini rate limits.

## Wave 28: Content-update scout (currency check)

**Agent**: 20-content-update-scout
**Target**: 1 pass per part (16 parts)
**Cost**: ~$30

Each scout read scans a part for:
- 2024 statements that need 2026 updates (model versions, costs, benchmark scores)
- Missing recent papers (post-2024)
- Deprecated tools or APIs still mentioned
- Cross-cutting findings flagged to a central report

## Wave 29: Deep explanation enrichment

**Agent**: 02-deep-explanation
**Target**: top 50 shallow-orphan concept intros from `CONCEPT_DEPTH_REPORT.md`
**Cost**: ~$60

For each flagged intro: either add depth (math, code, step-by-step) or add a concept-link to the canonical deep-dive section.

## Wave 30: Fact integrity

**Agent**: 11-fact-integrity
**Target**: chapters with the highest density of named entities (top 20 from dedup_detector hot list)
**Cost**: ~$40

Verifies: paper citations, model names + versions, dataset sizes, dates, benchmark scores. Flags hallucinated facts.

## Wave 31: Example + analogy + memorability

**Agents**: 06-example-analogy, 24-aha-moment-engineer
**Target**: top 30 abstract sections (high hedging density, low concrete-evidence from boilerplate_detector)
**Cost**: ~$60

Each agent adds one concrete worked example or one memorable analogy per section.

## Wave 32: Skeptical reader pass

**Agent**: 28-skeptical-reader
**Target**: frontier chapters (parts 16, modules 80-83) + claims-heavy ML chapters (modules 6, 7, 18)
**Cost**: ~$30

Pre-empts reader objections, finds weak claims, suggests caveats.

## Wave 33: Cross-reference verification

**Agent**: 13-cross-reference
**Target**: book-wide single pass
**Cost**: ~$20

Verifies: every `<a href="section-X.Y.html">` has correct target, every "see Chapter N" mention is current, every `concept-link` points to the canonical deep-dive.

## Wave 34: Prose clarity + style/voice + pacing

**Agents**: 29-prose-clarity-editor + 15-style-voice + 30-readability-pacing-editor
**Target**: top 50 sections by boilerplate_detector score
**Cost**: ~$60

Tightens awkward sentences, removes hedge accretion, matches the book's confident-and-sharp voice.

## Wave 35: Misconception + student advocate

**Agents**: 10-misconception-analyst + 04-student-advocate
**Target**: 30 sections most likely to confuse readers (concept-density × low example-density)
**Cost**: ~$40

Catches the common reader mistakes and adds protective framing.

## Wave 36: Terminology consistency

**Agent**: 12-terminology-keeper
**Target**: book-wide single pass
**Cost**: ~$25

Verifies entity spellings (Llama-3 not LLaMA-3 not LLAMA), method names, library casing consistency across the book.

## Wave 37: section-1.4 editorial restructure

**Manual** (Claude main session, not agent)
Section-1.4 has two endings. Pick the canonical one, merge/delete the other. Resolves 2 CALLOUT_ORDER issues.

## Wave 38: GIANT_SECTION decisions

**Agents**: 19-structural-architect (split planning) + general-purpose splits agent (execution)
**Target**: 4 P1 + 32 P2 GIANT_SECTION
**Cost**: ~$50

For each: structural-architect proposes split vs leave-as-catalog. Splits agent executes the proposed splits.

## Wave 39: Bibliography refresh

**Agents**: 35-bibliography + 18-research-scientist
**Target**: chapters with thin bibliographies or missing recent papers (per Wave 28 findings)
**Cost**: ~$40

Adds recent (2024-2026) seminal papers with annotations.

## Wave 40: Code pedagogy + caption polish

**Agents**: 08-code-pedagogy + 40-code-caption-agent
**Target**: every section with code (per dedup_detector code-ref counts)
**Cost**: ~$30

Verifies code is teachable, has captions, runs in the stated environment.

## Wave 41: Visual identity + figure fact-checker

**Agents**: 25-visual-identity-director + 39-figure-fact-checker
**Target**: all figures (existing + new from Wave 27)
**Cost**: ~$25

Verifies figures match prose claims, captions are accurate, visual style is consistent.

## Wave 42: Final publication QA

**Agent**: 38-publication-qa
**Target**: every section
**Cost**: ~$50

Final gatekeeper: visual rendering, link integrity, no orphan text, no formatting glitches.

## Wave summary

| Wave | Agents | Target | Cost |
|---|---|---|---:|
| 27 | illustrator + gemini-imagegen | 223 sections | $100 |
| 28 | content-update-scout | 16 parts | $30 |
| 29 | deep-explanation | top-50 shallow concepts | $60 |
| 30 | fact-integrity | top-20 entity-dense chapters | $40 |
| 31 | example + aha-moment | top-30 abstract | $60 |
| 32 | skeptical-reader | frontier chapters | $30 |
| 33 | cross-reference | book-wide | $20 |
| 34 | prose-clarity + style + pacing | top-50 verbose | $60 |
| 35 | misconception + student-advocate | top-30 confusing | $40 |
| 36 | terminology-keeper | book-wide | $25 |
| 37 | (manual) section-1.4 restructure | 1 file | $0 |
| 38 | structural-architect + splits | GIANT_SECTION × 36 | $50 |
| 39 | bibliography + research-scientist | thin-bib chapters | $40 |
| 40 | code-pedagogy + caption-agent | code-heavy sections | $30 |
| 41 | visual-identity + figure-checker | all figures | $25 |
| 42 | publication-qa | all sections | $50 |
| **Total** | **~40 distinct agent invocations** | **targeted** | **~$660** |

## Execution order

Wave 27 (images) starts NOW in parallel batches. Other waves dispatch sequentially as their detector outputs become available. Each wave commits independently.

Key principle: every agent gets a TARGETED scope from the detectors, never "run on everything." That's how we keep cost bounded while still applying expert-grade review to every chapter that benefits.
