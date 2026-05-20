"""Polish bibliography entries: add arXiv URLs to bib-ref divs that mention an arXiv ID but have no link.

Reads each section HTML, finds `<div class="bib-ref">...arXiv:NNNN.NNNNN...</div>` entries
without an existing link, and wraps the arXiv reference in a clickable anchor.
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
    # Deep-dive
    'part-1-llm-building-blocks/module-02-tokenization/section-2.3.html',
    'part-1-llm-building-blocks/module-03-embeddings-representations/section-3.5.html',
    'part-2-understanding-llms/module-07-modern-llm-landscape/section-7.3.html',
    'part-5-multimodal-llms/module-22-multimodal-foundations/section-22.1.html',
    'part-5-multimodal-llms/module-22-multimodal-foundations/section-22.3.html',
    'part-6-agentic-ai/module-26-ai-agents/section-26.2.html',
    'part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.4.html',
    'part-8-conversational-ai-with-llms/module-40-multilingual-cultural/section-40.1.html',
    'part-15-llm-agentic-ai-research-frontiers/module-75-frontier-architectures/section-75.2.html',
    # Mental-model
    'part-2-understanding-llms/module-09-inference-optimization/section-9.3.html',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.3.html',
    'part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.7.html',
    'part-9-llm-evaluation-observability/module-42-evaluation-foundations/section-42.12.html',
}


def normalize(p: str) -> str:
    return p.replace(os.sep, '/').lstrip('./')


def find_candidates(root: str):
    """Walk the tree and yield (path, full_match, body, arxiv_id)."""
    found = []
    for r, dirs, fs in os.walk(root):
        rel_root = normalize(r)
        if any(seg in rel_root for seg in ('pagefind', 'node_modules', '.git', '_archive', 'KDP', 'agents', 'scripts', 'docs')):
            continue
        for fn in fs:
            if not fn.endswith('.html'):
                continue
            path = os.path.join(r, fn)
            rel = normalize(os.path.relpath(path, root))
            if rel in AVOID:
                continue
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            pat = re.compile(r'<div class="bib-ref">([^<]*?arXiv:\s*\d{4}\.\d{4,5}[^<]*?)</div>')
            for m in pat.finditer(content):
                entry = m.group(1)
                if 'arxiv.org' in entry.lower() or '<a ' in entry:
                    continue
                ids = re.findall(r'arXiv:\s*(\d{4}\.\d{4,5})', entry)
                if ids:
                    found.append((path, rel, m.group(0), entry, ids[0]))
    return found


def make_replacement(body: str, arxiv_id: str) -> str:
    """Replace the bare `arXiv:ID` text with a hyperlinked version."""
    url = f"https://arxiv.org/abs/{arxiv_id}"
    link = f'<a href="{url}" rel="noopener" target="_blank">arXiv:{arxiv_id}</a>'
    # Replace first occurrence of arXiv:ID (with optional whitespace)
    pattern = re.compile(r'arXiv:\s*' + re.escape(arxiv_id))
    new_body = pattern.sub(link, body, count=1)
    return f'<div class="bib-ref">{new_body}</div>'


def main():
    root = os.path.abspath(os.path.dirname(__file__))
    root = os.path.dirname(root)
    os.chdir(root)
    candidates = find_candidates('.')
    print(f'Found {len(candidates)} candidate entries to fix', file=sys.stderr)
    by_file = {}
    for path, rel, full, body, aid in candidates:
        by_file.setdefault(path, []).append((full, body, aid, rel))

    fixes_log = []
    for path, items in by_file.items():
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        for full, body, aid, rel in items:
            new_full = make_replacement(body, aid)
            if full in content:
                content = content.replace(full, new_full, 1)
                fixes_log.append((rel, aid, body[:120]))
            else:
                print(f'WARN: could not find full match in {path}', file=sys.stderr)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    # Print summary log
    for rel, aid, snippet in fixes_log:
        print(f'{rel}\t{aid}\t{snippet}')


if __name__ == '__main__':
    main()
