# Senior Editor R2 — Wildcard Pass

**Agent**: 17-senior-editor (cycle-2 holistic review)
**Scope**: 26 randomly-sampled sections across parts 4-15 (every 15th file from sorted glob, parts 1-3 excluded)
**Mode**: ruthless triage; intervene only when a fix is a clear win
**Date**: 2026-05-19

## Summary

Of 26 sampled sections, **17 had at least one defect that warranted a surgical edit**. The rest were clean enough to leave alone. The recurring defects below repeat across the book and are worth a global sweep, not just the spots I touched here.

### Recurring defect classes (worth a sweep)

1. **"Why: Why" duplicated prefix in callout titles** — auto-generation artifact. Found in at least 3 places (53.1, 15.1, 17.2). Pattern: `Key Insight: Why: Why X`.
2. **Stray "X.Y.Z" prefix inside table titles** — auto-generation leftover where the old chapter number was prepended to a new one. Pattern: `Table 69.3.1: 47.4.1 ...`, `Table 67.3.1: 40.3.1 ...`, `Table 53.1.1: 1.1 ...`.
3. **Duplicate "What Comes Next" sections** — a manual `<h2 id="what-comes-next">` followed immediately by the standard `<div class="whats-next">` block, repeating the same forward pointer. Found in 72.3, 75.3, 78.2.
4. **Cross-reference rot** — text says one chapter/section number but the link points to a different one. Found in 49.1 ("Chapter 49" referring to itself, "Section 14.4" linking to 12.4), 53.1 (date inconsistencies), 55.1 (links to 47.1 for EU AI Act, mostly should be 53.1), 67.3 (refs to nonexistent "Chapter 62" budget example), 69.3 ("Section 47.4.3 below" should be 69.3.3), 28.4 ("Chapter 34" should be 42), 22.3 ("Section 13.2" should be 16.2), 45.5 ("Part VIII" should be "Part IX"), 24.12 ("Sections 40.1-40.5" should be 24.7-24.11), 20.10 (broken Section 41.3 / Section 33.1 refs), 31.3 (broken Section 27.1 ref).
5. **Exercise-numbering drift** — exercises labeled with the old chapter number. Found in 49.1 (24.1.X→49.1.X), 55.1 (29.10.X and 29.11.X→55.1.X).
6. **Header-tag bugs** — `<h3>` opened, `</h4>` closed. Found in 19.11 (six occurrences); likely a search-and-replace gone wrong.
7. **Code-Fragment placeholder labels** — `Code Fragment J.1.2` etc. (un-substituted Jinja-style placeholder). Found six in 19.10.
8. **Orphan/dangling sentences** — fragments left over from edits: "compares the LoRA and DoRA weight update mechanisms." (17.2), "The KV cache combine naturally with these..." (17.2), prerequisites with incomplete tail clauses (53.1, 26.1).

### Per-section disposition

| Section | Status | Notes |
|---------|--------|-------|
| part-10 / 49.1 | edited | Fixed broken prerequisites prose; self-ref to "Chapter 49" → "Chapter 47"; "Section 14.4" → "Section 12.4"; exercise labels 24.1.X → 49.1.X (5 fixes) |
| part-11 / 53.1 | edited | Removed off-topic jailbreak Key Insight (copy-paste error); fixed "Why: Why" title; fixed stray "1.1" in table title; reframed dates from "Mar 2027" to "May 2026" (book reality); fixed warning that claimed Phase 3 was active; tightened prerequisites tail |
| part-11 / 55.1 | edited | Fixed "EU AI Act compliance from Section 47.1" → Section 53.1; fixed "(covered in layer normalization)" placeholder → "Section 55.1.4 above"; renumbered exercises 29.10/29.11.X → 55.1.X (6 fixes); fixed What-Comes-Next pointing to wrong chapter |
| part-12 / 59.1 | edited | Fixed McCandlish-citation typo (McCandlish twice) → McCandlish, Kaplan, Amodei & OpenAI Dota Team |
| part-13 / 65.1 | edited | Fixed nonexistent "Section E.2" → "Section 65.2" |
| part-14 / 67.3 | edited | Fixed stray "40.3.1" prefix in table title; "Chapter 62" → "Section 67.4" for product spec; removed "Section 62.1 budget that was never written down" call-out that points nowhere; figcaption tightened |
| part-14 / 69.3 | edited | Fixed "47.4.3 below" → "Section 69.3.3"; stray "47.4.1" in table title; "Section 69.4 closes Chapter 69" (69.4 does not exist) → "Chapter 70 picks up" |
| part-14 / 72.3 | edited | Prerequisites "Section 55.1" (env-sustainability) → "Section 53.1" (regulation); merged duplicate What-Comes-Next |
| part-14 / 75.3 | edited | Same Section 55.1 → 53.1 prereq fix; merged duplicate What-Comes-Next |
| part-14 / 78.2 | edited | Merged duplicate What-Comes-Next |
| part-15 / 80.3 | edited | Fixed corrupted prerequisites ("Section 3.1 through chain-of-thought"); merged two near-duplicate research-frontier callouts about Mamba-2 SSD into one |
| part-15 / 83.5 | clean | Closing reading list; well-organised |
| part-4 / 15.1 | edited | Fixed "Key Insight: Why: Why synthetic data..." duplicate prefix |
| part-4 / 17.2 | edited | Fixed Big Picture stray "KV cache combine naturally" sentence fragment; fixed "Key Insight: Why: Why DoRA..." duplicate prefix; fixed orphan tail "compares the LoRA and DoRA weight update mechanisms" |
| part-4 / 19.10 | edited | Fixed 6 instances of `<h3>...</h4>` mismatched tags; replaced 7 `Code Fragment J.1.X` placeholders with `19.10.X` |
| part-5 / 20.10 | edited | Fixed broken "Section 41.3 on Gaussian splatting" (41.3 is unrelated) → Chapter 23; fixed "Sections 33.1-33.4" (33 doesn't exist) → "earlier sections in this chapter" |
| part-5 / 22.3 | edited | Prerequisites "Section 13.2" → "Section 16.2" (link target) |
| part-5 / 24.12 | edited | "Sections 40.1-40.5" → "Sections 24.7 through 24.11" |
| part-6 / 26.1 | edited | Prerequisites had garbled "Section 8.1 reasoning from Section 12.2" — rewrote as two clean cross-references |
| part-6 / 28.4 | edited | Meta description said 28.5 (off-by-one); "Chapter 34" → "Chapter 42" for eval frameworks |
| part-7 / 31.3 | edited | Removed broken Section 27.1 (Tool Use Protocols) cross-ref for "production deployment patterns" |
| part-7 / 34.3 | clean | Heading id `34-3-4` for the first H2 looks off but section may be a deliberate sub-deck; left as-is |
| part-8 / 37.1 | clean | Reads well, cross-refs check out |
| part-8 / 41.3 | clean | Datasets and benchmarks survey; tight |
| part-9 / 43.1 | clean | RAG evaluation; well-structured |
| part-9 / 45.5 | edited | "Part VIII's literature" → "Part IX's literature" (this section IS in Part IX) — same in meta description |

### Highest-impact patterns the meta agent should investigate

- **Cross-reference rot is endemic**, especially in late-part sections. A book-wide pass that resolves every "Section X.Y" mention to the actual link target and flags mismatches would catch a lot more than I sampled.
- **Auto-generation prefix artifacts** (`Why: Why...`, `Table 69.3.1: 47.4.1 ...`, `Code Fragment J.1.X`) are mechanical and could be swept with regex.
- **Duplicate "What Comes Next" blocks** are a templating issue, not editorial — likely worth a structural sweep.

### What I deliberately did NOT touch

- The "what makes an agent" set of intro paragraphs in 26.1 and 28.4 (reasonable as-is despite a heavy opening of overlapping callouts).
- The five back-to-back Warning callouts in 78.2 (each maps to a distinct failure mode; restructuring them would be a content rewrite, not a polish).
- The "GIANT_SECTION" sections marked do-not-split — I respected the marker even where box density was high (22.3, 31.3, 26.1, etc.).
- Sections 75.3 and 83.5 broader research-frontier text — content judgments outside this pass's mandate.

### Recommendation

A targeted cleanup pass focused on three regex-detectable defects (`Why: Why`, `Table X.Y.Z: A.B `, `Code Fragment [A-Z]\.`) plus a cross-reference validator would catch most of what remains without further human review.
