# Wave 38: Master Backlog Aggregation + Sweep Pipeline

**Date:** 2026-05-17 (extended session)
**Branch:** v2.0

## Goal
User requested "read all past audit results, create TODO items, ensure all audits feed improvement waves." Result: comprehensive backlog (`MASTER_BACKLOG.md`) + 5 sub-waves of mechanical sweeps that address P0/P1 items from cycle-3, anomalous-styling, random-detector, and engagement audits.

## Sub-waves applied

| Wave | Description | Files | Replacements |
|---|---|---|---|
| 38a | Removed inflated mid-content `<nav class="chapter-nav">+<footer>` pairs (canonical nav re-inserted before `</main>`) | 25 | 60 pairs |
| 38b | Zero-padded `Chapter 0N` (and structural-element off-by-1 cases) replaced with canonical chapter number in `<title>`, `<meta>`, breadcrumb, pagefind-meta, chapter-nav up-link | 78 | 81 |
| 38c | **Canonical chapter title propagation**: extracted h1 from each module-N/index.html, propagated to all section breadcrumbs (`<a href="index.html">Chapter N: TITLE</a>`) and chapter-nav up-link nav-title | **240** | **435** |
| 38d | section-6.9 duplicate `<li>` entry removed from part-2 index | 1 | 1 |
| 38e | Stripped stale `<em>N.M.K ` numeric prefixes from comparison-table titles (e.g., `<em>1.3 Activation Functions ` → `<em>Activation Functions `) | 14 | 14 |
| **Total** | | **357 unique files** | **591 fixes** |

## Stale audit findings filtered (no-op needed)

Verified that 6 cycle-3 / anomalous-styling claims are already resolved by earlier waves:

| Claim | Reality | Already fixed by |
|---|---|---|
| 526 `<strong><strong>` opening double-strong in 108 files | 0 actually present | Wave 33d closing sweep + earlier opening sweeps |
| 15 uppercase pagefind-meta variants (P:, R:, T:) | 0 found | Wave 33c (35 lowercase variants caught) |
| Ch 48 chapter-index title says "Chapter 40" (off-by-8) | Actually correctly "Chapter 48" | Earlier waves |
| Ch 54 chapter-index title says "Chapter 46" (off-by-8) | Actually correctly "Chapter 54" | Earlier waves |
| section-17.X.html files still link to "PEFT" old title | Title is already canonical "Parameter-Efficient Fine-Tuning, Distillation & Model Merging" | Wave 16 |
| Ch 20/21/22/24 256 H2 headings with bare `1, 2, 3` numbering | Actually canonical `N.M.K` form | Wave 17c |
| section-37.3:499 nested `<strong><strong>` | Already fixed | Wave 33d |

## Audit ingestion summary

14 audit reports digested (~700 KB combined) by 4 parallel agents:
- `REMEDIATION-PLAN.md` (cycle-1 plan): Waves 11-15 done, Wave 16-17 partial, Wave 19 deferred
- `wave23_callouts.md`: 5 content agents handled (~80 callouts)
- `wave25_diagrams.md`: SVG re-skin deferred (Ch 41/56/61 tile-maps)
- `wave26_depth.md`: math callouts landed in 4 chapters
- `wave28_content_issues.md`: 17/40 items addressed; rest = authoring
- `wave31_32_engagement_why.md`: most addressed via content agents
- `comic_illustration_audit.md`: 13/53 done; 40 backlog
- `bibliography_hallucination_audit.md`: 7 corrections applied (Wave 33)
- `hallucination_audit.md`: 2 HIGH errors corrected (Ch 56, Ch 61.3)
- `real_world_scenario_template_audit.md`: 312 callouts need extended-canonical sweep
- `random_detector_findings.md`: ~half addressed (Wave 38a/b/c); rest = authoring
- `library_shortcut_opportunities.md`: 59 opportunities open
- `anomalous_styling_audit.md`: partially addressed; ~20 P2 polish items remain
- `repo_reusable_assets_audit.md`: 76 obsolete scripts archived
- `missing-images.md`: 37 hero images generated, 57 wired
- `split_candidates.md`: 3 Tier-1 awaiting user approval

`cycle-2/part-group-*.md` (4 files): superseded by cycle-3.
`cycle-3/part-group-*.md` (4 files): digested, 6 stale claims filtered, 60+ real findings actioned.

## Master backlog state

`docs/content-audit/MASTER_BACKLOG.md` lists **120 items**:
- ✅ **38 P0/P1 SWEEPABLE**: completed in Waves 33-38
- 📋 **29 P0/P1 AUTHORING**: open (split big sections, fill missing bibs/big-pictures, library-shortcuts, RWS template normalization, Wave 14 Ch 41 content rewrite)
- 📋 **12 DECISIONS**: await user input (section splits, tools-template policy, industry-chapter scope)
- 📋 **~40 P2/P3 polish**: deferred

## What's open for next round

### Sweepable but author-decision-dependent
- 312 Real-World Scenario callouts → extended 8-field canonical (need 4 missing fields per callout authored)
- 8 giant sections (40.1, 50.1, 52.1, 19.2, 37.3, 3.1, 3.3, 47.1) → user approval on split scope
- 5 consolidation pairs (27.5↔32.2, 26.6↔37.3, 24.6↔24.13, 35.2↔35.3, 29.1↔29.4) → decision required

### Pure authoring
- 200+ section epigraphs (new chapters)
- 213 self-check Q&A pairs
- 13 chapters with 0% bibliography (Ch 24, 25, 34, 36, 41, 46, 51, 56, 61, 69, 71, 79)
- 67 missing big-pictures in industry chapters (Ch 71-79)
- 59 library-shortcut callouts (Ch 34/35/36/41/46/56/59/61)
- Wave 14 deferred: Ch 41 sections 41.1-41.5 still contain RAG content, need ConvAI rewrite
- 40 remaining comic / mental-map illustrations from `comic_illustration_audit.md`

## Plugin harness final state

85 active plugin checks under `agents/book-skills/scripts/audit/checks/` (Wave 33's 3 + Wave 34's 5 + Wave 35's 5 + Wave 36's 2 = 15 new checks built this session, on top of 70 pre-existing).

## Hold v2.0
Branch contains all fixes; not merged to main. Production stays tagged `production-v1.0`.
