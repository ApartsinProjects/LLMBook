"""Dump compact text for each figure for human review."""
import json
from pathlib import Path
ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
data = json.loads((ROOT/"KDP/validation/_raw/mermaid_content_audit_data.json").read_text(encoding="utf-8"))
out_lines = []
for r in data:
    out_lines.append("=" * 80)
    out_lines.append(f"FILE: {r['mmd']}")
    out_lines.append(f"HTML: {r.get('html','(none)')}")
    out_lines.append(f"PAGE: {r.get('page_title','')}")
    out_lines.append(f"SECTION: {r.get('nearest_heading','')}")
    out_lines.append(f"CAPTION: {r.get('caption','')}")
    pp = r.get("prev_paragraph","")[:300]
    out_lines.append(f"PREV: {pp}")
    out_lines.append("--- mmd ---")
    src = r["mmd_src"]
    # Strip style lines
    keep = []
    for ln in src.split("\n"):
        s = ln.strip()
        if s.startswith("style ") or s.startswith("classDef ") or s.startswith("class "):
            continue
        keep.append(ln)
    out_lines.append("\n".join(keep).rstrip())
out_path = ROOT / "KDP/validation/_raw/mermaid_dump.txt"
out_path.write_text("\n".join(out_lines), encoding="utf-8")
print("Wrote", out_path, "lines:", len(out_lines))
