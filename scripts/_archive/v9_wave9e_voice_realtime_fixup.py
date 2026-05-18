"""Wave 9 step E fixup: migrate images and clean up empty old chapter dirs."""
from pathlib import Path
import re
import shutil
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
PART = 'part-8-conversational-ai-with-llms'
CH37_DIR = ROOT / PART / 'module-37-conversational-ai'
CH38_DIR = ROOT / PART / 'module-38-tools-of-the-trade'
CH39_DIR = ROOT / PART / 'module-39-streaming-realtime-multimodal'
CH40_DIR = ROOT / PART / 'module-40-voice-realtime-multimodal'
CH41_DIR = ROOT / PART / 'module-41-conv-ai-tools'


def migrate_images_for(target_dir, *src_dirs):
    """For each section in target_dir, find image refs and copy from src_dirs."""
    target_img = target_dir / 'images'
    target_img.mkdir(exist_ok=True)
    needed = set()
    for f in sorted(target_dir.glob('section-*.html')):
        text = f.read_text(encoding='utf-8')
        for m in re.finditer(r'src="images/([^"]+)"', text):
            needed.add(m.group(1))
    moved = 0
    for img in needed:
        dst = target_img / img
        if dst.exists():
            continue
        for src_dir in src_dirs:
            src = src_dir / 'images' / img
            if src.exists():
                r = subprocess.run(
                    ['git', 'mv', str(src), str(dst)],
                    cwd=ROOT, capture_output=True, text=True
                )
                if r.returncode == 0:
                    moved += 1
                else:
                    shutil.copy2(src, dst)
                    moved += 1
                break
        else:
            print(f'  MISSING: {img} not in {[s.name for s in src_dirs]}')
    if moved:
        print(f'  Migrated {moved} images to {target_dir.name}')


def main():
    # Migrate images: Ch 40 pulls from Ch 37 + Ch 39
    migrate_images_for(CH40_DIR, CH37_DIR, CH39_DIR)
    # Ch 41 pulls from Ch 38
    migrate_images_for(CH41_DIR, CH38_DIR)

    # Now remove old empty chapter dirs (after image migration so nothing strands)
    for old in [CH38_DIR, CH39_DIR]:
        if old.exists():
            # Are there any remaining tracked files?
            r = subprocess.run(['git', 'ls-files', str(old.relative_to(ROOT))],
                               cwd=ROOT, capture_output=True, text=True)
            remaining = [l for l in r.stdout.strip().split('\n') if l]
            print(f'  {old.name}: {len(remaining)} tracked file(s) remaining')
            # Force-remove any leftover image files (they should've been migrated)
            if remaining:
                for f in remaining:
                    subprocess.run(['git', 'rm', '-f', f], cwd=ROOT, capture_output=True)
                    print(f'    Removed leftover {f}')
            # Remove the dir physically if it still exists (it may have empty images/)
            if old.exists():
                try:
                    shutil.rmtree(old)
                    print(f'  Removed {old.name} dir')
                except OSError as e:
                    print(f'  Could not remove {old}: {e}')


if __name__ == '__main__':
    main()
