# Footer & chapter-nav audit (read-only)

Root: `E:/Projects/BookBlogsHome/LLMBook` | Generated: read-only scan; no files modified.

## 1. Summary

| Metric | Count |
|---|---:|
| HTML pages scanned (excluding KDP/build/temp_*/node_modules/vendor) | 389 |
| Pages with a `<nav class="chapter-nav">` block | 387 |
| Pages missing `<footer>` entirely | 0 |
| Pages whose `<footer>` still contains unrendered `{{...}}` placeholders | 0 (across 0 of 387 pages) |
| Appendices affected by the section-prefix-letter bug | 0 |
| Individual 404 nav targets (outside the prefix bug) | 0 |
| Pages with chapter-nav present but a `prev`/`up`/`next` missing | 0 |
| Link-text vs. href mismatches (e.g. "Chapter 36" vs module-35) | 0 |
| Cross-Part transitions that bypass the Part landing page | 0 |
| Other intra-chapter `prev`/`next` deviations | 0 |
| Other intra-appendix `prev`/`next` deviations (non-prefix) | 0 |

## 2. Section A: Broken `chapter-nav` links

### A.0  Systemic section-prefix-letter bug in `appendices/`

Inside each affected appendix directory, `<a class="prev">` and `<a class="next">` 
links reference the *previous* appendix's letter instead of the current one. E.g.
`appendix-g-model-cards/section-g.1.html` has `next="section-f.2.html"` (should be `section-g.2.html`),
which 404s because the file with that name does not exist in this folder.

| Appendix dir | Expected letter | Observed letter(s) in nav hrefs | 404s found |
|---|:-:|:-:|---:|

Representative example per appendix:

### A.1  Other 404 nav targets

_None besides the systemic prefix bug above._

### A.2  Pages with chapter-nav present but a link missing from the prev/up/next trio

_None._

### A.3  Link text vs target mismatch

_None detected (note: heuristic relies on text containing "Chapter N" / "Section N.M")._

## 3. Section B: Logical sequence errors

### B.1  Cross-Part transitions bypass the Part landing page

Convention asks: last chapter of Part N's `next` -> `part-(N+1)/index.html`; 
first chapter of Part N's `prev` -> last section of Part (N-1)'s last chapter (or Part landing). 
In practice, every cross-Part transition currently jumps chapter-to-chapter and skips the Part landing.

_None._

### B.2  Intra-appendix `prev`/`next` issues (excluding the prefix-letter bug)

_None beyond the systemic prefix bug._

### B.3  Intra-chapter `prev`/`next` issues (parts only)

_None._

## 4. Section C: Footer issues

### C.1  Pages missing `<footer>` entirely

_None._

### C.2  Pages whose `<footer>` contains unrendered `{{...}}` placeholders

_None._

## 5. Section D: Special cases worth manual review

- Glossary lives at `appendices/glossary/` but uses `section-f.*` filenames (same as Appendix F hardware compute). WARNING: cross-links into Appendix F found: `appendices/glossary/section-f.5.html` `next` -> `../appendix-f-hardware-compute/index.html`
- Last chapter `module-42-manufacturing-llms/index.html` `next` -> `../../appendices/index.html` (`appendices/index.html`). OK (leads to appendices).
- Front-matter -> Part I bridges: `front-matter/copyright.html` `next` -> `../part-1-foundations/module-00-ml-pytorch-foundations/index.html`
- `part-1-foundations/index.html` `prev` -> `../toc.html`
- Capstone `capstone/index.html` nav: prev->`../front-matter/fm-course-syllabi.html`, up->`../toc.html`, next->`requirements.html`
- Capstone `capstone/requirements.html` nav: prev->`index.html`, up->`index.html`, next->`../appendices/index.html`

## 6. Recommended next actions

- Fix the systemic appendix prefix-letter bug (Section A.0) by walking `appendices/appendix-g-*` through `appendices/appendix-p-*` and replacing the leading section letter in each `prev`/`next` href to match the appendix's own letter; this alone resolves the bulk of Section A and the corresponding entries in B.
- Re-run the build pipeline so `{{book.edition}}` / `{{book.publication_year}}` get resolved into actual values across all 387 pages (Section C.2 - single root cause).
- Repair the cross-Part `prev`/`next` chain (Section B.1) so each Part landing page is part of the reading sequence (currently the chain jumps chapter-to-chapter across Part boundaries).
- Fix the four front-matter / Appendix-U dead links pointing to non-existent `appendix-aj-reading-pathways/` and `appendix-ak-course-syllabi/` (Section A.1).
- Add a `<footer>` block to `index.html` (the home page, currently the only page without one) and confirm `appendices/glossary/section-f.5.html` should have a `next` link (currently the only nav present with a missing link).

---
_Audit script: `scripts/_audit_nav_footer.py`; pages scanned: 389; pages with chapter-nav: 387._