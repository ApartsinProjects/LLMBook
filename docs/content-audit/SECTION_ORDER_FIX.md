# SECTION_ORDER Fix Report (v2.0 branch, 2026-05-19)

## Summary

Fixed **30 P1 SECTION_ORDER issues** flagged by the audit. After the fix:

```bash
/c/Python314/python agents/book-skills/scripts/audit/run.py --root . --priority P1 --checks SECTION_ORDER
# -> 0 issues
```

The full P1 sweep (`--priority P1`) also reports **0 P1 issues**; the only remaining flag is a single pre-existing P2 in `section-47.1a.html` (`SECTION_PAGE_LAYOUT`) that is unrelated to this work.

## Root cause

All 30 broken sections shared a near-identical structural template defect. The intended canonical layout is:

```
<blockquote class="epigraph">
  <p>short quote</p>
  <cite>...</cite>            (or agent-avatar + cite)
</blockquote>
<div class="callout big-picture">
  <div class="callout-title">Big Picture</div>
  <p>1-paragraph overview</p>
</div>
<div class="prerequisites">
  <h3>Prerequisites</h3>
  <p>...</p>
</div>
```

The broken files all had the same five-symptom defect:

1. The `<blockquote class="epigraph">` paragraph **concatenated the quote and the intended big-picture intro** into a single `<p>`.
2. The blockquote was **closed with `</div>` instead of `</blockquote>`** (malformed HTML).
3. The actual `<cite>` (and agent avatar in most cases) was **stranded near the end** of the file as an orphan `<cite>...</cite></blockquote>` block, floating between the whats-next callout and the bibliography.
4. The `<div class="callout big-picture">` callout existed but was **empty** (only a `callout-title` div, no body) and was being used as a wrapper around the bibliography `<details class="bibliography-collapsible">`.
5. Prerequisites therefore ended up before the (empty) big-picture, violating the canonical order.

For `section-47.1b.html` the same defect was present *plus* two extras:
- An `<aside class="section-internal-toc">` was nested *inside* the epigraph blockquote and absorbed the intro prose.
- The whats-next `<div>` was closed with `</aside>` (typo), which left the heading and the orphan big-picture wrapper landing between whats-next and bibliography.

## Approach

A single script (`agents/book-skills/scripts/audit/fix_section_order.py`) performs the transformation idempotently on 27 of the 28 files. It:

1. Parses the `<blockquote class="epigraph">` paragraph and splits it into a quote + intro prose (heuristic: matches an opening `"..."` or splits on the first sentence-ending punctuation).
2. Locates the orphan `<cite>` (with optional `agent-avatar-inline`) followed by `</blockquote>` near the end of the file.
3. Locates the empty `<div class="callout big-picture">` wrapper that surrounds the bibliography.
4. Rebuilds the start of the section with: correctly-terminated epigraph (quote + cite + `</blockquote>`) -> filled big-picture callout -> prerequisites.
5. Removes the orphan `<cite>...</blockquote>` and unwraps the bibliography so it stands alone as `<details class="bibliography-collapsible">`.

`section-47.1b.html` was patched with two manual `Edit` calls because of its extra `<aside>` and `</aside>`-instead-of-`</div>` defects.

## Per-section notes

All fixes follow option (A) from the original brief: **the big-picture callout already existed in the file** (as an empty wrapper around the bibliography), so the script extracted the introductory prose that had been packed into the epigraph paragraph and used it to fill the callout. No content was synthesized from scratch; every paragraph that existed before the fix still exists after, just in the right place.

| Section | Intro-prose length (chars) | Orphan style |
|---------|---------------------------:|--------------|
| section-1.7a.html | 679 | agent-avatar + cite |
| section-47.1b.html | manual edit | aside + cite |
| section-48.1.html | 555 | cite only |
| section-48.2.html | 664 | cite only |
| section-48.3.html | 711 | cite only |
| section-48.4.html | 598 | cite only |
| section-48.5.html | 639 | cite only |
| section-54.1.html | 612 | agent-avatar + cite |
| section-54.2.html | 717 | agent-avatar + cite |
| section-54.3.html | 816 | agent-avatar + cite |
| section-54.6.html | 1082 | agent-avatar + cite |
| section-54.8.html | 797 | agent-avatar + cite |
| section-54.9.html | 1126 | agent-avatar + cite |
| section-54.10.html | 764 | agent-avatar + cite |
| section-59.5.html | 818 | agent-avatar + cite |
| section-24.1.html | 597 | agent-avatar + cite |
| section-24.2.html | 537 | agent-avatar + cite |
| section-24.3.html | 596 | agent-avatar + cite |
| section-24.4.html | 647 | agent-avatar + cite |
| section-24.5.html | 402 | agent-avatar + cite |
| section-24.7.html | 548 | agent-avatar + cite |
| section-24.8.html | 598 | agent-avatar + cite |
| section-24.9.html | 588 | agent-avatar + cite |
| section-24.10.html | 609 | agent-avatar + cite |
| section-24.11.html | 446 | agent-avatar + cite |
| section-24.12.html | 488 | agent-avatar + cite |
| section-24.13.html | 898 | agent-avatar + cite |
| section-34.5.html | 398 | agent-avatar + cite |

## section-47.1b.html (special case)

Three audit issues required three coordinated fixes:

1. **Lines 43-49 (header)**: split the epigraph blockquote (which contained the quote + a nested `<aside class="section-internal-toc">` whose trailing `<p>` held the intro prose). Result:
   - Quote stays in `<blockquote class="epigraph">` with proper `</blockquote>` close.
   - Agent-avatar (`Guard`) + cite added to the epigraph (moved from end-of-file orphan).
   - New filled `<div class="callout big-picture">` between epigraph and prerequisites, holding the intro paragraph.
   - The internal TOC `<aside>` moved to *after* prerequisites where it belongs (decorative section nav).
2. **Lines 846-855 (whats-next region)**: rebuilt the broken `<div class="whats-next">` into the canonical `<div class="callout whats-next">` with `<div class="callout-title">What's Next</div>` and a `</div>` close. The misplaced `</aside>`, the orphan `<span class="agent-avatar-inline">...<cite>...</cite>`, the orphan `</blockquote>`, and the empty `<div class="callout big-picture"><div class="callout-title">Big Picture</div>` wrapper were all removed (their content had already been moved earlier).
3. **Bibliography**: unwrapped from inside the (removed) big-picture wrapper; the `<details class="bibliography-collapsible">` now sits directly between whats-next and chapter-nav, which is the canonical order.

## Files added

- `agents/book-skills/scripts/audit/fix_section_order.py` (transformation script, kept in repo for re-running if needed)

## Files modified

- 28 section HTML files listed above. Backup of the originals stored at `/tmp/section_order_backup/` for the duration of the session.

## Verification

```bash
$ /c/Python314/python agents/book-skills/scripts/audit/run.py --root . --priority P1 --checks SECTION_ORDER
... 0 issues

$ /c/Python314/python agents/book-skills/scripts/audit/run.py --root . --priority P1
... 0 issues (the lone P2 SECTION_PAGE_LAYOUT in section-47.1a.html pre-dates this change)

$ /c/Python314/python agents/book-skills/scripts/audit/run.py --root . --priority P0
... 0 issues
```
