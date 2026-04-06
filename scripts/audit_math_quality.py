"""
Audit and fix math quality issues across the entire book.

Detects:
1. ~ instead of \\sim in distribution notation ($r ~ U(0,1)$)
2. << or >> instead of \\ll or \\gg
3. Display math ($$...$$) not inside <div class="math-block">
4. Display math using / instead of \\frac for main expressions
5. Plain text labels in display math without \\text{} wrapper
6. O(...) big-O notation not inside math spans
7. _{...}_{...} consecutive subscripts (broken LaTeX)
8. &#36; inside quiz-question (KaTeX conflict)

Usage:
  python audit_math_quality.py          # Report only
  python audit_math_quality.py --fix    # Fix safe patterns
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")


def audit_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    issues = []

    # 1. ~ instead of \sim in math spans
    for m in re.finditer(r'\$([^$]+)\$', content):
        math = m.group(1)
        if re.search(r'[a-zA-Z]\s*~\s*[A-Z]', math) and '\\sim' not in math:
            line = content[:m.start()].count('\n') + 1
            issues.append(("tilde-not-sim", line, math.strip()[:60]))

    # 2. << or >> instead of \ll or \gg in math
    for m in re.finditer(r'\$([^$]+)\$', content):
        math = m.group(1)
        if '<<' in math and '\\ll' not in math:
            line = content[:m.start()].count('\n') + 1
            issues.append(("double-lt", line, math.strip()[:60]))
        if '>>' in math and '\\gg' not in math:
            line = content[:m.start()].count('\n') + 1
            issues.append(("double-gt", line, math.strip()[:60]))

    # 3. Bare $$...$$ not inside math-block
    for m in re.finditer(r'(?<!\$)\$\$(.+?)\$\$(?!\$)', content, re.DOTALL):
        preceding = content[max(0, m.start()-200):m.start()]
        if 'math-block' not in preceding:
            line = content[:m.start()].count('\n') + 1
            issues.append(("bare-display-math", line, m.group(1).strip()[:60]))

    # 4. Display math using / for main fraction (heuristic: word = expr / expr)
    for m in re.finditer(r'\$\$(.+?)\$\$', content, re.DOTALL):
        math = m.group(1).strip()
        # Check for patterns like "= (...) / (...)" without \frac
        if '\\frac' not in math and re.search(r'=\s*[^/]+\s*/\s*[^/]+$', math):
            line = content[:m.start()].count('\n') + 1
            issues.append(("slash-not-frac", line, math[:60]))

    # 5. Display math with plain English labels (no \text{})
    for m in re.finditer(r'\$\$(.+?)\$\$', content, re.DOTALL):
        math = m.group(1).strip()
        # Check for multi-word labels without \text{}: e.g., "Accept probability ="
        words = re.findall(r'[A-Z][a-z]+\s+[a-z]+', math)
        if words and '\\text' not in math and '\\mathrm' not in math:
            line = content[:m.start()].count('\n') + 1
            issues.append(("plain-label", line, f"'{words[0]}' in: {math[:60]}"))

    # 6. O(...) outside math spans
    for m in re.finditer(r'(?<![<\w])O\(([^)]+)\)(?!<)', content):
        # Check if inside a <span class="math"> or $...$
        preceding = content[max(0, m.start()-50):m.start()]
        if '<span class="math">' not in preceding and '$' not in preceding[-5:]:
            # Skip if inside code blocks
            code_check = content[max(0, m.start()-200):m.start()]
            if '<pre>' not in code_check and '<code>' not in code_check:
                line = content[:m.start()].count('\n') + 1
                issues.append(("bare-big-o", line, m.group(0)))

    # 7. Consecutive subscripts }_{ (often broken)
    for m in re.finditer(r'\$([^$]+)\$', content):
        math = m.group(1)
        if '}_{' in math:
            # Some are valid (like matrix element a_{i}_{j}), but flag for review
            line = content[:m.start()].count('\n') + 1
            issues.append(("consecutive-subscript", line, math.strip()[:60]))

    # 8. &#36; inside quiz-question
    for m in re.finditer(r'<div class="quiz-question">(.*?)</div>', content, re.DOTALL):
        if '&#36;' in m.group(1):
            line = content[:m.start()].count('\n') + 1
            issues.append(("dollar-in-quiz", line, "&#36; found in quiz question"))

    return issues, content


def fix_file(filepath):
    content = filepath.read_text(encoding="utf-8")
    original = content

    # Fix 1: ~ to \sim in math (only safe patterns)
    def fix_tilde(m):
        math = m.group(1)
        if re.search(r'[a-zA-Z]\s*~\s*[A-Z]', math) and '\\sim' not in math:
            math = re.sub(r'(\w)\s*~\s*([A-Z])', r'\1 \\sim \2', math)
        return f'${math}$'
    content = re.sub(r'\$([^$]+)\$', fix_tilde, content)

    # Fix 2: << to \ll, >> to \gg in math
    def fix_ll_gg(m):
        math = m.group(1)
        if '<<' in math and '\\ll' not in math:
            math = math.replace('<<', '\\ll')
        if '>>' in math and '\\gg' not in math:
            math = math.replace('>>', '\\gg')
        return f'${math}$'
    content = re.sub(r'\$([^$]+)\$', fix_ll_gg, content)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    fix_mode = '--fix' in sys.argv

    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))

    total_issues = 0
    files_with_issues = 0
    by_type = {}

    for f in all_files:
        issues, _ = audit_file(f)
        if issues:
            files_with_issues += 1
            rel = f.relative_to(BOOK_ROOT)
            print(f"\n=== {rel} ===")
            for itype, line, desc in issues:
                print(f"  [{itype}] L{line}: {desc}")
                by_type.setdefault(itype, []).append((str(rel), line, desc))
                total_issues += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    for itype, items in sorted(by_type.items()):
        print(f"  {itype}: {len(items)}")
    print(f"Total issues: {total_issues} across {files_with_issues} files")
    print(f"Scanned: {len(all_files)} files")

    if fix_mode:
        print(f"\n--- Applying safe fixes (tilde->sim, <<->ll) ---")
        fixed = 0
        for f in all_files:
            if fix_file(f):
                rel = f.relative_to(BOOK_ROOT)
                print(f"  FIXED: {rel}")
                fixed += 1
        print(f"Fixed: {fixed} files")


if __name__ == "__main__":
    main()
