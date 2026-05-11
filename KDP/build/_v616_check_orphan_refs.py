"""Confirm 23 orphan module-06 images have ZERO external references."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
orphans = [
    'adam-optimizer-navigator.png', 'chinchilla-vs-kaplan.png', 'clm-vs-mlm-puzzle.png',
    'data-curation-gold-panning.png', 'data-curation-pipeline.png', 'deduplication-clone-detector.png',
    'distributed-training-gpus.png', 'distributed-training-orchestra.png', 'emergent-abilities-butterfly.png',
    'figure-6.3.6.png', 'figure-6.5.3.png', 'gpt-scaling-rocket.png', 'learning-rate-warmup.png',
    'production-training-architecture', 'production-training-data-plane', 'production-training-reliability-plane',
    'scaling-laws-kitchen.png', 'scaling-laws-power-law.png', 'switch-transformer-moe-layer.png',
    'fig-6.1.4-param-growth.png.bak2',
]
SKIP_DIRS = ('node_modules', '.git', 'pagefind', 'KDP/build', 'KDP\\build')
SKIP_OWN = 'part-2-understanding-llms/module-06-pretraining-scaling-laws/images'
EXTS = {'.html', '.css', '.opf', '.ncx', '.xhtml', '.xml', '.py', '.md', '.json', '.txt'}

for name in orphans:
    n = 0
    samples = []
    for p in ROOT.rglob('*'):
        if not p.is_file():
            continue
        sp = str(p).replace('\\', '/')
        if any(s in sp for s in SKIP_DIRS):
            continue
        if SKIP_OWN in sp:
            continue
        if p.suffix.lower() not in EXTS:
            continue
        try:
            t = p.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if name in t:
            n += 1
            if len(samples) < 2:
                samples.append(sp)
    if n == 0:
        print(f'  {name}: 0 external refs  [safe to delete]')
    else:
        print(f'  {name}: {n} refs')
        for s in samples:
            print(f'    {s}')
