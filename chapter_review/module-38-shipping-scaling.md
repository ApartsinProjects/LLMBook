# Module 38: Shipping and Scaling AI Products

**Audit date**: 2026-05-11
**Sections reviewed**: 38.1, 38.2, 38.3, 38.4, 38.5 (5 sections)
**Total word count**: ~25,264 (753 index + 24,511 across 5 sections)

## Summary
The shortest chapter in the batch and the most structurally healthy. The capstone-lab framing (38.5) is consistent with Part 11's hypothesis-build-ship arc. The main issues are: (a) prereqs and overview still reference a now-deleted "Chapter 37: Building and Steering AI Products" which no longer exists, (b) Section 38.1 prereqs mention "observability (Chapter 30)" which is not a real chapter, and (c) Section 38.5 jumps from no h2 numbering directly to `38.5.7`, skipping intermediate headings.

## Inconsistencies
- **index.html line 34 (overview)**: "This chapter builds on the hypothesis work from Chapter 36 and the build methodology from Chapter 37." Chapter 37 was absorbed into Chapter 36 (36.5-36.9). The reference is stale.
- **index.html line 40 (Big Picture)**: "Building on the hypothesis work from Chapter 36 and the build methodology from Chapter 37" — same stale reference.
- **index.html line 58 (prereqs)**: lists "Chapter 37: Building and Steering AI Products (observe-steer loop, prototyping)" as a prerequisite. Chapter 37 does not exist.
- **index.html line 50 (learning outcomes)**: "Complete a capstone project that exercises hypothesis, build, and ship skills from Chapters 36 through 38" — implies a three-chapter span; should be "Chapters 36 and 38" or "across Part 11" now that 37 is gone.
- **index.html part-label** says "Part 11: From Idea to AI Product" (Arabic), inconsistent with "Part IX", "Part X" elsewhere in the book.
- **index.html line 27 epigraph cite**: "Compass, Production Hardened AI Agent" with `chinchilla.png` avatar. The Compass character image is normally `compass.png`; same avatar/identity mix-up as in Module 36.
- **Section 38.1 line 34 prereq**: "Familiarity with observability (Chapter 30)" — there is no Chapter 30 in the v3 book structure (Part 8 has Ch 29 and Ch 31). The observability content is inside Chapter 29.
- **Section 38.1 line 34 prereq pointer**: the in-text link for observability is `module-29-evaluation-observability/index.html` (same as evaluation), so the link is OK, but the printed label "Chapter 30" is wrong.
- **Section 38.5 line 20**: chapter-label "Chapter 38 · Section 38.5" — fine.
- **Section 38.5 h2 numbering jump**: file uses no `38.5.1`, `38.5.2`, ..., heads straight from the Lab phase headings (h3 "Phase 1-4") to `<h2>38.5.7 Assessment Rubric</h2>` (line 92). Either the lab phases should be numbered `38.5.1`-`38.5.6`, or the rubric should be `38.5.1`.
- **Section 38.5 line 28-29 epigraph attribution**: "Thirty-eight chapters of theory" — the book has 38 chapters numbered 0-38 plus 22 appendices A-V. "Thirty-eight" is technically correct (chapters 1-38) but might be more naturally phrased given the v3 reorganisation.
- **Section 38.3 line 7 title**: `Section 38.3: Lock-in, Portability, and Multi-Provider Strategy | Building Conversational AI` — has the book-suffix appended; other section titles (e.g. 38.1, 38.2, 38.4) omit it. Inconsistency in title format.

## Gaps
- The capstone lab (38.5) cross-references Code Fragments 38.5.1, 38.5.2, 38.5.3, 38.5.4 — verify all four are actually defined in the file (the audit didn't deeply inspect the code listings).
- Index "What's Next?" is correctly the book end ("This is the final chapter") but the Capstone Lab does not have a corresponding "What you have learned across Part 11" closer that ties back to the earlier role-canvas, prototype-loop, and IEB deliverables.
- No prereq link to Chapter 32 (safety, EU AI Act, OWASP LLM Top 10) even though Section 38.1's overview explicitly invokes EU AI Act + OWASP.
- Section 38.4 ("Post-Launch Monitoring") would benefit from a cross-ref to Module 18 (interpretability) for diagnostic monitoring beyond drift detection.
- Section 38.3 ("Lock-in, Portability") naturally pairs with 33.4 (Vendor Evaluation) but no explicit link.

## Errors
- **index.html line 34, line 40**: "Chapter 37" referenced multiple times — does not exist.
- **index.html line 58**: prereq "Chapter 37: Building and Steering AI Products" — does not exist.
- **Section 38.1 line 34**: "(Chapter 30)" label for observability — there is no Chapter 30 in the current ToC; should be Chapter 29.
- **Section 38.5 h2 hierarchy**: skipping from no numbered h2 to `38.5.7` is a numbering bug.
- **Section 38.3 line 7**: title has stray "| Building Conversational AI" suffix not present in sibling section titles.

## Improvements
- Rewrite chapter overview, Big Picture, and prereq list to reference Chapter 36 only (since the build content lives in 36.5-36.9), or explicitly note "Chapter 36 sections 5-9 cover the build methodology".
- Fix Section 38.1's "Chapter 30" mislabel — replace with "Chapter 29" (observability content lives there).
- Renumber Section 38.5 h2 headings so the Lab content is 38.5.1-38.5.6 and Assessment Rubric is 38.5.7, OR collapse to a flat structure with the rubric as 38.5.1. Either is better than the current gap.
- Standardise Section 38.3's `<title>` tag with sibling sections (drop the "| Building..." suffix or add it everywhere).
- Reconcile Compass avatar (`compass.png` vs `chinchilla.png`) across the chapter.
- Add explicit cross-references: 38.3 → 33.4 (vendor evaluation), 38.4 → Module 18 (interpretability for diagnostics), 38.1 → Chapter 32 (EU AI Act compliance, OWASP LLM Top 10).
- Resolve the "Part 11" vs "Part XI" Roman/Arabic ambiguity (book-wide).

## One-thing-only fix
Remove the three stale references to "Chapter 37" in `index.html` (overview line 34, Big Picture line 40, prereq line 58) and the "Chapter 30" mislabel in Section 38.1 line 34. These four short edits eliminate every dead chapter pointer in the chapter; everything else is cosmetic.
