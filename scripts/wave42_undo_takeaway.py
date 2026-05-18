"""Wave 42: revert files where the rename from "takeaway" to "key-takeaway"
created new failures. Those callouts were inline single-paragraph "Remember"
memory anchors. The semantically correct class is "key-insight", not
"key-takeaway" (which expects a bulleted recap list).

We change only the specific affected callouts: those that have a single <p>
body, no <ul>, and the title "Remember".
"""
import re
from pathlib import Path

REPO_ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

# Targets: files affected by the rename + retitle from "Remember" to "Key Insight: ..."
# We do this by replacing the callout class on blocks whose body is a single <p>.

CALLOUT_BLOCK = re.compile(
    r'(<div class="callout key-takeaway">\s*<div class="callout-title">[^<]+</div>\s*<p>)(.*?)(</p>\s*</div>)',
    re.DOTALL,
)

# Affected files (from grep): 18 originals + 2 we may have skipped.
# Just iterate all section-*.html and fix any single-<p> key-takeaway.

count_files = 0
count_blocks = 0
for fp in REPO_ROOT.rglob("section-*.html"):
    text = fp.read_text(encoding="utf-8")
    if 'class="callout key-takeaway"' not in text:
        continue
    new_text = text
    delta = 0
    for m in CALLOUT_BLOCK.finditer(text):
        body = m.group(2)
        # Skip if body contains a <ul> or <ol> (real takeaway list)
        if '<ul' in body or '<ol' in body:
            continue
        # Skip if there are multiple <p> tags
        if body.count('</p>') > 0:
            continue
        # This is a single-paragraph "memory anchor" takeaway.
        # Re-class as key-insight and rewrite the title.
        original = m.group(0)
        # Replace the class and title.
        new_block = original.replace(
            '<div class="callout key-takeaway">',
            '<div class="callout key-insight">',
            1,
        )
        # Rewrite the title: <div class="callout-title">Remember</div> -> Key Insight: Remember
        new_block = re.sub(
            r'<div class="callout-title">([^<]+)</div>',
            lambda mm: f'<div class="callout-title">Key Insight: {mm.group(1).strip()}</div>'
            if not mm.group(1).strip().lower().startswith("key insight")
            else mm.group(0),
            new_block,
            count=1,
        )
        new_text = new_text.replace(original, new_block, 1)
        delta += 1
    if delta:
        fp.write_text(new_text, encoding="utf-8")
        count_files += 1
        count_blocks += delta
        print(f"  {fp.relative_to(REPO_ROOT)}: {delta} block(s)")

print(f"\nFixed {count_blocks} block(s) in {count_files} files")
