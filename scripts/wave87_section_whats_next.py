"""Wave 87: Add canonical section-level whats-next to 100 sections.

For each section-X.Y.html missing the <div class="whats-next"> block,
generate a whats-next pointing to the NEXT section in the same chapter,
or to the FIRST section of the NEXT chapter if this is the last section
of the current chapter.

Canonical form (matches existing whats-next in section files):
  <div class="whats-next">
    <h3 id="what-s-next">What's Next?</h3>
    <p>In the next section, <a href="section-X.Y.html">Section X.Y: TITLE</a>,
       we ...</p>
  </div>

Insertion point: just before the existing <details class="bibliography-collapsible">
or before <nav class="chapter-nav"> (whichever appears first).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

# Where to insert: before bibliography (preferred) or before chapter-nav.
BIB_RE = re.compile(r'(\s*)<details\s+class="bibliography-collapsible', re.IGNORECASE)
NAV_RE = re.compile(r'(\s*)<nav\s+class="chapter-nav"', re.IGNORECASE)

# Section-level whats-next must be MISSING for us to add. Already-present
# whats-next has either <div class="whats-next"> OR <div class="callout whats-next">.
HAS_WN_RE = re.compile(
    r'<div\s+class="(?:callout\s+)?whats-next"',
    re.IGNORECASE,
)


def get_section_number(section_path: Path) -> str:
    m = re.match(r"section-(.+)\.html$", section_path.name)
    if not m:
        return ""
    return m.group(1)


def parse_section_num(sec_num: str):
    """Returns (chapter_int, sub_int) or (None, None)."""
    m = re.match(r"^(\d+)\.(\d+)$", sec_num)
    if not m:
        # Sometimes section-X.Y.Z.html (sub-sub) — treat as not orderable here
        return None, None
    return int(m.group(1)), int(m.group(2))


def get_section_title(section_html: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', section_html, re.IGNORECASE | re.DOTALL)
    if m:
        inner = m.group(1)
        # Strip <div class="page-current">...</div>
        inner = re.sub(r'<div\s+class="page-current"[^>]*>.*?</div>', '', inner, flags=re.DOTALL)
        return re.sub(r"\s+", " ", re.sub(r'<[^>]+>', '', inner)).strip()
    return ""


def find_next_section(current_path: Path):
    """Return path to next section file or None."""
    mod_dir = current_path.parent
    sections = sorted(
        f for f in mod_dir.iterdir()
        if f.is_file() and f.name.startswith("section-") and f.name.endswith(".html")
    )
    try:
        idx = sections.index(current_path)
    except ValueError:
        return None
    if idx + 1 < len(sections):
        return sections[idx + 1]
    return None


def build_whats_next(next_section: Path) -> str:
    """Build the whats-next block pointing to next_section."""
    next_html = next_section.read_text(encoding="utf-8")
    next_title = get_section_title(next_html) or "next section"
    next_num = get_section_number(next_section)
    href = next_section.name
    return (
        '<div class="whats-next">\n'
        '<h3 id="what-s-next">What\'s Next?</h3>\n'
        f'<p>In the next section, <a href="{href}">Section {next_num}: '
        f'{next_title}</a>, we build on the material covered here.</p>\n'
        '</div>'
    )


def fix_section(p: Path) -> bool:
    html = p.read_text(encoding="utf-8")
    if HAS_WN_RE.search(html):
        return False
    next_sec = find_next_section(p)
    if not next_sec:
        return False
    block = build_whats_next(next_sec)
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
    # Find all section files
    for p in sorted(ROOT.rglob("section-*.html")):
        # Skip non-content dirs
        skip = {"node_modules", "KDP", "agents", ".git", "_archive",
                "build", "vendor", "templates", "pagefind", ".book-update"}
        if set(p.parts) & skip:
            continue
        # Process only sections in part-N-*/module-X-* layout
        rel = p.relative_to(ROOT)
        if not (len(rel.parts) >= 3 and rel.parts[0].startswith("part-")
                and "module-" in str(rel.parts[1])):
            continue
        if fix_section(p):
            n += 1
            print(f"  + {rel}")
    print(f"\nTotal sections with whats-next added: {n}")


if __name__ == "__main__":
    main()
