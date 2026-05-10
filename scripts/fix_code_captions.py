#!/usr/bin/env python3
"""
fix_code_captions.py

Fixes "double code block, single caption" issues identified in double_code_blocks_report.txt.

Two issue types:
  Type 1 (shared caption): Two consecutive <pre><code> blocks share one trailing caption.
  Type 2 (missing caption): Two <pre> blocks between consecutive captions; one is missing.

Conservative approach:
  - Auto-fix only when caption numbering can be reliably determined
  - Wrap output blocks in <div class="code-output"> when appropriate
  - Report ambiguous cases for manual review
"""

import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(BASE_DIR, "scripts", "double_code_blocks_report.txt")

# Counters
auto_fixed = []
manual_review = []
skipped = []


def read_file(rel_path):
    """Read file content as list of lines (1-indexed access via lines[i-1])."""
    full = os.path.join(BASE_DIR, rel_path.replace("\\", "/"))
    with open(full, "r", encoding="utf-8") as f:
        return f.readlines()


def write_file(rel_path, lines):
    """Write list of lines back to file."""
    full = os.path.join(BASE_DIR, rel_path.replace("\\", "/"))
    with open(full, "w", encoding="utf-8") as f:
        f.writelines(lines)


def is_output_block(code_text):
    """
    Heuristic: does this code block look like program output rather than source code?
    Returns True if it looks like output.
    """
    stripped = code_text.strip()
    lines_list = stripped.split("\n")
    # If it contains import/def/class/from...import, it is code
    code_keywords = [
        "import ", "from ", "def ", "class ", "pip install", "sudo ",
        "conda ", "python -m", "async def", "source ", "#!", "#!/",
    ]
    for kw in code_keywords:
        if kw in stripped:
            return False
    # If it starts with comments, it is code
    first_nonblank = ""
    for ln in lines_list:
        if ln.strip():
            first_nonblank = ln.strip()
            break
    if first_nonblank.startswith("#") or first_nonblank.startswith("//"):
        return False
    # If most lines start with typical output patterns
    output_indicators = 0
    for ln in lines_list:
        s = ln.strip()
        if not s:
            continue
        # Lines like "Episode 200 | ..." or "key: value" or start with numbers
        if re.match(r'^(Episode|Step|Epoch|Loss|Accuracy|>>>|\.\.\.|\d+[\.\s])', s):
            output_indicators += 1
        # Lines that are mostly just printed values
        if re.match(r'^[\d\.\-\+\s,\[\]{}:]+$', s):
            output_indicators += 1
    if len(lines_list) > 0 and output_indicators >= len(lines_list) * 0.5:
        return True
    return False


def is_system_user_template_pair(block1_text, block2_text):
    """Check if these are system/user prompt template pairs (appendix-i pattern)."""
    return ("system template" in block1_text.lower() or "system message" in block1_text.lower()) and \
           ("user template" in block2_text.lower() or "user message" in block2_text.lower())


def is_algorithm_block(code_text):
    """Check if a code block is pseudocode (algo-line-keyword spans)."""
    return "algo-line-keyword" in code_text


def extract_code_block_text(lines, start_line):
    """Extract the text content of a <pre><code> block starting near start_line (1-indexed).
    Returns (text, end_line_1indexed)."""
    # Find the <pre><code opening
    idx = start_line - 1  # 0-indexed
    text_lines = []
    in_block = False
    for i in range(max(0, idx - 2), min(len(lines), idx + 300)):
        line = lines[i]
        if not in_block:
            if "<pre><code" in line:
                in_block = True
                # Get text after the tag on same line
                match = re.search(r'<pre><code[^>]*>(.*)', line, re.DOTALL)
                if match:
                    rest = match.group(1)
                    if "</code></pre>" in rest:
                        text_lines.append(rest.split("</code></pre>")[0])
                        return "\n".join(text_lines), i + 1
                    text_lines.append(rest)
        else:
            if "</code></pre>" in line:
                text_lines.append(line.split("</code></pre>")[0])
                return "\n".join(text_lines), i + 1
            text_lines.append(line)
    return "\n".join(text_lines), start_line


def find_pre_end(lines, start_line):
    """Find the line number (1-indexed) of </code></pre> for a block starting at start_line."""
    idx = start_line - 1
    for i in range(idx, min(len(lines), idx + 500)):
        if "</code></pre>" in lines[i]:
            return i + 1  # 1-indexed
    return start_line


def extract_caption_number_from_prose(lines, block_start_line):
    """
    Look at the preceding paragraph text (up to 20 lines before the block)
    to find a reference like "Code Fragment X.Y.Z" or "Pseudocode X.Y.Z".
    Returns the matched label string or None.
    """
    idx = block_start_line - 1  # 0-indexed
    search_start = max(0, idx - 25)
    text_chunk = "".join(lines[search_start:idx])
    # Look for "Code Fragment X.Y.Z" or "Pseudocode X.Y.Z" references
    matches = re.findall(
        r'((?:Code Fragment|Pseudocode)\s+[\w\.]+)',
        text_chunk
    )
    if matches:
        return matches[-1]  # Return the most recent reference
    return None


def increment_caption_number(label):
    """
    Given 'Code Fragment 6.6.1', try to produce 'Code Fragment 6.6.2'.
    Works for patterns like X.Y.Z where Z is a number.
    """
    match = re.match(r'((?:Code Fragment|Pseudocode)\s+)([\w\.]+\.?)(\d+)', label)
    if match:
        prefix = match.group(1)
        middle = match.group(2)
        num = int(match.group(3))
        return f"{prefix}{middle}{num + 1}"
    return None


def get_caption_label(caption_text):
    """Extract the label like 'Code Fragment 6.6.1' from caption HTML."""
    match = re.search(r'<strong>((?:Code Fragment|Pseudocode)\s+[\w\.]+\s*:?)</strong>', caption_text)
    if match:
        return match.group(1).rstrip(":")
    return None


def parse_report():
    """Parse the report file to extract issue entries."""
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    type1_section = content.split("ISSUE TYPE 1:")[1].split("ISSUE TYPE 2:")[0]
    type2_section = content.split("ISSUE TYPE 2:")[1].split("VERIFICATION:")[0]

    type1_issues = []
    type2_issues = []

    # Parse Type 1 issues
    entries = re.split(r'\n\s+\[\d+\]\s+', type1_section)
    for entry in entries[1:]:  # Skip first empty
        lines_entry = entry.strip().split("\n")
        filepath = lines_entry[0].strip()
        # Extract block line numbers
        b1_match = re.search(r'Block 1: lines (\d+)-(\d+)', entry)
        b2_match = re.search(r'Block 2: lines (\d+)-(\d+)', entry)
        cap_match = re.search(r'Shared caption \(line (\d+)\)', entry)
        if b1_match and b2_match and cap_match:
            type1_issues.append({
                "file": filepath,
                "block1_start": int(b1_match.group(1)),
                "block1_end": int(b1_match.group(2)),
                "block2_start": int(b2_match.group(1)),
                "block2_end": int(b2_match.group(2)),
                "caption_line": int(cap_match.group(1)),
            })

    # Parse Type 2 issues
    entries = re.split(r'\n\s+\[\d+\]\s+', type2_section)
    for entry in entries[1:]:
        lines_entry = entry.strip().split("\n")
        filepath = lines_entry[0].strip()
        cap1_match = re.search(r'caption at line (\d+) and caption at line (\d+)', entry)
        pre_match = re.search(r'<pre> blocks at lines: \[([^\]]+)\]', entry)
        cap2_text_match = re.search(r'Second caption text: (.+)', entry)
        if cap1_match and pre_match:
            pre_lines = [int(x.strip()) for x in pre_match.group(1).split(",")]
            type2_issues.append({
                "file": filepath,
                "caption1_line": int(cap1_match.group(1)),
                "caption2_line": int(cap1_match.group(2)),
                "pre_lines": pre_lines,
                "caption2_text": cap2_text_match.group(1).strip() if cap2_text_match else "",
            })

    return type1_issues, type2_issues


def fix_type1(issue):
    """
    Fix Type 1: two consecutive code blocks sharing a single caption.
    Strategy:
      - If system/user template pair (appendix-i): keep together, single caption is fine
        but the caption only describes the first. Add a second caption for the second.
      - If block1 is pseudocode and block2 is code: give pseudocode its own caption,
        the existing caption stays with block2 (or vice versa).
      - If block2 is output: wrap in code-output div.
      - Otherwise: check prose for a caption reference to assign.
    """
    filepath = issue["file"]
    lines = read_file(filepath)
    b1_start = issue["block1_start"]
    b2_start = issue["block2_start"]
    caption_line = issue["caption_line"]

    b1_text, b1_end = extract_code_block_text(lines, b1_start)
    b2_text, b2_end = extract_code_block_text(lines, b2_start)
    caption_html = lines[caption_line - 1].rstrip("\n")
    caption_label = get_caption_label(caption_html)

    # --- Strategy 1: System/User template pairs (appendix-i) ---
    if is_system_user_template_pair(b1_text, b2_text):
        # These are intentionally paired. The caption covers both.
        # No fix needed, skip.
        skipped.append((filepath, b1_start, "System/user template pair, caption covers both"))
        return

    # --- Strategy 2: Pseudocode + Code pair ---
    b1_is_algo = is_algorithm_block(b1_text)
    b2_is_algo = is_algorithm_block(b2_text)

    if b1_is_algo and not b2_is_algo:
        # The existing caption might describe the pseudocode.
        # The code block needs its own caption, or vice versa.
        # Check if the caption label mentions "Pseudocode"
        if caption_label and "Pseudocode" in caption_label:
            # Caption is for block1 (pseudocode). Block2 (code) needs a caption.
            # Find if prose references the code block
            prose_ref = extract_caption_number_from_prose(lines, b2_start)
            if prose_ref and "Code Fragment" in prose_ref:
                # Insert a caption after block2 with this reference, move pseudocode caption after block1
                b1_end_line = find_pre_end(lines, b1_start)
                # Insert caption after block1
                new_caption_b2 = f'<div class="code-caption"><strong>{prose_ref}:</strong> Production implementation corresponding to the pseudocode above.</div>\n'
                # Move existing caption after block1, add new one after block2
                # Actually: keep existing caption after block1, add new for block2
                # Remove existing caption from current position, insert after block1
                caption_idx = caption_line - 1
                removed_caption = lines.pop(caption_idx)
                # Insert after block1
                insert_idx = b1_end_line - 1 + 1  # after the </pre> line (0-indexed + 1)
                if insert_idx > caption_idx:
                    insert_idx -= 1  # adjust for removal
                lines.insert(insert_idx, removed_caption.rstrip("\n") + "\n")
                # Now add a new caption after block2
                # Recalculate b2 end since lines shifted
                b2_end_new = find_pre_end(lines, b2_start)
                lines.insert(b2_end_new, new_caption_b2)
                write_file(filepath, lines)
                auto_fixed.append((filepath, b1_start, f"Split: pseudocode caption after block1, new caption '{prose_ref}' after block2"))
                return
            else:
                # Move caption after block1, report block2 for manual review
                b1_end_line = find_pre_end(lines, b1_start)
                caption_idx = caption_line - 1
                removed_caption = lines.pop(caption_idx)
                insert_idx = b1_end_line  # after the </pre> line (0-indexed, line is at b1_end_line-1, so insert at b1_end_line)
                if insert_idx > caption_idx:
                    insert_idx -= 1
                lines.insert(insert_idx, removed_caption.rstrip("\n") + "\n")
                write_file(filepath, lines)
                auto_fixed.append((filepath, b1_start, f"Moved pseudocode caption after block1"))
                manual_review.append((filepath, b2_start, "Block2 (code) needs a caption added manually"))
                return
        elif caption_label and "Code Fragment" in caption_label:
            # Caption is for the code block (block2). Pseudocode (block1) needs its own caption.
            # Check prose for pseudocode reference
            prose_ref = extract_caption_number_from_prose(lines, b1_start)
            if prose_ref and "Pseudocode" in prose_ref:
                b1_end_line = find_pre_end(lines, b1_start)
                desc = extract_short_description(b1_text)
                new_caption = f'<div class="code-caption"><strong>{prose_ref}:</strong> {desc}</div>\n'
                lines.insert(b1_end_line, new_caption)
                write_file(filepath, lines)
                auto_fixed.append((filepath, b1_start, f"Added pseudocode caption '{prose_ref}' after block1"))
                return
            else:
                manual_review.append((filepath, b1_start, "Pseudocode block needs a caption (no prose reference found)"))
                return

    if not b1_is_algo and b2_is_algo:
        # Block2 is pseudocode, block1 is code. Less common.
        # Check if caption is for pseudocode or code
        if caption_label and "Pseudocode" in caption_label:
            # Caption for block2. Block1 needs caption.
            prose_ref = extract_caption_number_from_prose(lines, b1_start)
            if prose_ref:
                b1_end_line = find_pre_end(lines, b1_start)
                desc = extract_short_description(b1_text)
                new_caption = f'<div class="code-caption"><strong>{prose_ref}:</strong> {desc}</div>\n'
                lines.insert(b1_end_line, new_caption)
                write_file(filepath, lines)
                auto_fixed.append((filepath, b1_start, f"Added code caption '{prose_ref}' after block1"))
                return
            else:
                manual_review.append((filepath, b1_start, "Code block1 needs caption (no prose reference found)"))
                return

    # --- Strategy 3: Block2 looks like output ---
    if is_output_block(b2_text):
        # Wrap block2 in <div class="code-output">
        b2_start_idx = b2_start - 1  # 0-indexed
        b2_end_line = find_pre_end(lines, b2_start)
        b2_end_idx = b2_end_line - 1  # 0-indexed

        # Find the actual <pre> tag line
        pre_line_idx = b2_start_idx
        for i in range(max(0, b2_start_idx - 2), b2_start_idx + 2):
            if "<pre>" in lines[i] or "<pre><code" in lines[i]:
                pre_line_idx = i
                break

        # Extract just the text content (strip pre/code tags)
        block_content = []
        in_block = False
        for i in range(pre_line_idx, b2_end_idx + 1):
            block_content.append(lines[i])

        # Replace the pre/code block with a code-output div
        raw_text = "".join(block_content)
        # Extract inner text
        inner = re.search(r'<pre><code[^>]*>(.*?)</code></pre>', raw_text, re.DOTALL)
        if inner:
            output_text = inner.group(1).strip()
            replacement = f'<div class="code-output">{output_text}</div>\n'
            lines[pre_line_idx:b2_end_idx + 1] = [replacement]
            write_file(filepath, lines)
            auto_fixed.append((filepath, b2_start, "Wrapped block2 in <div class='code-output'>"))
            return

    # --- Strategy 4: Two genuine code blocks, check prose for references ---
    # The existing caption is at the end. It likely belongs to block2 (last one).
    # Check if prose before block1 references a caption number.
    prose_ref = extract_caption_number_from_prose(lines, b1_start)

    if prose_ref and caption_label:
        # Check they are different
        if prose_ref != caption_label:
            b1_end_line = find_pre_end(lines, b1_start)
            desc = extract_short_description(b1_text)
            new_caption = f'<div class="code-caption"><strong>{prose_ref}:</strong> {desc}</div>\n'
            lines.insert(b1_end_line, new_caption)
            write_file(filepath, lines)
            auto_fixed.append((filepath, b1_start, f"Added caption '{prose_ref}' after block1"))
            return
        else:
            # Same reference; the caption actually belongs to block1
            # Move it after block1, block2 needs manual caption
            b1_end_line = find_pre_end(lines, b1_start)
            caption_idx = caption_line - 1
            removed = lines.pop(caption_idx)
            insert_idx = b1_end_line
            if insert_idx > caption_idx:
                insert_idx -= 1
            lines.insert(insert_idx, removed)
            write_file(filepath, lines)
            auto_fixed.append((filepath, b1_start, f"Moved caption '{caption_label}' after block1"))
            manual_review.append((filepath, b2_start, f"Block2 needs a new caption after '{caption_label}'"))
            return

    # --- Strategy 5: Infer caption number from existing caption ---
    if caption_label:
        # Try to decrement the caption number to get block1's caption
        # e.g., if caption is "Code Fragment 6.6.2", block1 might be "Code Fragment 6.6.1"
        # But this is risky. Instead, try incrementing block1 reference.
        # Actually, the existing caption likely names block1 or block2.
        # Check if caption text describes block1 content
        caption_text_content = lines[caption_line - 1]
        b1_first_line = b1_text.strip().split("\n")[0] if b1_text.strip() else ""

        # If the caption text mentions something from block1 (first comment/line)
        b1_comment = ""
        for ln in b1_text.strip().split("\n"):
            if ln.strip().startswith("#"):
                b1_comment = ln.strip().lstrip("#").strip()
                break

        if b1_comment and b1_comment.lower() in caption_text_content.lower():
            # Caption belongs to block1. Move it after block1.
            b1_end_line = find_pre_end(lines, b1_start)
            caption_idx = caption_line - 1
            removed = lines.pop(caption_idx)
            insert_idx = b1_end_line
            if insert_idx > caption_idx:
                insert_idx -= 1
            lines.insert(insert_idx, removed)

            # Block2 needs a new caption. Try to create one.
            next_label = increment_caption_number(caption_label)
            if next_label:
                b2_desc = extract_short_description(b2_text)
                new_cap = f'<div class="code-caption"><strong>{next_label}:</strong> {b2_desc}</div>\n'
                # Recalculate b2 end
                b2_end_new = find_pre_end(lines, b2_start if b2_start <= insert_idx else b2_start + 1)
                lines.insert(b2_end_new, new_cap)
                write_file(filepath, lines)
                auto_fixed.append((filepath, b1_start, f"Moved '{caption_label}' to block1, added '{next_label}' for block2"))
                return
            else:
                write_file(filepath, lines)
                auto_fixed.append((filepath, b1_start, f"Moved '{caption_label}' after block1"))
                manual_review.append((filepath, b2_start, "Block2 needs a caption"))
                return

        b2_comment = ""
        for ln in b2_text.strip().split("\n"):
            if ln.strip().startswith("#"):
                b2_comment = ln.strip().lstrip("#").strip()
                break

        if b2_comment and b2_comment.lower() in caption_text_content.lower():
            # Caption belongs to block2. Block1 needs a new caption.
            prev_label = decrement_caption_number(caption_label)
            if prev_label:
                b1_end_line = find_pre_end(lines, b1_start)
                b1_desc = extract_short_description(b1_text)
                new_cap = f'<div class="code-caption"><strong>{prev_label}:</strong> {b1_desc}</div>\n'
                lines.insert(b1_end_line, new_cap)
                write_file(filepath, lines)
                auto_fixed.append((filepath, b1_start, f"Added '{prev_label}' for block1, existing caption stays for block2"))
                return

    # Fallback: report for manual review
    manual_review.append((filepath, b1_start,
                          f"Two code blocks share caption '{caption_label or 'unknown'}'. Could not determine fix automatically."))


def fix_type2(issue):
    """
    Fix Type 2: two <pre> blocks between consecutive captions (missing caption).
    The first code block after caption1 is usually missing its own caption.
    """
    filepath = issue["file"]
    lines = read_file(filepath)
    pre_lines = issue["pre_lines"]  # [line_of_first_pre, line_of_second_pre]
    caption1_line = issue["caption1_line"]
    caption2_line = issue["caption2_line"]

    if len(pre_lines) < 2:
        manual_review.append((filepath, pre_lines[0] if pre_lines else 0, "Type 2: unexpected number of pre blocks"))
        return

    first_pre = pre_lines[0]
    second_pre = pre_lines[1]

    b1_text, b1_end = extract_code_block_text(lines, first_pre)
    b2_text, b2_end = extract_code_block_text(lines, second_pre)

    # Check if first block is a setup/install block (pip install, short)
    b1_stripped = b1_text.strip()
    is_setup = b1_stripped.startswith("pip install") or b1_stripped.startswith("conda install")
    if is_setup and len(b1_stripped.split("\n")) <= 3:
        # Short setup block, typically does not need a caption
        skipped.append((filepath, first_pre, "Short setup/install block, no caption needed"))
        return

    # Check if first block is output
    if is_output_block(b1_text):
        # Wrap in code-output
        b1_start_idx = first_pre - 1
        b1_end_line = find_pre_end(lines, first_pre)
        b1_end_idx = b1_end_line - 1

        pre_line_idx = b1_start_idx
        for i in range(max(0, b1_start_idx - 2), min(len(lines), b1_start_idx + 2)):
            if "<pre>" in lines[i] or "<pre><code" in lines[i]:
                pre_line_idx = i
                break

        raw_text = "".join(lines[pre_line_idx:b1_end_idx + 1])
        inner = re.search(r'<pre><code[^>]*>(.*?)</code></pre>', raw_text, re.DOTALL)
        if inner:
            output_text = inner.group(1).strip()
            replacement = f'<div class="code-output">{output_text}</div>\n'
            lines[pre_line_idx:b1_end_idx + 1] = [replacement]
            write_file(filepath, lines)
            auto_fixed.append((filepath, first_pre, "Wrapped block1 in <div class='code-output'> (was output, not code)"))
            return

    # Check if first block has a caption reference in preceding prose
    prose_ref = extract_caption_number_from_prose(lines, first_pre)
    if prose_ref:
        b1_end_line = find_pre_end(lines, first_pre)
        desc = extract_short_description(b1_text)
        new_caption = f'<div class="code-caption"><strong>{prose_ref}:</strong> {desc}</div>\n'
        lines.insert(b1_end_line, new_caption)
        write_file(filepath, lines)
        auto_fixed.append((filepath, first_pre, f"Added missing caption '{prose_ref}' after block1"))
        return

    # Check if caption1 number can help us infer the missing caption number
    cap1_text = lines[caption1_line - 1]
    cap1_label = get_caption_label(cap1_text)
    cap2_text = lines[caption2_line - 1]
    cap2_label = get_caption_label(cap2_text)

    if cap1_label:
        next_label = increment_caption_number(cap1_label)
        if next_label and next_label != cap2_label:
            # The missing caption is likely the next number after caption1
            b1_end_line = find_pre_end(lines, first_pre)
            desc = extract_short_description(b1_text)
            new_caption = f'<div class="code-caption"><strong>{next_label}:</strong> {desc}</div>\n'
            lines.insert(b1_end_line, new_caption)
            write_file(filepath, lines)
            auto_fixed.append((filepath, first_pre, f"Added missing caption '{next_label}' (inferred from previous caption '{cap1_label}')"))
            return

    # Fallback
    manual_review.append((filepath, first_pre,
                          f"Type 2: missing caption between captions at lines {caption1_line} and {caption2_line}"))


def extract_short_description(code_text):
    """Extract a short description from the first comment line of a code block."""
    for line in code_text.strip().split("\n"):
        stripped = line.strip()
        # Skip algo-line-keyword lines
        if "algo-line-keyword" in stripped:
            continue
        if stripped.startswith("#"):
            desc = stripped.lstrip("#").strip()
            if desc:
                # Capitalize first letter, ensure ends with period
                desc = desc[0].upper() + desc[1:] if desc else desc
                if not desc.endswith("."):
                    desc += "."
                return desc
        if stripped.startswith("//"):
            desc = stripped.lstrip("/").strip()
            if desc:
                desc = desc[0].upper() + desc[1:] if desc else desc
                if not desc.endswith("."):
                    desc += "."
                return desc
    # If no comment, use the first meaningful line
    for line in code_text.strip().split("\n"):
        stripped = line.strip()
        if stripped and not stripped.startswith("<span"):
            # Truncate long lines
            if len(stripped) > 80:
                stripped = stripped[:77] + "..."
            return stripped + "."
    return "Code example."


def decrement_caption_number(label):
    """Given 'Code Fragment 6.6.2', produce 'Code Fragment 6.6.1'."""
    match = re.match(r'((?:Code Fragment|Pseudocode)\s+)([\w\.]+\.?)(\d+)', label)
    if match:
        prefix = match.group(1)
        middle = match.group(2)
        num = int(match.group(3))
        if num > 1:
            return f"{prefix}{middle}{num - 1}"
    return None


def main():
    print("=" * 70)
    print("FIX CODE CAPTIONS")
    print("=" * 70)
    print()

    type1_issues, type2_issues = parse_report()
    print(f"Parsed {len(type1_issues)} Type 1 issues and {len(type2_issues)} Type 2 issues.")
    print()

    # Process files in order, but handle each file's issues together
    # to avoid conflicts from line number shifts.
    # Group by file and process from bottom to top within each file.

    # Process Type 1 issues (process from last to first within each file)
    files_seen = set()
    type1_by_file = {}
    for issue in type1_issues:
        f = issue["file"]
        if f not in type1_by_file:
            type1_by_file[f] = []
        type1_by_file[f].append(issue)

    for f, issues in type1_by_file.items():
        # Process from bottom to top to avoid line shifts
        issues.sort(key=lambda x: x["block1_start"], reverse=True)
        for issue in issues:
            try:
                fix_type1(issue)
            except Exception as e:
                manual_review.append((issue["file"], issue["block1_start"],
                                      f"Error during fix: {e}"))

    # Process Type 2 issues
    type2_by_file = {}
    for issue in type2_issues:
        f = issue["file"]
        if f not in type2_by_file:
            type2_by_file[f] = []
        type2_by_file[f].append(issue)

    for f, issues in type2_by_file.items():
        issues.sort(key=lambda x: x["pre_lines"][0], reverse=True)
        for issue in issues:
            try:
                fix_type2(issue)
            except Exception as e:
                manual_review.append((issue["file"], issue["pre_lines"][0] if issue["pre_lines"] else 0,
                                      f"Error during fix: {e}"))

    # Print results
    print()
    print("=" * 70)
    print(f"AUTO-FIXED: {len(auto_fixed)}")
    print("=" * 70)
    for filepath, line, desc in auto_fixed:
        print(f"  {filepath}:{line}")
        print(f"    {desc}")
    print()

    print("=" * 70)
    print(f"SKIPPED (no fix needed): {len(skipped)}")
    print("=" * 70)
    for filepath, line, desc in skipped:
        print(f"  {filepath}:{line}")
        print(f"    {desc}")
    print()

    print("=" * 70)
    print(f"MANUAL REVIEW NEEDED: {len(manual_review)}")
    print("=" * 70)
    for filepath, line, desc in manual_review:
        print(f"  {filepath}:{line}")
        print(f"    {desc}")
    print()

    print(f"Total: {len(auto_fixed)} fixed, {len(skipped)} skipped, {len(manual_review)} need manual review.")


if __name__ == "__main__":
    main()
