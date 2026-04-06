"""
Fix self-check quiz questions that use "Exercise N (Level X):" format.
Converts to standard "QN:" format inside self-check callouts only.
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")


def fix_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    original = content

    # Find self-check blocks and fix quiz-question labels inside them
    # Pattern: inside .callout.self-check, replace
    #   <strong>Exercise N (Level X):</strong>
    #   <strong>Exercise N (Level X, Research):</strong>
    # with <strong>QN:</strong>

    # Strategy: find each self-check block, fix labels within it
    selfcheck_re = re.compile(
        r'(<div class="callout self-check">)(.*?)(</div>\s*(?=<div class="callout|<div class="takeaways|<div class="whats-next|<h2|<nav|</main|<footer|<section))',
        re.DOTALL
    )

    def fix_labels(match):
        prefix = match.group(1)
        body = match.group(2)
        suffix = match.group(3)

        # Replace Exercise N labels with QN
        body = re.sub(
            r'<strong>Exercise\s+(\d+)\s*\([^)]*\):</strong>',
            lambda m: f'<strong>Q{m.group(1)}:</strong>',
            body
        )
        return prefix + body + suffix

    content = selfcheck_re.sub(fix_labels, content)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        rel = filepath.relative_to(BOOK_ROOT)
        # Count fixes
        fixes = original.count("Exercise") - content.count("Exercise")
        print(f"  FIXED {fixes} label(s): {rel}")
        return True
    return False


def main():
    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    fixed = 0
    for f in all_files:
        if fix_file(f):
            fixed += 1
    print(f"\nFixed: {fixed} files")

    # Verify: no remaining "Exercise N" inside self-check blocks
    remaining = 0
    for f in all_files:
        text = f.read_text(encoding="utf-8")
        # Quick check: find self-check blocks with Exercise labels
        in_selfcheck = False
        for line in text.split('\n'):
            if 'callout self-check' in line:
                in_selfcheck = True
            if in_selfcheck and '<strong>Exercise' in line and 'quiz-question' in text[max(0, text.index(line)-200):text.index(line)]:
                remaining += 1
                print(f"  REMAINING: {f.relative_to(BOOK_ROOT)}: {line.strip()[:80]}")
            if in_selfcheck and ('</div>' in line and line.strip() == '</div>'):
                pass  # Don't reset, self-check blocks have nested divs

    print(f"Remaining: {remaining}")


if __name__ == "__main__":
    main()
