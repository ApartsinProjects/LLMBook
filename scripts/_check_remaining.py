import time, re
from pathlib import Path

ROOT = Path("E:/Projects/BookBlogsHome/LLMBook")
NOW = time.time()


def in_scope(path):
    rel = str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    if rel.startswith("front-matter/"):
        return True
    if rel.startswith("part-7-multimodal-generation/module-31-") or rel.startswith("part-7-multimodal-generation/module-32-"):
        return True
    if rel.startswith("part-10-idea-to-product/"):
        return True
    if rel.startswith("part-11-applications-across-industries/"):
        return True
    if rel.startswith("part-12-frontiers/module-63-") or rel.startswith("part-12-frontiers/module-64-") or rel.startswith("part-12-frontiers/module-65-"):
        return True
    if rel.startswith("appendices/appendix-n-") or rel.startswith("appendices/appendix-o-"):
        return True
    if "tools-of-the-trade" in rel:
        return True
    return False


remaining = {"hf": [], "so": [], "ow": []}
for p in ROOT.rglob("*.html"):
    if in_scope(p):
        continue
    if NOW - p.stat().st_mtime < 60:
        continue
    t = p.read_text(encoding="utf-8")
    if re.search(r'href="[^"]*module-13-llm-apis/section-13\.2\.html[^"]*"[^>]*>(Hugging\s*Face|HuggingFace)', t, re.IGNORECASE):
        remaining["hf"].append(str(p.relative_to(ROOT)))
    if re.search(r'href="[^"]*module-13-llm-apis/section-13\.3\.html[^"]*"[^>]*>((?:S|s)tructured\s+outputs?)', t):
        remaining["so"].append(str(p.relative_to(ROOT)))
    if re.search(r'href="[^"]*module-08-modern-llm-landscape/section-8\.1\.html[^"]*"[^>]*>([Oo]pen-weight)', t):
        remaining["ow"].append(str(p.relative_to(ROOT)))

print("Remaining HF (eligible, not yet fixed):", len(remaining["hf"]))
for f in remaining["hf"][:10]:
    print("  ", f)
print("Remaining SO:", len(remaining["so"]))
for f in remaining["so"][:10]:
    print("  ", f)
print("Remaining OW:", len(remaining["ow"]))
for f in remaining["ow"][:10]:
    print("  ", f)
