"""Invoke KPV3's converter JARs DIRECTLY, bypassing the Qt-wrapper IPC race.

KPV3's `Kindle Previewer 3.exe` is a Qt single-instance app. Its CLI mode has an
IPC race that on this Windows install fails ~5/5 attempts on large EPUBs:
the CLI request gets delegated to the GUI process and the actual converter
either returns generic "Failed to ProcessEpub" or returns "Success" with no KPF.

REVERSE-ENGINEERED PIPELINE (via process snoop):

    Stage 1   java EpubProcessorApp       (HTML clean / preprocess)
    Stage 2   java EpubAdapterApp         (EPUB -> KDF conversion driver)
    Stage 3   kindlegen.exe               (legacy Mobi generator; intermediate)
    Stage 4+  phantomjs main.js           (font + page rendering, ×N parallel)
    Stage 5   java KCFLocationMapCreatorApp   (only on success)
    Stage 6   java KCFPositionMapCreatorApp   (only on success)
    Stage 7   (KPF assembly inside Java land)

This runner reproduces stages 1-2 directly so we can:
  (a) confirm our EPUB is processable by the underlying converter library
  (b) bypass the single-instance Qt wrapper race that breaks KPV3 CLI

USAGE:
    python KDP/build/kpv_direct_jar.py <input.epub>                # smoke
    python KDP/build/kpv_direct_jar.py <input.epub> --stages 1,2   # subset
    python KDP/build/kpv_direct_jar.py <input.epub> --keep-temp    # don't clean

If Stage 1 succeeds, the cleaned EPUB lands in <out>/pOut/<book>.epub.
If Stage 2 succeeds, conv_out/ will contain the KDF + intermediate artifacts.
"""
from __future__ import annotations
import argparse
import base64
import os
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KPV3 = Path(os.environ.get("LOCALAPPDATA", "")) / "Amazon" / "Kindle Previewer 3"
JAVA = KPV3 / "lib" / "fc" / "jre" / "bin" / "java.exe"
LIB_DIR = KPV3 / "lib" / "fc"          # contains lib/* (the classpath)
KINDLEGEN = LIB_DIR / "bin" / "kindlegen.exe"
DEFAULT_EPUB = ROOT / "KDP" / "output" / "building-conversational-ai-llms-agents.epub"
OUTPUT_ROOT = ROOT / "KDP" / "output" / "kpv-direct"


# Reverse-engineered JVM flags (must match KPV3 exactly, including ParallelGC
# even though we proved it can crash on big books; G1 would be safer but we
# stick with KPV3's chosen flags first to match canonical behavior)
COMMON_JVM = [
    "-Djava.awt.headless=true",
    "-Dfile.encoding=UTF8",
    "-Djava.library.path=./lib;./lib/shared_libs",
    "-cp", "lib/*",
    "-XX:+UseParallelGC",   # what KPV3 uses; G1 is opt-in via --gc g1
    "-Xmx3072m",
]


def b64(s: str) -> str:
    """KPV3's base64 encoding: standard, no newlines."""
    return base64.b64encode(s.encode("utf-8")).decode("ascii")


def run_stage(label: str, cmd: list[str], cwd: Path, env: dict, timeout: int,
              run_dir: Path) -> dict:
    """Run one pipeline stage; capture stdout/stderr/timing."""
    print(f"\n>>> Stage [{label}]")
    print(f"    cmd: {cmd[0]} ... (+{len(cmd) - 1} args)")
    print(f"    cwd: {cwd}")
    log_dir = run_dir / "stage_logs"
    log_dir.mkdir(exist_ok=True)
    stdout_f = log_dir / f"{label}.stdout.txt"
    stderr_f = log_dir / f"{label}.stderr.txt"
    cli_f = log_dir / f"{label}.cmd.txt"
    cli_f.write_text("\n".join(cmd), encoding="utf-8")

    t0 = time.time()
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), env=env,
                              capture_output=True, timeout=timeout)
        rc = proc.returncode
        stdout_f.write_bytes(proc.stdout or b"")
        stderr_f.write_bytes(proc.stderr or b"")
    except subprocess.TimeoutExpired:
        rc = -1
        stdout_f.write_text("(timed out)", encoding="utf-8")
    elapsed = time.time() - t0

    print(f"    elapsed: {elapsed:.1f}s  exit: {rc}")
    # Show last 5 stderr lines (where real errors usually appear)
    if stderr_f.exists() and stderr_f.stat().st_size:
        try:
            errs = stderr_f.read_text(encoding="utf-8", errors="replace").splitlines()[-5:]
            for e in errs:
                if e.strip(): print(f"      stderr: {e[:150]}")
        except Exception:
            pass
    return {"label": label, "exit_code": rc, "elapsed": elapsed,
            "stdout_size": stdout_f.stat().st_size if stdout_f.exists() else 0,
            "stderr_size": stderr_f.stat().st_size if stderr_f.exists() else 0}


def stage1_html_cleaner(epub: Path, work: Path, timeout: int, env: dict,
                         run_dir: Path) -> dict:
    """com.amazon.html.cleaner.app.EpubProcessorApp: clean HTML, output preprocessed EPUB."""
    pout = work / "cTemp" / "pOut"
    ptemp = work / "cTemp" / "pTemp"
    pout.mkdir(parents=True, exist_ok=True)
    ptemp.mkdir(parents=True, exist_ok=True)
    cmd = [str(JAVA), *COMMON_JVM,
           "com.amazon.html.cleaner.app.EpubProcessorApp",
           b64(str(epub)),
           b64(str(pout)),
           b64(str(ptemp)),
           b64("--output-format"), b64("epub"),
           "--is-base64-encoded"]
    return run_stage("1_html_cleaner", cmd, LIB_DIR, env, timeout, run_dir)


def stage2_epub_adapter(epub: Path, work: Path, timeout: int, env: dict,
                         run_dir: Path) -> dict:
    """com.amazon.adapter.common.app.EpubAdapterApp: EPUB → KDF + intermediates."""
    pout = work / "cTemp" / "pOut"
    cleaned = pout / epub.name
    conv_out = work / "conv_out"
    conv_temp = work / "cTemp" / "conv_temp"
    conv_out.mkdir(parents=True, exist_ok=True)
    conv_temp.mkdir(parents=True, exist_ok=True)
    # If Stage 1 didn't run, fall back to original epub
    src = cleaned if cleaned.exists() else epub

    # The full snooped arg list for EpubAdapterApp:
    flags = ["--write-to-db",
             "--skip-remove-dual-cover-for-reflowable",
             "--log-level", "WARNING",
             "--skip-remove-dual-cover-for-fl",
             "--fail-fl-for-kpr",
             "--do-graceful-error-handling",
             "--locale", "en",
             "--file-creator-name", "KPR",
             "--file-creator-version", "3.104.0"]
    cmd = [str(JAVA), *COMMON_JVM,
           "-Dklibname=shared",
           "com.amazon.adapter.common.app.EpubAdapterApp",
           b64(str(src)), b64(str(conv_out)), b64(str(conv_temp)),
           *[b64(f) for f in flags],
           "--is-base64-encoded"]
    return run_stage("2_epub_adapter", cmd, LIB_DIR, env, timeout, run_dir)


def stage3_kindlegen(epub: Path, work: Path, timeout: int, env: dict,
                      run_dir: Path) -> dict:
    """kindlegen.exe: produce intermediate .mobi."""
    pout = work / "cTemp" / "pOut"
    cleaned = pout / epub.name
    src = cleaned if cleaned.exists() else epub
    mtemp = work / "cTemp" / "mTemp"
    mtemp.mkdir(parents=True, exist_ok=True)
    cmd = [str(KINDLEGEN),
           "-amzncreator", "Kindle Previewer 3.104.0",
           str(src),
           "-locale", "en",
           "-tempfolder", str(mtemp)]
    return run_stage("3_kindlegen", cmd, LIB_DIR, env, timeout, run_dir)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("epub", nargs="?", type=Path, default=DEFAULT_EPUB)
    ap.add_argument("--stages", default="1,2,3",
                    help="Comma-separated stage numbers (default 1,2,3)")
    ap.add_argument("--timeout", type=int, default=900,
                    help="Per-stage timeout in seconds (default 15 min)")
    ap.add_argument("--keep-temp", action="store_true",
                    help="Don't delete work dir after run")
    args = ap.parse_args()
    args.epub = args.epub.resolve()

    if not args.epub.exists():
        print(f"ERROR: EPUB not found: {args.epub}", file=sys.stderr); return 2
    if not JAVA.exists():
        print(f"ERROR: KPV3 java.exe not at {JAVA}", file=sys.stderr); return 2

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = OUTPUT_ROOT / run_id
    work = run_dir / "work"
    work.mkdir(parents=True, exist_ok=True)
    print(f"KPV3 direct-jar invocation: {run_id}")
    print(f"  EPUB:    {args.epub}  ({args.epub.stat().st_size / 1024 / 1024:.2f} MB)")
    print(f"  Work:    {work}")
    print(f"  Java:    {JAVA}")
    print(f"  Lib dir: {LIB_DIR}")
    print(f"  Stages:  {args.stages}")

    env = os.environ.copy()
    # Don't inject _JAVA_OPTIONS — match KPV3's exact env
    env.pop("_JAVA_OPTIONS", None)
    env.pop("JAVA_TOOL_OPTIONS", None)
    # CRITICAL: shared.dll depends on ICU + MSVCRT DLLs in lib/fc/lib/, and
    # libeay32/ssleay32 in lib/fc/bin/. Windows can't resolve them via Java's
    # -Djava.library.path alone (that only finds the FIRST DLL Java loads;
    # transitive dependents must be on PATH). Prepend both dirs to PATH.
    dll_dirs = [str(LIB_DIR / "lib"), str(LIB_DIR / "bin"),
                str(LIB_DIR / "jre" / "bin")]
    env["PATH"] = os.pathsep.join(dll_dirs) + os.pathsep + env.get("PATH", "")

    stages_run: list[dict] = []
    stage_fns = {"1": stage1_html_cleaner, "2": stage2_epub_adapter,
                 "3": stage3_kindlegen}

    for s in args.stages.split(","):
        s = s.strip()
        if s not in stage_fns:
            print(f"  Unknown stage: {s}; skipping"); continue
        result = stage_fns[s](args.epub, work, args.timeout, env, run_dir)
        stages_run.append(result)
        if result["exit_code"] != 0:
            print(f"  Stage {s} FAILED with exit {result['exit_code']}; "
                  f"halting (no point continuing pipeline)")
            break

    # Inventory artifacts produced
    print()
    print("=== Files produced in work dir ===")
    for p in sorted(work.rglob("*")):
        if p.is_file():
            print(f"  {p.stat().st_size:>10,}  {p.relative_to(work)}")

    print()
    print("=== Summary ===")
    for s in stages_run:
        icon = "[ok]" if s["exit_code"] == 0 else "[!!]"
        print(f"  {icon}  stage {s['label']:18s}  {s['elapsed']:6.1f}s  exit={s['exit_code']}")

    # Return 0 only if every requested stage succeeded
    return 0 if all(s["exit_code"] == 0 for s in stages_run) else 1


if __name__ == "__main__":
    sys.exit(main())
