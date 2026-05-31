"""Detect CSS properties that KFX silently ignores (W00015 warnings).

WHY THIS IS P2 (NOISE, NOT CRITICAL)
  These properties don't break the EPUB. KFX strips them silently during
  conversion. They are P2 because:
    (a) Each occurrence emits one W00015 line into the KFX conversion log;
        on a large book this can grow the log from ~1 MB to 70+ MB and
        bury real errors (W10001 etc).
    (b) Some properties create different rendering on Kindle vs web preview,
        which surprises authors who tested in a browser.

  Top offenders in the wild (counts from a 37 MB book):
    331,178  box-sizing: border-box     -> KFX uses fixed box model
     28,234  line-height: 1.5           -> KFX manages per device
     12,734  -webkit-column-break-inside: auto
     12,307  line-height: 1.25
      7,118  -webkit-print-color-adjust: exact   -> print-only
      3,629  -webkit-column-break-inside: avoid
      2,633  line-height: 1.3 (and many other line-height values)
        985  -webkit-column-span: none

  Documentation: claude-skills/epub2kpf/DIRECT_JAR_BYPASS.md

FIX
  Edit your EPUB-only stylesheet (typically `styles/epub_overrides.css`
  or `styles/book.css`) and remove these properties for the EPUB build.
  Keep them in the web-only stylesheet if your site needs them.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P2"
CHECK_ID = "KFX_UNSUPPORTED_CSS"
DESCRIPTION = (
    "CSS property KFX silently strips. Cosmetic — produces W00015 noise in "
    "conversion log but does not break the EPUB. Cleaning lets real warnings stand out."
)

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Properties confirmed to emit W00015 in KFX conversion (and how to think about them)
KFX_STRIPS = {
    "box-sizing":                       "ignored - KFX uses fixed box model",
    "line-height":                      "overridden - KFX manages per Kindle device",
    "-webkit-column-break-inside":      "ignored - no CSS columns on Kindle",
    "-webkit-column-span":              "ignored - no CSS columns on Kindle",
    "-webkit-column-count":             "ignored - no CSS columns on Kindle",
    "-webkit-column-width":             "ignored - no CSS columns on Kindle",
    "-webkit-column-gap":               "ignored - no CSS columns on Kindle",
    "-webkit-print-color-adjust":       "ignored - print-only property",
    "print-color-adjust":               "ignored - print-only property",
    "caption-side":                     "ignored - KFX places captions in fixed location",
}

# Match `prop: value` or `prop:value` in any CSS context (block, inline-style attr)
PROP_RE = re.compile(
    r'(^|[\s;{])\s*(' + "|".join(re.escape(p) for p in KFX_STRIPS) + r')\s*:',
    re.IGNORECASE | re.MULTILINE,
)


def check(filepath: Path, content: str) -> list[Issue]:
    """Return list of Issues for one CSS or HTML (inline style) file."""
    # Apply only to CSS + HTML/XHTML files
    if filepath.suffix.lower() not in {".css", ".html", ".xhtml"}:
        return []

    issues: list[Issue] = []
    for m in PROP_RE.finditer(content):
        prop = m.group(2).lower()
        reason = KFX_STRIPS.get(prop, "ignored by KFX")
        line = content.count("\n", 0, m.start()) + 1
        issues.append(Issue(
            PRIORITY, CHECK_ID, str(filepath), line,
            f"CSS prop '{prop}' on line {line} — KFX W00015 ({reason})"
        ))
    return issues
