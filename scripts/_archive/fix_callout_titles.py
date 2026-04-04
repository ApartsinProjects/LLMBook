"""Fix two callout formatting issues across all HTML files in the LLMCourse project.

Issue 1 (CALLOUT_H4_TITLE): Convert <h4>...</h4> inside callout divs to
    <div class="callout-title">...</div>

Issue 2 (FUN_NOTE_NO_TITLE): Add missing <div class="callout-title">Fun Fact</div>
    inside fun-note callouts that lack one.
"""

import os
import re
import sys

BASE_DIR = r"E:\Projects\LLMCourse"

# Directories to scan (top-level prefixes)
INCLUDE_PREFIXES = ("part-", "appendices", "front-matter")

# Directories to exclude
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", ".git", "scripts"}


def collect_html_files(base):
    """Collect all .html files under included directories."""
    html_files = []
    for entry in os.listdir(base):
        full = os.path.join(base, entry)
        if not os.path.isdir(full):
            continue
        if entry in EXCLUDE_DIRS:
            continue
        if not any(entry.startswith(p) for p in INCLUDE_PREFIXES):
            continue
        for root, dirs, files in os.walk(full):
            # Prune excluded subdirectories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                if f.endswith(".html"):
                    html_files.append(os.path.join(root, f))
    return sorted(html_files)


def fix_h4_in_callouts(content):
    """Issue 1: Replace <h4>...</h4> with <div class="callout-title">...</div>
    when the h4 is inside a callout div (preceded by <div class="callout within 500 chars)."""
    count = 0

    def replacer(match):
        nonlocal count
        start = max(0, match.start() - 500)
        preceding = content[start:match.start()]
        # Check if there is a callout div opening in the preceding text
        if re.search(r'<div\s+class="callout\s', preceding):
            count += 1
            inner = match.group(1)
            return f'<div class="callout-title">{inner}</div>'
        return match.group(0)

    # Match <h4>...</h4> (non-greedy, single line usually)
    result = re.sub(r'<h4>(.*?)</h4>', replacer, content, flags=re.DOTALL)
    return result, count


def fix_fun_note_missing_title(content):
    """Issue 2: Insert <div class="callout-title">Fun Fact</div> after fun-note
    callout opening tags that don't already have a callout-title."""
    count = 0

    # Pattern: <div class="callout fun-note" ...> followed by whitespace,
    # but NOT followed by <div class="callout-title">
    pattern = re.compile(
        r'(<div\s+class="callout\s+fun-note"[^>]*>)'  # group 1: opening tag
        r'(\s*)'                                        # group 2: whitespace after
        r'(?!<div\s+class="callout-title">)',           # negative lookahead
        re.DOTALL
    )

    def replacer(match):
        nonlocal count
        count += 1
        opening_tag = match.group(1)
        whitespace = match.group(2)
        # Determine indentation from whitespace
        # Use the whitespace as-is, then add the title div with similar indent
        # Detect the indentation level: find last newline in whitespace
        if "\n" in whitespace:
            lines = whitespace.split("\n")
            indent = lines[-1]  # whitespace on the last line (the indent before next element)
        else:
            indent = "    "
        return f'{opening_tag}\n{indent}<div class="callout-title">Fun Fact</div>\n{indent}'

    result = pattern.sub(replacer, content)
    return result, count


def main():
    html_files = collect_html_files(BASE_DIR)
    print(f"Found {len(html_files)} HTML files to process.\n")

    total_h4 = 0
    total_fun = 0
    files_h4 = 0
    files_fun = 0

    for filepath in html_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original = content

        content, h4_count = fix_h4_in_callouts(content)
        content, fun_count = fix_fun_note_missing_title(content)

        if h4_count > 0 or fun_count > 0:
            rel = os.path.relpath(filepath, BASE_DIR)
            parts = []
            if h4_count > 0:
                parts.append(f"h4_fix={h4_count}")
                files_h4 += 1
            if fun_count > 0:
                parts.append(f"fun_note_title={fun_count}")
                files_fun += 1
            print(f"  {rel}: {', '.join(parts)}")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

        total_h4 += h4_count
        total_fun += fun_count

    print(f"\nSummary")
    print(f"  CALLOUT_H4_TITLE fixes: {total_h4} (across {files_h4} files)")
    print(f"  FUN_NOTE_NO_TITLE fixes: {total_fun} (across {files_fun} files)")
    print(f"  Total fixes: {total_h4 + total_fun}")


if __name__ == "__main__":
    main()
