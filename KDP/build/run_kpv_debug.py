"""Run Kindle Previewer 3 with MAXIMUM JVM diagnostics enabled.

Why: KPV3's converter (com.amazon.kcfpositionmapcreator) crashes in jvm.dll
itself (EXCEPTION_ACCESS_VIOLATION, generic frame). The default crash dumps
under KPV3/lib/fc/hs_err_pid*.log are only ~592 bytes (truncated) and don't
identify the last class loaded, the last JNI call, or the heap state.

This script injects JVM flags via the _JAVA_OPTIONS environment variable,
which KPV3's child java.exe inherits automatically. The flags:

  -XX:+UnlockDiagnosticVMOptions      gate-opener for the next two
  -XX:+CreateMinidumpOnCrash          Windows .dmp on crash (WinDbg-loadable)
  -XX:+LogVMOutput                    write VM-internal log
  -XX:LogFile=<path>                  ...to a known location
  -XX:ErrorFile=<path>                hs_err_pid*.log to a known location
  -XX:HeapDumpPath=<path>             heap dump destination
  -XX:+HeapDumpOnOutOfMemoryError     dump heap if OOM (likely cause for big books)
  -verbose:class                      log every class loaded (-> last-class-before-crash)
  -verbose:jni                        log JNI bridge calls (crash is in jvm.dll, possibly JNI-side)
  -verbose:gc                         GC events (detect GC-related stalls)
  -XX:-OmitStackTraceInFastThrow      always show full stack traces (Java optimizes some away)
  -Xss4m                              4 MB stack vs default ~512 KB (handles deep recursion)
  -Xmx4g                              4 GB heap vs default ~256 MB (handles big position maps)

We also clean stale hs_err_pid*.log dumps BEFORE the run so any new ones are
unambiguously from this attempt, and parse the NEW dumps after.

Usage:
  python KDP/build/run_kpv_debug.py [path/to/file.epub]
  python KDP/build/run_kpv_debug.py --timeout 1200

Output:
  KDP/output/kpv-debug/<run-timestamp>/
    stdout.txt         KPV3 stdout
    stderr.txt         KPV3 stderr
    jvm.log            VM-internal log
    error.log          JVM crash log (if it crashed)
    minidump.dmp       Windows minidump (if it crashed; load in WinDbg)
    heap.hprof         heap dump (if OOM)
    NEW_CRASHES/       any new hs_err_pid*.log files from KPV3's lib/fc/
    Summary_Log.csv    KPV's own report (if it got that far)
    KPF/...            converted KFX (if conversion succeeded)
    Logs/...           KPV qualitychecks output (if it got that far)
    DEBUG_REPORT.md    auto-generated triage report
"""
from __future__ import annotations
import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_EPUB = PROJECT_ROOT / "KDP" / "output" / "building-conversational-ai-llms-agents.epub"
DEBUG_OUTPUT_ROOT = PROJECT_ROOT / "KDP" / "output" / "kpv-debug"

# KPV3 installation paths (Windows)
LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", ""))
KPV3_ROOT = LOCALAPPDATA / "Amazon" / "Kindle Previewer 3"
KPV3_EXE = KPV3_ROOT / "Kindle Previewer 3.exe"
KPV3_FC = KPV3_ROOT / "lib" / "fc"
KPV3_JAVA = KPV3_FC / "jre" / "bin" / "java.exe"


def find_kpv() -> Path | None:
    """Locate the KPV3 executable."""
    candidates = [
        KPV3_EXE,
        Path("C:/Program Files/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe"),
        Path("C:/Program Files (x86)/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe"),
    ]
    for c in candidates:
        if c.exists():
            return c
    env = os.environ.get("KINDLE_PREVIEWER")
    if env and Path(env).exists():
        return Path(env)
    return None


def snapshot_crash_dir() -> set[str]:
    """Return set of hs_err_pid*.log filenames currently present.
    Used to identify NEW crash dumps created during our run."""
    if not KPV3_FC.exists():
        return set()
    return {p.name for p in KPV3_FC.glob("hs_err_pid*.log")}


def kill_stale_kpv_processes() -> None:
    """KPV3 is single-instance; any stale GUI or worker hangs new -convert calls."""
    if sys.platform.startswith("win"):
        for image in ("KPR_NCD.exe", "Kindle Previewer 3.exe"):
            try:
                subprocess.run(
                    ["taskkill", "/F", "/IM", image],
                    capture_output=True, timeout=10,
                )
            except Exception:
                pass
        time.sleep(2)


def build_java_options(run_dir: Path, gc: str = "g1") -> str:
    """Compose the _JAVA_OPTIONS string that the KPV3 child JVM will inherit.

    Args:
        run_dir: per-run dir for log files
        gc: GC algorithm: 'g1' (default, robust), 'parallel' (KPV stock; crashes),
            'serial' (slowest but most stable), 'cms' (Java 8 legacy concurrent).

    Why g1 as default:
        Run 20260530-142400 confirmed KPV3 stock JVM dies in ParallelGC's
        Full GC code when the old gen saturates (ParOldGen 99% full -> Full GC
        triggers -> EXCEPTION_ACCESS_VIOLATION in jvm.dll GCTaskThread).
        G1GC manages the heap as regions instead of monolithic young/old gens,
        so the Full-GC-on-saturated-old-gen failure mode doesn't exist for it.
    """
    rd = run_dir.as_posix()
    gc_flags = {
        "g1":       ["-XX:+UseG1GC", "-XX:MaxGCPauseMillis=200",
                     "-XX:+ParallelRefProcEnabled"],
        "parallel": ["-XX:+UseParallelGC"],   # KPV3 default; reproduces the bug
        "serial":   ["-XX:+UseSerialGC"],     # slow but rock-solid
        "cms":      ["-XX:+UseConcMarkSweepGC"],  # legacy Java 8 concurrent
    }.get(gc, ["-XX:+UseG1GC"])

    opts = [
        "-XX:+UnlockDiagnosticVMOptions",
        "-XX:+CreateMinidumpOnCrash",
        "-XX:+LogVMOutput",
        f"-XX:LogFile={rd}/jvm.log",
        f"-XX:ErrorFile={rd}/error_pid_%p.log",
        f"-XX:HeapDumpPath={rd}/heap.hprof",
        "-XX:+HeapDumpOnOutOfMemoryError",
        # GC choice
        *gc_flags,
        # Trace + verbose (verbose:class spams jvm.log but pinpoints last-thing-before-crash)
        "-verbose:class",
        "-verbose:jni",
        "-verbose:gc",
        "-XX:+PrintGCDetails",
        "-XX:+PrintGCDateStamps",
        "-XX:-OmitStackTraceInFastThrow",
        # Sizing: a large book builds millions of position-map nodes
        "-Xss4m",
        "-Xmx4g",
    ]
    return " ".join(opts)


def collect_new_crashes(before: set[str], dest: Path) -> list[Path]:
    """Copy any NEW hs_err_pid*.log files from KPV3's lib/fc/ into dest."""
    if not KPV3_FC.exists():
        return []
    new_files = []
    for p in KPV3_FC.glob("hs_err_pid*.log"):
        if p.name not in before:
            dest.mkdir(parents=True, exist_ok=True)
            target = dest / p.name
            try:
                shutil.copy2(p, target)
                new_files.append(target)
            except Exception:
                pass
    return new_files


def summarize_crash_log(log_path: Path) -> dict:
    """Extract key fields from a hs_err_pid*.log file."""
    info = {
        "path": str(log_path),
        "size": log_path.stat().st_size,
        "exception": "",
        "frame": "",
        "jre": "",
        "java_thread": "",
        "java_command": "",
        "top_java_frames": [],
        "last_classes_loaded": [],
        "exceptions_thrown": [],
    }
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return info

    m = re.search(r"EXCEPTION[^\n]+", text)
    if m: info["exception"] = m.group(0).strip()
    m = re.search(r"Problematic frame:\s*\n#\s*(.+)", text)
    if m: info["frame"] = m.group(1).strip()
    m = re.search(r"JRE version:\s*(.+)", text)
    if m: info["jre"] = m.group(1).strip()
    m = re.search(r"Current thread.*", text)
    if m: info["java_thread"] = m.group(0)[:200]
    m = re.search(r"java_command:\s*(.+)", text)
    if m: info["java_command"] = m.group(1)[:200]
    # Top Java/JNI frames in stack
    for m in re.finditer(r"^[Jj]\s+\d+.*com\.amazon\.[\w.]+\.[\w$]+\([^)]*\)", text, re.MULTILINE):
        info["top_java_frames"].append(m.group(0).strip()[:200])
        if len(info["top_java_frames"]) >= 5:
            break
    # Last events (loading class X, throwing exception Y)
    for m in re.finditer(r"Event:\s+[\d.]+\s+loading class\s+([\w/$]+)", text):
        info["last_classes_loaded"].append(m.group(1))
    info["last_classes_loaded"] = info["last_classes_loaded"][-10:]
    for m in re.finditer(r"Event:\s+[\d.]+.*Exception <([^>]+)>", text):
        info["exceptions_thrown"].append(m.group(1)[:120])
    info["exceptions_thrown"] = info["exceptions_thrown"][-5:]
    return info


def parse_summary_log(summary: Path) -> dict:
    """Parse KPV's Summary_Log.csv into the headline result."""
    result = {"present": False}
    if not summary.exists():
        return result
    result["present"] = True
    try:
        for row in csv.DictReader(summary.open(encoding="utf-8-sig", newline="")):
            result.update({
                "status": row.get("Conversion Status", "?"),
                "errors": row.get("Error Count", "?"),
                "quality_issues": row.get("Quality Issue Count", "?"),
                "enhanced_typesetting": row.get("Enhanced Typesetting Status", "?"),
                "output_path": (row.get("Output File Path") or "").strip(),
                "quality_path": (row.get("Quality Report Path") or "").strip(),
            })
            break
    except Exception as e:
        result["parse_error"] = str(e)
    return result


def write_report(run_dir: Path, *, epub: Path, elapsed: float, returncode: int,
                 timed_out: bool, new_crashes: list[Path], summary: dict,
                 jvm_log_size: int, stdout_size: int, stderr_size: int) -> Path:
    """Write a triage-friendly DEBUG_REPORT.md inside run_dir."""
    report = run_dir / "DEBUG_REPORT.md"
    lines = []
    lines.append(f"# KPV3 Debug Run Report\n")
    lines.append(f"- Run dir: `{run_dir.relative_to(PROJECT_ROOT)}`")
    lines.append(f"- EPUB: `{epub}` ({epub.stat().st_size / 1024 / 1024:.2f} MB)")
    lines.append(f"- Elapsed: {elapsed:.1f}s")
    lines.append(f"- KPV exit code: {returncode}  {'(TIMED OUT)' if timed_out else ''}")
    lines.append(f"- jvm.log: {jvm_log_size:,} bytes")
    lines.append(f"- stdout.txt: {stdout_size:,} bytes")
    lines.append(f"- stderr.txt: {stderr_size:,} bytes")
    lines.append("")

    # Summary
    lines.append("## KPV Summary_Log.csv\n")
    if summary.get("present"):
        for k in ("status", "errors", "quality_issues", "enhanced_typesetting",
                  "output_path", "quality_path"):
            lines.append(f"- **{k}**: `{summary.get(k, '?')}`")
    else:
        lines.append("- *Not produced. Converter never reached the report-writing stage.*")
    lines.append("")

    # Crashes
    lines.append(f"## New JVM crash dumps: {len(new_crashes)}\n")
    if not new_crashes:
        lines.append("*No new hs_err_pid*.log files were created during this run.*\n")
    for c in new_crashes:
        info = summarize_crash_log(c)
        lines.append(f"### {c.name}\n")
        lines.append(f"- Size: {info['size']:,} bytes")
        lines.append(f"- Exception: `{info['exception']}`")
        lines.append(f"- Problematic frame: `{info['frame']}`")
        lines.append(f"- JRE: `{info['jre']}`")
        if info["java_command"]:
            lines.append(f"- java_command: `{info['java_command']}`")
        if info["top_java_frames"]:
            lines.append("- Top Java frames:")
            for f in info["top_java_frames"]:
                lines.append(f"  - `{f}`")
        if info["last_classes_loaded"]:
            lines.append("- Last classes loaded:")
            for c2 in info["last_classes_loaded"]:
                lines.append(f"  - `{c2}`")
        if info["exceptions_thrown"]:
            lines.append("- Recent exceptions thrown:")
            for e in info["exceptions_thrown"]:
                lines.append(f"  - `{e}`")
        lines.append("")

    # Files to inspect manually
    lines.append("## Manual deep-dive\n")
    lines.append("If `minidump.dmp` exists, load it in WinDbg with the KPV3 symbols path")
    lines.append(f"(`{KPV3_FC}\\\\jre\\\\bin`) to see the native stack at crash time.\n")
    lines.append(f"`jvm.log` contains the VM-internal log (heap, JIT compiles, safepoints).\n")
    lines.append(f"`stderr.txt` contains the verbose:class / verbose:jni stream; search for")
    lines.append(f"the LAST `Loaded ...` line to identify what was being processed at the crash.\n")

    report.write_text("\n".join(lines), encoding="utf-8")
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", nargs="?", type=Path, default=CANONICAL_EPUB)
    ap.add_argument("--timeout", type=int, default=2400,
                    help="KPV3 timeout in seconds (default 2400 = 40 min)")
    ap.add_argument("--no-kill", action="store_true",
                    help="Don't kill stale KPV3 processes before launching")
    ap.add_argument("--gc", default="g1", choices=["g1", "parallel", "serial", "cms"],
                    help="JVM GC algorithm (default g1; parallel reproduces the stock crash)")
    args = ap.parse_args()

    if not args.epub.exists():
        print(f"ERROR: EPUB not found: {args.epub}", file=sys.stderr)
        return 1
    kpv = find_kpv()
    if kpv is None:
        print("ERROR: Kindle Previewer 3 not detected.", file=sys.stderr)
        print("       Install from https://kdp.amazon.com/en_US/help/topic/G202131170",
              file=sys.stderr)
        return 1

    # Per-run subdir so multiple debug runs stay separated
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = DEBUG_OUTPUT_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"KPV3 debug run: {run_id}")
    print(f"  EPUB:     {args.epub}")
    print(f"  Run dir:  {run_dir.relative_to(PROJECT_ROOT)}")
    print(f"  KPV3:     {kpv}")
    print(f"  Java:     {KPV3_JAVA}")
    print()

    # Snapshot existing crash dumps so we can identify NEW ones
    before = snapshot_crash_dir()
    print(f"  Existing crash dumps in KPV3 dir: {len(before)}")

    if not args.no_kill:
        print("  Killing stale KPV3 processes...")
        kill_stale_kpv_processes()

    # Build the JVM options string and inject via _JAVA_OPTIONS env var
    jopts = build_java_options(run_dir, gc=args.gc)
    print(f"  GC algorithm:  {args.gc}")
    print(f"  _JAVA_OPTIONS:")
    for opt in jopts.split():
        print(f"    {opt}")
    print()

    env = os.environ.copy()
    env["_JAVA_OPTIONS"] = jopts
    # Also write the opts to a file in run_dir for the record
    (run_dir / "JAVA_OPTIONS.txt").write_text(jopts.replace(" ", "\n"), encoding="utf-8")

    # Command (input first, exactly as documented in KPV_CLI_ANALYSIS.md)
    cmd = [str(kpv), str(args.epub), "-convert",
           "-output", str(run_dir), "-qualitychecks"]
    print(f"  $ {' '.join(cmd)}")
    print()

    t0 = time.time()
    timed_out = False
    rc = -1
    try:
        proc = subprocess.run(
            cmd, cwd=str(PROJECT_ROOT), env=env,
            capture_output=True, timeout=args.timeout,
        )
        rc = proc.returncode
        (run_dir / "stdout.txt").write_bytes(proc.stdout or b"")
        (run_dir / "stderr.txt").write_bytes(proc.stderr or b"")
    except subprocess.TimeoutExpired as e:
        timed_out = True
        if e.stdout: (run_dir / "stdout.txt").write_bytes(e.stdout)
        if e.stderr: (run_dir / "stderr.txt").write_bytes(e.stderr)
    elapsed = time.time() - t0
    print(f"  KPV3 finished in {elapsed:.1f}s (rc={rc}{'  TIMED OUT' if timed_out else ''})")

    # Collect new crash dumps
    new_crashes = collect_new_crashes(before, run_dir / "NEW_CRASHES")
    print(f"  New JVM crashes during this run: {len(new_crashes)}")
    for c in new_crashes:
        sz = c.stat().st_size
        print(f"    - {c.name} ({sz:,} bytes)")

    # Parse KPV's report (if produced)
    summary = parse_summary_log(run_dir / "Summary_Log.csv")
    if summary.get("present"):
        print(f"  Summary_Log.csv: status={summary.get('status')} "
              f"errors={summary.get('errors')} quality={summary.get('quality_issues')}")
    else:
        print("  Summary_Log.csv: NOT PRODUCED (converter never reached report stage)")

    jvm_log = run_dir / "jvm.log"
    jvm_log_size = jvm_log.stat().st_size if jvm_log.exists() else 0
    stdout_size = (run_dir / "stdout.txt").stat().st_size if (run_dir / "stdout.txt").exists() else 0
    stderr_size = (run_dir / "stderr.txt").stat().st_size if (run_dir / "stderr.txt").exists() else 0

    report = write_report(
        run_dir, epub=args.epub, elapsed=elapsed, returncode=rc,
        timed_out=timed_out, new_crashes=new_crashes, summary=summary,
        jvm_log_size=jvm_log_size, stdout_size=stdout_size, stderr_size=stderr_size,
    )
    print()
    print(f"Triage report: {report.relative_to(PROJECT_ROOT)}")

    # Exit codes: 0 = ran, no new crashes, conversion success
    #             1 = new crashes detected
    #             2 = ran but conversion failed / never produced report
    if new_crashes:
        return 1
    if not summary.get("present") or summary.get("status", "").lower() not in ("success", "completed"):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
