#!/usr/bin/env python
"""Extract all whats-next blocks and count sentences."""
import re
import sys
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
SKIP_DIRS = {"node_modules", ".git", "KDP", "build", "temp_ebook", "temp_epub",
             "source_fix_backups", "pagefind", "templates", ".claude"}

def should_skip(p: Path) -> bool:
    parts = set(p.parts)
    return bool(parts & SKIP_DIRS)

# Match the whats-next block (covers both h2 "What Comes Next" and h3 "What's Next?" variants)
BLOCK_RE = re.compile(
    r'<div class="whats-next">\s*<h([23])>(What Comes Next|What&#x27;s Next\?|What\'s Next\?)</h\1>\s*(.*?)\s*</div>',
    re.DOTALL
)

def strip_tags(html: str) -> str:
    """Strip HTML tags for sentence counting."""
    t = re.sub(r'<[^>]+>', ' ', html)
    return re.sub(r'\s+', ' ', t).strip()

def count_sentences(text: str) -> int:
    """Count sentences (end with .!?)."""
    if not text:
        return 0
    # Split on .!? followed by space or end
    parts = re.split(r'[.!?]+(?:\s|$)', text)
    return sum(1 for p in parts if p.strip())

results = []
with open(r"E:/Projects/BookBlogsHome/LLMBook/whats_next_index.txt") as f:
    files = [Path(line.strip()) for line in f if line.strip()]

for fp in files:
    if should_skip(fp):
        continue
    try:
        html = fp.read_text(encoding='utf-8')
    except Exception as e:
        print(f"ERROR {fp}: {e}", file=sys.stderr)
        continue
    m = BLOCK_RE.search(html)
    if not m:
        continue
    body = m.group(3)
    text = strip_tags(body)
    n_sent = count_sentences(text)
    results.append((fp, n_sent, len(text)))

# Sort by sentence count desc to compress longest first
results.sort(key=lambda x: -x[1])
for fp, n, l in results:
    print(f"{n}\t{l}\t{fp.relative_to(ROOT)}")
