# Navigation Surface Alignment Audit Report

**Date:** 2026-05-19
**Branch:** v2.0
**Auditor:** `scripts/audit_nav_alignment.py`

## Context

After the a/b split-section renumbering (50 sections collapsed from
`section-X.Ya.html` + `section-X.Yb.html` into plain sequential numbers,
shifting downstream sections), four navigation surfaces needed
re-alignment with the current on-disk structure.

## On-Disk Truth

The book contains **15 parts, 78 modules (chapters), and 443 section
files** as of this audit.

| Part | Roman | Folder                                                | Ch | Sections |
|------|-------|-------------------------------------------------------|----|----------|
| 1    | I     | part-1-llm-building-blocks                            | 6  | 35       |
| 2    | II    | part-2-understanding-llms                             | 5  | 39       |
| 3    | III   | part-3-working-with-llms                              | 4  | 20       |
| 4    | IV    | part-4-training-adaptation                            | 5  | 44       |
| 5    | V     | part-5-multimodal-llms                                | 6  | 46       |
| 6    | VI    | part-6-agentic-ai                                     | 5  | 26       |
| 7    | VII   | part-7-retrieval-information-extraction-with-llms     | 6  | 34       |
| 8    | VIII  | part-8-conversational-ai-with-llms                    | 3  | 18       |
| 9    | IX    | part-9-llm-evaluation-observability                   | 5  | 33       |
| 10   | X     | part-10-llm-security-runtime-safety                   | 5  | 22       |
| 11   | XI    | part-11-llm-ethics-trust-governance                   | 6  | 25       |
| 12   | XII   | part-12-llm-systems-at-scale                          | 5  | 22       |
| 13   | XIII  | part-13-llmops-lifecycle                              | 5  | 16       |
| 14   | XIV   | part-14-applications-of-llms-across-industries        | 8  | 45       |
| 15   | XV    | part-15-llm-agentic-ai-research-frontiers             | 4  | 18       |
| Total|       |                                                       | 78 | 443      |

Note: the task spec listed 470 sections; actual on-disk count is 443
(after the renumber).

## Audit Tool

`scripts/audit_nav_alignment.py` checks the following navigation
surfaces:

1. `toc.html`
2. `appendices/appendix-b-course-syllabi/index.html`
3. `appendices/appendix-c-reading-pathways/index.html`
4. `front-matter/foreword.html`
5. `front-matter/fm-what-this-book-covers.html`
6. `front-matter/fm-who-should-read.html`
7. `front-matter/fm-how-to-use.html`
8. `front-matter/look-inside-preview.html`
9. `front-matter/about-authors.html`
10. `front-matter/copyright.html`

For each surface it runs these checks:

| Kind | What it catches |
|------|-----------------|
| STALE_AB | `section-X.Ya.html` / `Section X.Ya` / `X.Yb` labels |
| BROKEN_HREF | Relative href pointing at a file that does not exist |
| WRONG_PART_FOR_CHAPTER | Link puts a chapter under the wrong part folder |
| STALE_CHAPTER_PROSE_REF | Unlinked prose "Chapter N" where N no longer exists |
| STALE_AGGREGATE_COUNT | "N chapters across W parts" disagreeing with disk |
| STALE_PART_COUNT_WORD | "Sixteen/Fifteen/Fourteen parts" word disagreeing with 15 |
| TOC_VISIBLE_NUM_MISMATCH | TOC visible chapter label not matching href chapter |
| TOC_TITLE_MISMATCH | TOC visible title disagreeing with target `<title>` |
| TOC_PART_DATA_NUM_MISMATCH | `data-part-num` not matching `id="part-N"` |
| TOC_PART_CHAP_COUNT | "N chapters" in part header disagreeing with disk |
| TOC_PART_SECT_COUNT | "M sections" in part header disagreeing with disk |
| TOC_PART_ROMAN_MISMATCH | "Part X" roman numeral wrong for part id |

## Results

### Before fixes

**38 findings across 4 files.**

| Check kind                  | Count |
|-----------------------------|-------|
| TOC_VISIBLE_NUM_MISMATCH    | 12    |
| TOC_PART_SECT_COUNT         | 12    |
| STALE_PART_COUNT_WORD       | 6     |
| TOC_TITLE_MISMATCH          | 3     |
| TOC_PART_DATA_NUM_MISMATCH  | 2     |
| TOC_PART_CHAP_COUNT         | 1     |
| STALE_AGGREGATE_COUNT       | 1     |
| STALE_AB                    | 1     |

### After fixes

**0 findings.** All 38 issues fixed. In addition, 6 inline staleness
issues were caught by manual scan (Appendix B/C textual chapter
references that the script's prose check could not see) and fixed.

## Fixes Applied

### `toc.html`

| Line range | Change |
|------------|--------|
| 86         | Part I section count: 28 -> 35 |
| 137        | Part II section count: 34 -> 39 |
| 181        | Part III section count: 19 -> 20 |
| 218        | Part IV section count: 31 -> 44 |
| 313        | Part VI section count: 25 -> 26 |
| 357        | Part VII section count: 28 -> 34 |
| 369        | Chapter 32 title: "RAG Fundamentals" -> "Retrieval-Augmented Generation (RAG)" |
| 390        | Chapter 35 title: "Advanced RAG: Knowledge Graphs, Ingestion & Frameworks" -> "Advanced RAG" |
| 408        | Part VIII section count: 14 -> 18 |
| 437        | Part IX section count: 30 -> 33 |
| 481        | Part X section count: 18 -> 22 |
| 525        | Part XI: 5 -> 6 chapters, 23 -> 25 sections |
| 576        | Part XII section count: 20 -> 22 |
| 619        | Part XIII section count: 10 -> 16 |
| 661        | Part XIV: `data-part-num="15"` -> `"14"` |
| 669-718    | Part XIV chapter labels: 72-79 -> 67-74 (was off by +5) |
| 684        | Chapter 69 title: "LLMs in Healthcare & Biomedical" -> "LLMs in Healthcare" |
| 726        | Part XV: `data-part-num="16"` -> `"15"` |
| 734-755    | Part XV chapter labels: 80-83 -> 75-78 (was off by +5) |

### `front-matter/foreword.html`

| Line | Change |
|------|--------|
| 46   | "83 chapters across sixteen parts" -> "78 chapters across fifteen parts" |
| 52   | "walks the sixteen parts" -> "walks the fifteen parts" |

### `front-matter/fm-what-this-book-covers.html`

| Line | Change |
|------|--------|
| 16   | meta description "Sixteen parts" -> "Fifteen parts" |
| 44   | "Sixteen parts and 83 chapters" -> "Fifteen parts and 78 chapters" |
| 47   | "Parts XIV-XVI are strategy and frontier (product design...)" -> "Parts XIV-XV cover industry applications and the research frontier" |
| 49   | "The Sixteen Parts" -> "The Fifteen Parts" |
| 64   | Removed orphan duplicate "Part XIV: Designing LLM/Agent Products" entry (this product-design part was removed in v2.0) |
| 70   | "(IX-XVI) layer evaluation, safety, scale, operations, and product strategy" -> "(IX-XV) layer evaluation, safety, scale, operations, industry applications, and the research frontier" |
| 73   | Figure FM.2.1 caption: "How the sixteen parts" -> "How the fifteen parts"; "(IX-XVI)" -> "(IX-XV)"; alt-supplemental updated |

### `front-matter/fm-who-should-read.html`

| Line | Change |
|------|--------|
| 77   | "Sections 0.3 and 0.3b teach PyTorch" -> "Sections 0.3 and 0.4 teach PyTorch" |

### `front-matter/fm-how-to-use.html`

| Line | Change |
|------|--------|
| 44   | "across 83 chapters" -> "across 78 chapters" |
| 94   | "Begin at Part XIV: Designing LLM/Agent Products" -> "Begin at Chapter 13: Hybrid ML+LLM Architectures & Decision Frameworks" (linked) |

### `appendices/appendix-b-course-syllabi/index.html`

| Line | Change |
|------|--------|
| 86   | Week 13 of Track 1: "Section 70.5 (Application Architecture & Deployment)" (chapter no longer exists) -> "Chapter 62 (Production Engineering for LLM Systems)" with link |
| 227  | Week 10 of Track 5: "Chapter 67 (Ideation & Strategy)" (now is Legal LLMs) -> "Chapter 13 + Part XIV chapter for your domain" with links |
| 243  | Bottom prev nav: "Section B.4 / section-65.4.html" -> "Appendix A / appendix-a-mathematical-foundations/index.html" |

### `appendices/appendix-c-reading-pathways/index.html`

| Line | Change |
|------|--------|
| 62   | RAG Engineer step 6: "Section 70.5 (Deployment)" -> "Chapter 62 (Production Engineering)" with link |
| 115  | Researcher step 6: "Section 42.5" -> "Section 42.10" (Research Methodology for LLM Papers is actually 42.10 now; 42.5 is Evaluation-Driven Quality Gates) |
| 131  | Interpretability pathway step 6: "Section 33.7 (Mechanistic interpretability at scale)" (33 has only 4 sections; section is not there) -> "Section 10.2 (Mechanistic Interpretability)" with link |
| 141-147 | Founder/PM pathway: removed four stale references (Chapter 27 LLM Applications by Industry; Chapter 67 Strategy/PM/ROI; Chapter 67 Building LLM Products; Chapter 70 Shipping & Scaling) and replaced with Chapter 13, Part XIV index, Chapter 62 |

## Open Issues

None. All 38 script-flagged findings and 6 manually-caught stale prose
references were resolved. Re-running both `scripts/audit_nav_alignment.py`
and `python -m agents.book-skills.scripts.audit.run --priority P0,P1`
yields 0 issues.

## How to Re-run

```bash
# Custom nav alignment audit (this report's tool)
/c/Python314/python scripts/audit_nav_alignment.py

# Existing book-skills audit (P0+P1 priorities)
/c/Python314/python -m agents.book-skills.scripts.audit.run --priority P0,P1 --root .
```
