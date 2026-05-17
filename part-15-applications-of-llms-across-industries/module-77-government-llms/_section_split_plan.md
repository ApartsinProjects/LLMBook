# Chapter 56 (Government) - Section Split Plan

## Audit status
- Existing sections: 0
- `index.html` body: **2,091 words** with 6 h2 sections (41.1-41.6)
- Pattern: **Inline-content chapter**
- Effort: ~2-3 hours

## Plan: extract each index h2 into a section file

| New file              | Title                                                  | Source h2 |
| --------------------- | ------------------------------------------------------ | --------- |
| `section-56.1.html`   | Use Cases That Actually Work                           | 41.1      |
| `section-56.2.html`   | Failure Modes Specific to Government                   | 41.2      |
| `section-56.3.html`   | Regulatory and Policy Framework                        | 41.3      |
| `section-56.4.html`   | Architectural Pattern: Public-Sector Grounded Assistant| 41.4      |
| `section-56.5.html`   | Postmortems Worth Reading                              | 41.5      |
| `section-56.6.html`   | Where to Read More                                     | 41.6      |

The h3 list (Constituent Service, FOIA, Regulatory Drafting, Benefits Eligibility, Fraud Detection, Internal Knowledge Search) becomes intra-section h2's in `section-56.1.html`.

## Steps
1. Extract h2 subtrees -> 6 new files.
2. Renumber `41.x` -> `56.x` everywhere.
3. Replace index body with TOC.
4. Update `book_structure.yaml`.
