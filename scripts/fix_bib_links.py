#!/usr/bin/env python3
"""Find and fix bibliography entries missing hyperlinks."""
import os
import re
import sys

def find_files():
    files = []
    for root, dirs, fnames in os.walk('.'):
        dirs[:] = [d for d in dirs if d != '_archive']
        norm = root.replace(os.sep, '/')
        if 'part-10-frontiers' in norm:
            continue
        for f in fnames:
            if f.endswith('.html') and (f.startswith('section-') or f == 'index.html'):
                fp = os.path.join(root, f).replace(os.sep, '/')
                if '/part-' in fp or '/appendix' in fp or '/appendices/' in fp:
                    files.append(fp)
    return sorted(files)

def scan_missing_links(files):
    total_entries = 0
    total_missing = 0
    file_counts = {}
    missing_entries = []

    for fp in files:
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()
        for m in re.finditer(r'<p\s+class=[^>]*bib-ref[^>]*>', content):
            total_entries += 1
            start = m.start()
            end_p = content.find('</p>', start)
            if end_p < 0:
                continue
            block = content[start:end_p + 4]
            inner = content[m.end():end_p]
            if '<a href=' not in inner:
                total_missing += 1
                file_counts[fp] = file_counts.get(fp, 0) + 1
                clean = inner.strip().replace('\n', ' ').replace('\r', '')[:200]
                missing_entries.append((fp, start, end_p + 4, block, clean))
                print(f'{fp}: {clean}')

    print(f'\nTotal entries: {total_entries}, Missing links: {total_missing}')
    for fp, cnt in sorted(file_counts.items()):
        print(f'  {fp}: {cnt}')
    return missing_entries

if __name__ == '__main__':
    files = find_files()
    print(f'Found {len(files)} HTML files to scan')
    entries = scan_missing_links(files)
