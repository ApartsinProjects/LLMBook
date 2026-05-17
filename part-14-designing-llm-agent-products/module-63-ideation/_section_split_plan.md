# Chapter 40 (Ideation) - Section Split Plan

## Audit status
- Existing sections: 1 (`section-40.1.html`, ~2,467 words, omnibus)
- `index.html` body: 53 words (TOC + "What Comes Next" only - no inline prose)
- Pattern: **Omnibus section needs splitting** (Part-10 stub pattern)
- Effort: ~2-3 hours (mostly mechanical extraction; light prose smoothing per section)

## Plan: split `section-40.1.html` into 6 sections

Each existing `40.1.x` h2 becomes its own `section-40.x.html`. Renumbering aligns sub-IDs to top-level.

| New file              | Title                                              | Source heading (in 40.1) |
| --------------------- | -------------------------------------------------- | ------------------------ |
| `section-40.1.html`   | What Kinds of Problems LLMs Solve Well             | 40.1.1                   |
| `section-40.2.html`   | What Kinds of Problems LLMs Still Do Poorly        | 40.1.2                   |
| `section-40.3.html`   | Problem-Discovery Heuristics                       | 40.1.3                   |
| `section-40.4.html`   | The "Bet My Own Money" Test                        | 40.1.4                   |
| `section-40.5.html`   | Mapping Problems to LLM Capabilities               | 40.1.5                   |
| `section-40.6.html`   | A 30-Minute Ideation Workshop (exercise)           | 40.1.6                   |

## Steps
1. For each h2 above, extract the subtree (h2 + following content until next h2) into its new section file with standard header/footer/nav.
2. Re-number all internal h3/h4 from `40.1.x.y` -> `40.x.y` (subsections under new top-level).
3. Update `index.html` TOC list to point to the six new files.
4. Update `book_structure.yaml` for module-40.
5. Verify cross-references in other chapters still resolve (likely few since this is leaf content).
