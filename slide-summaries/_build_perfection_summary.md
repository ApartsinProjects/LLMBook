# Build perfection loop, summary

## Result (post-iteration 2)

| Gate | Before | After |
| --- | --- | --- |
| Build success | yes | yes |
| EPUBCheck (W3C) | 0/0/0 | 0/0/0 |
| Internal `step_quality_audit` | 4 errors, 93 warnings | 0 errors, 0 warnings |
| KPV qualitychecks | 0/0 (was already clean) | pending final run, expected 0/0 |
| EPUB size | 36.84 MB | 38.71 MB |

## What was fixed

1. 4 BROKEN-FRAG errors. The appendix-G signal-processing sections G.1, G.2, G.3, G.4 each linked to `section-20.0.html#audio-data`, an anchor that no longer exists. The id was renumbered to `20-0-1-the-bipartite-taxonomy` in an earlier edit cycle. All four hrefs were rewritten in place.

2. 93 LIVE-MATHML warnings. The book's math pipeline is a two-stage cache: the build emits `.book-update/math-manifest.json` listing every equation that needs a PNG, and `scripts/build_math_png_cache.py` (Playwright + KaTeX-on-Chromium at 3x DPI) renders any keys not yet in `.book-update/math-png-cache/`. The cache had 297 PNGs but the manifest had grown to 514 entries during recent enrichment work, so 220 equations were falling back to live `<math>` markup in the EPUB. Running the cache builder rendered the missing 220 PNGs; the next build swapped them in. Three stragglers (all `\begin{aligned}` blocks with `\Big(` delimiters and column-alignment ampersands) needed a second render pass before they landed (apparent transient Playwright timing issue on the first batch).

## What was not changed

- No HTML body content was rewritten. The 4 broken-frag fixes are href-only.
- No `html2epub.toml` config change. The math pipeline was already configured correctly; it just needed the missing PNGs.
- No regression risk: EPUBCheck was already clean and remains clean; math PNGs were bundled at the same DPI and CSS as the existing 297.

## Cost

- +1.87 MB in EPUB size (220 PNGs at ~8.5 KB each, after pngquant compression). The book is now 38.71 MB, still under the 40 MB KDP delivery-fee threshold sweet spot.
- Build time unchanged (~3.5 min per full build). The PNG render is a one-shot cost that ran in under 3 minutes.

## Re-run instructions

If the manifest grows again (any new equation added to the source HTML), the fix is:

```
C:/Python314/python scripts/build_math_png_cache.py
C:/Python314/python KDP/build/publish.py --no-kpv
```

The cache is incremental: it only renders keys whose PNG is missing.

## Recommended follow-up

Add a publish.py pre-flight that auto-runs `build_math_png_cache.py` after the first EPUB pass detects any non-empty `manifest - cache` set, so this latency never bites again. Filed as a backlog candidate; not required for shipping the current edition.
