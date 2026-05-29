"""Exhaustive per-page hunt for fixed-format HTML/CSS cues.

Beyond what audit_kindle_compliance and audit_h4_h5_h6_h7 already cover.
Reads every XHTML and looks for any of ~13 less-common patterns that
KDP's fixed-format classifier might weigh.
"""
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

EPUB = Path('KDP/output/editions/16th-edition/building-conversational-ai-llms-agents-16th-edition.epub')
if len(sys.argv) > 1:
    EPUB = Path(sys.argv[1])

# Each entry: (label, regex pattern, applies-to: ['xhtml','css','opf'])
PATTERNS = [
    ('img_px_dims',          re.compile(r'<img\b[^>]*\b(?:width|height)\s*=\s*"\d+(?:px)?"', re.IGNORECASE)),
    ('canvas_element',       re.compile(r'<canvas\b', re.IGNORECASE)),
    ('epub_page_spread',     re.compile(r'epub:type="page-spread-(?:left|right|center)"', re.IGNORECASE)),
    ('amzn_meta',            re.compile(r'<meta\b[^>]*\bname="amzn-[^"]+"', re.IGNORECASE)),
    ('amzn_attr',            re.compile(r'\bamzn:[a-z-]+\s*=', re.IGNORECASE)),
    ('xmlns_fxl_amzn',       re.compile(r'xmlns:(?:fxl|amzn|kf8)\s*=', re.IGNORECASE)),
    ('class_page_or_fxl',    re.compile(r'\bclass="[^"]*\b(?:page-\d+|spread-\d+|fxl-|comic-|panel-|fixed-page)\b', re.IGNORECASE)),
    ('inline_pos_absolute',  re.compile(r'\bstyle="[^"]*position\s*:\s*(?:absolute|fixed)[^"]*"', re.IGNORECASE)),
    ('inline_left_top_px',   re.compile(r'\bstyle="[^"]*\bleft\s*:\s*\d+px[^"]*\btop\s*:\s*\d+px', re.IGNORECASE)),
    ('media_orientation',    re.compile(r'media="\([^"]*orientation\s*:', re.IGNORECASE)),
    ('region_panel',         re.compile(r'<(?:region|panel)\b', re.IGNORECASE)),
    ('embed_iframe',         re.compile(r'<(?:embed|iframe|noscript)\b', re.IGNORECASE)),
    ('many_brs',             re.compile(r'(?:<br\s*/?>\s*){5,}', re.IGNORECASE)),  # 5+ consecutive
    ('img_fixed_size_attr',  re.compile(r'<img\b[^>]*\bheight\s*=\s*"\d+"', re.IGNORECASE)),
    ('viewport_in_body',     re.compile(r'<body\b[^>]*>(?:(?!</body>).)*?viewport', re.IGNORECASE | re.DOTALL)),
]

per_page_hits = []          # list of (file, [labels])
agg = Counter()
img_dim_examples = []

with zipfile.ZipFile(EPUB) as z:
    names = z.namelist()
    xhtml_files = [n for n in names if n.lower().endswith(('.xhtml', '.html'))]
    css_files = [n for n in names if n.lower().endswith('.css')]

    print(f'EPUB: {EPUB}')
    print(f'  size: {EPUB.stat().st_size/1024/1024:.2f} MB')
    print(f'  XHTML count: {len(xhtml_files)}')
    print(f'  CSS count:   {len(css_files)}')
    print()

    # Scan all XHTML
    for n in xhtml_files:
        try:
            content = z.read(n).decode('utf-8', errors='ignore')
        except Exception:
            continue
        hits = []
        for label, pat in PATTERNS:
            m = pat.search(content)
            if m:
                hits.append(label)
                agg[label] += 1
                if label == 'img_px_dims' and len(img_dim_examples) < 3:
                    img_dim_examples.append((n, m.group(0)[:120]))
        if hits:
            per_page_hits.append((n, hits))

    # Scan CSS (subset of patterns)
    css_agg = Counter()
    for c in css_files:
        try:
            content = z.read(c).decode('utf-8', errors='ignore')
        except Exception:
            continue
        for label in ('media_orientation', 'class_page_or_fxl'):
            pat = dict(PATTERNS)[label]
            if pat.search(content):
                css_agg[f'CSS:{label}'] += 1

# Image dimension UNIFORMITY check: are most images the same size?
# This is a KDP fixed-format hallmark (every page same panel size).
print('=' * 70)
print('AGGREGATE HITS ACROSS ALL 607 XHTML')
print('=' * 70)
if not agg and not css_agg:
    print('  No fixed-format cues found in any XHTML or CSS.')
else:
    for label, count in sorted(agg.items(), key=lambda x: -x[1]):
        sev = 'HIGH' if label in (
            'canvas_element', 'epub_page_spread', 'amzn_meta', 'amzn_attr',
            'xmlns_fxl_amzn', 'class_page_or_fxl', 'inline_left_top_px',
            'region_panel', 'media_orientation', 'viewport_in_body'
        ) else 'MED' if label in ('img_px_dims', 'img_fixed_size_attr',
                                    'embed_iframe') else 'LOW'
        print(f'  [{sev}] {label:25s}: {count} page(s)')
    for label, count in sorted(css_agg.items(), key=lambda x: -x[1]):
        print(f'  [LOW] {label:25s}: {count} CSS file(s)')

print()
print('IMAGE FIXED-SIZE EXAMPLES (first 3, if any):')
for n, snip in img_dim_examples:
    print(f'  {n}')
    print(f'    {snip}')

# Show per-page hit list (capped)
print()
print('=' * 70)
print(f'PER-PAGE HIT LIST (first 25 of {len(per_page_hits)} pages with any hit)')
print('=' * 70)
for n, hits in per_page_hits[:25]:
    print(f'  {n}')
    print(f'    -> {hits}')

# Also analyze image dimension uniformity (separately, since it's an aggregate)
print()
print('=' * 70)
print('IMAGE DIMENSION UNIFORMITY (potential scanned-page signal)')
print('=' * 70)
img_dims = Counter()
with zipfile.ZipFile(EPUB) as z:
    try:
        from PIL import Image
        import io
        for n in [x for x in z.namelist() if x.lower().endswith(('.jpg', '.jpeg', '.png'))]:
            try:
                im = Image.open(io.BytesIO(z.read(n)))
                img_dims[im.size] += 1
            except Exception:
                pass
    except ImportError:
        pass

# Most common dimensions
print(f'  Total images analyzed: {sum(img_dims.values())}')
print(f'  Distinct dimensions:   {len(img_dims)}')
print(f'  Top 10 dimensions by frequency:')
for (w, h), c in img_dims.most_common(10):
    pct = 100 * c / sum(img_dims.values())
    flag = '  <-- DOMINANT' if pct > 30 else ''
    print(f'    {w}x{h}: {c} files ({pct:.1f}%){flag}')

# Uniformity check: if any single dimension covers > 30% of all images, that's fixed-format-like
dimension_uniformity_hit = False
if img_dims:
    max_pct = max(c for c in img_dims.values()) / sum(img_dims.values()) * 100
    if max_pct > 30:
        print(f'  >>> SIGNAL: a single dimension covers {max_pct:.0f}% of images <<<')
        dimension_uniformity_hit = True
    else:
        print(f'  [OK] no dominant dimension; max single-dim share = {max_pct:.0f}%')

# Hard-gate exit: any HIGH-severity hit fails the build
HIGH_SEV_LABELS = {
    'canvas_element', 'epub_page_spread', 'amzn_meta', 'amzn_attr',
    'xmlns_fxl_amzn', 'class_page_or_fxl', 'inline_left_top_px',
    'region_panel', 'media_orientation', 'viewport_in_body',
}
high_hits = [(label, agg[label]) for label in HIGH_SEV_LABELS if agg.get(label, 0)]

print()
print('=' * 70)
if high_hits or dimension_uniformity_hit:
    print(f'RESULT: FAIL — {len(high_hits)} HIGH-severity FXL cue(s) present')
    for label, count in high_hits:
        print(f'  [FAIL] {label}: {count} hit(s)')
    if dimension_uniformity_hit:
        print(f'  [FAIL] dimension_uniformity: a single image size dominates >30%')
    print('Fix recipe: see html2kpd LESSONS.md (L-FXL-KEYWORDS, L-IMG-PX-DIMS,')
    print('  L-WEB-CHROME, L-CSS-DISALLOWED) and run the matching post-build patches.')
    sys.exit(1)
else:
    print('RESULT: PASS — no HIGH-severity FXL cues found across all pages')
    sys.exit(0)
