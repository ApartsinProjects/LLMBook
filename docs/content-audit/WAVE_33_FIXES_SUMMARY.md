# Wave 33: Plugin-Driven Fix Sweep Summary

**Date:** 2026-05-17
**Branch:** v2.0

This wave built the plugin-based template validation system the user asked for,
ran it against the whole book, and applied seven sweeping fixes catalogued below.

## Plugin runner

- **Location:** `agents/book-skills/scripts/audit/run.py` (pre-existing infrastructure,
  not run against LLMBook before this session because BOOK_ROOT was hard-coded
  to `LLMCourse`).
- **Wrapper:** `scripts/run_book_audit.py` invokes the runner with the correct
  `--root` and the right `SKIP_DIRS` (KDP backups, .claude demos, docs, scripts).
- **Plugins:** 70 existing + 3 new = 73 check modules under
  `agents/book-skills/scripts/audit/checks/`.

### New plugins authored this session

| File | Priority | CHECK_ID | Description |
|---|---|---|---|
| `p1_legacy_bibliography.py` | P1 | `LEGACY_BIBLIOGRAPHY` | Detects `<h2>Bibliography</h2><ul class="bibliography">` and `<section class="bibliography"><h2>...</h2><ol>` (the legacy pre-v9 format) |
| `p1_duplicate_bib_block.py` | P1 | `DUP_BIB_BLOCK` | Detects multiple `<details class="bibliography-collapsible">` on one page or legacy `<h2>` co-existing with the canonical `<details>` |
| `p2_pseudo_callout.py` | P2 | `PSEUDO_CALLOUT` | Detects callout-like blocks using bare HTML (`<div class="note">`, `<blockquote>`, inline `<strong>Note:</strong>` prose patterns) instead of `<div class="callout TYPE">` |

### Plugin bugs fixed

- **`p1_missing_meta_desc.py`:** required `name="description"` to come first
  after `<meta`, but the canonical book template uses `<meta content="..." name="description"/>`
  (content first). Bug caused 544 false-positive "missing meta desc" reports.
  Tightened regex to accept either attribute order. Net: 544 P1 issues vanish.
- **`p1_legacy_bibliography.py` + `p1_duplicate_bib_block.py`:** initial draft
  matched `<h2|h3>` for the legacy heading, but `<h3 id="..."` *inside* a
  canonical `<details>` is a legitimate sub-category (e.g. "Statistical Methods").
  Tightened to `<h2>` only.

### Skip-dirs expanded

Added to runner's `SKIP_DIRS`:
- `KDP` (everything under KDP/build/source_fix_backups/* was producing ~9,500
  fake BROKEN_XREF reports from pre-v9 path references)
- `source_fix_backups` (defense in depth)
- `.book-update` (v9-preserved-content fragments)
- `docs` (audit reports themselves)
- `scripts` (this directory's own .html templates)
- `.claude` (math2epub demos)

## Fix sweeps applied

| Wave | Description | Files | Replacements |
|---|---|---|---|
| 33  | `<div class="callout key-takeaway">` consolidated to `key-insight` (the canonical type; `SECTION_STRUCTURE` plugin recommends this). Also updated callout-title text "Key Takeaway" / "Key Takeaways" -> "Key Insight" / "Key Insights" | 96 | 101 |
| 33b | Legacy bibliography blocks (`<h2>Bibliography</h2><ul class="bibliography">` and `<section class="bibliography"><h2>...</h2><ol>`) converted to canonical `<details class="bibliography-collapsible" open><summary><strong>Further Reading</strong></summary><section class="bibliography"><div class="bib-entry-card"><div class="bib-ref">...</div></div></section></details>`. Both legacy variants now have 0 occurrences book-wide. | 20 | 20 |
| 33c | Corrupted `<span class="pagefind-meta-injected">` chapter metadata across Ch 42, 43, 44, 45, 46 (search index was broken; chapter-search wouldn't return these pages). Pattern `b:` / `c:` / `d:` / `f:` / etc. (single-letter prefix instead of `data-pagefind-meta="chapter:Chapter NN:`). Chapter number recovered from `module-NN-...` directory name. | 35 | 35 |
| 33d | `</strong>:</strong>` double-close caption bug (figure/table/code-fragment captions). Random-detector flagged 13+ pages; full sweep found 245 occurrences in 161 files. Pattern is `<strong>Figure X.Y</strong>:</strong>` collapsed to `<strong>Figure X.Y</strong>:`. | 161 | 245 |

## Bibliography hallucination fixes (from D2 audit)

Seven high-confidence corrections to URL-vs-title mismatches:

| File | Line | Bug | Fix |
|---|---|---|---|
| `section-26.6.html` | 231 | Zhang memory survey linked to `arxiv.org/abs/2310.08560` (wrong; that's MemGPT) | now `arxiv.org/abs/2404.13501` (the actual Zhang paper) |
| `section-26.6.html` | 237 | MemGPT linked to `arxiv.org/abs/2402.01032` (wrong; that's "Repeat After Me") | now `arxiv.org/abs/2310.08560` (the actual MemGPT) |
| `section-26.6.html` | 240 | `docs.langgraph.dev` returns ECONNREFUSED (domain never existed) | now `langchain-ai.github.io/langgraph/concepts/persistence/` |
| `section-29.1.html` | 322 | Devin attributed to arXiv:2411.01747 (that ID is DynaSaur; Devin has no preprint) | now Cognition blog `cognition.ai/blog/introducing-devin` |
| `section-29.1.html` | 325 | Cursor attributed to arXiv:2502.14499 (that ID is Meta MLGym; Cursor has no preprint) | now product page `cursor.com` |
| `section-35.3.html` | 424 | Leiden paper linked to `arxiv.org/abs/1810.00826` (wrong; that's the GIN paper) | now `arxiv.org/abs/1810.08473` (correct Leiden) |
| `section-56.1.html` | 187 | NeMo Guardrails attributed to "Rauber, A., et al. (2024)" (hallucinated lead author) | now real authors Rebedea, Dinu, Sreedhar, Parisien, Cohen (2023), with real arXiv:2310.10501 |
| `section-61.3.html` | 87 | Llama-3 data mix listed as "25% code, 17% multilingual, 8% math" (code/math swapped) | now correct "25% math and reasoning, 17% code, 8% multilingual" (per Llama-3 paper 2407.21783) |

## Pre-fix vs post-fix issue count

| Stage | P0 | P1 | P2 | Total | Notes |
|---|---|---|---|---|---|
| Initial whole-book scan | 8,035 BROKEN_XREF + others | many | many | 12,280 | most BROKEN_XREF was `KDP/build/source_fix_backups` noise |
| After SKIP_DIRS tightened | 62 | 2,430 | 291 | 2,783 | real issue baseline |
| After plugin bug fixes | 62 | 1,887 | 291 | 2,240 | meta-desc plugin no longer flags 544 false positives |
| After bib + key-takeaway sweeps | 62 | 1,851 | 280 | 2,193 | LEGACY_BIBLIOGRAPHY 36 -> 0; SECTION_STRUCTURE drops from `key-takeaway` consolidations |
| **Current** | **61** | **1,748** | **278** | **2,087** | the 6 further reductions are auxiliary cleanups |

## What remains (in priority order)

### P0 / mechanical bug surface (still 61)
- **`SVG_TITLE_TEXT` (35):** SVG diagrams have a `<text>` element near the top
  that duplicates the figure caption. Fix is per-file (the heuristic flags some
  legitimate intra-SVG labels, not just title duplicates).
- **`DUP_FIGURE_NUM` (26):** Figure/Code-Fragment numbers reused on the same
  page. Many are chapter-renumber artifacts (e.g. section-3.1 has captions
  labeled `Code Fragment 4.1.5`). Needs per-file investigation.

### P1 backlog (1,748)
- **`SECTION_ORDER` (586) + `FIGURE_SEQUENCE` (455):** structural-canonical-order
  violations. Mostly post-restructure drift. Likely many false positives because
  the canonical order in this book differs slightly from the plugin's expectation.
- **`SECTION_STRUCTURE` (312 P2 + ~37 P1):** sections missing epigraphs (most
  new chapters), missing What's Next, missing key-insight, etc. 14 missing
  epigraphs catalogued by the comic-illustration audit.
- **`CAPTION_MISALIGN` (224):** code captions misaligned with code blocks. Likely
  a numbering-drift side effect.
- **`FM4_PROMISE` (151):** chapter missing a feature promised in FM.4 ("How to
  Use This Book"). Per-chapter authoring.
- **`CHAPTER_STARTER` (106):** chapter index pages missing required structural
  elements. Per-chapter authoring.

### Authoring backlog (NOT script-fixable)
- 233 cross-reference link opportunities (Ch 36/41/56/61 highest yield).
- 312 of 378 `practical-example` callouts don't follow strict Real-World Scenario
  Who/Situation/Result/Lesson template. Needs template-strictness decision
  before mass-edit (extended 8-field form is also de-facto canonical).
- 53 comic-illustration / 41 analogy / 12 mental-map placement opportunities.
- 59 library-shortcut callouts to add.
- 14 missing epigraphs in new chapters.
- 37 missing hero images (8 part landings + 29 chapter landings) - needs
  Gemini Imagen batch.

## Auditor and detector reports landed this session

All under `docs/content-audit/`:

- `SESSION_BACKLOG.md` - every user request mapped to status
- `plugin_audit_whole_book.json` - 73-plugin audit, JSON dump
- `plugin_audit_new_chapters.json` - same, restricted to 7 new chapters
- `bibliography_hallucination_audit.md` - 4 high-confidence hallucinations + suspect entries
- `hallucination_audit.md` - 2 high + 8 medium fact errors in new chapters
- `repo_reusable_assets_audit.md` - 42 book-skills agents + 70 plugin checks inventory
- `real_world_scenario_template_audit.md` - 378 practical-example callouts, 66 fully conforming
- `comic_illustration_audit.md` - 53 comic + 41 analogy + 12 mental-map + 14 epigraph slots
- `library_shortcut_opportunities.md` - 59 places to add library-shortcut callouts
- `anomalous_styling_audit.md` - 80 cross-cutting style anomalies, P0/P1/P2
- `random_detector_findings.md` - 40 random pages, 178 distinct issues, 80+ proposed validators
- `missing-images.md` - 37 barren landings + Gemini batch plan
- `WAVE_33_FIXES_SUMMARY.md` - this file

## Detector scripts proposed but not yet built

From the random-detector report, ~80 additional plugin candidates exist for
future sessions, in three families:

1. Markup well-formedness (mismatched heading tags, orphan footer/nav after
   `</main>`, double-close strong, malformed pagefind-meta)
2. Numbering and labeling drift (chapter-number from path vs caption text;
   stale `<em>` numeric prefixes in comparison-table captions; figure files
   named `figure-32-1-1.svg` on a chapter-20 page)
3. Python code-block indent rot (top-level dataclass / class bodies with
   indent loss)

## Hold v2.0

This branch contains all fixes above but is NOT merged to main. Production
remains tagged `production-v1.0`.
