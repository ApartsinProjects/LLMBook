# Dispatch budget, agent plan, and section-targeting strategy

Last refreshed: 2026-05-18 (session segment continuation)

This doc answers four user-asked questions:
1. Estimate budget for the IMAGE_OPPORTUNITY backlog.
2. Which agents from `agents/book-skills/agents/` are worth running on
   (a) new sections, (b) the entire book?
3. Do we need a per-section summary to target agents without rescanning
   the book? (Yes; built `SECTION_DISPATCH_INDEX.jsonl`.)
4. What is the next-step priority list?

## 1. Image budget estimate

### Current audit state
- `IMAGE_OPPORTUNITY` flagged: **482 findings across 305 distinct files**
- Breakdown of audit messages:
  - 266 sections missing a `<div class="callout fun-note">` (comic/analogy)
  - 216 sections missing any figure or diagram (text-heavy sections)
- Many sections appear in BOTH buckets (no comic AND no figure).

### Per-image cost (Gemini 2.5 Flash Image as of 2026-05)
- API: ~$0.03-0.04 per image (1024 × 1024 JPEG, 75% quality)
- Storage: ~50-100 KB per JPEG → ~50 MB total at 482 images
- Wire-into-HTML: ~30 seconds per image (alt, caption, src, width, height,
  surrounding figcaption + tooltip)

### Total budget estimate
| Tier | Scope | API cost | Time (dispatch + wire) |
|------|------:|---------:|-----------------------:|
| HIGH only | 98 figure-poor sections with >1000 words | ~$4 | 6-8 hours |
| HIGH + MED | 98 figures + 194 comics in priority chapters | ~$12 | 14-18 hours |
| FULL backlog | 482 opportunities across 305 files | ~$20 | 24-32 hours |

### Recommended cut
- **Tier 1 (HIGH)**: 98 sections with no figure AND >1000 words. These
  are the most readability-degrading gaps. Estimated $4 API + ~6 hours.
- **Tier 2 (MED)**: Add a comic/analogy to chapters that are
  particularly text-dense (Module 8 reasoning, 18 alignment, 32 RAG,
  42 evaluation). ~80 sections, $3 API + ~5 hours.
- **Tier 3 (LOW)**: Generic fun-note coverage everywhere else. ~200
  sections, $8 API + ~10 hours.

Total Tier 1+2 budget: ~$8 API + ~11 hours of dispatch/wire work.

## 2. Available agent skills

`agents/book-skills/agents/` has **42 named agent personas**. Categorized
for dispatch:

### Run on EVERY new section (essential coverage)
| # | Agent | What it does |
|---|-------|--------------|
| 01 | curriculum-alignment | Verifies section maps to part/chapter learning objectives |
| 02 | deep-explanation | Adds problem/why/how/when for each major concept |
| 03 | teaching-flow | Ensures progressive disclosure, no leaps |
| 08 | code-pedagogy | Verifies code examples are educational, not just functional |
| 11 | fact-integrity | Citation-checks, hallucination scan |
| 13 | cross-reference | Adds See Also links to prereq/companion sections |
| 17 | senior-editor | Pass-level edit before publication |
| 29 | prose-clarity-editor | Sentence-level tightening |
| 38 | publication-qa | Final lint (matches audit plugin set) |

### Run as targeted sweeps (book-wide, gap-driven)
| Agent | Trigger from SECTION_DISPATCH_INDEX | Estimated scope |
|-------|--------------------------------------|----------------:|
| 09 visual-learning | sections with `needs_figure` (98) | ~6 hr |
| 34 fun-injector | sections with `needs_comic` (194) | ~10 hr |
| 07 exercise-designer | sections with `needs_self_check` (103) | ~5 hr |
| 41 lab-designer | sections with `needs_lab` (327) | ~16 hr |
| 35 bibliography | sections with `needs_bibliography` (68) | ~3 hr |
| 18 research-scientist | sections with `needs_algorithm_callout` (337) | ~17 hr |
| 24 aha-moment-engineer | sections with low key-insight count | ~6 hr |
| 28 skeptical-reader | text-heavy sections (>2500 words) | ~6 hr |
| 39 figure-fact-checker | every section with `figure_count` >= 3 | ~4 hr |

### Run rarely (already substantially complete)
| Agent | Status |
|-------|--------|
| 22 opening-hook-designer | Already covered by epigraph + big-picture |
| 32 epigraph-writer | 95% of sections have epigraphs |
| 33 application-example | Covered by practical-example callouts |
| 36 meta-agent | Internal coordinator; doesn't write content |
| 37 controller | Orchestrator; runs the others |

## 3. SECTION_DISPATCH_INDEX.jsonl

Built `docs/content-audit/SECTION_DISPATCH_INDEX.jsonl` with 556
records (one per content page). Each record has:

```json
{
  "path": "part-N-.../module-XX-.../section-X.Y.html",
  "is_tools_chapter": false,
  "word_count": 2847,
  "math_blocks": 4,
  "algorithm_callouts": 0,
  "citation_links": 8,
  "pseudocode_blocks": 0,
  "figure_count": 2,
  "comic_count": 0,
  "opener_present": false,
  "callout_counts": { "key-insight": 3, "warning": 1, ... },
  "has_prereqs": true,
  "has_big_picture": true,
  "has_whats_next": true,
  "has_takeaway": true,
  "has_self_check": false,
  "has_lab": false,
  "has_bibliography": true,
  "gaps": ["needs_algorithm_callout", "needs_lab", "needs_self_check",
           "needs_comic"],
  "gap_count": 4
}
```

### Top-line gap distribution (372 non-tools sections)

| Gap label | Count | Tier |
|-----------|------:|------|
| needs_algorithm_callout | 337 | HIGH (scientific depth) |
| needs_lab | 327 | HIGH (FM.4 promise) |
| needs_comic | 194 | MED (engagement) |
| needs_more_citations | 173 | MED (scholarly rigor) |
| needs_prereqs | 115 | MED |
| needs_self_check | 103 | MED |
| needs_figure | 98 | HIGH (text-heavy) |
| needs_bibliography | 68 | MED |
| needs_big_picture | 11 | LOW (almost complete) |
| needs_whats_next | 5 | LOW |

The dispatch index lets you grep/jq the JSONL for a target set
without re-reading section files. Example:

```bash
# Sections needing both an algorithm callout AND a figure (HIGH-priority
# scientific-depth + visual-learning targets):
jq -c 'select(.gaps | index("needs_algorithm_callout"))
      | select(.gaps | index("needs_figure"))
      | .path' SECTION_DISPATCH_INDEX.jsonl
```

## 4. Recommended next-step priority

1. **Wait for in-flight scientific-depth agent (ac7c3ef3)** to land
   before dispatching the research-scientist agent. The scientific
   depth agent IS the research-scientist agent's workload for the
   foundational chapters.
2. **Dispatch visual-learning agent** on the 98 figure-poor sections.
   Time: ~6 hours. Cost: ~$4 API.
3. **Dispatch fun-injector agent** for ~80 priority chapters' comics.
   Time: ~5 hours. Cost: ~$3 API.
4. **Dispatch lab-designer agent** on a curated 50-section subset of
   the 327 lab-poor sections (skip tools-of-trade derivatives).
   Time: ~10 hours.
5. **Dispatch publication-qa agent** for a final pre-merge pass once
   the above land.
