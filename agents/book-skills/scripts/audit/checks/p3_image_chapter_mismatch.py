"""Warn when an image file's chapter-number prefix doesn't match its module dir.

Motivation: in Edition 16 the Part VIII chapter renumber renamed module-41
to module-40, and the regex rewrote every "41.X" in HTML including
<img src="images/comic-41.2-..."> to <img src="images/comic-40.2-...">.
But the image files on disk stayed named comic-41.X.jpg. The script
p0_broken_img_src.py catches the resulting 404. This plugin catches
the WEAKER signal: image filenames that look chapter-numbered but live
in a directory whose chapter number disagrees.

Why P2 not P0: the file might be a deliberate cross-chapter borrow,
and the HTML src might correctly point at it. P0 BROKEN_IMG_SRC catches
the hard failures; this plugin surfaces "consider renaming for
consistency" cases.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P3"
CHECK_ID = "IMAGE_CHAPTER_MISMATCH"
DESCRIPTION = ("Image filename chapter-number prefix does not match the module "
               "dir's chapter number (hygiene; may be historic from earlier renumbers)")

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

MOD_RE = re.compile(r"^module-(\d+)-")
# Match image files like fig-N.X.Y-*, comic-N.X-*, comic-N.X.Y-*, listing-N.X-*
IMG_PREFIX_RE = re.compile(r"^(fig|comic|listing|table|diagram)-(\d+)\.\d", re.IGNORECASE)


def run(filepath, html, context):
    issues = []

    # Only run on each chapter's index.html (one invocation per chapter)
    if filepath.name != "index.html":
        return issues
    parent = filepath.parent
    mod_match = MOD_RE.match(parent.name)
    if not mod_match:
        return issues
    module_ch_num = int(mod_match.group(1))

    images_dir = parent / "images"
    if not images_dir.is_dir():
        return issues

    # Only flag mismatches that are ACTUALLY referenced from this chapter's
    # HTML (an unreferenced mismatched file is dead weight; other checks
    # handle that). Drops the historic-noise count from ~193 to the
    # actionable subset.
    refs = set()
    for f in parent.glob("*.html"):
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for m in re.finditer(r'src="images/([^"]+)"', text):
            refs.add(m.group(1).split("?")[0].split("#")[0])

    for img in images_dir.iterdir():
        if not img.is_file():
            continue
        pm = IMG_PREFIX_RE.match(img.name)
        if not pm:
            continue
        prefix_kind = pm.group(1)
        filename_ch_num = int(pm.group(2))
        if filename_ch_num == module_ch_num:
            continue
        if img.name not in refs:
            continue
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, 1,
            f"images/{img.name}: {prefix_kind} prefix {filename_ch_num} "
            f"!= module chapter {module_ch_num} (referenced from HTML; "
            f"rename file + update src for consistency)"
        ))
    return issues
