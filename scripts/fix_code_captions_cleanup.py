#!/usr/bin/env python3
"""
fix_code_captions_cleanup.py

1. Remove orphaned captions (code-caption divs not immediately after </code></pre>)
   that were incorrectly placed by earlier fix scripts.
2. Fix remaining multi-block issues by running the v3 fix iteratively
   until no more shared-caption pairs are found.
"""

import glob
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

patterns_glob = [
    os.path.join(BASE, "part-*", "module-*", "section-*.html"),
    os.path.join(BASE, "appendices", "appendix-*", "section-*.html"),
]

html_files = []
for p in patterns_glob:
    html_files.extend(sorted(glob.glob(p)))

# ============================================================
# STEP 1: Remove orphaned captions from pass 1/2
# An orphaned caption is a <div class="code-caption"> that is NOT
# immediately preceded by </code></pre> (with only whitespace between).
# ============================================================

print("=" * 70)
print("STEP 1: Remove orphaned captions")
print("=" * 70)

orphan_count = 0

for fpath in html_files:
    with open(fpath, encoding="utf-8") as f:
        lines = f.readlines()

    relpath = os.path.relpath(fpath, BASE)
    changed = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Is this a code-caption line?
        if stripped.startswith('<div class="code-caption">') and stripped.endswith('</div>'):
            # Check if the preceding non-blank line is </code></pre>
            prev_content = ""
            for j in range(len(new_lines) - 1, -1, -1):
                if new_lines[j].strip():
                    prev_content = new_lines[j].strip()
                    break

            if prev_content.endswith("</code></pre>") or prev_content.endswith("</pre>"):
                # Properly placed, keep it
                new_lines.append(line)
            else:
                # Orphaned caption. Check if this exact caption text already exists
                # adjacent to a code block elsewhere in the file.
                caption_strong = re.search(r'<strong>([^<]+)</strong>', stripped)
                if caption_strong:
                    label = caption_strong.group(1).rstrip(":")
                    # Check if this label already appears in a properly-placed caption
                    full_text = "".join(lines)
                    # Pattern: </code></pre> followed by whitespace then this caption
                    proper_pat = re.compile(
                        r'</code>\s*</pre>\s*<div class="code-caption"><strong>'
                        + re.escape(label)
                    )
                    if proper_pat.search(full_text):
                        # Duplicate orphan, remove it
                        print(f"  REMOVED orphan: {relpath}: {label}")
                        orphan_count += 1
                        changed = True
                        i += 1
                        continue
                    else:
                        # Not a duplicate, but misplaced. Keep it for now.
                        new_lines.append(line)
                else:
                    new_lines.append(line)
        else:
            new_lines.append(line)
        i += 1

    if changed:
        with open(fpath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

print(f"\nRemoved {orphan_count} orphaned captions.\n")

# ============================================================
# STEP 2: Iteratively fix remaining shared-caption pairs
# ============================================================

print("=" * 70)
print("STEP 2: Fix remaining shared-caption pairs (iterative)")
print("=" * 70)


def first_comment(text):
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


def caption_label(html):
    m = re.search(r'<strong>((?:Code Fragment|Pseudocode)\s+[\w\.]+)\s*:?</strong>', html)
    return m.group(1) if m else None


def increment_label(label):
    m = re.match(r'((?:Code Fragment|Pseudocode)\s+.+?)(\d+)$', label)
    if m:
        return f"{m.group(1)}{int(m.group(2)) + 1}"
    return None


def make_caption(label, desc):
    if not desc.endswith("."):
        desc += "."
    desc = desc[0].upper() + desc[1:]
    return f'<div class="code-caption"><strong>{label}:</strong> {desc}</div>'


def is_template_pair(b1, b2):
    b1l = b1.lower()
    b2l = b2.lower()
    return ("system template" in b1l or "system message" in b1l) and \
           ("user template" in b2l or "user message" in b2l)


pat = re.compile(
    r'(</code>\s*</pre>)'
    r'(\s*)'
    r'(<pre[^>]*>\s*<code[^>]*>)'
    r'(.*?)'
    r'(</code>\s*</pre>)'
    r'(\s*)'
    r'(<div\s+class="code-caption"[^>]*>.*?</div>)',
    re.DOTALL
)

total_fixes = 0
iteration = 0
MAX_ITERATIONS = 5

while iteration < MAX_ITERATIONS:
    iteration += 1
    round_fixes = 0
    print(f"\n  Iteration {iteration}:")

    for fpath in html_files:
        with open(fpath, encoding="utf-8", errors="replace") as f:
            content = f.read()

        relpath = os.path.relpath(fpath, BASE)
        original = content

        matches = list(pat.finditer(content))
        matches = [m for m in matches if 'code-caption' not in m.group(2)]

        if not matches:
            continue

        # Process last match only (to avoid position corruption)
        m = matches[-1]

        block2_text = m.group(4)
        caption_html = m.group(7)
        label = caption_label(caption_html)

        # Find block1 text
        search_area = content[:m.start(1)]
        open_matches = list(re.finditer(r'<pre[^>]*>\s*<code[^>]*>(.*)', search_area, re.DOTALL))
        if not open_matches:
            continue
        block1_text = open_matches[-1].group(1)

        # Skip template pairs
        if is_template_pair(block1_text, block2_text):
            continue

        b1_comment = first_comment(block1_text)
        b2_comment = first_comment(block2_text)
        caption_plain = re.sub(r'<[^>]+>', '', caption_html).lower()

        # Determine if caption describes block1
        b1_matches_caption = b1_comment and b1_comment.lower()[:30] in caption_plain

        if b1_matches_caption and label:
            # Caption belongs to block1. Create new caption for block2.
            next_label = increment_label(label)
            new_b2_caption = make_caption(next_label or (label + "b"), b2_comment or "Continuation of the example above")

            end_caption = m.start(7) + len(m.group(7))
            replacement = m.group(1) + "\n" + caption_html
            replacement += m.group(2) + m.group(3) + m.group(4) + m.group(5)
            replacement += "\n" + new_b2_caption

            content = content[:m.start(1)] + replacement + content[end_caption:]
        elif label:
            # Caption likely belongs to block2 or is generic. Add caption for block1.
            new_b1_caption = make_caption(label, b1_comment or "Code example")
            next_label = increment_label(label)
            new_b2_caption = make_caption(next_label or (label + "b"), b2_comment or "Continuation")

            end_caption = m.start(7) + len(m.group(7))
            replacement = m.group(1) + "\n" + new_b1_caption
            replacement += m.group(2) + m.group(3) + m.group(4) + m.group(5)
            replacement += "\n" + new_b2_caption

            content = content[:m.start(1)] + replacement + content[end_caption:]
        else:
            continue

        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            round_fixes += 1
            total_fixes += 1
            print(f"    Fixed: {relpath} ({label})")

    if round_fixes == 0:
        print("    No more fixes needed.")
        break

print(f"\nTotal fixes in step 2: {total_fixes}")

# ============================================================
# STEP 3: Handle Type 2 issues (missing captions between pairs)
# ============================================================
print(f"\n{'='*70}")
print("STEP 3: Check Type 2 issues (missing captions)")
print("=" * 70)

# Type 2: two <pre> blocks between consecutive captions
# The first <pre> block is usually a pip install (lab setup).
# Check and skip those, flag the rest.

type2_manual = []
type2_skipped = 0

for fpath in html_files:
    with open(fpath, encoding="utf-8") as f:
        content = f.read()

    relpath = os.path.relpath(fpath, BASE)

    pre_opens = [(m.start(), m.group()) for m in re.finditer(r'<pre[^>]*>\s*<code[^>]*>', content)]
    captions = [(m.start(), m.end(), m.group()) for m in re.finditer(r'<div\s+class="code-caption"[^>]*>.*?</div>', content, re.DOTALL)]

    for i in range(len(captions) - 1):
        cap1_end = captions[i][1]
        cap2_start = captions[i + 1][0]

        pre_between = [p for p in pre_opens if cap1_end < p[0] < cap2_start]
        if len(pre_between) >= 2:
            # Check if first block is a setup block
            first_pre_pos = pre_between[0][0]
            # Extract content of first pre block
            block_match = re.search(r'<pre[^>]*>\s*<code[^>]*>(.*?)</code>\s*</pre>', content[first_pre_pos:], re.DOTALL)
            if block_match:
                block_text = block_match.group(1).strip()
                if block_text.startswith("pip install") or block_text.startswith("conda install"):
                    if len(block_text.split("\n")) <= 3:
                        type2_skipped += 1
                        continue

            line_num = content[:first_pre_pos].count("\n") + 1
            type2_manual.append((relpath, line_num))

if type2_manual:
    print(f"\n  {len(type2_manual)} Type 2 issues remaining (need manual review):")
    for f, ln in type2_manual:
        print(f"    {f}:{ln}")
else:
    print("\n  No Type 2 issues remaining.")
print(f"  {type2_skipped} Type 2 issues skipped (setup/install blocks).")

print(f"\n{'='*70}")
print("DONE")
print("=" * 70)
