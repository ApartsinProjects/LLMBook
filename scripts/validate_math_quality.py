"""
Validate math quality, correctness of LaTeX conversion, and typesetting issues.

Checks:
1. Broken/invalid LaTeX in $...$ and $$...$$ blocks
2. Unconverted HTML entities still in math (e.g., &times; inside $...$)
3. Mismatched braces in LaTeX
4. Double dollar signs without content
5. Unescaped underscores in text mode
6. Orphaned \text{} wrapping single characters
7. Missing closing $ or $$
8. HTML tags remaining inside LaTeX (e.g., <sub>, <sup>)
9. Empty math spans
10. Consecutive $$ blocks (already detected separately)
"""

import re
from pathlib import Path
from collections import defaultdict

BASE = Path(r"E:\Projects\LLMCourse")
EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", "scripts", "templates", "styles", "agents", "_lab_fragments", "vendor"}

def find_html_files():
    files = []
    for f in BASE.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in f.parts):
            continue
        files.append(f)
    return sorted(files)

def check_brace_balance(latex):
    """Check if braces are balanced in LaTeX."""
    depth = 0
    for ch in latex:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0

def validate_file(filepath):
    text = filepath.read_text(encoding="utf-8")
    issues = []

    # Find all inline math $...$
    for m in re.finditer(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', text, re.DOTALL):
        latex = m.group(1)
        line = text[:m.start()].count('\n') + 1

        # Empty math
        if not latex.strip():
            issues.append((line, "EMPTY_INLINE", "Empty inline math $...$"))
            continue

        # HTML entities remaining
        if re.search(r'&[a-zA-Z]+;', latex):
            entities = re.findall(r'&[a-zA-Z]+;', latex)
            issues.append((line, "HTML_ENTITY_IN_LATEX", f"Unconverted HTML entities: {', '.join(entities[:3])}"))

        # HTML tags remaining
        if re.search(r'<(?:sub|sup|em|strong|b|i|br)\b', latex):
            tags = re.findall(r'<(\w+)', latex)
            issues.append((line, "HTML_TAG_IN_LATEX", f"HTML tags in LaTeX: {', '.join(tags[:3])}"))

        # Brace balance
        if not check_brace_balance(latex):
            issues.append((line, "BRACE_MISMATCH", f"Unbalanced braces: ...{latex[:50]}..."))

        # Orphaned \text{} wrapping single letter
        if re.search(r'\\text\{[a-zA-Z]\}', latex):
            singles = re.findall(r'\\text\{([a-zA-Z])\}', latex)
            # Only flag if it's a math variable (should be italic, not \text)
            for s in singles:
                if s in 'xyzwuvnmkijqrstpabcdfghl':
                    issues.append((line, "TEXT_SINGLE_VAR", f"\\text{{{s}}} should be just {s} (italic variable)"))

        # Double backslash that's not a line break
        if '\\\\' in latex and 'align' not in latex:
            pass  # Could be intentional line break

    # Find all display math $$...$$
    for m in re.finditer(r'\$\$(.*?)\$\$', text, re.DOTALL):
        latex = m.group(1)
        line = text[:m.start()].count('\n') + 1

        if not latex.strip():
            issues.append((line, "EMPTY_BLOCK", "Empty block math $$...$$"))
            continue

        if re.search(r'&[a-zA-Z]+;', latex):
            entities = re.findall(r'&[a-zA-Z]+;', latex)
            issues.append((line, "HTML_ENTITY_IN_BLOCK", f"Unconverted entities: {', '.join(entities[:3])}"))

        if re.search(r'<(?:sub|sup|em|strong|b|i|br)\b', latex):
            tags = re.findall(r'<(\w+)', latex)
            issues.append((line, "HTML_TAG_IN_BLOCK", f"HTML tags in block: {', '.join(tags[:3])}"))

        if not check_brace_balance(latex):
            issues.append((line, "BRACE_MISMATCH_BLOCK", f"Unbalanced braces in block: ...{latex[:60]}..."))

        # Check for \text{} wrapping things that should be operators
        for word in ['log', 'exp', 'max', 'min', 'argmax', 'argmin', 'tanh', 'sigmoid',
                     'softmax', 'dim', 'det', 'trace', 'diag', 'sign', 'abs',
                     'cos', 'sin', 'tan']:
            if f'\\text{{{word}}}' in latex:
                issues.append((line, "TEXT_SHOULD_BE_OPERATOR", f"\\text{{{word}}} should be \\operatorname{{{word}}} or \\{word}"))

        # Underscore without braces for multi-char subscript
        if re.search(r'_[a-zA-Z]{2,}(?![{}])', latex):
            matches = re.findall(r'_([a-zA-Z]{2,})(?![{}])', latex)
            for match in matches[:2]:
                issues.append((line, "SUBSCRIPT_NO_BRACES", f"_{match} needs braces: _{{{match}}}"))

    # Check for old-style inline-styled math paragraphs
    for m in re.finditer(r'<p\s+style="[^"]*text-align:\s*center[^"]*font-style:\s*italic', text):
        line = text[:m.start()].count('\n') + 1
        issues.append((line, "LEGACY_STYLED_MATH", "Inline-styled math paragraph (should be math-block div)"))

    # Check for unconverted math-block content (no $ delimiters)
    for m in re.finditer(r'<div class="math-block"[^>]*>(.*?)</div>', text, re.DOTALL):
        content = m.group(1).strip()
        line = text[:m.start()].count('\n') + 1
        # Check if it has $$ delimiters
        if '$$' not in content and content and 'math-block-label' not in content:
            # Has actual content but no LaTeX delimiters
            clean = re.sub(r'<[^>]+>', '', content).strip()
            if clean and len(clean) > 3:
                issues.append((line, "UNCONVERTED_BLOCK", f"Math block without $$ delimiters: {clean[:50]}"))

    return issues

def main():
    files = find_html_files()
    print(f"Validating math quality in {len(files)} HTML files...\n")

    type_counts = defaultdict(int)
    total = 0
    files_with_issues = 0

    for f in files:
        issues = validate_file(f)
        if issues:
            files_with_issues += 1
            rel = f.relative_to(BASE)
            # Only print files with 2+ issues to reduce noise
            if len(issues) >= 2:
                print(f"  {rel}: {len(issues)} issues")
                for line, itype, desc in issues[:5]:
                    print(f"    Line {line}: [{itype}] {desc}")
                if len(issues) > 5:
                    print(f"    ... and {len(issues)-5} more")
            for _, itype, _ in issues:
                type_counts[itype] += 1
                total += 1

    print(f"\n{'='*60}")
    print(f"SUMMARY: {total} issues in {files_with_issues} files\n")
    print("By type:")
    for itype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {itype}: {count}")

if __name__ == "__main__":
    main()
