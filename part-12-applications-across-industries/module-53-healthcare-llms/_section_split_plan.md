# Chapter 53 (Healthcare) - Section Split Plan

## Audit status
- Existing sections: 1 (`section-53.7.html` - **legacy survivor titled "Section 53.3: Healthcare & Biomedical AI", actually old Ch 27.3 content**)
- `index.html` body: **1,519 words** with 5 modern h2 sections (38.1-38.5)
- Pattern: **Hybrid: inline new content + legacy omnibus to retire**
- Effort: ~3-4 hours

## Plan: split index + retire 53.7

### New sections from index.html

| New file              | Title                                                  | Source h2 |
| --------------------- | ------------------------------------------------------ | --------- |
| `section-53.1.html`   | Use Cases That Actually Work                           | 38.1      |
| `section-53.2.html`   | Failure Modes Specific to Healthcare                   | 38.2      |
| `section-53.3.html`   | Regulatory Framework (FDA, HIPAA)                      | 38.3      |
| `section-53.4.html`   | Architectural Pattern: Defensive Clinical LLM          | 38.4      |
| `section-53.5.html`   | Where to Read More                                     | 38.5      |

The h3 subsections (Ambient Clinical Doc, CDS, Patient Triage, Medical Coding, Lit Synthesis, Drug Discovery) become intra-section h2's in `section-53.1.html`.

### Fate of `section-53.7.html`
Legacy `27.3.x` subsections cover Medical LLMs, Clinical NLP, Medical QA, Drug Discovery/Molecular Generation, Protein Structure/Genomics. Recommend:
1. Merge **drug discovery + protein/genomics** content into `section-53.1.html` (it's much richer than the new index treatment).
2. Merge **medical QA + clinical NLP** detail into `section-53.1.html`.
3. **Delete** `section-53.7.html`.

## Steps
1. Extract 5 new sections from index.
2. Renumber `38.x` -> `53.x`.
3. Merge 53.7's drug-discovery and protein content into 53.1.
4. Delete `section-53.7.html`.
5. Replace index body with TOC; update `book_structure.yaml`.
