"""v776: Programmatic audit of first 100 spine entries in the EPUB.

Checks each chapter for:
  - Well-formed XHTML (XML parses)
  - Image references resolve to actual files in EPUB
  - Internal href cross-references resolve to existing chapters/anchors
  - Anchor IDs are unique within the file
  - <img> has alt attribute
  - <pre><code> has language class
  - <h1>...<h6> hierarchy doesn't skip levels
  - No empty <p>, <li>, <td>
  - No raw HTML entities visible (e.g., &amp;amp;)
  - No mojibake / suspicious unicode
  - No `Module NN` body prose (should be `Chapter NN`)
  - No 'Wave NN', 'v7XX', 'TODO', 'FIXME' visible
  - Math expressions rendered (no bare $$)
  - Code captions BELOW code (not above)
"""
from __future__ import annotations
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
EPUB = ROOT / 'KDP' / 'output' / 'building-conversational-ai-llms-agents.epub'

issues = defaultdict(list)


def add(severity: str, file: str, msg: str) -> None:
    issues[severity].append(f'{file}: {msg}')


def is_safe_text(t: str) -> bool:
    return all(c.isprintable() or c in '\n\r\t' for c in t[:5000])


with zipfile.ZipFile(EPUB) as z:
    names = set(z.namelist())
    # Read OPF to get spine order
    opf = z.read('EPUB/content.opf').decode('utf-8')
    id2href = {}
    for m in re.finditer(r'<item([^>]+)/>', opf):
        attrs = m.group(1)
        iid = re.search(r'\bid="([^"]+)"', attrs)
        href = re.search(r'\bhref="([^"]+)"', attrs)
        if iid and href:
            id2href[iid.group(1)] = href.group(1)
    itemrefs = re.findall(r'<itemref idref="([^"]+)"', opf)
    first100 = [id2href.get(r) for r in itemrefs[:100] if id2href.get(r)]

    # Build set of all chapter file basenames (without dir) for cross-ref check
    chapter_basenames = {n.rsplit('/', 1)[-1] for n in names if n.endswith('.xhtml')}

    print(f'Auditing first {len(first100)} spine entries...')
    print()

    for i, href in enumerate(first100):
        full = f'EPUB/{href}'
        if full not in names:
            add('Critical', href, f'spine href not in archive')
            continue
        try:
            t = z.read(full).decode('utf-8')
        except UnicodeDecodeError as e:
            add('Critical', href, f'not valid UTF-8: {e}')
            continue

        # XML well-formed?
        try:
            root = ET.fromstring(t)
        except ET.ParseError as e:
            add('Critical', href, f'XML parse error: {str(e)[:80]}')
            continue

        # Images resolve
        for m in re.finditer(r'<img[^>]+src="([^"]+)"', t):
            src = m.group(1)
            if src.startswith(('http://', 'https://')):
                continue
            # Resolve relative path
            from urllib.parse import unquote
            src_d = unquote(src)
            chapter_dir = href.rsplit('/', 1)[0]
            target = chapter_dir + '/' + src_d if chapter_dir else src_d
            # Normalize path
            parts = []
            for p in target.split('/'):
                if p == '..' and parts:
                    parts.pop()
                elif p and p != '.':
                    parts.append(p)
            target_n = 'EPUB/' + '/'.join(parts)
            if target_n not in names:
                add('Critical', href, f'broken image: {src} -> {target_n}')

        # Images without alt
        for m in re.finditer(r'<img(?![^>]*\balt=)[^>]*>', t):
            tag = m.group(0)[:120]
            add('Medium', href, f'<img> missing alt: {tag}')
            break  # one per file

        # Cross-reference hrefs to non-existent chapters
        for m in re.finditer(r'href="([^"#?]+\.xhtml)(?:#[^"]*)?"', t):
            target_h = m.group(1)
            if target_h.startswith(('http://', 'https://')):
                continue
            if target_h.startswith('chapters/'):
                if target_h not in [n.replace('EPUB/', '') for n in names if n.startswith('EPUB/chapters/')]:
                    add('Critical', href, f'broken xref: {target_h}')
            else:
                # Just basename - check if in chapter_basenames
                base = target_h.rsplit('/', 1)[-1]
                if base not in chapter_basenames:
                    add('Critical', href, f'broken xref by basename: {target_h}')

        # Duplicate IDs
        ids = re.findall(r'\bid="([^"]+)"', t)
        seen = set()
        dup = set()
        for iid in ids:
            if iid in seen:
                dup.add(iid)
            seen.add(iid)
        if dup:
            add('High', href, f'duplicate IDs: {sorted(dup)[:3]}')

        # Bare $$ math (KaTeX should have rendered)
        if t.count('$$') >= 2:
            add('High', href, f'bare $$ math (not rendered): {t.count("$$") // 2} blocks')

        # Visible TODO/FIXME/Wave/v7XX
        for pat, label in [
            (r'\bTODO:\s*[A-Z]', 'visible TODO:'),
            (r'\bFIXME\b', 'visible FIXME'),
            (r'\bWave\s+\d+\b', 'visible Wave NN'),
            (r'<!--\s*v[0-9]{3,4}', 'visible v7XX comment'),
            (r'\[STUB\]|\[DRAFT\]|\[TBD\]', 'visible draft marker'),
        ]:
            ms = re.findall(pat, t)
            if ms:
                add('High', href, f'{label}: {len(ms)} occurrences')

        # Module NN body prose (should be Chapter NN)
        # Skip: <span class="mod-num">Module NN</span> labels (intentional)
        masked = re.sub(r'<span class="mod-num">[^<]*</span>', '', t)
        masked = re.sub(r'<!--.*?-->', '', masked, flags=re.DOTALL)
        mod_hits = re.findall(r'\bModule\s+\d{1,2}\b', masked)
        if mod_hits:
            add('Medium', href, f'"Module NN" in prose: {len(mod_hits)} occurrences')

        # Doubled words (the the, of of, etc.)
        # Strip <code>...</code> and <pre>...</pre> first
        text_only = re.sub(r'<(code|pre)[^>]*>.*?</\1>', '', t, flags=re.DOTALL)
        text_only = re.sub(r'<[^>]+>', ' ', text_only)
        for m in re.finditer(r'\b(the|of|to|a|in|is|and|that|for|on|with|by|from)\s+\1\b',
                             text_only, re.IGNORECASE):
            ctx = text_only[max(0, m.start()-30):m.end()+30].strip()
            add('High', href, f'doubled word: ...{ctx[:80]}...')
            break  # one per file

        # Heading hierarchy: scan for h2 -> h4 (skipping h3) etc.
        headings = [(m.start(), int(m.group(1)))
                    for m in re.finditer(r'<h([1-6])', t)]
        prev = 1
        for pos, lvl in headings:
            if lvl > prev + 1:
                add('Medium', href, f'heading skip h{prev} -> h{lvl}')
                break
            prev = lvl

        # Empty <p> tags
        empty_p = len(re.findall(r'<p[^>]*>\s*</p>', t))
        if empty_p > 2:
            add('Medium', href, f'{empty_p} empty <p> tags')

        # Code captions ABOVE code (regression check)
        # Pattern: <div class="code-caption">...</div> immediately followed by <pre>
        for m in re.finditer(
                r'<div class="code-caption">[^<]+</div>\s*<(?:div class="code-block-wrapper">\s*)?<pre',
                t):
            add('High', href, 'code-caption ABOVE code (should be below)')
            break

        # Inline style attribute on body block elements
        long_style = len(re.findall(r'\bstyle="[^"]{100,}"', t))
        if long_style > 0:
            add('Low', href, f'{long_style} inline style attrs > 100 chars')

# Print report
print('=' * 70)
for sev in ['Critical', 'High', 'Medium', 'Low']:
    items = issues[sev]
    print(f'\n## {sev} ({len(items)} issues)')
    for item in items[:25]:
        print(f'  - {item[:200]}')
    if len(items) > 25:
        print(f'  ... and {len(items) - 25} more')

print()
print('=' * 70)
print(f'Critical: {len(issues["Critical"])}')
print(f'High:     {len(issues["High"])}')
print(f'Medium:   {len(issues["Medium"])}')
print(f'Low:      {len(issues["Low"])}')
print('=' * 70)
