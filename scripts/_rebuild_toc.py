"""Rebuild `toc.html` from `book_structure.yaml`.

Output: a single beautiful two-level ToC (Part > Chapter) replacing the
previous dual `toc-short` / `toc-detailed` modes.

Layout per part:

    <section class="toc-part" id="part-N">
      <header class="toc-part-header">
        <div class="toc-part-num">Part I</div>
        <h2 class="toc-part-title">Foundations</h2>
        <p class="toc-part-subtitle">...subtitle...</p>
      </header>
      <ol class="toc-chapter-list">
        <li class="toc-chapter">
          <a href="...">
            <span class="toc-chapter-num">Chapter 0</span>
            <span class="toc-chapter-title">ML and PyTorch Foundations</span>
            <span class="toc-chapter-subtitle">...</span>
          </a>
        </li>
        ...
      </ol>
    </section>

Appendices and Glossary use the same shape, swapping "Part" for "Appendices"
and "Chapter N" for "Appendix X".

Reads exactly one source: `book_structure.yaml` at book root. Any drift between
the yaml and the rendered ToC is the yaml author's responsibility.

Idempotent.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]


def render_part(part: dict) -> str:
    """Render one part block."""
    num = part["num"]
    roman = part.get("roman", str(num))
    title = _esc(part["title"])
    subtitle = _esc(part.get("subtitle", ""))
    slug = part["slug"]

    chap_count = len(part.get("chapters", []))
    sec_count = sum(len(c.get("sections", [])) for c in part.get("chapters", []))

    out: list[str] = []
    out.append(f'<section class="toc-part" id="part-{num}">')
    out.append('<header class="toc-part-header">')
    out.append(f'<div class="toc-part-num">Part {roman}<span class="toc-part-count">{chap_count} chapter{"s" if chap_count != 1 else ""} · {sec_count} section{"s" if sec_count != 1 else ""}</span></div>')
    out.append(f'<h2 class="toc-part-title"><a href="part-{num}-{slug}/index.html">{title}</a></h2>')
    if subtitle:
        out.append(f'<p class="toc-part-subtitle">{subtitle}</p>')
    out.append('</header>')

    out.append('<ol class="toc-chapter-list">')
    for chap in part.get("chapters", []):
        out.append(_render_chapter(part, chap))
    out.append('</ol>')
    out.append('</section>')
    return "\n".join(out)


def _render_chapter(part: dict, chap: dict) -> str:
    cnum = chap["num"]
    cslug = chap["slug"]
    ctitle = _esc(chap["title"])
    csubtitle = _esc(chap.get("subtitle", ""))
    pnum = part["num"]
    pslug = part["slug"]
    href = f"part-{pnum}-{pslug}/module-{cnum:02d}-{cslug}/index.html"

    out: list[str] = []
    out.append('<li class="toc-chapter">')
    out.append(f'<a href="{href}">')
    # Number-only chip instead of "Chapter N" prefix.
    out.append(f'<span class="toc-chapter-num" aria-label="Chapter {cnum}">{cnum}</span>')
    out.append(f'<span class="toc-chapter-title">{ctitle}</span>')
    if csubtitle:
        out.append(f'<span class="toc-chapter-subtitle">{csubtitle}</span>')
    out.append('</a>')
    out.append('</li>')
    return "\n".join(out)


def render_appendices(appendices: list[dict], glossary: dict | None) -> str:
    """Render the Appendices block. Glossary is rendered as a special card
    inside the same section."""
    out: list[str] = []
    out.append('<section class="toc-part toc-appendices" id="appendices">')
    out.append('<header class="toc-part-header">')
    out.append('<div class="toc-part-num">Appendices</div>')
    out.append('<h2 class="toc-part-title"><a href="appendices/index.html">Reference, Frameworks, MLOps &amp; Pedagogy</a></h2>')
    out.append('</header>')
    out.append('<ol class="toc-chapter-list">')

    # Group appendices by group field (Foundations / FrameworkGuides / Infrastructure / PedagogyKit)
    groups: dict[str, list[dict]] = {}
    order: list[str] = []
    for a in appendices:
        g = a.get("group", "Other")
        if g not in groups:
            groups[g] = []
            order.append(g)
        groups[g].append(a)

    for g in order:
        if g != "Other":
            out.append(f'<li class="toc-group-divider">{_esc(g)}</li>')
        for app in groups[g]:
            letter = app["letter"]
            title = _esc(app["title"])
            subtitle = _esc(app.get("subtitle", ""))
            href = f"appendices/appendix-{letter.lower()}-{app['slug']}/index.html"
            out.append('<li class="toc-chapter toc-appendix">')
            out.append(f'<a href="{href}">')
            out.append(f'<span class="toc-chapter-num" aria-label="Appendix {letter}">{letter}</span>')
            out.append(f'<span class="toc-chapter-title">{title}</span>')
            if subtitle:
                out.append(f'<span class="toc-chapter-subtitle">{subtitle}</span>')
            out.append('</a>')
            out.append('</li>')

    # Glossary card (special, no letter)
    if glossary:
        out.append('<li class="toc-chapter toc-glossary">')
        out.append('<a href="appendices/glossary/index.html">')
        out.append('<span class="toc-chapter-num">Glossary</span>')
        out.append(f'<span class="toc-chapter-title">{_esc(glossary["title"])}</span>')
        if glossary.get("subtitle"):
            out.append(f'<span class="toc-chapter-subtitle">{_esc(glossary["subtitle"])}</span>')
        out.append('</a>')
        out.append('</li>')

    out.append('</ol>')
    out.append('</section>')
    return "\n".join(out)


def render_front_matter(items: list[dict]) -> str:
    if not items:
        return ""
    out: list[str] = []
    out.append('<section class="toc-part toc-front-matter" id="front-matter">')
    out.append('<header class="toc-part-header">')
    out.append('<div class="toc-part-num">Front Matter</div>')
    out.append('<h2 class="toc-part-title"><a href="front-matter/index.html">Welcome, Authors, How to Read</a></h2>')
    out.append('</header>')
    out.append('<ol class="toc-chapter-list">')
    for item in items:
        href = f"front-matter/{item['slug']}.html"
        title = _esc(item["title"])
        out.append('<li class="toc-chapter">')
        out.append(f'<a href="{href}">')
        out.append(f'<span class="toc-chapter-title">{title}</span>')
        out.append('</a>')
        out.append('</li>')
    out.append('</ol>')
    out.append('</section>')
    return "\n".join(out)


def _esc(s: str) -> str:
    """Minimal HTML-escape, preserves ampersand entities already present."""
    s = (s or "").replace("&", "&amp;").replace("&amp;amp;", "&amp;")
    s = s.replace("<", "&lt;").replace(">", "&gt;")
    return s


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Two-level table of contents for {title}." name="description"/>
<title>Contents | {title}</title>
<link href="styles/book.css" rel="stylesheet"/>
<link href="pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer src="pagefind/pagefind-ui.js"></script>
<script defer src="scripts/book.js"></script>
</head>
<body>
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="index.html">{title}</a>
<a class="toc-link" href="toc.html" aria-current="page" title="Table of Contents"><span class="toc-icon">☰</span> Contents</a>
</nav>
<div class="header-search"><div id="search"></div></div>
<h1>Table of Contents</h1>
<p class="chapter-subtitle">{edition}</p>
</header>
<main class="content toc-main">
{front_matter}
{parts}
{appendices}
</main>
<footer><p>{edition} &middot; <a href="index.html">Cover</a></p></footer>
<script>
window.addEventListener("DOMContentLoaded", function() {{
  if (window.PagefindUI) {{
    new PagefindUI({{
      element: "#search",
      showSubResults: true,
      showImages: false,
      resetStyles: false,
      pageSize: 8,
      autofocus: false,
      translations: {{ placeholder: "Search the book…" }},
    }});
  }}
}});
</script>
</body>
</html>
"""


def build_toc(struct: dict) -> str:
    book = struct.get("book", {})
    title = _esc(book.get("title", "Book"))
    edition = _esc(book.get("edition", ""))
    if book.get("year"):
        edition = f"{edition}, {book['year']}" if edition else str(book["year"])

    parts_html = "\n\n".join(render_part(p) for p in struct.get("parts", []))
    appendices_html = render_appendices(struct.get("appendices", []),
                                          struct.get("glossary"))
    front_matter_html = render_front_matter(struct.get("front_matter", []))

    return HTML_TEMPLATE.format(
        title=title,
        edition=edition,
        front_matter=front_matter_html,
        parts=parts_html,
        appendices=appendices_html,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yaml", type=Path, default=ROOT / "book_structure.yaml",
                    help="Path to book_structure.yaml")
    ap.add_argument("--out", type=Path, default=ROOT / "toc.html",
                    help="Output toc.html path")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.yaml.exists():
        print(f"ERROR: {args.yaml} not found.", file=sys.stderr)
        return 1

    struct = yaml.safe_load(args.yaml.read_text(encoding="utf-8"))
    html = build_toc(struct)

    if args.dry_run:
        print(html[:2000])
        print(f"\n...({len(html)} chars total)\n")
        print("(dry run; nothing written)")
        return 0

    args.out.write_text(html, encoding="utf-8")
    print(f"Wrote {args.out} ({len(html)} chars).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
