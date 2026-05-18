# Wave 34: Plugin-Audit-Driven Structural Sweep

**Date:** 2026-05-17 (continued)
**Branch:** v2.0
**Predecessor:** `WAVE_33_FIXES_SUMMARY.md`

This wave responded to a 16-item user requirement: standardize chapter / part / section structure, callout icons, table appearance, footer navigation, callout consistency, off-topic chapter framing, and code quality. Five new plugin checks landed; six fix sweeps applied; one plugin bug found and corrected.

## New plugins (5)

| File | Priority | CHECK_ID | Description |
|---|---|---|---|
| `p1_self_check_canonical.py` | P1 | `SELFCHECK_NON_CANONICAL` | Self-check uses `<ol><li>` or has questions without `<details><summary>Show Answer</summary>` toggles. Canonical: `<div class="quiz-question"><strong>QN:</strong></div>` + collapsible answer per question. |
| `p2_big_picture_excess_bold.py` | P2 | `BIG_PICTURE_EXCESS_BOLD` | Big Picture paragraph is >40% `<strong>` wrapped (typography heaviness). |
| `p2_off_topic_no_llm_context.py` | P2 | `OFFTOPIC_NO_LLM_CONTEXT` | Sections (especially in multimodal / vision / 3D / specialised parts) whose Big Picture lacks any LLM/agent bridge term. Recommends adding "Why this lives in an LLM and Agents book" paragraph. |
| `p1_chapter_nav_completeness.py` | P1 | `CHAPTER_NAV_INCOMPLETE` | Section page missing `<nav class="chapter-nav">` or its prev/up/next blocks, or wrong order. |
| `p2_whats_next_missing_link.py` | P2 | `WHATS_NEXT_NO_LINK` | `<div class="whats-next">` block contains no `<a href>` to the next section. |

## Plugin bugs found and fixed

- **`p1_missing_meta_desc.py`** (Wave 33): required `name="description"` first; canonical is `content` first. Saved 544 false positives.
- **`p1_section_ordering.py`** (Wave 34): expected `prerequisites` BEFORE `big-picture`. Confirmed actual canonical (and 76% of pages) is `big-picture` BEFORE `prerequisites`. Plugin updated; 168 false positives saved.
- **`p1_section_ordering.py`** (Wave 34): bibliography-end detection counted only `<div>` depth, missing `<details>` and `<section>` wrappers. Plugin updated to detect wrapper type; 40+ false positives saved.
- **`p2_big_picture_excess_bold.py`**: word-count included HTML tag content (URLs, attributes) inflating bold percent. Fixed by stripping tags first.
- **`p2_off_topic_no_llm_context.py`**: BRIDGE_TERMS too narrow (missed "embedding", "vector", "retrieval", "judge", "guardrail" etc). Expanded; 36 false positives saved.

## Fix sweeps applied (Wave 34)

| Wave | Description | Files | Replacements |
|---|---|---|---|
| 34a | `What's Next` block auto-linked to `section-X.(Y+1).html` (with title extracted from target h1) | 183 | 185 |
| 34b | Big Picture full-paragraph `<strong>` wrapping removed (entire `<p>` content was bold; typography reads as visual yelling). Inner key-term `<strong>` preserved. | 67 | 67 |
| 34c | Prerequisites + Big Picture swap to canonical "epigraph → big-picture → prerequisites" order | 45 | 45 |
| 34d | Un-nested prereq from inside big-picture (regex from 34c was non-greedy and nested prereq into the callout) | 44 | 44 |
| 34e | Removed unused KaTeX (48 tags) and Prism (24 tags) includes on pages with no math / no code | 26 | 72 |
| 34f | Moved `<footer>` inside `<main>` (canonical: 518/543 files had it inside) | 44 | 44 |
| 34g | Moved `<nav class="chapter-nav">` AND `<footer>` inside `<main>` for files where both were outside | 25 | 25 |

## Section-23.1 targeted fix (user pointed at this page)

The user flagged three problems on `module-23-3d-generation-neural-scenes/section-23.1.html`:
- ✅ "Too much bold in big picture": entire first paragraph was wrapped in `<strong>`. Unwrapped; only the first sentence remains bold for emphasis (in the broader Wave 34b sweep).
- ✅ "Add LLM/Agent framing": added a "Why this lives in an LLM and agents book" paragraph linking 3DGS to multimodal LLMs (Ch 24 VLA models), embodied agents, world-model agents (Section 41.4), and Chapter 1 gradient descent.
- ✅ "Self-check is not standard": migrated from `<ol><li>` list of 4 unanswered questions to canonical `<div class="quiz-question"><strong>QN:</strong></div>` + `<details><summary>Show Answer</summary><div class="answer">...</div></details>` form. All four answers authored with domain-correct content (sort-vs-march math, COLMAP init, SH degree memory, clone-vs-split adaptive density).

## Scripts directory cleanup

| Before | After | Archived |
|---|---|---|
| 311 | 236 | 76 |

Moved to `scripts/_archive/`:
- 60+ Wave * scripts (`wave1` through `wave32_*`, completed one-shots)
- 4 `_appendix_reshuffle_v*.py`
- 12 `_migration_step*.py` (v9 restructure migration steps)

## Audit-issue count progression (Wave 33 + 34)

| Stage | Total | Notes |
|---|---|---|
| Raw (no skip dirs) | 12,280 | included KDP backups, .claude demos |
| Real baseline (clean SKIP) | 2,783 | after fixing SKIP_DIRS |
| After Wave 33 sweeps | 2,087 | bibliography + key-takeaway + hallucinations + double-strong + pagefind metadata |
| After plugin bug fixes (Wave 34) | 1,884 | 168 false positives eliminated (prereq direction) |
| After Wave 34 sweeps (vendor, footer) | 1,743 | What's Next, Big Picture bold, prereq order, vendor cleanup, footer placement |
| After CAPTION_MISALIGN plugin fix | 1,582 | 161 false positives eliminated (caption attaches to preceding code, not following) |
| **FINAL (after all Wave 34)** | **1,579** | callout-after-bibliography sweep, additional cleanups |

**Net reduction:** 12,280 → 1,579 = **87% reduction** in audit-detected issues over the two waves.

## What remains (top 10 by category)

### Authoring (not script-fixable)
- **FIGURE_SEQUENCE (455)**: figure/code-fragment numbers out of order or duplicated; many are chapter-renumber artifacts from the v9 restructure (e.g. section-3.1 has captions labeled "Code Fragment 4.1.5"). Per-section investigation.
- **SECTION_STRUCTURE (312 P2)**: missing epigraphs (~200 sections in new chapters), missing What's Next, missing key-insight summary. 14 specific missing epigraphs catalogued in `comic_illustration_audit.md`.
- **CAPTION_MISALIGN (224)**: code captions don't sit next to their code blocks. Likely numbering-drift side effect.
- **SELFCHECK_NON_CANONICAL (213)**: needs authored answers for self-check questions (96 sections with `<ol>` form, 32 with `<div class="quiz-question">` but no answers, 85 mixed).
- **FM4_PROMISE (151)**: chapter missing a feature promised in FM.4 (e.g. exercises, real-world scenario, library shortcut).
- **CHAPTER_STARTER (106)**: 55 chapter index pages missing learning objectives; 51 missing chapter overview. Per-chapter authoring.

### P0 (mechanical, needs careful handling)
- **SVG_TITLE_TEXT (35 P0)**: SVG diagrams have a redundant `<title>` element near top duplicating the figure caption. Heuristic flags some legitimate intra-SVG labels.
- **DUP_FIGURE_NUM (26 P0)**: same figure/code-fragment number used twice in a single section. Many are chapter-renumber artifacts.

### Authoring backlog (catalogued from earlier audits)
- 233 cross-reference link insertions (Ch 36/41/56/61 highest yield)
- 53 comic-illustration / 41 analogy / 12 mental-map placement opportunities
- 59 library-shortcut callouts to add
- 14 missing epigraphs in new chapters
- 312 of 378 Real-World Scenario callouts don't follow strict Who/Situation/Result/Lesson template (open decision: strict 4-field vs extended 8-field)
- 37 missing hero images (8 part landings + 29 chapter landings, needs Gemini Imagen batch)

## Plugin inventory after Wave 34

73 + 5 = **78 plugin checks** in `agents/book-skills/scripts/audit/checks/`:
- 3 P0 (BROKEN_XREF, DUP_FIGURE_NUM, SVG_TITLE_TEXT)
- 36 P1 (structure, format, well-formedness)
- 36 P2 (style, accessibility, polish)
- 3 P3 (placement constraints, vendor paths)

## Hold v2.0

Branch contains all fixes; not merged to main. Production still tagged `production-v1.0`.
