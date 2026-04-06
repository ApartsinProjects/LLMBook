"""
Link orphaned images back to chapter HTML pages where they make sense.

Strategy:
1. Find all orphaned images (exist in images/ dirs but not referenced by any HTML)
2. For each orphaned image, determine the chapter it belongs to from the path
3. Find the best section file in that chapter to insert it
4. Match image filename keywords to section content to find the best fit
5. Insert an <img> with caption at an appropriate location

Excludes: appendices, vendor, scripts, front-matter agent avatars, styles/icons
"""

import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(r"E:\Projects\LLMCourse")
SKIP_DIRS = {"vendor", "node_modules", ".git", "__pycache__", "scripts", "_lab_fragments"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


def should_skip(fpath: Path) -> bool:
    parts = fpath.relative_to(ROOT).parts
    return any(p in SKIP_DIRS for p in parts)


def find_referenced_images() -> set:
    """Find all images currently referenced in HTML."""
    referenced = set()
    for fpath in ROOT.rglob("*.html"):
        if should_skip(fpath):
            continue
        text = fpath.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'<img\s[^>]*src="([^"]+)"', text):
            ref = m.group(1)
            if ref.startswith("http") or ref.startswith("data:"):
                continue
            abs_path = (fpath.parent / ref).resolve()
            referenced.add(abs_path)
    return referenced


def find_orphaned_chapter_images(referenced: set) -> dict:
    """Find orphaned images grouped by chapter directory. Exclude appendices and non-chapter dirs."""
    orphaned = defaultdict(list)
    for fpath in sorted(ROOT.rglob("*")):
        if fpath.suffix.lower() not in IMAGE_EXTS:
            continue
        if should_skip(fpath):
            continue
        if fpath.resolve() in referenced:
            continue

        rel = fpath.relative_to(ROOT)
        parts = rel.parts

        # Skip appendices
        if any(p.startswith("appendix") or p == "appendices" for p in parts):
            continue
        # Skip root-level images
        if len(parts) <= 2 and parts[0] != "part-":
            if not str(parts[0]).startswith("part-"):
                continue
        # Skip front-matter agent avatars and styles/icons
        if "agents" in str(fpath) and "avatars" in str(fpath):
            continue
        if "styles" in str(fpath) and "icons" in str(fpath):
            continue
        if "images/icons" in str(fpath).replace("\\", "/"):
            continue
        if "front-matter" in str(fpath) and "agents" in str(fpath):
            continue

        # Must be in a part/module/images directory
        if "images" not in parts:
            continue

        # Find the chapter (module) directory
        chapter_dir = fpath.parent.parent  # images/ -> module dir
        if chapter_dir.exists() and str(chapter_dir.relative_to(ROOT)).startswith("part-"):
            orphaned[str(chapter_dir)].append(fpath)

    return orphaned


def image_name_to_keywords(img_path: Path) -> list:
    """Extract keywords from image filename."""
    stem = img_path.stem.lower()
    # Remove common prefixes
    stem = re.sub(r'^(chapter-opener|fig-?\d+[.-]?\d*)', '', stem)
    # Split on hyphens and underscores
    words = re.split(r'[-_]', stem)
    # Filter short words and common terms
    stop = {'the', 'and', 'for', 'with', 'from', 'into', 'png', 'jpg', 'svg', 'img', 'figure', 'diagram'}
    keywords = [w for w in words if len(w) > 2 and w not in stop]
    return keywords


def find_best_section(chapter_dir: Path, keywords: list) -> tuple:
    """Find the section file that best matches the image keywords. Returns (section_path, score)."""
    best_path = None
    best_score = 0

    for section_file in sorted(Path(chapter_dir).glob("section-*.html")):
        text = section_file.read_text(encoding="utf-8", errors="ignore").lower()
        score = sum(1 for kw in keywords if kw in text)
        # Bonus for multiple keyword matches
        if score > best_score:
            best_score = score
            best_path = section_file

    return best_path, best_score


def get_figure_number(section_path: Path, text: str) -> str:
    """Compute the next figure number for this section."""
    # Extract section number from filename (e.g., section-22.3.html -> 22.3)
    m = re.search(r'section-(\d+\.\d+)', section_path.name)
    if not m:
        return ""
    section_num = m.group(1)

    # Count existing figures
    existing = len(re.findall(r'Figure\s+' + re.escape(section_num) + r'\.\d+', text))
    next_num = existing + 1
    return f"Figure {section_num}.{next_num}"


def make_caption_from_filename(img_path: Path) -> str:
    """Create a human-readable caption from the image filename."""
    stem = img_path.stem
    # Replace hyphens with spaces, title case
    caption = stem.replace('-', ' ').replace('_', ' ')
    # Capitalize properly
    caption = caption.title()
    return caption


def insert_image_in_section(section_path: Path, img_path: Path) -> bool:
    """Insert an image reference into the section file. Returns True if successful."""
    text = section_path.read_text(encoding="utf-8", errors="ignore")

    # Compute relative path from section to image
    rel_img = Path("images") / img_path.name

    # Check if already referenced
    if img_path.name in text:
        return False

    fig_num = get_figure_number(section_path, text)
    caption = make_caption_from_filename(img_path)

    # Build the image block
    img_block = f'''
    <figure>
        <img src="{rel_img}" alt="{caption}" style="max-width: 100%; height: auto; border-radius: 8px; margin: 1rem auto; display: block;">
        <figcaption class="diagram-caption">{fig_num}: {caption}</figcaption>
    </figure>
'''

    # Find the best insertion point: before the first <h2> or <h3> after the first third of content
    # Or before the nav/footer if no good spot

    # Strategy: insert before the last <h2> or <h3> in the content (before exercises/whats-next)
    # This places illustrations in the middle-to-late part of the section

    # Find all h2/h3 positions
    headings = list(re.finditer(r'<h[23][^>]*>', text))

    # Find nav position as boundary
    nav_pos = text.find('<nav class="chapter-nav">')
    if nav_pos == -1:
        nav_pos = text.find('</main>')
    if nav_pos == -1:
        nav_pos = text.find('<footer>')
    if nav_pos == -1:
        return False

    # Filter headings that are before nav
    valid_headings = [h for h in headings if h.start() < nav_pos]

    if len(valid_headings) >= 2:
        # Insert before the last heading (usually exercises or summary)
        insert_pos = valid_headings[-1].start()
    elif len(valid_headings) == 1:
        # Insert before nav
        insert_pos = nav_pos
    else:
        # Insert before nav
        insert_pos = nav_pos

    # Find a clean line break before the insertion point
    line_start = text.rfind('\n', 0, insert_pos)
    if line_start == -1:
        line_start = insert_pos

    new_text = text[:line_start] + '\n' + img_block + text[line_start:]
    section_path.write_text(new_text, encoding="utf-8")
    return True


def main():
    print("=" * 70)
    print("LINKING ORPHANED IMAGES TO CHAPTER PAGES")
    print("(Excluding appendices)")
    print("=" * 70)

    referenced = find_referenced_images()
    print(f"Found {len(referenced)} currently referenced images")

    orphaned = find_orphaned_chapter_images(referenced)
    total_orphaned = sum(len(imgs) for imgs in orphaned.values())
    print(f"Found {total_orphaned} orphaned chapter images across {len(orphaned)} chapters")

    linked = 0
    skipped = 0

    for chapter_dir, images in sorted(orphaned.items()):
        chapter_rel = Path(chapter_dir).relative_to(ROOT)
        print(f"\n  {chapter_rel}/ ({len(images)} orphaned images)")

        for img in images:
            keywords = image_name_to_keywords(img)
            if not keywords:
                print(f"    SKIP (no keywords): {img.name}")
                skipped += 1
                continue

            section_path, score = find_best_section(Path(chapter_dir), keywords)

            if section_path is None or score < 1:
                print(f"    SKIP (no matching section, score={score}): {img.name}")
                skipped += 1
                continue

            section_rel = section_path.relative_to(ROOT)
            if insert_image_in_section(section_path, img):
                print(f"    LINKED: {img.name} -> {section_rel} (score={score}, keywords={keywords})")
                linked += 1
            else:
                print(f"    SKIP (already present or failed): {img.name}")
                skipped += 1

    print(f"\n{'=' * 70}")
    print(f"SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Orphaned images found:  {total_orphaned}")
    print(f"  Successfully linked:    {linked}")
    print(f"  Skipped:                {skipped}")


if __name__ == "__main__":
    main()
