"""Generate the cartoon-comic raster images from comic-manifest.jsonl via
Gemini 2.5 Flash Image. Loads GEMINI_API_KEY from .env.all if not in env.
Resumable: skips images already on disk. Does NOT edit HTML (insertion is a
separate, judgment-based step handled by agents).
"""
from __future__ import annotations
import argparse, base64, io, json, os, re, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / '.book-update' / 'comic-manifest.jsonl'
LOG = ROOT / '.book-update' / 'comicgen-run.log'
ENDPOINT = ('https://generativelanguage.googleapis.com/v1beta/'
            'models/gemini-2.5-flash-image:generateContent')

STYLE_SUFFIX = (
    " Children's-book watercolor-over-ink cartoon, warm friendly palette, "
    "soft gradients, white or light background, no watermark, no real photos, "
    "no extra text beyond the labels named in this prompt, 16:9 aspect ratio."
)


def load_key():
    k = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if k:
        return k
    envf = ROOT / '.env.all'
    if envf.exists():
        for line in envf.read_text(encoding='utf-8').splitlines():
            m = re.match(r'\s*(?:GEMINI_API_KEY|GOOGLE_API_KEY)\s*=\s*(.+)\s*$', line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    return None


def call_gemini(prompt, key):
    import requests
    payload = {'contents': [{'parts': [{'text': prompt}]}],
               'generationConfig': {'responseModalities': ['IMAGE']}}
    try:
        r = requests.post(f'{ENDPOINT}?key={key}', json=payload, timeout=120)
    except Exception as e:
        print(f'  ! network: {e}'); return None
    if r.status_code != 200:
        print(f'  ! HTTP {r.status_code}: {r.text[:160]}'); return None
    try:
        parts = r.json()['candidates'][0]['content']['parts']
    except Exception:
        print('  ! no candidates'); return None
    for p in parts:
        if 'inlineData' in p:
            return base64.b64decode(p['inlineData'].get('data', ''))
    print('  ! no image part'); return None


def save_jpeg(b, dest):
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(b))
        if im.mode != 'RGB':
            im = im.convert('RGB')
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, 'JPEG', quality=82, optimize=True)
        return True
    except Exception as e:
        print(f'  ! save: {e}'); return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--kind', choices=['COMIC', 'MENTAL-MAP', 'all'], default='all')
    ap.add_argument('--sleep', type=float, default=1.5)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--manifest', default=None,
                    help='manifest jsonl (default .book-update/comic-manifest.jsonl)')
    args = ap.parse_args()

    manifest = Path(args.manifest) if args.manifest else MANIFEST
    rows = [json.loads(l) for l in manifest.open(encoding='utf-8') if l.strip()]
    if args.kind != 'all':
        rows = [r for r in rows if r['kind'] == args.kind]
    rows = [r for r in rows if r.get('section_exists')]
    key = None
    if not args.dry_run:
        key = load_key()
        if not key:
            print('ERROR: no GEMINI_API_KEY (env or .env.all)'); sys.exit(2)
    done = skip = fail = 0
    with LOG.open('a', encoding='utf-8') as logf:
        for r in rows:
            if args.limit and done >= args.limit:
                break
            sec = Path(r['section'])
            dest = sec.parent / r['filename']
            if dest.exists():
                skip += 1; continue
            print(f"[{r['chap_sec']} #{r['num']} {r['kind']}] -> {dest.relative_to(ROOT)}")
            if args.dry_run:
                print(f"  {r['prompt'][:110]}..."); continue
            b = call_gemini(r['prompt'] + STYLE_SUFFIX, key)
            if not b:
                fail += 1; logf.write(f"FAIL {r['filename']}\n"); time.sleep(args.sleep); continue
            if save_jpeg(b, dest):
                done += 1; logf.write(f"OK {dest}\n"); print('  OK')
            else:
                fail += 1; logf.write(f"FAILSAVE {r['filename']}\n")
            time.sleep(args.sleep)
    print(f"\nGenerated {done}, skipped {skip} (exist), failed {fail}")


if __name__ == '__main__':
    main()
