"""Rebuild `appendices/index.html` from book_structure.yaml.

Layout: same chapter-card grid as before, grouped by `group` field. Glossary
gets a special card (no Appendix letter, just "Glossary"). Front-matter
"Course Materials" links stay at bottom (not yaml-driven; preserved by
splicing them in).

Idempotent.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]


def _esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _group_slug(g: str) -> str:
    """Slugify a group name for HTML anchors (e.g., 'Framework Guides' -> 'framework-guides')."""
    s = g.lower()
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "&"):
            out.append("-")
    return "".join(out).strip("-").replace("--", "-")


def render_appendices_page(struct: dict) -> str:
    book = struct.get("book", {})
    title = _esc(book.get("title", "Book"))
    edition = _esc(book.get("edition", ""))
    if book.get("year"):
        edition = f"{edition}, {book['year']}" if edition else str(book["year"])

    # Group appendices by group field
    groups: dict[str, list[dict]] = {}
    order: list[str] = []
    for a in struct.get("appendices", []):
        g = a.get("group", "Other")
        if g not in groups:
            groups[g] = []
            order.append(g)
        groups[g].append(a)

    cards_html: list[str] = []
    for g in order:
        cards_html.append(f'<h2 id="group-{_group_slug(g)}">{_esc(g)}</h2>')
        for a in groups[g]:
            letter = a["letter"]
            t = _esc(a["title"])
            slug = a["slug"]
            cards_html.append(f'''<div class="chapter-card">
<div class="chapter-card-header">
<span class="mod-num">Appendix {letter}</span> {t}
        </div>
<div class="chapter-card-body">
<p>{_esc(a.get("subtitle", ""))}</p>
<p><a href="appendix-{letter.lower()}-{slug}/index.html">Read Appendix {letter} &rarr;</a></p>
</div>
</div>''')

    # Glossary card
    gloss = struct.get("glossary")
    if gloss:
        cards_html.append(f'''<h2>Glossary</h2>
<div class="chapter-card">
<div class="chapter-card-header">
<span class="mod-num">Glossary</span> Definitions of Key Terms
        </div>
<div class="chapter-card-body">
<p>Definitions of key terms, acronyms, and concepts used throughout the book. Not a lettered appendix; internally numbered F.1-F.5 for legacy reasons.</p>
<p><a href="glossary/index.html">Read the Glossary &rarr;</a></p>
</div>
</div>''')

    cards = "\n".join(cards_html)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Appendices: reference materials, framework guides, infrastructure tooling, and pedagogical kit for {title}." name="description"/>
<title>Appendices | {title}</title>
<link href="../styles/book.css" rel="stylesheet"/>
<script defer src="../scripts/book.js"></script>
<link href="../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer src="../pagefind/pagefind-ui.js"></script>
</head>
<body>
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../index.html">{title}</a>
<a class="toc-link" href="../toc.html" title="Table of Contents"><span class="toc-icon">☰</span> Contents</a>
</nav>
<div class="header-search"><div id="search"></div></div>
<h1>Appendices</h1>
<p class="chapter-subtitle">Reference materials, framework guides, and infrastructure tooling to support your journey through the book.</p>
</header>
<main class="content">
<blockquote class="epigraph">
<p>The best reference material is the kind you keep reaching for long after you have finished the book.</p>
<cite>A Pragmatic Educator</cite>
</blockquote>
<div class="part-overview">
<h2>Part Overview</h2>
<p>The appendices provide reference material organized into five groups. <strong>Foundations</strong> covers the mathematical and ML prerequisites. <strong>Framework Guides</strong> offers hands-on introductions to HuggingFace, LangChain, orchestration frameworks, agent frameworks, and the problem-solution key for navigating the book by task. <strong>Research and Development Infrastructure</strong> covers Python tooling, environment setup, version control, and experiment tracking. <strong>Production Infrastructure</strong> covers inference serving, distributed ML, and Docker. <strong>For Instructors</strong> contains course syllabi, reading pathways, intermediate projects, the capstone project, and named production war stories for classroom discussion.</p>
</div>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>These appendices serve two purposes: they provide prerequisite refreshers you can consult before diving into specific chapters, and they offer practical framework guides you will return to when building real projects. Think of them as the book's toolbox.</p>
</div>
{cards}

<nav class="chapter-nav">
<a class="prev" href="../index.html"><span class="nav-label">Previous</span><span class="nav-num">Cover</span><span class="nav-title">{title}</span></a>
<a class="up" href="../toc.html"><span class="nav-label">Up</span><span class="nav-num">Book Index</span><span class="nav-title">Table of Contents</span></a>
<a class="next" href="../front-matter/index.html"><span class="nav-label">Next</span><span class="nav-num">Front Matter</span><span class="nav-title">Welcome, Authors, How to Read</span></a>
</nav>

<footer><p>{edition} &middot; <a href="../toc.html">Contents</a></p></footer>
</main>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yaml", type=Path,
                    default=ROOT / "book_structure.yaml")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "appendices" / "index.html")
    args = ap.parse_args()

    struct = yaml.safe_load(args.yaml.read_text(encoding="utf-8"))
    html = render_appendices_page(struct)
    args.out.write_text(html, encoding="utf-8")
    print(f"Wrote {args.out} ({len(html)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
