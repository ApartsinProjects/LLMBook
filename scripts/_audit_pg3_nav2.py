"""Audit chapter index pages: chapter-nav prev/next via the real markup format."""
import os, re

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'
parts = [
    ('part-9-llm-evaluation-observability', 'IX', range(42, 47), {42:'evaluation-foundations', 43:'specialized-evaluation', 44:'online-eval-observability', 45:'tools-of-the-trade', 46:'llm-as-judge-automated-evaluation'}),
    ('part-10-llm-security-runtime-safety', 'X', range(47, 52), {47:'adversarial-security-red-team', 48:'guardrails-runtime-safety', 49:'agent-safety-autonomy', 50:'privacy-data-protection', 51:'tools-of-the-trade'}),
    ('part-11-llm-ethics-trust-governance', 'XI', range(52, 57), {52:'bias-fairness', 53:'regulation-compliance', 54:'watermarking-provenance', 55:'environmental-sustainability', 56:'responsible-ai-tools'}),
    ('part-12-llm-systems-at-scale', 'XII', range(57, 62), {57:'compute-planning', 58:'frontier-systems-hardware', 59:'distributed-training-systems', 60:'edge-on-device-llms', 61:'scale-tools'}),
]

# expected prev/next sequence
def expected(part_idx, ch):
    parts_list = parts
    part_name, _, chrange, _ = parts_list[part_idx]
    chrange_list = list(chrange)
    pos = chrange_list.index(ch)
    prev_ch = chrange_list[pos-1] if pos > 0 else None
    next_ch = chrange_list[pos+1] if pos+1 < len(chrange_list) else None
    return prev_ch, next_ch

for pi, (part, pnum, chrange, slugs) in enumerate(parts):
    print(f'\n=== {part} ===')
    for ch in chrange:
        slug = slugs[ch]
        idx = os.path.join(ROOT, part, f'module-{ch}-{slug}', 'index.html')
        if not os.path.exists(idx):
            print(f'  MISSING {idx}')
            continue
        with open(idx, encoding='utf-8') as fp:
            content = fp.read()
        # Match <a class="prev" href="..."><span class="nav-num">Chapter X</span><span class="nav-title">...</span></a>
        prev_m = re.search(r'<a class="prev" href="([^"]+)"[^>]*>([\s\S]*?)</a>', content)
        next_m = re.search(r'<a class="next" href="([^"]+)"[^>]*>([\s\S]*?)</a>', content)
        prev_ch_exp, next_ch_exp = expected(pi, ch)
        problems = []
        if prev_m:
            href = prev_m.group(1)
            num_m = re.search(r'class="nav-num">([^<]+)', prev_m.group(2))
            tit_m = re.search(r'class="nav-title">([^<]+)', prev_m.group(2))
            num = num_m.group(1) if num_m else '?'
            tit = tit_m.group(1) if tit_m else '?'
            actual_ch = None
            m = re.search(r'Chapter (\d+)', num)
            if m:
                actual_ch = int(m.group(1))
            # check href has correct module
            href_ch_m = re.search(r'module-(\d+)-', href)
            href_ch = int(href_ch_m.group(1)) if href_ch_m else None
            if prev_ch_exp is None:
                # crossing parts; just print
                print(f'Ch {ch}  prev (cross-part): num={num} href={href}')
            else:
                if actual_ch != prev_ch_exp:
                    problems.append(f'PREV LABEL wrong: shows "{num}", expected Chapter {prev_ch_exp}')
                if href_ch != prev_ch_exp:
                    problems.append(f'PREV HREF wrong: {href} (ch in href={href_ch}, expected {prev_ch_exp})')
        else:
            problems.append('NO prev link')
        if next_m:
            href = next_m.group(1)
            num_m = re.search(r'class="nav-num">([^<]+)', next_m.group(2))
            tit_m = re.search(r'class="nav-title">([^<]+)', next_m.group(2))
            num = num_m.group(1) if num_m else '?'
            tit = tit_m.group(1) if tit_m else '?'
            actual_ch = None
            m = re.search(r'Chapter (\d+)', num)
            if m:
                actual_ch = int(m.group(1))
            href_ch_m = re.search(r'module-(\d+)-', href)
            href_ch = int(href_ch_m.group(1)) if href_ch_m else None
            if next_ch_exp is None:
                print(f'Ch {ch}  next (cross-part): num={num} href={href}')
            else:
                if actual_ch != next_ch_exp:
                    problems.append(f'NEXT LABEL wrong: shows "{num}", expected Chapter {next_ch_exp}')
                if href_ch != next_ch_exp:
                    problems.append(f'NEXT HREF wrong: {href} (ch in href={href_ch}, expected {next_ch_exp})')
        else:
            problems.append('NO next link')
        if problems:
            print(f'Ch {ch}: {"; ".join(problems)}')
        else:
            print(f'Ch {ch}: OK')
