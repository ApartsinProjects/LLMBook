"""Rebuild every chapter index's section card list to canonical 3-span format.

Canonical card (verified from module-48-shipping-deploying/index.html):

  <a class="section-card" href="section-N.M.html">
  <span class="section-num">N.M</span>
  <span class="section-title">Section Title</span>
  <span class="section-desc">One-to-two sentence description.</span>
  </a>

Tasks:
  1. List actual section-NN.M.html files in each chapter directory.
  2. Parse the index's section cards (regardless of container style).
  3. ADD missing cards (with title from <h1> and description from first <p>).
  4. REMOVE orphan cards (pointing to non-existent files).
  5. REFORMAT all cards to canonical 3-span structure.
  6. Preserve the existing container type (<ul class="sections-list"> or
     <div class="section-card-list">).

Run: python _rebuild_chapter_indexes.py --apply
"""
from __future__ import annotations
import argparse
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_MTIME_SECONDS = 600

CHANGES = {
    "files_modified": [],
    "files_skipped_in_flight": [],
    "files_unchanged": [],
    "cards_added": 0,
    "cards_removed": 0,
    "cards_reformatted": 0,
    "descriptions_authored": 0,
    "per_chapter": [],
}


def find_module_indexes() -> list[Path]:
    out = []
    for part_dir in sorted(ROOT.glob("part-*")):
        if not part_dir.is_dir():
            continue
        for mod_dir in sorted(part_dir.glob("module-*")):
            if not mod_dir.is_dir():
                continue
            idx = mod_dir / "index.html"
            if idx.exists():
                out.append(idx)
    return out


def list_section_files(chapter_dir: Path) -> list[tuple[str, Path]]:
    sections = []
    for f in chapter_dir.glob("section-*.html"):
        m = re.match(r"section-(\d+)\.(\d+)\.html", f.name)
        if m:
            major = int(m.group(1))
            minor = int(m.group(2))
            sections.append(((major, minor), f"{major}.{minor}", f))
    sections.sort(key=lambda t: t[0])
    return [(label, path) for (_, label, path) in sections]


def extract_section_metadata(section_file: Path) -> dict:
    text = section_file.read_text(encoding="utf-8")
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', text, re.DOTALL)
    title = ""
    if h1_match:
        title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
    subtitle = ""
    subtitle_match = re.search(r'<p\s+class="chapter-subtitle"[^>]*>(.+?)</p>', text, re.DOTALL)
    if subtitle_match:
        subtitle = re.sub(r'<[^>]+>', '', subtitle_match.group(1)).strip()
    paras = re.findall(r'<p[^>]*>(.+?)</p>', text, re.DOTALL)
    first_p = ""
    for p in paras:
        # skip blockquote/cite/figcaption inner paragraphs
        clean = re.sub(r'<[^>]+>', '', p).strip()
        if not clean:
            continue
        if clean.startswith('"') and clean.endswith('"'):
            continue
        if len(clean) < 80:
            continue
        first_p = clean
        break
    return {"title": title, "subtitle": subtitle, "first_p": first_p}


def distill_description(meta: dict, max_chars: int = 240) -> str:
    if meta["subtitle"]:
        return meta["subtitle"]
    text = meta["first_p"]
    if not text:
        return ""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    out = sentences[0] if sentences else ""
    if len(out) < 120 and len(sentences) > 1:
        candidate = out + " " + sentences[1]
        if len(candidate) <= max_chars:
            out = candidate
    if len(out) > max_chars:
        out = out[:max_chars - 3].rsplit(" ", 1)[0] + "..."
    return out


def safe_text(s: str) -> str:
    """Escape for HTML span content. Preserves existing &amp; entities."""
    # First decode any double-encoded ampersands
    s = s.replace("&amp;", "&")
    # Then re-encode
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return s


def parse_existing_cards(text: str) -> dict[str, dict]:
    """Parse existing section cards. Returns {N.M: {desc, title, container}}."""
    out = {}
    # Match each <a class="section-card" ...> ... </a> anchor
    for m in re.finditer(
        r'<a\s+class="section-card"[^>]*href="([^"]*?section-(\d+)\.(\d+)\.html)"[^>]*>(.+?)</a>',
        text,
        re.DOTALL,
    ):
        href = m.group(1)
        major = int(m.group(2))
        minor = int(m.group(3))
        label = f"{major}.{minor}"
        inner = m.group(4)
        desc_match = re.search(
            r'<span\s+class="section-desc"[^>]*>(.+?)</span>',
            inner,
            re.DOTALL,
        )
        title_match = re.search(
            r'<span\s+class="section-title"[^>]*>(.+?)</span>',
            inner,
            re.DOTALL,
        )
        existing_desc = ""
        if desc_match:
            existing_desc = re.sub(r'\s+', ' ', desc_match.group(1)).strip()
        existing_title = ""
        if title_match:
            existing_title = re.sub(r'\s+', ' ', title_match.group(1)).strip()
        out[label] = {
            "desc": existing_desc,
            "title": existing_title,
            "href": href,
        }
    return out


def detect_container_style(text: str) -> str:
    """Detect 'ul' or 'div' container style. Default 'ul' (canonical)."""
    if re.search(r'<ul\s+class="sections-list"', text):
        return "ul"
    if re.search(r'<div\s+class="section-card-list"', text):
        return "div"
    if re.search(r'<div\s+class="sections-list"', text):
        return "div-sections-list"
    return "ul"


def build_canonical_card(num: str, title: str, desc: str, container_style: str) -> str:
    """Build the canonical 3-span section card.

    For 'ul' container: wrap in <li>. For 'div' container: no <li>.
    """
    # Drop "Section N.M:" prefix if h1 had it
    clean_title = re.sub(rf'^\s*Section\s+{re.escape(num)}[:.]?\s*', '', title).strip()
    clean_title = safe_text(clean_title)
    clean_desc = safe_text(desc)

    inner_card = (
        f'<a class="section-card" href="section-{num}.html">\n'
        f'<span class="section-num">{num}</span>\n'
        f'<span class="section-title">{clean_title}</span>\n'
        f'<span class="section-desc">{clean_desc}</span>\n'
        f'</a>'
    )
    if container_style == "ul":
        return f'<li>\n{inner_card}\n</li>'
    return inner_card


def rebuild_index(idx_path: Path) -> tuple[str | None, dict]:
    chapter_dir = idx_path.parent
    section_files = list_section_files(chapter_dir)
    if not section_files:
        return None, {}

    text = idx_path.read_text(encoding="utf-8")
    original = text

    container_style = detect_container_style(text)
    existing_cards = parse_existing_cards(text)

    stats = {
        "added": [],
        "removed": [],
        "reformatted": 0,
        "descriptions_authored": 0,
    }

    # Build canonical cards list
    new_cards = []
    for label, sec_path in section_files:
        meta = extract_section_metadata(sec_path)
        existing = existing_cards.get(label)

        if existing and existing["desc"] and len(existing["desc"]) > 30:
            desc = existing["desc"]
        else:
            desc = distill_description(meta)
            if desc:
                stats["descriptions_authored"] += 1
        if not desc:
            desc = f"Section {label} of this chapter."

        if not existing:
            stats["added"].append(label)
        new_cards.append(build_canonical_card(label, meta["title"], desc, container_style))

    # Identify orphans (cards that exist in index but no section file)
    actual_labels = {label for label, _ in section_files}
    for label in existing_cards:
        if label not in actual_labels:
            stats["removed"].append(label)

    # Count reformatted: cards with "Section N.M" prefix (old format)
    stats["reformatted"] = len(re.findall(
        r'<span\s+class="section-num">Section\s+\d+\.\d+</span>',
        original,
    ))

    new_cards_html = "\n".join(new_cards)
    if container_style == "ul":
        new_block = '<h2>Sections</h2>\n<ul class="sections-list">\n' + new_cards_html + '\n</ul>'
    elif container_style == "div":
        new_block = '<h2>Sections in This Chapter</h2>\n<div class="section-card-list">\n' + new_cards_html + '\n</div>'
    else:
        new_block = '<h2>Sections</h2>\n<div class="sections-list">\n' + new_cards_html + '\n</div>'

    # Find existing block and replace
    patterns = [
        # h2 + ul
        re.compile(
            r'<h2[^>]*>\s*Sections(?:\s+in\s+This\s+Chapter)?\s*</h2>\s*<ul\s+class="sections-list"[^>]*>.*?</ul>',
            re.DOTALL,
        ),
        # h2 + div.section-card-list
        re.compile(
            r'<h2[^>]*>\s*Sections(?:\s+in\s+This\s+Chapter)?\s*</h2>\s*<div\s+class="section-card-list"[^>]*>.*?</div>',
            re.DOTALL,
        ),
        # h2 + div.sections-list
        re.compile(
            r'<h2[^>]*>\s*Sections(?:\s+in\s+This\s+Chapter)?\s*</h2>\s*<div\s+class="sections-list"[^>]*>.*?</div>',
            re.DOTALL,
        ),
    ]

    replaced = False
    for pat in patterns:
        m = pat.search(text)
        if m:
            text = text[:m.start()] + new_block + text[m.end():]
            replaced = True
            break

    if not replaced:
        # Fallback: insert before <div class="whats-next">
        m = re.search(r'<div\s+class="whats-next"', text)
        if m:
            text = text[:m.start()] + new_block + "\n" + text[m.start():]
            replaced = True

    if not replaced:
        return f"could not locate section list anchor", stats

    if text == original:
        return None, stats

    idx_path.write_text(text, encoding="utf-8")
    return "rewritten", stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--chapter", type=str, default=None)
    args = parser.parse_args()

    if not args.apply and not args.dry_run:
        args.dry_run = True

    indexes = find_module_indexes()
    print(f"Found {len(indexes)} chapter index files", file=sys.stderr)

    now = time.time()
    for idx in indexes:
        if args.chapter and args.chapter not in str(idx):
            continue
        mtime = idx.stat().st_mtime
        if now - mtime < SKIP_MTIME_SECONDS:
            CHANGES["files_skipped_in_flight"].append(str(idx))
            print(f"SKIP (in flight): {idx.relative_to(ROOT)}", file=sys.stderr)
            continue
        if args.dry_run:
            # Read state, show diff
            chapter_dir = idx.parent
            section_files = list_section_files(chapter_dir)
            actual = {label for label, _ in section_files}
            text = idx.read_text(encoding="utf-8")
            existing = parse_existing_cards(text)
            missing = actual - set(existing.keys())
            orphan = set(existing.keys()) - actual
            old_format = len(re.findall(r'<span\s+class="section-num">Section\s+\d+\.\d+</span>', text))
            no_desc = sum(1 for k in existing if not existing[k].get("desc"))
            if missing or orphan or old_format or no_desc:
                rel = idx.relative_to(ROOT).as_posix()
                print(f"WOULD CHANGE {rel}: missing={sorted(missing)} orphan={sorted(orphan)} old_format={old_format} no_desc={no_desc}")
        else:
            result, stats = rebuild_index(idx)
            rel = idx.relative_to(ROOT).as_posix()
            if result == "rewritten":
                CHANGES["files_modified"].append(rel)
                CHANGES["cards_added"] += len(stats["added"])
                CHANGES["cards_removed"] += len(stats["removed"])
                CHANGES["cards_reformatted"] += stats["reformatted"]
                CHANGES["descriptions_authored"] += stats["descriptions_authored"]
                desc = []
                if stats["added"]:
                    desc.append(f"added {stats['added']}")
                if stats["removed"]:
                    desc.append(f"removed {stats['removed']}")
                if stats["reformatted"]:
                    desc.append(f"reformatted {stats['reformatted']} cards")
                if stats["descriptions_authored"]:
                    desc.append(f"authored {stats['descriptions_authored']} descriptions")
                if not desc:
                    desc.append("rebuilt canonical block")
                CHANGES["per_chapter"].append((rel, "; ".join(desc)))
                print(f"FIXED {rel}: {'; '.join(desc)}", file=sys.stderr)
            elif result:
                print(f"WARN {rel}: {result}", file=sys.stderr)
            else:
                CHANGES["files_unchanged"].append(rel)

    print(f"\n=== SUMMARY ===", file=sys.stderr)
    print(f"Files modified: {len(CHANGES['files_modified'])}", file=sys.stderr)
    print(f"Files unchanged: {len(CHANGES['files_unchanged'])}", file=sys.stderr)
    print(f"Files skipped (in flight): {len(CHANGES['files_skipped_in_flight'])}", file=sys.stderr)
    print(f"Cards added: {CHANGES['cards_added']}", file=sys.stderr)
    print(f"Cards removed: {CHANGES['cards_removed']}", file=sys.stderr)
    print(f"Cards reformatted (old 'Section N.M' prefix dropped): {CHANGES['cards_reformatted']}", file=sys.stderr)
    print(f"Descriptions authored: {CHANGES['descriptions_authored']}", file=sys.stderr)

    # Write detailed JSON for the report
    import json
    out_path = ROOT / "scripts" / "_rebuild_chapter_indexes.json"
    with out_path.open("w") as f:
        json.dump(CHANGES, f, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
