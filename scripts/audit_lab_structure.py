"""Audit lab visual style consistency across the entire book.

Standard pattern:
  <h3 class="lab-title">Lab: Title Here</h3>
  <div class="lab">
    ... lab content ...
  </div>

Reports:
  1. Files using the correct pattern
  2. Files using non-standard patterns
  3. Internal structure issues inside lab divs
"""

import re
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Collect all section HTML files
patterns = [
    os.path.join(ROOT, "part-*", "module-*", "section-*.html"),
    os.path.join(ROOT, "appendices", "*", "section-*.html"),
]

files = []
for p in patterns:
    files.extend(sorted(glob.glob(p)))

print(f"Scanning {len(files)} section HTML files...\n")

# Track results
correct_files = []  # (file, line, title_text)
issues = []  # (file, line, description)
all_lab_files = set()

for fpath in files:
    rel = os.path.relpath(fpath, ROOT).replace("\\", "/")
    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    content = "".join(lines)

    # --- Check 1: Find all lab-related patterns ---

    # Pattern A: correct <h3 class="lab-title">
    for i, line in enumerate(lines, 1):
        if 'class="lab-title"' in line or "class='lab-title'" in line:
            all_lab_files.add(rel)
            # Check tag type
            tag_match = re.search(r'<(h\d|p|div|span)\s[^>]*class="lab-title"', line) or \
                        re.search(r'<(h\d|p|div|span)\s[^>]*class=\'lab-title\'', line)
            if tag_match:
                tag = tag_match.group(1)
                if tag != "h3":
                    issues.append((rel, i, f"lab-title uses <{tag}> instead of <h3>: {line.strip()[:120]}"))
            # Check if it contains "Lab:" text
            if "Lab:" not in line and "Lab " not in line:
                issues.append((rel, i, f"lab-title heading may be missing 'Lab:' prefix: {line.strip()[:120]}"))

    # Pattern B: <div class="lab"> (correct wrapper)
    for i, line in enumerate(lines, 1):
        if re.search(r'<div\s+class="lab"', line) or re.search(r"<div\s+class='lab'", line):
            all_lab_files.add(rel)

    # Pattern C: <section class="lab"> (non-standard)
    for i, line in enumerate(lines, 1):
        if re.search(r'<section\s+class="lab"', line) or re.search(r"<section\s+class='lab'", line):
            all_lab_files.add(rel)
            issues.append((rel, i, f"Uses <section class=\"lab\"> instead of <div class=\"lab\">: {line.strip()[:120]}"))

    # Pattern D: <div class="callout lab"> or <div class="lab callout"> or similar compound classes
    for i, line in enumerate(lines, 1):
        m = re.search(r'<div\s+class="([^"]*lab[^"]*)"', line)
        if m:
            cls = m.group(1)
            if cls != "lab" and "lab" in cls.split():
                all_lab_files.add(rel)
                issues.append((rel, i, f"Lab div has compound class \"{cls}\" instead of just \"lab\": {line.strip()[:120]}"))

    # Pattern E: <h2 ...>Lab or <h2 class="lab-title"> (wrong heading level)
    for i, line in enumerate(lines, 1):
        if re.search(r'<h2[^>]*>.*\bLab\b', line, re.IGNORECASE):
            # Check if it's a lab heading
            if 'class="lab-title"' not in line:
                all_lab_files.add(rel)
                issues.append((rel, i, f"<h2> used for lab heading without lab-title class: {line.strip()[:120]}"))

    # Pattern F: Any heading with "Lab:" text but missing lab-title class
    for i, line in enumerate(lines, 1):
        m = re.search(r'<(h[1-6])[^>]*>(.*?Lab\s*:.*?)</\1>', line, re.IGNORECASE)
        if m:
            tag = m.group(1)
            if 'lab-title' not in line:
                all_lab_files.add(rel)
                issues.append((rel, i, f"Heading <{tag}> contains 'Lab:' but missing class=\"lab-title\": {line.strip()[:120]}"))

    # Pattern G: Headings with "Lab:" that span multiple attributes
    for i, line in enumerate(lines, 1):
        if re.search(r'<h[1-6]', line) and re.search(r'>\s*Lab\s*:', line):
            if 'lab-title' not in line:
                all_lab_files.add(rel)
                # Avoid duplicate with Pattern F
                already = any(iss[0] == rel and iss[1] == i and "missing class=\"lab-title\"" in iss[2] for iss in issues)
                if not already:
                    issues.append((rel, i, f"Heading contains 'Lab:' but missing class=\"lab-title\": {line.strip()[:120]}"))

    # Now verify correct pairing: h3.lab-title should be followed by div.lab
    for i, line in enumerate(lines, 1):
        if re.search(r'<h3\s+class="lab-title"', line):
            # Look ahead for the next significant tag (skip blank lines)
            found_div_lab = False
            for j in range(i, min(i + 10, len(lines))):
                next_line = lines[j]
                if re.search(r'<div\s+class="lab"', next_line):
                    found_div_lab = True
                    break
            if found_div_lab:
                title_text = re.search(r'<h3[^>]*>(.*?)</h3>', line)
                title = title_text.group(1).strip() if title_text else line.strip()[:80]
                correct_files.append((rel, i, title))
            else:
                issues.append((rel, i, f"<h3 class=\"lab-title\"> not followed by <div class=\"lab\"> within 10 lines: {line.strip()[:120]}"))

    # Check for div.lab without a preceding h3.lab-title
    for i, line in enumerate(lines, 1):
        if re.search(r'<div\s+class="lab"', line):
            # Look back for h3.lab-title
            found_title = False
            for j in range(max(0, i - 11), i - 1):
                if re.search(r'<h3\s+class="lab-title"', lines[j]):
                    found_title = True
                    break
            if not found_title:
                issues.append((rel, i, f"<div class=\"lab\"> without preceding <h3 class=\"lab-title\">: {line.strip()[:120]}"))

    # --- Check 3: Internal structure of lab divs ---
    # Find content between <div class="lab"> and its closing </div>
    in_lab = False
    lab_depth = 0
    lab_start = 0
    for i, line in enumerate(lines, 1):
        if re.search(r'<div\s+class="lab"', line):
            in_lab = True
            lab_depth = 1
            lab_start = i
            continue
        if in_lab:
            # Track div nesting
            opens = len(re.findall(r'<div[\s>]', line))
            closes = len(re.findall(r'</div>', line))
            lab_depth += opens - closes
            if lab_depth <= 0:
                in_lab = False
                continue

            # Check for h1 or h2 inside lab (should use h4 or lower)
            if re.search(r'<h[12][^>]*>', line):
                tag_m = re.search(r'<(h[12])[^>]*>', line)
                issues.append((rel, i, f"Inside lab div: unexpected high-level <{tag_m.group(1)}> heading: {line.strip()[:120]}"))

# --- Report ---
print("=" * 80)
print("CORRECT LAB PATTERNS (h3.lab-title + div.lab)")
print("=" * 80)
if correct_files:
    for fpath, line, title in correct_files:
        print(f"  {fpath}:{line}  ->  {title}")
else:
    print("  (none found)")

print(f"\n  Total correct: {len(correct_files)}")

print("\n" + "=" * 80)
print("NON-STANDARD LAB PATTERNS (issues)")
print("=" * 80)
if issues:
    # Deduplicate
    seen = set()
    unique_issues = []
    for item in issues:
        key = (item[0], item[1], item[2][:80])
        if key not in seen:
            seen.add(key)
            unique_issues.append(item)
    for fpath, line, desc in unique_issues:
        print(f"  {fpath}:{line}")
        print(f"    {desc}")
        print()
else:
    print("  (none found)")

print(f"  Total issues: {len(issues)}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"  Files scanned: {len(files)}")
print(f"  Files with any lab content: {len(all_lab_files)}")
print(f"  Correct lab patterns: {len(correct_files)}")
print(f"  Issues found: {len(issues)}")

# List files with labs but no correct pattern
files_with_correct = set(f for f, _, _ in correct_files)
files_with_issues_only = all_lab_files - files_with_correct
if files_with_issues_only:
    print(f"\n  Files with lab content but NO correct pattern:")
    for f in sorted(files_with_issues_only):
        print(f"    {f}")
