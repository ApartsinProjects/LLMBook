# Chapter 43 (Vibe-Coding) - Section Split Plan

## Audit status
- Existing sections: 2
  - `section-43.1.html`: "Prototyping via Vibe-Coding" - **~2,378 words, 6 h2 subsections (43.1.x)**
  - `section-43.2.html`: "Vibe-Coding & AI-Assisted Software Engineering" - **~3,759 words, 4 h2 subsections (legacy 27.1.x)**
- `index.html` body: 56 words (TOC only)
- Pattern: **Two omnibus sections; second has stale numbering from old Ch 27**
- Effort: ~3-4 hours (significant overlap between 43.1 and 43.2 to merge)

## Plan: split + merge into 6 sections

| New file              | Title                                          | Source                              |
| --------------------- | ---------------------------------------------- | ----------------------------------- |
| `section-43.1.html`   | What Vibe-Coding Means and When It Pays Off    | 43.1.1 + 43.1.2 merged              |
| `section-43.2.html`   | Code Completion and Fill-in-the-Middle         | 27.1.1                              |
| `section-43.3.html`   | The AI-Native IDE Landscape (Cursor, Zed, etc) | 43.1.4 + 27.1.2 merged              |
| `section-43.4.html`   | The Compressed Build-Test-Fix Cycle            | 43.1.3                              |
| `section-43.5.html`   | Agentic Coding and Spec-to-Code                | 27.1.3 + 27.1.4 merged              |
| `section-43.6.html`   | Mistakes to Avoid & Place in the Pipeline      | 43.1.5 + 43.1.6 merged              |

## Steps
1. Reconcile 43.1's 2026 "tool landscape" with 27.1.2's older list - keep latest.
2. Renumber `27.1.x` -> `43.x.y` and update anchors.
3. Move/distribute Exercises block.
4. Update `index.html` TOC and `book_structure.yaml`.
5. Cross-reference scan for `27.1.` and `section-43.2`.
