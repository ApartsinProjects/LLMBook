"""Tile several PNGs into one labelled montage, so many diagrams can be
inspected in a single multimodal Read (context-efficient comparison).

Usage: montage.py <out.png> [cols] label=path label=path ...
"""
import sys
from PIL import Image, ImageDraw

def main():
    out = sys.argv[1]
    args = sys.argv[2:]
    cols = 3
    if args and args[0].isdigit():
        cols = int(args[0]); args = args[1:]
    pairs = [a.split("=", 1) for a in args]
    cells = []
    cell_w = 540
    for lbl, p in pairs:
        im = Image.open(p).convert("RGB")
        r = cell_w / im.width
        cells.append((lbl, im.resize((cell_w, int(im.height * r)))))
    rows = (len(cells) + cols - 1) // cols
    pad, label_h = 10, 22
    cell_h = max(im.height for _, im in cells) + label_h
    W = cols * (cell_w + pad) + pad
    H = rows * (cell_h + pad) + pad
    canvas = Image.new("RGB", (W, H), "#eeeeee")
    d = ImageDraw.Draw(canvas)
    for i, (lbl, im) in enumerate(cells):
        cx = pad + (i % cols) * (cell_w + pad)
        cy = pad + (i // cols) * (cell_h + pad)
        d.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill="white", outline="#bbb")
        d.text((cx + 6, cy + 5), lbl, fill="#111")
        canvas.paste(im, (cx, cy + label_h))
    canvas.save(out)
    print("wrote", out, canvas.size)

if __name__ == "__main__":
    main()
