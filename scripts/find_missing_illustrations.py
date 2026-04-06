import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")
missing = []
for f in sorted(BOOK_ROOT.rglob("section-*.html")):
    s = str(f).replace("\\", "/")
    if any(x in s for x in ["_archive", "agents", "appendices", "front-matter"]):
        continue
    text = f.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in text:
        continue
    if '<figure class="illustration">' not in text:
        m = re.search(r"<h1>(.*?)</h1>", text)
        title = m.group(1) if m else "Unknown"
        rel = str(f.relative_to(BOOK_ROOT)).replace("\\", "/")
        missing.append((rel, title))

for fp, title in missing:
    print(f"{fp}: {title}")
print(f"Total: {len(missing)}")
