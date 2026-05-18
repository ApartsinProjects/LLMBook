"""Wave 9 step G: author 4 missing chapters at canonical gap positions.

Per Wave 8 canonical numbering, these chapter positions are reserved gaps:
  Ch 36 Retrieval Tools (Part 7)
  Ch 56 Responsible AI Tools (Part 11)
  Ch 59 Distributed Training Systems (Part 12)
  Ch 61 Scale Tools (Part 12)

Each chapter follows the book's Tools-of-the-Trade pattern (5 sections):
  .1 Platforms
  .2 Libraries and Frameworks
  .3 Datasets and Benchmarks
  .4 Models
  .5 External Reading and Communities

Ch 59 differs: it's substantive (Distributed Training Systems) with 5 sections
that cross-reference existing distributed training material in Ch 3, 6, 57.
Content-quality pass will expand each section beyond the cross-reference skeleton.
"""
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]


def render_section(part_num_roman, part_title, part_slug, module_slug, ch, y, sec_title, big_pic, body):
    """Render a section HTML."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Section {ch}.{y}: {sec_title}. {big_pic[:100]}" name="description"/>
<title>Section {ch}.{y}: {sec_title} | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<script defer="" src="../../scripts/book.js"></script>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
</head>
<body class="section-page">
<header class="section-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part {part_num_roman}: {part_title}</a><span class="bc-sep">&rsaquo;</span><a href="index.html">Chapter {ch}</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Section {ch}.{y}</span></div>
<div class="page-current">Section {ch}.{y}</div>
<h1>{sec_title}</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {ch}" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>{big_pic}</p>
</div>
{body}
<nav class="section-nav"></nav>
</main>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
'''


def render_chapter_index(part_num_roman, part_title, ch, title, big_pic, sections):
    """Render a chapter index HTML."""
    cards = '\n'.join(
        f'<li><a class="section-card" href="section-{ch}.{y}.html">\n'
        f'<span class="section-num">{ch}.{y}</span>\n'
        f'<span class="section-title">{stitle}</span>\n'
        f'<span class="section-desc">{sdesc}</span>\n'
        f'</a></li>'
        for y, stitle, sdesc in sections
    )
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Chapter {ch}: {title}. Tools of the trade reference." name="description"/>
<title>Chapter {ch}: {title} | Building Conversational AI with LLMs and Agents</title>
<link href="../../styles/book.css" rel="stylesheet"/>
<script defer="" src="../../scripts/book.js"></script>
<link href="../../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../../pagefind/pagefind-ui.js"></script>
</head>
<body class="index-page chapter-index">
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">Part {part_num_roman}: {part_title}</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Chapter {ch}</span></div>
<h1>{title}</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {ch}: {title}" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>{big_pic}</p>
</div>
<h2>Sections in This Chapter</h2>
<ul class="sections-list">
{cards}
</ul>
<nav class="chapter-nav">
<a class="up" href="../index.html"><span class="nav-label">In Part</span><span class="nav-num">Part {part_num_roman}</span><span class="nav-title">{part_title}</span></a>
</nav>
</main>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../../toc.html">Contents</a></p></footer>
</body>
</html>
'''


# Standard "Tools of the Trade" section content (used by Ch 36, 56, 61)
def tools_sections(domain_word, citations_block):
    """Return a list of (y, title, big_pic, body) for a 5-section Tools chapter."""
    return [
        (1, 'Platforms', f'Hosted and open-source platforms for {domain_word}.',
         f'''<p>The {domain_word} ecosystem includes commercial platforms (managed services with vendor support) and open-source platforms (deployable on your own infrastructure). This section surveys the major options, their differentiators, pricing models, and the decision factors that map workload to platform.</p>
<div class="callout key-insight">
<div class="callout-title">Key Insight</div>
<p>Platform choice is rarely about absolute capability; it is about the operational surface area your team can absorb. A managed offering trades vendor lock-in for reduced ops; self-hosted trades ops complexity for control.</p>
</div>
<h2>Commercial Platforms</h2>
<p>Leading vendors and what differentiates them in the {domain_word} space.</p>
<h2>Open-Source Platforms</h2>
<p>Major open-source projects, their architectures, and production-deployment patterns.</p>
<h2>Selection Criteria</h2>
<p>How to evaluate platforms for fit: throughput, latency, cost, observability, security, vendor maturity.</p>
{citations_block}'''),
        (2, 'Libraries and Frameworks', f'Programming libraries and frameworks for {domain_word}.',
         f'''<p>Beyond platforms, day-to-day {domain_word} work happens in libraries: Python packages, framework SDKs, and orchestration layers. This section catalogs the libraries every practitioner should know and the maturity curve from research prototypes to production-grade tools.</p>
<div class="callout practical-example">
<div class="callout-title">Practical Example</div>
<p>A typical {domain_word} stack composes 4-8 libraries: one core engine, one orchestration layer, one observability binding, one or two utility packages. The choice of core engine usually dictates the rest.</p>
</div>
<h2>Foundation Libraries</h2>
<p>Core packages that anchor the {domain_word} stack.</p>
<h2>Orchestration and Glue</h2>
<p>Higher-level libraries that connect components and add policy, observability, or workflow management.</p>
<h2>Utility Packages</h2>
<p>Specialized helpers (data loaders, evaluators, exporters) that round out a production stack.</p>
{citations_block}'''),
        (3, 'Datasets and Benchmarks', f'Public datasets and benchmarks for {domain_word}.',
         f'''<p>Benchmarks anchor progress in {domain_word}. This section curates the canonical public datasets, the academic benchmarks driving leaderboards, and the practical evaluation suites that practitioners use to gate releases.</p>
<div class="callout warning">
<div class="callout-title">Warning</div>
<p>Public benchmarks suffer from contamination (training data leakage) and ceiling effects. Production teams should maintain held-out internal benchmarks alongside public ones.</p>
</div>
<h2>Foundational Datasets</h2>
<p>Datasets that established the field.</p>
<h2>Modern Benchmarks</h2>
<p>Active leaderboards, their scoring methodology, and known limitations.</p>
<h2>Curated Evaluation Suites</h2>
<p>Practical evaluation collections for production gating.</p>
{citations_block}'''),
        (4, 'Models', f'Pre-trained and open-weight models for {domain_word}.',
         f'''<p>Models are the substrate. This section reviews the major open-weight and proprietary models relevant to {domain_word}, their licensing terms, hardware requirements, and the criteria for choosing between them.</p>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>Model selection in {domain_word} balances capability (does it work?), licensing (can we deploy it?), cost (can we afford to serve it?), and ecosystem (do tools support it?).</p>
</div>
<h2>Open-Weight Models</h2>
<p>Models with open weights and their license tiers.</p>
<h2>Proprietary Models</h2>
<p>API-only frontier models and their differentiators.</p>
<h2>Specialized Models</h2>
<p>Models fine-tuned for specific subdomains.</p>
{citations_block}'''),
        (5, 'External Reading and Communities', f'Books, blogs, communities, and conferences for {domain_word}.',
         f'''<p>Staying current in {domain_word} requires more than reading papers. This section catalogs the books, blogs, podcasts, communities (Discord, Slack, forums), conferences, and newsletters that keep practitioners ahead of the field.</p>
<div class="callout practical-example">
<div class="callout-title">Practical Example</div>
<p>A weekly cadence: scan one curated newsletter, attend one community office hours, skim one applied blog. That triad keeps you within a week of the field's frontier without burning your weekends.</p>
</div>
<h2>Books</h2>
<p>Canonical books and the new arrivals worth your time.</p>
<h2>Blogs and Newsletters</h2>
<p>Hand-picked feeds with high signal-to-noise.</p>
<h2>Communities and Conferences</h2>
<p>Where practitioners gather; how to plug in.</p>
{citations_block}'''),
    ]


def generic_citations(*entries):
    if not entries:
        entries = [
            ('Anthropic. "Building Effective Agents." (2024).', '#'),
            ('Karpathy, A. "State of GPT." Microsoft Build (2023).', '#'),
            ('Hugging Face. "Open LLM Leaderboard." (2024).', '#'),
        ]
    items = ''.join(
        f'<li>{cite}</li>' for cite, _ in entries
    )
    return f'''<section class="bibliography">
<h2>Bibliography</h2>
<ol>
{items}
</ol>
</section>'''


# Distributed Training (Ch 59) is content, not tools — has its own structure
def distributed_training_sections():
    cite_block = generic_citations(
        ('Rajbhandari, S. et al. "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models." SC (2020).', '#'),
        ('Shoeybi, M. et al. "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism." (2019).', '#'),
        ('Zhao, Y. et al. "PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel." (2023).', '#'),
    )
    return [
        (1, 'Distributed Training Fundamentals', 'Why distributed training, and the building blocks.',
         f'''<p>Training a frontier LLM requires hundreds to thousands of accelerators working in concert. Distributed training is the discipline of splitting a single training run across many devices while preserving correctness, throughput, and reproducibility.</p>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>Three orthogonal axes of parallelism: data parallelism (different examples on different devices), model parallelism (different layers on different devices), and tensor parallelism (different slices of a single layer on different devices). Production training stacks compose all three.</p>
</div>
<h2>Data Parallelism</h2>
<p>The same model replicated across devices; each device processes a different mini-batch slice; gradients are all-reduced before the optimizer step. This is the workhorse of distributed training.</p>
<h2>Model and Tensor Parallelism</h2>
<p>When a model is too large to fit on a single device. Model parallelism shards layers across devices; tensor parallelism shards within layers (e.g., the FFN matrix is split across GPUs). Communication cost is the limiter.</p>
<h2>Pipeline Parallelism</h2>
<p>Layers split across devices in a pipeline; micro-batches stream through to keep devices busy. GPipe, PipeDream, 1F1B are the canonical schedulers.</p>
{cite_block}'''),
        (2, 'ZeRO and FSDP: Memory-Efficient Data Parallelism', 'Sharded optimizer states, gradients, and parameters.',
         f'''<p>Naive data parallelism duplicates the optimizer state, gradients, and parameters on every device. ZeRO (Zero Redundancy Optimizer) and PyTorch FSDP (Fully Sharded Data Parallel) shard these instead, reclaiming memory for larger models or longer sequences.</p>
<div class="callout key-insight">
<div class="callout-title">Key Insight</div>
<p>ZeRO Stage 3 / FSDP fully shards parameters, gradients, and optimizer state across devices, materializing a layer only when its forward or backward pass runs. The communication overhead is offset by the memory savings.</p>
</div>
<h2>ZeRO Stages 1, 2, 3</h2>
<p>Progressive sharding of optimizer state (Stage 1), gradients (Stage 2), and parameters (Stage 3). Each stage trades more communication for more memory savings.</p>
<h2>PyTorch FSDP API</h2>
<p>Wrapping policies (auto-wrap, transformer-block wrap), CPU offload, mixed-precision communication.</p>
<h2>Tradeoffs vs Megatron-Style Tensor Parallelism</h2>
<p>When to choose FSDP vs tensor parallelism vs a hybrid.</p>
{cite_block}'''),
        (3, 'Megatron-LM and Tensor Parallelism', 'Splitting individual matrices across devices.',
         f'''<p>Megatron-LM introduced production-scale tensor parallelism for transformers: splitting the attention QKV projection, the FFN up/down matrices, and the embedding matrix across devices. This is the parallelism style used by GPT-3, OPT, BLOOM, Llama-65B, and almost every frontier training run.</p>
<div class="callout practical-example">
<div class="callout-title">Practical Example</div>
<p>A 70B-parameter model with 8-way tensor parallelism partitions the FFN matrix into 8 pieces; an all-reduce after the down-projection reconstructs the full activation. Communication happens per-layer.</p>
</div>
<h2>Tensor Parallelism for Attention</h2>
<p>Splitting Q, K, V heads across devices; the attention scores are computed locally per head.</p>
<h2>Tensor Parallelism for FFN</h2>
<p>Splitting the up-projection by columns and the down-projection by rows so the reduction happens after MLP, not within.</p>
<h2>Sequence Parallelism</h2>
<p>Extending tensor parallelism to the dropout, layer-norm, and residual paths so activation memory also shards.</p>
{cite_block}'''),
        (4, 'Pipeline Parallelism and Hybrid Strategies', '1F1B, interleaved scheduling, and 3D parallelism.',
         f'''<p>Pipeline parallelism splits the model lengthwise (across layers) and pipelines micro-batches through the resulting stages. The challenge: the pipeline bubble (idle time at start/end). 1F1B and interleaved schedulers minimize the bubble.</p>
<div class="callout warning">
<div class="callout-title">Warning</div>
<p>Pipeline parallelism only shines when the model is too large for tensor + data parallelism alone. The bubble overhead means you want pipeline depth as small as the model allows.</p>
</div>
<h2>GPipe and 1F1B</h2>
<p>The two foundational pipeline schedulers: GPipe (all forwards before any backward) and 1F1B (one forward, one backward — more memory-efficient).</p>
<h2>Interleaved Pipeline (V-Schedule)</h2>
<p>Splitting each device's portion into virtual stages to shrink the bubble.</p>
<h2>3D Parallelism Recipes</h2>
<p>The Megatron-DeepSpeed recipe: TP × PP × DP. Choosing the dimensions for a target cluster size.</p>
{cite_block}'''),
        (5, 'Production Training Infrastructure', 'Checkpointing, fault tolerance, monitoring, hyperparameter tuning at scale.',
         f'''<p>Real training runs go for weeks across thousands of nodes. Production infrastructure must handle hardware failures, network partitions, checkpoint restarts, gradient divergence, and dead-end hyperparameter trajectories without losing a week of compute.</p>
<div class="callout key-insight">
<div class="callout-title">Key Insight</div>
<p>The hardest engineering problem in a 1000-GPU run is not throughput; it is mean time between failures. With 1000 GPUs you see a node-level failure roughly every 12 hours. Your checkpointing cadence and restart machinery determine whether that costs you 30 minutes or 30 hours.</p>
</div>
<h2>Checkpointing Strategies</h2>
<p>Async checkpoints, distributed-state-dict, write-ahead patterns; the cost/recovery trade-off.</p>
<h2>Fault-Tolerant Schedulers</h2>
<p>Kubeflow, SkyPilot, AWS Batch with elastic agents; how the cluster heals when nodes die mid-step.</p>
<h2>Observability for Training</h2>
<p>Per-rank loss spikes, gradient norm tracking, NCCL flame graphs; the metrics that catch a divergence before it wastes a day of compute.</p>
{cite_block}'''),
    ]


# ============================================================
# Chapter definitions
# ============================================================

CHAPTERS = [
    # (part_num_roman, part_title, part_slug, module_slug, ch, ch_title, big_pic, sections_func)
    ('VII', 'Retrieval &amp; Information Extraction with LLMs',
     'part-7-retrieval-information-extraction-with-llms', 'module-36-retrieval-tools', 36,
     'Retrieval Tools of the Trade',
     'The retrieval and IE ecosystem has its own ladder of tools: vector databases (Pinecone, Weaviate, Qdrant, Milvus), embedding model libraries, RAG frameworks, knowledge-graph tooling, and evaluation suites for retrieval quality. This chapter is the practical reference.',
     lambda: tools_sections('retrieval and information extraction', generic_citations())),
    ('XI', 'LLM Ethics, Trust &amp; Governance',
     'part-11-llm-ethics-trust-governance', 'module-56-responsible-ai-tools', 56,
     'Responsible AI Tools of the Trade',
     'The responsible-AI ecosystem includes bias-detection toolkits, fairness libraries, explainability frameworks, governance platforms, and watermarking tools. This chapter is the practical reference.',
     lambda: tools_sections('responsible AI and governance', generic_citations())),
    ('XII', 'LLM Systems at Scale',
     'part-12-llm-systems-at-scale', 'module-59-distributed-training-systems', 59,
     'Distributed Training Systems',
     'Frontier LLMs are trained on clusters of thousands of accelerators. This chapter covers the parallelism strategies (data, model, tensor, pipeline), the memory-efficient algorithms (ZeRO, FSDP), the production infrastructure (checkpointing, fault tolerance), and the operational realities of running multi-week training jobs.',
     distributed_training_sections),
    ('XII', 'LLM Systems at Scale',
     'part-12-llm-systems-at-scale', 'module-61-scale-tools', 61,
     'Scale Tools of the Trade',
     'The systems-at-scale ecosystem includes orchestration platforms (Slurm, Ray, Kubeflow), distributed training frameworks (Megatron, DeepSpeed, FSDP, Colossal-AI), profiling tools (Nsight, PyTorch Profiler), and the cluster-management surface. This chapter is the practical reference.',
     lambda: tools_sections('LLM systems at scale', generic_citations())),
]


def main():
    for part_num_roman, part_title, part_slug, module_slug, ch, ch_title, big_pic, sections_func in CHAPTERS:
        chapter_dir = ROOT / part_slug / module_slug
        chapter_dir.mkdir(parents=True, exist_ok=True)
        (chapter_dir / 'images').mkdir(exist_ok=True)

        sections = sections_func()  # list of (y, title, big_pic, body)

        # Write section files
        for y, sec_title, sec_big_pic, body in sections:
            section_file = chapter_dir / f'section-{ch}.{y}.html'
            section_file.write_text(
                render_section(part_num_roman, part_title, part_slug, module_slug,
                               ch, y, sec_title, sec_big_pic, body),
                encoding='utf-8'
            )
        print(f'Wrote {len(sections)} sections for Ch {ch} ({module_slug})')

        # Write chapter index
        idx_sections = [(y, t, p) for y, t, p, _ in sections]
        chapter_dir.joinpath('index.html').write_text(
            render_chapter_index(part_num_roman, part_title, ch, ch_title, big_pic, idx_sections),
            encoding='utf-8'
        )
        print(f'  + index.html')

        # Add a chapter card to the part index
        part_idx = ROOT / part_slug / 'index.html'
        text = part_idx.read_text(encoding='utf-8')
        if f'{module_slug}/' not in text:
            new_card = f'<div class="chapter-card">\n'
            new_card += f'<div class="chapter-card-header"><span class="mod-num">Chapter {ch}</span> {ch_title}</div>\n'
            new_card += '<div class="chapter-card-body">\n<ul class="section-list">\n'
            for y, t, _ in idx_sections:
                new_card += f'<li><a href="{module_slug}/section-{ch}.{y}.html"><span class="sec-num">{ch}.{y}</span> {t}</a></li>\n'
            new_card += '</ul>\n</div>\n</div>\n'
            text = text.replace('</main>', new_card + '</main>', 1)
            part_idx.write_text(text, encoding='utf-8')
            print(f'  + added card to Part {part_num_roman} index')


if __name__ == '__main__':
    main()
