#!/usr/bin/env python3
"""
Generate avatar images for the 42 Wisdom Council AI agent characters
using Google Gemini's image generation API.

Usage:
    C:\\Users\\apart\\AppData\\Local\\Programs\\Python\\Python311\\python.exe _generate_avatars.py
    C:\\Users\\apart\\AppData\\Local\\Programs\\Python\\Python311\\python.exe _generate_avatars.py --api-key YOUR_KEY

Requires:
    pip install google-genai Pillow
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
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

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
REQUEST_DELAY_SECONDS = 8  # Delay between successive requests (10 req/min limit)


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


def generate_avatar(client, agent: dict, output_path: Path) -> bool:
    """
    Generate a single avatar image with retry logic.
    Returns True on success, False on failure.
    """
    prompt = build_prompt(agent)
    agent_id = agent["id"]

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_images(
                model="imagen-4.0-generate-001",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1",
                ),
            )

            if response.generated_images and len(response.generated_images) > 0:
                image = response.generated_images[0]
                # Save the raw image bytes
                img_bytes = image.image.image_bytes
                output_path.write_bytes(img_bytes)

                # Resize to 256x256 if needed
                with Image.open(output_path) as img:
                    if img.size != (256, 256):
                        img = img.resize((256, 256), Image.LANCZOS)
                        img.save(output_path, "PNG")

                return True
            else:
                print(f"  [attempt {attempt}/{MAX_RETRIES}] No image returned for '{agent_id}'")

        except Exception as e:
            print(f"  [attempt {attempt}/{MAX_RETRIES}] Error for '{agent_id}': {e}")

        if attempt < MAX_RETRIES:
            wait = RETRY_DELAY_SECONDS * attempt
            print(f"  Retrying in {wait}s...")
            time.sleep(wait)

    return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate Wisdom Council avatar images via Google Gemini"
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Google API key (falls back to GOOGLE_API_KEY env var)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate avatars even if the file already exists",
    )
    args = parser.parse_args()

    # Resolve API key
    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: No API key provided.")
        print("  Use --api-key YOUR_KEY or set the GOOGLE_API_KEY environment variable.")
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

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    total = len(agents)
    skipped = 0
    succeeded = 0
    failed = 0

    print(f"Generating avatars for {total} Wisdom Council agents...")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    for i, agent in enumerate(agents, start=1):
        agent_id = agent["id"]
        output_path = OUTPUT_DIR / f"{agent_id}.png"

        # Skip if file already exists (unless forced)
        if output_path.exists() and not args.force:
            print(f"[{i}/{total}] SKIP  {agent_id} (already exists)")
            skipped += 1
            continue

        print(f"[{i}/{total}] Generating {agent_id} ({agent.get('name', '')}, {agent.get('title', '')})...")

        ok = generate_avatar(client, agent, output_path)
        if ok:
            print(f"         Saved to {output_path}")
            succeeded += 1
        else:
            print(f"         FAILED after {MAX_RETRIES} attempts")
            failed += 1

        # Delay between requests to stay within rate limits
        if i < total:
            time.sleep(REQUEST_DELAY_SECONDS)

    # Summary
    print()
    print("=" * 50)
    print(f"Done. Total: {total}, Generated: {succeeded}, Skipped: {skipped}, Failed: {failed}")
    if failed > 0:
        print(f"Re-run the script to retry failed avatars (they were not saved).")
    print("=" * 50)


if __name__ == "__main__":
    main()
