# Prose Reference Audit

Audit run: **389** content HTML pages scanned. Inventories: 546 figure captions, 1099 code-fragment captions, 17 algorithm/pseudocode blocks, 214 section files, 42 chapters.

This audit complements the existing `numbering-audit.md`. The earlier pass walked PROSE only; this one scans inside code-fragment comments, inside `<img alt>` attributes, inside caption cross-references, and across plain-text prose mentions that could be hyperlinked.

**Headline:** No genuine reference breakage across any of the four problem categories. The only finding is **996** plain-text mentions of existing targets that *could* be hyperlinked (Cat. 2a; see Section 3).

## 1. Summary

| Category | Problems found |
|---|---:|
| Cat. 1 — Phantom refs inside code comments | 0 |
| Cat. 2a — Plain-text mentions that should be hyperlinks | 996 |
| Cat. 2b — Plain-text mentions whose target does not exist | 0 |
| Cat. 3a — `<img alt>` references with no matching target | 0 |
| Cat. 3b — `<img alt>` figure label disagrees with surrounding caption | 0 |
| Cat. 4 — Caption cross-refs to non-existent targets | 0 |
| **Total problems** (excluding Cat. 2a hyperlink suggestions) | **0** |

## 2. Category 1 — Phantom references inside code comments

References found inside `<pre><code>` comment spans whose target does not exist anywhere in the book.

_None found._

## 3. Category 2 — Plain-text mentions that could be hyperlinks

Prose contains `Figure X.Y.Z` / `Section X.Y` etc. as plain text, but the target exists and is normally linked elsewhere. Highest-value candidates are labels mentioned unlinked **on three or more pages**; single-mention occurrences are common (e.g. when discussing two figures by name in the same paragraph) and lower priority.

Total non-low-priority plain-text mentions: **988** across **460** distinct labels.

### Top 30 labels by un-linked-mention count

| Rank | Label | Count | Distinct files | Example file:line |
|---:|---|---:|---:|---|
| 1 | `Chapter 28` | 39 | 28 | `appendices/appendix-a-mathematical-foundations/index.html`:49 |
| 2 | `Chapter 17` | 20 | 14 | `appendices/appendix-a-mathematical-foundations/section-a.4.html`:88 |
| 3 | `Chapter 15` | 19 | 15 | `appendices/appendix-a-mathematical-foundations/section-a.1.html`:107 |
| 4 | `Chapter 11` | 17 | 13 | `appendices/appendix-c-python-for-llm/index.html`:40 |
| 5 | `Chapter 12` | 17 | 13 | `appendices/appendix-c-python-for-llm/index.html`:40 |
| 6 | `Chapter 21` | 17 | 14 | `appendices/appendix-k-langchain/index.html`:41 |
| 7 | `Chapter 00` | 16 | 8 | `appendices/appendix-a-mathematical-foundations/index.html`:49 |
| 8 | `Chapter 04` | 15 | 13 | `appendices/appendix-a-mathematical-foundations/index.html`:49 |
| 9 | `Chapter 06` | 15 | 11 | `appendices/appendix-a-mathematical-foundations/index.html`:49 |
| 10 | `Chapter 19` | 14 | 12 | `appendices/appendix-h-prompt-templates/index.html`:42 |
| 11 | `Section 4.1` | 13 | 11 | `appendices/appendix-a-mathematical-foundations/section-a.2.html`:104 |
| 12 | `Chapter 29` | 13 | 11 | `appendices/appendix-e-git-collaboration/index.html`:40 |
| 13 | `Section 17.1` | 12 | 11 | `appendices/appendix-a-mathematical-foundations/section-a.4.html`:88 |
| 14 | `Chapter 30` | 12 | 11 | `appendices/appendix-s-pedagogy-kit/index.html`:82 |
| 15 | `Chapter 16` | 11 | 10 | `appendices/appendix-a-mathematical-foundations/index.html`:56 |
| 16 | `Chapter 09` | 11 | 10 | `appendices/appendix-m-inference-serving/index.html`:37 |
| 17 | `Chapter 34` | 11 | 4 | `part-11-idea-to-product/index.html`:37 |
| 18 | `Chapter 10` | 9 | 8 | `appendices/appendix-b-ml-essentials/section-b.2.html`:69 |
| 19 | `Chapter 31` | 9 | 7 | `appendices/appendix-s-pedagogy-kit/index.html`:82 |
| 20 | `Section 6.1` | 9 | 9 | `appendices/appendix-t-problem-solution-key/index.html`:520 |
| 21 | `Chapter 25` | 8 | 7 | `appendices/appendix-s-pedagogy-kit/index.html`:78 |
| 22 | `Section 16.1` | 7 | 7 | `appendices/glossary/section-f.3.html`:36 |
| 23 | `Section 30.2` | 6 | 5 | `appendices/appendix-t-problem-solution-key/index.html`:790 |
| 24 | `Section 4.2` | 6 | 5 | `part-1-foundations/module-04-transformer-architecture/index.html`:38 |
| 25 | `Section 5.2` | 6 | 2 | `part-1-foundations/module-05-decoding-text-generation/section-5.1.html`:70 |
| 26 | `Section 28.1` | 6 | 5 | `part-10-frontiers/module-33-emerging-architectures/section-33.7.html`:253 |
| 27 | `Chapter 07` | 5 | 4 | `appendices/appendix-g-model-cards/index.html`:42 |
| 28 | `Section 8.1` | 5 | 5 | `part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html`:71 |
| 29 | `Chapter 08` | 5 | 5 | `part-2-understanding-llms/module-07-modern-llm-landscape/index.html`:128 |
| 30 | `Code Fragment 13.2.4` | 5 | 1 | `part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html`:116 |

### Cat. 2b — Plain-text mentions whose target does not exist

_None found._

## 4. Category 3 — Image alt-text reference issues

### Cat. 3a — alt-text cites a number that does not exist

_None found._

### Cat. 3b — alt-text figure number disagrees with surrounding figcaption

_None found._

## 5. Category 4 — Caption cross-references to non-existent targets

`<figcaption>`, `<caption>`, `div.diagram-caption`, `div.code-caption` that reference another figure / section / code-fragment whose target does not exist.

_None found._

## 6. Recommended action plan

- **No genuine reference breakage found.** All four problem categories (in-code phantoms, alt-text phantoms, alt-text mismatches, caption cross-references) returned zero hits. This strongly suggests the existing numbering audit + manual cleanup have already caught all phantom citations.
- **Optional hyperlinking pass (988 plain-text mentions across 460 distinct labels; 76 labels mentioned 3+ times unlinked)** — The top labels in Section 3 are good candidates for a single search-and-replace pass that wraps `Figure X.Y.Z` in `<a href=...>Figure X.Y.Z</a>`. Skip cases where the paragraph already links the same label (Cat. 2a does NOT include those — they are flagged internally as low-priority and excluded from the top-30).
- **Note on Cat. 2a scope** — Cat. 2a includes plain-text `Chapter NN` references in module-overview and appendix introductions where the chapter is named alongside its title (e.g. 'Chapter 28 (Evaluation)') and is *already* linked elsewhere on the page. These are stylistic choices and may not be worth bulk-rewriting; review the top-30 list before deciding.
- **Re-run after fixes** — re-run `python scripts/_audit_prose_references.py` after any structural change (renumbering, deletion of figures, restructure of sections).
