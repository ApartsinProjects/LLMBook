"""Check battery: run the audit, compare to the latest cycle snapshot, and
print regressions (new issue categories or counts going UP) so we catch
problems introduced by recent edits.

Usage:
  /c/Python314/python scripts/check_battery.py            # quick check, no save
  /c/Python314/python scripts/check_battery.py --save     # save as next cycle

Exit code 0 if no regressions; 1 if any check_id count INCREASED from prior cycle.
"""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAP_DIR = ROOT / "docs" / "content-audit" / "cycle_snapshots"


def run_audit_json() -> dict:
    runner = ROOT / "scripts" / "run_book_audit.py"
    result = subprocess.run(
        [sys.executable, str(runner), "--json"],
        capture_output=True, text=True, timeout=600,
    )
    stdout = result.stdout
    start = stdout.find("{")
    if start < 0:
        raise RuntimeError(f"Audit output had no JSON: {stdout[:500]}")
    return json.loads(stdout[start:])


def latest_snapshot() -> dict | None:
    snaps = sorted(SNAP_DIR.glob("cycle_*.json"))
    if not snaps:
        return None
    try:
        nums = [(int(p.stem.split("_")[1]), p) for p in snaps]
        nums.sort()
        return json.loads(nums[-1][1].read_text(encoding="utf-8"))
    except Exception:
        return None


def main():
    save = "--save" in sys.argv

    print("Running audit...")
    curr = run_audit_json()
    print(f"Current total: {curr['issue_count']} issues across {curr['file_count']} files")

    prev = latest_snapshot()
    if not prev:
        print("No prior snapshot to compare against.")
        if save:
            outfile = SNAP_DIR / "cycle_battery_initial.json"
            outfile.write_text(json.dumps(curr, indent=2), encoding="utf-8")
            print(f"Saved baseline to {outfile}")
        return 0

    print(f"Prior snapshot: {prev['issue_count']} issues")
    delta_total = curr["issue_count"] - prev["issue_count"]
    sign = "+" if delta_total > 0 else ""
    print(f"Total delta: {sign}{delta_total}")
    print()

    curr_by = Counter(i["check_id"] for i in curr["issues"])
    prev_by = Counter(i["check_id"] for i in prev["issues"])
    all_keys = set(curr_by) | set(prev_by)

    regressions = []
    improvements = []
    for k in all_keys:
        diff = curr_by[k] - prev_by[k]
        if diff > 0:
            regressions.append((diff, k))
        elif diff < 0:
            improvements.append((diff, k))

    regressions.sort(reverse=True)
    improvements.sort()

    if regressions:
        print(f"REGRESSIONS ({len(regressions)} check_ids with INCREASED counts):")
        for diff, k in regressions[:20]:
            print(f"  +{diff:4}  {k}")
    else:
        print("No regressions detected.")

    if improvements:
        print()
        print(f"Improvements ({len(improvements)} check_ids):")
        for diff, k in improvements[:10]:
            print(f"  {diff:4}  {k}")

    if save:
        # Find next cycle number
        existing = sorted(SNAP_DIR.glob("cycle_*.json"))
        nums = []
        for p in existing:
            try:
                nums.append(int(p.stem.split("_")[1]))
            except ValueError:
                pass
        nxt = max(nums) + 1 if nums else 1
        outfile = SNAP_DIR / f"cycle_{nxt:02d}.json"
        outfile.write_text(json.dumps(curr, indent=2), encoding="utf-8")
        print(f"\nSaved snapshot to {outfile.relative_to(ROOT)}")

    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
