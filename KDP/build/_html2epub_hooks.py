"""Project-specific html2epub hooks for the LLMBook.

Wired via html2epub.toml:

    [plugins]
    post_process_html = "_html2epub_hooks.post_process"

Adds the transforms that html2epub doesn't know about (Pygments syntax
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
            # v13.10: support both `language-X` (Prism convention) and
            # `lang-X` (project convention). Previously only language-
            # was checked, silently skipping all lang-* code blocks
            # (e.g. section 0.3.7.1 stayed unhighlighted).
            for prefix in ("language-", "lang-"):
                if c.startswith(prefix):
                    trial = c[len(prefix):]
                    try:
                        get_lexer_by_name(trial)
                        lang = trial
                        break
                    except ClassNotFound:
                        continue
            if lang:
                break
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


def strip_code_block_whitespace(soup: BeautifulSoup) -> int:
    """v13.15: Strip leading/trailing blank lines from <pre><code> blocks.

    Source HTML often has:
        <pre><code>
        import re
        class X:
            ...
        </code></pre>

    The first newline after <code> is rendered as a blank line at the top
    of the code block, making code blocks look "over-indented" / having
    visible whitespace at the top.

    This function preserves internal whitespace (indentation) but strips
    pure-whitespace leading/trailing lines.

    Works on plain <code> blocks AND pygments-highlighted blocks (where
    the first/last child might be a NavigableString containing just \\n).
    """
    from bs4 import NavigableString
    n = 0
    for code in soup.find_all('code'):
        children = list(code.children)
        if not children:
            continue

        # LEADING: if first child is NavigableString starting with whitespace
        # ending in \n, strip the leading whitespace through and including \n
        first = children[0]
        if isinstance(first, NavigableString):
            s = str(first)
            # Find first non-whitespace OR a meaningful content marker
            stripped = s.lstrip(' \t\n\r')
            if stripped != s:
                # Replace with stripped version
                # If stripped is empty, remove the node
                if not stripped:
                    first.extract()
                else:
                    first.replace_with(NavigableString(stripped))
                n += 1

        # TRAILING: same for last child
        children = list(code.children)  # refresh after possible extract
        if not children:
            continue
        last = children[-1]
        if isinstance(last, NavigableString):
            s = str(last)
            stripped = s.rstrip(' \t\n\r')
            if stripped != s:
                if not stripped:
                    last.extract()
                else:
                    last.replace_with(NavigableString(stripped))
                n += 1

    # Bare <pre> output blocks (no nested <code>) leak the same leading/trailing
    # blank line. Code-OUTPUT is authored as `<pre>\n...content...\n</pre>`, so the
    # first/last direct child is a "\n..."/"...\n" NavigableString that the <code>
    # loop above never sees. Strip those too (handles CRLF as well as LF).
    for pre in soup.find_all('pre'):
        if pre.find('code') is not None:
            continue
        kids = list(pre.children)
        if kids and isinstance(kids[0], NavigableString):
            s = str(kids[0]); stripped = s.lstrip(' \t\n\r')
            if stripped != s:
                (kids[0].extract() if not stripped
                 else kids[0].replace_with(NavigableString(stripped)))
                n += 1
        kids = list(pre.children)
        if kids and isinstance(kids[-1], NavigableString):
            s = str(kids[-1]); stripped = s.rstrip(' \t\n\r')
            if stripped != s:
                (kids[-1].extract() if not stripped
                 else kids[-1].replace_with(NavigableString(stripped)))
                n += 1

    return n


def dedent_overindented_code(soup: BeautifulSoup) -> int:
    """v13.13: Some <pre><code> blocks have huge leading whitespace
    (32+ spaces) on every line, causing "over-indented cascading"
    visual when EPUB readers wrap long lines. Strip the COMMON
    leading whitespace from all lines while preserving relative
    indentation.

    Only operates on bare-text <code> blocks (not pre-tokenized
    pygments blocks) and on `<pre>` text content.
    """
    n_blocks = 0
    n_dedented = 0

    def common_indent(lines):
        """Find minimum leading whitespace across non-empty lines."""
        indents = []
        for line in lines:
            if not line.strip():
                continue
            stripped = line.lstrip()
            indents.append(len(line) - len(stripped))
        if not indents:
            return 0
        return min(indents)

    for pre in soup.find_all("pre"):
        # Get all text content (including from spans for pre-highlighted)
        text = pre.get_text()
        lines = text.split('\n')
        ci = common_indent(lines)
        if ci < 8:  # only dedent if MASSIVE over-indent (>=8 leading spaces)
            continue
        n_blocks += 1
        # Strip `ci` chars from start of each line in the pre's children
        # We can't easily edit pre-existing spans, so we re-render the text.
        # Walk through and modify any direct NavigableString or span text.
        from bs4 import NavigableString
        for child in list(pre.descendants):
            if isinstance(child, NavigableString) and child.parent is not None:
                s = str(child)
                # If it starts at a line boundary or this is the first text node
                # We need to strip leading spaces ONLY at line starts
                new_s = re.sub(
                    r'(^|\n)([ ]{' + str(ci) + r'})',
                    lambda m: m.group(1),
                    s
                )
                if new_s != s:
                    child.replace_with(NavigableString(new_s))
                    n_dedented += 1
    return n_blocks


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
# v13.6: Strip the "Wide Table (N columns) - On narrow screens..."
# prose note that html2epub's content.py:276 wrap_wide_tables() injects
# before every wide table. User reports this text leaks into book as
# visible content. The note adds zero information for the reader
# (the table is right there); the .complex-table CSS class remains
# on the table itself for any styling needs.
# ----------------------------------------------------------------------
def strip_wide_table_notes(soup: BeautifulSoup) -> int:
    """Remove .complex-table-note divs injected by html2epub library."""
    n = 0
    for note in soup.find_all("div", class_="complex-table-note"):
        note.decompose()
        n += 1
    return n


# ----------------------------------------------------------------------
# Chapter-index "Sections" heading: KEEP everything (no-op).
#
# The previous behavior removed both the <h2>Sections</h2> heading AND
# its sibling <ul class="sections-list"> on /index.html pages, with the
# rationale "redundant with EPUB nav." That assumption was wrong: the
# chapter-overview cards give readers a visual map of the chapter as
# they're reading the chapter intro -- the global EPUB nav is in a side
# panel and is not a substitute. Removing the cards left chapter-index
# pages looking sparse.
#
# The companion content.py:slim_index_lists has already been changed
# to FLATTEN <ul class="sections-list"> into <div class="section-grid">
# (preserving cards). This hook is now a no-op so the heading stays too.
# ----------------------------------------------------------------------
def slim_chapter_index_sections_list(soup: BeautifulSoup, src_rel: str) -> int:
    return 0  # disabled v789-followup: keep heading + cards intact


# ----------------------------------------------------------------------
# Inline math: ensure $...$ and <span class="math"> become inline-aligned
# ----------------------------------------------------------------------



def simplify_inline_mathml(soup: BeautifulSoup) -> int:
    """Replace simple inline <math> wrappers with plain HTML sub/sup.
    Returns count of replacements made.

    Patterns handled (inline only -- display math is left alone):
      <math><mrow><mi>K</mi></mrow></math>                → K
      <math><mrow><mi>K</mi><mi>i</mi></mrow></math>      → Ki (rare)
      <math><mrow><msub>...</msub></mrow></math>          → x<sub>i</sub>
      <math><mrow><msup>...</msup></mrow></math>          → x<sup>2</sup>
      <math><mrow><msubsup>...</msubsup></mrow></math>    → x<sub>i</sub><sup>2</sup>

    The replacement is a plain <span class="inline-math"> wrapping
    HTML <sub>/<sup>. The original wrapper class (katex-rendered)
    is removed so the EPUB reader treats it as normal inline text
    with proper line flow.
    """
    from bs4 import NavigableString

    n = 0

    # v13.15: character substitution for math operators with poor font
    # rendering. U+22C5 DOT OPERATOR -> U+00D7 MULTIPLICATION SIGN.
    # See fix_math_alignment() for the rationale.
    MATH_CHAR_FIX = {'⋅': '×'}

    def render_token(tok):
        """Return text content of <mi>, <mn>, <mo>, etc. as str.
        Also handles <mrow> with simple content (e.g., '-z' for negative
        exponent superscripts like e^-z)."""
        if tok is None:
            return None
        name = getattr(tok, "name", None)
        if name in ("mi", "mn", "mo", "ms", "mtext"):
            text = tok.get_text()
            for orig, sub in MATH_CHAR_FIX.items():
                text = text.replace(orig, sub)
            return text
        if name == "mrow":
            # Allow simple mrow: only mi/mn/mo children
            inner = [x for x in tok.children if getattr(x, "name", None)]
            if not inner:
                return None
            parts = []
            for c in inner:
                if c.name in ("mi", "mn", "mo", "ms", "mtext"):
                    parts.append(c.get_text())
                else:
                    return None  # complex inner, give up
            return "".join(parts)
        return None

    def convert_mrow(mrow):
        """If mrow content is simple enough, return a list of
        NavigableString / Tag pieces. Otherwise return None."""
        children = [c for c in mrow.children if getattr(c, "name", None)]
        if not children:
            return None
        pieces = []
        for c in children:
            name = c.name
            if name in ("mi", "mn", "mo", "ms", "mtext"):
                t = c.get_text()
                if t:
                    pieces.append(NavigableString(t))
            elif name == "msub":
                ch = [x for x in c.children if getattr(x, "name", None)]
                if len(ch) != 2:
                    return None
                base_text = render_token(ch[0])
                sub_text = render_token(ch[1])
                if base_text is None or sub_text is None:
                    return None
                if base_text:
                    pieces.append(NavigableString(base_text))
                sub_tag = soup.new_tag("sub")
                sub_tag.string = sub_text
                pieces.append(sub_tag)
            elif name == "msup":
                ch = [x for x in c.children if getattr(x, "name", None)]
                if len(ch) != 2:
                    return None
                base_text = render_token(ch[0])
                sup_text = render_token(ch[1])
                if base_text is None or sup_text is None:
                    return None
                if base_text:
                    pieces.append(NavigableString(base_text))
                sup_tag = soup.new_tag("sup")
                sup_tag.string = sup_text
                pieces.append(sup_tag)
            elif name == "msubsup":
                ch = [x for x in c.children if getattr(x, "name", None)]
                if len(ch) != 3:
                    return None
                base_text = render_token(ch[0])
                sub_text = render_token(ch[1])
                sup_text = render_token(ch[2])
                if any(t is None for t in (base_text, sub_text, sup_text)):
                    return None
                if base_text:
                    pieces.append(NavigableString(base_text))
                sub_tag = soup.new_tag("sub")
                sub_tag.string = sub_text
                pieces.append(sub_tag)
                sup_tag = soup.new_tag("sup")
                sup_tag.string = sup_text
                pieces.append(sup_tag)
            elif name == "mfrac":
                # Fraction: <mfrac>num den</mfrac> → num/den (inline)
                ch = [x for x in c.children if getattr(x, "name", None)]
                if len(ch) != 2:
                    return None
                num_text = render_token(ch[0])
                den_text = render_token(ch[1])
                if num_text is None or den_text is None:
                    return None
                # If either side has multiple terms, wrap in parens
                num = f"({num_text})" if len(num_text) > 2 else num_text
                den = f"({den_text})" if len(den_text) > 2 else den_text
                pieces.append(NavigableString(f"{num}/{den}"))
            elif name == "msqrt":
                # Square root: <msqrt>x</msqrt> → √x
                ch = [x for x in c.children if getattr(x, "name", None)]
                inner_parts = []
                for x in ch:
                    txt = render_token(x)
                    if txt is None:
                        return None
                    inner_parts.append(txt)
                inner = "".join(inner_parts)
                pieces.append(NavigableString("√" + inner))
            else:
                # Unknown / complex element (mover, mtable, mfenced...)
                return None
        return pieces

    for math in list(soup.find_all("math")):
        # Skip display math
        if math.get("display") == "block":
            continue
        # Walk inside mrow
        mrow = math.find("mrow")
        if mrow is None:
            mrow = math
        pieces = convert_mrow(mrow)
        if pieces is None:
            continue   # too complex, keep MathML
        # Find the enclosing wrapper span (.katex.katex-rendered)
        wrapper = math.parent
        if wrapper is None or wrapper.name != "span":
            wrapper = math
        # Replace wrapper with a plain span containing the pieces
        new_span = soup.new_tag("span")
        new_span["class"] = ["inline-math"]
        for p in pieces:
            new_span.append(p)
        wrapper.replace_with(new_span)
        n += 1

    return n


def number_headings(soup: BeautifulSoup, src_rel: str) -> int:
    """Prepend the authored chapter/section number to the chapter <h1>.

    The EPUB nav (ToC) is built from each chapter's <h1>, but the source keeps
    the number out of <h1> -- it lives in separate <div class="page-breadcrumb">
    ("... Chapter 0", "... Appendix A") and <div class="page-current">
    ("Section 0.1", "Section A.1") elements. Result: the EPUB ToC shows bare
    titles with no numbers. This prepends the number so BOTH the ToC and the
    chapter heading read e.g. "0.1  What Every LLM Engineer Needs..." /
    "Chapter 0: ML and PyTorch Foundations" / "Appendix A: Mathematical
    Foundations". Website is unaffected (EPUB-build hook only).

    Part indexes already carry "Part I: ..." in <h1>, so they're skipped.
    """
    from bs4 import NavigableString
    h1 = soup.find("h1")
    if h1 is None:
        return 0
    cur = h1.get_text(strip=True)
    if not cur:
        return 0
    # Already numbered ("Part I: ...", or a re-run that left "0.1 ..."/"A.1 ...").
    # NOT a bare leading digit -- titles like "3D Generation" must be numbered.
    if re.match(r"^(Part|Chapter|Appendix|Section)\b", cur) or re.match(r"^[A-Za-z]?\d+\.\d", cur):
        return 0

    label = None
    sep = "  "
    # Sections (regular + appendix): page-current "Section 0.1" / "Section A.1".
    pc = soup.find(class_="page-current")
    if pc:
        m = re.search(r"Section\s+([\w.]+)", pc.get_text())
        if m:
            label = m.group(1).rstrip(".")
            sep = " "  # en space between number and title
    if label is None:
        # Index pages: breadcrumb last segment "Chapter N" / "Appendix X".
        bc = soup.find(class_="page-breadcrumb")
        if bc:
            txt = bc.get_text(" ", strip=True)
            m = re.search(r"(Chapter\s+\d+|Appendix\s+[A-Z])\s*$", txt)
            if m:
                label = m.group(1)
                sep = ": "
    if not label:
        return 0
    # Merge the number INTO the first text node (not a separate node): the EPUB
    # nav title comes from h1.get_text(strip=True), which strips each node's
    # whitespace before concatenating -- a separate "0.1 " node would lose its
    # trailing space, giving "0.1What...". Merging keeps the space.
    first_text = h1.find(string=True)
    if first_text is not None:
        first_text.replace_with(NavigableString(label + sep + str(first_text)))
    else:
        h1.insert(0, NavigableString(label + sep))
    return 1


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
    # v13.4: UNWRAP <semantics> from inline MathML. The <semantics> element
    # is just an alternative-representation wrapper (used to hold both the
    # MathML and the TeX <annotation>). Once we've stripped the annotation
    # above, <semantics> contains only one <mrow> child. Some EPUB readers
    # (Calibre, KFX converter) render <semantics> as a block element,
    # forcing inline math like `p_i` onto its own line.
    # We unwrap it: move its children up into the <math> directly.
    for sem in soup.find_all("semantics"):
        sem.unwrap()
    # v13.5: Convert simple inline MathML to plain HTML sub/sup.
    # Inline <math> elements with single-letter or letter+sub/sup
    # patterns get replaced with <span><sub>i</sub></span>-style
    # markup. Eliminates line-break-around-math bug in EPUB readers
    # that treat <math> as block-level.
    n_simplified = simplify_inline_mathml(soup)

    # v13.15: apply MATH_CHAR_FIX to ALL math <mo> elements (both inline
    # math that didn't simplify AND all display math blocks).
    # Root cause: KaTeX emits U+22C5 DOT OPERATOR for \cdot. EPUB reader
    # fonts often render this glyph at baseline (looks like a period).
    # U+00B7 MIDDLE DOT helps in some fonts but not all. The most reliable
    # fix is U+00D7 MULTIPLICATION SIGN (×) which is in Latin-1 and
    # is positioned correctly in EVERY font (it's a 2D cross at middle).
    #
    # Mathematical equivalence: a · b = a × b for scalar multiplication.
    # Chain rule, gradients, dot product — all use × commonly in textbooks.
    MATH_CHAR_FIX_GLOBAL = {
        '⋅': '×',  # ⋅ DOT OPERATOR -> × MULTIPLICATION SIGN
    }
    n_chars_fixed = 0
    for mo in soup.find_all('mo'):
        text = mo.get_text()
        new_text = text
        for orig, sub in MATH_CHAR_FIX_GLOBAL.items():
            if orig in new_text:
                new_text = new_text.replace(orig, sub)
        if new_text != text:
            mo.clear()
            mo.append(new_text)
            n_chars_fixed += 1
    # Also fix raw text inside <mi>/<mn>/<mtext> (less common but possible)
    for el in soup.find_all(['mi', 'mn', 'mtext']):
        text = el.get_text()
        new_text = text
        for orig, sub in MATH_CHAR_FIX_GLOBAL.items():
            if orig in new_text:
                new_text = new_text.replace(orig, sub)
        if new_text != text:
            el.clear()
            el.append(new_text)
            n_chars_fixed += 1

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
    # KaTeX emits <mtable columnspacing=""> for \begin{aligned} (empty value
    # because aligned doesn't specify columns). Empty-string fails epubcheck
    # RSC-005 (must match mathlength regex). Drop the empty attribute and
    # also fix rowspacing/columnalign if empty.
    for mtable in soup.find_all("mtable"):
        for attr in ("columnspacing", "rowspacing", "columnalign", "rowalign"):
            v = mtable.get(attr, None)
            if v is not None and (not v or not v.strip()):
                del mtable[attr]
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
# ----------------------------------------------------------------------
# v797 KPV E21018 FIX + img style strip + alt entity decode
# ----------------------------------------------------------------------
def fix_img_for_kindle(soup: BeautifulSoup) -> int:
    """1. Strip inline `style` from <img> (Mobi parser rejects
       `height:auto` etc., causing E21018).
    2. Decode common HTML entities inside `alt` attribute values:
       `&gt;` -> Unicode arrow, `&lt;` -> ASCII <, `&amp;` -> &.
       Kindle Previewer's enhanced-Mobi parser fails on
       entity-encoded characters inside attribute values; the
       Unicode form is parsed correctly.
       Section 6.4's "curation funnel" is the only image with
       this pattern in the book (4 `-&gt;` arrows in alt text)."""
    n = 0
    for img in soup.find_all("img"):
        # Strip style attribute
        if img.has_attr("style"):
            del img["style"]
            n += 1
        # Sanitize alt: any char bs4 entity-encodes inside an attribute value
        # (&amp; &lt; &gt; &quot;) makes Kindle's Enhanced-Mobi parser fail with
        # E21018 ("Enhanced Mobi building failure ... Content: <img>"), aborting
        # the whole KFX conversion. Replace those chars with Unicode/word forms
        # that serialize literally. (Confirmed via KPV qualitychecks 2026-05-21.)
        alt = img.get("alt")
        if alt:
            new_alt = (alt.replace("->", "→").replace("<-", "←")
                       .replace("&", " and ").replace('"', "”")
                       .replace("<", " less than ").replace(">", " greater than "))
            new_alt = re.sub(r"\s+", " ", new_alt).strip()
            if new_alt != alt:
                img["alt"] = new_alt
                n += 1
    return n


# Master entrypoint called from html2epub builder
# ----------------------------------------------------------------------
def fix_svg_viewbox(soup: BeautifulSoup) -> int:
    """SVG attribute is `viewBox` (camelCase per the SVG spec). Browsers
    parsing HTML5 lenient-mode accept lowercase `viewbox`, but XHTML
    parsers (which EPUB uses) and Kindle's strict renderer ignore the
    misnamed attribute, falling back to the SVG intrinsic size and
    causing diagrams to clip / paint at the wrong dimensions.

    This is purely a casing fix; no content change."""
    n = 0
    for svg in soup.find_all("svg"):
        if svg.has_attr("viewbox") and not svg.has_attr("viewBox"):
            svg["viewBox"] = svg["viewbox"]
            del svg["viewbox"]
            n += 1
    return n


def templatize_metadata(soup: BeautifulSoup, cfg) -> int:
    """v14.2: substitute {{book.edition}}, {{book.publication_year}} etc.
    placeholders in HTML text with the canonical values from metadata.

    Source HTML uses placeholders so the next edition bump touches only
    metadata.yaml + html2epub.toml — no flag-day across 392 source files.
    """
    # Resolve values from cfg (html2epub passes the parsed [book] table)
    book_meta = {}
    if hasattr(cfg, 'get'):
        book_meta = cfg.get('book') or {}
    elif isinstance(cfg, dict):
        book_meta = cfg.get('book', {})
    # Fall back to environment if cfg empty
    edition = book_meta.get('edition') or 'Fourteenth Edition'
    pub_date = book_meta.get('publication_date') or '2026-05-15'
    pub_year = str(pub_date)[:4] if pub_date else '2026'
    title = book_meta.get('title') or 'Building Conversational AI with LLMs and Agents'

    placeholders = {
        '{{book.edition}}': edition,
        '{{book.publication_year}}': pub_year,
        '{{book.title}}': title,
        '{{book.publication_date}}': pub_date,
    }

    from bs4 import NavigableString
    n = 0
    for el in soup.find_all(string=True):
        text = str(el)
        new_text = text
        for ph, val in placeholders.items():
            if ph in new_text:
                new_text = new_text.replace(ph, val)
        if new_text != text:
            el.replace_with(NavigableString(new_text))
            n += 1
    return n


def post_process(soup: BeautifulSoup, src_rel: str, cfg) -> None:
    """Apply all project transforms to the parsed chapter HTML."""
    if "wisdom-council" in src_rel:
        slim_wisdom_council(soup)
    # v14.2: template substitution first (so downstream hooks see resolved text)
    templatize_metadata(soup, cfg)
    # Prepend chapter/section numbers to <h1> so the EPUB nav (ToC) and chapter
    # headings are numbered (source keeps numbers in breadcrumb/page-current).
    number_headings(soup, src_rel)
    syntax_highlight(soup)
    normalize_code_block_content(soup)
    # v13.15: strip leading/trailing blank lines from code blocks (was
    # causing visible empty space at top of every <pre>)
    strip_code_block_whitespace(soup)
    wrap_wide_tables(soup, min_cols=4)  # lowered from 6: 5-col tables also overflow Kindle
    strip_wide_table_notes(soup)  # v13.6: strip prose note html2epub injects
    # v13.14: dedent_overindented_code disabled — KPV reported E21018 after
    # enabling it. The text manipulation breaks something in the XHTML.
    slim_chapter_index_sections_list(soup, src_rel)
    fix_math_alignment(soup)
    fix_svg_viewbox(soup)
    set_explicit_avatar_dimensions(soup)
    fix_img_for_kindle(soup)
