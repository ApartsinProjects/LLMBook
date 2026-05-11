"""v3.7 R6 Waves 4-8: misc cleanups.

Wave 4: Module 17.5 absorbed-section breadcrumbs (Part 9 -> Part 4, etc.)
Wave 5: Strip stale Module 37 references (Module 36/38 indexes still
        mention Chapter 37)
Wave 6: Detect & renumber duplicate figure numbers within a section
Wave 7: Fix doubled caption prefixes ("Code Fragment X.Y.Z: Code Fragment X.Y.Z: ...")
Wave 8: Remove ghost section-21.7 card (file doesn't exist)
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def wave_4_fix_17_5_breadcrumbs() -> None:
    p = ROOT / "part-4-training-adapting/module-17-alignment-rlhf-dpo/section-17.5.html"
    if not p.exists():
        print("  [skip] 17.5 missing")
        return
    text = p.read_text(encoding="utf-8", errors="replace")
    original = text
    # Replace "Chapter 35", "Part 9", "Part X", "Frontiers" labels
    replacements = [
        (r'class="part-label">.*?Part\s+(?:9|IX|X)\b[^<]*', 'class="part-label">Part 4'),
        (r'>Chapter 35[^<]*', '>Chapter 17'),
        (r'>AI &amp; Society[^<]*', '>Alignment Frontiers'),
        (r'>AI and Society[^<]*', '>Alignment Frontiers'),
        # Cross-refs into part-9/module-32 -> within own module
        (r'href="\.\./\.\./part-9-safety-strategy/module-32-safety-ethics-regulation/',
         'href="../../part-4-training-adapting/module-17-alignment-rlhf-dpo/'),
    ]
    n = 0
    for pat, repl in replacements:
        text, k = re.subn(pat, repl, text)
        n += k
    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"  17.5: {n} breadcrumb/label rewrites")


def wave_5_strip_module_37_refs() -> None:
    """Module 36/38 indexes mention 'Chapter 37' which no longer exists."""
    n_files = 0
    n_fixes = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in ("_archive", "KDP")):
            continue
        try:
            sz = p.stat().st_size
            if sz > 5_000_000:
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except (OSError, MemoryError):
            continue
        if "Chapter 37" not in text and "module-37" not in text:
            continue
        original = text
        # Replace "Chapter 37: Building..." with "Module 36 (continued)"
        text = re.sub(r'Chapter\s+37(\s*:\s*Building\s+(?:and\s+|&amp;\s+)?Steering[^<\n]*)?',
                       'Module 36', text)
        text = re.sub(r'href="[^"]*module-37-building-steering/[^"]*"',
                       'href="../module-36-idea-to-product/index.html"', text)
        text = re.sub(r'src="[^"]*module-37-building-steering/[^"]*"',
                       '', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_fixes += 1
    print(f"  Module 37 ghost cleanup: {n_fixes} fixes in {n_files} files")


def wave_7_fix_doubled_captions() -> None:
    """Caption pattern: 'Code Fragment X.Y.Z: Code Fragment X.Y.Z: <real>'."""
    n_files = 0
    n_fixes = 0
    pattern = re.compile(
        r'(<strong>Code Fragment\s+\d+\.\d+\.\d+:?</strong>)\s*'
        r'Code Fragment\s+\d+\.\d+\.\d+:?\s*',
    )
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in ("_archive", "KDP")):
            continue
        try:
            sz = p.stat().st_size
            if sz > 5_000_000:
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
        except (OSError, MemoryError):
            continue
        new_text, n = pattern.subn(r'\1 ', text)
        if n > 0 and new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_files += 1
            n_fixes += n
    print(f"  Doubled caption prefixes: {n_fixes} fixed in {n_files} files")


def wave_8_remove_ghost_21_7() -> None:
    p = ROOT / "part-5-retrieval-conversation/module-21-conversational-ai/index.html"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8", errors="replace")
    original = text
    # Remove any section-card pointing to section-21.7.html (which doesn't exist)
    text = re.sub(
        r'<a[^>]*href="section-21\.7\.html(?:#[^"]*)?"[^>]*class="section-card"[^>]*>.*?</a>',
        '', text, flags=re.DOTALL,
    )
    if text != original:
        p.write_text(text, encoding="utf-8")
        print("  21.7 ghost card removed from module-21 index")


def main() -> int:
    print("Wave 4: 17.5 breadcrumbs"); wave_4_fix_17_5_breadcrumbs()
    print("Wave 5: stale Module 37 refs"); wave_5_strip_module_37_refs()
    print("Wave 7: doubled caption prefixes"); wave_7_fix_doubled_captions()
    print("Wave 8: ghost 21.7 card"); wave_8_remove_ghost_21_7()
    return 0


if __name__ == "__main__":
    sys.exit(main())
