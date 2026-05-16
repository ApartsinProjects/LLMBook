"""Rewire stale cross-part links in chapter-index files only."""
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

REPLACEMENTS = [
    # part-11 industries linked to old Ch27. Re-point to Ch58.2 (Education/Legal/Creative).
    (
        r'<li><a href="\.\./\.\./part-7-multimodal-generation/module-27-llm-applications/section-27\.6\.html">Section 27\.6 \(Education, Legal &amp; Creative Industries\)</a>, broader industry survey\.</li>',
        '<li><a href="../module-58-creative-industries/section-58.2.html">Section 58.2 (Education, Legal &amp; Creative Industries)</a>, broader industry survey.</li>',
    ),
    # 31-strategy-product-roi (dissolved) -> current Part 10 strategy module
    (
        r'\.\./module-31-strategy-product-roi/',
        '../../part-10-idea-to-product/module-42-strategy-prioritization/',
    ),
    # module-25-agent-safety-production (dissolved) -> current Ch 38 in Part 9
    (
        r'\.\./module-25-agent-safety-production/',
        '../../part-9-safety-security-ethics/module-38-agent-safety-security/',
    ),
]

# Only touch chapter index files (index.html), only in part-* directories, NOT in section files.
target_files = []
for part_dir in ROOT.glob("part-*-*/"):
    for module_dir in part_dir.glob("module-*/"):
        idx = module_dir / "index.html"
        if idx.exists():
            target_files.append(idx)

count = 0
for f in target_files:
    text = f.read_text(encoding="utf-8")
    new_text = text
    for pattern, replacement in REPLACEMENTS:
        new_text = re.sub(pattern, replacement, new_text)
    if new_text != text:
        f.write_text(new_text, encoding="utf-8")
        rel = f.relative_to(ROOT)
        print(f"  {rel}: rewrote dead links")
        count += 1

print(f"\nTotal chapter indexes touched: {count}")
