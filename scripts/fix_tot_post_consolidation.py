"""After ToT consolidation: rebuild ToT chapter indexes, fix intra-section refs."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

TOT_CHAPTERS = [
    ('part-1-foundations/module-06-tools-of-the-trade', 6),
    ('part-2-understanding-llms/module-12-tools-of-the-trade', 12),
    ('part-3-working-with-llms/module-16-tools-of-the-trade', 16),
    ('part-4-training-adapting/module-21-tools-of-the-trade', 21),
    ('part-5-retrieval-conversation/module-25-tools-of-the-trade', 25),
    ('part-6-agentic-ai/module-30-tools-of-the-trade', 30),
    ('part-7-multimodal-generation/module-43-tools-of-the-trade', 43),
    ('part-8-evaluation-production/module-48-tools-of-the-trade', 48),
    ('part-9-safety-security-ethics/module-60-tools-of-the-trade', 60),
    ('part-11-designing-llm-products/module-71-tools-of-the-trade', 71),
    ('part-12-applications-across-industries/module-81-tools-of-the-trade', 81),
    ('part-13-frontiers/module-86-tools-of-the-trade', 86),
]

DELETED_TO_TARGET = {
    ('module-06-tools-of-the-trade', 6, 6):  (2, 'huggingface-hub'),
    ('module-06-tools-of-the-trade', 6, 7):  (2, 'essential-python-libraries'),
    ('module-06-tools-of-the-trade', 6, 8):  (1, 'virtual-environments'),
    ('module-06-tools-of-the-trade', 6, 9):  (1, 'jupyter-and-colab'),
    ('module-06-tools-of-the-trade', 6, 10): (2, 'common-llm-scripting-patterns'),
    ('module-06-tools-of-the-trade', 6, 11): (1, 'hardware-requirements'),
    ('module-06-tools-of-the-trade', 6, 12): (1, 'cuda-and-driver-setup'),
    ('module-06-tools-of-the-trade', 6, 13): (2, 'linking-cuda-to-pytorch'),
    ('module-06-tools-of-the-trade', 6, 14): (2, 'installing-key-libraries'),
    ('module-06-tools-of-the-trade', 6, 15): (1, 'cloud-compute-options'),
    ('module-06-tools-of-the-trade', 6, 16): (1, 'ide-setup-and-editor-integrations'),
    ('module-06-tools-of-the-trade', 6, 17): (2, 'verifying-your-setup'),
    ('module-06-tools-of-the-trade', 6, 18): (2, 'git-basics-for-ml-projects'),
    ('module-12-tools-of-the-trade', 12, 6):  (2, 'huggingface-transformers-deep-dive'),
    ('module-12-tools-of-the-trade', 12, 7):  (2, 'vllm-deep-dive'),
    ('module-12-tools-of-the-trade', 12, 8):  (2, 'text-generation-inference-tgi'),
    ('module-12-tools-of-the-trade', 12, 9):  (2, 'sglang'),
    ('module-12-tools-of-the-trade', 12, 10): (4, 'quantization-for-serving'),
    ('module-16-tools-of-the-trade', 16, 6):  (2, 'langchain-core-models-prompts-chains'),
    ('module-16-tools-of-the-trade', 16, 7):  (2, 'langchain-output-parsers-and-structured-output'),
    ('module-16-tools-of-the-trade', 16, 8):  (1, 'api-keys-and-secrets-management'),
    ('module-21-tools-of-the-trade', 21, 6):  (2, 'huggingface-datasets-and-tokenizers'),
    ('module-21-tools-of-the-trade', 21, 7):  (2, 'huggingface-trainer-and-accelerate'),
    ('module-21-tools-of-the-trade', 21, 8):  (2, 'huggingface-peft-and-trl'),
    ('module-21-tools-of-the-trade', 21, 9):  (3, 'data-version-control-dvc'),
    ('module-21-tools-of-the-trade', 21, 10): (2, 'linking-experiment-runs-to-git-commits'),
    ('module-21-tools-of-the-trade', 21, 11): (2, 'weights-and-biases-deep-dive'),
    ('module-21-tools-of-the-trade', 21, 12): (2, 'mlflow-deep-dive'),
    ('module-21-tools-of-the-trade', 21, 13): (2, 'experiment-comparison-and-hpo'),
    ('module-21-tools-of-the-trade', 21, 14): (3, 'pyspark-for-llm-data-pipelines'),
    ('module-21-tools-of-the-trade', 21, 15): (3, 'delta-lake-and-lakehouse-architecture'),
    ('module-21-tools-of-the-trade', 21, 16): (3, 'feature-stores-for-ml'),
    ('module-21-tools-of-the-trade', 21, 17): (2, 'distributed-training-deep-dive'),
    ('module-21-tools-of-the-trade', 21, 18): (1, 'databricks-workspace-and-unity-catalog'),
    ('module-21-tools-of-the-trade', 21, 19): (4, 'databricks-ai-and-foundation-models'),
    ('module-21-tools-of-the-trade', 21, 20): (2, 'ray-train-serve-data'),
    ('module-25-tools-of-the-trade', 25, 6):  (2, 'langchain-memory-and-conversation'),
    ('module-25-tools-of-the-trade', 25, 7):  (2, 'langchain-document-loaders-and-retrievers'),
    ('module-25-tools-of-the-trade', 25, 8):  (2, 'orchestration-frameworks-overview'),
    ('module-25-tools-of-the-trade', 25, 9):  (2, 'llamaindex-deep-dive'),
    ('module-25-tools-of-the-trade', 25, 10): (2, 'haystack-and-dspy-deep-dive'),
    ('module-30-tools-of-the-trade', 30, 6):  (2, 'langchain-agents-and-callbacks'),
    ('module-30-tools-of-the-trade', 30, 7):  (2, 'agent-frameworks-deep-dive'),
    ('module-30-tools-of-the-trade', 30, 8):  (2, 'multi-agent-patterns-and-topologies'),
    ('module-48-tools-of-the-trade', 48, 6):  (2, 'production-agent-deployment'),
    ('module-48-tools-of-the-trade', 48, 7):  (2, 'model-registry-and-deployment-workflows'),
    ('module-48-tools-of-the-trade', 48, 8):  (2, 'llm-evaluation-dashboards-and-observability'),
    ('module-48-tools-of-the-trade', 48, 9):  (1, 'inference-scaling-and-load-balancing'),
    ('module-48-tools-of-the-trade', 48, 10): (1, 'production-data-pipelines-and-serving-at-scale'),
    ('module-48-tools-of-the-trade', 48, 11): (2, 'llm-system-observability'),
    ('module-48-tools-of-the-trade', 48, 12): (2, 'monitoring-and-drift-detection'),
    ('module-48-tools-of-the-trade', 48, 13): (2, 'model-registry-and-lifecycle'),
    ('module-71-tools-of-the-trade', 71, 6): (2, 'reproducibility-and-cicd-for-ml'),
    ('module-71-tools-of-the-trade', 71, 7): (1, 'deployment-patterns'),
    ('module-71-tools-of-the-trade', 71, 8): (1, 'slos-alerting-and-finops'),
}

SKIP = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
        "source_fix_backups", "pagefind", "templates", ".claude",
        ".book-update", "vendor", "docs"}


def get_h1(p):
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    return m.group(1).strip() if m else ''


def get_meta_desc(p):
    text = p.read_text(encoding='utf-8')
    m = re.search(r'<meta content="Section \d+\.\d+:?[^.]+\.\s+([^"]+)"\s+name="description"', text)
    if m:
        s = m.group(1).strip()
        s = re.split(r'(?<=[.!?])\s+', s)[0]
        return s[:200]
    return ''


def rebuild_chapter_index(ch_path, ch_num):
    idx = ROOT / ch_path / 'index.html'
    if not idx.exists(): return False
    text = idx.read_text(encoding='utf-8')
    cards = []
    for y in range(1, 6):
        sec = ROOT / ch_path / f'section-{ch_num}.{y}.html'
        if not sec.exists(): continue
        title = get_h1(sec)
        desc = get_meta_desc(sec)
        cards.append(
            f'<li><a class="section-card" href="section-{ch_num}.{y}.html">\n'
            f'<span class="section-num">{ch_num}.{y}</span>\n'
            f'<span class="section-title">{title}</span>\n'
            f'<span class="section-desc">{desc}</span>\n'
            f'</a></li>'
        )
    cards_html = '\n'.join(cards)
    new_text, n = re.subn(
        r'<ul class="sections-list">[\s\S]*?</ul>',
        f'<ul class="sections-list">\n{cards_html}\n</ul>',
        text,
        count=1
    )
    if n > 0 and new_text != text:
        idx.write_text(new_text, encoding='utf-8')
        return True
    return False


def fix_intra_refs():
    n = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        for (mod_name, ch_num, deleted_y), (target_y, anchor) in DELETED_TO_TARGET.items():
            # Module-prefixed refs: href="<modname>/section-X.Y.html"
            text = re.sub(
                rf'(href="){re.escape(mod_name)}/section-{ch_num}\.{deleted_y}\.html(")',
                lambda m: f'{m.group(1)}{mod_name}/section-{ch_num}.{target_y}.html#{ch_num}-{target_y}-{anchor}{m.group(2)}',
                text
            )
            # Same-dir refs (no module prefix), only when current file is in that module
            if mod_name in p.parts:
                text = re.sub(
                    rf'(href=")section-{ch_num}\.{deleted_y}\.html(#[^"]*)?(")',
                    lambda m: f'{m.group(1)}section-{ch_num}.{target_y}.html#{ch_num}-{target_y}-{anchor}{m.group(3)}',
                    text
                )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n += 1
    return n


def main():
    n_idx = 0
    for ch_path, ch_num in TOT_CHAPTERS:
        if rebuild_chapter_index(ch_path, ch_num):
            n_idx += 1
            print(f'  Rebuilt index: {ch_path}')
    print(f'Updated {n_idx} ToT chapter indexes')

    n_refs = fix_intra_refs()
    print(f'Fixed intra-section refs in {n_refs} files')


if __name__ == '__main__':
    main()
