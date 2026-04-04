"""
Standardize all HTML headers across the textbook.

Canonical header templates (inline styles removed, CSS handles styling):

Section file:
    book-title-bar -> ../../index.html
    part-label -> ../index.html (Part N: Name)
    chapter-label -> index.html (Chapter NN: Title)
    h1 -> Section Title

Chapter index file:
    book-title-bar -> ../../index.html
    part-label -> ../index.html (Part N: Name)
    h1 -> Chapter NN: Title

Part index file:
    book-title-bar -> ../index.html
    h1 -> Part N: Name

Appendix section file:
    book-title-bar -> ../../index.html
    part-label -> ../../index.html (Appendices) [no appendices/index.html exists]
    chapter-label -> index.html (Appendix X: Title)
    h1 -> Section Title

Appendix index file:
    book-title-bar -> ../../index.html
    part-label -> ../../index.html (Appendices)
    h1 -> Appendix X: Title
"""

import os
import re
import glob

ROOT = r"E:\Projects\LLMCourse"


def classify_file(filepath):
    """Determine the type of HTML file."""
    rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
    parts = rel.split("/")

    # Root-level pages (toc.html, team.html, index.html)
    if len(parts) == 1:
        return "root"

    # Part index files: part-*/index.html
    if len(parts) == 2 and parts[0].startswith("part-") and parts[1] == "index.html":
        return "part-index"

    # Chapter index files: part-*/module-*/index.html
    if (len(parts) == 3 and parts[0].startswith("part-")
            and parts[1].startswith("module-") and parts[2] == "index.html"):
        return "chapter-index"

    # Section files: part-*/module-*/section-*.html
    if (len(parts) == 3 and parts[0].startswith("part-")
            and parts[1].startswith("module-") and parts[2].startswith("section-")):
        return "section"

    # Appendix index files: appendices/appendix-*/index.html
    if (len(parts) == 3 and parts[0] == "appendices"
            and parts[1].startswith("appendix-") and parts[2] == "index.html"):
        return "appendix-index"

    # Appendix section files: appendices/appendix-*/section-*.html
    if (len(parts) == 3 and parts[0] == "appendices"
            and parts[1].startswith("appendix-") and parts[2].startswith("section-")):
        return "appendix-section"

    return "unknown"


def remove_inline_styles_from_header_links(html):
    """Remove inline style= attributes from links inside .part-label and .chapter-label divs."""
    changed = False

    def strip_styles_in_div(match):
        nonlocal changed
        div_html = match.group(0)
        # Remove style="..." from <a> tags within this div
        new_div = re.sub(r'(<a\b[^>]*?)\s+style="[^"]*"', r'\1', div_html)
        # Also remove class="chapter-num" which is a legacy class
        new_div = re.sub(r'(<a\b[^>]*?)\s+class="chapter-num"', r'\1', new_div)
        if new_div != div_html:
            changed = True
        return new_div

    # Match part-label and chapter-label divs
    html = re.sub(
        r'<div\s+class="(?:part-label|chapter-label)">[^<]*<a[^>]*>[^<]*</a>[^<]*</div>',
        strip_styles_in_div,
        html
    )
    return html, changed


def fix_chapter_index_header(html, filepath):
    """
    Fix chapter index headers:
    - chapter-label should NOT exist (remove it)
    - h1 should contain the full "Chapter NN: Title"
    """
    changed = False

    # Check if there's a chapter-label div that links to toc.html (legacy pattern)
    # In chapter index files, the chapter-label links to toc.html with just "Chapter NN"
    # and the h1 has just the title. We need to merge them.
    chapter_label_match = re.search(
        r'<div class="chapter-label"><a href="[^"]*"[^>]*>([^<]*)</a></div>\s*\n\s*<h1>([^<]*)</h1>',
        html
    )
    if chapter_label_match:
        chapter_num = chapter_label_match.group(1).strip()
        title = chapter_label_match.group(2).strip()
        # Only fix if the chapter-label doesn't already contain the full title
        if ":" not in chapter_num:
            new_h1 = f"{chapter_num}: {title}"
            old_block = chapter_label_match.group(0)
            new_block = f"<h1>{new_h1}</h1>"
            html = html.replace(old_block, new_block)
            changed = True

    return html, changed


def fix_appendix_index_header(html, filepath):
    """
    Fix appendix index headers:
    - chapter-label should NOT exist (remove it)
    - h1 should contain the full "Appendix X: Title"
    """
    changed = False

    chapter_label_match = re.search(
        r'<div class="chapter-label"><a href="[^"]*"[^>]*>([^<]*)</a></div>\s*\n\s*<h1>([^<]*)</h1>',
        html
    )
    if chapter_label_match:
        appendix_num = chapter_label_match.group(1).strip()
        title = chapter_label_match.group(2).strip()
        if ":" not in appendix_num:
            new_h1 = f"{appendix_num}: {title}"
            old_block = chapter_label_match.group(0)
            new_block = f"<h1>{new_h1}</h1>"
            html = html.replace(old_block, new_block)
            changed = True

    return html, changed


def fix_part_index_header(html, filepath):
    """
    Fix part index headers:
    - part-label should NOT link to the book title (redundant with book-title-bar)
    - Remove the part-label div entirely; h1 already has "Part N: Name"
    """
    changed = False

    # The current pattern has a part-label linking to the book title, which is redundant
    part_label_match = re.search(
        r'\s*<div class="part-label"><a href="[^"]*">Building Conversational AI with LLMs and Agents</a></div>\s*\n',
        html
    )
    if part_label_match:
        html = html.replace(part_label_match.group(0), "\n")
        changed = True

    return html, changed


def fix_appendix_section_part_label(html, filepath):
    """
    Fix appendix section part-label links.
    The part-label for appendix sections should link to ../../index.html (no appendices index exists).
    """
    changed = False
    # Already correct in existing files based on audit
    return html, changed


def collect_files():
    """Collect all HTML files to process."""
    files = []

    # Part index files
    for f in glob.glob(os.path.join(ROOT, "part-*", "index.html")):
        files.append(f)

    # Chapter index and section files
    for f in glob.glob(os.path.join(ROOT, "part-*", "module-*", "*.html")):
        files.append(f)

    # Appendix index and section files
    for f in glob.glob(os.path.join(ROOT, "appendices", "appendix-*", "*.html")):
        files.append(f)

    return files


def main():
    files = collect_files()
    stats = {
        "total": 0,
        "inline_styles_removed": 0,
        "chapter_index_fixed": 0,
        "appendix_index_fixed": 0,
        "part_index_fixed": 0,
        "skipped_unknown": 0,
    }
    changes_log = []

    for filepath in sorted(files):
        ftype = classify_file(filepath)
        rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
        stats["total"] += 1

        if ftype == "unknown":
            stats["skipped_unknown"] += 1
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            original = f.read()

        html = original
        file_changes = []

        # Step 1: Remove inline styles from all header links (all file types)
        html, style_changed = remove_inline_styles_from_header_links(html)
        if style_changed:
            file_changes.append("removed inline styles")
            stats["inline_styles_removed"] += 1

        # Step 2: Type-specific fixes
        if ftype == "chapter-index":
            html, ch_changed = fix_chapter_index_header(html, filepath)
            if ch_changed:
                file_changes.append("merged chapter-label into h1")
                stats["chapter_index_fixed"] += 1

        elif ftype == "appendix-index":
            html, ap_changed = fix_appendix_index_header(html, filepath)
            if ap_changed:
                file_changes.append("merged appendix chapter-label into h1")
                stats["appendix_index_fixed"] += 1

        elif ftype == "part-index":
            html, pt_changed = fix_part_index_header(html, filepath)
            if pt_changed:
                file_changes.append("removed redundant part-label")
                stats["part_index_fixed"] += 1

        # Write back if changed
        if html != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            changes_log.append((rel, file_changes))

    # Report
    print("=" * 70)
    print("HEADER STANDARDIZATION REPORT")
    print("=" * 70)
    print(f"Files scanned:           {stats['total']}")
    print(f"Inline styles removed:   {stats['inline_styles_removed']}")
    print(f"Chapter index merged:    {stats['chapter_index_fixed']}")
    print(f"Appendix index merged:   {stats['appendix_index_fixed']}")
    print(f"Part index fixed:        {stats['part_index_fixed']}")
    print(f"Skipped (unknown type):  {stats['skipped_unknown']}")
    print(f"Total files changed:     {len(changes_log)}")
    print()

    if changes_log:
        print("CHANGES:")
        print("-" * 70)
        for rel, changes in changes_log:
            print(f"  {rel}")
            for c in changes:
                print(f"    -> {c}")
    else:
        print("No changes needed.")


if __name__ == "__main__":
    main()
