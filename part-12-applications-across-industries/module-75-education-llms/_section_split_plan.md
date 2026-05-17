# Chapter 54 (Education) - Section Split Plan

## Audit status
- Existing sections: 0
- `index.html` body: **1,458 words** with 5 h2 sections (39.1-39.5)
- Pattern: **Inline-content chapter** (clean case, no legacy file)
- Effort: ~2 hours

## Plan: extract each index h2 into a section file

| New file              | Title                                                  | Source h2 |
| --------------------- | ------------------------------------------------------ | --------- |
| `section-54.1.html`   | Use Cases That Actually Work                           | 39.1      |
| `section-54.2.html`   | Failure Modes Specific to Education                    | 39.2      |
| `section-54.3.html`   | Regulatory and Policy Framework (FERPA, COPPA)         | 39.3      |
| `section-54.4.html`   | Architectural Pattern: Pedagogically-Scaffolded Tutor  | 39.4      |
| `section-54.5.html`   | Where to Read More                                     | 39.5      |

The h3 list (Tutoring, Assessment Generation, Accessibility, Teacher Support, Programming Education) becomes intra-section h2's in `section-54.1.html`.

## Steps
1. Extract h2 subtrees from `index.html` -> 5 new files.
2. Renumber `39.x` -> `54.x` everywhere.
3. Replace index body with TOC.
4. Update `book_structure.yaml`.
5. Cross-ref scan for `39.` and `section-54` references.
