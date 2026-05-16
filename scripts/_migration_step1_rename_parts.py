"""Migration step 1: rename Part directories per the target yaml.

Specifically (with Frontiers moving to last):

  part-10-frontiers          -> part-12-frontiers
  part-11-idea-to-product    -> part-10-idea-to-product
  part-12-llm-applications-across-industries -> part-11-applications-across-industries
  part-7-multimodal-applications -> part-7-multimodal-generation  (slug change too)
  part-9-safety-strategy     -> part-9-safety-security-ethics     (slug change too)

The 10-11-12 rotation is a 3-way swap. We use a temp prefix to avoid
collisions:

  Step a: part-10-frontiers -> _tmp-12-frontiers
  Step b: part-11-idea-to-product -> part-10-idea-to-product
  Step c: part-12-llm-applications-across-industries -> part-11-applications-across-industries
  Step d: _tmp-12-frontiers -> part-12-frontiers

Plus the two slug-only renames (Part VII, Part IX) are straightforward.

After moves: walks every HTML file inside each renamed part and updates the
internal pagefind-meta references and the breadcrumb anchors so they reflect
the new Part number/title. Then runs a global pass to rewrite any
cross-reference to those parts in the rest of the book.

Idempotent: skips moves whose source no longer exists.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


# Old slug -> (final_slug, old_num, new_num, new_roman, new_title)
MOVES = [
    ("part-10-frontiers",
     "part-12-frontiers", 10, 12, "XII", "Frontiers"),
    ("part-11-idea-to-product",
     "part-10-idea-to-product", 11, 10, "X", "Idea to Product"),
    ("part-12-llm-applications-across-industries",
     "part-11-applications-across-industries", 12, 11, "XI",
     "Applications Across Industries"),
    ("part-7-multimodal-applications",
     "part-7-multimodal-generation", 7, 7, "VII", "Multimodal Generation"),
    ("part-9-safety-strategy",
     "part-9-safety-security-ethics", 9, 9, "IX",
     "Safety, Security & Ethics"),
]

# Parts whose num doesn't change (the swap involves only X / XI / XII)
SWAP_TRIO = {10, 11, 12}


def git_mv(src: Path, dst: Path, dry_run: bool) -> str:
    if not src.exists():
        return f"  SKIP {src.name}: source missing"
    if dst.exists():
        return f"  SKIP {src.name} -> {dst.name}: target exists"
    if dry_run:
        return f"  WOULD git mv {src.name} -> {dst.name}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "mv", str(src), str(dst)],
                    cwd=ROOT, check=False)
    return f"  git mv {src.name} -> {dst.name}"


def execute_part_renames(dry_run: bool) -> list[str]:
    """Execute the file-system moves with the 3-way swap trick."""
    msgs: list[str] = []

    # Slug-only renames first (no number swap)
    for old_slug, new_slug, _, _, _, _ in MOVES:
        if not old_slug.startswith("part-10") and not old_slug.startswith("part-11") and not old_slug.startswith("part-12"):
            msgs.append(git_mv(ROOT / old_slug, ROOT / new_slug, dry_run))

    # 3-way swap with temp prefix
    # Step a: 10 -> _tmp-12
    msgs.append(git_mv(ROOT / "part-10-frontiers",
                        ROOT / "_tmp-12-frontiers", dry_run))
    # Step b: 11 -> 10
    msgs.append(git_mv(ROOT / "part-11-idea-to-product",
                        ROOT / "part-10-idea-to-product", dry_run))
    # Step c: 12 -> 11
    msgs.append(git_mv(
        ROOT / "part-12-llm-applications-across-industries",
        ROOT / "part-11-applications-across-industries", dry_run))
    # Step d: _tmp-12 -> 12
    msgs.append(git_mv(ROOT / "_tmp-12-frontiers",
                        ROOT / "part-12-frontiers", dry_run))

    return msgs


def update_internal_metadata(dry_run: bool) -> list[str]:
    """For each HTML file inside a renamed part, rewrite the inline references
    that mention the OLD part number/title.

    Specifically:
    - data-pagefind-meta="part:Part X: Frontiers" -> "part:Part XII: Frontiers"
    - <a href="../index.html">Part X: Frontiers</a> -> "Part XII: Frontiers"
    - any "Part X" / "Part XI" / "Part XII" body-text mention that points at
       this Part lives in the same file.

    This is the WITHIN-part fix-up. The book-wide cross-ref rewrite is a
    separate step (_migration_step6_rewrite_crossrefs.py).
    """
    msgs: list[str] = []

    for old_slug, new_slug, old_num, new_num, new_roman, new_title in MOVES:
        part_dir = ROOT / new_slug
        if not part_dir.exists():
            msgs.append(f"  SKIP internal update {new_slug}: dir missing")
            continue
        old_roman = {7: "VII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}[old_num]
        # Old title may be different — read from existing index.html
        old_index = part_dir / "index.html"
        old_title = None
        if old_index.exists():
            text = old_index.read_text(encoding="utf-8")
            m = re.search(r'<h1[^>]*class="part-title"[^>]*>([^<]+)</h1>',
                            text)
            if m:
                old_title = m.group(1).strip()
                old_title = re.sub(r"^Part [IVXLCDM]+:\s*", "", old_title)

        if old_title is None:
            old_title_pat = r"[^<]+"
        else:
            old_title_pat = re.escape(old_title)

        n_files = 0
        for p in part_dir.rglob("*.html"):
            text = p.read_text(encoding="utf-8")
            orig = text

            # Update part-meta + breadcrumb anchor
            text = re.sub(
                rf'data-pagefind-meta="part:Part {old_roman}: ({old_title_pat})"',
                f'data-pagefind-meta="part:Part {new_roman}: {new_title}"',
                text,
            )
            text = re.sub(
                rf'(<a href="(?:\.\./)*index\.html">)Part {old_roman}: ({old_title_pat})(</a>)',
                rf'\1Part {new_roman}: {new_title}\3',
                text,
            )
            # Plain text breadcrumb-current span
            text = re.sub(
                rf'(<span class="bc-current">)Part {old_roman}(</span>)',
                rf'\1Part {new_roman}\2',
                text,
            )
            # h1 part-title on the part index
            text = re.sub(
                rf'(<h1[^>]*class="part-title"[^>]*>)Part {old_roman}: ({old_title_pat})(</h1>)',
                rf'\1Part {new_roman}: {new_title}\3',
                text,
            )

            if text != orig:
                n_files += 1
                if not dry_run:
                    p.write_text(text, encoding="utf-8")
        msgs.append(f"  {new_slug}: updated {n_files} files' internal metadata")
    return msgs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode}: Part renames ===")
    for m in execute_part_renames(dry_run):
        print(m)

    print(f"\n=== {mode}: Update internal metadata ===")
    for m in update_internal_metadata(dry_run):
        print(m)

    if dry_run:
        print("\n(dry run; re-run with --apply to execute)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
