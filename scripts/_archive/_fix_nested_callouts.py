"""
Scan all HTML files for nested callouts and optionally fix them.
A nested callout is a <div class="callout ..."> inside another <div class="callout ...">.
Fix strategy: move the inner callout to be a sibling after the outer callout.
"""

import re
import glob
import sys
from html.parser import HTMLParser

GLOB_PATTERNS = [
    "part-*/module-*/**/*.html",
    "part-*/**/module-*/**/*.html",
    "appendices/**/*.html",
    "front-matter/**/*.html",
    "capstone/**/*.html",
]

CALLOUT_RE = re.compile(r'callout\s+\S+')


class CalloutNestFinder(HTMLParser):
    """Find nested callout divs in HTML content."""

    def __init__(self, filepath, content):
        super().__init__()
        self.filepath = filepath
        self.content = content
        self.lines = content.split('\n')
        # Stack of (tag, is_callout, callout_type, line)
        self.div_stack = []
        self.nested = []  # list of (line, outer_type, inner_type)

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            classes = ''
            for name, val in attrs:
                if name == 'class' and val:
                    classes = val
            is_callout = bool(CALLOUT_RE.search(classes))
            callout_type = ''
            if is_callout:
                # Extract the callout type (e.g. "fun-fact" from "callout fun-fact")
                m = re.search(r'callout\s+(\S+)', classes)
                if m:
                    callout_type = m.group(1)
                # Check if we are already inside a callout
                for item in self.div_stack:
                    if item[1]:  # parent is a callout
                        self.nested.append((
                            self.getpos()[0],
                            item[2],  # outer type
                            callout_type,  # inner type
                        ))
                        break
            self.div_stack.append((tag, is_callout, callout_type, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag == 'div' and self.div_stack:
            self.div_stack.pop()


def find_nested_callouts(filepath):
    """Return list of (line, outer_type, inner_type) for nested callouts."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    finder = CalloutNestFinder(filepath, content)
    try:
        finder.feed(content)
    except Exception as e:
        print(f"  Parse error in {filepath}: {e}")
    return finder.nested


def fix_nested_callouts_in_file(filepath):
    """
    Fix nested callouts by regex-based approach:
    Find the inner callout div (with all its content up to its matching </div>),
    remove it from inside the outer callout, and place it right after the outer
    callout's closing </div>.

    Returns number of fixes applied.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fixes = 0
    # We need to iteratively fix because positions shift after each fix
    max_iterations = 20
    for _ in range(max_iterations):
        # Find all callout div openings with their positions
        callout_opens = list(re.finditer(r'<div\s+class="[^"]*callout\s+\S+[^"]*"[^>]*>', content))
        if len(callout_opens) < 2:
            break

        found_nested = False
        for i, outer_match in enumerate(callout_opens):
            outer_start = outer_match.start()
            # Find the matching </div> for the outer callout
            outer_close = find_matching_close_div(content, outer_match.end())
            if outer_close is None:
                continue

            # Check if any other callout opening is inside this outer callout
            for inner_match in callout_opens[i+1:]:
                inner_start = inner_match.start()
                if inner_start > outer_close:
                    break  # past the outer callout
                if inner_start > outer_start and inner_start < outer_close:
                    # Found a nested callout
                    inner_close = find_matching_close_div(content, inner_match.end())
                    if inner_close is None:
                        continue
                    inner_close_end = inner_close + len('</div>')

                    # Extract the inner callout (with surrounding whitespace cleanup)
                    # Find the start of the line containing the inner callout
                    extract_start = inner_start
                    extract_end = inner_close_end

                    # Look back to find leading whitespace/newline
                    while extract_start > 0 and content[extract_start - 1] in ' \t':
                        extract_start -= 1
                    if extract_start > 0 and content[extract_start - 1] == '\n':
                        extract_start -= 1

                    # Look forward past trailing newline
                    if extract_end < len(content) and content[extract_end] == '\n':
                        extract_end += 1

                    inner_block = content[inner_start:inner_close_end]

                    # Remove the inner callout from inside the outer
                    content = content[:extract_start] + content[extract_end:]

                    # Recalculate outer_close position after removal
                    removed_len = extract_end - extract_start
                    outer_close_new = outer_close - removed_len
                    outer_close_end_new = outer_close_new + len('</div>')

                    # Find the end of the line with </div> for the outer callout
                    insert_pos = outer_close_end_new
                    if insert_pos < len(content) and content[insert_pos] == '\n':
                        insert_pos += 1

                    # Insert the inner callout after the outer callout
                    content = content[:insert_pos] + '\n' + inner_block + '\n' + content[insert_pos:]

                    fixes += 1
                    found_nested = True
                    break  # restart scanning since positions changed
            if found_nested:
                break

        if not found_nested:
            break

    if fixes > 0:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)

    return fixes


def find_matching_close_div(content, start_pos):
    """
    Starting after an opening <div ...> tag (at start_pos),
    find the position of its matching </div>.
    Returns the index of the '<' in </div>, or None.
    """
    depth = 1
    pos = start_pos
    open_re = re.compile(r'<div[\s>]')
    close_re = re.compile(r'</div\s*>')

    while depth > 0 and pos < len(content):
        next_open = open_re.search(content, pos)
        next_close = close_re.search(content, pos)

        if next_close is None:
            return None

        if next_open and next_open.start() < next_close.start():
            depth += 1
            pos = next_open.end()
        else:
            depth -= 1
            if depth == 0:
                return next_close.start()
            pos = next_close.end()

    return None


def collect_files():
    """Collect all HTML files matching the glob patterns."""
    files = set()
    for pattern in GLOB_PATTERNS:
        for f in glob.glob(pattern, recursive=True):
            files.add(f.replace('\\', '/'))
    return sorted(files)


def main():
    mode = 'scan'
    if len(sys.argv) > 1 and sys.argv[1] == '--fix':
        mode = 'fix'

    files = collect_files()
    print(f"Scanning {len(files)} HTML files for nested callouts...\n")

    total_nested = 0
    total_fixes = 0
    affected_files = []

    for filepath in files:
        nested = find_nested_callouts(filepath)
        if nested:
            affected_files.append(filepath)
            total_nested += len(nested)
            print(f"  {filepath}:")
            for line, outer, inner in nested:
                print(f"    Line ~{line}: [{inner}] nested inside [{outer}]")

            if mode == 'fix':
                fixes = fix_nested_callouts_in_file(filepath)
                total_fixes += fixes
                print(f"    => Fixed {fixes} nested callout(s)")

    print(f"\n{'='*60}")
    print(f"Total files scanned: {len(files)}")
    print(f"Files with nested callouts: {len(affected_files)}")
    print(f"Total nested callouts found: {total_nested}")
    if mode == 'fix':
        print(f"Total fixes applied: {total_fixes}")
    else:
        print(f"\nRun with --fix to auto-fix these issues.")


if __name__ == '__main__':
    main()
