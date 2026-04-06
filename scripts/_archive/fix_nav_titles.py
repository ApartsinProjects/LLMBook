"""
Fix chapter-nav links across the entire book:
1. Replace generic "Next Chapter" / "Previous Chapter" / "Previous Section" text
   with actual page titles from the target file's <h1>.
2. Fill in empty <span class="prev"></span> with correct links to previous pages.
3. Fill in empty <span class="next"></span> with correct links to next pages.

Builds a complete page ordering from the directory structure, then updates
each file's nav block.
"""

import re
from pathlib import Path
from collections import OrderedDict

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", "scripts", "templates",
                "styles", "vendor", "images", ".git"}

# Canonical part ordering
PART_ORDER = [
    "front-matter",
    "part-1-foundations",
    "part-2-understanding-llms",
    "part-3-working-with-llms",
    "part-4-training-adapting",
    "part-5-retrieval-conversation",
    "part-6-agentic-ai",
    "part-7-multimodal-applications",
    "part-8-evaluation-production",
    "part-9-safety-strategy",
    "part-10-frontiers",
    "appendices",
    "capstone",
]

# Old/duplicate part directories to skip
SKIP_PARTS = {
    "part-6-agents-applications",
    "part-7-production-strategy",
    "part-5-retrieval-conversation\\module-18-embeddings-vector-db",
    "part-5-retrieval-conversation\\module-20-conversational-ai",
    "part-4-training-adapting\\module-17-interpretability",
}


def should_skip(filepath):
    """Check if a file is in a deprecated/duplicate directory."""
    rel = filepath.relative_to(BASE)
    parts_str = str(rel)
    for skip in SKIP_PARTS:
        if skip in parts_str:
            return True
    # Check top-level part
    top_dir = rel.parts[0]
    if top_dir in {"part-6-agents-applications", "part-7-production-strategy"}:
        return True
    return False


def extract_title(filepath):
    """Extract the page title from <h1> tag."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    # Try <h1>
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
    if m:
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        title = title.replace("&amp;", "&").replace("&#39;", "'").replace("&mdash;", " ")
        return title
    return None


def get_section_num(filepath):
    """Extract section number for sorting, e.g., section-14.3.html -> (14, 3)."""
    name = filepath.name
    m = re.match(r"section-(\w+)\.(\d+)\.html", name)
    if m:
        prefix = m.group(1)
        # Handle letter prefixes like a, b, c for appendices
        try:
            ch = int(prefix)
        except ValueError:
            ch = prefix  # keep as string for appendices
        return (ch, int(m.group(2)))
    return None


def build_chapter_pages(chapter_dir):
    """Build ordered list of pages within a chapter/appendix directory.
    Returns list of Path objects: [index.html, section-X.1.html, section-X.2.html, ...]
    """
    pages = []
    idx = chapter_dir / "index.html"
    if idx.exists():
        pages.append(idx)

    # Find sections
    sections = []
    for f in chapter_dir.glob("section-*.html"):
        snum = get_section_num(f)
        if snum:
            sections.append((snum, f))
    sections.sort(key=lambda x: (str(x[0][0]), x[0][1]))
    pages.extend([f for _, f in sections])

    return pages


def build_front_matter_pages():
    """Build ordered list of front-matter pages."""
    fm = BASE / "front-matter"
    if not fm.exists():
        return []

    # Specific ordering for front matter
    ordered_files = [
        "about-authors.html",
        "about-book.html",
        "section-fm.1.html",
        "pathways/index.html",
        "syllabi/index.html",
        "section-fm.4.html",
        "section-fm.5.html",
        "wisdom-council.html",
        "section-fm.7.html",
        "section-fm.8.html",
    ]

    pages = []
    # Add index
    idx = fm / "index.html"
    if idx.exists():
        pages.append(idx)

    for name in ordered_files:
        f = fm / name
        if f.exists():
            pages.append(f)

    return pages


def build_part_pages(part_dir):
    """Build ordered list of all pages in a part directory."""
    if not part_dir.exists():
        return []

    pages = []

    # Part index
    part_idx = part_dir / "index.html"
    if part_idx.exists():
        pages.append(part_idx)

    # Find all chapter/appendix directories
    if part_dir.name == "appendices":
        chapter_dirs = sorted([
            d for d in part_dir.iterdir()
            if d.is_dir() and d.name.startswith("appendix-") and (d / "index.html").exists()
        ], key=lambda d: d.name)
    else:
        chapter_dirs = sorted([
            d for d in part_dir.iterdir()
            if d.is_dir() and d.name.startswith("module-") and (d / "index.html").exists()
        ], key=lambda d: d.name)

    # Filter out deprecated directories
    chapter_dirs = [d for d in chapter_dirs if not should_skip(d / "index.html")]

    for ch_dir in chapter_dirs:
        pages.extend(build_chapter_pages(ch_dir))

    return pages


def build_full_ordering():
    """Build the complete ordered list of all book pages."""
    all_pages = []

    for part_name in PART_ORDER:
        part_dir = BASE / part_name
        if part_name == "front-matter":
            all_pages.extend(build_front_matter_pages())
        else:
            all_pages.extend(build_part_pages(part_dir))

    return all_pages


def shorten_title(title, max_len=60):
    """Shorten a title if too long for nav display."""
    if len(title) <= max_len:
        return title
    return title[:max_len-3] + "..."


def make_relative_path(from_file, to_file):
    """Compute relative path from one file to another."""
    from_dir = from_file.parent
    try:
        rel = to_file.relative_to(from_dir)
        return str(rel).replace("\\", "/")
    except ValueError:
        pass

    # Walk up from from_dir to common ancestor
    from_parts = from_dir.parts
    to_parts = to_file.parts

    # Find common prefix length
    common = 0
    for a, b in zip(from_parts, to_parts):
        if a == b:
            common += 1
        else:
            break

    ups = len(from_parts) - common
    rel_parts = [".."] * ups + list(to_parts[common:])
    return "/".join(rel_parts)


def update_nav(filepath, prev_path, prev_title, next_path, next_title):
    """Update the chapter-nav block in a file."""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return False

    if 'class="chapter-nav"' not in text:
        return False

    # Extract the nav block
    nav_pattern = re.compile(
        r'(<nav\s+class="chapter-nav">)(.*?)(</nav>)',
        re.DOTALL
    )
    m = nav_pattern.search(text)
    if not m:
        return False

    nav_content = m.group(2)

    # Check if there's an "up" link to preserve
    up_match = re.search(r'<a[^>]*class="up"[^>]*>.*?</a>', nav_content, re.DOTALL)
    up_link = up_match.group(0) if up_match else ""

    # Build new nav content
    new_parts = ["\n"]

    # Prev link
    if prev_path:
        rel = make_relative_path(filepath, prev_path)
        title = shorten_title(prev_title or "Previous")
        # Escape HTML entities
        title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        new_parts.append(f'    <a class="prev" href="{rel}">{title}</a>\n')
    else:
        new_parts.append('    <span class="prev"></span>\n')

    # Up link (preserve existing)
    if up_link:
        new_parts.append(f"    {up_link}\n")

    # Next link
    if next_path:
        rel = make_relative_path(filepath, next_path)
        title = shorten_title(next_title or "Next")
        title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        new_parts.append(f'    <a class="next" href="{rel}">{title}</a>\n')
    else:
        new_parts.append('    <span class="next"></span>\n')

    new_nav_content = "".join(new_parts)
    new_nav = m.group(1) + new_nav_content + m.group(3)
    new_text = text[:m.start()] + new_nav + text[m.end():]

    if new_text != text:
        filepath.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    print("Building complete page ordering...")
    all_pages = build_full_ordering()
    print(f"Found {len(all_pages)} pages in ordering\n")

    # Build title map
    title_map = {}
    for p in all_pages:
        title = extract_title(p)
        title_map[p] = title
        if not title:
            print(f"  WARNING: No title found for {p.relative_to(BASE)}")

    # Build index for quick lookup
    page_index = {p: i for i, p in enumerate(all_pages)}

    # Now process all HTML files with chapter-nav
    updated = 0
    skipped = 0
    no_nav = 0

    # Also find pages NOT in the ordering but with chapter-nav
    all_html = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        if should_skip(f):
            continue
        all_html.append(f)

    for filepath in sorted(all_html):
        try:
            text = filepath.read_text(encoding="utf-8")
        except Exception:
            continue

        if 'class="chapter-nav"' not in text:
            no_nav += 1
            continue

        if filepath not in page_index:
            # Page has nav but isn't in our ordering (pathway pages, syllabi pages, etc.)
            # Skip these, they have their own navigation
            skipped += 1
            continue

        idx = page_index[filepath]
        prev_path = all_pages[idx - 1] if idx > 0 else None
        next_path = all_pages[idx + 1] if idx < len(all_pages) - 1 else None
        prev_title = title_map.get(prev_path) if prev_path else None
        next_title = title_map.get(next_path) if next_path else None

        if update_nav(filepath, prev_path, prev_title, next_path, next_title):
            updated += 1
            rel = filepath.relative_to(BASE)
            pt = prev_title[:30] if prev_title else "None"
            nt = next_title[:30] if next_title else "None"
            print(f"  Updated: {rel}  prev=[{pt}]  next=[{nt}]")

    print(f"\n{'='*60}")
    print(f"SUMMARY: {updated} files updated, {skipped} skipped (not in ordering), {no_nav} without nav")


if __name__ == "__main__":
    main()
