"""Wave 88: Add whats-next to LAST sections (pointing to next chapter).

Wave 87 added whats-next to 124 sections, but skipped any section that
was the LAST in its chapter (no "next section" within the same module).
This wave handles those: for each last-in-chapter section, generate a
whats-next pointing to the FIRST section of the NEXT chapter.

If a chapter is the last in its part, fall back to pointing at the
next part's index page. If the part is the last too, point at the
table of contents (../../toc.html).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

BIB_RE = re.compile(r'(\s*)<details\s+class="bibliography-collapsible', re.IGNORECASE)
NAV_RE = re.compile(r'(\s*)<nav\s+class="chapter-nav"', re.IGNORECASE)
HAS_WN_RE = re.compile(r'<div\s+class="(?:callout\s+)?whats-next"', re.IGNORECASE)


def all_modules_in_part(part_dir: Path):
    return sorted(
        m for m in part_dir.iterdir()
        if m.is_dir() and m.name.startswith("module-")
    )


def all_sections_in_module(mod_dir: Path):
    return sorted(
        s for s in mod_dir.iterdir()
        if s.is_file() and s.name.startswith("section-") and s.name.endswith(".html")
    )


def get_title(html: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    if m:
        inner = m.group(1)
        inner = re.sub(r'<div\s+class="page-current"[^>]*>.*?</div>', '', inner, flags=re.DOTALL)
        return re.sub(r"\s+", " ", re.sub(r'<[^>]+>', '', inner)).strip()
    return ""


def get_chapter_num(mod_name: str):
    m = re.match(r"module-(\d+)-", mod_name)
    if m:
        return int(m.group(1))
    return None


def find_next_target(current_section: Path):
    """Returns (href, link_text, body_template) for the next-thing pointer."""
    mod_dir = current_section.parent
    part_dir = mod_dir.parent
    # Is this the last section in the module?
    sections = all_sections_in_module(mod_dir)
    if current_section not in sections:
        return None
    if current_section != sections[-1]:
        # Not last section; wave 87 handles this case (skip)
        return None
    # Last section: find next module in same part
    modules = all_modules_in_part(part_dir)
    try:
        mod_idx = modules.index(mod_dir)
    except ValueError:
        return None
    if mod_idx + 1 < len(modules):
        next_mod = modules[mod_idx + 1]
        # Get first section in next module (prefer module index page)
        next_sections = all_sections_in_module(next_mod)
        if next_sections:
            # Point to first section
            next_first = next_sections[0]
            next_html = next_first.read_text(encoding="utf-8")
            title = get_title(next_html) or "the next chapter"
            ch_num = get_chapter_num(next_mod.name)
            href_rel = f"../{next_mod.name}/{next_first.name}"
            kind = "chapter" if ch_num is not None else "section"
            link_label = (
                f"Chapter {ch_num}: {title}" if ch_num is not None else title
            )
            body = (
                f'In the next chapter, <a href="{href_rel}">{link_label}</a>, '
                f'we continue building on the material from this chapter.'
            )
            return href_rel, link_label, body
    # No next module in same part: find next part
    all_parts = sorted(
        p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith("part-")
    )
    # Re-sort by num
    def part_key(p):
        m = re.match(r"part-(\d+)-", p.name)
        return int(m.group(1)) if m else 0
    all_parts = sorted(all_parts, key=part_key)
    try:
        part_idx = all_parts.index(part_dir)
    except ValueError:
        return None
    if part_idx + 1 < len(all_parts):
        next_part = all_parts[part_idx + 1]
        next_part_index = next_part / "index.html"
        if next_part_index.exists():
            next_html = next_part_index.read_text(encoding="utf-8")
            title = get_title(next_html) or "the next part"
            href_rel = f"../../{next_part.name}/index.html"
            body = (
                f'This chapter completes the current part. The next part, '
                f'<a href="{href_rel}">{title}</a>, '
                f'opens a new arc; see the part index for chapter ordering.'
            )
            return href_rel, title, body
    # Last part of book: point at TOC
    body = (
        'This is the final section of the book. See the '
        '<a href="../../toc.html">Table of Contents</a> for navigation, '
        'or revisit any chapter where the material is most useful.'
    )
    return "../../toc.html", "Table of Contents", body


def fix_section(p: Path) -> bool:
    html = p.read_text(encoding="utf-8")
    if HAS_WN_RE.search(html):
        return False
    target = find_next_target(p)
    if not target:
        return False
    _, _, body = target
    block = (
        '<div class="whats-next">\n'
        '<h3 id="what-s-next">What\'s Next?</h3>\n'
        f'<p>{body}</p>\n'
        '</div>'
    )
    bib_m = BIB_RE.search(html)
    nav_m = NAV_RE.search(html)
    insert_pos = None
    if bib_m:
        insert_pos = bib_m.start()
    elif nav_m:
        insert_pos = nav_m.start()
    if insert_pos is None:
        return False
    new_html = html[:insert_pos] + "\n" + block + "\n" + html[insert_pos:]
    p.write_text(new_html, encoding="utf-8")
    return True


def main():
    n = 0
    skip = {"node_modules", "KDP", "agents", ".git", "_archive",
            "build", "vendor", "templates", "pagefind", ".book-update"}
    for p in sorted(ROOT.rglob("section-*.html")):
        if set(p.parts) & skip:
            continue
        rel = p.relative_to(ROOT)
        if not (len(rel.parts) >= 3 and rel.parts[0].startswith("part-")
                and "module-" in str(rel.parts[1])):
            continue
        if fix_section(p):
            n += 1
            print(f"  + {rel}")
    print(f"\nTotal last-sections updated: {n}")


if __name__ == "__main__":
    main()
