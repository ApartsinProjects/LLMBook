"""Find broken hrefs per Part."""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

results = {}
parts = [d for d in os.listdir('.') if d.startswith('part-')]
for part in parts:
    for root, dirs, files in os.walk(part):
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f).replace('\\', '/')
            try:
                txt = open(path, encoding='utf-8').read()
            except Exception:
                continue
            for m in re.finditer(r'href="([^"#?]+)(\#[^"]*)?"', txt):
                href = m.group(1)
                if href.startswith(('http://', 'https://', 'mailto:', 'data:', 'javascript:')):
                    continue
                if not href:
                    continue
                base_dir = os.path.dirname(path)
                target = os.path.normpath(os.path.join(base_dir, href)).replace('\\', '/')
                if not os.path.exists(target):
                    # find line number
                    pos = m.start()
                    ln = txt.count('\n', 0, pos) + 1
                    results.setdefault(part, []).append((path, ln, href, target))

for part in sorted(results):
    print(f'\n=== {part}: {len(results[part])} broken hrefs ===')
    for p, ln, h, t in results[part][:25]:
        print(f'  {p}:{ln}  href="{h}"  -> {t}')
