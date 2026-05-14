"""v806: Resize images that are too tall for EPUB page layout.

Strategy:
  - Find all PNGs/JPGs with height > 2000px AND aspect ratio > 1.4
  - Cap height at 2000px (keeps aspect ratio)
  - This combined with CSS max-height: 90vh prevents page clipping
  - Skip backups, only resize LIVE images used in book

Backup originals to KDP/build/source_fix_backups/tall_resize_<date>/
"""
from pathlib import Path
from PIL import Image
import shutil, time

ROOT = Path(__file__).resolve().parents[2]
BACKUP_DIR = ROOT / 'KDP/build/source_fix_backups' / f'tall_resize_{time.strftime("%Y%m%d_%H%M%S")}'
MAX_HEIGHT = 1800  # cap height
MIN_HEIGHT = 1200  # only resize if originally taller than this
MIN_ASPECT = 1.4   # only resize if taller than 1.4x wider

n_resized = 0
n_skipped = 0
total_saved = 0

for ext in ('*.png', '*.jpg', '*.jpeg'):
    for p in ROOT.rglob(ext):
        sp = str(p).replace('\\', '/')
        # Skip backups, output, vendor, tools dirs
        if any(s in sp for s in ['node_modules', '/output/', '.git', 'pagefind',
                                  'temp_epub', 'source_fix_backups', 'vendor/',
                                  'tools/', 'KDP/build/audit_thumbs', 'KDP/cover']):
            continue
        try:
            img = Image.open(p)
            w, h = img.size
        except Exception:
            continue
        if h < MIN_HEIGHT:
            continue
        ratio = h / w if w else 0
        if ratio < MIN_ASPECT:
            continue
        if h <= MAX_HEIGHT:
            continue
        # Resize: keep aspect ratio, cap height at MAX_HEIGHT
        scale = MAX_HEIGHT / h
        new_w = int(w * scale)
        new_h = MAX_HEIGHT
        # Backup
        rel = p.relative_to(ROOT)
        backup_path = BACKUP_DIR / rel
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, backup_path)
        # Resize
        orig_size = p.stat().st_size
        resized = img.resize((new_w, new_h), Image.LANCZOS)
        if p.suffix.lower() in ('.jpg', '.jpeg'):
            resized.save(p, 'JPEG', quality=88, optimize=True)
        else:  # png
            if resized.mode == 'RGBA':
                resized.save(p, 'PNG', optimize=True)
            else:
                resized.save(p, 'PNG', optimize=True)
        new_size = p.stat().st_size
        saved = orig_size - new_size
        total_saved += saved
        n_resized += 1
        if n_resized <= 30:
            print(f'  {w}x{h} -> {new_w}x{new_h}  (-{saved//1024} KB)  {str(rel).replace(chr(92), "/")}')

print()
print(f'Resized {n_resized} tall images.')
print(f'Backup at: {BACKUP_DIR}')
print(f'Total disk saved: {total_saved/1024/1024:.2f} MB')
