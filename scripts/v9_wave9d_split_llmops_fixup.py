"""Wave 9 step D fixup: fix bare cross-refs and migrate images after LLMOps split.

Same pattern as v9_wave9c_split_rag_fixup.py.
"""
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
PART13 = 'part-13-llmops-lifecycle'
PART12 = 'part-12-llm-systems-at-scale'
CH62_DIR = ROOT / PART13 / 'module-62-production-engineering-core'

# old_y -> (new_part, new_module, new_ch, new_y)
MOVE_MAP = {
    1: (PART13, 'module-62-production-engineering-core', 62, 1),
    2: (PART13, 'module-62-production-engineering-core', 62, 2),
    3: (PART13, 'module-63-ai-gateways-routing', 63, 1),
    4: (PART13, 'module-64-workflow-orchestration', 64, 1),
    5: (PART12, 'module-60-edge-on-device-llms', 60, 1),
    6: (PART13, 'module-66-reliability-slos-registry', 66, 1),
    7: (PART13, 'module-65-containers-kubernetes', 65, 1),
    8: (PART13, 'module-65-containers-kubernetes', 65, 2),
    9: (PART13, 'module-65-containers-kubernetes', 65, 3),
    10: (PART13, 'module-65-containers-kubernetes', 65, 4),
    11: (PART13, 'module-65-containers-kubernetes', 65, 5),
}


def rewrite_bare_section_hrefs(file_path, current_module, current_part):
    text = file_path.read_text(encoding='utf-8')
    orig = text

    def replace(m):
        prefix = m.group(1)
        old_y = int(m.group(2))
        anchor = m.group(3) or ''
        if old_y not in MOVE_MAP:
            return m.group(0)
        new_part, new_module, new_ch, new_y = MOVE_MAP[old_y]
        if new_module == current_module:
            return f'{prefix}section-{new_ch}.{new_y}.html{anchor}'
        elif new_part == current_part:
            return f'{prefix}../{new_module}/section-{new_ch}.{new_y}.html{anchor}'
        else:
            return f'{prefix}../../{new_part}/{new_module}/section-{new_ch}.{new_y}.html{anchor}'

    text = re.sub(
        r'(href=")section-62\.(\d+)\.html(#[^"]*)?',
        replace,
        text
    )
    if text != orig:
        file_path.write_text(text, encoding='utf-8')
        return True
    return False


def migrate_images_for(target_dir, src_dir=None):
    if src_dir is None:
        src_dir = CH62_DIR / 'images'
    target_img = target_dir / 'images'
    target_img.mkdir(exist_ok=True)
    needed = set()
    for f in sorted(target_dir.glob('section-*.html')):
        text = f.read_text(encoding='utf-8')
        for m in re.finditer(r'src="images/([^"]+)"', text):
            needed.add(m.group(1))
    moved = 0
    for img in needed:
        src = src_dir / img
        dst = target_img / img
        if src.exists() and not dst.exists():
            r = subprocess.run(
                ['git', 'mv', str(src), str(dst)],
                cwd=ROOT, capture_output=True, text=True
            )
            if r.returncode == 0:
                moved += 1
            else:
                shutil.copy2(src, dst)
                moved += 1
        elif not src.exists():
            print(f'  MISSING: {img} not in source')
    if moved:
        print(f'  Migrated {moved} images to {target_dir.name}')


def main():
    # Fix bare section-62.X.html refs in each new chapter
    targets = [
        (PART13, 'module-62-production-engineering-core'),
        (PART13, 'module-63-ai-gateways-routing'),
        (PART13, 'module-64-workflow-orchestration'),
        (PART13, 'module-65-containers-kubernetes'),
        (PART13, 'module-66-reliability-slos-registry'),
        (PART12, 'module-60-edge-on-device-llms'),
    ]
    total = 0
    for part, module in targets:
        chapter_dir = ROOT / part / module
        for f in sorted(chapter_dir.glob('section-*.html')):
            if rewrite_bare_section_hrefs(f, module, part):
                total += 1
    print(f'Sections updated: {total}')

    # Migrate images
    for part, module in targets:
        if module == 'module-62-production-engineering-core':
            continue
        migrate_images_for(ROOT / part / module)


if __name__ == '__main__':
    main()
