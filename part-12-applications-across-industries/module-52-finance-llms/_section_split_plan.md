# Chapter 52 (Finance) - Section Split Plan

## Audit status
- Existing sections: 1 (`section-52.7.html` - **legacy survivor titled "Section 52.2: LLMs in Finance & Trading", actually old Ch 27.2 content**)
- `index.html` body: **1,484 words** with 5 modern h2 sections (37.1-37.5)
- Pattern: **Hybrid: inline new content + legacy omnibus to merge or retire**
- Effort: ~3-4 hours (split index + decide on 52.7 fate)

## Plan: split index + retire 52.7

### New sections from index.html

| New file              | Title                                          | Source h2 |
| --------------------- | ---------------------------------------------- | --------- |
| `section-52.1.html`   | Use Cases That Actually Ship                   | 37.1      |
| `section-52.2.html`   | Failure Modes Specific to Finance              | 37.2      |
| `section-52.3.html`   | Regulatory Framework                           | 37.3      |
| `section-52.4.html`   | Architectural Pattern: Tiered LLM Trust        | 37.4      |
| `section-52.5.html`   | Where to Read More                             | 37.5      |

### Fate of `section-52.7.html`
The legacy file's 6 subsections (Financial NLP, Automated Reports, Trading Signals, Fraud/KYC, ABSA, Emotion Recognition) all duplicate (or could enrich) the new `52.1` use-case section. Recommend:
1. **Merge** useful content (ABSA, emotion recognition, specific tool references) into `section-52.1.html` and `section-52.2.html`.
2. **Delete** `section-52.7.html` once content is absorbed.

## Steps
1. Extract index h2 subtrees -> 5 new section files.
2. Renumber `37.x` -> `52.x`.
3. Merge surviving content from 52.7 into 52.1/52.2.
4. Delete `section-52.7.html` and remove from `book_structure.yaml`.
5. Replace index.html body with TOC.
6. Cross-ref scan for `37.` anchors and `section-52.7`.
