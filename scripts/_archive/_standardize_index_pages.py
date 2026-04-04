#!/usr/bin/env python3
"""
Standardize all Part index and Chapter index pages in the LLM Course.

Part index pages: Remove inline styles, remove .part-label, ensure footer inside .content.
Chapter index pages: Remove inline styles, ensure .part-label, add chapter-nav, ensure footer inside .content.
"""

import os
import re
import glob
from pathlib import Path

BASE = r"E:\Projects\LLMCourse"

# ============================================================
# Part ordering: list of (part_dir_name, part_roman, part_title)
# and within each part, the ordered list of module directory names
# ============================================================

PARTS_ORDER = [
    ("part-1-foundations", "I", "Foundations", [
        "module-00-ml-pytorch-foundations",
        "module-01-foundations-nlp-text-representation",
        "module-02-tokenization-subword-models",
        "module-03-sequence-models-attention",
        "module-04-transformer-architecture",
        "module-05-decoding-text-generation",
    ]),
    ("part-2-understanding-llms", "II", "Understanding LLMs", [
        "module-06-pretraining-scaling-laws",
        "module-07-modern-llm-landscape",
        "module-08-reasoning-test-time-compute",
        "module-09-inference-optimization",
        "module-18-interpretability",
    ]),
    ("part-3-working-with-llms", "III", "Working with LLMs", [
        "module-10-llm-apis",
        "module-11-prompt-engineering",
        "module-12-hybrid-ml-llm",
    ]),
    ("part-4-training-adapting", "IV", "Training and Adapting", [
        "module-13-synthetic-data",
        "module-14-fine-tuning-fundamentals",
        "module-15-peft",
        "module-16-distillation-merging",
        "module-17-alignment-rlhf-dpo",
    ]),
    ("part-5-retrieval-conversation", "V", "Retrieval and Conversation", [
        "module-19-embeddings-vector-db",
        "module-20-rag",
        "module-21-conversational-ai",
    ]),
    ("part-6-agentic-ai", "VI", "Agentic AI", [
        "module-22-ai-agents",
        "module-23-tool-use-protocols",
        "module-24-multi-agent-systems",
        "module-25-specialized-agents",
        "module-26-agent-safety-production",
    ]),
    ("part-7-multimodal-applications", "VII", "AI Applications", [
        "module-27-multimodal",
        "module-28-llm-applications",
    ]),
    ("part-8-evaluation-production", "VIII", "Evaluation & Production", [
        "module-29-evaluation-observability",
        "module-30-observability-monitoring",
        "module-31-production-engineering",
    ]),
    ("part-9-safety-strategy", "IX", "Safety & Strategy", [
        "module-32-safety-ethics-regulation",
        "module-33-strategy-product-roi",
    ]),
    ("part-10-frontiers", "X", "Frontiers", [
        "module-34-emerging-architectures",
        "module-35-ai-society",
    ]),
]

# Build a flat ordered list of all chapters across all parts
ALL_CHAPTERS = []  # list of (part_dir, part_roman, part_title, module_dir)
for part_dir, roman, title, modules in PARTS_ORDER:
    for mod in modules:
        ALL_CHAPTERS.append((part_dir, roman, title, mod))

CANONICAL_FOOTER = """    <footer>
        <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
        <p>Fifth Edition, 2026. Written by a team of 42 AI agents.</p>
    </footer>"""

# Stats tracking
stats = {
    "part_inline_styles_removed": 0,
    "part_part_labels_removed": 0,
    "part_footer_fixed": 0,
    "part_nav_removed": 0,
    "part_files_modified": 0,
    "chapter_inline_styles_removed": 0,
    "chapter_part_label_fixed": 0,
    "chapter_nav_added": 0,
    "chapter_nav_fixed": 0,
    "chapter_footer_fixed": 0,
    "chapter_whats_next_moved": 0,
    "chapter_files_modified": 0,
}


def remove_inline_styles(html):
    """Remove all style='...' attributes from HTML."""
    count = len(re.findall(r'\s+style="[^"]*"', html))
    count += len(re.findall(r"\s+style='[^']*'", html))
    cleaned = re.sub(r'\s+style="[^"]*"', '', html)
    cleaned = re.sub(r"\s+style='[^']*'", '', cleaned)
    return cleaned, count


def get_chapter_title_from_file(filepath):
    """Extract the chapter title from the <title> tag of an index.html file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        m = re.search(r'<title>(.*?)</title>', content)
        if m:
            title = m.group(1)
            # Decode HTML entities
            title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            return title
        return None
    except FileNotFoundError:
        return None


def get_module_number(module_dir):
    """Extract the module number from a directory name like module-22-ai-agents."""
    m = re.match(r'module-(\d+)', module_dir)
    if m:
        return int(m.group(1))
    return 0


def fix_part_index(part_dir, roman, title):
    """Fix a part index page."""
    filepath = os.path.join(BASE, part_dir, "index.html")
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    html = original
    modified = False

    # 1. Remove inline styles from ALL elements
    html_new, count = remove_inline_styles(html)
    if count > 0:
        html = html_new
        stats["part_inline_styles_removed"] += count
        modified = True

    # 2. Remove any .part-label div (parts don't link to parent parts)
    part_label_pattern = r'\s*<div class="part-label">.*?</div>\s*'
    if re.search(part_label_pattern, html, re.DOTALL):
        html = re.sub(part_label_pattern, '\n', html, flags=re.DOTALL)
        stats["part_part_labels_removed"] += 1
        modified = True

    # 3. Remove existing chapter-nav from part pages (parts should not have chapter-nav)
    nav_pattern = r'\s*<nav class="chapter-nav">.*?</nav>\s*'
    if re.search(nav_pattern, html, re.DOTALL):
        html = re.sub(nav_pattern, '\n', html, flags=re.DOTALL)
        stats["part_nav_removed"] += 1
        modified = True

    # 4. Fix footer: remove existing footer (wherever it is) and add canonical one inside .content
    # First, remove any existing footer
    footer_pattern = r'\s*<footer[^>]*>.*?</footer>\s*'
    had_footer = bool(re.search(footer_pattern, html, re.DOTALL))
    html = re.sub(footer_pattern, '\n', html, flags=re.DOTALL)

    # Now ensure footer is inside .content, right before closing </div> that closes .content
    # Find the last </div> before </body>
    # Strategy: find the content div closing and insert footer before it
    # The .content div is opened with <div class="content"> and its closing </div> should be
    # followed by </body>
    # We need to insert the footer just before the closing </div> of .content

    # Find position of </body>
    body_close = html.rfind('</body>')
    if body_close == -1:
        print(f"  WARNING: no </body> in {filepath}")
        return

    # The content closing </div> should be the last </div> before </body>
    # Find the last </div> before </body>
    before_body = html[:body_close].rstrip()

    # Check if content already has footer inside it
    # We need to insert footer before the last </div> before </body>
    if before_body.endswith('</div>'):
        insert_pos = before_body.rfind('</div>')
        # Check if footer is already there
        if '<footer>' not in html[insert_pos-200:insert_pos]:
            html = before_body[:insert_pos] + '\n' + CANONICAL_FOOTER + '\n</div>\n' + html[body_close:]
            stats["part_footer_fixed"] += 1
            modified = True
        else:
            # Footer exists but may not be canonical; rebuild
            html = before_body[:insert_pos] + '\n' + CANONICAL_FOOTER + '\n</div>\n' + html[body_close:]
            stats["part_footer_fixed"] += 1
            modified = True
    else:
        # Something unexpected, just insert before </body>
        html = before_body + '\n' + CANONICAL_FOOTER + '\n</div>\n' + html[body_close:]
        stats["part_footer_fixed"] += 1
        modified = True

    # Clean up multiple blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        stats["part_files_modified"] += 1
        print(f"  FIXED: {filepath}")
    else:
        print(f"  OK: {filepath}")


def fix_chapter_index(part_dir, part_roman, part_title, module_dir, prev_info, next_info):
    """
    Fix a chapter index page.
    prev_info / next_info: (part_dir, module_dir) or None for first/last chapter.
    """
    filepath = os.path.join(BASE, part_dir, module_dir, "index.html")
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    html = original
    modified = False

    # 1. Remove ALL inline styles
    html_new, count = remove_inline_styles(html)
    if count > 0:
        html = html_new
        stats["chapter_inline_styles_removed"] += count
        modified = True

    # 2. Ensure .part-label exists with correct link and no inline styles
    # The part-label should be inside <header class="chapter-header">
    part_label_correct = f'    <div class="part-label"><a href="../index.html">Part {part_roman}: {part_title}</a></div>'

    # Check if part-label exists
    part_label_match = re.search(r'<div class="part-label">.*?</div>', html, re.DOTALL)
    if part_label_match:
        existing = part_label_match.group(0)
        # Build the expected content (ignoring whitespace differences)
        expected_link = f'Part {part_roman}: {part_title}'
        if expected_link not in existing or 'style=' in existing:
            html = html.replace(existing, f'<div class="part-label"><a href="../index.html">Part {part_roman}: {part_title}</a></div>')
            stats["chapter_part_label_fixed"] += 1
            modified = True
    else:
        # Need to add part-label after <header class="chapter-header">
        header_match = re.search(r'(<header class="chapter-header">)\s*\n', html)
        if header_match:
            insert_pos = header_match.end()
            html = html[:insert_pos] + part_label_correct + '\n' + html[insert_pos:]
            stats["chapter_part_label_fixed"] += 1
            modified = True

    # 3. Move any .whats-next div that's OUTSIDE .content to inside .content
    # Check for whats-next outside of .content div (after </div> content close, before </body>)
    # Find the closing </div> of .content
    whats_next_outside = re.search(r'</div>\s*\n\s*(<div class="whats-next">.*?</div>)', html, re.DOTALL)
    if whats_next_outside:
        whats_next_html = whats_next_outside.group(1)
        # Remove it from current position
        html = html.replace(whats_next_outside.group(0), '</div>')
        # Insert before the closing of .content
        # Find the .content closing </div> (the one right before </body> area)
        body_close = html.rfind('</body>')
        before_body = html[:body_close].rstrip()
        last_div_close = before_body.rfind('</div>')
        # Remove inline styles from whats-next
        whats_next_html = re.sub(r'\s+style="[^"]*"', '', whats_next_html)
        html = html[:last_div_close] + '\n\n' + whats_next_html + '\n\n</div>' + html[last_div_close + len('</div>'):]
        stats["chapter_whats_next_moved"] += 1
        modified = True

    # 4. Handle chapter-nav: remove existing one (may be outside .content or have wrong links)
    #    and add correct one inside .content
    existing_nav = re.search(r'\s*<nav class="chapter-nav">.*?</nav>\s*', html, re.DOTALL)
    if existing_nav:
        html = html.replace(existing_nav.group(0), '\n')
        stats["chapter_nav_fixed"] += 1
        modified = True

    # Build the chapter-nav HTML
    nav_lines = ['    <nav class="chapter-nav">']

    # Previous chapter link
    if prev_info:
        prev_part_dir, prev_module_dir = prev_info
        prev_filepath = os.path.join(BASE, prev_part_dir, prev_module_dir, "index.html")
        prev_title = get_chapter_title_from_file(prev_filepath) or f"Chapter {get_module_number(prev_module_dir)}"
        if prev_part_dir == part_dir:
            prev_href = f"../{prev_module_dir}/index.html"
        else:
            prev_href = f"../../{prev_part_dir}/{prev_module_dir}/index.html"
        # Encode & as &amp; for HTML
        prev_title_html = prev_title.replace('&', '&amp;')
        nav_lines.append(f'        <a href="{prev_href}" class="prev">&larr; {prev_title_html}</a>')
    else:
        nav_lines.append(f'        <span></span>')

    # Part link (center)
    nav_lines.append(f'        <a href="../index.html">Part {part_roman}</a>')

    # Next chapter link
    if next_info:
        next_part_dir, next_module_dir = next_info
        next_filepath = os.path.join(BASE, next_part_dir, next_module_dir, "index.html")
        next_title = get_chapter_title_from_file(next_filepath) or f"Chapter {get_module_number(next_module_dir)}"
        if next_part_dir == part_dir:
            next_href = f"../{next_module_dir}/index.html"
        else:
            next_href = f"../../{next_part_dir}/{next_module_dir}/index.html"
        next_title_html = next_title.replace('&', '&amp;')
        nav_lines.append(f'        <a href="{next_href}" class="next">{next_title_html} &rarr;</a>')
    else:
        nav_lines.append(f'        <span></span>')

    nav_lines.append('    </nav>')
    nav_html = '\n'.join(nav_lines)

    # 5. Fix footer: remove existing footer and add canonical one inside .content
    footer_pattern = r'\s*<footer[^>]*>.*?</footer>\s*'
    html = re.sub(footer_pattern, '\n', html, flags=re.DOTALL)

    # Now we need to insert chapter-nav and footer inside .content, before its closing </div>
    # Find </body>
    body_close = html.rfind('</body>')
    if body_close == -1:
        print(f"  WARNING: no </body> in {filepath}")
        return

    before_body = html[:body_close].rstrip()

    # The last </div> before </body> should be the closing of .content
    last_div = before_body.rfind('</div>')
    if last_div == -1:
        print(f"  WARNING: no closing </div> in {filepath}")
        return

    # Insert nav and footer before the closing </div> of .content
    insert_content = '\n\n' + nav_html + '\n\n' + CANONICAL_FOOTER + '\n'
    html = before_body[:last_div] + insert_content + '\n</div>\n' + html[body_close:]

    stats["chapter_nav_added"] += 1
    stats["chapter_footer_fixed"] += 1
    modified = True

    # Clean up multiple blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        stats["chapter_files_modified"] += 1
        print(f"  FIXED: {filepath}")
    else:
        print(f"  OK: {filepath}")


def main():
    print("=" * 70)
    print("STEP 1: Fix Part Index Pages")
    print("=" * 70)

    for part_dir, roman, title, modules in PARTS_ORDER:
        print(f"\nPart {roman}: {title}")
        fix_part_index(part_dir, roman, title)

    print("\n" + "=" * 70)
    print("STEP 2: Fix Chapter Index Pages")
    print("=" * 70)

    for idx, (part_dir, part_roman, part_title, module_dir) in enumerate(ALL_CHAPTERS):
        # Determine prev/next
        prev_info = None
        next_info = None
        if idx > 0:
            prev_part_dir, _, _, prev_mod = ALL_CHAPTERS[idx - 1]
            prev_info = (prev_part_dir, prev_mod)
        if idx < len(ALL_CHAPTERS) - 1:
            next_part_dir, _, _, next_mod = ALL_CHAPTERS[idx + 1]
            next_info = (next_part_dir, next_mod)

        mod_num = get_module_number(module_dir)
        print(f"\nChapter {mod_num:02d} ({part_dir}/{module_dir})")
        fix_chapter_index(part_dir, part_roman, part_title, module_dir, prev_info, next_info)

    # Also handle any stale module dirs (like module-23-multi-agent-systems which is a duplicate)
    # Check for module dirs not in our ordering
    print("\n" + "=" * 70)
    print("STEP 3: Check for unlisted module directories")
    print("=" * 70)
    listed_modules = set()
    for part_dir, _, _, modules in PARTS_ORDER:
        for mod in modules:
            listed_modules.add(os.path.join(part_dir, mod))

    for part_dir, _, _, _ in PARTS_ORDER:
        part_path = os.path.join(BASE, part_dir)
        if os.path.isdir(part_path):
            for entry in sorted(os.listdir(part_path)):
                if entry.startswith("module-") and os.path.isdir(os.path.join(part_path, entry)):
                    key = os.path.join(part_dir, entry)
                    if key not in listed_modules:
                        print(f"  WARNING: unlisted module directory: {key}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nPart Index Pages:")
    print(f"  Files modified:        {stats['part_files_modified']}")
    print(f"  Inline styles removed: {stats['part_inline_styles_removed']}")
    print(f"  Part labels removed:   {stats['part_part_labels_removed']}")
    print(f"  Footers fixed:         {stats['part_footer_fixed']}")
    print(f"  Nav elements removed:  {stats['part_nav_removed']}")
    print(f"\nChapter Index Pages:")
    print(f"  Files modified:        {stats['chapter_files_modified']}")
    print(f"  Inline styles removed: {stats['chapter_inline_styles_removed']}")
    print(f"  Part labels fixed:     {stats['chapter_part_label_fixed']}")
    print(f"  Chapter navs added:    {stats['chapter_nav_added']}")
    print(f"  Old navs replaced:     {stats['chapter_nav_fixed']}")
    print(f"  Footers fixed:         {stats['chapter_footer_fixed']}")
    print(f"  Whats-next moved in:   {stats['chapter_whats_next_moved']}")
    print(f"\nTotal files modified:    {stats['part_files_modified'] + stats['chapter_files_modified']}")


if __name__ == "__main__":
    main()
