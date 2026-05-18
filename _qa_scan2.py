"""Second QA scan, broader random sample + all 30 sections required."""
import re
from pathlib import Path
from collections import defaultdict
import random

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')

# All recently-edited files + 30 random sample
TARGETS = []

# Opening hooks (14 + curriculum 13 overlapping; just 25 chapter indexes total)
TARGETS += [
    'part-4-training-adaptation/module-15-synthetic-data/index.html',
    'part-4-training-adaptation/module-16-fine-tuning-fundamentals/index.html',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/index.html',
    'part-5-multimodal-llms/module-21-document-understanding-ocr/index.html',
    'part-5-multimodal-llms/module-22-vision-language-models/index.html',
    'part-6-agentic-ai/module-26-ai-agents/index.html',
    'part-6-agentic-ai/module-27-tool-use-protocols/index.html',
    'part-6-agentic-ai/module-28-multi-agent-systems/index.html',
    'part-6-agentic-ai/module-29-specialized-agents/index.html',
    'part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/index.html',
    'part-7-retrieval-information-extraction-with-llms/module-32-rag/index.html',
    'part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/index.html',
    'part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/index.html',
    'part-8-conversational-ai-with-llms/module-37-conversational-ai/index.html',
    'part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/index.html',
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html',
    'part-9-llm-evaluation-observability/module-45-tools-of-the-trade/index.html',
    'part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/index.html',
    'part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/index.html',
    'part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/index.html',
    'part-10-llm-security-runtime-safety/module-50-privacy-data-protection/index.html',
    'part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/index.html',
    'part-11-llm-ethics-trust-governance/module-52-bias-fairness/index.html',
]

# Random sample 30 sections (seed=99 gives a good cross-book set)
random.seed(99)
SECTIONS = list(ROOT.glob('part-*/module-*/section-*.html'))
sample = random.sample(SECTIONS, 30)
for s in sample:
    TARGETS.append(str(s.relative_to(ROOT)).replace('\\', '/'))

# Dedupe
TARGETS = list(dict.fromkeys(TARGETS))
print(f'Total targets: {len(TARGETS)}')

issues = defaultdict(list)

def check_file(path):
    fp = ROOT / path
    if not fp.exists():
        issues['MISSING_FILE'].append(path)
        return
    text = fp.read_text(encoding='utf-8')
    text_orig = text

    # Strip comments and code blocks for prose checks
    no_comments = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    no_code = re.sub(r'<pre[^>]*>.*?</pre>', '', no_comments, flags=re.DOTALL)
    no_code = re.sub(r'<code[^>]*>.*?</code>', '', no_code, flags=re.DOTALL)
    no_script = re.sub(r'<script[^>]*>.*?</script>', '', no_code, flags=re.DOTALL)
    no_svg = re.sub(r'<svg[^>]*>.*?</svg>', '', no_script, flags=re.DOTALL)

    # 1. Em dashes
    em = re.search(r'—', no_svg)
    if em:
        # Find context
        idx = em.start()
        ctx = no_svg[max(0,idx-40):idx+40]
        issues['EM_DASH'].append(f'{path}: ...{ctx}...')

    # 2. Double dashes (not in comments / code / attrs / numbers)
    dd_matches = list(re.finditer(r'(?<![-\w])--(?![\w-])', no_svg))
    if dd_matches:
        for m in dd_matches[:2]:
            ctx = no_svg[max(0,m.start()-40):m.end()+40]
            # Filter: skip if surrounded by quotes (attributes)
            if 'class=' in ctx or 'href=' in ctx or 'src=' in ctx:
                continue
            issues['DOUBLE_DASH'].append(f'{path}: ...{ctx}...')

    # 3. Placeholder
    for kw in ['TODO:', 'FIXME', 'TBD ', 'XXX ', 'Lorem ipsum', 'lorem ipsum']:
        if kw in no_comments:
            tcopy = no_script
            if kw in tcopy:
                m = re.search(r'.{0,30}' + re.escape(kw) + r'.{0,40}', tcopy)
                issues['PLACEHOLDER'].append(f'{path}: ...{m.group(0) if m else kw}...')

    # 4. Div balance
    no_comments_full = re.sub(r'<!--.*?-->', '', text_orig, flags=re.DOTALL)
    opens = len(re.findall(r'<div\b', no_comments_full))
    closes = len(re.findall(r'</div>', no_comments_full))
    if opens != closes:
        issues['DIV_MISMATCH'].append(f'{path}: open={opens} close={closes}')

    # 5. Figure balance
    fopens = len(re.findall(r'<figure\b', text))
    fcloses = len(re.findall(r'</figure>', text))
    if fopens != fcloses:
        issues['FIGURE_MISMATCH'].append(f'{path}: open={fopens} close={fcloses}')

    # 6. Section balance
    sopens = len(re.findall(r'<section\b', text))
    scloses = len(re.findall(r'</section>', text))
    if sopens != scloses:
        issues['SECTION_MISMATCH'].append(f'{path}: open={sopens} close={scloses}')

    # 7. Empty p
    ep = re.findall(r'<p>\s*</p>', text)
    if ep:
        issues['EMPTY_P'].append(f'{path}: {len(ep)}')

    # 8. Duplicate IDs
    ids = re.findall(r'\bid="([^"]+)"', text)
    seen = {}
    for i in ids:
        seen[i] = seen.get(i, 0) + 1
    dups = {k: v for k, v in seen.items() if v > 1}
    if dups:
        issues['DUP_IDS'].append(f'{path}: {dups}')

    # 9. img alt
    imgs = re.findall(r'<img[^>]*>', text)
    for im in imgs:
        if 'alt=' not in im:
            issues['IMG_NO_ALT'].append(f'{path}: {im[:80]}')

    # 10. SVG aria
    svgs = re.findall(r'<svg[^>]*>', text)
    for s in svgs:
        if 'aria-label' not in s and 'aria-labelledby' not in s and 'role=' not in s:
            issues['SVG_NO_ARIA'].append(f'{path}: {s[:80]}')

    # 11. Code blocks rendered as prose - look for naked HTML escape sequences in prose
    # Specifically: <p>...&lt;...&gt;...</p> with no <code> wrapping is suspect
    # skip
    pass

    # 12. Orphan paragraph with "Section X.Y" or "Chapter NN" that doesn't match
    # skip - covered by curriculum-alignment

    # 13. Stale "Continue to Section X..." with broken anchor
    # skip - hrefs already checked

for t in TARGETS:
    check_file(t)

print('\n=== ISSUES ===\n')
for cat in sorted(issues.keys()):
    print(f'\n--- {cat}: {len(issues[cat])} ---')
    for item in issues[cat][:20]:
        print(f'  {item}')
    if len(issues[cat]) > 20:
        print(f'  ... and {len(issues[cat]) - 20} more')

print('\n=== END ===')
