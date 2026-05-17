# Cycle 3 Audit — Parts 13-16 + Appendices

Scope: `part-13-llmops-lifecycle/` (modules 62-66), `part-14-designing-llm-agent-products/` (modules 67-71), `part-15-applications-of-llms-across-industries/` (modules 72-79), `part-16-llm-agentic-ai-research-frontiers/` (modules 80-83), `appendices/` (A: Mathematical Foundations, B: Course Syllabi, C: Reading Pathways), `capstone/` (index + requirements). Read-only audit between cycle 2 (which described pervasive H2 numbering drift, stale chapter labels in breadcrumbs and prev/next nav, Frankenstein-stitched chapter 67/78, "Part XII" residue in Part 16, and miswritten appendix figure/table prefixes) and the cycle 3 starting state after waves 17a-g and 17b-targeted landings.

Note: the prompt described part-15 as containing modules 72-78, but the on-disk + yaml structure (`book_structure.yaml` lines 1610-1807) places module 79 (Tools of the Trade: Industry Solution Stack) inside Part XV, not Part XVI. The audit treats 79 as part of Part XV; Part XVI's tools chapter is module 83.

## Resolved since cycle 2

- **Wave 17b (Part 16 part-label / part-index)** verified: `part-16-llm-agentic-ai-research-frontiers/index.html` line 24 reads `<div class="part-label">Part XVI</div>` and the H1, `<title>`, meta description, breadcrumb-ish prose, and big-picture callout all read "Part XVI". The part-overview prose still claims "5 chapters / Chapters 61 through 65" (see Remaining P2) but the part identity itself is fixed.
- **Wave 17b (module-78 inline old-Ch-57 prose)** verified gone: `part-15.../module-78-manufacturing-llms/index.html` no longer contains H2s with prefix `57.X`, the duplicated inline Manufacturing narrative, the stale "Section 32.8/38.1/37.5/46.2/FM.12" cross-refs, or the "Chapter 35 LLMOps coverage" line. The chapter-card big-picture is now a clean single paragraph about the IT/OT boundary, and the section-card list (78.1-78.10) covers Manufacturing + Creative + Search/Rec without inline duplication.
- **Wave 17b (scratch files)** verified: `git ls`-equivalent glob `**/_section_split_plan.md` returns zero hits in the working tree. All nine cycle-2-flagged scratch files (modules 67, 68, 72-77) are removed.
- **Wave 17c (H2/H3 visible numbering and IDs)** verified for canonically-named `section-N.M.html` files in Parts 13, 14, 16:
  - Part 13 modules 62, 63, 64, 66 plus section 65.5 now use `62.X.Y` / `63.X.Y` / `64.X.Y` / `65.5.Y` / `66.X.Y` visible numbering with matching anchor IDs (cycle-2 reported `53.X.Y` / `51-1-1` styles).
  - Part 14 modules 67, 68, 69, 70 now use `67.X.Y` etc.; cycle-2-reported `31.2.X`, `45.X.X`, `58.1.X`, `63.X.X`, `65.X.X`, `66.X.X` prefixes are gone for files matched by the regex.
  - Part 16 modules 80.1-80.3, 81.1-81.4, 82.1-82.5, 83.1-83.5 all use `80/81/82/83.X.Y` visible + ID; cycle-2-reported `33.X.Y` / `64.X.Y` / `65.X.Y` are gone. Section 80.4 has an exception (see Remaining P1).
- **Wave 17b/c (Part-16 chapter labels in breadcrumbs)** verified: every section file under part-16 carries `Part XVI: LLM &amp; Agentic AI Research Frontiers` + `Chapter 80/81/82/83: ...` in the breadcrumb. Cycle-2's `Chapter 81-86 inflation` is gone for sections.
- **Wave 17g (chapter-nav rebuild) — Part 16** verified for module 80-83 section files: prev/next/up chapter numbers map correctly to 80-83 range; cycle-2-reported "Chapter 84/85/86" labels are gone.
- **Cycle-2 #2 self-link in module-67/index.html next-chapter nav** verified fixed: line 119 nav-next now points to `../module-68-vibe-coding/index.html` with label "Chapter 68 Prototyping via Vibe-Coding" (cycle-2 had it self-linking back to module-67).

## Remaining issues (priority order)

### P1. Section 80.4 has a malformed H2 that breaks the heading sequence

`part-16.../module-80-frontier-architectures/section-80.4.html` line 54 contains the literal text `2&gt;1. The Universal Recipe` (rendered as `2>1. The Universal Recipe`) outside any heading element. The intended `<h2 id="80-4-1-the-universal-recipe">80.4.1 The Universal Recipe</h2>` is missing entirely. As a result the H2 sequence starts at `80.4.2`, the section has no heading for the universal-recipe content, and `Exercises` (line 144) sits between `80.4.3` and `80.4.4` instead of at the end. Other section-80.4 H2/H3 IDs and visible numbers are correct.

### P2. Part-15 part-index still carries the cycle-2 "Part XI" identity bug

`part-15-applications-of-llms-across-industries/index.html`:
- Line 24: `<div class="part-label" data-pagefind-meta="part">Part XI</div>` — should be `Part XV`. Wave 17 did not touch this file.
- Line 29: hero image alt-text says `Part XI: LLM Applications Across Industries`.
- Line 37: part-overview opens "Part XI takes the techniques developed across the rest of the book ... and applies them to **nine industries**" — should be Part XV; "nine" contradicts the subtitle line 26 which says "Seven vertical applications" (and the index lists 7 vertical chapters 72-78 plus 1 tools chapter 79).
- Description meta (line 7) reads "nine verticals" but the part subtitle says "Seven vertical applications".

### P2. Part-16 part-overview still describes a vanished 5th chapter

`part-16-llm-agentic-ai-research-frontiers/index.html` line 40: "Chapters: 5 (Chapters 61 through 65)." The part-card list shows 4 chapters (80, 81, 82, 83). The overview body (line 37) still describes "frontier systems and hardware (non-NVIDIA silicon, decentralized training, edge LLMs, training-inference co-design)" as a covered chapter; that chapter does not exist in this part. Either the overview needs to drop that paragraph + correct the count to "4 chapters (80-83)", or the missing chapter needs to be restored.

### P2. "Part XII" residue inside Part 16 module indexes and one section body

Wave 17b fixed the part-16/index.html. It did not sweep the module indexes:
- `module-80-frontier-architectures/index.html` line 36: "Part XII covers what it has not. ... Theory of reasoning ... live in **Chapter 62**; hardware and systems live in **Chapter 63**; AGI trajectories live in **Chapter 64**." Three stale chapter numbers (real targets are 81, no chapter, 82) plus stale "Part XII".
- `module-80.../index.html` line 106: `<a href="../../part-14-designing-llm-agent-products/index.html">Part XI</a>` — visible text "Part XI" but href points to Part XIV. Should read "Part XIV".
- `module-82-agi-trajectories/index.html` line 75: "**Chapter 83** wraps **Part XII**" plus the same line links `<a href="../../appendices/index.html">capstone project</a>` — capstone now lives at `/capstone/`, not in `/appendices/`. Two bugs in one anchor.
- `module-83-tools-of-the-trade/index.html` line 35: "Part XII looked at the frontiers" — stale.
- `module-83-tools-of-the-trade/section-83.4.html` line 149: "Whether this trend extends or saturates is the open research question **Part XII** discusses."

### P2. Module-67 chapter-title identity mismatch + stale breadcrumb chapter labels

The chapter is consistently called either "From Idea to MVP" (part-14 index, module-67/index.html h1, module-67/index.html title) or "Ideation: Finding LLM-Worthy Problems" (most section-67.N.html breadcrumbs). It cannot be both:
- `module-67/index.html` line 8: title "Chapter 67: From Idea to MVP".
- `module-67/index.html` line 23: h1 "From Idea to MVP".
- `module-67/index.html` line 28: pagefind meta `chapter:Chapter 67: From Idea to MVP`.
- `section-67.1.html` line 23, 27: `Chapter 67: Ideation: Finding LLM-Worthy Problems`. Same in 67.2 and 67.3.

But for sections 67.4 through 67.15 the breadcrumb label is STILL the pre-merge chapter title from a different former chapter:
- 67.4, 67.5, 67.6 breadcrumbs: `Chapter 64: LLM Product Management` (line 23 / line 27 each).
- 67.7, 67.8 breadcrumbs: `Chapter 65: LLM Strategy & Use Case Prioritization`.
- 67.9, 67.10, 67.11, 67.12, 67.13, 67.14, 67.15 breadcrumbs: `Chapter 68: From Idea to Product Hypothesis`.

Wave 17g rebuilt prev/next/up navs but did not touch the breadcrumb `data-pagefind-meta="chapter"` chapter labels in section files. As a result pagefind search results inside module-67 show four different chapter names for what is one chapter.

### P2. Module-78 chapter-label drift in section breadcrumbs

Same pattern. The chapter is "Manufacturing, Creative Industries, Search & Recommendation" (line 22 of module-78/index.html). Section breadcrumbs still carry pre-merge titles:
- 78.1, 78.2, 78.3, 78.4, 78.5: `Chapter 78: LLMs in Manufacturing & Supply Chain` (the original yaml chapter title — close, but not the merged title).
- 78.6, 78.7: `Chapter 79: LLMs in Creative Industries` (the former Chapter 79 that got merged in).
- 78.8, 78.9, 78.10: `Chapter 80: LLM-Powered Recommendation & Search` (the former Chapter 80 that also got merged in).

Three different chapter numbers in pagefind for what is one chapter.

### P2. Module-67/index.html "What Comes Next" still mislabeled

Line 114: "In the next section, [Section 67.1: Ideation], we get to work on the chapter's first concrete topic. After this chapter you continue to [Chapter 67: LLM Product Management](../module-67-ideation/index.html)." The "next chapter" prose link points back at the current chapter and labels it "LLM Product Management" (which is the title of section 67.5, not a chapter). The actual next chapter is 68 (Prototyping via Vibe-Coding). Bottom chapter-nav next-link is correct; the "What Comes Next" prose is independently wrong.

### P2. Module-67 H2 numbering inconsistent across sections

Wave 17c left these unnumbered (kebab-only) — they don't conflict with any other chapter but break the deep-numbered pattern used in 67.1, 67.4, 67.5, 67.7-67.15:
- `section-67.2.html`: H2 ids 1./2./3./4./5./combining-the-heuristics (lines 33, 41, 51, 63, 71, 88 in body).
- `section-67.3.html`: H2 ids 1./2./3./4. (no 67.3.X prefix anywhere).
- `section-67.6.html`: H2 ids 1./2./3./4./5. (no 67.6.X prefix).
- `section-67.4.html`: mostly correct (67.4.1, 67.4.2, 67.4.4, 67.4.5) but the third H2 has id `risk-tiers` (line 65) and visible text `67.4.3 Risk Tiers: What Happens When the Model Is Wrong` — visible has the chapter prefix, id does not match.

### P2. Module-68 H2 numbering inconsistent

Wave 17c numbered 68.1, 68.2, 68.4 correctly but left:
- `section-68.3.html`: H2 ids `1-the-taxonomy...` / `2-the-six-tools...` / `3-the-tool-combination...` / `4-the-repo-context...` / `5-choosing-for-your-team` (lines 32-121), visible text "1. ... 2. ... 3. ... 4. ... 5. ...". No 68.3.X prefix.
- `section-68.5.html`: same 1./2./3./4. pattern.
- `section-68.6.html`: same 1./2./3./4. pattern.

### P2. Module-65 H2 numbering inconsistent

`part-13.../module-65-containers-kubernetes/`:
- `section-65.1.html`, `section-65.2.html`, `section-65.3.html`, `section-65.4.html`: each uses bare `1.` through `8.` headings with kebab IDs (no `65.X.Y` prefix anywhere). They also use "Summary" instead of the book-standard "Exercises" + "What Comes Next" closing pair.
- `section-65.5.html` alone uses `65.5.Y` correctly.

### P2. Part-14 module-67 chapter-card lists only 3 of 6 sections for chapter 68

`part-14-designing-llm-agent-products/index.html` chapter-68 card (lines 56-64) lists only sections 68.1, 68.2, 68.3. The yaml + on-disk reality is that module-68 has six sections (68.1 through 68.6). The part index undercounts the Vibe-Coding chapter by half.

### P2. Appendix A.6 is still the lifted Chapter-4 section verbatim

`appendices/appendix-a-mathematical-foundations/section-a.6.html` was NOT renumbered by Wave 17c — Wave 17c's regex requires `section-(\d+)\.(\d+)\.html` and `section-a.6.html` does not match. Result:
- Line 38: `<h2 id="4-1-2-information-theory-the-language-of-learning">4.1.2 Information Theory: The Language of Learning</h2>`. Should be `id="a-6-1-..."` and visible "A.6.1 ...".
- Lines 55, 95, 123, 145, 171, 186, 245, 250: H3 ids `4-1-2-X-...` and visible `4.1.2.X` headings. Should be A.6.X.
- Line 34: prose still says "It originated as a section of **Chapter 04** (Transformer Architecture) but was moved here". The Chapter 04 reference is doubly wrong (zero-padded; and Chapter 4 is now Decoding, not Transformer).
- Line 120: prose reference to "the magnification table in **Section 4.4**" — stale chapter, stale section.
- Line 244: caption `<strong>Code Fragment 4.1.1</strong>`. Should be A.6.X or A.6.1.
- Line 247: image src is `../../part-1-llm-building-blocks/module-03-transformer-architecture/images/fig-4.1.2-cross-entropy.png` — points to part-1 module-03 (transformer chapter), filename uses `fig-4.1.2-`. The image lives outside this appendix; if A.6 is supposed to be self-contained it needs its own image or the caption/cross-link to point at the source clearly.
- Line 248: caption `<strong>Figure 4.1.1</strong>` — stale prefix.
- Line 252: `<strong>Table a.6.1:</strong>` (lowercase a) — visible label should be `Table A.6.1` to match the book's other tables (e.g. `Table 80.4.1`).
- Lines 264, 270, 276, 282: cross-refs in the table cells say "Sec. 4.1", "Chapters 4, 8, 14", "Chapters 5, 14, 15", "Chapter 17/18" — all old-numbering for the modern Chapter 1-83 sequence.
- Line 296: `<a class="next" href="../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/index.html"><span class="nav-num">Appendix B</span><span class="nav-title">Machine Learning Essentials</span></a>` — visible label says "Appendix B Machine Learning Essentials" but Appendix B is Course Syllabi (line 296 also has a broken href that points to Chapter 0 in Part 1, not to Appendix B at all).

### P2. Appendix A index has stale cross-references and split section-list

`appendices/appendix-a-mathematical-foundations/index.html`:
- Line 43: "Six sections covering vectors and matrices ..." — claims six sections but the description below the big-picture (lines 49-56) still uses "Chapter 04", "Chapter 06", "Chapter 19", "Chapter 34" zero-padded references (book uses unpadded form everywhere else; Chapter 04 is now Decoding not Transformer; Chapter 34 is no longer Evaluation — Evaluation is now Chapter 42).
- Lines 56: "When to Use This Appendix" callout: "return here when **Chapter 04's** attention mechanism formulas feel opaque, when loss functions in **Chapter 06** need grounding, or when PEFT methods in **Chapter 19** involve matrix decompositions." All three chapter references are zero-padded; Chapter 04 is wrong (attention is in Chapter 02/03), Chapter 19 may still be PEFT.
- Line 39: pagefind meta `chapter:Appendix A` (no subtitle/colon form — minor consistency issue, other appendices use "Appendix B: Course Syllabi" pattern).
- Lines 58-90: A.1-A.5 sit in one `<ul class="sections-list">`.
- Lines 91-97: A.6 sits alone in a separate `<div class="section-grid">` with a different card style. Looks like a half-finished merge of two listings.

### P2. Appendix B figure caption + every table caption still wrong

`appendices/appendix-b-course-syllabi/index.html`:
- Line 28: `<strong>Figure C.0.1</strong>` (cycle-2 flagged) — still wrong; should be `Figure B.0.1`.
- Lines 37, 57, 87, 117, 137, 165, 180, 201: every comparison-table caption says `<strong>Table p.0.1:</strong>` / `Table p.0.2:` / ... / `Table p.0.8:`. The `p.0.X` letter prefix is gibberish (likely an older `Part X` or roman-numeral lift); should be `Table B.0.X`.
- Line 233: bottom prev nav `<span class="nav-num">Section O.4</span>` (cycle-2 flagged) — still gibberish; should be `Section 65.4`.
- Line 227: empty list item from cycle-2 — still present: `<li> for worked-through fixes to common end-of-chapter problems.</li>` (no link or anchor noun before "for").

### P2. Appendix B reading-link visible labels still use OLD chapter numbers

The hrefs are correct (Wave 17b/d updated them) but the visible link text inside table cells still uses the legacy chapter number — cycle-2 listed them all. Spot checks confirm cycle-2 #7 is unchanged:
- Line 65: visible "Chapter 1 (NLP and text representation)" → `module-01-foundations-nlp-text-representation/index.html`. Number is correct here.
- Line 66: visible "Chapter 1 (Tokenization, BPE)" → `module-01-foundations-nlp-text-representation/index.html`. Tokenization is now sections 1.5-1.7, not Chapter 1's main topic.
- Lines 67-76: most rows have the link text matching the href modulo single-digit-vs-zero-padding stylistic differences; cycle-2 found more granular drift in Track 3/4/5 rows (Wks 5-13).
- Bibliography list at line 225 still reads "Appendix A (Mathematical Foundations) and **Chapter 0** (ML & PyTorch Foundations)" — Chapter 0 reference is fine numerically.

### P2. Appendix C pagefind chapter meta + figure caption still wrong

`appendices/appendix-c-reading-pathways/index.html`:
- Line 24: `data-pagefind-meta="chapter:Chapter 0 (Section 0.1): Reading Pathways"` (cycle-2 flagged) — still pollutes pagefind result chrome.
- Line 27: `<strong>Figure D.0.1</strong>` (cycle-2 flagged) — still wrong; should be `Figure C.0.1`.
- The eight pathway lists (cycle-2 #7) still embed old chapter numbers as visible link text against new hrefs.

### P2. Capstone navigation has multiplicative-prefix corruption

`capstone/index.html`:
- Line 106: prev label text reads `Front Matter: Course Syllabi: Course Syllabi` — colon-and-repeat corruption. The href is `../appendices/appendix-b-course-syllabi/index.html`; nav-num is "Front Matter" (wrong, should be "Appendix B"); nav-title is the repeated subtitle.
- Line 108: next label text reads `Next Next Next Next Next C.1 Requirements & Deliverables` — five "Next" prefixes stacked; looks like Wave 17g ran multiple times against this file.

`capstone/requirements.html`:
- Line 552: prev label text reads `Previous Previous Previous Previous Previous Capstone: End-to-End LLM System` — five "Previous" prefixes stacked.
- Line 554: next nav-num "Appendices" without title — could be intentional but reads thinly.
- Line 31: H2 reads "C.1: Technical Requirements" — but capstone is a top-level section, not under Appendix C. The "C.1" prefix collides with Appendix C's letter.
- Lines 39, 56, 73, 91, 108, 124, 174: "Chapters: 05, 12, 13" / "Chapters: 12, 13, 14, 15" / "Chapters: 18, 19, 20" / "Chapters: 21, 22" / "Chapters: 20, 21, 22" / "Chapters: 26, 27" / "Chapters: 09, 10, 14, 19" — all zero-padded OLD chapter numbers from before the renumber. Current chapter mapping (e.g. Data prep → Chapter 1/13/16, Fine-tuning → 16/17/18, RAG → 31/32, Agents → 26-30, Deployment → 62/70, Eval → 42, Security → 47/49) differs throughout.
- Lines 141, 157, 189, 205: "Module: 26" / "Module: 25" / "Module: 27" — bare module numbers that don't map to anything coherent in the 1-83 chapter sequence.

`capstone/index.html` line 65 also uses `<span class="section-num">C.1</span>` for the requirements page link — same Appendix-C-letter collision.

### P3. Stale "Part XI" prose in Part-14 modules 70 and 71

- `module-70-shipping-products/index.html` line 41: "complete a capstone project that exercises every skill from **Part XI**". Should be Part XV (industries) or Part XIV (this part itself).
- `module-71-tools-of-the-trade/index.html` line 74: "**Part XI** surveys industries: legal, finance, healthcare, education, cyber, code, and the rest. **Chapter 70** closes **Part XI** with the per-vertical vendor map." Chapter 70 closes Part XIV, not Part XV; Part XI doesn't exist (likely meant Part XV).
- `module-79-tools-of-the-trade/index.html` line 35: "**Part XI** surveyed how LLMs are applied across industries". Should be "Part XV".
- `module-79-tools-of-the-trade/index.html` line 73: "**Part XII** (Frontiers) closes the book. Chapter 65 wraps up with the frontier-research toolbox." Should be Part XVI; chapter 65 is in Part XIII (Containers, Kubernetes).

### P3. Hero alt-text fragmentation (cycle-2 #10) still present

Spot checks confirm the alt-attribute-spills-into-figcaption defect remains in:
- `part-14-designing-llm-agent-products/module-67-ideation/index.html` line 27: `alt="... 'Ideation: Finding LLM-"` then figcaption opens `Worthy Problems', ...`.
- `part-15-applications-of-llms-across-industries/module-79-tools-of-the-trade/index.html` line 27: `alt="... 'Tools of the Trade: I"` then figcaption opens `dustry Solution Stack', ...`.
- `part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/index.html` line 26: alt-text says `LLMs in Manufacturing & Supply Chain` (stale single-domain title; doesn't reflect the post-merge chapter).
- `part-14-designing-llm-agent-products/module-68-vibe-coding/index.html`, `module-69-llm-economics/index.html`, `module-71-tools-of-the-trade/index.html`: similar pattern (truncated alt mid-word, rest in figcaption).
- `part-16-llm-agentic-ai-research-frontiers/module-83-tools-of-the-trade/index.html`: same.

### P3. Section-67.4 in-prose label/href mismatch

`section-67.4.html` line 34: "The hypothesis from **Chapter 67** is one paragraph" with href `../module-67-ideation/section-67.1.html` — the link text should read "Section 67.1" since the href points at a section, not a chapter index. Similar in Module 67 sections 67.5, 67.6 (multiple places refer to "Chapter 67" when pointing at peer sections inside chapter 67).

### P3. Section A.5 has a non-prose token "Section 0.1" in the numbered list

`appendices/appendix-a-mathematical-foundations/section-a.5.html` line 46: `<li><strong>Section 0.1</strong> updates the weights to reduce the loss (calculus, optimization).</li>`. Reads as a broken substitution — "Section 0.1" is not the intended subject (the list is enumerating forward-pass + backprop steps); the prose was probably "Gradient descent" or "The optimizer" before someone over-rewrote.

### P3. Module-80/index.html "Looking Back" links to phantom chapters

`module-80-frontier-architectures/index.html` line 36 (the prose snippet quoted in P2 above) names "Chapter 62" and "Chapter 64" — those modules exist in Part XIII (Production Engineering, Workflow Orchestration) and Part XIII (Containers), which is the wrong target. The intended targets for the "Looking Back" prose are likely chapters 81 (Theory) and 82 (AGI Trajectories), inside this same part.

### P3. Section 83.5 has no "next" chapter-nav link

`module-83-tools-of-the-trade/section-83.5.html` chapter-nav block has prev (83.4) and up (Chapter 83), but no `class="next"`. The appendices/index.html prev-nav (line 66) points back to this section, so the round-trip is broken. A "next" link to `../../appendices/index.html` (Appendices) or `../../capstone/index.html` (Capstone) would close the loop.

### P3. Module-82/index.html "capstone project" link points to wrong directory

`module-82-agi-trajectories/index.html` line 75: `<a href="../../appendices/index.html">capstone project</a>`. The capstone now lives at `/capstone/index.html`. The link text says "capstone project" but the href takes the reader to the Appendices index.

## Suggested cycle 4 actions

1. **Fix the one malformed H2 in section 80.4.** Manually replace the literal `2&gt;1. The Universal Recipe` at line 54 with `<h2 id="80-4-1-the-universal-recipe">80.4.1 The Universal Recipe</h2>` and move the misplaced `Exercises` H2 (line 144) to the end of the section. One-section fix; high visibility because it's the first heading the reader sees in that section.

2. **Fix Part-15 part-index identity** (P2). Edit `part-15-applications-of-llms-across-industries/index.html` lines 24, 26, 29, 37, 7 to use Part XV consistently and pick "seven verticals + one tools chapter" or "eight chapters" as the canonical count.

3. **Sweep "Part XII" out of Part 16 module + section files** (P2). Five occurrences: module-80/index.html (line 36), module-82/index.html (line 75), module-83/index.html (line 35), and section-83.4.html (line 149). Each needs the surrounding sentence rewritten (the prose also references chapters that don't exist).

4. **Run "rebuild breadcrumb chapter labels from canonical chapter title" pass.** The hrefs and bottom-nav numbers are correct after Wave 17g; the `<div class="page-breadcrumb">` chapter-label text and the `data-pagefind-meta="chapter:..."` injections are NOT. Script: walk every section file, read the chapter title from `module-NN/index.html` h1, and rewrite the breadcrumb chapter label + pagefind meta to match. Will close P2 for modules 67 (15 sections), 78 (10 sections), and reduce search-result chrome confusion.

5. **Rename Appendix A.6 file or expand Wave 17c regex.** Either rename `appendices/appendix-a-mathematical-foundations/section-a.6.html` to `section-A.6.html`/`section-a-6.html` and run Wave 17c with a relaxed regex (`section-[a-z0-9]+\.\d+\.html`), or hand-edit the eight H2/H3 IDs + visible numbers + the three caption labels in this one file. Also fix the next-nav block (line 296) which currently labels Chapter 0 of Part 1 as "Appendix B Machine Learning Essentials".

6. **Fix Appendix B caption letter prefixes and Section O.4 nav-num.** Single sed-style pass on `appendix-b-course-syllabi/index.html`: `Figure C.0.1` → `Figure B.0.1` (1 occurrence); `Table p.0.` → `Table B.0.` (8 occurrences); `Section O.4` → `Section 65.4` in line 233; delete the empty `<li>` on line 227.

7. **Fix Appendix C caption + pagefind meta.** Same shape: `Figure D.0.1` → `Figure C.0.1`; pagefind chapter meta `Chapter 0 (Section 0.1): Reading Pathways` → `Appendix C: Reading Pathways`.

8. **Fix capstone navigation corruption** (P2). Diff the two files against an earlier git revision to find where the `Next Next Next Next Next` and `Previous Previous Previous Previous Previous` accretion came from. Most likely Wave 17g ran multiple times without an idempotency guard. The fix is to regenerate the chapter-nav blocks from scratch using the canonical structure: prev → appendices index, up → none (capstone is top-level), next → requirements.html; on the requirements page prev → capstone index, next → appendices index. Also change the `C.1` section-prefix in capstone/index.html line 65 and capstone/requirements.html line 31 to a capstone-local identifier ("Section 1: Technical Requirements" or just "Technical Requirements"), since the C.1 letter collides with Appendix C.

9. **Renumber capstone Requirements 1-11 against the current chapter sequence** (P2). Walk every `<p><strong>Chapters: NN, NN</strong></p>` and `<p><strong>Module: NN</strong></p>` line in `capstone/requirements.html` and re-map the listed numbers to the modern part-13-through-part-16 chapter numbers (e.g. Synthetic Dataset → Chapter 1 (tokenization), 13 (Hybrid ML+LLM), 16 (Fine-tuning Fundamentals); Fine-Tuned Model → Chapters 16, 17, 18; RAG → 31, 32, 35; Agent with Tools → 26, 27, 28; Production Deployment → 62, 70; Security and Safety → 47, 49; Evaluation Suite → 42, 43, 44; ROI Analysis → 69, 70). Cycle-2 missed this; the prompt explicitly added it to cycle-3 scope.

10. **Number H2 headings consistently for modules 65, 67, 68** (P2). Sections 65.1-65.4, 67.2, 67.3, 67.6, 68.3, 68.5, 68.6 are currently using bare `1.`-`5.` headings; the rest of the audit scope uses `NN.X.Y`. Either prefix the bare ones with the chapter/section number (preferred) or strip prefixes from the numbered ones. The current half-and-half state is the worst option for navigation/search.

11. **Drop the part-overview reference to the missing Part XVI hardware chapter** (P2). Either rewrite `part-16.../index.html` lines 36-40 to describe the actual 4 chapters (Architectures, Theory, AGI Trajectories, Tools) or restore a frontier-systems-and-hardware chapter; do not leave the description claiming a chapter that does not exist.

12. **Fix the part-14 chapter-68 undercount** in `part-14-designing-llm-agent-products/index.html` lines 56-64 to list all six sections (68.1-68.6).

13. **Sweep alt-attribute fragmentation** (P3). Same pattern in 13+ files (cycle-2 #10 + cycle-3 spot checks): the alt attribute was character-limit-truncated and the remainder spilled into the figcaption. A small parser pass would reunite them; or simply rewrite each affected file's hero figure to use the part/chapter title verbatim.
