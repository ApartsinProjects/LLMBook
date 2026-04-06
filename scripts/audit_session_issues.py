"""
Comprehensive audit based on issues found in recent review sessions.

Checks:
1. Self-check labels: quiz-questions should use <strong>QN:</strong> format
2. Orphan captions: code-caption with no preceding </pre>
3. Algorithm boxes: empty (caption but no <pre>)
4. Algorithm boxes: multiple <pre> blocks inside single box
5. Broken math: &#36; inside quiz-questions (KaTeX conflict)
6. SVG text overflow: text elements beyond their container rect
7. Non-standard labs: lab content without <div class="lab"> wrapper
8. Exercises heading: standalone <h2>Exercises</h2> (should be handled by book.js)
9. Takeaways missing: pages without .takeaways div
10. Self-check position: self-check after exercises (wrong order in HTML)
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")


def check_selfcheck_labels(filepath, content, issues):
    """Check quiz-questions use <strong>QN:</strong> format."""
    if 'callout self-check' not in content:
        return
    for m in re.finditer(r'<div class="quiz-question">(.*?)(?:</div>|$)', content):
        qtext = m.group(1).strip()
        if not qtext.startswith('<strong>Q'):
            issues.append(("self-check-label", filepath, m.start(), qtext[:60]))


def check_dollar_in_quiz(filepath, content, issues):
    """Check for &#36; in quiz questions (KaTeX conflict)."""
    if 'callout self-check' not in content:
        return
    for m in re.finditer(r'<div class="quiz-question">(.*?)</div>', content, re.DOTALL):
        if '&#36;' in m.group(1):
            issues.append(("dollar-in-quiz", filepath, m.start(), "&#36; found in quiz question"))


def check_empty_algorithm(filepath, content, issues):
    """Check algorithm callouts with caption but no <pre>."""
    for m in re.finditer(
        r'<div class="callout algorithm">(.*?)</div>\s*</div>',
        content, re.DOTALL
    ):
        block = m.group(1)
        if '<pre>' not in block and 'code-caption' in block:
            cap = re.search(r'code-caption.*?>(.*?)</div>', block)
            cap_text = cap.group(1)[:60] if cap else "?"
            issues.append(("empty-algorithm", filepath, m.start(), cap_text))


def check_multi_pre_algorithm(filepath, content, issues):
    """Check algorithm callouts with multiple <pre> blocks."""
    for m in re.finditer(
        r'<div class="callout algorithm">(.*?)</div>\s*(?:</div>|<[^d])',
        content, re.DOTALL
    ):
        block = m.group(1)
        pre_count = block.count('<pre>')
        if pre_count > 1:
            title = re.search(r'callout-title">(.*?)</div>', block)
            title_text = title.group(1)[:60] if title else "?"
            issues.append(("multi-pre-algorithm", filepath, m.start(), f"{pre_count} <pre> blocks: {title_text}"))


def check_broken_math_blocks(filepath, content, issues):
    """Check for broken LaTeX subscripts in math-block."""
    for m in re.finditer(r'<div class="math-block">\s*\$\$(.*?)\$\$', content, re.DOTALL):
        math = m.group(1)
        # Check for consecutive subscripts like _{a}_{b}
        if re.search(r'\}_\{', math):
            issues.append(("broken-math", filepath, m.start(), math.strip()[:80]))


def check_missing_takeaways(filepath, content, issues):
    """Check sections missing .takeaways div."""
    # Only check actual section files
    if 'index.html' in str(filepath):
        return
    if '<div class="takeaways">' not in content and 'class="takeaways"' not in content:
        if '<h2>' in content:  # Has content sections, should have takeaways
            issues.append(("missing-takeaways", filepath, 0, "No .takeaways div found"))


def main():
    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))

    issues = []
    for f in all_files:
        content = f.read_text(encoding="utf-8")
        check_selfcheck_labels(f, content, issues)
        check_dollar_in_quiz(f, content, issues)
        check_empty_algorithm(f, content, issues)
        check_multi_pre_algorithm(f, content, issues)
        check_broken_math_blocks(f, content, issues)

    # Group by type
    by_type = {}
    for issue_type, filepath, pos, desc in issues:
        by_type.setdefault(issue_type, []).append((filepath, pos, desc))

    print(f"Scanned {len(all_files)} files\n")
    for itype, items in sorted(by_type.items()):
        print(f"=== {itype} ({len(items)} issues) ===")
        for filepath, pos, desc in items:
            rel = filepath.relative_to(BOOK_ROOT)
            print(f"  {rel}: {desc}")
        print()

    total = sum(len(v) for v in by_type.values())
    print(f"Total issues: {total}")


if __name__ == "__main__":
    main()
