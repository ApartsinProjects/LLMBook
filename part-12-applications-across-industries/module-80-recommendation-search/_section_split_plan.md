# Chapter 59 (Recommendation & Search) - Section Split Plan

## Audit status
- Existing sections: 2
  - `section-59.1.html`: "Ranking, Retrieval, and Personalization" - **~1,387 words, 3 h2 subsections**
  - `section-59.2.html`: "LLM-Powered Recommendation & Search" - **~6,266 words, legacy 27.4.x sprawling content**
- `index.html` body: 449 words (TOC + intro)
- Pattern: **Hybrid: split 59.1 + carve 59.2 into focused sections**
- Effort: ~4-5 hours

## Plan: split + reorganize into 6 sections

### From `section-59.1.html` (3 subsections)

| New file              | Title                                              | Source                                  |
| --------------------- | -------------------------------------------------- | --------------------------------------- |
| `section-59.1.html`   | Embedding-Based Candidate Generation               | 59.1.1                                  |
| `section-59.2.html`   | LLMs as Re-rankers and Explainers                  | 59.1.2 + merge 27.4.1                   |
| `section-59.3.html`   | Natural Language Search and Conversational Discovery | 59.1.3 + merge 27.4.2 + 27.4.3        |

### From legacy `section-59.2.html` (carve up)

| New file              | Title                                              | Source                                  |
| --------------------- | -------------------------------------------------- | --------------------------------------- |
| `section-59.4.html`   | User Preference Modeling                           | 27.4.4                                  |
| `section-59.5.html`   | NL-to-Dashboard and Automated Analytics            | 27.4.5                                  |
| `section-59.6.html`   | Text Analytics at Scale                            | 27.4.6                                  |

After re-distribution, **delete** `section-59.2.html` (the legacy file).

## Steps
1. Split 59.1 into 3 sections (59.1, 59.2, 59.3).
2. Carve legacy 59.2 into 59.4, 59.5, 59.6.
3. Merge 27.4.1 (LLMs as Recommendation Engines) into new 59.2.
4. Merge 27.4.2 + 27.4.3 (LLM-Powered Search, Conversational Rec) into new 59.3.
5. Delete legacy `section-59.2.html`; update `book_structure.yaml`.
6. Cross-ref scan for `27.4.` anchors.
