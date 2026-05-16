"""Apply deterministic fixes from the 5 per-section audits.

The audits converged on these mechanical patterns:

1. **H2/H3 chapter-prefix renumbering** (dominant pattern, 500+ rewrites):
   Each module's section files have <h2>X.Y.Z Title</h2> headings where X
   is the OLD chapter number from before various renumbers. Rewrite X to
   the current chapter number (the one in the path module-NN-...).

2. **Wrong-relative-depth hrefs in P/Q** (~80 broken in audit):
   appendix-p-course-syllabi/index.html and appendix-q-reading-pathways/
   index.html use ../part-N/ where they need ../../part-N/.

3. **Stale Problem-Solution Key references** (post-v11 cleanup):
   appendices/index.html, fm-how-to-use.html, fm-what-this-book-covers
   .html, appendix-p-course-syllabi/index.html still mention G.
   Strip mentions (the appendix is gone in v11).

4. **Appendix N index title typo**: "Appendix P: MLOps" -> "Appendix N: MLOps"

5. **Section 32.4 stale annotation**: "(from old 33.4)" in title -> remove.

6. **Title suffix missing** (26 section + 5 index files):
   <title>Section X.M: Title</title> -> <title>Section X.M: Title | Building Conversational AI with LLMs and Agents</title>

7. **Section 37.6.1 wrong**: title 27.9, h1 27.6 etc. -- targeted

8. **Add KaTeX** to section-34.11.html (math doesn't render without it).

Idempotent. Run with --apply.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude", ".book-update"}

# H2/H3 prefix renames: (module_num, [list of old prefix numbers that
# appear in this module's section h2/h3 headings])
# Built from the 5 per-section audit findings.
H2_RENAMES = {
    17: [14],
    18: [15],
    19: [16],
    20: [17],
    22: [18],
    23: [19],
    24: [20],
    26: [21],
    27: [22],         # 27.6 also has 33.x (handled below per-file)
    28: [23],         # 28.6 also has 25.x (handled below per-file)
    29: [24],
    31: [26],
    34: [28],
    35: [29],
    37: [30],
    38: [25],
}

# Per-file overrides for sections whose h2 prefix differs from module
# default
PER_FILE_H2_OVERRIDES = {
    "part-6-agentic-ai/module-27-tool-use-protocols/section-27.6.html": (33, 27),
    "part-6-agentic-ai/module-28-multi-agent-systems/section-28.6.html": (25, 28),
}


def fix_h2_prefix(file_path: Path, old_prefix: int, new_prefix: int) -> int:
    """Rewrite <h2>OLD.X.Y</h2> -> <h2>NEW.X.Y</h2>; similarly for h3, h4.
    Also rewrites the same prefix inside h2 IDs, anchor names, and
    'Code Fragment N.M.K' / 'Figure N.M.K' / 'Section N.M' / 'Listing'
    captions where they were renumbered with the chapter."""
    text = file_path.read_text(encoding="utf-8")
    orig = text

    # Patterns:
    # <h2>OLD.X[.Y] Title</h2>     -> <h2>NEW.X[.Y] Title</h2>
    # <h2 id="OLD-X-Y">OLD.X.Y ... -> <h2 id="NEW-X-Y">NEW.X.Y ...
    # Code Fragment OLD.X.Y        -> Code Fragment NEW.X.Y
    # Figure OLD.X.Y / Table OLD.X.Y / Listing OLD.X.Y / Pseudocode OLD.X.Y

    # Heading text
    for level in (2, 3, 4):
        # <hN>OLD.X[.Y] Title</hN>
        text = re.sub(
            rf'(<h{level}[^>]*>){old_prefix}\.(\d+)(\.\d+)?(\s+[^<]*)?(</h{level}>)',
            lambda m: f'{m.group(1)}{new_prefix}.{m.group(2)}{m.group(3) or ""}{m.group(4) or ""}{m.group(5)}',
            text,
        )

    # Captions
    for kind in ("Code Fragment", "Figure", "Table", "Listing", "Pseudocode"):
        text = re.sub(
            rf'\b{kind}\s+{old_prefix}\.(\d+)(\.\d+)?\b',
            lambda m: f'{kind} {new_prefix}.{m.group(1)}{m.group(2) or ""}',
            text,
        )

    if text == orig:
        return 0
    file_path.write_text(text, encoding="utf-8")
    return 1


def fix_wrong_depth_hrefs(file_path: Path) -> int:
    """In appendix index files in the For-Instructors group, hrefs that
    use ../part-N/ should use ../../part-N/ (one more level up)."""
    text = file_path.read_text(encoding="utf-8")
    orig = text
    # Match href="../part-XX-" and rewrite to href="../../part-XX-"
    text = re.sub(
        r'href="\.\./(part-\d+-)',
        r'href="../../\1',
        text,
    )
    # Also href="../appendix-X-" inside appendix index pages should
    # stay relative (they're correct as ../). Don't touch those.
    if text == orig:
        return 0
    file_path.write_text(text, encoding="utf-8")
    return 1


def strip_problem_solution_key_refs(file_path: Path) -> int:
    """Strip mentions of dropped Problem-Solution Key appendix (G in v10,
    dropped in v11). Patterns:
    - 'Appendix G: Problem-Solution Key' text
    - <a> wrappers around 'Problem-Solution Key' text
    - 'problem-solution-key' / 'appendix-g-problem-solution-key' in hrefs
    """
    text = file_path.read_text(encoding="utf-8")
    orig = text
    # Strip <a> wrappers pointing to dropped appendix
    text = re.sub(
        r'<a\s+[^>]*href="[^"]*appendix-g-problem-solution-key[^"]*"[^>]*>'
        r'([^<]*)</a>',
        r'\1',
        text,
    )
    # Strip 'Appendix G: Problem-Solution Key' standalone mentions
    text = text.replace("Appendix G: Problem-Solution Key", "")
    text = text.replace("Appendix G (Problem-Solution Key)", "")
    # Tidy resulting double-spaces / orphan parens
    text = re.sub(r'  +', ' ', text)
    text = text.replace("(, ", "(").replace(", )", ")")
    if text == orig:
        return 0
    file_path.write_text(text, encoding="utf-8")
    return 1


def add_title_suffix(file_path: Path) -> int:
    """If <title>...something</title> lacks the ` | Building Conversational
    AI with LLMs and Agents` suffix, add it."""
    text = file_path.read_text(encoding="utf-8")
    orig = text
    suffix = " | Building Conversational AI with LLMs and Agents"
    def repl(m: re.Match) -> str:
        inner = m.group(1).strip()
        if suffix in inner or "Building Conversational AI" in inner:
            return m.group(0)
        return f'<title>{inner}{suffix}</title>'
    text = re.sub(r'<title>([^<]+)</title>', repl, text, count=1)
    if text == orig:
        return 0
    file_path.write_text(text, encoding="utf-8")
    return 1


def fix_specific_files() -> dict:
    """Targeted fixes for individually-flagged anomalies."""
    counts = {"appx_n_title": 0, "ch32_4_title": 0, "katex_added": 0}

    # 1. Appendix N index <title> says 'Appendix P: MLOps' -> 'Appendix N: MLOps'
    p = ROOT / "appendices" / "appendix-n-mlops" / "index.html"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        if "Appendix P: MLOps" in text:
            text = text.replace("Appendix P: MLOps", "Appendix N: MLOps")
            p.write_text(text, encoding="utf-8")
            counts["appx_n_title"] = 1

    # 2. section-32.4 stale '(from old 33.4)' annotation
    p = ROOT / "part-7-multimodal-generation" / "module-32-embodied-world-models" / "section-32.4.html"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        orig = text
        text = re.sub(r'\s*\(from old 33\.4\)', '', text)
        if text != orig:
            p.write_text(text, encoding="utf-8")
            counts["ch32_4_title"] = 1

    # 3. KaTeX missing in section-34.11 (math doesn't render)
    p = ROOT / "part-8-evaluation-production" / "module-34-evaluation-observability" / "section-34.11.html"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        if 'katex' not in text.lower():
            # Insert KaTeX <link> + <script> + auto-render <script> after <link rel="stylesheet" href="...book.css"/>
            katex_block = (
                '<link href="../../vendor/katex/katex.min.css" rel="stylesheet"/>\n'
                '<script defer="" src="../../vendor/katex/katex.min.js"></script>\n'
                '<script defer="" onload="renderMathInElement(document.body, '
                '{delimiters: [{left: \'$$\', right: \'$$\', display: true},'
                ' {left: \'$\', right: \'$\', display: false}], throwOnError: false});" '
                'src="../../vendor/katex/contrib/auto-render.min.js"></script>\n'
            )
            text = re.sub(
                r'(<link href="[^"]*book\.css"[^>]*/>\n)',
                r'\1' + katex_block,
                text, count=1,
            )
            p.write_text(text, encoding="utf-8")
            counts["katex_added"] = 1
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if not args.apply:
        print("Run with --apply to execute. Estimated 500+ rewrites + small fixes.")
        return 0

    totals = {
        "h2_renames": 0,
        "wrong_depth": 0,
        "psk_refs": 0,
        "title_suffix": 0,
    }

    # H2 prefix renumbering per module
    for mod_num, old_prefixes in H2_RENAMES.items():
        for part_dir in sorted(ROOT.iterdir()):
            if not part_dir.is_dir():
                continue
            if not part_dir.name.startswith("part-"):
                continue
            mod_dirs = list(part_dir.glob(f"module-{mod_num:02d}-*"))
            if not mod_dirs:
                continue
            mod_dir = mod_dirs[0]
            for sec in sorted(mod_dir.glob(f"section-{mod_num}.*.html")):
                rel = str(sec.relative_to(ROOT)).replace("\\", "/")
                # Per-file override?
                if rel in PER_FILE_H2_OVERRIDES:
                    old_p, new_p = PER_FILE_H2_OVERRIDES[rel]
                    totals["h2_renames"] += fix_h2_prefix(sec, old_p, new_p)
                else:
                    for old_p in old_prefixes:
                        totals["h2_renames"] += fix_h2_prefix(sec, old_p, mod_num)

    # Wrong-depth hrefs in For-Instructors P/Q appendix indexes
    for p_path in [
        ROOT / "appendices" / "appendix-p-course-syllabi" / "index.html",
        ROOT / "appendices" / "appendix-q-reading-pathways" / "index.html",
    ]:
        if p_path.exists():
            totals["wrong_depth"] += fix_wrong_depth_hrefs(p_path)

    # Strip Problem-Solution Key references from known high-visibility pages
    psk_targets = [
        ROOT / "appendices" / "index.html",
        ROOT / "front-matter" / "fm-how-to-use.html",
        ROOT / "front-matter" / "fm-what-this-book-covers.html",
        ROOT / "appendices" / "appendix-p-course-syllabi" / "index.html",
    ]
    for p_path in psk_targets:
        if p_path.exists():
            totals["psk_refs"] += strip_problem_solution_key_refs(p_path)

    # Title suffix for appendix files lacking it
    for p_path in sorted(ROOT.rglob("*.html")):
        if set(p_path.parts) & SKIP_PARTS:
            continue
        if "appendices" not in str(p_path) and "front-matter" not in str(p_path):
            continue
        totals["title_suffix"] += add_title_suffix(p_path)

    # Specific one-off fixes
    one_offs = fix_specific_files()

    print(f"=== APPLY ===")
    print(f"H2 prefix renumbers:       {totals['h2_renames']} files")
    print(f"Wrong-depth href fixes:    {totals['wrong_depth']} files")
    print(f"PSK reference strips:      {totals['psk_refs']} files")
    print(f"Title suffix added:        {totals['title_suffix']} files")
    print(f"Appendix N title fix:      {one_offs['appx_n_title']}")
    print(f"Section 32.4 annotation:   {one_offs['ch32_4_title']}")
    print(f"KaTeX added to 34.11:      {one_offs['katex_added']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
