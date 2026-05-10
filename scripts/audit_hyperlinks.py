#!/usr/bin/env python3
"""Audit internal hyperlinks across all HTML files in the book project.

Scans HTML files, extracts <a href="..."> links, resolves relative paths,
and reports broken file references and missing fragment (anchor) targets.

Output: scripts/hyperlink_audit_report.txt
"""

import glob
import os
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

GLOB_PATTERNS = [
    "part-*/module-*/section-*.html",
    "part-*/module-*/index.html",
    "part-*/index.html",
    "appendices/appendix-*/section-*.html",
    "appendices/appendix-*/index.html",
    "appendices/index.html",
    "front-matter/*.html",
    "front-matter/pathways/*.html",
    "front-matter/syllabi/*.html",
    "toc.html",
    "index.html",
]


def discover_files():
    """Return a sorted list of HTML files matching the project patterns."""
    files = set()
    for pattern in GLOB_PATTERNS:
        for match in glob.glob(str(ROOT / pattern)):
            files.add(Path(match).resolve())
    return sorted(files)


# ---------------------------------------------------------------------------
# Link extraction (with line numbers)
# ---------------------------------------------------------------------------

_HREF_RE = re.compile(r"""<a\s[^>]*?href\s*=\s*["']([^"']*?)["']""", re.IGNORECASE)


def extract_links(filepath: Path):
    """Yield (line_number, href) tuples for every <a href="..."> in the file."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in _HREF_RE.finditer(line):
            yield lineno, m.group(1)


# ---------------------------------------------------------------------------
# ID extraction (for fragment checking)
# ---------------------------------------------------------------------------

_ID_RE = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""", re.IGNORECASE)

_id_cache: dict[Path, set[str]] = {}


def get_ids(filepath: Path) -> set[str]:
    """Return the set of id attribute values defined in a file (cached)."""
    resolved = filepath.resolve()
    if resolved not in _id_cache:
        ids = set()
        try:
            text = resolved.read_text(encoding="utf-8", errors="replace")
            for m in _ID_RE.finditer(text):
                ids.add(m.group(1))
        except OSError:
            pass
        _id_cache[resolved] = ids
    return _id_cache[resolved]


# ---------------------------------------------------------------------------
# Pattern detection helpers
# ---------------------------------------------------------------------------

_ZERO_PAD_SECTION = re.compile(r"section-0\d+\.\d+")
_ZERO_PAD_MODULE = re.compile(r"module-0\d+")


def detect_patterns(href: str):
    """Return a list of pattern warnings for the given href."""
    warnings = []
    if _ZERO_PAD_SECTION.search(href):
        warnings.append("zero-padded section number (e.g. section-07.1 instead of section-7.1)")
    if _ZERO_PAD_MODULE.search(href):
        warnings.append("zero-padded module number (e.g. module-07 instead of module-7)")
    return warnings


# ---------------------------------------------------------------------------
# Main audit logic
# ---------------------------------------------------------------------------

SKIP_PREFIXES = ("http://", "https://", "mailto:", "javascript:")


def audit():
    files = discover_files()
    print(f"Discovered {len(files)} HTML files to scan.")

    total_internal = 0
    broken_files = []      # (source, lineno, href, pattern_warnings)
    broken_fragments = []  # (source, lineno, href, fragment)
    pattern_warnings = []  # (source, lineno, href, warnings)

    for filepath in files:
        for lineno, href in extract_links(filepath):
            # Skip external and anchor-only links
            if not href or href.startswith("#"):
                continue
            if any(href.startswith(p) for p in SKIP_PREFIXES):
                continue

            total_internal += 1

            # Split off fragment
            if "#" in href:
                path_part, fragment = href.split("#", 1)
            else:
                path_part, fragment = href, None

            # Detect suspicious patterns regardless of whether link is broken
            pw = detect_patterns(href)
            if pw:
                pattern_warnings.append((filepath, lineno, href, pw))

            # If path_part is empty, the link is just a fragment on the same page
            if not path_part:
                if fragment:
                    ids = get_ids(filepath)
                    if fragment not in ids:
                        broken_fragments.append((filepath, lineno, href, fragment))
                continue

            # Resolve relative path
            target = (filepath.parent / path_part).resolve()

            if not target.is_file():
                broken_files.append((filepath, lineno, href, pw))
            elif fragment:
                ids = get_ids(target)
                if fragment not in ids:
                    broken_fragments.append((filepath, lineno, href, fragment))

    return total_internal, broken_files, broken_fragments, pattern_warnings


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def write_report(total, broken_files, broken_fragments, pattern_warnings):
    lines = []
    lines.append("=" * 72)
    lines.append("HYPERLINK AUDIT REPORT")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"Total internal links checked: {total}")
    lines.append(f"Broken links (file not found): {len(broken_files)}")
    lines.append(f"Broken fragments (id not found): {len(broken_fragments)}")
    lines.append(f"Suspicious patterns detected: {len(pattern_warnings)}")
    lines.append("")

    if broken_files:
        lines.append("-" * 72)
        lines.append("BROKEN LINKS (target file does not exist)")
        lines.append("-" * 72)
        for src, lineno, href, pw in broken_files:
            rel = src.relative_to(ROOT)
            lines.append(f"  {rel}:{lineno}")
            lines.append(f"    href: {href}")
            if pw:
                for w in pw:
                    lines.append(f"    pattern: {w}")
        lines.append("")

    if broken_fragments:
        lines.append("-" * 72)
        lines.append("BROKEN FRAGMENTS (file exists, but id/anchor not found)")
        lines.append("-" * 72)
        for src, lineno, href, frag in broken_fragments:
            rel = src.relative_to(ROOT)
            lines.append(f"  {rel}:{lineno}")
            lines.append(f"    href: {href}")
            lines.append(f"    missing id: #{frag}")
        lines.append("")

    if pattern_warnings:
        lines.append("-" * 72)
        lines.append("SUSPICIOUS PATTERNS (may indicate link issues)")
        lines.append("-" * 72)
        for src, lineno, href, pw in pattern_warnings:
            rel = src.relative_to(ROOT)
            lines.append(f"  {rel}:{lineno}")
            lines.append(f"    href: {href}")
            for w in pw:
                lines.append(f"    pattern: {w}")
        lines.append("")

    if not broken_files and not broken_fragments and not pattern_warnings:
        lines.append("No issues found. All internal links are valid.")
        lines.append("")

    lines.append("=" * 72)
    lines.append("END OF REPORT")
    lines.append("=" * 72)

    report_text = "\n".join(lines)
    report_path = ROOT / "scripts" / "hyperlink_audit_report.txt"
    report_path.write_text(report_text, encoding="utf-8")
    print(report_text)
    print(f"\nReport saved to: {report_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    total, broken_files, broken_fragments, pattern_warnings = audit()
    write_report(total, broken_files, broken_fragments, pattern_warnings)

    # Exit with error code if there are broken file links
    if broken_files:
        sys.exit(1)
    sys.exit(0)
