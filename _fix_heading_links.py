#!/usr/bin/env python3
"""Strip hyperlinks from h1, h2, h3 headings.

Headings should not contain clickable links. This script replaces
<a ...>text</a> inside h1/h2/h3 with just the text content.
Preserves everything else (level badges, section numbers, etc).
"""
import glob, re

files = sorted(set(
    glob.glob('part-*/module-*/**/*.html', recursive=True) +
    glob.glob('appendices/**/*.html', recursive=True) +
    glob.glob('front-matter/**/*.html', recursive=True) +
    glob.glob('capstone/**/*.html', recursive=True) +
    glob.glob('introduction*.html')
))

total = 0
files_fixed = 0

# Match <a ...>text</a> inside heading tags
link_pattern = re.compile(r'<a\s[^>]*>(.*?)</a>', re.DOTALL)

for f in files:
    content = open(f, 'r', encoding='utf-8').read()
    original = content

    def strip_links_in_heading(m):
        global total
        tag_open = m.group(1)  # e.g. <h2 ...>
        inner = m.group(2)     # heading content
        tag_close = m.group(3) # e.g. </h2>

        # Count and strip links
        count = len(link_pattern.findall(inner))
        if count == 0:
            return m.group(0)

        total += count
        cleaned = link_pattern.sub(r'\1', inner)
        return tag_open + cleaned + tag_close

    content = re.sub(
        r'(<h[123][^>]*>)(.*?)(</h[123]>)',
        strip_links_in_heading,
        content,
        flags=re.DOTALL
    )

    if content != original:
        open(f, 'w', encoding='utf-8').write(content)
        files_fixed += 1
        count = len(link_pattern.findall(original)) - len(link_pattern.findall(content))
        # Recount properly
        orig_headings = re.findall(r'<h[123][^>]*>.*?</h[123]>', original, re.DOTALL)
        new_headings = re.findall(r'<h[123][^>]*>.*?</h[123]>', content, re.DOTALL)
        orig_links = sum(len(link_pattern.findall(h)) for h in orig_headings)
        new_links = sum(len(link_pattern.findall(h)) for h in new_headings)
        removed = orig_links - new_links
        if removed > 0:
            print(f'{f}: {removed} links removed from headings')

print(f'\nTotal: {total} links removed from headings in {files_fixed} files')
