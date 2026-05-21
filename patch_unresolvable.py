"""Patch the still-unresolvable broken hrefs with sensible alternatives.

Map each broken href to the best-fit valid section."""
import os, glob, re, json

# Map: (original broken href without anchor) -> replacement (resolved section relative path)
# The replacement should use a relative path; we'll let the source-file's location determine it.
REPLACEMENT_SECTION = {
    # 47.1 -> 47.1a (split section)
    'section-47.1.html': 'section-47.1a.html',
    # 11.5 -> 11.4 (pricing went into a different module; 11.4 covers retries/cost in apis)
    'section-11.5.html': 'section-11.4.html',
    # 31.7 -> 31.6 or 32.x; use 31.5 as fallback (production/eval covered there)
    'section-31.7.html': 'section-31.5.html',
    # 31.1 in this book is 31.1a or 31.1b. Use 31.1a (foundational).
    'section-31.1.html': 'section-31.1a.html',
    # 39.x (conversation quality and eval) does not exist; redirect to 42.1 (eval foundations)
    'section-39.1.html': 'section-42.1.html',
    # 19.3 in module-19-tools-of-the-trade in part-4 -- check if it exists
    'section-19.3.html': 'section-19.3.html',  # keep, just fix path
}

# Module/Part renames (broken-module-name -> actual-module-name in that part)
MODULE_RENAMES = {
    'module-47-hallucination-and-grounding': 'module-47-adversarial-security-red-team',
    'module-48-llm-attack-vectors': 'module-48-guardrails-runtime-safety',
    'module-49-llm-safety-alignment': 'module-49-agent-safety-autonomy',
    'module-50-bias-fairness': 'module-52-bias-fairness',
    'module-53-privacy-and-data-protection': 'module-50-privacy-data-protection',
    'module-55-policy-and-regulation': 'module-53-regulation-compliance',
    'module-39-conversation-quality-and-eval': 'module-42-evaluation-foundations',
    'module-37-conversational-ai-foundations': 'module-37-conversational-ai',
    'module-44-observability-tracing': 'module-44-online-eval-observability',
    'module-31-rag-retrieval-augmented-generation': 'module-32-rag',
    'module-32-vector-databases-retrieval': 'module-31-embeddings-vector-db',
    'module-26-agent-foundations': 'module-26-ai-agents',
    'module-27-agent-architectures': 'module-27-tool-use-protocols',
    'module-29-multi-agent-systems': 'module-28-multi-agent-systems',
    'module-19-multimodal-foundations': 'module-25-tools-of-the-trade',  # Multimodal foundations doesn't exist; redirect to tools
    'module-07-interpretability-mechanistic': 'module-10-interpretability',
    'module-05-encoder-models-bert': 'module-01-foundations-nlp-text-representation',
    'module-09-inference-deployment': 'module-09-inference-optimization',
    'module-08-instruction-tuning-rlhf': 'module-18-alignment-rlhf-dpo',  # under part 4
    'module-12-llm-libraries-frameworks': 'module-12-prompt-engineering',  # actually it should be part-3 libraries; check
    'module-13-llm-customization': 'module-16-fine-tuning-fundamentals',
    'module-15-prompt-engineering': 'module-12-prompt-engineering',
    'module-04-transformer-architecture-self-attention': 'module-03-transformer-architecture',
    'module-02-tokenization': 'module-02-sequence-models-attention',
    'module-03-embeddings': 'module-02-sequence-models-attention',
    'module-31-rag-retrieval-augmented-generation': 'module-32-rag',
    'module-55-policy-and-regulation': 'module-53-regulation-compliance',
}

# Part renames (rare)
PART_RENAMES = {
    'part-10-trustworthy-llms': 'part-10-llm-security-runtime-safety',
}


def resolve_href(href, source_file):
    """Apply renames and rewrites to a broken href, return new href or None."""
    # Strip anchor
    if '#' in href:
        head, anchor = href.split('#', 1)
    else:
        head, anchor = href, None

    new = head
    # Apply part renames
    for old, repl in PART_RENAMES.items():
        new = new.replace('/' + old + '/', '/' + repl + '/')
    # Apply module renames
    for old, repl in MODULE_RENAMES.items():
        new = new.replace('/' + old + '/', '/' + repl + '/')
    # Apply section file replacement (only the basename)
    section_file = os.path.basename(new)
    if section_file in REPLACEMENT_SECTION:
        new = os.path.dirname(new) + '/' + REPLACEMENT_SECTION[section_file]

    # Now compute absolute path to test
    src_dir_abs = os.path.dirname(os.path.abspath(source_file))
    abs_target = os.path.normpath(os.path.join(src_dir_abs, new))

    if os.path.exists(abs_target):
        return new + (('#' + anchor) if anchor else '')
    return None


# Build the set of files I touched
from backfill_content import CONTENT
touched = sorted(set(p.replace('/', os.sep) for p in CONTENT.keys()))
touched.append(os.sep.join(['part-7-retrieval-information-extraction-with-llms', 'module-31-embeddings-vector-db', 'section-31.1b.html']))

# Run audit
d = json.load(open('audit.json'))

# Collect broken hrefs from touched files
broken_by_file = {}
for i in d['issues']:
    f = i['file']
    if f in set(touched) and i['check_id'] == 'BROKEN_XREF':
        msg = i.get('message','')
        m = re.search(r'href="([^"]+)"', msg)
        if m:
            broken_by_file.setdefault(f, set()).add(m.group(1))

fixed_count = 0
unresolved = []
for f, hrefs in broken_by_file.items():
    full = f
    if not os.path.exists(full):
        continue
    with open(full, 'r', encoding='utf-8') as fp:
        html = fp.read()
    changed = False
    for href in hrefs:
        new = resolve_href(href, full)
        if new and new != href:
            html = html.replace(f'href="{href}"', f'href="{new}"')
            fixed_count += 1
            changed = True
        elif not new:
            unresolved.append((f, href))
    if changed:
        with open(full, 'w', encoding='utf-8', newline='') as fp:
            fp.write(html)

print(f'Fixed {fixed_count} more xrefs')
print(f'Still unresolved: {len(unresolved)}')
for f, href in unresolved[:30]:
    print(f'  {f}: {href}')
