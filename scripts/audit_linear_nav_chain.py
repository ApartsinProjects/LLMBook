"""Audit (and optionally fix) the linear next/prev navigation chain across the
book.

Convention
==========

SECTION FILES (section-N.M.html)
  prev :: section-N.(M-1).html   OR  ../module-NN-<slug>/index.html (if M == 1)
  next :: section-N.(M+1).html   OR  ../module-(N+1)-<slug>/index.html (if last)

CHAPTER STARTER FILES (module-NN-<slug>/index.html)
  prev :: ../module-(N-1)-<slug>/section-(N-1).LAST.html
          OR ../index.html (if first chapter of a part)
  next :: section-N.1.html

PART STARTER FILES (part-K-<slug>/index.html)
  prev :: ../part-(K-1)-<slug>/module-LAST/section-LAST.LAST.html
          OR ../toc.html  (if part-1)
  next :: module-FIRST/index.html

The script:

  1. Walks every part / module / section on disk.
  2. Computes the expected prev/next for each page.
  3. Compares against the on-disk chapter-nav and reports mismatches.
  4. If `--fix` is supplied, rewrites the prev/next anchors in place.

Run modes
---------

  python scripts/audit_linear_nav_chain.py                  # audit only
  python scripts/audit_linear_nav_chain.py --fix            # audit + fix
  python scripts/audit_linear_nav_chain.py --json out.json  # dump findings

Boundaries
----------

  * First part-1 page: prev points to front-matter/copyright.html (existing
    behaviour preserved).
  * Last section of part-15: next points to capstone/index.html if it exists,
    else appendices/index.html.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

# ---------- HTML helpers -------------------------------------------------

NAV_RE = re.compile(
    r'(<nav\s+class="chapter-nav"[^>]*>)(.*?)(</nav>)',
    re.DOTALL | re.IGNORECASE,
)
LINK_RE = re.compile(
    r'<a\s+class="(prev|up|next)"\s+href="([^"]*)"\s*>(.*?)</a>',
    re.DOTALL | re.IGNORECASE,
)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
NUM_SPAN_RE = re.compile(
    r'<span\s+class="nav-num"[^>]*>(.*?)</span>', re.DOTALL | re.IGNORECASE
)
TITLE_SPAN_RE = re.compile(
    r'<span\s+class="nav-title"[^>]*>(.*?)</span>', re.DOTALL | re.IGNORECASE
)


def parse_nav(html: str) -> dict[str, dict] | None:
    """Return dict of {'prev'|'up'|'next' -> {'href','inner','full','nav_num','nav_title'}} or None."""
    m = NAV_RE.search(html)
    if not m:
        return None
    block = m.group(2)
    out: dict[str, dict] = {}
    for am in LINK_RE.finditer(block):
        cls = am.group(1).lower()
        inner = am.group(3)
        nm = NUM_SPAN_RE.search(inner)
        tm = TITLE_SPAN_RE.search(inner)
        nav_num = WS_RE.sub(" ", TAG_RE.sub("", nm.group(1))).strip() if nm else ""
        nav_title = WS_RE.sub(" ", TAG_RE.sub("", tm.group(1))).strip() if tm else ""
        out[cls] = {
            "href": am.group(2),
            "inner": inner,
            "full": am.group(0),
            "nav_num": nav_num,
            "nav_title": nav_title,
        }
    return out


def h1_text(html: str) -> str:
    m = H1_RE.search(html)
    if not m:
        return ""
    raw = TAG_RE.sub("", m.group(1))
    return WS_RE.sub(" ", raw).strip()


# ---------- Numbering helpers --------------------------------------------

ROMAN = [
    "0",
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
]


def part_num(name: str) -> int:
    m = re.match(r"part-(\d+)", name)
    return int(m.group(1)) if m else -1


def module_num(name: str) -> int | None:
    """Return the numeric module number for directory names like
    'module-54-x', 'module-54b-x' -> 54.  Suffix letters are stripped.
    """
    m = re.match(r"module-(\d+)([a-z]?)", name)
    return int(m.group(1)) if m else None


def section_key(name: str) -> tuple[int, int] | None:
    m = re.match(r"section-(\d+)\.(\d+)\.html$", name, re.IGNORECASE)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)))


# ---------- Discovery: build the book in order ---------------------------


@dataclass
class Section:
    path: Path
    chapter_num: int   # the N in section-N.M.html  (== chapter folder number)
    section_num: int   # the M


@dataclass
class Chapter:
    path: Path                 # directory
    index_html: Path           # directory/index.html
    number: int                # numeric N (52, 54, 54-with-b suffix all share 54-class)
    suffix: str = ""           # e.g. 'b' for module-54b
    sections: list[Section] = field(default_factory=list)
    title: str = ""

    @property
    def name(self) -> str:
        return self.path.name


@dataclass
class Part:
    path: Path
    index_html: Path
    number: int       # 1-based
    chapters: list[Chapter] = field(default_factory=list)
    title: str = ""

    @property
    def name(self) -> str:
        return self.path.name


def discover_book(root: Path) -> list[Part]:
    parts_dirs = sorted(
        [p for p in root.iterdir() if p.is_dir() and re.match(r"part-\d+", p.name)],
        key=lambda p: part_num(p.name),
    )
    out: list[Part] = []
    for pd in parts_dirs:
        if not (pd / "index.html").exists():
            continue
        part = Part(path=pd, index_html=pd / "index.html", number=part_num(pd.name))
        # Title
        try:
            html = part.index_html.read_text(encoding="utf-8", errors="replace")
            part.title = h1_text(html)
        except Exception:
            part.title = ""
        # Chapters
        chap_dirs = []
        for c in pd.iterdir():
            if not c.is_dir():
                continue
            mo = re.match(r"module-(\d+)([a-z]?)-", c.name)
            if not mo:
                continue
            if not (c / "index.html").exists():
                continue
            chap_dirs.append((int(mo.group(1)), mo.group(2), c))
        # Sort by module number, then suffix (so '54' before '54b')
        chap_dirs.sort(key=lambda t: (t[0], t[1]))
        for n, suf, cd in chap_dirs:
            chap = Chapter(
                path=cd,
                index_html=cd / "index.html",
                number=n,
                suffix=suf,
            )
            try:
                chap.title = h1_text(chap.index_html.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                chap.title = ""
            # Sections
            secs: list[Section] = []
            for sf in cd.iterdir():
                if not sf.is_file():
                    continue
                sk = section_key(sf.name)
                if sk is None:
                    continue
                secs.append(Section(path=sf, chapter_num=sk[0], section_num=sk[1]))
            secs.sort(key=lambda s: (s.chapter_num, s.section_num))
            chap.sections = secs
            part.chapters.append(chap)
        out.append(part)
    return out


# ---------- Expected nav targets -----------------------------------------


@dataclass
class NavTarget:
    href: str           # relative href from the source page
    abs_path: Path      # resolved absolute file path
    nav_num: str        # e.g. "Section 28.4", "Chapter 29", "Part VI"
    nav_title: str      # e.g. "Specialized Agents"


def rel_href(from_file: Path, to_file: Path) -> str:
    """Return a clean POSIX relative href from from_file to to_file."""
    import os
    rp = os.path.relpath(to_file, start=from_file.parent)
    return rp.replace("\\", "/")


def num_for_section(s: Section) -> str:
    return f"Section {s.chapter_num}.{s.section_num}"


def num_for_chapter(c: Chapter) -> str:
    # Display: "Chapter 29".  The corpus convention is no zero-pad
    # (e.g. "Chapter 0" not "Chapter 00"), so we strip leading zeros.
    # The 'b' suffix (e.g. module-54b) is appended as a lowercase letter.
    suffix = c.suffix or ""
    return f"Chapter {c.number}{suffix}"


def num_for_part(p: Part) -> str:
    if 0 < p.number < len(ROMAN):
        return f"Part {ROMAN[p.number]}"
    return f"Part {p.number}"


def title_for_part(p: Part) -> str:
    """Return the part's display title (stripped of 'Part V:' prefix)."""
    t = p.title or ""
    # Strip leading 'Part V:' / 'Part 5:' prefix.
    t = re.sub(r"^Part\s+[IVXLCDM\d]+\s*:\s*", "", t, flags=re.IGNORECASE).strip()
    return t


def title_for_section(s: Section, root: Path) -> str:
    try:
        html = s.path.read_text(encoding="utf-8", errors="replace")
        return h1_text(html)
    except Exception:
        return ""


def title_for_chapter(c: Chapter) -> str:
    return c.title


# ---------- Build expected-nav map ---------------------------------------


def build_expected(parts: list[Part], root: Path) -> dict[Path, dict[str, NavTarget | None]]:
    expected: dict[Path, dict[str, NavTarget | None]] = {}

    capstone = root / "capstone" / "index.html"
    appendices = root / "appendices" / "index.html"
    toc = root / "toc.html"
    fm_copyright = root / "front-matter" / "copyright.html"

    # Preserve existing convention: section 78.5 currently flows -> appendices/index.html
    # (capstone is reached from inside the appendix chain).  Prefer appendices.
    cap_target = appendices if appendices.exists() else (capstone if capstone.exists() else None)

    # Flatten chapters and sections in order for easy lookups
    all_parts = parts
    for pi, part in enumerate(all_parts):

        # ---- PART STARTER ---------------------------------------
        prev_t: NavTarget | None = None
        if pi == 0:
            # part-1 prev -> front-matter (existing convention) or toc
            if fm_copyright.exists():
                t = fm_copyright
                prev_t = NavTarget(
                    href=rel_href(part.index_html, t),
                    abs_path=t,
                    nav_num="Front Matter",
                    nav_title=h1_or_default(t, "About the Authors") or "About the Authors",
                )
            elif toc.exists():
                t = toc
                prev_t = NavTarget(
                    href=rel_href(part.index_html, t),
                    abs_path=t,
                    nav_num="Book",
                    nav_title="Table of Contents",
                )
        else:
            prev_part = all_parts[pi - 1]
            if prev_part.chapters and prev_part.chapters[-1].sections:
                last_sec = prev_part.chapters[-1].sections[-1]
                prev_t = NavTarget(
                    href=rel_href(part.index_html, last_sec.path),
                    abs_path=last_sec.path,
                    nav_num=num_for_section(last_sec),
                    nav_title=title_for_section(last_sec, root),
                )
            else:
                # fall back to previous part landing
                prev_t = NavTarget(
                    href=rel_href(part.index_html, prev_part.index_html),
                    abs_path=prev_part.index_html,
                    nav_num=num_for_part(prev_part),
                    nav_title=title_for_part(prev_part),
                )

        next_t: NavTarget | None = None
        if part.chapters:
            first_chap = part.chapters[0]
            next_t = NavTarget(
                href=rel_href(part.index_html, first_chap.index_html),
                abs_path=first_chap.index_html,
                nav_num=num_for_chapter(first_chap),
                nav_title=title_for_chapter(first_chap),
            )

        expected[part.index_html] = {"prev": prev_t, "next": next_t}

        # ---- CHAPTERS -------------------------------------------
        for ci, chap in enumerate(part.chapters):
            # Chapter starter
            prev_c: NavTarget | None = None
            if ci == 0:
                prev_c = NavTarget(
                    href=rel_href(chap.index_html, part.index_html),
                    abs_path=part.index_html,
                    nav_num=num_for_part(part),
                    nav_title=title_for_part(part),
                )
            else:
                prev_chap = part.chapters[ci - 1]
                if prev_chap.sections:
                    last_sec = prev_chap.sections[-1]
                    prev_c = NavTarget(
                        href=rel_href(chap.index_html, last_sec.path),
                        abs_path=last_sec.path,
                        nav_num=num_for_section(last_sec),
                        nav_title=title_for_section(last_sec, root),
                    )
                else:
                    prev_c = NavTarget(
                        href=rel_href(chap.index_html, prev_chap.index_html),
                        abs_path=prev_chap.index_html,
                        nav_num=num_for_chapter(prev_chap),
                        nav_title=title_for_chapter(prev_chap),
                    )

            next_c: NavTarget | None = None
            if chap.sections:
                first_sec = chap.sections[0]
                next_c = NavTarget(
                    href=rel_href(chap.index_html, first_sec.path),
                    abs_path=first_sec.path,
                    nav_num=num_for_section(first_sec),
                    nav_title=title_for_section(first_sec, root),
                )
            else:
                # no sections; chain to next chapter starter
                if ci + 1 < len(part.chapters):
                    nx = part.chapters[ci + 1]
                    next_c = NavTarget(
                        href=rel_href(chap.index_html, nx.index_html),
                        abs_path=nx.index_html,
                        nav_num=num_for_chapter(nx),
                        nav_title=title_for_chapter(nx),
                    )
                else:
                    nx_part = all_parts[pi + 1] if pi + 1 < len(all_parts) else None
                    if nx_part is not None:
                        next_c = NavTarget(
                            href=rel_href(chap.index_html, nx_part.index_html),
                            abs_path=nx_part.index_html,
                            nav_num=num_for_part(nx_part),
                            nav_title=title_for_part(nx_part),
                        )

            expected[chap.index_html] = {"prev": prev_c, "next": next_c}

            # ---- SECTIONS ------------------------------------
            for si, sec in enumerate(chap.sections):
                # PREV
                ps: NavTarget | None = None
                if si > 0:
                    prv = chap.sections[si - 1]
                    ps = NavTarget(
                        href=rel_href(sec.path, prv.path),
                        abs_path=prv.path,
                        nav_num=num_for_section(prv),
                        nav_title=title_for_section(prv, root),
                    )
                else:
                    ps = NavTarget(
                        href=rel_href(sec.path, chap.index_html),
                        abs_path=chap.index_html,
                        nav_num=num_for_chapter(chap),
                        nav_title=title_for_chapter(chap),
                    )
                # NEXT
                ns: NavTarget | None = None
                if si + 1 < len(chap.sections):
                    nx = chap.sections[si + 1]
                    ns = NavTarget(
                        href=rel_href(sec.path, nx.path),
                        abs_path=nx.path,
                        nav_num=num_for_section(nx),
                        nav_title=title_for_section(nx, root),
                    )
                else:
                    # last section of a chapter
                    if ci + 1 < len(part.chapters):
                        # last section -> next chapter's starter within the same part
                        nx_chap = part.chapters[ci + 1]
                        ns = NavTarget(
                            href=rel_href(sec.path, nx_chap.index_html),
                            abs_path=nx_chap.index_html,
                            nav_num=num_for_chapter(nx_chap),
                            nav_title=title_for_chapter(nx_chap),
                        )
                    elif pi + 1 < len(all_parts):
                        # last section of part's last chapter -> NEXT PART's starter
                        # (so the part starter is visited in the linear chain).
                        nx_part = all_parts[pi + 1]
                        ns = NavTarget(
                            href=rel_href(sec.path, nx_part.index_html),
                            abs_path=nx_part.index_html,
                            nav_num=num_for_part(nx_part),
                            nav_title=title_for_part(nx_part),
                        )
                    else:
                        # very last section of the book
                        if cap_target is not None:
                            label = "Capstone" if cap_target.name == "index.html" and "capstone" in str(cap_target).lower() else "Appendices"
                            title = "Capstone Project" if label == "Capstone" else "Reference Material"
                            ns = NavTarget(
                                href=rel_href(sec.path, cap_target),
                                abs_path=cap_target,
                                nav_num=label,
                                nav_title=title,
                            )
                expected[sec.path] = {"prev": ps, "next": ns}

    return expected


def h1_or_default(path: Path, default: str) -> str:
    try:
        return h1_text(path.read_text(encoding="utf-8", errors="replace")) or default
    except Exception:
        return default


# ---------- Comparison ---------------------------------------------------


def resolve_href(from_file: Path, href: str) -> Path | None:
    if not href:
        return None
    # strip #fragment
    h = href.split("#", 1)[0]
    if not h:
        return from_file
    target = (from_file.parent / h).resolve()
    return target


@dataclass
class Mismatch:
    page: Path
    kind: str            # 'part' / 'chapter' / 'section'
    direction: str       # 'prev' / 'next'
    have_href: str
    have_text: str
    want_href: str
    want_nav_num: str
    want_nav_title: str


def norm(s: str) -> str:
    """Lower-case, collapse whitespace, decode common HTML entities for comparison."""
    if not s:
        return ""
    s = s.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#8217;", "'")
    s = s.replace("&#x27;", "'").replace("&apos;", "'").replace("&quot;", '"')
    s = WS_RE.sub(" ", s).strip().lower()
    return s


def page_kind(path: Path) -> str:
    name = path.name
    parent = path.parent.name
    if path.parent == ROOT:
        return "root"
    if re.match(r"part-\d+", parent) and name == "index.html":
        return "part"
    if re.match(r"module-\d+", parent) and name == "index.html":
        return "chapter"
    if re.match(r"section-\d+\.\d+\.html$", name):
        return "section"
    return "other"


def text_for_target(t: NavTarget | None) -> str:
    if t is None:
        return ""
    # Recreate the inner span structure for comparison/normalization
    return f"{t.nav_num} {t.nav_title}".strip()


def normalize_inner(num: str, title: str) -> str:
    return f"{num} {title}".strip()


def compare(parts: list[Part], expected: dict[Path, dict[str, NavTarget | None]]) -> list[Mismatch]:
    mismatches: list[Mismatch] = []
    for page_path, want in expected.items():
        try:
            html = page_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        nav = parse_nav(html)
        kind = page_kind(page_path)
        for direction in ("prev", "next"):
            want_t = want.get(direction)
            have_link = nav.get(direction) if nav else None
            if want_t is None and have_link is None:
                continue
            if want_t is None and have_link is not None:
                # Boundary: the page shouldn't have this link, but does.
                mismatches.append(Mismatch(
                    page=page_path,
                    kind=kind,
                    direction=direction,
                    have_href=have_link.get("href", ""),
                    have_text=f"{have_link.get('nav_num','')} | {have_link.get('nav_title','')}",
                    want_href="",
                    want_nav_num="",
                    want_nav_title="(no link expected)",
                ))
                continue
            if want_t is not None and have_link is None:
                mismatches.append(Mismatch(
                    page=page_path,
                    kind=kind,
                    direction=direction,
                    have_href="(missing)",
                    have_text="(missing)",
                    want_href=want_t.href,
                    want_nav_num=want_t.nav_num,
                    want_nav_title=want_t.nav_title,
                ))
                continue
            # Both present, compare
            have_href_norm = (have_link.get("href") or "").strip()
            have_target = resolve_href(page_path, have_href_norm)
            want_target = want_t.abs_path.resolve()
            paths_match = (have_target == want_target) if have_target else False
            have_num = have_link.get("nav_num", "")
            have_title = have_link.get("nav_title", "")
            num_match = norm(have_num) == norm(want_t.nav_num)
            title_match = norm(have_title) == norm(want_t.nav_title)
            if not paths_match or not num_match or not title_match:
                mismatches.append(Mismatch(
                    page=page_path,
                    kind=kind,
                    direction=direction,
                    have_href=have_href_norm,
                    have_text=f"{have_num} | {have_title}",
                    want_href=want_t.href,
                    want_nav_num=want_t.nav_num,
                    want_nav_title=want_t.nav_title,
                ))
    return mismatches


# ---------- Fix ----------------------------------------------------------


def build_link(direction: str, kind: str, target: NavTarget) -> str:
    """Produce the <a class="prev|next" ...> HTML for a target.

    The nav-label is chosen based on the page kind and the target's nav-num:
      * Sections: 'Previous' / 'Next'.
      * Chapter starters:
          - prev: 'Previous Chapter' if target is a chapter's last section
                  (we're chaining back into the prev chapter's last section);
                  'Previous Part' if going to a part starter; 'Previous'
                  otherwise.
          - next: 'Next Section' if target is a section (the typical case);
                  'Next' otherwise.
      * Part starters: 'Previous' / 'Next'.
    """
    label = "Previous" if direction == "prev" else "Next"
    if kind == "chapter":
        if direction == "prev":
            if target.nav_num.startswith("Section "):
                label = "Previous Chapter"
            elif target.nav_num.startswith("Part "):
                label = "Previous Part"
            else:
                label = "Previous"
        else:
            if target.nav_num.startswith("Section "):
                label = "Next Section"
            elif target.nav_num.startswith("Chapter "):
                label = "Next Chapter"
            elif target.nav_num.startswith("Part "):
                label = "Next Part"
            else:
                label = "Next"
    return (
        f'<a class="{direction}" href="{target.href}">'
        f'<span class="nav-label">{label}</span>'
        f'<span class="nav-num">{target.nav_num}</span>'
        f'<span class="nav-title">{target.nav_title}</span></a>'
    )


def apply_fixes(parts: list[Part], expected: dict[Path, dict[str, NavTarget | None]]) -> tuple[int, list[str]]:
    """Rewrite prev/next anchors in place. Return (n_files_changed, log)."""
    changed = 0
    log: list[str] = []
    for page_path, want in expected.items():
        try:
            html = page_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            log.append(f"SKIP unreadable: {page_path}")
            continue
        m = NAV_RE.search(html)
        if not m:
            continue
        nav = parse_nav(html)
        if not nav:
            continue
        kind = page_kind(page_path)
        block = m.group(2)
        new_block = block
        page_changed = False

        for direction in ("prev", "next"):
            want_t = want.get(direction)
            have_link = nav.get(direction)
            if want_t is None:
                # Boundary case: leave existing link alone unless the user-defined
                # boundary explicitly requires absence. (None of the expected
                # entries are None for in-book pages, so this branch is rare.)
                continue
            new_link = build_link(direction, kind, want_t)
            if have_link is None:
                # Try to insert before/after the up link if present, else append.
                if "up" in nav:
                    up_full = nav["up"]["full"]
                    if direction == "prev":
                        new_block = new_block.replace(up_full, new_link + "\n" + up_full, 1)
                    else:
                        new_block = new_block.replace(up_full, up_full + "\n" + new_link, 1)
                else:
                    new_block = new_block.rstrip() + "\n" + new_link + "\n"
                page_changed = True
                continue

            old_full = have_link["full"]
            if old_full == new_link:
                continue
            new_block = new_block.replace(old_full, new_link, 1)
            page_changed = True

        if page_changed:
            new_html = html[: m.start(2)] + new_block + html[m.end(2):]
            page_path.write_text(new_html, encoding="utf-8")
            changed += 1
            log.append(f"FIXED: {page_path.relative_to(ROOT).as_posix()}")
    return changed, log


# ---------- Reporting / CLI ----------------------------------------------


def fmt_mismatch(m: Mismatch) -> str:
    rp = m.page.relative_to(ROOT).as_posix()
    return (
        f"[{m.kind}] {rp} :: {m.direction}\n"
        f"   have: href='{m.have_href}'  text='{m.have_text}'\n"
        f"   want: href='{m.want_href}'  text='{m.want_nav_num} {m.want_nav_title}'\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--fix", action="store_true", help="Rewrite prev/next anchors in place")
    ap.add_argument("--json", default=None, help="Optional path to dump mismatches as JSON")
    ap.add_argument("--limit", type=int, default=0, help="Print only N mismatches to stdout")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    parts = discover_book(root)

    n_parts = len(parts)
    n_chap = sum(len(p.chapters) for p in parts)
    n_sec = sum(len(c.sections) for p in parts for c in p.chapters)
    n_pages = n_parts + n_chap + n_sec
    print(f"Book: {n_parts} parts, {n_chap} chapters, {n_sec} sections  (total {n_pages} pages)")

    expected = build_expected(parts, root)
    mismatches = compare(parts, expected)
    print(f"Mismatches: {len(mismatches)}")

    if args.json:
        Path(args.json).write_text(
            json.dumps(
                [
                    {
                        "page": m.page.relative_to(root).as_posix(),
                        "kind": m.kind,
                        "direction": m.direction,
                        "have_href": m.have_href,
                        "have_text": m.have_text,
                        "want_href": m.want_href,
                        "want_nav_num": m.want_nav_num,
                        "want_nav_title": m.want_nav_title,
                    }
                    for m in mismatches
                ],
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"JSON written: {args.json}")

    to_show = mismatches if args.limit == 0 else mismatches[: args.limit]
    for m in to_show:
        print(fmt_mismatch(m))

    if args.fix:
        n, log = apply_fixes(parts, expected)
        for ln in log[:30]:
            print(ln)
        if len(log) > 30:
            print(f"... and {len(log) - 30} more files")
        print(f"\n{n} files modified.")
        # Re-audit
        parts = discover_book(root)
        expected = build_expected(parts, root)
        mismatches2 = compare(parts, expected)
        print(f"Post-fix mismatches: {len(mismatches2)}")
        if mismatches2:
            for m in mismatches2[:20]:
                print(fmt_mismatch(m))
        return 0 if not mismatches2 else 2

    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
