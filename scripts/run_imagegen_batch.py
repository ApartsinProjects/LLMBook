"""Batch-execute image generation for the HIGH+MED imagegen manifest.

Reads .book-update/imagegen-manifest.jsonl (one record per pending image),
calls Gemini 2.5 Flash Image via REST for each prompt, saves the JPEG to
the target filename relative to the source section's directory, and
flips data-imagegen-status="pending" -> data-imagegen-status="generated".

PRE-REQUISITES
- Set environment variable GOOGLE_API_KEY (or GEMINI_API_KEY) with a
  valid Google AI Studio key that has access to gemini-2.5-flash-image.
- pip install pillow requests
- ~108 records take ~10-15 minutes (one API call per image; Google rate
  limit ~60 RPM on free tier, ~360 RPM on paid).

USAGE
  /c/Python314/python scripts/run_imagegen_batch.py            # process pending
  /c/Python314/python scripts/run_imagegen_batch.py --limit 5  # do first 5 only
  /c/Python314/python scripts/run_imagegen_batch.py --dry-run  # print prompts
  /c/Python314/python scripts/run_imagegen_batch.py --resume   # skip already-generated

After each successful generation, the script:
1. Writes the JPEG to images/<filename> next to the section
2. Re-reads the section HTML and replaces data-imagegen-status="pending"
   with data-imagegen-status="generated" for that specific src
3. Logs a per-image line to .book-update/imagegen-run.log
"""
import argparse
import base64
import io
import json
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".book-update" / "imagegen-manifest.jsonl"
RUN_LOG = ROOT / ".book-update" / "imagegen-run.log"

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash-image:generateContent"
)


def get_api_key():
    for var in ("GOOGLE_API_KEY", "GEMINI_API_KEY"):
        key = os.environ.get(var)
        if key:
            return key
    return None


def call_gemini(prompt: str, api_key: str) -> bytes | None:
    """Call Gemini 2.5 Flash Image and return JPEG bytes, or None on error."""
    try:
        import requests
    except ImportError:
        print("ERROR: pip install requests", file=sys.stderr)
        sys.exit(1)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    headers = {"Content-Type": "application/json"}
    url = f"{GEMINI_ENDPOINT}?key={api_key}"
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
    except Exception as e:
        print(f"  ! network error: {e}")
        return None
    if r.status_code != 200:
        print(f"  ! API {r.status_code}: {r.text[:200]}")
        return None
    data = r.json()
    # Extract image bytes from inlineData
    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError):
        print(f"  ! no candidates in response")
        return None
    for part in parts:
        if "inlineData" in part:
            b64 = part["inlineData"].get("data", "")
            try:
                return base64.b64decode(b64)
            except Exception as e:
                print(f"  ! base64 decode error: {e}")
                return None
    print(f"  ! no inlineData in any part")
    return None


def save_jpeg(image_bytes: bytes, dest: Path) -> bool:
    try:
        from PIL import Image
    except ImportError:
        # Fall back to raw write if Pillow not available; image may not be JPEG
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(image_bytes)
        return True
    # Convert/recompress to ensure JPEG output
    try:
        im = Image.open(io.BytesIO(image_bytes))
        if im.mode != "RGB":
            im = im.convert("RGB")
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, "JPEG", quality=82, optimize=True)
        return True
    except Exception as e:
        print(f"  ! PIL save failed: {e}")
        return False


def mark_generated(section_path: Path, filename: str) -> bool:
    """Re-read section HTML and flip data-imagegen-status for the matching src."""
    text = section_path.read_text(encoding="utf-8")
    # Find img with this src
    target = filename.split("/")[-1]
    needle_prefix = f'src="images/{target}"'
    pos = text.find(needle_prefix)
    if pos < 0:
        return False
    # Find data-imagegen-status="pending" within the same <img> tag
    tag_start = text.rfind("<img", 0, pos)
    tag_end = text.find("/>", pos)
    if tag_start < 0 or tag_end < 0:
        return False
    tag = text[tag_start:tag_end + 2]
    new_tag = tag.replace(
        'data-imagegen-status="pending"',
        'data-imagegen-status="generated"',
    )
    if new_tag == tag:
        return False
    section_path.write_text(text[:tag_start] + new_tag + text[tag_end + 2:],
                            encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None,
                    help="Process at most N pending records")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print prompts; don't call the API")
    ap.add_argument("--resume", action="store_true",
                    help="Skip records whose JPEG already exists on disk")
    ap.add_argument("--sleep", type=float, default=1.2,
                    help="Seconds between API calls (rate limit)")
    args = ap.parse_args()

    if not MANIFEST.exists():
        print(f"ERROR: manifest not found at {MANIFEST}", file=sys.stderr)
        sys.exit(1)

    records = []
    with MANIFEST.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    # Filter HIGH only (MED are fun-note callouts, no image needed)
    records = [r for r in records if r.get("tier", "HIGH") == "HIGH"]
    print(f"Total HIGH records: {len(records)}")

    api_key = None
    if not args.dry_run:
        api_key = get_api_key()
        if not api_key:
            print("ERROR: set GOOGLE_API_KEY or GEMINI_API_KEY", file=sys.stderr)
            sys.exit(2)

    n_done = 0
    n_skipped = 0
    n_failed = 0
    with RUN_LOG.open("a", encoding="utf-8") as logf:
        for rec in records:
            if args.limit is not None and n_done >= args.limit:
                break
            section_path = ROOT / rec["section"]
            target_filename = rec["filename"]
            target_path = section_path.parent / target_filename
            if args.resume and target_path.exists():
                n_skipped += 1
                continue
            prompt = rec["prompt"]
            print(f"\n[{rec['figure_label']}] {section_path.relative_to(ROOT)}")
            print(f"  -> {target_path.relative_to(ROOT)}")
            if args.dry_run:
                print(f"  PROMPT: {prompt[:140]}...")
                continue
            img_bytes = call_gemini(prompt, api_key)
            if not img_bytes:
                n_failed += 1
                logf.write(f"FAIL {section_path} {target_filename}\n")
                continue
            if not save_jpeg(img_bytes, target_path):
                n_failed += 1
                logf.write(f"FAIL-SAVE {section_path} {target_filename}\n")
                continue
            if not mark_generated(section_path, target_filename):
                print("  ! could not flip data-imagegen-status (still generated; manually fix)")
            n_done += 1
            logf.write(f"OK   {section_path} {target_filename}\n")
            print(f"  OK")
            time.sleep(args.sleep)
    print(f"\nDone: {n_done} generated, {n_skipped} skipped (already exist), {n_failed} failed")


if __name__ == "__main__":
    main()
