#!/usr/bin/env python3
"""
Generate avatar images for the 42 Wisdom Council AI agent characters
using the Gemini Batch API (50% cost, async processing).

Usage:
    C:\\Users\\apart\\AppData\\Local\\Programs\\Python\\Python311\\python.exe _generate_avatars.py
    C:\\Users\\apart\\AppData\\Local\\Programs\\Python\\Python311\\python.exe _generate_avatars.py --api-key YOUR_KEY

Requires:
    pip install google-genai Pillow
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    from google import genai
except ImportError:
    print("ERROR: google-genai package not found. Install with:")
    print("  pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow package not found. Install with:")
    print("  pip install Pillow")
    sys.exit(1)

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
JSON_PATH = SCRIPT_DIR / "front-matter" / "wisdom-council.json"
OUTPUT_DIR = SCRIPT_DIR / "front-matter" / "images" / "agents"

POLL_INTERVAL = 15  # seconds


def build_prompt(agent: dict) -> str:
    """Build the image generation prompt for a single agent."""
    name = agent.get("name", "Unknown")
    title = agent.get("title", "")
    personality = agent.get("personality", "")
    expertise = agent.get("expertise", "")
    color = agent.get("color", "#3498db")

    return (
        f"A stylized digital portrait avatar of an AI character named '{name}', "
        f"{title}. Personality: {personality}. Expertise: {expertise}. "
        f"Style: modern digital art, dark background with {color} accent glow, "
        f"centered face/bust composition suitable for circular crop, "
        f"expressive and memorable character design, no text."
    )


def run_batch(client, agents, model, force):
    """Submit all avatars as a single batch job at 50% cost."""
    from google.genai import types
    requests = []
    agent_indices = []

    for i, agent in enumerate(agents):
        output_path = OUTPUT_DIR / f"{agent['id']}.png"
        if output_path.exists() and not force:
            print(f"  SKIP (exists): {agent['id']}.png")
            continue

        prompt = build_prompt(agent)
        requests.append(types.InlinedRequest(
            contents=[types.Content(parts=[types.Part(text=prompt)], role="user")],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio="1:1", image_size="1K"),
            ),
        ))
        agent_indices.append(i)

    if not requests:
        print("All avatars already exist. Use --force to regenerate.")
        return

    print(f"Submitting batch of {len(requests)} avatar requests to {model}...")
    print("  (Batch API: 50% cost, async processing)")

    batch_job = client.batches.create(
        model=model,
        src=requests,
        config={"display_name": f"wisdom-avatars-{int(time.time())}"},
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

    print("Batch complete. Saving avatars...")
    saved = 0
    failed = 0

    for resp_idx, resp_wrapper in enumerate(batch_job.dest.inlined_responses):
        if resp_idx >= len(agent_indices):
            break
        agent = agents[agent_indices[resp_idx]]
        output_path = OUTPUT_DIR / f"{agent['id']}.png"

        response = resp_wrapper.response
        if not response or not response.candidates:
            print(f"  FAIL: {agent['id']}.png (no image returned)")
            failed += 1
            continue

        image_saved = False
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data and part.inline_data.data:
                    img_data = part.inline_data.data
                    if isinstance(img_data, str):
                        img_data = base64.b64decode(img_data)
                    output_path.write_bytes(img_data)

                    # Resize to 256x256 if needed
                    with Image.open(output_path) as img:
                        if img.size != (256, 256):
                            img = img.resize((256, 256), Image.LANCZOS)
                            img.save(output_path, "PNG")

                    print(f"  OK: {agent['id']}.png")
                    saved += 1
                    image_saved = True
                    break
            if image_saved:
                break

        if not image_saved:
            print(f"  FAIL: {agent['id']}.png (no image data)")
            failed += 1

    print(f"\nDone: {saved} saved, {failed} failed out of {len(requests)} requested")


def run_sync(client, agents, model, force):
    """Fallback: synchronous generation using Imagen (full price)."""
    from google.genai import types

    total = len(agents)
    succeeded = 0
    failed = 0
    skipped = 0

    for i, agent in enumerate(agents, start=1):
        agent_id = agent["id"]
        output_path = OUTPUT_DIR / f"{agent_id}.png"

        if output_path.exists() and not force:
            print(f"[{i}/{total}] SKIP  {agent_id} (already exists)")
            skipped += 1
            continue

        print(f"[{i}/{total}] Generating {agent_id} ({agent.get('name', '')})...")
        prompt = build_prompt(agent)

        try:
            response = client.models.generate_images(
                model="imagen-4.0-generate-001",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1",
                ),
            )

            if response.generated_images:
                img_bytes = response.generated_images[0].image.image_bytes
                output_path.write_bytes(img_bytes)
                with Image.open(output_path) as img:
                    if img.size != (256, 256):
                        img = img.resize((256, 256), Image.LANCZOS)
                        img.save(output_path, "PNG")
                print(f"         Saved to {output_path}")
                succeeded += 1
            else:
                print(f"         FAIL: no image returned")
                failed += 1
        except Exception as e:
            print(f"         FAIL: {e}")
            failed += 1

        if i < total:
            time.sleep(8)

    print(f"\nDone. Generated: {succeeded}, Skipped: {skipped}, Failed: {failed}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Wisdom Council avatar images via Gemini Batch API (50% cost)"
    )
    parser.add_argument("--api-key", default=None, help="Google API key (falls back to GOOGLE_API_KEY env var)")
    parser.add_argument("--force", action="store_true", help="Regenerate even if file exists")
    parser.add_argument("--sync", action="store_true", help="Use synchronous Imagen API (full price, immediate)")
    parser.add_argument("--model", default=None, help="Gemini model for batch mode")
    args = parser.parse_args()

    # Resolve API key: arg > env > config file
    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        config_path = Path.home() / ".gemini-imagegen.json"
        if config_path.exists():
            config = json.loads(config_path.read_text())
            api_key = config.get("api_key")
    if not api_key:
        print("ERROR: No API key. Use --api-key, set GOOGLE_API_KEY, or create ~/.gemini-imagegen.json")
        sys.exit(1)

    # Load agent data
    if not JSON_PATH.exists():
        print(f"ERROR: Agent data file not found at {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    agents = data.get("agents", [])
    if not agents:
        print("ERROR: No agents found in the JSON file.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)

    model = args.model or "gemini-3.1-flash-image-preview"

    print(f"Generating avatars for {len(agents)} Wisdom Council agents...")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    if args.sync:
        run_sync(client, agents, model, args.force)
    else:
        run_batch(client, agents, model, args.force)


if __name__ == "__main__":
    main()
