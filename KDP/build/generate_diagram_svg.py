"""Generate technical diagrams as SVG via Claude API.

WHY: image-generation models (Imagen, DALL-E) garble text labels — bad for
technical diagrams where labels are mission-critical. LLMs that produce
RAW SVG markup encode text as literal `<text>` elements that always render
correctly. SVG is also vector (scales infinitely), version-controllable
(plain text), and can be hand-edited.

This is the Tier 1 implementation from KDP/DIAGRAM_PIPELINE.md.

Usage:
    python KDP/build/generate_diagram_svg.py \\
        --figure fig-4.2.2-decoder-only \\
        --concept "decoder-only Transformer: token+pos -> N x [LN+CausalAttn+residual+LN+FFN+residual] -> Final LN -> Linear -> Softmax. Show ghost blocks for x N. Dotted blue arrows for residuals." \\
        --aspect portrait \\
        --variants 3

Outputs:
    KDP/diagrams/svg/{figure}_v{N}.svg            (raw SVG source)
    KDP/diagrams/svg/{figure}_v{N}.png            (rasterized for PNG-only readers)
    KDP/diagrams/svg/{figure}_review.md           (per-variant review notes)
    KDP/diagrams/svg/{figure}_v{N}_prompt.txt     (LLM prompt used for reproducibility)
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = PROJECT_ROOT / "KDP/diagrams/svg"


def system_prompt() -> str:
    return """You are a technical illustrator producing SVG diagrams for an AI textbook.

Your output MUST be a single valid <svg>...</svg> document. No markdown fences,
no explanation, no commentary. Just the SVG. The first character of your reply
must be `<` and the last must be `>`.

DESIGN CONSTRAINTS:
- viewBox should match the requested aspect (portrait 600x800, landscape 800x600, square 700x700)
- White background. Dark text (#1a1a2e) for primary labels. Use a coordinated 5-color palette:
  primary navy #1a4078, accent gold #d4b96a, soft purple #722f8a, soft green #1f7a3a, neutral gray #6b7280
- Sans-serif font stack for labels (use `font-family="Helvetica, Arial, sans-serif"`)
- Body text 14-16px. Labels on boxes 13-15px. Avoid going below 12px.
- Boxes: rounded rectangles (rx="6") with light fills (#eef4fa, #f4ecf7, #ecf6ee) and 1.5px strokes
- Arrows: use <marker> for arrowheads. Solid arrows for forward flow, dotted (stroke-dasharray="4,3") for residuals/feedback
- Use linear gradients sparingly (only for hero elements)
- Drop shadows: subtle (filter="drop-shadow(0 2px 3px rgba(0,0,0,0.08))")
- Ghost/repetition indicator: stack 2-3 same-shape elements offset by 6-8px with reduced opacity (0.3, 0.5, 1.0)
- All text is encoded as literal <text> elements — never embed text in <image>

LAYOUT:
- Plan the layout before writing. List elements with x,y coordinates first (as a comment in your SVG, removed before output).
- Top-to-bottom OR left-to-right consistently — never both
- Generous whitespace. Don't pack densely.
- Group related elements with <g> tags so they're easy to manipulate later

STYLE TARGET: clean modern technical infographic. Think MIT-Press textbook diagrams,
Anthropic blog visuals, Distill.pub articles. NOT corporate clipart. NOT casual
hand-drawn. NOT 3D.

TECHNICAL CORRECTNESS: the diagram must accurately represent the concept stated.
Verify every component is in the right place, every arrow goes the right
direction, every label uses the correct technical term."""


def user_prompt(concept: str, aspect: str, figure_name: str) -> str:
    aspects = {
        "portrait": "viewBox=\"0 0 600 800\"  (3:4 portrait, fits Kindle)",
        "landscape": "viewBox=\"0 0 800 600\"  (4:3 landscape)",
        "square": "viewBox=\"0 0 700 700\"  (1:1 square)",
    }
    box = aspects.get(aspect, aspects["portrait"])
    return f"""Generate an SVG diagram for: {figure_name}

CONCEPT (must be accurately represented):
{concept}

ASPECT: {box}

OUTPUT a single complete <svg>...</svg> document. No fences, no preamble.
Begin with `<svg xmlns="http://www.w3.org/2000/svg" {box}>` and end with `</svg>`.
"""


def call_claude(prompt_user: str, prompt_system: str, model: str = "claude-sonnet-4-5") -> str:
    """Call Claude API. Requires ANTHROPIC_API_KEY env var."""
    try:
        import anthropic
    except ImportError:
        print("Installing anthropic SDK...", file=sys.stderr)
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "anthropic"], check=True)
        import anthropic

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=8192,
        system=prompt_system,
        messages=[{"role": "user", "content": prompt_user}],
    )
    return msg.content[0].text


def extract_svg(response: str) -> str:
    """Extract SVG from response. Handle markdown fences if present."""
    response = response.strip()
    # Strip markdown fence if present
    response = re.sub(r"^```(?:svg|xml)?\n", "", response)
    response = re.sub(r"\n```$", "", response)
    response = response.strip()
    # Find first <svg and last </svg>
    start = response.find("<svg")
    end = response.rfind("</svg>")
    if start < 0 or end < 0:
        raise ValueError(f"No <svg>...</svg> found in response (first 200 chars: {response[:200]!r})")
    return response[start:end + len("</svg>")]


def rasterize_svg(svg_path: Path, png_path: Path, max_width: int = 1280) -> bool:
    """Render SVG -> PNG.

    Preference order:
      1. resvg-py (pure-Rust, no system deps; `pip install resvg-py`)
      2. cairosvg (needs GTK runtime on Windows; admin install)
      3. Edge headless screenshot (always available, slowest)
    """
    # Try resvg-py first (no system deps, fastest)
    try:
        import resvg_py
        svg_text = svg_path.read_text(encoding="utf-8")
        png_bytes = resvg_py.svg_to_bytes(svg_string=svg_text, width=max_width)
        if isinstance(png_bytes, list):
            png_bytes = bytes(png_bytes)
        png_path.write_bytes(png_bytes)
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"  resvg-py failed ({e}); trying cairosvg", file=sys.stderr)
    # Fall back to cairosvg (needs GTK on Windows)
    try:
        import cairosvg
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path), output_width=max_width)
        return True
    except Exception as e:
        print(f"  cairosvg failed ({e}); trying Edge headless", file=sys.stderr)
        return rasterize_via_edge(svg_path, png_path, max_width)


def rasterize_via_edge(svg_path: Path, png_path: Path, max_width: int = 1280) -> bool:
    """Fallback: convert SVG to PNG by loading in Edge headless and screenshotting.

    SVG must be wrapped in HTML for Edge to render. We write a temp .html that
    embeds the SVG and use --screenshot.
    """
    import subprocess, tempfile
    edge = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
    if not edge.exists():
        return False
    user_data_dir = tempfile.mkdtemp(prefix="svg_render_", dir="E:/temp")
    try:
        html = f'<!DOCTYPE html><html><body style="margin:0">{svg_path.read_text(encoding="utf-8")}</body></html>'
        tmp_html = svg_path.with_suffix(".html")
        tmp_html.write_text(html, encoding="utf-8")
        cmd = [
            str(edge), "--headless=new", "--disable-gpu", "--no-sandbox",
            f"--user-data-dir={user_data_dir}",
            f"--screenshot={str(png_path).replace('/', chr(92))}",
            f"--window-size={max_width},{int(max_width * 4/3)}",
            tmp_html.resolve().as_uri(),
        ]
        subprocess.run(cmd, capture_output=True, timeout=60)
        tmp_html.unlink(missing_ok=True)
        return png_path.exists()
    finally:
        import shutil
        shutil.rmtree(user_data_dir, ignore_errors=True)


def write_review_md(figure_name: str, concept: str, aspect: str,
                    variants: list[tuple[int, Path, Path | None, str]]) -> Path:
    """Write per-figure review markdown."""
    md_path = OUT_DIR / f"{figure_name}_review.md"
    md = [f"# {figure_name} — variants generated {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
          f"**Concept:**\n\n> {concept}\n",
          f"**Aspect:** {aspect}\n",
          f"**Total variants:** {len(variants)}\n",
          "---\n"]
    for n, svg, png, prompt_path in variants:
        md.append(f"## Variant {n}\n")
        md.append(f"- SVG: [`{svg.name}`](./{svg.name})  ({svg.stat().st_size / 1024:.1f} KB)\n")
        if png and png.exists():
            md.append(f"- PNG: [`{png.name}`](./{png.name})  ({png.stat().st_size / 1024:.1f} KB)\n")
            md.append(f"- ![](./{png.name})\n")
        md.append(f"- Prompt: [`{Path(prompt_path).name}`](./{Path(prompt_path).name})\n\n")
    md.append("---\n\n")
    md.append("## Picking guide\n\n")
    md.append("After visually reviewing the PNGs above, copy the chosen SVG to the source location:\n\n")
    md.append("```bash\n")
    md.append(f"cp KDP/diagrams/svg/{figure_name}_vN.svg path/to/source/figure.svg\n")
    md.append("```\n\n")
    md.append("If the SVG needs minor edits (text positioning, arrow routing), open it in any\n")
    md.append("text editor or vector editor (Inkscape, Affinity Designer, Figma) — SVG is plain text.\n")
    md_path.write_text("".join(md), encoding="utf-8")
    return md_path


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--figure", required=True, help="Figure name (e.g., fig-4.2.2-decoder-only)")
    p.add_argument("--concept", required=True, help="Concept description (the more specific, the better)")
    p.add_argument("--aspect", choices=["portrait", "landscape", "square"], default="portrait")
    p.add_argument("--variants", type=int, default=3, help="Number of variants to generate")
    p.add_argument("--model", default="claude-sonnet-4-5", help="Claude model to use")
    p.add_argument("--no-rasterize", action="store_true", help="Skip PNG generation (SVG only)")
    args = p.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY env var not set.", file=sys.stderr)
        print("Set it via: export ANTHROPIC_API_KEY=sk-ant-...", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    sys_prompt = system_prompt()
    usr_prompt = user_prompt(args.concept, args.aspect, args.figure)

    print(f"Generating {args.variants} SVG variants for {args.figure} (aspect={args.aspect})")
    print(f"  Model: {args.model}")
    print(f"  Concept: {args.concept[:200]}...")
    print()

    variants: list[tuple[int, Path, Path | None, str]] = []

    for v in range(1, args.variants + 1):
        print(f"  Variant {v}/{args.variants}: calling Claude...")
        t0 = time.time()
        try:
            response = call_claude(usr_prompt, sys_prompt, model=args.model)
        except Exception as e:
            print(f"    [FAIL] Claude API error: {e}")
            continue

        elapsed = time.time() - t0
        try:
            svg = extract_svg(response)
        except ValueError as e:
            print(f"    [FAIL] {e}")
            continue

        svg_path = OUT_DIR / f"{args.figure}_v{v}.svg"
        svg_path.write_text(svg, encoding="utf-8")

        # Save the prompt used (for reproducibility)
        prompt_path = OUT_DIR / f"{args.figure}_v{v}_prompt.txt"
        prompt_path.write_text(f"=== SYSTEM ===\n{sys_prompt}\n\n=== USER ===\n{usr_prompt}\n\n=== RAW RESPONSE (first 500) ===\n{response[:500]}",
                                encoding="utf-8")

        png_path = None
        if not args.no_rasterize:
            png_path = OUT_DIR / f"{args.figure}_v{v}.png"
            ok = rasterize_svg(svg_path, png_path)
            if not ok:
                print(f"    [WARN] PNG rasterization failed; SVG saved")
                png_path = None

        variants.append((v, svg_path, png_path, str(prompt_path)))
        png_str = f"+ PNG ({png_path.stat().st_size / 1024:.0f} KB)" if (png_path and png_path.exists()) else ""
        print(f"    [OK] {elapsed:.1f}s  -> {svg_path.name} ({svg_path.stat().st_size / 1024:.1f} KB) {png_str}")

    if not variants:
        print("\n[FAIL] No variants generated.")
        return 1

    review = write_review_md(args.figure, args.concept, args.aspect, variants)
    print(f"\n[OK] {len(variants)} variants in {OUT_DIR.relative_to(PROJECT_ROOT)}")
    print(f"     Review: {review.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
