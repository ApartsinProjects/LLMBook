"""Render LaTeX equations to high-DPI PNG via KaTeX + headless Chromium.

Used to give the Kindle EPUB reliable, pixel-identical math (Kindle's MathML
support is gated on Enhanced Typesetting and breaks across apps; images render
everywhere). The website is unaffected -- it keeps client-side KaTeX.

Reads a manifest written by the html2epub build:
    .book-update/math-manifest.json  =  { key: {"tex": "...", "display": bool} }
Renders each entry (KaTeX HTML output, the same as the website) and writes:
    .book-update/math-png-cache/<key>.png   (pngquant-compressed)

The build (math_render + builder PNG step) looks up <key>.png and swaps the
MathML for <img>. Run order: build (writes manifest) -> this script -> build.

Usage:
  py -3 scripts/build_math_png_cache.py            # render everything in manifest
  py -3 scripts/build_math_png_cache.py --selftest # render a few sample eqs to /tmp
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
KATEX_DIST = ROOT / "KDP/build/node_modules/katex/dist"
CACHE = ROOT / ".book-update/math-png-cache"
MANIFEST = ROOT / ".book-update/math-manifest.json"
PNGQUANT = ROOT / ".tools/pngquant/pngquant.exe"

# Render scale: 3x device pixels -> crisp on high-DPI Kindle screens.
SCALE = 3


_SHELL_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="katex.min.css">
<style>
  body { margin: 0; background: #ffffff; }
  /* Shrink-wrap every equation so element.screenshot() is tight (KaTeX's
     .katex-display is block+centered by default, padding the PNG to viewport
     width otherwise). */
  .eq { display: inline-block; padding: 2px 6px; background: #ffffff; color: #000000; }
  .katex { color: #000000; }
  .katex-display { display: inline-block !important; text-align: left !important; margin: 0 !important; }
  .katex-display > .katex { text-align: left !important; }
</style>
<script src="katex.min.js"></script>
</head><body></body></html>"""

_RENDER_JS = """(items) => {
  const body = document.body;
  for (const it of items) {
    const el = document.createElement('div');
    el.className = 'eq';
    el.id = 'eq_' + it.key;
    body.appendChild(el);
    try { katex.render(it.tex, el, {displayMode: !!it.display, throwOnError: false, output: 'html'}); }
    catch (e) { el.textContent = it.tex; }
  }
  return items.length;
}"""


def render(items: list[dict], out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = KATEX_DIST / "_mathrender_tmp.html"   # in dist so katex.min.css/js + fonts resolve
    html_path.write_text(_SHELL_HTML, encoding="utf-8")
    n = 0
    payload = [{"key": it["key"], "tex": it["tex"], "display": it["display"]} for it in items]
    try:
        with sync_playwright() as p:
            br = p.chromium.launch()
            pg = br.new_page(device_scale_factor=SCALE, viewport={"width": 1400, "height": 1000})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.goto(html_path.as_uri())
            pg.wait_for_function("typeof katex !== 'undefined'", timeout=60000)
            pg.evaluate(_RENDER_JS, payload)   # data passed as JS arg (no HTML embedding)
            if errs:
                print("  [pageerror]", errs[:3])
            pg.wait_for_timeout(400)  # fonts settle
            for it in items:
                el = pg.query_selector(f'#eq_{it["key"]}')
                if el is None:
                    print("  [miss]", it["key"]); continue
                png = out_dir / f'{it["key"]}.png'
                try:
                    el.screenshot(path=str(png))
                    n += 1
                except Exception as e:
                    print("  [shot-fail]", it["key"], str(e)[:60])
            br.close()
    finally:
        html_path.unlink(missing_ok=True)
    # pngquant compress in place
    if PNGQUANT.exists():
        pngs = [str(out_dir / f'{it["key"]}.png') for it in items if (out_dir / f'{it["key"]}.png').exists()]
        for i in range(0, len(pngs), 50):
            batch = pngs[i:i+50]
            subprocess.run([str(PNGQUANT), "--force", "--ext", ".png", "--skip-if-larger",
                            "--quality=70-95", "--"] + batch,
                           capture_output=True)
    return n


def main():
    if "--selftest" in sys.argv:
        items = [
            {"key": "t_ce", "tex": r"\mathcal{L} = -\frac{1}{n} \sum y_{i} \log(p_{i})", "display": True},
            {"key": "t_mse", "tex": r"\frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i - y_i)^2", "display": True},
            {"key": "t_aligned", "tex": r"\begin{aligned} a &= b + c \\ &= d \end{aligned}", "display": True},
            {"key": "t_inline", "tex": r"x_{<t}", "display": False},
            {"key": "t_matrix", "tex": r"A = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}", "display": True},
        ]
        out = Path("C:/Users/apart/AppData/Local/Temp/math-selftest")
        n = render(items, out)
        print(f"selftest rendered {n} -> {out}")
        return
    if not MANIFEST.exists():
        print("no manifest at", MANIFEST, "- run the build once first to generate it.")
        sys.exit(1)
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = [{"key": k, "tex": v["tex"], "display": bool(v["display"])} for k, v in data.items()]
    # Skip already-cached
    todo = [it for it in items if not (CACHE / f'{it["key"]}.png').exists()]
    print(f"manifest: {len(items)} equations, {len(todo)} to render")
    if todo:
        n = render(todo, CACHE)
        print(f"rendered {n} new PNGs -> {CACHE}")
    else:
        print("cache already complete")


if __name__ == "__main__":
    main()
