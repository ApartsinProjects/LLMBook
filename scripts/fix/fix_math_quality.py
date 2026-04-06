"""
Fix math quality issues across the book.

Fixes:
1. bare-big-O: Wraps standalone O(...) in <span class="math">$O(...)$</span>
   - Simple: O(n), O(1), O(n^2), O(n log n)
   - HTML entities: O(n&sup2;), O(n &times; m)
   - Mixed: O(<span class="math">$T^{2}$</span>d) => <span class="math">$O(T^{2}d)$</span>

Usage:
  python fix_math_quality.py          # Dry run (report only)
  python fix_math_quality.py --fix    # Apply fixes
"""

import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# HTML entity to LaTeX mapping
HTML_TO_LATEX = {
    "&sup2;": "^{2}",
    "&sup3;": "^{3}",
    "&times;": r" \times ",
    "&minus;": "-",
    "&lt;": "<",
    "&gt;": ">",
    "&middot;": r" \cdot ",
    "&sdot;": r" \cdot ",
}


def is_inside_code_or_pre(content, pos):
    """Check if position is inside a <pre>, <code>, or <script> block."""
    # Search backwards for opening/closing tags
    before = content[max(0, pos - 2000):pos]
    # Check for unclosed <pre> or <code>
    last_pre_open = before.rfind("<pre")
    last_pre_close = before.rfind("</pre>")
    if last_pre_open > last_pre_close:
        return True

    last_code_open = before.rfind("<code")
    last_code_close = before.rfind("</code>")
    if last_code_open > last_code_close:
        return True

    last_script_open = before.rfind("<script")
    last_script_close = before.rfind("</script>")
    if last_script_open > last_script_close:
        return True

    return False


def is_inside_math_span(content, pos):
    """Check if position is already inside a <span class="math"> or $...$."""
    before = content[max(0, pos - 100):pos]
    # Already inside a math span
    if '<span class="math">' in before and '</span>' not in before[before.rfind('<span class="math">'):]:
        return True
    # Inside inline $...$ math
    # Count dollar signs in the last few chars
    recent = before[-10:]
    if recent.count('$') % 2 == 1:
        return True
    return False


def html_to_latex(text):
    """Convert HTML entities and tags to LaTeX equivalents."""
    result = text
    for entity, latex in HTML_TO_LATEX.items():
        result = result.replace(entity, latex)
    # Convert <sup>2</sup> to ^{2}
    result = re.sub(r'<sup>(\w+)</sup>', r'^{\1}', result)
    # Convert <sub>x</sub> to _{x}
    result = re.sub(r'<sub>(\w+)</sub>', r'_{\1}', result)
    # Extract content from nested math spans: <span class="math">$...$</span>
    result = re.sub(r'<span class="math">\$([^$]+)\$</span>', r'\1', result)
    # Use LaTeX operators for common functions
    result = re.sub(r'\blog\b', r'\\log', result)
    result = re.sub(r'\bsqrt\b', r'\\sqrt', result)
    # Escape bare underscores that are not LaTeX subscripts (e.g., n_steps)
    # Only escape _ when NOT followed by { (which is valid LaTeX subscript)
    result = re.sub(r'_(?!\{)', r'\\_', result)
    return result


def fix_bare_big_o(content):
    """Fix bare O(...) notation by wrapping in math spans.

    Handles:
    - Simple: O(n), O(1), O(n^2), O(n log n)
    - With HTML entities: O(n&sup2;), O(N &times; d)
    - With nested math spans: O(<span class="math">$T^{2}$</span>d)
    """
    changes = []

    # Pattern to match O(...) that may contain HTML tags, entities, etc.
    # We need a custom approach because the parens may contain nested spans.
    # Strategy: find each "O(" that is not inside code/math, then find its matching ")"

    i = 0
    new_content = content
    offset = 0  # track offset from insertions

    # Find all O( positions
    pattern = re.compile(r'(?<![<\w/])O\(')
    matches = list(pattern.finditer(content))

    for m in matches:
        pos = m.start()

        # Skip if inside code/pre block
        if is_inside_code_or_pre(content, pos):
            continue

        # Skip if already inside a math span
        if is_inside_math_span(content, pos):
            continue

        # Find matching closing paren, accounting for nested parens
        start = m.end()  # position after "O("
        depth = 1
        j = start
        while j < len(content) and depth > 0:
            if content[j] == '(':
                depth += 1
            elif content[j] == ')':
                depth -= 1
            j += 1

        if depth != 0:
            # Unbalanced parens, skip
            continue

        # Extract the full O(...) expression
        full_match = content[pos:j]
        inner = content[start:j - 1]  # content between O( and )

        # Skip if it looks like it's in a comment, attribute, or JS
        line_start = content.rfind('\n', 0, pos) + 1
        line = content[line_start:content.find('\n', pos)]
        if 'class=' in line and '"' in line[line.find('class='):line.find('class=') + 30]:
            # Possibly inside an HTML attribute, check more carefully
            before_on_line = content[line_start:pos]
            # Count quotes to see if we're inside an attribute value
            if before_on_line.count('"') % 2 == 1:
                continue

        # Convert inner content to LaTeX
        latex_inner = html_to_latex(inner)

        # Clean up: remove extra whitespace
        latex_inner = re.sub(r'\s+', ' ', latex_inner).strip()

        # Build the replacement
        replacement = f'<span class="math">$O({latex_inner})$</span>'

        line_num = content[:pos].count('\n') + 1
        changes.append((line_num, full_match, replacement))

        # Apply replacement with offset tracking
        adj_pos = pos + offset
        adj_end = j + offset
        new_content = new_content[:adj_pos] + replacement + new_content[adj_end:]
        offset += len(replacement) - (j - pos)

    return new_content, changes


def fix_file(filepath, apply=False):
    """Process a single file. Returns list of changes."""
    content = filepath.read_text(encoding="utf-8")
    new_content, changes = fix_bare_big_o(content)

    if apply and changes:
        filepath.write_text(new_content, encoding="utf-8")

    return changes


def main():
    fix_mode = '--fix' in sys.argv

    all_files = sorted(BOOK_ROOT.glob("part-*/module-*/section-*.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/section-*.html"))
    # Also include index.html files
    all_files += sorted(BOOK_ROOT.glob("part-*/module-*/index.html"))
    all_files += sorted(BOOK_ROOT.glob("appendices/*/index.html"))

    total_changes = 0
    files_changed = 0

    for f in all_files:
        changes = fix_file(f, apply=fix_mode)
        if changes:
            files_changed += 1
            rel = f.relative_to(BOOK_ROOT)
            print(f"\n{'FIXED' if fix_mode else 'WOULD FIX'}: {rel}")
            for line_num, old, new in changes:
                print(f"  L{line_num}: {old}")
                print(f"     => {new}")
            total_changes += len(changes)

    print(f"\n{'=' * 60}")
    mode_label = "Applied" if fix_mode else "Would apply"
    print(f"{mode_label}: {total_changes} fixes across {files_changed} files")
    print(f"Scanned: {len(all_files)} files")

    if not fix_mode:
        print("\nRun with --fix to apply changes.")


if __name__ == "__main__":
    main()
