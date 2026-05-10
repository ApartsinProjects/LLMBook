#!/usr/bin/env python3
"""
fix_code_captions_v3.py

Comprehensive fix for the "double code block, single caption" issue.
Works directly on file content using regex, not line numbers from a report.

Strategy for each consecutive pair (block1, block2, shared_caption):
  1. System/user template pairs (appendix-i): intentional, skip
  2. Insert caption after block1 (move or generate), keep/update caption after block2
"""

import glob
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

patterns = [
    os.path.join(BASE, "part-*", "module-*", "section-*.html"),
    os.path.join(BASE, "appendices", "appendix-*", "section-*.html"),
]

html_files = []
for p in patterns:
    html_files.extend(sorted(glob.glob(p)))

print(f"Scanning {len(html_files)} files...")

# Track changes
fixes = []
skips = []


def is_template_pair(b1, b2):
    """System/user template pair from appendix-i."""
    b1l = b1.lower()
    b2l = b2.lower()
    return ("system template" in b1l or "system message" in b1l) and \
           ("user template" in b2l or "user message" in b2l)


def first_comment(text):
    """Extract first comment line from code text."""
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("#") and not s.startswith("#!"):
            desc = s.lstrip("#").strip()
            if desc:
                return desc
        if s.startswith("//"):
            desc = s.lstrip("/").strip()
            if desc:
                return desc
    return None


def caption_label(caption_html):
    """Extract 'Code Fragment X.Y.Z' from caption div."""
    m = re.search(r'<strong>((?:Code Fragment|Pseudocode)\s+[\w\.]+)\s*:?</strong>', caption_html)
    if m:
        return m.group(1)
    return None


def increment_label(label):
    """Code Fragment 6.6.1 -> Code Fragment 6.6.2"""
    m = re.match(r'((?:Code Fragment|Pseudocode)\s+[\w\.]+\.)(\d+)$', label)
    if m:
        return f"{m.group(1)}{int(m.group(2)) + 1}"
    # Try without trailing dot: "Code Fragment A.1.1" -> split at last digit group
    m = re.match(r'((?:Code Fragment|Pseudocode)\s+.+?)(\d+)$', label)
    if m:
        return f"{m.group(1)}{int(m.group(2)) + 1}"
    return None


def make_caption(label, description):
    """Create a caption div."""
    if not description.endswith("."):
        description += "."
    # Capitalize first letter
    description = description[0].upper() + description[1:]
    return f'<div class="code-caption"><strong>{label}:</strong> {description}</div>'


def has_algo_keywords(text):
    """Check if block contains algo-line-keyword spans (pseudocode)."""
    return "algo-line-keyword" in text


# Pattern to find consecutive code blocks sharing a caption
pat = re.compile(
    r'(</code>\s*</pre>)'        # end of block1
    r'(\s*)'                       # gap (must not contain code-caption)
    r'(<pre[^>]*>\s*<code[^>]*>)' # start of block2
    r'(.*?)'                       # block2 content
    r'(</code>\s*</pre>)'         # end of block2
    r'(\s*)'                       # gap
    r'(<div\s+class="code-caption"[^>]*>.*?</div>)',  # shared caption
    re.DOTALL
)


for fpath in html_files:
    with open(fpath, encoding="utf-8", errors="replace") as f:
        content = f.read()

    relpath = os.path.relpath(fpath, BASE)
    original = content  # track if we changed anything

    # Find all matches. Process from END to START to preserve positions.
    matches = list(pat.finditer(content))
    # Filter: no caption in the gap
    matches = [m for m in matches if 'code-caption' not in m.group(2)]

    if not matches:
        continue

    # Process from last to first
    for m in reversed(matches):
        block2_text = m.group(4)
        caption_html = m.group(7)
        label = caption_label(caption_html)

        # Find block1 content by searching backwards for its opening tag
        search_area = content[:m.start(1)]
        open_matches = list(re.finditer(r'<pre[^>]*>\s*<code[^>]*>(.*)', search_area, re.DOTALL))
        if not open_matches:
            skips.append((relpath, "Could not find block1 opening tag"))
            continue
        block1_open = open_matches[-1]
        block1_text = block1_open.group(1)

        # Strategy 1: System/user template pairs (skip)
        if is_template_pair(block1_text, block2_text):
            skips.append((relpath, f"System/user template pair ({label})"))
            continue

        # Determine what caption to insert after block1
        # Check preceding prose for a caption reference
        pre_area = content[max(0, block1_open.start() - 2000):block1_open.start()]
        prose_refs = re.findall(r'((?:Code Fragment|Pseudocode)\s+[\w\.]+)', pre_area)

        new_label = None
        new_desc = None

        if label:
            # Check if the caption text describes block1 (by matching block1's first comment)
            b1_comment = first_comment(block1_text)
            caption_plain = re.sub(r'<[^>]+>', '', caption_html).lower()

            b1_is_algo = has_algo_keywords(block1_text)
            b2_is_algo = has_algo_keywords(block2_text)

            if b1_comment and b1_comment.lower()[:30] in caption_plain:
                # Caption describes block1. Keep it there, need new caption for block2.
                # Move caption after block1, add new one after block2.
                b2_comment = first_comment(block2_text)
                next_label = increment_label(label)
                if next_label and b2_comment:
                    new_b2_caption = make_caption(next_label, b2_comment)
                elif next_label:
                    new_b2_caption = make_caption(next_label, "Continuation of the example above")
                else:
                    new_b2_caption = None

                # Reconstruct: insert caption after block1, keep original for block2 or add new
                end_block1 = m.start(1) + len(m.group(1))
                start_block2 = m.start(3)
                end_block2 = m.start(5) + len(m.group(5))
                end_caption = m.start(7) + len(m.group(7))

                gap1 = m.group(2)  # whitespace between block1 end and block2 start
                gap2 = m.group(6)  # whitespace between block2 end and caption

                # New content: block1_end + caption_after_b1 + gap + block2 + block2_end + new_b2_caption
                replacement = m.group(1)  # </code></pre>
                replacement += "\n" + caption_html  # caption after block1
                replacement += gap1
                replacement += m.group(3) + m.group(4) + m.group(5)  # block2
                if new_b2_caption:
                    replacement += "\n" + new_b2_caption
                else:
                    replacement += gap2 + caption_html  # duplicate if no new caption

                content = content[:m.start(1)] + replacement + content[end_caption:]
                fixes.append((relpath, f"Moved '{label}' after block1, added '{next_label}' after block2"))
                continue

            # Caption describes block2 or is generic. Block1 needs a caption.
            if prose_refs:
                candidate = prose_refs[-1]
                if candidate != label:
                    new_label = candidate
                    new_desc = b1_comment or "Code example"
                else:
                    # Same label as existing; the caption should be on block1
                    # This means block2 needs the incremented label
                    pass

            if not new_label:
                # Try to determine from block content
                if b1_is_algo and "Pseudocode" in label:
                    # Both pseudocode? First gets the caption, second needs new
                    b2_comment = first_comment(block2_text)
                    next_label = increment_label(label)
                    if next_label:
                        new_b2_caption = make_caption(next_label, b2_comment or "Continuation of the algorithm")
                        end_block1 = m.start(1) + len(m.group(1))
                        end_caption = m.start(7) + len(m.group(7))
                        replacement = m.group(1) + "\n" + caption_html
                        replacement += m.group(2) + m.group(3) + m.group(4) + m.group(5)
                        replacement += "\n" + new_b2_caption
                        content = content[:m.start(1)] + replacement + content[end_caption:]
                        fixes.append((relpath, f"Split: '{label}' on block1, '{next_label}' on block2"))
                        continue

                if b1_is_algo and not b2_is_algo:
                    # Block1 is pseudo, block2 is code. Caption might be for either.
                    new_label = label  # give caption to block1 (pseudocode)
                    new_desc = b1_comment or "Algorithm pseudocode"
                elif not b1_is_algo and b2_is_algo:
                    new_label = label if "Code" in label else None
                    new_desc = b1_comment or "Code example"
                else:
                    # Both are code. First gets a new caption.
                    b1_comment_text = b1_comment or "Code example"
                    # Use the existing caption for the LAST block (typical pattern)
                    # Create a new one for block1
                    # If caption mentions block1's comment, swap
                    new_label = label
                    new_desc = b1_comment_text

        if new_label and new_desc:
            new_caption = make_caption(new_label, new_desc)
            # Insert after block1's closing </code></pre>
            insert_pos = m.start(1) + len(m.group(1))
            next_label_for_b2 = increment_label(new_label) if new_label == label else label
            b2_comment = first_comment(block2_text)

            if next_label_for_b2 and next_label_for_b2 != new_label:
                new_b2_caption = make_caption(next_label_for_b2, b2_comment or "Continuation")
            else:
                new_b2_caption = None

            end_caption = m.start(7) + len(m.group(7))

            replacement = m.group(1) + "\n" + new_caption
            replacement += m.group(2) + m.group(3) + m.group(4) + m.group(5)
            if new_b2_caption:
                replacement += "\n" + new_b2_caption
            else:
                replacement += m.group(6) + caption_html

            content = content[:m.start(1)] + replacement + content[end_caption:]
            fixes.append((relpath, f"Added '{new_label}' after block1, '{next_label_for_b2 or label}' after block2"))
            continue

        # Fallback: could not determine fix
        skips.append((relpath, f"Could not determine fix for '{label}'"))

    if content != original:
        print(f"  WRITING {relpath} (len {len(original)} -> {len(content)})")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
    elif matches:
        print(f"  NO CHANGE for {relpath} despite {len(matches)} matches")


print(f"\n{'='*70}")
print(f"FIXES APPLIED: {len(fixes)}")
print(f"{'='*70}")
for f, d in fixes:
    print(f"  {f}: {d}")

print(f"\n{'='*70}")
print(f"SKIPPED: {len(skips)}")
print(f"{'='*70}")
for f, d in skips:
    print(f"  {f}: {d}")

print(f"\nTotal: {len(fixes)} fixed, {len(skips)} skipped.")
