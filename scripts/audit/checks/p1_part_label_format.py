"""Check that part-label divs use consistent numbering format (Arabic, not Roman)."""
import re
from collections import namedtuple

PRIORITY = "P1"
CHECK_ID = "PART_LABEL_FORMAT"
DESCRIPTION = "Part label uses Roman numeral instead of Arabic numeral"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Match the part-label content: Part N: or Part X:
PART_LABEL_RE = re.compile(
    r'<div\s+class="part-label"[^>]*>.*?Part\s+([IVXLC]+|[0-9]+)\s*:',
    re.IGNORECASE,
)

# Map directory names to their expected part number (Arabic)
DIR_TO_NUM = {
    "part-1-": "1", "part-2-": "2", "part-3-": "3", "part-4-": "4",
    "part-5-": "5", "part-6-": "6", "part-7-": "7", "part-8-": "8",
    "part-9-": "9", "part-10-": "10",
}

ROMAN_RE = re.compile(r'^[IVXLC]+$')


def _expected_num(filepath):
    """Determine the Arabic part number from the directory name."""
    path_str = str(filepath).replace("\\", "/")
    for prefix, num in DIR_TO_NUM.items():
        if prefix in path_str:
            return num
    return None


def run(filepath, html, context):
    issues = []
    expected = _expected_num(filepath)
    if expected is None:
        return []

    for i, line in enumerate(html.split("\n"), 1):
        m = PART_LABEL_RE.search(line)
        if m:
            found = m.group(1)
            is_roman = bool(ROMAN_RE.match(found))

            if is_roman:
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, i,
                    f'Part label uses Roman numeral "Part {found}:" '
                    f'but directory uses Arabic "part-{expected}-"'
                ))
            elif found.isdigit() and found != expected:
                issues.append(Issue(
                    PRIORITY, CHECK_ID, filepath, i,
                    f'Part label number mismatch: "Part {found}:" '
                    f'but directory implies Part {expected}'
                ))
            break  # Only check first part-label per file
    return issues
