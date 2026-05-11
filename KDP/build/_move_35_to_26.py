"""Step 2: Move misplaced agent-production sections from Module 35
('AI & Society') into Module 26 ('Agent Safety & Production').

Moves:
  35.5 Reliability Engineering for Agents       -> 26.8
  35.6 Observability/CI for Agent Workflows     -> 26.9
  35.8 Self-Improving Agents                    -> 26.10

Then rewrites all cross-references and updates section numbers in H1/H2/H3
and breadcrumbs inside the moved files.

Run from project root:
    /c/Python314/python KDP/build/_move_35_to_26.py
"""
from __future__ import annotations
import re
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

MOVES = [
    ("part-10-frontiers/module-35-ai-society/section-35.5.html",
     "part-6-agentic-ai/module-26-agent-safety-production/section-26.8.html",
     "35.5", "26.8"),
    ("part-10-frontiers/module-35-ai-society/section-35.6.html",
     "part-6-agentic-ai/module-26-agent-safety-production/section-26.9.html",
     "35.6", "26.9"),
    ("part-10-frontiers/module-35-ai-society/section-35.8.html",
     "part-6-agentic-ai/module-26-agent-safety-production/section-26.10.html",
     "35.8", "26.10"),
]

EXCLUDE_DIRS = {"_archive", "KDP", "node_modules", "vendor", "scripts"}


def renumber_inside(text: str, old_num: str, new_num: str) -> str:
    """Update section-number references inside the moved file's content
    (H1 prefix, breadcrumb, navigation labels). Conservative: only
    touch '35.5' as a standalone token, not parts of larger numbers."""
    # H1 / H2 leading number (e.g., "35.5 Reliability...")
    text = re.sub(rf'>{re.escape(old_num)}(\s+|&nbsp;)', f'>{new_num}\\1', text)
    # "Section 35.5" / "section-35.5" mentions in breadcrumbs
    text = re.sub(rf'\bSection {re.escape(old_num)}\b', f'Section {new_num}', text)
    text = re.sub(rf'(?<![\d.]){re.escape(old_num)}(?![\d.])', new_num, text)
    return text


def fix_relative_paths(text: str, src_path: str, dst_path: str) -> str:
    """When moving a file across modules, relative ../ paths to OTHER
    chapters need to be re-rooted. The simplest approach: rewrite all
    '../../module-XX-...' paths from the source chapter's perspective
    to the destination chapter's perspective.

    Both source and dest are at depth 3 (part-X/module-Y/section.html),
    so '../../module-Z/...' patterns resolve to the same canonical path
    'part-?/module-Z/...' if originating in the same part. When parts
    differ (35 in part-10, 26 in part-6), we must rewrite to be relative
    to the new location.

    Strategy: convert all '../...' URLs to absolute (root-relative) paths
    using the source's canonical resolution, then convert back to relative
    from dst.
    """
    src_parent = Path(src_path).parent
    dst_parent = Path(dst_path).parent

    def _rewrite(match: re.Match) -> str:
        attr = match.group(1)
        url = match.group(2)
        if url.startswith(("http://", "https://", "mailto:", "javascript:", "#", "data:")):
            return match.group(0)
        # Resolve href relative to source
        try:
            anchor = ""
            if "#" in url:
                url_clean, anchor = url.split("#", 1)
                anchor = "#" + anchor
            else:
                url_clean = url
            if not url_clean:
                return match.group(0)
            target = (src_parent / url_clean).resolve()
            # Make relative to destination
            try:
                rel_to_dst = Path(*target.parts[len((dst_parent.resolve()).parts):])
                # Use os.path.relpath via PurePosixPath
                import os
                new_rel = os.path.relpath(str(target), str(dst_parent.resolve())).replace("\\", "/")
                return f'{attr}="{new_rel}{anchor}"'
            except Exception:
                return match.group(0)
        except Exception:
            return match.group(0)

    return re.sub(r'(href|src)="([^"]+)"', _rewrite, text)


def main() -> int:
    moved = 0
    for src_rel, dst_rel, old_num, new_num in MOVES:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists():
            print(f"  [skip] source missing: {src_rel}")
            continue
        if dst.exists():
            print(f"  [skip] dest exists: {dst_rel}")
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        # Fix relative paths first (uses src position)
        text = fix_relative_paths(text, str(src), str(dst))
        # Renumber section labels
        text = renumber_inside(text, old_num, new_num)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        src.unlink()
        moved += 1
        print(f"  mv  {src_rel}\n   -> {dst_rel}")

    # Rewrite inbound links from elsewhere
    print("\nRewriting inbound cross-references...")
    n_files = 0
    n_links = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE_DIRS):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        for src_rel, dst_rel, _ , _ in MOVES:
            old_base = Path(src_rel).stem  # section-35.5
            new_base = Path(dst_rel).stem  # section-26.8
            old_dir = Path(src_rel).parent.name  # module-35-ai-society
            new_dir = Path(dst_rel).parent.name  # module-26-agent-safety-production
            old_part = Path(src_rel).parts[0]    # part-10-frontiers
            new_part = Path(dst_rel).parts[0]    # part-6-agentic-ai
            # Pattern 1: any path containing the old basename -> swap to new
            text = text.replace(f"{old_dir}/{old_base}.html", f"{new_dir}/{new_base}.html")
            text = text.replace(f"{old_part}/{old_dir}/{old_base}.html", f"{new_part}/{new_dir}/{new_base}.html")
            # Pattern 2: bare basename references
            text = re.sub(rf'\b{re.escape(old_base)}\.html', f'{new_base}.html', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1
            n_links += 1  # we don't count exactly here

    print(f"  Updated {n_files} files")
    print(f"\nMoved {moved} files into Module 26.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
