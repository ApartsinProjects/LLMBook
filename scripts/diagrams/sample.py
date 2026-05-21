"""Render a diverse sample of existing inline SVGs (one per book part) into one
labelled montage, for a context-efficient quality scan via the Read tool."""
import json, re, sys
from pathlib import Path
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent.parent
SVG = re.compile(r"<svg\b[^>]*>.*?</svg>", re.S | re.I)
TM = ("<!doctype html><meta charset=utf-8><style>body{margin:0;padding:14px;"
      "background:#fff;font-family:system-ui,'Segoe UI',sans-serif}svg{display:block}"
      "</style>__B__")
recs = [json.loads(l) for l in (ROOT / ".book-update/svg-lint.jsonl")
        .read_text(encoding="utf-8").splitlines() if l.strip()]
bypart = {}
for r in recs:
    bypart.setdefault(r["file"].split("/")[0], []).append(r)
# selection modes:
#   (no args)         one diagram per part
#   complex [N]       top-N most-complex flowcharts (by arrow count), default 15
#   <substr> ...      restrict to parts whose path contains any substring
sample = []
if len(sys.argv) > 1 and sys.argv[1] == "complex":
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    sample = sorted([r for r in recs if r["flowchartish"]],
                    key=lambda r: -r["n_arrows"])[:n]
else:
    want = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    for part, rs in sorted(bypart.items()):
        if want and not any(w in part for w in want):
            continue
        rs.sort(key=lambda r: (0 if r["flowchartish"] else 1, r["svg_index"]))
        sample.append(rs[0])
P = ROOT / ".tools/_pilot"
P.mkdir(exist_ok=True, parents=True)
cells = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(device_scale_factor=2)
    for i, r in enumerate(sample):
        html = (ROOT / r["file"]).read_text(encoding="utf-8", errors="ignore")
        blocks = SVG.findall(html)
        if r["svg_index"] >= len(blocks):
            continue
        pg.set_content(TM.replace("__B__", blocks[r["svg_index"]]), wait_until="load")
        pg.wait_for_timeout(120)
        el = pg.query_selector("svg")
        out = P / f"samp_{i}.png"
        el.screenshot(path=str(out))
        lbl = (r["file"].split("/")[-1].replace("section-", "").replace(".html", "")
               + (" [flow]" if r["flowchartish"] else ""))
        cells.append((lbl, str(out)))
    b.close()
cw = 500
ims = [(l, Image.open(p).convert("RGB")) for l, p in cells]
ims = [(l, im.resize((cw, int(im.height * cw / im.width)))) for l, im in ims]
cols = 3
rows = (len(ims) + cols - 1) // cols
pad, lh = 8, 20
ch = max(im.height for _, im in ims) + lh
W = cols * (cw + pad) + pad
H = rows * (ch + pad) + pad
cv = Image.new("RGB", (W, H), "#e8e8e8")
d = ImageDraw.Draw(cv)
for i, (l, im) in enumerate(ims):
    x = pad + (i % cols) * (cw + pad)
    y = pad + (i // cols) * (ch + pad)
    d.rectangle([x, y, x + cw, y + ch], fill="white", outline="#aaa")
    d.text((x + 5, y + 4), l, fill="#111")
    cv.paste(im, (x, y + lh))
out = P / "sample_grid.png"
cv.save(out)
print("wrote", out, cv.size, "n=", len(ims))
