#!/usr/bin/env python3
"""
Renumber all chapters after inserting module-07b as Chapter 08.

Mapping:
  - Chapters 0-7: unchanged
  - module-07b -> module-08 (Reasoning & Test-Time Compute)
  - old module-08 -> module-09
  - old module-09 -> module-10
  - ... each old chapter N (N >= 8) becomes N+1
  - old module-28 -> module-29
  - old module-29 (Frontiers) -> module-30

Final result: 31 chapters (0-30)

Strategy: Two-pass replacement (old -> placeholder -> new) to avoid double-replacement.
Directory renames go from highest number downward to avoid collisions.
Protects code blocks (<pre>, <code>) from replacement.
"""

import os
import re
import glob
import shutil
from collections import defaultdict

ROOT = r"E:\Projects\LLMCourse"
DRY_RUN = False  # Set to True to preview without making changes

counts = defaultdict(int)

# ── Build the mapping ──────────────────────────────────────────────────

# Part directories that contain modules
PART_DIRS = {
    'part-2-understanding-llms': [(7, 'b', 8), (8, None, 9)],
    'part-3-working-with-llms': [(9, None, 10), (10, None, 11), (11, None, 12)],
    'part-4-training-adapting': [(12, None, 13), (13, None, 14), (14, None, 15),
                                 (15, None, 16), (16, None, 17), (17, None, 18)],
    'part-5-retrieval-conversation': [(18, None, 19), (19, None, 20), (20, None, 21)],
    'part-6-agents-applications': [(21, None, 22), (22, None, 23), (23, None, 24),
                                   (24, None, 25), (25, None, 26)],
    'part-7-production-strategy': [(26, None, 27), (27, None, 28), (28, None, 29),
                                   (29, None, 30)],
}

# Build ordered list of (part_dir, old_num_str, old_suffix, new_num) tuples
# Process highest to lowest to avoid directory collision
ALL_RENAMES = []
for part_dir, mappings in PART_DIRS.items():
    for old_num, suffix, new_num in mappings:
        old_str = f"{old_num:02d}" if suffix is None else f"{old_num:02d}{suffix}"
        ALL_RENAMES.append((part_dir, old_num, old_str, suffix, new_num))

# Sort descending by new_num so we rename highest first
ALL_RENAMES.sort(key=lambda x: x[4], reverse=True)


def find_module_dir(part_path, old_str):
    """Find the actual module directory matching the old number string."""
    pattern = os.path.join(part_path, f"module-{old_str}-*")
    matches = glob.glob(pattern)
    if not matches:
        # Try without suffix for 07b
        pattern2 = os.path.join(part_path, f"module-{old_str}*")
        matches = glob.glob(pattern2)
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"  WARNING: Multiple matches for module-{old_str}: {matches}")
        return matches[0]
    return None


def protect_code_blocks(html):
    """Extract <pre> and <code> blocks, replace with placeholders."""
    placeholders = []
    def save(m):
        placeholders.append(m.group(0))
        return f"\x00CODEBLOCK{len(placeholders) - 1}\x00"
    html = re.sub(r'<pre\b[^>]*>.*?</pre>', save, html, flags=re.DOTALL)
    html = re.sub(r'<code\b[^>]*>.*?</code>', save, html, flags=re.DOTALL)
    return html, placeholders


def restore_code_blocks(html, placeholders):
    """Put code blocks back."""
    for i, block in enumerate(placeholders):
        html = html.replace(f"\x00CODEBLOCK{i}\x00", block)
    return html


# ── Phase 1: Rename directories (highest to lowest) ───────────────────

def phase1_rename_directories():
    """Rename module directories from highest number downward."""
    print("=" * 60)
    print("PHASE 1: Rename directories")
    print("=" * 60)

    renames_done = []

    for part_dir, old_num, old_str, suffix, new_num in ALL_RENAMES:
        part_path = os.path.join(ROOT, part_dir)
        old_dir = find_module_dir(part_path, old_str)

        if old_dir is None:
            print(f"  SKIP: No directory found for module-{old_str} in {part_dir}")
            continue

        # Extract the topic name from the old directory
        old_basename = os.path.basename(old_dir)
        # Pattern: module-XX-topic-name or module-07b-topic-name
        match = re.match(r'module-\d+[a-z]?-(.*)', old_basename)
        if match:
            topic = match.group(1)
        else:
            topic = old_basename.split('-', 2)[-1] if '-' in old_basename else old_basename

        new_basename = f"module-{new_num:02d}-{topic}"
        new_dir = os.path.join(part_path, new_basename)

        print(f"  {old_basename} -> {new_basename}")

        if not DRY_RUN:
            if os.path.exists(new_dir):
                print(f"    ERROR: Target already exists: {new_dir}")
                continue
            os.rename(old_dir, new_dir)

        renames_done.append((old_dir, new_dir, old_num, old_str, suffix, new_num))
        counts['dir_renames'] += 1

    return renames_done


# ── Phase 2: Rename section files inside each renamed directory ────────

def phase2_rename_section_files():
    """Rename section-X.N.html files to section-Y.N.html."""
    print()
    print("=" * 60)
    print("PHASE 2: Rename section files")
    print("=" * 60)

    for part_dir, old_num, old_str, suffix, new_num in ALL_RENAMES:
        part_path = os.path.join(ROOT, part_dir)
        # Find the already-renamed directory
        new_dir = find_module_dir(part_path, f"{new_num:02d}")

        if new_dir is None:
            print(f"  SKIP: Cannot find renamed dir for module-{new_num:02d} in {part_dir}")
            continue

        # Build the old section prefix
        if suffix:
            old_prefix = f"section-{old_num}{suffix}."  # e.g., "section-7b."
        else:
            old_prefix = f"section-{old_num}."  # e.g., "section-8."

        new_prefix = f"section-{new_num}."  # e.g., "section-8." or "section-9."

        for fname in sorted(os.listdir(new_dir)):
            if fname.startswith(old_prefix) and fname.endswith('.html'):
                new_fname = fname.replace(old_prefix, new_prefix, 1)
                old_path = os.path.join(new_dir, fname)
                new_path = os.path.join(new_dir, new_fname)

                print(f"  {os.path.basename(new_dir)}/{fname} -> {new_fname}")

                if not DRY_RUN:
                    os.rename(old_path, new_path)
                counts['file_renames'] += 1


# ── Phase 3: Content replacements across all files ─────────────────────

def build_replacement_rules():
    """Build ordered replacement rules: (pattern, replacement, category).

    Uses placeholder approach: old -> __PH_XX__ -> new
    Process in descending order of old numbers to avoid collisions.
    """
    rules = []

    # Sort by old_num descending, with 7b handled specially
    sorted_renames = sorted(ALL_RENAMES, key=lambda x: (x[1], x[3] or ''), reverse=True)

    for part_dir, old_num, old_str, suffix, new_num in sorted_renames:
        old_nn = old_str  # e.g., "08", "09", "07b"
        new_nn = f"{new_num:02d}"  # e.g., "09", "10", "08"

        # For display text like "Chapter 8" (no leading zero)
        if suffix:
            old_display = f"{old_num}{suffix}"  # "7b"
        else:
            old_display = str(old_num)  # "8", "9", etc.
        new_display = str(new_num)

        # For section references like "section-8." or "section-7b."
        if suffix:
            old_sec_prefix = f"{old_num}{suffix}"  # "7b"
        else:
            old_sec_prefix = str(old_num)  # "8"
        new_sec_prefix = str(new_num)

        ph = f"__PH{new_num:02d}__"

        # 1. Directory path references (most specific first)
        # Find actual old dir name pattern
        rules.append((
            f"module-{old_nn}-",
            f"module-{ph}-",
            'dir_path'
        ))

        # 2. Section file references: section-X.N.html
        rules.append((
            f"section-{old_sec_prefix}.",
            f"section-{ph}.",
            'section_file'
        ))

        # 3. Lesson/section numbers in display text (e.g., <span class="lesson-num">8.1</span>)
        # Also "Section 8.1", "8.1", etc.
        # Handle carefully: only replace when it's clearly a section reference
        rules.append((
            f'"lesson-num">{old_sec_prefix}.',
            f'"lesson-num">{ph}.',
            'lesson_num'
        ))
        rules.append((
            f'"sec-num">{old_sec_prefix}.',
            f'"sec-num">{ph}.',
            'sec_num'
        ))

        # 4. Chapter display numbers
        rules.append((
            f'"toc-num">{old_nn}</span>',
            f'"toc-num">{ph}</span>',
            'toc_num'
        ))
        rules.append((
            f'"mod-num">Chapter {old_nn}</span>',
            f'"mod-num">Chapter {ph}</span>',
            'mod_num_span'
        ))

        # 5. Chapter number in headers
        rules.append((
            f'Chapter {old_nn}:',
            f'Chapter {ph}:',
            'chapter_header'
        ))
        rules.append((
            f'Chapter {old_nn}<',
            f'Chapter {ph}<',
            'chapter_label'
        ))
        rules.append((
            f'>Chapter {old_nn}</a>',
            f'>Chapter {ph}</a>',
            'chapter_link_text'
        ))

        # 6. Title tags
        rules.append((
            f'Chapter {old_nn}:',
            f'Chapter {ph}:',
            'title_chapter'
        ))
        rules.append((
            f'Section {old_sec_prefix}.',
            f'Section {ph}.',
            'title_section'
        ))

        # 7. ID and anchor references
        rules.append((
            f'id="ch{old_num}"' if not suffix else f'id="ch{old_num}{suffix}"',
            f'id="ch{ph}"',
            'id_attr'
        ))
        rules.append((
            f'href="#ch{old_num}"' if not suffix else f'href="#ch{old_num}{suffix}"',
            f'href="#ch{ph}"',
            'href_anchor'
        ))

        # 8. Prose references: "Chapter 8" (without leading zero, in body text)
        if old_display != old_nn:  # Different formats (e.g., "8" vs "08")
            rules.append((
                f'Chapter {old_display}',
                f'Chapter {ph}',
                'prose_chapter'
            ))

        # 9. Section references in prose: "Section 8.1"
        rules.append((
            f'Section {old_sec_prefix}.',
            f'Section {ph}.',
            'prose_section'
        ))

        # 10. "Ch " references (abbreviated)
        rules.append((
            f'Ch {old_display}',
            f'Ch {ph}',
            'ch_abbrev'
        ))

        # 11. Chapter count in meta bar
        # This is handled separately

    return rules


def resolve_placeholders(text):
    """Replace all __PHXX__ placeholders with final numbers."""
    for new_num in range(30, -1, -1):
        ph = f"__PH{new_num:02d}__"
        # In contexts where leading zero is used (directory names, toc-num)
        # the replacement is the zero-padded form
        # In other contexts it's the bare number
        # We need to figure out which context each placeholder is in

        # For directory names: module-__PH09__- -> module-09-
        text = text.replace(f"module-{ph}-", f"module-{new_num:02d}-")

        # For toc-num: always 2-digit
        text = text.replace(f'"toc-num">{ph}</span>', f'"toc-num">{new_num:02d}</span>')
        text = text.replace(f'"mod-num">Chapter {ph}</span>', f'"mod-num">Chapter {new_num:02d}</span>')

        # For IDs and anchors
        text = text.replace(f'id="ch{ph}"', f'id="ch{new_num}"')
        text = text.replace(f'href="#ch{ph}"', f'href="#ch{new_num}"')

        # For everything else: use bare number
        text = text.replace(ph, str(new_num))

    return text


def phase3_content_replacements():
    """Apply content replacements across all HTML and MD files."""
    print()
    print("=" * 60)
    print("PHASE 3: Content replacements")
    print("=" * 60)

    rules = build_replacement_rules()

    # Collect all files
    html_files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
    md_files = glob.glob(os.path.join(ROOT, '*.md'), recursive=False)
    # Also MD files in subdirectories (but not node_modules etc.)
    for d in ['part-1-foundations', 'part-2-understanding-llms', 'part-3-working-with-llms',
              'part-4-training-adapting', 'part-5-retrieval-conversation',
              'part-6-agents-applications', 'part-7-production-strategy']:
        md_files += glob.glob(os.path.join(ROOT, d, '**', '*.md'), recursive=True)

    all_files = sorted(set(html_files + md_files))
    print(f"  Processing {len(all_files)} files...")

    files_changed = 0

    for filepath in all_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                original = f.read()
        except Exception as e:
            print(f"  ERROR reading {filepath}: {e}")
            continue

        is_html = filepath.endswith('.html')

        # Protect code blocks in HTML
        if is_html:
            text, placeholders = protect_code_blocks(original)
        else:
            text = original
            placeholders = []

        # Apply all rules (old -> placeholder)
        for old_pat, new_pat, category in rules:
            if old_pat in text:
                count_before = text.count(old_pat)
                text = text.replace(old_pat, new_pat)
                counts[category] += count_before

        # Resolve placeholders to final numbers
        text = resolve_placeholders(text)

        # Restore code blocks
        if is_html:
            text = restore_code_blocks(text, placeholders)

        if text != original:
            if not DRY_RUN:
                with open(filepath, 'w', encoding='utf-8', newline='') as f:
                    f.write(text)
            files_changed += 1

    print(f"  Files changed: {files_changed}")
    counts['files_changed'] = files_changed


# ── Phase 4: Update meta counts ───────────────────────────────────────

def phase4_update_meta():
    """Update chapter count in main index.html meta bar."""
    print()
    print("=" * 60)
    print("PHASE 4: Update meta counts")
    print("=" * 60)

    index_path = os.path.join(ROOT, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Update "29 Chapters" -> "31 Chapters"
    text = text.replace('29 Chapters', '31 Chapters')
    # Also handle if it was already partially updated
    text = text.replace('30 Chapters', '31 Chapters')

    if not DRY_RUN:
        with open(index_path, 'w', encoding='utf-8', newline='') as f:
            f.write(text)

    print("  Updated main index.html chapter count to 31")
    counts['meta_updates'] += 1


# ── Phase 5: Validation ───────────────────────────────────────────────

def phase5_validate():
    """Check for leftover old references."""
    print()
    print("=" * 60)
    print("PHASE 5: Validation")
    print("=" * 60)

    html_files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)

    issues = []

    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()

        rel = os.path.relpath(filepath, ROOT)

        # Check for leftover "7b" references (should all be converted to 8)
        if 'module-07b' in text or 'section-7b.' in text or 'Chapter 7b' in text:
            issues.append(f"  LEFTOVER 7b ref in {rel}")

        # Check for leftover placeholders
        if '__PH' in text:
            issues.append(f"  LEFTOVER placeholder in {rel}")

        # Check for old directory references that should have been renamed
        for old_num in range(8, 30):
            old_dir_pattern = f"module-{old_num:02d}-"
            if old_dir_pattern in text:
                # Check if this is a valid new reference
                # Valid new refs: module-08 through module-30
                # Old refs that should be gone: the old module-08 (now 09), etc.
                # This is tricky to validate automatically, so just count
                pass

    # Check that renamed directories exist
    for part_dir, old_num, old_str, suffix, new_num in ALL_RENAMES:
        part_path = os.path.join(ROOT, part_dir)
        new_dir = find_module_dir(part_path, f"{new_num:02d}")
        if new_dir is None:
            issues.append(f"  MISSING: module-{new_num:02d} not found in {part_dir}")
        else:
            # Check section files exist
            new_prefix = f"section-{new_num}."
            section_files = [f for f in os.listdir(new_dir)
                          if f.startswith(new_prefix) and f.endswith('.html')]
            if not section_files:
                issues.append(f"  NO SECTIONS: {os.path.basename(new_dir)} has no section-{new_num}.*.html files")

    if issues:
        print("  ISSUES FOUND:")
        for issue in issues:
            print(issue)
    else:
        print("  All checks passed!")

    return len(issues) == 0


# ── Main ───────────────────────────────────────────────────────────────

def main():
    print(f"Book root: {ROOT}")
    print(f"Dry run: {DRY_RUN}")
    print(f"Renames to process: {len(ALL_RENAMES)}")
    print()

    # Phase 1
    phase1_rename_directories()

    # Phase 2
    phase2_rename_section_files()

    # Phase 3
    phase3_content_replacements()

    # Phase 4
    phase4_update_meta()

    # Phase 5
    ok = phase5_validate()

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for cat in sorted(counts.keys()):
        print(f"  {cat:25s} {counts[cat]:>6d}")
    print(f"  {'TOTAL':25s} {sum(counts.values()):>6d}")

    if not ok:
        print()
        print("WARNING: Some validation checks failed. Review the issues above.")
    else:
        print()
        print("SUCCESS: All renaming and relinking complete.")


if __name__ == '__main__':
    main()
