# Content Audit Cycle 2 — Parts 13-16 + Appendices

Scope: `part-13-llmops-lifecycle/`, `part-14-designing-llm-agent-products/`, `part-14-applications-of-llms-across-industries/`, `part-15-llm-agentic-ai-research-frontiers/`, `appendices/` (A, B, C).

Wave-11-16 remediation closed most title/breadcrumb-level issues. Cycle 2 finds that **section-body H2 numbering, prose cross-reference numbering, and chapter-to-chapter navigation are still pervasively stale** across this group. The body content was assembled by physically moving sections out of old-numbered chapters, but the visible `XX.Y.Z` numbers, the prose "Section/Chapter NN" labels, and the prev/next chapter chrome were never renumbered.

## Top remaining issues

1. **Part 13 H2 body numbering is uniformly stale.** Every numbered H2 in `module-62, 63, 64, 66`, and `section-65.5` reads `53.X.Y` (the old part-12 chapter 53) instead of the new `62/63/64/65/66.Y.Z`. Anchor IDs are also stale (e.g. `id="51-1-1"`). Modules 65.1-65.4 use bare `1.`, `2.`, `3.` style headings (no chapter prefix at all). This is the single biggest visible defect in Part 13.

2. **Part 14, Chapter 67 was a Frankenstein-stitch and the seams show everywhere.** Each of the 15 sections still carries a different stale chapter-prefix in its visible H2s (`58.1.X`, `31.2.X`, `45.2.X`, `45.7.X`, `45.9.X`, `63.1.X`, `63.2.X`, `63.7.X`, `63.9.X`, `65.1.X`, `65.2.X`, `66.X.Y`). Section 67.2 and 68.3 use bare `1.`, `2.`. The chapter index's "What Comes Next" still says "After this chapter you continue to **Chapter 62: LLM Product Management**" and its next-chapter nav says "Chapter 64 LLM Product Management" pointing at module-67 itself (broken self-link). The Chapter 62 page in turn has its next-chapter nav labelled "Chapter 63 Ideation" pointing to module-67 (label out-of-sync with the merged title).

3. **Part 15 Chapter 73 is the worst single page in the group.** The `module-73-manufacturing-llms/index.html` body is the OLD Chapter 57 manufacturing inlined verbatim (with stale `<h2>57.1`…`57.6</h2>` numbering, stale prose refs to Section 32.8, 38.1, 37.5, 46.2, "Chapter 35 LLMOps coverage", and "FM.12") and then has the new 10-section list appended below it. Hero alt text still says "LLMs in Manufacturing & Supply Chain" (stale title). Next-chapter nav reads "Chapter 74 LLMs in Creative Industries" but links to itself (module-78). Sections 73.6 and 78.8 use stale 58.1.X / 59.1.X visible numbering; 78.10 has only text-only h2s. Sections 73.1-78.5 also use text-only h2s. The three-industry merge is technically present but visually still three different chapters.

4. **Part 15 part-index has multiple identity bugs.** `part-14.../index.html` has `<div class="part-label">Part XI</div>` (should be Part XIV), part-overview prose says "nine industries" while the subtitle says "Seven vertical" (chapter contains 7 vertical chapters + 1 tools chapter), and the hero alt text says "Part XI: LLM Applications Across Industries". Inside chapter 72's index, "rest of Part XI builds on" and "Chapter 52" link are stale (should be Part XIV, Chapter 68). Modules 73, 74, 76 each reference a phantom "Section 68.6 / 74.6 / 76.6 (longer production-pattern companion)" that does not exist.

5. **Part 16 triple-numbering is NOT resolved.** Part-index has `<div class="part-label">Part XII</div>`, hero alt text "Part XII: Frontiers", part-overview says "Chapters: 5 (Chapters 61 through 65)" with a "frontier systems and hardware" chapter the index does not list, and the big-picture callout opens with "The field … Part XII looks ahead". Inside `module-80/index.html`, the Looking Back callout references Chapter 62/63/64 (should be 81/82, hardware chapter gone), next-chapter nav says "Chapter 78 Frontier Theory" pointing to module-81, prev nav says "Chapter 76 Tools of the Trade" pointing to part-14 module-79. `module-81` "What Comes Next" sends the reader to "Chapter 63" in `part-12/module-58-frontier-systems-hardware` (cross-part jump out of Part XV). `module-82` nav says "Chapter 84 Frontier Systems & Hardware" (prev) and "Chapter 86 Tools of the Trade" (next); "What Comes Next" says "Chapter 65 wraps Part XII". `module-83` prev says "Chapter 85 AGI Trajectories". Every visible H2 in 80.1-80.4 reads `33.X.Y`, in 81.1-81.4 reads `33.5-33.8.Y`, in 82.1-82.5 reads `64.X.Y`, in 83.1-83.5 reads `65.X.Y`. The dir names (80-83), the in-page H1/chapter labels (80-83), and the nav chapter numbers (81-86, plus stray Chapter 62/63/64/65 in body prose) form a three-way disagreement that exactly matches the cycle-1 finding.

6. **Appendix B figure label is "C.0.1"** (should be B.0.1). **Appendix C figure label is "D.0.1"** (should be C.0.1). Wave 9F renamed the breadcrumbs but missed the figure captions. Appendix C's pagefind chapter meta says `"Chapter 0 (Section 0.1): Reading Pathways"` (should just be "Appendix C").

7. **Appendix B and C use stale book chapter numbers throughout.** Every week-by-week row in B's tables uses the OLD chapter number as visible link text while the href points to the CURRENT module — e.g. Wk 1 row says "Chapter 0 (ML and PyTorch foundations)" linking to module-00 (which is Chapter 0 now, OK), but Wk 5 says "Chapter 4 (Transformer architecture)" linking to module-03 (which is now Chapter 3), Wk 7 says "Chapter 13 (LLM APIs)" linking to module-11 (now Chapter 11), Wk 12 says "Section 34.1" linking to section-42.1 (now Section 42.1), Wk 13 says "Section 35.1" linking to section-70.5, Track-3 Wk 8 says "Chapter 25 (Agent safety)" linking to part-10 module-49 (now Chapter 49), Track-3 Wk 9 says "Chapter 34 (Evaluation)" linking to module-42, Track-3 Wk 10 says "Chapter 35 (Production)" linking to module-62, Track-4 Sem-2 says "Chapter 33 (Frontiers)" linking to module-80 (now Chapter 75), Track-5 Wk 10 says "Chapter 31 (Strategy)" linking to module-67. Reference-appendices list says "Section 6.1 (Platforms)" linking to section-5.1 (now Section 5.1). Bottom nav reads `<span class="nav-num">Section O.4</span>` (gibberish). Line 227 has an empty `<li> for worked-through fixes to common end-of-chapter problems.</li>` (broken anchor). Appendix C's eight pathways have the exact same defect on almost every link: "Chapter 13 (LLM APIs)" → module-11, "Section 14.2" → section-12.2, "Chapter 22" → module-31, "Chapter 23" → module-32, "Chapter 24" → module-37, "Chapter 26/27/28/29" → module-26/27/28/29 (these happen to match), "Chapter 25 (Agent Safety)" → part-10 module-49, "Chapter 34 (Eval)" → module-42, "Chapter 33 (Frontiers)" → module-80, "Chapter 31 (Strategy, PM & ROI)" → module-67, "Chapter 45 (Building LLM and Agent Products)" → module-67, "Chapter 48 (Shipping & Scaling)" → module-70, "Section 18.1" → section-16.1, "Section 34.11" → section-42.5. Pathway 5 step 6 ("Section 33.7 Mechanistic interpretability at scale") is text-only, no link, and the new location is section-81.3.

8. **Appendix A keeps a section that pretends it is Chapter 4.** `section-a.6.html` is essentially the lifted Chapter 4 "Information Theory" subsection — body H2 is `4.1.2`, H3s are `4.1.2.1` through `4.1.2.8`, prose says "originated as a section of Chapter 04 (Transformer Architecture)" and links to "Section 20.1" (now 18.1). The appendix-A `index.html` description claims "Four domains are covered" but lists six section cards; the "When to Use This Appendix" callout still says "Chapter 04's attention mechanism", "Chapter 06 loss functions", "Chapter 19 PEFT" — the zero-padding is wrong style and Chapter 4 is now Decoding, not Transformer. `section-a.1.html` has a duplicated `Code Fragment a.1.1` (lowercase) caption sitting one block above the canonical `A.1.1` (uppercase) caption.

9. **Cross-part navigation chrome is broken across the group.** Cycle 1 fixed breadcrumbs at the top; the `<nav class="chapter-nav">` blocks at the bottom were not touched and still carry old chapter numbers (62→63→…→86 inflation across Part 16), wrong titles ("Chapter 63 Ideation" attached to module-67 from chapter 62), and self-links (module-67 next → module-67, module-78 next → module-78). Several inter-chapter "What Comes Next" prose blocks reference renamed/non-existent chapter titles.

10. **Hero alt-text fragmentation.** Several index hero `<img alt=…>` strings are truncated mid-sentence with the remainder spilling into the `<figcaption>`: `module-67-ideation` ("Ideation: Finding LLM-" / "Worthy Problems'"), `module-77-agi-trajectories` ("AGI Trajectories &" / "Open Questions'"), `module-78-tools-of-the-trade` ("Tools of the Trade: Fr" / "ontier Research Stack'"), `module-73-manufacturing-llms` (alt still "LLMs in Manufacturing & Supply Chain"). These are accessibility regressions from the renaming pass.

## Per-chapter findings

### Part 13 — LLMOps Lifecycle

- **Part index** (`part-13.../index.html`): clean. No part-label drift, no stale chapter cards. Cycle 1 fix held.
- **Chapter 62 index** (`module-62.../index.html`):
  - Breadcrumb says `Part X` (should be `Part XIII`).
  - Description (head + big-picture) still lists "AI gateways, workflow orchestration, edge deployment, reliability, Kubernetes-native operations" — content from the pre-split full Chapter 53, but this chapter now only contains 62.1 + 62.2 (scaling + LLMOps).
  - Next-chapter nav reads `Chapter 63 Ideation: Finding LLM-Worthy Problems` and links to `part-14.../module-67-ideation/index.html`. Should be Chapter 63 AI Gateways & Model Routing in this part.
- **Section 62.1**:
  - Body H2s: `53.1.1 Latency Optimization Strategies`, `53.1.2 Backpressure…`, `53.1.3 Production Guardrails`, `53.1.4 Production Memory Patterns`. Anchor ids `51-1-1`, etc.
  - Body prose figure ref: `Figure 53.1.1` (stale).
  - Prereq link text "Section 45.1: Application Architecture and Deployment" (now Section 70.5).
  - Prose: "the prompt injection defenses from Section 14.4" (now 12.4), "quantization techniques from Section 10.1" (now 9.1), "KV cache… Section 10.2" (now 9.2), "memory architectures discussed in Section 24.3" (now 37.3).
  - End "Section 45.4 covers the LLMOps practices…" and "Next: Section 45.4: LLMOps & Continuous Improvement" — should be 62.2.
- **Section 62.2**: H2 numbering `53.2.1`…`53.2.4`. Same pattern.
- **Section 63.1**: H2 numbering `53.3.1`…`53.3.6`. Anchor ids `51-3-1` etc.
- **Section 64.1**: H2 numbering `53.4.1`…`53.4.7`. Anchor ids `51-4-1` etc.
- **Sections 65.1-65.4**: H2s are unnumbered (`1. Why ML Engineers Need Docker`, …, `8. Cleaning Up`), no chapter prefix. Self-consistent within each section but inconsistent with the rest of the book.
- **Section 65.5**: H2 numbering `53.7.1`…`53.7.6` (note: 7th sub-chapter of old Chapter 53). Anchor ids `51-7-1` etc.
- **Section 66.1**: H2 numbering `53.6.1`…`53.6.8`. Anchor ids `51-6-1` etc.

### Part 14 — Designing LLM/Agent Products

- **Part index**: clean. Chapter cards correct.
- **Chapter 67 (From Idea to MVP) index**:
  - Hero alt-text broken: `alt="… 'Ideation: Finding LLM-"` then figcaption opens `Worthy Problems', a Kurzgesagt…`.
  - "What Comes Next" reads "After this chapter you continue to **Chapter 62: LLM Product Management**" — wrong number, wrong title, wrong successor.
  - Next-chapter nav: `Chapter 64 LLM Product Management` linking to `../module-67-ideation/index.html` (broken self-link).
- **Section 67.1**: visible H2 `58.1.1`…`58.1.6` (stale).
- **Section 67.2**: unnumbered bare `1.`…`5.`.
- **Section 67.5**: `31.2.1`…`31.2.6`.
- **Section 67.7**: visible `65.1.1`…`65.1.6` but anchor ids `67-7-1`…`67-7-6` (anchor right, text wrong).
- **Section 67.8**: visible `65.2.1`…`65.2.4`, anchor ids `65-4-1`…`65-4-4` (both wrong, two different stale prefixes).
- **Section 67.9**: visible `63.1.1`…`63.1.7`, anchor ids `45-1-1`…`45-1-7`.
- **Section 67.10**: visible `63.2.1`…`63.2.6`, anchor ids `45-2-1`…`45-2-6`.
- **Section 67.14**: visible `63.7.1`…`63.7.6`, anchor ids `45-7-1`…`45-7-6`.
- **Section 67.15**: visible `63.9.1`…`63.9.9`, anchor ids `45-9-1`…`45-9-9`.
- The 15 sections of Chapter 67 collectively contain numbering from at least seven different former chapters (31, 45, 58, 63, 65, plus bare-numbered and unnumbered styles). The "is this one coherent chapter?" question can be answered both ways: the section titles read as a coherent product-idea-to-MVP arc, but the body numbering is a strong signal these were separate chapters and the renumbering pass never ran.
- **Section 68.1**: visible `61.1.1`…`61.1.6`.
- **Section 68.3**: bare `1.`…`5.`.
- **Section 69.1**: visible `64.1.1`…`64.1.4`.
- **Section 70.1**: visible `45.1.1`…`45.1.5`, anchor ids `35-1-1`…`35-1-5`.
- **Section 70.5**: visible `65.5.1`…`65.5.5`, anchor ids `50-5-1`…`50-5-5`.
- **Section 71.1** (Tools — Platforms): visible `66.1.1`…`66.1.4` and then two extra unnumbered h2s (`Deployment Patterns`, `SLOs, Alerting, and FinOps`) that look out of place for a "Platforms" section — possibly leaked content from a different part's Tools-of-the-Trade page.
- **Section 71.2**: visible `66.2.1`…`66.2.3` plus a stray `Reproducibility and CI/CD for ML` heading.
- **Sections 71.3, 71.5**: visible `66.3.X` / `66.5.X`.

### Part 15 — Applications of LLMs Across Industries

- **Part index** (`part-14.../index.html`):
  - `<div class="part-label">Part XI</div>` (should be `Part XIV`).
  - Hero `<img alt="… 'Part XI: LLM Applications Across Industries'.">` (stale).
  - Subtitle says "Seven vertical applications" — true if you count merged Chapter 73 as one — but body prose says "Part XI takes the techniques … and applies them to **nine industries**". Pick a number.
  - The chapter-card list is correct (chapters 72-79).
- **Chapter 67 (Legal)**:
  - "Sections in This Chapter" body is accurate.
  - "What Comes Next" prose: "Legal sets the verification-heavy pattern that the rest of **Part XI** builds on. **Chapter 52** turns to finance" — both stale (should be Part XIV, Chapter 68).
  - Section H2s (72.1, 72.2): unnumbered text-only headings. Self-consistent and no stale numbers, but inconsistent with the deep-numbered style used elsewhere in the book.
- **Chapter 68 (Finance)**: index body references nonexistent "Section 68.6 (longer production-pattern companion)". Section 68.1 uses unnumbered text-only h2s — same pattern.
- **Chapter 69 (Healthcare)**: index body references nonexistent "Section 69.6". Title in `<title>` says "LLMs in Healthcare" but H1 says "LLMs in Healthcare & Biomedical".
- **Chapter 70 (Education)**: clean. (No phantom-section reference.)
- **Chapter 71 (Cybersecurity)**: index body references nonexistent "Section 71.6".
- **Chapter 72 (Government)**: clean.
- **Chapter 73 (Manufacturing+Creative+Search/Rec)**: catastrophically inconsistent.
  - Hero alt-text says "LLMs in Manufacturing & Supply Chain" (stale title, doesn't match merged H1).
  - The index body inlines the OLD Chapter 57 manufacturing prose verbatim with H2s `57.1`…`57.6`, then appends the 10-section card list below. Reader sees Manufacturing twice (once inline at chapter 57 numbering, once in the section cards at 78.X). Creative-industries and search/recommendation content has no inline coverage at all — only the section cards point at it.
  - "Where to Read More" block in the inline prose references "Section 32.8 (Robotics, Embodied AI & Scientific Discovery)" → part-5 module-24, "Section 38.1 (Agent Safety…)" → section-49.1, "Section 37.5 (LLM Risk Governance & Audit)" → section-53.3, "Section 46.2 (Enterprise Integration Patterns)" → section-57.2, plus a stub bullet `FM.12 (production-patterns playbook (now part of Chapter 35 LLMOps coverage))` — all stale.
  - Next-chapter nav: `Chapter 74 LLMs in Creative Industries` pointing to `module-73-manufacturing-llms/index.html` — wrong title (real chapter 79 is Tools of the Trade) and broken self-link.
  - Section 73.1-78.5: text-only h2s (matches the inline duplicate).
  - Section 73.6: `58.1.1`…`58.1.4`.
  - Section 73.8: `59.1.1`…`59.1.3`.
  - Section 73.10: text-only h2s.
- **Chapter 74 (Tools of the Trade)**: all sections use visible `60.X.Y` numbering (anchor ids `79-X-Y`, so anchors are correct, only visible text is stale).

### Part 16 — LLM & Agentic AI Research Frontiers

- **Part index** (`part-15.../index.html`):
  - `<div class="part-label">Part XII</div>` (should be `Part XV`).
  - Hero alt text: `"Part XII: Frontiers"`.
  - Part overview: "Part XII surveys the frontier … **across five chapters**. … (Chapters 61 through 65). … **frontier systems and hardware** (non-NVIDIA silicon, decentralized training, edge LLMs, training-inference co-design)". Index only lists 4 chapters and the hardware/systems chapter is gone. Either the chapter is missing or the description needs to be rewritten to match the current 4-chapter shape.
  - Big-picture callout: "Part XII looks ahead at emerging architectures, theory, hardware, AGI trajectories…".
- **Chapter 75 (Frontier Architectures)** index:
  - "Looking Back" callout: "Part XII covers what it has not. … Theory of reasoning … live in **Chapter 62**; hardware and systems live in **Chapter 63**; AGI trajectories live in **Chapter 64**." All stale (and Chapter 63 hardware doesn't exist).
  - Prerequisites use zero-padded "Chapter 04", "Chapter 06", "Chapter 10" — wrong padding style and Chapter 4 is now Decoding (transformer is Chapter 3); Chapter 06 = Pretraining (OK numerically); Chapter 10 = Interpretability (was Inference Opt at 9).
  - "What's Next?" sends reader to `Part XI` (should be Part XIV).
  - Prev nav: `Chapter 76 Tools of the Trade: Industry Solution Stack` (real chapter 79).
  - Next nav: `Chapter 78 Frontier Theory & Cognition` (real chapter 81).
- **Section 75.1**: H2 `33.1.1`…`33.1.5`.
- **Section 75.4**: H2 `33.10.2`…`33.10.11` (and the `33.10.1` numbered heading is missing — index opens straight at `33.10.2`).
- **Chapter 76 (Frontier Theory)** index:
  - "What Comes Next" sends reader to `Chapter 63` in `part-12/module-58-frontier-systems-hardware` (cross-part jump out of Part XV; chapter # nonsense).
  - Prev nav: `Chapter 77 Frontier Architectures & Scaling`.
  - Next nav: `Chapter 84 Frontier Systems & Hardware` pointing to `part-12/module-58-frontier-systems-hardware`.
- **Section 76.1**: H2 `33.5.1`…`33.5.8`. Section 76.4: H2 `33.8.1`…`33.8.7`.
- **Chapter 77 (AGI Trajectories)** index:
  - Hero alt-text broken (alt cuts off, rest in figcaption).
  - Section 77.2 desc: "alignment … covered in **Part IX** continue to work" — Part IX is Evaluation now; alignment is Part IV.
  - "What Comes Next" says "**Chapter 65** wraps Part XII" and labels appendices as "capstone project".
  - Prev nav: `Chapter 84 Frontier Systems & Hardware` (does not exist).
  - Next nav: `Chapter 86 Tools of the Trade: Frontier Research Stack`.
- **Sections 77.1, 82.5**: H2 `64.X.Y` visible, anchor ids `82-X-Y` (anchors correct, visible text stale).
- **Chapter 78 (Tools of the Trade)** index:
  - Hero alt-text broken (alt cuts off).
  - "Big Picture" opens "**Part XII** looked at the frontiers".
  - Prev nav: `Chapter 85 AGI Trajectories & Open Questions`.
- **Section 78.1**: H2 `65.1.1`…`65.1.4` visible, anchor ids `83-1-X`.

### Appendix A — Mathematical Foundations

- Index `<meta description>` says "This appendix collects the mathematical background…" (already covers it). Big-picture callout says "Four domains are covered" but the page lists 6 sections (A.1-A.6). Need to either say six, or remove A.6.
- "When to Use This Appendix" callout: "Chapter 04's attention mechanism formulas" — Chapter 4 is Decoding now, Transformer is Chapter 3. Also uses zero-padded "Chapter 04"/"Chapter 06"/"Chapter 19" while the rest of the book uses unpadded forms.
- Cross-link in opening prose: "Chapter 00 (ML and PyTorch Foundations)" — zero-padded; also "Chapter 06 (Pretraining and Scaling Laws)" and "Chapter 34 (Evaluation)" — Chapter 34 is wrong (Evaluation is Chapter 42 now).
- `section-a.1.html` has a duplicate `Code Fragment a.1.1:` caption (lowercase a) at line 54 just above the canonical `A.1.1` at line 63.
- `section-a.6.html` is the only section that hasn't been renumbered. H2 `4.1.2 Information Theory: The Language of Learning`. H3s `4.1.2.1`…`4.1.2.8`. Prose: "It originated as a section of **Chapter 04** (Transformer Architecture) but was moved here". Prose: "or a KL divergence penalty in **Section 20.1**" (link points to part-4 module-18 section 18.1, so prose label is wrong). `Code Fragment 4.1.1` caption at line 244. Heading text should be `A.6.X` and prose chapter/section labels should be updated.
- Section list on index has A.1-A.5 in one `<ul>` and A.6 alone in a separate `<div class="section-grid">` with a different card style — looks like a half-finished merge of two listings.

### Appendix B — Course Syllabi

- Title/breadcrumb/aria-label consistent ("Appendix B: Course Syllabi"). Wave 9F fix held at the chrome level.
- Figure caption: `<strong>Figure C.0.1</strong>` (wrong letter; should be B.0.1). `id="long-desc-59"` is a fine arbitrary id.
- Almost every table cell with a Reading link uses the old chapter/section number as the visible link text:
  - "Section 6.1 (Platforms)" → links to section-5.1 (current label is "Section 5.1").
  - Track-1 Wk 5: "Chapter 4 (Transformer architecture)" → module-03 (current Chapter 3).
  - Track-1 Wk 6: "Chapter 5 (Decoding strategies)" → module-04 (current Chapter 4).
  - Track-1 Wk 7: "Chapter 13 (LLM APIs)" → module-11 (current Chapter 11).
  - Track-1 Wk 8: "Chapter 14 (Prompt engineering)" → module-12 (current Chapter 12).
  - Track-1 Wk 9: "Chapter 22 (Embeddings and vector DBs)" → module-31 (current Chapter 31).
  - Track-1 Wk 10: "Chapter 23 (RAG)" → module-32 (current Chapter 32).
  - Track-1 Wk 11: "Chapter 24 (Conversational AI)" → module-37 (current Chapter 37).
  - Track-1 Wk 12: "Section 34.1" → section-42.1 (current Section 42.1).
  - Track-1 Wk 13: "Section 35.1" → section-70.5 (current Section 70.5).
  - Track-2 Wk 7-11: "Chapter 7-11" → module-06 to module-10 (need to verify each against TOC; module 6-10 = chapters 6-10 in current numbering, so these are correct numerically).
  - Track-2 Wk 12: "Chapter 18 (Fine-tuning)" → module-16. Confirm: module-16 = Chapter 16 ("Fine-Tuning Fundamentals") in current numbering. Need to recheck — likely "Chapter 16" current, not 18.
  - Track-3 Sem-1 Wk 11-12: "Chapter 17, 18, 19" → module-15, 16, 17 — same pattern (module 15 = Chapter 15 currently).
  - Track-3 Sem-1 Wk 13: "Chapter 20 (Alignment, RLHF, DPO)" → module-18 (current Chapter 18).
  - Track-3 Sem-2 Wk 8: "Chapter 25 (Agent safety)" → part-10 module-49 (current Chapter 49).
  - Track-3 Sem-2 Wk 9: "Chapter 34 (Evaluation)" → module-42 (current Chapter 42).
  - Track-3 Sem-2 Wk 10: "Chapter 35 (Production)" → module-62 (current Chapter 62).
  - Track-4 Sem-2 row 1: "Chapter 31 (Multimodal)" → part-5 module-20 (current Chapter 20).
  - Track-4 Sem-2 row 2: "Chapter 37 (Safety, ethics, regulation)" → part-10 module-47 (current Chapter 47).
  - Track-4 Sem-2 row 3: "Chapter 33 (Frontiers)" → module-80 (current Chapter 75).
  - Track-5 Wk 10: "Chapter 31 (Strategy)" → module-67 (current Chapter 67).
- "Reference appendices used across tracks" list has a broken `<li> for worked-through fixes to common end-of-chapter problems.</li>` (line 227) with no link wrapper or noun phrase before "for".
- Bottom prev nav: `<span class="nav-num">Section O.4</span><span class="nav-title">Containerizing LLM Inference Servers</span>` — `O.4` is gibberish (likely was old roman numeral lift); real prev is Section 65.4.

### Appendix C — Reading Pathways

- Title/breadcrumb/aria-label consistent.
- Pagefind chapter meta: `data-pagefind-meta="chapter:Chapter 0 (Section 0.1): Reading Pathways"` — should just be "Appendix C: Reading Pathways". This will pollute pagefind result chrome.
- Figure caption: `<strong>Figure D.0.1</strong>` (should be C.0.1).
- Every pathway has the same kind of stale visible-text/correct-href problem as Appendix B:
  - Pathway 1: "Chapter 13 (LLM APIs)" → module-11, "Chapter 14 (Prompt Engineering)" → module-12, "Chapter 22 (Embeddings & Vector DBs)" → module-31, "Chapter 23 (RAG)" → module-32, "Section 34.1 (Eval fundamentals)" → section-42.1, "Section 35.1 (Deployment)" → section-70.5.
  - Pathway 2: "Section 14.2 (Reasoning + ReAct)" → section-12.2, "Chapter 25 (Agent Safety & Production)" → part-10 module-49, "Chapter 34 (Eval)" → module-42.
  - Pathway 3: "Chapter 7 (Pretraining + Scaling Laws)" → module-06 (current Chapter 6), "Chapter 8 (Modern LLM Landscape)" → module-07 (current Chapter 7), "Chapter 15 (Hybrid ML+LLM)" → module-13 (current Chapter 13), "Chapter 18 (Fine-tuning Fundamentals)" → module-16, "Chapter 19 (PEFT)" → module-17, "Chapter 34 (Evaluation)" → module-42.
  - Pathway 4: "Full Part I (Chapters 0-5)" — chapters 0-5 are right but Part I has 6 chapters (0-5), language ok. "Full Part II (Chapters 6-9 + 31)" — Part II spans chapters 6-10 actually. "Full Part IV (Chapters 13-16)" — Part IV is fine-tune etc, chapters 15-19. "Chapter 33 (Emerging Architectures & Frontiers)" → module-80 (current Chapter 75). "Section 34.11" → section-42.5.
  - Pathway 5: "Chapter 7 (Pretraining)" → module-06 (OK), "Chapter 11 (Interpretability)" → module-10 (current Chapter 10), "Chapter 25 (Agent Safety)" → part-10 module-49, "Chapter 37 (Safety, Ethics & Regulation)" → part-10 module-47, "Section 33.7 (Mechanistic interpretability at scale)" — text-only, no link, real location section-81.3.
  - Pathway 6: "Section 14.1" → section-12.1, "Section 18.1 (Fine-tune-or-not decision tree)" → section-16.1, "Chapter 27 (LLM Applications by Industry)" — text-only, no link, this is now Part XIV (chapters 72-79). "Chapter 31 (Strategy, PM & ROI)" → module-67. "Chapter 45 (Building LLM and Agent Products)" → module-67 (same target — likely a duplicate; pick one). "Chapter 48 (Shipping & Scaling)" → module-70 (current Chapter 70).
  - Pathway 7: refers to "FM.7 Copyright & Legal" (FM-prefix is fine), "Appendix B (Course Syllabi)" (good), "Full Part I (Chapters 0-5)" (OK).
  - Pathway 8: "Chapter 8 (Modern LLM Landscape)" — `module-07` current Chapter 7, "Chapter 9 (Reasoning Models)" — `module-08` current Chapter 8, "Chapter 33 (Frontiers)" → module-80 (current Chapter 75).
- The "How to Choose" / "Combine Pathways" callouts at the bottom are fine.

### Capstone

- `capstone/requirements.html` references chapter numbers ("Chapters: 05, 12, 13", "Chapters: 12, 13, 14, 15", "Chapters: 18, 19, 20", "Chapters: 21, 22", "Chapters: 26, 27", "Chapters: 09, 10, 14, 19") that look like the OLD numbering and would need to be remapped against current Chapter 1-83.

## Suggested cycle 3 actions

1. **Run a "renumber section bodies" pass for Parts 13, 14, 16.** Walk every `section-NN.Y.html`, find numbered `<h2 id="...">XX.Y.Z TEXT</h2>` and `<h3 id="...">XX.Y.Z.W TEXT</h3>` headings, and replace the visible prefix with `NN.Y.Z` derived from the file path. Update anchor IDs and any in-page `#XX-Y-Z` links. For sections that currently use bare `1.`, `2.` (Part 13 modules 65.1-65.4 and Part 14 sections 67.2, 68.3) decide whether to add the `NN.Y.` prefix or strip the prefix from sister sections for consistency. This is the single highest-impact change.

2. **Run a "renumber prose cross-refs" pass.** Script: find `<a href="… section-AB.C.html…">Section XX.Y</a>` patterns. For each link, follow the href, read the actual section number from the breadcrumb/H1, and rewrite the visible "Section XX.Y" label. Same for `Chapter NN` labels — read the chapter card or module index to get the current chapter number. This will fix Appendix B and C en masse (their hrefs are right, only the labels are wrong) and also fix the body cross-refs in Part 13/14/16 sections.

3. **Rebuild the bottom `<nav class="chapter-nav">` chrome from scratch** based on the YAML structure or the part-index card order. The current state shows chapter numbers like 81, 82, 83, 84, 85, 86 inside Part XV (which has chapters 80-83), and chapter 62/63/64 inside Part XIII when chapter 63 should be Gateways. A small generator that walks the book_structure.yaml and emits prev/up/next nav for every section + chapter index would fix this in one pass.

4. **Fix Part 15 Chapter 73.** Three options:
   - (a) Strip the inlined "57.1"…"57.6" manufacturing prose out of `module-78/index.html` entirely (it duplicates section 73.1-78.5).
   - (b) Keep the inline content but renumber to 78.X and treat the section cards as a TOC summary.
   - (c) Split the chapter back into three (Manufacturing, Creative, Search/Rec) and update the part-index cards. Cycle-1 chose to merge, so (a) or (b) is the consistent move. Also fix the next-chapter nav self-link, the stale hero alt-text, and the stale "Section 32.8 / 38.1 / 37.5 / 46.2" links in the inline prose.

5. **Fix Part 16 part-index and all four chapter indexes.** Replace `Part XII` → `Part XV` in part-label, hero alt, overview prose, big-picture, Looking-Back callouts. Either rewrite the part overview to match the current 4 chapters (drop the missing "frontier systems & hardware" chapter from the description) or restore the missing chapter. Fix every `Chapter 61-65` and `Chapter 84-86` reference; nothing in Part XV is below 80 or above 83.

6. **Fix Part 15 part-index.** `Part XI` → `Part XIV` in part-label, hero alt, overview prose ("rest of Part XI"). Reconcile "Seven vertical" subtitle vs "nine industries" overview.

7. **Strip phantom Section X.6 references** from chapter 73, 74, 76 indexes (or create the section files if a "longer production-pattern companion" really is intended).

8. **Fix Appendix figure captions and pagefind meta**: `Figure C.0.1` → `B.0.1` in Appendix B; `Figure D.0.1` → `C.0.1` in Appendix C; pagefind chapter meta in Appendix C from `"Chapter 0 (Section 0.1): Reading Pathways"` to `"Appendix C: Reading Pathways"`.

9. **Decide Appendix A section A.6's fate.** Either fully promote it to A.6 numbering (rename H2 `4.1.2 …` to `A.6.1 …`, drop "originated as a section of Chapter 04" prose, fix `Section 20.1` ref, fix `Code Fragment 4.1.1` caption) or fold it back into A.4 since A.4 is already "Information Theory" (current A.6 title is "Information Theory for Language Models" — partially overlaps A.4). The split index card-style (A.1-A.5 in one list, A.6 in a separate grid) hints A.6 was added after the others.

10. **Address single-section chapters (63, 64, 66 in Part 13).** Each chapter index page has only one section, which makes the chapter index essentially redundant. Either accept the structure (and silence cycle-1's flag) or split the long sections into 2-3 per chapter so the index has substance. Recommend splitting because all three single-section files are 600+ lines (`section-63.1`, `section-64.1`, `section-66.1`) and contain 6-8 H2 subsections that would each make reasonable sections of their own.

11. **Fix hero alt-text fragmentation** in `module-67/index.html`, `module-78/index.html`, `module-82/index.html`, `module-83/index.html`. Single character-limit truncation has split the alt attribute across the alt and the figcaption; merge into one complete alt string.

12. **Remove `_section_split_plan.md` from each module dir** (modules 67, 68, 72-77) — these are leftover scratch files and shouldn't ship.
