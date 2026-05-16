# Chapter Section Audit (Parts 10-11)

**Date:** 2026-05-16
**Scope:** All chapters in `book_structure.yaml` flagged with fewer than 3 section-X.Y.html files.

## Headline finding

All 14 audited chapters need restructuring; **none qualify as "keep as-is" (lookup-style)**. Two distinct fix patterns dominate:

- **Pattern A (Part 10): "Single omnibus section"** - chapter has 1-2 sections, each carrying 2,000-4,600 words covering 5-8 sub-topics under one umbrella heading. The body of `index.html` is just a TOC stub. Fix: split the omnibus into per-topic sections.
- **Pattern B (Part 11): "Inline-content index + legacy survivor"** - chapter's `index.html` carries 1,400-2,300 words of substantive prose under 5-6 h2 sections (numbered with legacy IDs `36.x`-`42.x` from the old monolithic Ch 36-42). Some also retain a `section-X.7.html` from the even older Ch 27 structure. Fix: extract h2 sections from index + retire the legacy file.

## Per-chapter summary

| Ch | Title                  | Pattern        | Sections now | Sections planned | Index body words | Notes / Effort                    |
| -- | ---------------------- | -------------- | ------------ | ---------------- | ---------------- | --------------------------------- |
| 40 | Ideation               | A (omnibus)    | 1            | 6                | 53               | 2-3 h, mechanical split           |
| 41 | Product Management     | A (2 omnibus)  | 2            | 7                | 54               | 4 h, dedup needed                 |
| 43 | Vibe-Coding            | A (2 omnibus)  | 2            | 6                | 56               | 3-4 h, 27.1 -> 43.x renumber      |
| 44 | MVP                    | A (omnibus)    | 1            | 5                | 53               | 2 h, mechanical                   |
| 49 | Post-Launch Monitoring | A (omnibus)    | 1            | 6                | 53               | 2-3 h, mechanical                 |
| 51 | Legal                  | B (inline)     | 0            | 5                | 1,576            | 3 h, 36.x -> 51.x renumber        |
| 52 | Finance                | B + legacy     | 1 (52.7)     | 5 + retire 52.7  | 1,484            | 3-4 h, merge legacy content       |
| 53 | Healthcare             | B + legacy     | 1 (53.7)     | 5 + retire 53.7  | 1,519            | 3-4 h, migrate drug-discovery     |
| 54 | Education              | B (inline)     | 0            | 5                | 1,458            | 2 h, clean case                   |
| 55 | Cybersecurity          | B + legacy     | 1 (55.7)     | 5 + retire 55.7  | 1,698            | 3-4 h, legacy mostly subsumed     |
| 56 | Government             | B (inline)     | 0            | 6                | 2,091            | 2-3 h                             |
| 57 | Manufacturing          | B (inline)     | 0            | 6                | 2,308            | 2-3 h, largest inline body        |
| 58 | Creative Industries    | B + off-topic  | 2            | 5 + retire 58.2  | 482              | 4-5 h, legacy file off-topic      |
| 59 | Recommendation/Search  | Hybrid carve   | 2            | 6 + retire 59.2  | 449              | 4-5 h, redistribute 27.4.x        |

**Total estimated authoring effort:** ~42-55 hours (mechanical extraction + renumbering + dedup + light prose smoothing). No new prose writing required, except Ch 58.5 (workflow patterns + rights/licensing) ~3 h.

## Key cross-cutting risks

1. **Legacy ID drift:** Old `27.x`, `31.x`, `36.x`-`42.x` anchor IDs are still live in cross-references. Every split must include a repo-wide cross-ref scan + redirect/anchor-update pass.
2. **Off-topic legacy content:** `section-58.2.html` contains Education + Legal material that belongs in Ch 51, 54. Don't just delete; migrate first.
3. **Duplicate coverage:** Ch 41 (PM) has both new `41.1` risk-tier content and legacy `31.2.3` hallucination-risk content - merge instead of preserving both.
4. **Part 10 vs Part 11 stylistic gap:** Part 10 omnibus sections are well-written modern prose. Part 11 indices are also modern. Legacy `.7` files are clearly older and less polished - prefer the modern voice when merging.

## Output: per-chapter plan files

Written to each chapter directory as `_section_split_plan.md`:

- `part-10-idea-to-product/module-40-ideation/_section_split_plan.md`
- `part-10-idea-to-product/module-41-product-management/_section_split_plan.md`
- `part-10-idea-to-product/module-43-vibe-coding/_section_split_plan.md`
- `part-10-idea-to-product/module-44-mvp/_section_split_plan.md`
- `part-10-idea-to-product/module-49-post-launch-monitoring/_section_split_plan.md`
- `part-11-applications-across-industries/module-51-legal-llms/_section_split_plan.md`
- `part-11-applications-across-industries/module-52-finance-llms/_section_split_plan.md`
- `part-11-applications-across-industries/module-53-healthcare-llms/_section_split_plan.md`
- `part-11-applications-across-industries/module-54-education-llms/_section_split_plan.md`
- `part-11-applications-across-industries/module-55-cybersecurity-llms/_section_split_plan.md`
- `part-11-applications-across-industries/module-56-government-llms/_section_split_plan.md`
- `part-11-applications-across-industries/module-57-manufacturing-llms/_section_split_plan.md`
- `part-11-applications-across-industries/module-58-creative-industries/_section_split_plan.md`
- `part-11-applications-across-industries/module-59-recommendation-search/_section_split_plan.md`

## Recommended execution order

1. **Pattern B clean cases first** (Ch 51, 54, 56, 57) - no legacy file, pure index extraction. ~10 h total.
2. **Pattern A omnibus splits** (Ch 40, 44, 49) - simple, no overlaps. ~7 h.
3. **Pattern B + legacy retires** (Ch 52, 53, 55) - need merge decisions. ~10 h.
4. **Hybrid carve-ups** (Ch 41, 43, 58, 59) - heaviest cognitive load. ~17 h.
5. After all splits: run global cross-ref / anchor audit + regenerate `book_structure.yaml`.

No chapter qualifies as Pattern (c) "lookup-style". All 14 should be split into proper multi-section chapters.
