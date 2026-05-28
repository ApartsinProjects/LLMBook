"""Check that toc.html references every published part, chapter, appendix, capstone.

Motivation: in Edition 16 the Capstone project existed at capstone/index.html
but was missing from toc.html entirely. Readers using the ToC for navigation
never found it. The EPUB nav.xhtml had it; the source web ToC didn't.

This plugin runs once (on toc.html only) and emits one issue per missing
top-level entry.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P1"
CHECK_ID = "TOC_COMPLETENESS"
DESCRIPTION = "toc.html does not reference every on-disk part / chapter / appendix / capstone"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])


def run(filepath, html, context):
    issues = []
    book_root = context["book_root"]

    # Only run on the top-level toc.html
    if not (filepath.name == "toc.html" and filepath.parent == book_root):
        return issues

    refs = set(re.findall(r'href="([^"#]+)', html))

    # Inventory on-disk top-level pages
    expected = []
    for part in sorted(book_root.glob("part-*")):
        if part.is_dir():
            expected.append(("part", part.name))
            for mod in sorted(part.glob("module-*")):
                if mod.is_dir():
                    expected.append(("chapter", f"{part.name}/{mod.name}"))
    appendices = book_root / "appendices"
    if appendices.is_dir():
        for app in sorted(appendices.glob("appendix-*")):
            if app.is_dir():
                expected.append(("appendix", f"appendices/{app.name}"))
    if (book_root / "capstone" / "index.html").exists():
        expected.append(("capstone", "capstone"))

    for kind, key in expected:
        if not any(key in r for r in refs):
            issues.append(Issue(PRIORITY, CHECK_ID, filepath, 1,
                                f"toc.html does not reference {kind}: {key}"))
    return issues
