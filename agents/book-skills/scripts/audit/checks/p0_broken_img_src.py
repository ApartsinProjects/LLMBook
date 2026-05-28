"""Check for broken <img src=...> references (file does not exist on disk).

This is the companion to p0_broken_xref (which only covers href=).
A real-world failure mode it catches: renaming a chapter directory
(e.g. module-41 -> module-40) plus a regex pass that rewrites
"41" -> "40" in all HTML, including the src attribute of
<img src="images/comic-41.2-...">, but NOT renaming the image file
on disk. The img tag now points at a nonexistent file. EPUBCheck
catches this only at build time; this plugin catches it during the
HTML audit, before the build, when fixing is one rename away.

Also covers <source src=...> in <picture>/<audio>/<video> and
<svg ... xlink:href=...> referencing external images.
"""
import re
from collections import namedtuple

PRIORITY = "P0"
CHECK_ID = "BROKEN_IMG_SRC"
DESCRIPTION = "Image / media src points to a file that does not exist on disk"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

SRC_RE = re.compile(r'<(?:img|source)\b[^>]*\bsrc="([^"]+)"', re.IGNORECASE)
XLINK_RE = re.compile(r'<\w+[^>]*\bxlink:href="([^"]+)"', re.IGNORECASE)
SKIP_PREFIXES = ("http://", "https://", "mailto:", "javascript:", "tel:", "data:", "#")


def _check_refs(html: str, filepath, regex, kind: str, all_files):
    out = []
    for i, line in enumerate(html.split("\n"), 1):
        for m in regex.finditer(line):
            ref = m.group(1)
            if any(ref.startswith(p) for p in SKIP_PREFIXES):
                continue
            clean = ref.split("#")[0].split("?")[0]
            if not clean:
                continue
            target = (filepath.parent / clean).resolve()
            if target not in all_files and not target.exists():
                out.append(Issue(PRIORITY, CHECK_ID, filepath, i,
                                 f'Broken {kind}: {ref}'))
    return out


def run(filepath, html, context):
    issues = []
    all_files = context["all_files"]
    issues.extend(_check_refs(html, filepath, SRC_RE, "img src", all_files))
    issues.extend(_check_refs(html, filepath, XLINK_RE, "xlink:href", all_files))
    return issues
