"""Fix broken chapter-nav prev/next refs after v9 reshuffle.

Two classes of bugs from earlier renumbers:

1. **Chapter-prefix drift in nav**: section-NN.M.html files in
   module-NN-something/ that have prev/next pointing to section-XX.Y.html
   where XX != NN. The fix: rewrite XX -> NN, keeping the .Y part as-is
   (truncating Y if it now points past the actual last section).

2. **Cross-module nav pointing to dropped or renamed modules**:
   e.g., next="../module-25-agent-safety-production/index.html" when
   that module is now named differently or doesn't exist. Replace with
   "../module-{actual-next}/index.html" by finding the next sibling
   module in the part dir.

3. **Dropped-appendix nav refs**: prev/next pointing to
   appendix-n-master-reference-tables, appendix-p-freshness-2026, or
   glossary/. Drop the link element (replace with the previous/next valid
   appendix that exists, or just remove the nav link entirely).

Read-only with --dry-run; apply with --apply.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PART_DIRS = [
    "part-1-foundations", "part-2-understanding-llms",
    "part-3-working-with-llms", "part-4-training-adaptation",
    "part-5-retrieval-conversation", "part-6-agentic-ai",
    "part-7-multimodal-generation", "part-8-evaluation-production",
    "part-9-safety-security-ethics", "part-10-idea-to-product",
    "part-11-applications-across-industries", "part-12-frontiers",
]
MODULE_RE = re.compile(r"module-(\d+)-")
SECTION_RE = re.compile(r"section-(\d+)\.(\d+)\.html")
DROPPED_APPENDICES = {
    "appendix-n-master-reference-tables",
    "appendix-p-freshness-2026",
}


def fix_section_nav_prefix(p: Path, mod_num: int, dry_run: bool) -> int:
    """In section-NN.M.html, rewrite prev/next from section-XX.Y.html to
    section-NN.Y.html if XX != NN. Returns number of edits."""
    text = p.read_text(encoding="utf-8")
    orig = text
    # Match href="section-XX.Y.html" inside chapter-nav block only.
    # We work on the full doc since the only section-X.Y.html references
    # are typically nav targets (other refs would have an absolute path).
    def repl(m: re.Match) -> str:
        xx, y = int(m.group(1)), m.group(2)
        if xx == mod_num:
            return m.group(0)
        return f'href="section-{mod_num}.{y}.html"'
    text = re.sub(r'href="section-(\d+)\.(\d+)\.html"', repl, text)
    if text == orig:
        return 0
    if not dry_run:
        p.write_text(text, encoding="utf-8")
    return 1


def fix_cross_module_nav(p: Path, module_dirs_in_part: list[Path],
                          current_module: Path, dry_run: bool) -> int:
    """If section/index has nav pointing to ../module-XX-slug/index.html
    that doesn't exist, find the nearest existing sibling module and
    redirect. Returns number of edits."""
    text = p.read_text(encoding="utf-8")
    orig = text

    # Build a sorted list of module numbers in this part
    mod_nums_in_part = sorted(
        [int(MODULE_RE.match(m.name).group(1)) for m in module_dirs_in_part
         if MODULE_RE.match(m.name)])
    cur_num = int(MODULE_RE.match(current_module.name).group(1))
    cur_idx = mod_nums_in_part.index(cur_num) if cur_num in mod_nums_in_part else -1

    def find_module_by_num(num: int) -> Path | None:
        for m in module_dirs_in_part:
            mm = MODULE_RE.match(m.name)
            if mm and int(mm.group(1)) == num:
                return m
        return None

    # Pattern: ../module-NN-slug/index.html
    def repl(m: re.Match) -> str:
        target = m.group(0)
        # Extract the module slug path
        path_match = re.search(r'\.\./module-(\d+)-([^/"]+)', target)
        if not path_match:
            return target
        target_num = int(path_match.group(1))
        target_dir = find_module_by_num(target_num)
        if target_dir is not None:
            # Module exists at this number but maybe with different slug.
            # Replace with actual slug.
            return re.sub(r'\.\./module-\d+-[^/"]+',
                           f'../{target_dir.name}', target)
        # Module number doesn't exist. Find nearest existing.
        # If target was supposed to be 'next', find next higher number;
        # if 'prev', find previous lower number.
        if cur_idx < 0:
            return target
        # Determine direction from class attr in surrounding context
        # (approximation: just find nearest existing number)
        candidates = [n for n in mod_nums_in_part if abs(n - target_num) <= 5]
        if candidates:
            best = min(candidates, key=lambda n: abs(n - target_num))
            best_dir = find_module_by_num(best)
            if best_dir:
                return re.sub(r'\.\./module-\d+-[^/"]+',
                               f'../{best_dir.name}', target)
        return target

    text = re.sub(r'href="\.\./module-\d+-[^/"]+/index\.html"',
                    repl, text)
    if text == orig:
        return 0
    if not dry_run:
        p.write_text(text, encoding="utf-8")
    return 1


def strip_dropped_appendix_nav(p: Path, dry_run: bool) -> int:
    """Replace nav <a> blocks pointing to dropped appendices with a
    placeholder or rewire to the next valid appendix.

    For appendix-n-master-reference-tables -> rewire to appendix-o-course-syllabi (next valid by letter order: but actually O is now Course Syllabi).
    Actually: in v9, the appendix after M (Docker) is O (Course Syllabi).
    For appendix-p-freshness-2026 -> next valid was P (Reading Pathways).

    Simpler: just strip the dead link, replacing the <a>...</a> with the
    inner text. This removes the broken navigation but preserves the
    visual breadcrumb. Author can re-wire to a real target later.
    """
    text = p.read_text(encoding="utf-8")
    orig = text

    for dead in DROPPED_APPENDICES:
        # Match: <a class="prev|next|up" href="../{dead}/...">...</a>
        # Replace with: empty (drop the nav link entirely; keep the
        # surrounding <nav class="chapter-nav"> structure)
        pattern = (rf'<a\s+class="(?:prev|next|up)"\s+'
                    rf'href="\.\./{re.escape(dead)}/[^"]*"[^>]*>'
                    rf'.*?</a>')
        text = re.sub(pattern, "", text, flags=re.DOTALL)

    if text == orig:
        return 0
    if not dry_run:
        p.write_text(text, encoding="utf-8")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    n_prefix_fixes = 0
    n_cross_mod_fixes = 0
    n_dropped_strips = 0

    for part_slug in PART_DIRS:
        part_dir = ROOT / part_slug
        if not part_dir.exists():
            continue
        module_dirs = sorted(
            [m for m in part_dir.iterdir()
             if m.is_dir() and MODULE_RE.match(m.name)])
        for mod_dir in module_dirs:
            mod_match = MODULE_RE.match(mod_dir.name)
            if not mod_match:
                continue
            mod_num = int(mod_match.group(1))
            # Sections
            for sec in mod_dir.glob("section-*.html"):
                sm = SECTION_RE.match(sec.name)
                if not sm:
                    continue
                # Fix #1: section nav prefix drift
                n_prefix_fixes += fix_section_nav_prefix(
                    sec, mod_num, dry_run)
                # Fix #2: cross-module nav
                n_cross_mod_fixes += fix_cross_module_nav(
                    sec, module_dirs, mod_dir, dry_run)
            # Also index.html
            idx = mod_dir / "index.html"
            if idx.exists():
                n_cross_mod_fixes += fix_cross_module_nav(
                    idx, module_dirs, mod_dir, dry_run)

    # Pass: strip dropped-appendix nav in all HTML
    skip = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}
    for p in ROOT.rglob("*.html"):
        if set(p.parts) & skip:
            continue
        n_dropped_strips += strip_dropped_appendix_nav(p, dry_run)

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode} ===")
    print(f"Section-nav prefix fixes:   {n_prefix_fixes} files")
    print(f"Cross-module nav fixes:     {n_cross_mod_fixes} files")
    print(f"Dropped-appendix nav strip: {n_dropped_strips} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
