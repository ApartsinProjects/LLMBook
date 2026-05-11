"""Project-specific html2pub hooks for the LLMBook.

Wired via html2pub.toml:

    [plugins]
    post_process_html = "_html2pub_hooks.post_process"

Adds the transforms that html2pub doesn't know about (Pygments syntax
highlighting, wisdom-council slim, code-block normalization, wide-table
wrapping, etc.) — these were in the legacy KDP/build/build_epub.py and
must run on every chapter for the EPUB to look right.
"""
from __future__ import annotations
import re
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------
# Wisdom council: keep only the top-quoted agents
# ----------------------------------------------------------------------
WISDOM_COUNCIL_KEEP = frozenset({
    "deploy", "guard", "eval", "compass",
    "sage", "frontier", "agent-x", "pip",
})


def slim_wisdom_council(soup: BeautifulSoup) -> int:
    grid = soup.find("div", class_="wc-grid")
    if grid is None:
        return 0
    cards = grid.find_all("div", class_="wc-card", recursive=False)
    if len(cards) <= len(WISDOM_COUNCIL_KEEP):
        return 0
    kept = 0
    dropped = 0
    for card in cards:
        cid = card.get("id", "")
        if cid in WISDOM_COUNCIL_KEEP:
            kept += 1
        else:
            card.decompose()
            dropped += 1
    if dropped > 0:
        intro = soup.new_tag("p", attrs={"class": "wisdom-council-epub-note"})
        intro.string = (
            f"Note: This Kindle edition includes profiles for the {kept} most-quoted "
            f"members of the Wisdom Council. The web edition includes all 42."
        )
        intro_p = soup.find("p", class_="wisdom-council-intro")
        if intro_p is not None:
            intro_p.insert_after(intro)
        else:
            grid.insert_before(intro)
    return dropped


# ----------------------------------------------------------------------
# Pygments syntax highlighting
# ----------------------------------------------------------------------
_PYGMENTS = None
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
    "language-r": "r", "language-julia": "julia",
}


def syntax_highlight(soup: BeautifulSoup) -> int:
    global _PYGMENTS
    if _PYGMENTS is None:
        try:
            from pygments import highlight
            from pygments.formatters import HtmlFormatter
            from pygments.lexers import get_lexer_by_name
            from pygments.util import ClassNotFound
            _PYGMENTS = (highlight, HtmlFormatter, get_lexer_by_name, ClassNotFound)
        except ImportError:
            _PYGMENTS = False
    if _PYGMENTS is False:
        return 0
    highlight_fn, HtmlFormatter, get_lexer_by_name, ClassNotFound = _PYGMENTS
    formatter = HtmlFormatter(nowrap=True, classprefix="")

    n = 0
    for code in soup.find_all("code"):
        classes = code.get("class") or []
        lang = None
        for c in classes:
            if c in _LANG_ALIASES:
                lang = _LANG_ALIASES[c]; break
            if c.startswith("language-"):
                trial = c[len("language-"):]
                try:
                    get_lexer_by_name(trial)
                    lang = trial; break
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
                # Add pygments-highlighted class so the CSS selectors apply
                # (CSS targets `.pygments-highlighted .c1` etc.)
                cur_classes = code.get("class") or []
                if "pygments-highlighted" not in cur_classes:
                    code["class"] = cur_classes + ["pygments-highlighted"]
                n += 1
        except Exception:
            continue
    return n


# ----------------------------------------------------------------------
# Code block normalization (collapse nested block-level inside <pre><code>)
# ----------------------------------------------------------------------
def normalize_code_block_content(soup: BeautifulSoup) -> int:
    n = 0
    for code in soup.find_all("code"):
        if code.find(["div", "p", "ul", "ol", "li", "table"]):
            text = code.get_text()
            code.clear()
            code.string = text
            n += 1
    return n


# ----------------------------------------------------------------------
# Wide table wrapping (>= 6 cols → wrap with horizontal-scroll note)
# ----------------------------------------------------------------------
def wrap_wide_tables(soup: BeautifulSoup, min_cols: int = 6) -> int:
    n = 0
    for tbl in soup.find_all("table"):
        # Count columns from first row
        first_row = tbl.find("tr")
        if not first_row:
            continue
        ncols = len(first_row.find_all(["td", "th"]))
        if ncols < min_cols:
            continue
        if tbl.parent and "table-wide-wrap" in (tbl.parent.get("class") or []):
            continue
        wrapper = soup.new_tag("div", attrs={"class": "table-wide-wrap"})
        tbl.insert_before(wrapper)
        wrapper.append(tbl.extract())
        n += 1
    return n


# ----------------------------------------------------------------------
# Slim chapter index "Sections" list (redundant with nav)
# ----------------------------------------------------------------------
def slim_chapter_index_sections_list(soup: BeautifulSoup, src_rel: str) -> int:
    if not src_rel.endswith("/index.html"):
        return 0
    n = 0
    for h in soup.find_all(["h2", "h3"]):
        text = (h.get_text() or "").strip().lower()
        if text in ("sections", "in this chapter", "in this module"):
            ul = h.find_next_sibling(["ul", "ol"])
            if ul:
                ul.decompose()
                h.decompose()
                n += 1
                break
    return n


# ----------------------------------------------------------------------
# Inline math: ensure $...$ and <span class="math"> become inline-aligned
# ----------------------------------------------------------------------
def fix_math_alignment(soup: BeautifulSoup) -> int:
    """Post-process MathML output: strip TeX annotation (would leak as
    fallback text on non-MathML readers), add katex-rendered class, and
    mark display vs inline math for CSS targeting.

    Historical: this used to handle KaTeX HTML output which had ~400 empty
    structural spans per chapter (strut/pstrut/vlist) — Kindle painted those
    as tofu (■). We now render math as MathML (single <math> element), so
    those issues are gone. The legacy span-cleanup code below is kept as a
    safety net for any HTML-mode renders that slip through.
    """
    # Strip <annotation> tags: when Kindle falls back from MathML to plain
    # text, these would display the raw TeX source like "(x_1, x_2, T)".
    for ann in soup.find_all("annotation"):
        ann.decompose()
    # KaTeX bug: when an operator with limits (\max, \min, \sup, \inf) is used
    # as a subscript (e.g., D_{\max}), KaTeX emits a trailing
    # <mo>&#x2061;</mo> (function application, invisible) INSIDE the <msub>,
    # which violates the MathML schema (msub takes exactly 2 children) and
    # triggers epubcheck RSC-005. The character is invisible — safe to strip.
    for parent in soup.find_all(["msub", "msup", "msubsup"]):
        for child in list(parent.find_all("mo", recursive=False)):
            txt = child.get_text() or ""
            # U+2061 (function application), U+2062 (invisible times),
            # U+2063 (invisible separator), U+2064 (invisible plus)
            if any(c in txt for c in ("⁡", "⁢", "⁣", "⁤")):
                child.decompose()
    # Mark wrappers
    for el in soup.find_all(class_=lambda c: c and "katex" in c):
        cls = el.get("class") or []
        if "katex-rendered" not in cls:
            cls = list(cls) + ["katex-rendered"]
            el["class"] = cls
        parent = el.parent
        if parent and "math-block" in (parent.get("class") or []):
            if "katex-display" not in cls:
                el["class"] = cls + ["katex-display"]
    n = 0
    n_zwsp = 0
    n_closed = 0
    for span in soup.find_all(["span", "div"]):
        cls = span.get("class") or []
        if "katex" in cls and "katex-rendered" not in cls:
            new_cls = list(cls) + ["katex-rendered"]
            parent = span.parent
            if parent and "math-block" in (parent.get("class") or []):
                new_cls.append("katex-display")
            elif span.name == "div":
                new_cls.append("katex-display")
            span["class"] = new_cls
            n += 1
        # Strip ZWSPs from KaTeX vlist-s spans
        if "vlist-s" in cls:
            for child in list(span.children):
                if hasattr(child, "string") and child.string and "​" in child.string:
                    child.string.replace_with(child.string.replace("​", ""))
                    n_zwsp += 1
                elif isinstance(child, str) and "​" in child:
                    child.replace_with(child.replace("​", ""))
                    n_zwsp += 1
    # Global ZWSP strip across all katex elements
    for kx in soup.find_all(class_=lambda c: c and "katex" in c):
        for ns in list(kx.find_all(string=True)):
            if "​" in ns:
                ns.replace_with(ns.replace("​", ""))
                n_zwsp += 1
    # NUCLEAR: remove .vlist-s spans entirely (after ZWSP strip they're empty
    # but still 2px wide via display:table-cell; some Kindle versions paint
    # the cell as a tiny box ■). The vertical alignment they provided was
    # only useful for KaTeX's web layout — Kindle ignores those rules anyway.
    n_vs = 0
    for vs in soup.find_all(class_="vlist-s"):
        vs.decompose()
        n_vs += 1
    # Also: empty padding spans (no class, inside KaTeX vlist containers).
    # KaTeX writes things like <span class="vlist"><span></span></span>
    # for height-only spacers; Kindle paints them as 1-2px boxes.
    n_empty = 0
    for kx in soup.find_all(class_=lambda c: c and "katex" in c):
        for span in list(kx.find_all("span")):
            cls = span.get("class") or []
            # Drop only TRULY empty spans WITHOUT meaningful classes
            # (preserve mord, mopen, mclose, strut etc. which KaTeX needs even when empty)
            keep_classes = {
                'mord', 'mopen', 'mclose', 'mbin', 'mrel', 'mop', 'mpunct',
                'mspace', 'msupsub', 'strut', 'pstrut', 'mathnormal', 'mathrm',
                'mathit', 'mathbf', 'mathcal', 'mathfrak', 'sizing', 'base',
                'katex-html', 'katex', 'katex-display', 'katex-rendered',
                'vlist-t', 'vlist-t2', 'vlist-r', 'vlist',
                'svg-align', 'hide-tail', 'sqrt', 'accent', 'accent-body',
            }
            if not list(span.children) and not any(c in keep_classes for c in cls):
                span.decompose()
                n_empty += 1
    # Force explicit </span> on remaining empty KaTeX spans
    for kx in soup.find_all(class_=lambda c: c and "katex" in c):
        for empty in kx.find_all("span"):
            if not list(empty.children):
                from bs4 import NavigableString
                empty.append(NavigableString(""))
                n_closed += 1
    return n


# ----------------------------------------------------------------------
# Set explicit avatar dimensions (small avatars only)
# ----------------------------------------------------------------------
def set_explicit_avatar_dimensions(soup: BeautifulSoup) -> int:
    """Inline avatars (e.g. wisdom-council) need explicit width to render small."""
    n = 0
    for img in soup.find_all("img"):
        cls = img.get("class") or []
        src = img.get("src", "")
        is_avatar = (
            "agent-avatar-inline" in cls
            or "agent-avatar" in cls
            or "/agents/" in src
        )
        if is_avatar and not img.get("width"):
            img["width"] = "28"
            img["height"] = "28"
            n += 1
    return n


# ----------------------------------------------------------------------
# Master entrypoint called from html2pub builder
# ----------------------------------------------------------------------
def post_process(soup: BeautifulSoup, src_rel: str, cfg) -> None:
    """Apply all project transforms to the parsed chapter HTML."""
    if "wisdom-council" in src_rel:
        slim_wisdom_council(soup)
    syntax_highlight(soup)
    normalize_code_block_content(soup)
    wrap_wide_tables(soup, min_cols=6)
    slim_chapter_index_sections_list(soup, src_rel)
    fix_math_alignment(soup)
    set_explicit_avatar_dimensions(soup)
