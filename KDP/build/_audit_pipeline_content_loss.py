"""Audit the build pipeline for any place content can be lost or
discarded. Reports decompose/extract/unwrap/filter patterns.
Run this BEFORE rebuild to know what the pipeline strips."""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SCAN_DIRS = ['KDP/build', 'KDP/html2epub/src']

PATTERNS = {
    'decompose':       r'\.decompose\(\)',
    'extract':         r'\.extract\(\)',
    'unwrap':          r'\.unwrap\(\)',
    'replace_with':    r'\.replace_with\(',
    'string.replace':  r'\.string\.replace_with',
    'css_display_none':r'display\s*:\s*none',
    'css_visibility':  r'visibility\s*:\s*hidden',
    'class_remove':    r'\bdel\s+\w+\[[\'"](?:class|id|style)[\'"]\]',
    're_sub_remove':   r"re\.sub\(\s*r?['\"][^'\"]*<[^'\"]+>",
    'manifest_drop':   r'(spine|manifest|fragment)_drop|drop_id',
    'skip_continue':   r'^\s*continue\b',
}

findings = {p: [] for p in PATTERNS}

for d in SCAN_DIRS:
    full_d = os.path.join(ROOT, d)
    for r, _, files in os.walk(full_d):
        for f in files:
            if not f.endswith('.py'):
                continue
            path = os.path.join(r, f)
            rel = path.replace(ROOT, '').replace(os.sep, '/').lstrip('/')
            try:
                lines = open(path, encoding='utf-8').readlines()
            except UnicodeDecodeError:
                continue
            for i, line in enumerate(lines, 1):
                for name, pat in PATTERNS.items():
                    if re.search(pat, line):
                        ctx = line.strip()[:140]
                        findings[name].append((rel, i, ctx))

def safe_print(s):
    print(s.encode('ascii', 'replace').decode('ascii'))

for name, hits in findings.items():
    safe_print(f'=== {name} ({len(hits)} hits) ===')
    seen_files = {}
    for rel, i, ctx in hits:
        seen_files[rel] = seen_files.get(rel, 0) + 1
        if seen_files[rel] <= 2:
            safe_print(f'  {rel}:{i}  {ctx}')
    print()
