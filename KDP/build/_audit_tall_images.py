"""Find all book images with extreme aspect ratios likely to clip in EPUB."""
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
tall_images = []
total = 0

for p in ROOT.rglob('*.png'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in ['node_modules', 'tools/', 'KDP/output/',
                              '.git', 'pagefind', 'temp_epub']):
        continue
    try:
        w, h = Image.open(p).size
    except Exception:
        continue
    total += 1
    ratio = h / w if w else 0
    if ratio > 1.4 and h > 1200:  # taller than 1.4× and over 1200px tall
        tall_images.append((p, w, h, ratio))

# Also check JPG
for p in ROOT.rglob('*.jpg'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in ['node_modules', 'tools/', 'KDP/output/',
                              '.git', 'pagefind', 'temp_epub', 'cover']):
        continue
    try:
        w, h = Image.open(p).size
    except Exception:
        continue
    total += 1
    ratio = h / w if w else 0
    if ratio > 1.4 and h > 1200:
        tall_images.append((p, w, h, ratio))

print(f'Audited {total} images.')
print(f'Images at risk of clipping (taller than 1.4x AND >1200px tall): {len(tall_images)}')
print()
for p, w, h, r in sorted(tall_images, key=lambda x: -x[3])[:25]:
    rel = str(p).replace(str(ROOT)+'\\', '').replace('\\', '/')
    print(f'  {w:4}x{h:5}  ratio={r:.2f}  {rel}')
