"""
Move epigraph and prerequisites blocks that appear OUTSIDE the content wrapper
to INSIDE the content wrapper as the first children.

Handles both <main class="content"> and <div class="content"> wrappers.
"""

import re
import glob
import os

os.chdir(r"E:\Projects\LLMCourse")

files = sorted(glob.glob("part-*/module-*/section-*.html") + glob.glob("part-*/module-*/index.html"))

fixed = []
skipped_no_wrapper = []

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the content wrapper opening tag
    wrapper_match = re.search(r'<main\s+class="content">', content) or re.search(r'<div\s+class="content">', content)

    if not wrapper_match:
        skipped_no_wrapper.append(filepath)
        continue

    wrapper_start = wrapper_match.start()
    wrapper_tag = wrapper_match.group()

    # Find epigraph block before wrapper
    epigraph_before = None
    epigraph_match = re.search(r'<blockquote\s+class="epigraph">.*?</blockquote>', content[:wrapper_start], re.DOTALL)
    if epigraph_match:
        epigraph_before = epigraph_match.group()

    # Find prerequisites block before wrapper
    prereq_before = None
    prereq_match = re.search(r'<div\s+class="prerequisites">.*?</div>', content[:wrapper_start], re.DOTALL)
    if prereq_match:
        prereq_before = prereq_match.group()

    if not epigraph_before and not prereq_before:
        continue

    # Remove the blocks from before the wrapper
    new_content = content
    if epigraph_before:
        # Remove the epigraph and surrounding whitespace
        new_content = new_content.replace(epigraph_before, "", 1)
    if prereq_before:
        new_content = new_content.replace(prereq_before, "", 1)

    # Clean up extra blank lines between </header> and wrapper tag
    # Find the region between </header> and the wrapper tag, collapse to just two newlines
    new_content = re.sub(r'(</header>)\s*(' + re.escape(wrapper_tag) + r')', r'\1\n\n\2', new_content)

    # Build the insertion block (right after wrapper opening tag)
    insert_parts = []
    if epigraph_before:
        # Re-indent to 4 spaces (should already be, but ensure consistency)
        insert_parts.append("\n" + epigraph_before)
    if prereq_before:
        insert_parts.append("\n" + prereq_before)

    insertion = "".join(insert_parts) + "\n"

    # Insert after the wrapper opening tag
    new_content = new_content.replace(wrapper_tag, wrapper_tag + insertion, 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    parts = []
    if epigraph_before:
        parts.append("epigraph")
    if prereq_before:
        parts.append("prerequisites")
    fixed.append((filepath, parts))

print(f"Fixed {len(fixed)} files:")
for filepath, parts in fixed:
    print(f"  {filepath}: moved {', '.join(parts)}")

if skipped_no_wrapper:
    print(f"\nFiles with no content wrapper: {len(skipped_no_wrapper)}")
    for f in skipped_no_wrapper:
        print(f"  {f}")
else:
    print("\nAll files have a content wrapper.")
