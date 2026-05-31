"""Detect orphan same-document hrefs: href="#foo" where #foo is not defined anywhere.

WHY THIS IS P1
  Orphan anchors are dead links that the reader will click and land nowhere.
  They survive EPUBCheck strict (no schema violation) but KFX flags them
  as W10001 "Hyperlink could not be resolved", AND the link is dead on
  every Kindle device.

  Two cases:
    1. The target id used to exist in this file but was removed by a recent
       edit (intra-file orphan; needs manual review of intent).
    2. The target id lives in a SIBLING file but the href forgot the file
       prefix (cross-file orphan; auto-fixable via fix_orphan_anchors.py).

  Use the companion script:
    KDP/build/fix_orphan_anchors.py        # auto-find target file for case 2
    KDP/build/fix_same_doc_hrefs.py        # add filename prefix for working same-docs

EVIDENCE FROM FIELD
  On the LLMBook EPUB after one editing cycle, 9 such orphans surfaced:
    #3-3-2-3-rotary-position-embedding-rope   (renamed section)
    #3-3-2-4-alibi-attention-with-linear-biases
    #prm-orm                                  (deleted subsection)
    #9-2-1-the-kv-cache-explained             (renamed)
    #9-5-2-unstructured-pruning               (renamed)
    #9-5-3-structured-pruning
    #9-7-3-flashattention-tiled-attention-in-sram
    #main-content                             (in pages without main-content id)
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P1"
CHECK_ID = "ORPHAN_ANCHOR"
DESCRIPTION = (
    "Same-document href to an id that doesn't exist in this file (and may "
    "not exist anywhere). KFX W10001 + dead link on device."
)

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

HREF_FRAGMENT = re.compile(
    r'<a\b[^>]*?\bhref="(#[^"#]+)"[^>]*?>',
    flags=re.IGNORECASE | re.DOTALL,
)
ID_ATTR = re.compile(r'\bid="([^"]+)"')


def check(filepath: Path, content: str) -> list[Issue]:
    if 'href="#' not in content:
        return []
    issues: list[Issue] = []
    ids_in_file = set(ID_ATTR.findall(content))
    for m in HREF_FRAGMENT.finditer(content):
        anchor = m.group(1)
        target_id = anchor[1:]
        if target_id not in ids_in_file:
            line = content.count("\n", 0, m.start()) + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, str(filepath), line,
                f'href="{anchor}" -> id="{target_id}" not in this file. '
                f'Run fix_orphan_anchors.py to auto-find target file.'
            ))
    return issues
