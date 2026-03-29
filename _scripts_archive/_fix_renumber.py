#!/usr/bin/env python3
"""
Fix the double-rename issue by mapping topic names to correct numbers.
This is a one-time fix script.
"""
import os
import re
import glob
from collections import defaultdict

ROOT = r"E:\Projects\LLMCourse"

# Correct mapping: (part_dir, topic_suffix, correct_number)
CORRECT_MAP = [
    # Part 2
    ("part-2-understanding-llms", "pretraining-scaling-laws", 6),
    ("part-2-understanding-llms", "modern-llm-landscape", 7),
    ("part-2-understanding-llms", "reasoning-test-time-compute", 8),
    ("part-2-understanding-llms", "inference-optimization", 9),
    # Part 3
    ("part-3-working-with-llms", "llm-apis", 10),
    ("part-3-working-with-llms", "prompt-engineering", 11),
    ("part-3-working-with-llms", "hybrid-ml-llm", 12),
    # Part 4
    ("part-4-training-adapting", "synthetic-data", 13),
    ("part-4-training-adapting", "fine-tuning-fundamentals", 14),
    ("part-4-training-adapting", "peft", 15),
    ("part-4-training-adapting", "distillation-merging", 16),
    ("part-4-training-adapting", "alignment-rlhf-dpo", 17),
    ("part-4-training-adapting", "interpretability", 18),
    # Part 5
    ("part-5-retrieval-conversation", "embeddings-vector-db", 19),
    ("part-5-retrieval-conversation", "rag", 20),
    ("part-5-retrieval-conversation", "conversational-ai", 21),
    # Part 6
    ("part-6-agents-applications", "ai-agents", 22),
    ("part-6-agents-applications", "multi-agent-systems", 23),
    ("part-6-agents-applications", "multimodal", 24),
    ("part-6-agents-applications", "llm-applications", 25),
    ("part-6-agents-applications", "evaluation-observability", 26),
    # Part 7
    ("part-7-production-strategy", "production-engineering", 27),
    ("part-7-production-strategy", "safety-ethics-regulation", 28),
    ("part-7-production-strategy", "strategy-product-roi", 29),
    ("part-7-production-strategy", "frontiers", 30),
]

def find_dir_by_topic(part_path, topic):
    """Find directory ending with the topic suffix."""
    for d in os.listdir(part_path):
        if d.startswith("module-") and d.endswith(f"-{topic}"):
            return os.path.join(part_path, d)
        # Also match exact topic at end
        if d.startswith("module-") and topic in d:
            # More precise: extract the topic part
            match = re.match(r'module-\d+[a-z]?-(.*)', d)
            if match and match.group(1) == topic:
                return os.path.join(part_path, d)
    return None

def get_current_num(dirname):
    """Extract the current number from a module directory name."""
    match = re.match(r'module-(\d+[a-z]?)-', os.path.basename(dirname))
    if match:
        return match.group(1)
    return None

# Phase 1: Fix directory names
print("=" * 60)
print("PHASE 1: Fix directory names")
print("=" * 60)

# First pass: collect all renames needed (to avoid conflicts, use temp names)
renames = []
for part_dir, topic, correct_num in CORRECT_MAP:
    part_path = os.path.join(ROOT, part_dir)
    current_dir = find_dir_by_topic(part_path, topic)

    if current_dir is None:
        print(f"  NOT FOUND: {topic} in {part_dir}")
        continue

    current_basename = os.path.basename(current_dir)
    correct_basename = f"module-{correct_num:02d}-{topic}"

    if current_basename == correct_basename:
        print(f"  OK: {correct_basename}")
        continue

    renames.append((current_dir, os.path.join(part_path, correct_basename), topic, correct_num))
    print(f"  FIX: {current_basename} -> {correct_basename}")

# Use temp names to avoid collisions
print("\n  Renaming via temp names...")
for old_path, new_path, topic, num in renames:
    temp_path = old_path + "__TEMP__"
    os.rename(old_path, temp_path)

for old_path, new_path, topic, num in renames:
    temp_path = old_path + "__TEMP__"
    os.rename(temp_path, new_path)

print(f"  Fixed {len(renames)} directories")

# Phase 2: Fix section file names inside each directory
print()
print("=" * 60)
print("PHASE 2: Fix section file names")
print("=" * 60)

for part_dir, topic, correct_num in CORRECT_MAP:
    part_path = os.path.join(ROOT, part_dir)
    correct_dir = os.path.join(part_path, f"module-{correct_num:02d}-{topic}")

    if not os.path.exists(correct_dir):
        continue

    correct_prefix = f"section-{correct_num}."

    for fname in sorted(os.listdir(correct_dir)):
        if not fname.startswith("section-") or not fname.endswith(".html"):
            continue

        # Check if it already has the correct prefix
        if fname.startswith(correct_prefix):
            continue

        # Extract the section sub-number (e.g., "1" from "section-14.1.html")
        match = re.match(r'section-\d+[a-z]?\.(\d+)\.html', fname)
        if match:
            sub_num = match.group(1)
            new_fname = f"section-{correct_num}.{sub_num}.html"
            old_path = os.path.join(correct_dir, fname)
            new_path = os.path.join(correct_dir, new_fname)

            print(f"  {os.path.basename(correct_dir)}/{fname} -> {new_fname}")
            os.rename(old_path, new_path)

# Phase 3: Content replacements
# The first script already did most replacements, but the double-run
# shifted some numbers by +2. We need to fix content references too.
# The safest approach: rebuild all content references from scratch.
print()
print("=" * 60)
print("PHASE 3: Fix content references")
print("=" * 60)

def protect_code_blocks(html):
    placeholders = []
    def save(m):
        placeholders.append(m.group(0))
        return f"\x00CODEBLOCK{len(placeholders) - 1}\x00"
    html = re.sub(r'<pre\b[^>]*>.*?</pre>', save, html, flags=re.DOTALL)
    html = re.sub(r'<code\b[^>]*>.*?</code>', save, html, flags=re.DOTALL)
    return html, placeholders

def restore_code_blocks(html, placeholders):
    for i, block in enumerate(placeholders):
        html = html.replace(f"\x00CODEBLOCK{i}\x00", block)
    return html

# Build a map of wrong -> correct directory references
# The double-run shifted these directories by +1 extra:
# Dirs that were at X are now at X+1 when they should be at X
# affected: those that went through two +1 shifts

# The first run correctly renamed everything. The second run then
# shifted some by +1 more. The ones that got double-shifted are
# those whose topic names matched during the second run.

# Rather than trying to figure out which content was double-shifted,
# let's do a fresh pass that builds the correct mapping based on
# topic names and directory paths.

# Build wrong -> correct content replacements
# For each module that was at wrong number, fix references
# Map: wrong_dir_name -> correct_dir_name
dir_fixes = {}
for old_path, new_path, topic, num in renames:
    old_basename = os.path.basename(old_path)
    new_basename = os.path.basename(new_path)
    dir_fixes[old_basename] = new_basename

    # Also extract old and new numbers for section/chapter fixes
    old_match = re.match(r'module-(\d+)-', old_basename)
    if old_match:
        old_num = int(old_match.group(1))
        dir_fixes[f"section-{old_num}."] = f"section-{num}."
        dir_fixes[f'"lesson-num">{old_num}.'] = f'"lesson-num">{num}.'
        dir_fixes[f'"sec-num">{old_num}.'] = f'"sec-num">{num}.'
        dir_fixes[f'"toc-num">{old_num:02d}</span>'] = f'"toc-num">{num:02d}</span>'
        dir_fixes[f'Chapter {old_num:02d}:'] = f'Chapter {num:02d}:'
        dir_fixes[f'Chapter {old_num:02d}<'] = f'Chapter {num:02d}<'
        dir_fixes[f'>Chapter {old_num:02d}</a>'] = f'>Chapter {num:02d}</a>'
        dir_fixes[f'"mod-num">Chapter {old_num:02d}</span>'] = f'"mod-num">Chapter {num:02d}</span>'
        dir_fixes[f'id="ch{old_num}"'] = f'id="ch{num}"'
        dir_fixes[f'href="#ch{old_num}"'] = f'href="#ch{num}"'
        dir_fixes[f'Section {old_num}.'] = f'Section {num}.'
        dir_fixes[f'Chapter {old_num}'] = f'Chapter {num}'
        dir_fixes[f'Ch {old_num}'] = f'Ch {num}'

if dir_fixes:
    # Sort by length descending to avoid partial replacements
    sorted_fixes = sorted(dir_fixes.items(), key=lambda x: len(x[0]), reverse=True)

    html_files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
    md_files = glob.glob(os.path.join(ROOT, '*.md'))
    all_files = sorted(set(html_files + md_files))

    files_fixed = 0
    for filepath in all_files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                original = f.read()
        except:
            continue

        is_html = filepath.endswith('.html')
        if is_html:
            text, placeholders = protect_code_blocks(original)
        else:
            text = original
            placeholders = []

        changed = False
        for old_str, new_str in sorted_fixes:
            if old_str in text:
                text = text.replace(old_str, new_str)
                changed = True

        if is_html:
            text = restore_code_blocks(text, placeholders)

        if text != original:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            files_fixed += 1

    print(f"  Fixed content in {files_fixed} files")
else:
    print("  No content fixes needed (directories were already correct)")

# Phase 4: Validate
print()
print("=" * 60)
print("PHASE 4: Validate")
print("=" * 60)

issues = []
for part_dir, topic, correct_num in CORRECT_MAP:
    part_path = os.path.join(ROOT, part_dir)
    expected_dir = os.path.join(part_path, f"module-{correct_num:02d}-{topic}")

    if not os.path.exists(expected_dir):
        issues.append(f"  MISSING DIR: {expected_dir}")
        continue

    # Check section files
    expected_prefix = f"section-{correct_num}."
    section_files = [f for f in os.listdir(expected_dir)
                     if f.startswith(expected_prefix) and f.endswith('.html')]

    if not section_files:
        issues.append(f"  NO SECTIONS: module-{correct_num:02d}-{topic}")

if issues:
    print("  ISSUES:")
    for issue in issues:
        print(issue)
else:
    print("  All directories and section files are correctly numbered!")

# Print final state
print()
print("=" * 60)
print("FINAL STATE")
print("=" * 60)
for part_dir in ["part-1-foundations", "part-2-understanding-llms", "part-3-working-with-llms",
                 "part-4-training-adapting", "part-5-retrieval-conversation",
                 "part-6-agents-applications", "part-7-production-strategy"]:
    part_path = os.path.join(ROOT, part_dir)
    print(f"\n  {part_dir}:")
    for d in sorted(os.listdir(part_path)):
        if d.startswith("module-"):
            print(f"    {d}")
