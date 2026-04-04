"""
Generate 10 callout-box icons for the LLMCourse textbook using the Gemini Batch API (50% cost).
Each icon is 128x128, flat design, consistent style, suitable for display at 24x24.
"""

import base64
import io
import json
import sys
import time
from pathlib import Path

from PIL import Image

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
config_path = Path.home() / ".gemini-imagegen.json"
if not config_path.exists():
    print("ERROR: ~/.gemini-imagegen.json not found")
    sys.exit(1)

config = json.loads(config_path.read_text())

MODEL = config.get("default_model", "gemini-3.1-flash-image-preview")
OUTPUT_DIR = Path(r"E:\Projects\LLMCourse\styles\icons")
POLL_INTERVAL = 15  # seconds

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
# Batch generation (default, 50% cost)
# ---------------------------------------------------------------------------
def run_batch(client, force=False):
    """Submit all icons as a single batch job at 50% cost."""
    from google.genai import types
    requests = []
    indices = []

    for i, (filename, prompt) in enumerate(ICONS):
        out_path = OUTPUT_DIR / filename
        if out_path.exists() and not force:
            print(f"  SKIP (exists): {filename}")
            continue

        requests.append(types.InlinedRequest(
            contents=[types.Content(parts=[types.Part(text=prompt)], role="user")],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="1:1", image_size="512"),
            ),
        ))
        indices.append(i)

    if not requests:
        print("All icons already exist. Use --force to regenerate.")
        return

    print(f"Submitting batch of {len(requests)} icon requests to {MODEL}...")
    print("  (Batch API: 50% cost, async processing)")

    batch_job = client.batches.create(
        model=MODEL,
        src=requests,
        config={"display_name": f"callout-icons-{int(time.time())}"},
    )

    job_name = batch_job.name
    print(f"  Job: {job_name}")
    print(f"  Polling every {POLL_INTERVAL}s...")

    while True:
        batch_job = client.batches.get(name=job_name)
        state = batch_job.state.name if hasattr(batch_job.state, "name") else str(batch_job.state)
        if state in ("JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED"):
            break
        print(f"  State: {state}")
        time.sleep(POLL_INTERVAL)

    if state != "JOB_STATE_SUCCEEDED":
        print(f"Batch job {state}.")
        return

    print("Batch complete. Saving icons...")
    saved = 0
    failed = 0

    for resp_idx, resp_wrapper in enumerate(batch_job.dest.inlined_responses):
        if resp_idx >= len(indices):
            break
        icon_idx = indices[resp_idx]
        filename = ICONS[icon_idx][0]
        out_path = OUTPUT_DIR / filename

        response = resp_wrapper.response
        if not response or not response.candidates:
            print(f"  FAIL: {filename} (no image returned)")
            failed += 1
            continue

        image_saved = False
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data and part.inline_data.data:
                    img_data = part.inline_data.data
                    if isinstance(img_data, str):
                        img_data = base64.b64decode(img_data)
                    pil_img = Image.open(io.BytesIO(img_data))
                    pil_img = pil_img.resize((128, 128), Image.LANCZOS)
                    pil_img.save(str(out_path), "PNG")
                    print(f"  OK: {filename} (128x128)")
                    saved += 1
                    image_saved = True
                    break
            if image_saved:
                break

        if not image_saved:
            print(f"  FAIL: {filename} (no image data)")
            failed += 1

    print(f"\nDone: {saved} saved, {failed} failed out of {len(requests)} requested")


# ---------------------------------------------------------------------------
# Sync generation (fallback, full price)
# ---------------------------------------------------------------------------
def run_sync(client, force=False):
    """Synchronous generation, one at a time (full price)."""
    from google.genai import types

    results = {}
    for i, (filename, prompt) in enumerate(ICONS, 1):
        out_path = OUTPUT_DIR / filename
        if out_path.exists() and not force:
            print(f"  SKIP (exists): {filename}")
            results[filename] = True
            continue

        print(f"[{i}/{len(ICONS)}] {filename}")
        ok = False
        for attempt in range(1, 4):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(aspect_ratio="1:1", image_size="512"),
                    ),
                )
                for part in response.parts:
                    if part.inline_data is not None:
                        genai_img = part.as_image()
                        pil_img = Image.open(io.BytesIO(genai_img.image_bytes))
                        pil_img = pil_img.resize((128, 128), Image.LANCZOS)
                        pil_img.save(str(out_path), "PNG")
                        print(f"  OK: {filename} (128x128)")
                        ok = True
                        break
                if ok:
                    break
            except Exception as e:
                print(f"  ERROR attempt {attempt}: {e}")
                if attempt < 3:
                    time.sleep(5 * attempt)

        results[filename] = ok
        if not ok:
            print(f"  FAILED: {filename}")
        if i < len(ICONS):
            time.sleep(2)

    success = sum(1 for v in results.values() if v)
    print(f"\nDone: {success}/{len(ICONS)} icons generated")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate callout icons via Gemini Batch API (50% cost)")
    parser.add_argument("--force", action="store_true", help="Regenerate even if file exists")
    parser.add_argument("--sync", action="store_true", help="Use synchronous API (full price, immediate)")
    args = parser.parse_args()

    from google import genai
    client = genai.Client(api_key=config["api_key"])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating {len(ICONS)} callout icons into {OUTPUT_DIR}")
    print(f"Model: {MODEL}\n")

    if args.sync:
        run_sync(client, args.force)
    else:
        run_batch(client, args.force)


if __name__ == "__main__":
    main()
