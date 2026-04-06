#!/usr/bin/env python3
"""
Fix deprecated .subtitle class name in header elements across all HTML files.

Handles these cases:
1. Module index files: `<p class="subtitle"><a href="../index.html" ...>Part N</a></p>`
   -> `<div class="part-label"><a href="../index.html" ...>Part N</a></div>`
   Also reorders so part-label comes BEFORE h1 (currently after).

2. Section files with subtitle as part-label link:
   `<div class="subtitle"><a href="../index.html" ...>Part N</a></div>`
   -> `<div class="part-label"><a ...>Part N</a></div>`
   Reorders to: part-label, module-label, h1

3. Section files with `<a class="subtitle" href="../index.html" ...>Part N</a>`
   -> `<div class="part-label"><a href="../index.html" ...>Part N</a></div>`
   Reorders to: part-label, module-label, h1

4. Section files with subtitle as description text (after h1):
   `<div class="subtitle">description</div>` -> just rename class to "chapter-subtitle"
   (These are NOT part-labels; they are descriptive subtitles.)

5. Part index / main index / appendix / capstone subtitle descriptions:
   `<p class="subtitle">description</p>` -> rename to "chapter-subtitle"

6. CSS rules: `.subtitle` -> update accordingly

Also fixes header element order to: part-label first, module-label second, h1 third.
"""

import os
import re
import glob

BASE = r"E:\Projects\LLMCourse"
CHANGES = []


def log(filepath, msg):
    rel = os.path.relpath(filepath, BASE)
    CHANGES.append((rel, msg))


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def fix_css_subtitle(content, filepath):
    """Rename .subtitle CSS rules based on context."""
    changed = False

    # For module index files: the .subtitle is used as a part-label link
    # For section files: .subtitle might be a part-label or a description
    # We need to handle CSS renaming carefully

    # Pattern: `.chapter-header .subtitle` or `header .subtitle` CSS rules
    # Replace with `.chapter-header .chapter-subtitle` / `header .chapter-subtitle`
    # But ALSO add .part-label rules if not present

    # Replace CSS selector `.subtitle` with `.chapter-subtitle` for description subtitles
    # We'll do targeted replacements

    # Replace `.chapter-header .subtitle {` with `.chapter-header .chapter-subtitle {`
    old = ".chapter-header .subtitle {"
    new = ".chapter-header .chapter-subtitle {"
    if old in content:
        content = content.replace(old, new)
        changed = True

    old = ".chapter-header .subtitle{"
    new = ".chapter-header .chapter-subtitle{"
    if old in content:
        content = content.replace(old, new)
        changed = True

    # Replace `header .subtitle {` with `header .chapter-subtitle {`
    old = "header .subtitle {"
    new = "header .chapter-subtitle {"
    if old in content:
        content = content.replace(old, new)
        changed = True

    old = "header .subtitle{"
    new = "header .chapter-subtitle{"
    if old in content:
        content = content.replace(old, new)
        changed = True

    # Standalone `.subtitle {` CSS rule (indented, in section files)
    # Match lines like `    .subtitle {` or `        .subtitle {`
    pattern = r'([ \t]+)\.subtitle(\s*\{)'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1.chapter-subtitle\2', content)
        changed = True

    if changed:
        log(filepath, "Renamed .subtitle CSS rule(s) to .chapter-subtitle")

    return content, changed


def is_part_label_content(text):
    """Check if subtitle content is a Part label link (not a description)."""
    return bool(re.search(r'Part\s+[IVXLC]+|Part\s+\d+', text))


def fix_module_index_header(content, filepath):
    """
    Fix module index files where:
    - header has: module-num/module-label, h1, <p class="subtitle"><a>Part</a></p>
    - Should be: <div class="part-label"><a>Part</a></div>, module-label, h1
    """
    changed = False

    # Pattern: <p class="subtitle"><a href="..." ...>Part ...</a></p>
    # This appears in module index files AFTER h1, needs to move BEFORE h1
    # Match both <header class="chapter-header"> and plain <header>
    header_pattern = re.compile(
        r'(<header[^>]*>)(.*?)(</header>)',
        re.DOTALL
    )

    match = header_pattern.search(content)
    if not match:
        return content, False

    header_open = match.group(1)
    header_body = match.group(2)
    header_close = match.group(3)

    # Check for subtitle with Part link inside header
    subtitle_part_link = re.search(
        r'<p\s+class="subtitle">\s*<a\s+[^>]*>(Part\s+[^<]+)</a>\s*</p>',
        header_body
    )

    if not subtitle_part_link:
        # Also check for <div class="subtitle"><a ...>Part ...</a></div>
        subtitle_part_link = re.search(
            r'<div\s+class="subtitle">\s*<a\s+[^>]*>(Part\s+[^<]+)</a>\s*</div>',
            header_body
        )

    if not subtitle_part_link:
        # Check for <a class="subtitle" ...>Part ...</a>
        subtitle_part_link = re.search(
            r'<a\s+[^>]*class="subtitle"[^>]*>(Part\s+[^<]+)</a>',
            header_body
        )

    if subtitle_part_link and is_part_label_content(subtitle_part_link.group(0)):
        # Remove the old subtitle element
        old_subtitle = subtitle_part_link.group(0)

        # Extract the href from the link
        href_match = re.search(r'href="([^"]*)"', old_subtitle)
        href = href_match.group(1) if href_match else "../index.html"

        # Extract the Part text
        part_text_match = re.search(r'>(Part\s+[^<]+)<', old_subtitle)
        part_text = part_text_match.group(1) if part_text_match else "Part"

        # Build the new part-label div
        new_part_label = f'<div class="part-label"><a href="{href}" style="color: rgba(255,255,255,0.85); text-decoration: none;">{part_text}</a></div>'

        # Remove old subtitle from header body
        header_body = header_body.replace(old_subtitle, "")

        # Clean up any resulting blank lines
        header_body = re.sub(r'\n\s*\n\s*\n', '\n\n', header_body)

        # Now find h1 and module-label in header to reorder
        # We want: part-label, module-label/module-num, h1
        h1_match = re.search(r'<h1[^>]*>.*?</h1>', header_body, re.DOTALL)
        module_match = re.search(
            r'(?:<div\s+class="module-label"[^>]*>.*?</div>|<a\s+[^>]*class="module-(?:num|label)"[^>]*>.*?</a>)',
            header_body, re.DOTALL
        )

        if h1_match and module_match:
            # Remove existing elements
            h1_text = h1_match.group(0)
            module_text = module_match.group(0)

            # If module is a bare <a>, wrap in div
            if module_text.startswith("<a"):
                inner_a = module_text
                # Fix: wrap in div class="module-label"
                module_text_new = f'<div class="module-label">{inner_a}</div>'
            else:
                module_text_new = module_text

            # Strip everything and rebuild
            header_body_clean = header_body
            header_body_clean = header_body_clean.replace(h1_text, "")
            header_body_clean = header_body_clean.replace(module_match.group(0), "")
            # Remove leftover whitespace
            header_body_clean = re.sub(r'\n\s*\n', '\n', header_body_clean).strip()

            # Rebuild header body
            new_header_body = f"""
    {new_part_label}
    {module_text_new}
    {h1_text}
"""
            content = content.replace(
                header_open + match.group(2) + header_close,
                header_open + new_header_body + header_close
            )
            changed = True
            log(filepath, "Converted subtitle Part link to part-label and reordered header")
        else:
            # Just replace class name
            header_body = "\n    " + new_part_label + header_body
            content = content.replace(
                header_open + match.group(2) + header_close,
                header_open + header_body + header_close
            )
            changed = True
            log(filepath, "Converted subtitle Part link to part-label")

    return content, changed


def fix_section_header(content, filepath):
    """
    Fix section files where subtitle is used as:
    1. A Part label link (should become part-label, reorder)
    2. A description subtitle (just rename class)
    """
    changed = False

    # Match both <header class="chapter-header"> and plain <header>
    header_pattern = re.compile(
        r'(<header[^>]*>)(.*?)(</header>)',
        re.DOTALL
    )

    match = header_pattern.search(content)
    if not match:
        return content, False

    header_open = match.group(1)
    header_body = match.group(2)
    header_close = match.group(3)
    original_header = match.group(0)

    # Case 1: <div class="subtitle"><a href="../index.html" ...>Part N</a></div>
    # or <a class="subtitle" href="../index.html" ...>Part N</a>
    part_link_in_div = re.search(
        r'<div\s+class="subtitle">\s*(<a\s+[^>]*>Part\s+[^<]+</a>)\s*</div>',
        header_body
    )
    bare_a_subtitle = re.search(
        r'<a\s+[^>]*class="subtitle"[^>]*>Part\s+[^<]+</a>',
        header_body
    )

    if part_link_in_div:
        old = part_link_in_div.group(0)
        inner_a = part_link_in_div.group(1)
        # Ensure the link has proper styling
        if 'style=' not in inner_a:
            inner_a = inner_a.replace('<a ', '<a style="color: rgba(255,255,255,0.85); text-decoration: none;" ')
        new = f'<div class="part-label">{inner_a}</div>'
        header_body = header_body.replace(old, new)
        changed = True
        log(filepath, "Renamed subtitle div to part-label (Part link)")

    elif bare_a_subtitle:
        old = bare_a_subtitle.group(0)
        # Extract href and text
        href_match = re.search(r'href="([^"]*)"', old)
        text_match = re.search(r'>(Part\s+[^<]+)<', old)
        href = href_match.group(1) if href_match else "../index.html"
        text = text_match.group(1) if text_match else "Part"
        new = f'<div class="part-label"><a href="{href}" style="color: rgba(255,255,255,0.85); text-decoration: none;">{text}</a></div>'
        header_body = header_body.replace(old, new)
        changed = True
        log(filepath, "Converted <a class=subtitle> to <div class=part-label>")

    # Case 2: <div class="subtitle">description text</div> (no Part link)
    desc_subtitle = re.search(
        r'<div\s+class="subtitle">([^<]*(?:<(?!a\s)[^<]*)*)</div>',
        header_body
    )
    if desc_subtitle and not is_part_label_content(desc_subtitle.group(1)):
        old = desc_subtitle.group(0)
        new = old.replace('class="subtitle"', 'class="chapter-subtitle"')
        header_body = header_body.replace(old, new)
        changed = True
        log(filepath, "Renamed description subtitle to chapter-subtitle")

    if changed:
        # Now reorder: part-label first, module-label second, h1 third
        # Parse elements
        part_label = re.search(r'<div\s+class="part-label"[^>]*>.*?</div>', header_body, re.DOTALL)
        module_label = re.search(
            r'(?:<div\s+class="module-label"[^>]*>.*?</div>|<a\s+[^>]*class="module-(?:label|num)"[^>]*>.*?</a>)',
            header_body, re.DOTALL
        )
        h1_el = re.search(r'<h1[^>]*>.*?</h1>', header_body, re.DOTALL)
        chapter_sub = re.search(r'<div\s+class="chapter-subtitle"[^>]*>.*?</div>', header_body, re.DOTALL)

        if part_label and module_label and h1_el:
            # Check current order
            pl_pos = header_body.index(part_label.group(0))
            ml_pos = header_body.index(module_label.group(0))
            h1_pos = header_body.index(h1_el.group(0))

            if not (pl_pos < ml_pos < h1_pos):
                # Need to reorder
                # Remove all three (and optional chapter-subtitle)
                elements_to_remove = [part_label.group(0), module_label.group(0), h1_el.group(0)]
                if chapter_sub:
                    elements_to_remove.append(chapter_sub.group(0))

                temp = header_body
                for el in elements_to_remove:
                    temp = temp.replace(el, "")
                temp = re.sub(r'\n\s*\n', '\n', temp).strip()

                # Wrap bare <a> module-label in div if needed
                ml_text = module_label.group(0)
                if ml_text.startswith("<a"):
                    ml_text = f'<div class="module-label">{ml_text}</div>'

                # Rebuild
                parts = [
                    f"    {part_label.group(0)}",
                    f"    {ml_text}",
                    f"    {h1_el.group(0)}"
                ]
                if chapter_sub:
                    parts.append(f"    {chapter_sub.group(0)}")

                new_header_body = "\n" + "\n".join(parts) + "\n"
                content = content.replace(original_header, header_open + new_header_body + header_close)
                log(filepath, "Reordered header elements: part-label, module-label, h1")
                return content, True

        content = content.replace(original_header, header_open + header_body + header_close)

    return content, changed


def fix_description_subtitle(content, filepath):
    """Fix remaining <p class="subtitle"> and <div class="subtitle"> that are descriptions."""
    changed = False

    # <p class="subtitle">description</p> (in part indexes, appendices, main index, etc.)
    for pat in [
        r'<p\s+class="subtitle">([^<]*(?:<(?!/p>)[^<]*)*)</p>',
        r'<div\s+class="subtitle">([^<]*(?:<(?!/div>)[^<]*)*)</div>',
    ]:
        for m in re.finditer(pat, content):
            full = m.group(0)
            inner = m.group(1)
            # If it contains a Part link, skip (handled elsewhere)
            if is_part_label_content(inner):
                continue
            new = full.replace('class="subtitle"', 'class="chapter-subtitle"')
            if new != full:
                content = content.replace(full, new)
                changed = True
                log(filepath, "Renamed description <p/div class=subtitle> to chapter-subtitle")

    return content, changed


def fix_bare_part_links(content, filepath):
    """
    Fix bare <a> Part links in headers that were never wrapped in part-label.
    Pattern: <a href="../index.html" style="...">Part N: Name</a> directly in header
    (not wrapped in any div with a class).
    """
    changed = False

    header_pattern = re.compile(
        r'(<header[^>]*>)(.*?)(</header>)',
        re.DOTALL
    )

    match = header_pattern.search(content)
    if not match:
        return content, False

    header_open = match.group(1)
    header_body = match.group(2)
    header_close = match.group(3)
    original_header = match.group(0)

    # Skip if already has part-label
    if 'class="part-label"' in header_body:
        # Still check order
        pass
    else:
        # Look for bare <a> with Part text that's NOT inside a div/p with a class
        # Pattern: a line with just <a href="..." style="...">Part N: ...</a>
        bare_part = re.search(
            r'(\n\s*)<a\s+href="([^"]*)"[^>]*>(Part\s+[^<]+)</a>',
            header_body
        )
        if bare_part and is_part_label_content(bare_part.group(3)):
            # Check it's not already inside a div with a class
            full_match = bare_part.group(0)
            href = bare_part.group(2)
            part_text = bare_part.group(3)
            indent = bare_part.group(1)

            new_part_label = f'{indent}<div class="part-label"><a href="{href}" style="color: rgba(255,255,255,0.85); text-decoration: none;">{part_text}</a></div>'
            header_body = header_body.replace(full_match, new_part_label)
            changed = True
            log(filepath, "Wrapped bare Part link in <div class=part-label>")

    # Now check/fix order: part-label, module-label, h1
    part_label = re.search(r'<div\s+class="part-label"[^>]*>.*?</div>', header_body, re.DOTALL)
    module_label = re.search(
        r'(?:<div\s+class="module-label"[^>]*>.*?</div>|<a\s+[^>]*class="module-(?:label|num)"[^>]*>.*?</a>)',
        header_body, re.DOTALL
    )
    h1_el = re.search(r'<h1[^>]*>.*?</h1>', header_body, re.DOTALL)
    chapter_sub = re.search(r'<div\s+class="chapter-subtitle"[^>]*>.*?</div>', header_body, re.DOTALL)

    if part_label and module_label and h1_el:
        pl_pos = header_body.index(part_label.group(0))
        ml_pos = header_body.index(module_label.group(0))
        h1_pos = header_body.index(h1_el.group(0))

        if not (pl_pos < ml_pos < h1_pos):
            # Need to reorder
            elements_to_remove = [part_label.group(0), module_label.group(0), h1_el.group(0)]
            if chapter_sub:
                elements_to_remove.append(chapter_sub.group(0))

            temp = header_body
            for el in elements_to_remove:
                temp = temp.replace(el, "")
            temp = re.sub(r'\n\s*\n', '\n', temp).strip()

            ml_text = module_label.group(0)
            if ml_text.startswith("<a"):
                ml_text = f'<div class="module-label">{ml_text}</div>'

            parts = [
                f"    {part_label.group(0)}",
                f"    {ml_text}",
                f"    {h1_el.group(0)}"
            ]
            if chapter_sub:
                parts.append(f"    {chapter_sub.group(0)}")

            new_header_body = "\n" + "\n".join(parts) + "\n"
            content = content.replace(original_header, header_open + new_header_body + header_close)
            changed = True
            log(filepath, "Reordered header: part-label, module-label, h1")
            return content, changed

    if changed:
        content = content.replace(original_header, header_open + header_body + header_close)

    return content, changed


def fix_file(filepath):
    """Process a single HTML file."""
    content = read_file(filepath)
    original = content
    any_changed = False

    # Step 1: Fix CSS rules
    content, c = fix_css_subtitle(content, filepath)
    any_changed = any_changed or c

    # Step 2: Fix module index headers (Part link as subtitle after h1)
    content, c = fix_module_index_header(content, filepath)
    any_changed = any_changed or c

    # Step 3: Fix section headers
    content, c = fix_section_header(content, filepath)
    any_changed = any_changed or c

    # Step 4: Fix remaining description subtitles
    content, c = fix_description_subtitle(content, filepath)
    any_changed = any_changed or c

    # Step 5: Fix bare Part links and reorder headers
    content, c = fix_bare_part_links(content, filepath)
    any_changed = any_changed or c

    if any_changed:
        write_file(filepath, content)

    return any_changed


def main():
    # Find all HTML files (excluding agents/ directory)
    all_html = []
    for root, dirs, files in os.walk(BASE):
        # Skip agents directory and hidden dirs
        rel = os.path.relpath(root, BASE)
        if rel.startswith("agents") or rel.startswith("."):
            continue
        if "node_modules" in rel or ".git" in rel:
            continue
        for f in files:
            if f.endswith(".html"):
                all_html.append(os.path.join(root, f))

    all_html.sort()

    files_changed = 0
    files_scanned = 0

    for filepath in all_html:
        files_scanned += 1
        if fix_file(filepath):
            files_changed += 1

    # Report
    print(f"\nScanned {files_scanned} HTML files.")
    print(f"Changed {files_changed} files.\n")

    if CHANGES:
        print("Changes made:")
        seen = set()
        for rel_path, msg in CHANGES:
            key = f"  {rel_path}: {msg}"
            if key not in seen:
                print(key)
                seen.add(key)
    else:
        print("No changes needed.")

    # Verify: check if any class="subtitle" remains (excluding agents/)
    remaining = []
    for filepath in all_html:
        content = read_file(filepath)
        if 'class="subtitle"' in content:
            rel = os.path.relpath(filepath, BASE)
            remaining.append(rel)

    if remaining:
        print(f"\nWARNING: {len(remaining)} files still have class=\"subtitle\":")
        for r in remaining:
            print(f"  {r}")
    else:
        print("\nVerification passed: no class=\"subtitle\" remains in any HTML file (excluding agents/).")

    # Also check for CSS .subtitle rules
    css_remaining = []
    for filepath in all_html:
        content = read_file(filepath)
        if re.search(r'\.subtitle\s*\{', content) or re.search(r'\.subtitle\s*,', content):
            rel = os.path.relpath(filepath, BASE)
            css_remaining.append(rel)

    if css_remaining:
        print(f"\nWARNING: {len(css_remaining)} files still have .subtitle CSS rules:")
        for r in css_remaining:
            print(f"  {r}")
    else:
        print("Verification passed: no .subtitle CSS rules remain.")


if __name__ == "__main__":
    main()
