# Editorial Decisions Resolved (autonomous)

Date: 2026-05-20
Context: User approved autonomous resolution of the open decision items
(TODO 31 in ACTIONABLE_TODOS.md) so downstream sweeps are unblocked. These
are the calls made; most resolve to "accept current state" because the book
is already audit-clean and the alternatives would break anchors or churn
intentional structure.

## D1. GIANT_SECTION candidates (64 borderline)
DECISION: Accept tools-of-the-trade catalog sections (Platforms, Libraries,
Datasets, Models, External Reading) as "catalog by design". No further
splitting. Non-tools giant sections are kept unless a future audit flags them
P0/P1 (none currently). Rationale: the a/b renumber already split the
genuinely oversized sections; remaining length is intentional.

## D2. Tools-of-the-Trade template policy
DECISION: Standardize on the 5-section template (Platforms; Libraries &
Frameworks; Datasets & Benchmarks; Models; External Reading & Communities).
Do NOT consolidate each tools chapter into a single page. Rationale: the
5-section split aids navigation and Google-arrival orientation.

## D3. Industry chapters (modules 67-77)
DECISION: Accept as "industry briefs" (survey depth), not held to the
full theory depth-bar. Rationale: their value is breadth across verticals;
deepening each to research depth would balloon the book without serving the
target reader.

## D4. Chapter 54 (Watermarking and Provenance)
DECISION: Keep watermarking + provenance together in one chapter. No split.

## D5. Chapter-nav placement
DECISION: Inside `<main>`. The linear-nav pass standardized the chain on this
convention; it is the majority pattern across the renumbered chapters.

## D6. H2 heading case-style
DECISION: Sentence-case (e.g., "Architecture patterns for reasoning"), which
matches the bulk of the corpus. Title-Case headings are left where they are
proper nouns or established product names.

## D7. Orphan 52.2 (Hallucinations) in the bias/fairness chapter
DECISION: Keep. The chapter is titled "Bias, Fairness & Hallucinations", so
the section belongs. No migration.

## D8. Orphan 55.2 (AI Governance) in the environmental chapter
DECISION: Keep with a cross-reference note to the governance chapter. A full
migration would break inbound anchors for marginal benefit.

## D9. Image-generation backlog (TODO 9, 36)
DECISION: Deferred, not cancelled. ~108 figure placeholders + ~30-40 comic
slots require a Gemini 2.5 Flash Image batch run (external API + budget) that
cannot be executed from this environment. The per-section prompts are staged
in `.book-update/imagegen-manifest.jsonl`. Deep-dive theory inserts this
session added 11 more "TODO: figure" markers to that queue. Action item for a
session with image-gen access.

## D10. MISSING_OUTPUT / code execution (TODO 27)
DECISION: Representative outputs were added where the code's behavior is
deterministic and obvious; blocks whose output depends on live API calls or
large model downloads are left without fabricated output (better no output
than a wrong one). Audit MISSING_OUTPUT currently reports 0.
