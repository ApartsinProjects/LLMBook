#!/usr/bin/env python3
"""
Embed generated illustrations into section HTML files.

Reads the mapping file and generated images from /tmp/book-illustrations,
copies each image to the correct chapter images/ directory, and inserts
a <figure class="illustration"> element into the HTML.
"""

import json
import re
import shutil
from pathlib import Path

BOOK_ROOT = Path("E:/Projects/LLMCourse")
GENERATED_DIR = Path("/tmp/book-illustrations")
MAPPING_FILE = BOOK_ROOT / "scripts" / "illustration_mapping.json"

FIGURE_TEMPLATE = '''<figure class="illustration">
  <img src="images/{filename}"
       alt="{alt_text}"
       style="max-width: 100%; border-radius: 12px; margin: 1.5rem auto; display: block;"
       loading="lazy">
  <figcaption style="text-align: center; font-style: italic; color: #666; margin-top: 0.5rem;">
    {caption}
  </figcaption>
</figure>

'''


def find_insertion_point(html: str, h2_number: int) -> int:
    """Find the insertion point after the Nth h2 section's first paragraph.

    h2_number=0 means preamble (after the first <p> in <main>).
    h2_number=N means after the first <p> after the Nth <h2>.
    """
    if h2_number == 0:
        # Insert after the first <p>...</p> in <main class="content">
        main_match = re.search(r'<main[^>]*class="content"[^>]*>', html)
        if not main_match:
            main_match = re.search(r'<main[^>]*>', html)
        if not main_match:
            return -1

        # Find first </p> after main
        start = main_match.end()
        # Skip past any callout boxes, epigraphs, etc. to find the first real <p>
        p_end = html.find('</p>', start)
        if p_end == -1:
            return -1
        return p_end + len('</p>') + 1

    # Find the Nth <h2>
    h2_positions = [m.start() for m in re.finditer(r'<h2[^>]*>', html)]
    if h2_number > len(h2_positions):
        # Fall back to last h2
        h2_number = len(h2_positions)
    if h2_number == 0:
        return -1

    h2_pos = h2_positions[h2_number - 1]

    # Find the first </p> after this h2
    p_end = html.find('</p>', h2_pos)
    if p_end == -1:
        return -1
    return p_end + len('</p>') + 1


def main():
    with open(MAPPING_FILE, encoding='utf-8') as f:
        mapping = json.load(f)

    # Check which generated images exist
    generated_files = sorted(GENERATED_DIR.glob("img_*.png"))
    print(f"Found {len(generated_files)} generated images")
    print(f"Mapping has {len(mapping)} entries")

    if len(generated_files) < len(mapping):
        print(f"WARNING: Only {len(generated_files)} images for {len(mapping)} sections")

    success_count = 0
    skip_count = 0
    error_count = 0

    for i, entry in enumerate(mapping):
        img_idx = i + 1
        src_img = GENERATED_DIR / f"img_{img_idx:03d}.png"

        if not src_img.exists():
            print(f"  [{img_idx}] SKIP: {src_img.name} not found")
            skip_count += 1
            continue

        section_path = BOOK_ROOT / entry["section_path"]
        if not section_path.exists():
            print(f"  [{img_idx}] ERROR: Section not found: {entry['section_path']}")
            error_count += 1
            continue

        # Determine chapter images directory
        chapter_dir = section_path.parent
        images_dir = chapter_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)

        # Copy image to chapter images directory
        dest_img = images_dir / entry["image_filename"]
        shutil.copy2(src_img, dest_img)

        # Read HTML
        html = section_path.read_text(encoding='utf-8')

        # Check if illustration already embedded (idempotency)
        if entry["image_filename"] in html:
            print(f"  [{img_idx}] SKIP: Already embedded in {entry['section_path']}")
            skip_count += 1
            continue

        # Find insertion point
        insert_pos = find_insertion_point(html, entry["placement_h2"])
        if insert_pos == -1:
            print(f"  [{img_idx}] ERROR: Could not find insertion point in {entry['section_path']}")
            error_count += 1
            continue

        # Build figure HTML
        figure_html = FIGURE_TEMPLATE.format(
            filename=entry["image_filename"],
            alt_text=entry["alt_text"],
            caption=entry["caption"],
        )

        # Insert
        new_html = html[:insert_pos] + "\n\n" + figure_html + html[insert_pos:]
        section_path.write_text(new_html, encoding='utf-8')

        print(f"  [{img_idx}] OK: {entry['image_filename']} -> {entry['section_path']}")
        success_count += 1

    print(f"\nDone: {success_count} embedded, {skip_count} skipped, {error_count} errors")


if __name__ == "__main__":
    main()
