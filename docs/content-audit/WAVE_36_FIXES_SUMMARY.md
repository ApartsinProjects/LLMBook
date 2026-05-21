# Wave 36: Image Generation + Callout Title Prefix + Giant-Section Detector

**Date:** 2026-05-17 (4th turn)
**Branch:** v2.0

User asks addressed:
1. Extended 8-field RWS canonical confirmed (sweep deferred — can't author missing fields)
2. Callout titles: descriptive but must start with canonical type word
3. Gemini key found in `.env.all`; gitignored `.env*` patterns
4. Audit for giant / forcibly-merged sections — should split?

## Deliverables

### Infrastructure
- `scripts/_load_env.py`: dotenv-style loader for `.env.all` (32 keys including GEMINI_API_KEY).
- `.gitignore`: added `.env`, `.env.*`, `**/.env`, `**/.env.*` patterns. Confirmed `.env.all` is NOT tracked.

### New plugins (2, total now 85)
| File | Priority | CHECK_ID | Description |
|---|---|---|---|
| `p1_giant_section.py` | P0/P1/P2 | `GIANT_SECTION` | Section with line count and/or h2 count well outside typical envelope. Joint thresholds: P0 if both >1200 lines AND >10 h2; P0 if >1700 lines alone |
| `p2_callout_title_prefix.py` | P2 | `CALLOUT_TITLE_PREFIX` | Callout title doesn't start with canonical type word (e.g. `<div class="callout key-insight"><div class="callout-title">Why X works</div>` should be "Key Insight: Why X works") |

### Fix sweeps applied
| Wave | Description | Files | Items |
|---|---|---|---|
| 36a | Callout titles prefixed with canonical type word ("Key Insight:", "Real-World Scenario:", "Warning:", "Note:", "Tip:", "Fun Fact:", etc.) — preserves descriptive text after the prefix | 411 | **4,626** titles |
| 36b | 8 part-landing hero images generated via Imagen 4.0 (Kurzgesagt-meets-XKCD style) | 8 | 8 PNGs (~700KB-1.5MB each) |
| 36b | 29 chapter-opener hero images generated via Imagen 4.0 (19 first batch + 10 retry batch for 429s) | 29 | 29 PNGs |
| 36c | Chapter-opener `<figure class="illustration chapter-opener">` markup wired into 49 chapter-index pages | 49 | 49 figure blocks |
| 36c | Part-opener `<figure class="illustration part-opener">` markup wired into 8 part-index pages | 8 | 8 figure blocks |

**Total image work**: 37 new images generated + 57 pages wired = 94 image-related changes.

### Detection results

**GIANT_SECTION** finds 87 candidates (4 P0 + 22 P1 + 30 P2 — varying):
- **Tier 1 (definite splits, 3)**: section-40.1, section-50.1, section-52.1 — all have explicit duplicate-h2 markers
- **Tier 2 (probable splits, 4)**: section-19.2 (2249 lines!), section-37.3, section-3.1, section-3.3
- **Tier 3 (borderline, 8)**: long single-axis but other axis normal
- **Tier 4 (tools-of-the-trade pattern, 15)**: many small h2 = canonical TOTT format, NOT merged
- Full curated list with split-procedure guidance: `docs/content-audit/split_candidates.md`

**CALLOUT_TITLE_PREFIX** found 1,016 issues; sweep applied 4,626 prefixes (broader because some titles had multi-word non-canonical prefixes that mapped to "needs canonical addition"); validator now reports **0 issues** book-wide.

## .env.all status

- `GEMINI_API_KEY` confirmed present in `.env.all` and loaded into env.
- 32 keys total in `.env.all` (Anthropic, OpenAI, Cohere, Groq, Together, Tavily, HF, Cloudflare, Render, etc.).
- `.env.all` is NOT git-tracked (verified via `git ls-files --error-unmatch`).
- `.gitignore` updated with comprehensive `.env*` patterns.

## What now works after Wave 36

- ✅ Every part landing has a Kurzgesagt-style hero image.
- ✅ Every chapter index has a Kurzgesagt-style hero image.
- ✅ Every callout title starts with the canonical type word.
- ✅ Google Analytics (G-PWPHBQL2VL) tracking active on all 544 pages.
- ✅ Plugin harness has 85 checks running on `LLMBook/` root.

## What remains

### User decisions needed
- Tier 1 / Tier 2 section splits (changes URLs and cross-references — needs your green light).
- RWS template extended-canonical sweep (can't author missing Problem/Dilemma/Decision/How fields for 312 callouts; mechanical reorder for callouts that DO have all 8 fields is possible).

### Authoring backlog (not script-fixable)
- 213 sections need self-check answers authored
- 200 sections need epigraphs
- 199 sections need What's Next prose
- 127 sections need bibliographies (Ch 34, Ch 46 are entirely barren)
- 55 chapter Learning Objectives + 54 Looking Back callouts + 53 Chapter Overviews + 54 Prerequisites blocks
- 151 FM4 chapter feature promises
- 247 fun-note (comic) callouts could be authored + illustrated

### Hold v2.0
Production stays tagged `production-v1.0`; v2.0 not merged.
