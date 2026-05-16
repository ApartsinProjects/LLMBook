"""Rebuild every chapter index's section card list to canonical 3-span format.

Canonical format (verified from module-48-shipping-deploying/index.html):

  <a class="section-card" href="section-N.M.html">
  <span class="section-num">N.M</span>
  <span class="section-title">Section Title</span>
  <span class="section-desc">One-to-two sentence description.</span>
  </a>

Tasks:
  1. List actual section-NN.M.html files in each chapter directory.
  2. Compare to what the index advertises.
  3. ADD missing cards (with title from <h1> and description from first <p>).
  4. REMOVE orphan cards (pointing to non-existent files).
  5. REFORMAT all cards to canonical 3-span structure.

Run: python _rebuild_chapter_indexes.py --apply
"""
from __future__ import annotations
import argparse
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Module index files we should never touch (skip windows < 10 min mtime)
SKIP_MTIME_SECONDS = 600

# Track which files we changed for the report
CHANGES = {
    "files_modified": [],
    "files_skipped_in_flight": [],
    "cards_added": 0,
    "cards_removed": 0,
    "cards_reformatted": 0,
    "descriptions_authored": 0,
    "per_chapter": [],  # list of (chapter_dir, action_description)
}


def find_module_indexes() -> list[Path]:
    """Find every part-N-slug/module-NN-slug/index.html."""
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
    """List section-N.M.html files in numeric order. Returns [(N.M, path), ...]."""
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
    """Extract h1 title and first <p> for description.
    Returns: {title: str, first_p: str, subtitle: str}.
    """
    text = section_file.read_text(encoding="utf-8")
    # h1 (may be followed by <div class="page-current">)
    h1_match = re.search(r'<h1[^>]*>(.+?)</h1>', text, re.DOTALL)
    title = ""
    if h1_match:
        title = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
    # subtitle (skip the byline epigraph quotes - those start with ")
    subtitle = ""
    subtitle_match = re.search(r'<p\s+class="chapter-subtitle"[^>]*>(.+?)</p>', text, re.DOTALL)
    if subtitle_match:
        subtitle = re.sub(r'<[^>]+>', '', subtitle_match.group(1)).strip()
    # first substantive <p> after the header / page-current div
    # skip epigraphs (quoted "..."), skip nav-cite paragraphs
    paras = re.findall(r'<p[^>]*>(.+?)</p>', text, re.DOTALL)
    first_p = ""
    for p in paras:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        # skip epigraph quotes
        if clean.startswith('"') and clean.endswith('"'):
            continue
        # skip nav/breadcrumb fragments
        if len(clean) < 60:
            continue
        first_p = clean
        break
    return {"title": title, "subtitle": subtitle, "first_p": first_p}


def distill_description(meta: dict, max_chars: int = 240) -> str:
    """Make a 1-2 sentence description from section metadata."""
    if meta["subtitle"]:
        return meta["subtitle"]
    text = meta["first_p"]
    if not text:
        return ""
    # Split into sentences, keep first 1-2
    sentences = re.split(r'(?<=[.!?])\s+', text)
    out = sentences[0] if sentences else ""
    # Try to add second sentence if first is short
    if len(out) < 120 and len(sentences) > 1:
        candidate = out + " " + sentences[1]
        if len(candidate) <= max_chars:
            out = candidate
    if len(out) > max_chars:
        out = out[:max_chars - 3].rsplit(" ", 1)[0] + "..."
    return out


def build_canonical_card(num: str, title: str, desc: str) -> str:
    """Build the canonical 3-span section card.

    Format matches module-48 exactly, with <li> wrapper.
    """
    # Title: drop "Section N.M:" prefix if present in h1
    clean_title = re.sub(rf'^\s*Section\s+{re.escape(num)}[:.]?\s*', '', title).strip()
    # Don't double-encode
    clean_title = clean_title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("&amp;amp;", "&amp;")
    # Fix common: already-encoded &amp; got double-encoded
    clean_title = clean_title.replace("&amp;amp;", "&amp;")

    clean_desc = desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    clean_desc = clean_desc.replace("&amp;amp;", "&amp;")

    return (
        f'<li>\n'
        f'<a class="section-card" href="section-{num}.html">\n'
        f'<span class="section-num">{num}</span>\n'
        f'<span class="section-title">{clean_title}</span>\n'
        f'<span class="section-desc">{clean_desc}</span>\n'
        f'</a>\n'
        f'</li>'
    )


def rebuild_index(idx_path: Path) -> str | None:
    """Rebuild section card list for one chapter index file.

    Returns a brief action description if changed, None otherwise.
    """
    chapter_dir = idx_path.parent
    section_files = list_section_files(chapter_dir)
    if not section_files:
        return None

    text = idx_path.read_text(encoding="utf-8")
    original = text

    # Build canonical cards list, pulling title/desc from each section
    cards = []
    desc_authored_count = 0
    for label, sec_path in section_files:
        meta = extract_section_metadata(sec_path)
        # Check if index already has a description for this section
        existing_desc = ""
        existing_pattern = re.compile(
            rf'<a[^>]*href="section-{re.escape(label)}\.html"[^>]*>(.*?)</a>',
            re.DOTALL,
        )
        existing_match = existing_pattern.search(text)
        if existing_match:
            desc_m = re.search(
                r'<span\s+class="section-desc"[^>]*>(.+?)</span>',
                existing_match.group(1),
                re.DOTALL,
            )
            if desc_m:
                existing_desc = re.sub(r'\s+', ' ', desc_m.group(1)).strip()

        if existing_desc and len(existing_desc) > 30:
            desc = existing_desc
        else:
            desc = distill_description(meta)
            if desc:
                desc_authored_count += 1
        if not desc:
            desc = f"Section {label} of this chapter."
        cards.append(build_canonical_card(label, meta["title"], desc))

    # Find the section list container in the file
    # Two known shapes:
    #   <ul class="sections-list"> ... </ul>
    #   <div class="section-card-list"> ... </div>
    # Plus the variant where it's just "<h2>Sections</h2>" followed by anchors
    new_cards_html = "\n".join(cards)
    new_block_html = (
        '<h2>Sections</h2>\n<ul class="sections-list">\n'
        + new_cards_html
        + '\n</ul>'
    )

    # Try canonical pattern: <h2>Sections</h2> ... <ul class="sections-list"> ... </ul>
    pat1 = re.compile(
        r'<h2[^>]*>\s*Sections(?:\s+in\s+This\s+Chapter)?\s*</h2>\s*<ul\s+class="sections-list"[^>]*>.*?</ul>',
        re.DOTALL,
    )
    pat2 = re.compile(
        r'<h2[^>]*>\s*Sections(?:\s+in\s+This\s+Chapter)?\s*</h2>\s*<div\s+class="section-card-list"[^>]*>.*?</div>',
        re.DOTALL,
    )
    pat3 = re.compile(
        r'<h2[^>]*>\s*Sections(?:\s+in\s+This\s+Chapter)?\s*</h2>\s*<div\s+class="sections-list"[^>]*>.*?</div>',
        re.DOTALL,
    )

    replaced = False
    for pat in (pat1, pat2, pat3):
        m = pat.search(text)
        if m:
            text = text[:m.start()] + new_block_html + text[m.end():]
            replaced = True
            break

    if not replaced:
        # Fallback: insert before <div class="whats-next"> if section block missing
        m = re.search(r'<div\s+class="whats-next"', text)
        if m:
            text = text[:m.start()] + new_block_html + "\n" + text[m.start():]
            replaced = True

    if not replaced:
        return f"could not locate section list anchor"

    # Count diff
    if text == original:
        return None

    # Count old vs new card hrefs
    old_hrefs = set(re.findall(r'href="(section-\d+\.\d+\.html)"', original))
    new_hrefs = set(re.findall(r'href="(section-\d+\.\d+\.html)"', text))
    added = new_hrefs - old_hrefs
    removed = old_hrefs - new_hrefs
    # Count reformatted (cards with old "Section N.M" prefix and 2-span form)
    old_old_format_count = len(re.findall(r'<span\s+class="section-num">Section\s+\d+\.\d+</span>', original))
    # All cards in new are 3-span
    new_canonical_count = len(re.findall(r'<span\s+class="section-num">\d+\.\d+</span>', text))

    CHANGES["cards_added"] += len(added)
    CHANGES["cards_removed"] += len(removed)
    CHANGES["cards_reformatted"] += old_old_format_count
    CHANGES["descriptions_authored"] += desc_authored_count

    idx_path.write_text(text, encoding="utf-8")

    parts = []
    if added:
        parts.append(f"added {sorted(added)}")
    if removed:
        parts.append(f"removed {sorted(removed)}")
    parts.append(f"reformatted to 3-span ({new_canonical_count} cards)")
    if desc_authored_count:
        parts.append(f"authored {desc_authored_count} descriptions")
    return "; ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write changes")
    parser.add_argument("--dry-run", action="store_true", help="Dry run only")
    parser.add_argument("--chapter", type=str, default=None, help="Only this chapter (path fragment)")
    args = parser.parse_args()

    if not args.apply and not args.dry_run:
        args.dry_run = True

    indexes = find_module_indexes()
    print(f"Found {len(indexes)} chapter index files", file=sys.stderr)

    now = time.time()
    for idx in indexes:
        if args.chapter and args.chapter not in str(idx):
            continue
        # Skip in-flight files
        mtime = idx.stat().st_mtime
        if now - mtime < SKIP_MTIME_SECONDS:
            CHANGES["files_skipped_in_flight"].append(str(idx))
            print(f"SKIP (in flight): {idx.relative_to(ROOT)}", file=sys.stderr)
            continue
        if args.dry_run:
            # report only
            chapter_dir = idx.parent
            section_files = list_section_files(chapter_dir)
            text = idx.read_text(encoding="utf-8")
            advertised = set(re.findall(r'href="(section-\d+\.\d+\.html)"', text))
            actual = {f"section-{label}.html" for label, _ in section_files}
            missing = actual - advertised
            orphan = advertised - actual
            old_format_cards = re.findall(r'<span\s+class="section-num">Section\s+\d+\.\d+</span>', text)
            if missing or orphan or old_format_cards:
                print(f"WOULD CHANGE {idx.relative_to(ROOT)}: missing={missing} orphan={orphan} old_format={len(old_format_cards)}")
        else:
            result = rebuild_index(idx)
            if result:
                rel = idx.relative_to(ROOT).as_posix()
                CHANGES["files_modified"].append(rel)
                CHANGES["per_chapter"].append((rel, result))
                print(f"FIXED {rel}: {result}", file=sys.stderr)

    print(f"\n=== SUMMARY ===", file=sys.stderr)
    print(f"Files modified: {len(CHANGES['files_modified'])}", file=sys.stderr)
    print(f"Files skipped (in flight): {len(CHANGES['files_skipped_in_flight'])}", file=sys.stderr)
    print(f"Cards added: {CHANGES['cards_added']}", file=sys.stderr)
    print(f"Cards removed: {CHANGES['cards_removed']}", file=sys.stderr)
    print(f"Cards reformatted (old 'Section N.M' prefix dropped): {CHANGES['cards_reformatted']}", file=sys.stderr)
    print(f"Descriptions authored: {CHANGES['descriptions_authored']}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
