"""
Generate a fresh book cover via Google Gemini / Imagen, then post-process
to exact KDP dimensions (1600 x 2560 sRGB JPEG).

WHY two-stage (generate + post-process):
  Image-generation models do not produce exact pixel dimensions on demand.
  Imagen 4 at 9:16 gives roughly 1408 x 2496 (varies). To meet KDP's
  recommended 1600 x 2560 we always run the result through PIL.

WHY two output variants:
  1. cover_gemini_with_text_v<timestamp>.jpg
        Generated WITH the title/author text baked in via the prompt.
        Image models frequently produce garbled text; review carefully.
  2. cover_gemini_artwork_v<timestamp>.jpg
        Generated WITHOUT text, suitable for typography overlay if the
        with-text variant has issues.

Neither variant overwrites the existing `cover_kdp.jpg`. To promote a
generated variant to the active KDP cover, copy it manually:

    cp KDP/cover/cover_gemini_with_text_vXXX.jpg KDP/cover/cover_kdp.jpg

Usage:
    python KDP/cover/generate_cover_gemini.py            # both variants
    python KDP/cover/generate_cover_gemini.py --with-text-only
    python KDP/cover/generate_cover_gemini.py --artwork-only
    python KDP/cover/generate_cover_gemini.py --model imagen-4.0-ultra-generate-001

Config:
    Reads ~/.gemini-imagegen.json for { api_key, default_model }.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageCms

PROJECT_ROOT = Path(__file__).resolve().parents[2]
COVER_DIR = PROJECT_ROOT / "KDP" / "cover"
KDP_W, KDP_H = 1600, 2560

# -------- Prompts -------------------------------------------------------

# Thumbnail-optimized variant: title MUST be readable at 250 px wide.
# Drops subtitle, increases title size dramatically, uses high-contrast text.
PROMPT_THUMBNAIL_OPTIMIZED = (
    "Book cover, full-bleed portrait, 5:8 aspect ratio. Painterly digital art "
    "with subtle dreamlike quality. A luminous golden knowledge tree growing "
    "from an open book at the bottom. Tree roots formed of mathematical symbols "
    "(sigma, integral, partial-derivative, matrices) and neural-network connections. "
    "Tree branches support tiny vignette scenes: AI engineers at workstations, "
    "researchers studying attention patterns, conversations with chatbots, "
    "autonomous AI agents on quests, analytics dashboards, and a small council "
    "deliberating on safety. Diverse human figures climbing the tree at every level. "
    "Bathed in warm golden light against a deep navy starry sky. "
    "TEXT, rendered crisply and very large, optimized for readability at thumbnail size: "
    "Top half of cover dominated by a HUGE title in bright luminous gold serif lettering, "
    "two lines, taking up at least 25% of the cover height: "
    "'BUILDING CONVERSATIONAL AI' (line 1), 'WITH LLMS AND AGENTS' (line 2). "
    "NO subtitle. "
    "Bottom edge, in smaller bright gold serif: 'Alexander Apartsin & Yehudit Aperstein'. "
    "Background bleeds to deep navy/black at the edges. "
    "The title text MUST be the dominant element, large and high-contrast - this cover "
    "will be displayed at 250x400 pixels in Amazon search results."
)

# Minimalist variant: like Sebastian Raschka / Chip Huyen covers - abstract,
# typography-forward, high-contrast.
PROMPT_MINIMALIST = (
    "Book cover for a technical AI textbook, full-bleed portrait 5:8 aspect ratio. "
    "Minimalist design in the style of modern technical book covers (think O'Reilly, "
    "MIT Press, Manning). Solid deep navy background (#0d1226). "
    "Single abstract geometric illustration centered: a luminous golden network "
    "diagram suggesting both a tree and a transformer architecture - clean lines, "
    "glowing nodes, stylized vector aesthetic, NOT photorealistic. "
    "TEXT layout: "
    "Top third - HUGE title in bright gold sans-serif: 'BUILDING CONVERSATIONAL AI' "
    "(line 1, large) and 'WITH LLMs AND AGENTS' (line 2, smaller). "
    "Bottom edge - small gold serif: 'Alexander Apartsin & Yehudit Aperstein'. "
    "Top edge - tiny uppercase tag: 'FIFTH EDITION 2026'. "
    "High contrast, typography-forward, professional technical-book aesthetic. "
    "Optimized for Amazon thumbnail readability at 250x400 pixels."
)


PROMPT_WITH_TEXT = (
    "Book cover for a textbook, full bleed portrait composition, 5:8 aspect ratio. "
    "Painterly digital art with subtle dreamlike quality. "
    "A luminous golden knowledge tree growing from an open book at the bottom-center. "
    "The tree's roots are formed of intertwined mathematical symbols (sigma, integral, partial-derivative, matrices), "
    "neural-network connections, and tokenization fragments. "
    "The tree's branches support tiny vignette scenes: AI engineers at workstations, researchers studying attention-pattern heatmaps, "
    "people in conversation with chatbots, autonomous AI agents on quests, analytics dashboards with floating charts, "
    "and a small council of figures deliberating on AI safety. "
    "Diverse human figures (different ethnicities, genders, ages) climb the tree at every level. "
    "Bathed in warm golden light against a deep navy sky filled with subtle constellations and shooting stars. "
    "TEXT, rendered crisply and cleanly in elegant gold serif lettering: "
    "Top of cover, large prominent title in two lines: 'BUILDING CONVERSATIONAL AI' (line 1) "
    "'WITH LLMS AND AGENTS' (line 2). "
    "Below the title, in smaller italic gold serif: 'A practitioner's guide for engineers, researchers, and students'. "
    "Bottom of cover, in elegant smaller italic serif: 'Alexander Apartsin & Yehudit Aperstein'. "
    "Bottom edge: 'Fifth Edition · 2026' in small caps. "
    "Background bleeds to deep navy/black at the edges so the composition reads cleanly with no margins. "
    "Suitable for use as an Amazon Kindle book cover."
)

PROMPT_ARTWORK_ONLY = (
    "Book cover ARTWORK ONLY, NO TEXT, NO LETTERING, NO WORDS ANYWHERE. "
    "Full bleed portrait composition, 5:8 aspect ratio. "
    "Painterly digital art with subtle dreamlike quality. "
    "A luminous golden knowledge tree growing from an open book at the bottom-center. "
    "The tree's roots are formed of intertwined mathematical symbols (sigma, integral, partial-derivative, matrices), "
    "neural-network connections, and tokenization fragments. "
    "The tree's branches support tiny vignette scenes: AI engineers at workstations, researchers studying attention-pattern heatmaps, "
    "people in conversation with chatbots, autonomous AI agents on quests, analytics dashboards with floating charts, "
    "and a small council of figures deliberating on AI safety. "
    "Diverse human figures (different ethnicities, genders, ages) climb the tree at every level. "
    "Bathed in warm golden light against a deep navy sky filled with subtle constellations and shooting stars. "
    "Background bleeds to deep navy/black at the edges. "
    "Composition has clear empty space at the top quarter (for title text overlay later) and "
    "smaller empty space at the bottom for author text. "
    "STRICTLY NO TEXT OR LETTERS in the image, only artwork."
)


# -------- Generation ----------------------------------------------------


def load_config() -> dict:
    cfg_path = Path.home() / ".gemini-imagegen.json"
    if not cfg_path.exists():
        print(f"ERROR: {cfg_path} not found. Create it with at least 'api_key'.", file=sys.stderr)
        sys.exit(3)
    return json.loads(cfg_path.read_text())


def call_imagen(client, model: str, prompt: str) -> bytes:
    """Call an Imagen model. Returns PNG bytes of the first generated image."""
    from google.genai import types
    print(f"  Calling Imagen model: {model}")
    print(f"  Aspect ratio: 9:16 (closest portrait to 5:8)")
    response = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="9:16",
            safety_filter_level="BLOCK_LOW_AND_ABOVE",
        ),
    )
    if not response.generated_images:
        raise RuntimeError("Imagen returned no images")
    return response.generated_images[0].image.image_bytes


def call_gemini_native(client, model: str, prompt: str, reference_image: Path | None = None) -> bytes:
    """Call a Gemini native image-gen model.

    If reference_image is provided, the call is image-to-image: the model
    sees the reference and the prompt, and produces a transformed/improved
    output that preserves the reference's composition and style.

    Returns PNG bytes.
    """
    from google.genai import types
    print(f"  Calling Gemini native model: {model}")
    if reference_image and reference_image.exists():
        print(f"  Mode: IMAGE-TO-IMAGE (reference: {reference_image.name})")
        print(f"  Aspect ratio: 9:16, image_size: 2K")
        ref_bytes = reference_image.read_bytes()
        ref_mime = "image/png" if reference_image.suffix.lower() == ".png" else "image/jpeg"
        contents = [
            types.Part.from_bytes(data=ref_bytes, mime_type=ref_mime),
            prompt,
        ]
    else:
        print(f"  Mode: TEXT-TO-IMAGE")
        print(f"  Aspect ratio: 9:16, image_size: 2K")
        contents = prompt
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="9:16", image_size="2K"),
        ),
    )
    for part in response.parts:
        if getattr(part, "inline_data", None):
            return part.inline_data.data
    raise RuntimeError("Gemini native call returned no inline image data")


def generate(client, model: str, prompt: str, label: str, reference_image: Path | None = None) -> bytes:
    """Dispatch to the right SDK method based on model family.

    Imagen models do not support image-to-image, so reference_image is ignored
    when an Imagen model is selected (and a warning is printed).
    """
    is_imagen = model.startswith("imagen-")
    print(f"\n[{label}]")
    t0 = time.time()
    try:
        if is_imagen:
            if reference_image:
                print(f"  WARNING: Imagen does not support reference images; ignoring.")
            data = call_imagen(client, model, prompt)
        else:
            data = call_gemini_native(client, model, prompt, reference_image=reference_image)
    except Exception as e:
        print(f"  ERROR: generation failed: {e}")
        raise
    elapsed = time.time() - t0
    print(f"  Generated in {elapsed:.1f}s ({len(data) / 1024:.1f} KB raw)")
    return data


# -------- Post-processing -----------------------------------------------


def average_edge_color(im: Image.Image) -> tuple[int, int, int]:
    w, h = im.size
    samples = []
    for x in range(0, w, max(1, w // 50)):
        samples.append(im.getpixel((x, 0)))
        samples.append(im.getpixel((x, h - 1)))
    for y in range(0, h, max(1, h // 50)):
        samples.append(im.getpixel((0, y)))
        samples.append(im.getpixel((w - 1, y)))
    samples = [s[:3] if isinstance(s, tuple) else (s, s, s) for s in samples]
    r = sum(s[0] for s in samples) // len(samples)
    g = sum(s[1] for s in samples) // len(samples)
    b = sum(s[2] for s in samples) // len(samples)
    return (r, g, b)


def fit_to_kdp(raw_bytes: bytes) -> Image.Image:
    """
    Take raw model output and produce an exact 1600x2560 sRGB image.

    Strategy:
      1. If model output aspect ratio differs from 5:8, scale to fit and pad
         with edge color (NOT crop) so we never lose composed content.
      2. If the model output is larger than 1600x2560, resample down (Lanczos).
      3. Convert to RGB sRGB.
    """
    im = Image.open(BytesIO(raw_bytes)).convert("RGB")
    sw, sh = im.size
    print(f"  Raw size: {sw} x {sh}, aspect {sw / sh:.3f}")

    src_aspect = sw / sh
    dst_aspect = KDP_W / KDP_H  # 0.625

    if src_aspect > dst_aspect:
        new_w = KDP_W
        new_h = round(KDP_W / src_aspect)
    else:
        new_h = KDP_H
        new_w = round(KDP_H * src_aspect)

    print(f"  Scaling to: {new_w} x {new_h}")
    scaled = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

    pad = average_edge_color(scaled)
    print(f"  Pad color: rgb{pad}")
    canvas = Image.new("RGB", (KDP_W, KDP_H), pad)
    off_x = (KDP_W - new_w) // 2
    off_y = (KDP_H - new_h) // 2
    canvas.paste(scaled, (off_x, off_y))
    print(f"  Final canvas: {KDP_W} x {KDP_H}, source offset ({off_x}, {off_y})")

    return canvas


def save_kdp(im: Image.Image, out_path: Path) -> None:
    try:
        srgb = ImageCms.createProfile("sRGB")
        im.save(
            out_path,
            format="JPEG",
            quality=92,
            optimize=True,
            progressive=False,
            icc_profile=ImageCms.ImageCmsProfile(srgb).tobytes(),
        )
    except Exception as e:
        print(f"  (could not embed sRGB profile: {e}; saving without)")
        im.save(out_path, format="JPEG", quality=92, optimize=True, progressive=False)
    size = out_path.stat().st_size
    print(f"  Wrote {out_path.relative_to(PROJECT_ROOT)} ({size / 1024:.1f} KB)")


# -------- Main ----------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    p.add_argument("--with-text-only", action="store_true",
                   help="Only generate the with-text variant (skip artwork-only)")
    p.add_argument("--artwork-only", action="store_true",
                   help="Only generate the artwork-only variant (skip with-text)")
    p.add_argument("--thumbnail-optimized", action="store_true",
                   help="Thumbnail-optimized variant: HUGE title (no subtitle) for Amazon's 250-px result thumbnail")
    p.add_argument("--minimalist", action="store_true",
                   help="Minimalist variant: O'Reilly/MIT-style abstract typography-forward cover")
    p.add_argument("--all-variants", action="store_true",
                   help="Generate all 4 variants: with-text, artwork-only, thumbnail-optimized, minimalist")
    p.add_argument("--img2img", action="store_true",
                   help="Image-to-image mode: feed images/book-cover.png as reference. "
                        "Forces gemini-3-pro-image-preview for both variants since Imagen "
                        "does not support image input.")
    p.add_argument("--reference",
                   default=str(Path(__file__).resolve().parents[2] / "images" / "book-cover.png"),
                   help="Reference image path for --img2img (default: images/book-cover.png)")
    p.add_argument("--model-with-text", default="imagen-4.0-ultra-generate-001",
                   help="Model for the text-baked variant (default: imagen-4.0-ultra-generate-001 - best text rendering)")
    p.add_argument("--model-artwork", default="gemini-3-pro-image-preview",
                   help="Model for the artwork-only variant (default: gemini-3-pro-image-preview - best quality)")
    args = p.parse_args(argv)

    # In image-to-image mode, force Gemini Pro for both variants (Imagen can't take image input)
    reference_image = None
    if args.img2img:
        reference_image = Path(args.reference)
        if not reference_image.exists():
            print(f"ERROR: reference image not found: {reference_image}", file=sys.stderr)
            return 3
        if args.model_with_text.startswith("imagen-"):
            args.model_with_text = "gemini-3-pro-image-preview"
            print(f"img2img mode: switching with-text model to gemini-3-pro-image-preview")

    # Late import so missing dep errors are clear
    try:
        from google import genai
    except ImportError:
        print("ERROR: google-genai not installed. Run: pip install google-genai Pillow", file=sys.stderr)
        return 3

    cfg = load_config()
    client = genai.Client(api_key=cfg["api_key"])

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    raw_dir = COVER_DIR / "raw"
    raw_dir.mkdir(exist_ok=True)

    failures = 0

    # Choose prompts depending on mode. In img2img mode the prompts are
    # shorter and emphasize "preserve composition"; in text2img mode the
    # prompts describe the scene from scratch.
    if args.img2img:
        prompt_with_text = (
            "Regenerate this book cover at high resolution, preserving the "
            "overall composition, color palette, and artistic style of the "
            "reference image. Improve sharpness and detail. The title text "
            "'BUILDING CONVERSATIONAL AI WITH LLMS AND AGENTS' should be "
            "rendered crisply in elegant gold serif lettering at the top, "
            "with subtitle 'A practitioner's guide for engineers, researchers, "
            "and students' below. Author names 'Alexander Apartsin & Yehudit "
            "Aperstein' at the bottom in italic gold serif. Edition tag "
            "'Fifth Edition · 2026' at the very bottom in small caps. "
            "Maintain the deep navy starry background with golden tree composition."
        )
        prompt_artwork = (
            "Regenerate this book cover artwork at high resolution. "
            "Preserve the overall composition, color palette, and artistic "
            "style of the reference image (luminous golden knowledge tree, "
            "open book, scenes in branches, climbing figures, deep navy "
            "starry sky). Improve sharpness and detail. NO TEXT, NO LETTERING, "
            "NO WORDS. Leave the top quarter and bottom edge as clear "
            "background space for typography to be added later. "
            "Maintain the deep navy bleed at edges."
        )
    else:
        prompt_with_text = PROMPT_WITH_TEXT
        prompt_artwork = PROMPT_ARTWORK_ONLY

    suffix = "_i2i" if args.img2img else ""

    if not args.artwork_only:
        try:
            data = generate(client, args.model_with_text, prompt_with_text,
                           "WITH-TEXT VARIANT", reference_image=reference_image)
            (raw_dir / f"raw_with_text{suffix}_{ts}.png").write_bytes(data)
            print(f"  Raw saved: KDP/cover/raw/raw_with_text{suffix}_{ts}.png")
            im = fit_to_kdp(data)
            out = COVER_DIR / f"cover_gemini_with_text{suffix}_v{ts}.jpg"
            save_kdp(im, out)
        except Exception as e:
            print(f"  FAILED: {e}")
            failures += 1

    if not args.with_text_only:
        try:
            data = generate(client, args.model_artwork, prompt_artwork,
                           "ARTWORK-ONLY VARIANT", reference_image=reference_image)
            (raw_dir / f"raw_artwork{suffix}_{ts}.png").write_bytes(data)
            print(f"  Raw saved: KDP/cover/raw/raw_artwork{suffix}_{ts}.png")
            im = fit_to_kdp(data)
            out = COVER_DIR / f"cover_gemini_artwork{suffix}_v{ts}.jpg"
            save_kdp(im, out)
        except Exception as e:
            print(f"  FAILED: {e}")
            failures += 1

    # Thumbnail-optimized variant: huge title, no subtitle, designed for 250-px Amazon thumbnail
    if args.thumbnail_optimized or args.all_variants:
        try:
            data = generate(client, args.model_with_text, PROMPT_THUMBNAIL_OPTIMIZED,
                           "THUMBNAIL-OPTIMIZED VARIANT", reference_image=reference_image)
            (raw_dir / f"raw_thumbnail_{ts}.png").write_bytes(data)
            print(f"  Raw saved: KDP/cover/raw/raw_thumbnail_{ts}.png")
            im = fit_to_kdp(data)
            out = COVER_DIR / f"cover_gemini_thumbnail_v{ts}.jpg"
            save_kdp(im, out)
        except Exception as e:
            print(f"  FAILED: {e}")
            failures += 1

    # Minimalist variant: O'Reilly/MIT-Press-style typography-forward cover
    if args.minimalist or args.all_variants:
        try:
            data = generate(client, args.model_with_text, PROMPT_MINIMALIST,
                           "MINIMALIST VARIANT", reference_image=reference_image)
            (raw_dir / f"raw_minimalist_{ts}.png").write_bytes(data)
            print(f"  Raw saved: KDP/cover/raw/raw_minimalist_{ts}.png")
            im = fit_to_kdp(data)
            out = COVER_DIR / f"cover_gemini_minimalist_v{ts}.jpg"
            save_kdp(im, out)
        except Exception as e:
            print(f"  FAILED: {e}")
            failures += 1

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print()
    print("Review the variants in KDP/cover/, then promote the chosen one:")
    print(f"  cp KDP/cover/cover_gemini_with_text_v{ts}.jpg KDP/cover/cover_kdp.jpg")
    print()
    print("Notes:")
    print("  - With-text variants from any image model often have garbled letters.")
    print("    If the text is unusable, use the artwork-only variant and overlay")
    print("    typography in a graphics tool (Photoshop, Affinity, Figma).")
    print("  - The current upscaled placeholder remains at cover_kdp.jpg until you")
    print("    explicitly promote a generated variant.")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
