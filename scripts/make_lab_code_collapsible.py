"""
Make code fragments in hands-on labs collapsible (collapsed by default).

Wraps each <pre> block inside a .lab-step div with a <details> element.
Also ensures exercise answers use <details> without the 'open' attribute.

Pattern:
  Before: <pre><code>...</code></pre>
  After:  <details class="lab-code-collapse">
            <summary>Show Code</summary>
            <pre><code>...</code></pre>
          </details>

Also wraps any immediately following .code-output div inside the details.
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

stats = {
    "scanned": 0,
    "lab_code_wrapped": 0,
    "files_changed": 0,
    "details_open_removed": 0,
}


def wrap_lab_code(content):
    """Wrap <pre> blocks inside .lab-step divs with <details>."""
    changed = False

    # Find all lab-step sections
    # We need to find <pre> blocks that are inside lab-step divs
    # and not already inside <details>

    # Strategy: find lab-step div boundaries, then within those, wrap <pre> blocks
    # Simpler: look for <pre> blocks preceded by lab-step context

    # Actually, let's use a different approach:
    # Find all <pre> blocks that appear after a <div class="lab-step"> and before the next </div> at the same level
    # This is hard with regex. Instead, use a state machine approach.

    # Simpler approach: find <pre> blocks inside any element that has lab-step class
    # by checking the surrounding context

    lines = content.split('\n')
    result_lines = []
    in_lab_step = 0  # nesting depth
    i = 0

    while i < len(lines):
        line = lines[i]

        # Track lab-step nesting
        if 'class="lab-step"' in line or "class='lab-step'" in line:
            in_lab_step += 1
        if in_lab_step > 0:
            # Count div opens and closes to track nesting
            opens = len(re.findall(r'<div\b', line))
            closes = len(re.findall(r'</div>', line))

            # Check if this line starts a <pre> block that's not already in <details>
            if '<pre' in line and 'lab-code-collapse' not in lines[max(0, i-1)] and 'lab-code-collapse' not in lines[max(0, i-2)]:
                # Check if there's already a <details> wrapper
                prev_context = '\n'.join(lines[max(0, i-3):i])
                if 'lab-code-collapse' not in prev_context and '<details' not in prev_context:
                    # Wrap this <pre> block with <details>
                    result_lines.append('                    <details class="lab-code-collapse">')
                    result_lines.append('                    <summary>Show Code</summary>')

                    # Collect the <pre>...</pre> block (may span multiple lines)
                    pre_lines = [line]
                    while '</pre>' not in lines[i]:
                        i += 1
                        if i >= len(lines):
                            break
                        pre_lines.append(lines[i])
                    result_lines.extend(pre_lines)

                    # Check if next non-empty line is a code-output div
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == '':
                        j += 1
                    if j < len(lines) and 'class="code-output"' in lines[j]:
                        # Include the code-output div in the details
                        while j < len(lines):
                            result_lines.append(lines[j])
                            if '</div>' in lines[j]:
                                # Check if this closes the code-output div
                                # Simple heuristic: if the line has code-output or we've been collecting
                                break
                            j += 1
                        i = j

                    # Check for code-caption too
                    k = i + 1
                    while k < len(lines) and lines[k].strip() == '':
                        k += 1
                    if k < len(lines) and 'code-caption' in lines[k]:
                        result_lines.append(lines[k])
                        i = k

                    result_lines.append('                    </details>')
                    stats["lab_code_wrapped"] += 1
                    changed = True
                    i += 1
                    continue

            # Adjust lab-step depth
            if in_lab_step > 0:
                in_lab_step += opens - closes
                if in_lab_step < 0:
                    in_lab_step = 0

        result_lines.append(line)
        i += 1

    if changed:
        return '\n'.join(result_lines), True
    return content, False


def remove_details_open(content):
    """Remove 'open' attribute from <details> in exercise callouts."""
    new_content = re.sub(r'<details\s+open\s*>', '<details>', content)
    if new_content != content:
        count = len(re.findall(r'<details\s+open\s*>', content))
        stats["details_open_removed"] += count
        return new_content, True
    return content, False


def process_file(filepath):
    """Process a single file."""
    content = filepath.read_text(encoding="utf-8")
    original = content
    stats["scanned"] += 1

    # Wrap lab code
    content, lab_changed = wrap_lab_code(content)

    # Remove open from details
    content, details_changed = remove_details_open(content)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        stats["files_changed"] += 1
        return True
    return False


def main():
    patterns = [
        "part-*/module-*/section-*.html",
        "appendices/appendix-*/section-*.html",
    ]

    all_files = []
    for pattern in patterns:
        all_files.extend(BOOK_ROOT.glob(pattern))
    all_files = sorted(set(all_files))

    print(f"Scanning {len(all_files)} files...")

    for f in all_files:
        changed = process_file(f)
        if changed:
            print(f"  CHANGED: {f.relative_to(BOOK_ROOT)}")

    print(f"\n=== Summary ===")
    print(f"Total scanned: {stats['scanned']}")
    print(f"Files changed: {stats['files_changed']}")
    print(f"Lab code blocks wrapped: {stats['lab_code_wrapped']}")
    print(f"Details 'open' attributes removed: {stats['details_open_removed']}")


if __name__ == "__main__":
    main()
