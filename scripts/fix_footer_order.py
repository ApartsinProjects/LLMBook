"""
Fix pages where content appears after the footer element.
Moves stray content (callouts, whats-next, bibliography) to before the
chapter-nav block, so the page order is: content > nav > footer > </main>.
"""

import re
from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse")
SKIP_DIRS = {"vendor", "node_modules", ".git", "__pycache__", "scripts"}

def fix_file(fpath: Path) -> bool:
    text = fpath.read_text(encoding="utf-8", errors="ignore")

    # Find the footer block
    footer_match = re.search(r'([ \t]*<footer>.*?</footer>)', text, re.DOTALL)
    main_end_pos = text.find('</main>')
    if not footer_match or main_end_pos < 0:
        return False

    # Check for content between </footer> and </main>
    after_footer = text[footer_match.end():main_end_pos].strip()
    if not after_footer or after_footer.startswith('<!--'):
        return False

    # Find the nav.chapter-nav block before footer
    nav_match = re.search(
        r'([ \t]*<nav class="chapter-nav">.*?</nav>)',
        text[:footer_match.start()],
        re.DOTALL
    )

    # The stray content to relocate
    stray_content = text[footer_match.end():main_end_pos].rstrip()

    # Remove stray content from after footer
    new_text = text[:footer_match.end()] + "\n" + text[main_end_pos:]

    # Insert stray content before the nav block (or before footer if no nav)
    insert_before = nav_match.start() if nav_match else footer_match.start()
    new_text_before = new_text[:insert_before]
    new_text_after = new_text[insert_before:]
    new_text = new_text_before.rstrip() + "\n\n" + stray_content.strip() + "\n\n" + new_text_after.lstrip()

    fpath.write_text(new_text, encoding="utf-8")
    return True

def main():
    fixed = 0
    for fpath in sorted(ROOT.rglob("*.html")):
        parts = fpath.relative_to(ROOT).parts
        if any(p in SKIP_DIRS for p in parts):
            continue
        if fix_file(fpath):
            fixed += 1
            print(f"  Fixed: {fpath.relative_to(ROOT)}")

    print(f"\nDone: {fixed} files fixed.")

if __name__ == "__main__":
    main()
