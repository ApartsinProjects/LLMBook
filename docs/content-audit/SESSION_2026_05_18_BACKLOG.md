# Session Backlog: 2026-05-17/18 Audit-Fix Marathon

## Status
- **v2.0 branch only — NEVER merge to main**.
- Cumulative reduction: 7906 → 2982 issues (62.3%) across 31 audit cycles.
- 7 checkpoint commits landed on v2.0 (see git log).

## User-Reported Root Causes (chronological)

### Round 1 (initial complaints)
- ✅ Duplicate whats-next in section-40.1 (turned out section had 0 dupes; plugin added for detection)
- ✅ Key Insight starts with bold (section-40.3) → 147 unwrapped book-wide
- ✅ Double-title "Key Insight: Key Takeaways" → 153 collapsed + 150 class realigned
- ✅ Bibliography canonicalization → 21 bare-ref blocks wrapped + 1 summary normalized + 4 dup-bib merged
- ✅ Nested callouts at end (section-16.3) → 5 module-16 sections repaired + nested-tail catch
- ✅ Module index second image duplicates opener → 20 body figures removed
- ✅ Single lab split into two callouts (section-13.5) → ROOT CAUSE in scripts/book.js fixed
- ✅ Legacy whats-next + canonical whats-next coexisting → 2 legacy dups removed
- ✅ ToC/nav/cross-refs after splits → verifier agent repaired everything

### Round 2 (newer complaints)
- ✅ Code Fragment 26.5.1 box-in-box → 8 nested-note "Example output" → canonical code-output
- ✅ Code Fragment 26.5.6 non-standard format → agent dispatched
- ✅ 26.6.1 fun-fact with image → 33 unwrapped to bare figures
- ✅ 27.1 double bibliography header → root cause in book.js fixed (skip JS wrap inside canonical details)
- ✅ 27.2.1 Real-World Scenario non-standard format → agent dispatched
- ✅ 27.2 "Algorithm: Pseudocode N.M.X:" double-prefix → 15 collapsed
- ✅ 27.5.2 figure inside fun-fact → included in 33 unwraps
- ✅ 31.2 math/pseudocode formatting → agent dispatched
- ✅ 31.4b lab split → fixed by book.js update from Round 1
- ✅ 31.4b bibliography wrong title → fixed by book.js bib-wrap skip
- ✅ 31.5 key-takeaway box — IS canonical
- ✅ 32.1 canonical-reference → 17 renamed to "See also"; agent dispatched to introduce See Also callout type
- ✅ Lab callout standard layout → agent dispatched to audit
- ✅ Key Insight vs Key Takeaway distinction → agent dispatched to clarify via tooltips

### Round 3 (latest)
- ⏳ 33.4 research-frontier — consider justified text book-wide
- ⏳ 34.1.3 figure inside fun-fact (still some — pattern was fun-note WITH text + figure, my regex only caught figure-only)
- ⏳ JPEG vs PNG for non-diagram images (size optimization)
- ⏳ Pagefind search restoration
- ⏳ Make sure todos saved (this file)

## Plugin Updates (14 plugins improved for accuracy)

1. p2_code_no_language: accept `lang-X` (Pygments) not just `language-X`
2. p2_pseudo_callout: drop aside/blockquote checks; lookahead for canonical callout; accept .takeaways wrapper
3. p2_mixed_caption_style: disabled (intentional caption diversity)
4. p2_heading_hierarchy: skip headings inside meta-wrappers (prereqs, callouts, aside.section-internal-toc)
5. p2_consecutive_headings: recognize canonical Lab Steps/Part Overview pairs; skip h3 inside meta wrappers
6. p1_caption_misalignment: handle same-line PRE_CLOSE+CAPTION; 40-line lookback for code-output
7. p2_callout_canonical_structure: added key-takeaway to canonical set
8. p0_dup_figure_num: surgical caption-only first-number check; regex fix for X.Y.Z.W vs X.Y.Z
9. p1_section_structure: exempt tools/appendix from epigraph requirement; accept key-takeaway
10. p1_section_page_layout: accept callout whats-next; exempt tools/appendix
11. p2_lab_coverage: accept callout lab class; exempt tools-of-the-trade
12. p1_self_check_canonical: balanced-div parser (was missing details inside)
13. p1_section_ordering: exempt tools-of-the-trade + appendix modules
14. p3_math_rendering: &#36; entity → $ before counting delimiters
15. (NEW) p1_structural_violations: DUPLICATE_SINGLETON, DOUBLE_TITLE_PREFIX, KEY_INSIGHT_BOLD, INDEX_DUPLICATE_OPENER, NON_CANONICAL_BIB

## Mechanical Sweeps (Waves 41-64)

| Wave | Description | Count |
|------|-------------|------:|
| 41 | Skip-link injection | 563 files |
| 42 | img dimensions (PIL probe) | 533 + 13 retry |
| 43 | Table thead wrapping | 213 tables / 151 files |
| 44 | Callout-prefix + th-scope | 51 + 53 |
| 45 | Prereq/big-picture order swap | 7 + 3 |
| 46 | Dup code-fragment captions | 20 renumbered |
| 47 | Lab/exercise hN → callout-title (round 1) | 19 |
| 48 | Broken xrefs (module renames) | 25 |
| 49 | Lab title outside callout (round 2) | 17 |
| 50 | Whats-next link injection | 48 |
| 51 | Big-picture lead-strong unwrap | 157 |
| 52 | Move callout before bibliography | 9 + 15 |
| 53 | Lab hN → callout-title (round 3) | 16 |
| 54 | External link target/rel | 6 |
| 55/55b | h3 → h2 promotion in new sections | 43 + 12 |
| 56 | Module-16 whats-next/fun-note/bib structure | 5 |
| 57 | Comprehensive root-cause fixes | 234 |
| 58 | Bibliography canonicalization | 21 |
| 59 | Callout class realignment to title | 150 |
| 60 round 4 | Comic image generation + wire | 12 |
| 61 | Merge duplicate bibliography | 4 |
| 62 | Remove legacy whats-next | 2 |
| 63 | Comprehensive (Algorithm/fun-note/note-output/canon-ref) | 73 |
| 64 | 10.6 K.X.Y → 10.6.N | 18 |

## Section Splits (11 splits done)

- section-50.1 + section-50.3 (pilot)
- section-19.2 + 9 new sections (19.6-19.14)
- section-47.1 + section-47.3
- section-52.1 + section-52.3
- section-3.3 + section-3.6
- section-37.3 + section-37.5
- section-40.1 + section-40.6
- section-45.2 → 44.1 + 44.2 + 44.3
- Ch 54 split into module-54 + module-54b
- section-52.2 → module-49/section-49.5
- section-55.2 → module-53/section-53.5
- section-31.4 + section-31.4b
- section-10.4 + section-10.4b
- 2 P0 dup-h2 fixed (16.4.5, 0.3.7)
- Module 16 broken-structure repair (5 sections)

## Authoring Rounds (8 rounds)

- Library-shortcut callouts: 58 sections (full catalog)
- Self-check Q&A: 6 rounds, ~150 Q&A pairs across ~60 sections
- Real-World Scenario template: 30 callouts normalized to 8-field canonical
- Industry expansion Ch 74-77: 20 sections expanded
- FM4_PROMISE structure: 47 fixes across 37 modules (222 level badges + 9 Research Frontiers)
- Structural-gap fill: 30 main-content sections (epigraph + prereqs + whats-next + big-picture)
- Smaller policy items: 52.2/55.2 moves, module-01/10 fixes, Ch 19 PEFT scope verification
- Code-sample lame audit: 31 upgraded + 8 deleted (12 files modified)

## Background Agents Status

### Completed
- Section-31.4 + section-10.4 split (created .4b siblings)
- Section-37.3 + section-40.1 splits (round 1 splits)
- Section-45.2 → module-44 redirect
- Smaller policy items (Ch 54 split + orphan moves)
- Industry expansion Ch 74-77
- Library-shortcut final batch
- Self-check Q&A round 6
- FM4_PROMISE module-level fixes
- Structural-gap fill (30 files)
- RWS template normalization (30 callouts)
- Diagram improvement audit (10 keep, 2 improve)
- ToC/nav/xref verifier (chains repaired)
- Code-sample lame audit (12 files modified)
- Comic image generation round 4 (12 images)
- Section-31.4 + section-10.4 split agent

### In flight at backlog-save time
- See Also callout introduction agent
- Lab layout audit + 26.5/27.2/31.2 misc fixes
- Image-reuse + Key Insight/Takeaway tooltip clarification

## Pending Items (Round 3 ongoing)

1. Justified text in callout bodies (CSS update)
2. fun-fact callout containing TEXT + figure (broader pattern than wave 63)
3. PNG → JPEG conversion analysis for comic images
4. Pagefind search rebuild
5. Image-reuse opportunities (in flight)
6. Lab layout audit (in flight)
7. See Also opportunities throughout (in flight)
8. Key Insight vs Key Takeaway tooltips (in flight)

## Key Decisions / Rules Confirmed

- **No em-dashes anywhere** (use commas, semicolons, colons, parens, separate sentences)
- **v2.0 branch only** — never merge to main without explicit approval
- **Hold v2.0** = work continues on v2.0; commit OK; merge to main forbidden
- **Canonical callout**: `<div class="callout TYPE"><div class="callout-title">Prefix: Title</div>...</div>`
- **Canonical lab callout-title prefix**: "Lab: <Title>" (book.js normalizes "Hands-On Lab:" → "Lab:")
- **Canonical bibliography wrapper**: `<details class="bibliography-collapsible" open><summary><strong>Further Reading</strong></summary><section class="bibliography">...</section></details>`
- **Tools-of-the-trade and appendix sections**: reference-style, exempt from narrative-element audits (epigraph, prereqs, whats-next, big-picture)
- **fun-fact ≠ fun-illustration**: fun-fact callout is text-only; figures/comics are standalone `<figure>` elements
- **Key Insight (single observation) ≠ Key Takeaways (bulleted summary)**: both canonical, distinguished by role
- **See Also (cross-ref)**: standardized title for cross-references between sections
