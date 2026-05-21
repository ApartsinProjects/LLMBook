"""Final manual xref fixes for remaining broken refs."""
import os, re

# (source_relpath, old_href, new_href) tuples
FIXES = [
    ('part-8-conversational-ai-with-llms/module-41-conv-ai-tools/section-41.3.html',
     '../module-39-conversation-quality-and-eval/section-39.1.html',
     '../module-37-conversational-ai/section-37.5.html'),
    ('part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.2.html',
     '../module-31-rag-retrieval-augmented-generation/section-31.1.html',
     '../module-32-rag/section-32.1.html'),
    ('part-7-retrieval-information-extraction-with-llms/module-33-cross-modal-reasoning-rag/section-33.4.html',
     '../module-31-rag-retrieval-augmented-generation/section-31.7.html',
     '../module-32-rag/section-32.4.html'),
    ('part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.4.html',
     '../module-31-rag-retrieval-augmented-generation/section-31.7.html',
     '../module-32-rag/section-32.4.html'),
    ('part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.1.html',
     '../module-31-rag-retrieval-augmented-generation/section-31.1.html',
     '../module-32-rag/section-32.1.html'),
    ('part-7-retrieval-information-extraction-with-llms/module-36-retrieval-tools/section-36.2.html',
     '../module-31-rag-retrieval-augmented-generation/section-31.1.html',
     '../module-32-rag/section-32.1.html'),
    ('part-2-understanding-llms/module-10-interpretability/section-10.5.html',
     '../../part-4-training-adaptation/module-19-tools-of-the-trade/section-19.3.html#21-3-pyspark-for-llm-data-pipelines',
     '../../part-4-training-adaptation/module-19-tools-of-the-trade/section-19.3.html'),
    ('part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.4.html',
     '../../part-7-retrieval-information-extraction-with-llms/module-31-rag-retrieval-augmented-generation/section-31.1.html',
     '../../part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html'),
    ('part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.4.html',
     '../../part-7-retrieval-information-extraction-with-llms/module-31-rag-retrieval-augmented-generation/section-31.1.html',
     '../../part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html'),
    ('part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.4.html',
     '../../part-7-retrieval-information-extraction-with-llms/module-31-rag-retrieval-augmented-generation/section-31.1.html',
     '../../part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html'),
]

fixed = 0
for relpath, old, new in FIXES:
    full = relpath.replace('/', os.sep)
    if not os.path.exists(full):
        print(f'MISSING: {full}')
        continue
    with open(full, 'r', encoding='utf-8') as f:
        html = f.read()
    if old in html:
        # Verify target exists
        src_dir_abs = os.path.dirname(os.path.abspath(full))
        target_abs = os.path.normpath(os.path.join(src_dir_abs, new))
        if not os.path.exists(target_abs):
            print(f'  Target NOT found, skipping: {target_abs}')
            continue
        new_html = html.replace(f'href="{old}"', f'href="{new}"')
        if new_html != html:
            with open(full, 'w', encoding='utf-8', newline='') as f:
                f.write(new_html)
            fixed += 1
            print(f'  Fixed in {relpath}')
        else:
            print(f'  No change in {relpath}')
    else:
        print(f'  Old not found in {relpath}')

print(f'\nTotal: {fixed}/{len(FIXES)} fixed')
