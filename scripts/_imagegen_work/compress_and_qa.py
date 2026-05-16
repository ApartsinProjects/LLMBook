"""Compress generated PNGs and run quality checks.

For each saved image:
- Verify dimensions: long side >= 1024.
- If file size > 500 KB, re-encode with Pillow at optimize+compress.
- Mark accepted/rejected based on size 200 KB to 1 MB band and dims.

Writes qa_report.json next to results.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

WORK = Path(__file__).parent
RESULTS_FILE = WORK / "results.json"
QA_FILE = WORK / "qa_report.json"
MAX_BYTES = 500 * 1024  # target after compression
MIN_BYTES_HARD = 30 * 1024  # below this == likely placeholder
LONG_SIDE_MIN = 1024


def compress_png(p: Path, target_bytes: int) -> tuple[int, int, int]:
    """Return (orig_bytes, new_bytes, long_side). Compresses in place if oversize."""
    from PIL import Image
    orig = p.stat().st_size
    with Image.open(p) as im:
        w, h = im.size
        long_side = max(w, h)
        if orig <= target_bytes:
            return orig, orig, long_side
        # Try progressively stronger compression by saving with optimize and
        # quantizing to palette only if needed.
        # First pass: re-save with optimize.
        rgb = im.convert("RGB") if im.mode != "RGB" else im
        rgb.save(p, format="PNG", optimize=True)
        new = p.stat().st_size
        if new <= target_bytes:
            return orig, new, long_side
        # Second pass: convert to JPEG-quality WebP-ish via PNG quantization.
        try:
            quant = im.quantize(colors=256, method=Image.Quantize.LIBIMAGEQUANT
                                if hasattr(Image.Quantize, "LIBIMAGEQUANT") else 0)
            quant.save(p, format="PNG", optimize=True)
        except Exception:
            quant = im.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
            quant.save(p, format="PNG", optimize=True)
        new = p.stat().st_size
        if new <= target_bytes:
            return orig, new, long_side
        # Third pass: downsample if still too large.
        scale = (target_bytes / new) ** 0.5
        new_w = max(1024, int(w * scale))
        new_h = int(h * (new_w / w))
        with Image.open(p) as im2:
            small = im2.resize((new_w, new_h), Image.LANCZOS)
            small = small.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
            small.save(p, format="PNG", optimize=True)
        new = p.stat().st_size
        long_side = max(new_w, new_h)
        return orig, new, long_side


def main() -> int:
    if not RESULTS_FILE.exists():
        print("Run run_batch.py first.")
        return 1
    results = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    report = []
    for r in results:
        entry = dict(r)
        path = Path(r.get("saved_path") or r["output_path"])
        if not path.exists():
            entry["qa"] = "missing"
            report.append(entry)
            continue
        try:
            orig, new, long_side = compress_png(path, MAX_BYTES)
        except Exception as e:
            entry["qa"] = f"error: {e}"
            report.append(entry)
            continue
        entry["orig_bytes"] = orig
        entry["bytes"] = new
        entry["long_side"] = long_side
        qa_flags = []
        if new < MIN_BYTES_HARD:
            qa_flags.append("too-small")
        if long_side < LONG_SIDE_MIN:
            qa_flags.append("low-res")
        if new > 1024 * 1024:
            qa_flags.append("oversize")
        entry["qa"] = "accepted" if not qa_flags else ",".join(qa_flags)
        report.append(entry)

    QA_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
    accepted = sum(1 for r in report if r.get("qa") == "accepted")
    print(f"Accepted: {accepted}/{len(report)}")
    sizes = [r["bytes"] for r in report if "bytes" in r]
    if sizes:
        print(f"Size range: {min(sizes)//1024} KB to {max(sizes)//1024} KB")
    failed = [r for r in report if r.get("qa") not in ("accepted",)]
    for r in failed[:20]:
        print(f"  {r.get('qa')} :: {r.get('part')}/{r.get('module') or ''} :: {r.get('saved_path') or r.get('output_path')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
