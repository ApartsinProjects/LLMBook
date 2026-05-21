"""Polish bibliography entries: pass 2.

This pass handles multi-line bib-ref entries containing markup (e.g., <em>, <strong>)
where the arXiv ID appears within. It replaces the first bare `arXiv:NNNN.NNNNN` text
with a hyperlinked anchor.
"""
import re
import os
import sys

AVOID = {
    'part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.3.html',
    'part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.4.html',
    'part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.2.html',
    'part-12-llm-systems-at-scale/module-59-distributed-training-systems/section-59.3.html',
    'part-6-agentic-ai/module-27-tool-use-protocols/section-27.5.html',
    'part-1-llm-building-blocks/module-02-tokenization/section-2.3.html',
    'part-1-llm-building-blocks/module-03-embeddings-representations/section-3.5.html',
    'part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html',
    'part-5-multimodal-llms/module-22-multimodal-foundations/section-22.1.html',
    'part-5-multimodal-llms/module-22-multimodal-foundations/section-22.3.html',
    'part-6-agentic-ai/module-26-ai-agents/section-26.2.html',
    'part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html',
    'part-8-conversational-ai-with-llms/module-40-multilingual-cultural/section-40.1.html',
    'part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.2.html',
    'part-2-understanding-llms/module-09-inference-optimization/section-9.3.html',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.7.html',
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html',
}


def normalize(p: str) -> str:
    return p.replace(os.sep, '/').lstrip('./')


def main():
    root = os.path.abspath(os.path.dirname(__file__))
    root = os.path.dirname(root)
    os.chdir(root)

    bib_pat = re.compile(r'(<(?:div|p) class="bib-ref">)(.*?)(</(?:div|p)>)', re.DOTALL)
    fixes_log = []
    files_touched = set()

    for r, dirs, fs in os.walk('.'):
        rel_root = normalize(r)
        if any(seg in rel_root for seg in ('pagefind','node_modules','.git','_archive','KDP','agents','scripts','docs')):
            continue
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(r, fn)
            rel = normalize(os.path.relpath(path, '.'))
            if rel in AVOID:
                continue
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            def repl(m: re.Match) -> str:
                open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
                if 'arxiv.org' in body.lower():
                    return m.group(0)
                # First arXiv ID
                id_m = re.search(r'arXiv:\s*(\d{4}\.\d{4,5})', body)
                if not id_m:
                    return m.group(0)
                aid = id_m.group(1)
                url = f"https://arxiv.org/abs/{aid}"
                link = f'<a href="{url}" rel="noopener" target="_blank">arXiv:{aid}</a>'
                # Replace the arXiv:ID text, preserving prefix whitespace exactly
                new_body = re.sub(r'arXiv:\s*' + re.escape(aid), link, body, count=1)
                fixes_log.append((rel, aid))
                return open_tag + new_body + close_tag

            new_content, n = bib_pat.subn(repl, content)
            if n and new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                files_touched.add(rel)

    print(f'Fixes applied: {len(fixes_log)} across {len(files_touched)} files', file=sys.stderr)
    for rel, aid in fixes_log:
        print(f'{rel}\t{aid}')


if __name__ == '__main__':
    main()
