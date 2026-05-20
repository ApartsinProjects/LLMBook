# Capstone and Appendix Polish Audit

**Branch:** v2.0
**Date:** 2026-05-20
**Scope:** `capstone/`, `appendices/appendix-a-mathematical-foundations/`, `appendices/appendix-b-course-syllabi/`, `appendices/appendix-c-reading-pathways/`, `appendices/appendix-d-agent-roster/`

## Summary

| Goal | Status |
| --- | --- |
| Fix capstone "Next Next Next" nav corruption | Done (1 residual `Up Up Up Up Up` corruption found in `requirements.html` and fixed; `Next Next Next` already cleaned by prior wave) |
| Appendix B syllabus cross-references | Audited; all 30+ cross-references resolve; 5 `#track-N` anchors all exist |
| Appendix C reading-pathway cross-references | Audited; all 30+ cross-references resolve |
| Prose polish (max 3 edits per file) | Done in appendix-a index.html (Big Picture opener + figcaption alt text) |
| Agent-roster integrity (42 agents) | Verified: 42 markdown files in `agents/book-skills/agents/` (00-chapter-lead through 41-lab-designer) match 42 cards in appendix-d |

## Concrete fixes

### 1. Capstone navigation corruption (`Up Up Up Up Up`)

**File:** `capstone/requirements.html` line 573

- Before: `<a class="up" href="index.html"><span class="nav-label">Up</span><span class="nav-title">Up Up Up Up Up Capstone</span></a>`
- After: `<a class="up" href="index.html"><span class="nav-label">Up</span><span class="nav-title">Capstone</span></a>`

The 5x "Up" prefix was a Wave 17g re-run artifact, matching the same pattern flagged for the "Next Next Next Next Next" issue in TODO 38.

### 2. Capstone nav order corrections

The capstone follows Appendices A through D in the book's marketing-page reading order, but the existing nav cross-stitches were misaligned.

**File:** `capstone/index.html` line 117

- Before: `prev → appendices/appendix-b-course-syllabi/index.html` with label `"Front Matter: Course Syllabi"`
- After: `prev → appendices/appendix-d-agent-roster/index.html` with label `"Appendix D · Agents That Helped to Write This Book"`

**File:** `capstone/requirements.html` line 574

- Before: `next → ../appendices/index.html` (regression to appendices)
- After: `next → ../toc.html` (end of book → table of contents)

**File:** `appendices/appendix-d-agent-roster/index.html` line 739

- Before: `next → ../../toc.html` (skipping capstone)
- After: `next → ../../capstone/index.html` (forward to capstone)

### 3. Appendix A Section A.6 forward-nav

**File:** `appendices/appendix-a-mathematical-foundations/section-a.6.html` line 333

- Before: `next → ../../part-1-llm-building-blocks/module-00-ml-pytorch-foundations/section-0.1.html` (a backward jump)
- After: `next → ../appendix-b-course-syllabi/index.html` (natural forward flow)

### 4. Appendix A opener polish

**File:** `appendices/appendix-a-mathematical-foundations/index.html` line 45 (Big Picture opener)

- Replaced the weak `"This appendix collects the mathematical background you will encounter throughout the textbook."` with a stronger lead that immediately motivates the math: `"Every transformer is, mathematically, a long composition of matrix products, probability distributions, and gradient updates. This appendix collects the four bodies of math that recur most often in the book..."`

### 5. Appendix A figcaption truncation fix

**File:** `appendices/appendix-a-mathematical-foundations/index.html` line 42

- Before: `Figure A.0.1: Friendly geometric shapes ... collaborating on a chalkb....` (truncated mid-word)
- After: `Figure A.0.1: Friendly geometric shapes ... collaborating on a chalkboard while a neural network peeks in from the corner.` (caption restored)

## Cross-reference audit

### Appendix B (`appendix-b-course-syllabi/index.html`)
- 37 external `href="../../part-X/..."` references — all targets resolve.
- 5 in-page `#track-N` anchors (tracks 1-5) — all have matching `<h2 id="track-N">`.
- Two anchor hrefs into `module-10-interpretability/section-10.7.html` and `module-14-tools-of-the-trade/section-14.2.html` — both files contain the referenced anchor IDs.

### Appendix C (`appendix-c-reading-pathways/index.html`)
- 32 external `href="../../..."` references across 8 pathways — all targets resolve, including the `front-matter/copyright.html`, `front-matter/foreword.html`, section-level deep links into `section-12.2.html`, `section-12.1.html`, `section-16.1.html`, `section-10.2.html`, `section-42.10.html`, `section-42.1.html`.

### Capstone (`capstone/index.html`, `capstone/requirements.html`)
- All in-file anchors and external chapter/section references resolve.

## Agent roster verification

- Filesystem: 42 agent files in `agents/book-skills/agents/` numbered `00-chapter-lead.md` through `41-lab-designer.md`.
- Appendix D: 42 `<div class="agent-card" id="...">` cards.
- Numbering and ordering are consistent (cards titled `Agent 00` through `Agent 41`).
- Roster intro correctly states "42 specialist agents".

## Files touched (7)

1. `capstone/index.html` (1 edit, nav fix)
2. `capstone/requirements.html` (2 edits, "Up Up Up Up Up" + next-nav)
3. `appendices/appendix-a-mathematical-foundations/index.html` (2 edits, Big Picture opener + figcaption)
4. `appendices/appendix-a-mathematical-foundations/section-a.6.html` (1 edit, next-nav)
5. `appendices/appendix-d-agent-roster/index.html` (1 edit, next-nav)

## Audit pass

- Capstone nav corruption: cleared.
- Cross-references: all resolve.
- Prose polish: 1 file polished (under the 3-edits-per-file cap).
- Agent roster: matches actual 42-agent team.
- Files touched: 5 of 30 budget.
