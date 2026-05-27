"""
Scan the Drive MCP tool-results directory, identify .pptx blob files,
read each blob's {id, title} envelope, and build a batch-extract manifest
for a given set of target file_ids -> output_relpath mappings.
"""
import json
import sys
from pathlib import Path

TOOL_RESULTS_DIR = Path(r"C:/Users/apart/.claude/projects/E--Projects-BookBlogsHome-LLMBook/5cc13830-8e0b-4bac-a65e-22dd500870fc/tool-results")

def main():
    if len(sys.argv) != 3:
        print("Usage: python _build_manifest.py <targets.json> <output_manifest.json>")
        print("  targets.json: {<file_id>: {deck_stem, folder_path}}")
        return 2
    targets = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out_path = Path(sys.argv[2])

    # Scan all download blobs, sort newest first so older blobs get overwritten by the freshest one
    blobs = sorted(TOOL_RESULTS_DIR.glob("mcp-d404a4b3-*-download_file_content-*.txt"),
                   key=lambda p: p.stat().st_mtime, reverse=True)

    id_to_blob = {}
    for blob in blobs:
        try:
            envelope = json.loads(blob.read_text(encoding="utf-8"))
            fid = envelope.get("id")
            if fid and fid in targets and fid not in id_to_blob:
                id_to_blob[fid] = str(blob).replace("\\", "/")
        except Exception:
            continue

    manifest = []
    for fid, target in targets.items():
        if fid in id_to_blob:
            manifest.append({
                "deck_stem": target["deck_stem"],
                "folder_path": target["folder_path"],
                "blob_path": id_to_blob[fid],
            })
        else:
            print(f"WARNING: no blob for file_id={fid} ({target.get('deck_stem')})", file=sys.stderr)

    out_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: {len(manifest)}/{len(targets)} entries -> {out_path}")

if __name__ == "__main__":
    sys.exit(main())
