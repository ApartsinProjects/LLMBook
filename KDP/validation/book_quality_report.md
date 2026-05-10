# Book Quality Report — Pre-KDP Submission Audit

**Book:** Building Conversational AI with LLMs and Agents (Fifth Edition, 2026)
**Authors:** Alexander Apartsin, Yehudit Aperstein
**Generated:** 2026-05-10
**Source tree:** `E:/Projects/BookBlogsHome/LLMBook` (473 HTML files)

---

## 1. Executive summary

| Metric                              | Before fix | After fix |
|-------------------------------------|-----------:|----------:|
| Total audit issues (all priorities) |      4,209 |     3,647 |
| P0 (BLOCKER) issues                 |        605 |        43 |
| P1 (MAJOR) issues                   |        589 |       589 |
| P2 (MINOR) issues                   |      3,010 |     3,010 |
| P3 (POLISH) issues                  |          5 |         5 |

**EPUB is currently passing structural validation** (`KDP/validation/structural_report.txt`):
946 manifest items, 443 spine entries, 8264 internal links checked with **0 broken**, 790 images present, 70.76 MB total. Royalty math: at 70 percent royalty the delivery fee is $10.61 per sale; the existing report recommends switching to the 35 percent royalty plan for an EPUB this large.

The book is structurally submittable today. Remaining issues are content-quality polish, not file-format blockers.

---

## 2. Mechanical fixes applied this run

### 2.1 Zero-padded section refs (563 broken cross-references → 0)

**Script:** `scripts/fix/fix_zero_padded_sections.py`
**Files modified:** 95 (all under `part-*/module-*/section-*.html`)
**Effect:** Replaced `section-0N.M.html` (e.g. `section-08.1.html`) with `section-N.M.html`. The targets exist without padding; padding was an artifact of an earlier batch script. After this fix the audit framework reports a single remaining `BROKEN_XREF` (a stale module slug, see Section 4 below). Raw before/after data is in `KDP/validation/_raw/audit_full.json` and `audit_after_fix.json`.

### 2.2 No other mechanical fixes were applied

Every other fix script in `scripts/fix*.py` was either:

- hardcoded to the old path `E:/Projects/LLMCourse` (would have done nothing or scanned the wrong tree), or
- non-trivial in scope (rewrites footers across 472 files, renumbers captions, restructures bibliographies) where a wrong call would damage prose, or
- targets an issue with **zero matches** in the current tree (`fix_capnum_placeholders.py`, `fix_double_bib_icon.py`, `fix_unclosed_callouts.py`).

See Section 5 for the deferred queue.

---

## 3. Issue inventory by category

All counts are **after** the zero-padding fix. Severity legend: **BLOCKER** would be rejected by KDP review or break reading; **MAJOR** degrades reader experience without causing failure; **MINOR** is polish.

### 3.1 Cross-references and links — BLOCKER level

| Check          | Count | Status |
|----------------|------:|--------|
| `BROKEN_XREF`  |     1 | 1 stale link (see 4.1) |
| TOC link check |     0 | 556 links, 0 broken (`scripts/verify_toc_links.py`) |
| EPUB internal links | 0 | 8264 checked, 0 broken |

The book's internal link graph is essentially clean.

### 3.2 Forbidden text characters — clean

| Check                        | Count | Notes |
|------------------------------|------:|-------|
| Em-dashes (U+2014) in prose  |     0 | Full sweep of 472 HTML files outside `<code>`/`<pre>` |
| Double-hyphens `--` in prose |     0 | 9 raw matches, all inside legitimate technical content (HuggingFace model paths `models--mistralai--Mistral-7B`, Mermaid graph arrows `--> respond`, vLLM CLI flags `--model=`, CSS `var(--primary)`, ASCII arrow `<--`). Context dump in `KDP/validation/_raw/double_dash_context.txt`. |

No author intervention required for `templates/README.md` rule 71 ("No em dashes or double dashes in text").

### 3.3 Bibliographies — chapter content

| Check                                            | Count | Severity |
|--------------------------------------------------|------:|----------|
| Section files missing `<section class="bibliography">` (non-appendix) | 29 | MAJOR |
| Chapter index files missing bibliography         |    31 | MAJOR |
| Section files missing What's Next                |     3 | MAJOR |
| Section files missing Key Insight callout        |     2 | MAJOR |
| Chapter index files missing Big Picture          |     7 | MAJOR |
| Bibliography position issues (after `<nav>` etc.)|    16 | MAJOR |
| Old `<ul class="bibliography">` format           |     1 | MAJOR (`part-6-agentic-ai/module-26-agent-safety-production/section-26.6.html`) |
| Old `<div class="bibliography">` format          |     1 | MAJOR (`part-8-evaluation-production/module-31-production-engineering/section-31.6.html`) |
| Duplicate bibliography sections                  |     0 | OK |
| Stray `bibliography-title` outside `<section>`   |     0 | OK |
| Duplicate callout icons (inline + CSS ::before)  |     0 | OK |

### 3.4 Bibliographies — appendices

| Check                                          | Count | Severity |
|------------------------------------------------|------:|----------|
| Appendix sections WITH bibliography            |     2 | OK |
| Appendix sections WITHOUT bibliography         |   106 | MAJOR (content) |
| Appendix sections with malformed entries       |     0 | OK |

Only `appendix-a/section-a.5.html` and `appendix-b/section-b.4.html` carry bibliographies. The author may intentionally omit them from glossaries, environment-setup, and template appendices, but the spread across 21 appendices suggests the policy was not finalised. Full list in `scripts/appendix_bibliography_report.txt`.

### 3.5 Section structure (per `templates/README.md`)

| Check                                  | Count | Severity |
|----------------------------------------|------:|----------|
| `SECTION_ORDER` (P1) elements out of canonical order | 308 | MAJOR |
| `SECTION_STRUCTURE` (P2) missing/extra blocks         | 168 | MINOR |
| `SECTION_STRUCTURE` (P1) bigger violations            |   7 | MAJOR |
| `FOOTER_PLACEMENT` (P1) footer not directly in `<main>`| 18 | MAJOR |
| Pages missing `<header class="chapter-header">`        |  1 (`index.html`) | MAJOR |
| Pages missing `<main class="content">`                  | 1 (`index.html`) | MAJOR |
| Pages missing `class="toc-link"`                        | 1 (`index.html`) | MAJOR |
| Pages missing `class="book-title-link"`                 | 1 (`index.html`) | MAJOR |
| Pages missing `<footer>` tag                            | 1 (`index.html`) | MAJOR |
| Pages missing "Fifth Edition, 2026" string in footer   | 1 (`toc.html`) | MAJOR |

`SECTION_ORDER` concentrates heavily in part 8 (module-29, 30, 31) and parts 11 (modules 36-38). 19 of the 308 hits are in `part-8/module-30-observability-monitoring/section-30.5.html` alone. These reflect blocks like Self-Check appearing after What's Next, or Big Picture being absent.

### 3.6 Callouts (per `templates/README.md` rule, 11 valid types)

| Check                                         | Count | Severity |
|-----------------------------------------------|------:|----------|
| Total callouts                                |  4,257 | OK |
| Callouts using `<p class="callout-label">` (old) | 0 | OK |
| Inline `style=` on callout                    |     0 | OK |
| Non-standard callout types                    |    28 | MINOR |

Non-standard breakdown: `pathway` (20 occurrences) is actually styled in `styles/book.css` line 1224 — **add it to `templates/README.md` as the 11th approved type**, or rebrand to `practical-example`. `numeric-example` (7) and `numerical-example` (1) appear to be a typo / outlier and could be merged into `practical-example`.

### 3.7 Figures, captions, and code fragments

| Check                            | Count | Severity |
|----------------------------------|------:|----------|
| `DUP_FIGURE_NUM` (P0)            |    41 | BLOCKER (visible duplication) |
| `FIGURE_SEQUENCE` (P1)           |    90 | MAJOR (gaps in figure numbers) |
| `CAPTION_MISALIGN` (P1)          |    95 | MAJOR |
| `BROKEN_FIGURE_REF` (P1)         |     9 | MAJOR |
| `MIXED_CAPTION_STYLE` (P2)       |   326 | MINOR |
| `MISSING_OUTPUT` (P2)            |   131 | MINOR |
| `MISSING_IMG_DIMS` (P2)          |   733 | MINOR (but slows page load and EPUB rendering) |
| `SVG_TITLE_TEXT` (P0)            |     1 | BLOCKER (`section-15.4.html` line 76) |
| `STACKED_CAPTIONS` check         |   N/A | check module currently broken (`p1_stacked_captions.py` missing required attrs) |

Worst code-fragment number duplications are in the production-engineering modules (29.x, 31.x) and `part-6/module-22/section-22.7.html` (6 dupes).

### 3.8 HTML well-formedness (source tree, before EPUB build)

| Issue type                       | Count | Files |
|----------------------------------|------:|------:|
| Orphan `</div>`                  |     ~6 | 6 |
| Unclosed `<div>` / `<section>`   |     ~5 | 4 |
| Unclosed `<strong>`              |     4 | 4 |
| Orphan `</p>`, `</h2>`, `</main>` |     5 | 5 |
| Other (literal `<j}>`, etc.)     |     1 | 1 (`part-9/module-32/section-32.2.html` line 106) |

Total: ~21 well-formedness issues across 18 files. **The EPUB build cleans these up** (final EPUB has 0 parse errors), but the source HTML should still be fixed before re-export.

### 3.9 Inline-style audit (per `templates/README.md` rule "No inline styles")

| Tag with inline `style=`         | Occurrences |
|----------------------------------|------------:|
| `<span>`                         | 289 |
| `<img>`                          | 178 |
| `<div>`                          |  64 |
| `<figcaption>`                   |  28 |
| `<td>`                           |  15 |
| `<p>`                            |   7 |
| Other (`<label>`, `<input>`, `<h2>`, `<table>`, `<caption>`, `<ol>`) | 6 |
| **Total** | **587** across 295 files |

The five worst offenders concentrate the violations:
- `front-matter/wisdom-council.html` (42 inline styles)
- `part-1/module-01/section-1.2.html` (19)
- `part-1/module-04/section-4.1.html` (19)
- `part-1/module-01/section-1.1.html` (11)
- `toc.html` (8 — these are the dark-mode toggle widget, may be intentional)

### 3.10 Accessibility

| Check                            | Count | Severity |
|----------------------------------|------:|----------|
| `MISSING_SKIP_LINK` (P2)         |   472 | MINOR (entire book lacks skip-to-content link) |
| `MISSING_TH_SCOPE` (P2)          |     9 | MINOR |
| `TABLE_NO_THEAD` (P2)            |   179 | MINOR |
| `EXT_LINK_ATTRS` (P2)            |     7 | MINOR |
| `SVG_ARIA_TRUNCATED` (P2)        |    17 | MINOR |
| `TRUNCATED_NAV` (P2)             |    12 | MINOR |

Skip-link is a P2 accessibility nicety but applies to every page. Consider one-time bulk patch.

---

## 4. Top-10 worst offender files

### 4.1 The single remaining BROKEN_XREF (P0)

`part-4-training-adapting/module-13-synthetic-data/section-13.8.html` line 22 links to `../../part-1-foundations/module-02-language-models-word-embeddings/section-2.2.html`. The actual module folder is `module-02-tokenization-subword-models`. This is a **stale slug from a chapter rename**. Author needs to confirm intended target (likely `module-02-tokenization-subword-models/section-2.2.html`).

### 4.2 Top files by total issue count

| File                                                                                       | Issues |
|--------------------------------------------------------------------------------------------|------:|
| `front-matter/section-fm.7.html`                                                          | ~46 (mostly missing img dims) |
| `front-matter/wisdom-council.html`                                                        | ~46 (inline styles + img dims) |
| `part-8/module-30-observability-monitoring/section-30.5.html`                            | 19 (SECTION_ORDER) |
| `part-1/module-02-tokenization-subword-models/section-2.3.html`                           | 9 (FIGURE_SEQUENCE) |
| `part-2/module-18-interpretability/section-18.1.html`                                     | 6+ |
| `part-2/module-18-interpretability/section-18.2.html`                                     | 6 (incl. unclosed div) |
| `appendices/appendix-j-datasets-benchmarks/section-j.3.html`                              | 14 (10 TABLE_NO_THEAD + 4 CONSECUTIVE_HEADINGS) |
| `part-7/module-27-multimodal/section-27.7.html`                                           | 9 CONSECUTIVE_HEADINGS |
| `part-6/module-22-ai-agents/section-22.7.html`                                            | 6 DUP_FIGURE_NUM |
| `part-8/module-31-production-engineering/section-31.8.html`                               | 5 DUP_FIGURE_NUM + 5 SECTION_ORDER |

### 4.3 Concentration by part

`SECTION_ORDER`, `MIXED_CAPTION_STYLE`, `INLINE_STYLE_IN_CODE` all cluster in **part-8 (Evaluation/Production)** and **part-9 (Safety/Strategy)**, suggesting those parts went through a different drafting pipeline. Part-1 shows the bulk of `MISSING_IMG_DIMS` and section-level inline styles. Front-matter and the wisdom-council page need their own mini-pass.

---

## 5. Manual review queue (deferred to human)

These items were **not** auto-fixed because they require judgement, content authoring, or destructive rewrites.

### 5.1 Content authoring required (BLOCKER for "complete" feel, not for KDP submission)

1. **Add bibliography to 31 chapter index pages** (`part-9/module-32/index.html`, etc.) and **29 section files**. Templates expect a bibliography in every section/chapter. Sources must be researched per topic.
2. **Add bibliography to 106 appendix sections.** May be intentional for glossary/setup appendices; the author should decide on a per-appendix policy and document it in `templates/README.md`.
3. **Fix the stale slug in `section-13.8.html`** (the one remaining BROKEN_XREF, see 4.1).
4. **Add 7 missing Big Picture callouts** in chapter index pages of part-1 and part-2.
5. **Add 3 missing What's Next + 2 missing Key Insight blocks** in `part-8/module-29-evaluation-observability` sections 29.5, 29.7, 29.11.

### 5.2 Structural fixes that need a careful regex pass

6. **41 duplicate code-fragment numbers (P0).** Cannot be safely auto-renumbered: the figure-references inside prose need to be updated in lockstep. `scripts/fix_caption_numbering.py` can do this but its hardcoded `BOOK_ROOT = E:/Projects/LLMCourse` would need to be patched, then run with `--dry-run` to review every change. Recommend: patch script root to use `Path(__file__).resolve().parent.parent`, dry-run, hand-review, then apply.
7. **308 SECTION_ORDER (P1) violations** in part-8 and part-11. The audit's `p1_section_ordering` check knows the expected order; a focused dry-run of `scripts/fix/fix_section_ordering.py` against just those modules is the right next step. Confirm canonical order in `templates/README.md` first.
8. **Reposition 16 misplaced bibliographies** (after `<nav>` or before What's Next). Each needs to be moved manually because content above/below may need re-ordering.
9. **Convert 1 old `<ul class="bibliography">` and 1 old `<div class="bibliography">`** to the new `<section class="bibliography">` + `<div class="bib-entry-card">` format (`part-6/module-26/section-26.6.html`, `part-8/module-31/section-31.6.html`).
10. **Patch 18 well-formedness issues** in source HTML (orphan/unclosed tags). All localized; see Section 3.8 for the file list.

### 5.3 Polish items (MAJOR/MINOR; nice to have)

11. **587 inline `style=` attributes** spread across 295 files — promote repeated patterns to `book.css` classes. Concentrate on the top-5 worst files first; they account for ~99 of the total.
12. **733 `<img>` tags missing width/height** — bulk-add via PIL inspection of actual image dimensions.
13. **472 pages missing skip-to-content accessibility link** — one regex insertion per page.
14. **179 `<table>` without `<thead>`** — bulk-add `<thead>` wrapper around the first row of header cells.
15. **326 `MIXED_CAPTION_STYLE`** — standardize on either inline `<strong>...</strong>` or external `<div class="figure-caption">`.
16. **131 `MISSING_OUTPUT`** — code blocks without expected output panes.
17. **109 `UNEXPLAINED_IMPORT`** — code that uses a library without a sentence introducing it.
18. **42 `FM4_PROMISE`** — Front-matter chapter-4 (i.e. `section-fm.4.html`) makes promises that audit can't reconcile to actual chapter content.

### 5.4 Template/style policy decisions

19. **Decide on the `pathway` callout type:** it has CSS in `book.css` (line 1224), is used 20 times, but is not in `templates/README.md`'s canonical 10/11 list. Either document it as an approved 12th type or migrate the 20 callouts to `practical-example`.
20. **Decide on `numeric-example` / `numerical-example` callouts** (7 + 1 occurrences). Likely should be `practical-example`.
21. **The `p1_stacked_captions.py` audit module is broken** ("missing PRIORITY/CHECK_ID/DESCRIPTION/run"). Quick fix: add the four module-level constants. Currently the framework warns and skips it.

---

## 6. Audit infrastructure observations

- **Most scripts in `scripts/audit/` and `scripts/audit_*.py` hardcode `E:/Projects/LLMCourse`** (the previous book name). Only `scripts/audit/run.py` accepts `--root`. Audit scripts that auto-detect via `Path(__file__).resolve().parent.parent` work today: `audit_callout_bibliography.py`, `audit_appendix_bibliographies.py`, `verify_toc_links.py`. The rest produce stale reports based on a tree that no longer exists.
- **Stale reports** in `scripts/`: `callout_audit_report.txt` (Apr 6), `html_class_audit_report.txt` (Apr 6), `hyperlink_audit_report.txt` (Apr 6), `html_wellformed_report.txt` (Apr 6), `appendix_bibliography_report.txt` (this run, Apr 6 → May 10). Recommend a one-shot pass to update the hardcoded `BOOK_ROOT` constant in all scripts to `Path(__file__).resolve().parents[N]` so they remain portable.
- **Audit framework `scripts/audit/run.py`** is the most usable and was the primary tool of this audit. It runs 64 individual check modules and supports JSON output for downstream synthesis. Re-run after every batch of fixes:
  `/c/Python314/python -m scripts.audit.run --root E:/Projects/BookBlogsHome/LLMBook --json > KDP/validation/_raw/audit_after_fix.json`

---

## 7. Files written by this audit

| Path                                                | Purpose |
|-----------------------------------------------------|---------|
| `KDP/validation/book_quality_report.md`             | This report |
| `KDP/validation/_raw/audit_full.json`               | Full audit BEFORE the zero-pad fix (4209 issues) |
| `KDP/validation/_raw/audit_after_fix.json`          | Full audit AFTER the zero-pad fix (3647 issues) |
| `KDP/validation/_raw/double_dash_context.txt`       | Context for the 9 raw `--` matches (all in code/CLI) |
| 95 modified HTML files in `part-*/module-*/`        | Zero-padding fixes from `scripts/fix/fix_zero_padded_sections.py` |

No files in `KDP/`, `scripts/`, `styles/`, `templates/`, `vendor/`, or any markdown were modified other than this report and the raw-data dumps in `KDP/validation/_raw/`.

---

## 8. KDP submission readiness

| Gate                                | Status |
|-------------------------------------|--------|
| EPUB structural validation         | **PASS** (0 errors, 0 warnings, all manifest items present, all links resolve, cover present) |
| EPUB file size (70.76 MB)          | PASS (under 650 MB KDP limit) but recommend 35 percent royalty due to delivery fee |
| EPUB metadata (title, authors, language, identifier) | PASS |
| In-book broken cross-references     | **PASS** after fix (1 stale slug remaining; needs author decision) |
| Em-dash / double-dash policy        | PASS |
| Footer / header presence            | PASS for all 470 content pages (1 root `index.html` and `toc.html` are landing pages with their own structure) |
| Bibliography coverage               | INCOMPLETE (60 chapter / 106 appendix sections without bibliographies) — content gap, not a KDP blocker |
| Callout markup conformance         | PASS (28 of 4257 are non-standard, all stylistic) |
| Code-fragment number uniqueness     | 41 dupes — visible to reader but not a submission blocker |

**Verdict:** the book can be uploaded to KDP today. The 41 duplicate code-fragment numbers and 60+ missing bibliographies are the highest-value targets for a content pass before launch.
