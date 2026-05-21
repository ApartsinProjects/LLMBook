"""Build wave60_imagen_tasks.json (script-compatible) from wave60_comic_round4.json.

Adds the `output` path (per section's images/ directory) and the `aspect_ratio`
("16:9") fields that the modified generate_icons_gemini.py understands.
"""
import json
from pathlib import Path

ROOT = Path(r"E:\Projects\BookBlogsHome\LLMBook")
SCRIPTS = ROOT / "scripts"
SRC = SCRIPTS / "wave60_comic_round4.json"
DST = SCRIPTS / "wave60_imagen_tasks.json"

data = json.loads(SRC.read_text(encoding="utf-8"))
tasks = []
for entry in data:
    name = entry["name"]
    section_path = entry["section_path"]
    section_dir = (ROOT / section_path).parent
    images_dir = section_dir / "images"
    # Strip the "chXY-N-" prefix to derive a clean image filename
    # e.g. "ch16-3-catastrophic-forgetting-lr" -> "comic-catastrophic-forgetting-lr.png"
    parts = name.split("-")
    # find first non-chapter token (the chapter chunk is like "ch16", "3")
    if parts[0].startswith("ch") and len(parts) >= 3:
        slug = "-".join(parts[2:])
    else:
        slug = "-".join(parts)
    image_name = f"comic-{slug}.png"
    output = str(images_dir / image_name)
    tasks.append({
        "name": name,
        "prompt": entry["prompt"],
        "output": output,
        "aspect_ratio": "16:9",
        "image_filename": image_name,  # for the wire script
    })

DST.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
print(f"Wrote {len(tasks)} tasks to {DST}")
for t in tasks:
    print(f"  {t['name']:38s} -> {t['output']}")
