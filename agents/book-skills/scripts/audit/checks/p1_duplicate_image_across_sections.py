"""Detect the same image (by src filename + content) used in more than
one section/index file in the book.

Pattern (BAD): section-18.1a.html and section-18.1b.html both reference
the same images/rlhf-talent-show.png. Both render the figure on
publication; the duplicate is a leftover from the split.

Allowed exceptions:
- Inline avatar images (images/agents/*.png) used in epigraph attributions
- chapter-opener.jpg / chapter-opener.png inside a SINGLE chapter
  (one per module index plus same image inside section files of THAT
  module is OK, but the same chapter-opener image should not appear
  in DIFFERENT modules)
- Image used in a section AND its chapter-index/part-index (sometimes a
  hero image is shared), flagged as advisory, not error.
- Deliberate cross-module references via ``../../part-XX/module-YY/...``
  paths (e.g., a security section in part-10 reusing a prompt-injection
  illustration from a prompt-engineering module in part-3). These are
  intentional citations, not accidental copies.

The cross-section-file invariant we enforce: an image SRC ending in
specific filename (chapter-opener.jpg excluded) must appear in <= 1
section-*.html file.
"""
import re
from collections import defaultdict, namedtuple
from pathlib import Path

PRIORITY = "P1"
CHECK_ID = "DUPLICATE_IMAGE_ACROSS_SECTIONS"
DESCRIPTION = "Same image referenced in more than one section file"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

IMG_RE = re.compile(r'<img\b[^>]*?src="([^"]+)"', re.IGNORECASE)

# Avatar / decorative images that are intentionally shared across sections
ALLOWED_SHARED = (
    'front-matter/images/agents/',
    'chapter-opener.jpg', 'chapter-opener.png',
    'part-opener.jpg', 'part-opener.png',
)

# Cross-module reference pattern: src that traverses up to another part's
# module images folder is a DELIBERATE cross-reference (e.g., section 49.1
# in part-10 reusing a prompt-injection illustration from part-3/module-12).
# Such intentional references should not be flagged as accidental duplicates.
CROSS_MODULE_RE = re.compile(r'\.\./\.\./part-', re.IGNORECASE)


def _allowed(src: str) -> bool:
    s = src.lower()
    if any(frag in s for frag in ALLOWED_SHARED):
        return True
    # Deliberate cross-module reference (../../part-XX/module-YY/images/...)
    if CROSS_MODULE_RE.search(src):
        return True
    return False


def _resolve(filepath: Path, src: str) -> str:
    """Resolve image src relative to the section file into a normalized
    book-rooted path, so we can compare across files."""
    # Skip absolute URLs
    if src.startswith(('http://', 'https://', '//', 'data:')):
        return ''
    base = filepath.parent
    try:
        resolved = (base / src).resolve()
        return str(resolved).replace('\\', '/').lower()
    except Exception:
        return ''


def run(filepath, html, context):
    """Cross-file invariant. We accumulate {abs_path -> [(file, line), ...]}
    and report an issue on the SECOND+ occurrence."""
    issues = []
    # Only look at section files (not module indexes / part indexes which
    # legitimately have hero images per module)
    if not filepath.name.startswith('section-'):
        return issues

    state = context.setdefault('_dup_img_state', defaultdict(list))
    for m in IMG_RE.finditer(html):
        src = m.group(1)
        if _allowed(src):
            continue
        abs_path = _resolve(filepath, src)
        if not abs_path:
            continue
        rel_self = str(filepath).replace('\\', '/')
        prior = [p for p in state[abs_path] if p[0] != rel_self]
        if prior:
            other_file = prior[-1][0]
            other_short = '/'.join(other_file.split('/')[-3:])
            line = html[:m.start()].count('\n') + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, filepath, line,
                f'Image src="{src}" also appears in {other_short}'
            ))
        state[abs_path].append((rel_self, m.start()))
    return issues
