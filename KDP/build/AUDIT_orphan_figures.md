# Orphan Figure Caption Audit

Generated: 2026-05-15
Script: `KDP/build/_audit_orphan_figures.py`
JSON detail: `KDP/build/AUDIT_orphan_figures.json`

## Scope

Scanned every `.html` file under the repository root, excluding `node_modules`,
`.git`, `.github`, `pagefind`, `temp_epub`, `.html2pub_cache`, `vendor`,
`KDP/build`, `KDP/output`, `KDP/html2pub`, and every `source_fix_backups`
subtree.

## What we look for

| Cat | Issue | Detection rule |
|-----|-------|----------------|
| A   | Orphan `<figcaption>` | `<figcaption>` whose `<figure>` parent has **no** `<img>/<svg>/<pre>/<table>/<iframe>/<canvas>/<video>/<audio>/<object>` descendant and no `.diagram-container` / `.mermaid` / `.katex-display` descendant. |
| B   | Unresolved `Figure X.Y` reference in prose | Pattern `Figure <label>` (label = optional letter + digits + dotted sub-labels, optional trailing letter) appears in text outside captions, but no figure with that exact label is declared anywhere in the book. |
| C   | Orphan `.diagram-caption` div | `<div class="diagram-caption">` with no `<img>/<svg>/<pre>/<table>/...` sibling and no such descendant inside its `figure` / `.diagram-container` / `.figure-container` / `.illustration` parent. |
| D   | Empty `<figure>` wrapper | `<figure>` whose only child (besides whitespace) is the `<figcaption>`. |
| E   | Sibling-orphan `<figcaption>` | `<figcaption>` not contained in any `<figure>` ancestor. |

## Headline results

| Metric | Count |
|--------|-------|
| Total figures with captions (figcaption + diagram-caption + Figure-labelled table caption) | **605** |
| Category A — orphan figcaptions (caption without image) | **0** |
| Category B — unresolved Figure-X.Y refs in prose | **1** |
| Category C — orphan `.diagram-caption` divs | **1** |
| Category D — empty `<figure>` wrappers | **0** |
| Category E — sibling-orphan figcaptions | **0** |

The book is in excellent shape on this dimension: 605 figure captions across the
repo and only **2 issues** require action. The recent 2026-05-15 SVG-conversion
pass (backups under `KDP/build/source_fix_backups/2026-05-15-figures/`) is
verified: every appendix-S/T/U section that had a `<pre>` ASCII diagram
replaced by an `<svg>` now has the SVG present alongside its `<figcaption>`.

## All issues (only 2)

### Issue 1 — Category C, orphan diagram caption

- **File:** `part-6-agentic-ai/module-21-ai-agents/section-21.5.html`
- **Label:** Figure 21.5.1
- **Anchor markup (lines 59-61):**

```html
<div aria-label="Reference architecture diagram for an end-to-end agent system"
     class="diagram-container" role="img">
<div class="diagram-caption"><strong>Figure 21.5.1</strong>: Reference architecture
  for a production agent system. ...</div>
</div>
```

The `.diagram-container` carries the correct ARIA metadata but contains **no
image, no SVG, and no ASCII-art `<pre>`** — only the caption. The surrounding
prose ("The following diagram describes the reference architecture.") promises a
diagram that never renders. This is the most user-visible defect found.

- **Recommended action:** **CREATE** the diagram (option a).
- **Diagram concept (for `technical-diagram-designer`):** Linear pipeline of 8
  labelled boxes — *Permissions Gate → Cost Controller → Memory Manager →
  Planner → Tool Router → Execution Sandbox → Evaluator → Recovery Handler →
  Response* — solid arrows for the happy path and dashed feedback arrows from
  Evaluator back to Planner / Tool Router to indicate recovery / retry loops.
  Roughly 900x300 SVG to match other appendix diagrams.

### Issue 2 — Category B, unresolved Figure ref

- **File:** `part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.1.html`
- **Line 111:** *"That figure zooms in on the final RL step. To see how it fits
  into the full ChatGPT-style training journey, Figure 16.1.1b zooms out and
  shows all three stages..."*
- **Problem:** Module 16 owns no `Figure 16.1.1b`. The very next paragraph
  in the same file shows the actual three-stage diagram with caption **Figure
  17.1.1b**. The "16" is a typo.
- **Recommended action:** **REPHRASE** the reference (option d) — replace
  `Figure 16.1.1b` with `Figure 17.1.1b`.

### Bonus finding (out of scope but cheap)

While verifying Issue 2, I noticed two **malformed close tags** on the two real
figure labels in the same file (lines 109 and 114):

```
<figcaption><strong>Figure 17.1.1a<\strong>: ...
<figcaption><strong>Figure 17.1.1b<\strong>: ...
```

Should be `</strong>` not `<\strong>`. Browsers tolerate this but it leaks
through into EPUB/Kindle rendering. Likely worth fixing in the same PR as
Issue 2 since they are adjacent.

## Effort estimate

| Issue | Type | Effort |
|-------|------|--------|
| 21.5.1 missing reference diagram | CREATE (SVG, ~8-box pipeline) | 30-45 min via `technical-diagram-designer` skill |
| 17.1 "Figure 16.1.1b" typo | REPHRASE (one-character edit) | 1 min |
| 17.1 `<\strong>` close tags (bonus) | TYPO fix | 1 min |

**Total**: under one hour. No content needs to be authored from scratch beyond
the one missing pipeline diagram. No delete-only or rename-only issues exist.
No category A/D/E issues anywhere in the book.

## Verification of the SVG conversion pass

Files restored from `2026-05-15-figures/` backups all have valid figure
content now:

| Section | figcaptions | svg | pre |
|---------|-------------|-----|-----|
| `section-s.5` | 3 | 1 | 5 |
| `section-t.2` | 2 | 2 | 4 |
| `section-t.4` | 1 | 1 | 11 |
| `section-t.6` | 1 | 1 | 5 |
| `section-t.7` | 1 | 1 | 5 |
| `section-u.1` | 2 | 1 | 6 |
| `section-u.2` | 2 | 1 | 8 |
| `section-u.3` | 1 | 1 | 8 |

The audit confirms 0 figcaptions in those sections are orphaned: the remaining
non-SVG captions wrap valid `<table>` elements (S.5.2, S.5.3) or other
content-bearing children.
