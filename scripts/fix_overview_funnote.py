"""Move <div class="callout fun-note"> blocks OUT of <div class="overview">.

Pattern (BAD):
  <div class="overview">
    <h2>Chapter Overview</h2>
    <p>...overview prose...</p>
    <div class="callout fun-note">...</div>   <-- inside overview
    <p>...more overview prose...</p>
  </div>

Fix: extract the fun-note and move it AFTER the </div> closing the overview.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fix_text(text: str) -> tuple[str, int]:
    fixes = 0
    # Find the <div class="overview">...</div> block
    # Use depth-counting because overviews can contain other divs.
    while True:
        i = text.find('<div class="overview">')
        if i == -1:
            break
        # Find matching </div>
        depth = 1
        j = i + len('<div class="overview">')
        while j < len(text) and depth > 0:
            open_idx = text.find('<div', j)
            close_idx = text.find('</div>', j)
            if close_idx == -1:
                return text, fixes
            if open_idx != -1 and open_idx < close_idx:
                depth += 1
                j = open_idx + 4
            else:
                depth -= 1
                j = close_idx + 6
        overview_end = j  # past </div>
        overview_body = text[i:overview_end]
        # Find any fun-note callout inside
        fn_re = re.compile(
            r'<div class="callout fun-note">.*?</div>\s*</div>',
            re.DOTALL,
        )
        # That regex assumes single-paragraph fun-note; do depth-count instead
        fn_start = overview_body.find('<div class="callout fun-note">')
        if fn_start == -1:
            # No fun-note in this overview, move on
            break
        # depth-count to find matching </div>
        fn_abs = i + fn_start
        depth = 1
        k = fn_abs + len('<div class="callout fun-note">')
        while k < len(text) and depth > 0:
            o = text.find('<div', k)
            c = text.find('</div>', k)
            if c == -1:
                return text, fixes
            if o != -1 and o < c:
                depth += 1
                k = o + 4
            else:
                depth -= 1
                k = c + 6
        fn_end = k  # past closing </div> of fun-note
        fn_block = text[fn_abs:fn_end].rstrip() + '\n'
        # Remove fun-note from inside overview
        # Eat trailing whitespace too
        rm_start = fn_abs
        rm_end = fn_end
        while rm_end < len(text) and text[rm_end] in ' \n\t':
            rm_end += 1
        text_no_fn = text[:rm_start] + text[rm_end:]
        # overview_end shifted by removal of fn_block
        new_overview_end = overview_end - (rm_end - rm_start)
        # Insert fn_block AFTER the overview's </div>
        text = text_no_fn[:new_overview_end] + '\n' + fn_block + text_no_fn[new_overview_end:]
        fixes += 1
    return text, fixes


def main():
    apply = '--apply' in sys.argv
    print(f"{'APPLY' if apply else 'DRY-RUN'}")
    total = 0
    files_changed = 0
    for f in ROOT.rglob('*.html'):
        if any(s in f.parts for s in ('_archive', 'node_modules', '.git',
                                       'pagefind', 'KDP', 'build', 'vendor',
                                       '.claude', '__pycache__', 'templates')):
            continue
        if f.name != 'index.html':
            continue
        if 'module-' not in str(f):
            continue
        text = f.read_text(encoding='utf-8')
        new_text, fixes = fix_text(text)
        if fixes:
            total += fixes
            files_changed += 1
            print(f'  {f.relative_to(ROOT)}: {fixes} fun-note(s) extracted')
            if apply:
                f.write_text(new_text, encoding='utf-8')
    print(f'\nFiles changed: {files_changed}, total fun-notes moved: {total}')


if __name__ == '__main__':
    main()
