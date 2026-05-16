"""Header style consistency audit for LLMBook. Read-only.
Reads all chapter and appendix HTML files, checks header structure against
reference standard, writes a structured Markdown report.
"""
import os
import re
import sys
from collections import defaultdict

ROOT = r"E:\Projects\BookBlogsHome\LLMBook"
OUT = os.path.join(ROOT, "header-style-audit.md")

PART_ROOTS = [
    "part-1-foundations",
    "part-2-understanding-llms",
    "part-3-working-with-llms",
    "part-4-training-adapting",
    "part-5-retrieval-conversation",
    "part-6-agentic-ai",
    "part-7-multimodal-generation",
    "part-8-evaluation-production",
    "part-9-safety-security-ethics",
    "part-10-idea-to-product",
    "part-11-applications-across-industries",
    "part-12-frontiers",
]
APPENDIX_ROOT = "appendices"
FRONT_ROOT = "front-matter"
SKIP_DIRS = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
             "source_fix_backups", "pagefind", "templates", ".claude", "vendor"}


def find_html_files():
    files = []
    for r in PART_ROOTS + [APPENDIX_ROOT, FRONT_ROOT]:
        d = os.path.join(ROOT, r)
        if not os.path.isdir(d):
            continue
        for dp, dns, fns in os.walk(d):
            dns[:] = [x for x in dns if x not in SKIP_DIRS]
            for f in fns:
                if f.endswith(".html"):
                    files.append(os.path.join(dp, f))
    return files


def classify(path):
    """Return (group, kind) tuple.
    group: 'part-N', 'appendix-X', 'front-matter'
    kind: 'chapter-index', 'section', 'appendix-index', 'appendix-section',
          'part-index', 'front', 'other'
    """
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    fn = os.path.basename(path)
    if rel.startswith("front-matter/"):
        return ("front-matter", "front")
    if rel.startswith("appendices/"):
        parts = rel.split("/")
        if len(parts) == 2:
            # appendices/index.html (the appendix list)
            return ("appendices-list", "appendix-list")
        # appendices/appendix-X-.../...
        app_dir = parts[1]
        if fn == "index.html":
            return (app_dir, "appendix-index")
        if fn.startswith("section-"):
            return (app_dir, "appendix-section")
        return (app_dir, "other")
    # part-N
    parts = rel.split("/")
    part = parts[0]
    if len(parts) == 2 and fn == "index.html":
        return (part, "part-index")
    if len(parts) >= 3:
        module = parts[1]
        if fn == "index.html":
            return (f"{part}/{module}", "chapter-index")
        if fn.startswith("section-"):
            return (f"{part}/{module}", "section")
        return (f"{part}/{module}", "other")
    return (part, "other")


# Pre-compile some regexes.
RE_TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
RE_CHAPTER_HEADER = re.compile(r'<header[^>]*class="[^"]*chapter-header[^"]*"[^>]*>(.*?)</header>', re.S | re.I)
RE_HEADER_NAV = re.compile(r'<nav[^>]*class="[^"]*header-nav[^"]*"', re.I)
RE_BOOK_TITLE_LINK = re.compile(r'<a[^>]*class="[^"]*book-title-link[^"]*"', re.I)
RE_TOC_LINK = re.compile(r'<a[^>]*class="[^"]*toc-link[^"]*"', re.I)
RE_HEADER_SEARCH = re.compile(r'<div[^>]*class="[^"]*header-search[^"]*"', re.I)
RE_BOTTOM_SEARCH = re.compile(r'<div[^>]*class="[^"]*bottom-search[^"]*"', re.I)
RE_BREADCRUMB = re.compile(r'<div[^>]*class="[^"]*page-breadcrumb[^"]*"[^>]*>(.*?)</div>', re.S | re.I)
RE_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)
RE_SUBTITLE = re.compile(r'<p[^>]*class="[^"]*chapter-subtitle[^"]*"[^>]*>(.*?)</p>', re.S | re.I)
RE_PAGE_CURRENT = re.compile(r'<div[^>]*class="[^"]*page-current[^"]*"[^>]*>(.*?)</div>', re.S | re.I)
RE_MAIN = re.compile(r'<main[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</main>', re.S | re.I)
RE_PAGEFIND_PART = re.compile(r'data-pagefind-meta="part:([^"]*)"', re.I)
RE_PAGEFIND_CHAPTER = re.compile(
    r'<span[^>]*class="[^"]*pagefind-meta-injected[^"]*"[^>]*data-pagefind-meta="chapter:([^"]*)"', re.I)
RE_CHAPTER_NAV = re.compile(r'<nav[^>]*class="[^"]*chapter-nav[^"]*"', re.I)
RE_ILLUSTRATION = re.compile(r'<figure[^>]*class="[^"]*illustration[^"]*"', re.I)
RE_EPIGRAPH = re.compile(r'<blockquote[^>]*class="[^"]*epigraph[^"]*"', re.I)
RE_BIG_PICTURE = re.compile(r'<div[^>]*class="[^"]*big-picture[^"]*"', re.I)

# Path depth helpers — book-title-link href depth.
DEPTH_TWO_PREFIXES = ("../../",)
DEPTH_ONE_PREFIXES = ("../",)


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def strip_tags(s):
    return collapse(re.sub(r"<[^>]+>", "", s))


def expected_href_depth(path):
    """Return how many '../' segments the page needs to reach root."""
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    depth = rel.count("/")
    return depth


def audit_file(path):
    """Return dict with detected issues for this file."""
    issues = []
    info = {}
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    group, kind = classify(path)
    info["rel"] = rel
    info["group"] = group
    info["kind"] = kind
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        return {"rel": rel, "group": group, "kind": kind, "issues": [("READ_ERROR", str(e))]}

    # Title
    tm = RE_TITLE.search(html)
    title = collapse(tm.group(1)) if tm else ""
    info["title"] = title

    # Header block
    hm = RE_CHAPTER_HEADER.search(html)
    if not hm:
        issues.append(("MISSING_CHAPTER_HEADER", "no <header class='chapter-header'> found"))
        info["issues"] = issues
        return info
    header = hm.group(1)

    has_header_nav = bool(RE_HEADER_NAV.search(header))
    has_book_link = bool(RE_BOOK_TITLE_LINK.search(header))
    has_toc_link = bool(RE_TOC_LINK.search(header))
    has_header_search = bool(RE_HEADER_SEARCH.search(header))
    has_bottom_search = bool(RE_BOTTOM_SEARCH.search(header))
    bm = RE_BREADCRUMB.search(header)
    has_breadcrumb = bm is not None
    breadcrumb_text = strip_tags(bm.group(1)) if bm else ""
    info["breadcrumb"] = breadcrumb_text

    h1m = RE_H1.search(header)
    if h1m is None:
        h1m = RE_H1.search(html)
    h1_text = strip_tags(h1m.group(1)) if h1m else ""
    info["h1"] = h1_text

    sm = RE_SUBTITLE.search(header)
    subtitle_text = strip_tags(sm.group(1)) if sm else ""
    info["subtitle"] = subtitle_text

    pcm = RE_PAGE_CURRENT.search(header)
    page_current = strip_tags(pcm.group(1)) if pcm else ""
    info["page_current"] = page_current

    # Multiple h1
    h1_all = RE_H1.findall(html)
    if len(h1_all) > 1:
        issues.append(("MULTIPLE_H1", f"{len(h1_all)} <h1> elements"))

    # Header pieces
    if not has_header_nav:
        issues.append(("HEADER_MISSING_NAV", "no <nav class='header-nav'>"))
    if not has_book_link:
        issues.append(("HEADER_MISSING_BOOK_LINK", "no <a class='book-title-link'> in header"))
    if not has_toc_link:
        issues.append(("HEADER_MISSING_TOC_LINK", "no toc-link"))
    if not has_header_search and has_bottom_search:
        issues.append(("HEADER_BOTTOM_SEARCH", "uses bottom-search class instead of header-search"))
    elif not has_header_search:
        issues.append(("HEADER_MISSING_SEARCH", "no header-search div"))
    if not has_breadcrumb:
        issues.append(("MISSING_BREADCRUMB", "no <div class='page-breadcrumb'>"))

    # Book title link href depth check
    blm = re.search(r'<a[^>]*class="[^"]*book-title-link[^"]*"[^>]*href="([^"]+)"', header)
    if blm:
        href = blm.group(1)
        expected = "../" * expected_href_depth(path)
        if not expected:
            expected = ""
        # For files in root, the link would be 'index.html'.
        if expected_href_depth(path) == 0:
            if href not in ("index.html", "./index.html"):
                issues.append(("BOOK_LINK_HREF", f"expected 'index.html', got '{href}'"))
        else:
            expected_full = expected + "index.html"
            if href != expected_full:
                issues.append(("BOOK_LINK_HREF",
                              f"expected '{expected_full}' for depth {expected_href_depth(path)}, got '{href}'"))

    # Title format
    expected_title_suffix = "| Building Conversational AI"
    if title and expected_title_suffix not in title:
        issues.append(("TITLE_MISSING_SUFFIX", f"<title>='{title[:80]}'"))

    if kind == "chapter-index":
        # Should be "Chapter N: Title | Building Conversational AI..."
        m = re.match(r"Chapter\s+\d+\w*:", title)
        if not m and "Chapter" not in title:
            issues.append(("TITLE_WRONG_FORMAT", f"chapter index title missing 'Chapter N:' prefix: '{title[:80]}'"))
    elif kind == "section":
        m = re.match(r"Section\s+\d+\.\d+\w*:", title)
        if not m:
            issues.append(("TITLE_WRONG_FORMAT", f"section title missing 'Section N.M:' prefix: '{title[:80]}'"))
    elif kind == "appendix-index":
        m = re.match(r"Appendix\s+[A-Z]:", title)
        if not m:
            issues.append(("TITLE_WRONG_FORMAT", f"appendix index title missing 'Appendix X:' prefix: '{title[:80]}'"))
    elif kind == "appendix-section":
        m = re.match(r"Section\s+[A-Z]\.\d+:", title)
        if not m:
            issues.append(("TITLE_WRONG_FORMAT", f"appendix section title missing 'Section X.M:' prefix: '{title[:80]}'"))

    # Breadcrumb pattern
    if has_breadcrumb:
        # chapter-index: should end with "Chapter N" or "Appendix X" (no colon)
        # section: should have "Chapter N: Title › Section N.M" or simply more parts
        if kind == "chapter-index":
            if not re.search(r"›\s*Chapter\s+\d+\w*\s*$", breadcrumb_text) and not re.search(r">\s*Chapter\s+\d+", breadcrumb_text):
                # be flexible: just check there's no colon following chapter ref
                if re.search(r"Chapter\s+\d+:", breadcrumb_text) and not re.search(r"›\s*Section", breadcrumb_text):
                    issues.append(("BREADCRUMB_HAS_COLON", f"chapter index breadcrumb has 'Chapter N:' (should be no colon): '{breadcrumb_text[:100]}'"))
        elif kind == "section":
            if "Chapter" in breadcrumb_text and ":" not in breadcrumb_text:
                issues.append(("BREADCRUMB_MISSING_COLON", f"section breadcrumb missing 'Chapter N: Title': '{breadcrumb_text[:100]}'"))
        elif kind == "appendix-index":
            if re.search(r"Appendix\s+[A-Z]:", breadcrumb_text):
                issues.append(("BREADCRUMB_HAS_COLON", f"appendix index breadcrumb has 'Appendix X:' (should be no colon): '{breadcrumb_text[:100]}'"))
        elif kind == "appendix-section":
            if "Appendix" in breadcrumb_text and ":" not in breadcrumb_text:
                issues.append(("BREADCRUMB_MISSING_COLON", f"appendix section breadcrumb missing 'Appendix X: Title': '{breadcrumb_text[:100]}'"))

    # H1 format
    if kind == "chapter-index":
        # h1 should NOT start with "Chapter N:"
        if re.match(r"Chapter\s+\d+", h1_text):
            issues.append(("H1_HAS_CHAPTER_PREFIX", f"chapter index h1 starts with 'Chapter N': '{h1_text[:80]}'"))
    elif kind == "appendix-index":
        if re.match(r"Appendix\s+[A-Z]", h1_text):
            issues.append(("H1_HAS_APPENDIX_PREFIX", f"appendix index h1 starts with 'Appendix X': '{h1_text[:80]}'"))
    elif kind == "section":
        # h1 may or may not start with "N.M"; flag if no page-current
        if not page_current:
            issues.append(("MISSING_PAGE_CURRENT", "section page missing <div class='page-current'>"))
    elif kind == "appendix-section":
        if not page_current:
            issues.append(("MISSING_PAGE_CURRENT", "appendix section page missing <div class='page-current'>"))

    # Subtitle presence
    if kind == "chapter-index" and not subtitle_text:
        issues.append(("MISSING_SUBTITLE", "chapter index missing <p class='chapter-subtitle'>"))
    elif kind == "appendix-index" and not subtitle_text:
        issues.append(("MISSING_SUBTITLE", "appendix index missing <p class='chapter-subtitle'>"))
    elif kind == "section" and subtitle_text:
        issues.append(("UNEXPECTED_SUBTITLE", f"section page has chapter-subtitle: '{subtitle_text[:80]}'"))
    elif kind == "appendix-section" and subtitle_text:
        issues.append(("UNEXPECTED_SUBTITLE", f"appendix section has chapter-subtitle: '{subtitle_text[:80]}'"))

    # main first child
    mm = RE_MAIN.search(html)
    if mm:
        main_content = mm.group(1)
        # Strip pagefind injected spans then leading whitespace.
        main_after_meta = re.sub(r'<span[^>]*class="[^"]*pagefind-meta-injected[^"]*"[^>]*></span>',
                                 "", main_content)
        main_after_meta = main_after_meta.lstrip()
        first_tag_match = re.match(r"<(\w+)([^>]*)>", main_after_meta)
        first_tag = first_tag_match.group(1) if first_tag_match else ""
        first_attrs = first_tag_match.group(2) if first_tag_match else ""
        info["main_first_tag"] = f"<{first_tag}{first_attrs}>"
        if kind == "chapter-index":
            # Should start with figure (chapter-opener), epigraph, or big-picture callout
            ok = (
                ("illustration" in first_attrs and "chapter-opener" in first_attrs and first_tag == "figure") or
                (first_tag == "blockquote" and "epigraph" in first_attrs) or
                (first_tag == "div" and "big-picture" in first_attrs) or
                (first_tag == "figure" and "illustration" in first_attrs)
            )
            if not ok:
                issues.append(("MAIN_OPENS_WITH_OTHER",
                              f"<main> opens with <{first_tag} {first_attrs.strip()[:60]}> (expected figure.illustration, blockquote.epigraph, or div.big-picture)"))
        elif kind == "appendix-index":
            ok = (
                (first_tag == "figure" and "illustration" in first_attrs) or
                (first_tag == "blockquote" and "epigraph" in first_attrs) or
                (first_tag == "div" and "big-picture" in first_attrs)
            )
            if not ok:
                issues.append(("MAIN_OPENS_WITH_OTHER",
                              f"<main> opens with <{first_tag} {first_attrs.strip()[:60]}>"))

    # Chapter-nav at bottom
    if kind in ("chapter-index", "section", "appendix-index", "appendix-section"):
        if not RE_CHAPTER_NAV.search(html):
            issues.append(("MISSING_CHAPTER_NAV", "no <nav class='chapter-nav'> at bottom"))

    # Pagefind meta injection
    part_meta = RE_PAGEFIND_PART.findall(html)
    chap_meta = RE_PAGEFIND_CHAPTER.findall(html)
    # Filter to only the injected spans (avoid breadcrumb data-pagefind-meta="chapter" which is unvalued).
    info["part_meta"] = part_meta
    info["chapter_meta"] = chap_meta
    # Need at least one part: span (in pagefind-meta-injected). Look more strictly.
    part_inj = re.findall(r'<span[^>]*class="[^"]*pagefind-meta-injected[^"]*"[^>]*data-pagefind-meta="part:([^"]*)"', html)
    chap_inj = re.findall(r'<span[^>]*class="[^"]*pagefind-meta-injected[^"]*"[^>]*data-pagefind-meta="chapter:([^"]*)"', html)
    info["part_inj"] = part_inj
    info["chap_inj"] = chap_inj
    if not part_inj:
        issues.append(("PAGEFIND_MISSING_PART", "no pagefind-meta-injected span for part"))
    if not chap_inj:
        issues.append(("PAGEFIND_MISSING_CHAPTER", "no pagefind-meta-injected span for chapter"))

    info["issues"] = issues
    return info


def main():
    files = find_html_files()
    results = [audit_file(p) for p in files]
    # Save raw results.
    return results


if __name__ == "__main__":
    results = main()
    print("Total files:", len(results))
    by_kind = defaultdict(int)
    drift = 0
    for r in results:
        by_kind[r["kind"]] += 1
        if r.get("issues"):
            drift += 1
    print("Files with drift:", drift)
    for k, n in by_kind.items():
        print(f"  {k}: {n}")

    # Save for further processing.
    import json
    with open(os.path.join(ROOT, "_audit_raw.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
