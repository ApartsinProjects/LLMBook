"""Fix broken xrefs created by the structural backfill.

Strategy: build a mapping of (part, section-number) -> actual_path. Then for
each broken xref, derive the section number from the broken path, search for
the actual file in the same part, and rewrite the href.
"""
import os
import re
import glob
import json


def index_sections():
    """Map (part_dir, section_number) -> actual relative path."""
    by_section = {}
    by_part_section = {}
    for f in glob.glob('part-*/module-*/section-*.html'):
        # Extract section number from filename (section-X.Y[a|b].html or similar)
        m = re.search(r'section-([\d\.\w]+)\.html', os.path.basename(f))
        if not m:
            continue
        num = m.group(1)
        norm = f.replace('\\', '/')
        parts = norm.split('/')
        part = parts[0]
        module = parts[1]
        by_section[num] = norm
        by_part_section[(part, num)] = norm
    return by_section, by_part_section


def find_replacement(broken_href, source_file):
    """Given a broken href (relative to source_file) try to find the right file.

    Returns either a new relative href or None if no replacement.
    """
    # Strip anchor
    if '#' in broken_href:
        head, anchor = broken_href.split('#', 1)
    else:
        head, anchor = broken_href, None

    # Compute the absolute target as the broken href would resolve to
    src_dir = os.path.dirname(source_file)
    abs_target = os.path.normpath(os.path.join(src_dir, head)).replace('\\', '/')

    # Try section number lookup
    m = re.search(r'section-([\d\.\w]+)\.html$', head)
    if not m:
        return None
    section_num = m.group(1)

    actual = by_section.get(section_num)
    if not actual:
        return None

    # Compute href relative to source_file's directory
    src_abs = os.path.abspath(source_file)
    src_dir_abs = os.path.dirname(src_abs)
    tgt_abs = os.path.abspath(actual)
    rel = os.path.relpath(tgt_abs, src_dir_abs).replace('\\', '/')
    if anchor:
        rel = rel + '#' + anchor
    return rel


# Load audit
d = json.load(open('audit.json'))
from backfill_content import CONTENT
touched = set(p.replace('/', os.sep) for p in CONTENT.keys())
touched.add(os.sep.join(['part-7-retrieval-information-extraction-with-llms', 'module-31-embeddings-vector-db', 'section-31.1b.html']))

by_section, by_part_section = index_sections()

# For each broken xref, fix the source file
fixes_per_file = {}
for i in d['issues']:
    if i['file'] in touched and i['check_id'] == 'BROKEN_XREF':
        msg = i.get('message','')
        m = re.search(r'href="([^"]+)"', msg)
        if not m: continue
        href = m.group(1)
        srcfile = i['file'].replace('\\', '/')
        new_href = find_replacement(href, srcfile)
        if new_href and new_href != href:
            fixes_per_file.setdefault(srcfile, []).append((href, new_href))

# Apply fixes
applied = 0
unresolved = 0
for srcfile, pairs in fixes_per_file.items():
    full = srcfile.replace('/', os.sep)
    if not os.path.exists(full):
        continue
    with open(full, 'r', encoding='utf-8') as f:
        html = f.read()
    changed = False
    for old, new in pairs:
        if old in html:
            html = html.replace(f'href="{old}"', f'href="{new}"')
            applied += 1
            changed = True
    if changed:
        with open(full, 'w', encoding='utf-8', newline='') as f:
            f.write(html)

# Report still-broken
still_broken_summary = {}
for srcfile, pairs in fixes_per_file.items():
    for old, new in pairs:
        if new is None:
            still_broken_summary.setdefault(old, []).append(srcfile)

print(f'Applied {applied} xref fixes across {len(fixes_per_file)} files')
# Also report which broken hrefs we could not resolve (had no section match)
unresolved_set = set()
for i in d['issues']:
    if i['file'] in touched and i['check_id'] == 'BROKEN_XREF':
        msg = i.get('message','')
        m = re.search(r'href="([^"]+)"', msg)
        if not m: continue
        href = m.group(1)
        srcfile = i['file'].replace('\\', '/')
        new = find_replacement(href, srcfile)
        if new is None:
            unresolved_set.add(href)
print(f'Unresolvable broken hrefs (section not found anywhere):')
for u in sorted(unresolved_set):
    print(f'  {u}')
