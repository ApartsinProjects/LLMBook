"""Audit: which PNGs have no alpha (convertible to JPEG) and how much would
they save? How much do current JPEGs save at q=65 vs current?
Sample 40 PNGs and 20 JPEGs > 50 KB to project total savings."""
import io
import random
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
SKIP = ('node_modules', '.git/', 'pagefind/', 'KDP/build/', 'KDP/output/', 'KDP/validation/')

totals = {
    'png_with_alpha': [0, 0],
    'png_no_alpha':   [0, 0],
    'png_to_jpeg_save': [0, 0],
    'jpeg':           [0, 0],
    'jpeg_q65_save':  [0, 0],
}
samples = []

all_pngs, all_jpgs = [], []
for p in ROOT.rglob('*.png'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in SKIP):
        continue
    if p.stat().st_size > 50_000:
        all_pngs.append(p)
for p in ROOT.rglob('*.jpg'):
    sp = str(p).replace('\\', '/')
    if any(s in sp for s in SKIP):
        continue
    if p.stat().st_size > 50_000:
        all_jpgs.append(p)

random.seed(0)
png_sample = random.sample(all_pngs, min(40, len(all_pngs)))
jpg_sample = random.sample(all_jpgs, min(20, len(all_jpgs)))

print(f'Sampling {len(png_sample)} PNGs (>50KB), {len(jpg_sample)} JPEGs (>50KB)')
print(f'(of {len(all_pngs)} total PNGs >50KB, {len(all_jpgs)} total JPEGs >50KB in source tree)\n')

for p in png_sample:
    sz = p.stat().st_size
    try:
        im = Image.open(p)
        has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
        if has_alpha:
            totals['png_with_alpha'][0] += 1
            totals['png_with_alpha'][1] += sz
        else:
            totals['png_no_alpha'][0] += 1
            totals['png_no_alpha'][1] += sz
            buf = io.BytesIO()
            im.convert('RGB').save(buf, 'JPEG', quality=82, optimize=True)
            new_sz = len(buf.getvalue())
            saved = sz - new_sz
            if saved > 0:
                totals['png_to_jpeg_save'][0] += 1
                totals['png_to_jpeg_save'][1] += saved
                samples.append(('PNG->JPG@82', sz, new_sz, p.name[:40]))
    except Exception:
        pass

for p in jpg_sample:
    sz = p.stat().st_size
    try:
        im = Image.open(p)
        totals['jpeg'][0] += 1
        totals['jpeg'][1] += sz
        buf = io.BytesIO()
        im.convert('RGB').save(buf, 'JPEG', quality=65, optimize=True)
        new_sz = len(buf.getvalue())
        saved = sz - new_sz
        if saved > 0:
            totals['jpeg_q65_save'][0] += 1
            totals['jpeg_q65_save'][1] += saved
            samples.append(('JPG@65', sz, new_sz, p.name[:40]))
    except Exception:
        pass

print('===== Sample-level results =====')
n_w, b_w = totals['png_with_alpha']
n_no, b_no = totals['png_no_alpha']
print(f'PNG with alpha:        {n_w:>3} files, {b_w/1024:>8.1f} KB  (must keep PNG)')
print(f'PNG NO alpha:          {n_no:>3} files, {b_no/1024:>8.1f} KB  (convertible)')
n_s, b_s = totals['png_to_jpeg_save']
if b_no:
    print(f'  -> JPG q=82 saves:   {b_s/1024:>8.1f} KB  ({100*b_s/b_no:.1f}% of no-alpha PNG bytes)')
print()

n_j, b_j = totals['jpeg']
print(f'JPEGs (current):       {n_j:>3} files, {b_j/1024:>8.1f} KB')
n_q, b_q = totals['jpeg_q65_save']
if b_j:
    print(f'  -> q=65 saves:       {b_q/1024:>8.1f} KB  ({100*b_q/b_j:.1f}% of JPEG bytes)')
print()

# Project to whole image set
print('===== Projected EPUB savings =====')
# All sampled PNGs:
total_png_bytes = sum(p.stat().st_size for p in all_pngs) / 1024  # KB
total_jpg_bytes = sum(p.stat().st_size for p in all_jpgs) / 1024
no_alpha_frac = b_no / max(1, (b_w + b_no))
png_save_frac = b_s / max(1, b_no) if b_no else 0
proj_png_save_kb = total_png_bytes * no_alpha_frac * png_save_frac
jpg_save_frac = b_q / max(1, b_j) if b_j else 0
proj_jpg_save_kb = total_jpg_bytes * jpg_save_frac
print(f'PNG -> JPG conversion:  ~{proj_png_save_kb/1024:.1f} MB (across {len(all_pngs)} large PNGs)')
print(f'JPEG q=72 -> q=65:      ~{proj_jpg_save_kb/1024:.1f} MB (across {len(all_jpgs)} large JPEGs)')
print(f'Combined:               ~{(proj_png_save_kb+proj_jpg_save_kb)/1024:.1f} MB')
print()

print('===== Top per-file savings (sample) =====')
for tag, before, after, name in sorted(samples, key=lambda x: -(x[1] - x[2]))[:10]:
    print(f'  {tag:11s} {before/1024:>6.1f}KB -> {after/1024:>6.1f}KB  ({100*(before-after)/before:>4.0f}%)  {name}')
