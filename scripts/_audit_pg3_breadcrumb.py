"""Audit section breadcrumb chapter labels and section self-title."""
import os, re

ROOT = r'E:\Projects\BookBlogsHome\LLMBook'
parts = [
    ('part-9-llm-evaluation-observability', range(42, 47)),
    ('part-10-llm-security-runtime-safety', range(47, 52)),
    ('part-11-llm-ethics-trust-governance', range(52, 57)),
    ('part-12-llm-systems-at-scale', range(57, 62)),
]

# Canonical chapter titles per-chapter (from chapter index H1)
canonical = {}
slugs = {
    42:('part-9-llm-evaluation-observability','evaluation-foundations'),
    43:('part-9-llm-evaluation-observability','specialized-evaluation'),
    44:('part-9-llm-evaluation-observability','online-eval-observability'),
    45:('part-9-llm-evaluation-observability','tools-of-the-trade'),
    46:('part-9-llm-evaluation-observability','llm-as-judge-automated-evaluation'),
    47:('part-10-llm-security-runtime-safety','adversarial-security-red-team'),
    48:('part-10-llm-security-runtime-safety','guardrails-runtime-safety'),
    49:('part-10-llm-security-runtime-safety','agent-safety-autonomy'),
    50:('part-10-llm-security-runtime-safety','privacy-data-protection'),
    51:('part-10-llm-security-runtime-safety','tools-of-the-trade'),
    52:('part-11-llm-ethics-trust-governance','bias-fairness'),
    53:('part-11-llm-ethics-trust-governance','regulation-compliance'),
    54:('part-11-llm-ethics-trust-governance','watermarking-provenance'),
    55:('part-11-llm-ethics-trust-governance','environmental-sustainability'),
    56:('part-11-llm-ethics-trust-governance','responsible-ai-tools'),
    57:('part-12-llm-systems-at-scale','compute-planning'),
    58:('part-12-llm-systems-at-scale','frontier-systems-hardware'),
    59:('part-12-llm-systems-at-scale','distributed-training-systems'),
    60:('part-12-llm-systems-at-scale','edge-on-device-llms'),
    61:('part-12-llm-systems-at-scale','scale-tools'),
}
for ch, (part, slug) in slugs.items():
    p = os.path.join(ROOT, part, f'module-{ch}-{slug}', 'index.html')
    with open(p, encoding='utf-8') as fp:
        c = fp.read()
    m = re.search(r'<h1[^>]*>([^<]+)', c)
    if m:
        canonical[ch] = m.group(1).strip().replace('&amp;', '&')

print("Canonical chapter titles:")
for k,v in canonical.items():
    print(f'  Ch {k}: {v}')

bad = []
for part, chrange in parts:
    for ch in chrange:
        slug = slugs[ch][1]
        dirp = os.path.join(ROOT, part, f'module-{ch}-{slug}')
        for fname in sorted(os.listdir(dirp)):
            if not fname.startswith('section-') or not fname.endswith('.html'):
                continue
            full = os.path.join(dirp, fname)
            m = re.match(r'section-(\d+)\.(\d+)\.html', fname)
            if not m:
                continue
            fch = int(m.group(1))
            fsec = int(m.group(2))
            with open(full, encoding='utf-8') as fp:
                c = fp.read()
            # check breadcrumb: <a href="index.html">Chapter NN: TITLE</a>
            bc = re.search(r'<a href="index\.html"[^>]*>([^<]+)</a></div>', c)
            page_curr = re.search(r'<div class="page-current">Section (\d+)\.(\d+)', c)
            title = re.search(r'<title>([^<]+)</title>', c)
            problems = []
            if bc:
                txt = bc.group(1).replace('&amp;', '&').strip()
                # Expected: "Chapter NN: <canonical title>"
                expected = f'Chapter {fch}: {canonical.get(fch, "??")}'
                if txt != expected:
                    problems.append(f'breadcrumb chapter wrong: "{txt}" (expected "{expected}")')
            else:
                problems.append('NO breadcrumb anchor')
            if page_curr:
                pc_ch = int(page_curr.group(1))
                pc_sec = int(page_curr.group(2))
                if (pc_ch, pc_sec) != (fch, fsec):
                    problems.append(f'page-current wrong: {pc_ch}.{pc_sec} (expected {fch}.{fsec})')
            else:
                problems.append('NO page-current')
            if title:
                t = title.group(1).strip().replace('&amp;', '&')
                # Should start with "Section NN.NN"
                m2 = re.match(r'Section (\d+)\.(\d+)', t)
                if m2:
                    tch, tsec = int(m2.group(1)), int(m2.group(2))
                    if (tch, tsec) != (fch, fsec):
                        problems.append(f'title section wrong: "{t[:60]}"')
                else:
                    problems.append(f'title not in "Section NN.NN" form: "{t[:60]}"')
            if problems:
                bad.append((full, problems))

print('\nBAD breadcrumb/title:')
for full, problems in bad:
    rel = full.replace(ROOT, '').lstrip('\\').replace('\\','/')
    print(rel)
    for p in problems:
        print(f'  - {p}')
print(f'\nTotal bad section files: {len(bad)}')
