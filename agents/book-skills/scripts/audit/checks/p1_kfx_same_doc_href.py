"""Detect same-document fragment hrefs (`href="#foo"`) that KFX cannot resolve.

WHY THIS IS P1
  EPUBCheck accepts `<a href="#foo">` as valid EPUB 3 (the fragment refers
  to the same XHTML file). Amazon's KFX converter does NOT resolve these
  fragment-only references; every one emits a W10001 "Hyperlink could not
  be resolved" warning during -convert -qualitychecks, and the resulting
  KFX has dead links on Kindle devices.

  Fix: rewrite to `<a href="filename.xhtml#foo">`. html2epub will map the
  source basename to the flat chapter filename, producing
  `href="ch_NNNN_*.xhtml#foo"` which KFX handles correctly.

  Source-level fix script: KDP/build/fix_same_doc_hrefs.py
  Documentation:           claude-skills/epub2kpf/DIRECT_JAR_BYPASS.md

EVIDENCE FROM FIELD
  On a 37 MB / 605-chapter EPUB, 30 such hrefs were silently broken in
  the .kpf. EPUBCheck strict reported 0/0/0/0 (clean). Only the direct
  KFX conversion log revealed them.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P1"
CHECK_ID = "KFX_SAME_DOC_HREF"
DESCRIPTION = (
    "Same-document fragment href (href=\"#foo\") that KFX cannot resolve. "
    "Use href=\"filename.html#foo\" instead."
)

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# <a ... href="#foo" ...>  (fragment-only, no filename before #)
SAME_DOC_HREF = re.compile(
    r'<a\b[^>]*?\bhref="(#[^"#]+)"[^>]*?>',
    re.IGNORECASE | re.DOTALL,
)
# Match id="foo" on any element (to know which anchors exist in this file)
ID_ATTR = re.compile(r'\bid="([^"]+)"')


def check(filepath: Path, content: str) -> list[Issue]:
    """Return list of Issues for one HTML/XHTML file."""
    # Quick exit
    if 'href="#' not in content:
        return []

    issues: list[Issue] = []
    ids_in_file = set(ID_ATTR.findall(content))
    self_name = filepath.name

    # Walk every same-doc href; report each occurrence with its line number
    for m in SAME_DOC_HREF.finditer(content):
        anchor = m.group(1)            # e.g. "#section-1"
        target_id = anchor[1:]
        line = content.count("\n", 0, m.start()) + 1

        if target_id in ids_in_file:
            issues.append(Issue(
                PRIORITY, CHECK_ID, str(filepath), line,
                f'href="{anchor}" -> KFX-fatal; '
                f'rewrite to href="{self_name}{anchor}"'
            ))
        else:
            issues.append(Issue(
                PRIORITY, CHECK_ID, str(filepath), line,
                f'href="{anchor}" -> KFX-fatal AND orphan (no id="{target_id}" '
                f'anywhere in this file); review intent before fixing'
            ))
    return issues
