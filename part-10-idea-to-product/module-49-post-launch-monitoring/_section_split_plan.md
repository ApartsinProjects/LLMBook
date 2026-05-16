# Chapter 49 (Post-Launch Monitoring) - Section Split Plan

## Audit status
- Existing sections: 1 (`section-49.1.html`, ~2,471 words, omnibus)
- `index.html` body: 53 words
- Pattern: **Omnibus section needs splitting**
- Effort: ~2-3 hours

## Plan: split into 6 sections

| New file              | Title                                                | Source heading |
| --------------------- | ---------------------------------------------------- | -------------- |
| `section-49.1.html`   | Eval-in-Prod: Continuous Evaluation Replaces Gates   | 49.1.1         |
| `section-49.2.html`   | Drift Detection: Five Flavours, Five Responses       | 49.1.2         |
| `section-49.3.html`   | Retraining and Re-Tuning Cadence                     | 49.1.3         |
| `section-49.4.html`   | User Feedback Loops in Production                    | 49.1.4         |
| `section-49.5.html`   | Model-Rotation Strategy                              | 49.1.5         |
| `section-49.6.html`   | The Continuous Steering Loop (synthesis)             | 49.1.6         |

## Steps
1. Extract each `49.1.x` subtree into its own section.
2. Renumber `49.1.x.y` -> `49.x.y` and update anchors.
3. Update TOC + `book_structure.yaml`.
4. Cross-link to Ch 48 (Deployment) and Ch 50 (Tools of the Trade) where relevant.
