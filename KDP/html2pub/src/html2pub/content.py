"""Per-chapter HTML cleanup and transformations."""
from __future__ import annotations

import re
from typing import Iterable

from bs4 import BeautifulSoup, NavigableString

from html2pub.config import TransformsSpec

SVG_NS = "http://www.w3.org/2000/svg"
UNWANTED_TAGS = ["script", "noscript"]
INVALID_URL_CHARS_RE = re.compile(r"[{}^\\\[\]`]")
BLOCK_TAGS_IN_CODE = frozenset({
    "pre", "div", "p", "ul", "ol", "table",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "section", "article", "blockquote", "figure",
})

ALLOWED_TAGS = frozenset({
    "html", "head", "body", "title", "meta", "link", "style", "base",
    "article", "aside", "footer", "header", "h1", "h2", "h3", "h4", "h5", "h6",
    "hgroup", "main", "nav", "section", "address",
    "blockquote", "dd", "div", "dl", "dt", "figcaption", "figure", "hr",
    "li", "menu", "ol", "p", "pre", "ul",
    "a", "abbr", "b", "bdi", "bdo", "br", "cite", "code", "data", "dfn",
    "em", "i", "kbd", "mark", "q", "rp", "rt", "ruby", "s", "samp",
    "small", "span", "strong", "sub", "sup", "time", "u", "var", "wbr",
    "del", "ins",
    "area", "audio", "img", "map", "track", "video", "embed", "iframe",
    "object", "picture", "source",
    "caption", "col", "colgroup", "table", "tbody", "td", "tfoot",
    "th", "thead", "tr",
    "button", "datalist", "fieldset", "form", "input", "label", "legend",
    "meter", "optgroup", "option", "output", "progress", "select", "textarea",
    "details", "dialog", "summary",
    "slot", "template",
    "canvas",
    # SVG
    "svg", "g", "defs", "symbol", "use", "image",
    "rect", "circle", "ellipse", "line", "polyline", "polygon", "path",
    "text", "tspan", "textpath",
    "marker", "pattern", "clippath", "mask", "filter",
    "lineargradient", "radialgradient", "stop",
    "desc", "metadata", "foreignobject", "switch", "set",
    # MathML
    "math", "mi", "mn", "mo", "ms", "mspace", "mtext",
    "mfrac", "mroot", "msqrt", "msub", "msup", "msubsup",
    "munder", "mover", "munderover", "mrow", "mfenced",
    "merror", "mphantom", "mpadded", "mstyle", "mtable", "mtr", "mtd",
    "menclose", "annotation", "annotation-xml", "semantics",
})


def clean_html(soup: BeautifulSoup, transforms: TransformsSpec) -> None:
    """Apply all per-chapter cleanup in place."""
    for tag in soup(UNWANTED_TAGS):
        tag.decompose()

    for style in soup.find_all("style"):
        if len(style.get_text() or "") > transforms.drop_inline_style_over:
            style.decompose()

    # Drop SVG inside <a> (decorative)
    for a in soup.find_all("a"):
        for svg in a.find_all("svg"):
            svg.decompose()

    # Drop user-selected selectors entirely (chrome / nav buttons / etc.)
    for sel in transforms.drop_selectors:
        for el in soup.select(sel):
            el.decompose()

    # Unwrap unknown / non-XHTML tags
    for el in soup.find_all(True):
        if el.name and el.name not in ALLOWED_TAGS:
            el.unwrap()

    for svg in soup.find_all("svg"):
        if "xmlns" not in svg.attrs:
            svg["xmlns"] = SVG_NS

    sanitize_invalid_url_chars(soup)
    dedupe_element_ids(soup)
    drop_orphan_fragment_refs(soup)
    normalize_code_block_content(soup)
    syntax_highlight(soup)
    set_explicit_avatar_dimensions(soup, transforms.avatar_sizes)
    if transforms.slim_index_lists:
        slim_index_lists(soup)
    wrap_wide_tables(soup, transforms.wide_table_min_cols)


def sanitize_invalid_url_chars(soup: BeautifulSoup) -> None:
    for el in soup.find_all(attrs={"id": True}):
        if INVALID_URL_CHARS_RE.search(el["id"]):
            el["id"] = INVALID_URL_CHARS_RE.sub("_", el["id"])
    for a in soup.find_all(href=True):
        href = a["href"]
        if "#" in href:
            path, frag = href.split("#", 1)
            if INVALID_URL_CHARS_RE.search(frag):
                clean = INVALID_URL_CHARS_RE.sub("_", frag)
                a["href"] = f"{path}#{clean}" if path else f"#{clean}"
    for el in soup.find_all(True):
        for k in list(el.attrs):
            v = el.attrs[k]
            if isinstance(v, str) and "url(#" in v and INVALID_URL_CHARS_RE.search(v):
                el.attrs[k] = re.sub(
                    r"url\(#([^)]+)\)",
                    lambda m: f"url(#{INVALID_URL_CHARS_RE.sub('_', m.group(1))})",
                    v,
                )


def dedupe_element_ids(soup: BeautifulSoup) -> None:
    seen: dict[str, int] = {}
    for el in soup.find_all(attrs={"id": True}):
        old = el["id"]
        if not old:
            continue
        if old not in seen:
            seen[old] = 1
            continue
        n = seen[old]
        while True:
            new = f"{old}_d{n}"
            if new not in seen:
                break
            n += 1
        seen[old] = n + 1
        seen[new] = 1
        scope = el
        while scope.parent is not None and scope.name != "svg":
            scope = scope.parent
        if scope.name != "svg":
            scope = soup
        el["id"] = new
        for ref in scope.find_all(True):
            for k in list(ref.attrs):
                v = ref.attrs[k]
                if not isinstance(v, str):
                    continue
                if f"url(#{old})" in v:
                    ref.attrs[k] = v.replace(f"url(#{old})", f"url(#{new})")
                elif v == f"#{old}":
                    ref.attrs[k] = f"#{new}"


def drop_orphan_fragment_refs(soup: BeautifulSoup) -> None:
    all_ids = {el["id"] for el in soup.find_all(attrs={"id": True}) if el.get("id")}
    for el in soup.find_all(True):
        for k in list(el.attrs):
            v = el.attrs[k]
            if not isinstance(v, str):
                continue
            m = re.search(r"url\(#([^)]+)\)", v)
            if m and m.group(1) not in all_ids:
                el.attrs[k] = re.sub(r"url\(#[^)]+\)", "none", v)
                continue
            if k in ("href", "{http://www.w3.org/1999/xlink}href") and v.startswith("#"):
                if v[1:] not in all_ids:
                    if el.name == "a":
                        el.unwrap()
                    else:
                        del el.attrs[k]


def normalize_code_block_content(soup: BeautifulSoup) -> None:
    for el in soup.find_all(["code", "pre"]):
        nested = el.find_all(BLOCK_TAGS_IN_CODE)
        if not nested:
            continue
        text = el.get_text()
        el.clear()
        el.append(NavigableString(text))


_LANG_ALIASES = {
    "language-python": "python", "language-py": "python",
    "language-bash": "bash", "language-sh": "bash", "language-shell": "bash",
    "language-js": "javascript", "language-javascript": "javascript",
    "language-ts": "typescript", "language-typescript": "typescript",
    "language-json": "json", "language-yaml": "yaml", "language-yml": "yaml",
    "language-toml": "toml", "language-html": "html", "language-xml": "xml",
    "language-css": "css", "language-c": "c", "language-cpp": "cpp",
    "language-rust": "rust", "language-go": "go", "language-sql": "sql",
    "language-dockerfile": "dockerfile", "language-makefile": "makefile",
    "language-text": "text", "language-plain": "text",
    "language-diff": "diff", "language-md": "markdown", "language-markdown": "markdown",
}

_PYG = None


def syntax_highlight(soup: BeautifulSoup) -> int:
    global _PYG
    if _PYG is None:
        try:
            from pygments import highlight
            from pygments.formatters import HtmlFormatter
            from pygments.lexers import get_lexer_by_name
            from pygments.util import ClassNotFound
            _PYG = (highlight, HtmlFormatter, get_lexer_by_name, ClassNotFound)
        except ImportError:
            _PYG = False
    if not _PYG:
        return 0
    highlight_fn, HtmlFormatter, get_lexer_by_name, ClassNotFound = _PYG
    formatter = HtmlFormatter(nowrap=True, classprefix="")
    n = 0
    for code in soup.find_all("code"):
        classes = code.get("class") or []
        lang = None
        for c in classes:
            if c in _LANG_ALIASES:
                lang = _LANG_ALIASES[c]
                break
            elif c.startswith("language-"):
                trial = c[len("language-"):]
                try:
                    get_lexer_by_name(trial)
                    lang = trial
                    break
                except ClassNotFound:
                    continue
        if not lang:
            continue
        if code.find("span", class_=re.compile(r"^[a-z]{1,4}$")):
            continue
        text = code.get_text()
        try:
            lexer = get_lexer_by_name(lang)
            highlighted = highlight_fn(text, lexer, formatter).rstrip("\n")
            new_soup = BeautifulSoup(f"<wrap>{highlighted}</wrap>", "lxml")
            wrap = new_soup.find("wrap")
            if wrap:
                code.clear()
                code.append(wrap)
                wrap.unwrap()
                n += 1
        except Exception:
            continue
    return n


def set_explicit_avatar_dimensions(soup: BeautifulSoup, sizes: dict[str, list[int]]) -> None:
    for cls, dims in sizes.items():
        if len(dims) < 2:
            continue
        w, h = dims[0], dims[1]
        for wrap in soup.select(f".{cls}"):
            for img in wrap.find_all("img"):
                if "width" not in img.attrs:
                    img["width"] = str(w)
                if "height" not in img.attrs:
                    img["height"] = str(h)


def slim_index_lists(soup: BeautifulSoup) -> None:
    """Strip 'Sections' lists from chapter index pages (redundant with EPUB nav)."""
    for ul in soup.find_all("ul", class_="sections-list"):
        prev = ul.find_previous_sibling()
        if prev and prev.name == "h2" and prev.get_text(strip=True).lower() == "sections":
            prev.decompose()
        ul.decompose()


def wrap_wide_tables(soup: BeautifulSoup, min_cols: int) -> None:
    if min_cols <= 0:
        return
    for table in soup.find_all("table"):
        max_cols = 0
        for row in table.find_all("tr"):
            cells = row.find_all(["td", "th"])
            max_cols = max(max_cols, len(cells))
        if max_cols < min_cols:
            continue
        existing = table.get("class") or []
        if "complex-table" not in existing:
            existing.append("complex-table")
            table["class"] = existing
        prev = table.find_previous_sibling()
        if (prev is not None and prev.name == "div"
                and "complex-table-note" in (prev.get("class") or [])):
            continue
        note = soup.new_tag("div", attrs={"class": "callout note complex-table-note"})
        title = soup.new_tag("div", attrs={"class": "callout-title"})
        title.string = f"Wide Table ({max_cols} columns)"
        note.append(title)
        body = soup.new_tag("p")
        body.string = ("On narrow screens, columns will wrap or compress. "
                       "For best layout, view on a tablet or desktop.")
        note.append(body)
        table.insert_before(note)


def populate_dropped_fragments(spine_entries: list[dict], project_root, fragment_drop: dict[str, list[str]]) -> dict[str, set[str]]:
    """Return {file_basename: {fragment_ids_to_drop}}.

    Driven by config: each key in `fragment_drop` is a source-filename basename
    (without .html), the value is a list of element IDs that the user expects
    to be removed during build (e.g. via slim transforms or external pre-pass).
    """
    out: dict[str, set[str]] = {}
    for k, ids in fragment_drop.items():
        out[k] = set(ids)
    return out
