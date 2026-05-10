# Cover Image Notes

## Files in this folder

| File | Purpose | Status |
|------|---------|--------|
| `cover_source.png` | Copy of the original `images/book-cover.png` (896 x 1200) | Source asset |
| `cover_kdp.jpg` | The cover currently used by the EPUB build (1600 x 2560 sRGB JPEG) | **Placeholder — replace before final submission** |
| `cover_gemini_artwork_v<TIMESTAMP>.jpg` | Gemini-generated artwork ONLY (no text), 1600 x 2560 | Native-resolution candidate |
| `cover_gemini_with_text_v<TIMESTAMP>.jpg` | Gemini-generated WITH title and author text baked in, 1600 x 2560 | Native-resolution candidate |
| `process_cover.py` | Script that produced the upscaled placeholder from `cover_source.png` | One-shot tool |
| `generate_cover_gemini.py` | Reproducible Gemini generation script | Re-run anytime |
| `raw/` | Raw model outputs at native model dimensions (PNG) | Audit trail |

## How to choose / promote a cover

You now have **three options** for the active cover. Pick one and copy it over `cover_kdp.jpg`:

```bash
# Option A: keep the upscaled placeholder (current)
# (no action needed)

# Option B: use the Gemini with-text variant (text rendered by the model)
cp KDP/cover/cover_gemini_with_text_v<TIMESTAMP>.jpg KDP/cover/cover_kdp.jpg

# Option C: use the Gemini artwork-only variant (overlay text yourself)
cp KDP/cover/cover_gemini_artwork_v<TIMESTAMP>.jpg KDP/cover/cover_kdp.jpg
```

After promoting, rebuild:

```bash
python KDP/build/publish.py
```

## Comparison of variants

| | Upscaled placeholder | Gemini with-text | Gemini artwork-only |
|---|---|---|---|
| Native resolution | No (upscaled 2.13x) | **Yes** (1600 x 2560 from 768 x 1408 model output) | **Yes** (1600 x 2560 from 1536 x 2752 model output) |
| Text quality | Sharp (text was in source) | Acceptable (Imagen 4 Ultra rendered it correctly this run; verify each generation) | None — overlay your own |
| Composition | Original artistic intent | Busier, more vignettes around the tree | Cleaner, single luminous tree, fewer competing elements |
| Best for | Iteration; KDP submission as a fallback | Quick KDP submission with auto-rendered text | Higher-end production: layer your own typography |
| Color depth | Same as source | Native generation | Native generation |
| File size | 418 KB | ~750 KB | ~700 KB |

## Recommendation

For the **first KDP submission**: use the **with-text Gemini variant**. The text rendered correctly in the most recent generation, and you can always update the cover after publication (KDP allows cover updates anytime).

For a **polished long-term cover**: use the **artwork-only variant** and overlay typography in a graphics tool (Photoshop, Affinity, Figma, GIMP). This gives you pixel-perfect title kerning, proper fonts (Cinzel for title, Cormorant Garamond for subtitle/authors), and the freedom to A/B test different wordings.

## Re-generating

Image generation is non-deterministic; each run produces different output. To generate fresh variants:

```bash
# Both variants
python KDP/cover/generate_cover_gemini.py

# Just artwork (the cleaner composition)
python KDP/cover/generate_cover_gemini.py --artwork-only

# Just with-text (try a different seed)
python KDP/cover/generate_cover_gemini.py --with-text-only

# Different model
python KDP/cover/generate_cover_gemini.py --model-with-text imagen-4.0-generate-001
```

Each run leaves both old and new variants in place (timestamped filenames) so you can compare. Curate the folder periodically by deleting variants you don't want.

## Why two variants

Image-generation models (including Imagen 4 Ultra) are inconsistent at rendering text on covers. Sometimes letters come out garbled, sometimes spacing is off, sometimes it works perfectly. The artwork-only variant avoids this risk entirely — you get a clean composition that you can layer text on top of with full control. The with-text variant is a one-shot bet that's worth taking when it works.

## KDP cover requirements (reference)

| Requirement | Value | This package |
|-------------|-------|--------------|
| Recommended dimensions | 1600 x 2560 pixels | All variants meet |
| Minimum | 1000 px on longest side | All variants meet |
| Aspect ratio | 1.6 (height/width) = 5:8 | All variants meet |
| Format | JPEG (.jpg) preferred, TIFF accepted | JPEG ✓ |
| Color space | sRGB | Embedded ICC profile ✓ |
| Color profile | RGB only (no CMYK) | RGB ✓ |
| Max file size | 50 MB | All under 1 MB ✓ |
| DPI | Not enforced (KDP uses pixel dimensions only) | n/a |
| Text on cover | Title + subtitle + author should be legible at 250 px wide thumbnail | Verify after promotion |
