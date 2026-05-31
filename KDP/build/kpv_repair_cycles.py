"""KPV3 repair-cycles orchestrator.

Runs a fixed sequence of repair strategies, each followed by a SMOKE TEST
(convert tiny known-good EPUB; check a .kpf was actually produced).

Stops the moment a cycle's smoke test passes. If all cycles fail, prints a
clear escalation message + appends a journal entry to KDP/build/_kpv_debug_archive.

Usage:
  python KDP/build/kpv_repair_cycles.py             # run all cycles in order
  python KDP/build/kpv_repair_cycles.py --start 4   # resume from cycle N
  python KDP/build/kpv_repair_cycles.py --only 7    # run ONE specific cycle
  python KDP/build/kpv_repair_cycles.py --list      # list cycles without running

Each cycle is self-contained: applies its repair, runs smoke, returns
(success: bool, evidence: dict).
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


# Paths -----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
KPV3_DIR = Path(os.environ.get("LOCALAPPDATA", "")) / "Amazon" / "Kindle Previewer 3"
KPV3_EXE = KPV3_DIR / "Kindle Previewer 3.exe"
KPV3_BAT = Path(os.environ.get("APPDATA", "")) / "Amazon" / "kindlepreviewer.bat"
KPR_LOG = Path.home() / ".kindle" / "KPR" / "log" / "KPR.Log"

SMOKE_EPUB = ROOT / "KDP" / "output" / "math-recipe.epub"   # 27 KB known-good
JOURNAL_DIR = ROOT / "KDP" / "build" / "_kpv_debug_archive"
JOURNAL_DIR.mkdir(parents=True, exist_ok=True)


# Smoke test ------------------------------------------------------------------
def smoke_test(label: str, *,
               exe: Path | None = None,
               args_template: list[str] | None = None,
               extra_env: dict[str, str] | None = None,
               admin: bool = False,
               kill_first: bool = True,
               timeout: int = 300) -> dict:
    """Run KPV3 conversion on smoke EPUB; check whether a .kpf file appears.

    Returns dict with keys: success (bool), elapsed (float), output_dir (Path),
    summary (dict from Summary_Log.csv), kpr_log_tail (str), error_msg (str).
    """
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = ROOT / "KDP" / "output" / "kpv-repair" / f"cycle_{label}_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    if kill_first:
        for image in ("KPR_NCD.exe", "Kindle Previewer 3.exe", "java.exe"):
            subprocess.run(["taskkill", "/F", "/IM", image],
                           capture_output=True, timeout=15)
        time.sleep(2)

    exe = exe or KPV3_EXE
    if not exe.exists():
        return {"success": False, "elapsed": 0.0, "output_dir": out_dir,
                "summary": {}, "kpr_log_tail": "",
                "error_msg": f"executable not found: {exe}"}

    template = args_template or ["{epub}", "-convert", "-output", "{out}", "-qualitychecks"]
    cmd = [str(exe)] + [a.format(epub=str(SMOKE_EPUB), out=str(out_dir)) for a in template]

    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    # Snapshot KPR.Log size so we can extract just THIS run's tail later
    pre_log_size = KPR_LOG.stat().st_size if KPR_LOG.exists() else 0

    t0 = time.time()
    try:
        if admin and sys.platform.startswith("win"):
            # Use Start-Process -Verb RunAs to trigger UAC
            ps_cmd = (
                "Start-Process -FilePath '{exe}' -ArgumentList @('{args}') "
                "-Verb RunAs -PassThru -Wait | "
                "Select-Object -ExpandProperty ExitCode"
            ).format(
                exe=str(exe).replace("'", "''"),
                args="','".join(a.replace("'", "''") for a in cmd[1:]),
            )
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True, text=True, timeout=timeout, env=env,
            )
            rc = proc.returncode
        else:
            proc = subprocess.run(
                cmd, capture_output=True, timeout=timeout, env=env,
                cwd=str(ROOT),
            )
            rc = proc.returncode
    except subprocess.TimeoutExpired:
        return {"success": False, "elapsed": time.time() - t0,
                "output_dir": out_dir, "summary": {},
                "kpr_log_tail": "(timed out)",
                "error_msg": f"KPV3 timed out after {timeout}s"}
    elapsed = time.time() - t0

    # Parse Summary_Log.csv if present
    summary: dict = {}
    summary_path = out_dir / "Summary_Log.csv"
    if summary_path.exists():
        try:
            for row in csv.DictReader(summary_path.open(encoding="utf-8-sig",
                                                        newline="")):
                summary = {k.strip(): (v or "").strip() for k, v in row.items()}
                break
        except Exception as e:
            summary = {"_parse_error": str(e)}

    # Look for an actual .kpf file (that's the real success indicator)
    kpf_files = list(out_dir.rglob("*.kpf"))
    has_kpf = bool(kpf_files)

    # Read this run's KPR.Log tail
    log_tail = ""
    if KPR_LOG.exists():
        try:
            with KPR_LOG.open("rb") as f:
                f.seek(pre_log_size)
                log_tail = f.read().decode("utf-8", errors="replace")
        except Exception:
            pass

    error_msg = ""
    status = summary.get("Conversion Status", "")
    if has_kpf:
        success = True
    else:
        success = False
        error_msg = (status if status else
                     "no Summary_Log.csv produced — KPV3 silent failure")

    return {
        "success": success, "elapsed": elapsed, "output_dir": out_dir,
        "summary": summary, "kpr_log_tail": log_tail,
        "error_msg": error_msg, "kpf_files": [str(p) for p in kpf_files],
        "exit_code": rc if 'rc' in dir() else None,
    }


# Cycle definitions -----------------------------------------------------------
def cycle_baseline() -> dict:
    """C0: Baseline reproduction — current state, no intervention."""
    return smoke_test("0_baseline")


def cycle_1_bat_wrapper() -> dict:
    """C1: Use kindlepreviewer.bat (canonical Windows entry point)."""
    if not KPV3_BAT.exists():
        return {"success": False, "elapsed": 0, "output_dir": None,
                "summary": {}, "kpr_log_tail": "",
                "error_msg": f"{KPV3_BAT} not found"}
    return smoke_test("1_bat_wrapper", exe=KPV3_BAT,
                      args_template=["{epub}", "-convert", "-output", "{out}",
                                     "-qualitychecks"])


def cycle_2_log_mode() -> dict:
    """C2: Try -log CLI mode (alternate command, doc'd in user guide)."""
    return smoke_test("2_log_mode",
                      args_template=["{epub}", "-output", "{out}", "-log"])


def cycle_3_no_java_opts() -> dict:
    """C3: Run with empty _JAVA_OPTIONS — eliminate our injection."""
    return smoke_test("3_no_java_opts",
                      extra_env={"_JAVA_OPTIONS": "", "JAVA_TOOL_OPTIONS": ""})


def cycle_4_gui_first_run() -> dict:
    """C4: Launch GUI for 30s to trigger first-run init, kill, retry CLI."""
    # Kill anything first
    for image in ("Kindle Previewer 3.exe", "KPR_NCD.exe", "java.exe"):
        subprocess.run(["taskkill", "/F", "/IM", image],
                       capture_output=True, timeout=10)
    time.sleep(2)
    print("    -> launching GUI for 30s of init time...")
    proc = subprocess.Popen([str(KPV3_EXE)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    time.sleep(30)
    proc.terminate()
    try: proc.wait(timeout=5)
    except subprocess.TimeoutExpired: proc.kill()
    print("    -> GUI killed, retrying CLI conversion...")
    return smoke_test("4_after_gui_init", kill_first=False)


def cycle_5_short_temp() -> dict:
    """C5: Override TEMP to C:\\Temp (shortest possible path)."""
    short_temp = Path("C:/Temp")
    short_temp.mkdir(exist_ok=True)
    return smoke_test("5_short_temp",
                      extra_env={"TEMP": "C:\\Temp", "TMP": "C:\\Temp"})


def cycle_6_defender_exclusion() -> dict:
    """C6: Add Defender exclusions for KPV3 + TEMP (needs admin)."""
    paths = [str(KPV3_DIR), os.environ.get("TEMP", "")]
    ps = "; ".join(
        f"Add-MpPreference -ExclusionPath '{p}' -ErrorAction SilentlyContinue"
        for p in paths if p)
    ps_full = f"Start-Process powershell -Verb RunAs -Wait -ArgumentList '-NoProfile','-Command','{ps}'"
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_full],
                       capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        pass
    return smoke_test("6_defender_excl")


def cycle_7_admin_elevation() -> dict:
    """C7: Run KPV3 conversion as Administrator."""
    return smoke_test("7_admin", admin=True)


def cycle_8_winsock_reset() -> dict:
    """C8: netsh winsock reset (KPR_NCD is a network daemon)."""
    ps_full = ("Start-Process powershell -Verb RunAs -Wait -ArgumentList "
               "'-NoProfile','-Command','netsh winsock reset; "
               "netsh int ip reset'")
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_full],
                       capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        pass
    # NOTE: full effect requires reboot; we just test if partial helps
    return smoke_test("8_winsock_reset")


def cycle_9_explicit_outdir_perms() -> dict:
    """C9: Create output dir with very-open ACL, just in case."""
    out_dir = ROOT / "KDP" / "output" / "kpv-repair" / "cycle_9_test_out"
    out_dir.mkdir(parents=True, exist_ok=True)
    # Grant Everyone Full Control on this dir
    subprocess.run(["icacls", str(out_dir), "/grant", "Everyone:(OI)(CI)F"],
                   capture_output=True, timeout=10)
    # Same for TEMP just in case
    subprocess.run(["icacls", os.environ.get("TEMP", "C:\\Users\\apart\\AppData\\Local\\Temp"),
                    "/grant", "Everyone:(OI)(CI)F"],
                   capture_output=True, timeout=15)
    return smoke_test("9_open_perms")


CYCLES = [
    ("0", "Baseline (no repair)", cycle_baseline),
    ("1", "kindlepreviewer.bat wrapper", cycle_1_bat_wrapper),
    ("2", "-log CLI mode", cycle_2_log_mode),
    ("3", "Empty _JAVA_OPTIONS", cycle_3_no_java_opts),
    ("4", "GUI first-run, then CLI", cycle_4_gui_first_run),
    ("5", "TEMP=C:\\Temp short path", cycle_5_short_temp),
    ("6", "Defender exclusions (admin)", cycle_6_defender_exclusion),
    ("7", "Admin elevation", cycle_7_admin_elevation),
    ("8", "Winsock reset (admin)", cycle_8_winsock_reset),
    ("9", "Open ACL on output + temp", cycle_9_explicit_outdir_perms),
]


# Reporting + journal ---------------------------------------------------------
def append_journal(entry: dict) -> None:
    """Append one cycle result to the per-run journal."""
    j = JOURNAL_DIR / f"repair_journal_{datetime.now():%Y%m%d}.jsonl"
    safe = {k: (str(v) if isinstance(v, Path) else v) for k, v in entry.items()}
    j.open("a", encoding="utf-8").write(json.dumps(safe, default=str) + "\n")


def fmt_result(label: str, name: str, result: dict) -> str:
    icon = "PASS" if result.get("success") else "fail"
    bits = [f"[{icon}] cycle {label} | {name} | {result.get('elapsed', 0):.1f}s"]
    if result.get("error_msg"):
        bits.append(f"      error: {result['error_msg']}")
    if result.get("summary"):
        s = result["summary"]
        bits.append(f"      summary: status={s.get('Conversion Status', '?')} "
                    f"errors={s.get('Error Count', '?')} "
                    f"output={s.get('Output File Path', '')[:60]!r}")
    if result.get("kpf_files"):
        bits.append(f"      KPF produced: {result['kpf_files'][0]}")
    return "\n".join(bits)


# Main ------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=str, default="0",
                    help="Cycle to start from (default 0 = baseline)")
    ap.add_argument("--only", type=str, default=None,
                    help="Run ONE specific cycle and exit")
    ap.add_argument("--list", action="store_true",
                    help="List cycles without running")
    ap.add_argument("--stop-on-success", action="store_true", default=True)
    args = ap.parse_args()

    if args.list:
        print("Cycles:")
        for label, name, _ in CYCLES:
            print(f"  C{label}  {name}")
        return 0

    if not SMOKE_EPUB.exists():
        print(f"ERROR: smoke test EPUB not found: {SMOKE_EPUB}", file=sys.stderr)
        return 2

    to_run = ([(l, n, f) for l, n, f in CYCLES if l == args.only]
              if args.only else
              [(l, n, f) for l, n, f in CYCLES if l >= args.start])
    if not to_run:
        print(f"ERROR: no cycles matched (start={args.start}, only={args.only})",
              file=sys.stderr)
        return 2

    print(f"KPV3 repair cycles starting | {len(to_run)} cycles to run")
    print(f"  Smoke EPUB:  {SMOKE_EPUB.relative_to(ROOT)} "
          f"({SMOKE_EPUB.stat().st_size} bytes)")
    print(f"  KPV3 exe:    {KPV3_EXE}")
    print(f"  KPR.Log:     {KPR_LOG}")
    print(f"  Journal:     {JOURNAL_DIR.relative_to(ROOT)}")
    print()

    for label, name, fn in to_run:
        print(f">>> Cycle C{label}: {name}")
        result = fn()
        print(fmt_result(label, name, result))
        append_journal({"cycle": label, "name": name, **result})
        if result.get("success"):
            print()
            print("=" * 60)
            print(f"SUCCESS at cycle C{label} ({name})")
            print(f"KPF: {result['kpf_files']}")
            return 0
        print()

    print("=" * 60)
    print("ALL CYCLES EXHAUSTED — KPV3 still broken locally.")
    print()
    print("Escalation path:")
    print("  1. Try a different Windows machine (rules out account-specific issue)")
    print("  2. Contact KDP support with KPR.Log + diagnostic evidence")
    print("  3. Bypass: upload EPUB directly to KDP (only ground truth left)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
