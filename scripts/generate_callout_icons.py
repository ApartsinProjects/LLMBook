"""
Generate 10 callout-box icons for the LLMCourse textbook using Gemini native image generation.
Each icon is 128x128, flat design, consistent style, suitable for display at 24x24.
"""

import json
import time
import sys
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
config_path = Path.home() / ".gemini-imagegen.json"
if not config_path.exists():
    print("ERROR: ~/.gemini-imagegen.json not found")
    sys.exit(1)

config = json.loads(config_path.read_text())
client = genai.Client(api_key=config["api_key"])
MODEL = config.get("default_model", "gemini-3.1-flash-image-preview")

OUTPUT_DIR = Path(r"E:\Projects\LLMCourse\styles\icons")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Icon definitions: (filename, prompt)
# ---------------------------------------------------------------------------
STYLE_SUFFIX = (
    "Flat design icon on a plain white background. Clean lines, minimal detail, "
    "warm and friendly style matching a university textbook. Single centered symbol. "
    "No text, no lettering, no words. Consistent line weight. "
    "The icon must be instantly recognizable when displayed at 24x24 pixels."
)

ICONS = [
    (
        "callout-big-picture.png",
        f"A simple purple compass-star icon suggesting a high-level overview or big picture. "
        f"Purple tones (#8e24aa). {STYLE_SUFFIX}"
    ),
    (
        "callout-key-insight.png",
        f"A simple green lightbulb icon suggesting a key idea or aha moment. "
        f"Green tones (#43a047). {STYLE_SUFFIX}"
    ),
    (
        "callout-note.png",
        f"A simple blue notepad with a small pencil icon suggesting additional information. "
        f"Blue tones (#1976d2). {STYLE_SUFFIX}"
    ),
    (
        "callout-warning.png",
        f"A simple amber/orange warning triangle with an exclamation mark icon suggesting caution. "
        f"Amber tones (#f57c00). {STYLE_SUFFIX}"
    ),
    (
        "callout-practical-example.png",
        f"A simple teal construction hammer icon suggesting real-world practical application. "
        f"Teal tones (#00897b). {STYLE_SUFFIX}"
    ),
    (
        "callout-fun-note.png",
        f"A simple pink party hat or circus tent icon suggesting an entertaining fun tangent. "
        f"Pink tones (#e91e63). {STYLE_SUFFIX}"
    ),
    (
        "callout-research-frontier.png",
        f"A simple cyan microscope icon suggesting cutting-edge scientific research. "
        f"Cyan/teal tones (#00897b). {STYLE_SUFFIX}"
    ),
    (
        "callout-algorithm.png",
        f"A simple indigo gear/cog icon suggesting a formal algorithm or procedure. "
        f"Indigo tones (#5c6bc0). {STYLE_SUFFIX}"
    ),
    (
        "callout-tip.png",
        f"A simple cyan lightbulb combined with a small wrench icon suggesting practical tips and advice. "
        f"Cyan tones (#00acc1). {STYLE_SUFFIX}"
    ),
    (
        "callout-exercise.png",
        f"A simple deep orange pencil writing on a notepad icon suggesting a practice exercise task. "
        f"Deep orange tones (#e64a19). {STYLE_SUFFIX}"
    ),
]

# ---------------------------------------------------------------------------
# Generate each icon
# ---------------------------------------------------------------------------
def generate_icon(filename: str, prompt: str, retries: int = 3) -> bool:
    """Generate a single icon, resize to 128x128, save as PNG."""
    out_path = OUTPUT_DIR / filename
    if out_path.exists():
        print(f"  SKIP (already exists): {filename}")
        return True

    for attempt in range(1, retries + 1):
        try:
            print(f"  Attempt {attempt}/{retries} for {filename} ...")
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(
                        aspect_ratio="1:1",
                        image_size="512",
                    ),
                ),
            )

            # Extract image from response
            for part in response.parts:
                if part.inline_data is not None:
                    genai_img = part.as_image()
                    # Convert genai Image to PIL Image via bytes
                    import io
                    pil_img = Image.open(io.BytesIO(genai_img.image_bytes))
                    pil_img = pil_img.resize((128, 128), Image.LANCZOS)
                    pil_img.save(str(out_path), "PNG")
                    print(f"  OK: {filename} ({pil_img.size})")
                    return True

            print(f"  WARNING: No image returned for {filename}")

        except Exception as e:
            print(f"  ERROR on attempt {attempt}: {e}")
            if attempt < retries:
                wait = 5 * attempt
                print(f"  Waiting {wait}s before retry ...")
                time.sleep(wait)

    print(f"  FAILED: {filename}")
    return False


def main():
    print(f"Generating {len(ICONS)} callout icons into {OUTPUT_DIR}")
    print(f"Model: {MODEL}\n")

    results = {}
    for i, (filename, prompt) in enumerate(ICONS, 1):
        print(f"[{i}/{len(ICONS)}] {filename}")
        ok = generate_icon(filename, prompt)
        results[filename] = ok
        # Small delay between requests to avoid rate limits
        if i < len(ICONS):
            time.sleep(2)

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    success = sum(1 for v in results.values() if v)
    print(f"  Success: {success}/{len(ICONS)}")
    for filename, ok in results.items():
        status = "OK" if ok else "FAILED"
        print(f"  [{status}] {filename}")

    if success < len(ICONS):
        sys.exit(1)


if __name__ == "__main__":
    main()
