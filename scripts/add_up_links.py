"""
Add 'up' navigation links to all section files.

The 'up' link points to the chapter's index.html page.
It goes between the 'prev' and 'next' links in <nav class="chapter-nav">.

For section files: up -> index.html (chapter overview)
For index.html files (chapter overviews): up -> ../index.html (part overview)
For part index.html: no up link needed (already at part level)
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

stats = {
    "scanned": 0,
    "already_has_up": 0,
    "added_up": 0,
    "no_nav": 0,
    "skipped": 0,
}

# Chapter index titles (for display text)
# We'll extract from the actual index.html h1 tag

def get_chapter_title(index_path):
    """Extract chapter title from index.html."""
    if not index_path.exists():
        return "Chapter Overview"
    content = index_path.read_text(encoding="utf-8")
    h1 = re.search(r'<h1>(.*?)</h1>', content)
    if h1:
        return h1.group(1).strip()
    return "Chapter Overview"

def get_up_target(filepath):
    """Determine what the 'up' link should point to and its display text."""
    rel = filepath.relative_to(BOOK_ROOT)
    parts = rel.parts
    name = filepath.name

    # Section files (e.g., part-X/module-Y/section-Z.html) -> up to index.html
    if name.startswith("section-"):
        index_path = filepath.parent / "index.html"
        title = get_chapter_title(index_path)
        return "index.html", title

    # Chapter index files (e.g., part-X/module-Y/index.html) -> up to part index
    if name == "index.html" and len(parts) >= 3 and parts[0].startswith("part-"):
        part_index = filepath.parent.parent / "index.html"
        if part_index.exists():
            title = get_chapter_title(part_index)
            return "../index.html", title
        return None, None

    # Appendix section files
    if name.startswith("section-") and "appendix" in str(filepath):
        index_path = filepath.parent / "index.html"
        title = get_chapter_title(index_path)
        return "index.html", title

    # Appendix index files -> appendices index
    if name == "index.html" and "appendix" in str(filepath):
        return "../index.html", "Appendices"

    # Front-matter files -> front-matter index
    if "front-matter" in str(filepath) and name != "index.html":
        return "index.html", "Front Matter"

    return None, None

def add_up_link(filepath):
    """Add an 'up' link to the chapter-nav of a file."""
    content = filepath.read_text(encoding="utf-8")
    stats["scanned"] += 1

    # Check if already has an up link
    if 'class="up"' in content:
        stats["already_has_up"] += 1
        return False

    # Find chapter-nav
    nav_match = re.search(r'<nav class="chapter-nav">(.*?)</nav>', content, re.DOTALL)
    if not nav_match:
        stats["no_nav"] += 1
        return False

    nav_content = nav_match.group(1)

    # Determine up target
    up_href, up_text = get_up_target(filepath)
    if not up_href:
        stats["skipped"] += 1
        return False

    up_link = f'<a class="up" href="{up_href}">{up_text}</a>'

    # Insert up link between prev and next
    # Find the position after the first <a> (prev) closing tag
    links = list(re.finditer(r'<a\s+class="(prev|next)"[^>]*>.*?</a>', nav_content, re.DOTALL))

    if len(links) == 0:
        stats["skipped"] += 1
        return False
    elif len(links) == 1:
        # Only one link (prev or next), add up after/before it
        link = links[0]
        if link.group(1) == "prev":
            new_nav_content = nav_content[:link.end()] + "\n" + up_link + nav_content[link.end():]
        else:
            new_nav_content = nav_content[:link.start()] + up_link + "\n" + nav_content[link.start():]
    else:
        # Two links: insert between them
        first_end = links[0].end()
        new_nav_content = nav_content[:first_end] + "\n" + up_link + nav_content[first_end:]

    new_nav = f'<nav class="chapter-nav">{new_nav_content}</nav>'
    new_content = content[:nav_match.start()] + new_nav + content[nav_match.end():]

    filepath.write_text(new_content, encoding="utf-8")
    stats["added_up"] += 1
    return True


def main():
    patterns = [
        "part-*/module-*/section-*.html",
        "part-*/module-*/index.html",
        "appendices/appendix-*/section-*.html",
        "appendices/appendix-*/index.html",
        "front-matter/*.html",
    ]

    all_files = []
    for pattern in patterns:
        all_files.extend(BOOK_ROOT.glob(pattern))
    all_files = sorted(set(all_files))

    print(f"Scanning {len(all_files)} files...")

    for f in all_files:
        changed = add_up_link(f)
        if changed:
            print(f"  ADDED UP: {f.relative_to(BOOK_ROOT)}")

    print(f"\n=== Summary ===")
    print(f"Total scanned: {stats['scanned']}")
    print(f"Already had up link: {stats['already_has_up']}")
    print(f"Up links added: {stats['added_up']}")
    print(f"No chapter-nav found: {stats['no_nav']}")
    print(f"Skipped (part index or unknown): {stats['skipped']}")

    # Verification
    print(f"\n=== Verification ===")
    up_count = 0
    for f in all_files:
        content = f.read_text(encoding="utf-8")
        if 'class="up"' in content:
            up_count += 1
    print(f"Files with 'up' link: {up_count}")


if __name__ == "__main__":
    main()
