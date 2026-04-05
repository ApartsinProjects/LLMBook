"""
Shared utilities for drift-detection scripts.
Provides file discovery, HTML parsing, path resolution, and section number extraction.
"""

import os
import re
import glob as globmod
from html.parser import HTMLParser
from pathlib import Path

# ---------------------------------------------------------------------------
# Book root: default = repo root (two levels up from this script)
# ---------------------------------------------------------------------------
BOOK_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

SECTION_GLOBS = [
    "part-*/module-*/section-*.html",
    "appendices/*/section-*.html",
    "front-matter/section-*.html",
]

INDEX_GLOBS = [
    "part-*/index.html",
    "part-*/module-*/index.html",
    "appendices/*/index.html",
    "front-matter/index.html",
    "front-matter/pathways/index.html",
    "front-matter/syllabi/index.html",
]

ALL_HTML_GLOBS = [
    "part-*/**/*.html",
    "appendices/**/*.html",
    "front-matter/**/*.html",
    "index.html",
    "toc.html",
    "capstone/**/*.html",
]


def find_files(patterns, root=None):
    """Return sorted list of files matching any of the glob patterns."""
    root = Path(root or BOOK_ROOT)
    found = set()
    for pat in patterns:
        for f in globmod.glob(str(root / pat), recursive=True):
            fp = Path(f)
            # Skip agents/ and templates/
            if "agents" in fp.parts or "templates" in fp.parts:
                continue
            # Skip _archive
            if "_archive" in fp.parts:
                continue
            found.add(fp)
    return sorted(found)


def find_section_files(root=None):
    return find_files(SECTION_GLOBS, root)


def find_index_files(root=None):
    return find_files(INDEX_GLOBS, root)


def find_all_html(root=None):
    return find_files(ALL_HTML_GLOBS, root)


# ---------------------------------------------------------------------------
# HTML parsing helpers
# ---------------------------------------------------------------------------

class _TagExtractor(HTMLParser):
    """Extract specific information from HTML."""

    def __init__(self):
        super().__init__()
        self._capture_tag = None
        self._capture_depth = 0
        self._captured = []
        self.results = {}

    def _start_capture(self, tag):
        self._capture_tag = tag
        self._capture_depth = 1
        self._captured = []

    def handle_data(self, data):
        if self._capture_tag:
            self._captured.append(data)

    def handle_starttag(self, tag, attrs):
        if self._capture_tag and tag == self._capture_tag:
            self._capture_depth += 1

    def handle_endtag(self, tag):
        if self._capture_tag and tag == self._capture_tag:
            self._capture_depth -= 1
            if self._capture_depth <= 0:
                self._capture_tag = None


def read_file(path):
    """Read file contents, trying utf-8 then latin-1."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return Path(path).read_text(encoding="latin-1")


def extract_h1(html):
    """Extract the text content of the first <h1> tag."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return None


def extract_title(html):
    """Extract the <title> content."""
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return None


def extract_nav_links(html):
    """Extract prev, up, next links from <nav class="chapter-nav">."""
    nav_m = re.search(
        r'<nav\s+class="chapter-nav">(.*?)</nav>', html, re.DOTALL | re.IGNORECASE
    )
    if not nav_m:
        return None
    nav_html = nav_m.group(1)
    links = {}
    for cls in ("prev", "up", "next"):
        m = re.search(
            rf'<a\s+href="([^"]*)"[^>]*class="[^"]*{cls}[^"]*"', nav_html, re.IGNORECASE
        )
        if not m:
            m = re.search(
                rf'<a\s+[^>]*class="[^"]*{cls}[^"]*"[^>]*href="([^"]*)"', nav_html, re.IGNORECASE
            )
        if m:
            links[cls] = m.group(1)
    return links


def extract_all_links(html):
    """Extract all <a href="..."> links with their text."""
    results = []
    for m in re.finditer(r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL | re.IGNORECASE):
        href = m.group(1)
        text = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        results.append((href, text))
    return results


def extract_captions(html):
    """Extract figure/table/code/exercise captions with their numbers."""
    patterns = [
        (r"Figure\s+(\d+[\w.]*\d*)", "Figure"),
        (r"Table\s+(\d+[\w.]*\d*)", "Table"),
        (r"Code\s+(\d+[\w.]*\d*)", "Code"),
        (r"Listing\s+(\d+[\w.]*\d*)", "Listing"),
        (r"Exercise\s+(\d+[\w.]*\d*)", "Exercise"),
    ]
    captions = []
    for pat, kind in patterns:
        for m in re.finditer(pat, html):
            captions.append((kind, m.group(1), m.start()))
    return sorted(captions, key=lambda x: x[2])


def extract_part_label(html):
    """Extract part label text from <div class="part-label">."""
    m = re.search(r'<div\s+class="part-label"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    if m:
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        return text
    return None


def extract_chapter_label(html):
    """Extract chapter label text from <div class="chapter-label">."""
    m = re.search(r'<div\s+class="chapter-label"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    if m:
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        return text
    return None


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

def resolve_href(source_file, href):
    """Resolve a relative href from a source file to an absolute path."""
    if href.startswith(("http://", "https://", "mailto:", "javascript:", "#")):
        return None
    # Strip fragment
    href_no_frag = href.split("#")[0]
    if not href_no_frag:
        return None
    source_dir = Path(source_file).parent
    resolved = (source_dir / href_no_frag).resolve()
    return resolved


def href_fragment(href):
    """Extract the #fragment from an href, or None."""
    if "#" in href:
        return href.split("#", 1)[1]
    return None


# ---------------------------------------------------------------------------
# Section number extraction
# ---------------------------------------------------------------------------

def section_num_from_filename(filepath):
    """Extract section number from filename like section-9.2.html -> '9.2'."""
    name = Path(filepath).stem  # section-9.2
    m = re.match(r"section-(.+)", name)
    if m:
        return m.group(1)
    return None


def chapter_num_from_dirname(filepath):
    """Extract chapter number from module directory like module-09-slug -> 9."""
    parts = Path(filepath).parts
    for p in parts:
        m = re.match(r"module-(\d+)", p)
        if m:
            return int(m.group(1))
    return None


def part_num_from_dirname(filepath):
    """Extract part number from part directory like part-2-slug -> 2."""
    parts = Path(filepath).parts
    for p in parts:
        m = re.match(r"part-(\d+)", p)
        if m:
            return int(m.group(1))
    return None


def id_exists_in_html(html, fragment_id):
    """Check if an id attribute exists in the HTML."""
    pattern = rf'''id\s*=\s*["']{re.escape(fragment_id)}["']'''
    return bool(re.search(pattern, html))


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

class DriftReport:
    """Collect and format drift issues."""

    def __init__(self, category):
        self.category = category
        self.issues = []

    def error(self, source, msg, expected=None, actual=None):
        self.issues.append(("ERROR", source, msg, expected, actual))

    def warn(self, source, msg, expected=None, actual=None):
        self.issues.append(("WARN", source, msg, expected, actual))

    def info(self, source, msg, expected=None, actual=None):
        self.issues.append(("INFO", source, msg, expected, actual))

    def print_report(self):
        errors = sum(1 for i in self.issues if i[0] == "ERROR")
        warns = sum(1 for i in self.issues if i[0] == "WARN")
        infos = sum(1 for i in self.issues if i[0] == "INFO")

        print(f"\n{'=' * 60}")
        print(f"  {self.category}")
        print(f"{'=' * 60}")

        if not self.issues:
            print("  No issues found.")
        else:
            for sev, source, msg, expected, actual in self.issues:
                rel = _rel_path(source)
                print(f"  [{sev}] {rel}: {msg}")
                if expected is not None:
                    print(f"    Expected: {expected}")
                if actual is not None:
                    print(f"    Actual:   {actual}")

        print(f"\n  Summary: {len(self.issues)} issues "
              f"({errors} errors, {warns} warnings, {infos} info)")
        return errors, warns, infos


def _rel_path(p):
    """Make path relative to BOOK_ROOT for display."""
    try:
        return str(Path(p).relative_to(BOOK_ROOT))
    except ValueError:
        return str(p)
