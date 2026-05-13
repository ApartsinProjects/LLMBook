"""Run EPUBCheck against the current EPUB and report fatals/errors/warns.

Uses the portable JRE + epubcheck.jar bundled under KDP/build/tools/.
Designed to slot into the QA pipeline alongside the v6xx detectors.

USAGE
    python run_epubcheck.py [path/to/file.epub]

If no path is given, validates the canonical output
KDP/output/building-conversational-ai-llms-agents.epub.

Exit codes: 0 = clean (0 fatals/errors). Warnings allowed.
"""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS = Path(__file__).resolve().parent / 'tools'
JAVA = TOOLS / 'jdk-21.0.11+10-jre' / 'bin' / 'java.exe'
JAR = TOOLS / 'epubcheck-5.2.1' / 'epubcheck.jar'

DEFAULT_EPUB = ROOT / 'KDP' / 'output' / 'building-conversational-ai-llms-agents.epub'


def main(argv: list[str]) -> int:
    epub = Path(argv[1]) if len(argv) > 1 else DEFAULT_EPUB
    if not epub.exists():
        print(f'ERROR: EPUB not found: {epub}', file=sys.stderr)
        return 2
    if not JAVA.exists():
        print(f'ERROR: bundled JRE missing: {JAVA}', file=sys.stderr)
        print('       Re-install KDP/build/tools/jdk-21.0.11+10-jre/', file=sys.stderr)
        return 2
    if not JAR.exists():
        print(f'ERROR: epubcheck.jar missing: {JAR}', file=sys.stderr)
        return 2
    print(f'EPUBCheck 5.2.1 validating {epub.relative_to(ROOT)}')
    proc = subprocess.run(
        [str(JAVA), '-jar', str(JAR), str(epub)],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        timeout=600)
    # EPUBCheck writes summary to stderr.
    combined = (proc.stdout or '') + (proc.stderr or '')
    # Parse the summary block:
    # Messages: 0 fatals / 0 errors / 0 warnings / 0 infos
    summary = re.search(
        r'Messages:\s*(\d+)\s*fatals?\s*/\s*(\d+)\s*errors?\s*/\s*(\d+)\s*warnings?\s*/\s*(\d+)\s*infos?',
        combined)
    if summary:
        fatals = int(summary.group(1))
        errors = int(summary.group(2))
        warns = int(summary.group(3))
        infos = int(summary.group(4))
        print(f'  Fatals:   {fatals}')
        print(f'  Errors:   {errors}')
        print(f'  Warnings: {warns}')
        print(f'  Infos:    {infos}')
        # Surface non-zero categories so the user can see them
        if fatals or errors or warns:
            print('\n--- EPUBCheck output ---')
            print(combined.strip())
        if fatals or errors:
            return 1
        return 0
    # Couldn't parse summary; fall back to exit code.
    print(combined)
    return proc.returncode


if __name__ == '__main__':
    sys.exit(main(sys.argv))
