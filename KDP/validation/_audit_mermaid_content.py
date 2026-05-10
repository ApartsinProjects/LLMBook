"""Gather Mermaid figure context for content audit.

Walks every *.mmd, finds the matching <img> in section-N.M.html, captures:
- mmd source
- figure caption
- preceding paragraph text
- chapter / section title
"""
import json
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")

mmd_files = sorted(ROOT.rglob("*.mmd"))
print(f"Found {len(mmd_files)} .mmd files")

records = []

def find_html_for_image(mmd_path: Path):
    """Given a path to /images/foo.mmd, find sibling section-*.html files
    that reference foo.png in an <img>."""
    images_dir = mmd_path.parent
    module_dir = images_dir.parent
    png_name = mmd_path.stem + ".png"
    candidates = sorted(module_dir.glob("section-*.html"))
    candidates += sorted(module_dir.glob("index.html"))
    # also markdown sources
    md_root = ROOT / "md"
    candidates += sorted(md_root.rglob(f"*{module_dir.name}*.md"))
    for html in candidates:
        try:
            txt = html.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if png_name in txt:
            return html, txt
    return None, None


def extract_context(html_text: str, png_name: str):
    # Find img tag line
    idx = html_text.find(png_name)
    if idx < 0:
        return {}
    # find caption div near img (search forward up to ~600 chars)
    after = html_text[idx: idx + 1200]
    cap_m = re.search(r'<div class="diagram-caption">(.*?)</div>', after, re.S)
    caption = ""
    if cap_m:
        caption = re.sub(r"<[^>]+>", " ", cap_m.group(1))
        caption = re.sub(r"\s+", " ", caption).strip()
    # find alt text
    img_window = html_text[max(0, idx - 200): idx + 500]
    alt_m = re.search(r'alt="([^"]+)"', img_window)
    alt = alt_m.group(1) if alt_m else ""
    # find paragraph before figure (within 1500 chars before idx)
    before = html_text[max(0, idx - 2000): idx]
    paras = re.findall(r"<p[^>]*>(.*?)</p>", before, re.S)
    prev_para = ""
    if paras:
        prev_para = re.sub(r"<[^>]+>", " ", paras[-1])
        prev_para = re.sub(r"\s+", " ", prev_para).strip()
    # find h1/h2/h3 chapter and section titles
    title_h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html_text, re.S)
    title = ""
    if title_h1:
        title = re.sub(r"<[^>]+>", " ", title_h1.group(1))
        title = re.sub(r"\s+", " ", title).strip()
    # nearest h2/h3 before idx
    headings = list(re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", html_text, re.S))
    nearest = ""
    for m in headings:
        if m.start() > idx:
            break
        nearest = re.sub(r"<[^>]+>", " ", m.group(1))
        nearest = re.sub(r"\s+", " ", nearest).strip()
    return {
        "alt": alt,
        "caption": caption,
        "prev_paragraph": prev_para[:600],
        "page_title": title,
        "nearest_heading": nearest,
    }


for mmd in mmd_files:
    rel = mmd.relative_to(ROOT).as_posix()
    src = mmd.read_text(encoding="utf-8", errors="ignore")
    html_path, html_txt = find_html_for_image(mmd)
    ctx = {}
    html_rel = ""
    if html_txt:
        ctx = extract_context(html_txt, mmd.stem + ".png")
        html_rel = html_path.relative_to(ROOT).as_posix()
    records.append({
        "mmd": rel,
        "html": html_rel,
        "mmd_src": src,
        **ctx,
    })

out = ROOT / "KDP" / "validation" / "_raw" / "mermaid_content_audit_data.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(records, indent=1), encoding="utf-8")
print(f"Wrote {out} ({len(records)} records)")
missing = [r for r in records if not r.get("html")]
print(f"{len(missing)} records lacked HTML context")
for r in missing[:10]:
    print(" -", r["mmd"])
