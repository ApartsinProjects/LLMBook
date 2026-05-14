"""Find stale 'Section X.Y' references where X != current chapter and not a cross-chapter href."""
import os, re

issues=[]
for root, dirs, files in os.walk('.'):
    rn = root.replace('\\','/')
    if any(s in rn for s in ['KDP','node_modules','temp_epub','pagefind','_scripts_archive','templates','vendor']):
        continue
    if '/part-' not in rn:
        continue
    for f in files:
        if not f.startswith('section-') or not f.endswith('.html'):
            continue
        m = re.match(r'section-(\d+)\.', f)
        if not m: continue
        chap = int(m.group(1))
        path = os.path.join(root, f)
        try:
            with open(path, encoding='utf-8') as fh:
                txt = fh.read()
        except Exception:
            continue
        for ln, line in enumerate(txt.split('\n'),1):
            for sm in re.finditer(r'\bSection (\d+)\.(\d+)\b', line):
                refchap = int(sm.group(1))
                if refchap == chap:
                    continue
                ls = line
                if f'module-{refchap:02d}-' in ls or f'/section-{refchap}.' in ls:
                    continue
                issues.append((path, ln, ls.strip()[:240]))
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
print(f'Found {len(issues)} potential stale Section refs')
for p,l,s in issues[:200]:
    print(f'{p}:{l}: {s}')
