"""Render an SVG file to PNG using Playwright (headless Chromium).

Usage:
    python render_svg_to_png.py <svg_path> [png_path] [scale]
"""

import sys
import os
import re
from playwright.sync_api import sync_playwright


def render(svg_path, png_path=None, scale=2):
    if png_path is None:
        png_path = svg_path.rsplit(".", 1)[0] + ".png"

    with open(svg_path, "r", encoding="utf-8") as f:
        svg = f.read()

    # Pull viewBox to fix viewport size
    m = re.search(r'viewBox="([\d.\s\-]+)"', svg)
    if m:
        parts = m.group(1).split()
        vw = float(parts[2])
        vh = float(parts[3])
    else:
        vw, vh = 1400, 820

    html = (
        "<html><head><style>body{margin:0;padding:0;background:#ffffff}"
        "svg{display:block}</style></head><body>" + svg + "</body></html>"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": int(vw), "height": int(vh)},
            device_scale_factor=scale,
        )
        page.set_content(html)
        page.locator("svg").first.screenshot(path=png_path)
        browser.close()

    size = os.path.getsize(png_path)
    print(f"  rendered {os.path.basename(png_path)} ({size} bytes)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: render_svg_to_png.py <svg> [png] [scale]")
        sys.exit(1)
    svg_path = sys.argv[1]
    png_path = sys.argv[2] if len(sys.argv) > 2 else None
    scale = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    render(svg_path, png_path, scale)
