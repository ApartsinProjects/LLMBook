"""Detect numbering gaps in part / chapter / section / sub-section numbering.

What it catches (real Edition 16 example before fix):
  Part VIII had module-37, module-38, module-40, module-41 on disk - a
  gap at Chapter 39 caused by a Wave 9 chapter merge that did NOT
  renumber 40/41 down. The ToC silently inherited the gap and KDP
  shipped with a Ch 37 -> 38 -> 40 -> 41 jump.

Three kinds of gap checked:
  1) Chapter gap within a Part:
       module-N1, module-N2 with N2 > N1 + 1 (not just the part's start)
  2) Section gap within a Chapter:
       section-X.A, section-X.B with B > A + 1
  3) Sub-section gap within a Section file:
       headings numbered X.Y.0.A, X.Y.0.B with B > A + 1 inside one file

Emits one issue per gap. Run on every part-index.html and every
chapter-index.html; sub-section gaps run on every section file.

Priority P1 (content correctness, not build-blocking).
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P1"
CHECK_ID = "NUMBERING_GAP"
DESCRIPTION = "Chapter / section / sub-section numbering has a gap (e.g., 38 -> 40 skips 39)"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

MOD_RE = re.compile(r"^module-(\d+)-")
SEC_RE = re.compile(r"^section-(\d+)\.(\d+)(?:\.(\d+))?\.html$")


def _gaps(numbers: list[int]) -> list[tuple[int, int]]:
    """Return [(prev, next)] pairs where next > prev + 1."""
    out = []
    nums = sorted(set(numbers))
    for a, b in zip(nums, nums[1:]):
        if b > a + 1:
            out.append((a, b))
    return out


def _scan_chapter_gaps_in_part(part_dir: Path) -> list[tuple[int, int]]:
    mods = []
    for d in part_dir.iterdir():
        if d.is_dir():
            m = MOD_RE.match(d.name)
            if m:
                mods.append(int(m.group(1)))
    return _gaps(mods)


def _scan_section_gaps_in_chapter(chapter_dir: Path) -> list[tuple[str, int, int]]:
    """Return [(chapter_num_str, gap_from, gap_to)]."""
    # group by chapter-number prefix (almost always one per dir, but handle
    # edge cases like section-0.X and section-1.X in the same module)
    by_chapter = {}
    for f in chapter_dir.glob("section-*.html"):
        m = SEC_RE.match(f.name)
        if not m:
            continue
        ch_str = m.group(1)
        sec_num = int(m.group(2))
        by_chapter.setdefault(ch_str, []).append(sec_num)
    out = []
    for ch_str, secs in by_chapter.items():
        for a, b in _gaps(secs):
            out.append((ch_str, a, b))
    return out


HEADING_NUM_RE = re.compile(
    r"<h[2-4][^>]*>\s*(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?\s",
    re.IGNORECASE,
)


def _scan_subsection_gaps_in_file(html: str) -> list[tuple[str, int, int, int]]:
    """Return [(prefix_X.Y.Z, gap_at_level, gap_from, gap_to)]."""
    # Build {prefix: [list of next-level numbers]}
    # prefix is "X.Y", level-3 numbers are the values; OR prefix "X.Y.Z"
    # with level-4 numbers as the values.
    groups = {}
    for m in HEADING_NUM_RE.finditer(html):
        x, y, z = m.group(1), m.group(2), int(m.group(3))
        w = m.group(4)
        # level 3 grouping
        groups.setdefault((f"{x}.{y}", 3), set()).add(z)
        # level 4 grouping
        if w:
            groups.setdefault((f"{x}.{y}.{z}", 4), set()).add(int(w))
    out = []
    for (prefix, lvl), nums in groups.items():
        for a, b in _gaps(sorted(nums)):
            out.append((prefix, lvl, a, b))
    return out


def run(filepath, html, context):
    issues = []
    name = filepath.name
    parent = filepath.parent
    book_root = context["book_root"]

    # --- 1) chapter gaps: emit on part-X/index.html ---
    if (
        name == "index.html"
        and parent.parent == book_root
        and parent.name.startswith("part-")
    ):
        for a, b in _scan_chapter_gaps_in_part(parent):
            # Find module dir names for both ends to give a useful message
            issues.append(
                Issue(
                    PRIORITY,
                    CHECK_ID,
                    filepath,
                    1,
                    f"Chapter numbering gap in {parent.name}: jumps from {a} to {b} "
                    f"(missing chapter {a + 1}{f' through {b - 1}' if b - a > 2 else ''})",
                )
            )

    # --- 2) section gaps: emit on module-XX/index.html ---
    if name == "index.html" and parent.name.startswith("module-"):
        for ch_str, a, b in _scan_section_gaps_in_chapter(parent):
            issues.append(
                Issue(
                    PRIORITY,
                    CHECK_ID,
                    filepath,
                    1,
                    f"Section numbering gap in {parent.name}: "
                    f"Section {ch_str}.{a} -> {ch_str}.{b} (missing "
                    f"{ch_str}.{a + 1}{f' through {ch_str}.{b - 1}' if b - a > 2 else ''})",
                )
            )

    # --- 3) sub-section gaps inside one section file ---
    if name.startswith("section-") and name.endswith(".html"):
        for prefix, lvl, a, b in _scan_subsection_gaps_in_file(html):
            issues.append(
                Issue(
                    PRIORITY,
                    CHECK_ID,
                    filepath,
                    1,
                    f"Sub-section numbering gap at level {lvl} under {prefix}: "
                    f"{prefix}.{a} -> {prefix}.{b}",
                )
            )

    return issues
