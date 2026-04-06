"""
Update internal navigation links that pointed to root index.html (the ToC)
to now point to toc.html, since root index.html is now a cover/landing page.

Rules:
- ../../index.html  in files at depth 2 (part/module/ or appendices/appendix/) -> ../../toc.html
- ../index.html     in files at depth 1 (capstone/) that are "back to book" links -> ../toc.html
- index.html        in root-level files (team.html, introduction.html) -> toc.html

DO NOT change:
- ../index.html in depth-2 files (those point to part-level index, not root)
- index.html in depth-2 section files (those point to chapter index)
- index.html in cover.html or toc.html
- Non-HTML files
"""

import os
import re
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")

# Track changes
changes = []
total_replacements = 0


def get_depth(filepath):
    """Get directory depth relative to ROOT."""
    rel = filepath.relative_to(ROOT)
    return len(rel.parts) - 1  # subtract the filename itself


def process_file(filepath):
    global total_replacements

    rel = filepath.relative_to(ROOT)
    depth = get_depth(filepath)
    fname = filepath.name

    # Skip non-HTML
    if filepath.suffix != '.html':
        return

    # Skip toc.html and index.html at root (the cover page)
    if depth == 0 and fname in ('toc.html', 'index.html', 'cover.html'):
        return

    content = filepath.read_text(encoding='utf-8')
    original = content
    file_changes = 0

    if depth >= 2:
        # Files at depth 2+: ../../index.html -> ../../toc.html (these resolve to root)
        pattern = r'href="../../index\.html"'
        replacement = 'href="../../toc.html"'
        count = len(re.findall(pattern, content))
        if count:
            content = re.sub(pattern, replacement, content)
            file_changes += count
            changes.append(f"  {rel}: ../../index.html -> ../../toc.html ({count}x)")

    if depth == 1:
        # Files at depth 1 (e.g., capstone/index.html, capstone/requirements.html):
        # ../index.html -> ../toc.html (these resolve to root)
        pattern = r'href="\.\./index\.html"'
        replacement = 'href="../toc.html"'
        count = len(re.findall(pattern, content))
        if count:
            content = re.sub(pattern, replacement, content)
            file_changes += count
            changes.append(f"  {rel}: ../index.html -> ../toc.html ({count}x)")

    if depth == 0:
        # Root-level files (team.html, introduction.html):
        # href="index.html" -> href="toc.html"
        pattern = r'href="index\.html"'
        replacement = 'href="toc.html"'
        count = len(re.findall(pattern, content))
        if count:
            content = re.sub(pattern, replacement, content)
            file_changes += count
            changes.append(f"  {rel}: index.html -> toc.html ({count}x)")

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        total_replacements += file_changes


# Walk through all HTML files
for html_file in sorted(ROOT.rglob('*.html')):
    # Skip hidden dirs, agent dirs, __pycache__, etc.
    rel_parts = html_file.relative_to(ROOT).parts
    if any(p.startswith('.') or p.startswith('__') or p == 'agents' or p == '_lab_fragments' for p in rel_parts):
        continue
    process_file(html_file)

print(f"Total replacements: {total_replacements}")
print(f"Files modified: {len(changes)}")
print()
for c in sorted(changes):
    print(c)
