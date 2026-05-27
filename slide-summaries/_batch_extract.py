"""
Batch driver: extract many Drive-downloaded .pptx blobs in sequence.
Reads a manifest JSON listing {blob_path, deck_stem, folder_path} entries,
runs the PPTSummary extractor for each, and writes a results summary.
"""
import json
import subprocess
import sys
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent  # slide-summaries/
EXTRACTOR = Path.home() / ".claude" / "skills" / "PPTSummary" / "scripts" / "extract_pptx.py"

def main(manifest_path: str) -> int:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    results = []
    for entry in manifest:
        deck_stem = entry["deck_stem"]
        folder = entry["folder_path"]
        blob = entry["blob_path"]
        work_dir = ROOT / "_downloads" / folder / deck_stem
        struct_json = work_dir / "struct.json"
        if struct_json.exists() and entry.get("skip_if_exists", True):
            results.append({"deck_stem": deck_stem, "status": "skipped_exists",
                            "struct_path": str(struct_json)})
            print(f"SKIP: {deck_stem} (already extracted)")
            continue
        t0 = time.time()
        cmd = ["C:/Python314/python", str(EXTRACTOR),
               "--from-drive-blob", blob,
               str(work_dir),
               str(struct_json)]
        print(f"RUN: {deck_stem}")
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            elapsed = time.time() - t0
            ok = out.returncode == 0
            slide_count = None
            if ok and struct_json.exists():
                slide_count = json.loads(struct_json.read_text(encoding="utf-8")).get("slide_count")
            results.append({
                "deck_stem": deck_stem,
                "folder_path": folder,
                "status": "ok" if ok else "fail",
                "slide_count": slide_count,
                "elapsed_sec": round(elapsed, 1),
                "struct_path": str(struct_json),
                "stdout_tail": out.stdout.strip().splitlines()[-1] if out.stdout else "",
                "stderr_tail": out.stderr.strip().splitlines()[-1] if out.stderr else "",
            })
            print(f"  -> {results[-1]['status']} slides={slide_count} elapsed={elapsed:.1f}s")
        except subprocess.TimeoutExpired:
            results.append({"deck_stem": deck_stem, "status": "timeout"})
            print(f"  -> TIMEOUT")

    out_path = ROOT / "_batch_results.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote results -> {out_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
