#!/usr/bin/env python3
"""Strip inline arrow entities from chapter-nav links.

CSS pseudo-elements now handle arrows, so HTML arrows create duplicates.
Removes: &larr; &rarr; ← → and leading/trailing whitespace around them.
"""
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

    # Only modify content inside <nav class="chapter-nav"> ... </nav> blocks
    def fix_nav_block(m):
        global total
        block = m.group(0)
        count = 0

        # Remove leading arrows from link text: >&larr; text</a> or >← text</a>
        def strip_leading(match):
            nonlocal count
            before = match.group(1)  # <a ...>
            arrow_space = match.group(2)  # arrow + whitespace
            text = match.group(3)  # remaining text
            count += 1
            return before + text

        block = re.sub(
            r'(<a[^>]*>)\s*(?:&larr;|&lArr;|\u2190|\u21D0|←)\s*(.*?)(</a>)',
            lambda m: m.group(1) + m.group(2).strip() + m.group(3),
            block, flags=re.DOTALL
        )

        # Remove trailing arrows: text &rarr;</a> or text →</a>
        block = re.sub(
            r'(<a[^>]*>)(.*?)\s*(?:&rarr;|&rArr;|\u2192|\u21D2|→)\s*(</a>)',
            lambda m: m.group(1) + m.group(2).strip() + m.group(3),
            block, flags=re.DOTALL
        )

        return block

    content = re.sub(
        r'<nav\s+class="chapter-nav"[^>]*>.*?</nav>',
        fix_nav_block, content, flags=re.DOTALL
    )

    # Also handle <div class="chapter-nav">
    content = re.sub(
        r'<div\s+class="chapter-nav"[^>]*>.*?</div>',
        fix_nav_block, content, flags=re.DOTALL
    )

    if content != original:
        open(f, 'w', encoding='utf-8').write(content)
        files_fixed += 1
        # Count arrows removed
        arrows_removed = original.count('&larr;') + original.count('&rarr;') + original.count('←') + original.count('→')
        arrows_remaining = content.count('&larr;') + content.count('&rarr;') + content.count('←') + content.count('→')
        removed = arrows_removed - arrows_remaining
        total += removed
        if removed > 0:
            print(f'{f}: {removed} arrows removed')

print(f'\nTotal: {total} arrows removed in {files_fixed} files')
