#!/usr/bin/env python3
"""Fix malformed closing HTML tags: <\tag> -> </tag>"""
import glob, re

total = 0
fixed = 0
pattern = re.compile(r'<\\(\w+)>')

for f in sorted(glob.glob('part-*/module-*/**/*.html', recursive=True) +
                glob.glob('appendices/**/*.html', recursive=True) +
                glob.glob('front-matter/**/*.html', recursive=True) +
                glob.glob('capstone/**/*.html', recursive=True) +
                glob.glob('introduction*.html') +
                glob.glob('cover.html') + glob.glob('toc.html')):
    content = open(f, 'r', encoding='utf-8').read()
    matches = pattern.findall(content)
    if matches:
        new = pattern.sub(r'</\1>', content)
        open(f, 'w', encoding='utf-8').write(new)
        total += len(matches)
        fixed += 1
        print(f'{f}: {len(matches)} fixes ({matches[:5]})')

print(f'\nTotal: {total} malformed closing tags fixed in {fixed} files')
