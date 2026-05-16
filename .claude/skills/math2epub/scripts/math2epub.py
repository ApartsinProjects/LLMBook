r"""Unified math2epub API.

Single entry point for callers that don't care which pipeline runs.

Usage:
    import sys
    sys.path.insert(0, ".claude/skills/math2epub/scripts")
    from math2epub import render, render_batch

    svg_str   = render(r"y_i", pipeline="svg", display=False)
    png_bytes = render(r"E = mc^2", pipeline="png", display=True)

    items = [
        {"id": "eq1", "tex": r"y_i", "display": False},
        {"id": "eq2", "tex": r"\sum_i x_i", "display": True},
    ]
    svgs = render_batch(items, pipeline="svg")   # {id: str}
    pngs = render_batch(items, pipeline="png")   # {id: bytes}

Pipelines exposed:
    "svg" - MathJax SVG, post-processed for Kindle (LESSONS L2/L3/L4)
    "png" - matplotlib mathtext at 300dpi (LESSONS L10/L11)

Two pipelines we explored but rejected: MathML (broken on KPV3) and
plain HTML (ugly fractions, no integral/sum). See LESSONS.md.
"""
from __future__ import annotations

from typing import Any

import render_png
import render_svg

PIPELINES = ("svg", "png")


def render(tex: str, pipeline: str = "svg", display: bool = False) -> Any:
    """Render one LaTeX expression. Returns str for svg, bytes for png."""
    if pipeline == "svg":
        return render_svg.render(tex, display=display)
    if pipeline == "png":
        return render_png.render(tex, display=display)
    raise ValueError(
        f"Unknown pipeline {pipeline!r}. Use one of {PIPELINES}."
    )


def render_batch(items: list[dict], pipeline: str = "svg") -> dict:
    """Render a batch of {id, tex, display} dicts.

    Returns {id: str} for svg, {id: bytes} for png.
    """
    if pipeline == "svg":
        return render_svg.render_batch(items)
    if pipeline == "png":
        return render_png.render_batch(items)
    raise ValueError(
        f"Unknown pipeline {pipeline!r}. Use one of {PIPELINES}."
    )


if __name__ == "__main__":
    # Smoke test both pipelines on the same input.
    items = [
        {"id": "inline", "tex": r"y_i", "display": False},
        {"id": "block",
         "tex": r"\frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2",
         "display": True},
    ]
    print("=== SVG ===")
    for k, v in render_batch(items, pipeline="svg").items():
        print(f"[{k}] {len(v):,} chars, head: {v[:60]}...")
    print()
    print("=== PNG ===")
    for k, v in render_batch(items, pipeline="png").items():
        print(f"[{k}] {len(v):,} bytes")
