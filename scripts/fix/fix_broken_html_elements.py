#!/usr/bin/env python3
"""Fix broken HTML elements missing their opening '<' character.

A previous script consumed the '<' when extracting blocks, leaving lines
like `igure class=` instead of `<figure class=`. This script detects and
repairs those truncated tags.

Usage:
    python fix_broken_html_elements.py          # dry run (report only)
    python fix_broken_html_elements.py --fix    # apply fixes
"""
import argparse
import re
import sys
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
SCAN_DIRS = [BOOK_ROOT / d for d in [
    "part-1-foundations",
    "part-2-understanding-llms",
    "part-3-working-with-llms",
    "part-4-training-adapting",
    "part-5-retrieval-conversation",
    "part-6-agentic-ai",
    "part-7-multimodal-applications",
    "part-8-evaluation-production",
    "part-9-safety-strategy",
    "part-10-frontiers",
    "part-11-idea-to-product",
    "appendices",
]]

# ---------------------------------------------------------------------------
# Strategy: we define two categories of broken-tag patterns.
#
# Category A: Full tag name present but missing '<'.
#   The line starts (after optional whitespace) with a valid HTML tag name
#   followed immediately by tag-like syntax: '>' or ' class=' or ' id=' etc.
#   Example: "figure class="illustration">"  should be  "<figure class=..."
#   Example: "h2>Exercises</h2>"             should be  "<h2>Exercises</h2>"
#   Example: "!-- comment -->"               should be  "<!-- comment -->"
#
#   We require the tag name to be followed by '>', ' class=', ' id=',
#   ' style=', ' data-', ' aria-', ' role=', ' href=', ' src=', ' alt=',
#   ' type=', or similar HTML attribute syntax. This eliminates false
#   positives where English prose happens to start with a tag name.
#
# Category B: Partial tag name (first char(s) also consumed).
#   Example: "igure class="  from "<figure"   (lost '<f')
#   Example: "iv class="     from "<div"       (lost '<d')
#   Example: "ection "       from "<section"   (lost '<s')
#   Same requirement: must be followed by tag-like syntax.
# ---------------------------------------------------------------------------

# HTML attribute indicators that distinguish a real tag from prose.
_ATTR_INDICATOR = r'(?:>|/>|\s+(?:class|id|style|data-|aria-|role|href|src|alt|type|name|value|for|action|method|target|rel|width|height|viewBox|xmlns|d|fill|stroke|transform|cx|cy|r|x[12]?|y[12]?|points)\s*=)'

# Category A: full tag names missing only '<'
_FULL_TAGS = [
    "figure", "figcaption", "div", "section", "blockquote",
    "table", "thead", "tbody", "tfoot", "caption", "colgroup", "col",
    "tr", "td", "th",
    "ul", "ol", "li", "dl", "dt", "dd",
    "p", "a", "span", "img", "br", "hr",
    "pre", "code", "em", "strong", "b", "i", "u", "s", "sub", "sup",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "nav", "main", "header", "footer", "aside", "article",
    "details", "summary",
    "label", "input", "select", "option", "textarea", "form", "button",
    "svg", "path", "circle", "rect", "line", "polyline", "polygon",
    "text", "tspan", "g", "defs", "use", "symbol",
    "style", "link", "meta", "title", "head", "body", "html",
    "script", "noscript", "iframe",
]

# Build Category A regex.
# Match: ^(\s*)(tagname)(>| attr=)
# The tag name must be followed by '>' or an attribute pattern.
_full_tag_alts = "|".join(re.escape(t) for t in _FULL_TAGS)
_full_re = re.compile(
    r"^(\s*)(" + _full_tag_alts + r")" + _ATTR_INDICATOR
)

# Also match closing tags missing '<': /div>, /figure>, /h2>, etc.
_closing_re = re.compile(
    r"^(\s*)/(" + _full_tag_alts + r")\s*>"
)

# Broken HTML comments: line starts with !-- (from <!--)
_comment_re = re.compile(r"^(\s*)!--")

# Broken DOCTYPE
_doctype_re = re.compile(r"^(\s*)!DOCTYPE", re.IGNORECASE)

# Category B: partial tag names (first char(s) also consumed).
# (partial_fragment, restored_full_tag)
_PARTIAL_TAGS = [
    ("igure",      "figure"),
    ("igcaption",  "figcaption"),
    ("iv",         "div"),
    ("ection",     "section"),
    ("lockquote",  "blockquote"),
    ("eader",      "header"),
    ("ooter",      "footer"),
    ("itle",       "title"),
    ("ody",        "body"),
    ("tml",        "html"),
    ("trong",      "strong"),
    ("pan",        "span"),
    ("able",       "table"),
    ("head",       "thead"),   # ambiguous with <head>, but we require attr pattern
    ("etails",     "details"),
    ("ummary",     "summary"),
    ("ticle",      "article"),
    ("side",       "aside"),
    ("cript",      "script"),
    ("rame",       "iframe"),
]

# Build Category B regexes.
_partial_patterns = []
for frag, full_tag in _PARTIAL_TAGS:
    pat = re.compile(
        r"^(\s*)" + re.escape(frag) + _ATTR_INDICATOR
    )
    _partial_patterns.append((pat, frag, full_tag))

# Partial closing tags: e.g., "/igure>" from "</figure>"
_partial_closing_patterns = []
for frag, full_tag in _PARTIAL_TAGS:
    pat = re.compile(
        r"^(\s*)/" + re.escape(frag) + r"\s*>"
    )
    _partial_closing_patterns.append((pat, frag, full_tag))


def collect_html_files():
    """Gather all .html files under the scan directories, skipping _archive."""
    files = []
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for f in sorted(scan_dir.rglob("*.html")):
            if "_archive" in str(f):
                continue
            files.append(f)
    return files


def is_inside_pre_block(lines, line_idx):
    """Return True if line_idx is inside an unclosed <pre> block."""
    depth = 0
    for i in range(line_idx):
        depth += lines[i].count("<pre")
        depth -= lines[i].count("</pre")
    return depth > 0


def fix_line(line, lines, line_idx):
    """Check if a line has a broken HTML tag. Return fixed line or None."""
    stripped = line.lstrip()
    if not stripped or stripped.startswith("<"):
        return None

    # Skip lines inside <pre> blocks
    if is_inside_pre_block(lines, line_idx):
        return None

    leading_ws = line[: len(line) - len(stripped)]

    # Check broken HTML comments: !-- ...
    if _comment_re.match(line):
        return leading_ws + "<" + stripped

    # Check broken DOCTYPE
    if _doctype_re.match(line):
        return leading_ws + "<" + stripped

    # Check Category A: full tag name, missing only '<'
    m = _full_re.match(line)
    if m:
        return leading_ws + "<" + stripped

    # Check closing tags missing '<': /div>, /section>, etc.
    m = _closing_re.match(line)
    if m:
        return leading_ws + "<" + stripped

    # Check Category B: partial tag name (first char(s) also lost)
    for pat, frag, full_tag in _partial_patterns:
        pm = pat.match(line)
        if pm:
            # Replace partial fragment with full tag name
            rest = stripped[len(frag):]
            return leading_ws + "<" + full_tag + rest

    # Check partial closing tags
    for pat, frag, full_tag in _partial_closing_patterns:
        pm = pat.match(line)
        if pm:
            rest = stripped[1 + len(frag):]  # skip the '/' and frag
            return leading_ws + "</" + full_tag + rest

    return None


def scan_file(filepath, apply_fix=False):
    """Scan a single file for broken tags. Returns list of (line_no, before, after)."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    fixes = []

    for i, line in enumerate(lines):
        fixed_line = fix_line(line, lines, i)
        if fixed_line is not None and fixed_line != line:
            fixes.append((i + 1, line, fixed_line))
            if apply_fix:
                lines[i] = fixed_line

    if apply_fix and fixes:
        filepath.write_text("\n".join(lines), encoding="utf-8")

    return fixes


def main():
    parser = argparse.ArgumentParser(
        description="Find and fix HTML elements missing their opening '<'."
    )
    parser.add_argument(
        "--fix", action="store_true",
        help="Apply fixes (default is dry-run, report only)."
    )
    args = parser.parse_args()

    html_files = collect_html_files()
    total_fixes = 0
    files_affected = 0

    for filepath in html_files:
        fixes = scan_file(filepath, apply_fix=args.fix)
        if fixes:
            files_affected += 1
            rel = filepath.relative_to(BOOK_ROOT)
            print(f"\n{'FIXED' if args.fix else 'FOUND'}: {rel}")
            for line_no, before, after in fixes:
                print(f"  L{line_no}:")
                print(f"    - {before.strip()}")
                print(f"    + {after.strip()}")
            total_fixes += len(fixes)

    mode = "Fixed" if args.fix else "Would fix"
    print(f"\n{mode} {total_fixes} broken tag(s) across {files_affected} file(s).")
    print(f"Scanned {len(html_files)} HTML files total.")

    if not args.fix and total_fixes > 0:
        print("\nRe-run with --fix to apply changes.")

    return 0 if total_fixes == 0 or args.fix else 1


if __name__ == "__main__":
    sys.exit(main())
