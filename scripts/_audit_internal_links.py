"""Read-only audit of every internal <a href> in BODY content across LLMBook.

Walks every .html under E:/Projects/BookBlogsHome/LLMBook/, skipping the
KDP / .claude / temp_* / scripts / *backups* / node_modules / pagefind /
templates directories. For every <a href> inside <body> that is NOT inside
one of the structural shells already covered by the chapter-nav/footer
audits (<header class="chapter-header">, <nav class="chapter-nav">,
<nav class="header-nav">, <footer>), classify the href and verify it
resolves on disk (and, if anchored, that the anchor exists in the target).

Writes a compact, deduplicated report to
E:/Projects/BookBlogsHome/LLMBook/internal-link-audit.md. The script makes
zero modifications and zero network calls.
"""
from __future__ import annotations

import os
import re
from collections import defaultdict, Counter
from pathlib import Path
from urllib.parse import urlsplit, unquote

from bs4 import BeautifulSoup

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
OUT_PATH = ROOT / "internal-link-audit.md"

# Directories to skip wholesale anywhere in the tree.
EXCLUDE_DIR_NAMES = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind", "templates",
    "vendor", "images", ".git", ".github", ".html2pub_cache", "agents",
    "styles", "downloads", "_concept-figs",
}
# Excluded prefixes (substring on the path component).
EXCLUDE_PREFIXES = ("temp_",)


def is_excluded_dir(name: str) -> bool:
    if name in EXCLUDE_DIR_NAMES:
        return True
    if any(name.startswith(p) for p in EXCLUDE_PREFIXES):
        return True
    if "backups" in name:
        return True
    return False


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not is_excluded_dir(d)]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(Path(dirpath) / fn)
    return sorted(out)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


# Selectors that mark structural shell. Any <a> inside one of these is
# considered already covered by the earlier nav/footer audits, so we skip it.
STRUCTURAL_SELECTORS = [
    ("header", "chapter-header"),
    ("nav", "chapter-nav"),
    ("nav", "header-nav"),
    ("footer", None),  # any <footer>
]


def mark_structural_anchors(soup: BeautifulSoup) -> set[int]:
    """Return id() values of <a> tags inside structural shell elements."""
    marked: set[int] = set()
    for tag_name, cls in STRUCTURAL_SELECTORS:
        if cls is None:
            shells = soup.find_all(tag_name)
        else:
            shells = soup.find_all(tag_name, class_=cls)
        for shell in shells:
            for a in shell.find_all("a"):
                marked.add(id(a))
    return marked


def collect_anchors(soup: BeautifulSoup) -> set[str]:
    """Collect every id="..." and name="..." anchor in a soup."""
    out: set[str] = set()
    for el in soup.find_all(attrs={"id": True}):
        v = el.get("id")
        if v:
            out.add(v.strip())
    for el in soup.find_all("a", attrs={"name": True}):
        v = el.get("name")
        if v:
            out.add(v.strip())
    return out


def classify_href(href: str) -> str:
    if not href or href.strip() == "":
        return "empty"
    h = href.strip()
    sp = urlsplit(h)
    if sp.scheme in ("http", "https", "mailto", "tel", "javascript", "data", "ftp", "ftps", "ws", "wss"):
        return "external"
    if h.startswith("//"):
        return "external"  # protocol-relative
    if h.startswith("#"):
        return "anchor"
    if h.startswith("/"):
        return "absolute"
    if "#" in h:
        return "relfile_anchor"
    return "relfile"


def resolve_relative_path(page_path: Path, raw_path: str) -> Path | None:
    """Resolve a relative path part (no fragment, no query) against page dir."""
    if not raw_path:
        return None
    base = page_path.parent
    try:
        target = (base / raw_path).resolve()
    except Exception:
        return None
    # If trailing slash, treat as dir/index.html.
    if raw_path.endswith("/"):
        return target / "index.html"
    if target.exists() and target.is_dir():
        return target / "index.html"
    if not target.suffix and not target.exists():
        as_dir = target / "index.html"
        if as_dir.exists():
            return as_dir
    return target


def resolve_absolute_path(raw_path: str) -> Path | None:
    p = raw_path.lstrip("/")
    target = (ROOT / p).resolve()
    if raw_path.endswith("/"):
        return target / "index.html"
    if target.exists() and target.is_dir():
        return target / "index.html"
    if not target.suffix and not target.exists():
        as_dir = target / "index.html"
        if as_dir.exists():
            return as_dir
    return target


# Cache: target file path -> set of anchors (or None if file missing/unreadable).
_anchor_cache: dict[Path, set[str] | None] = {}


def anchors_for(target: Path) -> set[str] | None:
    if target in _anchor_cache:
        return _anchor_cache[target]
    if not target.exists() or not target.is_file():
        _anchor_cache[target] = None
        return None
    try:
        html = target.read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(html, "html.parser")
        anchors = collect_anchors(soup)
    except Exception:
        _anchor_cache[target] = None
        return None
    _anchor_cache[target] = anchors
    return anchors


def main() -> None:
    pages = iter_html_files()
    print(f"Found {len(pages)} HTML pages to scan.")

    # Counts
    total_hrefs = 0
    n_external = 0
    n_empty = 0
    n_anchor = 0
    n_anchor_broken = 0
    n_relfile = 0
    n_relfile_broken = 0
    n_relfile_anchor = 0
    n_relfile_anchor_broken_file = 0
    n_relfile_anchor_broken_anchor = 0
    n_absolute = 0
    n_absolute_broken = 0

    broken_file_targets: list[tuple[str, int, str, str]] = []   # (src_rel, line, href, resolved_rel_or_path)
    broken_anchor_targets: list[tuple[str, int, str, str, str]] = []  # (src_rel, line, href, resolved_target_rel, anchor)
    broken_self_anchor: list[tuple[str, int, str]] = []         # (src_rel, line, href)

    # Pattern counters
    pattern_broken_file: Counter[str] = Counter()
    pattern_broken_anchor: Counter[str] = Counter()  # "target_rel#anchor"

    for idx, page in enumerate(pages):
        if idx % 50 == 0:
            print(f"  [{idx}/{len(pages)}] {rel(page)}")
        try:
            html = page.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  ! failed to read {page}: {e}")
            continue
        try:
            soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            print(f"  ! failed to parse {page}: {e}")
            continue

        body = soup.body
        if body is None:
            continue

        # Pre-collect self anchors for "#fragment" links
        self_anchors = collect_anchors(soup)

        structural_ids = mark_structural_anchors(soup)

        # We want line numbers; BeautifulSoup's html.parser gives sourceline.
        # If not available, fall back to None.
        for a in body.find_all("a"):
            if id(a) in structural_ids:
                continue
            href = a.get("href")
            if href is None:
                continue
            href = href.strip()
            if not href:
                continue
            total_hrefs += 1
            line_no = getattr(a, "sourceline", None) or 0

            cls = classify_href(href)
            if cls == "external":
                n_external += 1
                continue
            if cls == "empty":
                n_empty += 1
                continue
            if cls == "anchor":
                n_anchor += 1
                frag = href[1:]
                # url-decode any percent-encoded fragment
                frag_dec = unquote(frag).strip()
                if frag_dec and frag_dec not in self_anchors:
                    n_anchor_broken += 1
                    broken_self_anchor.append((rel(page), line_no, href))
                continue
            if cls == "absolute":
                n_absolute += 1
                # Strip fragment
                sp = urlsplit(href)
                target = resolve_absolute_path(unquote(sp.path)) if sp.path else None
                frag = unquote(sp.fragment).strip()
                if target is None or not target.exists():
                    n_absolute_broken += 1
                    resolved = rel(target) if target else "(unresolved)"
                    broken_file_targets.append((rel(page), line_no, href, resolved))
                    pattern_broken_file[href] += 1
                else:
                    if frag:
                        anchors = anchors_for(target)
                        if anchors is not None and frag not in anchors:
                            n_relfile_anchor_broken_anchor += 1
                            broken_anchor_targets.append((rel(page), line_no, href, rel(target), frag))
                            pattern_broken_anchor[f"{rel(target)}#{frag}"] += 1
                continue

            # relfile or relfile_anchor
            sp = urlsplit(href)
            path_part = unquote(sp.path)
            frag = unquote(sp.fragment).strip()

            if cls == "relfile":
                n_relfile += 1
                target = resolve_relative_path(page, path_part)
                if target is None or not target.exists():
                    n_relfile_broken += 1
                    resolved = rel(target) if target else "(unresolved)"
                    broken_file_targets.append((rel(page), line_no, href, resolved))
                    pattern_broken_file[href] += 1
                continue

            # relfile_anchor
            n_relfile_anchor += 1
            # Case: href starts with "#"? already handled above.
            # Case: path_part is empty, fragment-only on a page with a path,
            # but since we routed "#..." to cls=='anchor', this branch implies
            # path_part is non-empty.
            target = resolve_relative_path(page, path_part)
            if target is None or not target.exists():
                n_relfile_anchor_broken_file += 1
                resolved = rel(target) if target else "(unresolved)"
                broken_file_targets.append((rel(page), line_no, href, resolved))
                pattern_broken_file[href] += 1
                continue
            # File exists. Now check anchor.
            anchors = anchors_for(target)
            if anchors is None:
                # could not load - treat as broken-anchor (rare)
                n_relfile_anchor_broken_anchor += 1
                broken_anchor_targets.append((rel(page), line_no, href, rel(target), frag))
                pattern_broken_anchor[f"{rel(target)}#{frag}"] += 1
                continue
            if frag and frag not in anchors:
                n_relfile_anchor_broken_anchor += 1
                broken_anchor_targets.append((rel(page), line_no, href, rel(target), frag))
                pattern_broken_anchor[f"{rel(target)}#{frag}"] += 1

    # ------ Build report ------
    total_broken = (
        n_anchor_broken
        + n_relfile_broken
        + n_relfile_anchor_broken_file
        + n_relfile_anchor_broken_anchor
        + n_absolute_broken
    )

    lines: list[str] = []
    lines.append("# Internal link audit (inline body links, read-only)")
    lines.append("")
    lines.append(f"Root: `{ROOT.as_posix()}` | Scanned: {len(pages)} HTML files")
    lines.append("")
    lines.append("Scope: every `<a href>` inside `<body>` that is NOT inside ")
    lines.append("`<header class=\"chapter-header\">`, `<nav class=\"chapter-nav\">`, ")
    lines.append("`<nav class=\"header-nav\">`, or `<footer>` (those are covered ")
    lines.append("by the chapter-nav / footer / header-nav audits).")
    lines.append("")

    lines.append("## 1. Summary")
    lines.append("")
    lines.append("| Category | Total | Broken |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Inline body `<a href>` scanned | {total_hrefs} | - |")
    lines.append(f"| External (http/https/mailto/tel/data/etc., skipped) | {n_external} | - |")
    lines.append(f"| Empty `href` (excluded from broken count) | {n_empty} | - |")
    lines.append(f"| Pure-anchor `#frag` (same-page) | {n_anchor} | {n_anchor_broken} |")
    lines.append(f"| Relative-file (no anchor) | {n_relfile} | {n_relfile_broken} |")
    lines.append(f"| Relative-file with anchor | {n_relfile_anchor} | {n_relfile_anchor_broken_file + n_relfile_anchor_broken_anchor} |")
    lines.append(f"|     ... target file missing | - | {n_relfile_anchor_broken_file} |")
    lines.append(f"|     ... file ok, anchor missing | - | {n_relfile_anchor_broken_anchor} |")
    lines.append(f"| Absolute-path `/...` | {n_absolute} | {n_absolute_broken} |")
    lines.append(f"| **Total broken inline links** | - | **{total_broken}** |")
    lines.append("")

    # Patterns first - bubble up the biggest repeated issues.
    lines.append("## 2. Common broken patterns (top repeated targets)")
    lines.append("")

    # Source-file grouping: how many broken links does each source page own?
    by_source: Counter[str] = Counter()
    for src, _line, _href, _resolved in broken_file_targets:
        by_source[src] += 1
    for src, _line, _href, _t_rel, _frag in broken_anchor_targets:
        by_source[src] += 1
    for src, _line, _href in broken_self_anchor:
        by_source[src] += 1

    if by_source:
        lines.append("### 2.1  Source pages with the most broken inline links")
        lines.append("")
        lines.append("| Broken | Source page |")
        lines.append("|---:|---|")
        for src, c in by_source.most_common(20):
            lines.append(f"| {c} | `{src}` |")
        lines.append("")

    # Directory prefix heuristic: does the resolved path consistently fail
    # under a known directory? E.g. all `front-matter/.../../glossary/...`
    # references resolve to root `glossary/` instead of `appendices/glossary/`.
    resolved_dir_counts: Counter[str] = Counter()
    for _src, _line, _href, resolved in broken_file_targets:
        if not resolved or resolved == "(unresolved)":
            continue
        # First path component of the resolved relative path.
        first = resolved.split("/")[0] if "/" in resolved else resolved
        resolved_dir_counts[first] += 1
    if resolved_dir_counts:
        lines.append("### 2.2  Broken file targets grouped by first directory of resolved path")
        lines.append("")
        lines.append("(Useful for spotting `../` over- or under-stepping. E.g. references that resolve to ")
        lines.append("`glossary/...` at the project root when the real folder is `appendices/glossary/`.)")
        lines.append("")
        lines.append("| Broken | Resolves under |")
        lines.append("|---:|---|")
        for d, c in resolved_dir_counts.most_common():
            lines.append(f"| {c} | `{d}/` |")
        lines.append("")

    top_file_patterns = [(p, c) for p, c in pattern_broken_file.most_common() if c >= 2]
    top_anchor_patterns = [(p, c) for p, c in pattern_broken_anchor.most_common() if c >= 2]

    if not top_file_patterns and not top_anchor_patterns:
        lines.append("### 2.3  Repeating hrefs")
        lines.append("")
        lines.append("_No exact href is broken on 2 or more pages._")
        lines.append("")
    else:
        if top_file_patterns:
            lines.append("### 2.3  Broken file targets that repeat across pages")
            lines.append("")
            lines.append("| Pages | href |")
            lines.append("|---:|---|")
            for href, count in top_file_patterns[:40]:
                lines.append(f"| {count} | `{href}` |")
            if len(top_file_patterns) > 40:
                lines.append(f"| ... | _and {len(top_file_patterns) - 40} more repeating broken file targets_ |")
            lines.append("")
        if top_anchor_patterns:
            lines.append("### 2.4  Broken anchor targets that repeat across pages")
            lines.append("")
            lines.append("| Pages | target#anchor |")
            lines.append("|---:|---|")
            for ta, count in top_anchor_patterns[:40]:
                lines.append(f"| {count} | `{ta}` |")
            if len(top_anchor_patterns) > 40:
                lines.append(f"| ... | _and {len(top_anchor_patterns) - 40} more repeating broken anchor targets_ |")
            lines.append("")

    # --- broken file targets ---
    lines.append("## 3. Broken file targets (file not found on disk)")
    lines.append("")
    lines.append(f"Total: {n_relfile_broken + n_relfile_anchor_broken_file + n_absolute_broken}")
    lines.append("")
    lines.append("Format: `source_page.html:LINE  href -> resolved_path`")
    lines.append("")
    broken_file_targets_sorted = sorted(broken_file_targets, key=lambda t: (t[0], t[1]))
    cap = 200
    shown = broken_file_targets_sorted[:cap]
    for src, line, href, resolved in shown:
        lines.append(f"- `{src}:{line}`  `{href}` -> `{resolved}`")
    if len(broken_file_targets_sorted) > cap:
        lines.append(f"")
        lines.append(f"_... {len(broken_file_targets_sorted) - cap} more broken-file entries omitted (cap = {cap}); see counts above._")
    if not broken_file_targets_sorted:
        lines.append("_None._")
    lines.append("")

    # --- broken self-anchors ---
    lines.append("## 4. Broken same-page `#anchor` links")
    lines.append("")
    lines.append(f"Total: {n_anchor_broken}")
    lines.append("")
    if broken_self_anchor:
        for src, line, href in sorted(broken_self_anchor, key=lambda t: (t[0], t[1]))[:cap]:
            lines.append(f"- `{src}:{line}`  `{href}`")
        if len(broken_self_anchor) > cap:
            lines.append("")
            lines.append(f"_... {len(broken_self_anchor) - cap} more entries omitted (cap = {cap})._")
    else:
        lines.append("_None._")
    lines.append("")

    # --- broken anchors on existing target files ---
    lines.append("## 5. Broken anchor targets (file exists, anchor missing)")
    lines.append("")
    lines.append(f"Total: {n_relfile_anchor_broken_anchor}")
    lines.append("")
    lines.append("Format: `source_page.html:LINE  href  (target file ok, anchor missing)`")
    lines.append("")
    broken_anchor_sorted = sorted(broken_anchor_targets, key=lambda t: (t[0], t[1]))
    shown_a = broken_anchor_sorted[:cap]
    for src, line, href, t_rel, frag in shown_a:
        lines.append(f"- `{src}:{line}`  `{href}`  (target `{t_rel}`, anchor `{frag}` not found)")
    if len(broken_anchor_sorted) > cap:
        lines.append("")
        lines.append(f"_... {len(broken_anchor_sorted) - cap} more broken-anchor entries omitted (cap = {cap}); see counts above._")
    if not broken_anchor_sorted:
        lines.append("_None._")
    lines.append("")

    # --- Recommendations ---
    lines.append("## 6. Recommended fixes")
    lines.append("")
    recs: list[str] = []

    # Front-matter "../glossary" / "../appendix-*/" miss-step detection.
    fm_misstep_glossary = 0
    fm_misstep_appendix = 0
    fm_sources = set()
    for src, _line, href, _resolved in broken_file_targets:
        if not src.startswith("front-matter/"):
            continue
        if href.startswith("../glossary/"):
            fm_misstep_glossary += 1
            fm_sources.add(src)
        elif href.startswith("../appendix-"):
            fm_misstep_appendix += 1
            fm_sources.add(src)
    fm_misstep_total = fm_misstep_glossary + fm_misstep_appendix
    if fm_misstep_total >= 5:
        recs.append(
            f"Fix the `front-matter/` mis-stepped relative paths ({fm_misstep_total} broken "
            f"links across {len(fm_sources)} pages, e.g. {', '.join(sorted(fm_sources))}): "
            f"links currently use `../glossary/...` and `../appendix-X/...`, which resolve to "
            f"`glossary/...` and `appendix-X/...` at the project root. The real files live under "
            f"`appendices/glossary/` and `appendices/appendix-X/`. The references read as if these pages "
            f"were copied from inside `appendices/`. Change `../glossary/` -> `../appendices/glossary/` "
            f"and `../appendix-X/` -> `../appendices/appendix-X/` in the affected front-matter files."
        )

    # Auto-derived: largest broken file pattern - only call out if it isn't
    # already covered by the front-matter mis-step pattern (otherwise it's
    # noise restating the same problem).
    if top_file_patterns:
        top_href, top_count = top_file_patterns[0]
        already_covered = (
            top_href.startswith("../glossary/") or top_href.startswith("../appendix-")
        ) and fm_misstep_total
        if not already_covered and top_count >= 3:
            recs.append(
                f"Fix the most-repeated broken file pattern: `{top_href}` is referenced from "
                f"{top_count} inline links. Either create that target file or rewrite the references."
            )
    if top_anchor_patterns:
        top_anchor, top_anchor_count = top_anchor_patterns[0]
        recs.append(
            f"Fix the most-repeated broken anchor pattern: `{top_anchor}` is referenced "
            f"from {top_anchor_count} pages. Either add the missing `id`/`name` anchor to the target file, "
            f"or update the references."
        )
    # Heuristic: glossary anchor pattern
    glossary_broken_anchor_count = sum(
        c for k, c in pattern_broken_anchor.items() if "appendices/glossary/" in k
    )
    if glossary_broken_anchor_count:
        recs.append(
            f"Audit glossary cross-references: {glossary_broken_anchor_count} broken anchor references "
            f"resolve to a glossary file but the `#gl-...` term anchor is missing. "
            f"Likely the glossary section file exists but the specific term was renamed or never defined."
        )
    glossary_broken_file_count = sum(
        c for k, c in pattern_broken_file.items() if "appendices/glossary/" in k
    )
    if glossary_broken_file_count:
        recs.append(
            f"Audit glossary file paths: {glossary_broken_file_count} inline references point to a "
            f"glossary file path that no longer exists (file renamed or merged)."
        )
    # Module renumbering hint (only meaningful if not already covered by FM mis-step)
    module_broken_count = sum(c for k, c in pattern_broken_file.items() if "/module-" in k)
    if module_broken_count >= 5:
        recs.append(
            f"Look for chapter/module renumbering: {module_broken_count} inline broken links point at "
            f"missing `module-XX-...` directories. This usually means a chapter was renumbered or renamed "
            f"and inline cross-references were not updated."
        )
    appendix_broken_count = sum(c for k, c in pattern_broken_file.items() if "/appendix-" in k)
    # Subtract front-matter mis-step matches to avoid double-counting.
    appendix_broken_count -= fm_misstep_appendix
    if appendix_broken_count >= 5:
        recs.append(
            f"Look for appendix renumbering: {appendix_broken_count} inline broken links (after subtracting "
            f"the front-matter mis-step pattern) point at missing `appendix-XX-...` files. "
            f"Confirm against the appendix-letter map."
        )
    # Detect homepage KDP miss
    for src, _line, href, _resolved in broken_file_targets:
        if src == "index.html" and href.startswith("KDP/"):
            recs.append(
                f"`index.html` line references `{href}` which lives under the `KDP/` build output "
                f"(excluded from this audit's tree). Confirm the homepage should link to `KDP/output/...` "
                f"in the published artifact, or rewrite to a non-KDP target."
            )
            break

    recs.append(
        "After pattern fixes, sweep the residual one-off broken links in Section 3 and Section 5; "
        "they are typically typos (missing `.html`, wrong section number, or stale anchor ids)."
    )
    recs.append(
        f"Re-run `scripts/_audit_internal_links.py` after each batch of fixes to track progress; "
        f"current baseline: {total_broken} broken inline links."
    )
    for r in recs[:7]:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("---")
    lines.append(f"_Audit script: `scripts/_audit_internal_links.py`. Inline hrefs scanned: {total_hrefs}; pages: {len(pages)}._")

    report = "\n".join(lines) + "\n"
    OUT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(report)} bytes, {report.count(chr(10))} lines).")
    print(f"Total inline body hrefs scanned: {total_hrefs}")
    print(f"Total broken inline links: {total_broken}")


if __name__ == "__main__":
    main()
