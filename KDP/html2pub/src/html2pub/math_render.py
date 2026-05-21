"""KaTeX server-side math renderer (Node bridge).

Extracts $$...$$, \\(...\\), \\[...\\], and <span class="math">$...$</span>
from a soup, sends to a Node katex script, replaces with rendered HTML.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

from html2pub.config import MathSpec

RENDER_SCRIPT = Path(__file__).parent / "render_math.js"

# Math-PNG sizing. PNGs are rendered at this device-pixel scale (must match
# scripts/build_math_png_cache.py SCALE) for crispness; the build divides by it
# to set logical width/height. MAX_W caps display equations to a typical Kindle
# content width (CSS px) so they don't overflow the right edge.
MATH_PNG_SCALE = 3
MATH_PNG_MAX_W = 560

# TeX-source rewrites applied BEFORE KaTeX rendering. Three purposes:
#   1. Schema-valid MathML output (avoids epubcheck RSC-005 errors where
#      KaTeX emits an `<mo>` inside `<msub>` for `\text{...}` subscripts).
#   2. \mathrm renders identically to \text for alphanumeric-only content
#      (the visual difference only matters when \text contains spaces or
#      punctuation, which we leave untouched).
#   3. Multi-line display math written as `$$ a \\ b \\ c $$` is rendered by
#      KaTeX as ONE wide line that overflows narrow Kindle pages with a
#      horizontal scrollbar. Wrapping in `\begin{aligned}` produces real
#      stacked lines that wrap naturally.
import re as _re
# Match \text{XXX} where XXX is letters/digits/underscore only — safe to
# rewrite to \mathrm. Skip cases with spaces, accented chars, or escapes.
_TEXT_TO_MATHRM = _re.compile(r"\\text\{([A-Za-z0-9_]+)\}")
# Detect `\\` line-break in TeX source (NOT inside an existing aligned/array
# environment, which we leave alone). Heuristic: if the TeX contains `\\`
# AND does NOT already contain `\begin{aligned`/`\begin{align`/`\begin{gathered`/`\begin{cases`/`\begin{matrix`/`\begin{array`,
# wrap the whole thing.
_BACKSLASH_BREAK = _re.compile(r"\\\\")
_HAS_ENV = _re.compile(r"\\begin\{(?:aligned|align\*?|gathered|cases|matrix|array|bmatrix|pmatrix|vmatrix|smallmatrix|split|multline)\}")
# `=` becomes `&=` inside aligned for proper column alignment, when each
# line has at most one top-level `=`. We do this conservatively: only insert
# `&` at the FIRST `=` per line.
_EQ_PER_LINE = _re.compile(r"^([^=&\n]*)=", _re.MULTILINE)


def _wrap_aligned(tex: str) -> str:
    if not _BACKSLASH_BREAK.search(tex):
        return tex
    if _HAS_ENV.search(tex):
        return tex
    # Insert `&` before first `=` on each line for column alignment
    aligned_body = _EQ_PER_LINE.sub(r"\1&=", tex)
    return r"\begin{aligned}" + aligned_body + r"\end{aligned}"


def _rewrite_tex(tex: str, display: bool = False) -> str:
    tex = _TEXT_TO_MATHRM.sub(r"\\mathrm{\1}", tex)
    if display:
        tex = _wrap_aligned(tex)
    return tex


def render(soup: BeautifulSoup, math_cfg: MathSpec) -> int:
    """Render math in-place; returns count rendered."""
    if math_cfg.render != "katex":
        return 0
    if not RENDER_SCRIPT.exists():
        return 0
    katex_modules = Path(math_cfg.katex_path) if math_cfg.katex_path else None
    if katex_modules is None or not katex_modules.exists():
        return 0

    items: list[dict] = []
    targets: list[tuple] = []

    # 1. <span class="math"> / <div class="math-block">
    for el in soup.find_all(attrs={"class": True}):
        cls = el.get("class") or []
        if "math" in cls and el.name in ("span", "div"):
            tex_raw = el.get_text()
            tex = _strip_delim(tex_raw)
            if not tex:
                continue
            display = ("math-block" in cls) or tex_raw.strip().startswith("$$")
            items.append({"id": str(len(items)), "tex": _rewrite_tex(tex, display=display), "display": display})
            targets.append(("element", el))

    # 2. text nodes with $$...$$ or \(...\) or \[...\]
    for text_node in list(soup.find_all(string=True)):
        parent = text_node.parent
        if parent is None:
            continue
        skip = False
        for anc in parent.parents:
            if anc.name in ("code", "pre", "script", "style"):
                skip = True
                break
            cls = anc.get("class") if anc.name else None
            if cls and "math" in cls:
                skip = True
                break
        if skip:
            continue
        s = str(text_node)
        if "$$" not in s and "\\(" not in s and "\\[" not in s:
            continue
        new_parts = _split_text(s, items)
        if new_parts is None:
            continue
        new_nodes = []
        for kind, content in new_parts:
            if kind == "text":
                new_nodes.append(NavigableString(content))
            else:
                placeholder = soup.new_tag("span", attrs={
                    "class": ["_math_placeholder"],
                    "data-math-id": content,
                })
                placeholder.string = ""
                new_nodes.append(placeholder)
                targets.append(("placeholder", placeholder))
        for n in reversed(new_nodes):
            text_node.insert_after(n)
        text_node.extract()

    if not items:
        return 0

    try:
        env = os.environ.copy()
        env["NODE_PATH"] = str(katex_modules)
        proc = subprocess.run(
            [math_cfg.node_exe, str(RENDER_SCRIPT)],
            input=json.dumps(items),
            capture_output=True, text=True, env=env,
            timeout=60, encoding="utf-8",
        )
        if proc.returncode != 0:
            return 0
        rendered = json.loads(proc.stdout)
    except Exception:
        return 0

    by_id = {r["id"]: r["html"] for r in rendered}
    items_by_id = {it["id"]: it for it in items}
    n = 0
    for i, (kind, el) in enumerate(targets):
        mid = str(i) if kind == "element" else el.get("data-math-id", "")
        html = by_id.get(mid)
        if html is None:
            continue
        new_soup = BeautifulSoup(html, "lxml")
        wrap = new_soup.find(["span", "div"], class_="katex")
        if wrap is None:
            if kind == "placeholder":
                continue
            wrap = new_soup
        new_el = soup.new_tag("span")
        for child in list(wrap.children if hasattr(wrap, "children") else []):
            new_el.append(child.extract() if hasattr(child, "extract") else child)
        # CRITICAL: include the original `katex` class. KaTeX's own CSS
        # (katex.min.css) targets `.katex .vlist-t`, `.katex .strut`,
        # `.katex .msupsub` etc. Without it, sub/superscripts collapse to
        # the baseline and \mathcal/\mathfrak font selection silently fails.
        cls = ["katex", "katex-rendered"]
        is_display = kind == "element" and "math-block" in (el.get("class") or [])
        if is_display:
            cls.append("katex-display")
        new_el["class"] = cls
        # Stamp the source TeX + display flag so a later build step can swap
        # MathML for a pre-rendered PNG (Kindle's MathML support is gated on
        # Enhanced Typesetting and unreliable across apps). data-tex carries
        # the exact rewritten TeX used as the math-png cache key + img alt.
        item = items_by_id.get(mid)
        if item is not None:
            new_el["data-tex"] = item["tex"]
            new_el["data-mathdisplay"] = "1" if item.get("display") else "0"
        el.replace_with(new_el)
        n += 1
    return n


def math_key(tex: str, display: bool) -> str:
    """Stable cache key for a (rewritten-tex, display) pair."""
    import hashlib
    h = hashlib.sha1((tex + "|" + ("1" if display else "0")).encode("utf-8"))
    return h.hexdigest()[:16]


_ALT_WORDS = {
    "sum": "sum", "prod": "product", "int": "integral", "frac": "",
    "sqrt": "sqrt", "cdot": "*", "times": "x", "div": "/", "pm": "+/-",
    "leq": "lte", "geq": "gte", "neq": "!=", "approx": "~", "to": "to",
    "rightarrow": "to", "leftarrow": "from", "gets": "from", "mapsto": "to",
    "infty": "infinity",
    "partial": "d", "nabla": "grad", "alpha": "alpha", "beta": "beta",
    "gamma": "gamma", "delta": "delta", "epsilon": "epsilon", "theta": "theta",
    "lambda": "lambda", "mu": "mu", "sigma": "sigma", "pi": "pi", "phi": "phi",
    "omega": "omega", "in": "in", "log": "log", "exp": "exp", "min": "min",
    "max": "max", "hat": "", "bar": "", "tilde": "", "vec": "", "mathbb": "",
    "mathcal": "", "mathrm": "", "mathbf": "", "text": "", "left": "",
    "right": "", "bigl": "", "bigr": "", "Bigl": "", "Bigr": "", "mid": "|",
}


def _tex_to_alt(tex: str) -> str:
    """Short, human-ish alt text from TeX (<=140 chars per KDP guidance)."""
    import re as _r
    t = tex.replace("\\\\", " ; ")
    t = _r.sub(r"\\(begin|end)\{[a-zA-Z*]+\}", " ", t)
    # \frac{a}{b} -> a/b  (one level; nested fracs degrade gracefully)
    for _ in range(3):
        t = _r.sub(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)", t)
    # map known commands to words/symbols, drop the rest's backslash
    t = _r.sub(r"\\([a-zA-Z]+)", lambda m: _ALT_WORDS.get(m.group(1), m.group(1)), t)
    t = t.replace("{", "").replace("}", "").replace("\\", "")
    # Hard-strip characters that bs4 entity-encodes inside an attribute value
    # (&lt; &gt; &amp; &quot;). Kindle's Enhanced-Mobi parser FAILS (E21018) on
    # entity-encoded chars in attributes, so the alt must contain none.
    t = (t.replace("&", " and ").replace('"', " ")
          .replace("<", " lt ").replace(">", " gt "))
    t = _r.sub(r"\s+", " ", t).strip()
    if len(t) > 138:
        t = t[:135] + "..."
    return t or "equation"


def replace_mathml_with_png(soup: BeautifulSoup, images, cache_dir, manifest: dict) -> int:
    """Swap every remaining MathML wrapper (span/div.katex with data-tex) for a
    pre-rendered PNG <img>. Records every (key -> tex/display) into `manifest`
    so the cache builder knows what to render. If the cache PNG already exists,
    its bytes are bundled directly into `images` (kept as PNG, no JPEG
    re-encode) and the wrapper is replaced; otherwise the MathML is left in
    place (graceful fallback until the cache is built).

    Runs AFTER the project's simplify_inline_mathml hook, so simple inline math
    is already <sub>/<sup> and only complex/display equations remain.
    """
    from pathlib import Path as _P
    cache_dir = _P(cache_dir)
    n = 0
    for el in soup.find_all(["span", "div"], attrs={"data-tex": True}):
        cls = el.get("class") or []
        if "katex" not in cls:
            continue
        tex = el.get("data-tex") or ""
        if not tex:
            continue
        display = el.get("data-mathdisplay") == "1"
        key = math_key(tex, display)
        manifest[key] = {"tex": tex, "display": display}
        png = cache_dir / f"{key}.png"
        if not png.exists():
            continue  # cache not built yet -> keep MathML fallback
        bundled = f"img/math_{key}.png"
        if bundled not in images.bundled_bytes:
            images.bundled_bytes[bundled] = png.read_bytes()
            images.bundled_mime[bundled] = "image/png"
            images.path_to_bundle[f"__math__{key}"] = bundled
        img = soup.new_tag("img")
        img["src"] = "../" + bundled
        img["alt"] = _tex_to_alt(tex)
        img["class"] = ["math-png-display"] if display else ["math-png-inline"]
        # Size: PNGs are rendered at MATH_PNG_SCALE x device pixels for
        # crispness. Set explicit logical width/height (px / scale) so the
        # equation displays at text-matching size (Kindle honors the width/
        # height HTML attributes but ignores CSS max-width/height on <img>).
        # Cap display equations to a typical Kindle content width to avoid
        # right-edge overflow (no CSS max-width to rely on).
        try:
            from PIL import Image as _Img
            with _Img.open(png) as _im:
                pw, ph = _im.size
            lw, lh = pw / MATH_PNG_SCALE, ph / MATH_PNG_SCALE
            if display and lw > MATH_PNG_MAX_W:
                lh = lh * (MATH_PNG_MAX_W / lw)
                lw = MATH_PNG_MAX_W
            img["width"] = str(max(1, round(lw)))
            img["height"] = str(max(1, round(lh)))
        except Exception:
            pass
        el.replace_with(img)
        n += 1
    return n


def _strip_delim(s: str) -> str:
    s = s.strip()
    if s.startswith("$$") and s.endswith("$$") and len(s) > 4:
        return s[2:-2].strip()
    if s.startswith("$") and s.endswith("$") and len(s) > 2:
        return s[1:-1].strip()
    if s.startswith("\\(") and s.endswith("\\)"):
        return s[2:-2].strip()
    if s.startswith("\\[") and s.endswith("\\]"):
        return s[2:-2].strip()
    return s


def _split_text(s: str, items: list):
    parts = []
    pos = 0
    found = False
    while pos < len(s):
        markers = [
            (s.find("$$", pos), "$$", "$$", True),
            (s.find("\\(", pos), "\\(", "\\)", False),
            (s.find("\\[", pos), "\\[", "\\]", True),
        ]
        markers = [m for m in markers if m[0] >= 0]
        if not markers:
            break
        markers.sort(key=lambda m: m[0])
        start, open_d, close_d, display = markers[0]
        close_pos = s.find(close_d, start + len(open_d))
        if close_pos < 0:
            break
        tex = s[start + len(open_d):close_pos].strip()
        if not tex:
            pos = close_pos + len(close_d)
            continue
        if start > pos:
            parts.append(("text", s[pos:start]))
        mid = str(len(items))
        items.append({"id": mid, "tex": _rewrite_tex(tex, display=display), "display": display})
        parts.append(("math", mid))
        pos = close_pos + len(close_d)
        found = True
    if not found:
        return None
    if pos < len(s):
        parts.append(("text", s[pos:]))
    return parts
