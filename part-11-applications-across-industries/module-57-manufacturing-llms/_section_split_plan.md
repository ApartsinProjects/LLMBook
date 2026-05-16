# Chapter 57 (Manufacturing) - Section Split Plan

## Audit status
- Existing sections: 0
- `index.html` body: **2,308 words** with 6 h2 sections (42.1-42.6)
- Pattern: **Inline-content chapter** (largest of the Part-11 inline cases)
- Effort: ~2-3 hours

## Plan: extract each index h2 into a section file

| New file              | Title                                                  | Source h2 |
| --------------------- | ------------------------------------------------------ | --------- |
| `section-57.1.html`   | Use Cases That Actually Work                           | 42.1      |
| `section-57.2.html`   | Failure Modes Specific to Manufacturing                | 42.2      |
| `section-57.3.html`   | Regulatory and Standards Framework                     | 42.3      |
| `section-57.4.html`   | Architectural Pattern: Plant-Floor Maintenance Copilot | 42.4      |
| `section-57.5.html`   | Postmortems Worth Reading                              | 42.5      |
| `section-57.6.html`   | Where to Read More                                     | 42.6      |

The h3 list (Maintenance Copilots, Inspection Reports, Work-Order Drafting, Supplier Risk, ERP/MES Query, Predictive-Maintenance Triage, Shop-Floor Voice) becomes intra-section h2's in `section-57.1.html`.

## Steps
1. Extract h2 subtrees -> 6 new files.
2. Renumber `42.x` -> `57.x`.
3. Replace index body with TOC.
4. Update `book_structure.yaml`.
5. Note: IT/OT boundary discussion may want its own section if it grows past one page during the split.
