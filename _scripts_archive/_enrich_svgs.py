"""
SVG Visual Enrichment Script
TASK-022: Add subtle linear gradients to flat-filled rectangles
TASK-023: Add subtle drop shadows to container rectangles

Targets section files in parts 1-5 only, skipping agents/.
"""

import re
import os
import hashlib

BASE = os.path.dirname(os.path.abspath(__file__))

# Collect section files from parts 1-5
section_files = []
for root, dirs, fnames in os.walk(BASE):
    rel = root.replace(os.sep, '/').replace(BASE.replace(os.sep, '/'), '')
    if not any(f'/part-{i}-' in rel for i in range(1, 6)):
        continue
    if '/agents/' in rel:
        continue
    for f in sorted(fnames):
        if f.startswith('section-') and f.endswith('.html'):
            section_files.append(os.path.join(root, f))

section_files.sort()

# Color mapping for gradients: base color -> lighter variant (subtle top-to-bottom lightening)
def lighten(hex_color, amount=20):
    """Lighten a hex color by `amount` units per channel."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c*2 for c in hex_color)
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)
    return f'#{r:02x}{g:02x}{b:02x}'

def make_gradient_id(color):
    """Create a unique gradient ID from a color."""
    clean = color.lstrip('#')
    return f'grad_{clean}'

# Common fill colors found on rectangles in the SVGs (background/container fills)
# We target light background fills and medium-tone fills
GRADIENT_CANDIDATES = {
    '#fafafa', '#f8f9fa', '#ecf0f1', '#e0e0e0',
    '#e8f4fd', '#d6eaf8', '#dbeafe', '#e3f2fd', '#ebf5fb',
    '#d5f5e3', '#d4efdf', '#d1fae5', '#f0fff0', '#e8f8f5',
    '#fef9e7', '#fef9c3', '#fff5f5', '#fee2e2', '#fdebd0',
    '#f3e8ff', '#f0e6ff', '#e8daef', '#ede7f6',
    '#fff', '#ffffff',
    '#f5f5f5', '#f0f0f0', '#e8e8e8', '#f9f9f9',
    '#eaf2f8', '#fdf2e9', '#fdedec', '#eafaf1',
    '#fff8e1', '#e1f5fe', '#f1f8e9', '#fce4ec',
    '#e0f7fa', '#f3e5f5', '#e8eaf6', '#fff3e0',
    '#e1bee7', '#bbdefb', '#c8e6c9', '#ffecb3',
    '#b3e5fc', '#dcedc8', '#f0f4c3', '#ffe0b2',
    '#ffccbc', '#d1c4e9', '#b2dfdb', '#ffcdd2',
    '#cfd8dc', '#f5f5f5', '#eeeeee',
    '#e6f3ff', '#f0f8ff', '#fffde7', '#e0f2f1',
}

# Convert all to lowercase for matching
GRADIENT_CANDIDATES = {c.lower() for c in GRADIENT_CANDIDATES}

def should_add_gradient(fill_color):
    """Check if this fill color should get a gradient."""
    return fill_color.lower() in GRADIENT_CANDIDATES

def process_svg(svg_text, svg_index_in_file, file_path):
    """Process a single SVG, adding gradients and drop shadow. Returns modified SVG."""
    has_gradient = 'linearGradient' in svg_text or 'radialGradient' in svg_text
    has_filter = '<filter' in svg_text
    has_rect = '<rect' in svg_text

    if not has_rect:
        return svg_text, False, False

    added_gradient = False
    added_shadow = False

    # Unique prefix for IDs to avoid conflicts between SVGs
    uid = hashlib.md5(f'{file_path}_{svg_index_in_file}'.encode()).hexdigest()[:6]

    # Collect gradient definitions needed
    gradient_defs = []
    fill_replacements = {}  # old_fill_attr -> new_fill_attr

    if not has_gradient:
        # Find all rect fill colors
        rect_fills = re.findall(r'<rect[^>]*fill="(#[0-9a-fA-F]{3,8})"', svg_text)
        unique_fills = set(rect_fills)

        for color in unique_fills:
            if should_add_gradient(color):
                grad_id = f'grad_{uid}_{color.lstrip("#").lower()}'
                lighter = lighten(color, 15)
                gradient_defs.append(
                    f'<linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">'
                    f'<stop offset="0%" stop-color="{lighter}"/>'
                    f'<stop offset="100%" stop-color="{color}"/>'
                    f'</linearGradient>'
                )
                fill_replacements[color] = f'url(#{grad_id})'
                added_gradient = True

    # Drop shadow filter
    shadow_filter_id = f'shadow_{uid}'
    shadow_def = ''
    if not has_filter:
        shadow_def = (
            f'<filter id="{shadow_filter_id}" x="-5%" y="-5%" width="115%" height="115%">'
            f'<feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.1"/>'
            f'</filter>'
        )
        added_shadow = True

    # Now inject the defs and apply changes
    if not added_gradient and not added_shadow:
        return svg_text, False, False

    # Build new defs content
    new_defs_content = '\n'.join(gradient_defs)
    if shadow_def:
        new_defs_content = (new_defs_content + '\n' + shadow_def) if new_defs_content else shadow_def

    # Insert into existing <defs> or create new one
    if '<defs>' in svg_text or '<defs ' in svg_text:
        # Append to existing defs
        svg_text = re.sub(
            r'(<defs[^>]*>)',
            r'\1\n' + new_defs_content + '\n',
            svg_text,
            count=1
        )
    else:
        # Insert new defs after <svg...>
        svg_text = re.sub(
            r'(<svg[^>]*>)',
            r'\1\n<defs>\n' + new_defs_content + '\n</defs>',
            svg_text,
            count=1
        )

    # Apply gradient fills to rects
    if fill_replacements:
        def replace_rect_fill(match):
            full_rect = match.group(0)
            fill_match = re.search(r'fill="(#[0-9a-fA-F]{3,8})"', full_rect)
            if fill_match:
                color = fill_match.group(1)
                if color in fill_replacements:
                    full_rect = full_rect.replace(
                        f'fill="{color}"',
                        f'fill="{fill_replacements[color]}"'
                    )
            return full_rect

        svg_text = re.sub(r'<rect[^/]*/?>', replace_rect_fill, svg_text)

    # Apply shadow filter to the FIRST large rect (background/container)
    if added_shadow:
        # Find the first rect that looks like a container (typically the first rect, or one with large dimensions)
        def add_shadow_to_first_container(match):
            rect = match.group(0)
            # Check if it already has a filter
            if 'filter=' in rect:
                return rect
            # Add filter attribute
            rect = rect.replace('<rect ', f'<rect filter="url(#{shadow_filter_id})" ', 1)
            return rect

        # Only apply to the first rect (the background container)
        svg_text = re.sub(r'<rect\s[^/]*/?>', add_shadow_to_first_container, svg_text, count=1)

    return svg_text, added_gradient, added_shadow


# Process all files
total_gradient = 0
total_shadow = 0
files_modified = set()

for fp in section_files:
    content = open(fp, encoding='utf-8').read()
    original = content

    svg_pattern = re.compile(r'(<svg[^>]*>.*?</svg>)', re.DOTALL)
    svgs = list(svg_pattern.finditer(content))

    if not svgs:
        continue

    # Process in reverse order to preserve positions
    file_grad = 0
    file_shadow = 0
    for i, match in enumerate(reversed(svgs)):
        idx = len(svgs) - 1 - i
        svg_text = match.group(1)
        new_svg, did_gradient, did_shadow = process_svg(svg_text, idx, fp)

        if did_gradient:
            file_grad += 1
        if did_shadow:
            file_shadow += 1

        if new_svg != svg_text:
            content = content[:match.start(1)] + new_svg + content[match.end(1):]

    if content != original:
        open(fp, 'w', encoding='utf-8').write(content)
        files_modified.add(fp)
        total_gradient += file_grad
        total_shadow += file_shadow
        if file_grad or file_shadow:
            short = fp.replace(BASE, '').replace('\\', '/')
            print(f'  {short}: +{file_grad} gradients, +{file_shadow} shadows')

print(f'\nTotal: {total_gradient} SVGs with gradients, {total_shadow} SVGs with shadows across {len(files_modified)} files')
