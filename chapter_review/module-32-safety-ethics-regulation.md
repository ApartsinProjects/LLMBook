# Module 32: Safety, Ethics & Regulation

**Audit date**: 2026-05-11
**Sections reviewed**: 32.1, 32.2, 32.3, 32.4, 32.5, 32.6, 32.7, 32.8, 32.9, 32.10, 32.11, 32.12 (12 sections; index claims 13)
**Total word count**: ~91,366 (1,134 index + 12 sections totaling ~90,232)

## Summary
The chapter content is uniformly high-quality and current (covers 2024-2025 OWASP, EU AI Act, NIST AI RMF, DP-SGD, machine unlearning, etc.), but the v3.2/v3.4 slim/merge work left the index page and several section files structurally inconsistent: phantom sections, mislabeled file numbers, broken anchors, and a stranded "Chapter 35: AI and Society" section (32.12) whose breadcrumbs and h2 numbering still belong to the deleted Module 35.

## Inconsistencies
- **index.html lines 186-227**: lists 13 sections (32.1 through 32.13), but only 12 files exist (no `section-32.13.html`). Sections 32.10, 32.11, 32.12, and 32.13 in the index point to the WRONG files:
  - "32.10 Automated Red Teaming as Benchmarked Science" → `section-32.3.html` (which is Bias, Fairness & Ethics).
  - "32.11 Environmental Impact & Green AI" → `section-32.10.html` (which is correct content but wrong slug).
  - "32.12 Privacy Attacks & DP" → `section-32.11.html`.
  - "32.13 Federated Learning for LLMs" → `section-32.11.html` (duplicate with 32.12, and there is no separate file).
  Result: clicking three of the section cards lands on the wrong page or a duplicate.
- **section-32.11.html line 6-7**: `<title>Section 32.10: Privacy Attacks ...</title>` and meta description say "32.10" but the h1 is correct ("Privacy Attacks & Differential Privacy for LLMs") and the file is `section-32.11.html`. Title/meta lag the renumber.
- **section-32.12.html line 18**: chapter-label `<a href="../../part-10-frontiers/module-32-safety-ethics-regulation/index.html">Chapter 35: AI and Society</a>` — anchors to a non-existent path under Part 10, and labels the chapter as the deleted "Chapter 35".
- **section-32.12.html lines 41, 68**: h2 headings are numbered `35.2.1 Compute Governance`, `35.2.2 International Regulatory Landscape` — old Chapter-35 numbering survived the move into 32.12.
- **section-32.12.html line 25 epigraph**: "Multimodal models see, hear, and read. They still cannot fold laundry, but give them time." — has nothing to do with AI governance/open problems; it is a leftover epigraph from a multimodal chapter.
- **index.html line 17**: `Part IX: Safety & Strategy` (uses ampersand) but line 236 in the same file says `Part IX: Safety and Strategy`. Consistency wobble.
- **index.html line 161**: section-32.7 description says "Relates to alignment (Chapter 17)" — fine, but no other section description carries inline "Relates to" notes; format is inconsistent with the rest of the index.
- **index.html line 235**: prev nav points to `module-31-production-engineering/section-31.9.html` ("Kubernetes-Native LLM Operations") — needs to verify Section 31.9 still exists post-restructure.
- **section-32.11.html line 647**: contains `<section class="merged-section" data-merged-from="section-32.13">` confirming federated learning was merged in, but the index still advertises 32.13 as a standalone card.

## Gaps
- The "missing" section 32.13 (federated learning) is genuinely absorbed into 32.11 as a merged-section block, but readers who navigate from the index card will land on 32.11 with no anchor jumping to the FL portion. Add `id="federated-learning"` and link to `section-32.11.html#federated-learning`.
- Section 32.10 (Environmental Impact) is the file named `section-32.10.html`, but the chapter-overview prose (line 44-48) lists topics in a different order than the index card grid; environmental impact is mentioned mid-overview but the index puts it as item 11.
- Section 32.12 has no "Prerequisites" pointer to Chapter 18 (interpretability) even though "AI Governance and Open Problems" naturally chains from interpretability research.
- No section explicitly addresses Chapter 17 (alignment) as a prerequisite even though the index Learning Objectives and 32.3 prereqs both invoke RLHF; the chapter prereq list mentions Ch 17 but cross-references inside content are sparse.
- Chapter overview (index lines 34-49) says the chapter "covers... federated learning for privacy-preserving LLM training" but the actual federated-learning content lives as a sub-section of 32.11 and is hard to discover.

## Errors
- **section-32.11.html line 7**: `<title>Section 32.10: ...</title>` is wrong (should be 32.11). Affects browser tab titles and search indexing.
- **section-32.12.html line 18 anchor**: `../../part-10-frontiers/module-32-safety-ethics-regulation/index.html` is a 404 — the path mixes Part 10 with the Part 9 module slug.
- **section-32.12.html lines 41, 68**: h2 numbering "35.2.1", "35.2.2" — incorrect; should be "32.12.1", "32.12.2" (or whatever the chosen scheme is).
- **section-32.12.html line 381 (footer up-link)**: `<a class="up" ...>Chapter 35: AI, Society & Open Problems</a>` — wrong chapter name.
- **index.html lines 196-203**: card 32.10 description points to `section-32.3.html`. This is a content-routing bug, not just a label mismatch — clicking it sends the reader to Bias/Fairness instead of Red Teaming.
- The 32.10/32.11/32.12 numbering shuffle means several intra-chapter cross-references inside other sections may now point to the wrong topic. Sample: 32.7 references "section-32.4.html" (regulation) — verify still correct.
- Index prereq list (line 79-84) lists Chapter 31, 11, 29, 17. After the v3 restructure (Part 8 condensation), need to confirm Chapter 11 numbering is unchanged.

## Improvements
- Renumber the index sections to match the actual file inventory (12 sections) and fix all four mis-targeted hrefs in lines 186, 196, 207, 218.
- Either restore a real `section-32.13.html` with the federated-learning content, or remove the 32.13 card from the index and add an anchor jump on 32.11.
- Repair `section-32.12.html`: replace breadcrumb chapter-label with "Chapter 32", renumber h2s from `35.2.x` to `32.12.x`, swap the laundry epigraph for one that fits governance (or move 32.12 entirely into a different chapter — it reads as a wrap-up for Part 9, not a sibling of "Privacy Attacks").
- Fix the `<title>` and `<meta description>` of `section-32.11.html` to reference 32.11, not 32.10.
- Standardise "Part IX: Safety & Strategy" vs "Part IX: Safety and Strategy" across files (pick one).
- Add a top-of-32.11 anchored TOC so the merged 32.13 federated-learning content is discoverable.

## One-thing-only fix
Repair the index page's `sections-list` (lines 186-227) so all 12 cards point to the right files with correct numbers. The current state shows a 13th phantom card and routes three real cards to the wrong file — readers will hit the wrong content from the chapter landing page on at least three section clicks.
