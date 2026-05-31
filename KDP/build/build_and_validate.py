"""Master build + validate orchestrator for a KDP-acceptable EPUB.

Run from any book project root that follows the html2epub layout:
    <project>/
      html2epub.toml
      styles/book.css
      part-N-*/module-MM-*/section-N.M.html
      KDP/build/publish.py
      KDP/build/fonts/*.ttf
      KDP/build/epub_overrides.css
      KDP/output/

Usage:
    python build_and_validate.py [--no-kfx] [--no-audit] [--quick]

Stages:
    1. Pre-flight audit  (book-skills P0+P1 plugins)
    2. Auto-fix          (idempotent source-level scrubbers)
    3. Build             (publish.py: html2epub + post-build patches)
    4. KFX Stage 2 verify (kpv_direct_jar.py)
    5. Summary report

Exits non-zero only if any P0 audit issue remains unfixed after auto-fix,
or if publish.py fails. KFX residuals are reported but non-fatal (KDP
server-side conversion is authoritative).
"""
from __future__ import annotations
import argparse
import subprocess
import sys
import time
from pathlib import Path


def find_project_root() -> Path:
    """Locate the book project root (the dir containing html2epub.toml)."""
    cur = Path.cwd().resolve()
    while cur != cur.parent:
        if (cur / "html2epub.toml").exists():
            return cur
        cur = cur.parent
    raise SystemExit("ERROR: no html2epub.toml found in cwd or any parent")


def run(label: str, cmd: list[str], cwd: Path, fatal: bool = True) -> int:
    """Run a subprocess, stream output, return exit code."""
    print(f"\n=== {label} ===")
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=str(cwd))
    dt = time.time() - t0
    print(f"  ({label} done in {dt:.1f}s, exit={proc.returncode})")
    if proc.returncode != 0 and fatal:
        raise SystemExit(f"ERROR: {label} failed (exit {proc.returncode})")
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-audit", action="store_true", help="skip the pre-flight book-skills audit")
    ap.add_argument("--no-autofix", action="store_true", help="skip the auto-fix scrubbers")
    ap.add_argument("--no-kfx", action="store_true", help="skip the local KFX direct-jar verify")
    ap.add_argument("--quick", action="store_true", help="pass --quick to publish.py")
    args = ap.parse_args()

    root = find_project_root()
    print(f"Project root: {root}")
    py = sys.executable
    build = root / "KDP" / "build"

    # Stage 1: pre-flight audit
    if not args.no_audit:
        audit = root / "agents" / "book-skills" / "scripts" / "audit" / "run.py"
        if not audit.exists():
            # Try via -m
            run("Pre-flight audit (P0+P1)",
                [py, "-m", "agents.book-skills.scripts.audit.run",
                 "--priority", "P0+P1", "--root", str(root)],
                root, fatal=False)
        else:
            run("Pre-flight audit (P0+P1)",
                [py, str(audit), "--priority", "P0+P1", "--root", str(root)],
                root, fatal=False)

    # Stage 2: auto-fix idempotent scrubbers
    if not args.no_autofix:
        # Each script is a no-op if source is already clean
        scrubbers = [
            ("svg-inline-style-fonts",  "fix_svg_inline_style_fonts.py"),
            ("caption-letter-prefix",   "fix_caption_letter_prefix.py"),
            ("caption-list-residue",    "fix_caption_numbered_list_residue.py"),
            ("long-callout-titles",     "fix_long_callout_titles.py"),
            ("callout-subtitle-split",  "fix_callout_subtitle_split.py"),
            ("bare-dollar-math",        "fix_bare_dollar_math.py"),
        ]
        for label, script in scrubbers:
            p = build / script
            if p.exists():
                run(f"auto-fix: {label}", [py, str(p)], root, fatal=False)

    # Stage 3: build
    cmd = [py, str(build / "publish.py")]
    if args.quick:
        cmd.append("--quick")
    run("Build EPUB (publish.py)", cmd, root)

    # Locate the built EPUB
    out = root / "KDP" / "output"
    epubs = sorted(out.glob("*.epub"))
    epubs = [e for e in epubs if not any(x in e.name.lower() for x in ("raw", "pre-", "light", "reflowable", "_v"))]
    if not epubs:
        print("ERROR: no EPUB found in KDP/output/", file=sys.stderr)
        return 1
    epub = epubs[0]
    print(f"\nEPUB: {epub} ({epub.stat().st_size / 1024 / 1024:.1f} MB)")

    # Stage 4: KFX Stage 2 verify
    if not args.no_kfx:
        kpv = build / "kpv_direct_jar.py"
        if kpv.exists():
            run("KFX Stage 2 verify",
                [py, str(kpv), str(epub), "--stages", "2", "--timeout", "1500"],
                root, fatal=False)
            # Find latest run and summarize errors/warnings
            kpv_runs = sorted((out / "kpv-direct").glob("*/"), reverse=True)
            if kpv_runs:
                latest = kpv_runs[0]
                stderr = latest / "stage_logs" / "2_epub_adapter.stderr.txt"
                if stderr.exists():
                    import re
                    text = stderr.read_text(encoding="utf-8", errors="replace")
                    errors = {}
                    warnings = {}
                    for line in text.splitlines():
                        m = re.search(r"\b(E\d{5})\b", line)
                        if m:
                            errors[m.group(1)] = errors.get(m.group(1), 0) + 1
                        m = re.search(r"\b(W\d{5})\b", line)
                        if m:
                            warnings[m.group(1)] = warnings.get(m.group(1), 0) + 1
                    print(f"\n=== KFX Stage 2 result ===")
                    print(f"Errors:")
                    for k, v in sorted(errors.items()):
                        print(f"  {v:4d}  {k}")
                    print(f"Warnings (top 5):")
                    for k, v in sorted(warnings.items(), key=lambda x: -x[1])[:5]:
                        print(f"  {v:4d}  {k}")

    print("\n=== Summary ===")
    print(f"EPUB ready at: {epub}")
    print(f"Size: {epub.stat().st_size / 1024 / 1024:.1f} MB")
    print(f"Next: upload to KDP at https://kdp.amazon.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
