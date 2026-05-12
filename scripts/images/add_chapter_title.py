"""Overlay a chapter title on a Gemini-generated chapter-opener image.

Why: Imagen reliably mis-renders embedded text (typos, dropped letters).
The fix is to generate the cartoon WITHOUT in-image text, then overlay
the chapter title using a real font. This script is the overlay step.

Style match: existing chapter openers in the book use a heavy bold
all-caps sans-serif title at the top, dark on light. We reproduce that
with Arial Bold + a subtle white gradient strip behind for legibility
even when the cartoon's top edge is busy.

Usage:
    python add_chapter_title.py <input.png> <output.png> "TITLE TEXT"

Example:
    python add_chapter_title.py opener-v2.png opener-v3.png \\
        "EMBEDDINGS AND VECTOR DATABASES"
"""
from __future__ import annotations
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Constants tuned to match existing chapter-opener visual identity
FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"  # Arial Bold
TITLE_COLOR = (26, 32, 64)  # dark navy, matches existing book palette
GRADIENT_FRAC = 0.16  # gradient strip = top 16% of image height
TITLE_TOP_FRAC = 0.025  # title sits at 2.5% from top
H_MARGIN_FRAC = 0.06  # text must fit within (image_w - 2 * 6%)


def fit_font_size(text: str, max_width: int, max_height: int) -> ImageFont.FreeTypeFont:
    """Find the largest font size where `text` fits within max_width and max_height."""
    # Binary search between 12 and max_height
    lo, hi = 12, max_height
    best = ImageFont.truetype(FONT_PATH, lo)
    while lo <= hi:
        mid = (lo + hi) // 2
        font = ImageFont.truetype(FONT_PATH, mid)
        # Use textbbox for accurate measurement
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if text_width <= max_width and text_height <= max_height:
            best = font
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def add_top_gradient(img: Image.Image, frac: float = GRADIENT_FRAC) -> Image.Image:
    """Composite a white-to-transparent gradient on the top `frac` of the image.

    Ensures the title is legible regardless of the cartoon's top-edge color.
    Strongest at the top (alpha 220) fading to alpha 0 at the bottom of the strip.
    """
    img = img.convert("RGBA")
    w, h = img.size
    strip_h = int(h * frac)
    gradient = Image.new("RGBA", (w, strip_h), (255, 255, 255, 0))
    pixels = gradient.load()
    for y in range(strip_h):
        # Linearly fade alpha from 220 (top) to 0 (bottom of strip)
        alpha = int(220 * (1 - y / strip_h))
        for x in range(w):
            pixels[x, y] = (255, 255, 255, alpha)
    img.alpha_composite(gradient, dest=(0, 0))
    return img


def add_title(input_path: str, output_path: str, title: str) -> None:
    img = Image.open(input_path)
    img = add_top_gradient(img)
    w, h = img.size

    # Available text box: full width minus margins, height = ~9% of image
    h_margin = int(w * H_MARGIN_FRAC)
    max_text_width = w - 2 * h_margin
    max_text_height = int(h * 0.09)

    # Title rendered ALL CAPS to match existing openers
    title_upper = title.upper()
    font = fit_font_size(title_upper, max_text_width, max_text_height)

    draw = ImageDraw.Draw(img)
    bbox = font.getbbox(title_upper)
    text_width = bbox[2] - bbox[0]
    text_x = (w - text_width) // 2 - bbox[0]  # center horizontally
    text_y = int(h * TITLE_TOP_FRAC)

    # Subtle dark shadow for depth (1px offset)
    draw.text((text_x + 1, text_y + 1), title_upper, font=font, fill=(0, 0, 0, 80))
    draw.text((text_x, text_y), title_upper, font=font, fill=TITLE_COLOR)

    # Save as RGB (drop alpha for final PNG)
    img.convert("RGB").save(output_path, optimize=True)
    print(f"Saved: {output_path}  (font size {font.size}px, {w}x{h})")


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 1
    input_path, output_path, title = sys.argv[1], sys.argv[2], sys.argv[3]
    if not Path(input_path).exists():
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        return 1
    add_title(input_path, output_path, title)
    return 0


if __name__ == "__main__":
    sys.exit(main())
