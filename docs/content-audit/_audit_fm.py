"""Audit front-matter HTML hrefs. Check each href resolves to an existing file
and report any references to chapters/sections that don't exist."""
import re
from pathlib import Path
import json

ROOT = Path(r"E:\Projects\BookBlogsHome\LLMBook")
FM_DIR = ROOT / "front-matter"
GT = ROOT / "docs" / "content-audit" / "_book_structure.json"


def main():
    issues = []
    files = sorted(FM_DIR.glob("*.html"))
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        # Find all href values
        hrefs = re.findall(r'href="([^"]+)"', text)
        for h in hrefs:
            if h.startswith(("#", "http://", "https://", "mailto:")):
                continue
            # Resolve relative to this file's location
            target = (f.parent / h).resolve()
            # Strip anchors
            target_path = Path(str(target).split("#", 1)[0])
            if not target_path.exists():
                issues.append({"file": f.name, "href": h, "kind": "broken_href"})
    print(f"Found {len(issues)} broken hrefs in FM files.")
    for i in issues:
        print(json.dumps(i, ensure_ascii=False))


if __name__ == "__main__":
    main()
