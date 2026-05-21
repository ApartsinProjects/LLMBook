"""Render diagrams to PNG for visual inspection / comparison.

Faithful rendering via Playwright (real Chromium), so inline SVGs look exactly
as they do in the book (gradients, filters, system-ui fonts). Also wraps the
native generators so every candidate format lands as a PNG that can be opened
with the multimodal Read tool and compared side by side.

Modes:
  svgfile  <in.svg>            <out.png>     render a standalone .svg
  svg      <page.html> <index> <out.png>     render the Nth inline <svg> in a page
  mermaid  <in.mmd>            <out.png>     via mmdc
  dot      <in.dot>            <out.png>     via Graphviz
  d2       <in.d2>             <out.png>     via D2

Tool binaries (portable, no admin) live under .tools/.
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = ROOT / ".tools"
GV_BIN = TOOLS / "Graphviz-14.1.5-win64" / "bin"
DOT = GV_BIN / "dot.exe"
D2 = TOOLS / "d2-v0.7.1" / "bin" / "d2.exe"
# put graphviz + d2 on PATH for any child process / python binding
os.environ["PATH"] = f"{GV_BIN};{D2.parent};" + os.environ.get("PATH", "")

SVG_BLOCK = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL | re.I)

HTML_TMPL = (
    '<!doctype html><html><head><meta charset="utf-8">'
    "<style>body{margin:0;padding:16px;background:#fff;"
    "font-family:system-ui,-apple-system,'Segoe UI',sans-serif;}"
    "svg{display:block;}</style></head><body>{body}</body></html>"
)


def render_html_to_png(html: str, out_png: str, scale: int = 2):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(device_scale_factor=scale)
        pg.set_content(html, wait_until="load")
        pg.wait_for_timeout(150)
        el = pg.query_selector("svg") or pg.query_selector("body")
        el.screenshot(path=out_png)
        b.close()


def svg_to_png(svg: str, out_png: str):
    render_html_to_png(HTML_TMPL.replace("{body}", svg), out_png)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    mode = sys.argv[1]
    out = sys.argv[-1]
    if mode == "svgfile":
        svg_to_png(Path(sys.argv[2]).read_text(encoding="utf-8"), out)
    elif mode == "svg":
        html = Path(sys.argv[2]).read_text(encoding="utf-8", errors="ignore")
        idx = int(sys.argv[3])
        blocks = SVG_BLOCK.findall(html)
        if idx >= len(blocks):
            print(f"only {len(blocks)} svg(s) in {sys.argv[2]}")
            sys.exit(2)
        svg_to_png(blocks[idx], out)
    elif mode == "mermaid":
        cfg = ROOT / "scripts" / "mermaid" / "mermaid-config-elk.json"
        cmd = ["mmdc", "-i", sys.argv[2], "-o", out, "-b", "white", "-s", "2"]
        if cfg.exists():
            cmd += ["-c", str(cfg)]
        subprocess.run(cmd, shell=True, check=True)
    elif mode == "dot":
        subprocess.run([str(DOT), "-Tpng", "-Gdpi=144", sys.argv[2], "-o", out], check=True)
    elif mode == "d2":
        env = dict(os.environ, D2_LAYOUT="elk")
        subprocess.run([str(D2), "--scale", "2", sys.argv[2], out], check=True, env=env)
    else:
        print("unknown mode", mode)
        sys.exit(1)
    print("wrote", out)


if __name__ == "__main__":
    main()
