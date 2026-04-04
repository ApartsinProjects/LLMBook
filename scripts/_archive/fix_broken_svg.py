"""
Fix broken SVG self-closing tags across all HTML files.

The pattern: attribute="value"/ nextattr="..."  (slash before space instead of />)
Should be:   attribute="value" nextattr="..." />  OR  attribute="value"/>

Also fixes unclosed <rect>, <circle>, <line>, <path>, <ellipse>, <polygon>, <polyline>,
<stop>, <use>, <image> elements that have the broken pattern.
"""

import re
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")
SKIP_DIRS = {"vendor", "node_modules", ".git", "__pycache__", "scripts"}

# Pattern: "value"/ followed by a word char (attribute name) or >
# This catches the malformed self-closing syntax
BROKEN_PATTERN = re.compile(r'"(\s*)/\s+(\w)')

# Also fix: stroke-width="1"/ stroke-linecap="round">  ->  stroke-width="1" stroke-linecap="round"/>
# More specifically: attr="val"/ attr2="val2"> should become attr="val" attr2="val2"/>
BROKEN_CLOSE = re.compile(r'"(\s*)/\s+([\w-]+=)')


def fix_file(fpath: Path) -> int:
    text = fpath.read_text(encoding="utf-8", errors="ignore")
    original = text

    # Fix pattern: "value"/ nextattr  ->  "value" nextattr
    # But only inside SVG-like contexts (tags with these patterns)
    text = BROKEN_CLOSE.sub(r'" \2', text)

    # Also fix remaining "/ pattern at end before >
    # e.g., stroke-width="1"/ >  ->  stroke-width="1" />
    text = re.sub(r'"/\s*>', '"/>', text)

    # Fix tags that now end with "> but should be self-closing
    # SVG void elements that should be self-closing
    void_tags = ['rect', 'circle', 'line', 'path', 'ellipse', 'polygon',
                 'polyline', 'stop', 'use', 'image', 'feDropShadow',
                 'feGaussianBlur', 'feOffset', 'feMergeNode']

    for tag in void_tags:
        # Find opening tags that aren't self-closed and have no matching close
        # Pattern: <rect ... > (not <rect ... /> and not <rect>...</rect>)
        pattern = re.compile(
            r'(<' + tag + r'\s[^>]*[^/])>(?!\s*</' + tag + r'>)',
            re.IGNORECASE
        )
        text = pattern.sub(r'\1/>', text)

    if text != original:
        fpath.write_text(text, encoding="utf-8")
        changes = sum(1 for a, b in zip(original, text) if a != b)
        return changes
    return 0


def main():
    fixed = 0
    total_changes = 0
    for fpath in sorted(ROOT.rglob("*.html")):
        parts = fpath.relative_to(ROOT).parts
        if any(p in SKIP_DIRS for p in parts):
            continue
        changes = fix_file(fpath)
        if changes:
            fixed += 1
            print(f"  Fixed: {fpath.relative_to(ROOT)}")
            total_changes += changes

    print(f"\nDone: {fixed} files fixed.")


if __name__ == "__main__":
    main()
