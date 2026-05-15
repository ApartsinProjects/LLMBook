"""
Build a KDP-ready EPUB 3 from the LLMBook source HTML.

Usage:
    python build_epub.py [--max-image-side 1600] [--jpeg-quality 82]

What it does:
  1. Loads metadata.yaml and spine_manifest.json.
  2. For each HTML file in spine order:
       - Reads and parses with BeautifulSoup (lxml).
       - Strips <script> tags (animations, JS not supported in EPUB).
       - Drops the cover-page inline <style> block (canvas/animation CSS).
       - Rewrites all internal hrefs ("../foo.html") to flat EPUB-internal ids.
       - Collects all referenced images, re-encodes them (resize + JPEG-ify
         non-transparent PNGs) into the EPUB's img/ folder.
  3. Adds a generated cover.xhtml that displays cover_kdp.jpg.
  4. Bundles book.css plus epub_overrides.css.
  5. Generates the EPUB 3 nav (table of contents).
  6. Writes output/building-conversational-ai-llms-agents.epub.

Run from the KDP/build/ directory or anywhere; paths are absolute via PROJECT_ROOT.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import unicodedata
import urllib.parse
import uuid
from pathlib import Path
from typing import Iterable

import yaml
from bs4 import BeautifulSoup, NavigableString, Tag
from ebooklib import epub
from PIL import Image

SVG_NS = "http://www.w3.org/2000/svg"

# --------------------------------------------------------------------- paths

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KDP_DIR = PROJECT_ROOT / "KDP"
BUILD_DIR = KDP_DIR / "build"
OUTPUT_DIR = KDP_DIR / "output"
METADATA_FILE = KDP_DIR / "metadata" / "metadata.yaml"
SPINE_FILE = BUILD_DIR / "spine_manifest.json"
COVER_KDP = KDP_DIR / "cover" / "cover_kdp.jpg"
BOOK_CSS = PROJECT_ROOT / "styles" / "book.css"
OVERRIDES_CSS = BUILD_DIR / "epub_overrides.css"

OUTPUT_EPUB = OUTPUT_DIR / "building-conversational-ai-llms-agents.epub"
BLITZ_CSS = BUILD_DIR / "blitz.css"
FONTS_DIR = BUILD_DIR / "fonts"

# --------------------------------------------------------------------- helpers


def slugify(text: str) -> str:
    """Make a path-safe id from a string."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "x"


def resolve_relative(from_path: str, href: str) -> str:
    """
    Resolve an HTML href like '../../foo.html' relative to a source path
    (e.g. 'part-1-foundations/module-04/section-4.1.html'), returning a
    project-root-relative POSIX path. Drops any '#fragment' or '?query'.
    Returns '' if href is external (http/mailto/javascript) or empty.
    """
    href = (href or "").strip()
    if not href or href.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "#", "tel:")):
        return ""
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return ""
    base = Path(from_path).parent
    try:
        return (base / href).resolve().relative_to(PROJECT_ROOT).as_posix()
    except Exception:
        return ""


def fragment_of(href: str) -> str:
    """Return the '#fragment' portion of an href, or '' if absent."""
    if "#" in href:
        return "#" + href.split("#", 1)[1]
    return ""


def file_hash(p: Path) -> str:
    h = hashlib.md5()
    h.update(p.read_bytes())
    return h.hexdigest()[:10]


def _sniff_image_type(data: bytes, declared_ext: str) -> tuple[str | None, str | None]:
    """
    Return (mime, canonical_ext) based on actual file magic bytes.
    Used to detect mislabeled image files (JPEG content with .png suffix etc.)
    """
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ("image/png", ".png")
    if data.startswith(b"\xff\xd8\xff"):
        return ("image/jpeg", ".jpg")
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return ("image/gif", ".gif")
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return ("image/webp", ".webp")
    if declared_ext == ".svg" or data.lstrip().startswith(b"<svg") or data.lstrip().startswith(b"<?xml"):
        return ("image/svg+xml", ".svg")
    return (None, None)


# --------------------------------------------------------------------- image processing

class ImageBundle:
    """
    Collects every image referenced by any spine HTML file and produces
    a deduplicated, compressed set destined for the EPUB's img/ folder.

    Mapping is: source_relative_path (e.g. 'images/book-cover.png')
                -> bundled_name (e.g. 'img/abc1234567_book-cover.jpg')
    """

    def __init__(self, max_side: int = 1600, jpeg_quality: int = 82):
        self.max_side = max_side
        self.jpeg_quality = jpeg_quality
        self.path_to_bundle: dict[str, str] = {}  # source rel -> bundled epub path
        self.bundled_bytes: dict[str, bytes] = {}  # bundled epub path -> bytes
        self.bundled_mime: dict[str, str] = {}     # bundled epub path -> mime
        self.skipped: list[tuple[str, str]] = []   # (path, reason)

    def add(self, src_rel_from_root: str) -> str | None:
        """
        Register a source image and return its bundled EPUB-internal path,
        or None if the image is unavailable / unsupported.
        """
        if not src_rel_from_root:
            return None
        if src_rel_from_root in self.path_to_bundle:
            return self.path_to_bundle[src_rel_from_root]
        full = PROJECT_ROOT / src_rel_from_root
        if not full.exists() or not full.is_file():
            self.skipped.append((src_rel_from_root, "missing on disk"))
            return None

        ext = full.suffix.lower()
        if ext == ".svg":
            data = full.read_bytes()
            bundled = f"img/{file_hash(full)}_{slugify(full.stem)}.svg"
            mime = "image/svg+xml"
        elif ext in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            try:
                data, bundled, mime = self._reencode(full)
            except Exception as e:
                self.skipped.append((src_rel_from_root, f"reencode failed: {e}"))
                return None
        else:
            self.skipped.append((src_rel_from_root, f"unsupported ext {ext}"))
            return None

        self.path_to_bundle[src_rel_from_root] = bundled
        self.bundled_bytes[bundled] = data
        self.bundled_mime[bundled] = mime
        return bundled

    def _reencode(self, full: Path) -> tuple[bytes, str, str]:
        """Resize and (where appropriate) JPEG-ify a raster image.

        Strategy: figures inside the EPUB always render on a white page
        background. So we ALWAYS composite onto white and emit JPEG, which
        compresses dramatically better than RGBA PNG. This removes the
        Mermaid-leaves-transparent-corners bloat (saves ~15 MB across the
        book). The only exception is small icons / logos where preserving
        edge transparency matters; those are bundled from styles/icons/
        through a different code path.
        """
        with Image.open(full) as im:
            im.load()
            w, h = im.size

            # Composite onto white background (handles RGBA, LA, palette-with-
            # transparency, and the common case of Mermaid PNGs with alpha=0
            # in the corner padding).
            if im.mode in ("RGBA", "LA", "P"):
                rgba = im.convert("RGBA")
                white_bg = Image.new("RGB", rgba.size, (255, 255, 255))
                white_bg.paste(rgba, mask=rgba.split()[-1])
                im = white_bg
            else:
                im = im.convert("RGB")

            out_ext = "jpg"
            out_mime = "image/jpeg"

            # Downscale if longest side > max_side
            if max(w, h) > self.max_side:
                scale = self.max_side / max(w, h)
                new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
                im = im.resize(new_size, Image.Resampling.LANCZOS)

            buf = io.BytesIO()
            if out_ext == "jpg":
                im.save(buf, format="JPEG", quality=self.jpeg_quality, optimize=True, progressive=False)
            else:
                im.save(buf, format="PNG", optimize=True)
            data = buf.getvalue()

        bundled = f"img/{file_hash(full)}_{slugify(full.stem)}.{out_ext}"
        return data, bundled, out_mime


# --------------------------------------------------------------------- HTML cleaning

UNWANTED_TAGS = ["script", "noscript"]

# Inline <style> blocks larger than this many chars are dropped; the
# main book.css covers the bulk of the styling and these are usually
# page-specific animations / cover-page CSS.
DROP_INLINE_STYLE_OVER = 1500


# Whitelist of element names allowed in EPUB 3 XHTML (HTML5 + SVG 1.1 + MathML).
# Any element whose tag isn't in this set will be unwrapped during cleaning,
# which catches stray template-like tags such as <email_address> or <user_id>
# accidentally left in source HTML.
_ALLOWED_TAGS = frozenset({
    # HTML5 root + metadata + sections
    "html", "head", "body", "title", "meta", "link", "style", "base", "script", "noscript",
    "article", "aside", "footer", "header", "h1", "h2", "h3", "h4", "h5", "h6",
    "hgroup", "main", "nav", "section", "search", "address",
    # HTML5 grouping content
    "blockquote", "dd", "div", "dl", "dt", "figcaption", "figure", "hr",
    "li", "menu", "ol", "p", "pre", "ul",
    # HTML5 text-level
    "a", "abbr", "b", "bdi", "bdo", "br", "cite", "code", "data", "dfn",
    "em", "i", "kbd", "mark", "q", "rp", "rt", "ruby", "s", "samp",
    "small", "span", "strong", "sub", "sup", "time", "u", "var", "wbr",
    # HTML5 edits
    "del", "ins",
    # HTML5 embedded
    "area", "audio", "img", "map", "track", "video", "embed", "iframe",
    "object", "picture", "portal", "source",
    # HTML5 tabular
    "caption", "col", "colgroup", "table", "tbody", "td", "tfoot",
    "th", "thead", "tr",
    # HTML5 forms
    "button", "datalist", "fieldset", "form", "input", "label", "legend",
    "meter", "optgroup", "option", "output", "progress", "select", "textarea",
    # HTML5 interactive
    "details", "dialog", "summary",
    # HTML5 web components
    "slot", "template",
    # HTML5 canvas
    "canvas",
    # SVG
    "svg", "g", "defs", "symbol", "use", "image",
    "rect", "circle", "ellipse", "line", "polyline", "polygon", "path",
    "text", "tspan", "textpath", "tref",
    "marker", "pattern", "clippath", "mask", "filter",
    "lineargradient", "radialgradient", "stop",
    "fespecularlighting", "fediffuselighting", "fedistantlight", "fepointlight", "fespotlight",
    "feblend", "fecolormatrix", "fecomponenttransfer", "fecomposite", "feconvolvematrix",
    "fedisplacementmap", "fedropshadow", "feflood", "fegaussianblur", "feimage",
    "femerge", "femergenode", "femorphology", "feoffset", "feturbulence", "fetile",
    "func-r", "func-g", "func-b", "func-a",
    "desc", "metadata", "foreignobject", "switch", "set", "animate", "animatemotion",
    "animatetransform", "mpath",
    # MathML
    "math", "mi", "mn", "mo", "ms", "mspace", "mtext",
    "mfrac", "mroot", "msqrt", "msub", "msup", "msubsup",
    "munder", "mover", "munderover", "mrow", "mfenced",
    "merror", "mphantom", "mpadded", "mstyle", "mtable", "mtr", "mtd",
    "maligngroup", "malignmark", "menclose",
    "annotation", "annotation-xml", "semantics",
    # epub-specific
    "epub:switch", "epub:trigger", "epub:case", "epub:default",
})


def clean_chapter_html(soup: BeautifulSoup) -> None:
    """In-place: strip scripts, oversized inline styles, and EPUB-incompatible markup."""
    # Drop scripts entirely
    for tag in soup(UNWANTED_TAGS):
        tag.decompose()

    # Drop oversized inline styles (page-specific animations, cover CSS, etc.)
    for style in soup.find_all("style"):
        if len(style.get_text() or "") > DROP_INLINE_STYLE_OVER:
            style.decompose()

    # Drop SVG nested inside <a> (decorative social-media icons in front-matter pages).
    # EPUB's strict XHTML doesn't permit <svg> inside <a> without proper namespacing
    # and these are decorative anyway - the link itself remains.
    for a in soup.find_all("a"):
        for svg in a.find_all("svg"):
            svg.decompose()

    # Unwrap any tag that isn't part of HTML5/SVG/MathML. Source HTML
    # sometimes contains literal placeholder-like tags (<true>, <false>,
    # <email_address>, <user_name>, <api_key>) that are typos for escaped
    # example text. Unwrap them so the inner text survives.
    for el in soup.find_all(True):
        if el.name and el.name not in _ALLOWED_TAGS:
            el.unwrap()

    # Add the SVG namespace to any bare <svg> elements that don't have it.
    # Inline SVG in HTML5 is namespace-implicit, but XHTML in EPUB needs it explicit.
    for svg in soup.find_all("svg"):
        if "xmlns" not in svg.attrs:
            svg["xmlns"] = SVG_NS

    # Fix invalid characters in id attributes and url() / href fragments.
    # SVGs sometimes have ids like "grad_{bfbc}61_e8f4fd" with braces
    # which are illegal in URL fragments per RFC 3986.
    sanitize_invalid_url_chars(soup)

    # Make all element IDs unique within the document. Multiple SVGs in the
    # same chapter often reuse defs ids ("stdGrad2", "shadow2", "arrow").
    # XHTML requires document-wide ID uniqueness; epubcheck reports RSC-005.
    dedupe_element_ids(soup)

    # Drop or fix references to fragments that don't exist in the document.
    # epubcheck reports RSC-012 for these.
    drop_orphan_fragment_refs(soup)

    # Some code blocks contain unescaped HTML-like literal text (e.g. a
    # Python string `f"<pre>{x}</pre>"` written without escaping the angle
    # brackets). lxml parses those as real nested elements and produces
    # invalid block-in-inline structure. Collapse nested elements inside
    # <code> / <pre> to escaped text content.
    normalize_code_block_content(soup)

    # Apply Pygments syntax highlighting to <pre><code class='language-X'>
    # blocks. Source HTML uses Prism.js (client-side); without highlighting
    # at build time, code shows monochrome in EPUB readers.
    syntax_highlight(soup)

    # Pre-render math (KaTeX server-side via Node) so EPUB readers without
    # JavaScript see typeset math instead of raw $$...$$ syntax.
    render_math_in_soup(soup)

    # Slim chapter index pages: remove the "Sections" list (redundant with
    # EPUB's nav, saves 3-8 KB per chapter index = ~150 KB total).
    # Only affects chapter/module index pages, not actual content sections.
    slim_chapter_index_sections_list(soup)

    # Slim wisdom-council page: drop agent cards for personas not actually
    # quoted in the book's epigraphs. Saves ~30 unused agent images +
    # ~25 KB HTML. Keeps the cards for the 8 most-quoted agents only.
    slim_wisdom_council(soup)

    # Wrap wide tables (6+ cols) with a "complex - best viewed on tablet"
    # note. Per the tables_audit.md, 26 HIGH-severity tables won't fit
    # Kindle's ~600 px portrait width. Source HTML stays unchanged (the
    # tables are fine on desktop); this only adds a Kindle-friendly hint.
    wrap_wide_tables(soup)


def wrap_wide_tables(soup: BeautifulSoup) -> None:
    """Wrap any <table> with 6+ columns in a 'complex table' note + horizontal-scroll wrapper.

    Strategy:
      1. Add a class 'complex-table' to wide tables for CSS styling
      2. Insert a small note BEFORE the table: "Note: Wide table - on Kindle,
         text may wrap. For best layout, view on tablet or desktop."
      3. CSS in epub_overrides.css makes the table allow horizontal scroll
         so the data is at least preserved (not truncated)
    """
    for table in soup.find_all("table"):
        max_cols = 0
        for row in table.find_all("tr"):
            cells = row.find_all(["td", "th"])
            max_cols = max(max_cols, len(cells))
        if max_cols < 6:
            continue
        # Mark with class for CSS
        existing = table.get("class") or []
        if "complex-table" not in existing:
            existing.append("complex-table")
            table["class"] = existing
        # Skip if a note is already present immediately before
        prev = table.find_previous_sibling()
        if (prev is not None
            and prev.name == "div"
            and "complex-table-note" in (prev.get("class") or [])):
            continue
        # Build the note <div> as a callout
        note_div = soup.new_tag("div", attrs={"class": "callout note complex-table-note"})
        title_div = soup.new_tag("div", attrs={"class": "callout-title"})
        title_div.string = f"Wide Table ({max_cols} columns)"
        note_div.append(title_div)
        body_p = soup.new_tag("p")
        body_p.string = (
            "On narrow Kindle screens, columns will wrap or compress. "
            "For best layout, view on a tablet, computer, or in landscape orientation."
        )
        note_div.append(body_p)
        table.insert_before(note_div)


# Top-quoted agents from the audit (run grep for `wisdom-council.html#X`
# across all source HTML; counts as of 2026-05-10):
#   deploy:26, guard:18, eval:17, compass:16, sage:14, frontier:13,
#   agent-x:12, pip:11, rag:11, synth:10, scale:9, ...
# Keeping the top 8 (covers ~140 of the ~270 epigraph references).
WISDOM_COUNCIL_KEEP = frozenset({
    "deploy", "guard", "eval", "compass",
    "sage", "frontier", "agent-x", "pip",
})

# Module-level set of agent IDs that were dropped during this build.
# Populated by slim_wisdom_council; consumed by sanitize_invalid_url_chars
# (well, actually by a separate dropped-fragment rewriter). Tracks BOTH
# dropped IDs and which page they belonged to, so chapter epigraphs that
# linked to a dropped agent can be rewritten (drop the fragment, link
# still resolves to the wisdom-council page).
_DROPPED_FRAGMENTS: dict[str, set[str]] = {}  # file_basename -> {fragment_ids}


def _populate_dropped_fragments(spine_entries, chapter_map) -> None:
    """Pre-scan source files for IDs that will be dropped during build.

    Currently only handles the wisdom-council slim, but extensible to other
    drop-during-build mutations.
    """
    # Find the wisdom-council source page in the spine
    for entry in spine_entries:
        if entry["path"].endswith("wisdom-council.html"):
            src_path = PROJECT_ROOT / entry["path"]
            if not src_path.exists():
                return
            text = src_path.read_text(encoding="utf-8", errors="replace")
            # Match <div class="wc-card" id="X">
            for m in re.finditer(r'<div class="wc-card" id="([^"]+)"', text):
                wc_id = m.group(1)
                if wc_id not in WISDOM_COUNCIL_KEEP:
                    _DROPPED_FRAGMENTS.setdefault("wisdom-council", set()).add(wc_id)
            n = len(_DROPPED_FRAGMENTS.get("wisdom-council", set()))
            if n:
                print(f"  Pre-recorded {n} wisdom-council fragments that will be dropped during slim "
                      f"(chapter epigraph hrefs to those agents will be rewritten without fragment)")
            return


def slim_wisdom_council(soup: BeautifulSoup) -> None:
    """On the wisdom-council page, drop cards for agents not in the keep list.

    Detection: page contains a <div class="wc-grid"> with multiple
    <div class="wc-card" id="X"> children. We keep cards whose id is in
    WISDOM_COUNCIL_KEEP, decompose the rest, and prepend a brief note
    explaining the slim.
    """
    grid = soup.find("div", class_="wc-grid")
    if grid is None:
        return
    cards = grid.find_all("div", class_="wc-card", recursive=False)
    if len(cards) <= len(WISDOM_COUNCIL_KEEP):
        return  # already slim or no slimming needed

    kept = 0
    dropped = 0
    dropped_ids: set[str] = set()
    for card in cards:
        cid = card.get("id", "")
        if cid in WISDOM_COUNCIL_KEEP:
            kept += 1
        else:
            if cid:
                dropped_ids.add(cid)
            card.decompose()
            dropped += 1
    # Record dropped fragments so cross-document href references can be rewritten.
    # Wisdom-council file ends up at chapters/ch_NNNN_front-matter-wisdom-council.xhtml
    # in the EPUB. We track by the source-file slug "wisdom-council".
    if dropped_ids:
        _DROPPED_FRAGMENTS.setdefault("wisdom-council", set()).update(dropped_ids)

    # Prepend a note explaining the slim (only if we actually dropped cards)
    if dropped > 0:
        intro = soup.new_tag("p", attrs={"class": "wisdom-council-epub-note"})
        intro.string = (
            f"Note: This Kindle edition includes profiles for the {kept} most-quoted "
            f"members of the Wisdom Council. The web edition at llmbook.apartsin.com "
            f"includes profiles for all 42 Council members."
        )
        # Insert after the wisdom-council-intro paragraph if it exists
        intro_p = soup.find("p", class_="wisdom-council-intro")
        if intro_p is not None:
            intro_p.insert_after(intro)
        else:
            grid.insert_before(intro)


def render_math_in_soup(soup: BeautifulSoup) -> int:
    """Pre-render LaTeX math via KaTeX server-side (Node).

    The book's source HTML uses 4 math notations:
      1. <span class="math">$x^2$</span>            -> inline math
      2. $$...$$ standalone in text                  -> display math
      3. \\(...\\) inline in text                    -> inline math
      4. <div class="math-block">$$...$$</div>       -> display math

    All are KaTeX-targeted by the source's vendor/prism JS. EPUB strips
    JavaScript so without server-side rendering, readers see raw $...$
    syntax. We extract all math, send to a Node KaTeX renderer in one
    batch per chapter, and replace the original markup with rendered HTML.

    Returns the number of math expressions rendered.
    """
    import json, subprocess
    render_script = BUILD_DIR / "render_math.js"
    if not render_script.exists():
        return 0
    katex_modules = Path("E:/Tools/katex/node_modules")
    if not katex_modules.exists():
        return 0

    # ---- Collect math expressions to render
    items: list[dict] = []
    targets: list[tuple] = []  # (item_index, target_element, tag_to_replace)

    # 1. <span class="math">$expr$</span>  (and similar)
    for el in soup.find_all(attrs={"class": True}):
        if not el.get("class"):
            continue
        if "math" in el.get("class") and el.name in ("span", "div"):
            tex_raw = el.get_text()
            # Strip wrapper $...$ or $$...$$
            tex = _strip_math_delimiters(tex_raw)
            if not tex:
                continue
            display = ("math-block" in el.get("class")) or tex_raw.strip().startswith("$$")
            items.append({"id": str(len(items)), "tex": tex, "display": display})
            targets.append(("element", el))

    # 2. $$...$$ in text nodes (display math standalone)
    # 3. \(...\) in text nodes (inline math)
    # We handle these by walking text nodes that contain $ or \( markers.
    # To avoid double-processing, skip text already inside .math elements.
    for text_node in list(soup.find_all(string=True)):
        parent = text_node.parent
        if parent is None:
            continue
        # Skip if inside a math/code/pre/script/style element
        skip = False
        for ancestor in parent.parents:
            if ancestor.name in ("code", "pre", "script", "style"):
                skip = True
                break
            cls = ancestor.get("class") if ancestor.name else None
            if cls and "math" in cls:
                skip = True
                break
        if skip:
            continue
        s = str(text_node)
        if "$$" not in s and "\\(" not in s:
            continue
        # Find $$...$$ blocks
        new_parts = _split_math_in_text(s, items, targets)
        if new_parts is not None:
            # Replace the text node with a sequence of NavigableString + placeholder spans
            from bs4 import NavigableString
            new_nodes = []
            for kind, content in new_parts:
                if kind == "text":
                    new_nodes.append(NavigableString(content))
                else:
                    # placeholder span; we'll fill in after rendering
                    placeholder = soup.new_tag("span", attrs={
                        "class": ["_math_placeholder"],
                        "data-math-id": content,
                    })
                    placeholder.string = ""
                    new_nodes.append(placeholder)
                    targets.append(("placeholder", placeholder))
            # Replace text node with new nodes
            for n in reversed(new_nodes):
                text_node.insert_after(n)
            text_node.extract()

    if not items:
        return 0

    # ---- Call Node KaTeX renderer
    try:
        node_env = __import__("os").environ.copy()
        node_env["NODE_PATH"] = str(katex_modules)
        proc = subprocess.run(
            ["node", str(render_script)],
            input=json.dumps(items),
            capture_output=True,
            text=True,
            env=node_env,
            timeout=60,
            encoding="utf-8",
        )
        if proc.returncode != 0:
            return 0
        rendered = json.loads(proc.stdout)
    except Exception:
        return 0

    # Map id -> rendered html
    by_id = {r["id"]: r["html"] for r in rendered}
    # Map id -> original tex (used to inject alttext on <math> for ACC-009)
    tex_by_id = {it["id"]: it["tex"] for it in items}

    def _inject_math_alttext(parsed_soup, tex_source: str) -> None:
        """Set alttext on every <math> element inside parsed_soup.

        KaTeX 'html' output emits a <math> shell for accessibility but
        omits alttext. EPUB accessibility (ACC-009) requires alttext on
        every <math> element. Use the original LaTeX as alttext.
        """
        if not tex_source:
            return
        # Trim aggressively; alttext is a single attribute value, no newlines
        alt = " ".join(tex_source.split())
        for m in parsed_soup.find_all("math"):
            if not m.get("alttext"):
                m["alttext"] = alt

    # ---- Replace targets with rendered HTML
    n_replaced = 0
    for i, target in enumerate(targets):
        kind, el = target
        if kind == "element":
            mid = str(i)
            html = by_id.get(mid)
            if html is None:
                continue
            new_soup = BeautifulSoup(html, "lxml")
            _inject_math_alttext(new_soup, tex_by_id.get(mid, ""))
            wrap = new_soup.find(["span", "div"], class_="katex")
            if wrap is None:
                wrap = new_soup
            new_el = soup.new_tag("span")
            for child in list(wrap.children if hasattr(wrap, "children") else []):
                new_el.append(child.extract() if hasattr(child, "extract") else child)
            new_el["class"] = ["katex-rendered"] + (["katex-display"] if "math-block" in (el.get("class") or []) else [])
            el.replace_with(new_el)
            n_replaced += 1
        elif kind == "placeholder":
            mid = el.get("data-math-id", "")
            html = by_id.get(mid)
            if html is None:
                continue
            new_soup = BeautifulSoup(html, "lxml")
            _inject_math_alttext(new_soup, tex_by_id.get(mid, ""))
            wrap = new_soup.find(["span", "div"], class_="katex")
            if wrap is None:
                continue
            new_el = soup.new_tag("span")
            for child in list(wrap.children):
                new_el.append(child.extract() if hasattr(child, "extract") else child)
            new_el["class"] = ["katex-rendered"]
            el.replace_with(new_el)
            n_replaced += 1
    return n_replaced


def _strip_math_delimiters(s: str) -> str:
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


def _split_math_in_text(s: str, items: list, targets: list):
    """Split a text string on $$...$$ and \\(...\\) math delimiters.

    Returns a list of (kind, content) tuples where kind is 'text' or 'math'
    and content is either the literal text or the assigned math-id, or None
    if the text contained no math markers.
    """
    parts = []
    pos = 0
    found_any = False
    while pos < len(s):
        # Find next math marker
        next_dd = s.find("$$", pos)
        next_inline = s.find("\\(", pos)
        if next_dd < 0 and next_inline < 0:
            break
        # Pick whichever comes first
        if next_dd >= 0 and (next_inline < 0 or next_dd < next_inline):
            # Display math $$...$$
            close = s.find("$$", next_dd + 2)
            if close < 0:
                break
            tex = s[next_dd + 2:close].strip()
            if not tex:
                pos = close + 2
                continue
            # Add preceding text + math placeholder
            if next_dd > pos:
                parts.append(("text", s[pos:next_dd]))
            mid = str(len(items))
            items.append({"id": mid, "tex": tex, "display": True})
            parts.append(("math", mid))
            pos = close + 2
            found_any = True
        else:
            # Inline math \(...\)
            close = s.find("\\)", next_inline + 2)
            if close < 0:
                break
            tex = s[next_inline + 2:close].strip()
            if not tex:
                pos = close + 2
                continue
            if next_inline > pos:
                parts.append(("text", s[pos:next_inline]))
            mid = str(len(items))
            items.append({"id": mid, "tex": tex, "display": False})
            parts.append(("math", mid))
            pos = close + 2
            found_any = True
    if not found_any:
        return None
    if pos < len(s):
        parts.append(("text", s[pos:]))
    return parts


def _fix_svg_attr_case_in_zip(epub_path: Path) -> None:
    """Restore camelCase SVG attributes inside the written EPUB.

    Why this is needed: ebooklib's `write_epub` runs every chapter through
    its own html.parser-based pipeline before writing, which lowercases
    camelCase attribute names (`viewBox` -> `viewbox`, etc.). SVG renderers
    (including Kindle/KPV) require the camelCase form for these. We fix it
    by rewriting affected XHTML files in the produced ZIP.

    String substitution is safe because the lowercase forms never appear
    legitimately in HTML markup — only as a side-effect of BS4 mangling.
    """
    import zipfile, tempfile, shutil
    # SVG attribute case fixes (camelCase required by SVG spec)
    attr_fixes = {
        b"viewbox=":              b"viewBox=",
        b"preserveaspectratio=":  b"preserveAspectRatio=",
        b"patternunits=":         b"patternUnits=",
        b"patterntransform=":     b"patternTransform=",
        b"gradientunits=":        b"gradientUnits=",
        b"gradienttransform=":    b"gradientTransform=",
        b"clippathunits=":        b"clipPathUnits=",
        b"markerunits=":          b"markerUnits=",
        b"markerwidth=":          b"markerWidth=",
        b"markerheight=":         b"markerHeight=",
        b"refx=":                 b"refX=",
        b"refy=":                 b"refY=",
        b"spreadmethod=":         b"spreadMethod=",
        b"textlength=":           b"textLength=",
        b"lengthadjust=":         b"lengthAdjust=",
        b"basefrequency=":        b"baseFrequency=",
        b"numoctaves=":           b"numOctaves=",
        b"diffuseconstant=":      b"diffuseConstant=",
        b"specularconstant=":     b"specularConstant=",
        b"specularexponent=":     b"specularExponent=",
        b"stddeviation=":         b"stdDeviation=",
        b"kernelmatrix=":         b"kernelMatrix=",
        b"kernelunitlength=":     b"kernelUnitLength=",
        b"surfacescale=":         b"surfaceScale=",
        b"primitiveunits=":       b"primitiveUnits=",
        b"filterres=":            b"filterRes=",
        b"filterunits=":          b"filterUnits=",
        b"maskunits=":            b"maskUnits=",
        b"maskcontentunits=":     b"maskContentUnits=",
        b"tablevalues=":          b"tableValues=",
    }
    # SVG element name case fixes (camelCase required by SVG spec).
    # Replace both opening tag <foo and closing tag </foo
    elem_fixes_camel = {
        b"lineargradient":   b"linearGradient",
        b"radialgradient":   b"radialGradient",
        b"clippath":         b"clipPath",
        b"fedropshadow":     b"feDropShadow",
        b"feoffset":         b"feOffset",
        b"femerge":          b"feMerge",
        b"femergenode":      b"feMergeNode",
        b"fegaussianblur":   b"feGaussianBlur",
        b"feblend":          b"feBlend",
        b"fecolormatrix":    b"feColorMatrix",
        b"fecomposite":      b"feComposite",
        b"feconvolvematrix": b"feConvolveMatrix",
        b"fediffuselighting":  b"feDiffuseLighting",
        b"fespecularlighting": b"feSpecularLighting",
        b"fedisplacementmap":  b"feDisplacementMap",
        b"feflood":          b"feFlood",
        b"feimage":          b"feImage",
        b"femorphology":     b"feMorphology",
        b"feturbulence":     b"feTurbulence",
        b"fetile":           b"feTile",
        b"fefunca":          b"feFuncA",
        b"fefuncr":          b"feFuncR",
        b"fefuncg":          b"feFuncG",
        b"fefuncb":          b"feFuncB",
        b"felightsource":    b"feLightSource",
        b"fedistantlight":   b"feDistantLight",
        b"fepointlight":     b"fePointLight",
        b"fespotlight":      b"feSpotLight",
        b"fecomponenttransfer": b"feComponentTransfer",
        b"foreignobject":    b"foreignObject",
    }
    fixes = dict(attr_fixes)
    for low, mixed in elem_fixes_camel.items():
        fixes[b"<" + low] = b"<" + mixed
        fixes[b"</" + low] = b"</" + mixed
    n_files = 0
    n_subs = 0
    with tempfile.NamedTemporaryFile(suffix=".epub", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        with zipfile.ZipFile(epub_path, "r") as zin, \
             zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                data = zin.read(info.filename)
                if info.filename.endswith((".xhtml", ".html", ".svg", ".opf")):
                    file_subs = 0
                    for lo, hi in fixes.items():
                        if lo in data:
                            cnt = data.count(lo)
                            data = data.replace(lo, hi)
                            file_subs += cnt
                    if file_subs:
                        n_files += 1
                        n_subs += file_subs
                zout.writestr(info, data)
        shutil.move(str(tmp_path), str(epub_path))
        print(f"  [svg-attr-case] {n_subs} substitutions across {n_files} files")
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


def slim_chapter_index_sections_list(soup: BeautifulSoup) -> None:
    """Remove the redundant 'Sections' list from chapter index pages.

    Source HTML chapter-index pages (part-X/module-Y/index.html) have a
    "Sections" heading + <ul class="sections-list"> with one card per
    section. This is useful on the website (clickable card UI), but in
    EPUB it duplicates the auto-generated nav.xhtml table-of-contents.
    Strip from EPUB only; source HTML retains it for the web edition.
    """
    sections_lists = soup.find_all("ul", class_="sections-list")
    for ul in sections_lists:
        # Remove the preceding <h2>Sections</h2> heading too
        prev = ul.find_previous_sibling()
        if prev and prev.name == "h2" and prev.get_text(strip=True).lower() == "sections":
            prev.decompose()
        ul.decompose()

    # For agent-avatar-inline / agent-avatar-large wrappers, add explicit
    # width/height to the inner <img> elements so EPUB readers that don't
    # honor display:inline-flex still render the icon at the right size.
    set_explicit_avatar_dimensions(soup)


def set_explicit_avatar_dimensions(soup: BeautifulSoup) -> None:
    """Add width/height attributes to images inside agent-avatar wrappers.

    Source markup looks like:
        <span class="agent-avatar-inline" style="..."><img src="..."></span>
    The wrapper class controls sizing in CSS, but EPUB readers may ignore
    display:inline-flex and let the inner <img> render at its intrinsic
    size (often 200+ px). Setting width/height explicitly on the <img>
    fixes this regardless of CSS support.
    """
    sizes = {
        "agent-avatar-inline": (28, 28),
        "agent-avatar-large":  (80, 80),
        "agent-avatar":         (80, 80),
        "agent-card-avatar":   (52, 52),
    }
    for wrap_class, (w, h) in sizes.items():
        for wrap in soup.select(f".{wrap_class}"):
            for img in wrap.find_all("img"):
                if "width" not in img.attrs:
                    img["width"] = str(w)
                if "height" not in img.attrs:
                    img["height"] = str(h)


_BLOCK_TAGS_IN_CODE = frozenset({"pre", "div", "p", "ul", "ol", "table",
                                  "h1", "h2", "h3", "h4", "h5", "h6",
                                  "section", "article", "blockquote", "figure"})


def normalize_code_block_content(soup: BeautifulSoup) -> None:
    """Inside <code> or <pre>, if there are nested block-level elements,
    collapse the entire content to its plain-text representation. This
    handles source HTML where <pre>/</pre> inside string literals wasn't
    properly escaped."""
    for el in soup.find_all(["code", "pre"]):
        nested = el.find_all(_BLOCK_TAGS_IN_CODE)
        if not nested:
            continue
        text = el.get_text()
        el.clear()
        el.append(NavigableString(text))


# ----------------------------------------- Pygments-based syntax highlighting

_PYGMENTS = None  # lazy import

# Map source HTML language hints (Prism class names) to Pygments lexer names
_LANG_ALIASES = {
    "language-python": "python", "language-py": "python",
    "language-bash": "bash", "language-sh": "bash", "language-shell": "bash",
    "language-js": "javascript", "language-javascript": "javascript",
    "language-ts": "typescript", "language-typescript": "typescript",
    "language-json": "json",
    "language-yaml": "yaml", "language-yml": "yaml",
    "language-toml": "toml",
    "language-html": "html", "language-xml": "xml",
    "language-css": "css",
    "language-c": "c", "language-cpp": "cpp", "language-c++": "cpp",
    "language-rust": "rust",
    "language-go": "go",
    "language-sql": "sql",
    "language-dockerfile": "dockerfile",
    "language-makefile": "makefile",
    "language-text": "text", "language-plain": "text",
    "language-diff": "diff",
    "language-md": "markdown", "language-markdown": "markdown",
    "language-r": "r", "language-julia": "julia",
}


def syntax_highlight(soup: BeautifulSoup) -> int:
    """Add Pygments-tokenized spans to <pre><code class='language-X'> blocks.

    Most source HTML uses Prism.js client-side highlighting (just adds
    `language-X` classes; expects Prism to add token spans at runtime).
    EPUB readers don't run JS, so without server-side highlighting the
    code shows monochrome. This function pre-tokenizes those blocks at
    build time using Pygments so the EPUB ships with colored spans.

    Returns the number of code blocks highlighted.
    """
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
    formatter = HtmlFormatter(nowrap=True, classprefix="")  # spans only, no wrapper

    n = 0
    for code in soup.find_all("code"):
        # Look for language hint
        classes = code.get("class") or []
        lang = None
        for c in classes:
            if c in _LANG_ALIASES:
                lang = _LANG_ALIASES[c]
                break
            elif c.startswith("language-"):
                # Try the trimmed name directly
                trial = c[len("language-"):]
                try:
                    get_lexer_by_name(trial)
                    lang = trial
                    break
                except ClassNotFound:
                    continue
        if not lang:
            continue
        # Skip if already highlighted (has token spans)
        if code.find("span", class_=re.compile(r"^[a-z]{1,4}$")):
            continue
        text = code.get_text()
        try:
            lexer = get_lexer_by_name(lang)
            highlighted = highlight_fn(text, lexer, formatter).rstrip("\n")
            # Replace contents with parsed highlighted spans
            new_soup = BeautifulSoup(f"<wrap>{highlighted}</wrap>", "lxml")
            wrap = new_soup.find("wrap")
            if wrap:
                code.clear()
                # Wrap in a div with class 'highlight' to scope CSS
                code.append(wrap)
                wrap.unwrap()  # remove the wrap element, keep children
                n += 1
        except Exception:
            continue
    return n


def drop_orphan_fragment_refs(soup: BeautifulSoup) -> None:
    """
    Find all `#frag` references whose target id doesn't exist; clear them.
    For url(#id) attribute values, replace with 'none' so SVG fills/strokes
    don't break. For <a href="#frag">, just unwrap the link.
    """
    all_ids = {el["id"] for el in soup.find_all(attrs={"id": True}) if el.get("id")}
    for el in soup.find_all(True):
        for attr_name in list(el.attrs):
            val = el.attrs[attr_name]
            if not isinstance(val, str):
                continue
            # url(#frag) refs
            m = re.search(r"url\(#([^)]+)\)", val)
            if m and m.group(1) not in all_ids:
                el.attrs[attr_name] = re.sub(
                    r"url\(#[^)]+\)", "none", val
                )
                continue
            # href="#frag" or xlink:href="#frag"
            if attr_name in ("href", "{http://www.w3.org/1999/xlink}href") and val.startswith("#"):
                if val[1:] not in all_ids:
                    if el.name == "a":
                        el.unwrap()
                    else:
                        del el.attrs[attr_name]


_INVALID_URL_CHARS_RE = re.compile(r"[{}^\\\[\]`]")  # chars illegal in URL fragments


def _clean_id(text: str) -> str:
    return _INVALID_URL_CHARS_RE.sub("_", text)


def dedupe_element_ids(soup: BeautifulSoup) -> None:
    """
    Make all element id attributes unique within the document.
    When a duplicate is found, rename it and rewrite all references to it
    (url(#id) attribute values and href="#id" attributes) inside the same
    <svg> ancestor so SVG references continue to resolve.
    """
    seen: dict[str, int] = {}  # id -> next-available suffix counter

    for el in soup.find_all(attrs={"id": True}):
        old_id = el["id"]
        if not old_id:
            continue
        if old_id not in seen:
            seen[old_id] = 1
            continue
        # Duplicate. Generate a unique new id.
        n = seen[old_id]
        while True:
            new_id = f"{old_id}_d{n}"
            if new_id not in seen:
                break
            n += 1
        seen[old_id] = n + 1
        seen[new_id] = 1

        # Find the nearest containing <svg> (or fallback to whole doc).
        scope = el
        while scope.parent is not None and (scope.name != "svg"):
            scope = scope.parent
        if scope.name != "svg":
            scope = soup  # fall back to document scope

        el["id"] = new_id
        # Update url(#old) references and #old href fragments inside this scope
        for ref_el in scope.find_all(True):
            for attr_name in list(ref_el.attrs):
                val = ref_el.attrs[attr_name]
                if not isinstance(val, str):
                    continue
                if f"url(#{old_id})" in val:
                    ref_el.attrs[attr_name] = val.replace(
                        f"url(#{old_id})", f"url(#{new_id})"
                    )
                elif val == f"#{old_id}":
                    ref_el.attrs[attr_name] = f"#{new_id}"


def sanitize_invalid_url_chars(soup: BeautifulSoup) -> None:
    """Replace illegal URL chars in id attrs and url(...) refs."""
    # Sanitize id attributes
    for el in soup.find_all(attrs={"id": True}):
        if _INVALID_URL_CHARS_RE.search(el["id"]):
            el["id"] = _clean_id(el["id"])
    # Sanitize href fragments (#xxx)
    for a in soup.find_all(href=True):
        href = a["href"]
        if "#" in href:
            path, frag = href.split("#", 1)
            if _INVALID_URL_CHARS_RE.search(frag):
                a["href"] = f"{path}#{_clean_id(frag)}" if path else f"#{_clean_id(frag)}"
    # Sanitize SVG fill="url(#...)" and similar attributes
    for el in soup.find_all(True):
        for attr_name in list(el.attrs):
            val = el.attrs[attr_name]
            if isinstance(val, str) and "url(#" in val and _INVALID_URL_CHARS_RE.search(val):
                el.attrs[attr_name] = re.sub(
                    r"url\(#([^)]+)\)",
                    lambda m: f"url(#{_clean_id(m.group(1))})",
                    val,
                )


def extract_title(soup: BeautifulSoup, fallback: str) -> str:
    """Best-effort chapter title, used for nav."""
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    title = soup.find("title")
    if title and title.get_text(strip=True):
        # Strip "| Building Conversational AI..." suffix if present
        t = title.get_text(strip=True)
        if "|" in t:
            t = t.split("|", 1)[0].strip()
        return t
    return fallback


def chapter_id_for(spine_index: int, src_rel: str) -> str:
    """Stable EPUB chapter id derived from spine position + slug of source path."""
    base = slugify(src_rel.replace("/", "_").replace(".html", ""))
    return f"ch_{spine_index:04d}_{base}"[:80]


def chapter_filename(chapter_id: str) -> str:
    return f"chapters/{chapter_id}.xhtml"


# --------------------------------------------------------------------- EPUB build

def build(max_side: int, jpeg_quality: int) -> int:
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"Loading metadata: {METADATA_FILE.relative_to(PROJECT_ROOT)}")
    md = yaml.safe_load(METADATA_FILE.read_text(encoding="utf-8"))
    spine_entries = json.loads(SPINE_FILE.read_text(encoding="utf-8"))
    print(f"Spine has {len(spine_entries)} entries")

    images = ImageBundle(max_side=max_side, jpeg_quality=jpeg_quality)

    # ---- Pre-pass 1: assign chapter ids
    chapter_map: dict[str, dict] = {}  # src_rel -> { id, file, title, spine_index }
    for i, entry in enumerate(spine_entries):
        src_rel = entry["path"]
        cid = chapter_id_for(i, src_rel)
        chapter_map[src_rel] = {
            "id": cid,
            "file": chapter_filename(cid),
            "title": entry.get("title_hint") or src_rel,
            "kind": entry["kind"],
            "spine_index": i,
        }

    # ---- Pre-pass 1b: populate _DROPPED_FRAGMENTS for cross-document href rewriting.
    # Some build-time mutations (like slim_wisdom_council) drop element ids
    # that are referenced from other chapters' hrefs. We need to know which
    # ids will be dropped BEFORE we start rewriting hrefs in spine order.
    _populate_dropped_fragments(spine_entries, chapter_map)

    # ---- Pass 2: parse, clean, rewrite each chapter; collect images
    print("\nProcessing chapters...")
    chapter_xhtml: dict[str, str] = {}  # src_rel -> xhtml bytes (utf-8 string)

    n_links_rewritten = 0
    n_links_dropped = 0
    n_imgs_seen = 0

    for i, entry in enumerate(spine_entries):
        src_rel = entry["path"]
        full = PROJECT_ROOT / src_rel
        try:
            html = full.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  [skip] cannot read {src_rel}: {e}")
            continue
        soup = BeautifulSoup(html, "lxml")
        clean_chapter_html(soup)

        # Title
        title = extract_title(soup, fallback=src_rel)
        chapter_map[src_rel]["title"] = title

        # Rewrite anchor hrefs
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if not href or href.startswith(("http://", "https://", "mailto:", "javascript:", "tel:", "data:")):
                continue
            if href.startswith("#"):
                continue  # in-page anchor, leave alone
            target = resolve_relative(src_rel, href)
            frag = fragment_of(href)
            if target and target in chapter_map:
                # Both chapters live in chapters/, so href is just the filename.
                # If the fragment was dropped from the target page (e.g. by
                # slim_wisdom_council), strip the fragment so the link still
                # works (lands at top of target page).
                target_basename = target.rsplit("/", 1)[-1].replace(".html", "")
                effective_frag = frag
                if frag and target_basename in _DROPPED_FRAGMENTS:
                    frag_id = frag.lstrip("#")
                    if frag_id in _DROPPED_FRAGMENTS[target_basename]:
                        effective_frag = ""
                a["href"] = chapter_map[target]["file"].rsplit("/", 1)[-1] + effective_frag
                n_links_rewritten += 1
            else:
                # Drop the link (turn into plain text) so EPUB readers don't 404
                a.unwrap()
                n_links_dropped += 1

        # Rewrite img srcs
        for img in soup.find_all("img"):
            n_imgs_seen += 1
            src = img.get("src", "")
            if not src or src.startswith(("http://", "https://", "data:")):
                continue
            target = resolve_relative(src_rel, src)
            bundled = images.add(target)
            if bundled is None:
                # Image missing - drop the img tag so EPUB validates
                img.decompose()
                continue
            # epub-internal path is relative to the chapter file in chapters/
            img["src"] = "../" + bundled

        # Drop <link rel="stylesheet"> tags - we manage CSS at the EPUB level
        for link in soup.find_all("link", rel=lambda v: v and "stylesheet" in v):
            link.decompose()

        # Drop external scripts referenced via <script src=...> - already removed by clean_chapter_html

        # Body content extraction
        body = soup.find("body")
        if body is None:
            print(f"  [warn] {src_rel} has no <body>; using whole document")
            body_inner = str(soup)
        else:
            body_inner = "".join(str(c) for c in body.children)

        # SVG camelCase attributes (viewBox, preserveAspectRatio, etc.) are
        # restored AFTER ebooklib writes the EPUB; see _fix_svg_attr_case_in_zip.
        # Doing it inline here would be wasted work because ebooklib re-parses
        # the content through its own html.parser before writing the ZIP, and
        # would lowercase it again.

        # Wrap into a clean XHTML document.
        # Stylesheet load order matters:
        #   1. blitz.css       - cross-reader typography baseline (FriendsOfEpub/Blitz)
        #   2. book.css        - project's design identity
        #   3. epub_overrides.css - EPUB-specific tweaks + embedded fonts + callout colors
        xhtml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>{escape_xml(title)}</title>
<link rel="stylesheet" type="text/css" href="../styles/blitz.css" />
<link rel="stylesheet" type="text/css" href="../styles/katex.min.css" />
<link rel="stylesheet" type="text/css" href="../styles/book.css" />
<link rel="stylesheet" type="text/css" href="../styles/epub_overrides.css" />
</head>
<body>
{body_inner}
</body>
</html>
"""
        chapter_xhtml[src_rel] = xhtml

        if (i + 1) % 50 == 0 or i == len(spine_entries) - 1:
            print(f"  [{i+1:>3}/{len(spine_entries)}] {src_rel}")

    print(f"\nLinks rewritten: {n_links_rewritten}, dropped (external/unknown): {n_links_dropped}")
    print(f"Images seen: {n_imgs_seen}, bundled: {len(images.bundled_bytes)}, skipped: {len(images.skipped)}")
    if images.skipped:
        print("First 10 skipped images:")
        for p, reason in images.skipped[:10]:
            print(f"  {p}: {reason}")

    # ---- Pass 3: assemble the EPUB
    print("\nAssembling EPUB...")
    book = epub.EpubBook()

    # Identifier - use ISBN if present, else a real UUID4. The metadata file
    # may contain a non-UUID-formatted "urn:uuid:..." string which epubcheck rejects.
    isbn = (md.get("identifiers", {}) or {}).get("isbn", "") or ""
    cfg_uuid = (md.get("identifiers", {}) or {}).get("uuid", "") or ""
    if not isbn:
        try:
            uuid.UUID(cfg_uuid.replace("urn:uuid:", "").strip())
            book_uuid = cfg_uuid if cfg_uuid.startswith("urn:uuid:") else f"urn:uuid:{cfg_uuid}"
        except (ValueError, AttributeError):
            book_uuid = f"urn:uuid:{uuid.uuid4()}"
        book.set_identifier(book_uuid)
        print(f"  Identifier: {book_uuid}")
    else:
        book.set_identifier(isbn)
        print(f"  Identifier (ISBN): {isbn}")

    book.set_language(md["book"].get("language", "en"))

    # Title and subtitle
    full_title = md["book"]["title"]
    subtitle = md["book"].get("subtitle", "")
    if subtitle:
        book.set_title(f"{full_title}: {subtitle}")
    else:
        book.set_title(full_title)

    # Authors. We bypass book.add_author() because it produces duplicate
    # creator entries with shared file-as refinement, which epubcheck rejects.
    # Instead, add each creator with a unique id and refine file-as/role
    # to point to that id.
    for i, au in enumerate(md.get("authors", []) or []):
        cid = f"creator_{i:02d}"
        book.add_metadata("DC", "creator", au["name"], {"id": cid})
        book.add_metadata(
            None, "meta", au.get("file_as", au["name"]),
            {"refines": f"#{cid}", "property": "file-as"},
        )
        book.add_metadata(
            None, "meta", au.get("role", "aut"),
            {"refines": f"#{cid}", "property": "role", "scheme": "marc:relators"},
        )

    # Description and rights
    desc_html = (KDP_DIR / "metadata" / "description.html").read_text(encoding="utf-8")
    book.add_metadata("DC", "description", strip_tags(desc_html))
    if md["book"].get("rights"):
        book.add_metadata("DC", "rights", md["book"]["rights"])
    if md["book"].get("publication_date"):
        book.add_metadata("DC", "date", md["book"]["publication_date"])
    publisher = (md.get("publisher") or {}).get("name") or ""
    if publisher:
        book.add_metadata("DC", "publisher", publisher)

    # Subject keywords
    for kw in (md.get("kdp", {}) or {}).get("keywords", []):
        book.add_metadata("DC", "subject", kw)

    # Cover image
    cover_bytes = COVER_KDP.read_bytes()
    book.set_cover("cover.jpg", cover_bytes)

    # KaTeX CSS for server-side-rendered math (loaded before book.css
    # so the project's overrides can refine math styles).
    # Strip woff and ttf src() entries from each @font-face block so we
    # only need to bundle woff2 fonts (smallest, modern reader support).
    katex_css = Path("E:/Tools/katex/node_modules/katex/dist/katex.min.css")
    if katex_css.exists():
        import re as _re
        css_text = katex_css.read_text(encoding="utf-8")
        # Each @font-face block has src:url(fonts/X.woff2) format("woff2"),
        # url(fonts/X.woff) format("woff"),url(fonts/X.ttf) format("truetype");
        # Drop the woff and ttf entries (keep only woff2).
        css_text = _re.sub(
            r',url\(fonts/[^)]+\.woff\) format\("woff"\)',
            "",
            css_text,
        )
        css_text = _re.sub(
            r',url\(fonts/[^)]+\.ttf\) format\("truetype"\)',
            "",
            css_text,
        )
        # Rewrite remaining woff2 paths from styles/-relative to fonts/ at root
        css_text = css_text.replace("url(fonts/", "url(../fonts/")
        book.add_item(epub.EpubItem(
            uid="css_katex",
            file_name="styles/katex.min.css",
            media_type="text/css",
            content=css_text.encode("utf-8"),
        ))
        # Bundle KaTeX fonts. CSS @font-face references all 3 formats
        # (woff2, woff, ttf) - epubcheck flags missing as RSC-007.
        katex_fonts_dir = katex_css.parent / "fonts"
        n_katex_fonts = 0
        if katex_fonts_dir.exists():
            font_media_types = {".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf"}
            for font in katex_fonts_dir.iterdir():
                if font.suffix.lower() in font_media_types:
                    book.add_item(epub.EpubItem(
                        uid=f"katex_font_{slugify(font.stem)}_{font.suffix[1:]}",
                        file_name=f"fonts/{font.name}",
                        media_type=font_media_types[font.suffix.lower()],
                        content=font.read_bytes(),
                    ))
                    n_katex_fonts += 1
        print(f"  Bundled katex.min.css + {n_katex_fonts} KaTeX font files")

    # CSS items - Blitz first (typography baseline), then book.css (project
    # design), then epub_overrides.css (EPUB-specific tweaks, fonts, callouts).
    if BLITZ_CSS.exists():
        book.add_item(epub.EpubItem(
            uid="css_blitz",
            file_name="styles/blitz.css",
            media_type="text/css",
            content=BLITZ_CSS.read_bytes(),
        ))
        print(f"  Bundled blitz.css ({BLITZ_CSS.stat().st_size / 1024:.1f} KB)")
        # Bundle Blitz's asterism.svg ornament (referenced by blitz.css as
        # ../Images/asterism.svg, resolves to EPUB/Images/asterism.svg)
        asterism = BUILD_DIR / "asterism.svg"
        if asterism.exists():
            book.add_item(epub.EpubItem(
                uid="img_asterism",
                file_name="Images/asterism.svg",
                media_type="image/svg+xml",
                content=asterism.read_bytes(),
            ))
    book.add_item(epub.EpubItem(
        uid="css_book",
        file_name="styles/book.css",
        media_type="text/css",
        content=BOOK_CSS.read_bytes(),
    ))
    book.add_item(epub.EpubItem(
        uid="css_overrides",
        file_name="styles/epub_overrides.css",
        media_type="text/css",
        content=OVERRIDES_CSS.read_bytes(),
    ))

    # Bundle subsetted woff2 fonts. CSS @font-face rules in epub_overrides.css
    # reference these as ../fonts/<name>.woff2 from each chapter file.
    n_fonts = 0
    if FONTS_DIR.exists():
        for font in sorted(FONTS_DIR.glob("*.woff2")):
            book.add_item(epub.EpubItem(
                uid=f"font_{slugify(font.stem)}",
                file_name=f"fonts/{font.name}",
                media_type="font/woff2",
                content=font.read_bytes(),
            ))
            n_fonts += 1
    print(f"  Bundled {n_fonts} font files from KDP/build/fonts/")

    # Bundle the styles/icons/ folder so book.css's url(...) references
    # resolve inside the EPUB. Without this, epubcheck reports RSC-007.
    # Some icons in this project have wrong extensions (JPEG content with
    # .png suffix); we sniff actual content and emit with the correct
    # mime type and extension to avoid epubcheck OPF-029 / PKG-022.
    icons_dir = PROJECT_ROOT / "styles" / "icons"
    n_icons = 0
    if icons_dir.exists():
        for icon in sorted(icons_dir.iterdir()):
            if not icon.is_file():
                continue
            data = icon.read_bytes()
            actual_mime, actual_ext = _sniff_image_type(data, icon.suffix.lower())
            if actual_mime is None:
                continue  # unsupported / unknown
            # Use the original filename (CSS references it by that name) but
            # when the content disagrees with the extension, both get fixed:
            # we re-encode mismatched files to match the declared extension.
            out_data = data
            out_name = icon.name
            if icon.suffix.lower() != actual_ext:
                # Either re-encode to match the declared extension, or rename.
                # Renaming would break CSS url() refs, so re-encode instead.
                try:
                    with Image.open(io.BytesIO(data)) as im:
                        buf = io.BytesIO()
                        if icon.suffix.lower() == ".png":
                            im.convert("RGBA" if im.mode in ("RGBA", "LA") else "RGB").save(buf, format="PNG", optimize=True)
                            actual_mime = "image/png"
                        elif icon.suffix.lower() in (".jpg", ".jpeg"):
                            im.convert("RGB").save(buf, format="JPEG", quality=85, optimize=True)
                            actual_mime = "image/jpeg"
                        out_data = buf.getvalue()
                except Exception as e:
                    print(f"  WARN: could not re-encode icon {icon.name}: {e}")
            book.add_item(epub.EpubItem(
                uid=f"icon_{slugify(icon.stem)}",
                file_name=f"styles/icons/{out_name}",
                media_type=actual_mime,
                content=out_data,
            ))
            n_icons += 1
    print(f"  Bundled {n_icons} icon files from styles/icons/")

    # Image items
    for bundled, data in images.bundled_bytes.items():
        mime = images.bundled_mime[bundled]
        uid = "img_" + slugify(bundled)
        book.add_item(epub.EpubItem(
            uid=uid,
            file_name=bundled,
            media_type=mime,
            content=data,
        ))

    # Chapter items. EPUB 3 requires properties="svg" on the OPF manifest item
    # for any XHTML that contains an inline SVG. Detect and set automatically.
    chapter_items: list[epub.EpubHtml] = []
    n_svg_chapters = 0
    for entry in spine_entries:
        src_rel = entry["path"]
        if src_rel not in chapter_xhtml:
            continue
        info = chapter_map[src_rel]
        xhtml_content = chapter_xhtml[src_rel]
        ch = epub.EpubHtml(
            uid=info["id"],
            file_name=info["file"],
            title=info["title"],
            lang=md["book"].get("language", "en"),
            content=xhtml_content.encode("utf-8"),
        )
        # CRITICAL: ebooklib's EpubHtml uses its own internal template that
        # IGNORES <link> tags inside the content's <head>. We must register
        # stylesheets via .add_link() so they appear in the rendered head.
        # Without this, the EPUB renders with browser defaults — no Blitz
        # typography, no book.css design, no callouts, no math fonts.
        ch.add_link(href="../styles/blitz.css", rel="stylesheet", type="text/css")
        ch.add_link(href="../styles/katex.min.css", rel="stylesheet", type="text/css")
        ch.add_link(href="../styles/book.css", rel="stylesheet", type="text/css")
        ch.add_link(href="../styles/epub_overrides.css", rel="stylesheet", type="text/css")
        if "<svg" in xhtml_content.lower():
            ch.properties = ["svg"]
            n_svg_chapters += 1
        book.add_item(ch)
        chapter_items.append(ch)
    print(f"  {n_svg_chapters} chapters tagged with properties='svg'")

    # Make ebooklib's auto-generated cover.xhtml linear so it's reachable
    # from the spine. Without this, epubcheck reports OPF-096.
    cover_html = book.get_item_with_id("cover")
    if cover_html is not None:
        cover_html.is_linear = True

    # ebooklib's set_cover() already created cover.xhtml and registered it.
    # We just need to put it into the spine in front.

    # ---- Build the nav (table of contents + landmarks)
    # Custom nav.xhtml with both <nav epub:type="toc"> and <nav epub:type="landmarks">.
    # The landmarks nav lets Kindle/Apple Books show a "Go To" menu that jumps
    # directly to cover, foreword, body, capstone, appendices - much more useful
    # than scrolling the full 441-entry chapter list.
    toc = build_toc(spine_entries, chapter_map, chapter_items)
    book.toc = toc

    # Build a custom nav.xhtml as a regular EpubItem (not EpubNav) so we
    # can include landmarks alongside the TOC.
    nav_html = build_nav_xhtml(spine_entries, chapter_map, chapter_items, full_title)
    nav_item = epub.EpubItem(
        uid="nav",
        file_name="nav.xhtml",
        media_type="application/xhtml+xml",
        content=nav_html.encode("utf-8"),
    )
    nav_item.properties = ["nav"]
    book.add_item(nav_item)
    book.add_item(epub.EpubNcx())

    # Spine: cover, then nav, then all chapters
    book.spine = ["cover", "nav"] + chapter_items

    # ---- Write
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(OUTPUT_EPUB), book, {})

    # Post-write: ebooklib re-parses content through html.parser when writing,
    # which lowercases SVG camelCase attributes (viewBox -> viewbox, etc.).
    # Patch the ZIP in place to restore the SVG attribute case Kindle and
    # SVG renderers expect.
    _fix_svg_attr_case_in_zip(OUTPUT_EPUB)

    out_size = OUTPUT_EPUB.stat().st_size
    print(f"\n[OK] Wrote {OUTPUT_EPUB.relative_to(PROJECT_ROOT)}")
    print(f"  Size: {out_size / 1024 / 1024:.2f} MB ({out_size:,} bytes)")
    print(f"  Chapters: {len(chapter_items)}")
    print(f"  Images bundled: {len(images.bundled_bytes)}")

    # Also archive a per-edition copy so editions don't overwrite each other.
    # The current edition is read from KDP/metadata/metadata.yaml -> book.edition_number.
    # Falls back silently if metadata is missing or unreadable.
    # NOTE: do NOT re-import yaml here -- it would shadow the module-level
    # import inside this function and break the earlier metadata load.
    try:
        with open(METADATA_FILE, encoding="utf-8") as fh:
            meta = yaml.safe_load(fh) or {}
        book_meta = meta.get("book", {}) or {}
        edition_n = book_meta.get("edition_number")
        if edition_n:
            edition_label = f"{edition_n}th-edition"
            # Use proper ordinal suffixes for 1, 2, 3
            if edition_n == 1:
                edition_label = "1st-edition"
            elif edition_n == 2:
                edition_label = "2nd-edition"
            elif edition_n == 3:
                edition_label = "3rd-edition"
            edition_dir = OUTPUT_DIR / "editions" / edition_label
            edition_dir.mkdir(parents=True, exist_ok=True)
            edition_copy = edition_dir / f"building-conversational-ai-llms-agents-{edition_label}.epub"
            import shutil
            shutil.copy2(OUTPUT_EPUB, edition_copy)
            print(f"  Edition archive: {edition_copy.relative_to(PROJECT_ROOT)}")
    except Exception as e:
        print(f"  (skipped edition archive: {e})")

    # KDP delivery-fee implication
    mb = out_size / 1024 / 1024
    fee = mb * 0.15
    print(f"\nKDP delivery fee estimate (70% royalty plan): ~USD {fee:.2f} per sale at ~$0.15/MB")
    if mb > 50:
        print(f"  WARNING: > 50 MB; may be too large for 70% royalty plan to be profitable")

    return 0


def build_nav_xhtml(spine_entries, chapter_map, chapter_items, book_title: str) -> str:
    """Build a custom nav.xhtml with both <nav epub:type='toc'> and <nav epub:type='landmarks'>.

    The landmarks nav is what powers the 'Go To' menu in Kindle / Apple Books / Kobo,
    letting readers jump straight to cover, foreword, body, appendices, etc. without
    scrolling a 441-entry TOC.
    """
    items_by_id = {ci.id: ci for ci in chapter_items}

    # Build hierarchical TOC HTML
    toc_html = _build_toc_ol(spine_entries, chapter_map, items_by_id)

    # Build landmarks list
    landmarks = _build_landmarks(spine_entries, chapter_map, items_by_id)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Contents</title>
<link rel="stylesheet" type="text/css" href="styles/blitz.css" />
<link rel="stylesheet" type="text/css" href="styles/epub_overrides.css" />
</head>
<body>
<nav epub:type="toc" id="toc" role="doc-toc">
<h1>Contents</h1>
{toc_html}
</nav>
<nav epub:type="landmarks" id="landmarks" hidden="">
<h2>Guide</h2>
<ol>
{landmarks}
</ol>
</nav>
</body>
</html>
"""


def _build_toc_ol(spine_entries, chapter_map, items_by_id) -> str:
    """Build a hierarchical <ol> grouping chapters under part / module.

    Strategy: bucket entries into a tree first, then render. Avoids the
    open/close state-machine bugs from the previous flat-loop approach.
    """
    front_matter: list[dict] = []
    # parts is dict order-preserving: {"part-N-name": {"info": part_info,
    #     "modules": [{"info": mod_info, "sections": [section_info]}]}}
    parts: dict[str, dict] = {}
    capstone: list[dict] = []
    appendix_root_info: dict | None = None
    appendices: list[dict] = []  # individual appendix-X items

    cur_part_name = None
    cur_module = None
    cur_appendix = None

    for entry in spine_entries:
        info = chapter_map.get(entry["path"])
        if not info:
            continue
        kind = entry["kind"]
        path_parts = entry["path"].split("/")

        if kind == "front-matter":
            front_matter.append(info)
        elif kind == "part-index":
            cur_part_name = path_parts[0]
            parts[cur_part_name] = {"info": info, "modules": []}
            cur_module = None
        elif kind == "module-index":
            cur_module = {"info": info, "sections": []}
            if cur_part_name and cur_part_name in parts:
                parts[cur_part_name]["modules"].append(cur_module)
        elif kind == "section":
            if cur_module is not None:
                cur_module["sections"].append(info)
        elif kind == "capstone-index" or kind == "capstone":
            capstone.append(info)
        elif kind == "appendix-index":
            appendix_root_info = info
            cur_appendix = None
        elif kind == "appendix":
            cur_appendix = {"info": info, "sections": []}
            appendices.append(cur_appendix)
        elif kind == "appendix-section":
            if cur_appendix is not None:
                cur_appendix["sections"].append(info)

    # Render the tree as nested <ol>/<li>/<a> with no orphan tags
    L: list[str] = ["<ol>"]

    if front_matter:
        L.append("<li>")
        # Use the first front-matter item as the link target for the parent label
        L.append(f'<a href="{escape_xml(front_matter[0]["file"])}">Front Matter</a>')
        L.append("<ol>")
        for info in front_matter:
            L.append(f'<li><a href="{escape_xml(info["file"])}">{escape_xml(info["title"])}</a></li>')
        L.append("</ol>")
        L.append("</li>")

    for part_data in parts.values():
        part_info = part_data["info"]
        L.append("<li>")
        L.append(f'<a href="{escape_xml(part_info["file"])}">{escape_xml(part_info["title"])}</a>')
        if part_data["modules"]:
            L.append("<ol>")
            for mod in part_data["modules"]:
                mod_info = mod["info"]
                L.append("<li>")
                L.append(f'<a href="{escape_xml(mod_info["file"])}">{escape_xml(mod_info["title"])}</a>')
                if mod["sections"]:
                    L.append("<ol>")
                    for sec in mod["sections"]:
                        L.append(f'<li><a href="{escape_xml(sec["file"])}">{escape_xml(sec["title"])}</a></li>')
                    L.append("</ol>")
                L.append("</li>")
            L.append("</ol>")
        L.append("</li>")

    if capstone:
        L.append("<li>")
        L.append(f'<a href="{escape_xml(capstone[0]["file"])}">Capstone</a>')
        if len(capstone) > 1:
            L.append("<ol>")
            for info in capstone[1:]:
                L.append(f'<li><a href="{escape_xml(info["file"])}">{escape_xml(info["title"])}</a></li>')
            L.append("</ol>")
        L.append("</li>")

    if appendix_root_info or appendices:
        L.append("<li>")
        link_target = appendix_root_info["file"] if appendix_root_info else appendices[0]["info"]["file"]
        L.append(f'<a href="{escape_xml(link_target)}">Appendices</a>')
        if appendices:
            L.append("<ol>")
            for apx in appendices:
                apx_info = apx["info"]
                L.append("<li>")
                L.append(f'<a href="{escape_xml(apx_info["file"])}">{escape_xml(apx_info["title"])}</a>')
                if apx["sections"]:
                    L.append("<ol>")
                    for sec in apx["sections"]:
                        L.append(f'<li><a href="{escape_xml(sec["file"])}">{escape_xml(sec["title"])}</a></li>')
                    L.append("</ol>")
                L.append("</li>")
            L.append("</ol>")
        L.append("</li>")

    L.append("</ol>")
    return "\n".join(L)


def _build_landmarks(spine_entries, chapter_map, items_by_id) -> str:
    """Build the EPUB 3 landmarks list - key entry points for 'Go To' menus."""
    lines: list[str] = []

    # 1. Cover
    lines.append('<li><a epub:type="cover" href="cover.xhtml">Cover</a></li>')
    # 2. TOC itself
    lines.append('<li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>')

    # Find by source path in spine
    def find_by_path(suffix: str):
        for entry in spine_entries:
            if entry["path"].endswith(suffix):
                info = chapter_map.get(entry["path"])
                if info:
                    return info
        return None

    # 3. Front matter (first front-matter chapter)
    fm = next((chapter_map.get(e["path"]) for e in spine_entries
               if e["kind"] == "front-matter" and e["path"] in chapter_map), None)
    if fm:
        lines.append(f'<li><a epub:type="frontmatter" href="{escape_xml(fm["file"])}">Front Matter</a></li>')

    # 4. Foreword
    fw = find_by_path("foreword.html")
    if fw:
        lines.append(f'<li><a epub:type="foreword" href="{escape_xml(fw["file"])}">Foreword</a></li>')

    # 5. Body matter (first part-index)
    body = next((chapter_map.get(e["path"]) for e in spine_entries
                 if e["kind"] == "part-index" and e["path"] in chapter_map), None)
    if body:
        lines.append(f'<li><a epub:type="bodymatter" href="{escape_xml(body["file"])}">Begin Reading (Part I)</a></li>')

    # Note: deliberately NOT adding per-part landmarks. EPUB 3.3 spec wants
    # landmarks sparse and canonical. Each part already has its own epub:type
    # would need to be unique, but bodymatter is reserved for "the body of the
    # work" as a whole - reusing it for each part causes duplicate-landmark
    # errors. Readers find parts via the main TOC nav above.

    # 7. Capstone
    cs = next((chapter_map.get(e["path"]) for e in spine_entries
               if e["kind"] == "capstone-index" and e["path"] in chapter_map), None)
    if cs:
        lines.append(f'<li><a epub:type="afterword" href="{escape_xml(cs["file"])}">Capstone</a></li>')

    # 8. Appendices entry point
    apx = next((chapter_map.get(e["path"]) for e in spine_entries
                if e["kind"] == "appendix-index" and e["path"] in chapter_map), None)
    if apx:
        lines.append(f'<li><a epub:type="backmatter" href="{escape_xml(apx["file"])}">Appendices</a></li>')

    return "\n".join(lines)


def build_toc(spine_entries, chapter_map, chapter_items):
    """
    Build a hierarchical TOC:
      Front Matter (section)
      Part I: ... (section)
        Chapter 0 (link or section if it has sections)
          Section 0.1 (link)
          ...
      Appendices (section)
        Appendix A (link)
      Capstone (link)
    """
    # Index chapter items by src_rel via uid match
    items_by_id = {ci.id: ci for ci in chapter_items}

    toc: list = []
    fm_section: list = []
    parts_section: list = []
    capstone_section: list = []
    appx_section: list = []

    # Group chapters by part / section
    by_part: dict[str, list] = {}
    by_module: dict[str, list] = {}
    part_titles: dict[str, str] = {}
    module_titles: dict[str, str] = {}

    for entry in spine_entries:
        src_rel = entry["path"]
        info = chapter_map.get(src_rel)
        if not info:
            continue
        ci = items_by_id.get(info["id"])
        if not ci:
            continue
        kind = entry["kind"]
        if kind == "front-matter":
            fm_section.append(ci)
        elif kind == "part-index":
            part = src_rel.split("/")[0]
            part_titles[part] = info["title"]
            by_part.setdefault(part, []).append(("part-index", ci, src_rel))
        elif kind == "module-index":
            parts = src_rel.split("/")
            part = parts[0]
            module = parts[1]
            module_titles[module] = info["title"]
            by_part.setdefault(part, []).append(("module-index", ci, src_rel))
            by_module.setdefault((part, module), [])
        elif kind == "section":
            parts = src_rel.split("/")
            part = parts[0]
            module = parts[1]
            by_module.setdefault((part, module), []).append(ci)
            # Don't add directly to by_part; we'll splice modules with their sections
        elif kind in ("appendix-index", "appendix"):
            appx_section.append(ci)
        elif kind == "appendix-section":
            appx_section.append(ci)
        elif kind in ("capstone-index", "capstone"):
            capstone_section.append(ci)

    # Build parts_section
    for part_name, items in by_part.items():
        ptitle = part_titles.get(part_name, part_name)
        # First item is the part-index
        part_chapters = []
        for kind, ci, src in items:
            if kind == "part-index":
                continue
            if kind == "module-index":
                module_name = src.split("/")[1]
                sections = by_module.get((part_name, module_name), [])
                if sections:
                    part_chapters.append((epub.Section(ci.title), [ci] + sections))
                else:
                    part_chapters.append(ci)
        # Use a Link/Section structure compatible with ebooklib's toc
        parts_section.append((epub.Section(ptitle, ci_for_section(items)), part_chapters))

    if fm_section:
        toc.append((epub.Section("Front Matter"), fm_section))
    toc.extend(parts_section)
    if capstone_section:
        toc.append((epub.Section("Capstone"), capstone_section))
    if appx_section:
        toc.append((epub.Section("Appendices"), appx_section))
    return toc


def ci_for_section(items) -> str | None:
    """Return the file_name of the part-index item if present, for the Section's href."""
    for kind, ci, _src in items:
        if kind == "part-index":
            return ci.file_name
    return None


def escape_xml(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))


def strip_tags(html: str) -> str:
    return BeautifulSoup(html, "lxml").get_text(separator=" ", strip=True)


# --------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build LLMBook EPUB for KDP")
    # Defaults tuned 2026-05-10 to "conservative reduction" per QUALITY_TOOLS.md:
    # 1280 px (covers Kindle Scribe 1200x1920) + Q78 JPEG (near-imperceptible
    # quality loss vs Q82, ~10 MB EPUB savings).
    p.add_argument("--max-image-side", type=int, default=1280,
                   help="Maximum dimension (px) for any bundled image (default 1280)")
    p.add_argument("--jpeg-quality", type=int, default=78,
                   help="JPEG quality for re-encoded images (default 78)")
    p.add_argument("--no-sample-pdf", action="store_true",
                   help="Skip regenerating the landing-page sample PDF")
    args = p.parse_args(argv)
    rc = build(max_side=args.max_image_side, jpeg_quality=args.jpeg_quality)
    if rc == 0 and not args.no_sample_pdf:
        import subprocess
        import sys as _sys
        sample_script = Path(__file__).resolve().parent / "build_sample_pdf.py"
        if sample_script.exists():
            print("\nRegenerating landing-page sample PDF from fresh EPUB...")
            try:
                subprocess.run(
                    [_sys.executable, str(sample_script)],
                    check=True,
                    cwd=str(Path(__file__).resolve().parents[2]),
                )
            except subprocess.CalledProcessError as e:
                print(f"  [WARN] sample-PDF regen returned code {e.returncode}; EPUB build still OK")
            except Exception as e:
                print(f"  [WARN] sample-PDF regen skipped ({e}); EPUB build still OK")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
