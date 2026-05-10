"""
Regenerate a single book diagram via Google Imagen 4.

Writes 4 variants per call to KDP/diagrams/regenerated/{figure}_v{TS}_{N}.png.
Does NOT replace any source figure; the user picks the best variant manually.

Usage:
    python KDP/build/regenerate_diagram.py \
        --figure fig-4.2.2-decoder-only \
        --concept "decoder-only Transformer ..." \
        --aspect portrait
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "KDP" / "diagrams" / "regenerated"

STYLE_BOILERPLATE = (
    "Technical infographic for an AI textbook (Kindle e-book), "
    "modern flat-vector style, clean white background, "
    "max 6 distinct colors (use a coherent palette: deep navy, teal, "
    "amber/gold, soft red, light gray, white), crisp sans-serif labels, "
    "thin precise arrows with clear directionality, well-spaced layout. "
    "AVOID: photorealism, clipart, decorative elements, 3D perspective, "
    "drop shadows, gradients on text, labels exceeding 4 words, "
    "horizontal flow when concept is sequential top-to-bottom, "
    "boxes that contain only generic text without an icon or symbol. "
    "Render all label text crisply and spelled exactly as listed."
)


def load_config() -> dict:
    cfg_path = Path.home() / ".gemini-imagegen.json"
    if not cfg_path.exists():
        print(f"ERROR: {cfg_path} not found.", file=sys.stderr)
        sys.exit(3)
    return json.loads(cfg_path.read_text())


def build_prompt(concept: str) -> str:
    return f"{concept}\n\nVisual style: {STYLE_BOILERPLATE}"


def call_imagen(client, model: str, prompt: str, aspect: str, n: int) -> list[bytes]:
    from google.genai import types
    aspect_ratio = "3:4" if aspect == "portrait" else "4:3"
    print(f"  Imagen model: {model}, aspect {aspect_ratio}, n={n}")
    resp = client.models.generate_images(
        model=model,
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=n,
            aspect_ratio=aspect_ratio,
            safety_filter_level="BLOCK_LOW_AND_ABOVE",
        ),
    )
    if not resp.generated_images:
        raise RuntimeError("Imagen returned no images")
    return [img.image.image_bytes for img in resp.generated_images]


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--figure", required=True, help="Figure id, e.g. fig-4.2.2-decoder-only")
    p.add_argument("--concept", required=True, help="Concept description prompt body")
    p.add_argument("--aspect", choices=["portrait", "landscape"], default="portrait")
    p.add_argument("--n", type=int, default=4)
    p.add_argument("--model", default="imagen-4.0-generate-001")
    args = p.parse_args(argv)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        from google import genai
    except ImportError:
        print("ERROR: google-genai not installed.", file=sys.stderr)
        return 3

    cfg = load_config()
    client = genai.Client(api_key=cfg["api_key"])

    prompt = build_prompt(args.concept)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    print(f"\n[{args.figure}] aspect={args.aspect} n={args.n}")
    print(f"  Prompt ({len(prompt)} chars): {prompt[:200]}...")

    t0 = time.time()
    try:
        images = call_imagen(client, args.model, prompt, args.aspect, args.n)
    except Exception as e:
        print(f"  ERROR: {e}")
        return 2
    elapsed = time.time() - t0
    print(f"  Generated {len(images)} images in {elapsed:.1f}s")

    paths = []
    for i, data in enumerate(images, start=1):
        out = OUT_DIR / f"{args.figure}_v{ts}_{i}.png"
        out.write_bytes(data)
        print(f"  Wrote {out.relative_to(PROJECT_ROOT)} ({len(data) / 1024:.1f} KB)")
        paths.append(out)

    # Also save prompt next to the variants for reproducibility.
    prompt_path = OUT_DIR / f"{args.figure}_v{ts}_prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
