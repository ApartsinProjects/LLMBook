"""
Fix all cross-reference issues in LLMCourse HTML files:
1. Wrong section titles (32.4 -> 28.4, 32.5 -> 28.5)
2. Broken href paths pointing to old/nonexistent directories
3. Display text showing wrong section/chapter numbers vs href target
"""

import os
import re
import glob

ROOT = r"E:\Projects\LLMCourse"

# Mutable counter for use in nested callbacks
counter = [0]

# ── Step 0: Build directory map ──────────────────────────────────────────────
actual_parts = {}
actual_modules = {}

for entry in sorted(os.listdir(ROOT)):
    full = os.path.join(ROOT, entry)
    if os.path.isdir(full) and entry.startswith("part-"):
        m = re.match(r'(part-\d+)', entry)
        if m:
            actual_parts[m.group(1)] = entry
        for mod_entry in sorted(os.listdir(full)):
            mod_full = os.path.join(full, mod_entry)
            if os.path.isdir(mod_full) and mod_entry.startswith("module-"):
                mm = re.match(r'(module-\d+)', mod_entry)
                if mm:
                    actual_modules[mm.group(1)] = (entry, mod_entry)

print("=== Actual directory structure ===")
for pkey in sorted(actual_parts):
    print(f"  {pkey} -> {actual_parts[pkey]}")
for mkey in sorted(actual_modules, key=lambda x: int(x.split('-')[1])):
    part_name, mod_name = actual_modules[mkey]
    print(f"  {mkey} -> {part_name}/{mod_name}")
print()

all_html = glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)

# ── Step 1: Fix wrong titles (32.4->28.4, 32.5->28.5) ───────────────────────
print("=== Issue 1: Fix wrong section titles ===")
issue1_count = 0

for fpath in all_html:
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    new_content = content
    new_content = new_content.replace("Section 32.4", "Section 28.4")
    new_content = new_content.replace("Section 32.5", "Section 28.5")
    new_content = re.sub(r'\b32\.4:', '28.4:', new_content)
    new_content = re.sub(r'\b32\.5:', '28.5:', new_content)

    if new_content != content:
        issue1_count += 1
        print(f"  Fixed: {os.path.relpath(fpath, ROOT)}")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

print(f"  Total files: {issue1_count}\n")

# ── Step 2: Fix broken href paths ────────────────────────────────────────────
print("=== Issue 2: Fix broken href paths ===")

href_pattern = re.compile(r'href="(\.\./[^"#]*(?:#[^"]*)?)"')
issue2_count = 0
issue2_replacements = 0

for fpath in all_html:
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    fdir = os.path.dirname(fpath)
    new_content = content
    changed = False

    for match in href_pattern.finditer(content):
        href_val = match.group(1)
        path_part = href_val.split("#")[0]
        anchor = ""
        if "#" in href_val:
            anchor = "#" + href_val.split("#", 1)[1]

        resolved = os.path.normpath(os.path.join(fdir, path_part))

        if not os.path.exists(resolved):
            parts_of_href = path_part.replace("\\", "/").split("/")
            new_parts = []
            needs_fix = False

            for segment in parts_of_href:
                if segment == "..":
                    new_parts.append(segment)
                    continue

                part_match = re.match(r'(part-\d+)', segment)
                if part_match and part_match.group(1) in actual_parts:
                    correct_segment = actual_parts[part_match.group(1)]
                    if segment != correct_segment:
                        needs_fix = True
                    new_parts.append(correct_segment)
                    continue

                mod_match = re.match(r'(module-\d+)', segment)
                if mod_match and mod_match.group(1) in actual_modules:
                    _, correct_mod = actual_modules[mod_match.group(1)]
                    if segment != correct_mod:
                        needs_fix = True
                    new_parts.append(correct_mod)
                    continue

                new_parts.append(segment)

            if needs_fix:
                new_path = "/".join(new_parts) + anchor
                old_href = f'href="{href_val}"'
                new_href = f'href="{new_path}"'
                if old_href in new_content:
                    new_content = new_content.replace(old_href, new_href)
                    changed = True
                    issue2_replacements += 1

    if changed:
        issue2_count += 1
        print(f"  Fixed: {os.path.relpath(fpath, ROOT)}")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)

print(f"  Total files: {issue2_count}, replacements: {issue2_replacements}\n")

# ── Step 3: Fix display text mismatches ──────────────────────────────────────
print("=== Issue 3: Fix cross-ref display text mismatches ===")

section_link_re = re.compile(
    r'(<a\s[^>]*href="[^"]*section-(\d+)\.(\d+)\.html[^"]*"[^>]*>)(.*?)(</a>)',
    re.DOTALL
)
section_text_re = re.compile(r'(Section\s+)(\d+)\.(\d+)')

chapter_link_re = re.compile(
    r'(<a\s[^>]*href="[^"]*module-(\d+)-[^"]*"[^>]*>)(.*?)(</a>)',
    re.DOTALL
)
chapter_text_re = re.compile(r'(Chapter\s+)(\d+)')

issue3_count = 0
issue3_replacements = 0

for fpath in all_html:
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    file_fixes = 0

    # Pass 1: Fix section links
    # We'll do manual finditer + rebuild to avoid nested closure issues
    result_parts = []
    last_end = 0

    for m in section_link_re.finditer(content):
        result_parts.append(content[last_end:m.start()])
        prefix = m.group(1)
        href_major = m.group(2)
        href_minor = m.group(3)
        display = m.group(4)
        suffix = m.group(5)

        # Fix all "Section X.Y" in the display text
        new_display = display
        for sm in section_text_re.finditer(display):
            if sm.group(2) != href_major or sm.group(3) != href_minor:
                old_text = sm.group(0)
                new_text = f"{sm.group(1)}{href_major}.{href_minor}"
                new_display = new_display.replace(old_text, new_text, 1)
                file_fixes += 1

        result_parts.append(prefix + new_display + suffix)
        last_end = m.end()

    result_parts.append(content[last_end:])
    content = "".join(result_parts)

    # Pass 2: Fix chapter links
    result_parts = []
    last_end = 0

    for m in chapter_link_re.finditer(content):
        result_parts.append(content[last_end:m.start()])
        prefix = m.group(1)
        href_mod_num = m.group(2)
        display = m.group(3)
        suffix = m.group(4)

        new_display = display

        # Fix "Chapter X"
        for cm in chapter_text_re.finditer(display):
            if cm.group(2) != href_mod_num:
                old_text = cm.group(0)
                new_text = f"{cm.group(1)}{href_mod_num}"
                new_display = new_display.replace(old_text, new_text, 1)
                file_fixes += 1

        # Fix "Section X.Y" where X doesn't match module number
        for sm in section_text_re.finditer(new_display):
            if sm.group(2) != href_mod_num:
                old_text = sm.group(0)
                new_text = f"{sm.group(1)}{href_mod_num}.{sm.group(3)}"
                new_display = new_display.replace(old_text, new_text, 1)
                file_fixes += 1

        result_parts.append(prefix + new_display + suffix)
        last_end = m.end()

    result_parts.append(content[last_end:])
    content = "".join(result_parts)

    if file_fixes > 0:
        issue3_count += 1
        issue3_replacements += file_fixes
        print(f"  Fixed {file_fixes} in: {os.path.relpath(fpath, ROOT)}")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

print(f"  Total files: {issue3_count}, replacements: {issue3_replacements}\n")

# ── Summary ──────────────────────────────────────────────────────────────────
print("=== SUMMARY ===")
print(f"Issue 1 (title fixes): {issue1_count} files")
print(f"Issue 2 (broken hrefs): {issue2_count} files, {issue2_replacements} replacements")
print(f"Issue 3 (display text): {issue3_count} files, {issue3_replacements} replacements")
total = issue1_count + issue2_replacements + issue3_replacements
print(f"Total fixes applied: {total}")
