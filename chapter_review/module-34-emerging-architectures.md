# Module 34: Emerging Architectures & Scaling Frontiers

**Audit date**: 2026-05-11
**Sections reviewed**: 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9, 34.10 (10 sections)
**Total word count**: ~58,662 (930 index + 57,732 across 10 sections)

## Summary
Module 34 has the cleanest structure of the batch — 10 well-numbered sections, consistent breadcrumbs, no phantom cards. New diagrams added in Round 4 are wired in. The two real concerns are (a) scope overlap between 34.7 ("Mechanistic Interpretability at Scale") and Chapter 18's 18.2, neither of which acknowledges the other, and (b) stale cross-references to a now-deleted Chapter 35 ("AI and Society") in the chapter's "What's Next?" pointer.

## Inconsistencies
- **index.html line 172-173**: "What's Next?" says "In the next chapter, Chapter 35: AI and Society, we zoom out to consider AI's broader societal impact". Chapter 35 was merged/deleted in v3.2 — its content (compute governance, international regulation) ended up in `section-32.12.html` ("AI Governance and Open Problems"). The pointer leads readers to a chapter that does not exist.
- **Section 34.7 vs Chapter 18 Section 18.2**: both cover sparse autoencoders, superposition, polysemanticity, residual stream, scaling SAEs to frontier models. 34.7 prereq (line 44) only references 32.1 for AI safety context, but does not point to 18.2 for the foundational mechanics. Reciprocally, 18.2 does not link forward to 34.7 to disambiguate "research overview" vs "scaling at frontier".
- **index.html line 22**: epigraph cite is "Frontier, Humbly Curious AI Agent" but section files use other Frontier bios ("Illusion Dispelling AI Agent" in 34.1 line 26, "Road Mapping AI Agent" in 34.7 line 36). Same agent, three personalities.
- **index.html line 176**: prev nav points to `../../part-9-safety-strategy/module-33-strategy-product-roi/section-33.7.html` ("Economic Design of LLM Systems") — fine in principle but module-33 has the misnumbered 33.7 issue documented in the 33 audit; the prev link is at least to the correct file.
- Section 34.7 is technically standalone but reads as a near-rewrite of 18.2; the section-level epigraph and big-picture callout repeat the "interview the city one resident at a time" superposition framing already used in 18.2.
- **Section 34.4 (World Models)**: title and content describe Sora, Genie 2, Cosmos — these are 2024-2025 systems. Reasonable for a 2026 publication but should cite versions/release dates explicitly to age more gracefully.

## Gaps
- No section addresses the chapter prereq mention of "Chapter 09: Inference Optimization" in any cross-reference — the prereq list (index line 70) is decorative.
- Section 34.10 ("Beyond Text: Universal Sequence Machines") covers genomics, proteins, time series, robotics — but does not cross-reference Chapter 25 (Multimodal) or whatever covers vision-language models. The "universal sequence machine" framing should at least link back to multimodal foundations.
- The chapter overview promises "data walls, synthetic data strategies, test-time compute" (line 33-34) but synthetic data is the topic of Chapter 13; no link to Ch 13 from 34.2.
- No bibliography or "Further Reading" appears in the index (some sections have references but the chapter-level synthesis is missing).
- Chapter overview does not warn readers that 34.7 overlaps with Chapter 18; readers who already worked through 18.2 will feel like 34.7 is redundant.

## Errors
- **index.html line 172**: "Chapter 35: AI and Society" link/reference is dead — Ch 35 was removed.
- **Section 34.7 line 44 prereq cross-ref**: links to "AI safety material from Section 32.1" but does not link to the obviously relevant 18.2 (where the actual mechanistic-interp foundation is taught).
- **index.html line 21-22 epigraph**: "The only thing I know is that I know nothing." attributed to "Frontier" — the quotation is Socrates' (paraphrased from Plato's Apology). Even if intentionally attributed to the Frontier agent character, a footnote acknowledging the source would prevent confusion.
- **Section 34.4** — claims about Sora, Genie 2, Cosmos as "2024-2025 systems" need version specificity to avoid factual drift in a published 2026 edition.
- "Three axes of scaling (data, compute, inference)" framing in 34.2 description: the canonical Chinchilla framing is data + compute (parameters), with inference-time-compute as the recently-added third axis. Worth confirming the ordering matches what 6.3 / 6.7 said earlier in the book to stay consistent.

## Improvements
- Update "What's Next?" to point to Part 11 (Chapter 36) since Ch 35 no longer exists; add a sentence steering readers who want governance content to `section-32.12.html`.
- Add an explicit scope-divider sentence at the top of 34.7 along the lines of: "Section 18.2 introduced superposition, SAEs, and circuit analysis. This section focuses on what changes when these methods are applied at frontier scale (100B+ parameters)."
- Mirror that pointer in 18.2's "What Comes Next" so readers know 34.7 is the scale-up companion.
- Standardise the Frontier agent bio across the chapter (one tagline, one role).
- Add a synthesis bibliography or further-reading section at chapter level (sections have refs, chapter does not).
- Cross-reference 34.10 → multimodal chapter and 34.2 → Chapter 13 (synthetic data) so the chapter feels integrated with the rest of the book.
- For 2026 longevity, freeze model-version mentions in 34.4 with explicit dates ("Sora as of mid-2024", "Genie 2 announced Dec 2024") to make staleness self-documenting.

## One-thing-only fix
Replace the broken "What's Next: Chapter 35" pointer in `index.html` line 172-173 with a correct hand-off to Chapter 36 (Part 11), and add a single scope-divider sentence inside 34.7 distinguishing it from 18.2 so the duplication does not feel like an editorial mistake.
