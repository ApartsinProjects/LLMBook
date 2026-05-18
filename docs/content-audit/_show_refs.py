"""Show unlinked references organized by file for batch processing."""
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _xref_resolver import resolve_section, resolve_chapter, verify_path_exists

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'
findings = json.load(open(os.path.join(ROOT, 'docs', 'content-audit', '_xref_findings.json')))

# Group by file
by_file = defaultdict(lambda: {'sections': [], 'chapters': []})
for r in findings['unlinked_section_refs']:
    by_file[r['file']]['sections'].append(r)
for r in findings['unlinked_chapter_refs']:
    by_file[r['file']]['chapters'].append(r)

# Filter to files this agent should process
TARGETED_PREFIXES = sys.argv[1].split(',') if len(sys.argv) > 1 else []

def matches(f, prefixes):
    if not prefixes:
        return True
    f_norm = f.replace('\\', '/')
    return any(f_norm.startswith(p) for p in prefixes)

for f in sorted(by_file.keys()):
    if not matches(f, TARGETED_PREFIXES):
        continue
    sec = by_file[f]['sections']
    ch = by_file[f]['chapters']
    if not sec and not ch:
        continue
    print(f'\n==== {f} ====')
    print(f'  Sections ({len(sec)}):')
    for r in sec:
        href, verified, actual = resolve_section(f, r['section'])
        exists = verify_path_exists(f, href) if href else False
        ok = 'OK' if exists else 'MISS'
        print(f'    [{ok}] Section {r["section"]} -> {href} ({actual}) | {r["context"][:60]}')
    print(f'  Chapters ({len(ch)}):')
    for r in ch:
        href, verified = resolve_chapter(f, r['chapter'])
        exists = verify_path_exists(f, href) if href else False
        ok = 'OK' if exists else 'MISS'
        print(f'    [{ok}] Chapter {r["chapter"]} -> {href} | {r["context"][:60]}')
