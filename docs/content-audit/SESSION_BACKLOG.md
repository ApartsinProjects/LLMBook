# Comprehensive Session Backlog

Every user request from this session, mapped to status and target wave.

## Legend
- ✅ Done
- 🔄 In flight (agent / script running)
- 📋 Backlog (queued, not yet started)
- ❓ Awaiting decision

---

## A. Structural restructure (waves 1–17, earlier turns)
- ✅ A1. Waves 1–10 restructure (16 parts, 82 chapters, 425 sections, 3 appendices)
- ✅ A2. Wave 9 step F (drop Apx B redundancy, B.4 → Ch 42)
- ✅ A3. Content quality cycle 1 (4 audit agents, 2,277 lines findings)
- ✅ A4. Waves 11–17 cycle-1 remediation (mechanical sweeps, structural moves)
- ✅ A5. Waves 17a–O cycle-2 remediation (~30 commits)
- ✅ A6. Cycle 3 audit reports (4 agents, parts 1-4 / 5-8 / 9-12 / 13-16)
- ✅ A7. Wave 17M (parts 9-12 sync), Wave 17N (bare-H2 numbering), Wave 17O (in-prose chapter remap)
- ✅ A8. Wave 17i (5 consolidation candidates resolved)
- ✅ A9. Wave 19 (Front Matter deep pass)
- ✅ A10. Wave 20 (typography + callout + code-block unification)
- ✅ A11. Wave 21 (66 epigraphs converted to AI-Agent style)
- ✅ A12. Wave 22 (math + bibliography root-cause for Part 5 modules 21+22)
- ✅ A13. Wave 27 (double-prefix H2 + table-caption Figure→Table)
- ✅ A14. Wave 28 (bold-bleed root cause, 1,508 unmatched `<strong><strong>`)
- ✅ A15. Wave 29 (h2-section→callout standardization, 39 fixes)
- ✅ A16. Wave 30 (math-as-code root cause fix; 24.3.2 caught + fixed)
- ✅ A17. Wave 31 (appendix linear list; 81.1 inline math; 1,306 `\$NUM` → `&#36;NUM`)

## B. Index + analysis infrastructure
- ✅ B1. Content index built (`book_content_index.jsonl`, 554 records, refreshed)
- ✅ B2. ~36 `_audit_*.py` detector scripts inventoried in `scripts/`
- ✅ B3. **75+ additional detect/fix scripts** found in `agents/book-skills/scripts/{audit,detect,fix}/` (newly discovered this turn)

## C. Audit reports landed
- ✅ C1. Wave 24 (callout opportunities, 2 fake callouts found)
- ✅ C2. Wave 25 (diagram quality, 10 off-palette SVGs, Ch 36 zero diagrams)
- ✅ C3. Wave 26 (scientific/technical depth — Ch 59 publication-grade; tools chapters miss math foundations)
- ✅ C4. Wave 28 (content issues via index — §19.2 outlier, 3 dups, 17 under-built sections)
- ✅ C5. Wave 31+32 (engagement / "why" audit — Ch 36 driest; Ch 56 = buyer's guide)

## D. Audits running (this turn)
- 🔄 D1. Random detector loop (40 iterations, picks random pages, generalizes patterns)
- 🔄 D2. Bibliography hallucination check (URL + author/year/venue verification)
- 🔄 D3. Real-world-scenario template + cross-ref audit (Who/Situation/Result/Lesson conformance)
- 🔄 D4. Content hallucination + repo-reusable-assets audit (fact-check + 46-agent inventory)

## E. Audits to launch (this turn)
- 📋 E1. **Comic illustration / analogy / fun-image audit** for new chapters (sister of Wave 31+32 but more focused on visual humor)
- 📋 E2. **Image compression audit** (existing `_compress_book_images.py` — run and verify)
- 📋 E3. **Anomalous styling/typesetting audit** (check all pages against template)
- 📋 E4. **Library shortcut scouting** for new chapters — propose advanced-but-mainstream libraries to add

## F. Fix sweeps awaiting agent reports
- 📋 F1. Apply Wave 24 callout opportunities (Ch 34 + Ch 46 — add 3-5 callouts each)
- 📋 F2. Apply Wave 25 diagram redraws (10 tile-map SVGs → book palette; Ch 36 needs 5 diagrams)
- 📋 F3. Apply Wave 26 depth fixes (NDCG/MRR primer, fairness math + Kleinberg, FP8 numerics)
- 📋 F4. Apply Wave 28 content fixes (§19.2 split decision, 3 dup resolutions, 17 under-built section expansion)
- 📋 F5. Apply Wave 31+32 engagement fixes (Ch 36 fun-notes, Ch 56 history, Ch 59 illustrations)
- 📋 F6. Cross-reference opportunity sweep (from running agent D3)
- 📋 F7. Real-world-scenario template propagation (from running agent D3)
- 📋 F8. Random-detector pattern auto-fixers (from running agent D1)

## G. Image generation (gemini)
- ❓ G1. **37 missing hero images** (8 part landings + 29 chapter landings) — cataloged in `missing-images.md`
- 📋 G2. After G1: 10 tile-map SVGs need re-skin
- 📋 G3. After G1: Ch 36 needs 5 diagrams; Ch 59.5 needs re-skin

## H. Content authoring waves (defer)
- 📋 H1. Ch 36/41/56/61 depth callouts (math foundations from Wave 26)
- 📋 H2. Ch 36 engagement (fun-notes, mental-maps from Wave 31+32)
- 📋 H3. Ch 56 history + impossibility-theorem callouts
- 📋 H4. New cross-field-connection callouts across new chapters

## I. Style policy decisions (awaiting user input)
- ❓ I1. Callout title strictness (1,394 descriptive titles — intentional or violate?)
- ❓ I2. Comic illustration density target (1 per section? 1 per chapter?)
- ❓ I3. Math notation strictness (when to escape literal $ vs use math mode)

## J. Other / housekeeping
- 📋 J1. Audit 225 files with h1→h3 heading-level skips (mostly appendix sections)
- 📋 J2. §19.2 over-content (317KB / 14k words) — split decision
- 📋 J3. Part 15 industry chapters thin (~10KB avg, 0% images) — design decision
- 📋 J4. Branch v2.0: hold until user signals ready to merge to main

## Triggered this turn (need fresh wave numbers)
- ✅ T1. Section 76.1 inline math fix (Wave 31)
- ✅ T2. Appendix partition dropped (Wave 31)
- ✅ T3. Math-as-code detector built + 24.3.2 fixed (Wave 30)
- ✅ T4. Missing-image catalog (`docs/content-audit/missing-images.md`)
- ✅ T5. Cross-reference opportunities audit (D3 done; 233 candidates catalogued in `real_world_scenario_template_audit.md`)
- ✅ T6. Bibliography hallucination check (D2 done; 4 high-conf + LangGraph URL fixed in Wave 33)
- ✅ T7. Hallucination check new pages (D4 done; 2 HIGH fixed in Wave 33: Ch 56 NeMo author, Ch 61.3 Llama-3 mix)
- ✅ T8. Image compression done (92/139 images, 16.1 MB saved earlier this session)
- ✅ T9. Anomalous styling/typesetting audit done (80 anomalies catalogued)
- ✅ T10. Library shortcut scouting done (59 opportunities catalogued)
- ✅ T11. Comic illustration audit done (53 comic + 41 analogy + 12 mental-map + 14 epigraph slots)
- ✅ T12. **Open Questions callout** — research-frontier exists, fits perfectly. No new callout needed.

## Wave 33 (this turn) — Plugin-driven fix sweep
- ✅ W33-a. Plugin runner wrapper built (`scripts/run_book_audit.py`); 70 existing + 3 new plugins = 73 checks
- ✅ W33-b. SKIP_DIRS tightened (`KDP`, `source_fix_backups`, `.book-update`, `docs`, `scripts`, `.claude`)
- ✅ W33-c. New plugin: `p1_legacy_bibliography.py` (detects pre-v9 bib format)
- ✅ W33-d. New plugin: `p1_duplicate_bib_block.py` (detects "double header" pattern user reported)
- ✅ W33-e. New plugin: `p2_pseudo_callout.py` (detects callout-mimicking bare HTML)
- ✅ W33-f. Plugin bug fix: `p1_missing_meta_desc.py` attribute-order (saves 544 false positives)
- ✅ W33-1. Consolidate 101 `key-takeaway` callouts → `key-insight` (user's 82.1 concern; canonical per plugin)
- ✅ W33-2. Convert 20 legacy bibliography blocks → canonical `<details class="bibliography-collapsible">` (both `<ul class="bibliography">` and `<section class="bibliography"><ol>` variants)
- ✅ W33-3. Fix 35 corrupted `pagefind-meta-injected` spans (Ch 42-46 search index was broken; `b:`/`c:`/`d:`/`f:` patterns)
- ✅ W33-4. Fix 245 `</strong>:</strong>` double-close caption patterns (161 files)
- ✅ W33-5. 7 bibliography hallucinations fixed:
  - 26.6: swapped arXiv IDs 2310.08560 ↔ 2402.01032 (Zhang memory survey ↔ MemGPT)
  - 26.6: dead `docs.langgraph.dev` → `langchain-ai.github.io/langgraph/concepts/persistence/`
  - 29.1: removed fabricated Devin arXiv (was DynaSaur); now Cognition blog
  - 29.1: removed fabricated Cursor arXiv (was MLGym); now product page
  - 35.3: Leiden arXiv ID 1810.00826 (GIN paper) → 1810.08473 (correct)
  - 56.1: NeMo Guardrails author Rauber → Rebedea et al. (real lead author + real arXiv 2310.10501)
  - 61.3: Llama-3 mix swap: "25% code, 17% multilingual, 8% math" → "25% math/reasoning, 17% code, 8% multilingual"
- ✅ W33-6. section-1.1 Figure 1.1.3 duplicate caption removed
- 📋 W33-7. SVG_TITLE_TEXT (35 P0) — per-file investigation, heuristic flags legit labels
- 📋 W33-8. DUP_FIGURE_NUM (26 P0) — most are chapter-renumber artifacts, needs per-file review
- 📋 W33-9. SECTION_ORDER (586 P1) + FIGURE_SEQUENCE (455 P1) — likely false positives from canonical-order drift; review plugins
- 📋 W33-10. 233 cross-reference link insertions — authoring work
- 📋 W33-11. Real-World Scenario template strictness decision — needs user input
- 📋 W33-12. 14 missing epigraphs + 53 comic illustrations + 59 library shortcuts — authoring work
- 📋 W33-13. 37 hero images via gemini-imagegen batch — needs API key

**Issue count progression:** 12,280 (raw) → 2,783 (SKIP_DIRS clean) → 2,240 (plugin fix) → 2,087 (after Wave 33 sweeps). Detailed report: `docs/content-audit/WAVE_33_FIXES_SUMMARY.md`.

## Wave 34 (this turn) — Structure standardization sweep (16-item user request)

User asked for canonical chapter/part/section/callout/table/footer-nav/code structure. Built 5 new plugins, fixed 3 plugin bugs, applied 7 fix sweeps.

- ✅ W34-discover. Canonical patterns confirmed: self-check (quiz-question + details>Show Answer), callout icons via CSS ::before, callout tooltips via CSS ::after, big-picture-first order (76% dominant), chapter-nav 3-block prev/up/next, footer inside main (518/543 files), table caption ABOVE table.
- ✅ W34-plugins. 5 new plugin checks: SELFCHECK_NON_CANONICAL, BIG_PICTURE_EXCESS_BOLD, OFFTOPIC_NO_LLM_CONTEXT, CHAPTER_NAV_INCOMPLETE, WHATS_NEXT_NO_LINK.
- ✅ W34-bugs. Plugin bugs fixed: SECTION_ORDER had wrong canonical direction (saved 168 false positives), bibliography-end detection ignored <details>/<section> wrappers (saved 40+), BIG_PICTURE bold-percent counted HTML tag content, OFFTOPIC bridge-terms list expanded.
- ✅ W34-1. section-23.1 user-pointed fixes: big-picture de-bolded + LLM/Agent framing paragraph added + self-check converted to canonical with 4 authored answers.
- ✅ W34-2. 185 What's Next blocks auto-linked to next section (with title from target h1) in 183 files.
- ✅ W34-3. 67 Big Picture full-paragraph `<strong>` wrappings unwrapped (typography fix; key-term `<strong>` inside preserved).
- ✅ W34-4. 45 files prereq+big-picture swapped to canonical order; then 44 corrupted nesting fixes after non-greedy regex bug.
- ✅ W34-5. 72 unused vendor tags removed (48 KaTeX + 24 Prism) from 26 pages with no math / no code.
- ✅ W34-6. 69 footer-placement fixes (44 footer-inside-main + 25 nav+footer-inside-main); all FOOTER_PLACEMENT now 0.
- ✅ W34-7. 76 obsolete wave-scripts archived to `scripts/_archive/` (scripts/ went 311→236).
- 📋 W34-8. CHAPTER_STARTER (106) — 55 chapter indexes missing Learning Objectives, 51 missing Chapter Overview. Authoring.
- 📋 W34-9. FIGURE_SEQUENCE (455) + DUP_FIGURE_NUM (26 P0) + CODE_FRAG_NUM (18) — chapter-renumber drift, per-file fix.
- 📋 W34-10. SELFCHECK_NON_CANONICAL (213) — needs authored answers for 96 `<ol>` form + 32 quiz-question without answers.
- 📋 W34-11. FM4_PROMISE (151) + SECTION_STRUCTURE (312 P2) — chapter-feature authoring.

**Issue count progression (cumulative across Wave 33 + 34):** 12,280 → 2,783 → 2,087 → 1,743. **Net: 86% reduction.** Detailed report: `docs/content-audit/WAVE_34_FIXES_SUMMARY.md`.

## Wave 35 (this turn) — GA install + 5 new validators + section-40.1 split investigation

- ✅ W35-ga. Google Analytics 4 (G-PWPHBQL2VL) installed on all 544 pages in <head> after <meta charset>
- ✅ W35-plugins. 5 new plugin checks built (now 83 total):
  - PART_INDEX_LAYOUT (40 part-index issues found)
  - CHAPTER_INDEX_LAYOUT (356 chapter-index issues)
  - SECTION_PAGE_LAYOUT (796 P2 + new P0 detectors for merged/duplicate sections)
  - IMAGE_OPPORTUNITY (516 image opportunities: 49 missing chapter heroes, 220 text-heavy sections, 247 lacking fun-note)
  - CALLOUT_NON_CANONICAL (0 issues — proves callout-type consolidation succeeded)
- ✅ W35-discovery-1. section-40.1 confirmed forcibly-merged: explicit "(merged content)" marker at line 599 + duplicate h2 numbering 40.1.1-40.1.7
- ✅ W35-discovery-2. Two MORE forcibly-merged sections detected by new validator: section-50.1 (Privacy, 50.1.1-50.1.5 duplicate), section-52.1 (Bias, 52.1.1-52.1.4 duplicate)
- ✅ W35-discovery-3. Other duplicate-h2 typos: section-0.3 (0.4.1), section-16.4 (16.4.5) - single-h2 typos
- ✅ W35-image-audit. Image opportunities catalogued (524+ open opportunities for hero/figure/fun-note generation)
- ❌ W35-gemini. GEMINI_API_KEY NOT SET in env (verified via Python os.environ). Image generation BLOCKED.
- 📋 W35-split-40.1. Section-40.1 split: recommended but not applied (changes URLs, needs user approval)
- 📋 W35-split-50.1. Section-50.1 split: recommended
- 📋 W35-split-52.1. Section-52.1 split: recommended
- 📋 W35-rws. Real-World Scenario template normalization: extended 8-field canonical decided, sweep deferred
- 📋 W35-scripts. 30+ `_audit_*.py` scripts in scripts/ remain; identify and fold useful ones into plugin harness
- 📋 W35-authoring-backlog: 200 missing section epigraphs, 199 missing whats-next, 127 missing bibliographies, 213 sections needing canonical self-check answers, 55 chapter LearningObjectives, 54 LookingBack, 54 Prerequisites blocks, 53 Chapter Overviews, 16 part whats-next, 8 part-overview, 49 chapter hero images, 247 fun-note comic opportunities

**Plugin harness now: 83 checks** in `agents/book-skills/scripts/audit/checks/`. Detailed report: `docs/content-audit/WAVE_35_FIXES_SUMMARY.md`.

## Wave 36 (this turn) — RWS decision + callout-title prefix sweep + image generation + giant-section detection

User decisions accepted:
- Real-World Scenario: extended 8-field canonical
- Callout titles: descriptive but must START with canonical type word
- Gemini key found in `.env.all`; gitignored

- ✅ W36-env. `.gitignore` updated (`.env`, `.env.*`, `**/.env*` patterns). Confirmed `.env.all` not git-tracked.
- ✅ W36-loader. `scripts/_load_env.py` built (loads 32 API keys from `.env.all` into os.environ).
- ✅ W36-plugins. 2 new plugin checks added (85 total): GIANT_SECTION, CALLOUT_TITLE_PREFIX.
- ✅ W36-callout-titles. **4,626 callout titles prefixed** with canonical type word in 411 files. Validator now reports 0 issues. Examples: "Why sort-and-blend beats ray marching" -> "Key Insight: Why sort-and-blend beats ray marching"; "A/B Testing a Prompt Rewrite" (practical-example) -> "Real-World Scenario: A/B Testing a Prompt Rewrite".
- ✅ W36-images. **37 new hero images generated via Imagen 4.0**: 8 part-landing heroes + 29 chapter-opener heroes (Kurzgesagt-meets-XKCD style). Two batches (19 + 10 after 429 rate-limit retry).
- ✅ W36-wire. **57 hero figures wired into HTML**: 49 chapter-index pages + 8 part-index pages now reference `<figure class="illustration chapter-opener|part-opener">`.
- ✅ W36-giant-detect. GIANT_SECTION plugin found 87 candidates (4 P0 + 22 P1 + 30 P2). Curated report: `docs/content-audit/split_candidates.md` (3 Tier-1 definite splits, 4 Tier-2 probable, 8 Tier-3 borderline, 15 Tier-4 tools-of-the-trade canonical pattern - not split).
- 📋 W36-split-decision. Splits await user approval: section-40.1, section-50.1, section-52.1 (Tier 1); section-19.2, section-37.3, section-3.1, section-3.3 (Tier 2).
- 📋 W36-rws-defer. RWS extended-8-field normalization: cannot author missing Problem/Dilemma/Decision/How fields for 312 callouts mechanically.

**Total session deliverables (Wave 33-36):**
- 12 audit reports landed in `docs/content-audit/`
- **85 plugin checks** in plugin harness (up from 0 active)
- ~20 fix-sweep scripts under `scripts/wave3[3-6]_*.py`
- 37 hero images + 57 HTML wirings
- 4,626 callout title prefixes
- 245 double-strong-close fixes
- 185 What's Next links added
- 67 Big Picture bold unwraps
- 101 key-takeaway -> key-insight consolidations
- 35 pagefind metadata fixes
- 7 bibliography hallucination corrections
- 20 legacy bibliography conversions to canonical
- 76 obsolete scripts archived
- Google Analytics on all 544 pages

Detailed reports: `WAVE_33_FIXES_SUMMARY.md`, `WAVE_34_FIXES_SUMMARY.md`, `WAVE_35_FIXES_SUMMARY.md`, `WAVE_36_FIXES_SUMMARY.md`, `split_candidates.md`.

## Wave 37 (this turn) — Audit-driven callout + comic remediation

User asked: read wave23_callouts/wave25_diagrams/wave26_depth reports, apply mechanical fixes, dispatch content agents per chapter.

- ✅ W37-fakecallouts. 2 confirmed fake callouts in Ch 34 converted to canonical (<div class="callout key-insight"> / <div class="callout big-picture">).
- ✅ W37-37.3. section-37.3:499 nested-strong bug verified already fixed by Wave 33d (245 double-strong-close sweep).
- ✅ W37-figref. BROKEN_FIGURE_REF = 1 hit (false positive: cross-chapter ref).
- ✅ W37-Ch34. Content agent landed 11 callouts in Ch 34 (big-picture, library-shortcut, P10 production-pattern, 2 numeric-example, pathway, whats-next, etc.).
- ✅ W37-Ch36. Content agent landed 12 math callouts (NDCG, BM25, RRF, MaxSim, Matryoshka, InfoNCE, HNSW complexity, history primer, looking-back, whats-next) + KaTeX wired into 5 sections.
- ✅ W37-Ch46. Content agent landed 21 callouts (sections 46.3 and 46.5 went from 0 to 5-6 each; Bradley-Terry, G-Eval algorithm, length-controlled win rate, multi-judge ensemble, JudgeLM distillation).
- ✅ W37-Ch56. Content agent landed 12 math callouts (Fairness Metrics Primer with demographic-parity + equalized-odds + 4/5ths rule, Kleinberg-Mullainathan-Raghavan / Chouldechova impossibility theorem, DP (epsilon, delta), SHAP Shapley + 4 axioms, Kirchenbauer green/red-list watermark, Sadasivan AI-detection impossibility, Inline Guard + Offline Eval pattern).
- ✅ W37-Ch41-59-61. Content agent landed 14 callouts (voice latency budget, Bradley-Terry, four canonical judge biases, DPO loss, McCandlish gradient noise scale, tree-vs-ring all-reduce, FP8 E4M3/E5M2 algorithm, roofline model, bisection bandwidth, Flash Attention online-softmax, thinnest training stack, $2-3M pretrain cost).
- ✅ W37-comics. 13 comic images generated via Imagen 4.0 (Ch 34 x6, 24.6, 26.6, 35.2, 37.3, 41.2 x2, 59.2) and wired into HTML as `<div class="callout fun-note">` with `<figure>` figures (8 first pass + 5 retry with correct h2 anchors).

**Wave 37 total deliverables: ~80 new callouts + 13 comic images wired = ~93 content-quality additions.**

## Wave 38 (this turn) — Master audit aggregation + mechanical sweeps

User asked: read all past audit results, create TODO items for each finding, ensure all audits feed improvement waves.

- ✅ W38-extract. 4 audit-extract agents read 14 audit reports (cycle-2/3 part-groups + real-world-scenario + random-detector + library-shortcut + anomalous-styling + comic-illustration + REMEDIATION-PLAN + wave28 + wave31_32) and produced unresolved findings list.
- ✅ W38-master. `docs/content-audit/MASTER_BACKLOG.md` written: 120 consolidated findings tagged by P0/P1/P2/P3 and SWEEP/AUTHORING/AGENT/DECISION.
- ✅ W38a. **Inflated mid-content nav-footer sweep**: 60 pairs removed from 25 files. section-19.2 lost 9, section-45.2 lost 6, section-10.6 lost 4, section-30.2 lost 3, section-14.2 lost 2, etc. The canonical nav (prev/up/next) is preserved and re-inserted just before `</main>`.
- ✅ W38b. **Chapter-label sweep**: 81 zero-padded "Chapter 0N" → "Chapter N" fixes across 78 files in `<title>`, `<meta description>`, `<span class="bc-current">`, `data-pagefind-meta="chapter:`, and chapter-nav up-link `<span class="nav-num">`.
- 📋 W38c. Module-67 breadcrumb fixes (Chapter 64/65/68 → 67) in sections 67.4-67.15 — generic sweep skipped diff>12 to avoid over-rewriting; needs targeted per-module follow-up.
- 📋 W38d. 256 H2 headings in Chs 20/21/22/24 with bare `1, 2, 3` numbering instead of `N.M.K` — needs chapter-context-aware rewriter (per-section).
- 📋 W38e. ~29 P0/P1 authoring items (split big sections, fill missing bibliographies in 13 chapters, RWS template extended-canonical sweep for 312 callouts, fill missing big-pictures in industry chapters, etc.).
- 📋 W38f. ~12 user-decision items (section splits, tools-template policy, industry-chapter scope, callout-class consolidation).

Stale audit findings already resolved (verified):
- 526 `<strong><strong>` opening double-strong claimed by cycle-3-G2 → 0 actually found (Wave 33d swept)
- Uppercase pagefind-meta variants (P:, R:, T:) claimed → 0 found (Wave 33c swept)
- Ch 48 off-by-8 "Chapter 40" claim → file actually says Chapter 48 (already correct)
- Ch 54 off-by-8 "Chapter 46" claim → file actually says Chapter 54 (already correct)
- PEFT old-title in section-17.X.html files → already renamed to new canonical
- section-37.3:499 nested-strong → already fixed by Wave 33d

**Issue-count progression including Wave 37+38:**
- After Wave 36 (plugin audit baseline): 1,579 P0+P1 issues
- After Wave 37 (callouts + comics, increases callout-density score but adds no errors): ~1,579 (callout count went UP, audit-issue count flat or slightly down)
- After Wave 38a (inflated nav cleanup): -60 structural elements
- After Wave 38b (chapter-label fixes): -81 stale-label issues

**Master backlog: `docs/content-audit/MASTER_BACKLOG.md`** — 120 items mapped to remediation waves. Decisions D1-D12 await user input.

---

## Existing reusable test/fix batteries discovered

`agents/book-skills/scripts/detect/` (31 scripts):
- audit_conformance, audit_content_coverage, audit_content_loss, audit_duplicate_images
- audit_html_quality, audit_image_links, audit_images, audit_inline_styles
- audit_print_contrast, audit_skill_genericity, audit_svg_quality
- check_broken_html, check_callouts_v2, check_lowvalue_code, check_missing_code_captions
- deep_standardization_audit
- detect_bare_tables, detect_bib_relevance, detect_broken_callouts
- detect_comparison_opportunities, detect_consecutive_math
- detect_illustration_placement, detect_illustration_relevance
- detect_missing_images, detect_small_svgs, detect_unexplained_terms
- fix_duplicate_captions
- scan_non_ai_code, scan_non_ai_v2, validate_format

`agents/book-skills/scripts/fix/` (44 scripts):
- convert_math_to_katex, fix_accessibility, fix_algorithm_styling
- fix_bibliography_format, fix_callout_h3_to_title, fix_callout_icons
- fix_caption_numbering, fix_caption_position, fix_chapter_nav
- fix_code_blocks, fix_code_language_classes, fix_cross_refs
- fix_latex_funcs, fix_manual_highlights, fix_math_blocks
- fix_merge_tip_variants, fix_meta_desc, fix_nav_chain
- fix_old_module_paths, fix_old_part_paths, fix_pathway_cards
- fix_post_whatsnext_content, fix_quiz_to_callout
- fix_remaining_broken_xrefs, fix_section_numbers_in_refs
- fix_section_ordering, fix_stacked_captions, fix_structural_html
- fix_svg_clipping, fix_svg_text_right_clip, fix_svg_titles
- fix_th_scope, fix_unclosed_callouts, fix_unclosed_p, fix_unclosed_p_tags
- fix_zero_padded_sections, wrap_comparison_tables

Plus `scripts/_compress_book_images.py` — existing image compression tool.
