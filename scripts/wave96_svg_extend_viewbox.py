"""Wave 96: Extend SVG viewBox to fix SVG_TEXT_RIGHT_CLIP small overflows.

p1_svg_text_right_clip.py estimates how far text extends past the
viewBox's right edge. For small overflows (< 40 px), extending the
viewBox width by `overflow + 20` margin makes the text visible
without distorting the diagram. For large overflows (>= 40 px), the
SVG needs editorial redesign (text-anchor change, font-size reduction,
or rewording) so we skip those.

Operates on both inline SVG inside section HTML and external .svg files.
"""
import re
import sys
import json
import subprocess
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "node_modules", "KDP", "build", "source_fix_backups",
        "pagefind", ".book-update", "vendor", ".claude", "_archive",
        "agents", "templates", "docs", "scripts"}

THRESHOLD = 40.0  # px; only auto-fix small overflows


def get_audit_findings():
    """Run the audit and return per-file: {file: max_overflow_in_each_svg}."""
    runner = ROOT / "scripts" / "run_book_audit.py"
    result = subprocess.run(
        [sys.executable, str(runner), "--json"],
        capture_output=True, text=True, timeout=600,
    )
    out = result.stdout
    start = out.find("{")
    d = json.loads(out[start:])
    findings = defaultdict(list)
    for i in d["issues"]:
        if i["check_id"] != "SVG_TEXT_RIGHT_CLIP":
            continue
        f = i.get("file", "").replace("\\", "/")
        msg = i.get("message", "")
        m = re.search(r"extends ~([0-9.]+)px beyond viewBox width (\d+(?:\.\d+)?)",
                      msg)
        if not m:
            continue
        findings[f].append({
            "line": i.get("line", 0),
            "overflow": float(m.group(1)),
            "viewbox_w": float(m.group(2)),
        })
    return findings


def fix_svg_in_html(p: Path, hits: list) -> int:
    """Extend viewBox for each SVG with a fixable hit."""
    text = p.read_text(encoding="utf-8")
    # Group hits per viewBox width (each SVG has a unique viewBox in the
    # file; the audit reports the relevant width). Compute max overflow
    # per width.
    by_w = defaultdict(float)
    for h in hits:
        if h["overflow"] >= THRESHOLD:
            continue
        by_w[h["viewbox_w"]] = max(by_w[h["viewbox_w"]], h["overflow"])
    if not by_w:
        return 0
    n_changes = 0
    for old_w, max_overflow in by_w.items():
        new_w = int(old_w + max_overflow + 20)  # margin
        old_w_int = int(old_w)
        # Match viewBox="0 0 old_w h" patterns
        pattern = re.compile(
            rf'viewBox\s*=\s*"\s*(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+'
            rf'{old_w_int}(?:\.0+)?\s+(\d+(?:\.\d+)?)\s*"',
            re.IGNORECASE,
        )
        new_text, n = pattern.subn(
            lambda m: f'viewBox="{m.group(1)} {m.group(2)} {new_w} {m.group(3)}"',
            text,
        )
        # Also handle viewbox lowercase
        pattern_l = re.compile(
            rf'viewbox\s*=\s*"\s*(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+'
            rf'{old_w_int}(?:\.0+)?\s+(\d+(?:\.\d+)?)\s*"',
            re.IGNORECASE,
        )
        if n == 0:
            new_text, n = pattern_l.subn(
                lambda m: f'viewbox="{m.group(1)} {m.group(2)} {new_w} {m.group(3)}"',
                text,
            )
        if n > 0:
            text = new_text
            n_changes += n
    if n_changes == 0:
        return 0
    p.write_text(text, encoding="utf-8")
    return n_changes


def main():
    findings = get_audit_findings()
    print(f"Files with SVG_TEXT_RIGHT_CLIP findings: {len(findings)}")
    n_files = 0
    n_total = 0
    for f, hits in findings.items():
        p = ROOT / f
        if not p.exists():
            continue
        n = fix_svg_in_html(p, hits)
        if n:
            n_files += 1
            n_total += n
            print(f"  + {f}: {n} viewBox extension(s)")
    print(f"\nFiles touched: {n_files}, viewBox extensions: {n_total}")


if __name__ == "__main__":
    main()
