"""Flag figure and code-fragment captions that are numbered out of sequence.

The check only considers numbers INSIDE caption-bearing elements
(figcaption, diagram-caption, code-caption). Prose cross-references that
mention "Figure X.Y.Z" do NOT count toward the sequence check — authors
legitimately reference figures both before and after their introduction
in the surrounding prose, and a forward reference is not an ordering bug.
"""
import re
from collections import defaultdict, namedtuple

PRIORITY = "P1"
CHECK_ID = "FIGURE_SEQUENCE"
DESCRIPTION = "Figure or Code Fragment captions are numbered out of order or have gaps"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Caption-bearing substrings: figcaption, diagram-caption, code-caption.
# We extract these THEN scan for the Figure/Code-Fragment number inside.
# Caption titles use <strong>Figure X.Y.Z</strong> or
# <strong>Code Fragment X.Y.Z:</strong> as the LEADING token.
CAPTION_SUBSTRING_RE = re.compile(
    r'<figcaption\b[^>]*>(.*?)</figcaption>'
    r'|<div\s+class="(?:diagram-caption|code-caption)"[^>]*>(.*?)</div>',
    re.IGNORECASE | re.DOTALL,
)

# Match the FIRST number inside a caption substring.
# Optional single-letter suffix for library-shortcut variants is captured
# separately so a, b, c don't all collide on the same seq number.
NUM_IN_CAPTION_RE = re.compile(
    r"<strong>\s*(?P<kind>Figure|Code Fragment)\s+"
    r"(?P<prefix>\d+\.\d+)\.(?P<seq>\d+)(?P<letter>[a-z])?"
    r"\s*[:</]",
    re.IGNORECASE,
)


def run(filepath, html, context):
    issues = []

    # Collect all captioned items: (kind, prefix) -> [(seq_num, letter, line_num)]
    groups = defaultdict(list)
    for cm in CAPTION_SUBSTRING_RE.finditer(html):
        caption_text = cm.group(1) or cm.group(2) or ''
        if not caption_text.strip():
            continue
        line_no = html.count("\n", 0, cm.start()) + 1
        # Only the FIRST number in the caption text is the caption's OWN
        # label; later numbers are author-written cross-references.
        m = NUM_IN_CAPTION_RE.search(caption_text)
        if not m:
            continue
        kind = m.group("kind").title()
        prefix = m.group("prefix")
        seq = int(m.group("seq"))
        letter = m.group("letter") or ""
        groups[(kind, prefix)].append((seq, letter, line_no))

    for (kind, prefix), entries in groups.items():
        if len(entries) < 2:
            continue

        # Check ordering. A letter-suffixed entry like "9.2.5a" is a variant
        # of "9.2.5"; multiple letter variants in a row at the same base are
        # legitimate. The base seq must still be monotonically non-decreasing
        # (a, b, c can stack on the same seq number).
        for idx in range(1, len(entries)):
            prev_seq, prev_letter, prev_line = entries[idx - 1]
            curr_seq, curr_letter, curr_line = entries[idx]
            # Strictly out of order if curr_seq < prev_seq.
            # Same seq is OK only if both have letters in increasing order.
            if curr_seq < prev_seq:
                prev_label = f"{prev_seq}{prev_letter}" if prev_letter else str(prev_seq)
                curr_label = f"{curr_seq}{curr_letter}" if curr_letter else str(curr_seq)
                issues.append(Issue(
                    priority=PRIORITY,
                    check_id=CHECK_ID,
                    filepath=filepath,
                    line=curr_line,
                    message=(
                        f"{kind} {prefix}.{curr_label} (line {curr_line}) "
                        f"appears after {kind} {prefix}.{prev_label} (line {prev_line})"
                    ),
                ))
            elif curr_seq == prev_seq:
                # Both must have letters in increasing order (a, b, c, ...).
                if not (prev_letter and curr_letter and curr_letter > prev_letter):
                    prev_label = f"{prev_seq}{prev_letter}" if prev_letter else str(prev_seq)
                    curr_label = f"{curr_seq}{curr_letter}" if curr_letter else str(curr_seq)
                    issues.append(Issue(
                        priority=PRIORITY,
                        check_id=CHECK_ID,
                        filepath=filepath,
                        line=curr_line,
                        message=(
                            f"{kind} {prefix}.{curr_label} (line {curr_line}) "
                            f"appears after {kind} {prefix}.{prev_label} (line {prev_line})"
                        ),
                    ))

        # Check for zero-based numbering bug
        seq_nums = sorted(set(s for s, _, _ in entries))
        if seq_nums and seq_nums[0] == 0:
            issues.append(Issue(
                priority=PRIORITY,
                check_id=CHECK_ID,
                filepath=filepath,
                line=entries[0][2],
                message=f"{kind} {prefix}.0 uses zero-based numbering (should start at 1)",
            ))

    return issues
