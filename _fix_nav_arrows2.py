#!/usr/bin/env python3
"""Strip remaining numeric HTML arrow entities from chapter-nav links.
Catches &#8592; &#8594; &#x2190; &#x2192; that the first script missed."""
import glob, re

files = sorted(set(
    glob.glob('part-*/module-*/**/*.html', recursive=True) +
    glob.glob('appendices/**/*.html', recursive=True) +
    glob.glob('front-matter/**/*.html', recursive=True) +
    glob.glob('capstone/**/*.html', recursive=True) +
    glob.glob('introduction*.html') +
    glob.glob('part-*/index.html')
))

total = 0
files_fixed = 0

for f in files:
    content = open(f, 'r', encoding='utf-8').read()
    original = content

    def fix_nav_block(m):
        block = m.group(0)
        # Remove numeric arrow entities
        block = re.sub(
            r'(<a[^>]*>)\s*(?:&#8592;|&#x2190;)\s*',
            r'\1',
            block
        )
        block = re.sub(
            r'\s*(?:&#8594;|&#x2192;)\s*(</a>)',
            r' \1',
            block
        )
        return block

    content = re.sub(
        r'<nav\s+class="chapter-nav"[^>]*>.*?</nav>',
        fix_nav_block, content, flags=re.DOTALL
    )
    content = re.sub(
        r'<div\s+class="chapter-nav"[^>]*>.*?</div>',
        fix_nav_block, content, flags=re.DOTALL
    )

    if content != original:
        open(f, 'w', encoding='utf-8').write(content)
        files_fixed += 1
        removed = (original.count('&#8592;') + original.count('&#8594;') +
                   original.count('&#x2190;') + original.count('&#x2192;')) - \
                  (content.count('&#8592;') + content.count('&#8594;') +
                   content.count('&#x2190;') + content.count('&#x2192;'))
        total += removed
        if removed > 0:
            print(f'{f}: {removed} arrows removed')

print(f'\nTotal: {total} arrows removed in {files_fixed} files')
