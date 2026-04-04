"""
Fix navigation footers across all pages to ensure 3-link structure:
  prev | up (chapter/appendix index) | next

Adds missing 'up' links and fixes 1-link navs by adding appropriate prev/next.
"""

import re
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")
SKIP_DIRS = {"vendor", "node_modules", ".git", "__pycache__", "scripts", "_lab_fragments"}


def get_chapter_title(index_path: Path) -> str:
    """Extract chapter title from an index.html file."""
    if not index_path.exists():
        return index_path.parent.name
    text = index_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<h1>(.*?)</h1>", text, re.DOTALL)
    if m:
        # Strip HTML tags
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        return title
    return index_path.parent.name


def compute_up_link(fpath: Path) -> tuple:
    """Compute the 'up' link for a file. Returns (href, title) or None."""
    rel = fpath.relative_to(ROOT)
    parts = rel.parts
    parent = fpath.parent

    # Section files: up goes to chapter index
    if fpath.name.startswith("section-"):
        index_path = parent / "index.html"
        if index_path.exists():
            title = get_chapter_title(index_path)
            return ("index.html", title)

    # Chapter index files: up goes to part index
    if fpath.name == "index.html":
        # Check for part-level parent
        grandparent = parent.parent
        gp_index = grandparent / "index.html"
        if gp_index.exists() and grandparent != ROOT:
            title = get_chapter_title(gp_index)
            return ("../index.html", title)

    # Capstone, front-matter sections
    if "capstone" in str(parent):
        return ("../toc.html", "Table of Contents")

    if "front-matter" in str(parent):
        return ("index.html", "Front Matter")

    return None


def fix_nav(fpath: Path) -> bool:
    """Add missing 'up' link to chapter-nav. Returns True if modified."""
    text = fpath.read_text(encoding="utf-8", errors="ignore")

    nav_match = re.search(
        r'(<nav class="chapter-nav">)(.*?)(</nav>)',
        text, re.DOTALL
    )
    if not nav_match:
        return False

    nav_content = nav_match.group(2)

    # Already has up link?
    if 'class="up"' in nav_content:
        return False

    links = re.findall(r'<a\s[^>]*>.*?</a>', nav_content, re.DOTALL)
    if len(links) >= 3:
        return False  # Already has 3+ links

    up_info = compute_up_link(fpath)
    if not up_info:
        return False

    up_href, up_title = up_info
    up_link = f'    <a class="up" href="{up_href}">{up_title}</a>'

    # Find prev and next links
    prev_link = None
    next_link = None
    for link in links:
        if 'class="prev"' in link or "Previous" in link or "Prev" in link:
            prev_link = link.strip()
        elif 'class="next"' in link or "Next" in link:
            next_link = link.strip()
        else:
            # Ambiguous: if only 2 links, first is prev, second is next
            if prev_link is None:
                prev_link = link.strip()
            else:
                next_link = link.strip()

    # Reconstruct nav with 3 links
    new_nav_parts = []
    if prev_link:
        # Ensure it has class="prev"
        if 'class="prev"' not in prev_link:
            prev_link = prev_link.replace("<a ", '<a class="prev" ', 1)
        new_nav_parts.append(f"    {prev_link}")
    new_nav_parts.append(f"    {up_link}")
    if next_link:
        # Ensure it has class="next"
        if 'class="next"' not in next_link:
            next_link = next_link.replace("<a ", '<a class="next" ', 1)
        new_nav_parts.append(f"    {next_link}")

    new_nav_inner = "\n".join(new_nav_parts)
    new_nav = f'<nav class="chapter-nav">\n{new_nav_inner}\n</nav>'

    new_text = text[:nav_match.start()] + new_nav + text[nav_match.end():]

    if new_text != text:
        fpath.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    fixed = 0
    for fpath in sorted(ROOT.rglob("*.html")):
        parts = fpath.relative_to(ROOT).parts
        if any(p in SKIP_DIRS for p in parts):
            continue
        if fix_nav(fpath):
            fixed += 1
            print(f"  Fixed: {fpath.relative_to(ROOT)}")

    print(f"\nDone: {fixed} files fixed with up links.")


if __name__ == "__main__":
    main()
