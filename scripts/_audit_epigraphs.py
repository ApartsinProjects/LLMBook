"""Audit every epigraph block for AI-agent compliance.

Pattern (canonical):
  <blockquote class="epigraph">
  <p>"...quote..."</p>
  <span class="agent-avatar-inline" style="background-color: #XXXXXX;">
    <img alt="AgentName" height="28" src=".../agents/SLUG.png" width="28"/>
  </span><cite>AgentName, <span class="agent-desc">Trait AI Agent</span></cite>
  </blockquote>

A compliant epigraph must have:
1. An <span class="agent-avatar-inline"> with an <img> child
2. A <cite> that contains <span class="agent-desc">...AI Agent</span>

Report violations + suggest fixes.
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs', 'agents'}

violations = []
agents_seen = defaultdict(int)

for p in sorted(ROOT.rglob('*.html')):
    if set(p.parts) & SKIP:
        continue
    text = p.read_text(encoding='utf-8')
    for m in re.finditer(r'<blockquote class="epigraph">([\s\S]*?)</blockquote>', text):
        block = m.group(1)
        rel = str(p.relative_to(ROOT)).replace('\\', '/')

        has_avatar = '<span class="agent-avatar-inline"' in block
        has_agent_desc = '<span class="agent-desc">' in block and 'AI Agent</span>' in block

        if has_avatar and has_agent_desc:
            agent_m = re.search(r'<cite>([A-Za-z0-9-]+),\s*<span class="agent-desc">', block)
            if agent_m:
                agents_seen[agent_m.group(1)] += 1
        else:
            cite_m = re.search(r'<cite>([\s\S]*?)</cite>', block)
            cite = cite_m.group(1).strip() if cite_m else '(no cite)'
            quote_m = re.search(r'<p>([\s\S]*?)</p>', block)
            quote = re.sub(r'<[^>]+>', '', quote_m.group(1)).strip()[:120] if quote_m else ''
            violations.append({
                'path': rel,
                'cite': re.sub(r'<[^>]+>', '', cite).strip(),
                'quote': quote,
                'has_avatar': has_avatar,
                'has_agent_desc': has_agent_desc,
            })

print(f'\n=== {len(violations)} epigraph violations found ===\n')
for v in violations:
    print(f'{v["path"]}')
    print(f'  cite: {v["cite"]!r}')
    print(f'  quote: {v["quote"][:100]!r}')
    print(f'  avatar={v["has_avatar"]}, agent-desc={v["has_agent_desc"]}')
    print()

print(f'\n=== Agent name frequencies ({len(agents_seen)} unique) ===\n')
for agent, count in sorted(agents_seen.items(), key=lambda x: -x[1]):
    print(f'  {agent}: {count}')
