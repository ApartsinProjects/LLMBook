"""Audit math rendering across the EPUB."""
import zipfile, re

EPUB = 'KDP/output/building-conversational-ai-llms-agents.epub'
OK_CLASS = 'class="katex katex-rendered"'
RAW_DOLLAR = re.compile(r'\$\$\s*\\?[A-Za-z]')
OLD_BROKEN = re.compile(r'class="katex-rendered[^"]*"')

with zipfile.ZipFile(EPUB) as z:
    chapters = [n for n in z.namelist()
                if n.startswith('EPUB/chapters/') and n.endswith('.xhtml')]
    n_with_math = 0
    n_old_format = 0
    raw_dollar_chapters = []
    total_proper = 0
    for ch in chapters:
        text = z.read(ch).decode('utf-8', errors='replace')
        proper = text.count(OK_CLASS)
        all_kr = len(OLD_BROKEN.findall(text))
        old_broken = all_kr - proper
        raw = bool(RAW_DOLLAR.search(text))
        if proper or all_kr:
            n_with_math += 1
        if old_broken > 0:
            n_old_format += 1
        if raw:
            raw_dollar_chapters.append(ch.split('/')[-1])
        total_proper += proper

print(f'Chapters with math: {n_with_math}')
print(f'Chapters with OLD broken wrapper class: {n_old_format}')
print(f'Total properly-classed math elements: {total_proper}')
print(f'Chapters with raw $$ leakage: {len(raw_dollar_chapters)}')
for c in raw_dollar_chapters[:10]:
    print(f'  {c}')
