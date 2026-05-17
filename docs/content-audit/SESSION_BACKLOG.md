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
- ✅ T1. Section 81.1 inline math fix (Wave 31)
- ✅ T2. Appendix partition dropped (Wave 31)
- ✅ T3. Math-as-code detector built + 24.3.2 fixed (Wave 30)
- ✅ T4. Missing-image catalog (`docs/content-audit/missing-images.md`)
- 📋 T5. Cross-reference opportunities audit (in D3)
- 📋 T6. Bibliography hallucination check (in D2)
- 📋 T7. Hallucination check new pages (in D4)
- 📋 T8. Image compression status check (E2)
- 📋 T9. Anomalous styling/typesetting audit (E3)
- 📋 T10. Library shortcut scouting (E4)
- 📋 T11. Comic illustration audit (E1)
- 📋 T12. **Open Questions callout** — research-frontier exists, fits perfectly. No new callout needed.

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
