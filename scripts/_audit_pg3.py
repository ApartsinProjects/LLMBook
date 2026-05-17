import os, re, sys

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'
parts = ['part-9-llm-evaluation-observability', 'part-10-llm-security-runtime-safety', 'part-11-llm-ethics-trust-governance', 'part-12-llm-systems-at-scale']

results = []
for part in parts:
    pdir = os.path.join(ROOT, part)
    for root, dirs, files in os.walk(pdir):
        for f in sorted(files):
            if not f.startswith('section-') or not f.endswith('.html'):
                continue
            full = os.path.join(root, f)
            m = re.match(r'section-(\d+)\.(\d+)\.html', f)
            if not m:
                continue
            ch, sec = int(m.group(1)), int(m.group(2))
            with open(full, encoding='utf-8') as fp:
                content = fp.read()
            stale_h2 = []
            stale_h3 = []
            for m2 in re.finditer(r'<h2[^>]*>([^<]*)', content):
                t = m2.group(1).strip()
                m3 = re.match(r'(\d+)\.(\d+)\.(\d+)', t)
                if m3:
                    a = int(m3.group(1))
                    if a != ch:
                        stale_h2.append(t[:50])
            for m2 in re.finditer(r'<h3[^>]*>([^<]*)', content):
                t = m2.group(1).strip()
                m3 = re.match(r'(\d+)\.(\d+)\.(\d+)', t)
                if m3:
                    a = int(m3.group(1))
                    if a != ch:
                        stale_h3.append(t[:50])
            stale_ids = []
            for m2 in re.finditer(r'id="(\d+)-(\d+)-(\d+)', content):
                if int(m2.group(1)) != ch:
                    stale_ids.append('{}-{}-{}'.format(m2.group(1), m2.group(2), m2.group(3)))
            if stale_h2 or stale_h3 or stale_ids:
                results.append((full, len(stale_h2), len(stale_h3), len(stale_ids), stale_h2[:2]+stale_h3[:2]+stale_ids[:2]))
for r in results:
    rel = r[0].replace(ROOT, '').lstrip('\\').replace('\\', '/')
    print(rel, 'H2', r[1], 'H3', r[2], 'IDs', r[3], r[4])
print('TOTAL stale files:', len(results))
