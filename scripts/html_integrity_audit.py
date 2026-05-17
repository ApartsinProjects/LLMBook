#!/usr/bin/env python3
"""HTML Integrity Audit (post-v9 reshuffle).

Audits ALL HTML files in LLMBook for four classes of issues:
(a) Missing or wrong cross-references
(b) Bottom navigation correctness
(c) Generation placeholders or leftovers
(d) Broken image pointers

Read-only. Produces a single Markdown report.
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
REPORT_PATH = ROOT / "html-integrity-audit.md"

SKIP_DIRS = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude", "vendor",
}

DROPPED_REFS_PATTERNS = [
    (re.compile(r"appendix-n-master-reference-tables", re.IGNORECASE), "appendix-n-master-reference-tables (dropped)"),
    (re.compile(r"appendix-p-freshness-2026", re.IGNORECASE), "appendix-p-freshness-2026 (dropped)"),
    (re.compile(r"glossary/section-", re.IGNORECASE), "glossary/section-* (dropped glossary)"),
    (re.compile(r"\b(?:/|href=\"|\")glossary/", re.IGNORECASE), "/glossary/ path (dropped)"),
    (re.compile(r"Master Reference Tables", re.IGNORECASE), "Master Reference Tables (dropped)"),
    (re.compile(r"Freshness Index", re.IGNORECASE), "Freshness Index (dropped)"),
]

# Prose references to dropped resources (text only, not in href attributes)
# Appendix letter assignments after the v14 consolidation:
#   A = Mathematical Foundations
#   B = ML Essentials
#   C = Course Syllabi               (was P)
#   D = Reading Pathways             (was Q)
#   E = Intermediate Projects        (was R)
#   F = Capstone Project             (was S)
#   G = War Stories for Discussion   (was T)
# Original C-N (framework guides + ops) were consolidated into part-specific
# Tools of the Trade chapters. O (Docker) was folded into Part 10 / Chapter 62.
PROSE_DROPPED_PATTERNS = [
    # Appendix-letter prose drift is detected only if the IMMEDIATE context
    # (a short window before AND after) doesn't mention the expected topic.
    # The original regex used only a lookahead, which missed legitimate forms
    # like "war stories in Appendix G". Allow either direction.
    (re.compile(r"(?<!\w)(?<!Reading\s)(?<!war\s)(?<!war\sstories\sin\s)(?<!for\s)(?<!Capstone\s)\bAppendix\s+C\b(?!\s*(?:[\.\-:,\(]|\s|<)*(?:Course|Syllab))(?<!Course\sSyllabi\s\bC\b)", re.IGNORECASE), "'Appendix C' refers to non-Course-Syllabi content"),
    (re.compile(r"\bAppendix\s+D\b(?!\s*(?:[\.\-:,\(]|\s|<)*(?:Reading|Pathways))", re.IGNORECASE), "'Appendix D' refers to non-Pathways content"),
    (re.compile(r"\bAppendix\s+E\b(?!\s*(?:[\.\-:,\(]|\s|<)*(?:Intermediate|Project))", re.IGNORECASE), "'Appendix E' refers to non-Intermediate-Projects content"),
    (re.compile(r"\bAppendix\s+F\b(?!\s*(?:[\.\-:,\(]|\s|<)*(?:Capstone))", re.IGNORECASE), "'Appendix F' refers to non-Capstone content"),
    # For Appendix G: allow either "Appendix G (War...)" form OR "war stor[y/ies] in Appendix G" form
    (re.compile(r"(?<!war\sstories\sin\s)(?<!Story\s\d\sin\s)(?<!Stories\sin\s)\bAppendix\s+G\b(?!\s*(?:[\.\-:,\(]|\s|<)*(?:War|Story|Stories))", re.IGNORECASE), "'Appendix G' refers to non-WarStories content"),
    (re.compile(r"\bGlossary entry for\b", re.IGNORECASE), "'Glossary entry for ...' (glossary dropped)"),
    (re.compile(r"\bsee the [Gg]lossary\b", re.IGNORECASE), "'see the glossary' (glossary dropped)"),
    (re.compile(r"\bin the [Gg]lossary\b", re.IGNORECASE), "'in the glossary' (glossary dropped)"),
]

# Tags / contexts where Appendix O/P/Q mentions are expected and benign:
# - inside <span class="nav-num">, <span class="bc-current">, <span class="mod-num">, <span class="toc-chapter-num">
# - in <title>, <h1>, data-pagefind-meta of any appendix landing page
# - inside aria-label attributes (toc-chapter-num)
PROSE_BENIGN_NEAR_PATTERNS = re.compile(
    r"""(?:nav-num|bc-current|mod-num|toc-chapter-num|aria-label\s*=\s*["']Appendix\s+[A-Z]|data-pagefind-meta="(?:chapter|appendix):Appendix\s+[A-Z]|data-pagefind-meta="part:Appendix\s+[A-Z]|<title>[^<]*Appendix\s+[A-Z])""",
    re.IGNORECASE,
)

PLACEHOLDER_PATTERNS = [
    (re.compile(r"TODO\("), "TODO("),
    (re.compile(r"\bFIXME\b"), "FIXME"),
    (re.compile(r"<!--\s*TODO", re.IGNORECASE), "<!-- TODO"),
    (re.compile(r"<!--\s*placeholder", re.IGNORECASE), "<!-- placeholder"),
    (re.compile(r"\bXXX\b"), "XXX"),
    (re.compile(r"lorem ipsum", re.IGNORECASE), "lorem ipsum"),
    (re.compile(r"figure-replaced"), "figure-replaced"),
    (re.compile(r"TODO author", re.IGNORECASE), "TODO author"),
    (re.compile(r"TODO migrate", re.IGNORECASE), "TODO migrate"),
    (re.compile(r"<p>\s*</p>"), "empty <p></p>"),
    (re.compile(r"<p>\s*<em>\s*TODO", re.IGNORECASE), "<p><em>TODO"),
    (re.compile(r"figure-stub"), "figure-stub"),
    (re.compile(r"image-missing"), "image-missing"),
    (re.compile(r"Coming soon", re.IGNORECASE), "Coming soon"),
    (re.compile(r"section-todo"), "section-todo"),
    (re.compile(r"<!--\s*BUG:"), "BUG: comment"),
]

# A href on a tag we care about
HREF_RE = re.compile(r"""<a\s+[^>]*?href\s*=\s*["']([^"'#]+)(#[^"']*)?["'][^>]*>""", re.IGNORECASE | re.DOTALL)
# img src
IMG_SRC_RE = re.compile(r"""<img\s+[^>]*?src\s*=\s*["']([^"']+)["'][^>]*>""", re.IGNORECASE | re.DOTALL)
# Chapter nav block
NAV_RE = re.compile(
    r"""<nav[^>]*class\s*=\s*["'][^"']*chapter-nav[^"']*["'][^>]*>(.*?)</nav>""",
    re.IGNORECASE | re.DOTALL,
)
NAV_REL_RE = re.compile(
    r"""<a\s+[^>]*?(?:class\s*=\s*["']?nav-(prev|up|next)["']?|rel\s*=\s*["'](prev|up|next)["'])[^>]*?href\s*=\s*["']([^"']+)["']""",
    re.IGNORECASE | re.DOTALL,
)
# Alternate nav extraction: get all a hrefs inside the nav block
NAV_ANY_LINK_RE = re.compile(
    r"""<a\s+[^>]*?(?:class\s*=\s*["']([^"']*)["'])?[^>]*?href\s*=\s*["']([^"']+)["'][^>]*>(.*?)</a>""",
    re.IGNORECASE | re.DOTALL,
)
# H1 detection
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
# section file id like section-1.2 or 12.3
SECTION_NUM_RE = re.compile(r"section-(\d+)\.(\d+)\.html$", re.IGNORECASE)


def is_skipped(path: Path) -> bool:
    parts = set(path.parts)
    return any(d in parts for d in SKIP_DIRS)


def collect_html_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*.html"):
        if is_skipped(p):
            continue
        files.append(p)
    return files


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def resolve_href(file_path: Path, href: str) -> Path | None:
    """Resolve href to absolute filesystem path. Returns None for external/anchor/special."""
    if not href:
        return None
    href = href.strip()
    if href.startswith(("#", "mailto:", "javascript:", "tel:")):
        return None
    parsed = urlparse(href)
    if parsed.scheme in ("http", "https", "data", "ftp"):
        return None
    raw = unquote(parsed.path)
    if not raw:
        return None
    if raw.startswith("/"):
        # Treat as ROOT-relative
        candidate = ROOT / raw.lstrip("/")
    else:
        candidate = (file_path.parent / raw).resolve()
    return candidate


def file_exists(path: Path) -> bool:
    if path is None:
        return False
    if path.exists():
        return True
    # Some links point at directories without trailing /
    if path.is_dir():
        return True
    return False


def line_of(content: str, idx: int) -> int:
    return content.count("\n", 0, idx) + 1


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def main() -> int:
    files = collect_html_files()
    files.sort()
    print(f"Scanning {len(files)} HTML files...", file=sys.stderr)

    # Findings buckets
    p0: list[str] = []  # Critical: dropped-ref href links / broken nav targets
    p1: list[str] = []  # Broken cross-refs / broken images
    p2: list[str] = []  # Placeholders / TODOs
    p3: list[str] = []  # Minor drift / suspicious prose / etc.

    broken_image_by_dir: dict[str, list[str]] = defaultdict(list)
    placeholder_total = 0

    for fpath in files:
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception as e:
            p3.append(f"{rel(fpath)} - could not read: {e}")
            continue

        rel_path = rel(fpath)

        # ---- (a) Cross-refs: dropped resources in any text/href ----
        for pat, label in DROPPED_REFS_PATTERNS:
            for m in pat.finditer(content):
                line = line_of(content, m.start())
                snippet = content[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
                snippet = re.sub(r"\s+", " ", snippet).strip()
                p0.append(f"{rel_path}:{line} - dropped ref '{label}' - context: ...{snippet[:120]}...")

        for pat, label in PROSE_DROPPED_PATTERNS:
            for m in pat.finditer(content):
                # Only consider when not inside an href / file path
                start = m.start()
                window = content[max(0, start - 120): start]
                if 'href="' in window[-60:] or "href='" in window[-60:]:
                    continue
                # Skip benign breadcrumb / nav / TOC chapter labels surrounding this match
                near = content[max(0, start - 80): min(len(content), m.end() + 40)]
                if PROSE_BENIGN_NEAR_PATTERNS.search(near):
                    continue
                # Skip the Appendix N/P landing pages themselves (own title/h1)
                if "appendix-n-docker-containers" in rel_path or "appendix-p-reading-pathways" in rel_path:
                    # Allow only if it's clearly a textual reference that's wrong (rare); skip top-of-page mentions
                    continue
                line = line_of(content, start)
                snippet = content[max(0, start - 30): m.end() + 60].replace("\n", " ")
                snippet = re.sub(r"\s+", " ", snippet).strip()
                p3.append(f"{rel_path}:{line} - prose drift '{label}' - ...{snippet[:120]}...")

        # ---- (a) Broken href cross-refs ----
        hrefs_seen: set[tuple[int, str]] = set()
        for m in HREF_RE.finditer(content):
            href = m.group(1)
            target = resolve_href(fpath, href)
            if target is None:
                continue
            if file_exists(target):
                continue
            line = line_of(content, m.start())
            key = (line, href)
            if key in hrefs_seen:
                continue
            hrefs_seen.add(key)
            # Determine priority: if it's a dropped resource href, P0 already; else P1
            if any(pat.search(href) for pat, _ in DROPPED_REFS_PATTERNS):
                # already reported above
                continue
            p1.append(f"{rel_path}:{line} - broken href -> {href}")

        # ---- (d) Broken images ----
        for m in IMG_SRC_RE.finditer(content):
            src = m.group(1)
            if src.startswith("data:"):
                continue
            target = resolve_href(fpath, src)
            if target is None:
                continue
            if file_exists(target):
                continue
            line = line_of(content, m.start())
            dir_key = str(fpath.parent.relative_to(ROOT)).replace("\\", "/") if fpath.parent != ROOT else "."
            broken_image_by_dir[dir_key].append(f"{rel_path}:{line} -> {src}")
            # Also flag svg/png pair fallback opportunity
            if src.lower().endswith(".svg"):
                png_alt = target.with_suffix(".png") if target else None
                if png_alt and png_alt.exists():
                    p3.append(f"{rel_path}:{line} - missing .svg but .png exists for {src}")
            elif src.lower().endswith(".png"):
                svg_alt = target.with_suffix(".svg") if target else None
                if svg_alt and svg_alt.exists():
                    p3.append(f"{rel_path}:{line} - missing .png but .svg exists for {src}")

        # ---- (c) Placeholders ----
        # Dedupe per (file, line) — report only first label hit per line
        seen_placeholder_lines: set[int] = set()
        for pat, label in PLACEHOLDER_PATTERNS:
            for m in pat.finditer(content):
                line = line_of(content, m.start())
                if line in seen_placeholder_lines:
                    continue
                seen_placeholder_lines.add(line)
                snippet = content[max(0, m.start() - 20): m.end() + 40].replace("\n", " ")
                snippet = re.sub(r"\s+", " ", snippet).strip()
                p2.append(f"{rel_path}:{line} - placeholder '{label}' - ...{snippet[:120]}...")
                placeholder_total += 1

        # Empty/Appendix-only h1
        for m in H1_RE.finditer(content):
            inner = strip_tags(m.group(1)).strip()
            if not inner:
                p2.append(f"{rel_path}:{line_of(content, m.start())} - empty <h1>")
            elif re.fullmatch(r"Appendix\s+[A-Z](?::|\.)?\s*", inner, re.IGNORECASE):
                p2.append(f"{rel_path}:{line_of(content, m.start())} - <h1> has only 'Appendix X:' (no title)")

        # ---- (b) Bottom navigation correctness ----
        # Only check section-*.html under part-*/module-*/ subdirs (chapter sections)
        is_section = SECTION_NUM_RE.search(fpath.name) is not None and "module-" in str(fpath).lower()
        nav_match = NAV_RE.search(content)
        if is_section:
            if not nav_match:
                p1.append(f"{rel_path} - section file MISSING <nav class='chapter-nav'>")
            else:
                nav_html = nav_match.group(1)
                # Find prev/up/next via rel/class hints
                nav_links: dict[str, str] = {}
                # Try rel/class attributes first
                for am in re.finditer(
                    r"""<a\b[^>]*?(?:(?:rel|class)\s*=\s*["'][^"']*(?:nav-)?(prev|up|next)[^"']*["'])[^>]*?href\s*=\s*["']([^"']+)["'][^>]*>(.*?)</a>""",
                    nav_html,
                    re.IGNORECASE | re.DOTALL,
                ):
                    key = am.group(1).lower()
                    nav_links.setdefault(key, am.group(2))
                # Fallback heuristic by link order
                if not nav_links:
                    all_links = re.findall(
                        r"""<a\s+[^>]*?href\s*=\s*["']([^"']+)["'][^>]*>(.*?)</a>""",
                        nav_html,
                        re.IGNORECASE | re.DOTALL,
                    )
                    if len(all_links) >= 3:
                        nav_links["prev"] = all_links[0][0]
                        nav_links["up"] = all_links[1][0]
                        nav_links["next"] = all_links[2][0]

                # Validate targets exist
                nav_line = line_of(content, nav_match.start())
                # Identify book endpoints: very first section (Part I, Chapter 0, Section 0.1)
                # and very last section (Part XIII, Chapter 86, Section 86.5).
                # These legitimately have no prev / next within the linear chain.
                rp = rel_path.replace("\\", "/")
                is_first_section = rp.endswith("part-1-foundations/module-00-ml-pytorch-foundations/section-0.1.html")
                is_last_section = rp.endswith("part-13-frontiers/module-86-tools-of-the-trade/section-86.5.html")
                for rel_key in ("prev", "up", "next"):
                    if rel_key not in nav_links:
                        if rel_key == "prev" and is_first_section:
                            continue  # first section has no prev
                        if rel_key == "next" and is_last_section:
                            continue  # last section has no next
                        p1.append(f"{rel_path}:{nav_line} - nav missing '{rel_key}' link")
                        continue
                    href = nav_links[rel_key]
                    target = resolve_href(fpath, href)
                    if target is None:
                        continue
                    if not file_exists(target):
                        # Check if it's a dropped ref
                        if any(pat.search(href) for pat, _ in DROPPED_REFS_PATTERNS):
                            p0.append(f"{rel_path}:{nav_line} - nav '{rel_key}' points to DROPPED resource {href}")
                        else:
                            p0.append(f"{rel_path}:{nav_line} - nav '{rel_key}' BROKEN: {href}")

                # Validate ordering for prev/next within same chapter
                snum = SECTION_NUM_RE.search(fpath.name)
                if snum:
                    chap = int(snum.group(1))
                    sec = int(snum.group(2))
                    # Expected prev: section-CHAP.(sec-1).html if sec > 1; expected next: section-CHAP.(sec+1).html
                    for key, expected_off in (("prev", -1), ("next", 1)):
                        if key not in nav_links:
                            continue
                        href = nav_links[key]
                        m2 = re.search(r"section-(\d+)\.(\d+)\.html", href)
                        if not m2:
                            continue  # could be index.html for first/last section
                        h_chap = int(m2.group(1))
                        h_sec = int(m2.group(2))
                        if h_chap != chap:
                            # crossing chapter is OK only if at boundary; flag for review
                            if (key == "prev" and sec != 1) or (key == "next"):
                                # next can cross to next chapter if last section, prev can cross if first section
                                pass  # we don't know last-section index without yaml
                            continue
                        if h_sec != sec + expected_off:
                            p1.append(
                                f"{rel_path}:{nav_line} - nav '{key}' is section-{h_chap}.{h_sec} but expected section-{chap}.{sec + expected_off}"
                            )
                    # up should point at an index.html
                    if "up" in nav_links:
                        if "index" not in nav_links["up"].lower():
                            p3.append(f"{rel_path}:{nav_line} - nav 'up' does not look like a chapter index: {nav_links['up']}")

    # ---- Aggregate broken images ----
    p1_image_lines: list[str] = []
    for dir_key in sorted(broken_image_by_dir.keys()):
        items = broken_image_by_dir[dir_key]
        p1_image_lines.append(f"### broken images in `{dir_key}` ({len(items)})")
        for it in items[:40]:
            p1_image_lines.append(f"- {it}")
        if len(items) > 40:
            p1_image_lines.append(f"- ... and {len(items) - 40} more")

    # Cap report at 600 lines. Reserve some for headers.
    out_lines: list[str] = []
    out_lines.append("# HTML Integrity Audit (post-v9 reshuffle)")
    out_lines.append("")
    out_lines.append("Generated by `scripts/html_integrity_audit.py`. Read-only.")
    out_lines.append("")
    out_lines.append("## Summary")
    out_lines.append(f"- P0 critical (broken nav / dropped-ref links): {len(p0)}")
    total_p1 = len(p1) + sum(len(v) for v in broken_image_by_dir.values())
    out_lines.append(f"- P1 broken cross-refs / broken images: {total_p1}")
    out_lines.append(f"- P2 placeholders / TODOs: {len(p2)}")
    out_lines.append(f"- P3 minor drift: {len(p3)}")
    out_lines.append(f"- Files scanned: {len(files)}")
    out_lines.append("")

    def emit_section(title: str, items: list[str], budget: int) -> int:
        if not items:
            out_lines.append(f"## {title}")
            out_lines.append("- (none found)")
            out_lines.append("")
            return 0
        out_lines.append(f"## {title}")
        if len(items) <= budget:
            out_lines.extend(f"- {x}" for x in items)
            used = len(items)
        else:
            out_lines.extend(f"- {x}" for x in items[:budget])
            out_lines.append(f"- ... and {len(items) - budget} more (truncated)")
            used = budget + 1
        out_lines.append("")
        return used

    # Budgets (rough, capped at 600 total report lines)
    p0_budget = min(150, len(p0))
    p1_budget = 200
    p2_budget = 90
    p3_budget = 50

    emit_section("P0: Critical (dropped-ref links, broken nav, etc.)", p0, p0_budget)
    # P1 section starts
    out_lines.append("## P1: Broken refs / images")
    if not p1 and not broken_image_by_dir:
        out_lines.append("- (none found)")
        out_lines.append("")
    else:
        # Non-image P1 first
        n_non_img = min(p1_budget, len(p1))
        out_lines.extend(f"- {x}" for x in p1[:n_non_img])
        if len(p1) > n_non_img:
            out_lines.append(f"- ... and {len(p1) - n_non_img} more (truncated)")
        out_lines.append("")
        if broken_image_by_dir:
            out_lines.append("### Broken images by directory")
            for line in p1_image_lines:
                out_lines.append(line)
            out_lines.append("")

    emit_section("P2: Placeholders / leftovers", p2, p2_budget)
    emit_section("P3: Minor drift", p3, p3_budget)

    # Cap at 600 lines
    if len(out_lines) > 600:
        kept = out_lines[:598]
        kept.append("")
        kept.append(f"... report truncated at 600 lines (total findings remain in counters above)")
        out_lines = kept

    REPORT_PATH.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    print(f"Report written to {REPORT_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
