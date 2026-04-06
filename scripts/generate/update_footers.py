"""
Update all HTML page footers to the standardized format:
  - Book title
  - Copyright + Contents link
  - Auto-updating last-modified date via JS

Also fixes agents/ pages that say "42-Agent" to "46-Agent".
Skips vendor/, node_modules/, .git/ directories.
"""

import re
import os
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")
SKIP_DIRS = {"vendor", "node_modules", ".git", "__pycache__", "scripts"}

# New footer template. {toc_path} will be replaced per file.
NEW_FOOTER = """    <footer>
        <p class="footer-title">Building Conversational AI with LLMs and Agents, Fifth Edition</p>
        <p>&copy; 2026 Alexander Apartsin &amp; Yehudit Aperstein &middot; <a href="{toc_path}">Contents</a></p>
        <p class="footer-updated">Last updated: <script>document.write(new Date(document.lastModified).toLocaleDateString('en-US', {{year:'numeric', month:'long', day:'numeric'}}))</script></p>
    </footer>"""

# Patterns to match existing footers
STANDARD_FOOTER_RE = re.compile(
    r'[ \t]*<footer>\s*<p>Fifth Edition, 2026 &middot; <a href="([^"]+)">Contents</a></p>\s*</footer>',
    re.DOTALL
)

AGENT_FOOTER_RE = re.compile(
    r'[ \t]*<footer>Part of the 4[26]-Agent Textbook Production Pipeline</footer>'
)

def compute_toc_path(html_file: Path) -> str:
    """Compute relative path from html_file to toc.html at root."""
    rel = html_file.parent.relative_to(ROOT)
    depth = len(rel.parts)
    if depth == 0:
        return "toc.html"
    return "../" * depth + "toc.html"

def process_file(fpath: Path) -> bool:
    """Update footer in a single HTML file. Returns True if modified."""
    text = fpath.read_text(encoding="utf-8")
    toc_path = compute_toc_path(fpath)
    replacement = NEW_FOOTER.format(toc_path=toc_path)

    new_text = text
    modified = False

    # Try standard footer first
    m = STANDARD_FOOTER_RE.search(new_text)
    if m:
        new_text = new_text[:m.start()] + replacement + new_text[m.end():]
        modified = True

    # Try agent footer
    if not modified:
        m = AGENT_FOOTER_RE.search(new_text)
        if m:
            new_text = new_text[:m.start()] + replacement + new_text[m.end():]
            modified = True

    if modified:
        fpath.write_text(new_text, encoding="utf-8")
    return modified

def main():
    updated = 0
    skipped = 0
    no_footer = []

    for fpath in sorted(ROOT.rglob("*.html")):
        # Skip excluded directories
        parts = fpath.relative_to(ROOT).parts
        if any(p in SKIP_DIRS for p in parts):
            continue

        if process_file(fpath):
            updated += 1
            print(f"  Updated: {fpath.relative_to(ROOT)}")
        else:
            # Check if file has any footer at all
            text = fpath.read_text(encoding="utf-8")
            if "<footer>" not in text:
                no_footer.append(str(fpath.relative_to(ROOT)))
            skipped += 1

    print(f"\nDone: {updated} files updated, {skipped} unchanged.")
    if no_footer:
        print(f"\nFiles with NO footer ({len(no_footer)}):")
        for f in no_footer:
            print(f"  {f}")

if __name__ == "__main__":
    main()
