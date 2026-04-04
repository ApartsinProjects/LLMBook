#!/usr/bin/env python3
"""
TASK-131: Fix callout boxes that use bare <strong> tags instead of
proper <div class="callout-title"> for their titles.

Scans all HTML files and finds callout divs where the first child element
is a <strong> or <p><strong> instead of <div class="callout-title">.
Wraps the strong text in a proper <div class="callout-title"> element.
Also reports callouts that have NO title at all.
"""

import glob
import os
import re
from html.parser import HTMLParser


ROOT = os.path.dirname(os.path.abspath(__file__))

GLOB_PATTERNS = [
    "part-*/module-*/**/*.html",
    "appendices/**/*.html",
    "front-matter/**/*.html",
]


def find_html_files():
    """Collect all HTML files matching the glob patterns."""
    files = set()
    for pattern in GLOB_PATTERNS:
        for f in glob.glob(os.path.join(ROOT, pattern), recursive=True):
            files.add(os.path.normpath(f))
    return sorted(files)


# Regex to find callout divs and capture what follows them
# We look for <div class="callout ..."> then capture the next chunk of content
CALLOUT_OPEN = re.compile(
    r'(<div\s+class="callout\s+[^"]*">)'   # the callout div opening tag
    r'(\s*)'                                 # whitespace after opening tag
)


def analyze_file(filepath):
    """
    Parse a file and find callout divs. For each, determine what the
    first child element is:
      - <div class="callout-title"> : correct
      - <strong> : bare strong, needs fix
      - <p><strong> : paragraph-wrapped strong, needs fix
      - anything else without callout-title : missing title

    Returns list of dicts describing issues found.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    issues = []

    # Find all callout div openings
    for m in CALLOUT_OPEN.finditer(content):
        callout_tag = m.group(1)
        start_pos = m.end()

        # Get the next ~500 chars to inspect what follows
        snippet = content[start_pos:start_pos + 500].lstrip()

        # Determine the callout type from class
        cls_match = re.search(r'class="callout\s+([^"]*)"', callout_tag)
        callout_type = cls_match.group(1) if cls_match else "unknown"

        # Line number
        line_num = content[:m.start()].count("\n") + 1

        # Check what comes first
        if snippet.startswith('<div class="callout-title">'):
            # Correct structure, skip
            continue
        elif snippet.startswith("<strong>"):
            # Bare <strong> as first child
            strong_match = re.match(r"<strong>(.*?)</strong>", snippet, re.DOTALL)
            if strong_match:
                title_text = strong_match.group(1)
                issues.append({
                    "file": filepath,
                    "line": line_num,
                    "type": callout_type,
                    "issue": "bare_strong",
                    "title_text": title_text,
                })
        elif snippet.startswith("<p><strong>"):
            # <p><strong>Title</strong></p> pattern
            pstrong_match = re.match(
                r"<p><strong>(.*?)</strong></p>", snippet, re.DOTALL
            )
            if pstrong_match:
                title_text = pstrong_match.group(1)
                issues.append({
                    "file": filepath,
                    "line": line_num,
                    "type": callout_type,
                    "issue": "p_strong",
                    "title_text": title_text,
                })
            else:
                # Might be <p><strong>Title</strong> followed by more text in same <p>
                pstrong_match2 = re.match(
                    r"<p><strong>(.*?)</strong>", snippet, re.DOTALL
                )
                if pstrong_match2:
                    title_text = pstrong_match2.group(1)
                    issues.append({
                        "file": filepath,
                        "line": line_num,
                        "type": callout_type,
                        "issue": "p_strong_inline",
                        "title_text": title_text,
                    })
        elif not re.match(r"<div\b", snippet):
            # No div at all as first child, could be missing title
            # Check if there's a callout-title anywhere nearby (within 200 chars)
            nearby = content[start_pos:start_pos + 200]
            if "callout-title" not in nearby:
                # Get first tag for reporting
                first_tag_match = re.match(r"(<\w+[^>]*>)", snippet)
                first_tag = first_tag_match.group(1) if first_tag_match else snippet[:60]
                issues.append({
                    "file": filepath,
                    "line": line_num,
                    "type": callout_type,
                    "issue": "no_title",
                    "title_text": f"[first element: {first_tag}]",
                })

    return issues, content


def fix_bare_strong(content, filepath):
    """
    Fix pattern: <div class="callout TYPE">
                   <strong>Title</strong>
    Replace with: <div class="callout TYPE">
                   <div class="callout-title">Title</div>
    """
    changed = False

    # Pattern 1: bare <strong> right after callout div
    def replace_bare_strong(m):
        nonlocal changed
        changed = True
        callout_tag = m.group(1)
        whitespace = m.group(2)
        title_text = m.group(3)
        return f'{callout_tag}{whitespace}<div class="callout-title">{title_text}</div>'

    content = re.sub(
        r'(<div\s+class="callout\s+[^"]*">)'   # callout opening
        r'(\s*)'                                  # whitespace
        r'<strong>(.*?)</strong>',                 # bare strong
        replace_bare_strong,
        content,
        flags=re.DOTALL,
    )

    # Pattern 2: <p><strong>Title</strong></p> right after callout div
    def replace_p_strong(m):
        nonlocal changed
        changed = True
        callout_tag = m.group(1)
        whitespace = m.group(2)
        title_text = m.group(3)
        return f'{callout_tag}{whitespace}<div class="callout-title">{title_text}</div>'

    content = re.sub(
        r'(<div\s+class="callout\s+[^"]*">)'   # callout opening
        r'(\s*)'                                  # whitespace
        r'<p><strong>(.*?)</strong></p>',          # <p><strong>Title</strong></p>
        replace_p_strong,
        content,
        flags=re.DOTALL,
    )

    return content, changed


def main():
    files = find_html_files()
    print(f"Scanning {len(files)} HTML files...\n")

    all_issues = []
    files_fixed = 0
    fixes_applied = 0

    for filepath in files:
        issues, content = analyze_file(filepath)
        if issues:
            all_issues.extend(issues)

    # Report findings
    print("=" * 70)
    print("SCAN RESULTS")
    print("=" * 70)

    if not all_issues:
        print("\nNo issues found. All callout boxes use proper callout-title divs.")
    else:
        # Group by issue type
        bare_strong = [i for i in all_issues if i["issue"] == "bare_strong"]
        p_strong = [i for i in all_issues if i["issue"] == "p_strong"]
        p_strong_inline = [i for i in all_issues if i["issue"] == "p_strong_inline"]
        no_title = [i for i in all_issues if i["issue"] == "no_title"]

        fixable = bare_strong + p_strong + p_strong_inline

        if bare_strong:
            print(f"\n[BARE <strong>] {len(bare_strong)} instance(s):")
            for i in bare_strong:
                rel = os.path.relpath(i["file"], ROOT)
                print(f"  Line {i['line']}: {rel}")
                print(f"    Type: {i['type']}, Title: {i['title_text'][:80]}")

        if p_strong:
            print(f"\n[<p><strong>] {len(p_strong)} instance(s):")
            for i in p_strong:
                rel = os.path.relpath(i["file"], ROOT)
                print(f"  Line {i['line']}: {rel}")
                print(f"    Type: {i['type']}, Title: {i['title_text'][:80]}")

        if p_strong_inline:
            print(f"\n[<p><strong> inline] {len(p_strong_inline)} instance(s):")
            for i in p_strong_inline:
                rel = os.path.relpath(i["file"], ROOT)
                print(f"  Line {i['line']}: {rel}")
                print(f"    Type: {i['type']}, Title: {i['title_text'][:80]}")

        if no_title:
            print(f"\n[NO TITLE] {len(no_title)} instance(s):")
            for i in no_title:
                rel = os.path.relpath(i["file"], ROOT)
                print(f"  Line {i['line']}: {rel}")
                print(f"    Type: {i['type']}, First child: {i['title_text'][:80]}")

        # Now apply fixes
        if fixable:
            print(f"\n{'=' * 70}")
            print(f"APPLYING FIXES to {len(fixable)} fixable issue(s)...")
            print(f"{'=' * 70}")

            affected_files = set(i["file"] for i in fixable)
            for filepath in sorted(affected_files):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content, changed = fix_bare_strong(content, filepath)

                if changed:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    rel = os.path.relpath(filepath, ROOT)
                    print(f"  Fixed: {rel}")
                    files_fixed += 1

            # Re-scan to verify
            print(f"\n{'=' * 70}")
            print("VERIFICATION SCAN")
            print(f"{'=' * 70}")

            remaining = []
            for filepath in files:
                issues, _ = analyze_file(filepath)
                remaining.extend(issues)

            fixable_remaining = [
                i for i in remaining
                if i["issue"] in ("bare_strong", "p_strong", "p_strong_inline")
            ]
            no_title_remaining = [i for i in remaining if i["issue"] == "no_title"]

            if fixable_remaining:
                print(f"\n  WARNING: {len(fixable_remaining)} fixable issues remain!")
                for i in fixable_remaining:
                    rel = os.path.relpath(i["file"], ROOT)
                    print(f"    {i['issue']} at line {i['line']}: {rel}")
            else:
                print("\n  All fixable issues resolved.")

            if no_title_remaining:
                print(f"\n  INFO: {len(no_title_remaining)} callout(s) still have no title (may be intentional).")
                for i in no_title_remaining:
                    rel = os.path.relpath(i["file"], ROOT)
                    print(f"    Line {i['line']}: {rel} ({i['type']})")
        else:
            print("\nNo fixable issues (bare <strong> or <p><strong>) found.")

            if no_title:
                print(f"\n  INFO: {len(no_title)} callout(s) have no title (may be intentional).")

    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Files scanned: {len(files)}")
    print(f"  Total issues found: {len(all_issues)}")
    print(f"  Files modified: {files_fixed}")


if __name__ == "__main__":
    main()
