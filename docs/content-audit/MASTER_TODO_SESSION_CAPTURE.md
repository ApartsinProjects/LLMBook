# MASTER TODO — Session Capture (everything not forgotten)

Last refresh: 2026-05-18 (session continuation segment, post Round 16).

This is the **single comprehensive todo** that captures EVERY item from:
- The 2097-issue current audit
- User feedback Rounds 1-17 (file-specific bugs, structural concerns)
- In-flight agent results
- Outstanding decisions
- Image-opportunity backlog

Refresh trigger: run `/c/Python314/python scripts/run_book_audit.py --json` and
diff against this document.

---

## 0. State of the union (2026-05-18 post-Round-17)

- **Total audit issues**: 1975 (down from 7906 at session start; 75.0% reduction)
- **Commits this session continuation**: 76+ on branch v2.0
- **Background agents landed**:
  - `ac7c3ef3` — Scientific depth (foundational, 24 algo callouts in 9 modules). LANDED.
  - `a5c8c689` — Scientific depth (safety/ethics, 12 algo callouts in Part 10 + 11). LANDED.
  - `aed76e8e` — Image generation (108 HIGH+MED placeholders inserted with prompts ready for batch Gemini run). LANDED.
- **Background agents in flight**:
  - `aa13e1db` — Bibliography backfill (114 sections missing `<details class="bibliography-collapsible">`).
  - `afbd35d9` — Chapter-starter (54 chapter-index overview + 57 learning-objectives).
- **v2.0 held**. Production main untouched.

---

## A. Background image generation (HIGH+MED tier — user-approved)

Budget per `DISPATCH_BUDGET_AND_AGENT_PLAN.md`:
- HIGH: 98 figure-poor sections (>1000 words, no figure/diagram)
- MED: ~80 comic/fun-note slots in priority chapters

Total: ~178 image generations. Estimated $8 API cost + ~11 hr dispatch+wire.

**Plan**: Dispatch agent to generate placeholder/SVG diagrams for HIGH
sections, and fun-note comic prompts for MED sections.

---

## B. Authoring-heavy buckets (need agents, not sweeps)

### B.1. SECTION_PAGE_LAYOUT (374, top non-image bucket)
- 139 missing prerequisites block
- 114 missing bibliography-collapsible
- 106 missing epigraph
- 15 missing big-picture callout
- 0 missing whats-next (cleared in waves 87/88)

**Dispatch**: bibliography agent + prereqs/epigraph agent.

### B.2. CHAPTER_INDEX_LAYOUT (291)
- 83 missing Prerequisites
- 57 missing Learning Objectives
- 55 missing looking-back callout
- 54 missing chapter overview block
- 41 missing canonical epigraph
- 1 missing canonical whats-next (residual)

**Dispatch**: chapter-starter agent (overview + learning-objectives).

### B.3. SECTION_STRUCTURE (149)
- 106 missing epigraph
- 22 missing takeaway/key-insight
- ~21 other (no callouts, last-section issues)

### B.4. CHAPTER_STARTER (109)
- 57 missing learning objectives
- 52 missing chapter overview section

### B.5. FM4_PROMISE (47)
- 26 missing Research Frontier callout
- 18 missing exercise or self-check
- 2 missing Warn callout
- 1 missing Key Insight

### B.6. LAB_COVERAGE (44)
44 chapters lack a hands-on lab.

### B.7. MISSING_OUTPUT (62)
print() found without .code-output following. Per-file: either remove
the print() if it's internal, or add the actual output. Needs author
to RUN the code or judge intent.

### B.8. GIANT_SECTION (62)
63 sections flagged as >600 lines. 7 high-confidence SPLIT recommendations
in `GIANT_SECTION_RECOMMENDATIONS.md` await user approval.

---

## C. Mechanical fixes possible (no agent needed)

### C.1. CALLOUT_INTERNAL (32)
- 14 callouts with 2+ callout-title divs (mostly nested callouts inside labs/exercises)
- 7 labs without sub-headings (h3 Objective/Steps/Expected output)
- 3 self-check callouts without `<details>`
- 2 labs with nested h2 (double-header)
- 1 fun-note + 1 practical-example with double callout-title
- 1 key-takeaway without `<ul>`

### C.2. LIBRARY_SHORTCUT_HAS_CODE (16)
Library-shortcut callouts without a `<pre><code>` snippet. Either
add code or demote to tip callout.

### C.3. WRONG_NESTING (13)
- 10 labs containing a sub-callout (library-shortcut, note, tip, warning)
- 1 fun-note containing a cross-ref
- 1 exercise containing a self-check
- 1 lab containing a warning

### C.4. NON_CALLOUT_LAB (13)
Lab heading not followed by a `<div class="callout lab">` block.

### C.5. CODE_BLOCK_WRAPPER (9)
Bare lang-text pseudocode outside algorithm callouts. Convert each to
a proper algorithm callout or wrap in code-block-wrapper.

### C.6. DIAGRAM_BOTTOM_CAPTION (4)
SVG bottom banners duplicating figcaption text.
- section-12.1.html:151
- section-59.2.html:168
- section-59.3.html:171
- section-59.4.html:351

### C.7. SVG_TITLE_TEXT (12)
Inline SVG title text near bottom. Already exempt for descriptive
aria-labels; remaining 12 may need aria-label improvements.

### C.8. CODE_FRAGMENT_STRUCTURE (4)
- Two consecutive `<div class="code-output">` blocks (3 files)
- Code block wrapped in `<details>` instead of code-block-wrapper

### C.9. HEADING_HIERARCHY (9)
- h1 -> h3 skip in 5 section files
- h2 -> h4 skip in 2 section files
- 2 capstone/specialized cases

### C.10. MATH_RENDERING (10)
KaTeX/MathJax entity edge cases.

### C.11. STRUCTURAL_VIOLATION (6)
Various: nested singletons, layout violations.

### C.12. PSEUDO_CALLOUT (4)
Markup that looks like a callout but uses wrong wrapper.

### C.13. CAPTION_MISALIGN (6)
Caption text doesn't match figure content (per author review).

### C.14. SVG_PANEL_ASYM (5)
SVG panels with asymmetric dimensions.

### C.15. SVG_OVERLAP (21)
SVG elements overlapping in rendering.

### C.16. SVG_TEXT_OVERFLOW (11), SVG_TEXT_CLIPPING (120), SVG_TEXT_RIGHT_CLIP (56)
SVG text overflowing the viewBox. ~187 SVG redesigns.

### C.17. CONSECUTIVE_HEADINGS (52)
h2 followed immediately by h3 with no transition prose. Each needs
1-3 sentences of transition.

### C.18. CALLOUT_ORDER (51)
51 sections where singleton callouts appear in wrong order
(e.g., key-takeaway after self-check). Per-file reorder.

### C.19. MANUAL_HIGHLIGHT_SPANS (5)
Hardcoded color highlight spans bypassing the design tokens.

### C.20. Misc (1 each)
- BROKEN_FIGURE_REF: 1 prose reference to non-existent figure
- UNESCAPED_AMPERSAND_TITLE: 1 file
- UNCLOSED_P_TAG: 1
- TRIPLE_DOLLAR_MATH: 1
- DECISION_FRAMEWORK_EARLY: 1
- INDEX_ORDER: 1
- SELFCHECK_NON_CANONICAL: 1
- MISSING_IMG_DIMS: 1 (broken src)
- BOLD_DENSITY: 2
- KEY_INSIGHT_VS_TAKEAWAY: 2
- NAV_LINEAR_CHAIN: 2

---

## D. User-reported file-specific bugs (Rounds 14-17)

### Resolved during the session
- section-3.6.html: algorithm bold + lab + further-reading + see-also (DONE)
- section-3.7.html: "Warning: Common Misconception" double prefix (DONE)
- section-3.8.html: warning icon-title same line + key-takeaway nested in takeaways (DONE)
- section-4.1.html: Algorithm 5.1.2 ↔ Code Fragment 4.1.3 mixup (DONE)
- section-4.2.html: Table 4.2.1 unwrap + 4.2.9 Lab structured (DONE)
- section-4.3.html: key-takeaway double title (DONE)
- section-5.1.html: See Also red hover (hardened with body-prefixed override; user reports re-test)
- section-18.1.html: double headers/icons in key-takeaways (DONE; 8 files cleaned)
- section-29.1.html: See Also red hover (DONE via 5.1 fix) + double lab title (DONE)
- section-29.3.html: non-standard code in library shortcut (Wave 94 cleaned 647 bare blocks)
- section-54.4.html: orphan prose merged into whats-next; bottom banner dropped
- section-57.4.html: stray h2 inside key-takeaway (DONE)
- section-58.1.html: &amp;amp; in header (DONE; 203 files cleaned in wave 92)
- module-57/index.html: hero image prompt leak (DONE; 106 figures cleaned in wave 91)

### User asks awaiting action
- "Read section by section, what additional algorithms/models should be included" — IN FLIGHT (agents ac7c3ef3 + a5c8c689)
- "Avoid high-level fluff and shopping list sections" — IN FLIGHT (safety/ethics agent)
- 482 IMAGE_OPPORTUNITY backlog — agent to dispatch (HIGH+MED tier per user)

---

## E. Scripts and validators added this session

### Mechanical waves (numbered)
- Wave 82: chapter card clickable (83 cards, 16 part-indexes)
- Wave 83: part-index whats-next + chapter-nav (16 parts)
- Wave 84: appendix-A h3 -> h2 (4 sections, 16 headings)
- Wave 85: part-overview wrap (8 parts)
- Wave 86: chapter-index whats-next + pagefind meta (51 files)
- Wave 87: section whats-next (124 sections)
- Wave 88: last-section cross-chapter whats-next (22 sections)
- Wave 89: PIL img dims (17 imgs, 13 files)
- Wave 90: unwrap takeaways wrapper (11 files)
- Wave 91: hero image prompt cleanup (106 figures)
- Wave 92: &amp;amp; -> &amp; (203 files)
- Wave 93: key-takeaway double-header dedup (8 files)
- Wave 94: bare code -> code-block-wrapper (647 blocks, 207 files)

### Plugin updates
New plugins added (8):
- p1_wrong_nesting
- p2_bold_fraction
- p2_library_shortcut_has_code
- p2_non_callout_lab
- p2_callout_internal_compliance
- p2_diagram_bottom_caption
- p2_code_block_wrapper
- (built-in scientific depth catalog via reports)

Plugin tunes (11): see commits.

### Reports
- `MASTER_TODO_CONSOLIDATED.md` — earlier consolidation
- `MASTER_TODO_SESSION_CAPTURE.md` — THIS doc
- `GIANT_SECTION_RECOMMENDATIONS.md` — 63 sections SPLIT/KEEP/TRIM
- `DISPATCH_BUDGET_AND_AGENT_PLAN.md` — image budget + agent map
- `SECTION_DISPATCH_INDEX.jsonl` — per-section dispatch metadata (556 records)
- `SCIENTIFIC_DEPTH_ADDITIONS.md` (pending) — by foundational agent
- `SAFETY_ETHICS_DEPTH_REPORT.md` (pending) — by safety/ethics agent

---

## F. Next-step priority order (autonomous loop)

While agents work, the parent should:
1. **Mechanical sweeps** for Categories C.1-C.6 (32 + 16 + 13 + 13 + 9 + 4 = 87 fixable).
2. **Front-matter / appendix gap fills** (smaller, isolated).
3. **Caption/title cleanup** for the 4 DIAGRAM_BOTTOM_CAPTION residuals.
4. **CONSECUTIVE_HEADINGS transition prose** — dispatch as a follow-on agent.
5. **CALLOUT_ORDER reorder** — per-file editorial.
6. **Wait for depth agents to land**, then commit, then dispatch:
   - image generation agent (HIGH+MED tier)
   - bibliography agent (114 sections)
   - chapter overview / learning objectives agent (109+ chapter pages)

---

## Hold v2.0; no merge to main.
