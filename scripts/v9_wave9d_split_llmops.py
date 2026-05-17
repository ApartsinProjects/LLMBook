"""Wave 9 step D: split old Ch 62 LLMOps monster (11 sections) into 5 chapters.

Old Ch 62 has 11 sections totaling ~726 KB. Splits per v9 plan:

  Ch 62 Production Engineering Core (2 sections retained):
    62.1  Scaling, Performance & Production Guardrails  (was 62.1, kept)
    62.2  LLMOps & Continuous Improvement              (was 62.2, kept)

  Ch 63 AI Gateways & Model Routing (1 section, ~62 KB):
    63.1  AI Gateways and Model Routing                (was 62.3)

  Ch 64 Workflow Orchestration & Durable Execution (1 section, ~88 KB):
    64.1  Workflow Orchestration and Durable Execution (was 62.4)

  Ch 65 Containers, Kubernetes & Deployment (5 sections, 237 KB total):
    65.1  Docker Fundamentals                          (was 62.7)
    65.2  Writing Dockerfiles for ML and LLM           (was 62.8)
    65.3  Docker Compose for Multi-Service AI          (was 62.9)
    65.4  Containerizing LLM Inference Servers         (was 62.10)
    65.5  Kubernetes-Native LLM Operations             (was 62.11)

  Ch 66 Reliability, SLOs & Model Registry (1 section, ~127 KB):
    66.1  Reliability Engineering for LLM Applications (was 62.6)

  Cross-part move:
    Part 12 Ch 60 Edge & On-Device LLMs (1 section, ~62 KB):
      60.1  Edge and On-Device LLM Deployment           (was 62.5)

Total: 11 sections preserved across 6 chapter homes (no content loss).
Single-section chapters intentional — content-quality pass will expand later.
"""
from pathlib import Path
import re
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
PART13 = 'part-13-llmops-lifecycle'
PART12 = 'part-12-llm-systems-at-scale'
CH62_DIR = ROOT / PART13 / 'module-62-production-engineering-core'

# (old_y, new_part, new_module_slug, new_ch, new_y, new_title)
MOVES = [
    # Stay in Ch 62
    (1, PART13, 'module-62-production-engineering-core', 62, 1, 'Scaling, Performance & Production Guardrails'),
    (2, PART13, 'module-62-production-engineering-core', 62, 2, 'LLMOps & Continuous Improvement'),
    # Promote to new chapters in Part 13
    (3, PART13, 'module-63-ai-gateways-routing', 63, 1, 'AI Gateways and Model Routing'),
    (4, PART13, 'module-64-workflow-orchestration', 64, 1, 'Workflow Orchestration and Durable Execution'),
    (7, PART13, 'module-65-containers-kubernetes', 65, 1, 'Docker Fundamentals: Images, Containers, and Volumes'),
    (8, PART13, 'module-65-containers-kubernetes', 65, 2, 'Writing Dockerfiles for ML and LLM Projects'),
    (9, PART13, 'module-65-containers-kubernetes', 65, 3, 'Docker Compose for Multi-Service AI Applications'),
    (10, PART13, 'module-65-containers-kubernetes', 65, 4, 'Containerizing LLM Inference Servers'),
    (11, PART13, 'module-65-containers-kubernetes', 65, 5, 'Kubernetes-Native LLM Operations: Scheduling, Serving, and GPU Management'),
    (6, PART13, 'module-66-reliability-slos-registry', 66, 1, 'Reliability Engineering for LLM Applications'),
    # Cross-part move to Part 12
    (5, PART12, 'module-60-edge-on-device-llms', 60, 1, 'Edge and On-Device LLM Deployment'),
]

CHAPTER_TEMPLATES = {
    63: ('AI Gateways &amp; Model Routing',
         'Part XIII: LLMOps Lifecycle',
         'Production LLM deployments need gateways for rate limiting, model routing for cost/quality optimization, and observability. This chapter covers the gateway pattern, intelligent routing, and the operational surface that AI gateways expose.',
         '../../', PART13),
    64: ('Workflow Orchestration &amp; Durable Execution',
         'Part XIII: LLMOps Lifecycle',
         'LLM-powered applications often span hours of work — chained tool calls, human review, retries, and long-running document processing. This chapter covers durable workflow engines (Temporal, AWS Step Functions, Airflow) and the patterns that make stateful agent workflows reliable.',
         '../../', PART13),
    65: ('Containers, Kubernetes &amp; Deployment',
         'Part XIII: LLMOps Lifecycle',
         'Production LLM serving runs on containers, and at scale, on Kubernetes. This chapter covers Docker fundamentals, writing Dockerfiles for ML workloads, Docker Compose for multi-service apps, containerizing inference servers (vLLM, TGI, Triton), and Kubernetes-native patterns for GPU scheduling and serving.',
         '../../', PART13),
    66: ('Reliability, SLOs &amp; Model Registry',
         'Part XIII: LLMOps Lifecycle',
         'LLM applications fail in modes that traditional reliability engineering does not cover: hallucination spikes, prompt regressions, latency cliffs from long contexts. This chapter covers SLO definition for LLM systems, error budgets, model registry patterns, canary deployments, and incident response for production LLM apps.',
         '../../', PART13),
    60: ('Edge &amp; On-Device LLMs',
         'Part XII: LLM Systems at Scale',
         'Not every LLM workload belongs in the cloud. This chapter covers running models on consumer hardware (laptops, phones), quantization for edge, framework support (llama.cpp, MLC, MediaPipe, Core ML), privacy-preserving on-device inference, and the operational patterns that differ from server-side serving.',
         '../../', PART12),
}


def build_chapter_index(ch, title, breadcrumb_part, big_pic, root_prefix, part_slug):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Chapter {ch}: {re.sub('<[^>]+>', '', title)}. Production LLM systems engineering." name="description"/>
<title>Chapter {ch}: {re.sub('<[^>]+>', '', title)} | Building Conversational AI with LLMs and Agents</title>
<link href="{root_prefix}styles/book.css" rel="stylesheet"/>
<script defer="" src="{root_prefix}scripts/book.js"></script>
<link href="{root_prefix}pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="{root_prefix}pagefind/pagefind-ui.js"></script>
</head>
<body class="index-page chapter-index">
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="{root_prefix}index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="{root_prefix}toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="page-breadcrumb" data-pagefind-meta="chapter"><a href="../index.html">{breadcrumb_part}</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Chapter {ch}</span></div>
<h1>{title}</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {ch}: {re.sub('<[^>]+>', '', title)}" hidden=""></span>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>{big_pic}</p>
</div>
<h2>Sections in This Chapter</h2>
<ul class="sections-list">
{{section_cards}}
</ul>
<nav class="chapter-nav">
<a class="up" href="../index.html"><span class="nav-label">In Part</span><span class="nav-num">{breadcrumb_part.split(":")[0].strip()}</span><span class="nav-title">{breadcrumb_part.split(":",1)[1].strip()}</span></a>
</nav>
</main>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="{root_prefix}toc.html">Contents</a></p></footer>
</body>
</html>
'''


def rewrite_section_metadata(file_path, old_ch, old_y, new_ch, new_y, new_title):
    text = file_path.read_text(encoding='utf-8')
    new_label = f'{new_ch}.{new_y}'

    # title tag: <title>Section X.Y: ... | Building...</title>
    text = re.sub(
        rf'<title>Section {old_ch}\.{old_y}:[^<]*</title>',
        f'<title>Section {new_label}: {new_title} | Building Conversational AI with LLMs and Agents</title>',
        text
    )
    # meta description
    text = re.sub(
        rf'(<meta content=")Section {old_ch}\.{old_y}:[^"]*(")',
        rf'\1Section {new_label}: {new_title}\2',
        text
    )
    # page-current
    text = re.sub(r'<div class="page-current">Section [^<]+</div>',
                  f'<div class="page-current">Section {new_label}</div>', text)
    # breadcrumb current
    text = re.sub(r'<span class="bc-current">Section [^<]+</span>',
                  f'<span class="bc-current">Section {new_label}</span>', text)
    # h1
    text = re.sub(r'<h1>[^<]+</h1>',
                  f'<h1>{new_title}</h1>', text, count=1)

    if old_ch != new_ch:
        # Update breadcrumb chapter link
        text = re.sub(
            r'<a href="index\.html">Chapter \d+[^<]*</a>',
            f'<a href="index.html">Chapter {new_ch}</a>',
            text
        )
        # Update pagefind chapter meta
        text = re.sub(
            r'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:[^"]+"',
            f'<span class="pagefind-meta-injected" data-pagefind-meta="chapter:Chapter {new_ch}"',
            text
        )
        # Update chapter-nav up link
        text = re.sub(
            r'<span class="nav-num">Chapter \d+</span><span class="nav-title">[^<]+</span>',
            f'<span class="nav-num">Chapter {new_ch}</span><span class="nav-title">{new_title}</span>',
            text
        )

    # Anchor IDs and same-page anchors
    text = re.sub(rf'\bid="{old_ch}-{old_y}-', f'id="{new_ch}-{new_y}-', text)
    text = re.sub(rf'\bhref="#{old_ch}-{old_y}-', f'href="#{new_ch}-{new_y}-', text)
    text = re.sub(rf'\bSection {old_ch}\.{old_y}\b', f'Section {new_label}', text)
    # X.Y.Z numeric references (figure numbers etc.)
    text = re.sub(rf'\b{old_ch}\.{old_y}\.(\d+)\b', rf'{new_ch}.{new_y}.\1', text)

    file_path.write_text(text, encoding='utf-8')


def main():
    # Step 1: stage all moves to .__tmp__ to avoid collisions
    print('Step 1: stage moves to __tmp__')
    for old_y, new_part, new_module, new_ch, new_y, _title in MOVES:
        src = CH62_DIR / f'section-62.{old_y}.html'
        if old_y == new_y and new_ch == 62:
            continue  # in-place keepers
        tgt_dir = ROOT / new_part / new_module
        tgt_dir.mkdir(parents=True, exist_ok=True)
        (tgt_dir / 'images').mkdir(exist_ok=True)
        tmp = tgt_dir / f'section-{new_ch}.{new_y}.html.__tmp__'
        if src.exists() and not tmp.exists():
            subprocess.run(['git', 'mv', str(src), str(tmp)], cwd=ROOT, capture_output=True)
            print(f'  Staged 62.{old_y} -> {new_module}/section-{new_ch}.{new_y}.__tmp__')

    # Step 2: rename .__tmp__ to final and rewrite metadata
    print('Step 2: finalize moves')
    for old_y, new_part, new_module, new_ch, new_y, new_title in MOVES:
        if old_y == new_y and new_ch == 62:
            continue
        tgt_dir = ROOT / new_part / new_module
        tmp = tgt_dir / f'section-{new_ch}.{new_y}.html.__tmp__'
        dst = tgt_dir / f'section-{new_ch}.{new_y}.html'
        if tmp.exists() and not dst.exists():
            subprocess.run(['git', 'mv', str(tmp), str(dst)], cwd=ROOT, capture_output=True)
            rewrite_section_metadata(dst, 62, old_y, new_ch, new_y, new_title)
            print(f'  62.{old_y} -> {new_module}/section-{new_ch}.{new_y}')

    # Step 3: write chapter index files for new chapters
    print('Step 3: build chapter indices')
    for new_ch in (63, 64, 65, 66, 60):
        if new_ch not in CHAPTER_TEMPLATES:
            continue
        title, breadcrumb, big_pic, root_prefix, part_slug = CHAPTER_TEMPLATES[new_ch]
        module = next(m for old_y, p, m, ch, y, t in MOVES if ch == new_ch)
        chapter_dir = ROOT / part_slug / module

        # Build section cards from MOVES filtered by new_ch
        cards = []
        for old_y, p, m, ch, y, t in MOVES:
            if ch == new_ch:
                cards.append(
                    f'<li><a class="section-card" href="section-{ch}.{y}.html">\n'
                    f'<span class="section-num">{ch}.{y}</span>\n'
                    f'<span class="section-title">{t}</span>\n'
                    f'<span class="section-desc">Promoted from old Ch 62 monster.</span>\n'
                    f'</a></li>'
                )
        idx_html = build_chapter_index(new_ch, title, breadcrumb, big_pic, root_prefix, part_slug)
        idx_html = idx_html.replace('{section_cards}', '\n'.join(cards))
        (chapter_dir / 'index.html').write_text(idx_html, encoding='utf-8')
        print(f'  Wrote {module}/index.html')

    # Step 4: update Ch 62 index — only 62.1 and 62.2 remain
    print('Step 4: update Ch 62 index')
    ch62_idx = CH62_DIR / 'index.html'
    if ch62_idx.exists():
        text = ch62_idx.read_text(encoding='utf-8')
        cards = []
        for old_y, p, m, ch, y, t in MOVES:
            if ch == 62:
                cards.append(
                    f'<li><a class="section-card" href="section-62.{y}.html">\n'
                    f'<span class="section-num">62.{y}</span>\n'
                    f'<span class="section-title">{t}</span>\n'
                    f'<span class="section-desc">Core production engineering.</span>\n'
                    f'</a></li>'
                )
        text = re.sub(
            r'<ul class="sections-list">[\s\S]*?</ul>',
            '<ul class="sections-list">\n' + '\n'.join(cards) + '\n</ul>',
            text,
            count=1
        )
        # Strip any leftover section cards for sections that moved
        for old_y in [3, 4, 5, 6, 7, 8, 9, 10, 11]:
            text = re.sub(
                rf'<li>\s*<a class="section-card" href="section-62\.{old_y}\.html">[\s\S]*?</a>\s*</li>\s*',
                '',
                text
            )
        # Also strip any second sections-list ul block (orphan)
        text = re.sub(
            r'<ul class="sections-list">\s*</ul>\s*',
            '',
            text
        )
        ch62_idx.write_text(text, encoding='utf-8')
        print('  Ch 62 index updated')

    # Step 5: update Part 13 index — add chapter cards for 63, 64, 65, 66
    print('Step 5: update Part 13 index')
    part13_idx = ROOT / PART13 / 'index.html'
    text = part13_idx.read_text(encoding='utf-8')
    new_cards_p13 = ''
    for new_ch in (63, 64, 65, 66):
        if f'module-' in text and CHAPTER_TEMPLATES[new_ch] and f'module-{new_ch}-' in text:
            continue
        module = next(m for old_y, p, m, ch, y, t in MOVES if ch == new_ch)
        title = CHAPTER_TEMPLATES[new_ch][0]
        if f'{module}/' in text:
            continue
        new_card = f'<div class="chapter-card">\n'
        new_card += f'<div class="chapter-card-header"><span class="mod-num">Chapter {new_ch}</span> {title}</div>\n'
        new_card += f'<div class="chapter-card-body">\n<ul class="section-list">\n'
        for old_y, p, m, ch, y, t in MOVES:
            if ch == new_ch:
                new_card += f'<li><a href="{module}/section-{ch}.{y}.html"><span class="sec-num">{ch}.{y}</span> {t}</a></li>\n'
        new_card += '</ul>\n</div>\n</div>\n'
        new_cards_p13 += new_card
    if new_cards_p13:
        text = text.replace('</main>', new_cards_p13 + '</main>', 1)
        part13_idx.write_text(text, encoding='utf-8')
        print('  Part 13 index updated with new chapter cards')

    # Step 6: update Part 12 index — add Ch 60 (Edge)
    print('Step 6: update Part 12 index')
    part12_idx = ROOT / PART12 / 'index.html'
    text = part12_idx.read_text(encoding='utf-8')
    if 'module-60-edge-on-device-llms/' not in text:
        title = CHAPTER_TEMPLATES[60][0]
        new_card = f'<div class="chapter-card">\n'
        new_card += f'<div class="chapter-card-header"><span class="mod-num">Chapter 60</span> {title}</div>\n'
        new_card += '<div class="chapter-card-body">\n<ul class="section-list">\n'
        for old_y, p, m, ch, y, t in MOVES:
            if ch == 60:
                new_card += f'<li><a href="module-60-edge-on-device-llms/section-{ch}.{y}.html"><span class="sec-num">{ch}.{y}</span> {t}</a></li>\n'
        new_card += '</ul>\n</div>\n</div>\n'
        text = text.replace('</main>', new_card + '</main>', 1)
        part12_idx.write_text(text, encoding='utf-8')
        print('  Part 12 index updated with Ch 60')

    # Step 7: cross-ref rewrite globally
    print('Step 7: rewrite cross-refs')
    move_map = {}
    for old_y, new_part, new_module, new_ch, new_y, _ in MOVES:
        move_map[old_y] = (new_part, new_module, new_ch, new_y)
    SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
            'source_fix_backups', 'pagefind', 'templates', '.claude',
            '.book-update', 'vendor', 'docs'}
    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP:
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Sentinel pattern: replace old paths with sentinels first
        for old_y in sorted(move_map.keys(), reverse=True):  # 11 before 1 to avoid prefix collision
            text = re.sub(
                rf'(href="[^"]*?)part-13-llmops-lifecycle/module-62-production-engineering-core/section-62\.{old_y}\.html',
                rf'\1__MOVE_62_{old_y}__',
                text
            )
        # Replace sentinels with new paths
        for old_y, (new_part, new_module, new_ch, new_y) in move_map.items():
            # Determine depth: count `../` prefix in the href
            sentinel = f'__MOVE_62_{old_y}__'
            # Need to handle each occurrence with its actual relative depth.
            # Use a regex that captures the prefix `../` portion.
            def replace_sentinel(m):
                prefix = m.group(1)  # everything before the sentinel
                # Count how many `../` are in the prefix's tail leading up to href content
                # Use the part-XX-... pattern: prefix already has correct depth to reach root-level part dirs
                # So we just rebuild with new_part/new_module/section-new_ch.new_y.html
                return f'{prefix}{new_part}/{new_module}/section-{new_ch}.{new_y}.html'
            text = re.sub(
                rf'(href="[^"]*?){re.escape(sentinel)}',
                replace_sentinel,
                text
            )
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Cross-refs updated in {n_files} files')


if __name__ == '__main__':
    main()
