"""PNG pipeline: LaTeX -> matplotlib mathtext -> 300dpi PNG bytes.

Why use PNG when SVG works?
    - KDP's converter has stripped <svg> attributes in past Kindle versions.
      PNG is the historically safe bet for math on Kindle.
    - matplotlib mathtext has no <defs>/<use> shadow DOM issues.
    - Embed via <img src="img/eq###.png" alt="..."> with bundled files
      (not data: URIs, see LESSONS.md L5).

Trade-off: PNG files are 2-5 KB each, so an EPUB with 300 equations
gains ~1 MB. SVG is ~500 bytes per inline expression.
"""
from __future__ import annotations

import io
from pathlib import Path

# matplotlib must be imported with Agg backend before pyplot to avoid
# the default Tk backend trying to open a window in headless contexts.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Computer Modern matches the LaTeX look readers expect and pairs well
# with serif body text. STIX Two is an alternative (`'stix'`) for a
# slightly more modern serif.
matplotlib.rcParams["mathtext.fontset"] = "cm"


def render(tex: str, display: bool = False, fontsize: int | None = None,
           dpi: int = 300) -> bytes:
    """Render one LaTeX expression to PNG bytes (transparent background).

    Args:
        tex: LaTeX source, no surrounding $...$ delimiters.
        display: True for display-math (slightly larger glyphs).
        fontsize: Override the default (14 inline, 16 display).
        dpi: Render resolution. 300 looks crisp on Paperwhite 300dpi screens.
    """
    if fontsize is None:
        fontsize = 16 if display else 14

    fig = plt.figure(figsize=(0.1, 0.1), dpi=dpi)
    fig.patch.set_alpha(0)  # transparent so it overlays page color
    fig.text(0.5, 0.5, f"${tex}$",
             fontsize=fontsize, ha="center", va="center", color="black")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, transparent=True,
                bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    return buf.getvalue()


def render_batch(items: list[dict]) -> dict[str, bytes]:
    """Render a batch of {id, tex, display} dicts to PNG bytes.

    matplotlib has no batch primitive; this is just a loop. Each render
    spawns a fresh Figure to avoid memory growth across long batches.
    """
    return {
        str(it["id"]): render(
            it["tex"],
            display=bool(it.get("display", False)),
            fontsize=it.get("fontsize"),
            dpi=it.get("dpi", 300),
        )
        for it in items
    }


if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent / "_smoke_png"
    out_dir.mkdir(exist_ok=True)
    samples = [
        {"id": "a", "tex": r"y_i", "display": False},
        {"id": "b", "tex": r"\frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2",
         "display": True},
    ]
    out = render_batch(samples)
    for k, v in out.items():
        p = out_dir / f"eq_{k}.png"
        p.write_bytes(v)
        print(f"[{k}] wrote {p} ({len(v):,} bytes)")
