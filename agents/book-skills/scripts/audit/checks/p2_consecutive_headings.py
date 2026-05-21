"""Check for consecutive headings with no intervening content.

Skips canonical patterns where the heading-after-heading sequence is intentional:
  - Lab "Steps" parent followed by "Step 1/2/3..." child headings
  - Part index "Part X: ..." h1 followed by "Part Overview" h2
  - About-Authors h2 followed by individual author h3 names
  - Copyright pages where multiple sub-sections stack closely
  - Deliverables list h2 followed by "Deliverable N: ..." h3
  - Exercise blocks with numbered Exercise headings
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "CONSECUTIVE_HEADINGS"
DESCRIPTION = "Two consecutive headings with no content between them"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Match any heading tag (h1 through h6)
HEADING_RE = re.compile(r'<(h[1-6])\b[^>]*>(.*?)</\1>', re.DOTALL | re.IGNORECASE)

# Canonical parent / child pairs where stacked headings are expected
CANONICAL_STACKS = [
    ("steps", re.compile(r'^step\s+\d', re.IGNORECASE)),
    ("about the authors", re.compile(r'.+,?\s*(?:ph\.?d|m\.?s|dr|prof)', re.IGNORECASE)),
    ("deliverables", re.compile(r'^deliverable\s+\d', re.IGNORECASE)),
    ("exercises", re.compile(r'^exercise\s+\d', re.IGNORECASE)),
    ("requirements", re.compile(r'^requirement\s+\d', re.IGNORECASE)),
]

# Canonical parent text patterns (h1) -> any direct child h2 is fine
H1_PARENTS = re.compile(r'^(part\s+[IVXLCDM\d]+|appendix\s+[A-Z]|copyright|capstone)', re.IGNORECASE)


NUMERIC_PARENT_RE = re.compile(r'^(\d+(?:\.\d+)+)\b')


def _is_canonical_pair(cur_text: str, nxt_text: str) -> bool:
    cur_low = cur_text.strip().lower().rstrip(':')
    for parent, child_pat in CANONICAL_STACKS:
        if cur_low.startswith(parent) and child_pat.match(nxt_text.strip()):
            return True
    # Part overview/Appendix-X h2 right after Part X / Appendix Y h1 is canonical
    if H1_PARENTS.match(cur_text.strip()):
        return True
    # Numeric subsection pattern: "X.Y.Z Title" h2 followed by
    # any h3 (numbered or unnumbered). This is the canonical academic
    # book convention where the parent h2 establishes a topic and the
    # first h3 sub-section begins the content. Numbered children
    # ("X.Y.Z.1") are obvious; unnumbered children ("The Greedy
    # Decoding Algorithm" under "4.1.2 Greedy Decoding") are equally
    # idiomatic. Common across thousands of textbooks.
    cur_match = NUMERIC_PARENT_RE.match(cur_text.strip())
    if cur_match:
        # cur_text is a numbered h2 like "0.1.3 Loss Functions and Optimization"
        return True
    return False


META_WRAPPER_OPEN_RE = re.compile(
    r'<div\s+class="(?:prerequisites|prereqs|learning-objectives|objectives|'
    r'learning-outcomes|outcomes|takeaways)"',
    re.IGNORECASE,
)


def _inside_meta_wrapper(html: str, pos: int) -> bool:
    """Return True if `pos` is inside an open prerequisites/objectives/takeaways div."""
    window = html[max(0, pos - 800):pos]
    last_open = None
    for m in META_WRAPPER_OPEN_RE.finditer(window):
        last_open = m
    if not last_open:
        return False
    # The last </div> that occurs AFTER the open close it
    rel = window[last_open.end():]
    if '</div>' in rel:
        return False
    return True


def run(filepath, html, context):
    issues = []
    headings = list(HEADING_RE.finditer(html))

    for idx in range(len(headings) - 1):
        current = headings[idx]
        nxt = headings[idx + 1]

        # Skip if the NEXT heading is inside a meta wrapper (prereqs/takeaways).
        # Those wrappers visually separate the meta from the section content,
        # so heading-immediately-after-h2 is canonical.
        if _inside_meta_wrapper(html, nxt.start()):
            continue

        # Get the text between end of current heading and start of next
        between = html[current.end():nxt.start()]

        # Strip HTML tags and whitespace to see if there is real content
        text_between = re.sub(r'<[^>]+>', '', between).strip()

        if not text_between:
            cur_tag = current.group(1).lower()
            nxt_tag = nxt.group(1).lower()
            cur_text = re.sub(r'<[^>]+>', '', current.group(2)).strip()[:80]
            nxt_text = re.sub(r'<[^>]+>', '', nxt.group(2)).strip()[:80]
            # h2 -> h2 with no content between is always a structural bug:
            # two same-level sections need at least an intro paragraph.
            # Canonical patterns only apply to h2->h3 (parent introducing
            # subsection).
            if cur_tag == "h2" and nxt_tag == "h2":
                line_num = html[:nxt.start()].count("\n") + 1
                issues.append(Issue(PRIORITY, CHECK_ID, filepath, line_num,
                    f'<{nxt_tag}> "{nxt_text[:50]}" follows <{cur_tag}> "{cur_text[:50]}" '
                    f'with no content between them'))
                continue
            # Skip canonical patterns
            if _is_canonical_pair(cur_text, nxt_text):
                continue
            line_num = html[:nxt.start()].count("\n") + 1
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line_num,
                f'<{nxt_tag}> "{nxt_text[:50]}" follows <{cur_tag}> "{cur_text[:50]}" '
                f'with no content between them'))

    return issues
