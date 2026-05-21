# Five-Cycle Sweep Plan

**Starting state**: 1668 → 124 audit issues (92.6% reduction from project start; 96 sections still flagged for missing fun-notes/figures, the rest are small singletons).

Each cycle dispatches 6 parallel agents, each scoped to 20-40 targeted sections from detector findings. Total: ~30 agent invocations across the 5 cycles. Cost: ~$60-100.

## Cycle 1: Engagement + content scout

| Agent | Target | Goal |
|---|---|---|
| 20-content-update-scout (round 2) | Parts 1-5 fresh re-read | Catch 2025-2026 updates the first pass missed |
| 22-opening-hook-designer | Top 30 chapter intros that feel slow | Make first 100 words pull the reader in |
| 16-engagement-designer | Top 30 sections with high hedging density | Surface punchlines earlier |
| 27-memorability-designer | Key foundational concepts | Tighten one-line summaries |
| 14-narrative-continuity | Inter-chapter transitions across parts | Verify each chapter's What's-Next flows |
| 23-project-catalyst | Chapters that could benefit from project anchors | Identify multi-section project ideas |

## Cycle 2: Voice + clarity sweep

| Agent | Target | Goal |
|---|---|---|
| 15-style-voice (round 2) | Top 50 by hedging density | Match confident-and-sharp voice |
| 29-prose-clarity-editor (round 2) | Top 50 verbose | Tighten constructions |
| 30-readability-pacing-editor (round 2) | Long wall-of-text sections | Add white space + bridge sentences |
| 17-senior-editor | Random 30 across book | Catch what other agents missed |
| 06-example-analogy (round 2) | New abstract sections | Add concrete examples |
| 24-aha-moment-engineer (round 2) | Counter-intuitive results | Add the "click" example |

## Cycle 3: Visual + code + structural

| Agent | Target | Goal |
|---|---|---|
| 31-illustrator (round 2) | Remaining 86 sections without figures | Continue inline SVG additions |
| 25-visual-identity-director (round 2) | All new figures from Wave 27 | Consistent styling |
| 39-figure-fact-checker | Every figure | Verify caption claims match prose |
| 08-code-pedagogy (round 2) | Untouched code-heavy sections | Comments + variable naming |
| 40-code-caption-agent (round 2) | Remaining code blocks | Polish captions |
| 19-structural-architect (round 2) | Remaining giant catalogs | Tag or split |

## Cycle 4: Integrity + consistency

| Agent | Target | Goal |
|---|---|---|
| 11-fact-integrity (round 2) | Top 25 entity-dense sections | Verify another batch |
| 12-terminology-keeper (apply) | Top inconsistencies from Wave 36 report | Apply mass fixes (pretraining, Chain-of-Thought, Hugging Face) |
| 13-cross-reference (round 2) | 487 unlinked Section X.Y mentions | Add hyperlinks |
| 35-bibliography (round 2) | Remaining thin-bib chapters | Add canonical refs |
| 01-curriculum-alignment | Inter-part prerequisite chains | Verify book progression |
| 21-self-containment-verifier | Random 30 sections | Ensure standalone-readable |

## Cycle 5: Final QA + safety

| Agent | Target | Goal |
|---|---|---|
| 38-publication-qa (round 2) | Random 30 sections + recently-edited | Visual rendering pass |
| 28-skeptical-reader (round 2) | Non-frontier chapters | Hedge over-confident claims |
| 10-misconception-analyst (round 2) | Math/code dense chapters | Pre-empt confusions |
| 18-research-scientist | Theoretical chapters | Deep paper-knowledge pass |
| 04-student-advocate | Random 30 (different from Cycle 4) | Reader-perspective sanity |
| 03-teaching-flow | Sections with consecutive headings | Add bridge prose |

## Execution

Each cycle:
1. Dispatch 6 agents in parallel with non-overlapping section targets
2. Commit on completion (each agent's output independently committable)
3. Re-run audit + detectors to brief Cycle N+1
4. Move to next cycle

Reports/scripts generated:
- Each cycle produces a `CYCLE_N_REPORT.md` in `docs/content-audit/`
- Detector outputs feed into next cycle's targeting

Total session estimate: ~30 agent invocations × $1-3 each = $30-100.
