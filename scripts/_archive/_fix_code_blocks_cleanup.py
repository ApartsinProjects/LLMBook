"""
Cleanup script: remove duplicate code-caption divs.
When a caption exists BOTH before and after a <pre> block, remove the one after.
Also fix numbering (ensure sequential 1,2,3... per file).
"""

import re
import os
import glob

files = sorted(
    glob.glob("E:/Projects/LLMCourse/part-1-foundations/module-*/section-*.html") +
    glob.glob("E:/Projects/LLMCourse/part-2-understanding-llms/module-*/section-*.html")
)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Strategy: find all <pre>...</pre> blocks and check for duplicate captions
    pre_pattern = re.compile(r'<pre[^>]*>.*?</pre>', re.DOTALL)
    matches = list(pre_pattern.finditer(content))

    if not matches:
        return 0

    duplicates_removed = 0

    # Process in reverse to preserve positions
    for match in reversed(matches):
        pre_start = match.start()
        pre_end = match.end()

        # Check for caption BEFORE <pre>
        before_zone = content[max(0, pre_start - 500):pre_start]
        cap_before = re.search(r'<div class="code-caption">.*?</div>\s*$', before_zone, re.DOTALL)

        # Check for caption AFTER </pre>
        after_zone = content[pre_end:pre_end + 500]
        cap_after = re.match(r'\s*<div class="code-caption">.*?</div>', after_zone, re.DOTALL)

        # If both exist, remove the one AFTER
        if cap_before and cap_after:
            after_start = pre_end + cap_after.start()
            after_end = pre_end + cap_after.end()
            content = content[:after_start] + content[after_end:]
            duplicates_removed += 1

    # Now renumber all Code Fragment labels sequentially
    fragment_counter = [0]
    def renumber(m):
        fragment_counter[0] += 1
        return f'<strong>Code Fragment {fragment_counter[0]}:</strong>'

    content = re.sub(r'<strong>Code Fragment \d+:</strong>', renumber, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return duplicates_removed

total_removed = 0
for filepath in files:
    short = os.path.relpath(filepath, "E:/Projects/LLMCourse")
    removed = process_file(filepath)
    if removed > 0:
        print(f"{short}: removed {removed} duplicate caption(s)")
        total_removed += removed

print(f"\nTotal duplicates removed: {total_removed}")
