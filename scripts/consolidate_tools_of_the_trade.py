"""Consolidate Tools of the Trade chapters to the canonical 5-section pattern.

Each ToT chapter must have exactly:
  X.1 Platforms
  X.2 Libraries & Frameworks
  X.3 Datasets & Benchmarks
  X.4 Models
  X.5 External Reading & Communities

Deep-dive sections (X.6 onwards) get merged into the appropriate canonical
section as new H2 subsections, then the source file is deleted and
cross-references are rewritten to canonical-section + anchor.

Categorization map per chapter is hand-tuned below.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# For each deep-dive section: (target_canonical_y, anchor_slug, h2_title)
# canonical_y is one of 1..5 inside the same chapter.
CONSOLIDATION_MAP = {
    # ============================
    # Part 1 / Chapter 6: Foundations Stack
    # ============================
    ('part-1-foundations/module-06-tools-of-the-trade', 6): {
        6:  (2, 'huggingface-hub', 'HuggingFace Hub: Sharing, Versioning, and Spaces'),
        7:  (2, 'essential-python-libraries', 'Essential Python Libraries for LLM Work'),
        8:  (1, 'virtual-environments', 'Virtual Environments and Dependency Management'),
        9:  (1, 'jupyter-and-colab', 'Jupyter Notebooks and Google Colab'),
        10: (2, 'common-llm-scripting-patterns', 'Common Patterns for LLM Scripting'),
        11: (1, 'hardware-requirements', 'Hardware Requirements for LLM Work'),
        12: (1, 'cuda-and-driver-setup', 'CUDA and Driver Setup'),
        13: (2, 'linking-cuda-to-pytorch', 'Linking CUDA to PyTorch'),
        14: (2, 'installing-key-libraries', 'Installing Key Libraries'),
        15: (1, 'cloud-compute-options', 'Cloud Compute Options'),
        16: (1, 'ide-setup-and-editor-integrations', 'IDE Setup and Editor Integrations'),
        17: (2, 'verifying-your-setup', 'Verifying Your Setup'),
        18: (2, 'git-basics-for-ml-projects', 'Git Basics for ML Projects'),
    },
    # ============================
    # Part 2 / Chapter 12: Understanding LLMs Stack
    # ============================
    ('part-2-understanding-llms/module-12-tools-of-the-trade', 12): {
        6:  (2, 'huggingface-transformers-deep-dive', 'HuggingFace Transformers Deep Dive'),
        7:  (2, 'vllm-deep-dive', 'vLLM Deep Dive'),
        8:  (2, 'text-generation-inference-tgi', 'Text Generation Inference (TGI)'),
        9:  (2, 'sglang', 'SGLang'),
        10: (4, 'quantization-for-serving', 'Quantization for Serving'),
    },
    # ============================
    # Part 3 / Chapter 16: Working with LLMs Stack
    # ============================
    ('part-3-working-with-llms/module-16-tools-of-the-trade', 16): {
        6:  (2, 'langchain-core-models-prompts-chains', 'LangChain Core: Models, Prompts, and Chains'),
        7:  (2, 'langchain-output-parsers-and-structured-output', 'LangChain Output Parsers and Structured Output'),
        8:  (1, 'api-keys-and-secrets-management', 'API Keys and Secrets Management'),
    },
    # ============================
    # Part 4 / Chapter 21: Training & Adaptation Stack
    # ============================
    ('part-4-training-adapting/module-21-tools-of-the-trade', 21): {
        6:  (2, 'huggingface-datasets-and-tokenizers', 'HuggingFace Datasets and Tokenizers Deep Dive'),
        7:  (2, 'huggingface-trainer-and-accelerate', 'HuggingFace Trainer and Accelerate'),
        8:  (2, 'huggingface-peft-and-trl', 'HuggingFace PEFT and TRL Deep Dive'),
        9:  (3, 'data-version-control-dvc', 'Data Version Control (DVC)'),
        10: (2, 'linking-experiment-runs-to-git-commits', 'Linking Experiment Runs to Git Commits'),
        11: (2, 'weights-and-biases-deep-dive', 'Weights and Biases Deep Dive'),
        12: (2, 'mlflow-deep-dive', 'MLflow Deep Dive'),
        13: (2, 'experiment-comparison-and-hpo', 'Experiment Comparison and Hyperparameter Optimization'),
        14: (3, 'pyspark-for-llm-data-pipelines', 'PySpark for LLM Data Pipelines'),
        15: (3, 'delta-lake-and-lakehouse-architecture', 'Delta Lake and Lakehouse Architecture'),
        16: (3, 'feature-stores-for-ml', 'Feature Stores for ML'),
        17: (2, 'distributed-training-deep-dive', 'Distributed Training Deep Dive'),
        18: (1, 'databricks-workspace-and-unity-catalog', 'Databricks Workspace and Unity Catalog'),
        19: (4, 'databricks-ai-and-foundation-models', 'Databricks AI and Foundation Models'),
        20: (2, 'ray-train-serve-data', 'Ray Train, Ray Serve, and Ray Data'),
    },
    # ============================
    # Part 5 / Chapter 25: Retrieval & Conversation Stack
    # ============================
    ('part-5-retrieval-conversation/module-25-tools-of-the-trade', 25): {
        6:  (2, 'langchain-memory-and-conversation', 'LangChain Memory and Conversation Management'),
        7:  (2, 'langchain-document-loaders-and-retrievers', 'LangChain Document Loaders and Retrievers'),
        8:  (2, 'orchestration-frameworks-overview', 'Orchestration Frameworks: LangChain, LlamaIndex, Haystack, DSPy'),
        9:  (2, 'llamaindex-deep-dive', 'LlamaIndex Deep Dive'),
        10: (2, 'haystack-and-dspy-deep-dive', 'Haystack and DSPy Deep Dive'),
    },
    # ============================
    # Part 6 / Chapter 30: Agentic AI Stack
    # ============================
    ('part-6-agentic-ai/module-30-tools-of-the-trade', 30): {
        6:  (2, 'langchain-agents-and-callbacks', 'LangChain Agents (Legacy) and Callbacks'),
        7:  (2, 'agent-frameworks-deep-dive', 'Agent Frameworks Deep Dive'),
        8:  (2, 'multi-agent-patterns-and-topologies', 'Multi-Agent Patterns and Topologies'),
    },
    # ============================
    # Part 8 / Chapter 48: Evaluation & Production Stack
    # ============================
    ('part-8-evaluation-production/module-48-tools-of-the-trade', 48): {
        6:  (2, 'production-agent-deployment', 'Production Agent Deployment: Observability, Cost, Guardrails'),
        7:  (2, 'model-registry-and-deployment-workflows', 'Model Registry and Deployment Workflows'),
        8:  (2, 'llm-evaluation-dashboards-and-observability', 'LLM Evaluation Dashboards and Observability'),
        9:  (1, 'inference-scaling-and-load-balancing', 'Inference Scaling and Load Balancing'),
        10: (1, 'production-data-pipelines-and-serving-at-scale', 'Production Data Pipelines and Serving at Scale'),
        11: (2, 'llm-system-observability', 'LLM System Observability'),
        12: (2, 'monitoring-and-drift-detection', 'Monitoring and Drift Detection'),
        13: (2, 'model-registry-and-lifecycle', 'Model Registry and Lifecycle'),
    },
    # ============================
    # Part 11 / Chapter 71: Designing Products Stack
    # ============================
    ('part-11-designing-llm-products/module-71-tools-of-the-trade', 71): {
        6:  (2, 'reproducibility-and-cicd-for-ml', 'Reproducibility and CI/CD for ML'),
        7:  (1, 'deployment-patterns', 'Deployment Patterns'),
        8:  (1, 'slos-alerting-and-finops', 'SLOs, Alerting, and FinOps'),
    },
}

SKIP_DIRS = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
             "source_fix_backups", "pagefind", "templates", ".claude",
             ".book-update", "vendor", "docs"}


def extract_body_content(text):
    """Strip <header>, leading <main> wrapper, trailing <nav class='chapter-nav'> and footer.
    Return the inner content of <main>.
    """
    m = re.search(r'<main[^>]*>([\s\S]*?)</main>', text)
    if not m: return ''
    body = m.group(1)
    # Strip pagefind-meta-injected span at start
    body = re.sub(r'<span class="pagefind-meta-injected"[^>]*></span>\s*', '', body)
    return body.strip()


def strip_h1_and_intro_metadata(body):
    """Remove epigraph, prerequisites, big-picture (intro chrome) from the body.

    These were part of the deep-dive section's own framing, but when merged as
    a subsection inside another section we don't want extra epigraphs.
    """
    # Drop epigraph blocks
    body = re.sub(r'<blockquote class="epigraph">[\s\S]*?</blockquote>\s*', '', body)
    # Drop prerequisites blocks
    body = re.sub(r'<div class="prerequisites">[\s\S]*?</div>\s*', '', body)
    return body.strip()


def make_h2_subsection(canonical_ch, canonical_y, anchor_slug, title, body):
    """Wrap merged content as <section> with an H2 anchor."""
    anchor = f'{canonical_ch}-{canonical_y}-{anchor_slug}'
    # Demote H2s inside body to H3 so the new H2 (the deep-dive title) is the outer header
    body = re.sub(r'<h2(\s[^>]*)?>', r'<h3\1>', body)
    body = re.sub(r'</h2>', '</h3>', body)
    # Demote H3->H4
    body = re.sub(r'<h3(\s[^>]*)?>', lambda m: '<h4' + (m.group(1) or '') + '>' if 'id=' not in (m.group(1) or '') else m.group(0), body, count=0)
    # That regex is unsafe, simpler: just demote h3 once
    body = re.sub(r'<h3>', '<h4>', body)
    body = re.sub(r'</h3>', '</h4>', body)
    return (
        f'\n<section class="tot-subsection" id="{anchor}">\n'
        f'<h2 id="{anchor}">{title}</h2>\n'
        f'{body}\n'
        f'</section>\n'
    )


def append_to_canonical(canonical_path, subsection_html):
    """Insert subsection_html into the canonical section, right before </main>."""
    text = canonical_path.read_text(encoding='utf-8')
    # Find </main> and insert before it (but after any existing content)
    new_text = text.replace('</main>', f'{subsection_html}\n</main>', 1)
    canonical_path.write_text(new_text, encoding='utf-8')


def delete_section(path, dry_run):
    if not dry_run:
        r = subprocess.run(['git', 'rm', '-f', str(path)], cwd=ROOT,
                          capture_output=True, text=True)
        return r.returncode == 0
    return True


def consolidate(ch_path, ch_num, mappings, dry_run):
    """Consolidate one chapter."""
    ch_dir = ROOT / ch_path
    print(f'\n=== {ch_path} ===')
    for src_y, (tgt_y, anchor, title) in sorted(mappings.items()):
        src = ch_dir / f'section-{ch_num}.{src_y}.html'
        tgt = ch_dir / f'section-{ch_num}.{tgt_y}.html'
        if not src.exists():
            print(f'  SKIP {src.name}: not found')
            continue
        if not tgt.exists():
            print(f'  SKIP {src.name}: target {tgt.name} missing')
            continue
        body = extract_body_content(src.read_text(encoding='utf-8'))
        body = strip_h1_and_intro_metadata(body)
        if not body:
            print(f'  SKIP {src.name}: empty body')
            continue
        sub = make_h2_subsection(ch_num, tgt_y, anchor, title, body)
        if not dry_run:
            append_to_canonical(tgt, sub)
        print(f'  {src.name} ({len(body)//1024}KB) -> {tgt.name} as H2 #{ch_num}-{tgt_y}-{anchor}')
        if not dry_run:
            delete_section(src, dry_run)


def rewrite_crossrefs(dry_run):
    """After merge: rewrite all cross-file refs from deleted deep-dive sections
    to canonical-section + anchor.
    """
    mapping = {}
    for (ch_path, ch_num), mp in CONSOLIDATION_MAP.items():
        mod_name = ch_path.split('/')[-1]
        for src_y, (tgt_y, anchor, _title) in mp.items():
            old = f'{mod_name}/section-{ch_num}.{src_y}.html'
            new = f'{mod_name}/section-{ch_num}.{tgt_y}.html#{ch_num}-{tgt_y}-{anchor}'
            mapping[old] = new

    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP_DIRS: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        for old, new in mapping.items():
            text = text.replace(old, new)
        if text != orig:
            if not dry_run:
                p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'\nRewrote cross-refs in {n_files} files')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    dry_run = not args.apply
    if dry_run:
        print('(DRY-RUN; pass --apply to execute)\n')

    for (ch_path, ch_num), mappings in CONSOLIDATION_MAP.items():
        consolidate(ch_path, ch_num, mappings, dry_run)

    rewrite_crossrefs(dry_run)


if __name__ == '__main__':
    sys.exit(main())
