#!/usr/bin/env python3
"""Sweep all HTML files to find and fix callout class issues.

Phase 1: Fix non-standard class names and class/title mismatches
Phase 2: Add missing callout-title divs where the title is in <strong> or <h4>
"""

import re
import os
import glob

ROOT = r"E:\Projects\LLMCourse"

VALID_CLASSES = {
    "big-picture", "key-insight", "note", "warning", "practical-example",
    "fun-note", "research-frontier", "algorithm", "tip", "exercise",
    "pathway", "prerequisites", "objectives",
}

CLASS_NAME_MAP = {
    "insight": "key-insight",
    "key-idea": "key-insight",
    "important": "key-insight",
    "example": "practical-example",
    "practice": "practical-example",
    "caution": "warning",
    "danger": "warning",
    "info": "note",
    "information": "note",
    "fun-fact": "fun-note",
    "fun": "fun-note",
    "frontier": "research-frontier",
    "research": "research-frontier",
    "best-practice": "tip",
    "pro-tip": "tip",
    "hint": "tip",
}

TITLE_TO_CLASS = [
    (r"^The Big Picture", "big-picture"),
    (r"^Big Picture", "big-picture"),
    (r"^Key Insight", "key-insight"),
    (r"^Aha Moment", "key-insight"),
    (r"^Paper Spotlight", "key-insight"),
    (r"^Warning", "warning"),
    (r"^Caution", "warning"),
    (r"^Misconception Warning", "warning"),
    (r"^Cost Awareness", "warning"),
    (r"^Practical Example", "practical-example"),
    (r"^Application Example", "practical-example"),
    (r"^Example\b", "practical-example"),
    (r"^Fun Fact", "fun-note"),
    (r"^Fun Note", "fun-note"),
    (r"^Did You Know", "fun-note"),
    (r"^Research Frontier", "research-frontier"),
    (r"^Research$", "research-frontier"),
    (r"^Algorithm", "algorithm"),
    (r"^Pro Tip", "tip"),
    (r"^Best Practice", "tip"),
    (r"^Tip\b", "tip"),
    (r"^Exercise\b", "exercise"),
    (r"^Note\b", "note"),
    (r"^When to Use", "note"),
    (r"^Pathway\b", "pathway"),
    (r"^Prerequisites", "prerequisites"),
    (r"^Learning Objectives", "objectives"),
]

CLASS_TO_DEFAULT_TITLE = {
    "big-picture": "Big Picture",
    "key-insight": "Key Insight",
    "note": "Note",
    "warning": "Warning",
    "practical-example": "Practical Example",
    "fun-note": "Fun Note",
    "research-frontier": "Research Frontier",
    "algorithm": "Algorithm",
    "tip": "Tip",
    "exercise": "Exercise",
}

def strip_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def strip_emoji(text):
    return re.sub(r'^[\U0001f300-\U0001f9ff\u2600-\u27bf\u2b50\u26a0\U0001f4a1\U0001f4dd\U0001f3af\U0001f914\U0001f52c\U0001f9ea\U0001f4d6\U0001f527\U0001f3ac\u2733\u2734\u2728\u2764\u270f\u2699\u2b55\u274c\u2705\u26d4\u2757\u2753\s]+', '', text)

def title_to_class(title_text):
    title_text = strip_emoji(title_text.strip())
    for pattern, cls in TITLE_TO_CLASS:
        if re.search(pattern, title_text, re.IGNORECASE):
            return cls
    return None


all_issues = []
modified_files = []

html_files = glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
html_files.sort()

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    rel_path = os.path.relpath(filepath, ROOT)
    original = content

    # =====================================================================
    # PHASE 1: Fix non-standard classes and class/title mismatches
    # Match callout div + optional callout-title
    # =====================================================================
    def phase1_replacer(m):
        prefix = m.group(1)
        classes = m.group(2).strip()
        close = m.group(3)
        title_block = m.group(4) or ""
        title_text_raw = m.group(5)

        current_type = classes.split()[0] if classes else None
        clean_title = None
        if title_text_raw:
            clean_title = strip_html(title_text_raw).strip()
            # Strip HTML entities
            for ent, repl in [('&#9733;',''), ('&#128161;',''), ('&#127914;',''),
                              ('&#128221;',''), ('&#9888;',''), ('&amp;','&'),
                              ('&#x27;',"'")]:
                clean_title = clean_title.replace(ent, repl)
            clean_title = clean_title.strip()

        # No type class
        if not current_type and clean_title:
            expected = title_to_class(clean_title)
            if expected:
                all_issues.append(f"FIX BARE: {rel_path} - title='{clean_title}' -> '{expected}'")
                return f'{prefix} {expected}{close}{title_block}'
            return m.group(0)

        # Non-standard class
        if current_type and current_type not in VALID_CLASSES:
            expected = None
            if clean_title:
                expected = title_to_class(clean_title)
            if not expected and current_type in CLASS_NAME_MAP:
                expected = CLASS_NAME_MAP[current_type]
            if expected:
                all_issues.append(f"FIX CLASS: {rel_path} - '{current_type}' -> '{expected}' (title='{clean_title}')")
                new_classes = classes.replace(current_type, expected, 1)
                return f'{prefix} {new_classes}{close}{title_block}'
            all_issues.append(f"SKIP: {rel_path} - unknown class '{current_type}' title='{clean_title}'")
            return m.group(0)

        # Class/title mismatch
        if current_type and clean_title and current_type not in ('pathway', 'prerequisites', 'objectives'):
            expected = title_to_class(clean_title)
            if expected and expected != current_type:
                all_issues.append(f"FIX MISMATCH: {rel_path} - class='{current_type}' title='{clean_title}' -> '{expected}'")
                new_classes = classes.replace(current_type, expected, 1)
                return f'{prefix} {new_classes}{close}{title_block}'

        return m.group(0)

    pattern1 = re.compile(
        r'(<div\s+class="callout)( [^"]*|)(">)'
        r'(\s*<div\s+class="callout-title">(.*?)</div>)?',
        re.DOTALL
    )
    content = pattern1.sub(phase1_replacer, content)

    # =====================================================================
    # PHASE 2: Add missing callout-title where <strong> or <h4> is first child
    # =====================================================================

    # Pattern A: <div class="callout TYPE">\n<strong>Title</strong>\n<content...
    def phase2a_replacer(m):
        full_open = m.group(1)   # <div class="callout TYPE">
        ws1 = m.group(2)         # whitespace
        title = m.group(3)       # text inside <strong>
        ws2 = m.group(4)         # whitespace after </strong>
        callout_class = re.search(r'class="callout ([^"]*)"', full_open)
        ctype = callout_class.group(1).split()[0] if callout_class else "note"
        clean = strip_html(title).strip()
        all_issues.append(f"FIX TITLE(strong): {rel_path} - adding callout-title for '{clean}' (class={ctype})")
        indent = "    " if ws1 and "\n" in ws1 else ""
        return f'{full_open}\n{indent}<div class="callout-title">{clean}</div>{ws2}'

    pattern2a = re.compile(
        r'(<div\s+class="callout [^"]*">)'
        r'(\s*)'
        r'<strong>([^<]*)</strong>'
        r'(\s*)',
    )
    content = pattern2a.sub(phase2a_replacer, content)

    # Pattern B: <div class="callout TYPE">\n    <h4>Title</h4>\n<content...
    def phase2b_replacer(m):
        full_open = m.group(1)
        ws1 = m.group(2)
        title = m.group(3)
        ws2 = m.group(4)
        callout_class = re.search(r'class="callout ([^"]*)"', full_open)
        ctype = callout_class.group(1).split()[0] if callout_class else "note"
        clean = strip_html(title).strip()
        all_issues.append(f"FIX TITLE(h4): {rel_path} - adding callout-title for '{clean}' (class={ctype})")
        indent = "    " if ws1 and "\n" in ws1 else ""
        return f'{full_open}\n{indent}<div class="callout-title">{clean}</div>{ws2}'

    pattern2b = re.compile(
        r'(<div\s+class="callout [^"]*">)'
        r'(\s*)'
        r'<h4>([^<]*)</h4>'
        r'(\s*)',
    )
    content = pattern2b.sub(phase2b_replacer, content)

    # =====================================================================
    # PHASE 3: Fix class based on newly added title (re-run phase 1 logic)
    # =====================================================================
    content = pattern1.sub(phase1_replacer, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        modified_files.append(filepath)


# =========================================================================
# FINAL REPORT: Check for remaining issues
# =========================================================================
print("=" * 80)
print(f"SWEEP COMPLETE: Scanned {len(html_files)} HTML files")
print(f"Actions taken: {len(all_issues)}")
print(f"Modified: {len(modified_files)} files")
print("=" * 80)

for issue in all_issues:
    print(issue)

print()
print("=" * 80)
print("FILES MODIFIED:")
for f in modified_files:
    print(f"  {os.path.relpath(f, ROOT)}")

# Now re-scan to find any remaining issues
print()
print("=" * 80)
print("REMAINING ISSUES (post-fix scan):")
remaining = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    rel_path = os.path.relpath(filepath, ROOT)

    # Find all callout divs
    for m in re.finditer(r'<div\s+class="callout( [^"]*|)">', content):
        pos = m.end()
        classes = m.group(1).strip()
        current_type = classes.split()[0] if classes else None

        if current_type in ('pathway', 'prerequisites', 'objectives'):
            continue

        # Check for non-standard class
        if current_type and current_type not in VALID_CLASSES:
            print(f"  REMAINING NON_STANDARD: {rel_path} - class='{current_type}'")
            remaining += 1
            continue

        # Check if no type class
        if not current_type:
            print(f"  REMAINING BARE: {rel_path} - no type class")
            remaining += 1
            continue

        # Check for missing callout-title in next 200 chars
        next_chunk = content[pos:pos+300]
        if '<div class="callout-title">' not in next_chunk:
            # Could be legitimate if it has <strong> or <h4> as first child
            if re.match(r'\s*<(strong|h4)>', next_chunk):
                print(f"  REMAINING MISSING_TITLE: {rel_path} - class='{current_type}' (has <strong>/<h4> but no callout-title)")
                remaining += 1
            elif re.match(r'\s*<p>', next_chunk):
                print(f"  REMAINING MISSING_TITLE: {rel_path} - class='{current_type}' (starts with <p>, no title)")
                remaining += 1

        # Check for mismatch
        title_m = re.match(r'\s*<div\s+class="callout-title">(.*?)</div>', next_chunk, re.DOTALL)
        if title_m:
            clean = strip_html(title_m.group(1))
            for ent, repl in [('&#9733;',''), ('&#128161;',''), ('&#127914;',''),
                              ('&#128221;',''), ('&#9888;',''), ('&amp;','&'),
                              ('&#x27;',"'")]:
                clean = clean.replace(ent, repl)
            clean = clean.strip()
            expected = title_to_class(clean)
            if expected and expected != current_type:
                print(f"  REMAINING MISMATCH: {rel_path} - class='{current_type}' title='{clean}' -> should be '{expected}'")
                remaining += 1

print(f"\nTotal remaining issues: {remaining}")
