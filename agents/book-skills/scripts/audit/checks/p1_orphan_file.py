"""Detect orphan section files: section-X.Y.html on disk but not referenced
by the parent module-XX/index.html.

Motivation: when a section is added by a subagent or wave, it might exist
on disk but never get linked from the chapter index. EPUB build will still
ship it (html2epub walks the filesystem) but readers using the chapter
landing page will never find it.

Conversely, a chapter-index entry pointing at a deleted section is caught
by p0_broken_xref. This plugin catches the OTHER direction.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P1"
CHECK_ID = "ORPHAN_SECTION"
DESCRIPTION = "Section file exists on disk but is not linked from its chapter index.html"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

SECTION_RE = re.compile(r"^section-[\d.]+\.html$", re.IGNORECASE)


def run(filepath, html, context):
    issues = []
    name = filepath.name
    parent = filepath.parent

    # Run once per chapter (on its index.html)
    if name != "index.html" or not parent.name.startswith("module-"):
        return issues

    on_disk = sorted([f.name for f in parent.iterdir()
                      if f.is_file() and SECTION_RE.match(f.name)])

    referenced = set(re.findall(r'href="([^"#]+)', html))
    # Normalize: keep only the filename portion of each ref
    referenced_files = {r.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
                        for r in referenced}

    for f in on_disk:
        if f not in referenced_files:
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                                f"section file {f} exists on disk but is not linked from this chapter index"))
    return issues
