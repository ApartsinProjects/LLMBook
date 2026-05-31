"""Retry KPV3 KFX conversion until it produces a valid .kpf, then stop.

WHY THIS EXISTS:
  KPV3 3.104.0 has an intermittent failure on large EPUBs (37 MB / 607 chapters
  in our case). One attempt may succeed in ~3 minutes; the next four may fail
  with "Failed to ProcessEpub" + "Failed to create temp directory" without
  producing a KPF. The failure is content-independent: same EPUB, identical
  flags, the only variable is which attempt happens to win KPV3's internal race.

  Smoke testing with a 27 KB EPUB always succeeds. So KPV3 isn't broken — it
  has a flaky path on big-book conversion only.

  Strategy: retry until success or max attempts exhausted. Between attempts,
  fully clean state (kill all KPV3 processes, clean KPR support dirs, wait,
  re-launch GUI to re-prime OOBE).

USAGE:
  python KDP/build/kpv_retry_until_success.py                  # default 10 retries on canonical EPUB
  python KDP/build/kpv_retry_until_success.py path/to/foo.epub
  python KDP/build/kpv_retry_until_success.py --max 20         # up to 20 attempts
  python KDP/build/kpv_retry_until_success.py --no-clean       # don't wipe KPR support between attempts

OUTPUT:
  KDP/output/kpv-retry/<timestamp>/
    attempt_NN/                                  per-attempt run dir
    SUCCESS.md                                   if any attempt succeeds
    SUMMARY.json                                 attempt log + stats
"""
from __future__ import annotations
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KPV3_DIR = Path(os.environ.get("LOCALAPPDATA", "")) / "Amazon" / "Kindle Previewer 3"
KPV3_EXE = KPV3_DIR / "Kindle Previewer 3.exe"
KPR_SUPPORT_DIRS = [
    Path(os.environ.get("LOCALAPPDATA", "")) / "Amazon" / "KPR",
    Path.home() / ".kindle" / "KPR",
]
DEFAULT_EPUB = ROOT / "KDP" / "output" / "building-conversational-ai-llms-agents.epub"
OUTPUT_ROOT = ROOT / "KDP" / "output" / "kpv-retry"


def kill_everything_kpv() -> None:
    """Hard-kill every KPV3-related process. No survivors."""
    for img in ("Kindle Previewer 3.exe", "KPR_NCD.exe",
                "java.exe", "kindlegen.exe", "javaw.exe"):
        subprocess.run(["taskkill", "/F", "/IM", img],
                       capture_output=True, timeout=15)
    time.sleep(3)


def clean_kpr_support() -> int:
    """Wipe per-user KPR support dirs (returns count wiped). NOT the install dir."""
    n = 0
    for d in KPR_SUPPORT_DIRS:
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
            n += 1
    return n


def relaunch_gui_to_prime() -> bool:
    """Launch GUI for 10s to re-create OOBE state, then kill it."""
    subprocess.Popen([str(KPV3_EXE)],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
    time.sleep(10)
    # Kill the GUI before running CLI — empirically CLI needs GUI dead OR alive,
    # but the OOBE state created by GUI launch persists after GUI dies.
    kill_everything_kpv()
    return True


def build_java_opts(run_dir: Path) -> str:
    rd = run_dir.as_posix()
    return " ".join([
        "-XX:+UnlockDiagnosticVMOptions", "-XX:+CreateMinidumpOnCrash",
        f"-XX:ErrorFile={rd}/error_pid_%p.log",
        f"-XX:HeapDumpPath={rd}/heap.hprof",
        "-XX:+HeapDumpOnOutOfMemoryError",
        "-XX:+UseG1GC", "-XX:MaxGCPauseMillis=200",
        "-XX:+ParallelRefProcEnabled",
        "-XX:-OmitStackTraceInFastThrow",
        "-Xss4m", "-Xmx4g",
    ])


def one_attempt(epub: Path, attempt: int, base_dir: Path,
                clean_between: bool, timeout: int) -> dict:
    """One KPV3 conversion attempt. Returns dict with success/kpf/timing."""
    print(f"\n>>> Attempt {attempt}")

    # Phase A: clean slate
    kill_everything_kpv()
    if clean_between:
        n = clean_kpr_support()
        print(f"    cleaned {n} KPR support dir(s)")

    # Phase B: prime OOBE
    relaunch_gui_to_prime()
    print(f"    primed OOBE state via GUI launch+kill")

    # Phase C: run CLI
    run_dir = base_dir / f"attempt_{attempt:02d}"
    run_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["_JAVA_OPTIONS"] = build_java_opts(run_dir)

    cmd = [str(KPV3_EXE), str(epub),
           "-convert", "-locale", "en",
           "-output", str(run_dir),
           "-qualitychecks"]
    print(f"    CLI: {KPV3_EXE.name} ... -convert -output {run_dir.name}")

    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout,
                              env=env, cwd=str(ROOT))
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        rc = -1
    elapsed = time.time() - t0

    # Phase D: verify (success = .kpf file actually produced)
    kpfs = list(run_dir.rglob("*.kpf"))
    summary = {}
    sp = run_dir / "Summary_Log.csv"
    if sp.exists():
        try:
            for row in csv.DictReader(sp.open(encoding="utf-8-sig", newline="")):
                summary = {k.strip(): (v or "").strip() for k, v in row.items()}
                break
        except Exception:
            pass

    status_str = summary.get("Conversion Status", "?")
    success = bool(kpfs) and status_str.lower() == "success"

    print(f"    elapsed: {elapsed:.1f}s  rc={rc}  status={status_str}  KPFs={len(kpfs)}  "
          f"{'✅ SUCCESS' if success else '❌ fail'}")

    return {
        "attempt": attempt,
        "elapsed": elapsed, "exit_code": rc,
        "summary": summary,
        "kpf_files": [str(p) for p in kpfs],
        "kpf_sizes": [Path(p).stat().st_size for p in kpfs],
        "success": success,
        "run_dir": str(run_dir),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", nargs="?", type=Path, default=DEFAULT_EPUB)
    ap.add_argument("--max", type=int, default=10,
                    help="Max attempts (default 10)")
    ap.add_argument("--no-clean", action="store_true",
                    help="Don't wipe KPR support dirs between attempts")
    ap.add_argument("--timeout", type=int, default=600,
                    help="Per-attempt timeout in seconds (default 600 = 10 min)")
    args = ap.parse_args()
    args.epub = args.epub.resolve()
    if not args.epub.exists():
        print(f"ERROR: EPUB not found: {args.epub}", file=sys.stderr)
        return 2

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = OUTPUT_ROOT / run_id
    base.mkdir(parents=True, exist_ok=True)

    print(f"KPV3 retry-until-success: {run_id}")
    print(f"  EPUB:       {args.epub}  ({args.epub.stat().st_size / 1024 / 1024:.2f} MB)")
    print(f"  Max retry:  {args.max}")
    print(f"  Per-attempt timeout: {args.timeout}s")
    print(f"  Clean KPR between: {not args.no_clean}")
    print(f"  Output:     {base.relative_to(ROOT)}")

    attempts: list[dict] = []
    success = None
    t_start = time.time()
    for n in range(1, args.max + 1):
        result = one_attempt(args.epub, n, base, not args.no_clean, args.timeout)
        attempts.append(result)
        # persist after every attempt so we don't lose progress on crash
        (base / "SUMMARY.json").write_text(
            json.dumps({"started": run_id,
                        "epub": str(args.epub),
                        "elapsed_total": time.time() - t_start,
                        "attempts": attempts}, indent=2, default=str),
            encoding="utf-8")
        if result["success"]:
            success = result
            break

    total = time.time() - t_start
    print()
    print("=" * 60)
    if success:
        kpf = success["kpf_files"][0]
        sz = success["kpf_sizes"][0]
        print(f"✅ SUCCESS on attempt #{success['attempt']} ({len(attempts)} total tries, "
              f"{total:.0f}s wall)")
        print(f"   KPF: {kpf}  ({sz:,} bytes)")
        # Write SUCCESS.md
        ok_md = base / "SUCCESS.md"
        timings = ", ".join(f"{a['elapsed']:.0f}s" for a in attempts)
        ok_md.write_text(
            f"# KPV3 conversion succeeded\n\n"
            f"- Run id: {run_id}\n"
            f"- EPUB: `{args.epub}`\n"
            f"- Successful attempt: **#{success['attempt']}** of {args.max} allowed\n"
            f"- Total wall time: {total:.0f}s ({total / 60:.1f} min)\n"
            f"- KPF: `{kpf}` ({sz:,} bytes)\n"
            f"- Per-attempt elapsed: [{timings}]\n",
            encoding="utf-8")
        print(f"   Report: {ok_md.relative_to(ROOT)}")
        return 0
    else:
        print(f"❌ All {args.max} attempts exhausted, no KPF produced ({total:.0f}s wall)")
        print(f"   See: {base.relative_to(ROOT)}/SUMMARY.json")
        return 1


if __name__ == "__main__":
    sys.exit(main())
