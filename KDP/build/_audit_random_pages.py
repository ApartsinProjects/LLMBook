"""Random sample 20 chapters and check for common issues."""
import random, zipfile, re
from pathlib import Path

EPUB = Path('KDP/output/building-conversational-ai-llms-agents.optimized.epub')
random.seed(42)

with zipfile.ZipFile(EPUB) as z:
    chapters = sorted(n for n in z.namelist() if n.startswith('EPUB/chapters/') and n.endswith('.xhtml'))
    sample = random.sample(chapters, 20)

    issues_per_chapter = {}
    for ch in sample:
        text = z.read(ch).decode('utf-8', errors='replace')
        issues = []

        # 1. Raw $...$ math escaped to surface
        if re.search(r'(?<!\\)\$\$(?!\s*\$)', text):
            n = len(re.findall(r'(?<!\\)\$\$', text))
            issues.append(f'raw $$ math markers: {n}')
        if re.search(r'\$[A-Za-z][A-Za-z0-9_]+\$', text):
            n = len(re.findall(r'\$[A-Za-z][A-Za-z0-9_]+\$', text))
            issues.append(f'raw $...$ inline math: {n}')

        # 2. Broken anchor refs: <a href="#xxx"> with no matching id="xxx"
        ids = set(re.findall(r'\bid="([^"]+)"', text))
        for href in re.findall(r'href="#([^"]+)"', text):
            if href not in ids:
                issues.append(f'orphan anchor: #{href}')
                break  # only first

        # 3. Empty/broken <img> (no src or src empty)
        for m in re.finditer(r'<img[^>]*>', text):
            if 'src=""' in m.group(0) or 'src=' not in m.group(0):
                issues.append('img with empty/missing src')
                break

        # 4. Suspect literal HTML entities still showing as text
        if re.search(r'&amp;(amp|lt|gt|quot|apos)(?![a-zA-Z;])', text):
            issues.append('double-escaped entities (&amp;amp etc.)')

        # 5. Code blocks with leading/trailing whitespace runs (formatting bug)
        for m in re.finditer(r'<pre>\s*<code[^>]*>(.*?)</code>\s*</pre>', text, re.DOTALL):
            body = m.group(1)
            if body and len(body) > 20 and body.strip() == '':
                issues.append('empty code block')
                break

        # 6. Wisdom-council orphan refs (after the slim, links should point to real ids)
        for m in re.finditer(r'wisdom-council\.xhtml#([a-z\-]+)', text):
            # check if it's a kept agent
            kept = {'deploy','guard','eval','compass','sage','frontier','agent-x','pip'}
            if m.group(1) not in kept and m.group(1) != '':
                issues.append(f'wisdom-council ref to dropped agent: #{m.group(1)}')
                break

        # 7. Image filename appears in text but no <img> tag (broken render)
        for m in re.finditer(r'(fig-[\d\.]+-[a-z\-]+\.png)', text):
            if not re.search(r'<img[^>]*src="[^"]*' + re.escape(m.group(1)), text):
                # might be reference in text — flag low priority
                pass

        # 8. Doubled spaces (suggests formatting issue)
        # only flag if many doubles in body text
        body_text = re.sub(r'<[^>]+>', '', text)
        n_doubled = len(re.findall(r'  +', body_text))
        if n_doubled > 30:
            issues.append(f'doubled spaces in body: {n_doubled}')

        if issues:
            issues_per_chapter[ch] = issues

print(f'Sampled 20 chapters from {EPUB.name}')
print(f'Chapters with issues: {len(issues_per_chapter)} / 20')
print()
for ch, iss in issues_per_chapter.items():
    short = ch.split('/')[-1].replace('ch_', '').replace('.xhtml', '')
    print(f'  {short}')
    for i in iss[:3]:
        print(f'    - {i}')
    if len(iss) > 3:
        print(f'    ... and {len(iss)-3} more')
