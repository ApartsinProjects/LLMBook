"""8th edition: fix all <main>-placement bugs detected by v703.

Strategy per file:
1. Find the FIRST </main>. If content after it (before </body>) contains
   any of: chapter-nav, footer, bibliography, whats-next, lab,
   Exercises h2 -> the </main> is misplaced. Remove it.
2. Inject a single </main> right before the first <script> tag (or
   before </body> if no script).
3. Deduplicate <footer> tags: if >1 <footer> exists in the file, keep
   only the LAST one (which is the canonical one right before </main>).

Idempotent: re-running on a clean file does nothing.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/',
        'templates/', '_archive/', 'temp_epub/', 'vendor/', '/agents/')

LEAK_PATTERNS = [
    re.compile(r'<section[^>]*class="bibliography"', re.IGNORECASE),
    re.compile(r'<div[^>]*class="whats-next"', re.IGNORECASE),
    re.compile(r'<div[^>]*class="lab"', re.IGNORECASE),
    re.compile(r'<h2[^>]*>\s*Exercises\s*</h2>', re.IGNORECASE),
    re.compile(r'<div[^>]*class="callout exercise"', re.IGNORECASE),
    re.compile(r'<nav[^>]*class="chapter-nav"', re.IGNORECASE),
    re.compile(r'<footer', re.IGNORECASE),
]

MAIN_CLOSE = re.compile(r'</main\s*>', re.IGNORECASE)
SCRIPT_OPEN = re.compile(r'<script\b', re.IGNORECASE)
BODY_CLOSE = re.compile(r'</body\s*>', re.IGNORECASE)
FOOTER_BLOCK = re.compile(r'<footer[^>]*>[\s\S]*?</footer>', re.IGNORECASE)


def has_leak(tail: str) -> bool:
    # Strip scripts/styles before testing
    cleaned = re.sub(r'<script[\s\S]*?</script>', '', tail,
                     flags=re.IGNORECASE)
    cleaned = re.sub(r'<style[\s\S]*?</style>', '', cleaned,
                     flags=re.IGNORECASE)
    return any(pat.search(cleaned) for pat in LEAK_PATTERNS)


def fix_one(text: str) -> tuple[str, bool]:
    m = MAIN_CLOSE.search(text)
    if not m:
        return text, False
    body = BODY_CLOSE.search(text)
    if not body:
        return text, False
    tail = text[m.end():body.start()]
    if not has_leak(tail):
        # </main> placement is fine; but we may still need to dedupe footers.
        return _dedupe_footers(text), False  # report unchanged unless dedup

    # Remove the first </main>
    new = text[:m.start()] + text[m.end():]
    # Find insertion point for new </main>: right before first <script>
    # after the leak content, OR before </body>.
    body2 = BODY_CLOSE.search(new)
    # Look for </footer> closest to body close; insert </main> after it.
    last_footer = None
    for fm in FOOTER_BLOCK.finditer(new):
        last_footer = fm
    if last_footer and last_footer.end() < body2.start():
        insert_at = last_footer.end()
    else:
        # Insert before the first <script> that appears before </body>,
        # or before </body> itself.
        script_m = None
        for sm in SCRIPT_OPEN.finditer(new):
            if sm.start() < body2.start():
                script_m = sm
                break
        insert_at = script_m.start() if script_m else body2.start()
    new = new[:insert_at] + '\n</main>\n' + new[insert_at:]
    return _dedupe_footers(new), True


def _dedupe_footers(text: str) -> str:
    """If >1 <footer>...</footer> blocks exist between <main> and </main>,
    keep only the LAST one."""
    # Find all footer blocks
    footers = list(FOOTER_BLOCK.finditer(text))
    if len(footers) <= 1:
        return text
    # Keep the last; drop earlier ones.
    out = []
    last_end = 0
    for fm in footers[:-1]:
        out.append(text[last_end:fm.start()])
        last_end = fm.end()
    out.append(text[last_end:])
    return ''.join(out)


def main() -> int:
    fix = '--fix' in sys.argv
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP):
            continue
        try:
            text = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        new, changed = fix_one(text)
        if new != text:
            n_files += 1
            print(f'  {"fixed" if fix else "would fix"}: {p.relative_to(ROOT)}')
            if fix:
                p.write_text(new, encoding='utf-8')
    print(f'\nFiles {"changed" if fix else "needing change"}: {n_files}')
    if not fix:
        print('Re-run with --fix to apply.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
