"""Wave 5: realize v9 part structure (16 parts, chapters in correct parts).

Does NOT renumber chapters to canonical 0-83 — that's a follow-up.
This wave gets every chapter into its v9 target part directory.

Plan:
  1. Use .__tmp__ intermediate names to avoid collisions
  2. Move chapters from old part dirs to staging
  3. Create new part dirs with correct v9 slugs
  4. Move chapters from staging to new part dirs
  5. Rewrite cross-refs (path prefixes for moved chapters)
  6. Regenerate ToC, part indexes
"""
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

# Mapping: current_part / chapter -> target_new_part_slug
# Each entry: (current_part_dir, chapter_module_name, new_part_slug)
CHAPTER_MOVES = [
    # Part 5 (Retrieval+Conversation) splits between new VII (Retrieval+IE) and new VIII (Conv AI)
    ('part-5-retrieval-conversation', 'module-22-embeddings-vector-db',
     'part-7-retrieval-information-extraction-with-llms'),
    ('part-5-retrieval-conversation', 'module-23-rag',
     'part-7-retrieval-information-extraction-with-llms'),
    ('part-5-retrieval-conversation', 'module-42-cross-modal-reasoning-rag',
     'part-7-retrieval-information-extraction-with-llms'),
    ('part-5-retrieval-conversation', 'module-24-conversational-ai',
     'part-8-conversational-ai-with-llms'),
    ('part-5-retrieval-conversation', 'module-38-streaming-realtime-multimodal',
     'part-8-conversational-ai-with-llms'),
    ('part-5-retrieval-conversation', 'module-25-tools-of-the-trade',
     'part-8-conversational-ai-with-llms'),  # Tools-Retrieval becomes Tools-Conv (will split in Wave 9)
    # Part 7 (Multimodal) -> all goes to new V (Multimodal LLMs)
    ('part-7-multimodal-generation', 'module-32-audio-music-generation',
     'part-5-multimodal-llms'),
    ('part-7-multimodal-generation', 'module-34-document-understanding-ocr',
     'part-5-multimodal-llms'),
    ('part-7-multimodal-generation', 'module-35-vision-language-models',
     'part-5-multimodal-llms'),
    ('part-7-multimodal-generation', 'module-36-3d-generation-neural-scenes',
     'part-5-multimodal-llms'),
    ('part-7-multimodal-generation', 'module-39-vla-models',
     'part-5-multimodal-llms'),
    ('part-7-multimodal-generation', 'module-43-tools-of-the-trade',
     'part-5-multimodal-llms'),
    # Part 9 (Safety) splits between new X (Security) and new XI (Ethics)
    ('part-9-safety-security-ethics', 'module-49-adversarial-security-red-team',
     'part-10-llm-security-runtime-safety'),
    ('part-9-safety-security-ethics', 'module-50-guardrails-runtime-safety',
     'part-10-llm-security-runtime-safety'),
    ('part-9-safety-security-ethics', 'module-51-agent-safety-autonomy',
     'part-10-llm-security-runtime-safety'),
    ('part-9-safety-security-ethics', 'module-52-privacy-data-protection',
     'part-10-llm-security-runtime-safety'),
    ('part-9-safety-security-ethics', 'module-53-bias-fairness',
     'part-11-llm-ethics-trust-governance'),
    ('part-9-safety-security-ethics', 'module-55-regulation-compliance',
     'part-11-llm-ethics-trust-governance'),
    ('part-9-safety-security-ethics', 'module-56-watermarking-provenance',
     'part-11-llm-ethics-trust-governance'),
    ('part-9-safety-security-ethics', 'module-58-environmental-sustainability',
     'part-11-llm-ethics-trust-governance'),
    ('part-9-safety-security-ethics', 'module-60-tools-of-the-trade',
     'part-10-llm-security-runtime-safety'),  # Tools-Safety: place in Security; Ethics gets new Tools in Wave 9
    # Part 10 (LLMOps) splits between new XII (Scale) and new XIII (LLMOps)
    ('part-10-llmops', 'module-61-compute-planning',
     'part-12-llm-systems-at-scale'),
    ('part-10-llmops', 'module-84-frontier-systems-hardware',
     'part-12-llm-systems-at-scale'),
    ('part-10-llmops', 'module-62-production-engineering-core',
     'part-13-llmops-lifecycle'),
]

# Pure part directory renames (chapters stay)
PART_RENAMES = [
    ('part-1-foundations', 'part-1-llm-building-blocks'),
    ('part-4-training-adapting', 'part-4-training-adaptation'),
    ('part-8-evaluation-production', 'part-9-llm-evaluation-observability'),
    ('part-11-designing-llm-products', 'part-14-designing-llm-agent-products'),
    ('part-12-applications-across-industries', 'part-15-applications-of-llms-across-industries'),
    ('part-13-frontiers', 'part-16-llm-agentic-ai-research-frontiers'),
]

# Old part dirs that become empty (after their chapters move) and should be deleted
OLD_EMPTY_PARTS = [
    'part-5-retrieval-conversation',
    'part-7-multimodal-generation',
    'part-9-safety-security-ethics',
    'part-10-llmops',
]

# New parts that are pure NEW (didn't exist before chapter moves)
NEW_PART_INFO = [
    ('part-5-multimodal-llms', 'V', 'Multimodal LLMs',
     'Vision-language and Omni models, image/video/audio generation, document understanding, 3D, embodied AI / VLA / robotics.'),
    ('part-7-retrieval-information-extraction-with-llms', 'VII', 'Retrieval & Information Extraction with LLMs',
     'Embeddings, structured information extraction & NER, RAG, knowledge graphs, cross-modal retrieval.'),
    ('part-8-conversational-ai-with-llms', 'VIII', 'Conversational AI with LLMs',
     'Dialogue architecture, memory, multi-turn flows, voice and realtime multimodal assistants.'),
    ('part-10-llm-security-runtime-safety', 'X', 'LLM Security & Runtime Safety',
     'Adversarial threats, guardrails, agent safety, privacy, security tooling.'),
    ('part-11-llm-ethics-trust-governance', 'XI', 'LLM Ethics, Trust & Governance',
     'Bias and hallucination, provenance and transparency, regulation and compliance, frontier safety.'),
    ('part-12-llm-systems-at-scale', 'XII', 'LLM Systems at Scale',
     'Compute planning, distributed training systems, hardware and chip diversity, edge and on-device LLMs.'),
    ('part-13-llmops-lifecycle', 'XIII', 'LLMOps & Lifecycle Management',
     'AI gateways and routing, workflow orchestration, containers, reliability and SLOs, model registry and lifecycle.'),
]


def git_mv(src, dst):
    if not src.exists() or dst.exists(): return False
    r = subprocess.run(['git', 'mv', str(src), str(dst)], cwd=ROOT,
                      capture_output=True, text=True)
    return r.returncode == 0


def git_rm(p):
    if not p.exists(): return False
    r = subprocess.run(['git', 'rm', '-rf', str(p)], cwd=ROOT,
                      capture_output=True, text=True)
    return r.returncode == 0


def step1_move_chapters_to_staging():
    """Move chapters from their current parts into a staging area
    (using __tmp__ prefix on the part to avoid name collisions during the part-rename phase).
    """
    print('--- Step 1: stage chapters in __tmp__ dirs ---')
    n = 0
    for old_part, chapter, _new_part in CHAPTER_MOVES:
        src = ROOT / old_part / chapter
        staged = ROOT / '__chapter_staging__' / chapter
        if not src.exists(): continue
        staged.parent.mkdir(parents=True, exist_ok=True)
        if git_mv(src, staged):
            n += 1
    print(f'  Staged {n} chapters')


def step2_rename_parts():
    """Rename pure-rename parts and clean up empty old parts."""
    print('--- Step 2: rename part directories ---')
    # First, pure renames (with tmp intermediate)
    for old, new in PART_RENAMES:
        sp = ROOT / old
        dp = ROOT / new
        tmp = ROOT / (new + '.__tmp__')
        if sp.exists() and not dp.exists() and not tmp.exists():
            if git_mv(sp, tmp):
                pass
    for old, new in PART_RENAMES:
        tmp = ROOT / (new + '.__tmp__')
        dp = ROOT / new
        if tmp.exists() and not dp.exists():
            if git_mv(tmp, dp):
                print(f'  Renamed: {old} -> {new}')

    # Delete now-empty old parts (after chapters have been staged)
    print('--- Step 2b: delete empty old parts ---')
    for empty in OLD_EMPTY_PARTS:
        p = ROOT / empty
        if p.exists():
            # Should only contain index.html + images (no module-* subdirs)
            remaining_mods = list(p.glob('module-*/'))
            if not remaining_mods:
                if git_rm(p):
                    print(f'  Deleted: {empty}')
            else:
                print(f'  SKIP {empty}: still has {len(remaining_mods)} modules')


def step3_create_new_parts():
    """Create new part directories with index.html scaffolding."""
    print('--- Step 3: create new part dirs ---')
    for slug, roman, title, subtitle in NEW_PART_INFO:
        new_part_dir = ROOT / slug
        if new_part_dir.exists(): continue
        new_part_dir.mkdir(parents=True)
        (new_part_dir / 'images').mkdir(exist_ok=True)
        skel = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<meta content="Part {roman}: {title}. {subtitle}" name="description"/>
<title>Part {roman}: {title} | Building Conversational AI with LLMs and Agents</title>
<link href="../styles/book.css" rel="stylesheet"/>
<script defer="" src="../scripts/book.js"></script>
<link href="../pagefind/pagefind-ui.css" rel="stylesheet"/>
<script defer="" src="../pagefind/pagefind-ui.js"></script>
</head>
<body class="index-page part-index">
<header class="chapter-header">
<nav class="header-nav">
<a class="book-title-link" href="../index.html">Building Conversational AI with LLMs and Agents</a>
<a class="toc-link" href="../toc.html" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
</nav>
<div class="page-breadcrumb" data-pagefind-meta="part"><a href="../index.html">Building Conversational AI</a><span class="bc-sep">&rsaquo;</span><span class="bc-current">Part {roman}</span></div>
<h1>Part {roman}: {title}</h1>
</header>
<main class="content">
<span class="pagefind-meta-injected" data-pagefind-meta="part:Part {roman}: {title}" hidden=""></span>
<h2>Part Overview</h2>
<p>{subtitle}</p>
<div class="callout big-picture">
<div class="callout-title">Big Picture</div>
<p>{subtitle}</p>
</div>
<h2>Chapters</h2>
<div class="chapter-card-list">
<!-- Chapter cards added by rebuild script -->
</div>
</main>
<footer><p>Fifteenth Edition, 2026 &middot; <a href="../toc.html">Contents</a></p></footer>
</body>
</html>
'''
        (new_part_dir / 'index.html').write_text(skel, encoding='utf-8')
        print(f'  Created: {slug}')


def step4_unstage_to_new_parts():
    """Move staged chapters from __chapter_staging__ to their target new parts."""
    print('--- Step 4: unstage chapters into new parts ---')
    n = 0
    staging = ROOT / '__chapter_staging__'
    for old_part, chapter, new_part in CHAPTER_MOVES:
        staged = staging / chapter
        dst = ROOT / new_part / chapter
        if staged.exists() and not dst.exists():
            (ROOT / new_part).mkdir(parents=True, exist_ok=True)
            if git_mv(staged, dst):
                n += 1
                print(f'  {chapter} -> {new_part}/')
    # Clean up staging dir
    if staging.exists() and not list(staging.iterdir()):
        staging.rmdir()
    print(f'  Unstaged {n} chapters')


def step5_rewrite_part_refs():
    """Update all cross-refs to use new part slugs."""
    print('--- Step 5: rewrite part-path references ---')
    SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
            'source_fix_backups', 'pagefind', 'templates', '.claude',
            '.book-update', 'vendor', 'docs', '__chapter_staging__'}

    # Build mapping
    part_renames_map = dict(PART_RENAMES)
    chapter_move_map = {}  # old_part -> {chapter: new_part}
    for old_part, ch, new_part in CHAPTER_MOVES:
        chapter_move_map.setdefault(old_part, {})[ch] = new_part

    n_files = 0
    for p in sorted(ROOT.rglob('*.html')):
        if set(p.parts) & SKIP: continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Apply part renames (e.g., part-1-foundations → part-1-llm-building-blocks)
        for old_part, new_part in part_renames_map.items():
            text = text.replace(f'/{old_part}/', f'/{new_part}/')
            text = text.replace(f'"{old_part}/', f'"{new_part}/')
        # Apply chapter moves (path includes both old part and chapter)
        for old_part, ch_to_new in chapter_move_map.items():
            for ch, new_part in ch_to_new.items():
                text = text.replace(f'/{old_part}/{ch}/', f'/{new_part}/{ch}/')
                text = text.replace(f'"{old_part}/{ch}/', f'"{new_part}/{ch}/')
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n_files += 1
    print(f'  Updated refs in {n_files} files')


def main():
    print('=== WAVE 5: realize v9 part structure ===\n')
    step1_move_chapters_to_staging()
    step2_rename_parts()
    step3_create_new_parts()
    step4_unstage_to_new_parts()
    step5_rewrite_part_refs()
    print('\nWave 5 structural moves complete.')


if __name__ == '__main__':
    main()
