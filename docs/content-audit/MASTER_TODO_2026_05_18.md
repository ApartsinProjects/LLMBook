# Master TODO — Audit Findings Consolidation

Last updated: 2026-05-18 session continuation.

## ✅ Completed (mechanical sweeps + plugin updates)

Tracked via git log on v2.0 (~15 checkpoint commits this session segment).

### User-reported issues resolved (chronological)
- Duplicate whats-next in section-40.1 (root cause: book.js JS wrapping confusion)
- Key Insight body opens with leading bold sentence (147 unwrapped)
- "Key Insight: Key Takeaways" double-prefix titles (153 collapsed + 150 class realigned)
- Bibliography canonicalization (21 bare-ref blocks wrapped + 4 dup-bib merged)
- Nested callouts at end of section-16.3 (5 Module-16 sections repaired)
- Module index second image duplicates opener (20 body figures removed)
- Single lab split into two callouts in section-13.5 (book.js fix; canonical .callout-title now prioritized)
- 27.1 double bibliography header (book.js fix: skip JS bib-wrap inside canonical details)
- 27.2 Algorithm bold prefix "Algorithm: Pseudocode X.Y.Z:" double-prefix (15 collapsed)
- 26.6.1 / 27.5.2 fun-fact with image (33 unwrapped to bare figures; fun-fact ≠ fun-illustration)
- 31.4b lab split (book.js fix)
- 31.4b bibliography wrong title "Chunking Frameworks & Tutorials" (book.js fix)
- 31.5 key-takeaway box: verified canonical
- 32.1 canonical-reference → See Also (17 renamed; 28 NEW See Also callouts added by agent)
- 31.2 math/pseudocode formatting (KaTeX wrapped consistently)
- Lab layout audit (17 canonical labs + 10 Hands-On Lab → Lab + 10 lab-extensions → lab-stretch)
- Key Insight vs Key Takeaway tooltip clarification + 49 key-insight-with-list reclassified
- 26.5.1 box-in-box callout (8 nested-note "Example output" → canonical code-output)
- Pathway callout dropped (47 → callout note; CSS + 4 plugins updated)
- Thesis-thread callout dropped (6 → callout key-insight; CSS + 4 plugins updated)
- Comic image gen round 4 (12 new comics generated + wired)
- 10.6 K.X.Y → 10.6.N renumbering (18 captions)
- PNG → JPEG conversion (155 images, 75 MB saved, 74% size reduction)
- Pagefind search rebuilt (41,682 words)
- 35 broken callout-titles repaired (missing </div> before <p>)
- 16 lame exercise intros removed
- See Also red-text hover → slate-gray hover; cursor:help dropped from cross-ref title
- Justified text for callout bodies (CSS)
- 49 key-insight callouts with lists → reclassified to key-takeaway (titles realigned)
- ToC/nav/xref verifier (chains repaired for all recent splits)
- Diagram improvement audit (10 keep, 2 improve, 0 delete)
- Code-sample lame audit (31 upgraded, 8 deleted, 12 files modified)
- Structural-gap fill (30 sections got epigraph/prereqs/whats-next)
- Image-reuse: 10 wirings from sibling modules
- See Also opportunities: 28 new (total now 116)
- Tools-of-trade content drift audit: identified 11 callouts that NEED_NEW_HOME (still pending; see below)
- Section header templates documented + 50 pages normalized (header-search added/removed)
- Bibliography collapsed by default (329 pages)
- 13 code-block details-wrapper unwrapped
- 3 duplicate code-output blocks removed
- 38 disconnected arrows in SVGs wired with marker-end
- 13 bare <svg> wrapped in <figure class="illustration">
- URL overflow CSS rule added (40.3.3 pattern)
- See Also callout closed-state styled like other callouts (gradient bg + colored band)
- Bibliography callout closed-state styled to match callout grid (amber gradient + chevron)
- Responsive design audit (110 lines safety-net CSS added; book was already mostly responsive)
- Repeated-content detection: 179 duplicate blocks identified, ~6300 words reduction estimated; report in REPEATED_CONTENT_AUDIT.md

### Plugin updates (canonical-set drift catchers)
- p0_dup_figure_num: surgical caption-only first-number; regex fixed for X.Y.Z.W
- p1_caption_misalignment: 40-line lookback for code-output
- p1_section_ordering: exempt tools/appendix modules
- p1_section_structure: exempt tools/appendix from epigraph; accept key-takeaway
- p1_section_page_layout: accept callout whats-next; exempt tools/appendix
- p1_self_check_canonical: balanced-div parser
- p2_callout_canonical_structure: +key-takeaway, -pathway, -thesis-thread
- p2_callout_title_prefix: tightened cross-ref → "See Also" only
- p2_consecutive_headings: skip canonical pairs (Lab Steps / Part Overview / Prereqs h3)
- p2_heading_hierarchy: skip <aside class="section-internal-toc">
- p2_lab_coverage: accept callout lab; exempt tools-of-the-trade
- p2_mixed_caption_style: disabled (intentional caption diversity)
- p3_math_rendering: &#36; entity → $ before counting delimiters
- p2_pseudo_callout: drop aside/blockquote check; lookahead canonical callout
- p2_code_no_language: accept lang-X (Pygments)
- p2_code_fragment_structure: retired "caption outside wrapper" check
- **NEW** p1_structural_violations: DUPLICATE_SINGLETON, DOUBLE_TITLE_PREFIX, KEY_INSIGHT_BOLD, INDEX_DUPLICATE_OPENER, NON_CANONICAL_BIB
- **NEW** p2_see_also_canonical: title="See Also" + ≥1 anchor link
- **NEW** p2_key_insight_vs_takeaway: list-in-insight or single-paragraph-in-takeaway
- **NEW** p2_callout_order: singleton callout sequence enforcement
- **NEW** p2_header_template: part/chapter/section template compliance
- **NEW** p2_code_fragment_structure: details-wrapped code, duplicate code-output
- **NEW** p2_nav_linear_chain: chapter-nav next pointer linearity

## ⏳ Pending / Open Items

### Content authoring (needs per-section work)
- **11 algorithm/key-insight callouts** in tools-of-the-trade modules contain unique theoretical content (e.g., section-36.3 IR metrics primer with full NDCG/MRR/MAP/BM25 formulas; section-36.1 vector-index complexity; section-36.2 RRF formula; section-36.4 ColBERT MaxSim/InfoNCE/Matryoshka; section-56.2 fairness metrics + SHAP; section-56.4 watermark detection asymptote; section-61.2 Flash Attention recurrence). User decision: migrate to appropriate main chapter OR keep with cross-ref note.
- **92 figures without figcaption** book-wide need captions (or to be unwrapped if they're decorative)
- **170 additional See Also opportunities** identified by agent but not wired this round
- **179 duplicate blocks** identified by repeated-content audit (DELETE / REWRITE / RESTRUCTURE per cluster)
- **132 CALLOUT_ORDER violations** still in flight (reordering agent making progress)
- **41.3.3-style "bulleted list with bold labels"** sections: 10 sections >20% bold density. User wants this reduced — needs per-section content decision (keep label-bold or strip).
- **Scientific depth audit**: opportunities for adding algorithms, neural architectures, processing steps to make book more scientific (dispatch agent)
- **Section headers → callout candidates**: review h2/h3 headings that should be callouts (dispatch agent)

### Decisions
- **Section-36.3 algorithm callout (IR metrics primer)**: NOT duplicated in module 42 or 43. Migrate? — User decision.
- **41 sub-h2 conversion**: which h2s like "The Emerging Open Frontier" should become callouts vs stay as section headers — User decision.
- **GIANT_SECTION (70 candidates)**: which to split — User decision per file.

### Per-file structural issues
- **4 pages had content after </footer>** — 3 fixed (wave 73); index.html intentional layout
- **18 broken image refs** in MISSING_IMG_DIMS (src="figure-32-X-X.svg" pointing to non-existent files) — need image generation or removal of refs
- **2 thesis-thread residuals** in .book-update/ archived content — out of scope
- **Production-pattern callout (36 instances)**: VERIFIED canonical, kept

### Process
- **Check-battery (regression catch)** is in place; run after each major edit: `python scripts/check_battery.py --save`
- **5 background agents** dispatched and largely completed this session segment

## Reports & Catalogues (location reference)

- `docs/content-audit/CALLOUT_CATALOGUE.md` — 20 canonical callout types (after pathway + thesis-thread drops)
- `docs/content-audit/HEADER_TEMPLATES.md` — 3 canonical page header templates
- `docs/content-audit/MASTER_BACKLOG.md` — original 120-issue audit consolidation
- `docs/content-audit/REPEATED_CONTENT_AUDIT.md` — duplicate-content reconciliation report
- `docs/content-audit/SESSION_2026_05_18_BACKLOG.md` — session backlog
- `docs/content-audit/cycle_snapshots/cycle_NN.json` — audit cycle snapshots (43+ cycles)
