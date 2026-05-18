# Callout Catalogue — Single Source of Truth

Last reviewed: 2026-05-18 session.

## Canonical 21 callout types

All callouts use the form:
```html
<div class="callout TYPE">
  <div class="callout-title">CanonicalPrefix: Optional context</div>
  <p>Body content.</p>
</div>
```

| # | Class | Title prefix(es) | Role | Body shape | Count in book |
|---|-------|------------------|------|-----------|--------------:|
| 1 | `big-picture` | "Big Picture" | Sets context, why-it-matters opener | 1 paragraph | 529 |
| 2 | `key-insight` | "Key Insight" | Single inline aha-moment, mental model | ONE paragraph | 852 |
| 3 | `key-takeaway` | "Key Takeaways" | End-of-section bulleted recap | `<ul>` 3-7 items | 232 |
| 4 | `looking-back` | "Looking Back" | Chapter/section opener that recalls prior material | 1 paragraph | 36 |
| 5 | `whats-next` | "What's Next" / "What Comes Next" | Transition to next section/chapter | 1 paragraph + anchor link | 62 |
| 6 | `cross-ref` (See Also) | "See Also" | Inter-section/chapter pointer | `<ul>` of anchor-linked phrases | 89 |
| 7 | `practical-example` | "Real-World Scenario" | 8-field scenario (Who/Situation/Problem/Dilemma/Decision/How/Result/Lesson) | Bold field labels + prose | 396 |
| 8 | `numeric-example` | "Numeric Example" | Worked computation with specific numbers | Math + reasoning | 36 |
| 9 | `production-pattern` | "Production Pattern" | Named pattern with "what/when-not-to-use" | Bold sub-labels | 36 |
| 10 | `research-frontier` | "Research Frontier" / "Open Questions" | Active research with 2024-2026 citations | 2-3 paragraphs | 207 |
| 11 | `library-shortcut` | "Library Shortcut" | pip install + minimal working snippet | Prose + code block | 162 |
| 12 | `algorithm` | "Algorithm X.Y.Z" | Pseudocode using `algo-line-keyword` spans | `<pre><code class="lang-text">` | 39 |
| 13 | `note` | "Note" | General informational supplement | 1 paragraph | 369 |
| 14 | `tip` | "Tip" / "Pro Tip" / "Production Tip" | Actionable hint | 1 paragraph | 278 |
| 15 | `warning` | "Warning" / "Caution" | Common mistake or pitfall | 1 paragraph | 425 |
| 16 | `fun-note` | "Fun Fact" | Textual humor or trivia (NOT illustrations) | 1 paragraph | 219 |
| 17 | `lab` | "Lab: \<Title\>" | Hands-on exercise with lab-meta/objective/skills/prereqs/steps/expected/stretch | Multi-section structure | 45 |
| 18 | `exercise` | "Exercise N.M.K" | Practice problem with `<details><summary>Answer Sketch</summary>` | Question + collapsible answer | 950 |
| 19 | `self-check` | "Self-Check" | Q&A quiz (`<div class="quiz-question">` + `<details>Show Answer</details>`) | 2-4 Q&A pairs | 270 |
| 20 | `postmortem` | "Postmortem" / "Lessons Learned" | Production-incident analysis | Multi-paragraph narrative | 27 |
| 21 | `thesis-thread` | "Thesis Thread" | Recurring book-wide argument tied to current section | 1 paragraph | 8 |

**Total: 4,265 callouts across 21 canonical types.**

## Retired types

- `pathway` — retired 2026-05-18 (wave 69). Was used for both front-matter pathway narratives AND chapter-index learning-objectives. Replaced by `note` callout. Front-matter Reading Pathway feature (`<section class="pathway">`, `.pathway-card`, `.pathway-grid`) is a separate concept and remains.

## Recommended ordering within a section

The canonical section flow:

```
<header> + breadcrumb + h1
<main>
  1.  epigraph                        (blockquote.epigraph, single)
  2.  big-picture                     (callout, "why this matters")
  3.  prerequisites                   (div.prerequisites with h3, single)
  4.  body content                    (h2 subsections, prose, figures, code,
                                       interspersed callouts: key-insight,
                                       practical-example, numeric-example,
                                       note, tip, warning, fun-note,
                                       library-shortcut, production-pattern,
                                       algorithm, postmortem, see-also)
  5.  research-frontier               (callout, single, optional)
  6.  lab                             (callout, single, optional)
  7.  key-takeaway                    (callout, single, end-of-section summary)
  8.  self-check                      (callout, single, Q&A quiz)
  9.  exercises                       (section.exercises with multiple callout.exercise)
  10. whats-next                      (callout, single, transition)
  11. bibliography                    (details.bibliography-collapsible, single)
  12. chapter-nav                     (nav.chapter-nav)
  13. footer                          (inside </main>)
</main>
```

### Singleton rules
These callouts MUST appear at most ONCE per section:
- big-picture
- prerequisites (div)
- key-takeaway
- self-check
- whats-next
- bibliography (details)

### Plural-allowed callouts
These may appear multiple times within a section:
- key-insight (multiple aha-moments)
- practical-example (multiple scenarios)
- numeric-example
- note / tip / warning
- fun-note (max ~2 per section recommended)
- library-shortcut (one per relevant library)
- production-pattern
- algorithm
- cross-ref (See Also)
- postmortem
- research-frontier (typically one, but multiple permitted in survey sections)

### Cross-section variation
- Reference sections (tools-of-the-trade, appendix) MAY omit: epigraph, prerequisites, whats-next, big-picture.
- Lab-heavy sections MAY have lab as the dominant block.

## Audit enforcement

The following plugins enforce this catalogue:

| Plugin | Enforces |
|--------|----------|
| `p2_callout_canonical_structure` | CANONICAL_TYPES set, callout-title presence, no h3/h4 as title |
| `p2_callout_title_prefix` | Title starts with canonical prefix per type |
| `p1_structural_violations` | DUPLICATE_SINGLETON, DOUBLE_TITLE_PREFIX, KEY_INSIGHT_BOLD |
| `p2_key_insight_vs_takeaway` | List-in-key-insight or single-paragraph-in-key-takeaway |
| `p2_see_also_canonical` | Title="See Also" + ≥1 anchor link |
| `p1_section_ordering` | Big-picture before prerequisites; nothing after bibliography |
| `p1_section_page_layout` | Required + recommended elements per section |
| `p2_pseudo_callout` | Bare `<div class="note">` etc. without "callout" prefix |
