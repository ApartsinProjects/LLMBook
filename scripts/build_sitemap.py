"""Generate sitemap.xml + robots.txt (+ CNAME) for the published book.

Walks every reader-facing HTML page (skips templates, scripts, agents, KDP,
archive, vendor, pagefind), emits clean URLs (directory form for index pages),
and a robots.txt that allows all and points at the sitemap. For a custom domain
it also writes a CNAME file (bare host) for GitHub Pages.

Usage:
  py -3 scripts/build_sitemap.py https://book.example.com
  py -3 scripts/build_sitemap.py https://apartsinprojects.github.io/LLMBook
"""
from __future__ import annotations
import datetime, sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"_archive", "node_modules", ".git", "vendor", ".claude", "__pycache__",
        ".book-update", ".tools", "KDP", "pagefind", "templates", "temp_epub",
        "agents", "scripts", "docs"}


def loc_for(rel: str, base: str) -> str:
    if rel == "index.html":
        return base + "/"
    if rel.endswith("/index.html"):
        return base + "/" + rel[: -len("index.html")]  # directory form
    return base + "/" + rel


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    base = sys.argv[1].rstrip("/")
    pages = []
    for p in ROOT.rglob("*.html"):
        if any(s in p.parts for s in SKIP):
            continue
        rel = p.relative_to(ROOT).as_posix()
        lastmod = datetime.date.fromtimestamp(p.stat().st_mtime).isoformat()
        if rel == "index.html":
            pr = "1.0"
        elif p.name == "index.html":
            pr = "0.8"
        else:
            pr = "0.6"
        pages.append((loc_for(rel, base), lastmod, pr))
    pages.sort()

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, pr in pages:
        loc = loc.replace("&", "&amp;")
        out.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod>"
                   f"<changefreq>monthly</changefreq><priority>{pr}</priority></url>")
    out.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(out), encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")

    host = urlsplit(base).netloc
    is_gh_pages = host.endswith("github.io")
    if host and not is_gh_pages:
        (ROOT / "CNAME").write_text(host + "\n", encoding="utf-8")

    print(f"sitemap.xml: {len(pages)} URLs (base {base})")
    print("robots.txt written")
    if host and not is_gh_pages:
        print(f"CNAME written: {host}")
    else:
        print("CNAME skipped (github.io project URL)")


if __name__ == "__main__":
    main()
