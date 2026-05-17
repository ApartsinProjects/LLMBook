# Cycle 3 Audit — Parts 9-12

Scope: Part 9 `part-9-llm-evaluation-observability/` (modules 42-46), Part 10 `part-10-llm-security-runtime-safety/` (modules 47-51), Part 11 `part-11-llm-ethics-trust-governance/` (modules 52-56), Part 12 `part-12-llm-systems-at-scale/` (modules 57-61). Read-only audit between cycle 2 (which described wholesale H2/H3 stale numbering across 58 section files, off-by-2-to-8 chapter-nav prev/next labels, three skeletal 55-line gap-fill chapters, malformed Part 9 part-index, and 13+ chapter-index meta/title mismatches) and the cycle 3 starting state after waves 17a-h landed.

## Resolved since cycle 2

- **Wave 17c (H2/H3 visible numbering)** verified clean across Parts 9-12: a programmatic scan of all 92 section files in scope (`scripts/_audit_pg3.py`) finds only 2 stragglers (sec 43.3 with one `46.3.3` H2 + one `36-3-3` anchor id; sec 47.1 with 12 H3s labelled `49.1.x` and matching `id="30-1-x"` anchors). Every other section now has H2/H3 visible labels that match the filename chapter prefix and matching anchor IDs.
- **Wave 17d (in-prose label-vs-href)** verified clean: a scan of all 92 section files for `<a href="...">Section N.M</a>` and `<a href="...">Chapter N</a>` patterns finds ZERO label-vs-href mismatches in scope. Cycle 2 issue #9 (Section 13.1/14.1/0.3/49.x mismatches in sec 42.1/47.1/50.1/52.2/53.1/60.1) fully resolved.
- **Wave 17g (chapter-nav prev/next rebuild)** verified clean: a programmatic walk (`scripts/_audit_pg3_nav2.py`) of all 20 chapter indices in scope confirms every prev/next link points at the correct neighbour chapter with matching visible label. Cycle 2 #2 (16+ chapter-nav defects including Ch 58 pointing at Part 16 Ch 83/85) is fully resolved. Ch 56, 59, 60, 61 all have proper prev/next blocks (cycle 2 said they only had "In Part" links).
- **Caption renumbering (Figure / Table / Code Fragment)** mostly resolved: only 2 section files still carry stale captions (sec 47.2 with 2 `Code Fragment 49.8.x` captions, sec 57.4 with 3 `Code Fragment 44.14.x` captions plus matching pagefind/breadcrumb chapter staleness). Cycle 2 #8 (figures stale across "most authored section bodies") is closed for the bulk of the corpus.
- **Wave 17h (content authoring)** verified for Ch 56 (Responsible AI Tools), Ch 59 (Distributed Training Systems), Ch 61 (Scale Tools): all 15 sections (5 each) are now substantive content (171-434 lines per section, real H2 numbering 56.1.x through 61.5.x, named-platform/named-paper density, KaTeX math in Ch 59, SVG diagrams, callouts, prereqs, key-insight blocks). Cycle 2 #3 (skeletal 55-line stub sections with identical 3-entry generic bibliography) is RESOLVED. Bibliography depth varies (see below for Ch 59 gap).
- **Ch 46 LLM-as-Judge section card descriptions** are no longer the cycle-2 placeholder "Promoted and expanded from old section 42.8". All five section cards (46.1-46.5) in `part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/index.html` now carry tailored, big-picture-derived descriptions. Cycle 2 #6 RESOLVED.
- **Part 9 top-level index part-label fixed**: `part-9-llm-evaluation-observability/index.html` now shows "Part IX" in `<div class="part-label">`, alt text, overview prose, big-picture, and `<title>`. The duplicate Ch 46 card with malformed `</main>` nesting is GONE. "Chapters: 5 (Chapters 42 through 46)" reads correctly. Cycle 2 #4 partly resolved (Ch 42 entry and Ch 44 entry remain broken — see below).
- **Ch 42 in-chapter index** lists sections 42.1 through 42.12 cleanly without the cycle-2 duplicate-42.9. Section descriptions are tailored per-section. Cross-section linear nav between 42.9, 42.10, 42.11, 42.12 (prev/next blocks) is correct.
- **Section 42.10 and 42.11** self-title correctly: `<title>` is "Section 42.10: Research Methodology for LLM Papers" / "Section 42.11: Structured-Output Validity Testing"; `<h1>` and `page-current` agree; visible H2 numbering inside the bodies uses 42.10.x / 42.11.x.
- **Part-label / part-prose** in Parts 10/11/12 top-level indices verified: every Part X / Part XI / Part XII label is consistent (meta, title, breadcrumb, h1, pagefind-meta).
- **Cross-section linear nav at section level** (the `<nav class="chapter-nav">` at the bottom of every section body) verified clean for the spot samples checked (sec 42.9 ↔ 42.10 ↔ 42.11 ↔ 42.12; sec 52.1 → 52.2 with Ch 51 cross-part prev; sec 54.10 → 55.1 cross-part next). The cycle 2 regression on Ch 58 (Ch 83/85 Part 16 nav) is gone — Ch 58 chapter-nav now reads Ch 57 ↔ Ch 59 correctly.

## Remaining issues (priority order)

### P1. Section 47.1 anchor-IDs and visible H3 labels both stale; internal TOC broken

- `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html` is the worst remaining file in scope. The in-page section-internal-toc at line ~50 carries anchor `href="#47-1-1"` through `href="#47-1-12"` with VISIBLE labels `30.1.1` through `30.1.12`. The 12 corresponding subsection H3s carry `id="30-1-1"` through `id="30-1-12"` with VISIBLE labels `49.1.1` through `49.1.12`. So three different chapter numbers (47, 30, 49) are simultaneously baked into one file: the section TOC's hrefs (47) point at IDs (30) that don't exist, so every in-page jump from the TOC fails. The visible labels disagree with both. New sub-subsections like `id="47-1-4-1"` are correct, which means the file was renumbered partway and the H3 sub-section numbering script never finished.
- Action: rewrite all 12 H3 elements to use `id="47-1-N"` with visible label `47.1.N`. Same operation needed for the section TOC's textual numbering.

### P1. Section 57.4 is an orphan migration: breadcrumb, pagefind, and captions all say Chapter 44

- `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html`: the section file lives correctly at `module-57-compute-planning/section-57.4.html` and is linked from the Ch 57 chapter index, but its content was migrated from old Chapter 44 and the migration only touched the filename. The page-breadcrumb anchor reads `Chapter 44: LLM Evaluation & Quality Metrics`; the pagefind chapter meta reads `chapter:Chapter 44: LLM Evaluation & Quality Metrics`; three Code Fragment captions read `Code Fragment 44.14.2a`, `44.14.3a`, `44.14.4a` (the `.14` subsection prefix is also stale — Ch 57.4 cannot have a fourteenth subsection). The file is a 2026-current piece of MaxText / KV-cache / quantization content that the pagefind index will mislabel and that a reader landing on it will see the wrong chapter for.
- Action: rewrite breadcrumb to `Chapter 57: Compute Planning & Infrastructure`; rewrite pagefind chapter meta to match; renumber the three Code Fragment captions to `57.4.X` with whatever subsection number is appropriate.

### P1. Part 9 part-index still has duplicate 42.9 entry and missing 42.10-42.12

- `part-9-llm-evaluation-observability/index.html` lines 60-61 list section 42.9 twice in the Ch 42 card: once as `42.9 OpenTelemetry for LLM Applications` (href correct) and once as `42.9 Research Methodology for LLM Papers` (visible label wrong, href ALSO points at section-42.9.html which is actually OpenTelemetry, not Research Methodology). The actual "Research Methodology" file is section-42.10.html.
- Sections 42.10, 42.11, 42.12 all exist on disk and are listed in the Ch 42 chapter index (which is correct), but they are MISSING from the part-9 part-index's Ch 42 chapter card. So readers reaching Ch 42 from the part index see only 9 sections, half of them mislabelled; readers reaching from the chapter index see all 12. Cycle 2 #4(c) only half-resolved.
- Action: rewrite the Ch 42 chapter card in the part-9 part-index to list sections 42.1-42.12 with the correct titles and hrefs from the chapter index.

### P1. Part 9 part-index Ch 44 chapter card lists only 44.4-44.7; first three section slots empty

- `part-9-llm-evaluation-observability/index.html` lines 80-85 (the Ch 44 chapter card) lists only `44.4 Post-Launch Monitoring`, `44.5 Drift Detection`, `44.6 Model-Rotation Strategy`, `44.7 Eval-as-Product`. On disk, only `section-44.4.html` through `section-44.7.html` exist; sections 44.1, 44.2, 44.3 are gone. The Ch 44 chapter index also lists only 44.4-44.7.
- Either renumber 44.4-44.7 to 44.1-44.4 (the right call, since there is nothing else in the chapter), or back-fill three new sections to occupy 44.1/44.2/44.3 (less likely given the existing 44.4-44.7 content covers the chapter scope). Cycle 2 #4(d) unchanged.
- Action: decide and propagate. The renumber path is mechanical: rename files, update all anchor IDs and visible H2 prefixes inside, update the section descriptions in chapter index and part index, update all four section-level prev/next nav blocks, and update the single Ch 43 → Ch 44 cross-chapter link.

### P1. Chapter-44 chapter index breadcrumb says "Part VIII"

- `part-9-llm-evaluation-observability/module-44-online-eval-observability/index.html` line 23: `<div class="page-breadcrumb">...<a href="../index.html">Part VIII</a>...</div>`. Every other Ch 44 part reference shows "Part IX". The pagefind-meta-injected line 27 says correctly "Chapter 44: Online Evaluation, Observability, and Production Monitoring" so search results will be fine, but the on-page breadcrumb is broken.

### P1. Chapter-index `<title>`, `<meta description>`, and breadcrumb-current still drag old chapter numbers/titles for three chapters

- **Ch 47**: `module-47-adversarial-security-red-team/index.html` line 7-8 — `<meta description>` and `<title>` both say "Chapter 47: Safety, Ethics & Regulation"; H1 correctly says "Adversarial Security and Red Teaming". Pagefind-meta is not explicitly set for chapter on this file, so search will fall back to `<title>` and surface the wrong chapter name. Cycle 2 #7 unchanged.
- **Ch 48**: `module-48-guardrails-runtime-safety/index.html` line 7-8 + line 20 (breadcrumb-current) + line 24 (pagefind-meta) ALL say "Chapter 40". H1 is correct. Off-by-8. Cycle 2 #7 unchanged.
- **Ch 54**: `module-54-watermarking-provenance/index.html` line 7-8 + line 20 + line 24 say "Chapter 46: Watermarking, Provenance, and Deepfake Defense". H1 correctly says "Provenance, Watermarking & Transparency". Both number AND title wrong. Cycle 2 #7 unchanged.

### P1. Breadcrumb chapter labels stale in 26+ section files

A programmatic scan (`scripts/_audit_pg3_breadcrumb.py`) finds 43 section files whose breadcrumb anchor `<a href="index.html">...</a>` disagrees with the canonical chapter title taken from the chapter index H1. Highlights:
- Ch 43 sections 43.1-43.5 all show `Chapter 43: Specialized Evaluation` (truncated) or `Chapter 43: Multimodal & Specialized Evaluation` (43.5) — should be the full canonical `Chapter 43: Specialized Evaluation: RAG, Agents, Multimodal, Long-Context`.
- Ch 44 sec 44.7 shows `Chapter 44: Eval Platforms & Workflows` — should be `Chapter 44: Online Evaluation, Observability, and Production Monitoring`.
- Ch 47 sec 47.1 and 47.2 show `Chapter 47: Safety, Ethics & Regulation` — should be `Chapter 47: Adversarial Security and Red Teaming`.
- Ch 52 sec 52.1 shows `Chapter 52: Bias, Fairness, and Disparate Impact`; sec 52.2 shows `Chapter 54: Hallucination and Truthfulness`. Both should be `Chapter 52: Bias, Fairness & Hallucinations`. (Cycle 2 explicitly called out the 52.2 hallucinations orphan; the breadcrumb still hasn't been retitled.)
- Ch 54 sec 54.1-54.5 show `Chapter 54: Watermarking, Provenance, and Deepfake Defense`; sec 54.6-54.10 (the transparency sections that cycle 2 said had been added to the index) show `Chapter 57: Transparency, Documentation, and Auditability`. Should all be `Chapter 54: Provenance, Watermarking & Transparency`. (The 54.6-54.10 group reveals these sections were grafted in from old Ch 57 in cycle 1; the breadcrumbs were never rewritten.)
- Ch 55 sec 55.1 shows `Chapter 55: Environmental Impact and Sustainability`; sec 55.2 shows `Chapter 59: Frontier Safety and Open Problems`. Both should be `Chapter 55: Environmental Impact & AI Governance`.
- Ch 42 sec 42.11 shows `Chapter 45: Functional Eval & Behavioral Testing`; sec 42.12 shows `Appendix B: Machine Learning Essentials`. Both should be `Chapter 42: LLM Evaluation & Quality Metrics`.
- Ch 57 sec 57.4 shows `Chapter 44: LLM Evaluation & Quality Metrics` (part of the broader 57.4 orphan-migration issue noted above).
- Ch 60 sec 60.1 shows `Chapter 60` (no title) — inconsistent with the rest-of-book pattern of `Chapter NN: Title`.

### P2. Sections in Ch 56, 59, 61 use truncated breadcrumb format

- The 15 sections in Ch 56 (`module-56-responsible-ai-tools/section-56.1.html` through `56.5`), Ch 59 (`section-59.1.html` through `59.5`), and Ch 61 (`section-61.1.html` through `61.5`) all use a breadcrumb format `Part XX > Chapter NN > Section NN.M` where the chapter link reads only `Chapter 56` / `Chapter 59` / `Chapter 61` — no chapter title. Every other section in the book uses `Chapter NN: <title>`. This is a wave-17h template oversight.
- Action: extend the breadcrumb anchor text to include the chapter title to match the rest of the book.

### P2. Section 49.3 and 49.4 `<title>` tags still say Section 49.6 and 49.7

- `module-49-agent-safety-autonomy/section-49.3.html` line 5 / `section-49.4.html` line 5 carry `<title>Section 49.6: Agentic Security Benchmarks for Tool-Using Systems</title>` and `<title>Section 49.7: Supply-Chain Security for Agent Sandboxes</title>`. The H1 and `page-current` div correctly say `Section 49.3` and `Section 49.4`. Browser tabs and search results will surface the wrong section number. Cycle 2 #1 stragglers — H2 numbering was fixed but the `<title>` element was missed.

### P2. Chapter 42 "What's Next" paragraph still self-links to "Chapter 55"

- `module-42-evaluation-foundations/index.html` line 164: `<a href="index.html">Chapter 55: LLM Evaluation & Quality Metrics</a>` — self-link with wrong chapter number and wrong chapter title (Ch 55 is Environmental Impact). Should be the canonical next chapter (Ch 43). Cycle 2 #5 partly resolved; the index-card duplicate is gone but this "What's Next" reference was never rewritten.

### P2. Cross-part prose mismatches in Tools-of-the-Trade chapters and Ch 47/49 narrative

- **Ch 45 (Eval Tools, Part IX) index** still says: "Part VIII split into two halves" (Big Picture), "Two model categories matter for Part VIII" (sec 45.4 desc), "Part VIII's literature" (sec 45.5 desc), "Part IX turns to safety, security, and ethics... Chapter 51 closes Part IX" (What Comes Next). All "Part VIII" should be "Part IX"; the What Comes Next claim is wrong on multiple axes (the next part is Part X security; Ch 51 closes Part X; ethics is Part XI). Cycle 2 #10 unchanged.
- **Ch 47 (Adversarial Security, Part X) index**: Looking Back says "Parts III-VIII built and operated LLM systems. Part IX zooms out" — should be "Parts III-IX... Part X zooms out". Chapter Overview says "production engineering foundations from Chapter 45" (Ch 45 is Tools of the Trade Eval, not foundations; production engineering core is Ch 62 in Part 13), "alignment techniques covered in Chapter 20" (Ch 18 is alignment; Ch 20 is RAG architectures), "strategic and ROI considerations in Chapter 31" (Ch 31 is Conv AI persona patterns). Big Picture and Learning Obj #2 each carry a "Chapter 20" alignment claim and a "Chapter 11" interpretability claim, both off by ~8.
- **Ch 49 (Agent Safety, Part X) index**: "Chapter 51 consolidates the Part IX safety toolchain" — should be Part X.
- **Ch 51 (Safety Tools, Part X) index**: Big Picture says "Part IX is the safety, security, and ethics part of the book" — should be Part X (ethics is Part XI). Section 51.1 desc says "Part IX's platforms". What Comes Next says "Part X turns to the product side... Chapter 71 closes Part X" — both wrong (next part is XI ethics; Ch 71 is in Part 14 which is product design).

### P2. Ch 58 narrative "What Comes Next" still references Chapter 64

- `module-58-frontier-systems-hardware/index.html` line 75: "Chapter 64 closes Part XII with the question this whole part has been building toward..." — Ch 61 closes Part XII; Ch 64 does not exist in the canonical layout (or is in Part XIII LLMOps). The cycle-2 regression on the chapter-nav was fixed (prev/next now read Ch 57 / Ch 59), but the body prose was not synchronized.

### P3. Ch 59 sections have zero bibliography entries

- All five sections in `module-59-distributed-training-systems/` (59.1 through 59.5) carry zero `bib-entry-card` divs. Cycle 2 flagged a 3-entry generic placeholder bibliography; wave 17h replaced the placeholder with no bibliography at all. Ch 56 sections carry 5-6 entries each; Ch 61 sections carry 5-6 entries each. Distributed-training-systems content cites specific papers (ZeRO, FSDP, Megatron, GSPMD, FlashAttention) inline but never collects them in a section-level References block.
- Action: append a 4-8 entry bibliography to each of 59.1-59.5.

### P3. Ch 60 sec 60.1 prereq label says "Chapter 18" but the href points at module-17-peft

- `module-60-edge-on-device-llms/section-60.1.html`: a prereq link reads `<a class="prereq-link" href="../../part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html">Chapter 18</a>` framed as "quantization fundamentals". The href is to Ch 18 (alignment), and a nearby inline anchor with the same text reads `href="../../part-4-training-adaptation/module-17-peft/index.html"`. The quantization material lives in Ch 17 PEFT; the right combination is "Chapter 17" + module-17-peft. The cycle-2 in-prose label sweep cleared most of these, but this one slipped through because the label and href both used a chapter number rather than a section number.

### P3. Sections 43.3 and 47.2 have small caption/numbering stragglers

- Sec 43.3 carries one H2 reading `46.3.3 τ-bench...` (the other H2s say 43.3.x correctly) and one matching anchor id `id="36-3-3"`.
- Sec 47.2 carries two stale captions `Code Fragment 49.8.1` and `Code Fragment 49.8.3` (the H2 numbering inside the body is correct 47.2.x).
- These are isolated stragglers; a single follow-up sweep clears both.

## Suggested cycle 4 actions

1. **Rewrite section 47.1 H3 anchor IDs and visible labels.** Twelve H3s in `part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.1.html` need `id="47-1-N"` with visible text `47.1.N` instead of the current `id="30-1-N"` + visible `49.1.N`. The internal section-TOC's hrefs already say `#47-1-N` so once the IDs match, the in-page jumps will work.

2. **Re-author section 57.4 metadata.** The migration of old Ch 44 content into Ch 57 left behind a `Chapter 44` breadcrumb, pagefind chapter meta, and three `Code Fragment 44.14.x` captions in `part-12-llm-systems-at-scale/module-57-compute-planning/section-57.4.html`. Rewrite the four staleness sites and renumber the captions to `57.4.N`.

3. **Rebuild the Part 9 part-index Ch 42 and Ch 44 chapter cards.** The Ch 42 card needs the duplicate-42.9 collapsed and sections 42.10/42.11/42.12 added (their titles can come from `module-42-evaluation-foundations/index.html` line 146-160). The Ch 44 card needs either renumber-44.4-44.7-to-44.1-44.4 (preferred) or back-fill 44.1-44.3 sections (heavier lift). The Ch 44 chapter-index breadcrumb "Part VIII" needs the matching fix.

4. **Fix the three chapter-index meta blocks** (Ch 47, 48, 54): rewrite `<meta description>`, `<title>`, the breadcrumb-current span, and the pagefind-meta-injected chapter line to match the current H1. Off-by-1 to off-by-8 staleness.

5. **Run a breadcrumb-chapter-label rebuild across the 43 section files** flagged by `scripts/_audit_pg3_breadcrumb.py`. Authoritative chapter title comes from the chapter index H1. The script is in-repo and prints a one-line-per-file diff so a follow-up sweep is mechanical.

6. **Extend the Ch 56/59/61 section breadcrumb format** from `Chapter NN` to `Chapter NN: <title>` to match every other section in the book. Single-template change applied to 15 section files.

7. **Sync three section `<title>` elements with `<h1>`/`page-current`**: section 49.3 (49.6 → 49.3), section 49.4 (49.7 → 49.4). These are cycle-2 H2-numbering stragglers in the `<title>` element rather than body H2s.

8. **Rewrite the Ch 42 "What's Next" paragraph** to point at Ch 43 with the correct title; the current self-link with text "Chapter 55: LLM Evaluation & Quality Metrics" has been there since cycle 1.

9. **Sweep cross-part prose** in Ch 45, 47, 49, 51, 58. Each carries 3-6 narrative claims about which Part covers which topic and which Chapter closes which Part; the cycle-1-and-2 renumber left these as stale prose. List of specific sentences in the "Cross-part prose mismatches" section above.

10. **Add bibliographies to Ch 59 sections.** 4-8 references per section, citing the ZeRO/FSDP/Megatron/GSPMD/FlashAttention/Pathways/DeMo/MegaBlocks papers the sections reference inline. This brings Ch 59 in line with the Ch 56 and Ch 61 reference depth.

11. **Clean up minor stragglers**: sec 43.3 one H2 (46.3.3 → 43.3.3) + anchor id (36-3-3 → 43-3-3); sec 47.2 two Code Fragment captions (49.8.1 → 47.2.x, 49.8.3 → 47.2.x); sec 60.1 prereq label "Chapter 18" → "Chapter 17" alongside fixing the duplicate-href confusion.
