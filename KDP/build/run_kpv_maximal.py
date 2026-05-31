"""Run KPV3 with the ENTIRE diagnostic kitchen sink.

What this does that run_kpv_debug.py doesn't:
  * Uses every KPV3 CLI flag we've reverse-engineered:
      -convert -output <dir> -qualitychecks
      -log                     (auxiliary log files)
      -conversionLog           (per-step conversion log)
      -clearKindlegenLogs      (start with clean kindlegen state)
      --log-level VERBOSE      (max verbosity)
      -debug                   (debug mode)
  * Injects MAX JVM diagnostics via _JAVA_OPTIONS (G1GC, verbose:class+jni+gc,
    HeapDumpOnOOM, ErrorFile redirect, minidump on crash, PrintGCDetails)
  * Snapshots KPR.Log before/after to extract only THIS run's tail
  * Also runs EPUBCheck 5.3.0 in 4 profiles (default + edupub + preview + dict)
    in parallel with KPV3
  * Captures every output file KPV3 produces (KPF, Mobi, Logs, jvm.log)
  * Generates a comprehensive single-file Markdown report

Output:
  KDP/output/kpv-maximal/<timestamp>/
    REPORT.md             <- start here
    JAVA_OPTIONS.txt
    cli_args.txt
    Summary_Log.csv
    Logs/                 (KPV per-file log)
    KPF/                  (converted KFX, if it survived past conversion)
    Mobi/                 (legacy mobi, if produced)
    jvm.log               (JVM internal log)
    stdout.txt, stderr.txt
    kpr_log_tail.txt      (this-run-only slice of ~/.kindle/KPR/log/KPR.Log)
    epubcheck_5_3_0_default.txt
    epubcheck_5_3_0_edupub.txt
    epubcheck_5_3_0_preview.txt
    epubcheck_5_3_0_dict.txt
"""
from __future__ import annotations
import argparse
import concurrent.futures
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


def rel(p: Path) -> str:
    """relative_to(ROOT) that doesn't crash on paths outside ROOT."""
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)

KPV3_DIR = Path(os.environ.get("LOCALAPPDATA", "")) / "Amazon" / "Kindle Previewer 3"
KPV3_EXE = KPV3_DIR / "Kindle Previewer 3.exe"
KPV3_JAVA = KPV3_DIR / "lib" / "fc" / "jre" / "bin" / "java.exe"
KPR_LOG = Path.home() / ".kindle" / "KPR" / "log" / "KPR.Log"
EPUBCHECK_JAR = ROOT / "KDP" / "build" / "tools" / "epubcheck-5.3.0" / "epubcheck.jar"
DEFAULT_EPUB = ROOT / "KDP" / "output" / "building-conversational-ai-llms-agents.epub"
OUTPUT_ROOT = ROOT / "KDP" / "output" / "kpv-maximal"


def build_java_options(run_dir: Path) -> str:
    rd = run_dir.as_posix()
    return " ".join([
        "-XX:+UnlockDiagnosticVMOptions",
        "-XX:+CreateMinidumpOnCrash",
        "-XX:+LogVMOutput",
        f"-XX:LogFile={rd}/jvm.log",
        f"-XX:ErrorFile={rd}/error_pid_%p.log",
        f"-XX:HeapDumpPath={rd}/heap.hprof",
        "-XX:+HeapDumpOnOutOfMemoryError",
        # G1GC: confirmed-working choice (ParallelGC crashes on big books).
        "-XX:+UseG1GC", "-XX:MaxGCPauseMillis=200",
        "-XX:+ParallelRefProcEnabled",
        # Maximum verbosity
        "-verbose:class", "-verbose:jni", "-verbose:gc",
        "-XX:+PrintGCDetails", "-XX:+PrintGCDateStamps",
        "-XX:-OmitStackTraceInFastThrow",
        # Sizing
        "-Xss4m", "-Xmx4g",
    ])


def kill_stale_kpv() -> None:
    """Kill stale KPV3 workers (NOT the GUI — its presence may be required)."""
    # IMPORTANT: do NOT kill 'Kindle Previewer 3.exe' (the GUI). Empirically,
    # if the GUI is dead when CLI conversion is invoked, the 37 MB book
    # produces "Failed to ProcessEpub" + "Failed to create temp directory".
    # The 27 KB smoke test passes either way, so the dependency is timing
    # / state related, not a flat requirement. Safest: leave GUI alone.
    # Only kill orphaned worker daemons (java, kindlegen) and KPR_NCD.
    for image in ("java.exe", "kindlegen.exe"):
        subprocess.run(["taskkill", "/F", "/IM", image],
                       capture_output=True, timeout=15)
    time.sleep(2)


def ensure_gui_running() -> bool:
    """Launch KPV3 GUI if not already running. Returns True if started fresh."""
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Get-Process 'Kindle Previewer 3' -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count"],
        capture_output=True, text=True, timeout=10,
    )
    count = (proc.stdout or "0").strip()
    if count == "0":
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"Start-Process -FilePath '{KPV3_EXE}'"],
            capture_output=True, timeout=10,
        )
        time.sleep(8)  # let GUI initialise
        return True
    return False


def run_kpv(epub: Path, run_dir: Path, timeout: int,
            experimental_flags: bool = False) -> dict:
    """Run KPV3 with every flag we know, capture everything.

    Baseline (confirmed-working per jhowell's Calibre KFX plugin):
        -convert -locale en -output <dir> -qualitychecks
    Experimental (undocumented strings found in binary; may or may not work):
        -conversionLog -clearKindlegenLogs --log-level VERBOSE -debug -log
    Enable experimental flags with experimental_flags=True (CLI: --experimental).
    """
    cmd = [str(KPV3_EXE), str(epub),
           "-convert",
           "-locale", "en",        # confirmed safe in Calibre KFX plugin source
           "-output", str(run_dir),
           "-qualitychecks"]
    if experimental_flags:
        cmd.extend([
            "-log",                 # auxiliary log files
            "-conversionLog",       # per-step conversion log
            "-clearKindlegenLogs",  # clean kindlegen state
            "--log-level", "VERBOSE",
            "-debug",
        ])
    (run_dir / "cli_args.txt").write_text(
        "\n".join(cmd), encoding="utf-8")

    jopts = build_java_options(run_dir)
    (run_dir / "JAVA_OPTIONS.txt").write_text(
        jopts.replace(" ", "\n"), encoding="utf-8")

    env = os.environ.copy()
    env["_JAVA_OPTIONS"] = jopts

    # Snapshot KPR.Log size to extract this-run-only tail later
    pre_log_size = KPR_LOG.stat().st_size if KPR_LOG.exists() else 0

    print(f"  [KPV] command: {' '.join(cmd)}")
    print(f"  [KPV] env _JAVA_OPTIONS injected ({len(jopts)} chars)")
    print(f"  [KPV] running, timeout={timeout}s...")
    t0 = time.time()
    timed_out = False
    rc = -1
    try:
        proc = subprocess.run(
            cmd, capture_output=True, timeout=timeout, env=env, cwd=str(ROOT))
        rc = proc.returncode
        (run_dir / "stdout.txt").write_bytes(proc.stdout or b"")
        (run_dir / "stderr.txt").write_bytes(proc.stderr or b"")
    except subprocess.TimeoutExpired as e:
        timed_out = True
        if e.stdout: (run_dir / "stdout.txt").write_bytes(e.stdout)
        if e.stderr: (run_dir / "stderr.txt").write_bytes(e.stderr)
    elapsed = time.time() - t0

    # Pull this-run slice of KPR.Log
    log_tail = ""
    if KPR_LOG.exists():
        try:
            with KPR_LOG.open("rb") as f:
                f.seek(pre_log_size)
                log_tail = f.read().decode("utf-8", errors="replace")
            (run_dir / "kpr_log_tail.txt").write_text(log_tail, encoding="utf-8")
        except Exception:
            pass

    # Parse Summary_Log.csv
    summary: dict = {}
    sp = run_dir / "Summary_Log.csv"
    if sp.exists():
        try:
            for row in csv.DictReader(sp.open(encoding="utf-8-sig", newline="")):
                summary = {k.strip(): (v or "").strip() for k, v in row.items()}
                break
        except Exception as e:
            summary = {"_parse_error": str(e)}

    # Find KPF + Mobi
    kpfs = list(run_dir.rglob("*.kpf"))
    mobis = list(run_dir.rglob("*.mobi"))

    return {
        "elapsed": elapsed, "exit_code": rc, "timed_out": timed_out,
        "summary": summary, "log_tail": log_tail,
        "kpf_files": [str(p) for p in kpfs],
        "mobi_files": [str(p) for p in mobis],
        "jvm_log_size": ((run_dir / "jvm.log").stat().st_size
                         if (run_dir / "jvm.log").exists() else 0),
        "stdout_size": ((run_dir / "stdout.txt").stat().st_size
                        if (run_dir / "stdout.txt").exists() else 0),
        "stderr_size": ((run_dir / "stderr.txt").stat().st_size
                        if (run_dir / "stderr.txt").exists() else 0),
    }


def run_epubcheck(epub: Path, profile: str, out_file: Path) -> dict:
    """Run EPUBCheck 5.3.0 in the given profile."""
    cmd = [str(KPV3_JAVA), "-jar", str(EPUBCHECK_JAR),
           "--mode", "epub", "--profile", profile, "-u",
           str(epub)]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=600)
        out_file.write_bytes(proc.stdout + b"\n--STDERR--\n" + proc.stderr)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        out_file.write_text("(timed out)", encoding="utf-8")
        rc = -1
    elapsed = time.time() - t0

    # Parse the summary line "Messages: 0 fatals / 0 errors / 0 warnings / 0 infos / 20 usages"
    text = out_file.read_text(encoding="utf-8", errors="replace")
    summary_line = ""
    for line in text.splitlines():
        if line.startswith("Messages:"):
            summary_line = line.strip()
            break
    return {"profile": profile, "exit_code": rc, "elapsed": elapsed,
            "summary": summary_line, "file": str(out_file)}


def write_report(run_dir: Path, *, epub: Path, kpv: dict,
                 epubchecks: list[dict]) -> Path:
    rpt = run_dir / "REPORT.md"
    lines = []
    lines.append("# KPV3 + EPUBCheck Maximal Diagnostic Report\n")
    lines.append(f"- Run dir: `{rel(run_dir)}`")
    lines.append(f"- EPUB: `{rel(epub)}` ({epub.stat().st_size / 1024 / 1024:.2f} MB)")
    lines.append(f"- Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")

    lines.append("## KPV3 conversion + qualitychecks\n")
    lines.append(f"- Wall time: **{kpv['elapsed']:.1f}s**")
    lines.append(f"- Process exit code: `{kpv['exit_code']}` "
                 f"{'(TIMED OUT)' if kpv['timed_out'] else ''}")
    lines.append(f"- jvm.log size: {kpv['jvm_log_size']:,} bytes")
    lines.append(f"- stdout / stderr: {kpv['stdout_size']:,} / {kpv['stderr_size']:,} bytes")
    if kpv["summary"]:
        s = kpv["summary"]
        status = s.get("Conversion Status", "?")
        icon = "✅" if status.lower() == "success" else "❌"
        lines.append(f"- **Conversion Status: {icon} {status}**")
        for key in ("Error Count", "Quality Issue Count",
                    "Enhanced Typesetting Status",
                    "Output File Path", "Log File Path", "Quality Report Path"):
            lines.append(f"  - {key}: `{s.get(key, '?')}`")
    else:
        lines.append("- ❌ Summary_Log.csv was NOT produced")
    lines.append("")
    lines.append(f"- KPF files produced: {len(kpv['kpf_files'])}")
    for k in kpv["kpf_files"]:
        sz = Path(k).stat().st_size
        lines.append(f"  - `{Path(k).name}` ({sz:,} bytes)")
    lines.append(f"- Mobi files produced: {len(kpv['mobi_files'])}")
    for m in kpv["mobi_files"]:
        sz = Path(m).stat().st_size
        lines.append(f"  - `{Path(m).name}` ({sz:,} bytes)")
    lines.append("")

    lines.append("## EPUBCheck 5.3.0 (4 profiles)\n")
    lines.append("| Profile | Exit | Time | Summary |")
    lines.append("|---|---|---|---|")
    for ec in epubchecks:
        lines.append(f"| `{ec['profile']}` | {ec['exit_code']} | {ec['elapsed']:.1f}s | "
                     f"{ec['summary'] or '(none)'} |")
    lines.append("")
    lines.append("Profile semantics:")
    lines.append("- `default`: standard EPUB 3 validation (what KDP cares about)")
    lines.append("- `preview`: requires `dc:type=preview` + `dc:source` (false-positive for full books)")
    lines.append("- `dict`: requires `dc:type=dictionary` + search-key-map (false-positive for non-dictionaries)")
    lines.append("- `edupub`: DAISY EduPub schema (very strict; false-positives unless book IS edupub)")
    lines.append("")

    lines.append("## Per-file quality log (KPV qualitychecks)\n")
    log_csvs = list((run_dir / "Logs").glob("*.csv")) if (run_dir / "Logs").exists() else []
    if log_csvs:
        for f in log_csvs:
            lines.append(f"### `{f.name}`\n")
            lines.append("```")
            lines.append(f.read_text(encoding="utf-8-sig", errors="replace")[:5000])
            lines.append("```")
    else:
        lines.append("- No per-file log produced")
    lines.append("")

    lines.append("## KPR.Log slice (events from THIS run only)\n")
    lines.append("```")
    log_tail = kpv.get("log_tail", "")
    if log_tail:
        # Trim to most informative parts: keep errors + last 50 lines
        errs = [l for l in log_tail.splitlines() if "[ERROR]" in l]
        tail = log_tail.splitlines()[-50:]
        keep = sorted(set(errs + tail), key=lambda s: log_tail.find(s) if s in log_tail else 0)
        lines.append("\n".join(keep[:80]))
    else:
        lines.append("(no KPR.Log content captured)")
    lines.append("```")
    lines.append("")

    lines.append("## Files in run dir\n")
    lines.append("```")
    for p in sorted(run_dir.rglob("*")):
        if p.is_file():
            rel_path = p.relative_to(run_dir)  # local var; don't shadow rel()
            lines.append(f"  {p.stat().st_size:>10,}  {rel_path}")
    lines.append("```")

    rpt.write_text("\n".join(lines), encoding="utf-8")
    return rpt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", nargs="?", type=Path, default=DEFAULT_EPUB)
    ap.add_argument("--timeout", type=int, default=1800,
                    help="KPV3 timeout in seconds (default 30 min)")
    ap.add_argument("--no-kill", action="store_true")
    ap.add_argument("--experimental", action="store_true",
                    help="Add undocumented binary-string flags (-debug, "
                         "--log-level VERBOSE, -conversionLog, "
                         "-clearKindlegenLogs, -log) on top of confirmed-safe baseline")
    args = ap.parse_args()

    # Resolve to absolute path so relative_to(ROOT) works consistently
    args.epub = args.epub.resolve()
    if not args.epub.exists():
        print(f"ERROR: EPUB not found: {args.epub}", file=sys.stderr)
        return 2
    # NOTE: rel() helper is now module-level (line ~52) so write_report() can use it
    if not KPV3_EXE.exists():
        print(f"ERROR: KPV3 not found at {KPV3_EXE}", file=sys.stderr)
        return 2
    if not EPUBCHECK_JAR.exists():
        print(f"ERROR: EPUBCheck jar not found at {EPUBCHECK_JAR}", file=sys.stderr)
        return 2

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = OUTPUT_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"KPV3 + EPUBCheck MAXIMAL run: {run_id}")
    print(f"  EPUB:      {rel(args.epub)}  "
          f"({args.epub.stat().st_size / 1024 / 1024:.2f} MB)")
    print(f"  Run dir:   {rel(run_dir)}")
    print(f"  KPV3:      {KPV3_EXE}")
    print(f"  EPUBCheck: {rel(EPUBCHECK_JAR)}")
    print()

    if not args.no_kill:
        print("  Killing stale KPV3 workers (NOT the GUI)...")
        kill_stale_kpv()

    print("  Ensuring KPV3 GUI is running (required for CLI conversion of big books)...")
    fresh = ensure_gui_running()
    print(f"  GUI {'launched fresh' if fresh else 'already running'}")

    # IMPORTANT: KPV3 conversion is FRAGILE — it competes with other JVMs and
    # heavy file-system activity on the host. Run it ALONE first (no parallel
    # EPUBCheck competing for %TEMP%, java.exe, file handles), THEN fan out the
    # EPUBCheck profile runs after KPV3 has finished. Earlier attempts to run
    # all 5 java.exe processes simultaneously caused KPV3 to fail with the
    # spurious "Failed to create temp directory" error.
    print(">>> Phase 1: KPV3 conversion (alone, no resource competition)")
    kpv = run_kpv(args.epub, run_dir, args.timeout, args.experimental)
    print(f"  KPV3 done in {kpv['elapsed']:.1f}s (exit {kpv['exit_code']})")

    print()
    print(">>> Phase 2: 4 EPUBCheck profiles in parallel (KPV3 is finished)")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        ec_futures = []
        for profile in ("default", "preview", "dict", "edupub"):
            out_file = run_dir / f"epubcheck_5_3_0_{profile}.txt"
            ec_futures.append(ex.submit(run_epubcheck, args.epub, profile, out_file))
        epubchecks = [f.result() for f in ec_futures]

    print()
    for ec in epubchecks:
        print(f"  EPUBCheck {ec['profile']:8s}: {ec['summary'][:80]}")

    rpt = write_report(run_dir, epub=args.epub, kpv=kpv, epubchecks=epubchecks)
    print()
    print(f"Report: {rel(rpt)}")

    # Exit codes:
    # 0 = KPV3 conversion succeeded AND default-profile EPUBCheck passed
    # 1 = KPV3 conversion failed
    # 2 = KPV3 ok but EPUBCheck default profile has errors
    if not kpv["summary"] or kpv["summary"].get("Conversion Status", "").lower() != "success":
        return 1
    default_ec = next((ec for ec in epubchecks if ec["profile"] == "default"), {})
    if "0 errors" not in default_ec.get("summary", ""):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
