# Chapter 51 (Legal) - Section Split Plan

## Audit status
- Existing sections: 0
- `index.html` body: **1,576 words** with 5 well-structured h2 sections (already numbered 36.1-36.5 from legacy ordering)
- Pattern: **Inline-content chapter** (classic single-page pattern). Direct extraction.
- Effort: ~2 hours mechanical + ~1 hour to renumber 36.x -> 51.x

## Plan: extract each index h2 into a section file

| New file              | Title                                            | Source h2 in index |
| --------------------- | ------------------------------------------------ | ------------------ |
| `section-51.1.html`   | Use Cases That Actually Work                     | 36.1               |
| `section-51.2.html`   | Failure Modes Specific to Legal                  | 36.2               |
| `section-51.3.html`   | Bar Association and Regulatory Rules             | 36.3               |
| `section-51.4.html`   | Architectural Pattern: Verified-RAG for Legal    | 36.4               |
| `section-51.5.html`   | Where to Read More                               | 36.5               |

The h3 list under 36.1 (Contract Review, E-Discovery, Citation Gen, Regulatory Research, Legal Doc Summarization) becomes intra-section h2's in the new `section-51.1.html`.

## Steps
1. Move each h2 subtree from `index.html` -> new section file with standard wrapper.
2. Renumber `36.x.y` -> `51.x.y` across all anchors.
3. Replace index.html body content with a TOC list (Part-10 style).
4. Update `book_structure.yaml`.
5. Cross-ref scan: search repo for `36.1`-`36.5` anchors and `section-51` paths.
