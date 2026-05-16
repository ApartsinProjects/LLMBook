# Chapter 41 (Product Management) - Section Split Plan

## Audit status
- Existing sections: 2
  - `section-41.1.html`: "From Hypothesis to Product Spec" - **~2,139 words, 5 h2 subsections**
  - `section-41.2.html`: "LLM Product Management" - **~4,624 words, 6 h2 subsections + legacy 31.2.x numbering**
- `index.html` body: 54 words (TOC only)
- Pattern: **Two omnibus sections; second has stale numbering from old Ch 31**
- Effort: ~4 hours (renumbering, light prose merging where 41.1 and 41.2 subtopics overlap, e.g. risk tiers vs hallucination risk)

## Plan: split into ~6-8 sections

Merge overlaps and renumber to a clean `41.x.html` layout.

| New file              | Title                                                     | Source                                  |
| --------------------- | --------------------------------------------------------- | --------------------------------------- |
| `section-41.1.html`   | From Hypothesis to Product Spec                           | keep 41.1 intro + 41.1.1 + 41.1.2       |
| `section-41.2.html`   | Translating Business Problems to LLM Requirements         | 41.2 + 31.2.1 merged                    |
| `section-41.3.html`   | Risk Tiers and Hallucination Risk Management              | 41.1.3 + 31.2.3 merged                  |
| `section-41.4.html`   | Success Metrics, Latency, Cost & Quality Budgets          | 41.1.4 + 31.2.2 merged                  |
| `section-41.5.html`   | UX Design for LLM Products                                | 31.2.4                                  |
| `section-41.6.html`   | Iterative Delivery for LLM Products                       | 31.2.5                                  |
| `section-41.7.html`   | The Cross-Functional Spec Review & Stakeholder Comms      | 41.1.5 + 31.2.6 merged                  |

## Steps
1. De-duplicate where 41.1 risk-tier discussion overlaps with 31.2.3 hallucination-risk.
2. Renumber every `31.2.x` -> matching `41.y` ID and update internal anchors.
3. Move existing Exercises block to end of `section-41.7.html` or split into per-section exercises.
4. Regenerate `index.html` TOC + `book_structure.yaml` entries.
5. Audit cross-references (search repo for `31.2.` and `section-41.2`).
