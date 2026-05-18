"""Dump all forward+stale findings without truncation."""
import sys
import re
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))
from prereq_audit import gather, PREREQ_BLOCK_RE, LINK_RE, TITLE_RE, visible, ROOT
from urllib.parse import unquote
from pathlib import Path

order_map = gather()
forward_findings = []
stale_findings = []

for p in sorted(order_map):
    try:
        html = p.read_text(encoding='utf-8', errors='replace')
    except OSError:
        continue
    my_order = order_map[p]
    rel = str(p.relative_to(ROOT)).replace('\\', '/')

    block_m = PREREQ_BLOCK_RE.search(html)
    if not block_m:
        continue

    block_html = block_m.group(1)
    for lm in LINK_RE.finditer(block_html):
        href = lm.group(1)
        link_text = visible(lm.group(2))
        if href.startswith(('http://', 'https://', 'mailto:')):
            continue
        target = (p.parent / unquote(href)).resolve()
        if target not in order_map:
            continue
        target_order = order_map[target]
        if target_order > my_order:
            forward_findings.append((rel, href, link_text, target_order, my_order))
        try:
            target_html = target.read_text(encoding='utf-8', errors='replace')
            tm = TITLE_RE.search(target_html)
            if tm:
                target_title = visible(tm.group(1))
                if (len(link_text) > 12
                        and not re.match(r'^(?:Chapter|Section)\s+[\d.]+(?:\s+\(.+\))?$', link_text)
                        and link_text.lower() not in target_title.lower()
                        and target_title.lower() not in link_text.lower()):
                    text_words = set(re.findall(r'\b\w{4,}\b', link_text.lower()))
                    title_words = set(re.findall(r'\b\w{4,}\b', target_title.lower()))
                    if text_words and not (text_words & title_words):
                        stale_findings.append((rel, href, link_text, target_title))
        except OSError:
            pass

# Write CSV-like output
out_path = ROOT / 'docs' / 'content-audit' / 'PREREQ_AUDIT_FULL.txt'
with out_path.open('w', encoding='utf-8') as f:
    f.write(f'FORWARD ({len(forward_findings)}):\n')
    for s, h, t, to, mo in forward_findings:
        f.write(f'  {s}|{h}|{t}|target={to}|self={mo}\n')
    f.write('\n')
    f.write(f'STALE ({len(stale_findings)}):\n')
    for s, h, t, tt in stale_findings:
        f.write(f'  {s}|{h}|{t}|{tt}\n')
print(f'Wrote {out_path}')
print(f'Forward: {len(forward_findings)}, Stale: {len(stale_findings)}')
