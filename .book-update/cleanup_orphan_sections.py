#!/usr/bin/env python3
"""Clean up orphaned <section class="bibliography" id="bibliography"> wrappers.

These were left behind when an earlier standardization pass replaced the inner
content but did not match the outer section open tag (which had extra attrs).
The result is an unmatched <section ...> with no </section>.

This script removes those orphan wrappers (leaving the canonical
<div class="callout bibliography">...</div> in place).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
             "source_fix_backups", "pagefind", "templates", ".claude",
             ".book-update", "_concept-figs", ".html2epub_cache"}
SKIP_FILE_SUFFIX = ("-audit.md", "-report.md")

def should_skip(path):
    parts = path.parts
    for skip in SKIP_DIRS:
        if skip in parts:
            return True
    if "front-matter" in parts:
        return True
    name = path.name
    if name.endswith(SKIP_FILE_SUFFIX):
        return True
    if name.startswith("_tmp"):
        return True
    return False

# Match the orphan opening section tag right before a canonical callout
# Pattern: <section class="bibliography"...> (no immediate closing) followed by <div class="callout bibliography">
ORPHAN_OPEN_PAT = re.compile(
    r'<section class="bibliography"(?:\s+[^>]*)?>\s*(?=<div class="callout bibliography">)'
)

# After removing the open tag, there may be a stray </section> later in the file that
# was NOT matched to anything except the original open tag. We need to remove that too.
# But it's safer to do this in a pair: only remove section open if there's a corresponding
# trailing </section> before the next nav/footer/main close.

# Actually it's simpler: find <section class="bibliography"...><div class="callout bibliography">
# then find the </section> that wraps the same callout. The callout has a balanced closing </div>.
# The </section> should be RIGHT after the final </div> of the callout.

def find_balanced_div(text, start_idx):
    if not text[start_idx:start_idx+4] == "<div":
        return None
    depth = 0
    i = start_idx
    open_pat = re.compile(r'<div\b')
    close_pat = re.compile(r'</div>')
    while i < len(text):
        nopen = open_pat.search(text, i)
        nclose = close_pat.search(text, i)
        if nclose is None:
            return None
        if nopen is not None and nopen.start() < nclose.start():
            depth += 1
            i = nopen.end()
        else:
            depth -= 1
            i = nclose.end()
            if depth == 0:
                return i
    return None

def process_file(path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False
    original = text
    new_text = text

    # Look for the orphan pattern
    while True:
        m = re.search(r'(<section class="bibliography"(?:\s+[^>]*)?>)\s*(<div class="callout bibliography">)', new_text)
        if not m:
            break
        section_open = m.group(1)
        callout_start = m.start(2)
        # Find end of callout
        callout_end = find_balanced_div(new_text, callout_start)
        if callout_end is None:
            break
        # Find next </section> after callout_end. If it's right after the callout
        # (possibly with whitespace), remove the pair.
        after = new_text[callout_end:].lstrip()
        if after.startswith('</section>'):
            # Compute positions: remove section open at m.start(1) to m.end(1)+whitespace,
            # and the </section> at callout_end+ws to callout_end+ws+len('</section>')
            ws_after = new_text[callout_end:callout_end + len(new_text[callout_end:]) - len(after)]
            # Replace open
            new_text = (
                new_text[:m.start(1)]
                + new_text[m.end(1):callout_end]  # keep callout
                + new_text[callout_end + len(ws_after) + len('</section>'):]
            )
            continue
        # If no trailing </section>, just remove the open tag (the close was already inside)
        new_text = new_text[:m.start(1)] + new_text[m.end(1):]

    if new_text != original:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False

def main():
    edited = 0
    for path in ROOT.rglob("*.html"):
        if should_skip(path):
            continue
        if process_file(path):
            edited += 1
            print("FIXED:", str(path.relative_to(ROOT)))
    print(f"\nTotal orphan sections fixed: {edited}")

if __name__ == "__main__":
    main()
