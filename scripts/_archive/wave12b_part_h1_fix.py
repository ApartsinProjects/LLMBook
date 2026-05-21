"""Wave 12b: fix part-N/index.html h1 titles to canonical names + roman numerals."""
import re
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

PART_NAMES = {
    'part-1-llm-building-blocks': ('Part I', 'LLM Building Blocks'),
    'part-2-understanding-llms': ('Part II', 'Understanding LLMs'),
    'part-3-working-with-llms': ('Part III', 'Working with LLMs'),
    'part-4-training-adaptation': ('Part IV', 'LLM Training and Adaptation'),
    'part-5-multimodal-llms': ('Part V', 'Multimodal LLMs'),
    'part-6-agentic-ai': ('Part VI', 'Agentic AI'),
    'part-7-retrieval-information-extraction-with-llms': ('Part VII', 'Retrieval &amp; Information Extraction with LLMs'),
    'part-8-conversational-ai-with-llms': ('Part VIII', 'Conversational AI with LLMs'),
    'part-9-llm-evaluation-observability': ('Part IX', 'LLM Evaluation &amp; Observability'),
    'part-10-llm-security-runtime-safety': ('Part X', 'LLM Security &amp; Runtime Safety'),
    'part-11-llm-ethics-trust-governance': ('Part XI', 'LLM Ethics, Trust &amp; Governance'),
    'part-12-llm-systems-at-scale': ('Part XII', 'LLM Systems at Scale'),
    'part-13-llmops-lifecycle': ('Part XIII', 'LLMOps Lifecycle'),
    'part-14-designing-llm-agent-products': ('Part XIV', 'Designing LLM/Agent Products'),
    'part-15-applications-of-llms-across-industries': ('Part XV', 'Applications of LLMs Across Industries'),
    'part-16-llm-agentic-ai-research-frontiers': ('Part XVI', 'LLM &amp; Agentic AI Research Frontiers'),
}


def main():
    for slug, (roman, name) in PART_NAMES.items():
        p = ROOT / slug / 'index.html'
        if not p.exists():
            print(f'  {slug}: no index.html')
            continue
        t = p.read_text(encoding='utf-8')
        o = t

        # Replace any <h1 ...>Part X: ...</h1> with canonical
        # Handles: <h1>Part I: Foundations</h1>, <h1 class="part-title">Part XI: ...</h1>
        t = re.sub(
            r'(<h1[^>]*>)Part [IVXLCDM]+:\s*[^<]+(</h1>)',
            rf'\1{roman}: {name}\2',
            t,
            count=1
        )
        # Also fix <title> and <meta description> at top
        t = re.sub(
            r'(<title>)Part [IVXLCDM]+:\s*[^|<]+(\s*\|)',
            rf'\1{roman}: {name}\2',
            t,
            count=1
        )
        t = re.sub(
            r'(<meta content=")Part [IVXLCDM]+:\s*[^.]+\.',
            rf'\1{roman}: {name}.',
            t,
            count=1
        )
        # Fix breadcrumb current label: <span class="bc-current">Part X</span>
        t = re.sub(
            r'(<span class="bc-current">)Part [IVXLCDM]+(</span>)',
            rf'\1{roman}\2',
            t,
            count=1
        )

        if t != o:
            p.write_text(t, encoding='utf-8')
            print(f'  Fixed {slug}/index.html')


if __name__ == '__main__':
    main()
