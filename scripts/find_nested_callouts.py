#!/usr/bin/env python3
"""Find nested callout divs in book HTML files.

Scans all section and index HTML files for cases where a
<div class="callout ..."> is nested inside another callout div.
Reports the file, line numbers, callout types, and text previews.
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Glob patterns for HTML files to scan
PATTERNS = [
    "part-*/module-*/section-*.html",
    "part-*/module-*/index.html",
    "appendices/appendix-*/section-*.html",
    "appendices/appendix-*/index.html",
    "front-matter/*.html",
]

CALLOUT_OPEN_RE = re.compile(r'<div\s+class="callout\s+([^"]*)"', re.IGNORECASE)
DIV_OPEN_RE = re.compile(r'<div[\s>]', re.IGNORECASE)
DIV_CLOSE_RE = re.compile(r'</div\s*>', re.IGNORECASE)


def extract_text_preview(lines, start_line, max_chars=80):
    """Extract first max_chars of visible text from lines starting at start_line."""
    text = []
    for line in lines[start_line:start_line + 20]:
        # Strip HTML tags
        cleaned = re.sub(r'<[^>]+>', ' ', line)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        if cleaned:
            text.append(cleaned)
        combined = ' '.join(text)
        if len(combined) >= max_chars:
            return combined[:max_chars]
    return ' '.join(text)[:max_chars]


def find_nested_callouts_in_file(filepath):
    """Find nested callouts in a single file.

    Returns a list of dicts with keys:
      file, outer_line, inner_line, outer_type, inner_type,
      outer_preview, inner_preview
    """
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    results = []
    # Stack of active callout contexts: (line_number, callout_type, div_depth)
    # div_depth counts how many unmatched <div> tags are open inside this callout
    callout_stack = []
    # We also track general div depth to know when a callout closes
    # Each callout entry: {line, type, depth_at_open}
    # depth_at_open = the global div depth when this callout's <div> was opened
    global_div_depth = 0

    for line_idx, line in enumerate(lines):
        # We need to process all div opens and closes in order within this line.
        # Build a list of events: (position, event_type, match_data)
        events = []

        for m in DIV_OPEN_RE.finditer(line):
            callout_match = CALLOUT_OPEN_RE.match(line, m.start())
            if callout_match:
                events.append((m.start(), 'callout_open', callout_match.group(1).strip()))
            else:
                events.append((m.start(), 'div_open', None))

        for m in DIV_CLOSE_RE.finditer(line):
            events.append((m.start(), 'div_close', None))

        # Sort by position in line
        events.sort(key=lambda e: e[0])

        for _pos, event_type, data in events:
            if event_type == 'callout_open':
                # This is a <div class="callout ...">
                # If there are already callouts on the stack, this is nested
                if callout_stack:
                    outer = callout_stack[-1]
                    results.append({
                        'file': filepath,
                        'outer_line': outer['line'] + 1,
                        'inner_line': line_idx + 1,
                        'outer_type': outer['type'],
                        'inner_type': data,
                        'outer_preview': extract_text_preview(lines, outer['line']),
                        'inner_preview': extract_text_preview(lines, line_idx),
                    })
                callout_stack.append({
                    'line': line_idx,
                    'type': data,
                    'depth_at_open': global_div_depth,
                })
                global_div_depth += 1

            elif event_type == 'div_open':
                global_div_depth += 1

            elif event_type == 'div_close':
                global_div_depth -= 1
                # Check if any callout on the stack just closed
                while callout_stack and global_div_depth <= callout_stack[-1]['depth_at_open']:
                    callout_stack.pop()

    return results


def main():
    all_files = []
    for pattern in PATTERNS:
        full_pattern = os.path.join(ROOT, pattern)
        matched = glob.glob(full_pattern, recursive=False)
        all_files.extend(matched)

    # Deduplicate and sort
    all_files = sorted(set(all_files))

    print(f"Scanning {len(all_files)} HTML files for nested callouts...")

    all_results = []
    for filepath in all_files:
        results = find_nested_callouts_in_file(filepath)
        all_results.extend(results)

    # Build report
    report_lines = []
    report_lines.append(f"Nested Callout Report")
    report_lines.append(f"Scanned {len(all_files)} files, found {len(all_results)} nested callout(s).")
    report_lines.append("")

    if not all_results:
        report_lines.append("No nested callouts found. All clear!")
    else:
        for i, r in enumerate(all_results, 1):
            rel_path = os.path.relpath(r['file'], ROOT).replace('\\', '/')
            report_lines.append(f"--- Finding #{i} ---")
            report_lines.append(f"  File:         {rel_path}")
            report_lines.append(f"  Outer line:   {r['outer_line']}  (type: {r['outer_type']})")
            report_lines.append(f"  Inner line:   {r['inner_line']}  (type: {r['inner_type']})")
            report_lines.append(f"  Outer text:   {r['outer_preview']}")
            report_lines.append(f"  Inner text:   {r['inner_preview']}")
            report_lines.append("")

    report_text = '\n'.join(report_lines)
    print(report_text)

    report_path = os.path.join(ROOT, "scripts", "nested_callouts_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
