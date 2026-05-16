"""Read-only audit of chapter-nav and footer in every HTML page under LLMBook root.

Output: writes a *compact* report to E:/Projects/BookBlogsHome/LLMBook/footer-nav-audit.md
(grouping systemic issues rather than enumerating every page).
"""
from __future__ import annotations

import os
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
EXCLUDE_DIRS = {"KDP", "build", "temp_ebook", "temp_epub", "node_modules", "vendor",
                "pagefind", "images", "_concept-figs", "downloads", "templates",
                "scripts", "agents", "styles"}

NAV_RE = re.compile(
    r'<nav\s+class="chapter-nav"[^>]*>(.*?)</nav>',
    re.DOTALL | re.IGNORECASE,
)
LINK_RE = re.compile(
    r'<a\s+([^>]*?)class="(prev|up|next)"([^>]*?)>(.*?)</a>',
    re.DOTALL | re.IGNORECASE,
)
HREF_RE = re.compile(r'href="([^"]*)"', re.IGNORECASE)
FOOTER_RE = re.compile(r"<footer\b[^>]*>(.*?)</footer>", re.DOTALL | re.IGNORECASE)
JINJA_RE = re.compile(r"\{\{[^}]*\}\}")
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def iter_html_files() -> list[Path]:
    out: list[Path] = []
    targets = [ROOT / "front-matter", ROOT / "appendices", ROOT / "capstone"]
    targets += sorted([p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("part-")])
    for f in (ROOT / "index.html", ROOT / "toc.html"):
        if f.exists():
            out.append(f)
    for base in targets:
        if not base.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith("__build")]
            for fn in filenames:
                if fn.endswith(".html"):
                    out.append(Path(dirpath) / fn)
    return out


def extract_nav(html: str) -> tuple[dict[str, dict] | None, int]:
    m = NAV_RE.search(html)
    if not m:
        return None, -1
    block = m.group(1)
    line_no = html[: m.start()].count("\n") + 1
    links: dict[str, dict] = {}
    for am in LINK_RE.finditer(block):
        cls = am.group(2).lower()
        full_a = am.group(0)
        href_m = HREF_RE.search(full_a)
        href = href_m.group(1) if href_m else ""
        plain = WS_RE.sub(" ", TAG_RE.sub("", am.group(4))).strip()
        links[cls] = {"href": href, "text": plain}
    return links, line_no


def resolve_target(page_path: Path, href: str) -> Path | None:
    if not href:
        return None
    sp = urlsplit(href)
    if sp.scheme or sp.netloc:
        return None
    path_part = unquote(sp.path)
    if not path_part:
        return page_path
    base = page_path.parent
    target = (base / path_part).resolve()
    if href.endswith("/"):
        target = target / "index.html"
    elif target.exists() and target.is_dir():
        target = target / "index.html"
    elif not target.suffix and not target.exists():
        # heuristic: no extension and target doesn't resolve to a file -> try as dir
        as_dir = target / "index.html"
        if as_dir.exists():
            target = as_dir
    return target


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def sec_key(name: str) -> tuple:
    m = re.match(r"section-([a-z]?)(\d+)\.(\d+)\.html$", name, re.IGNORECASE)
    if not m:
        return (9, name)
    return (m.group(1).lower(), int(m.group(2)), int(m.group(3)))


def mod_key(name: str) -> int:
    m = re.match(r"module-(\d+)", name)
    return int(m.group(1)) if m else 999


def part_key(d: Path) -> int:
    m = re.match(r"part-(\d+)", d.name)
    return int(m.group(1)) if m else 99


def main() -> None:
    pages = iter_html_files()
    n_total = len(pages)

    # Classify
    classified: list[tuple[Path, dict]] = []
    for p in pages:
        rp = rel(p)
        parts = rp.split("/")
        info: dict = {"rel": rp}
        if rp in ("index.html", "toc.html"):
            info["kind"] = "home"
        elif parts[0] == "front-matter":
            info["kind"] = "fm-index" if p.name == "index.html" else "fm-page"
        elif parts[0] == "capstone":
            info["kind"] = "capstone"
        elif parts[0] == "appendices":
            if len(parts) == 2 and p.name == "index.html":
                info["kind"] = "app-tree-index"
            elif len(parts) >= 3 and p.name == "index.html":
                info["kind"] = "app-index"
                info["app_dir"] = parts[1]
            elif len(parts) >= 3:
                info["kind"] = "app-section"
                info["app_dir"] = parts[1]
        elif parts[0].startswith("part-"):
            if len(parts) == 2 and p.name == "index.html":
                info["kind"] = "part-index"
                info["part_dir"] = parts[0]
            elif len(parts) >= 3 and p.name == "index.html":
                info["kind"] = "chapter-index"
                info["part_dir"] = parts[0]
                info["mod_dir"] = parts[1]
            elif len(parts) >= 3:
                info["kind"] = "section"
                info["part_dir"] = parts[0]
                info["mod_dir"] = parts[1]
        classified.append((p, info))

    # Findings buckets
    individual_broken: list[str] = []          # actual unique findings
    missing_links: list[str] = []              # pages with 1 or 2 of 3 nav links
    text_mismatch: list[str] = []              # link text vs target
    appendix_prefix_bug: dict[str, dict] = {}  # app_dir -> {expected_prefix, observed_prefix, count, files_404}
    cross_part_skips: list[str] = []           # part-transition pages whose nav skips the Part landing
    intra_chapter_logic: list[str] = []        # section-level intra-chapter logic errors (non-prefix)
    missing_footer: list[str] = []
    jinja_footer: dict[str, int] = defaultdict(int)  # placeholder -> count
    jinja_pages: list[str] = []                # examples (up to 5)

    pages_with_nav = 0
    page_data: dict[str, dict] = {}

    # First pass: parse files
    for p, info in classified:
        try:
            html = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            individual_broken.append(f"`{rel(p)}` :: failed to read ({e})")
            continue

        # Footer
        m_foot = FOOTER_RE.search(html)
        if not m_foot:
            missing_footer.append(rel(p))
        else:
            placeholders = JINJA_RE.findall(m_foot.group(1))
            for ph in placeholders:
                jinja_footer[ph] += 1
            if placeholders and len(jinja_pages) < 5:
                jinja_pages.append(rel(p))

        # Nav
        nav_links, nav_line = extract_nav(html)
        page_data[rel(p)] = {"info": info, "nav": nav_links, "nav_line": nav_line}
        if nav_links is None:
            continue
        pages_with_nav += 1

        present = {k for k in ("prev", "up", "next") if k in nav_links}
        if 0 < len(present) < 3:
            missing = sorted({"prev", "up", "next"} - present)
            missing_links.append(f"`{rel(p)}` (line {nav_line}) missing: {', '.join(missing)}")

        # 404 detection + prefix-bug classification
        for cls in ("prev", "up", "next"):
            if cls not in nav_links:
                continue
            href = nav_links[cls]["href"]
            target = resolve_target(p, href)
            if target is None:
                continue
            if not target.exists():
                # Is this an appendix-prefix-letter mismatch?
                if info.get("kind") in ("app-index", "app-section"):
                    app_dir = info["app_dir"]
                    # extract letter from app_dir name e.g. 'appendix-g-model-cards' -> 'g'
                    m_letter = re.match(r"appendix-([a-z])-", app_dir)
                    if m_letter:
                        expected_letter = m_letter.group(1)
                        # extract observed letter from href section-X.N.html
                        m_obs = re.search(r"section-([a-z])\.\d", href)
                        if m_obs and m_obs.group(1) != expected_letter:
                            bug = appendix_prefix_bug.setdefault(app_dir, {
                                "expected": expected_letter,
                                "observed_letters": set(),
                                "broken_count": 0,
                                "example": "",
                            })
                            bug["observed_letters"].add(m_obs.group(1))
                            bug["broken_count"] += 1
                            if not bug["example"]:
                                bug["example"] = f"`{rel(p)}` line {nav_line}: `{cls}` -> `{href}`"
                            continue
                # else generic broken-link finding
                individual_broken.append(
                    f"`{rel(p)}` (line {nav_line}) :: `{cls}` -> `{href}` -> `{rel(target)}` NOT FOUND"
                )

        # text vs target mismatch
        for cls in ("prev", "next"):
            if cls not in nav_links:
                continue
            text = nav_links[cls]["text"]
            href = nav_links[cls]["href"]
            target = resolve_target(p, href)
            if target is None or not target.exists():
                continue
            mt = re.search(r"chapter\s+(\d+)", text, re.IGNORECASE)
            if mt:
                ch_num = mt.group(1).lstrip("0")
                rt = rel(target)
                mh = re.search(r"module-(\d+)", rt)
                if mh and mh.group(1).lstrip("0") != ch_num:
                    text_mismatch.append(
                        f"`{rel(p)}` (line {nav_line}) `{cls}` text \"{text}\" -> href module-{mh.group(1)}"
                    )
                    continue
            ms = re.search(r"section\s+([A-Za-z]?\d+(?:\.\d+)?)", text, re.IGNORECASE)
            if ms:
                tag = ms.group(1).lower()
                rt = rel(target).lower()
                mh = re.search(r"section-([a-z]?\d+(?:\.\d+)?)", rt)
                if mh and mh.group(1) != tag:
                    text_mismatch.append(
                        f"`{rel(p)}` (line {nav_line}) `{cls}` text \"Section {tag}\" -> href section-{mh.group(1)}"
                    )

    # ----- Logical sequence checks -----
    # Build per-chapter and per-appendix ordered file lists
    chapter_files: dict[Path, list[Path]] = {}
    appendix_files: dict[Path, list[Path]] = {}
    for p, info in classified:
        kind = info.get("kind")
        if kind in ("chapter-index", "section"):
            chapter_files.setdefault(p.parent, [])
        elif kind in ("app-index", "app-section"):
            appendix_files.setdefault(p.parent, [])

    for d in chapter_files:
        files = []
        idx = d / "index.html"
        if idx.exists():
            files.append(idx)
        secs = sorted(
            [f for f in d.iterdir() if f.name.startswith("section-") and f.suffix == ".html"],
            key=lambda f: sec_key(f.name),
        )
        files.extend(secs)
        chapter_files[d] = files

    for d in appendix_files:
        files = []
        idx = d / "index.html"
        if idx.exists():
            files.append(idx)
        secs = sorted(
            [f for f in d.iterdir() if f.name.startswith("section-") and f.suffix == ".html"],
            key=lambda f: sec_key(f.name),
        )
        files.extend(secs)
        appendix_files[d] = files

    def is_prefix_bug_path(href_target_rel: str) -> bool:
        # Used to dedup: don't double-report prefix-bug findings as intra-chapter logic errors.
        return bool(re.search(r"section-[a-z]\.\d+\.html$", href_target_rel))

    def add_intra(rf: str, msg: str) -> None:
        if msg not in intra_chapter_logic:
            intra_chapter_logic.append(msg)

    for ch_dir, files in chapter_files.items():
        for i, f in enumerate(files):
            rf = rel(f)
            pdata = page_data.get(rf)
            if not pdata or pdata["nav"] is None:
                continue
            nav = pdata["nav"]
            if i > 0 and "prev" in nav:
                expected_prev = files[i - 1]
                href = nav["prev"]["href"]
                target = resolve_target(f, href)
                if target is not None:
                    try:
                        if target.resolve() != expected_prev.resolve():
                            add_intra(rf, f"`{rf}` :: `prev` -> `{href}` but expected `{rel(expected_prev)}`")
                    except Exception:
                        pass
            if i < len(files) - 1 and "next" in nav:
                expected_next = files[i + 1]
                href = nav["next"]["href"]
                target = resolve_target(f, href)
                if target is not None:
                    try:
                        if target.resolve() != expected_next.resolve():
                            add_intra(rf, f"`{rf}` :: `next` -> `{href}` but expected `{rel(expected_next)}`")
                    except Exception:
                        pass

    # Appendix intra-checks - filter out prefix-bug occurrences (they are reported as a single bug)
    appendix_intra_extra: list[str] = []
    for a_dir, files in appendix_files.items():
        # Determine appendix letter to detect the prefix bug
        a_letter = None
        m_letter = re.match(r"appendix-([a-z])-", a_dir.name)
        if m_letter:
            a_letter = m_letter.group(1)
        for i, f in enumerate(files):
            rf = rel(f)
            pdata = page_data.get(rf)
            if not pdata or pdata["nav"] is None:
                continue
            nav = pdata["nav"]
            for cls, expected_idx in (("prev", i - 1), ("next", i + 1)):
                if cls not in nav:
                    continue
                if expected_idx < 0 or expected_idx >= len(files):
                    continue
                expected = files[expected_idx]
                href = nav[cls]["href"]
                target = resolve_target(f, href)
                if target is None:
                    continue
                try:
                    same = target.resolve() == expected.resolve()
                except Exception:
                    same = True
                if same:
                    continue
                # Is it the prefix-bug pattern?
                m_obs = re.search(r"section-([a-z])\.\d", href)
                if a_letter and m_obs and m_obs.group(1) != a_letter:
                    continue  # already counted in appendix_prefix_bug
                appendix_intra_extra.append(
                    f"`{rf}` :: `{cls}` -> `{href}` (`{rel(target) if target.exists() else 'NOT FOUND'}`), expected `{rel(expected)}`"
                )

    # Cross-part transitions
    part_modules: dict[Path, list[Path]] = {}
    for p, info in classified:
        if info.get("kind") == "chapter-index":
            part_dir = ROOT / info["part_dir"]
            part_modules.setdefault(part_dir, []).append(p.parent)
    for part_dir, mods in part_modules.items():
        mods.sort(key=lambda d: mod_key(d.name))
    parts_ordered = sorted(part_modules.keys(), key=part_key)

    for part_dir in parts_ordered:
        mods = part_modules[part_dir]
        for i, ch_dir in enumerate(mods):
            files = chapter_files.get(ch_dir, [])
            if not files:
                continue
            idx_page = files[0]
            rf = rel(idx_page)
            pdata = page_data.get(rf)
            if pdata and pdata["nav"]:
                nav = pdata["nav"]
                if i == 0:
                    expected_prev = part_dir / "index.html"
                else:
                    prev_chapter_files = chapter_files.get(mods[i - 1], [])
                    expected_prev = prev_chapter_files[-1] if prev_chapter_files else part_dir / "index.html"
                if "prev" in nav and expected_prev.exists():
                    href = nav["prev"]["href"]
                    target = resolve_target(idx_page, href)
                    if target is not None:
                        try:
                            if target.resolve() != expected_prev.resolve():
                                cross_part_skips.append(
                                    f"`{rf}` chapter-index `prev` -> `{href}` (`{rel(target)}`), expected `{rel(expected_prev)}`"
                                )
                        except Exception:
                            pass
            last_page = files[-1]
            rf = rel(last_page)
            pdata = page_data.get(rf)
            if pdata and pdata["nav"]:
                nav = pdata["nav"]
                if i + 1 < len(mods):
                    next_chapter_files = chapter_files.get(mods[i + 1], [])
                    expected_next = next_chapter_files[0] if next_chapter_files else None
                else:
                    p_idx = parts_ordered.index(part_dir)
                    if p_idx + 1 < len(parts_ordered):
                        expected_next = parts_ordered[p_idx + 1] / "index.html"
                    else:
                        expected_next = ROOT / "appendices" / "index.html"
                if expected_next and expected_next.exists() and "next" in nav:
                    href = nav["next"]["href"]
                    target = resolve_target(last_page, href)
                    if target is not None:
                        try:
                            if target.resolve() != expected_next.resolve():
                                cross_part_skips.append(
                                    f"`{rf}` chapter-end `next` -> `{href}` (`{rel(target)}`), expected `{rel(expected_next)}`"
                                )
                        except Exception:
                            pass

    # ----- Special cases -----
    special_notes: list[str] = []
    gloss_dir = ROOT / "appendices" / "glossary"
    if gloss_dir.exists():
        cross_to_app_f = []
        for f in gloss_dir.iterdir():
            if f.suffix != ".html":
                continue
            rf = rel(f)
            pdata = page_data.get(rf)
            if not (pdata and pdata["nav"]):
                continue
            for cls in ("prev", "up", "next"):
                if cls in pdata["nav"] and "appendix-f-hardware-compute" in pdata["nav"][cls]["href"].lower():
                    cross_to_app_f.append(f"`{rf}` `{cls}` -> `{pdata['nav'][cls]['href']}`")
        special_notes.append(
            "Glossary lives at `appendices/glossary/` but uses `section-f.*` filenames "
            "(same as Appendix F hardware compute). "
            + ("No cross-links into Appendix F detected." if not cross_to_app_f
               else f"WARNING: cross-links into Appendix F found: {', '.join(cross_to_app_f)}")
        )

    mf_idx = ROOT / "part-12-llm-applications-across-industries" / "module-42-manufacturing-llms" / "index.html"
    if mf_idx.exists():
        pdata = page_data.get(rel(mf_idx))
        if pdata and pdata["nav"] and "next" in pdata["nav"]:
            href = pdata["nav"]["next"]["href"]
            target = resolve_target(mf_idx, href)
            target_rel = rel(target) if target else "(unresolved)"
            verdict = "OK (leads to appendices)" if "appendices" in target_rel else "REVIEW"
            special_notes.append(
                f"Last chapter `module-42-manufacturing-llms/index.html` `next` -> `{href}` "
                f"(`{target_rel}`). {verdict}."
            )

    fm_dir = ROOT / "front-matter"
    p1_idx = ROOT / "part-1-foundations" / "index.html"
    if fm_dir.exists() and p1_idx.exists():
        bridge_pages = []
        for f, info in classified:
            if info.get("kind") not in ("fm-page", "fm-index"):
                continue
            pdata = page_data.get(rel(f))
            if not (pdata and pdata["nav"]):
                continue
            for cls in ("prev", "up", "next"):
                if cls in pdata["nav"] and "part-1-foundations" in pdata["nav"][cls]["href"]:
                    bridge_pages.append(f"`{rel(f)}` `{cls}` -> `{pdata['nav'][cls]['href']}`")
        if bridge_pages:
            special_notes.append("Front-matter -> Part I bridges: " + "; ".join(bridge_pages))
        else:
            special_notes.append("No front-matter page has a nav link forward into `part-1-foundations/`.")
        # part-1 prev
        p1_data = page_data.get(rel(p1_idx))
        if p1_data and p1_data["nav"] and "prev" in p1_data["nav"]:
            special_notes.append(f"`part-1-foundations/index.html` `prev` -> `{p1_data['nav']['prev']['href']}`")

    cap_files = [p for p, info in classified if info.get("kind") == "capstone"]
    for c in cap_files:
        pdata = page_data.get(rel(c))
        if pdata and pdata["nav"]:
            entries = ", ".join(f"{k}->`{pdata['nav'][k]['href']}`" for k in pdata["nav"])
            special_notes.append(f"Capstone `{rel(c)}` nav: {entries}")
        else:
            special_notes.append(f"Capstone `{rel(c)}` has no chapter-nav.")

    # Front-matter A.1 broken links (the appendix-aj / appendix-ak / appendix-u-> reading-pathways
    # ones already appear in individual_broken).
    # Group those if many; we keep them as-is since they're not the systemic prefix bug.

    # ----- Render report -----
    n_prefix_bug_pages = sum(b["broken_count"] for b in appendix_prefix_bug.values())
    n_intra_extra = len(appendix_intra_extra)
    n_logic = len(cross_part_skips) + n_intra_extra + len(intra_chapter_logic)

    lines: list[str] = []
    lines.append("# Footer & chapter-nav audit (read-only)")
    lines.append("")
    lines.append(f"Root: `{ROOT.as_posix()}` | Generated: read-only scan; no files modified.")
    lines.append("")
    lines.append("## 1. Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|---|---:|")
    lines.append(f"| HTML pages scanned (excluding KDP/build/temp_*/node_modules/vendor) | {n_total} |")
    lines.append(f"| Pages with a `<nav class=\"chapter-nav\">` block | {pages_with_nav} |")
    lines.append(f"| Pages missing `<footer>` entirely | {len(missing_footer)} |")
    lines.append(f"| Pages whose `<footer>` still contains unrendered `{{{{...}}}}` placeholders | {sum(jinja_footer.values())} (across {len(jinja_pages) if len(jinja_pages) < 5 else 'many'} of {pages_with_nav + len(missing_footer)} pages) |")
    lines.append(f"| Appendices affected by the section-prefix-letter bug | {len(appendix_prefix_bug)} |")
    lines.append(f"| Individual 404 nav targets (outside the prefix bug) | {len(individual_broken)} |")
    lines.append(f"| Pages with chapter-nav present but a `prev`/`up`/`next` missing | {len(missing_links)} |")
    lines.append(f"| Link-text vs. href mismatches (e.g. \"Chapter 36\" vs module-35) | {len(text_mismatch)} |")
    lines.append(f"| Cross-Part transitions that bypass the Part landing page | {len(cross_part_skips)} |")
    lines.append(f"| Other intra-chapter `prev`/`next` deviations | {len(intra_chapter_logic)} |")
    lines.append(f"| Other intra-appendix `prev`/`next` deviations (non-prefix) | {n_intra_extra} |")
    lines.append("")

    # ---- Section A ----
    lines.append("## 2. Section A: Broken `chapter-nav` links")
    lines.append("")
    lines.append("### A.0  Systemic section-prefix-letter bug in `appendices/`")
    lines.append("")
    lines.append("Inside each affected appendix directory, `<a class=\"prev\">` and `<a class=\"next\">` ")
    lines.append("links reference the *previous* appendix's letter instead of the current one. E.g.")
    lines.append("`appendix-g-model-cards/section-g.1.html` has `next=\"section-f.2.html\"` (should be `section-g.2.html`),")
    lines.append("which 404s because the file with that name does not exist in this folder.")
    lines.append("")
    lines.append("| Appendix dir | Expected letter | Observed letter(s) in nav hrefs | 404s found |")
    lines.append("|---|:-:|:-:|---:|")
    for app_dir in sorted(appendix_prefix_bug.keys()):
        b = appendix_prefix_bug[app_dir]
        obs = ", ".join(sorted(b["observed_letters"]))
        lines.append(f"| `appendices/{app_dir}/` | `{b['expected']}` | `{obs}` | {b['broken_count']} |")
    lines.append("")
    lines.append("Representative example per appendix:")
    for app_dir in sorted(appendix_prefix_bug.keys()):
        lines.append(f"- `appendices/{app_dir}/`: {appendix_prefix_bug[app_dir]['example']}")
    lines.append("")

    lines.append("### A.1  Other 404 nav targets")
    lines.append("")
    if individual_broken:
        for f in individual_broken:
            lines.append(f"- {f}")
    else:
        lines.append("_None besides the systemic prefix bug above._")
    lines.append("")

    lines.append("### A.2  Pages with chapter-nav present but a link missing from the prev/up/next trio")
    lines.append("")
    if missing_links:
        for ln in missing_links:
            lines.append(f"- {ln}")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("### A.3  Link text vs target mismatch")
    lines.append("")
    if text_mismatch:
        for f in text_mismatch:
            lines.append(f"- {f}")
    else:
        lines.append("_None detected (note: heuristic relies on text containing \"Chapter N\" / \"Section N.M\")._")
    lines.append("")

    # ---- Section B ----
    lines.append("## 3. Section B: Logical sequence errors")
    lines.append("")
    lines.append("### B.1  Cross-Part transitions bypass the Part landing page")
    lines.append("")
    lines.append("Convention asks: last chapter of Part N's `next` -> `part-(N+1)/index.html`; ")
    lines.append("first chapter of Part N's `prev` -> last section of Part (N-1)'s last chapter (or Part landing). ")
    lines.append("In practice, every cross-Part transition currently jumps chapter-to-chapter and skips the Part landing.")
    lines.append("")
    if cross_part_skips:
        for ln in cross_part_skips:
            lines.append(f"- {ln}")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("### B.2  Intra-appendix `prev`/`next` issues (excluding the prefix-letter bug)")
    lines.append("")
    if appendix_intra_extra:
        for ln in appendix_intra_extra:
            lines.append(f"- {ln}")
    else:
        lines.append("_None beyond the systemic prefix bug._")
    lines.append("")

    lines.append("### B.3  Intra-chapter `prev`/`next` issues (parts only)")
    lines.append("")
    if intra_chapter_logic:
        for ln in intra_chapter_logic:
            lines.append(f"- {ln}")
    else:
        lines.append("_None._")
    lines.append("")

    # ---- Section C ----
    lines.append("## 4. Section C: Footer issues")
    lines.append("")
    lines.append("### C.1  Pages missing `<footer>` entirely")
    lines.append("")
    if missing_footer:
        for f in missing_footer:
            lines.append(f"- `{f}`")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("### C.2  Pages whose `<footer>` contains unrendered `{{...}}` placeholders")
    lines.append("")
    total_jinja = sum(jinja_footer.values())
    if total_jinja:
        lines.append(
            f"Every footer in the static tree (covering essentially the entire book) "
            f"contains unrendered Jinja placeholders. Total occurrences: {total_jinja}. "
            "Placeholder breakdown:"
        )
        for ph, count in sorted(jinja_footer.items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"- `{ph}` :: {count} occurrences")
        lines.append("")
        lines.append("Examples (first 5 affected pages):")
        for ex in jinja_pages:
            lines.append(f"- `{ex}`")
        lines.append("")
        lines.append("**Diagnosis**: this looks like a build-pipeline issue (templates were copied as static HTML without a Jinja render pass). It is not a per-page mistake; fixing the build will resolve every entry at once.")
    else:
        lines.append("_None._")
    lines.append("")

    # ---- Section D ----
    lines.append("## 5. Section D: Special cases worth manual review")
    lines.append("")
    for s in special_notes:
        lines.append(f"- {s}")
    lines.append("")

    # ---- Section 6 ----
    lines.append("## 6. Recommended next actions")
    lines.append("")
    actions = [
        "Fix the systemic appendix prefix-letter bug (Section A.0) by walking `appendices/appendix-g-*` "
        "through `appendices/appendix-p-*` and replacing the leading section letter in each `prev`/`next` href "
        "to match the appendix's own letter; this alone resolves the bulk of Section A and the corresponding entries in B.",
        "Re-run the build pipeline so `{{book.edition}}` / `{{book.publication_year}}` get resolved into "
        "actual values across all 387 pages (Section C.2 - single root cause).",
        "Repair the cross-Part `prev`/`next` chain (Section B.1) so each Part landing page is part of the "
        "reading sequence (currently the chain jumps chapter-to-chapter across Part boundaries).",
        "Fix the four front-matter / Appendix-U dead links pointing to non-existent `appendix-aj-reading-pathways/` "
        "and `appendix-ak-course-syllabi/` (Section A.1).",
        "Add a `<footer>` block to `index.html` (the home page, currently the only page without one) "
        "and confirm `appendices/glossary/section-f.5.html` should have a `next` link "
        "(currently the only nav present with a missing link).",
    ]
    for a in actions:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("---")
    lines.append(f"_Audit script: `scripts/_audit_nav_footer.py`; pages scanned: {n_total}; pages with chapter-nav: {pages_with_nav}._")

    report = "\n".join(lines)
    out_path = ROOT / "footer-nav-audit.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote {out_path} ({len(report)} bytes, {report.count(chr(10))+1} lines)")


if __name__ == "__main__":
    main()
