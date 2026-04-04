#!/usr/bin/env python3
"""Find and fix nested <a> tags inside <a class="section-card"> elements.
Browsers cannot nest anchors, so inner links break the card layout.
Strategy: find <span class="section-desc"> blocks and strip inner <a> tags."""
import glob, re

# Match section-desc spans that contain <a> tags
desc_pattern = re.compile(
    r'(<span class="section-desc">)(.*?)(</span>)',
    re.DOTALL
)
inner_link = re.compile(r'<a\s[^>]*>(.*?)</a>', re.DOTALL)

total_fixes = 0
files_fixed = 0

for f in sorted(glob.glob('part-*/module-*/index.html') +
                glob.glob('part-*/index.html') +
                glob.glob('front-matter/index.html') +
                glob.glob('appendices/*/index.html') +
                glob.glob('capstone/index.html')):
    content = open(f, 'r', encoding='utf-8').read()

    def fix_desc(m):
        global total_fixes
        opener = m.group(1)
        body = m.group(2)
        closer = m.group(3)
        links = inner_link.findall(body)
        if links:
            total_fixes += len(links)
            fixed_body = inner_link.sub(r'\1', body)
            return opener + fixed_body + closer
        return m.group(0)

    new_content = desc_pattern.sub(fix_desc, content)
    if new_content != content:
        open(f, 'w', encoding='utf-8').write(new_content)
        files_fixed += 1
        print(f'{f}: fixed nested links in section-desc')

print(f'\nTotal: {total_fixes} nested links removed in {files_fixed} files')
