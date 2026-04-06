"""Fix structural issues across all HTML files in LLMCourse.

Fixes applied (in order per file):
1. HEADER_NO_CLASS: Replace bare <header> with <header class="chapter-header">
2. NAV_MISSING: Insert <nav class="header-nav"> block after opening header tag
3. MAIN_DIV_CONTAINER: Replace <div class="container"> with <main class="content">
4. PART_LABEL_INLINE_STYLE: Remove inline style from part-label links
5. CHAPTER_LABEL_INLINE_STYLE: Remove inline style from chapter-label links
"""

import re
from pathlib import Path

BASE = Path(r"E:\Projects\LLMCourse")

EXCLUDE_DIRS = {"_scripts_archive", "node_modules", ".claude", ".git", "styles", "images", "scripts"}

# Directories to scan
SCAN_ROOTS = []
for p in BASE.iterdir():
    if p.is_dir() and p.name not in EXCLUDE_DIRS:
        if p.name.startswith("part-") or p.name in ("appendices", "front-matter"):
            SCAN_ROOTS.append(p)

# Also include root-level HTML files
ROOT_HTML = list(BASE.glob("*.html"))


def compute_relative_path(filepath: Path) -> str:
    """Compute relative path from the file back to BASE."""
    rel = filepath.parent.relative_to(BASE)
    parts = rel.parts
    if len(parts) == 0:
        return "."
    elif len(parts) == 1:
        return ".."
    elif len(parts) == 2:
        return "../.."
    elif len(parts) >= 3:
        return "/".join([".."] * len(parts))
    return "."


def make_nav_block(rel_path: str) -> str:
    """Create the standard nav block."""
    return (
        f'<nav class="header-nav">\n'
        f'    <a href="{rel_path}/index.html" class="book-title-link">'
        f'Building Conversational AI with LLMs and Agents</a>\n'
        f'    <a href="{rel_path}/toc.html" class="toc-link" title="Table of Contents">'
        f'<span class="toc-icon">&#9776;</span> Contents</a>\n'
        f'</nav>'
    )


def fix_file(filepath: Path) -> list[str]:
    """Apply all fixes to a single file. Returns list of fix names applied."""
    fixes = []
    content = filepath.read_text(encoding="utf-8")
    original = content

    # --- Fix 1: HEADER_NO_CLASS ---
    # Replace the first bare <header> (not <header class=...>) with <header class="chapter-header">
    # Only match <header> that is NOT followed by a class attribute already
    pattern_bare_header = re.compile(r"<header(?=\s*>)(\s*)>", re.IGNORECASE)
    match = pattern_bare_header.search(content)
    if match:
        content = content[:match.start()] + '<header class="chapter-header">' + content[match.end():]
        fixes.append("HEADER_NO_CLASS")

    # --- Fix 2: NAV_MISSING ---
    # Check if file has <header class="chapter-header"> but no <nav class="header-nav">
    has_chapter_header = 'class="chapter-header"' in content
    has_header_nav = 'class="header-nav"' in content

    if has_chapter_header and not has_header_nav:
        rel_path = compute_relative_path(filepath)
        nav_block = make_nav_block(rel_path)

        # Insert nav right after <header class="chapter-header">
        header_pattern = re.compile(r'(<header\s+class="chapter-header"\s*>)', re.IGNORECASE)
        m = header_pattern.search(content)
        if m:
            insert_pos = m.end()
            # Check what follows: newline?
            after = content[insert_pos:]
            if after.startswith("\n"):
                content = content[:insert_pos] + "\n" + nav_block + content[insert_pos:]
            else:
                content = content[:insert_pos] + "\n" + nav_block + "\n" + content[insert_pos:]
            fixes.append("NAV_MISSING")

    # --- Fix 3: MAIN_DIV_CONTAINER ---
    # Replace <div class="container"> with <main class="content">
    if '<div class="container">' in content:
        content = content.replace('<div class="container">', '<main class="content">', 1)

        # Find the matching closing </div> for the container.
        # Strategy: find the last </div> before <footer> or </body>
        # Look for </div> that appears right before <footer or before </body>
        # Pattern: </div> followed by whitespace then <footer or </body>
        close_pattern = re.compile(r"</div>(\s*(?:<footer|</body>))", re.IGNORECASE)
        m = close_pattern.search(content)
        if m:
            content = content[:m.start()] + "</main>" + m.group(1) + content[m.end():]
            fixes.append("MAIN_DIV_CONTAINER")

    # --- Fix 4: PART_LABEL_INLINE_STYLE ---
    # Remove style="..." from links inside <div class="part-label">
    part_label_pattern = re.compile(
        r'(<div\s+class="part-label"><a\s+href="[^"]*")\s+style="[^"]*"'
    )
    if part_label_pattern.search(content):
        content = part_label_pattern.sub(r'\1', content)
        fixes.append("PART_LABEL_STYLE")

    # --- Fix 5: CHAPTER_LABEL_INLINE_STYLE ---
    # Remove style="..." from links inside <div class="chapter-label">
    # Also handle <a ... class="chapter-num" style="...">
    chapter_label_pattern = re.compile(
        r'(<div\s+class="chapter-label"><a\s+href="[^"]*"(?:\s+class="[^"]*")?)\s+style="[^"]*"'
    )
    if chapter_label_pattern.search(content):
        content = chapter_label_pattern.sub(r'\1', content)
        fixes.append("CHAPTER_LABEL_STYLE")

    if content != original:
        filepath.write_text(content, encoding="utf-8")

    return fixes


def collect_html_files() -> list[Path]:
    """Collect all HTML files to process."""
    files = list(ROOT_HTML)
    for root_dir in SCAN_ROOTS:
        files.extend(root_dir.rglob("*.html"))
    return sorted(set(files))


def main():
    html_files = collect_html_files()
    print(f"Scanning {len(html_files)} HTML files...\n")

    counters: dict[str, int] = {}
    fixed_files = 0

    for fpath in html_files:
        fixes = fix_file(fpath)
        if fixes:
            fixed_files += 1
            rel = fpath.relative_to(BASE)
            print(f"  {rel}: {', '.join(fixes)}")
            for f in fixes:
                counters[f] = counters.get(f, 0) + 1

    print(f"\n{'='*60}")
    print(f"Summary: {fixed_files} files modified")
    for fix_name, count in sorted(counters.items()):
        print(f"  {fix_name}: {count}")
    print(f"  Total HTML files scanned: {len(html_files)}")


if __name__ == "__main__":
    main()
