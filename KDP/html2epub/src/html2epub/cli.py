"""html2epub command-line interface."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from html2epub import __version__
from html2epub import builder, config as config_mod, validators


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="html2epub",
        description="Convert a directory of HTML files into a publishable EPUB 3.",
    )
    p.add_argument("--version", action="version", version=f"html2epub {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    bp = sub.add_parser("build", help="Build the EPUB")
    bp.add_argument("project_dir", nargs="?", default=".", help="Path to project dir (must contain html2epub.toml)")
    bp.add_argument("--validate-only", action="store_true", help="Validate config + assets but don't build")

    vp = sub.add_parser("validate", help="Validate an existing EPUB file")
    vp.add_argument("epub", help="Path to EPUB file")

    args = p.parse_args(argv)

    if args.cmd == "build":
        return _cmd_build(args)
    elif args.cmd == "validate":
        return _cmd_validate(args)
    return 1


def _cmd_build(args) -> int:
    project = Path(args.project_dir).resolve()
    cfg = config_mod.load(project)
    warns = validators.validate_pre(cfg)
    for w in warns:
        print(f"[warn] {w}")
    if args.validate_only:
        print("[ok] config + assets validate")
        return 0

    out = builder.build(cfg)
    report = validators.validate_post(out)
    print()
    print(f"[validate] chapters: {report['stats'].get('chapter_count', 0)}")
    for w in report["warnings"]:
        print(f"[validate-warn] {w}")
    for e in report["errors"]:
        print(f"[validate-err] {e}")
    return 0 if report["ok"] else 2


def _cmd_validate(args) -> int:
    report = validators.validate_post(Path(args.epub))
    print(f"chapters: {report['stats'].get('chapter_count', 0)}")
    for w in report["warnings"]:
        print(f"[warn] {w}")
    for e in report["errors"]:
        print(f"[err] {e}")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
