"""Produce a unique-named copy of the final EPUB for KDP upload.

Why a unique name on every upload?
  KDP's upload pipeline appears to cache by filename / content hash. When the
  same file path is uploaded twice in a row, it can short-circuit and return
  the prior (cached) rejection without actually re-running the converter.
  A fresh filename + fresh content-hash forces a full re-conversion server
  side, which both:
    (a) cache-busts spurious rejections, and
    (b) gives us a clean trail of which file got which verdict.

Naming pattern:
  building-conversational-ai-llms-agents-<YYYYMMDD>-<HHMMSS>-<git_short_sha>-<size_mb>MB.epub

  Example:  building-conversational-ai-llms-agents-20260530-153012-d9cebaa-37MB.epub

Pieces:
  - YYYYMMDD-HHMMSS  monotonic, lexicographically sortable
  - git short SHA    ties this file to the source commit (lets us re-build it)
  - size MB          visual sanity check at a glance (caught a 0-byte build once)

Canonical EPUB is left UNTOUCHED. Copy lands in KDP/output/uploads/.

Usage:
  python KDP/build/make_upload_copy.py                  # auto-discovers canonical
  python KDP/build/make_upload_copy.py path/to/foo.epub # explicit source
  python KDP/build/make_upload_copy.py --quiet          # only print final path

Returns 0 on success, 1 if the source EPUB is missing.
"""
from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


CANONICAL_EPUB = Path("KDP/output/building-conversational-ai-llms-agents.epub")
UPLOAD_DIR = Path("KDP/output/uploads")


def git_short_sha() -> str:
    """Return current HEAD short SHA, or 'nogit' if not a repo."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0:
            return out.stdout.strip() or "nogit"
    except Exception:
        pass
    return "nogit"


def working_tree_dirty() -> bool:
    """True if there are uncommitted changes. Adds a 'dirty' marker so we
    don't pretend a hand-tweaked build matches a clean commit."""
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=5,
        )
        return bool(out.stdout.strip())
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", nargs="?", type=Path, default=CANONICAL_EPUB,
                    help="Source EPUB (default: canonical KDP output)")
    ap.add_argument("--out-dir", type=Path, default=UPLOAD_DIR,
                    help="Destination directory (default: KDP/output/uploads)")
    ap.add_argument("--quiet", action="store_true",
                    help="Only print the final filename (good for shell capture)")
    args = ap.parse_args()

    src: Path = args.source
    if not src.exists():
        print(f"ERROR: source EPUB not found: {src}", file=sys.stderr)
        return 1

    size_bytes = src.stat().st_size
    size_mb = size_bytes // (1024 * 1024)
    sha = git_short_sha()
    if working_tree_dirty():
        sha = f"{sha}-dirty"
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")

    stem = src.stem  # building-conversational-ai-llms-agents
    new_name = f"{stem}-{ts}-{sha}-{size_mb}MB.epub"

    args.out_dir.mkdir(parents=True, exist_ok=True)
    dest = args.out_dir / new_name
    shutil.copy2(src, dest)

    if args.quiet:
        print(dest)
    else:
        print("Upload-ready EPUB:")
        print(f"  source : {src}  ({size_bytes / 1024 / 1024:.2f} MB)")
        print(f"  dest   : {dest}")
        print(f"  ts     : {ts}")
        print(f"  commit : {sha}")
        print()
        print("Drag this NEW file into KDP. The unique filename forces KDP")
        print("to re-run the converter rather than returning a cached verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
