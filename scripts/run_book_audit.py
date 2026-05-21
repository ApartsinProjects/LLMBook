"""Wrapper for `agents/book-skills/scripts/audit/run.py` that points it at
LLMBook root. The shared book-skills runner has BOOK_ROOT hard-coded to
LLMCourse for historical reasons.

Usage:
    /c/Python314/python scripts/run_book_audit.py
    /c/Python314/python scripts/run_book_audit.py --priority P0+P1
    /c/Python314/python scripts/run_book_audit.py --list
    /c/Python314/python scripts/run_book_audit.py --files section-82.1
    /c/Python314/python scripts/run_book_audit.py --json > docs/content-audit/plugin_audit.json
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "agents" / "book-skills" / "scripts" / "audit" / "run.py"

if not RUNNER.exists():
    print(f"ERROR: runner not found at {RUNNER}", file=sys.stderr)
    sys.exit(1)

cmd = [sys.executable, str(RUNNER), "--root", str(ROOT), *sys.argv[1:]]
sys.exit(subprocess.call(cmd))
