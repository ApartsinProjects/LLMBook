"""Build target list with titles and check existing bibs."""
import re
import os

with open('bib_targets.txt', 'r') as f:
    paths = [line.strip() for line in f if line.strip()]

out_lines = []
for p in paths:
    unix_p = p.replace('\\', '/')
    if not os.path.exists(unix_p):
        print(f"MISSING: {unix_p}")
        continue
    with open(unix_p, 'r', encoding='utf-8') as f:
        content = f.read()
    title_m = re.search(r'<title>([^<]+)</title>', content)
    h1_m = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    title = title_m.group(1).strip() if title_m else ''
    h1 = h1_m.group(1).strip() if h1_m else ''
    has_bib = '<details class="bibliography-collapsible"' in content
    out_lines.append(f"{p} | {title} | {h1} | has_bib={has_bib}")

with open('targets_with_titles.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print(f"Total: {len(out_lines)}")
