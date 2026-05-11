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

# TeX-source rewrites applied BEFORE KaTeX rendering. Two purposes:
#   1. Schema-valid MathML output (avoids epubcheck RSC-005 errors where
#      KaTeX emits an `<mo>` inside `<msub>` for `\text{...}` subscripts).
#   2. \mathrm renders identically to \text for alphanumeric-only content
#      (the visual difference only matters when \text contains spaces or
#      punctuation, which we leave untouched).
import re as _re
# Match \text{XXX} where XXX is letters/digits/underscore only — safe to
# rewrite to \mathrm. Skip cases with spaces, accented chars, or escapes.
_TEXT_TO_MATHRM = _re.compile(r"\\text\{([A-Za-z0-9_]+)\}")


def _rewrite_tex(tex: str) -> str:
    return _TEXT_TO_MATHRM.sub(r"\\mathrm{\1}", tex)


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
            items.append({"id": str(len(items)), "tex": _rewrite_tex(tex), "display": display})
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
        if kind == "element" and "math-block" in (el.get("class") or []):
            cls.append("katex-display")
        new_el["class"] = cls
        el.replace_with(new_el)
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
        items.append({"id": mid, "tex": _rewrite_tex(tex), "display": display})
        parts.append(("math", mid))
        pos = close_pos + len(close_d)
        found = True
    if not found:
        return None
    if pos < len(s):
        parts.append(("text", s[pos:]))
    return parts
