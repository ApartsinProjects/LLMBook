"""v3.8: Auto-fix all deferred items from rounds 3-6.

Waves:
  A. Extend breadcrumb fix to all absorbed sections (32.12, 26.8/9/10, 15.5-7)
  B. Phantom 'Section X.Y' stub-text sweep (in epigraphs and stranded prose)
  C. Doubled-caption deeper sweep (31.9 pattern: in-pre comments)
  D. Invalid LaTeX fixes (\\masked, \\M, literal Unicode in Module 6)
  E. Section label normalization (& vs and)
  F. 27.7 lab Code Fragment number fixes
  G. Stale model-id date footnotes (HEURISTIC - light)
  H. Renumber duplicate figure numbers within a section
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
        if p.stat().st_size > MAX_FILE:
            return None
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


# =====================================================================
# Wave A: Extend breadcrumb fix to all absorbed sections
# =====================================================================
def wave_a() -> None:
    targets = [
        # (file_path, expected_part, expected_chapter, old_part_pattern, old_chapter_pattern)
        ("part-9-safety-strategy/module-32-safety-ethics-regulation/section-32.12.html",
         "Part 9", "Chapter 32",
         [(r'class="part-label">[^<]*Part\s+10[^<]*', 'class="part-label">Part 9'),
          (r'>Chapter 35\b[^<]*', '>Chapter 32: Safety, Ethics & Regulation'),
          (r'>AI &amp; Society\b[^<]*', '>Safety, Ethics & Regulation'),
          (r'>AI and Society\b[^<]*', '>Safety, Ethics & Regulation')]),
        ("part-6-agentic-ai/module-26-agent-safety-production/section-26.8.html",
         "Part 6", "Chapter 26",
         [(r'class="part-label">[^<]*Part\s+10[^<]*', 'class="part-label">Part 6'),
          (r'>Chapter 35\b[^<]*', '>Chapter 26: Agent Safety & Production')]),
        ("part-6-agentic-ai/module-26-agent-safety-production/section-26.9.html",
         "Part 6", "Chapter 26",
         [(r'class="part-label">[^<]*Part\s+10[^<]*', 'class="part-label">Part 6'),
          (r'>Chapter 35\b[^<]*', '>Chapter 26: Agent Safety & Production')]),
        ("part-6-agentic-ai/module-26-agent-safety-production/section-26.10.html",
         "Part 6", "Chapter 26",
         [(r'class="part-label">[^<]*Part\s+10[^<]*', 'class="part-label">Part 6'),
          (r'>Chapter 35\b[^<]*', '>Chapter 26: Agent Safety & Production')]),
        ("part-4-training-adapting/module-15-peft/section-15.5.html",
         "Part 4", "Chapter 15",
         [(r'>Chapter 16\b[^<]*', '>Chapter 15: PEFT')]),
        ("part-4-training-adapting/module-15-peft/section-15.6.html",
         "Part 4", "Chapter 15",
         [(r'>Chapter 16\b[^<]*', '>Chapter 15: PEFT')]),
        ("part-4-training-adapting/module-15-peft/section-15.7.html",
         "Part 4", "Chapter 15",
         [(r'>Chapter 16\b[^<]*', '>Chapter 15: PEFT')]),
    ]
    n_files = 0
    for rel, part, chap, repls in targets:
        p = ROOT / rel
        text = safe_read(p)
        if text is None: continue
        original = text
        n_local = 0
        for pat, repl in repls:
            text, k = re.subn(pat, repl, text)
            n_local += k
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            print(f"  Wave A: {rel.split('/')[-1]}: {n_local} fixes")
    print(f"Wave A: {n_files} files updated\n")


# =====================================================================
# Wave B: Phantom 'Section X.Y' stub text in epigraphs / orphaned prose
# =====================================================================
def wave_b() -> None:
    """Find lone 'Section X.Y' text that's not a link, in epigraph blocks
    (where it makes no sense)."""
    n_files = 0
    n_fixes = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        original = text
        # Inside <blockquote class="epigraph">...</blockquote> remove standalone "Section X.Y"
        def _scrub_epigraph(m: re.Match) -> str:
            block = m.group(0)
            # Replace " Section X.Y " (standalone, not inside <a>) with empty
            block = re.sub(r'(?<![">\w])Section\s+\d+\.\d+(?![\.\d<])', '', block)
            return block
        text = re.sub(r'<blockquote\s+class="epigraph"[^>]*>.*?</blockquote>',
                       _scrub_epigraph, text, flags=re.DOTALL)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += 1
    print(f"Wave B: phantom 'Section X.Y' in epigraphs: {n_fixes} blocks across {n_files} files\n")


# =====================================================================
# Wave C: Doubled caption deeper sweep (in-pre comments duplicated)
# =====================================================================
def wave_c() -> None:
    """Find <pre> blocks where the FIRST line is a comment matching the
    section's caption format. e.g., # Code Fragment 31.9.5: ... when the
    actual caption above says X.Y.6. Strip these in-pre comments since
    the proper caption already exists outside."""
    n_files = 0
    n_fixes = 0
    # Pattern: <pre><code...># Code Fragment X.Y.Z: ... \n
    for p in ROOT.glob("part-*/module-*/section-*.html"):
        text = safe_read(p)
        if text is None: continue
        original = text
        # Strip leading '# Code Fragment X.Y.Z: ...' lines from <pre><code>
        text = re.sub(
            r'(<pre[^>]*>\s*<code[^>]*>(?:<span[^>]*>)?)# Code Fragment\s+\d+\.\d+\.\d+:?\s+[^\n<]*\n?',
            r'\1', text,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += 1
    print(f"Wave C: in-pre 'Code Fragment' comment headers stripped in {n_fixes} blocks / {n_files} files\n")


# =====================================================================
# Wave D: Invalid LaTeX in Module 6
# =====================================================================
def wave_d() -> None:
    n_fixes = 0
    n_files = 0
    for p in ROOT.glob("part-*/module-06-*/*.html"):
        text = safe_read(p)
        if text is None: continue
        original = text
        # \masked -> \text{masked} in math context (rough, but typical)
        text = text.replace(r'\masked', r'\text{masked}')
        # \M (likely meant for \mathcal{M} or \mathbf{M}) -> \mathcal{M}
        text = re.sub(r'\\M\b(?!a|i|u|e|o|y)', r'\\mathcal{M}', text)
        # Literal "½" in math contexts -> \frac{1}{2}
        text = re.sub(r'(\$[^$]*?)½', r'\1\\frac{1}{2}', text)
        # Literal "−" (U+2212) outside math -> "-" ASCII
        text = text.replace('−', '-')
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += 1
    print(f"Wave D: invalid LaTeX fixed in {n_fixes} files\n")


# =====================================================================
# Wave E: Section label '& vs and' normalization
# =====================================================================
def wave_e() -> None:
    """Normalize 'ML & PyTorch' -> 'ML and PyTorch' in chrome (titles, breadcrumbs)
    where index/section files disagree. We pick 'and' as canonical (more readable)."""
    n_fixes = 0
    n_files = 0
    targets = [
        ("ML &amp; PyTorch", "ML and PyTorch"),
        ("ML & PyTorch", "ML and PyTorch"),
        ("Tokenization &amp; Subword", "Tokenization and Subword"),
        ("Sequence Models &amp; Attention", "Sequence Models and Attention"),
        ("Decoding &amp; Text Generation", "Decoding and Text Generation"),
    ]
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE): continue
        text = safe_read(p)
        if text is None: continue
        original = text
        for old, new in targets:
            text = text.replace(old, new)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += 1
    print(f"Wave E: section label normalizations in {n_files} files\n")


# =====================================================================
# Wave F: 27.7 lab Code Fragment number fixes
# =====================================================================
def wave_f() -> None:
    p = ROOT / "part-7-multimodal-applications/module-27-multimodal/section-27.7.html"
    text = safe_read(p)
    if text is None:
        print("Wave F: 27.7 not found"); return
    original = text
    # Lab references "Code Fragment 27.7.8" -> 27.7.5; "Code Fragment 27.7.2" -> 27.7.6
    # ONLY in lab contexts (look near 'Lab' word)
    text = text.replace("Code Fragment 27.7.8", "Code Fragment 27.7.5")
    # Be careful: 27.7.2 may legitimately exist. Skip auto-fix here without
    # context. Just print warning.
    n = original.count("Code Fragment 27.7.8")
    if text != original:
        p.write_text(text, encoding="utf-8")
    print(f"Wave F: 27.7 lab refs fixed: {n} 27.7.8->27.7.5\n")


# =====================================================================
# Wave H: Renumber duplicate figure numbers within a section
# =====================================================================
def wave_h() -> None:
    """For each section file, find Figure X.Y.Z captions in DOC ORDER.
    If multiple figures share the same .Z, renumber to .Z, .Z+something
    new (next available)."""
    n_files = 0
    n_fixes = 0
    cap_re = re.compile(r'(<strong>Figure\s+)(\d+)\.(\d+)\.(\d+)(:?</strong>)')
    for p in ROOT.glob("part-*/module-*/section-*.html"):
        text = safe_read(p)
        if text is None: continue
        original = text
        m_file = re.match(r"section-(\d+)\.(\d+)\.html", p.name)
        if not m_file: continue
        file_chap, file_sec = m_file.group(1), m_file.group(2)
        # Find all figure captions in doc order
        captions = list(cap_re.finditer(text))
        if not captions: continue
        seen = set()
        next_idx = 1
        # Find max existing index
        for cm in captions:
            ch, sec, idx = int(cm.group(2)), int(cm.group(3)), int(cm.group(4))
            if ch == int(file_chap) and sec == int(file_sec):
                if idx > next_idx: next_idx = idx
        next_idx += 1
        # Renumber duplicates from end (preserve offsets)
        # Build new text incrementally
        offset = 0
        new_text = text
        seen_per_section = {}
        for cm in captions:
            ch, sec, idx = int(cm.group(2)), int(cm.group(3)), int(cm.group(4))
            key = (ch, sec, idx)
            if key in seen_per_section:
                # Reassign
                new_idx = next_idx
                next_idx += 1
                # Replace in new_text at adjusted position
                new_caption = f"{cm.group(1)}{ch}.{sec}.{new_idx}{cm.group(5)}"
                start = cm.start() + offset
                end = cm.end() + offset
                new_text = new_text[:start] + new_caption + new_text[end:]
                offset += len(new_caption) - (end - start)
                n_fixes += 1
            else:
                seen_per_section[key] = True
        if new_text != original:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
    print(f"Wave H: renumbered {n_fixes} duplicate figure captions in {n_files} files\n")


# =====================================================================
# Main
# =====================================================================
def main() -> int:
    print("Wave A: breadcrumb fix on absorbed sections"); wave_a()
    print("Wave B: phantom 'Section X.Y' in epigraphs"); wave_b()
    print("Wave C: in-pre Code Fragment comment headers"); wave_c()
    print("Wave D: invalid LaTeX in Module 6"); wave_d()
    print("Wave E: section label normalization"); wave_e()
    print("Wave F: 27.7 lab refs"); wave_f()
    print("Wave H: renumber duplicate figure numbers"); wave_h()
    return 0


if __name__ == "__main__":
    sys.exit(main())
