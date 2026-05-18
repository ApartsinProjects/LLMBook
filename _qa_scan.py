"""Quick publication QA scan. Reads files and reports structural / rendering bugs."""
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path('E:/Projects/BookBlogsHome/LLMBook')

# All recently-edited files
TARGETS = []

# Opening hooks R2 chapter index pages (15 of them - one duplicate adjusted)
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
]

# Memorability R2 (21 sections)
TARGETS += [
    'part-1-llm-building-blocks/module-01-foundations-nlp-text-representation/section-1.5.html',
    'part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.2.html',
    'part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3a.html',
    'part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1a.html',
    'part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html',
    'part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.1.html',
    'part-1-llm-building-blocks/module-04-decoding-text-generation/section-4.2.html',
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html',
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.2.html',
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html',
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html',
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.6.html',
    'part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.7.html',
    'part-3-working-with-llms/module-12-prompt-engineering/section-12.1.html',
    'part-3-working-with-llms/module-12-prompt-engineering/section-12.2.html',
    'part-3-working-with-llms/module-12-prompt-engineering/section-12.3.html',
    'part-3-working-with-llms/module-12-prompt-engineering/section-12.4.html',
    'part-3-working-with-llms/module-12-prompt-engineering/section-12.5.html',
    'part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.1.html',
    'part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.2.html',
    'part-3-working-with-llms/module-13-hybrid-ml-llm/section-13.3.html',
]

# Illustrator R2 (29 sections with new figures)
TARGETS += [
    'part-6-agentic-ai/module-26-ai-agents/section-26.2.html',
    'part-6-agentic-ai/module-26-ai-agents/section-26.4.html',
    'part-6-agentic-ai/module-27-tool-use-protocols/section-27.6.html',
    'part-6-agentic-ai/module-28-multi-agent-systems/section-28.4.html',
    'part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html',
    'part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.5b.html',
    'part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.1.html',
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.4.html',
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.8.html',
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.9.html',
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.11.html',
    'part-9-llm-evaluation-observability/module-43-specialized-evaluation/section-43.4.html',
    'part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.2.html',
    'part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html',
    'part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.4.html',
    'part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.6.html',
    'part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.7.html',
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html',
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.3.html',
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.4.html',
    'part-6-agentic-ai/module-30-tools-of-the-trade/section-30.1.html',
    'part-6-agentic-ai/module-30-tools-of-the-trade/section-30.3.html',
    'part-6-agentic-ai/module-30-tools-of-the-trade/section-30.4.html',
    'part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.1.html',
    'part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.3.html',
    'part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.4.html',
    'part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.5.html',
    'part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.5b.html',
    'part-6-agentic-ai/module-30-tools-of-the-trade/section-30.2b.html',
]

# Curriculum-alignment R2 (13 chapter index pages from Part X)
TARGETS += [
    'part-4-training-adaptation/module-15-synthetic-data/index.html',  # already in list
    'part-6-agentic-ai/module-26-ai-agents/index.html',  # already
    'part-6-agentic-ai/module-27-tool-use-protocols/index.html',  # already
    'part-6-agentic-ai/module-28-multi-agent-systems/index.html',  # already
    'part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/index.html',
    'part-8-conversational-ai-with-llms/module-37-conversational-ai/index.html',
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/index.html',
    'part-9-llm-evaluation-observability/module-45-tools-of-the-trade/index.html',
    'part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/index.html',
    'part-10-llm-security-runtime-safety/module-48-guardrails-runtime-safety/index.html',
    'part-10-llm-security-runtime-safety/module-49-agent-safety-autonomy/index.html',
    'part-10-llm-security-runtime-safety/module-50-privacy-data-protection/index.html',
    'part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/index.html',
    'part-11-llm-ethics-trust-governance/module-52-bias-fairness/index.html',
]

# De-dupe
TARGETS = list(dict.fromkeys(TARGETS))

# Random sample - 5 sections across the book
import random
random.seed(42)
SECTIONS_GLOB = list(ROOT.glob('part-*/module-*/section-*.html'))
sample = random.sample(SECTIONS_GLOB, 8)
for s in sample:
    TARGETS.append(str(s.relative_to(ROOT)).replace('\\', '/'))

# Dedupe again
TARGETS = list(dict.fromkeys(TARGETS))

print(f'Total targets: {len(TARGETS)}')

issues = defaultdict(list)

def check_file(path):
    fp = ROOT / path
    if not fp.exists():
        issues['MISSING_FILE'].append(path)
        return
    try:
        text = fp.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        text = fp.read_text(encoding='utf-8', errors='replace')
        issues['ENCODING'].append(path)

    # 1. Em dash / double dash (excluding HTML comments and code)
    # Strip comments + code blocks before checking
    no_comments = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    no_code = re.sub(r'<pre.*?</pre>', '', no_comments, flags=re.DOTALL)
    no_code = re.sub(r'<code.*?</code>', '', no_code, flags=re.DOTALL)
    if re.search(r'—', no_code):
        # Find first occurrence
        m = re.search(r'.{0,40}—.{0,40}', no_code)
        issues['EM_DASH'].append(f'{path}: {m.group(0)}')
    # Double dash anywhere outside code: be more lenient (lots of CLI flags etc)

    # 2. Placeholder text
    for kw in ['TODO', 'FIXME', 'TBD', 'Lorem ipsum', 'XXX', 'lorem ipsum']:
        if re.search(r'\b' + kw + r'\b', text):
            # exclude code/script contexts
            tcopy = re.sub(r'<pre.*?</pre>', '', text, flags=re.DOTALL)
            tcopy = re.sub(r'<code.*?</code>', '', tcopy, flags=re.DOTALL)
            tcopy = re.sub(r'<script.*?</script>', '', tcopy, flags=re.DOTALL)
            if re.search(r'\b' + kw + r'\b', tcopy):
                m = re.search(r'.{0,40}\b' + kw + r'\b.{0,40}', tcopy)
                issues['PLACEHOLDER'].append(f'{path}: {kw}: {m.group(0) if m else ""}')

    # 3. Heading skip (h2 -> h4 with no h3)
    headings = [(m.start(), int(m.group(1))) for m in re.finditer(r'<h([1-6])\b', text)]
    for i in range(1, len(headings)):
        prev = headings[i-1][1]
        curr = headings[i][1]
        if curr > prev + 1:
            issues['HEADING_SKIP'].append(f'{path}: h{prev} -> h{curr} at offset {headings[i][0]}')
            break  # Only report first

    # 4. Empty paragraphs
    empty_p = re.findall(r'<p>\s*</p>', text)
    if empty_p:
        issues['EMPTY_P'].append(f'{path}: {len(empty_p)} empty <p>')

    # 5. SVG without aria-label or role="img"
    svgs = re.findall(r'<svg[^>]*>', text)
    for svg in svgs:
        if 'aria-label' not in svg and 'aria-labelledby' not in svg and 'role="img"' not in svg:
            issues['SVG_NO_ARIA'].append(f'{path}: {svg[:80]}')

    # 6. img without alt
    imgs = re.findall(r'<img[^>]*>', text)
    for img in imgs:
        if 'alt=' not in img:
            issues['IMG_NO_ALT'].append(f'{path}: {img[:80]}')
        elif re.search(r'alt=""', img):
            issues['IMG_EMPTY_ALT'].append(f'{path}: {img[:80]}')

    # 7. Tables without thead
    tables = re.findall(r'<table[^>]*>.*?</table>', text, flags=re.DOTALL)
    for t in tables:
        if '<thead>' not in t and '<th>' in t:
            # table with th but no thead is not strictly wrong but suboptimal
            pass
        if '<thead>' not in t and '<th' not in t:
            issues['TABLE_NO_THEAD'].append(f'{path}: table with no thead/th')

    # 8. Unclosed/orphan tags - count common ones
    for tag in ['div', 'figure', 'section', 'p', 'li', 'ul', 'ol', 'a', 'span']:
        opens = len(re.findall(r'<' + tag + r'\b', text))
        closes = len(re.findall(r'</' + tag + r'>', text))
        if opens != closes:
            issues['TAG_MISMATCH'].append(f'{path}: <{tag}> open={opens} close={closes} (diff={opens-closes})')

    # 9. Double dashes outside HTML comments and code
    # Check for "--" outside comments and code that isn't a CLI flag
    tcopy = no_code
    # Remove comments more aggressively
    tcopy = re.sub(r'<!--[\s\S]*?-->', '', tcopy)
    if re.search(r'(?<!-)--(?!-)', tcopy):
        # find first match with context
        m = re.search(r'.{0,30}(?<!-)--(?!-).{0,30}', tcopy)
        if m:
            ctx = m.group(0)
            # Filter false positives: CLI flags, hyphenated terms in code contexts we missed
            if not re.match(r'^[^\s]*--[^\s]', ctx):
                issues['DOUBLE_DASH'].append(f'{path}: {ctx}')

    # 10. Duplicate IDs
    ids = re.findall(r'\bid="([^"]+)"', text)
    seen = {}
    for i in ids:
        seen[i] = seen.get(i, 0) + 1
    dups = {k: v for k, v in seen.items() if v > 1}
    if dups:
        issues['DUPLICATE_IDS'].append(f'{path}: {dups}')

    # 11. Orphan callout (callout div not closed)
    callout_open = len(re.findall(r'<div class="callout', text))
    callout_close = text.count('</div>')  # this is global, not useful
    # better - balanced
    pass  # already covered by TAG_MISMATCH

    # 12. Lorem
    if 'lorem ipsum' in text.lower():
        issues['LOREM'].append(path)

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
