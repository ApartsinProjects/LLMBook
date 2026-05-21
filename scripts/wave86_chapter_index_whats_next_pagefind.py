"""Wave 86: Add canonical whats-next + pagefind chapter meta to chapter index pages.

CHAPTER_INDEX_LAYOUT audit flags 31 chapters missing canonical whats-next
and 21 chapters missing canonical pagefind chapter meta. Both are
mechanically derivable from disk structure.

whats-next:
  <div class="whats-next">
    <h3>What's Next?</h3>
    <p>In the next section, <a href="section-X.1.html">Section X.1: TITLE</a>,
       <DESCRIPTION>.</p>
  </div>
  Inserted just before <nav class="chapter-nav"> (always exists per template).

pagefind chapter meta:
  <span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter N: TITLE" hidden></span>
  Inserted right after <main class="content"...> opening tag.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

CHAPTER_NAV_RE = re.compile(r'(\s*)<nav\s+class="chapter-nav"', re.IGNORECASE)
MAIN_OPEN_RE = re.compile(r'(<main\s+class="content"[^>]*>)', re.IGNORECASE)


def discover_chapter_indexes():
    """Yield (chapter_index_path, first_section_path, chapter_num) tuples."""
    for part in sorted(ROOT.iterdir()):
        if not (part.is_dir() and part.name.startswith("part-")):
            continue
        for mod in sorted(part.iterdir()):
            if not (mod.is_dir() and mod.name.startswith("module-")):
                continue
            idx = mod / "index.html"
            if not idx.exists():
                continue
            # Chapter number from module dir (module-NN-...)
            m = re.match(r"module-(\d+)-", mod.name)
            if not m:
                continue
            ch_num = int(m.group(1))
            # Find first section by scanning section-N.M.html or section-a.M.html
            sections = sorted(
                f for f in mod.iterdir()
                if f.is_file() and f.name.startswith("section-")
                and f.name.endswith(".html")
            )
            if not sections:
                continue
            first_section = sections[0]
            yield idx, first_section, ch_num


def get_chapter_title(idx_html: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', idx_html, re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r"\s+", " ", re.sub(r'<[^>]+>', '', m.group(1))).strip()
    return ""


def get_section_title(section_html: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', section_html, re.IGNORECASE | re.DOTALL)
    if m:
        # Strip <div class="page-current">...</div> from end
        inner = m.group(1)
        inner = re.sub(r'<div\s+class="page-current"[^>]*>.*?</div>', '', inner, flags=re.DOTALL)
        return re.sub(r"\s+", " ", re.sub(r'<[^>]+>', '', inner)).strip()
    return ""


def get_section_subtitle(section_html: str) -> str:
    """Try to extract a 1-clause description from prose."""
    # Look for chapter-subtitle / section subtitle / first paragraph
    m = re.search(
        r'<p[^>]*class="chapter-subtitle"[^>]*>(.*?)</p>',
        section_html, re.IGNORECASE | re.DOTALL,
    )
    if m:
        text = re.sub(r"\s+", " ", re.sub(r'<[^>]+>', '', m.group(1))).strip()
        if text:
            return text
    # First non-callout/non-prereq <p> after the header
    return ""


def get_section_number(section_path: Path) -> str:
    """Extract section number from filename, e.g., section-1.1.html -> 1.1."""
    m = re.match(r"section-(.+)\.html$", section_path.name)
    if not m:
        return ""
    return m.group(1)


def build_whats_next(section_path: Path, section_title: str) -> str:
    sec_num = get_section_number(section_path)
    desc = ""  # No fancy description — keep it simple and accurate
    return (
        '<div class="whats-next">\n'
        '<h3>What\'s Next?</h3>\n'
        f'<p>This chapter begins with <a href="{section_path.name}">Section '
        f'{sec_num}: {section_title}</a>. Each section builds on the '
        f'previous one, so we recommend reading them in order.</p>\n'
        '</div>'
    )


def build_pagefind_meta(chapter_num: int, chapter_title: str) -> str:
    return (
        '<span class="pagefind-meta-injected" '
        f'data-pagefind-meta="chapter:Chapter {chapter_num}: {chapter_title}" '
        'hidden></span>'
    )


def fix_chapter(idx_path: Path, first_section: Path, ch_num: int) -> tuple[bool, bool]:
    """Returns (added_whats_next, added_pagefind_meta)."""
    html = idx_path.read_text(encoding="utf-8")
    chapter_title = get_chapter_title(html)
    section_html = first_section.read_text(encoding="utf-8")
    section_title = get_section_title(section_html) or "first section"

    added_wn = False
    added_pf = False

    # 1. whats-next (only if missing)
    if 'class="whats-next"' not in html:
        wn_block = build_whats_next(first_section, section_title)
        nav_m = CHAPTER_NAV_RE.search(html)
        if nav_m:
            insert_at = nav_m.start()
            html = html[:insert_at] + "\n" + wn_block + "\n" + html[insert_at:]
            added_wn = True

    # 2. pagefind chapter meta (only if missing)
    if 'data-pagefind-meta="chapter:' not in html:
        if chapter_title:
            pf_block = build_pagefind_meta(ch_num, chapter_title)
            main_m = MAIN_OPEN_RE.search(html)
            if main_m:
                insert_at = main_m.end()
                html = html[:insert_at] + "\n" + pf_block + html[insert_at:]
                added_pf = True

    if added_wn or added_pf:
        idx_path.write_text(html, encoding="utf-8")
    return added_wn, added_pf


def main():
    n_wn = 0
    n_pf = 0
    n_chapters = 0
    for idx, first_sec, ch_num in discover_chapter_indexes():
        wn, pf = fix_chapter(idx, first_sec, ch_num)
        n_chapters += 1
        if wn:
            n_wn += 1
        if pf:
            n_pf += 1
        if wn or pf:
            flags = []
            if wn: flags.append("whats-next")
            if pf: flags.append("pagefind-meta")
            print(f"  + {idx.parent.parent.name}/{idx.parent.name}: {', '.join(flags)}")
    print(f"\nTotal chapters scanned: {n_chapters}")
    print(f"whats-next added: {n_wn}")
    print(f"pagefind-meta added: {n_pf}")


if __name__ == "__main__":
    main()
