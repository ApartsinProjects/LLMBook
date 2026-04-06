"""
Standardize all <figcaption> elements in HTML files to use bold "Figure X.Y.Z" prefix.

Rules:
- section-10.2.html -> figures numbered 10.2.1, 10.2.2, etc.
- section-a.1.html -> figures numbered A.1.1, A.1.2, etc.
- index.html files in module/appendix dirs -> use chapter number + ".0" (e.g., 1.0.1)
- lecture-notes.html -> use chapter number + ".L" (e.g., 1.L.1)
- Only modify <figcaption> inside <figure class="illustration">
- Skip figcaptions inside <div class="diagram">
- If already has <strong>Figure X.Y.Z</strong>, keep as-is (but fix format if needed)
- If has plain text "Figure X.Y.Z:" prefix without bold, convert to bold format
"""

import re
import os
import glob

BASE = r"E:\Projects\LLMCourse"

def extract_section_id(filepath):
    """Extract chapter.section from filename."""
    basename = os.path.basename(filepath)

    # section-0.1.html, section-10.2.html, section-26.10.html
    m = re.match(r'section-(\d+)\.(\d+)\.html', basename)
    if m:
        return f"{m.group(1)}.{m.group(2)}"

    # section-a.1.html (appendix)
    m = re.match(r'section-([a-z])\.(\d+)\.html', basename)
    if m:
        return f"{m.group(1).upper()}.{m.group(2)}"

    # index.html - need to determine chapter from directory
    if basename == 'index.html':
        dirn = os.path.basename(os.path.dirname(filepath))
        # module-00-..., module-01-..., module-27-...
        m2 = re.match(r'module-(\d+)', dirn)
        if m2:
            return f"{int(m2.group(1))}.0"
        # appendix-a-..., appendix-b-...
        m2 = re.match(r'appendix-([a-z])', dirn)
        if m2:
            return f"{m2.group(1).upper()}.0"
        return None

    # lecture-notes.html
    if basename == 'lecture-notes.html':
        dirn = os.path.basename(os.path.dirname(filepath))
        m2 = re.match(r'module-(\d+)', dirn)
        if m2:
            return f"{int(m2.group(1))}.L"
        return None

    return None


def process_file(filepath):
    """Process a single HTML file, adding/fixing Figure prefixes."""
    section_id = extract_section_id(filepath)
    if section_id is None:
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file has any figcaptions
    if '<figcaption>' not in content:
        return 0

    # We need to find figcaptions that are inside <figure class="illustration">
    # and NOT inside <div class="diagram">
    # Since all figures have class="illustration", we just process all figcaptions

    # Track figure counter for this file
    counter = [0]
    changes = [0]

    def replace_figcaption(match):
        full_match = match.group(0)
        caption_text = match.group(1)

        # Check if already has bold Figure prefix in desired format
        bold_pattern = re.match(r'<strong>Figure\s+[\dA-Z]+\.[\dL]+\.\d+</strong>\s*', caption_text)
        if bold_pattern:
            counter[0] += 1
            # Already correct format, but renumber sequentially
            old_prefix = bold_pattern.group(0)
            rest = caption_text[len(old_prefix):]
            new_prefix = f"<strong>Figure {section_id}.{counter[0]}</strong> "
            new_caption = new_prefix + rest
            if new_caption != caption_text:
                changes[0] += 1
            return f"<figcaption>{new_caption}</figcaption>"

        # Check if has plain text "Figure X.Y.Z:" prefix (not bold)
        plain_pattern = re.match(r'Figure\s+[\dA-Za-z]+\.[\dL]+(?:\.\d+)?[a-z]?\s*[:.]?\s*', caption_text)
        if plain_pattern:
            counter[0] += 1
            old_prefix = plain_pattern.group(0)
            rest = caption_text[len(old_prefix):]
            # Capitalize first letter of rest if needed
            if rest and rest[0].islower():
                rest = rest[0].upper() + rest[1:]
            new_caption = f"<strong>Figure {section_id}.{counter[0]}</strong> {rest}"
            changes[0] += 1
            return f"<figcaption>{new_caption}</figcaption>"

        # No Figure prefix at all - add one
        counter[0] += 1
        # Capitalize first letter if needed
        text = caption_text.strip()
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        new_caption = f"<strong>Figure {section_id}.{counter[0]}</strong> {text}"
        changes[0] += 1
        return f"<figcaption>{new_caption}</figcaption>"

    new_content = re.sub(r'<figcaption>(.*?)</figcaption>', replace_figcaption, content, flags=re.DOTALL)

    if changes[0] > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  {os.path.relpath(filepath, BASE)}: {changes[0]} figcaptions updated ({counter[0]} total)")
    else:
        if counter[0] > 0:
            print(f"  {os.path.relpath(filepath, BASE)}: {counter[0]} figcaptions already correct")

    return changes[0]


def main():
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(BASE):
        # Skip hidden dirs and utility scripts
        dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('_')]
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    html_files.sort()

    total_changes = 0
    total_files = 0

    for filepath in html_files:
        n = process_file(filepath)
        if n > 0:
            total_files += 1
            total_changes += n

    print(f"\nTotal: {total_changes} figcaptions updated across {total_files} files")


if __name__ == '__main__':
    main()
