"""v4.1: Apply all auto-fixable items the audit-mining agent surfaced.

Items:
  1. Wider auto-link bug: <a>Section X.Y</a> still appears in table cells,
     formula rows, Key Takeaways. v3.7 unwrap only caught running prose.
  2. Module 18 part-label propagation (Part 2 -> Part 10) — all 5 files.
  3. Module 36 absorbed-sections reference deleted module-37/images/* —
     fix img src paths to module-36 image dir.
  4. Auto-annotation leakage: '1. Heading Intermediate' / '2. X Advanced'
     patterns in table titles, SVG aria-labels, comparison-table titles.
  5. Stale Ch30 / Ch35 / Ch37 mentions in nav/prose beyond v3.7 sweep.
  6. Doubled caption deeper sweep (matches `# Code Fragment` in pre + a
     separate caption div).
  7. Title-tag mismatches (e.g., section-32.11 <title> says 32.10).
  8. Cross-chapter index card hrefs (10/13/25 card -> wrong chapter file).
  9. Strong-tag mid-number splits ('<strong>Section 27.</strong>5').
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}
MAX_FILE = 5_000_000


def safe_read(p: Path) -> str | None:
    try:
        if p.stat().st_size > MAX_FILE: return None
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


# =====================================================================
# Item 1: wider auto-link bug — also catch in <th>, <td>, .takeaways, etc.
# =====================================================================
def item_1_wider_unwrap() -> None:
    """Unwrap <a>Section X.Y</a> in all non-chrome contexts (was prose-only).

    The v3.7 script restricted to running prose. Audit found instances in:
      - <td> / <th> cells (esp. activation-function formula table)
      - Key Takeaways <li>
      - SVG <text>
      - <strong>Section X.Y</strong> mid-sentence
      - Epigraph quote bodies

    Strategy: if anchor display text is EXACTLY 'Section X.Y' (no surrounding
    word), unwrap UNLESS it's inside a real cross-ref context (preceded by
    'see', 'in', 'from', etc.).
    """
    anchor = re.compile(
        r'<a\s+[^>]*href="[^"]*section-(\d+\.\d+)\.html(?:#[^"]*)?"[^>]*>'
        r'Section\s+(\d+\.\d+)'
        r'</a>'
    )
    intentional = re.compile(
        r'(?:see|in|from|to|of|chapter|cf\.?|under|via|covered\s+in|'
        r'discussed\s+in|introduced\s+in|presented\s+in|detailed\s+in|'
        r'explained\s+in|described\s+in|defined\s+in|including|earlier|later)\s+$',
        re.IGNORECASE,
    )

    def is_intentional(text: str, start: int) -> bool:
        chunk = text[max(0, start - 40):start]
        chunk = re.sub(r'<[^>]+>', '', chunk)
        return bool(intentional.search(chunk))

    # No chrome guard this time — we go everywhere except inside <h1> or .toc-link
    def is_chrome(text: str, start: int) -> bool:
        chunk = text[max(0, start - 600):start]
        # Only protect H1 (page title) and explicit TOC nav
        for marker in [r"<h1\b", r'class="[^"]*(?:toc-link|chapter-nav|sidebar|chapter-card-title|module-card-title|section-card)[^"]*"']:
            opens = list(re.finditer(marker, chunk))
            if opens and not re.search(r"</(?:h1|nav|aside|a)>", chunk[opens[-1].start():]):
                return True
        return False

    n_files = 0
    n_unwrapped = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        original = text
        matches = list(anchor.finditer(text))
        for m in reversed(matches):
            if is_chrome(text, m.start()): continue
            if is_intentional(text, m.start()): continue
            # Unwrap: replace with plain "Section X.Y" text
            text = text[:m.start()] + f"Section {m.group(1)}" + text[m.end():]
            n_unwrapped += 1
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"  Item 1: {n_unwrapped} additional 'Section X.Y' anchors unwrapped in {n_files} files")


# =====================================================================
# Item 2: Module 18 part-label propagation
# =====================================================================
def item_2_module_18() -> None:
    n_files = 0
    n_fixes = 0
    for p in (ROOT / "part-10-frontiers/module-18-interpretability").rglob("*.html"):
        text = safe_read(p)
        if text is None: continue
        original = text
        # Part 2 -> Part 10 in part-label / breadcrumb / prev-next
        text = re.sub(r'class="part-label">[^<]*Part\s+(?:2|II)\b[^<]*', 'class="part-label">Part 10', text)
        text = re.sub(r'Part\s+II:\s*Understanding\s+LLMs', 'Part X: Frontiers', text)
        text = re.sub(r'Part\s+2:\s*Understanding\s+LLMs', 'Part 10: Frontiers', text)
        # Bread crumb link to part-2 → part-10
        text = re.sub(r'href="(?:\.\./)*part-2-understanding-llms/index\.html',
                       'href="../index.html', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += 1
    print(f"  Item 2: Module 18 part-label propagated in {n_files} files")


# =====================================================================
# Item 3: Module 36 broken image paths to deleted module-37/images/
# =====================================================================
def item_3_module_36_images() -> None:
    n_files = 0
    n_fixes = 0
    for p in (ROOT / "part-11-idea-to-product/module-36-idea-to-product").rglob("*.html"):
        text = safe_read(p)
        if text is None: continue
        original = text
        text = re.sub(
            r'src="(?:\.\./)*module-37-building-steering/images/',
            'src="images/',
            text,
        )
        text = re.sub(
            r'href="(?:\.\./)*module-37-building-steering/images/',
            'href="images/',
            text,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += 1
    print(f"  Item 3: Module 36 broken image paths fixed in {n_files} files")


# =====================================================================
# Item 4: auto-annotation leakage ('1. Heading Intermediate')
# =====================================================================
def item_4_strip_annotation_leakage() -> None:
    """Strip leading enumeration '1. ' and trailing difficulty badge from
    titles/aria-labels/comparison-table-title that leaked from an internal
    skill annotation."""
    n_files = 0
    n_fixes = 0
    # Pattern: "N. Title Difficulty" inside specific containers
    difficulty_words = r"(?:Beginner|Intermediate|Advanced|Expert)"
    targets = [
        # Comparison-table title
        re.compile(rf'(<div\s+class="comparison-table-title"[^>]*>)\s*\d+\.\s*([^<]+?)\s+{difficulty_words}(?:</div>|\s*\()'),
        # aria-label="Diagram: N. Title Difficulty"
        re.compile(rf'(aria-label="Diagram:\s*)\d+\.\s*([^"]+?)\s+{difficulty_words}(")'),
        # Generic strong-tag title
        re.compile(rf'(<strong>)\s*\d+\.\s*([^<]+?)\s+{difficulty_words}(</strong>)'),
    ]
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        original = text
        for pat in targets:
            text, n = pat.subn(lambda m: m.group(1) + m.group(2).strip() + (m.group(3) if len(m.groups()) >= 3 else ''), text)
            n_fixes += n
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"  Item 4: {n_fixes} auto-annotation leakages stripped in {n_files} files")


# =====================================================================
# Item 5: stale Ch30 / Ch35 / Ch37 mentions
# =====================================================================
def item_5_stale_chapter_refs() -> None:
    n_files = 0
    n_fixes = 0
    replacements = [
        # Chapter 30 was merged into 29
        (r'\bcompanion Chapter 30\b', 'companion sections later in this chapter'),
        (r'\bChapter 30\b', 'Module 29 (Observability sections)'),
        (r'\bobservability\s+\(\s*Chapter\s+30\s*\)', 'observability (later in Module 29)'),
        # Chapter 35 was merged into 32 + 17
        (r'\bChapter 35: AI and Society\b', 'Module 32: Safety, Ethics & Regulation'),
        (r'\bChapter 35:\s*AI &amp; Society\b', 'Module 32: Safety, Ethics & Regulation'),
        (r'\bChapter 35\b', 'Module 32'),
        # Chapter 37 was merged into 36
        (r'\bChapter 37: Building and Steering\b', 'Module 36 (sections 36.4-36.7)'),
        (r'\bChapter 37\b', 'Module 36'),
    ]
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        original = text
        for pat, repl in replacements:
            text, n = re.subn(pat, repl, text)
            n_fixes += n
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"  Item 5: {n_fixes} stale chapter refs fixed in {n_files} files")


# =====================================================================
# Item 6: doubled caption deeper sweep
# =====================================================================
def item_6_doubled_captions_round_2() -> None:
    n_files = 0
    n_fixes = 0
    # Pattern: <strong>Code Fragment X.Y.Z:</strong> Code Fragment X'.Y'.Z':
    # (the second prefix even if different number)
    pat = re.compile(
        r'(<strong>Code Fragment\s+\d+\.\d+\.\d+:?</strong>)\s*'
        r'Code Fragment\s+\d+\.\d+\.\d+:?\s*'
    )
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        new_text, n = pat.subn(r'\1 ', text)
        if n > 0 and new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_fixes += n
    print(f"  Item 6: {n_fixes} doubled captions (round 2) fixed in {n_files} files")


# =====================================================================
# Item 7: title-tag mismatches (heuristic: <title>Section X.Y... but file is X.Z)
# =====================================================================
def item_7_title_tag_match() -> None:
    n_files = 0
    n_fixes = 0
    for p in ROOT.glob("part-*/module-*/section-*.html"):
        m_file = re.match(r"section-(\d+)\.(\d+)\.html", p.name)
        if not m_file: continue
        file_num = f"{m_file.group(1)}.{m_file.group(2)}"
        text = safe_read(p)
        if text is None: continue
        # Find <title>Section X.Y...</title>
        title_m = re.search(r'<title[^>]*>Section\s+(\d+\.\d+):', text)
        if not title_m: continue
        if title_m.group(1) == file_num: continue
        # Mismatch - fix to file_num
        original = text
        text = re.sub(
            rf'(<title[^>]*>Section\s+){re.escape(title_m.group(1))}(:)',
            rf'\g<1>{file_num}\g<2>',
            text,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += 1
            print(f"    fix <title>{title_m.group(1)} -> {file_num} in {p.name}")
    print(f"  Item 7: {n_fixes} title tags resynced in {n_files} files")


# =====================================================================
# Item 8: cross-chapter index card hrefs
# =====================================================================
def item_8_cross_chapter_cards() -> None:
    """Remove cards in module-X/index.html that link to a different chapter's
    section file."""
    n_files = 0
    n_removed = 0
    for mod_dir in ROOT.glob("part-*/module-*/"):
        if not mod_dir.is_dir(): continue
        chapter = mod_dir.name.split("-")[1]
        try:
            chapter_int = int(chapter)
        except ValueError:
            continue
        idx = mod_dir / "index.html"
        if not idx.exists(): continue
        text = safe_read(idx)
        if text is None: continue
        original = text
        # Find <a class="section-card" href="section-N.M.html"> where N != chapter
        bad_pat = re.compile(
            rf'<a[^>]*href="section-(\d+)\.\d+\.html(?:#[^"]*)?"[^>]*class="section-card"[^>]*>.*?</a>',
            re.DOTALL,
        )
        def maybe_drop(m):
            nonlocal n_removed
            href_chap = int(m.group(1))
            if href_chap != chapter_int:
                n_removed += 1
                return ''
            return m.group(0)
        text = bad_pat.sub(maybe_drop, text)
        if text != original:
            idx.write_text(text, encoding="utf-8")
            n_files += 1
    print(f"  Item 8: {n_removed} cross-chapter index cards removed in {n_files} files")


# =====================================================================
# Item 10: strong-tag splits section number ('<strong>Section 27.</strong>5')
# =====================================================================
def item_10_markup_straddle() -> None:
    n_files = 0
    n_fixes = 0
    pat = re.compile(r'<strong>([^<]*Section\s+\d+)\.</strong>(\d+)')
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        new_text = pat.sub(r'<strong>\1.\2</strong>', text)
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_fixes += 1
    print(f"  Item 10: {n_fixes} markup-straddle fixes in {n_files} files")


def main() -> int:
    print("Item 1: wider auto-link unwrap"); item_1_wider_unwrap()
    print("Item 2: Module 18 part-label propagation"); item_2_module_18()
    print("Item 3: Module 36 broken image paths"); item_3_module_36_images()
    print("Item 4: auto-annotation leakage"); item_4_strip_annotation_leakage()
    print("Item 5: stale Ch30/35/37 refs"); item_5_stale_chapter_refs()
    print("Item 6: doubled captions round 2"); item_6_doubled_captions_round_2()
    print("Item 7: title-tag mismatch"); item_7_title_tag_match()
    print("Item 8: cross-chapter index cards"); item_8_cross_chapter_cards()
    print("Item 10: strong-tag markup straddle"); item_10_markup_straddle()
    return 0


if __name__ == "__main__":
    sys.exit(main())
