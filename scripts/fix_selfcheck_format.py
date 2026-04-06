"""
Standardize self-check quiz question labels to Q1:/Q2:/Q3: format.

Handles various non-standard patterns found in self-check blocks:
- "1. question" -> "<strong>Q1:</strong> question"
- "<strong>1.</strong> question" -> "<strong>Q1:</strong> question"
- "<strong>Q1:</strong> question" (already correct, skip)
- "<strong>Exercise N (Level X):</strong>" -> "<strong>QN:</strong>" (handled by previous script)
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")


def fix_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    original = content

    # Find self-check blocks
    # Strategy: find the self-check div, then fix quiz-question labels inside

    # Pattern 1: <div class="quiz-question">N. question text</div>
    # (number followed by period at start of quiz-question content)
    content = re.sub(
        r'(<div class="quiz-question">)\s*(\d+)\.\s+',
        lambda m: f'{m.group(1)}<strong>Q{m.group(2)}:</strong> ',
        content
    )

    # Pattern 2: <div class="quiz-question"><strong>N.</strong> question text
    content = re.sub(
        r'(<div class="quiz-question">)\s*<strong>(\d+)\.</strong>\s*',
        lambda m: f'{m.group(1)}<strong>Q{m.group(2)}:</strong> ',
        content
    )

    # Pattern 3: <div class="quiz-question"><strong>Q\d+.</strong> (missing colon)
    content = re.sub(
        r'(<div class="quiz-question">)\s*<strong>Q(\d+)\.</strong>\s*',
        lambda m: f'{m.group(1)}<strong>Q{m.group(2)}:</strong> ',
        content
    )

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        rel = filepath.relative_to(BOOK_ROOT)
        print(f"  FIXED: {rel}")
        return True
    return False


def main():
    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))

    fixed = 0
    for f in all_files:
        if fix_file(f):
            fixed += 1
    print(f"\nFixed: {fixed} files")

    # Verify: find quiz-questions that DON'T start with <strong>Q
    remaining = 0
    for f in all_files:
        text = f.read_text(encoding="utf-8")
        if 'callout self-check' not in text:
            continue
        for match in re.finditer(r'<div class="quiz-question">(.*?)(?:</div>|$)', text):
            qtext = match.group(1).strip()
            if not qtext.startswith('<strong>Q'):
                remaining += 1
                rel = f.relative_to(BOOK_ROOT)
                print(f"  NON-STANDARD: {rel}: {qtext[:80]}")

    print(f"Remaining non-standard: {remaining}")


if __name__ == "__main__":
    main()
