"""Migration step 3: renumber chapters per the target yaml.

After step 1 (Part renames) ran, the parts are at their final slugs but the
modules inside still use OLD chapter numbers. Step 3 walks the target yaml
and:

1. For each chapter that exists in current state (has `old_num`) and whose
   number changed: `git mv` the module-NN-slug dir to module-MM-slug.

2. For each chapter that exists but stays in its current part (no move):
   if old_num != new num, rename module dir + update internal references.

3. For each chapter that MOVED PARTS (the chapter slug exists in target's
   part but NOT in current's same part), it has already been git mv-d in
   step 1 if the whole part moved (parts X/XI/XII swap), OR it's a chapter
   from a DISSOLVING module that has no whole-dir analog (sections move
   individually in step 5).

4. After moves: update breadcrumb chapter num, page-current text, pagefind
   chapter meta in every file inside the renamed module.

NOTE: Sections from dissolving modules (25, 27, 31) are NOT moved by this
script. Step 5 handles those.

Idempotent: skips moves whose source no longer exists.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]


def find_part_dir(target_part: dict) -> Path:
    """Return current on-disk dir for a target part (slugs may have been
    updated in step 1)."""
    candidates = [
        ROOT / f"part-{target_part['num']}-{target_part['slug']}",
    ]
    for c in candidates:
        if c.exists():
            return c
    # Fall back to glob
    matches = list(ROOT.glob(f"part-{target_part['num']}-*"))
    if matches:
        return matches[0]
    return None


def find_module_dir_by_slug(part_dir: Path, slug: str) -> Path | None:
    """Find a module dir inside part_dir by slug (slug stable across renumber)."""
    matches = list(part_dir.glob(f"module-*-{slug}"))
    if matches:
        return matches[0]
    return None


def update_module_internal(mod_dir: Path, new_chap_num: int, new_chap_title: str,
                            new_chap_subtitle: str | None, dry_run: bool) -> int:
    """Update breadcrumb chapter num + page-current + chapter meta in every
    file inside the renamed module."""
    n = 0
    for p in mod_dir.rglob("*.html"):
        text = p.read_text(encoding="utf-8")
        orig = text
        # Pagefind chapter meta
        text = re.sub(
            r'data-pagefind-meta="chapter:Chapter \d+(?:: [^"]+)?"',
            f'data-pagefind-meta="chapter:Chapter {new_chap_num}: {new_chap_title}"',
            text,
        )
        # Breadcrumb "Chapter N: ..." anchor inside .page-breadcrumb
        text = re.sub(
            r'(<a href="index\.html">)Chapter \d+(?::[^<]*)?(</a>)',
            rf'\1Chapter {new_chap_num}: {new_chap_title}\2',
            text,
        )
        # bc-current "Chapter N"
        text = re.sub(
            r'(<span class="bc-current">)Chapter \d+(</span>)',
            rf'\1Chapter {new_chap_num}\2',
            text,
        )
        # h1 on chapter landing (only if file is index.html in module)
        if p.name == "index.html":
            # Don't touch h1 text (it's the chapter title, already correct)
            pass

        if text != orig:
            n += 1
            if not dry_run:
                p.write_text(text, encoding="utf-8")
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=Path,
                    default=ROOT / "book_structure.target.yaml")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    target = yaml.safe_load(args.target.read_text(encoding="utf-8"))

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"=== {mode}: Chapter renumbers ===")

    renumber_count = 0
    update_count = 0
    for p in target["parts"]:
        part_dir = find_part_dir(p)
        if part_dir is None:
            print(f"  WARN: part dir for Part {p['num']} ({p['slug']}) missing")
            continue
        for c in p.get("chapters", []):
            if c.get("_new"):
                continue  # New chapter, was scaffolded already
            slug = c["slug"]
            new_num = c["num"]
            # Locate current module by slug
            mod_dir = find_module_dir_by_slug(part_dir, slug)
            if mod_dir is None:
                # Try old slug from the chapter (if it changed) - look for slug variants
                # The slug may have been renamed in t6/t8 (e.g. idea-to-product -> prototype-to-production)
                # Use a known alias if present
                if slug == "prototype-to-production":
                    mod_dir = find_module_dir_by_slug(part_dir, "idea-to-product")
                elif slug == "shipping-deploying":
                    mod_dir = find_module_dir_by_slug(part_dir, "shipping-scaling")
                elif slug == "multimodal":
                    mod_dir = find_module_dir_by_slug(part_dir, "multimodal")
                elif slug == "emerging-architectures":
                    mod_dir = find_module_dir_by_slug(part_dir, "emerging-architectures")
            if mod_dir is None:
                print(f"  SKIP {p['slug']}/{slug}: not found")
                continue

            old_num = re.match(r"module-(\d+)-", mod_dir.name)
            if not old_num:
                continue
            old_num = int(old_num.group(1))

            # Compute target module name. Use the TARGET slug (may differ from
            # current dir slug for the renamed chapters above).
            new_dir = part_dir / f"module-{new_num:02d}-{slug}"
            if mod_dir == new_dir:
                continue  # already at target

            # Apply move
            if new_dir.exists():
                print(f"  SKIP rename {mod_dir.name}: target {new_dir.name} exists")
                continue
            print(f"  git mv {mod_dir.name} -> {new_dir.name}")
            if not dry_run:
                subprocess.run(["git", "mv", str(mod_dir), str(new_dir)],
                                cwd=ROOT, check=False)
                renumber_count += 1

            # Update internal references
            target_dir = new_dir if not dry_run else mod_dir
            n = update_module_internal(target_dir, new_num, c["title"],
                                         c.get("subtitle"), dry_run)
            update_count += n

    print(f"\n{mode}: renumbered {renumber_count} module dirs; updated "
          f"internal refs in {update_count} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
