"""Part-index "next" must point to the FIRST CHAPTER of THIS part,
not to the next part.

Linear navigation rule:
  part-N index -> first chapter of part-N (module-MM/index.html)
  chapter-N index -> first section of chapter-N (section-N.1.html)
  section -> next section
  last section of chapter -> first section of next chapter

If a part-index "next" goes directly to the next PART, it skips all the
chapters in this part — bad linear flow.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P1"
CHECK_ID = "LINEAR_NAV_PART_INDEX"
DESCRIPTION = "Part-index next must point to first chapter of THIS part"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

NEXT_RE = re.compile(r'<a\s+class="next"[^>]*?href="([^"]+)"', re.IGNORECASE)


def run(filepath, html, context):
    issues = []
    # Only check part-level index files (not module-level)
    if filepath.name != "index.html":
        return issues
    rel = str(filepath).replace("\\", "/")
    # Part-index files are at part-NN/index.html (no module- in path)
    if "/module-" in rel or "\\module-" in rel:
        return issues
    if "/part-" not in rel and "\\part-" not in rel:
        return issues
    # Skip part dirs that don't have modules (unlikely)
    part_dir = filepath.parent
    mods = sorted([m for m in part_dir.iterdir()
                   if m.is_dir() and m.name.startswith("module-")])
    if not mods:
        return issues

    # Pick first module
    first_mod = mods[0]
    expected_href = f"{first_mod.name}/index.html"

    m = NEXT_RE.search(html)
    if not m:
        return issues  # no next anchor at all is a separate check
    href = m.group(1)
    # Accept either the exact expected href or the same with #anchor
    if not href.endswith(expected_href):
        line = html[:m.start()].count('\n') + 1
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, line,
            f'Part-index next "{href}" should point to first chapter of this part: "{expected_href}"'
        ))
    return issues
