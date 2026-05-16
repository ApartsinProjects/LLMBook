"""SVG pipeline: LaTeX -> MathJax SVG -> Kindle-safe markup.

Why this exists separately from render_png.py: SVG is the compact
inline path. PNG is the bulletproof rasterized path. They take the
same input (list of items) and produce different outputs (str vs
bytes), so it's clearer to keep them in separate modules.

What this does:
    1. Bundles items into JSON
    2. Pipes JSON to Node running scripts/tex2svg.js
    3. Reads SVG strings back
    4. Post-processes:
         a. `currentColor` -> `#000`     (Kindle theme switcher does not
            resolve currentColor through <use> shadow DOM)
         b. width/height in ex|em -> px  (Kindle treats ex/em as
            sub-pixel values, giving illegible glyphs)

See LESSONS.md L2, L3, L4 for the underlying KPV3 bugs.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEX2SVG_JS = SCRIPT_DIR / "tex2svg.js"

# Where mathjax-full is installed. Override with MATH2EPUB_MATHJAX env var.
DEFAULT_MATHJAX_DIR = Path("E:/Tools/mathjax")


def _resolve_mathjax_dir() -> Path:
    override = os.environ.get("MATH2EPUB_MATHJAX")
    if override:
        return Path(override)
    return DEFAULT_MATHJAX_DIR


def _post_process(svg: str) -> str:
    """Apply the two Kindle-required transforms to an SVG string."""
    # L3: currentColor does not resolve through <use> shadow DOM
    svg = svg.replace('stroke="currentColor"', 'stroke="#000"')
    svg = svg.replace('fill="currentColor"', 'fill="#000"')

    # L4: ex/em units are interpreted as sub-pixel by Kindle. Convert to px.
    # Conversion factor matches tex2svg.js per-render options em=24, ex=12.
    UNIT_PX = {"ex": 12, "em": 24, "pt": 1.33, "px": 1}
    def _convert(m: re.Match) -> str:
        attr, value, unit = m.group(1), float(m.group(2)), m.group(3)
        px = value * UNIT_PX.get(unit, 1)
        return f'{attr}="{px:.1f}px"'
    svg = re.sub(r'(width|height)="(\d+(?:\.\d+)?)(ex|em|pt)"', _convert, svg)
    return svg


def render_batch(items: list[dict]) -> dict[str, str]:
    """Render a batch of {id, tex, display} dicts to post-processed SVG strings.

    Spawns Node once. Use this instead of per-call render() when you have
    more than a handful of expressions: Node startup is ~500ms.
    """
    mathjax_dir = _resolve_mathjax_dir()
    node_modules = mathjax_dir / "node_modules"
    if not node_modules.exists():
        raise FileNotFoundError(
            f"Expected MathJax node_modules at {node_modules}. "
            f"Set MATH2EPUB_MATHJAX env var to override."
        )

    payload = json.dumps([
        {"id": str(it["id"]), "tex": it["tex"], "display": bool(it.get("display", False))}
        for it in items
    ])

    env = {**os.environ, "NODE_PATH": str(node_modules)}
    proc = subprocess.run(
        ["node", str(TEX2SVG_JS)],
        input=payload, capture_output=True, text=True,
        env=env, timeout=120, encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"tex2svg.js failed: {proc.stderr}")

    out: dict[str, str] = {}
    for r in json.loads(proc.stdout):
        if r.get("error"):
            raise RuntimeError(f"MathJax parse error for id={r['id']}: {r['error']}")
        out[r["id"]] = _post_process(r.get("svg", ""))
    return out


def render(tex: str, display: bool = False) -> str:
    """Render a single LaTeX expression to a post-processed SVG string."""
    result = render_batch([{"id": "0", "tex": tex, "display": display}])
    return result["0"]


if __name__ == "__main__":
    # Quick sanity check: render one inline and one display expression.
    samples = [
        {"id": "a", "tex": r"y_i", "display": False},
        {"id": "b", "tex": r"\frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2", "display": True},
    ]
    out = render_batch(samples)
    for k, v in out.items():
        print(f"[{k}] {v[:80]}{'...' if len(v) > 80 else ''}")
