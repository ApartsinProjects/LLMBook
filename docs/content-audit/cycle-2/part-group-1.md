# Content Audit Cycle 2 — Parts 1-4

Scope: `part-1-llm-building-blocks/` (modules 00-05), `part-2-understanding-llms/` (modules 06-10), `part-3-working-with-llms/` (modules 11-14), `part-4-training-adaptation/` (modules 15-19). Read-only audit.

## Top remaining issues

1. **Body-text chapter references are still using the OLD numbering scheme across ALL four parts.** Wave 11-16 fixed part-index cards and most breadcrumbs but did NOT fix in-prose "Chapter X" / "Section X.Y" hyperlinks. Examples: section-1.3 refs "Chapter 22 / Chapter 23" (real 31/32), section-0.4 refs "Section 20.1" / "Chapter 20" (real 18.1/18), section-13.5 refs "Section 17.1" / "Section 13.1" / "Chapter 20 Alignment" (real 15.1/11.1/18), section-12.4 refs "Section 13.1" / "Section 37.3" (real 11.1/52.1), section-8.5 refs "Chapter 34" (real 42), section-5.1 refs "Chapter 50.2" (real 68.2), section-9.6 refs "Chapter 20" (real 18). This affects dozens of section files; not a typo-class issue, it is the dominant remaining drift.

2. **Figure / Table / Code-Fragment numbers wholesale wrong** (off by +1 in Part 1 modules 2/3/4 and Part 2 modules 7/8/9, off by +2 in Part 3 modules 11/12/13 and Part 4 modules 15/16/17/18). The numbering uses the OLD chapter index. Examples: module-02 has "Figure 3.X.Y" / "Table 3.X.Y" / "Code Fragment 3.X.Y" everywhere (should be 2.X.Y); module-17 has "Table 19.X.Y" (should be 17.X.Y); module-10 has "Figure 11.X.Y" (should be 10.X.Y). Section 2.1's `<figcaption>` even cites "Figure 3.1.2" while embedding `images/fig-3.1.7-rnn-unrolled.png` (caption-vs-filename also out of sync).

3. **H2 subheading visible text dual-numbering not resolved.** Anchor IDs match the section number (e.g. `id="14-1-1"`), but the rendered heading still reads the OLD prefix (e.g. `<h2 id="14-1-1">16.1.1 First-party model providers</h2>`). Affected: Part 1 modules 2/3/4, Part 2 module-10 sections 10.6-10.9, Part 3 module-14, Part 4 modules 15/16/17/18/19. Where chapter numbers were stable (modules 0/1/5/6/7/8/9/11/12/13) the h2 visible text is consistent.

4. **Tools-of-the-Trade chapter inflation NOT fully fixed.** Cycle 1 said this was not yet addressed; cycle 2 confirms the part-index cards have been demoted (5 sections each), BUT the section files themselves still embed many mid-content `chapter-nav` blocks pretending anchor-deep sub-sections are siblings: section-5.1 has 7 chapter-nav blocks (labels include "Section 5.9", "Section 5.12", "Section 5.16"), section-5.2 has 8, section-19.2 has 10 (labels "Section 19.6" through "Section 19.14"), section-19.3 has 5, section-10.6 has 5 (with "In Chapter Chapter 12" repeated). The inflated nav links also use `href="section-19.2.html#21-2-..."` (self-anchors with old-numbering anchors).

5. **Part 2 Tools chapter is still physically `module-10/section-10.5` through `10.9`** with breadcrumbs claiming `<a href="index.html">Chapter 12: Tools of the Trade: Models & Tokenizers</a>` while the page-current div says "Section 10.6". The part-2 index lists module-10 with only 4 sections (10.1-10.4); the tools sections are not discoverable from the chapter index and the linked breadcrumb target (the module-10 index) treats itself as "Chapter 10: Interpretability". Cycle 1 #3 is unresolved.

6. **Tokenization sections 1.5-1.7 still folded into module-01** with breadcrumbs claiming "Chapter 2: Tokenization and Subword Models" pointing back to the module-01 index, which only lists 1.1-1.4. The part-1 index does not list 1.5/1.6/1.7 anywhere. Cycle 1 #4 unresolved. Module-01's "Next Chapter" link in chapter-nav points to `../module-01-foundations-nlp-text-representation/index.html` (itself) with label "Chapter 02 Tokenization and Subword Models" — broken self-link.

7. **Part-index "Part Overview" prose still cites the OLD chapter numbers** in every part. Part I: "Chapters: 7 (Chapters 0 through 6) ... closes with Chapter 6: Tools of the Trade" while cards show 0-5. Part II: "Chapters: 6 (Chapters 7 through 12)" while cards show 6-10. Part III: "Chapters: 4 (Chapters 13 through 16)" while cards show 11-14. Part IV: "Chapters: 5 (Chapters 17 through 21)" while cards show 15-19.

8. **Module index `<title>` and `<meta description>` still zero-padded with OLD numbering** for Part 1 modules 0, 1, 2, 3, 4 and Part 2 modules 6, 7, 8. Examples: module-02 title "Chapter 03: Sequence Models & the Attention Mechanism" while breadcrumb is "Chapter 2". Module-03 title "Chapter 04: ..." while breadcrumb is "Chapter 3". Module-08 title "Chapter 08: Reasoning Models & Test-Time Compute" while breadcrumb is "Chapter 8". Inconsistent zero-padding: some titles say "Chapter 06" some say "Chapter 9".

9. **Module index `<nav class="chapter-nav">` prev/next labels still use OLD chapter numbers.** Module-08 says "Previous Chapter ... Chapter 08 Modern LLM Landscape" / "Next Chapter ... Chapter 10 Inference Optimization" — both should be 7 and 9. Module-09 says "Chapter 09" / "Chapter 11" (real 8/10). Module-12 says "Chapter 13" / "Chapter 15" (real 11/13). Pervasive across the chapter index files in Parts 1-4.

10. **Section 6.9 is duplicated inside the part-2 index chapter-6 card** (one `<li>` in the `section-list` ul, then another whole `<div class="section-grid">` card right after the ul). Also duplicated within module-06's own index (Sections list lists 6.9 once, then a separate `section-grid` div with the same card).

11. **Module-10 section-10.6 has 5 `chapter-nav` blocks and section-10.8 has 2** — indicates the content was concatenated multiple times (visible: 4 "In Chapter Chapter 12" footers per file).

12. **Module-17 (PEFT) section breadcrumbs still use OLD title** — "Chapter 17: Parameter-Efficient Fine-Tuning (PEFT)" — while the module index and part index now use "Chapter 17 Parameter-Efficient Fine-Tuning, Distillation & Model Merging". The Wave 16 rename was not propagated to section files.

13. **Concept-link `title="..."` attributes embed STALE chapter/section names** that the link's underlying target no longer matches: e.g. `title="Section 37.1: LLM Security Threats"` but the href points to section-47.1. These tooltips will display the wrong label to readers.

## Per-chapter findings

### Part 1

**Chapter 0 (module-00)**: title "Chapter 00" / breadcrumb "Chapter 0" zero-padding mismatch. Body refs: "Chapter 26" (agents, fine), "Chapter 04 Transformer" (real 3), "Chapter 20: Alignment, RLHF & DPO" (real 18), "Chapter 18 Fine-Tuning Fundamentals" (real 16). Figure 0.0.1 caption OK. Section 0.5 (RL Foundations) body has 3 references to "Section 20.1" / "Chapter 20" pointing at section-18.1/module-18 — stale visible text on otherwise-correct hrefs.

**Chapter 1 (module-01)**: title "Chapter 01" / breadcrumb "Chapter 1". Body refs: "Chapter 04 Transformer Architecture" (real 3). MAJOR BUG: chapter-nav "Next Chapter" points to module-01 (itself) with label "Chapter 02 Tokenization and Subword Models" — the link is broken and the next-chapter label is from the obsolete tokenization-as-Ch-2 plan. Sections 1.5/1.6/1.7 (tokenization) exist on disk but are not listed in the chapter index. Section 1.3 body cites "Chapter 22" (vector DB, real 31) and "Chapter 23" (RAG, real 32). Section 1.2 body cites "Chapter 23 RAG" (real 32). Section 1.6 prereq says "Section 2.1: Why Tokenization Matters" pointing at section-1.5 — stale visible label. Section 1.3 has a substitution-corruption-style fragment: "fine-tuning Section 7.1 on product descriptions" (a section reference appears in place of a noun).

**Chapter 2 (module-02)**: title "Chapter 03: Sequence Models" / breadcrumb "Chapter 2" — title off by +1. Section-2.1 figures captioned "Figure 3.1.X" (off by +1), tables "Table 3.X.Y", code fragments "Code Fragment 3.X.Y". H2 IDs use "2-1-X" but visible h2 text says "3.1.X". Caption "Figure 3.1.2" displays image `fig-3.1.7-rnn-unrolled.png` (mismatch). Body says "You now have tokens (Chapter 2)" while breadcrumb says THIS is Chapter 2 — self-reference.

**Chapter 3 (module-03)**: title "Chapter 04" / breadcrumb "Chapter 3". Figures captioned "Figure 4.X.Y" (off +1). Tables/code-fragments similarly off. Body says "Chapter 3 introduces attention" while THIS is Chapter 3 — self-reference. H2 visible text says "4.1.1" etc. while IDs say "3-1-1".

**Chapter 4 (module-04)**: title "Chapter 05" / breadcrumb "Chapter 4". Figures "Figure 5.X.Y" (off +1). Body says "You built a Transformer in Chapter 4" while THIS is Chapter 4 — self-reference. Same h2 dual-numbering pattern (id="4-1-1" / text "5.1.1"). Next-chapter nav says "Chapter 06 Tools of the Trade" (real Chapter 5).

**Chapter 5 (module-05, Tools of the Trade)**: title and breadcrumb both "Chapter 5" — consistent. Section 5.1 has 7 chapter-nav blocks with nav-num labels "Section 5.9", "Section 5.11", "Section 5.12", "Section 5.16" (and self-pointing anchor hrefs `section-5.1.html#6-1-...`). Section 5.2 has 8 similar inline nav blocks. "Code Fragment h.6.1" (literal "h") and "Table h.6.1" caption corruptions in section-5.1. Body cites "Chapter 50.2 (Vibe-Coding)" (real 68.2). Cross-ref to "Section 16.1 (Platforms)" labeling section-14.1 (real 14.1). Next-chapter nav says "Chapter 07 Pre-training" (real Chapter 6).

### Part 2

**Chapter 6 (module-06)**: title "Chapter 06" / breadcrumb "Chapter 6". Section-6.9 is duplicated in the chapter index (one in `sections-list` ul, then another `section-grid` div). Part-2 index also duplicates section-6.9. Body in section-6.9 references "Chapter 15: Hybrid ML and LLM Systems" (real 13) in its What's Next. Prereq lists "Chapter 18: Fine-Tuning" (real 16) and "Chapter 20" (real 18). Module-06 chapter-nav says Previous "Chapter 06 Tools" (real Chapter 5) / Next "Chapter 08 Modern LLM Landscape" (real 7). H2 numbering in sections looks consistent (6.X.Y).

**Chapter 7 (module-07)**: title "Chapter 07" / breadcrumb "Chapter 7". Figures "Figure 8.X.Y" (off +1). Section 7.4 body: "Chapter 18" (real 16, fine-tuning) appears multiple times. Section 7.3 body: "Chapter 15" (real 13, hybrid). H2 visible text "8.1.1" while IDs use "7-1-1".

**Chapter 8 (module-08)**: title "Chapter 08" / breadcrumb "Chapter 8". Figures "Figure 9.X.Y". Prereq labels in chapter index: "Chapter 04" (real 3), "Chapter 05" (real 4), "Chapter 06" (real 6 OK), "Chapter 08" Modern LLM (real 7). What's Next says "Chapter 10 Inference Optimization" (real 9). Chapter-nav nav-num "Chapter 08" / "Chapter 10". Section 8.1 body: "Reward models in RLHF (Chapter 20.1)" (real 18.1). Section 8.5 body: "Chapter 34" eval (real 42).

**Chapter 9 (module-09)**: title "Chapter 9" / breadcrumb "Chapter 9" — consistent. Figures "Figure 10.X.Y" (off +1). Body in section 9.8 refs "Chapter 20" alignment (real 18). What's Next refs "Chapter 11 Interpretability" (real 10). Chapter-nav nav-num "Chapter 09" / "Chapter 11".

**Chapter 10 (module-10, Interpretability + Tools)**: title and breadcrumb both "Chapter 10". Chapter opener figure captioned "Figure 11.0.1" (off +1). All figures throughout module-10 captioned "Figure 11.X.Y". Body refs in section 10.1 "Chapter 20 alignment", "Chapter 34 evaluation", "Chapter 37 safety" (real 18/42/47). Section-10.5 through 10.9 are the misplaced Tools-of-the-Trade chapter with `<title>Section 10.6: Platforms</title>` but breadcrumb `<a href="index.html">Chapter 12: Tools of the Trade: Models & Tokenizers</a>` — completely inconsistent: 10.X file, "Section 10.X" page-current, "Chapter 12" breadcrumb linking to "Chapter 10" index. H2 IDs use "10-5-1", visible text "12.1.1". Body in section-10.5 says "the runtime layer is Section 16.2's job in Part III" — Section 16.2 doesn't exist in Part III (real reference probably 14.2). Section-10.6 has 5 chapter-nav blocks ("In Chapter Chapter 12" repeated 4 times). Section-10.8 has 2 chapter-nav blocks. Chapter index prereq "Chapter 04" (real 3), "Chapter 07" (real 7 OK), "Chapter 05 Embeddings" (real 5 is Tools, not embeddings). Chapter index Previous "Chapter 10 Inference Optimization" (real 9 OK, but "Chapter 10" label wrong).

### Part 3

**Chapter 11 (module-11)**: title and breadcrumb both "Chapter 11" — consistent. Section h2 numbering also consistent (11.X.Y both id and text). BUT section 11.2 has h2 IDs that JUMP: 11.2.1, 11.2.2, 11.2.4 (missing 11.2.3). Body references: section-11.2 "Chapter 35's LLMOps coverage (Pattern P4)" — Chapter 35 doesn't exist with that content (real Part 13 LLMOps). Section-11.1 body cites "Section 27.1" correctly. Figures captioned "Figure 13.1.X" (off +2). Tables "Table 13.X.Y". Chapter index body: link to "production information extraction" in Part 7 module-34 (OK href, but old "Chapter 15.5" pattern still in section 11.2 body).

**Chapter 12 (module-12)**: title and breadcrumb both "Chapter 12" — consistent. Figure 14.0.1 in chapter opener (off +2). Body: "RAG systems (Chapter 23), agents (Chapter 26), and evaluation (Chapter 34)" — Chapter 23 should be 32, 34 should be 42 (26 OK). Prereq "Chapter 05 Decoding" (real 4), "Chapter 13 APIs" (real 11). What's Next "Chapter 15 Hybrid ML" (real 13). Chapter-nav nav-num "Chapter 13" / "Chapter 15" (real 11/13). Section 12.4 body: "Section 13.1" API (real 11.1), "Section 37.3" security (real 52.1). Section 12.3 body: "Section 34.5" eval (real 42.9), "Section 23.5 on AutoRAG" (real 32.3). Concept-link title="Section 37.1: LLM Security Threats" while target is section-47.1.

**Chapter 13 (module-13)**: title and breadcrumb both "Chapter 13" — consistent. Figures "Figure 15.X.Y" (off +2). Body in section 13.5: "Section 17.1 Principles of Synthetic Data" (real 15.1), "Section 13.1 API Landscape" (real 11.1), "Chapter 20: Alignment" (real 18), "Chapter 17 Synthetic Data" (real 15). Chapter index body: "Chapter 23 on RAG" (real 32). Section 13.1.X h2 numbering has a gap (13.1.1, 13.1.2, then jumps to 13.1.5).

**Chapter 14 (module-14, Tools of the Trade)**: title and breadcrumb both "Chapter 14". H2 visible text "16.X.Y" (off +2) while IDs "14-X-Y". Section 14.1 chapter-nav next-link nav-num says "Section 17.1" (real 15.1) for the Part-4 hand-off. Section 14.2 has 3 chapter-nav blocks (anchor-deep "Section X" labels). Section 14.3 body: "still used for Chapter 18 examples" (real 18 OK? actually 16-fine-tuning or 17-peft). Section 14.4 body: "Section 16.5" (doesn't exist; real 14.5) and "Chapter 50's full Idea-to-Product Tools of the Trade chapter" (real 68 / 19 depending on which is meant).

### Part 4

**Chapter 15 (module-15)**: title and breadcrumb both "Chapter 15" — consistent. Figures "Figure 17.X.Y" (off +2). H2 visible "17.X.Y", IDs "15-X-Y". Sections look clean otherwise.

**Chapter 16 (module-16)**: title and breadcrumb both "Chapter 16". Figures "Figure 18.X.Y" (off +2). H2 visible "18.X.Y", IDs "16-X-Y". Body otherwise looks clean.

**Chapter 17 (module-17)**: title and breadcrumb at the chapter index say "Chapter 17: Parameter-Efficient Fine-Tuning, Distillation & Model Merging" (Wave 16 rename). All seven section breadcrumbs (section-17.1 through 17.7) still link to `index.html` with the OLD label `Chapter 17: Parameter-Efficient Fine-Tuning (PEFT)` — Wave 16 stopped at the index. Figures "Figure 19.X.Y" (off +2). Tables "Table 19.X.Y". Section 17.8 What's Next says "Chapter 20: Alignment: RLHF, DPO & Preference Tuning" (real 18).

**Chapter 18 (module-18)**: title and breadcrumb both "Chapter 18". Figures "Figure 20.X.Y" (off +2). H2 visible "20.X.Y", IDs "18-X-Y". Section 18.7 body: "Section 37.12 AI Governance" → target points to module-55 in Part 11 (real Section 55.2 or similar), "Chapter 37" → target points to module-47 (real Chapter 47).

**Chapter 19 (module-19, Tools of the Trade)**: title and breadcrumb both "Chapter 19". H2 visible "21.X.Y" (off +2), IDs "19-X-Y". MAJOR INFLATION: section 19.2 has 10 chapter-nav blocks (nav-num labels "Section 19.6" through "Section 19.14" pretending to be siblings); section 19.3 has 5. Self-pointing hrefs like `section-19.2.html#21-2-...` with old-numbering anchors. Section 19.5 body: "Chapter 34" eval (real 42), "Chapter 23" RAG (real 32). Section 19.6 looks clean.

### Resolved categories (verified during this audit)

- Cross-part section cards (Cycle 1 #5): RESOLVED. No `section-card` elements jump across parts in Parts 1-4.
- Substitution corruptions ("softmax library", "for softmax"): RESOLVED. The only "for softmax" matches in Parts 1-4 are now legitimate prose (e.g. "Reasons for softmax: ...").
- Placeholder "A comprehensive chapter from the Building Conversational AI textbook": NOT FOUND in Parts 1-4 (resolved).
- Part-index chapter cards rebuilt from filesystem: MOSTLY resolved, except (a) Part-2 chapter-6 card has a duplicate section-6.9 entry; (b) Part-2 index does NOT list sections 10.6-10.9 even though they exist physically; (c) Part-1 index does NOT list sections 1.5-1.7 (tokenization).
- Appendix B/C self-references and 42.10/42.11 self-titling: out of scope for this group, not encountered.

## Suggested cycle 3 actions

1. **Body-text reference renumbering pass.** This is the single biggest remaining cleanup. Auto-scan every `<a href="...">Chapter N</a>` / `<a href="...">Section N.M</a>` in Parts 1-4 section files, dereference the href to its real chapter/section number, and update the visible label. Same treatment for `title="Section N.M: ..."` attributes on `concept-link`. Same for prose strings like "in Chapter N" / "see Section N.M" where N has been renumbered. Expect ~80-150 fixes across Parts 1-4.

2. **Figure / Table / Code-Fragment caption renumbering.** Script: for each section file at path `module-XX/section-X.Y.html`, rewrite `<strong>Figure A.B.C</strong>` / `<strong>Table A.B.C</strong>` / `<strong>Code Fragment A.B.C</strong>` / `<strong>Listing A.B.C</strong>` so the leading "A" matches the chapter number derived from the path (Chapter X). Also rename image filenames where they encode the old number, OR fix only captions and leave filenames (the alt-text mostly already encodes the new number). About a dozen files in Parts 1-4 need this.

3. **H2 subheading visible-text renumbering.** Where `<h2 id="X-Y-Z">A.B.C ...</h2>` mismatches X-Y-Z != A-B-C, rewrite the visible text to match the ID. Affected modules: Part 1 (2/3/4), Part 2 module-10 sections 10.6-10.9, Part 3 module-14, Part 4 modules 15/16/17/18/19. Single regex pass per file.

4. **Demote tools-of-the-trade inflated chapter-nav blocks** in: part-1/module-05 section-5.1, section-5.2; part-2/module-10 section-10.6, section-10.8; part-4/module-19 section-19.2, section-19.3. Replace the per-subsection `<nav class="chapter-nav">` clusters with a single chapter-nav at the end of each section, matching the structure of section-5.3/5.4/5.5 and section-19.5. Remove the self-pointing `href="section-X.Y.html#anchor"` Previous/Next chains.

5. **Decide what to do with the misplaced "Chapter 12: Tools of the Trade: Models & Tokenizers" content** living as sections 10.6-10.9 inside module-10. Either: (a) create a real module-NN-tools-of-the-trade folder in part-2 and move sections 10.6-10.9 there with renumbered IDs and a new chapter index, then add a new chapter card to the part-2 index; or (b) keep them in module-10 but rebrand them as part of "Chapter 10: Interpretability" (rename h2 IDs from "10-5-" but rename "Chapter 12: Tools of the Trade" breadcrumbs to "Chapter 10: Interpretability"). Option (a) is cleaner because the content is genuinely Tools-of-the-Trade material.

6. **Decide what to do with tokenization sections 1.5-1.7** living inside module-01. Either: (a) lift them to a new module-NN-tokenization folder as Chapter 2, push everything else in part-1 down by 1 (back to the old plan); or (b) keep them in module-01 and rebrand breadcrumbs from "Chapter 2: Tokenization and Subword Models" to "Chapter 1: Foundations of NLP & Text Representation". Whichever path is chosen, the chapter index needs to either list 1.5/1.6/1.7 as sections of the same chapter or stop hiding them. Also fix module-01's chapter-nav next-link which currently points to itself.

7. **Fix part-overview prose in each part-index** to match the actual chapter range. Part I: "Chapters: 6 (Chapters 0 through 5) ... closes with Chapter 5: Tools of the Trade". Part II: "Chapters: 5 (Chapters 6 through 10)". Part III: "Chapters: 4 (Chapters 11 through 14)". Part IV: "Chapters: 5 (Chapters 15 through 19)".

8. **Fix module index `<title>` / `<meta description>` zero-padding and off-by-one.** Modules 0/1/2/3/4 in Part 1 still title-tag as "Chapter 00/01/03/04/05"; module 5 is "Chapter 5". Modules 6/7/8 in Part 2 still zero-pad as "Chapter 06/07/08". Settle on one format (recommend unpadded matching breadcrumb: "Chapter N: Title").

9. **Fix module index chapter-nav prev/next nav-num labels** in Part 1 modules 0-4, Part 2 modules 6-9, Part 3 module-12, and module-08 prereq labels. These still use OLD numbering.

10. **Propagate Wave 16 rename** to all module-17 section breadcrumbs (change "(PEFT)" to "Parameter-Efficient Fine-Tuning, Distillation & Model Merging" or equivalently shorter "Parameter-Efficient Fine-Tuning"); the section files are still on the pre-rename label.

11. **De-duplicate section-6.9** entries in the part-2 index chapter-6 card (drop the second `<li>`) and in module-06's own index (drop the `section-grid` div). Investigate why section-10.6 has 5 chapter-nav blocks and section-10.8 has 2 — likely append-without-replace bug during a previous wave; either dedupe the inline navs or rebuild those section files from canonical content.

12. **Sweep concept-link `title="..."` attributes** for stale chapter/section labels (e.g. `title="Section 37.1: LLM Security Threats"` while href points to `section-47.1.html`). Same pass as #1 but separate selector.
