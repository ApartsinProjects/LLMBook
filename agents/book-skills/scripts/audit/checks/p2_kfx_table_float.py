"""Detect float CSS on <table> elements (W11007 in KFX conversion log).

WHY THIS IS P2 (COSMETIC)
  KFX silently strips `float: left|right` from any table element (tables
  are always block in Kindle). Each occurrence emits one W11007 in the
  conversion log. Harmless but noise.

  Two source patterns flagged:
    1. Inline: `<table style="float: left">...`
    2. CSS rule:  `table, table.foo { float: left }`

  Fix at SOURCE for case 1, at CSS for case 2. Or wholesale strip via
  KDP/build/fix_kfx_epub_css.py (post-build, leaves source untouched).

EVIDENCE FROM FIELD
  On the LLMBook EPUB: 243 occurrences in conversion.log, ALL from a CSS
  rule (zero inline matches). The rule target was a class applied to
  floating-tables-with-caption styling on the web; on Kindle the float
  is stripped and the layout shifts slightly.
"""
import re
from collections import namedtuple
from pathlib import Path

PRIORITY = "P2"
CHECK_ID = "KFX_TABLE_FLOAT"
DESCRIPTION = (
    "Float CSS on <table> element. KFX strips it (W11007). Cosmetic noise."
)

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# Case 1: inline style on table
INLINE_RE = re.compile(
    r'<table\b[^>]*?\bstyle="[^"]*\bfloat\s*:\s*(left|right)',
    re.IGNORECASE,
)
# Case 2: CSS rule whose selector mentions table AND body declares float
# Simpler: scan rule-by-rule
RULE_RE = re.compile(r"([^{}]*?)\{([^{}]*?)\}", re.DOTALL)
FLOAT_DECL = re.compile(r"\bfloat\s*:\s*(left|right)", re.IGNORECASE)


def check(filepath: Path, content: str) -> list[Issue]:
    issues: list[Issue] = []
    suffix = filepath.suffix.lower()

    if suffix in {".html", ".xhtml"}:
        for m in INLINE_RE.finditer(content):
            line = content.count("\n", 0, m.start()) + 1
            issues.append(Issue(
                PRIORITY, CHECK_ID, str(filepath), line,
                f"Inline `<table style='float:{m.group(1)}'>` -> W11007 "
                f"(KFX strips float from tables)"
            ))
    elif suffix == ".css":
        for m in RULE_RE.finditer(content):
            selector, body = m.group(1), m.group(2)
            if "table" in selector.lower() and FLOAT_DECL.search(body):
                line = content.count("\n", 0, m.start()) + 1
                issues.append(Issue(
                    PRIORITY, CHECK_ID, str(filepath), line,
                    f"CSS rule `{selector.strip()[:60]}` declares float on table -> W11007"
                ))
    return issues
