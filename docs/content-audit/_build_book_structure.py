"""Build ground truth book structure from part-*/module-*/index.html files.

Extracts (part_num, part_title, chapter_num, chapter_title) plus all
section files in each module.
"""
import json
import os
import re
from pathlib import Path

ROOT = Path(r"E:\Projects\BookBlogsHome\LLMBook")
OUT = ROOT / "docs" / "content-audit" / "_book_structure.json"


def extract_h1(html_path: Path) -> str:
    """Extract the first <h1> text from an HTML file."""
    if not html_path.exists():
        return ""
    text = html_path.read_text(encoding="utf-8", errors="replace")
    # Find first <h1>...</h1>; strip tags inside
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    inner = m.group(1)
    # Remove tags
    inner = re.sub(r"<[^>]+>", "", inner)
    inner = re.sub(r"\s+", " ", inner).strip()
    return inner


def extract_section_title(html_path: Path) -> str:
    """Extract main heading from a section-X.Y.html.

    Section files typically have an h1 like "Section 1.2: Token Embeddings" or
    similar.  Returns the cleaned heading text.
    """
    if not html_path.exists():
        return ""
    text = html_path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL | re.IGNORECASE)
    if not m:
        # Try h2 if h1 not present
        m = re.search(r"<h2[^>]*>(.*?)</h2>", text, re.DOTALL | re.IGNORECASE)
        if not m:
            return ""
    inner = m.group(1)
    inner = re.sub(r"<[^>]+>", "", inner)
    inner = re.sub(r"\s+", " ", inner).strip()
    return inner


def main():
    parts = []
    part_dirs = sorted(
        [d for d in ROOT.iterdir() if d.is_dir() and d.name.startswith("part-")],
        key=lambda d: int(re.match(r"part-(\d+)", d.name).group(1)),
    )

    for pd in part_dirs:
        m = re.match(r"part-(\d+)-(.+)", pd.name)
        if not m:
            continue
        part_num = int(m.group(1))
        part_slug = m.group(2)
        # Try to extract part title from a part index if available
        part_index_candidates = [pd / "index.html", pd / "part-index.html"]
        part_title = ""
        for cand in part_index_candidates:
            if cand.exists():
                part_title = extract_h1(cand)
                if part_title:
                    break
        # Fallback: derive from slug
        if not part_title:
            part_title = part_slug.replace("-", " ").title()

        modules = []
        mod_dirs = sorted(
            [d for d in pd.iterdir() if d.is_dir() and d.name.startswith("module-")],
            key=lambda d: (
                # Sort by numeric chapter; allow suffix like 54b
                int(re.match(r"module-(\d+)", d.name).group(1)),
                d.name,
            ),
        )
        for md in mod_dirs:
            mm = re.match(r"module-(\d+)([a-z]?)-(.+)", md.name)
            if not mm:
                continue
            chap_num_str = mm.group(1) + mm.group(2)
            chap_num = int(mm.group(1))
            chap_slug = mm.group(3)
            idx = md / "index.html"
            chap_title = extract_h1(idx) if idx.exists() else ""
            # Section files
            sections = []
            for f in sorted(md.iterdir()):
                if f.is_file() and f.name.startswith("section-") and f.suffix == ".html":
                    sec_match = re.match(r"section-(\d+)\.(\d+[a-z]?)\.html", f.name)
                    if sec_match:
                        sec_num = sec_match.group(2)
                        sec_title = extract_section_title(f)
                        sections.append(
                            {
                                "file": f.name,
                                "section": sec_match.group(0).replace("section-", "").replace(".html", ""),
                                "section_num": sec_num,
                                "title": sec_title,
                                "rel_path": str(f.relative_to(ROOT)).replace("\\", "/"),
                            }
                        )
            modules.append(
                {
                    "chap_num": chap_num,
                    "chap_num_str": chap_num_str,
                    "module_dir": md.name,
                    "module_slug": chap_slug,
                    "title": chap_title,
                    "rel_path": str(idx.relative_to(ROOT)).replace("\\", "/") if idx.exists() else "",
                    "sections": sections,
                }
            )
        parts.append(
            {
                "part_num": part_num,
                "part_dir": pd.name,
                "title": part_title,
                "modules": modules,
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump({"parts": parts}, f, indent=2, ensure_ascii=False)
    # Also print summary
    total_modules = sum(len(p["modules"]) for p in parts)
    total_sections = sum(
        len(mod["sections"]) for p in parts for mod in p["modules"]
    )
    print(
        f"Wrote {OUT} - {len(parts)} parts, {total_modules} chapters, {total_sections} sections."
    )


if __name__ == "__main__":
    main()
