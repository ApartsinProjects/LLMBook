"""Verify every "(Ch N-M)" in description.txt / description.html matches reality.

Motivation: in Edition 16 the description.txt said
  "Part VIII, Conversational AI with LLMs (Ch 37-41)"
when Part VIII actually had 4 chapters (37, 38, 40, 41 - gap at 39).
The description claimed 5 chapters; the book had 4. The numbers were
also wrong even ignoring the gap, since 41 - 37 + 1 = 5 not 4.

This plugin walks every Part heading + chapter range claim in the two
description files and checks against on-disk chapter numbers.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P1"
CHECK_ID = "DESC_CHAPTER_RANGE"
DESCRIPTION = "Chapter range in description.txt / description.html disagrees with on-disk chapter numbers"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Match patterns like "Part VIII, Conversational AI with LLMs (Ch 37-41)"
# Capture the part roman numeral and the low/high chapter numbers.
PART_RANGE_RE = re.compile(
    r"Part\s+([IVX]+)[^()]*?\(\s*Ch\s+(\d+)\s*[-–]\s*(\d+)\s*\)",
    re.IGNORECASE,
)

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7,
         "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13,
         "XIV": 14, "XV": 15}


def _chapters_in_part(book_root: Path, part_num: int) -> list[int]:
    """Return sorted module numbers for part-N."""
    out = []
    for d in book_root.glob(f"part-{part_num}-*"):
        if not d.is_dir():
            continue
        for m in d.glob("module-*"):
            mat = re.match(r"module-(\d+)-", m.name)
            if mat:
                out.append(int(mat.group(1)))
    return sorted(out)


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]

    # Only run on KDP description files
    rel = str(filepath.relative_to(book_root)).replace("\\", "/").lower()
    if rel not in {"kdp/metadata/description.txt", "kdp/metadata/description.html"}:
        return issues

    text = html  # plugin framework passes content as html param
    for m in PART_RANGE_RE.finditer(text):
        roman, lo, hi = m.group(1).upper(), int(m.group(2)), int(m.group(3))
        if roman not in ROMAN:
            continue
        part_num = ROMAN[roman]
        actual = _chapters_in_part(book_root, part_num)
        if not actual:
            continue
        # The description's "Ch lo-hi" implies the range [lo, hi] (inclusive).
        # Reality: chapter set is `actual`, with first=min, last=max.
        # Two failure modes:
        #   (a) lo or hi don't match actual min/max
        #   (b) the range claim implies (hi-lo+1) chapters but actual has fewer (gap)
        a_min, a_max = actual[0], actual[-1]
        if (lo, hi) != (a_min, a_max):
            line = text[:m.start()].count("\n") + 1
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                                f"Part {roman} (Ch {lo}-{hi}) does not match disk: "
                                f"actual chapters {actual}"))
            continue
        claimed = hi - lo + 1
        if len(actual) != claimed:
            line = text[:m.start()].count("\n") + 1
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, line,
                                f"Part {roman} description says Ch {lo}-{hi} (implies {claimed} chapters) "
                                f"but disk has {len(actual)} chapters: {actual}"))
    return issues
