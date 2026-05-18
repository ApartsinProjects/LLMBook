"""Wave 83: Add canonical whats-next + chapter-nav to all 16 part-index files.

The PART_INDEX_LAYOUT plugin requires:
- <div class="whats-next">  pointing to first chapter of this part
- <nav class="chapter-nav"> with prev-part / up-to-TOC / next-part

All 16 part-index files are currently missing both. This wave generates them
mechanically using the part's own structure (first module, prev/next part on
disk).

Insertion point: just before the existing <footer>...</footer> inside <main>.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX",
         "X", "XI", "XII", "XIII", "XIV", "XV", "XVI"]


def discover_parts():
    """Return list of dicts ordered by part number."""
    parts = []
    for d in sorted(ROOT.iterdir()):
        if not (d.is_dir() and d.name.startswith("part-")):
            continue
        m = re.match(r"part-(\d+)-(.+)", d.name)
        if not m:
            continue
        num = int(m.group(1))
        # h1 may span lines and contain attrs; use a relaxed pattern
        idx_path = d / "index.html"
        if not idx_path.exists():
            continue
        html = idx_path.read_text(encoding="utf-8")
        title_m = re.search(
            r'<h1[^>]*class="part-title"[^>]*>(.*?)</h1>',
            html, re.IGNORECASE | re.DOTALL,
        )
        if not title_m:
            # Fall back to bare <h1>
            title_m = re.search(
                r'<h1[^>]*>(.*?)</h1>',
                html, re.IGNORECASE | re.DOTALL,
            )
        if title_m:
            inner = re.sub(r'<[^>]+>', '', title_m.group(1))
            title = re.sub(r"\s+", " ", inner).strip()
        else:
            title = f"Part {ROMAN[num]}"
        # First module dir
        mods = sorted(
            x.name for x in d.iterdir()
            if x.is_dir() and x.name.startswith("module-")
        )
        if not mods:
            continue
        first_mod = mods[0]
        # Get first chapter's index title from <h1>
        first_chap_idx = d / first_mod / "index.html"
        chap_title = first_mod
        chap_num = None
        if first_chap_idx.exists():
            chap_html = first_chap_idx.read_text(encoding="utf-8")
            # h1 with chapter-title class first
            ct_m = re.search(
                r'<h1[^>]*class="chapter-title"[^>]*>(.*?)</h1>',
                chap_html, re.IGNORECASE | re.DOTALL,
            )
            if not ct_m:
                # Fall back to bare <h1>...</h1>
                ct_m = re.search(
                    r'<h1[^>]*>(.*?)</h1>',
                    chap_html, re.IGNORECASE | re.DOTALL,
                )
            if ct_m:
                # Strip any inner tags (some chapters have <span class="ch-num">...)
                inner = re.sub(r'<[^>]+>', '', ct_m.group(1))
                chap_title = re.sub(r"\s+", " ", inner).strip()
            # Chapter number
            cn_m = re.search(r'class="mod-num">Chapter\s+(\d+)</span>', chap_html)
            if cn_m:
                chap_num = int(cn_m.group(1))
            else:
                pl_m = re.search(r'class="part-label">Chapter\s+(\d+)', chap_html)
                if pl_m:
                    chap_num = int(pl_m.group(1))
                else:
                    mm = re.match(r"module-(\d+)-", first_mod)
                    if mm:
                        chap_num = int(mm.group(1))
        parts.append({
            "num": num,
            "dir": d.name,
            "title": title,
            "first_mod": first_mod,
            "chap_title": chap_title,
            "chap_num": chap_num,
        })
    parts.sort(key=lambda x: x["num"])
    return parts


def build_whats_next(part):
    """Whats-next callout pointing to first chapter of this part."""
    chap_num = part["chap_num"] if part["chap_num"] is not None else "?"
    chap_title = part["chap_title"]
    href = f"{part['first_mod']}/index.html"
    return (
        '<div class="whats-next">\n'
        f'<h3 id="what-s-next">What\'s Next?</h3>\n'
        f'<p>This part begins with <a href="{href}">Chapter {chap_num}: '
        f'{chap_title}</a>. Each chapter builds on the previous one, so we '
        f'recommend reading {part["title"].split(":")[0].strip()} in order.</p>\n'
        '</div>'
    )


def build_chapter_nav(part, prev_part, next_part):
    """Part-level chapter-nav with prev-part / up-to-TOC / next-part."""
    parts_str = ['<nav class="chapter-nav">']
    # Prev part
    if prev_part:
        parts_str.append(
            f'<a class="prev" href="../{prev_part["dir"]}/index.html">'
            f'<span class="nav-label">Previous</span>'
            f'<span class="nav-num">Part {ROMAN[prev_part["num"]]}</span>'
            f'<span class="nav-title">'
            f'{prev_part["title"].split(":", 1)[-1].strip() if ":" in prev_part["title"] else prev_part["title"]}'
            f'</span></a>'
        )
    # Up to TOC
    parts_str.append(
        '<a class="up" href="../toc.html">'
        '<span class="nav-label">Contents</span>'
        '<span class="nav-num">Book</span>'
        '<span class="nav-title">Table of Contents</span></a>'
    )
    # Next part
    if next_part:
        parts_str.append(
            f'<a class="next" href="../{next_part["dir"]}/index.html">'
            f'<span class="nav-label">Next</span>'
            f'<span class="nav-num">Part {ROMAN[next_part["num"]]}</span>'
            f'<span class="nav-title">'
            f'{next_part["title"].split(":", 1)[-1].strip() if ":" in next_part["title"] else next_part["title"]}'
            f'</span></a>'
        )
    parts_str.append('</nav>')
    return "\n".join(parts_str)


FOOTER_RE = re.compile(
    r'(\s*)<footer\b', re.IGNORECASE,
)


def fix_part(part, prev_part, next_part) -> bool:
    idx = ROOT / part["dir"] / "index.html"
    html = idx.read_text(encoding="utf-8")
    # Skip if already has whats-next or chapter-nav (shouldn't happen but safe)
    has_wn = 'class="whats-next"' in html
    has_nav = '<nav class="chapter-nav"' in html
    if has_wn and has_nav:
        return False

    wn = build_whats_next(part)
    nav = build_chapter_nav(part, prev_part, next_part)

    block_parts = []
    if not has_wn:
        block_parts.append(wn)
    if not has_nav:
        block_parts.append(nav)
    insert_block = "\n".join(block_parts) + "\n"

    # Insert before the <footer>
    m = FOOTER_RE.search(html)
    if not m:
        print(f"  ! {part['dir']}: no footer found, skipping")
        return False
    insert_at = m.start()
    new_html = html[:insert_at] + "\n" + insert_block + html[insert_at:]
    idx.write_text(new_html, encoding="utf-8")
    return True


def main():
    parts = discover_parts()
    print(f"Discovered {len(parts)} parts")
    n_fixed = 0
    for i, p in enumerate(parts):
        prev_p = parts[i - 1] if i > 0 else None
        next_p = parts[i + 1] if i + 1 < len(parts) else None
        if fix_part(p, prev_p, next_p):
            n_fixed += 1
            print(f"  + {p['dir']}: added whats-next + chapter-nav")
    print(f"\nTotal parts updated: {n_fixed}")


if __name__ == "__main__":
    main()
