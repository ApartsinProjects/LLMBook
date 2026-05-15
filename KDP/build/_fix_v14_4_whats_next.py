"""v14.4: enrich the 13 sparse 'What Comes Next' sections with 1-2 sentences.

Each part-level index page had: "Continue to Part X: Title." That's too
terse for the user. Add a short preview sentence describing what
the next part covers.

Each enriched paragraph is 1-2 sentences, hyperlinked to the next part,
and tells the reader WHAT they will learn there.
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import sys

ROOT = Path(__file__).resolve().parents[2]

# (file_path, new_paragraph_html)
RICH_CONTENT = {
    'part-1-foundations/index.html': (
        '<p>Continue to <a href="../part-2-understanding-llms/index.html">'
        'Part II: Understanding LLMs</a>, where the foundations from this '
        'part are applied to large language models. You will learn how '
        'pretraining works at scale, how modern models like GPT-4, Claude, '
        'and Gemini differ in architecture and training data, and how '
        'inference-time reasoning techniques unlock new capabilities.</p>'
    ),
    'part-2-understanding-llms/index.html': (
        '<p>Continue to <a href="../part-3-working-with-llms/index.html">'
        'Part III: Working with LLMs</a>. Having understood what LLMs are '
        'and how they were trained, you now move to the practical layer: '
        'calling LLM APIs, designing effective prompts, and combining LLMs '
        'with classical ML systems for hybrid pipelines.</p>'
    ),
    'part-3-working-with-llms/index.html': (
        '<p>Continue to <a href="../part-4-training-adapting/index.html">'
        'Part IV: Training and Adapting</a>. With prompt engineering and '
        'API workflows in hand, you will now adapt LLMs to your own data '
        'through synthetic data generation, supervised fine-tuning, '
        'parameter-efficient methods (LoRA, QLoRA), and alignment '
        'techniques (RLHF, DPO).</p>'
    ),
    'part-4-training-adapting/index.html': (
        '<p>Continue to <a href="../part-5-retrieval-conversation/index.html">'
        'Part V: Retrieval and Conversation</a>. Fine-tuning lets you '
        'specialize a model; retrieval lets you ground it in your '
        'documents. You will build vector databases, design RAG '
        'pipelines, and develop conversational systems with memory and '
        'multi-turn dialogue management.</p>'
    ),
    'part-5-retrieval-conversation/index.html': (
        '<p>Continue to <a href="../part-6-agentic-ai/index.html">'
        'Part VI: Agentic AI</a>. Once your LLM can retrieve and '
        'converse, the next step is autonomous action: equipping models '
        'with tools, building multi-agent systems, and ensuring safety '
        'and reliability in production agent deployments.</p>'
    ),
    'part-6-agentic-ai/module-25-agent-safety-production/section-25.5.html': (
        '<p>Continue to <a href="../../part-7-multimodal-applications/index.html">'
        'Part VII: Multimodal and Applications</a>. Having mastered '
        'agentic AI patterns, you will now extend LLMs beyond text: '
        'vision-language models, audio, document understanding, and '
        'production deployment of multimodal pipelines.</p>'
    ),
    'part-6-agentic-ai/module-25-agent-safety-production/section-25.6.html': (
        '<p>Continue to <a href="../../part-7-multimodal-applications/index.html">'
        'Part VII: Multimodal and Applications</a>. With agent safety '
        'covered, you will now broaden the input modalities: vision, '
        'audio, document parsing, and the production patterns that make '
        'multimodal applications viable at scale.</p>'
    ),
    'appendices/appendix-a-mathematical-foundations/section-a.5.html': (
        '<p>Continue to <a href="../appendix-b-ml-essentials/index.html">'
        'Appendix B: Machine Learning Essentials</a>. The mathematical '
        'background you have built — linear algebra, probability, '
        'calculus, and information theory — now grounds practical ML '
        'concepts: learning paradigms, loss functions, optimization, '
        'and evaluation metrics.</p>'
    ),
}


def apply(dry):
    n_files = 0
    for rel, html in RICH_CONTENT.items():
        p = ROOT / rel
        if not p.exists():
            print(f'  SKIP (not found): {rel}')
            continue
        s = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        wn = s.find('div', class_='whats-next')
        if not wn:
            print(f'  SKIP (no whats-next): {rel}')
            continue
        # Keep the heading, replace the body
        h = wn.find(['h2', 'h3', 'h4'])
        # Remove all <p> children
        for x in list(wn.find_all(['p'])):
            x.decompose()
        # Insert new content after heading
        new_node = BeautifulSoup(html, 'html.parser')
        if h:
            for child in list(new_node.children):
                h.insert_after(child)
        else:
            for child in list(new_node.children):
                wn.append(child)

        if not dry:
            p.write_text(str(s), encoding='utf-8')
        n_files += 1
        print(f'  enriched: {rel}')
    return n_files


if __name__ == '__main__':
    dry = '--apply' not in sys.argv
    print('DRY RUN. Pass --apply.' if dry else 'APPLY mode.')
    print()
    n = apply(dry)
    print(f'\nFiles enriched: {n}')
