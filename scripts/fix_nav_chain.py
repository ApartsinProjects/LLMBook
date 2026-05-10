import glob, os, re

def natural_sort_key(path):
    parts = re.split(r'(\d+)', path)
    return [int(p) if p.isdigit() else p.lower() for p in parts]

parts_config = [
    ('part-1-foundations', ['module-00-ml-pytorch-foundations', 'module-01-foundations-nlp-text-representation', 'module-02-tokenization-subword-models', 'module-03-sequence-models-attention', 'module-04-transformer-architecture', 'module-05-decoding-text-generation']),
    ('part-2-understanding-llms', ['module-06-pretraining-scaling-laws', 'module-07-modern-llm-landscape', 'module-08-reasoning-test-time-compute', 'module-09-inference-optimization', 'module-18-interpretability']),
    ('part-3-working-with-llms', ['module-10-llm-apis', 'module-11-prompt-engineering', 'module-12-hybrid-ml-llm']),
    ('part-4-training-adapting', ['module-13-synthetic-data', 'module-14-fine-tuning-fundamentals', 'module-15-peft', 'module-16-distillation-merging', 'module-17-alignment-rlhf-dpo']),
    ('part-5-retrieval-conversation', ['module-19-embeddings-vector-db', 'module-20-rag', 'module-21-conversational-ai']),
    ('part-6-agentic-ai', ['module-22-ai-agents', 'module-23-tool-use-protocols', 'module-24-multi-agent-systems', 'module-25-specialized-agents', 'module-26-agent-safety-production']),
    ('part-7-multimodal-applications', ['module-27-multimodal', 'module-28-llm-applications']),
    ('part-8-evaluation-production', ['module-29-evaluation-observability', 'module-30-observability-monitoring', 'module-31-production-engineering']),
    ('part-9-safety-strategy', ['module-32-safety-ethics-regulation', 'module-33-strategy-product-roi']),
    ('part-10-frontiers', ['module-34-emerging-architectures', 'module-35-ai-society']),
    ('part-11-idea-to-product', ['module-36-idea-to-product', 'module-37-building-steering', 'module-38-shipping-scaling']),
]

roman = {'1':'I','2':'II','3':'III','4':'IV','5':'V','6':'VI','7':'VII','8':'VIII','9':'IX','10':'X','11':'XI'}

# Build reading order
reading_order = []
reading_order.append('front-matter/index.html')
for f in sorted(glob.glob('front-matter/section-fm.*.html'), key=natural_sort_key):
    reading_order.append(f.replace(os.sep, '/'))

for part_dir, chapters in parts_config:
    reading_order.append(part_dir + '/index.html')
    for ch_dir in chapters:
        ch_path = part_dir + '/' + ch_dir
        reading_order.append(ch_path + '/index.html')
        ch_num = re.search(r'module-(\d+)', ch_dir).group(1)
        for s in sorted(glob.glob(ch_path + '/section-' + str(int(ch_num)) + '.*.html'), key=natural_sort_key):
            reading_order.append(s.replace(os.sep, '/'))

reading_order.append('appendices/index.html')
for ad in sorted(glob.glob('appendices/appendix-*/'), key=natural_sort_key):
    ad = ad.replace(os.sep, '/').rstrip('/')
    letter = os.path.basename(ad).split('-')[1]
    reading_order.append(ad + '/index.html')
    for s in sorted(glob.glob(ad + '/section-' + letter + '.*.html'), key=natural_sort_key):
        reading_order.append(s.replace(os.sep, '/'))

def make_relative(file_from, file_to):
    from_dir = os.path.dirname(file_from)
    rel = os.path.relpath(file_to, from_dir)
    return rel.replace(os.sep, '/')

def resolve_relative(base_file, rel_href):
    base_dir = os.path.dirname(base_file)
    resolved = os.path.normpath(os.path.join(base_dir, rel_href))
    return resolved.replace(os.sep, '/')

def get_nav_label(filepath):
    basename = os.path.basename(filepath)
    parent = os.path.basename(os.path.dirname(filepath))
    if basename == 'index.html':
        if parent.startswith('part-'):
            num = parent.split('-')[1]
            return 'Part ' + roman.get(num, num)
        elif parent.startswith('module-'):
            ch_num = re.search(r'module-(\d+)', parent).group(1)
            return 'Chapter ' + str(int(ch_num))
        elif parent.startswith('appendix-'):
            letter = parent.split('-')[1].upper()
            return 'Appendix ' + letter
        elif parent == 'appendices':
            return 'Appendices'
        elif parent == 'front-matter':
            return 'Front Matter'
    elif basename.startswith('section-'):
        m = re.search(r'section-(.+)\.html', basename)
        if m:
            return 'Section ' + m.group(1)
    return basename

def get_middle_link(filepath):
    basename = os.path.basename(filepath)
    parent = os.path.basename(os.path.dirname(filepath))
    if basename.startswith('section-'):
        if parent.startswith('module-'):
            ch_num = re.search(r'module-(\d+)', parent).group(1)
            return 'index.html', 'Chapter ' + str(int(ch_num))
        elif parent.startswith('appendix-'):
            letter = parent.split('-')[1].upper()
            return 'index.html', 'Appendix ' + letter
        else:
            return 'index.html', 'Index'
    elif basename == 'index.html' and parent.startswith('module-'):
        grandparent = os.path.basename(os.path.dirname(os.path.dirname(filepath)))
        if grandparent.startswith('part-'):
            num = grandparent.split('-')[1]
            return '../index.html', 'Part ' + roman.get(num, num)
        return '../index.html', 'Part'
    elif basename == 'index.html' and parent.startswith('appendix-'):
        return '../index.html', 'Appendices'
    elif basename == 'index.html' and (parent.startswith('part-') or parent == 'appendices' or parent == 'front-matter'):
        return '../toc.html', 'Contents'
    return 'index.html', 'Index'

# Fix nav for each file
fixed_count = 0
for i, filepath in enumerate(reading_order):
    if not os.path.isfile(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    expected_prev = reading_order[i-1] if i > 0 else None
    expected_next = reading_order[i+1] if i < len(reading_order)-1 else None

    prev_m = re.search(r'<a\s+href="([^"]+)"\s+class="prev"', content) or re.search(r'class="prev"[^>]*href="([^"]+)"', content)
    next_m = re.search(r'<a\s+href="([^"]+)"\s+class="next"', content) or re.search(r'class="next"[^>]*href="([^"]+)"', content)

    needs_fix = False
    if expected_next:
        if next_m:
            actual = resolve_relative(filepath, next_m.group(1))
            if actual != expected_next:
                needs_fix = True
        else:
            needs_fix = True
    if expected_prev:
        if prev_m:
            actual = resolve_relative(filepath, prev_m.group(1))
            if actual != expected_prev:
                needs_fix = True
        else:
            needs_fix = True

    if not needs_fix:
        continue

    middle_href, middle_text = get_middle_link(filepath)

    prev_part = ''
    if expected_prev:
        prev_href = make_relative(filepath, expected_prev)
        prev_label = get_nav_label(expected_prev)
        prev_part = '<a href="' + prev_href + '" class="prev">&larr; ' + prev_label + '</a>'

    next_part = ''
    if expected_next:
        next_href = make_relative(filepath, expected_next)
        next_label = get_nav_label(expected_next)
        next_part = '<a href="' + next_href + '" class="next">' + next_label + ' &rarr;</a>'

    new_nav = '<nav class="chapter-nav">\n        ' + prev_part + '\n        <a href="' + middle_href + '">' + middle_text + '</a>\n        ' + next_part + '\n    </nav>'

    nav_pattern = re.compile(r'<nav\s+class="chapter-nav">.*?</nav>', re.DOTALL)
    nav_match = nav_pattern.search(content)

    if nav_match:
        content = content[:nav_match.start()] + new_nav + content[nav_match.end():]
    else:
        body_end = content.find('</body>')
        if body_end > 0:
            content = content[:body_end] + '\n    ' + new_nav + '\n\n' + content[body_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    fixed_count += 1
    print('FIXED: ' + filepath)

print('\nTotal fixed: ' + str(fixed_count))
