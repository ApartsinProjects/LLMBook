"""Insert an Exercises block into a section HTML file.

The block is inserted at the first match of one of these markers, in priority order:
  1. Right before <div class="callout research-frontier">
  2. Right before <div class="whats-next">
  3. Right before <details class="bibliography-collapsible"
  4. Right before <nav class="chapter-nav"

Exercises payload is read from a separate file (HTML snippet) and wrapped with
<h2>Exercises</h2> if not already present.

Usage:
  python insert_exercises.py <target_html> <payload_html>
"""
import sys
from pathlib import Path


def insert_exercises(target_path: str, payload_path: str) -> bool:
    target = Path(target_path)
    payload = Path(payload_path).read_text(encoding="utf-8").strip()
    text = target.read_text(encoding="utf-8")

    if "callout exercise" in text:
        print(f"SKIP (already has exercises): {target_path}")
        return False

    block = "<h2>Exercises</h2>\n" + payload + "\n"

    markers = [
        '<div class="callout research-frontier">',
        '<div class="whats-next">',
        '<details class="bibliography-collapsible"',
        '<nav class="chapter-nav">',
    ]
    for marker in markers:
        idx = text.find(marker)
        if idx != -1:
            new_text = text[:idx] + block + text[idx:]
            target.write_text(new_text, encoding="utf-8")
            print(f"OK  ({marker[:30]}): {target_path}")
            return True
    print(f"FAIL (no insertion marker found): {target_path}")
    return False


if __name__ == "__main__":
    insert_exercises(sys.argv[1], sys.argv[2])
