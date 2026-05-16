"""Thin wrapper around epubcheck. Exits 0 on clean, nonzero otherwise.

Usage:
    python validate.py path/to/book.epub
    python validate.py path/to/book.epub --json   # machine-readable output

Defaults:
    epubcheck JAR: E:/Tools/epubcheck/epubcheck-5.1.0/epubcheck.jar
    java binary:   E:/Tools/epubcheck/jdk-17.0.19+10-jre/bin/java.exe

Override with MATH2EPUB_EPUBCHECK and MATH2EPUB_JAVA env vars.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_EPUBCHECK = Path("E:/Tools/epubcheck/epubcheck-5.1.0/epubcheck.jar")
DEFAULT_JAVA = Path("E:/Tools/epubcheck/jdk-17.0.19+10-jre/bin/java.exe")


def _resolve(env_var: str, default: Path) -> Path:
    override = os.environ.get(env_var)
    return Path(override) if override else default


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate an EPUB with epubcheck.")
    ap.add_argument("epub", help="Path to the .epub file")
    ap.add_argument("--json", action="store_true",
                    help="Pass --json to epubcheck (machine-readable output)")
    args = ap.parse_args()

    epub_path = Path(args.epub).resolve()
    if not epub_path.exists():
        print(f"error: epub not found: {epub_path}", file=sys.stderr)
        return 2

    jar = _resolve("MATH2EPUB_EPUBCHECK", DEFAULT_EPUBCHECK)
    java = _resolve("MATH2EPUB_JAVA", DEFAULT_JAVA)

    if not jar.exists():
        print(f"error: epubcheck jar not found: {jar}\n"
              f"Set MATH2EPUB_EPUBCHECK env var.", file=sys.stderr)
        return 2
    if not java.exists():
        print(f"error: java not found: {java}\n"
              f"Set MATH2EPUB_JAVA env var.", file=sys.stderr)
        return 2

    cmd = [str(java), "-jar", str(jar), str(epub_path)]
    if args.json:
        cmd.append("--json")
    print(f"running: {' '.join(cmd)}", file=sys.stderr)
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
