"""Fix duplicated/double-emoji titles in key-takeaway callouts.

Pattern (BAD):
  <div class="callout-title">Key Takeaways: &#128204; Key Takeaways</div>
                            ^^^^^^^^^^^^^^^^^   ^   ^^^^^^^^^^^^^^^^^
                            CSS ::before adds icon already; text duplicates it.

Patterns to fix:
  - "Key Takeaways: <emoji-or-icon> Key Takeaways" -> "Key Takeaways"
  - "Key Takeaway: <emoji> Key Takeaway" -> "Key Takeaway"
  - Same pattern for other callout types (Note, Warning, Tip, Key Insight,
    Fun Fact, etc.)

CSS already adds an icon via ::before, so the emoji in the title text
is a double icon. The duplicated word is a separate bug from a copy-paste
template.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Match a callout-title where the text repeats with an icon between the
# words (any character that isn't a letter or whitespace, typically &#NNNN;
# HTML entities, emoji, or unicode glyphs).
DOUBLE_TITLE_RE = re.compile(
    r'(<div class="callout-title">)'
    r'([\w\s\']+):\s+'                # "Key Takeaways: "
    r'(?:&#x?[\w]+;|[\U0001F300-\U0001FAFF☀-➿✀-➿]+)\s+'
    r'\2'                             # SAME word again
    r'(\s*</div>)',
    re.UNICODE,
)


def main():
    apply = '--apply' in sys.argv
    print(f"{'APPLY' if apply else 'DRY-RUN'}")
    fixes = 0
    files = 0
    for f in ROOT.rglob('*.html'):
        if any(s in f.parts for s in ('_archive', 'node_modules', '.git',
                                       'pagefind', 'KDP', 'build', 'vendor',
                                       '.claude', '__pycache__', 'templates')):
            continue
        text = f.read_text(encoding='utf-8')
        new_text, n = DOUBLE_TITLE_RE.subn(r'\1\2\3', text)
        if n:
            files += 1
            fixes += n
            print(f'  {f.relative_to(ROOT)}: {n} dup title(s) fixed')
            if apply:
                f.write_text(new_text, encoding='utf-8')
    print(f'\nFiles changed: {files}, total fixes: {fixes}')


if __name__ == '__main__':
    main()
