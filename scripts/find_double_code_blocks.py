"""
Find HTML files where two consecutive <pre><code> blocks share a single
<div class="code-caption"> instead of each having their own caption.

Scans:
  part-*/module-*/section-*.html
  appendices/appendix-*/section-*.html

Reports:
  1. Two consecutive </code></pre> followed by one <div class="code-caption">
  2. Two <pre> blocks between two consecutive <div class="code-caption"> elements
  3. (Verification) A <div class="code-caption"> correctly between two <pre> blocks
"""

import glob
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

patterns = [
    os.path.join(BASE, "part-*", "module-*", "section-*.html"),
    os.path.join(BASE, "appendices", "appendix-*", "section-*.html"),
]

html_files = []
for p in patterns:
    html_files.extend(sorted(glob.glob(p)))

print(f"Scanning {len(html_files)} HTML files...\n")


def line_number_at(text, pos):
    """Return 1-based line number for a character position."""
    return text.count("\n", 0, pos) + 1


def first_lines(block, n=3):
    """Return the first n non-empty lines of a code block, stripped."""
    lines = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped:
            lines.append(stripped)
        if len(lines) >= n:
            break
    return "\n    ".join(lines) if lines else "(empty)"


def extract_caption_text(tag_html):
    """Pull visible text from a code-caption div."""
    text = re.sub(r"<[^>]+>", "", tag_html).strip()
    return text[:120] if text else "(empty)"


# Collect all findings
findings_shared = []   # Two code blocks sharing one caption
findings_missing = []  # Two <pre> blocks between two captions (missing caption)
findings_correct = []  # Caption correctly between two <pre> blocks

for fpath in html_files:
    with open(fpath, encoding="utf-8", errors="replace") as f:
        content = f.read()

    relpath = os.path.relpath(fpath, BASE)

    # ---- Strategy 1: find </code></pre> ... </code></pre> ... <div class="code-caption">
    # allowing optional whitespace/newlines between them, but NO caption div in between
    pat1 = re.compile(
        r'(</code>\s*</pre>)'        # end of first code block
        r'(\s*)'                       # whitespace gap
        r'(<pre[^>]*>\s*<code[^>]*>)'  # start of second code block
        r'(.*?)'                       # second block content
        r'(</code>\s*</pre>)'         # end of second code block
        r'(\s*)'                       # whitespace gap
        r'(<div\s+class="code-caption"[^>]*>.*?</div>)',  # single caption
        re.DOTALL
    )

    for m in pat1.finditer(content):
        # Make sure there is no caption between the two code blocks
        gap = m.group(2)
        if 'code-caption' in gap:
            continue

        line_end1 = line_number_at(content, m.start(1))
        line_start2 = line_number_at(content, m.start(3))
        line_end2 = line_number_at(content, m.start(5))
        line_caption = line_number_at(content, m.start(7))
        caption_text = extract_caption_text(m.group(7))

        # Get the second block content preview
        block2_preview = first_lines(m.group(4))

        # Now find the first block content: search backwards from match start
        # Find the <pre><code> that opened the first block
        search_area = content[:m.start(1)]
        open_match = list(re.finditer(r'<pre[^>]*>\s*<code[^>]*>(.*)', search_area, re.DOTALL))
        if open_match:
            last_open = open_match[-1]
            block1_content = last_open.group(1)
            line_start1 = line_number_at(content, last_open.start())
            block1_preview = first_lines(block1_content)
        else:
            line_start1 = "?"
            block1_preview = "(could not locate opening tag)"

        findings_shared.append({
            "file": relpath,
            "line_block1_start": line_start1,
            "line_block1_end": line_end1,
            "line_block2_start": line_start2,
            "line_block2_end": line_end2,
            "line_caption": line_caption,
            "caption": caption_text,
            "block1_preview": block1_preview,
            "block2_preview": block2_preview,
        })

    # ---- Strategy 2: find all <pre> and <div class="code-caption"> positions
    pre_opens = [(m.start(), m.end(), m.group()) for m in re.finditer(r'<pre[^>]*>\s*<code[^>]*>', content)]
    pre_closes = [(m.start(), m.end()) for m in re.finditer(r'</code>\s*</pre>', content)]
    captions = [(m.start(), m.end(), m.group()) for m in re.finditer(r'<div\s+class="code-caption"[^>]*>.*?</div>', content, re.DOTALL)]

    # For each pair of consecutive captions, count how many <pre> opens fall between them
    for i in range(len(captions) - 1):
        cap1_end = captions[i][1]
        cap2_start = captions[i + 1][0]
        pres_between = [p for p in pre_opens if cap1_end <= p[0] <= cap2_start]
        if len(pres_between) >= 2:
            line_cap1 = line_number_at(content, captions[i][0])
            line_cap2 = line_number_at(content, captions[i + 1][0])
            cap2_text = extract_caption_text(captions[i + 1][2])

            pre_lines = []
            for p in pres_between:
                pre_lines.append(line_number_at(content, p[0]))

            # Check if this is already captured by Strategy 1
            # (avoid double reporting for the same issue)
            already_found = False
            for f in findings_shared:
                if f["file"] == relpath and f["line_caption"] == line_cap2:
                    already_found = True
                    break

            if not already_found:
                findings_missing.append({
                    "file": relpath,
                    "caption1_line": line_cap1,
                    "caption2_line": line_cap2,
                    "caption2_text": cap2_text,
                    "pre_count": len(pres_between),
                    "pre_lines": pre_lines,
                })

    # ---- Strategy 3 (verification): caption correctly placed between two <pre> blocks
    for i in range(len(captions)):
        cap_start = captions[i][0]
        cap_end = captions[i][1]

        # Find the closest </code></pre> before this caption
        close_before = [c for c in pre_closes if c[1] <= cap_start]
        # Find the closest <pre><code> after this caption
        open_after = [o for o in pre_opens if o[0] >= cap_end]

        if close_before and open_after:
            last_close = close_before[-1]
            next_open = open_after[0]

            # Check nothing else interesting between them
            between_before = content[last_close[1]:cap_start].strip()
            between_after = content[cap_end:next_open[0]].strip()

            # If there is minimal content between, this is a caption sandwiched between code blocks
            if len(between_before) < 50 and len(between_after) < 50:
                findings_correct.append({
                    "file": relpath,
                    "caption_line": line_number_at(content, cap_start),
                    "caption_text": extract_caption_text(captions[i][2]),
                })


# ---- Output ----
out_lines = []


def emit(msg=""):
    print(msg)
    out_lines.append(msg)


emit("=" * 80)
emit("DOUBLE CODE BLOCK REPORT")
emit("=" * 80)

emit(f"\nScanned {len(html_files)} files.\n")

emit("-" * 80)
emit("ISSUE TYPE 1: Two consecutive code blocks sharing a single caption")
emit("-" * 80)
if findings_shared:
    for i, f in enumerate(findings_shared, 1):
        emit(f"\n  [{i}] {f['file']}")
        emit(f"      Block 1: lines {f['line_block1_start']}-{f['line_block1_end']}")
        emit(f"        Preview: {f['block1_preview']}")
        emit(f"      Block 2: lines {f['line_block2_start']}-{f['line_block2_end']}")
        emit(f"        Preview: {f['block2_preview']}")
        emit(f"      Shared caption (line {f['line_caption']}): {f['caption']}")
else:
    emit("\n  (none found)")

emit("")
emit("-" * 80)
emit("ISSUE TYPE 2: Multiple <pre> blocks between consecutive captions (missing caption)")
emit("-" * 80)
if findings_missing:
    for i, f in enumerate(findings_missing, 1):
        emit(f"\n  [{i}] {f['file']}")
        emit(f"      Between caption at line {f['caption1_line']} and caption at line {f['caption2_line']}")
        emit(f"      Found {f['pre_count']} <pre> blocks at lines: {f['pre_lines']}")
        emit(f"      Second caption text: {f['caption2_text']}")
else:
    emit("\n  (none found)")

emit("")
emit("-" * 80)
emit("VERIFICATION: Captions correctly placed between two code blocks")
emit("-" * 80)
if findings_correct:
    emit(f"\n  Found {len(findings_correct)} correctly placed captions.")
    for i, f in enumerate(findings_correct, 1):
        emit(f"    [{i}] {f['file']} line {f['caption_line']}: {f['caption_text']}")
else:
    emit("\n  (none found)")

emit("")
emit("=" * 80)
emit(f"SUMMARY: {len(findings_shared)} shared-caption issues, "
     f"{len(findings_missing)} missing-caption issues, "
     f"{len(findings_correct)} correctly placed captions verified.")
emit("=" * 80)

# Save report
report_path = os.path.join(BASE, "scripts", "double_code_blocks_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines) + "\n")

print(f"\nReport saved to: {report_path}")
