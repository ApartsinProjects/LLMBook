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
    """Add `katex-rendered` class + ensure inline math has vertical-align: middle.

    html2pub renders KaTeX but emits raw <span class="katex"> blocks. The book's
    epub_overrides.css expects `.katex-rendered` and `.katex-display` for proper
    inline vs display separation. Without these, sub/superscripts and Greek
    letters break vertical alignment.
    """
    n = 0
    for span in soup.find_all(["span", "div"]):
        cls = span.get("class") or []
        if "katex" in cls and "katex-rendered" not in cls:
            new_cls = list(cls) + ["katex-rendered"]
            # Detect display vs inline: display math is wrapped in <p class="math-block">
            # or <div class="math-block">; inline is in <span class="math"> or text.
            parent = span.parent
            if parent and "math-block" in (parent.get("class") or []):
                new_cls.append("katex-display")
            elif span.name == "div":
                new_cls.append("katex-display")
            span["class"] = new_cls
            n += 1
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
