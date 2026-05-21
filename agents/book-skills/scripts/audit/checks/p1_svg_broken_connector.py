"""Detect inline SVG flowcharts whose arrows do not connect to their target.

LLM-authored SVG diagrams are drawn with absolute pixel coordinates and no
layout engine, so an arrow's tail can sit on a node while its arrowhead floats
in empty space short of the destination node. The rest of the SVG audit suite
checks text bounds, panel overlap, and ARIA labels, but nothing verifies arrow
connectivity, which is the most visible "broken diagram" symptom.

This check flags only the high-confidence bug signature:

    an arrow (a <line>/<path>/<polyline> carrying marker-end or marker-start)
    whose arrowhead end is far from every node, while its OPPOSITE end (the
    tail) IS anchored on a node.

That one-end-anchored rule deliberately ignores decorative / gutter / legend
arrows (both ends free), which are a common and legitimate design choice in
multi-panel figures. SVGs that position content with <g transform=...> are
skipped because absolute-coordinate math is unreliable under a translate.

Node targets recognised: <rect>, <circle>, <ellipse>, <polygon> (decision
diamonds, via bounding box), and <text> anchors (an arrow may point at a bare
label). The tuned threshold gives effectively zero false positives across the
current book; if you add a genuinely new layout idiom, re-verify.
"""
import math
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "SVG_BROKEN_CONNECTOR"
DESCRIPTION = ("SVG arrow's tail is on a node but its arrowhead does not reach "
               "any target node (broken connector)")

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

SVG_BLOCK = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL | re.IGNORECASE)
TAG = re.compile(r"<([a-zA-Z][\w:-]*)\b([^>]*?)/?>", re.DOTALL)
ATTR = re.compile(r'([\w:-]+)\s*=\s*"([^"]*)"')
NUM = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?")
TEXT_EL = re.compile(r"<text\b([^>]*)>(.*?)</text>", re.DOTALL | re.IGNORECASE)
TAGS_INNER = re.compile(r"<[^>]+>")
ENTITY = re.compile(r"&#?\w+;")
GROUP_TRANSFORM = re.compile(
    r'<g\b[^>]*\btransform\s*=\s*"[^"]*(?:translate|matrix|rotate|scale)', re.I)
PATH_TOK = re.compile(
    r"[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?")


def _attrs(s):
    return {k.lower(): v for k, v in ATTR.findall(s)}


def _f(d, key, default=0.0):
    try:
        return float(d.get(key, default))
    except (TypeError, ValueError):
        return default


def _viewbox(a):
    vb = a.get("viewbox")
    if vb:
        nums = NUM.findall(vb)
        if len(nums) == 4:
            return tuple(float(n) for n in nums)
    w, h = _f(a, "width"), _f(a, "height")
    return (0.0, 0.0, w, h) if (w and h) else None


def _path_endpoints(d):
    toks = PATH_TOK.findall(d)
    i, cur, start, sub = 0, [0.0, 0.0], None, [0.0, 0.0]
    cmd = None
    argc = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}

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
                cur = list(sub)
                continue
        if cmd is None:
            break
        up, rel = cmd.upper(), cmd.islower()
        n = argc.get(up, 0)
        if n == 0:
            i += 1
            continue
        args = take(n)
        if args is None:
            break
        if up == "H":
            cur[0] = cur[0] + args[0] if rel else args[0]
        elif up == "V":
            cur[1] = cur[1] + args[0] if rel else args[0]
        else:
            ex, ey = args[-2], args[-1]
            if rel:
                cur[0] += ex
                cur[1] += ey
            else:
                cur[0], cur[1] = ex, ey
        if up == "M":
            sub = list(cur)
            cmd = "l" if rel else "L"
        if start is None:
            start = list(cur)
    return tuple(start or cur), tuple(cur)


def _d_rect(px, py, x, y, w, h):
    dx = max(x - px, 0, px - (x + w))
    dy = max(y - py, 0, py - (y + h))
    return math.hypot(dx, dy)


def _clean(inner):
    return ENTITY.sub("x", TAGS_INNER.sub("", inner)).strip()


def _collect(svg):
    """Return (boxes, circles, texts, arrows) in absolute coords."""
    boxes, circles, texts, arrows = [], [], [], []
    for m in TAG.finditer(svg):
        tag = m.group(1).lower()
        a = _attrs(m.group(2))
        if tag == "rect":
            boxes.append((_f(a, "x"), _f(a, "y"), _f(a, "width"), _f(a, "height")))
        elif tag == "circle":
            circles.append((_f(a, "cx"), _f(a, "cy"), _f(a, "r")))
        elif tag == "ellipse":
            circles.append((_f(a, "cx"), _f(a, "cy"), max(_f(a, "rx"), _f(a, "ry"))))
        elif tag == "line":
            if "marker-end" in a or "marker-start" in a:
                arrows.append({"ps": (_f(a, "x1"), _f(a, "y1")),
                               "pe": (_f(a, "x2"), _f(a, "y2")),
                               "ms": "marker-start" in a, "me": "marker-end" in a})
        elif tag == "path":
            d = a.get("d", "")
            if ("marker-end" in a or "marker-start" in a) and d:
                s, e = _path_endpoints(d)
                arrows.append({"ps": s, "pe": e,
                               "ms": "marker-start" in a, "me": "marker-end" in a})
        elif tag in ("polyline", "polygon"):
            nums = NUM.findall(a.get("points", ""))
            if "marker-end" in a or "marker-start" in a:
                if len(nums) >= 4:
                    arrows.append({"ps": (float(nums[0]), float(nums[1])),
                                   "pe": (float(nums[-2]), float(nums[-1])),
                                   "ms": "marker-start" in a, "me": "marker-end" in a})
            elif tag == "polygon" and len(nums) >= 6:
                xs = [float(n) for n in nums[0::2]]
                ys = [float(n) for n in nums[1::2]]
                boxes.append((min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)))
    for tm in TEXT_EL.finditer(svg):
        a = _attrs(tm.group(1))
        txt = _clean(tm.group(2))
        if not txt or "transform" in a:
            continue
        fs = _f(a, "font-size", 12) or 12
        texts.append((_f(a, "x"), _f(a, "y"), len(txt) * fs * 0.55, fs,
                      a.get("text-anchor", "start")))
    return boxes, circles, texts, arrows


def _dist_to_targets(px, py, boxes, circles, texts):
    best = float("inf")
    for (x, y, w, h) in boxes:
        best = min(best, _d_rect(px, py, x, y, w, h))
        if best <= 1e-6:
            return best
    for (cx, cy, r) in circles:
        best = min(best, max(0.0, math.hypot(px - cx, py - cy) - r))
    for (tx, ty, tw, fs, anchor) in texts:
        bx = tx - tw / 2 if anchor == "middle" else (tx - tw if anchor == "end" else tx)
        best = min(best, _d_rect(px, py, bx, ty - fs, tw, fs * 1.4))
    return best


def run(filepath, html, context):
    issues = []
    for m in SVG_BLOCK.finditer(html):
        svg = m.group(0)
        open_m = re.match(r"<svg\b([^>]*)>", svg, re.IGNORECASE)
        vb = _viewbox(_attrs(open_m.group(1))) if open_m else None
        if not vb or vb[2] < 200:
            continue
        if GROUP_TRANSFORM.search(svg):
            continue  # transformed coords: cannot trust absolute positions
        boxes, circles, texts, arrows = _collect(svg)
        if not arrows:
            continue
        # drop a full-canvas background rect as an attachment target
        nodes = [(x, y, w, h) for (x, y, w, h) in boxes
                 if w > 0 and h > 0 and not (w >= vb[2] * 0.9 and h >= vb[3] * 0.9)]
        thresh = max(16.0, 0.022 * math.hypot(vb[2], vb[3]))
        line_num = html.count("\n", 0, m.start()) + 1
        for ar in arrows:
            ends = []
            if ar["me"]:
                ends.append((ar["pe"], ar["ps"]))
            if ar["ms"]:
                ends.append((ar["ps"], ar["pe"]))
            for head, tail in ends:
                hd = _dist_to_targets(head[0], head[1], nodes, circles, texts)
                if hd <= thresh:
                    continue
                td = _dist_to_targets(tail[0], tail[1], nodes, circles, texts)
                if td <= thresh:
                    issues.append(Issue(
                        PRIORITY, CHECK_ID, filepath, line_num,
                        f"Arrow tail is on a node but its arrowhead at "
                        f"({head[0]:.0f},{head[1]:.0f}) is {hd:.0f}px from any "
                        f"node (threshold {thresh:.0f}px); connector looks broken."))
    return issues
