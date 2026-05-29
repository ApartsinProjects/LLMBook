# EPUB Size Analysis — May 2026

**Current**: `KDP/output/building-conversational-ai-llms-agents.epub` = **53.6 MB**
**Target**: < 50 MB to make the 70% royalty plan economical
**Stretch**: < 30 MB doubles net royalty per sale at $9.99 list

---

## What's in the file

| Type      | Total   | Files | Notes                                       |
|-----------|---------|-------|---------------------------------------------|
| **JPEG**  | 25.8 MB | 298   | Photos, screenshots, Gemini illustrations   |
| **PNG**   | 23.4 MB | 157   | Mermaid diagrams, matplotlib charts, icons  |
| **XHTML** | 15.9 MB | 377   | Chapter prose + KaTeX-rendered math markup  |
| Fonts     | 1.1 MB  | 64    | TTF + WOFF + WOFF2 (mostly KaTeX glyph fonts) |
| Other     | 0.5 MB  | 16    | OPF, NCX, CSS, SVG cover, manifest          |
| **Total** | **53.6 MB on disk / 66.7 MB uncompressed** | 911 | |

**Images dominate at 92% of the file.** Anything we do to text moves the needle by < 1 MB. To shrink the EPUB meaningfully we must shrink images.

---

## Top single-file offenders

| Size    | File                                       | What it is              |
|---------|--------------------------------------------|-------------------------|
| 723 KB  | `cover.jpg`                                | Front cover (1600×2560) |
| 434 KB  | `coding-exercise-icon.png`                 | A single sidebar icon!  |
| 350 KB  | `fig-8-1-3-reasoning-architecture-compared` | Mermaid diagram → PNG  |
| 292 KB  | `fig-2-2-4-unigram.png`                    | Mermaid diagram → PNG   |
| 290 KB  | `fig-32-9-1-eu-ai-act-risk-tiers.png`     | Mermaid diagram → PNG   |
| ...     | 28 more PNGs in the 200–280 KB range       | Almost all Mermaid → PNG |

The 30 oversized images alone account for **~7.6 MB**. The single coding-exercise icon (434 KB) is the most embarrassing — a sidebar icon that ships once but is referenced from many chapters.

---

## Royalty math (why this matters)

KDP 70% royalty plan: `royalty = 0.70 × (list_price − 0.15 × MB)`

| EPUB size | Delivery fee | Net royalty at $9.99 list | vs 53.6 MB |
|-----------|--------------|---------------------------|------------|
| 53.6 MB   | $8.04        | **$1.36 / sale**          | —          |
| 50.0 MB   | $7.50        | **$1.74 / sale**          | +28%       |
| 40.0 MB   | $6.00        | **$2.79 / sale**          | +105%      |
| 30.0 MB   | $4.50        | **$3.84 / sale**          | +182%      |
| 20.0 MB   | $3.00        | **$4.89 / sale**          | +260%      |

Below 20 MB and the 70% plan saturates. Above ~67 MB you make negative net royalty per sale.

---

## Reduction options, ranked by impact

### 1. Convert Mermaid PNGs to SVG  *(estimated save: 12–18 MB)*

Most of our 200+ KB images are Mermaid flowcharts/architectures that we currently render at `-w 1200 -s 3` to PNG. Mermaid can output SVG directly. SVG is text + math, compresses extremely well, and scales perfectly on Kindle Scribe / Kindle web. Kindle KFX has supported SVG since 2018. Risk: small (some old Kindle devices fall back to a poster image, but the SVG is still parsed).

**Action:** Update `scripts/mermaid/generate_mermaid_diagrams.py` to emit `.svg` next to each `.png`. Then update `KDP/build/_html2epub_hooks.py` to prefer the `.svg` if present and the EPUB target supports it.

### 2. Recompress the few oversized JPEGs  *(estimated save: 0.5–1 MB)*

`cover.jpg` is 723 KB. KDP cover spec says 1600×2560, sRGB, < 50 MB — but smaller is fine. A re-export at q=80 typically lands at ~300–400 KB without visible quality loss.

**Action:** One-shot re-encode of cover via `Pillow`.

### 3. Fix the 434 KB coding-exercise icon  *(estimated save: 400 KB)*

A single sidebar icon should be < 5 KB. This file is probably a 1024×1024 source image embedded as-is.

**Action:** Resize to 64×64 or replace with an inline SVG icon.

### 4. Convert PNG screenshots/figures to JPEG  *(estimated save: 4–6 MB)*

Many of the 157 PNGs do not need alpha transparency (they are flowcharts with white backgrounds). PNG-to-JPEG at q=78 typically saves 30–50%. Mermaid diagrams with thin lines can stay PNG (JPEG artifacts hurt them); diagrams with solid color blocks and labels convert cleanly.

**Action:** Add a transparency-detection step to `build_epub.py`'s image pipeline; if pixel scan shows no alpha and < 256 colors, output is already small as PNG-8 — keep it. Otherwise re-encode as JPEG.

### 5. Drop unused KaTeX font glyphs  *(estimated save: 300–500 KB)*

The 60 KaTeX font files cover every Unicode math symbol; we use a small subset. KaTeX provides a `fonts.css` subset list, but you'd need to scan the rendered MathML to know which fonts to keep.

**Action:** Lower priority — modest gain, fragile maintenance cost.

### 6. Tighter image downscaling (max=800 instead of 1000)  *(estimated save: 2–4 MB)*

Current `--max-image-side 1000` matches Kindle Paperwhite's effective width (1072 px). Going to 800 px is visually noticeable on Kindle Scribe (1860 px) but invisible on phones and small Kindles. Trade-off, not a free win.

### 7. WebP conversion  *(estimated save: 8–12 MB, BUT)*

WebP is 30–50% smaller than equivalent JPEG. **Risk:** Kindle KFX support for WebP is documented as "limited" — older Kindle devices (pre-2020) may show fallback grey boxes. Probably not worth the support headache.

### 8. Split into multiple EPUBs  *(no save, but better economics per book)*

Sell Part 1–4 ("Foundations through Adaptation") and Part 5–11 ("Retrieval to Production") as two volumes. Each ~ 27 MB. Same total content, but you collect royalty on two sales.

---

## Recommended combo (realistic, low-risk)

| Step                                          | Est. save | Effort |
|-----------------------------------------------|-----------|--------|
| 1. Mermaid PNG → SVG                          | 14 MB     | 3 hrs  |
| 2. Recompress cover.jpg                       | 0.4 MB    | 5 min  |
| 3. Fix coding-exercise icon                   | 0.4 MB    | 10 min |
| 4. PNG → JPEG for non-transparent screenshots | 5 MB      | 1 hr   |
| **Total**                                     | **~20 MB** | **~5 hrs** |

Projected new size: **~33 MB**, royalty per sale at $9.99: **$3.50 (+157%)**.

---

## What we already did

- v6.10–v6.18: page text changes, no size impact
- v6.19: rebuild with `build_epub.py --max-image-side 1000 --jpeg-quality 72` (was the default 1280/78). Saved ~21 MB (74.6 MB → 53.6 MB) in one shot.
