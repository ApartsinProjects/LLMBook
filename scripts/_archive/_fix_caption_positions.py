"""
Fix code caption positioning across all section HTML files.

Moves <div class="code-caption"> from BEFORE <pre> blocks to AFTER them
(or after any .code-output div that follows the </pre>).

Also handles captions that ended up inside <pre> blocks.
"""

import re
import glob
import os

def fix_captions_before_pre(content):
    """Find caption divs that appear before a <pre> block and move them after."""
    fixes = 0

    # Pattern: caption div followed (possibly with whitespace) by a <pre> block
    # The caption div is a single line: <div class="code-caption">...</div>
    # We need to match: caption_div \n <pre>...</pre> (optionally followed by code-output div)

    # Strategy: work line-by-line for reliability
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if this line is a code-caption div
        if stripped.startswith('<div class="code-caption">') and stripped.endswith('</div>'):
            # Look ahead: skip blank lines, find <pre>
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1

            if j < len(lines) and '<pre' in lines[j].strip()[:10]:
                # This caption is BEFORE a pre block. We need to move it.
                caption_line = lines[i]
                # Skip the caption line, we'll insert it later
                i = j  # now i points to the <pre> line

                # Find the end of the pre block
                # The </pre> might be on the same line or a later line
                pre_end = i
                while pre_end < len(lines):
                    if '</pre>' in lines[pre_end]:
                        break
                    pre_end += 1

                # Output the pre block lines
                for k in range(i, pre_end + 1):
                    new_lines.append(lines[k])

                i = pre_end + 1

                # Check if a code-output div follows
                peek = i
                while peek < len(lines) and lines[peek].strip() == '':
                    peek += 1

                if peek < len(lines) and 'class="code-output"' in lines[peek]:
                    # Output everything up to and including the closing </div> of code-output
                    # code-output may span multiple lines
                    out_start = peek
                    # Find closing </div> for code-output
                    out_end = peek
                    # The code-output div might close on same line or later
                    depth = 0
                    found_close = False
                    for k in range(peek, len(lines)):
                        # Simple approach: find </div> on the line
                        if '</div>' in lines[k]:
                            out_end = k
                            found_close = True
                            break

                    # Output any blank lines between pre and code-output
                    for k in range(i, out_start):
                        new_lines.append(lines[k])
                    # Output code-output lines
                    for k in range(out_start, out_end + 1):
                        new_lines.append(lines[k])

                    # Now insert the caption
                    new_lines.append(caption_line)
                    fixes += 1
                    i = out_end + 1
                else:
                    # No code-output, insert caption right after </pre>
                    new_lines.append(caption_line)
                    fixes += 1
                continue
            else:
                # Caption is not before a pre block, leave it
                new_lines.append(line)
                i += 1
                continue
        else:
            new_lines.append(line)
            i += 1

    return '\n'.join(new_lines), fixes


def fix_captions_inside_pre(content):
    """Find caption divs that are inside <pre> blocks and extract them."""
    fixes = 0

    # Pattern: inside a <pre>...</pre>, there's a code-caption div
    # This would look like: </pre>\n some stuff \n <div class="code-caption">...</div>\n<pre>
    # But actually from the earlier analysis, the issue is that the caption appears
    # between the closing </pre> of one block and before the <pre> of the next,
    # which got detected as "inside" because the search was confused.
    # Let me check for actual inside-pre cases differently.

    # Look for: <pre> ... <div class="code-caption"> ... </pre>
    # where the caption div is literally inside the pre content

    lines = content.split('\n')
    new_lines = []
    in_pre = False
    captions_to_extract = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if '<pre' in stripped and '</pre>' not in stripped:
            in_pre = True

        if in_pre and stripped.startswith('<div class="code-caption">') and stripped.endswith('</div>'):
            # Caption inside a pre block! Extract it.
            captions_to_extract.append(line)
            fixes += 1
            i += 1
            continue

        if '</pre>' in stripped:
            in_pre = False
            new_lines.append(line)
            # Insert any extracted captions after this </pre>
            # But first check for code-output
            if captions_to_extract:
                # Peek for code-output
                peek = i + 1
                while peek < len(lines) and lines[peek].strip() == '':
                    peek += 1
                if peek < len(lines) and 'class="code-output"' in lines[peek]:
                    # Output blank lines and code-output first
                    for k in range(i + 1, peek):
                        new_lines.append(lines[k])
                    # Find end of code-output
                    out_end = peek
                    for k in range(peek, len(lines)):
                        if '</div>' in lines[k]:
                            out_end = k
                            break
                    for k in range(peek, out_end + 1):
                        new_lines.append(lines[k])
                    for cap in captions_to_extract:
                        new_lines.append(cap)
                    captions_to_extract = []
                    i = out_end + 1
                    continue
                else:
                    for cap in captions_to_extract:
                        new_lines.append(cap)
                    captions_to_extract = []
            i += 1
            continue

        new_lines.append(line)
        i += 1

    return '\n'.join(new_lines), fixes


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix captions inside pre first
    content, fixes_inside = fix_captions_inside_pre(content)

    # Fix captions before pre
    content, fixes_before = fix_captions_before_pre(content)

    # Second pass in case there were nested issues
    content, fixes_before2 = fix_captions_before_pre(content)
    fixes_before += fixes_before2

    total_fixes = fixes_inside + fixes_before

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return total_fixes, fixes_inside, fixes_before


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(base, '**/section-*.html'), recursive=True))

    total_files_fixed = 0
    total_captions_moved = 0

    for filepath in files:
        rel = os.path.relpath(filepath, base)
        fixes, inside, before = process_file(filepath)
        if fixes > 0:
            total_files_fixed += 1
            total_captions_moved += fixes
            print(f"  Fixed {rel}: {before} before-pre, {inside} inside-pre ({fixes} total)")

    print(f"\nSummary: Fixed {total_captions_moved} captions across {total_files_fixed} files (out of {len(files)} scanned)")


if __name__ == '__main__':
    main()
