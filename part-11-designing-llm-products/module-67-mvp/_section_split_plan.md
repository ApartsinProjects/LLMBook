# Chapter 44 (MVP) - Section Split Plan

## Audit status
- Existing sections: 1 (`section-44.1.html`, ~2,248 words, omnibus)
- `index.html` body: 53 words
- Pattern: **Omnibus section needs splitting**
- Effort: ~2 hours

## Plan: split into 5 sections

| New file              | Title                                              | Source heading |
| --------------------- | -------------------------------------------------- | -------------- |
| `section-44.1.html`   | The 80/20 Cuts: What an LLM MVP Is Allowed to Skip | 44.1.1         |
| `section-44.2.html`   | The Vertical-Slice Pattern                         | 44.1.2         |
| `section-44.3.html`   | The Internal Pilot Before the Public Launch        | 44.1.3         |
| `section-44.4.html`   | When to Keep Building vs Pivot vs Kill             | 44.1.4         |
| `section-44.5.html`   | A 30-Day MVP Plan (worked example)                 | 44.1.5         |

## Steps
1. Extract each `44.1.x` subtree into own section file with standard chrome.
2. Renumber `44.1.x.y` -> `44.x.y`.
3. Update `index.html` TOC + `book_structure.yaml`.
