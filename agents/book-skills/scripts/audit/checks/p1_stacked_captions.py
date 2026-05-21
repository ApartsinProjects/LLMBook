"""Detect stacked code-captions: two <div class="code-caption"> blocks
with no <pre> code block between them.

This indicates one of:
  - A misplaced caption (should be after its own code block)
  - A missing code block (the shortcut code was never inserted)
  - Two captions accidentally placed on the same code block

Note: the legacy letter-suffix check (5a, 5b) was removed because the
book convention explicitly uses letter suffixes for paired fragments
(e.g., 42.1.3a + 42.1.3b for two-part code). Flagging those is wrong.

Tolerance: if more than 5 non-empty lines separate the two captions,
they are probably in different structural contexts (different sections
or callouts) and not truly stacked.
"""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "STACKED_CAPTIONS"
DESCRIPTION = "Two code-caption divs with no <pre> code block between them"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

CAPTION_RE = re.compile(r'class="code-caption"')
PRE_RE = re.compile(r'<pre\b', re.IGNORECASE)
FRAGMENT_LABEL_RE = re.compile(r'Code Fragment\s+([\d.]+[a-zA-Z]?)')


def run(filepath, html, context):
    issues = []
    if not filepath.name.endswith(".html"):
        return issues
    if not filepath.name.startswith("section-"):
        return issues

    lines = html.split("\n")
    caption_lines = []  # list of (line_num, label)
    pre_lines = []      # list of line_nums where <pre> appears

    for i, line in enumerate(lines, 1):
        if CAPTION_RE.search(line):
            m = FRAGMENT_LABEL_RE.search(line)
            caption_lines.append((i, m.group(1) if m else "unknown"))
        if PRE_RE.search(line):
            pre_lines.append(i)

    # Check consecutive caption pairs
    for idx in range(len(caption_lines) - 1):
        line_a, label_a = caption_lines[idx]
        line_b, label_b = caption_lines[idx + 1]

        has_pre_between = any(line_a < p < line_b for p in pre_lines)
        if has_pre_between:
            continue

        between_lines = [l for l in lines[line_a:line_b - 1] if l.strip()]
        if len(between_lines) > 5:
            # Significant structural HTML separates them; not truly stacked.
            continue

        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line_a,
            f"Stacked captions: Code Fragment {label_a} (line {line_a}) and "
            f"Code Fragment {label_b} (line {line_b}) have no <pre> block between them"
        ))

    return issues
