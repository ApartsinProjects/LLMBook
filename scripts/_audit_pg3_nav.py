"""Audit chapter index pages: chapter-nav prev/next, meta/title, breadcrumb, section card description text."""
import os, re

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'
parts = [
    ('part-9-llm-evaluation-observability', 'IX', range(42, 47), {42:'evaluation-foundations', 43:'specialized-evaluation', 44:'online-eval-observability', 45:'tools-of-the-trade', 46:'llm-as-judge-automated-evaluation'}),
    ('part-10-llm-security-runtime-safety', 'X', range(47, 52), {47:'adversarial-security-red-team', 48:'guardrails-runtime-safety', 49:'agent-safety-autonomy', 50:'privacy-data-protection', 51:'tools-of-the-trade'}),
    ('part-11-llm-ethics-trust-governance', 'XI', range(52, 57), {52:'bias-fairness', 53:'regulation-compliance', 54:'watermarking-provenance', 55:'environmental-sustainability', 56:'responsible-ai-tools'}),
    ('part-12-llm-systems-at-scale', 'XII', range(57, 62), {57:'compute-planning', 58:'frontier-systems-hardware', 59:'distributed-training-systems', 60:'edge-on-device-llms', 61:'scale-tools'}),
]

for part, pnum, chrange, slugs in parts:
    print(f'\n=== {part} ===')
    for ch in chrange:
        slug = slugs[ch]
        idx = os.path.join(ROOT, part, f'module-{ch}-{slug}', 'index.html')
        if not os.path.exists(idx):
            print(f'  MISSING {idx}')
            continue
        with open(idx, encoding='utf-8') as fp:
            content = fp.read()
        # title, meta description
        title = re.search(r'<title>([^<]+)', content)
        meta = re.search(r'<meta content="([^"]+)" name="description"', content)
        h1 = re.search(r'<h1[^>]*>([^<]+)', content)
        # breadcrumb / part label
        partlbl = re.search(r'data-pagefind-meta="part">([^<]+)', content)
        # pagefind-meta chapter
        pfch = re.search(r'data-pagefind-meta="chapter">([^<]+)', content)
        # chapter-nav prev / next
        nav = re.findall(r'class="chapter-nav-link[^"]*"[^>]*href="([^"]+)"[^>]*>[^<]*<[^>]*>([^<]+)</', content)
        # alternative: parse "<a class=\"chapter-nav-link prev\"" or aria-label
        nav_alt = re.findall(r'<a[^>]*class="[^"]*chapter-nav[^"]*"[^>]*href="([^"]*)"[^>]*>([\s\S]{0,400}?)</a>', content)
        prev_next = []
        for href, body in nav_alt:
            label_match = re.search(r'(Chapter \d+[^<]*)', body)
            label = label_match.group(1).strip() if label_match else body[:60].strip().replace('\n', ' ')
            prev_next.append((href, label))
        print(f'Ch {ch} ({slug})')
        print(f'  title:  {title.group(1) if title else "??"}')
        print(f'  meta :  {(meta.group(1)[:120] + ("..." if len(meta.group(1))>120 else "")) if meta else "??"}')
        print(f'  H1   :  {h1.group(1) if h1 else "??"}')
        print(f'  part :  {partlbl.group(1) if partlbl else "??"}')
        print(f'  pfch :  {pfch.group(1) if pfch else "??"}')
        for href, label in prev_next:
            print(f'  nav  :  href={href}  label={label[:80]}')
