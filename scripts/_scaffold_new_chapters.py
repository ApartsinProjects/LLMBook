"""Scaffold directory + index.html for every chapter in book_structure.target.yaml
that's marked `_new: true`.

For each new chapter, writes:

  <book_root>/part-<N>-<part-slug>/module-<NN>-<chapter-slug>/
    index.html
    images/    (empty)
    section-X.Y.html (one per section in target yaml, also stub)

The `index.html` is a complete page using the LLMBook template:
- chapter-header with breadcrumb + h1 + subtitle
- main with epigraph (TODO author), big-picture callout (TODO),
  section overview list, whats-next placeholder, chapter-nav placeholder.

The `section-X.Y.html` files are similar minimal stubs with an h1 and a
TODO author marker. Author fills in real content in Phase E.

Idempotent: skips chapters whose target directory already exists.
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


ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII",
         8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}


CHAPTER_TEMPLATE = """<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="{chapter_subtitle}" name="description"/>
<title>Chapter {chapter_num}: {chapter_title} | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
<script defer="" src="../../scripts/book.js"></script>
</head>
<body>
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">☰</span> Contents</a>
</nav>
<div class="header-search"><div id="search"></div></div>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part {part_roman}: {part_title}</a><span class="bc-sep">›</span><span class="bc-current">Chapter {chapter_num}</span></div>
<h1>{chapter_title}</h1>
<p class="chapter-subtitle">{chapter_subtitle}</p>
</header>
<main class="content"><span class="pagefind-meta-injected" data-pagefind-meta="part:Part {part_roman}: {part_title}" hidden=""></span><span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {chapter_num}: {chapter_title}" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>TODO author this big-picture callout: why this chapter matters and how it connects to the broader story of {part_title}.</p>
</div>

<h2>Sections in This Chapter</h2>
<div class="section-card-list">
{section_cards}
</div>

<div class="whats-next">
<h2>What Comes Next</h2>
<p>TODO author this. Outline where this chapter sits in the narrative arc and what the next chapter builds on.</p>
</div>

<nav class="chapter-nav">
<a class="prev" href="../index.html"><span class="nav-label">Previous</span><span class="nav-num">Part {part_roman}</span><span class="nav-title">{part_title}</span></a>
<a class="up" href="../index.html"><span class="nav-label">In Part</span><span class="nav-num">Part {part_roman}</span><span class="nav-title">{part_title}</span></a>
<a class="next" href="../index.html"><span class="nav-label">Next</span><span class="nav-num">Part {part_roman}</span><span class="nav-title">{part_title}</span></a>
</nav>

<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</main>
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


SECTION_TEMPLATE = """<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Section {section_num}: {section_title}. A chapter from the Building Conversational AI textbook." name="description"/>
<title>Section {section_num}: {section_title}</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<link href="../../styles/pygments.css" rel="stylesheet"/>
<script defer="" src="../../scripts/book.js"></script>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
</head>
<body>
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">☰</span> Contents</a>
</nav>
<div class="header-search"><div id="search"></div></div>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part {part_roman}: {part_title}</a><span class="bc-sep">›</span><a href="index.html">Chapter {chapter_num}: {chapter_title}</a></div>
<h1>{section_title}</h1>
<div class="page-current">Section {section_num}</div>
</header>
<main class="content"><span class="pagefind-meta-injected" data-pagefind-meta="part:Part {part_roman}: {part_title}" hidden=""></span><span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {chapter_num}: {chapter_title}" hidden=""></span>

<p>TODO author this section. This is a scaffold; replace with chapter content authored in Phase E.</p>

<nav class="chapter-nav">
<a class="prev" href="index.html"><span class="nav-label">Previous</span><span class="nav-num">Chapter {chapter_num}</span><span class="nav-title">{chapter_title}</span></a>
<a class="up" href="index.html"><span class="nav-label">In Chapter</span><span class="nav-num">Chapter {chapter_num}</span><span class="nav-title">{chapter_title}</span></a>
<a class="next" href="index.html"><span class="nav-label">Next</span><span class="nav-num">Chapter {chapter_num}</span><span class="nav-title">{chapter_title}</span></a>
</nav>

<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</main>
</body>
</html>
"""


def _esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def scaffold_chapter(part: dict, chap: dict, dry_run: bool, force: bool = False) -> int:
    """Create the chapter dir + index.html + section stubs."""
    pnum = part["num"]
    pslug = part["slug"]
    proman = part.get("roman") or ROMAN.get(pnum, str(pnum))
    ptitle = _esc(part["title"])
    cnum = chap["num"]
    cslug = chap["slug"]
    ctitle = _esc(chap["title"])
    csubtitle = _esc(chap.get("subtitle", ""))

    chap_dir = ROOT / f"part-{pnum}-{pslug}" / f"module-{cnum:02d}-{cslug}"
    if chap_dir.exists() and not force:
        return 0  # already exists; idempotent skip

    if dry_run:
        print(f"  WOULD CREATE {chap_dir.relative_to(ROOT)} (+ {len(chap.get('sections', []))} sections)")
        return 1

    chap_dir.mkdir(parents=True, exist_ok=True)
    (chap_dir / "images").mkdir(exist_ok=True)

    # Build section cards list for the index.html
    section_cards = []
    for s in chap.get("sections", []):
        snum = s["num"]
        sslug = s.get("slug", f"section-{snum}")
        stitle = _esc(s["title"])
        href = f"{sslug}.html"
        section_cards.append(
            f'<a class="section-card" href="{href}">'
            f'<span class="section-num">Section {snum}</span>'
            f'<span class="section-title">{stitle}</span>'
            f'</a>'
        )

    index_html = CHAPTER_TEMPLATE.format(
        part_roman=proman, part_title=ptitle,
        chapter_num=cnum, chapter_title=ctitle, chapter_subtitle=csubtitle,
        section_cards="\n".join(section_cards) or "<p><em>Sections forthcoming.</em></p>",
    )
    (chap_dir / "index.html").write_text(index_html, encoding="utf-8")

    # Section stubs
    for s in chap.get("sections", []):
        snum = s["num"]
        sslug = s.get("slug", f"section-{snum}")
        stitle = _esc(s["title"])
        sec_html = SECTION_TEMPLATE.format(
            part_roman=proman, part_title=ptitle,
            chapter_num=cnum, chapter_title=ctitle,
            section_num=snum, section_title=stitle,
        )
        (chap_dir / f"{sslug}.html").write_text(sec_html, encoding="utf-8")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path,
                    default=ROOT / "book_structure.target.yaml")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite existing scaffolds")
    args = ap.parse_args()

    target = yaml.safe_load(args.target.read_text(encoding="utf-8"))
    created = 0
    for p in target["parts"]:
        for c in p.get("chapters", []):
            if c.get("_new"):
                created += scaffold_chapter(p, c, args.dry_run, args.force)
    print(f"\n{'WOULD CREATE' if args.dry_run else 'CREATED'}: {created} new chapter scaffolds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
