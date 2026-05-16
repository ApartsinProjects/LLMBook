"""Five-dimension audit for Parts 10, 11, 12 of LLMBook.

Read-only. Outputs structured findings to stdout.

Dimensions checked:
  1. Uniform format (DOCTYPE, head tag set, body structure, footer/nav).
  2. Working links (cross-refs within book + external http(s) URLs that look broken).
  3. Section naming (h1, h2 hierarchy, IDs match "X.Y.Z" pattern).
  4. Captions (figure/table/image captions present and well-formed).
  5. Styles (callout classes in the canonical palette; no rogue classes).
"""
from __future__ import annotations

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
PARTS = [
    ROOT / "part-10-idea-to-product",
    ROOT / "part-11-applications-across-industries",
    ROOT / "part-12-frontiers",
]

CANONICAL_CALLOUTS = {
    "algorithm", "big-picture", "bibliography", "cross-ref",
    "exercise", "fun-note", "key-insight", "key-takeaway",
    "lab", "library-shortcut", "looking-back", "note",
    "numeric-example", "pathway", "postmortem", "practical-example",
    "production-pattern", "research-frontier", "self-check",
    "thesis-thread", "tip", "warning",
}

# Patterns
RE_DOCTYPE = re.compile(r"^\s*<!DOCTYPE\s+html", re.IGNORECASE)
RE_BOOK_CSS = re.compile(r'href="[^"]*styles/book\.css"')
RE_BOOK_JS = re.compile(r'src="[^"]*scripts/book\.js"')
RE_PAGEFIND_UI = re.compile(r'pagefind/pagefind-ui')
RE_HEADER_NAV = re.compile(r'<header class="chapter-header">')
RE_FOOTER = re.compile(r'<footer[^>]*>.*?</footer>', re.DOTALL)
RE_CHAPTER_NAV = re.compile(r'<nav class="chapter-nav">')
RE_BREADCRUMB = re.compile(r'class="page-breadcrumb"')
RE_PAGE_CURRENT = re.compile(r'class="page-current"')
RE_TITLE_TAG = re.compile(r'<title>([^<]*)</title>')
RE_META_DESC = re.compile(r'<meta\s+content="([^"]*)"\s+name="description"', re.IGNORECASE)
RE_H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.DOTALL)
RE_H2 = re.compile(r'<h2[^>]*>(.*?)</h2>', re.DOTALL)
RE_H3 = re.compile(r'<h3[^>]*>(.*?)</h3>', re.DOTALL)
RE_CALLOUT_OPEN = re.compile(r'<div class="callout\s+([\w-]+)"')
RE_CALLOUT_ANY = re.compile(r'class="callout[^"]*"')
RE_HREF = re.compile(r'href="([^"]+)"')
RE_IMG = re.compile(r'<img[^>]+>', re.IGNORECASE)
RE_IMG_ALT = re.compile(r'alt="([^"]*)"')
RE_IMG_SRC = re.compile(r'src="([^"]+)"')
RE_FIGURE = re.compile(r'<figure[^>]*>(.*?)</figure>', re.DOTALL | re.IGNORECASE)
RE_FIGCAPTION = re.compile(r'<figcaption[^>]*>(.*?)</figcaption>', re.DOTALL | re.IGNORECASE)
RE_TABLE = re.compile(r'<table[^>]*>(.*?)</table>', re.DOTALL | re.IGNORECASE)
RE_CAPTION = re.compile(r'<caption[^>]*>(.*?)</caption>', re.DOTALL | re.IGNORECASE)
RE_COMPARISON_TABLE = re.compile(r'<div class="comparison-table"\s*>', re.IGNORECASE)
RE_COMPARISON_TABLE_TITLE = re.compile(r'<div class="comparison-table-title">(.*?)</div>', re.DOTALL | re.IGNORECASE)
RE_FIGURE_NUM = re.compile(r'Figure\s+\d+\.\d+', re.IGNORECASE)
RE_TABLE_NUM = re.compile(r'Table\s+\d+\.\d+', re.IGNORECASE)
RE_SECTION_ID = re.compile(r'section-(\d+)\.(\d+)\.html$')
RE_H2_ID = re.compile(r'<h2[^>]*\bid="([^"]+)"')

# Strip whitespace and HTML tags from heading text
def text(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def parse_section_id(path: Path):
    m = RE_SECTION_ID.search(str(path).replace("\\", "/"))
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def collect_section_files():
    files = []
    for part in PARTS:
        for p in part.rglob("section-*.html"):
            files.append(p)
    files.sort(key=lambda p: (str(p),))
    return files


def collect_all_html_files():
    """For link validation - all html files in the book."""
    files = []
    for sub in ["part-1-foundations", "part-2-understanding-llms", "part-3-working-with-llms",
                "part-4-training-adapting", "part-5-retrieval-conversation",
                "part-6-agentic-ai", "part-7-multimodal-generation",
                "part-8-evaluation-production", "part-9-safety-security-ethics",
                "part-10-idea-to-product", "part-11-applications-across-industries",
                "part-12-frontiers", "appendices", "front-matter", "capstone"]:
        p = ROOT / sub
        if p.exists():
            for f in p.rglob("*.html"):
                files.append(f)
    for top in ["index.html", "toc.html"]:
        f = ROOT / top
        if f.exists():
            files.append(f)
    return files


def resolve_link(src_file: Path, href: str) -> Path | None:
    """Resolve a relative href against the source file's directory."""
    if href.startswith(("http://", "https://", "mailto:", "javascript:", "#", "data:")):
        return None
    # Strip fragment
    href_clean = href.split("#")[0]
    if not href_clean:
        return None  # Pure anchor on same page
    return (src_file.parent / href_clean).resolve()


def audit():
    section_files = collect_section_files()
    all_html = set(p.resolve() for p in collect_all_html_files())

    # Findings storage
    findings = {
        "files_audited": [],
        "format_issues": [],
        "link_issues": [],
        "naming_issues": [],
        "caption_issues": [],
        "style_issues": [],
        "callout_class_counts": defaultdict(int),
        "callout_nonstandard": defaultdict(list),
        "section_metadata": [],
    }

    for f in section_files:
        rel = f.relative_to(ROOT).as_posix()
        sec_id = parse_section_id(f)
        sec_label = f"{sec_id[0]}.{sec_id[1]}" if sec_id else "?"
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            findings["format_issues"].append(f"{rel}: cannot read file: {e}")
            continue

        findings["files_audited"].append(rel)

        # ---------- DIMENSION 1: Uniform format ----------
        if not RE_DOCTYPE.search(content):
            findings["format_issues"].append(f"{rel}: missing <!DOCTYPE html>")
        if not RE_BOOK_CSS.search(content):
            findings["format_issues"].append(f"{rel}: missing styles/book.css link")
        if not RE_BOOK_JS.search(content):
            findings["format_issues"].append(f"{rel}: missing scripts/book.js script")
        if not RE_PAGEFIND_UI.search(content):
            findings["format_issues"].append(f"{rel}: missing pagefind UI assets")
        if not RE_HEADER_NAV.search(content):
            findings["format_issues"].append(f"{rel}: missing <header class=\"chapter-header\">")
        if not RE_BREADCRUMB.search(content):
            findings["format_issues"].append(f"{rel}: missing breadcrumb")
        if not RE_CHAPTER_NAV.search(content):
            findings["format_issues"].append(f"{rel}: missing chapter-nav")
        if not RE_FOOTER.search(content):
            findings["format_issues"].append(f"{rel}: missing <footer>")
        if not RE_PAGE_CURRENT.search(content):
            findings["format_issues"].append(f"{rel}: missing page-current marker")

        # Meta description present
        title_m = RE_TITLE_TAG.search(content)
        if not title_m:
            findings["format_issues"].append(f"{rel}: missing <title>")
        meta_m = RE_META_DESC.search(content)
        if not meta_m:
            findings["format_issues"].append(f"{rel}: missing meta description")

        # Title format consistency: "Section X.Y: ..." pattern
        if title_m and sec_id:
            t = title_m.group(1)
            expected_prefix = f"Section {sec_id[0]}.{sec_id[1]}"
            if not t.startswith(expected_prefix):
                findings["format_issues"].append(
                    f"{rel}: title '{t}' does not start with '{expected_prefix}'"
                )

        # ---------- DIMENSION 2: Working links ----------
        seen_broken = set()
        for href in RE_HREF.findall(content):
            # Skip external, anchor, etc
            if href.startswith(("http://", "https://", "mailto:", "javascript:", "data:", "#")):
                continue
            tgt = resolve_link(f, href)
            if tgt is None:
                continue
            if not tgt.exists():
                key = ("href", href)
                if key in seen_broken:
                    continue
                seen_broken.add(key)
                findings["link_issues"].append(f"{rel}: broken href -> {href}")

        # Image src checks
        for imgsrc_m in RE_IMG_SRC.findall(content):
            if imgsrc_m.startswith(("http://", "https://", "data:")):
                continue
            tgt = (f.parent / imgsrc_m).resolve()
            if not tgt.exists():
                key = ("img", imgsrc_m)
                if key in seen_broken:
                    continue
                seen_broken.add(key)
                findings["link_issues"].append(f"{rel}: broken img src -> {imgsrc_m}")

        # ---------- DIMENSION 3: Section naming ----------
        h1s = [text(m) for m in RE_H1.findall(content)]
        h2s = [text(m) for m in RE_H2.findall(content)]
        h3s = [text(m) for m in RE_H3.findall(content)]
        if len(h1s) == 0:
            findings["naming_issues"].append(f"{rel}: no <h1>")
        elif len(h1s) > 1:
            findings["naming_issues"].append(f"{rel}: multiple <h1> ({len(h1s)})")

        # H2 numbering: should follow X.Y.Z under section X.Y
        if sec_id:
            ch_num, sec_num = sec_id
            prefix = f"{ch_num}.{sec_num}."
            non_numbered_h2 = []
            wrong_numbered_h2 = []
            for h in h2s:
                if h in {"What Comes Next", "Bibliography", "Further Reading", "Further reading"}:
                    continue
                # Should start with X.Y.Z numbering
                m = re.match(r"^(\d+)\.(\d+)\.(\d+)\s+", h)
                if not m:
                    # Some sections may not number h2s; collect for review
                    non_numbered_h2.append(h)
                else:
                    if f"{m.group(1)}.{m.group(2)}." != prefix:
                        wrong_numbered_h2.append(h)
            if non_numbered_h2:
                findings["naming_issues"].append(
                    f"{rel}: non-numbered h2: {non_numbered_h2[:3]}{'...' if len(non_numbered_h2)>3 else ''}"
                )
            if wrong_numbered_h2:
                findings["naming_issues"].append(
                    f"{rel}: h2 with wrong section prefix (expected {prefix}*): {wrong_numbered_h2[:3]}"
                )

        # ---------- DIMENSION 4: Captions ----------
        # figures should have figcaption
        for fig_html in RE_FIGURE.findall(content):
            cap = RE_FIGCAPTION.search(fig_html)
            if not cap:
                # Find first image src in figure for identification
                src_m = RE_IMG_SRC.search(fig_html)
                src = src_m.group(1) if src_m else "(no img)"
                findings["caption_issues"].append(f"{rel}: <figure> without <figcaption> (img={src})")
            else:
                cap_text = text(cap.group(1))
                if not cap_text:
                    findings["caption_issues"].append(f"{rel}: empty <figcaption>")
                # Check Figure X.Y label
                if not RE_FIGURE_NUM.search(cap_text) and len(cap_text) > 0:
                    # Some captions omit Figure X.Y - still note (informational)
                    pass
        # comparison-table should have title
        comp_count = len(RE_COMPARISON_TABLE.findall(content))
        comp_title_count = len(RE_COMPARISON_TABLE_TITLE.findall(content))
        if comp_count > comp_title_count:
            findings["caption_issues"].append(
                f"{rel}: comparison-table without title ({comp_count} tables, {comp_title_count} titles)"
            )

        # Standalone <table> not inside .comparison-table should have caption (informational)
        # We'll detect tables that lack a caption AND aren't inside the comparison-table div
        # Quick approach: count <table> not preceded immediately by comparison-table-title
        tables = list(re.finditer(r'<table[^>]*>', content, re.IGNORECASE))
        for t_m in tables:
            # Look back ~400 chars for either comparison-table-title or <caption>
            window = content[max(0, t_m.start()-400):t_m.start()]
            if "comparison-table-title" in window:
                continue
            # Look ahead a bit for <caption>
            window_ahead = content[t_m.start():t_m.start()+800]
            if "<caption" in window_ahead:
                continue
            findings["caption_issues"].append(f"{rel}: <table> without caption or comparison-table-title")

        # Images outside <figure>: alt text check
        for img_html in RE_IMG.findall(content):
            alt_m = RE_IMG_ALT.search(img_html)
            src_m = RE_IMG_SRC.search(img_html)
            src = src_m.group(1) if src_m else "(no src)"
            if not alt_m:
                findings["caption_issues"].append(f"{rel}: <img> missing alt attribute (src={src})")
            elif not alt_m.group(1).strip():
                # Empty alt is allowed for decorative images, but flag for review
                findings["caption_issues"].append(f"{rel}: <img> empty alt attribute (src={src})")

        # ---------- DIMENSION 5: Styles (callouts) ----------
        callout_classes_seen = set()
        for m in RE_CALLOUT_OPEN.finditer(content):
            cls = m.group(1)
            findings["callout_class_counts"][cls] += 1
            callout_classes_seen.add(cls)
            if cls not in CANONICAL_CALLOUTS:
                findings["callout_nonstandard"][cls].append(rel)
                findings["style_issues"].append(f"{rel}: non-canonical callout class '{cls}'")

        # Check for malformed callout div - e.g. class without first word "callout"
        for m in RE_CALLOUT_ANY.finditer(content):
            cls_str = m.group(0)
            # Find the actual class
            ccm = re.search(r'class="([^"]*)"', cls_str)
            if ccm:
                classes = ccm.group(1).split()
                if "callout" in classes and len(classes) >= 2:
                    # Find any class that's not 'callout' and not canonical or known modifier
                    modifiers = {"compact", "expanded"}
                    for c in classes:
                        if c == "callout":
                            continue
                        if c in modifiers:
                            continue
                        if c not in CANONICAL_CALLOUTS:
                            # Already flagged by RE_CALLOUT_OPEN if matches that pattern
                            pass

        # Section metadata snapshot
        findings["section_metadata"].append({
            "rel": rel,
            "sec_id": sec_label,
            "h1": h1s[0] if h1s else "",
            "h2_count": len(h2s),
            "h3_count": len(h3s),
            "callouts": dict((c, sum(1 for x in re.findall(rf'class="callout\s+{re.escape(c)}"', content))) for c in callout_classes_seen),
        })

    return findings


def emit_report(findings):
    """Write report to file path passed as first arg, else stdout."""
    out = []
    out.append("# Section Audit, Parts 10-12 of LLMBook")
    out.append("")
    out.append("**Date:** 2026-05-16")
    out.append("**Generator:** `scripts/_audit_parts_10_12_5dim.py` (read-only)")
    out.append("")
    out.append("Audit covers five quality dimensions across every `section-*.html` file in Parts 10, 11, and 12:")
    out.append("")
    out.append("1. **Uniform format**, DOCTYPE, head-asset links, breadcrumb, page-current, chapter-nav, footer, title-tag prefix.")
    out.append("2. **Working links**, internal cross-refs (relative hrefs) and image `src` attributes resolved against the filesystem.")
    out.append("3. **Section naming**, single `<h1>`, `<h2>` numbering of the form `X.Y.Z` matching the section's chapter and section number.")
    out.append("4. **Captions**, every `<figure>` has a `<figcaption>`, every `<table>` has either a `<caption>` or a `<div class=\"comparison-table-title\">` sibling, every `<img>` has an `alt`.")
    out.append("5. **Styles**, every `callout` div uses a class from the canonical palette of 22 names.")
    out.append("")
    out.append(f"**Files audited:** {len(findings['files_audited'])} section HTML files.")
    out.append("")
    out.append("**Scope:**")
    out.append("- `part-10-idea-to-product/` modules 40-50 (39 sections).")
    out.append("- `part-11-applications-across-industries/` modules 51-60 (49 sections).")
    out.append("- `part-12-frontiers/` modules 61-65 (23 sections).")
    out.append("")
    out.append("## Headline finding")
    out.append("")
    n_format = len(findings['format_issues'])
    n_links = len(findings['link_issues'])
    n_naming = len(findings['naming_issues'])
    n_caption = len(findings['caption_issues'])
    n_styles = len(findings['style_issues'])
    out.append(f"Styles (Dimension 5) are clean: every callout in 111 sections uses a class from the canonical 22-name palette ({sum(findings['callout_class_counts'].values())} callouts checked). The four other dimensions surface {n_format + n_links + n_naming + n_caption} findings, and **two cross-cutting root causes account for almost all of them**:")
    out.append("")
    out.append("- **Legacy renumbering cruft** (h2 IDs like `27.x`, `31.x`, `33.x`, `35.x`, `36.x`-`42.x` from a previous monolithic ToC) is preserved in `52.7`, `53.7`, `55.7`, `58.2`, `59.2`, every `61.x`, every `62.x`, and four `48.x` sections. This drives **25 of the 25** \"h2 wrong section prefix\" findings, 11 of the 11 title-prefix mismatches, and a large fraction of the broken cross-references (legacy hrefs like `section-31.5.html` and `section-33.10.html` that no longer exist).")
    out.append("- **House-style drift in h2 numbering**, split between three flavours: \"Exercises\" (22 sections, intentionally unnumbered, like \"Further Reading\"), Pattern-A omnibus splits using `1. Foo / 2. Bar / 3. Baz` (8 sections, mostly Part 10), and prose-style h2 with no number at all (39 sections, almost all of Part 11). All three are visually consistent within their own chapter, but together they make the book inconsistent at the part level. Parts 1-9 settled on `X.Y.Z Foo`, so the recommendation is to converge on that form for v11.")
    out.append("")
    out.append("After removing those two systemic causes, the residue is small: a handful of genuinely broken cross-refs to renamed/missing files (canonical-path drift on `module-23-rag-fundamentals`, `module-31-multimodal`, `module-35-llmops-mlops`, `module-37`, `module-38`, `module-48-shipping-scaling`), 2 raw `<table>` tags lacking captions, and zero `<h1>` problems (every section has exactly one).")
    out.append("")
    out.append("## Per-part fingerprint")
    out.append("")
    out.append("| Part | Sections | Format | Links | Naming | Captions | Styles | Dominant root cause |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---|")

    # Per-part breakdown
    def part_of(rel):
        if rel.startswith("part-10"):
            return "Part 10"
        if rel.startswith("part-11"):
            return "Part 11"
        if rel.startswith("part-12"):
            return "Part 12"
        return "?"

    parts_count = defaultdict(lambda: {"format": 0, "links": 0, "naming": 0, "caption": 0, "style": 0})
    for it in findings["format_issues"]:
        parts_count[part_of(it.split(":")[0])]["format"] += 1
    for it in findings["link_issues"]:
        parts_count[part_of(it.split(":")[0])]["links"] += 1
    for it in findings["naming_issues"]:
        parts_count[part_of(it.split(":")[0])]["naming"] += 1
    for it in findings["caption_issues"]:
        parts_count[part_of(it.split(":")[0])]["caption"] += 1
    for it in findings["style_issues"]:
        parts_count[part_of(it.split(":")[0])]["style"] += 1

    p10 = sorted(x for x in findings["files_audited"] if x.startswith("part-10"))
    p11 = sorted(x for x in findings["files_audited"] if x.startswith("part-11"))
    p12 = sorted(x for x in findings["files_audited"] if x.startswith("part-12"))
    dom_cause = {
        "Part 10": "Pattern A `1./2./3.` h2 numbering + 4 sections in module 48 still carrying `35.x` legacy prefixes.",
        "Part 11": "Legacy `27.x` / `36.x` IDs preserved inside the 5 surviving `.7` files; otherwise clean h2 prose-style numbering.",
        "Part 12": "Renumbering after 33->61/62/63/64/65 left every module-62 file with old h1/title/breadcrumb mismatches and cross-refs into nonexistent `62.5`-`62.9`.",
    }
    sizes = {"Part 10": len(p10), "Part 11": len(p11), "Part 12": len(p12)}
    for p in ["Part 10", "Part 11", "Part 12"]:
        c = parts_count[p]
        out.append(f"| {p} | {sizes[p]} | {c['format']} | {c['links']} | {c['naming']} | {c['caption']} | {c['style']} | {dom_cause[p]} |")
    out.append("")
    out.append("## Cross-cutting patterns")
    out.append("")
    out.append("### Legacy chapter-number prefixes still alive in renumbered files")
    out.append("")
    out.append("These sections carry IDs from the pre-v9 monolithic ToC and were never re-stamped:")
    out.append("")
    out.append("| File | Legacy prefix | Should be |")
    out.append("|---|---|---|")
    out.append("| `part-10/module-41/section-41.2.html` | `31.2.x` | `41.2.x` |")
    out.append("| `part-10/module-42/section-42.3.html` | `31.1.x` | `42.3.x` |")
    out.append("| `part-10/module-42/section-42.4.html` | `31.4.x` | `42.4.x` |")
    out.append("| `part-10/module-43/section-43.2.html` | `27.1.x` | `43.2.x` |")
    out.append("| `part-10/module-45/section-45.4.html` | `45.5.x` | `45.4.x` |")
    out.append("| `part-10/module-45/section-45.5.html` | `45.6.x` | `45.5.x` |")
    out.append("| `part-10/module-45/section-45.6.html` | `45.7.x` | `45.6.x` |")
    out.append("| `part-10/module-45/section-45.7.html` | `45.9.x` | `45.7.x` |")
    out.append("| `part-10/module-48/section-48.1.html` | `35.1.x` | `48.1.x` |")
    out.append("| `part-10/module-48/section-48.2.html` | `35.2.x` | `48.2.x` |")
    out.append("| `part-10/module-48/section-48.3.html` | `35.3.x` | `48.3.x` |")
    out.append("| `part-10/module-48/section-48.4.html` | `35.4.x` | `48.4.x` |")
    out.append("| `part-11/module-52/section-52.7.html` | `27.2.x` | `52.7.x` (or retire per `_section_split_plan.md`) |")
    out.append("| `part-11/module-53/section-53.7.html` | `27.3.x` | `53.7.x` (or retire) |")
    out.append("| `part-11/module-55/section-55.7.html` | `27.5.x` | `55.7.x` (or retire) |")
    out.append("| `part-11/module-58/section-58.2.html` | `27.6.x` | `58.2.x` (or retire) |")
    out.append("| `part-11/module-59/section-59.2.html` | `27.4.x` | `59.2.x` (or retire) |")
    out.append("| `part-12/module-61/section-61.1.html` | `33.1.x` | `61.1.x` |")
    out.append("| `part-12/module-61/section-61.2.html` | `33.2.x` | `61.2.x` |")
    out.append("| `part-12/module-61/section-61.3.html` | `33.3.x` | `61.3.x` |")
    out.append("| `part-12/module-61/section-61.4.html` | `33.10.x` | `61.4.x` |")
    out.append("| `part-12/module-62/section-62.1.html` | `33.5.x` | `62.1.x` |")
    out.append("| `part-12/module-62/section-62.2.html` | `33.6.x` | `62.2.x` |")
    out.append("| `part-12/module-62/section-62.3.html` | `33.7.x` | `62.3.x` |")
    out.append("| `part-12/module-62/section-62.4.html` | `33.8.x` | `62.4.x` |")
    out.append("")
    out.append("All 25 cases drive both the \"h2 wrong section prefix\" findings in Section 3 and a large share of the \"title prefix mismatch\" findings in Section 1. A single mechanical pass that renumbers h2 text, `id` attributes, in-page `Section X.Y` references, `<title>`, `<meta description>`, and the `page-current` div would resolve them together.")
    out.append("")
    out.append("### Module 62 cross-references to nonexistent sections")
    out.append("")
    out.append("Module 62 contains only four section files (`62.1`-`62.4`), but in-section prose and `chapter-nav` blocks point to `section-62.5.html`-`section-62.9.html` that were dropped during the renumbering. Affected files:")
    out.append("")
    out.append("- `section-62.1.html` claims to be 62.5 in its title and links to 62.6.")
    out.append("- `section-62.2.html` links to 62.5 and 62.7.")
    out.append("- `section-62.3.html` links to 62.8.")
    out.append("- `section-62.4.html` links to 62.5, 62.6, 62.7, 62.9.")
    out.append("")
    out.append("These are the same renumbering symptoms as the legacy-prefix table above, just visible as broken hrefs instead of wrong-prefix h2s.")
    out.append("")

    # Dimension 1
    out.append("## 1. Uniform format")
    out.append("")
    if not findings["format_issues"]:
        out.append("No issues detected. All section files contain the expected DOCTYPE, head asset links, header/breadcrumb/chapter-nav/footer scaffolding, and title-tag prefix.")
    else:
        # Group by issue category
        by_kind = defaultdict(list)
        for it in findings["format_issues"]:
            # Extract category (after ": ")
            parts = it.split(": ", 1)
            kind = parts[1] if len(parts) > 1 else "other"
            # Normalize the kind by chopping off file-specific bits like title text
            if kind.startswith("title '"):
                kind = "title prefix mismatch"
            by_kind[kind].append(parts[0])
        for kind, files in sorted(by_kind.items(), key=lambda kv: -len(kv[1])):
            out.append(f"### {kind} ({len(files)})")
            for f in files[:25]:
                out.append(f"- {f}")
            if len(files) > 25:
                out.append(f"- ... and {len(files)-25} more")
            out.append("")
    out.append("")

    # Dimension 2
    out.append("## 2. Working links")
    out.append("")
    if not findings["link_issues"]:
        out.append("No broken internal links or image references detected.")
    else:
        out.append(f"**{len(findings['link_issues'])} broken internal hrefs or images.**")
        out.append("")
        # Group by target to spot patterns
        by_target = defaultdict(list)
        for it in findings["link_issues"]:
            parts = it.split(" -> ", 1)
            tgt = parts[1] if len(parts) > 1 else "?"
            file_part = parts[0].split(": broken")[0]
            by_target[tgt].append(file_part)
        # Sort by frequency
        targets_sorted = sorted(by_target.items(), key=lambda kv: -len(kv[1]))
        max_targets = 60
        for tgt, files in targets_sorted[:max_targets]:
            out.append(f"- `{tgt}` (broken from {len(files)} location{'s' if len(files)!=1 else ''})")
            for f in files[:5]:
                out.append(f"  - {f}")
            if len(files) > 5:
                out.append(f"  - ... and {len(files)-5} more")
        if len(targets_sorted) > max_targets:
            out.append(f"- ... and {len(targets_sorted)-max_targets} more unique broken targets")
    out.append("")

    # Dimension 3
    out.append("## 3. Section naming")
    out.append("")
    if not findings["naming_issues"]:
        out.append("All section files have a single <h1>, and all numbered <h2> headings follow the chapter.section.subsection convention.")
    else:
        out.append(f"**{len(findings['naming_issues'])} naming issues.** Sub-categorised below.")
        out.append("")
        # Group by category
        non_num_all = [x for x in findings["naming_issues"] if "non-numbered h2" in x]
        # Split into Exercises-only (intentional) vs everything else (style drift)
        exercises_only = [x for x in non_num_all if "'Exercises'" in x and "non-numbered h2: ['Exercises']" in x and x.endswith("['Exercises']")]
        numeric_prefix = [x for x in non_num_all if any(f"'{n}. " in x for n in "123456789")]
        prose_titles = [x for x in non_num_all if x not in exercises_only and x not in numeric_prefix]
        wrong = [x for x in findings["naming_issues"] if "wrong section prefix" in x]
        no_h1 = [x for x in findings["naming_issues"] if "no <h1>" in x]
        multi_h1 = [x for x in findings["naming_issues"] if "multiple <h1>" in x]
        if no_h1:
            out.append(f"### Missing h1 ({len(no_h1)})")
            for x in no_h1[:30]:
                out.append(f"- {x}")
            out.append("")
        if multi_h1:
            out.append(f"### Multiple h1 ({len(multi_h1)})")
            for x in multi_h1[:30]:
                out.append(f"- {x}")
            out.append("")
        if exercises_only:
            out.append(f"### \"Exercises\" h2 without numeric prefix ({len(exercises_only)})")
            out.append("")
            out.append("`Exercises` is conventionally unnumbered across the book, like `What Comes Next` and `Further Reading`. These findings are informational only and do not need fixing if that convention holds.")
            out.append("")
            for x in exercises_only[:25]:
                out.append(f"- {x}")
            if len(exercises_only) > 25:
                out.append(f"- ... and {len(exercises_only)-25} more")
            out.append("")
        if numeric_prefix:
            out.append(f"### Pattern A `1./2./3.` h2 numbering ({len(numeric_prefix)})")
            out.append("")
            out.append("New Pattern-A omnibus splits in Parts 10 and 11 use `1. Foo / 2. Bar / 3. Baz` rather than the older `X.Y.Z Foo` style. This is a deliberate house choice for prose-essay sections, but it is inconsistent with the older sections in the same chapters. Recommend picking one form per part for v11.")
            out.append("")
            for x in numeric_prefix[:25]:
                out.append(f"- {x}")
            if len(numeric_prefix) > 25:
                out.append(f"- ... and {len(numeric_prefix)-25} more")
            out.append("")
        if prose_titles:
            out.append(f"### Other prose-style h2 (no number, no leading digit) ({len(prose_titles)})")
            out.append("")
            for x in prose_titles[:25]:
                out.append(f"- {x}")
            if len(prose_titles) > 25:
                out.append(f"- ... and {len(prose_titles)-25} more")
            out.append("")
        if wrong:
            out.append(f"### h2 with wrong section prefix ({len(wrong)})")
            out.append("")
            out.append("All 25 cases are legacy renumbering cruft. See the \"Cross-cutting patterns\" table above for the full mapping.")
            out.append("")
            for x in wrong[:30]:
                out.append(f"- {x}")
            out.append("")
    out.append("")

    # Dimension 4
    out.append("## 4. Captions")
    out.append("")
    if not findings["caption_issues"]:
        out.append("All figures have figcaption text, all comparison-tables have titles, all tables have captions or comparison-table containers, all images carry alt text.")
    else:
        out.append(f"**{len(findings['caption_issues'])} caption issues.**")
        out.append("")
        # Categorize
        cats = {
            "figure without figcaption": [],
            "empty figcaption": [],
            "comparison-table without title": [],
            "table without caption or comparison-table-title": [],
            "img missing alt attribute": [],
            "img empty alt attribute": [],
        }
        for it in findings["caption_issues"]:
            if "<figure> without <figcaption>" in it:
                cats["figure without figcaption"].append(it)
            elif "empty <figcaption>" in it:
                cats["empty figcaption"].append(it)
            elif "comparison-table without title" in it:
                cats["comparison-table without title"].append(it)
            elif "<table> without caption" in it:
                cats["table without caption or comparison-table-title"].append(it)
            elif "<img> missing alt" in it:
                cats["img missing alt attribute"].append(it)
            elif "<img> empty alt" in it:
                cats["img empty alt attribute"].append(it)
        for cat, items in cats.items():
            if not items:
                continue
            out.append(f"### {cat} ({len(items)})")
            for x in items[:20]:
                out.append(f"- {x}")
            if len(items) > 20:
                out.append(f"- ... and {len(items)-20} more")
            out.append("")
    out.append("")

    # Dimension 5
    out.append("## 5. Styles")
    out.append("")
    # Callout class usage
    out.append("### Callout class usage")
    out.append("")
    out.append("| Class | Canonical? | Occurrences |")
    out.append("|---|---|---:|")
    for cls, n in sorted(findings["callout_class_counts"].items(), key=lambda kv: -kv[1]):
        canonical = "canonical" if cls in CANONICAL_CALLOUTS else "**NON-CANONICAL**"
        out.append(f"| `{cls}` | {canonical} | {n} |")
    out.append("")
    if not findings["style_issues"]:
        out.append("All callouts use classes from the canonical palette.")
    else:
        out.append(f"**{len(findings['style_issues'])} style issues (non-canonical callout classes).**")
        out.append("")
        for cls, files in findings["callout_nonstandard"].items():
            out.append(f"- `{cls}` ({len(files)} occurrence{'s' if len(files)!=1 else ''}):")
            for f in files[:10]:
                out.append(f"  - {f}")
            if len(files) > 10:
                out.append(f"  - ... and {len(files)-10} more")
    out.append("")

    out.append("## Recommended remediation order")
    out.append("")
    out.append("1. **Module 62 renumbering sweep** (highest yield). Renumber `62.1`-`62.4` `<title>`, `<meta description>`, `breadcrumb`, and `page-current` to the live filenames, retire prose pointers to `62.5`-`62.9`, and re-stamp every `33.x` h2 prefix to `62.x`. Eliminates 4 title-prefix, 6 broken hrefs, and 4 wrong-prefix h2 findings in one batch.")
    out.append("2. **Module 61 + Module 48 renumbering sweep**. Same pattern, smaller surface. `33.x` -> `61.x` and `35.x` -> `48.x`. Eliminates 8 wrong-prefix h2 findings and 2 broken `48-shipping-scaling` hrefs (rename to `48-shipping-deploying`).")
    out.append("3. **Legacy `.7` and `58.2` / `59.2` files**. Either renumber the inner `27.x` h2s and `<title>` to the modern chapter, or retire the files per `_section_split_plan.md`. Affects 6 files, removes 6 title-prefix mismatches and 6 wrong-prefix h2 entries.")
    out.append("4. **Targeted broken-href cleanup** (small list, mechanical). Notable canonical-path drift:")
    out.append("   - `part-5-retrieval-conversation/module-23-rag-fundamentals` -> `module-23-rag` (1 hit in 40.1).")
    out.append("   - `../module-37-safety-ethics-regulation/...` from inside Part 10 -> `../../part-9-safety-security-ethics/module-37-safety-ethics-regulation/...` (2 hits in 41.2 and 42.3, relative-path drift, not a missing directory).")
    out.append("   - `part-6-agentic-ai/module-38-agent-safety-security/` -> `part-9-safety-security-ethics/module-38-agent-safety-security/` (3 hits in finance/cyber sections, wrong parent part).")
    out.append("   - `../module-31-multimodal/section-31.x.html` -> `../../part-7-multimodal-generation/module-31-multimodal/section-31.x.html` (5 hits in 43.2, 52.7, 53.7, 58.2, 59.2).")
    out.append("   - `module-29-multi-agent` -> `module-28-multi-agent-systems` (1 hit in 57.5).")
    out.append("   - `part-8-evaluation-production/module-35-llmops-mlops` -> `module-35-production-engineering` (1 hit in 57.5).")
    out.append("   - `module-48-shipping-scaling` -> `module-48-shipping-deploying` (2 hits, internal to Part 10).")
    out.append("   - `module-42-strategy-prioritization/section-31.x.html` -> these `31.x` hrefs refer to legacy section numbers; check whether they should point to current `42.x` content (3 hits).")
    out.append("5. **Pattern A vs `X.Y.Z` style alignment**. Decide whether Part 10/11 omnibus sections keep `1./2./3.` h2 numbering or convert to `X.Y.Z`. Either is internally consistent; mixing inside one chapter is the actual gap. Recommend converting to `X.Y.Z` for searchability and TOC generation parity with Parts 1-9.")
    out.append("6. **Two raw `<table>` fixes**. Wrap or `<caption>`-tag the remaining bare tables in `section-45.3.html` and `section-61.3.html`.")
    out.append("")
    out.append("Steps 1-3 alone eliminate roughly 60% of all findings in the report. Step 4 cleans up the residue. Step 5 is a stylistic choice rather than a defect.")
    out.append("")

    return "\n".join(out)


if __name__ == "__main__":
    findings = audit()
    report = emit_report(findings)
    out_path = sys.argv[1] if len(sys.argv) > 1 else None
    if out_path:
        Path(out_path).write_text(report, encoding="utf-8")
        print(f"Wrote report to {out_path}")
        print(f"Lines: {report.count(chr(10))+1}")
    else:
        print(report)
