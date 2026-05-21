"""Geometric correctness linter for hand-authored inline SVG diagrams.

The book's existing audit plugins (SVG_TEXT_CLIPPING, SVG_OVERLAP, etc.) check
text bounds and panel symmetry but have NO check for the most common visual
breakage in LLM-authored SVGs: arrows whose heads do not actually land on a
node. Those SVGs are drawn with absolute pixel coordinates and no layout
engine, so a miscount leaves an arrowhead floating in empty space or a label
outside its box. This linter renders the geometry symbolically and flags:

  DANGLING_ARROW  a <line>/<path> carrying a marker-end/marker-start arrowhead
                  whose tip does not terminate near any node (rect/circle/
                  ellipse edge) or text anchor.
  TEXT_OOB        a <text> whose estimated extent falls outside the viewBox.

Design goals:
  - Precision over recall. We do NOT want to flag clean diagrams (that would
    cause needless migration). Decorative <line>s without a marker are ignored.
    SVGs that use <g transform=...> on positioned content are reported as
    "needs-visual" rather than guessed at, because absolute-coordinate math is
    unreliable under transforms.
  - Stdlib only (re, math, json, pathlib). These SVGs are machine-generated,
    so regex extraction is reliable enough.

Also classifies each diagram as flowchart-like (arrows + boxes => a good
Mermaid migration candidate) vs illustrative (curves/geometry/images => keep
hand-authored).

Run:
  py -3 scripts/mermaid/svg_lint.py                 # rank + summary
  py -3 scripts/mermaid/svg_lint.py --json out.jsonl
  py -3 scripts/mermaid/svg_lint.py --file <path.html>   # detail one file
"""
from __future__ import annotations
import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent.parent
SKIP_DIRS = {"_archive", "node_modules", ".git", "pagefind", "KDP", "build",
             "vendor", ".claude", "__pycache__", ".book-update", "scripts"}

SVG_BLOCK = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL | re.IGNORECASE)
TAG = re.compile(r"<([a-zA-Z][\w:-]*)\b([^>]*?)/?>", re.DOTALL)
ATTR = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')
NUM = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?")
TEXT_EL = re.compile(r"<text\b([^>]*)>(.*?)</text>", re.DOTALL | re.IGNORECASE)
TAGS_INNER = re.compile(r"<[^>]+>")
ENTITY = re.compile(r"&#?\w+;")


def attrs(s: str) -> dict:
    return {k.lower(): v for k, v in ATTR.findall(s)}


def fnum(d: dict, key: str, default=0.0) -> float:
    try:
        return float(d.get(key, default))
    except (TypeError, ValueError):
        return default


def parse_viewbox(svg_open_attrs: dict):
    vb = svg_open_attrs.get("viewbox") or svg_open_attrs.get("viewBox")
    if vb:
        nums = NUM.findall(vb)
        if len(nums) == 4:
            x, y, w, h = (float(n) for n in nums)
            return x, y, w, h
    w = fnum(svg_open_attrs, "width", 0)
    h = fnum(svg_open_attrs, "height", 0)
    if w and h:
        return 0.0, 0.0, w, h
    return None


def path_endpoints(d: str):
    """Return (start_xy, end_xy) for an SVG path data string.

    Walks the path with a pen cursor; handles M/L/H/V/C/S/Q/T/A/Z (abs+rel).
    Endpoint extraction is robust to curves; arcs are approximated by taking
    the trailing coordinate pair of their argument group.
    """
    toks = re.findall(r"[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?", d)
    i = 0
    cur = [0.0, 0.0]
    start = None
    sub_start = [0.0, 0.0]
    cmd = None
    ARGC = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}

    def take(n):
        nonlocal i
        vals = []
        for _ in range(n):
            if i >= len(toks):
                return None
            vals.append(float(toks[i]))
            i += 1
        return vals

    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in "Zz":
                cur = list(sub_start)
                continue
        if cmd is None:
            break
        up = cmd.upper()
        rel = cmd.islower()
        n = ARGC.get(up, 0)
        if n == 0:
            i += 1
            continue
        args = take(n)
        if args is None:
            break
        if up == "H":
            cur[0] = (cur[0] + args[0]) if rel else args[0]
        elif up == "V":
            cur[1] = (cur[1] + args[0]) if rel else args[0]
        else:
            ex, ey = args[-2], args[-1]
            if rel:
                cur[0] += ex
                cur[1] += ey
            else:
                cur[0], cur[1] = ex, ey
        if up == "M":
            sub_start = list(cur)
        if start is None:
            start = list(cur)
        # implicit repeat: subsequent coords reuse cmd (M->L)
        if up == "M":
            cmd = "l" if rel else "L"
    if start is None:
        start = list(cur)
    return tuple(start), tuple(cur)


def dist_point_rect(px, py, rx, ry, rw, rh):
    dx = max(rx - px, 0, px - (rx + rw))
    dy = max(ry - py, 0, py - (ry + rh))
    return math.hypot(dx, dy)


def dist_point_circle(px, py, cx, cy, r):
    return max(0.0, math.hypot(px - cx, py - cy) - r)


def clean_text(inner: str) -> str:
    inner = TAGS_INNER.sub("", inner)
    inner = ENTITY.sub("x", inner)  # entity counts as ~1 glyph
    return inner.strip()


class Diagram:
    def __init__(self, raw: str):
        self.raw = raw
        m = re.match(r"<svg\b([^>]*)>", raw, re.IGNORECASE)
        self.svg_attrs = attrs(m.group(1)) if m else {}
        self.viewbox = parse_viewbox(self.svg_attrs)
        self.boxes = []      # (x,y,w,h)
        self.circles = []    # (cx,cy,r)
        self.text_anchors = []  # (x,y,est_w,fs,anchor)
        self.arrows = []     # (kind, pts_to_check[list of (x,y)])
        self.n_lines = 0
        self.n_paths = 0
        self.n_curves = 0
        self.has_transform = False
        self.has_image = False
        self._parse()

    def _parse(self):
        # transforms on positioned groups make absolute coords unreliable
        if re.search(r'<g\b[^>]*\btransform\s*=\s*"[^"]*(translate|matrix|rotate|scale)', self.raw, re.I):
            self.has_transform = True
        if re.search(r"<image\b", self.raw, re.I):
            self.has_image = True
        for mm in TAG.finditer(self.raw):
            tag = mm.group(1).lower()
            a = attrs(mm.group(2))
            if tag == "rect":
                w, h = fnum(a, "width"), fnum(a, "height")
                # ignore full-canvas background rects as attachment targets
                self.boxes.append((fnum(a, "x"), fnum(a, "y"), w, h))
            elif tag == "circle":
                self.circles.append((fnum(a, "cx"), fnum(a, "cy"), fnum(a, "r")))
            elif tag == "ellipse":
                self.circles.append((fnum(a, "cx"), fnum(a, "cy"),
                                     max(fnum(a, "rx"), fnum(a, "ry"))))
            elif tag == "line":
                self.n_lines += 1
                if ("marker-end" in a) or ("marker-start" in a):
                    self.arrows.append({
                        "kind": "line",
                        "ps": (fnum(a, "x1"), fnum(a, "y1")),
                        "pe": (fnum(a, "x2"), fnum(a, "y2")),
                        "ms": "marker-start" in a, "me": "marker-end" in a})
            elif tag == "path":
                self.n_paths += 1
                d = a.get("d", "")
                if re.search(r"[CcSsQqTtAa]", d):
                    self.n_curves += 1
                if (("marker-end" in a) or ("marker-start" in a)) and d:
                    s, e = path_endpoints(d)
                    self.arrows.append({
                        "kind": "path", "ps": s, "pe": e,
                        "ms": "marker-start" in a, "me": "marker-end" in a})
            elif tag == "polyline" or tag == "polygon":
                nums = NUM.findall(a.get("points", ""))
                if "marker-end" in a or "marker-start" in a:
                    if len(nums) >= 4:
                        self.arrows.append({
                            "kind": tag,
                            "ps": (float(nums[0]), float(nums[1])),
                            "pe": (float(nums[-2]), float(nums[-1])),
                            "ms": "marker-start" in a, "me": "marker-end" in a})
                elif tag == "polygon" and len(nums) >= 6:
                    # a node shape (e.g. decision diamond); use its bbox as a target
                    xs = [float(n) for n in nums[0::2]]
                    ys = [float(n) for n in nums[1::2]]
                    self.boxes.append((min(xs), min(ys),
                                       max(xs) - min(xs), max(ys) - min(ys)))
        # text anchors
        for tm in TEXT_EL.finditer(self.raw):
            a = attrs(tm.group(1))
            txt = clean_text(tm.group(2))
            if not txt:
                continue
            fs = fnum(a, "font-size", 12) or 12
            est_w = len(txt) * fs * 0.55
            has_tf = "transform" in a  # rotated/translated text: coords unreliable
            self.text_anchors.append((fnum(a, "x"), fnum(a, "y"), est_w, fs,
                                      a.get("text-anchor", "start"), txt, has_tf))

    def _targets(self):
        """Attachment targets: node boxes/circles + text label boxes.

        Excludes a full-canvas background rect (covers the whole viewBox)."""
        boxes = []
        vb = self.viewbox
        for (x, y, w, h) in self.boxes:
            if vb and w >= vb[2] * 0.9 and h >= vb[3] * 0.9:
                continue  # background panel, not a node
            if w <= 0 or h <= 0:
                continue
            boxes.append((x, y, w, h))
        return boxes

    def _dist_to_targets(self, px, py, boxes):
        best = float("inf")
        for (x, y, w, h) in boxes:
            best = min(best, dist_point_rect(px, py, x, y, w, h))
            if best <= 1e-6:
                return best
        for (cx, cy, r) in self.circles:
            best = min(best, dist_point_circle(px, py, cx, cy, r))
        for (tx, ty, tw, fs, anchor, _t, _tf) in self.text_anchors:
            if anchor == "middle":
                bx = tx - tw / 2
            elif anchor == "end":
                bx = tx - tw
            else:
                bx = tx
            best = min(best, dist_point_rect(px, py, bx, ty - fs, tw, fs * 1.4))
        return best

    def dangling_arrows(self):
        """High-confidence broken connectors only.

        Returns dict with two buckets:
          broken: arrowhead end NOT anchored while the tail IS anchored on a
                  node (the real "arrow leaves a box but misses its target"
                  bug).
          floating: neither end anchored (usually a deliberate decorative /
                    gutter / annotation arrow; reported separately, low value).
        Returns None when coordinates cannot be trusted (group transforms).
        """
        if self.has_transform:
            return None
        vb = self.viewbox
        if not vb:
            return None
        diag = math.hypot(vb[2], vb[3])
        thresh = max(16.0, 0.022 * diag)
        boxes = self._targets()
        broken, floating = [], []
        for ar in self.arrows:
            # check each arrowhead end; its tail is the opposite endpoint
            ends = []
            if ar["me"]:
                ends.append((ar["pe"], ar["ps"]))
            if ar["ms"]:
                ends.append((ar["ps"], ar["pe"]))
            for (head, tail) in ends:
                hd = self._dist_to_targets(head[0], head[1], boxes)
                if hd <= thresh:
                    continue
                td = self._dist_to_targets(tail[0], tail[1], boxes)
                rec = {"x": round(head[0], 1), "y": round(head[1], 1),
                       "kind": ar["kind"], "gap": round(hd, 1),
                       "tail_gap": round(td, 1)}
                if td <= thresh:
                    broken.append(rec)   # tail on a node, head floating = bug
                else:
                    floating.append(rec)  # both ends free = decorative
        return {"broken": broken, "floating": floating}

    def text_oob(self):
        vb = self.viewbox
        if not vb:
            return []
        if self.has_transform:
            return []  # group translate(): absolute text coords unreliable
        x0, y0, w, h = vb
        x1, y1 = x0 + w, y0 + h
        m = 2.0
        out = []
        for (tx, ty, tw, fs, anchor, txt, has_tf) in self.text_anchors:
            if has_tf:
                continue  # rotated/translated text: x/y not the rendered box
            if anchor == "middle":
                left, right = tx - tw / 2, tx + tw / 2
            elif anchor == "end":
                left, right = tx - tw, tx
            else:
                left, right = tx, tx + tw
            over = 0.0
            if right > x1 + m:
                over = max(over, right - x1)
            if left < x0 - m:
                over = max(over, x0 - left)
            if ty > y1 + m:
                over = max(over, ty - y1)
            if ty - fs < y0 - m:
                over = max(over, y0 - (ty - fs))
            if over > max(4.0, 0.02 * w):
                out.append({"text": txt[:32], "over": round(over, 1)})
        return out

    def is_flowchartish(self):
        node_boxes = len(self._targets())
        return (len(self.arrows) >= 2 and node_boxes >= 2
                and not self.has_image and self.n_curves <= max(2, len(self.arrows)))


def iter_html():
    for p in ROOT.rglob("*.html"):
        if any(s in p.parts for s in SKIP_DIRS):
            continue
        yield p


def analyze_file(path: Path):
    html = path.read_text(encoding="utf-8", errors="ignore")
    results = []
    for idx, m in enumerate(SVG_BLOCK.finditer(html)):
        dg = Diagram(m.group(0))
        if not dg.viewbox:
            continue
        if dg.viewbox[2] < 200:  # skip small inline icons
            continue
        dang = dg.dangling_arrows()
        oob = dg.text_oob()
        broken = dang["broken"] if dang else []
        floating = dang["floating"] if dang else []
        rec = {
            "file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "svg_index": idx,
            "viewbox": dg.viewbox,
            "n_arrows": len(dg.arrows),
            "n_boxes": len(dg._targets()),
            "flowchartish": dg.is_flowchartish(),
            "has_transform": dg.has_transform,
            "has_image": dg.has_image,
            "needs_visual": dang is None,
            "n_broken": len(broken),
            "broken": broken[:6],
            "n_floating": len(floating),
            "n_text_oob": len(oob),
            "text_oob": oob[:6],
        }
        # broken connectors are the real bug; text-oob and decorative floaters
        # are weighted far lower.
        rec["score"] = rec["n_broken"] * 5 + rec["n_text_oob"]
        results.append(rec)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=str, default=None)
    ap.add_argument("--file", type=str, default=None)
    ap.add_argument("--min-score", type=int, default=1)
    args = ap.parse_args()

    if args.file:
        recs = analyze_file(Path(args.file).resolve())
        print(json.dumps(recs, indent=2))
        return

    all_recs = []
    n_svg = 0
    n_files = 0
    for p in iter_html():
        recs = analyze_file(p)
        if recs:
            n_files += 1
            n_svg += len(recs)
            all_recs.extend(recs)

    broken_recs = [r for r in all_recs if r["n_broken"] > 0]
    flagged = [r for r in all_recs if r["score"] >= args.min_score]
    needs_visual = [r for r in all_recs if r["needs_visual"]]
    flowcharts = [r for r in all_recs if r["flowchartish"]]
    floaters = [r for r in all_recs if r["n_floating"] > 0]

    flagged.sort(key=lambda r: (-r["score"], r["file"]))

    if args.json:
        out = Path(args.json)
        out.write_text("\n".join(json.dumps(r) for r in all_recs), encoding="utf-8")
        print(f"wrote {len(all_recs)} records -> {out}")

    print("=" * 70)
    print(f"Inline SVG diagrams analyzed   : {n_svg} (in {n_files} files)")
    print(f"Flowchart-like (Mermaid-able)  : {len(flowcharts)}")
    print(f"Needs visual (transform/skip)  : {len(needs_visual)}")
    print(f"BROKEN connectors (real bug)   : {len(broken_recs)}  <-- migration/fix targets")
    print(f"Decorative floating arrows     : {len(floaters)} (deliberate; ignored)")
    print(f"Text out-of-bounds (lower conf): {sum(1 for r in all_recs if r['n_text_oob'])}")
    print("=" * 70)
    print("\n### BROKEN CONNECTORS (tail on node, arrowhead misses target):")
    for r in sorted(broken_recs, key=lambda r: -r["n_broken"]):
        tag = "FLOW" if r["flowchartish"] else "illus"
        print(f"  [{r['n_broken']}] {tag:5} arrows={r['n_arrows']} {r['file']}#svg{r['svg_index']}")
        for d in r["broken"][:4]:
            print(f"        head@({d['x']},{d['y']}) gap={d['gap']} tail_gap={d['tail_gap']}")
    print("\n### TEXT OUT-OF-BOUNDS (top 25; verify against rendered font):")
    for r in sorted([x for x in all_recs if x["n_text_oob"]],
                    key=lambda r: -r["n_text_oob"])[:25]:
        tag = "FLOW" if r["flowchartish"] else "illus"
        print(f"  [{r['n_text_oob']}] {tag:5} {r['file']}#svg{r['svg_index']}")
        for t in r["text_oob"][:2]:
            print(f"        '{t['text']}' over={t['over']}")


if __name__ == "__main__":
    main()
