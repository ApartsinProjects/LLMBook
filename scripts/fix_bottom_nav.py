"""Bottom <nav class="chapter-nav"> auditor and fixer for the LLMBook.

Builds a canonical reading order from the filesystem (sections, chapter indexes,
part indexes, appendix indexes, appendix sections, front-matter pages),
checks every page's bottom chapter-nav block against the contract, and fixes
href / nav-num / nav-title / nav-label, adds a missing block, removes duplicates,
and strips broken hrefs.
"""

from __future__ import annotations

import os
import re
import sys
import time
import html
from pathlib import Path

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {
    "node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
    "source_fix_backups", "pagefind", "templates", ".claude", ".book-update",
    "agents", "scripts", "styles", "downloads", "tmp_whats_next",
    "_concept-figs", "images", "_concept_figs", "vendor",
}

NAV_RE = re.compile(
    r'<nav class="chapter-nav">.*?</nav>',
    re.DOTALL,
)

# ---------------- Structure discovery ----------------

PARTS = []  # list of dicts: {num, roman, slug, dir, chapters: [...]}
CHAPTERS_BY_PATH = {}  # absolute_chapter_dir -> chapter dict
FRONT_MATTER = []  # ordered list of (slug, file_path)
APPENDICES = []  # list of {letter, slug, dir, sections: [...]}

# Front matter reading order (the user said FM index.html is dropped, foreword is first;
# we honour the order from book_structure.yaml).
FRONT_MATTER_ORDER = [
    ("foreword.html", "Why This Book Exists"),
    ("look-inside-preview.html", "What's Inside"),
    ("fm-what-this-book-covers.html", "What This Book Covers"),
    ("fm-who-should-read.html", "Who Should Read This Book"),
    ("fm-how-to-use.html", "How to Use This Book"),
    ("about-authors.html", "About the Authors"),
    ("copyright.html", "Copyright and Legal"),
]


def _natkey_section(name: str):
    """Sort key for section-N.M.html style filenames."""
    m = re.match(r"section-(\d+|[a-z])\.(\d+)\.html$", name)
    if not m:
        return (999, 999, name)
    first = m.group(1)
    if first.isdigit():
        return (int(first), int(m.group(2)), name)
    return (ord(first) - ord('a'), int(m.group(2)), name)


def _natkey_module(name: str):
    """Sort key for module-NN-slug dirs."""
    m = re.match(r"module-(\d+)", name)
    if not m:
        return (999, name)
    return (int(m.group(1)), name)


def _natkey_part(name: str):
    m = re.match(r"part-(\d+)", name)
    if not m:
        return (999, name)
    return (int(m.group(1)), name)


def _natkey_appendix(name: str):
    m = re.match(r"appendix-([a-z])-", name)
    if not m:
        return (999, name)
    return (ord(m.group(1)), name)


def discover():
    """Populate PARTS, CHAPTERS_BY_PATH, APPENDICES, FRONT_MATTER."""
    # Parts
    part_dirs = sorted(
        [p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("part-") and p.name not in SKIP_DIRS],
        key=lambda p: _natkey_part(p.name),
    )
    for pdir in part_dirs:
        m = re.match(r"part-(\d+)-(.+)", pdir.name)
        if not m:
            continue
        num = int(m.group(1))
        slug = m.group(2)
        roman_map = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII",
                     8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}
        roman = roman_map.get(num, str(num))
        chapters = []
        for cdir in sorted(
            [c for c in pdir.iterdir() if c.is_dir() and c.name.startswith("module-")],
            key=lambda c: _natkey_module(c.name),
        ):
            mm = re.match(r"module-(\d+)-(.+)", cdir.name)
            if not mm:
                continue
            cnum = int(mm.group(1))
            cslug = mm.group(2)
            sections = sorted(
                [s for s in cdir.iterdir() if s.is_file() and s.name.startswith("section-") and s.name.endswith(".html")],
                key=lambda s: _natkey_section(s.name),
            )
            chap = {
                "num": cnum,
                "slug": cslug,
                "dir": cdir,
                "index": cdir / "index.html",
                "sections": sections,
                "part": None,
            }
            chapters.append(chap)
            CHAPTERS_BY_PATH[cdir] = chap
        part = {
            "num": num,
            "roman": roman,
            "slug": slug,
            "dir": pdir,
            "index": pdir / "index.html",
            "chapters": chapters,
        }
        for c in chapters:
            c["part"] = part
        PARTS.append(part)
    # Appendices
    app_root = ROOT / "appendices"
    if app_root.is_dir():
        for adir in sorted(
            [a for a in app_root.iterdir() if a.is_dir() and a.name.startswith("appendix-")],
            key=lambda a: _natkey_appendix(a.name),
        ):
            mm = re.match(r"appendix-([a-z])-(.+)", adir.name)
            if not mm:
                continue
            letter = mm.group(1).upper()
            sections = sorted(
                [s for s in adir.iterdir() if s.is_file() and s.name.startswith("section-") and s.name.endswith(".html")],
                key=lambda s: _natkey_section(s.name),
            )
            APPENDICES.append({
                "letter": letter,
                "slug": mm.group(2),
                "dir": adir,
                "index": adir / "index.html",
                "sections": sections,
            })
    # Front matter (only files that exist)
    fm_root = ROOT / "front-matter"
    for fname, title in FRONT_MATTER_ORDER:
        fp = fm_root / fname
        if fp.is_file():
            FRONT_MATTER.append((fname, title, fp))


# ---------------- HTML helpers ----------------

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL | re.IGNORECASE)
SUBTITLE_RE = re.compile(
    r'<p[^>]*class="[^"]*chapter-subtitle[^"]*"[^>]*>(.*?)</p>',
    re.DOTALL | re.IGNORECASE,
)


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def get_h1(file_path: Path) -> str | None:
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = H1_RE.search(text)
    if not m:
        return None
    return strip_tags(m.group(1))


# Cleans h1 like "Chapter 0: ML and PyTorch Foundations" -> "ML and PyTorch Foundations"
HEADING_PREFIX_RE = re.compile(
    r'^(?:Chapter|Section|Appendix|Part)\s+(?:[IVXLC]+|\d+(?:\.\d+)?|[A-Z](?:\.\d+)?)\s*[:–—.\-]\s*',
    re.IGNORECASE,
)


def clean_h1(text: str) -> str:
    if not text:
        return text
    return HEADING_PREFIX_RE.sub("", text).strip()


# ---------------- Reading order ----------------

def all_nav_pages():
    """Return reading-order list of dicts: {path, kind, num/letter, ...}."""
    order = []
    # Front matter
    for fname, title, fp in FRONT_MATTER:
        order.append({"kind": "fm", "path": fp, "title": title, "fname": fname})
    # Parts > chapters > sections
    for part in PARTS:
        order.append({"kind": "part", "path": part["index"], "part": part})
        for chap in part["chapters"]:
            order.append({"kind": "chapter", "path": chap["index"], "chap": chap})
            for sf in chap["sections"]:
                order.append({"kind": "section", "path": sf, "chap": chap, "section_file": sf})
    # Appendices index
    if APPENDICES:
        order.append({"kind": "appendix_root", "path": ROOT / "appendices/index.html"})
        for app in APPENDICES:
            order.append({"kind": "appendix", "path": app["index"], "app": app})
            for sf in app["sections"]:
                order.append({"kind": "appendix_section", "path": sf, "app": app, "section_file": sf})
    return order


def section_num_letter(name: str):
    """Return (kind, num_or_letter, section_num) for a section filename."""
    m = re.match(r"section-(\d+|[a-z])\.(\d+)\.html$", name)
    if not m:
        return None
    g1 = m.group(1)
    g2 = m.group(2)
    if g1.isdigit():
        return ("section", int(g1), int(g2))
    return ("appendix_section", g1.upper(), int(g2))


# ---------------- Target computation ----------------

def truncate(text: str, n: int = 80) -> str:
    text = text.strip()
    if len(text) <= n:
        return text
    return text[: n - 1].rstrip() + "…"


def chapter_title(chap) -> str:
    h = get_h1(chap["index"])
    return clean_h1(h or chap["slug"].replace("-", " ").title())


def part_title(part) -> str:
    h = get_h1(part["index"])
    return clean_h1(h or part["slug"].replace("-", " ").title())


def section_title(section_file: Path, chap_num: int) -> str:
    h = get_h1(section_file) or section_file.stem
    return clean_h1(h)


def appendix_section_title(section_file: Path) -> str:
    h = get_h1(section_file) or section_file.stem
    return clean_h1(h)


def appendix_title(app) -> str:
    h = get_h1(app["index"])
    return clean_h1(h or app["slug"].replace("-", " ").title())


def compute_targets(page, page_idx, order):
    """Compute correct prev/up/next anchors for a given page.

    Each target is a dict: {label, num, title, href}.
    href is rel to the page's own directory.
    """
    src_dir = page["path"].parent

    def make(target_path: Path, label: str, num: str, title: str):
        href = os.path.relpath(target_path, start=src_dir).replace(os.sep, "/")
        return {"label": label, "num": num, "title": truncate(title, 80), "href": href}

    prev = up = nxt = None
    kind = page["kind"]
    if kind == "fm":
        idx = next(i for i, fm in enumerate(FRONT_MATTER) if fm[2] == page["path"])
        if idx == 0:
            prev = make(ROOT / "toc.html", "Previous", "Book Index", "Table of Contents")
        else:
            pfname, ptitle, pfp = FRONT_MATTER[idx - 1]
            prev = make(pfp, "Previous", "Front Matter", ptitle)
        up = make(ROOT / "toc.html", "Up", "Book Index", "Table of Contents")
        if idx + 1 < len(FRONT_MATTER):
            nfname, ntitle, nfp = FRONT_MATTER[idx + 1]
            nxt = make(nfp, "Next", "Front Matter", ntitle)
        else:
            # After FM the conventional next page is Part 1.
            if PARTS:
                p = PARTS[0]
                nxt = make(p["index"], "Next", f"Part {p['roman']}", part_title(p))
            else:
                nxt = make(ROOT / "toc.html", "Next", "Book Index", "Table of Contents")
    elif kind == "part":
        part = page["part"]
        # prev: previous part index, or toc.html if Part 1
        idx = PARTS.index(part)
        if idx == 0:
            # Part 1 prev: last FM page if exists else toc
            if FRONT_MATTER:
                lf = FRONT_MATTER[-1]
                prev = make(lf[2], "Previous", "Front Matter", lf[1])
            else:
                prev = make(ROOT / "toc.html", "Previous", "Book Index", "Table of Contents")
        else:
            prev_part = PARTS[idx - 1]
            prev = make(prev_part["index"], "Previous", f"Part {prev_part['roman']}", part_title(prev_part))
        up = make(ROOT / "toc.html", "Up", "Book Index", "Table of Contents")
        if idx + 1 < len(PARTS):
            nxt_part = PARTS[idx + 1]
            nxt = make(nxt_part["index"], "Next", f"Part {nxt_part['roman']}", part_title(nxt_part))
        elif APPENDICES:
            nxt = make(ROOT / "appendices/index.html", "Next", "Appendices", "Appendices")
        else:
            nxt = make(ROOT / "toc.html", "Next", "Book Index", "Table of Contents")
    elif kind == "chapter":
        chap = page["chap"]
        part = chap["part"]
        idx = part["chapters"].index(chap)
        if idx == 0:
            prev = make(part["index"], "Previous", f"Part {part['roman']}", part_title(part))
        else:
            prev_chap = part["chapters"][idx - 1]
            prev = make(prev_chap["index"], "Previous", f"Chapter {prev_chap['num']}", chapter_title(prev_chap))
        up = make(part["index"], "In Part", f"Part {part['roman']}", part_title(part))
        if idx + 1 < len(part["chapters"]):
            nxt_chap = part["chapters"][idx + 1]
            nxt = make(nxt_chap["index"], "Next", f"Chapter {nxt_chap['num']}", chapter_title(nxt_chap))
        else:
            # Last chapter of part: next is next part
            part_idx = PARTS.index(part)
            if part_idx + 1 < len(PARTS):
                np_ = PARTS[part_idx + 1]
                nxt = make(np_["index"], "Next", f"Part {np_['roman']}", part_title(np_))
            elif APPENDICES:
                nxt = make(ROOT / "appendices/index.html", "Next", "Appendices", "Appendices")
            else:
                nxt = make(ROOT / "toc.html", "Next", "Book Index", "Table of Contents")
    elif kind == "section":
        chap = page["chap"]
        sec_file = page["section_file"]
        sidx = chap["sections"].index(sec_file)
        sn = section_num_letter(sec_file.name)
        cur_num_str = f"{sn[1]}.{sn[2]}"
        if sidx == 0:
            prev = make(chap["index"], "Previous", f"Chapter {chap['num']}", chapter_title(chap))
        else:
            pf = chap["sections"][sidx - 1]
            pn = section_num_letter(pf.name)
            prev = make(pf, "Previous", f"Section {pn[1]}.{pn[2]}", section_title(pf, chap["num"]))
        up = make(chap["index"], "In Chapter", f"Chapter {chap['num']}", chapter_title(chap))
        if sidx + 1 < len(chap["sections"]):
            nf = chap["sections"][sidx + 1]
            nn = section_num_letter(nf.name)
            nxt = make(nf, "Next", f"Section {nn[1]}.{nn[2]}", section_title(nf, chap["num"]))
        else:
            # Last section: next is the next chapter's first section, else chapter index of next chapter
            part = chap["part"]
            cidx = part["chapters"].index(chap)
            next_chap = None
            if cidx + 1 < len(part["chapters"]):
                next_chap = part["chapters"][cidx + 1]
            else:
                pidx = PARTS.index(part)
                if pidx + 1 < len(PARTS):
                    np_ = PARTS[pidx + 1]
                    if np_["chapters"]:
                        next_chap = np_["chapters"][0]
            if next_chap is not None:
                if next_chap["sections"]:
                    nf = next_chap["sections"][0]
                    nn = section_num_letter(nf.name)
                    nxt = make(nf, "Next", f"Section {nn[1]}.{nn[2]}", section_title(nf, next_chap["num"]))
                else:
                    nxt = make(next_chap["index"], "Next", f"Chapter {next_chap['num']}", chapter_title(next_chap))
            elif APPENDICES:
                nxt = make(ROOT / "appendices/index.html", "Next", "Appendices", "Appendices")
            else:
                nxt = make(chap["index"], "Next", f"Chapter {chap['num']}", chapter_title(chap))
    elif kind == "appendix_root":
        # prev: last part's index (Part 12) else toc; up: toc; next: appendix A
        if PARTS:
            lp = PARTS[-1]
            prev = make(lp["index"], "Previous", f"Part {lp['roman']}", part_title(lp))
        else:
            prev = make(ROOT / "toc.html", "Previous", "Book Index", "Table of Contents")
        up = make(ROOT / "toc.html", "Up", "Book Index", "Table of Contents")
        if APPENDICES:
            a = APPENDICES[0]
            nxt = make(a["index"], "Next", f"Appendix {a['letter']}", appendix_title(a))
        else:
            nxt = make(ROOT / "toc.html", "Next", "Book Index", "Table of Contents")
    elif kind == "appendix":
        app = page["app"]
        aidx = APPENDICES.index(app)
        if aidx == 0:
            prev = make(ROOT / "appendices/index.html", "Previous", "Appendices", "Appendices")
        else:
            pa = APPENDICES[aidx - 1]
            prev = make(pa["index"], "Previous", f"Appendix {pa['letter']}", appendix_title(pa))
        up = make(ROOT / "appendices/index.html", "Appendices", "Appendices", "Appendices")
        if aidx + 1 < len(APPENDICES):
            na = APPENDICES[aidx + 1]
            nxt = make(na["index"], "Next", f"Appendix {na['letter']}", appendix_title(na))
        else:
            nxt = make(ROOT / "toc.html", "Next", "Book Index", "Table of Contents")
    elif kind == "appendix_section":
        app = page["app"]
        sec_file = page["section_file"]
        sidx = app["sections"].index(sec_file)
        sn = section_num_letter(sec_file.name)  # ('appendix_section', 'A', 1)
        if sidx == 0:
            prev = make(app["index"], "Previous", f"Appendix {app['letter']}", appendix_title(app))
        else:
            pf = app["sections"][sidx - 1]
            pn = section_num_letter(pf.name)
            prev = make(pf, "Previous", f"Section {pn[1]}.{pn[2]}", appendix_section_title(pf))
        up = make(app["index"], "In Appendix", f"Appendix {app['letter']}", appendix_title(app))
        if sidx + 1 < len(app["sections"]):
            nf = app["sections"][sidx + 1]
            nn = section_num_letter(nf.name)
            nxt = make(nf, "Next", f"Section {nn[1]}.{nn[2]}", appendix_section_title(nf))
        else:
            aidx = APPENDICES.index(app)
            if aidx + 1 < len(APPENDICES):
                na = APPENDICES[aidx + 1]
                if na["sections"]:
                    nf = na["sections"][0]
                    nn = section_num_letter(nf.name)
                    nxt = make(nf, "Next", f"Section {nn[1]}.{nn[2]}", appendix_section_title(nf))
                else:
                    nxt = make(na["index"], "Next", f"Appendix {na['letter']}", appendix_title(na))
            else:
                nxt = make(app["index"], "Next", f"Appendix {app['letter']}", appendix_title(app))
    return prev, up, nxt


# ---------------- Nav block rendering and parsing ----------------

def render_nav(prev, up, nxt) -> str:
    parts = ['<nav class="chapter-nav">']
    for cls, t in [("prev", prev), ("up", up), ("next", nxt)]:
        if t is None:
            continue
        title_span = f'<span class="nav-title">{html.escape(t["title"])}</span>' if t.get("title") else ""
        parts.append(
            f'<a class="{cls}" href="{html.escape(t["href"])}">'
            f'<span class="nav-label">{html.escape(t["label"])}</span>'
            f'<span class="nav-num">{html.escape(t["num"])}</span>'
            f'{title_span}</a>'
        )
    parts.append("</nav>")
    return "\n".join(parts)


def parse_nav_links(nav_html: str):
    """Return list of (cls, href, label, num, title) for each <a> inside."""
    out = []
    for m in re.finditer(r'<a\s+([^>]*)>(.*?)</a>', nav_html, re.DOTALL):
        attrs = m.group(1)
        body = m.group(2)
        cls = re.search(r'class="([^"]+)"', attrs)
        href = re.search(r'href="([^"]+)"', attrs)
        if not cls:
            continue
        cls_v = cls.group(1).strip()
        href_v = href.group(1) if href else ""
        label = num = title = ""
        ml = re.search(r'class="nav-label"[^>]*>(.*?)</span>', body, re.DOTALL)
        if ml:
            label = strip_tags(ml.group(1))
        mn = re.search(r'class="nav-num"[^>]*>(.*?)</span>', body, re.DOTALL)
        if mn:
            num = strip_tags(mn.group(1))
        mt = re.search(r'class="nav-title"[^>]*>(.*?)</span>', body, re.DOTALL)
        if mt:
            title = strip_tags(mt.group(1))
        out.append((cls_v, href_v, label, num, title))
    return out


# ---------------- File processing ----------------

def find_nav_block_locations(text: str):
    """Find all nav.chapter-nav blocks as (start, end) tuples."""
    return [(m.start(), m.end()) for m in NAV_RE.finditer(text)]


def link_targets_match(expected, actual_href, actual_label, actual_num, actual_title):
    """Heuristic: do expected and actual disagree on href / num / title / label?"""
    issues = []
    # Compare hrefs ignoring leading ./
    eh = expected["href"]
    ah = actual_href or ""
    if eh != ah:
        issues.append("href")
    if expected["label"].lower() != (actual_label or "").lower():
        issues.append("label")
    if expected["num"].lower() != (actual_num or "").lower():
        issues.append("num")
    if expected.get("title") and expected["title"].lower() != (actual_title or "").lower():
        issues.append("title")
    return issues


def insert_nav_into_html(text: str, nav_block: str) -> str:
    """Insert nav_block before <footer> inside <main>. Falls back to end."""
    # Try to insert just before <footer
    m = re.search(r"<footer[\s>]", text)
    if m:
        idx = m.start()
        return text[:idx] + nav_block + "\n" + text[idx:]
    # Else: just before </main>
    m = re.search(r"</main>", text)
    if m:
        idx = m.start()
        return text[:idx] + nav_block + "\n" + text[idx:]
    # Else: before </body>
    m = re.search(r"</body>", text)
    if m:
        idx = m.start()
        return text[:idx] + nav_block + "\n" + text[idx:]
    return text + "\n" + nav_block


def process_page(page, page_idx, order, now, in_flight_min_age, stats, fixed_files, skipped_files):
    fp: Path = page["path"]
    if not fp.is_file():
        return
    # mtime skip
    try:
        mtime = fp.stat().st_mtime
    except OSError:
        return
    if now - mtime < in_flight_min_age * 60:
        skipped_files.append(str(fp))
        return

    text = fp.read_text(encoding="utf-8", errors="replace")
    prev, up, nxt = compute_targets(page, page_idx, order)

    # Check broken hrefs and strip
    def target_exists(t):
        if t is None:
            return False
        target_path = (fp.parent / t["href"]).resolve()
        return target_path.is_file()

    # Strip broken targets if missing
    broken_stripped = 0
    for slot_name, t in [("prev", prev), ("up", up), ("next", nxt)]:
        if t is not None and not target_exists(t):
            # Try to keep but log; we will set None to omit
            broken_stripped += 1
            if slot_name == "prev":
                prev = None
            elif slot_name == "up":
                up = None
            else:
                nxt = None
    if broken_stripped:
        stats["broken_stripped"] += broken_stripped

    locs = find_nav_block_locations(text)
    duplicates_cleaned = 0
    new_text = text

    if len(locs) > 1:
        # Keep the FIRST nav block, delete the rest
        # Remove from last to first (after first)
        for st, en in reversed(locs[1:]):
            new_text = new_text[:st] + new_text[en:]
        duplicates_cleaned = len(locs) - 1
        stats["duplicates"] += duplicates_cleaned
        # Refresh
        locs = find_nav_block_locations(new_text)

    nav_block = render_nav(prev, up, nxt)

    if not locs:
        # Missing: insert
        new_text = insert_nav_into_html(new_text, nav_block)
        stats["missing_created"] += 1
        fixed_files.append((str(fp), page["kind"], "missing+created"))
        bucket_inc(stats, page["kind"], "missing")
    else:
        # Compare existing
        st, en = locs[0]
        cur = new_text[st:en]
        cur_links = parse_nav_links(cur)
        cur_by_cls = {c[0]: c for c in cur_links}
        expected = {"prev": prev, "up": up, "next": nxt}

        issue_kinds = set()
        any_issue = False
        # Check structure: do all three classes exist?
        for cls in ("prev", "up", "next"):
            if expected[cls] is None:
                # If actual has a link of this class but expected says omit, mark issue
                if cls in cur_by_cls:
                    any_issue = True
                    issue_kinds.add("href")
                continue
            actual = cur_by_cls.get(cls)
            if actual is None:
                any_issue = True
                issue_kinds.add("href")
                continue
            issues = link_targets_match(expected[cls], actual[1], actual[2], actual[3], actual[4])
            if issues:
                any_issue = True
                for i in issues:
                    issue_kinds.add(i)

        if any_issue:
            # Replace block
            new_text = new_text[:st] + nav_block + new_text[en:]
            for ik in issue_kinds:
                stats[f"issue_{ik}"] = stats.get(f"issue_{ik}", 0) + 1
            fixed_files.append((str(fp), page["kind"], ",".join(sorted(issue_kinds))))
            bucket_inc(stats, page["kind"], "fixed")
        elif duplicates_cleaned:
            # Only dup cleanup
            fixed_files.append((str(fp), page["kind"], "duplicates"))
            bucket_inc(stats, page["kind"], "fixed")
        else:
            stats["correct"] += 1
            bucket_inc(stats, page["kind"], "correct")
            return

    if new_text != text:
        fp.write_text(new_text, encoding="utf-8")


def bucket_inc(stats, kind, key):
    b = stats["buckets"].setdefault(kind, {"correct": 0, "fixed": 0, "missing": 0})
    b[key] = b.get(key, 0) + 1


# ---------------- Main ----------------

def main():
    discover()
    order = all_nav_pages()
    stats = {
        "scanned": 0,
        "correct": 0,
        "missing_created": 0,
        "duplicates": 0,
        "broken_stripped": 0,
        "buckets": {},
    }
    fixed_files = []
    skipped_files = []
    now = time.time()
    in_flight_min = 10  # minutes

    for idx, page in enumerate(order):
        stats["scanned"] += 1
        process_page(page, idx, order, now, in_flight_min, stats, fixed_files, skipped_files)

    # Write report
    report_lines = []
    report_lines.append("# Bottom Nav Correctness Report\n")
    report_lines.append("## Summary")
    report_lines.append(f"- Files scanned: {stats['scanned']}")
    report_lines.append(f"- Files with correct nav (no edit): {stats['correct']}")
    fixed_count = len([f for f in fixed_files if 'missing' not in f[2]])
    report_lines.append(f"- Files fixed: {fixed_count}")
    report_lines.append(f"- Files with no nav block (created): {stats['missing_created']}")
    report_lines.append(f"- Files skipped (in flight, mtime < 10 min): {len(skipped_files)}\n")

    report_lines.append("## Per-bucket findings")
    bucket_names = {
        "section": "Sections",
        "chapter": "Chapter indexes",
        "part": "Part indexes",
        "appendix_section": "Appendix sections",
        "appendix": "Appendix indexes",
        "appendix_root": "Appendix root",
        "fm": "Front matter",
    }
    for k, label in bucket_names.items():
        b = stats["buckets"].get(k, {"correct": 0, "fixed": 0, "missing": 0})
        report_lines.append(
            f"- {label}: {b.get('fixed', 0)} fixed, "
            f"{b.get('correct', 0)} correct, {b.get('missing', 0)} created"
        )
    report_lines.append("")
    report_lines.append("## Issue type breakdown")
    report_lines.append(f"- Wrong href target: {stats.get('issue_href', 0)}")
    report_lines.append(f"- Wrong nav-num text: {stats.get('issue_num', 0)}")
    report_lines.append(f"- Wrong nav-title text: {stats.get('issue_title', 0)}")
    report_lines.append(f"- Wrong nav-label text: {stats.get('issue_label', 0)}")
    report_lines.append(f"- Missing nav block (created): {stats['missing_created']}")
    report_lines.append(f"- Duplicate nav blocks (cleaned): {stats['duplicates']}")
    report_lines.append(f"- Broken hrefs stripped: {stats['broken_stripped']}")
    if skipped_files:
        report_lines.append("\n## Skipped (in-flight, mtime < 10 min)")
        for s in skipped_files:
            report_lines.append(f"- {s}")

    report = "\n".join(report_lines) + "\n"
    out_path = ROOT / "bottom-nav-fix-report.md"
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote report to {out_path}")
    print(f"Stats: scanned={stats['scanned']} fixed={fixed_count} created={stats['missing_created']} correct={stats['correct']} skipped={len(skipped_files)}")


if __name__ == "__main__":
    main()
