"""
Fix misplaced code captions inside library-shortcut callouts.

Pattern detected: A <div class="code-caption"> that describes the MAIN code block
appears INSIDE a library-shortcut callout, before the shortcut's own <pre> block.

Fix: Move the caption to just before the library-shortcut callout opening tag,
so it sits between the main code block (or its output) and the shortcut.
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# Pattern: inside a library-shortcut, find code-caption that appears before <pre>
# We look for the full library-shortcut block and check if it starts with a code-caption
# before its <pre>

def fix_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    original = content

    # Find library-shortcut callouts that have a code-caption before their <pre>
    # Pattern: <div class="callout library-shortcut">...text...<div class="code-caption">CAPTION</div>\n<pre>
    # We need to move that caption div outside, before the callout

    # Strategy: find each library-shortcut block opening, then check if there's
    # a code-caption before the first <pre> inside it

    pattern = re.compile(
        r'(<div class="callout library-shortcut">\s*'   # callout open
        r'(?:<div class="callout-title">.*?</div>\s*|<p class="callout-label">.*?</p>\s*)'  # title/label
        r'<p>.*?</p>\s*)'                                # description paragraph
        r'(<div class="code-caption">.*?</div>\s*)'      # MISPLACED caption
        r'(<pre>)',                                        # pre block
        re.DOTALL
    )

    fixes = 0
    while True:
        match = pattern.search(content)
        if not match:
            break

        # The caption needs to move before the callout opening
        callout_start = match.start()
        caption_text = match.group(2)

        # Find where to insert the caption: just before the <div class="callout library-shortcut">
        # Insert caption + newline before the callout div
        before_callout = content[:callout_start]
        after_match_start = match.group(1) + match.group(3)  # callout opening + description + pre (without caption)
        rest = content[match.end():]

        content = before_callout + caption_text.strip() + '\n' + after_match_start + rest
        fixes += 1

    if fixes > 0:
        filepath.write_text(content, encoding="utf-8")
        rel = filepath.relative_to(BOOK_ROOT)
        print(f"  FIXED {fixes} caption(s): {rel}")

    return fixes


def main():
    patterns = [
        "part-*/module-*/section-*.html",
        "appendices/*/section-*.html",
    ]

    all_files = []
    for p in patterns:
        all_files.extend(BOOK_ROOT.glob(p))
    all_files = sorted(set(all_files))

    total_fixes = 0
    for f in all_files:
        total_fixes += fix_file(f)

    print(f"\nTotal fixes: {total_fixes}")

    # Verify: find remaining code-captions inside library-shortcuts before <pre>
    verify_pattern = re.compile(
        r'<div class="callout library-shortcut">.*?'
        r'<div class="code-caption">.*?</div>\s*<pre>',
        re.DOTALL
    )
    remaining = 0
    for f in all_files:
        text = f.read_text(encoding="utf-8")
        matches = verify_pattern.findall(text)
        for m in matches:
            remaining += 1
            rel = f.relative_to(BOOK_ROOT)
            # Extract caption text
            cap = re.search(r'<div class="code-caption">(.*?)</div>', m)
            cap_text = cap.group(1)[:80] if cap else "?"
            print(f"  REMAINING: {rel}: {cap_text}")

    print(f"Remaining misplaced: {remaining}")


if __name__ == "__main__":
    main()
