"""Restore images that were deleted along with merged source chapters.

When a chapter merge happened (e.g. Ch 33 → Ch 32), `git rm -rf` of the
source chapter also removed source/images/. The merged section files still
reference those images. Restore the images from the git history into the
TARGET chapter's images/ folder.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', 'node_modules', 'KDP', 'build', 'temp_ebook', 'temp_epub',
        'source_fix_backups', 'pagefind', 'templates', '.claude',
        '.book-update', 'vendor', 'docs'}

# Mapping: source_module → target_module (which chapter was merged into which)
# This is the Wave 3 merge map
SOURCE_TO_TARGET = {
    'module-02-tokenization-subword-models': ('part-1-foundations', 'module-01-foundations-nlp-text-representation'),
    'module-12-tools-of-the-trade': ('part-2-understanding-llms', 'module-11-interpretability'),
    'module-33-video-generation': ('part-7-multimodal-generation', 'module-32-audio-music-generation'),
    'module-37-unified-multimodal-omni': ('part-7-multimodal-generation', 'module-35-vision-language-models'),
    'module-40-llm-robotics': ('part-7-multimodal-generation', 'module-39-vla-models'),
    'module-54-hallucination-truthfulness': ('part-9-safety-security-ethics', 'module-53-bias-fairness'),
    'module-57-transparency-documentation': ('part-9-safety-security-ethics', 'module-56-watermarking-provenance'),
    'module-59-frontier-safety-open-problems': ('part-9-safety-security-ethics', 'module-58-environmental-sustainability'),
    'module-64-product-management': ('part-11-designing-llm-products', 'module-63-ideation'),
    'module-65-strategy-prioritization': ('part-11-designing-llm-products', 'module-63-ideation'),
    'module-68-prototype-to-production': ('part-11-designing-llm-products', 'module-63-ideation'),
    'module-67-mvp': ('part-11-designing-llm-products', 'module-66-vibe-coding'),
    'module-79-creative-industries': ('part-12-applications-across-industries', 'module-78-manufacturing-llms'),
    'module-80-recommendation-search': ('part-12-applications-across-industries', 'module-78-manufacturing-llms'),
}


def restore_images_from_git():
    """For each source module, find its images in git history and restore them."""
    n_restored = 0
    for src_mod, (tgt_part, tgt_mod) in SOURCE_TO_TARGET.items():
        # Find the git path of the source module's images
        # Use git ls-tree on the most recent commit that had these files
        r = subprocess.run(
            ['git', 'log', '--all', '--diff-filter=D', '--name-only',
             '--format=', '-1', f'--diff-filter=D'],
            cwd=ROOT, capture_output=True, text=True
        )
        # That doesn't quite work — use a different approach
        # Find the commit just BEFORE Wave 3 deletions (HEAD~1 for Wave 1 commit)
        r = subprocess.run(
            ['git', 'rev-parse', 'HEAD~1'],
            cwd=ROOT, capture_output=True, text=True
        )
        wave1_commit = r.stdout.strip()
        if not wave1_commit: continue

        # List images in the source module at Wave 1 commit
        # Find all dirs that match the source mod name
        r = subprocess.run(
            ['git', 'ls-tree', '-r', '--name-only', wave1_commit],
            cwd=ROOT, capture_output=True, text=True
        )
        all_files = r.stdout.splitlines()
        src_images = [f for f in all_files if f'/{src_mod}/images/' in f]

        if not src_images: continue

        tgt_images_dir = ROOT / tgt_part / tgt_mod / 'images'
        tgt_images_dir.mkdir(parents=True, exist_ok=True)

        for img_path in src_images:
            img_name = img_path.split('/')[-1]
            dst = tgt_images_dir / img_name
            if dst.exists(): continue  # already there
            # Restore from git
            r = subprocess.run(
                ['git', 'show', f'{wave1_commit}:{img_path}'],
                cwd=ROOT, capture_output=True
            )
            if r.returncode == 0 and r.stdout:
                dst.write_bytes(r.stdout)
                n_restored += 1
        print(f'  {src_mod} -> {tgt_mod}/images/: {len(src_images)} images')
    print(f'\nTotal images restored: {n_restored}')


def main():
    print('=== Wave 3 image restoration ===\n')
    restore_images_from_git()


if __name__ == '__main__':
    main()
