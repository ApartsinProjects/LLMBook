# Shallow Content Audit & Depth Plan

## Problem statement (user)

> "Many modules/sections leave the impression of shallow presentation — that is, library concepts, architectures, ideas are not explained in sufficient depth and more like a shopping list of what exists. Audit all texts; consider adding depth or cross-references to other places in the book where explained in depth. Consider where to add (if to add); add or modify appropriate callout boxes or plain prose. Prepare detailed plan."

## What "shallow" looks like in this codebase

Three distinct failure modes, all common in survey-style technical writing:

**Mode 1: Naming-without-explaining ("shopping list").** A sentence enumerates 4-6 named systems with no mechanism, just titles:
> "Modern frameworks include LangChain, LlamaIndex, DSPy, CrewAI, AutoGen, Semantic Kernel, and Haystack."

The reader gets the names but no model of how they differ.

**Mode 2: One-paragraph concept introductions.** A new concept appears, receives 3-4 sentences of definition, and immediately becomes a building block in a longer pattern. The reader who has not previously encountered the concept either takes it on faith or stops to look it up elsewhere.

Examples in this book:
- Speculative decoding (§9.3) — defined in 4 sentences, then used as scaffolding for production patterns
- Constitutional AI (§17.x) — described in one paragraph, then referenced as if understood
- KV cache (§9.2) — introduced via diagram only, no algebraic walk-through

**Mode 3: Deferred explanation that never happens.** Phrases like "we discuss this in detail later" or "see Chapter X" where the cross-reference target is itself shallow or missing. This compounds: the reader is sent on a goose chase.

## Detection methodology

Three quantitative heuristics + one qualitative pass.

### Heuristic A: paragraph density of named entities

For each paragraph, count proper nouns / framework names / model names. A paragraph with 4+ named entities and < 80 words is a "shopping list" candidate.

Implementation: NER-lite via capitalized-word patterns + a known-entity list (~200 framework / model names already in the book).

Expected output: 50-150 candidate paragraphs.

### Heuristic B: section length vs concept count

For each H2/H3 section:
- Count distinct H3 sub-headings AND named callouts inside it
- Count total prose word count
- Compute "words per concept"

Sections with < 250 words per declared concept are review-the-depth candidates.

### Heuristic C: dangling cross-reference detection

Find every "see Section X.Y" / "covered in Chapter NN" mention.
- Verify the target exists (already done in v6.27 references audit)
- ADDITIONALLY: check that the target section is itself > 800 words and contains at least one runnable example or worked diagram. If it's short, it's a fake handoff.

### Qualitative pass D: chapter-by-chapter spot-check

For each chapter:
- Read the first paragraph after the chapter opener
- Read the chapter's "Big Picture" callout
- Compare to the LAST paragraph of the chapter

If the last paragraph just lists tools/frameworks without summarizing the *intuition* the reader is supposed to walk away with, the chapter is a shopping list.

This needs a human reader (or a focused agent run); cannot be fully mechanized.

## Decision framework: deepen vs. cross-reference

Once a candidate is flagged, decide between three actions:

| Symptom                                         | Action                                              |
|-------------------------------------------------|-----------------------------------------------------|
| Concept is the chapter's main topic             | **DEEPEN here** (add 200-500 words + 1 figure)      |
| Concept is fully explained in another chapter   | **CROSS-REFERENCE** (replace with ≥ 1-sentence intuition + link) |
| Concept is genuinely peripheral (mentioned once)| **DROP THE NAME** (keep prose, lose the buzzword)   |
| Concept needs depth book has nowhere            | **NEW APPENDIX subsection** + cross-reference       |

## Callout-box patterns to use when deepening in place

The book already has these callout types (catalogued in `styles/book.css`). Pick the one that matches the depth gap:

- **`callout big-picture`** — when shallow due to lack of WHY. Add 1-paragraph "the bet behind this" callout.
- **`callout key-insight`** — when shallow due to missing AHA moment. Add a worked example with concrete numbers.
- **`callout algorithm`** — when shallow due to missing HOW. Add 5-10 step pseudocode.
- **`callout practical-example`** — when shallow due to abstraction. Add a 1-page "real story" scenario.
- **`callout library-shortcut`** — when comparing frameworks. Add a 3-bullet "when to pick X" decision rule.

## What NOT to do

- Do not deepen everything. The book is already large; 50% of "shallow" sections are intentionally a survey before a deep dive.
- Do not add cross-references that point at equally-shallow targets. Verify depth at the target first (Heuristic C).
- Do not introduce new framework names while deepening. Naming-density is the symptom; adding more names makes it worse.

## Acceptance criteria for one deepening pass

For a chapter to be considered "depth-audited":
- Heuristic A flag count for that chapter drops 50%
- Every Heuristic C dangling cross-reference is either fixed (target genuinely deep) or rewritten (replaced with a 2-sentence summary)
- Reader smoke test: can someone who has *only* read this chapter implement the mental model? If no, deepen further.

## Effort estimate

| Phase                                                   | Effort   |
|---------------------------------------------------------|----------|
| 1. Build heuristic-A/B/C audit scripts (`_v638-_v640`)  | 4 hrs    |
| 2. Generate chapter-by-chapter shallow-content reports  | 1 hr     |
| 3. Manual review of top-30 worst sections              | 4 hrs    |
| 4. Write deepening callouts / cross-refs               | 12 hrs   |
| 5. Apply across full book + diff-review                | 6 hrs    |
| **Total**                                               | **~27 hrs** |

This is a v7.x activity, parallel to the Hyperlinks Plan and the Content Update Plan. Best run AFTER the Content Update Plan (v7.0) so 2026 content is in place before depth-tuning.

## Order of operations across the three big content plans

1. **Content Update Plan** (~50 hrs) — bring 2026 content in
2. **Hyperlinks Plan** (~13 hrs) — establish concept anchor table
3. **This plan / Shallow Content Audit** (~27 hrs) — fix depth gaps using anchor table
4. **Duplicate Content Plan** (~13 hrs) — collapse re-explanations after depth-audit reveals canonical homes

Total integrated content audit: ~100 hours of focused editing work.
