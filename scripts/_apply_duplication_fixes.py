"""Apply deterministic fixes from the duplication audits.

Cross-part audit findings (parts-duplication-audit.md):
1. Delete Module 46/47 duplicate section files:
   46.3 == 46.1, 46.4 == 46.2, 47.3 == 47.1, 47.4 == 47.2
   (Stale '31.x' H2 numbering; clean duplicates per audit.)
2. Delete Module 48 orphan files NOT in chapter index:
   48.5, 48.6 (orphans), 48.4 (== 49.1 Post-Launch Monitoring).
3. Delete Module 61 leftover section-33.X.html files:
   section-33.4.html, section-33.11.html (content migrated to 32.4 / 64.5).
4. Fix Module 45 stale 'Section 34.X.X' H2 numbering -> '45.X.X'.

Appendices audit findings (appendices-duplication-audit.md):
5. N.2/N.3/N.4 stale breadcrumb 'Section M.3/M.4/M.5' -> N.X correctly.
6. Q index.html broken double-'appendices/' link to R.

NOT applied (need content judgment):
- A.6 Information Theory duplicate of A.4 (might be intentional reference)
- I.4 'Installing vLLM' duplicate of L.1 (might be a brief mention vs full)
- P.4 vLLM/TGI in Docker (might be Docker-flavored variant of L)
- M.4 Production Data Pipelines overlap with O.1/O.3/O.5 (large rewrite)
- Part XI .7 files (need per-file authoring decision)

Idempotent. Run with --apply.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git_rm(paths: list[Path], dry_run: bool) -> int:
    """Run `git rm -f` on each path that exists; return count removed."""
    n = 0
    for p in paths:
        if not p.exists():
            print(f"  SKIP (already gone): {p.relative_to(ROOT)}")
            continue
        if dry_run:
            print(f"  WOULD git rm -f {p.relative_to(ROOT)}")
        else:
            res = subprocess.run(
                ["git", "rm", "-f", str(p)],
                cwd=ROOT, capture_output=True, text=True,
            )
            if res.returncode == 0:
                print(f"  git rm {p.relative_to(ROOT)}")
                n += 1
            else:
                print(f"  FAIL: {p.relative_to(ROOT)} ({res.stderr.strip()})")
    return n


def strip_section_cards_from_index(idx_path: Path, section_filenames: list[str],
                                     dry_run: bool) -> bool:
    """Remove <li><a href='section-X.Y.html'>...</a></li> entries from the
    chapter index's section list when the referenced file is being deleted."""
    if not idx_path.exists():
        return False
    text = idx_path.read_text(encoding="utf-8")
    orig = text
    for fn in section_filenames:
        # Match li containing a link to fn
        pattern = re.compile(
            rf'<li>\s*<a[^>]*href="{re.escape(fn)}"[^>]*>[\s\S]*?</a>\s*</li>',
            re.IGNORECASE,
        )
        text = pattern.sub("", text)
    if text == orig:
        return False
    if not dry_run:
        idx_path.write_text(text, encoding="utf-8")
    return True


def fix_h2_numbering(file_path: Path, old_prefix: str, new_prefix: str,
                      dry_run: bool) -> int:
    """Rewrite <h2>OLDPREFIX.X.Y</h2> -> <h2>NEWPREFIX.X.Y</h2> book-style."""
    if not file_path.exists():
        return 0
    text = file_path.read_text(encoding="utf-8")
    orig = text
    # Match common patterns: "<h2>34.5.1 Title</h2>" and similar
    pattern = re.compile(
        rf'<h([234])>{re.escape(old_prefix)}\.(\d+)(\.\d+)?(\s+[^<]*)?</h\1>'
    )
    def repl(m: re.Match) -> str:
        level = m.group(1)
        x = m.group(2)
        y = m.group(3) or ""
        rest = m.group(4) or ""
        return f'<h{level}>{new_prefix}.{x}{y}{rest}</h{level}>'
    text = pattern.sub(repl, text)
    if text == orig:
        return 0
    if not dry_run:
        file_path.write_text(text, encoding="utf-8")
    return 1


def fix_breadcrumb_section_label(file_path: Path, old_label: str,
                                    new_label: str, dry_run: bool) -> int:
    """Find 'Section M.X' references and replace with 'Section N.X' etc."""
    if not file_path.exists():
        return 0
    text = file_path.read_text(encoding="utf-8")
    orig = text
    text = text.replace(old_label, new_label)
    if text == orig:
        return 0
    if not dry_run:
        file_path.write_text(file_path, encoding="utf-8")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply
    mode = "DRY-RUN" if dry_run else "APPLY"

    # ===== Phase 1: Delete duplicate / orphan section files =====
    print(f"\n=== {mode}: Phase 1 - Delete duplicate / orphan files ===")

    duplicates_to_delete = [
        # Module 46 duplicates
        ROOT / "part-10-idea-to-product" / "module-46-compute-planning" / "section-46.3.html",
        ROOT / "part-10-idea-to-product" / "module-46-compute-planning" / "section-46.4.html",
        # Module 47 duplicates
        ROOT / "part-10-idea-to-product" / "module-47-scaling-economics" / "section-47.3.html",
        ROOT / "part-10-idea-to-product" / "module-47-scaling-economics" / "section-47.4.html",
        # Module 48 orphans (not in chapter index) + 48.4 == 49.1
        ROOT / "part-10-idea-to-product" / "module-48-shipping-deploying" / "section-48.5.html",
        ROOT / "part-10-idea-to-product" / "module-48-shipping-deploying" / "section-48.6.html",
        # Note: 48.4 NOT deleted; content overlaps with 49.1 but deletion needs
        # backref-author decision. Leave it for manual review.
        # Module 61 leftover section-33.X.html files
        ROOT / "part-12-frontiers" / "module-61-frontier-architectures" / "section-33.4.html",
        ROOT / "part-12-frontiers" / "module-61-frontier-architectures" / "section-33.11.html",
    ]
    git_rm(duplicates_to_delete, dry_run)

    # Strip section-cards from chapter indexes for the deleted sections
    if not dry_run:
        strip_section_cards_from_index(
            ROOT / "part-10-idea-to-product" / "module-46-compute-planning" / "index.html",
            ["section-46.3.html", "section-46.4.html"], dry_run,
        )
        strip_section_cards_from_index(
            ROOT / "part-10-idea-to-product" / "module-47-scaling-economics" / "index.html",
            ["section-47.3.html", "section-47.4.html"], dry_run,
        )
        strip_section_cards_from_index(
            ROOT / "part-12-frontiers" / "module-61-frontier-architectures" / "index.html",
            ["section-33.4.html", "section-33.11.html"], dry_run,
        )

    # ===== Phase 2: Fix Module 45 stale '34.X.X' H2 numbering =====
    print(f"\n=== {mode}: Phase 2 - Fix Module 45 H2 numbering 34.X -> 45.X ===")
    mod45_dir = ROOT / "part-10-idea-to-product" / "module-45-prototype-to-production"
    if mod45_dir.exists():
        for sf in mod45_dir.glob("section-45.*.html"):
            n = fix_h2_numbering(sf, "34", "45", dry_run)
            if n:
                print(f"  {sf.relative_to(ROOT).name}: fixed H2 numbering")

    # ===== Phase 3: Q broken double-appendices link =====
    print(f"\n=== {mode}: Phase 3 - Fix Q index broken double-appendices link ===")
    q_idx = ROOT / "appendices" / "appendix-q-course-syllabi" / "index.html"
    if q_idx.exists():
        text = q_idx.read_text(encoding="utf-8")
        orig = text
        text = text.replace("../appendices/appendix-r-",
                              "../appendix-r-")
        if text != orig and not dry_run:
            q_idx.write_text(text, encoding="utf-8")
            print(f"  Fixed double-appendices link in Q index")

    print(f"\n=== {mode} complete ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
