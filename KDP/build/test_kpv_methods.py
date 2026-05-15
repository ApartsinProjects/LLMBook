"""Test KPV invocation from Python subprocess across multiple methods.

For each method:
  - record exit code
  - record stdout/stderr
  - record elapsed time
  - check for output KPF in:
      - working dir
      - %LOCALAPPDATA%/Amazon/Kindle Previewer 3/workspace/
      - %TEMP%
      - alongside EPUB
  - list child processes during run
"""
import os
import subprocess
import sys
import time
from pathlib import Path

KPV = r"C:\Users\apart\AppData\Local\Amazon\Kindle Previewer 3\Kindle Previewer 3.exe"
EPUB = r"E:\Projects\BookBlogsHome\LLMBook\KDP\build\test_kpv_target.epub"
WORKSPACE = Path(os.environ['LOCALAPPDATA']) / 'Amazon' / 'Kindle Previewer 3' / 'workspace'
TEMP = Path(os.environ['TEMP'])
EPUB_DIR = Path(EPUB).parent
OUTPUT_KPF = str(Path(EPUB).with_suffix('.kpf'))


def kill_kpv():
    subprocess.run(
        ['powershell', '-Command',
         "Stop-Process -Name 'KPR_NCD','Kindle Previewer 3' -Force -ErrorAction SilentlyContinue"],
        capture_output=True, timeout=15
    )
    time.sleep(2)


def snapshot_files(since_ts):
    found = []
    for root in [WORKSPACE, TEMP, EPUB_DIR, Path.cwd()]:
        if not root.exists():
            continue
        for p in root.rglob('*.kpf'):
            try:
                m = p.stat().st_mtime
                if m >= since_ts - 1:
                    found.append((str(p), m, p.stat().st_size))
            except Exception:
                pass
    return found


def list_running_kpv():
    r = subprocess.run(
        ['powershell', '-Command',
         "Get-Process -Name 'KPR_NCD','Kindle Previewer 3' -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,StartTime,CommandLine | ConvertTo-Json"],
        capture_output=True, text=True, timeout=20
    )
    return r.stdout.strip()


def run_test(label, runner_fn):
    print(f"\n{'='*70}\nMETHOD: {label}\n{'='*70}")
    kill_kpv()
    # remove any stale KPF
    for p in [Path(OUTPUT_KPF)]:
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass
    t0 = time.time()
    try:
        rc, stdout, stderr = runner_fn()
    except Exception as e:
        print(f"  EXCEPTION: {type(e).__name__}: {e}")
        return
    elapsed = time.time() - t0
    print(f"  exit_code: {rc}")
    print(f"  elapsed:   {elapsed:.1f}s")
    if stdout:
        print(f"  stdout (last 400 chars): {stdout[-400:]}")
    if stderr:
        print(f"  stderr (last 400 chars): {stderr[-400:]}")
    # processes after
    procs = list_running_kpv()
    if procs:
        print(f"  KPV procs still running:\n    {procs}")
    found = snapshot_files(t0)
    print(f"  KPF files modified since start ({len(found)}):")
    for path, mtime, size in found:
        print(f"    {path}  ({size} bytes)")
    if Path(OUTPUT_KPF).exists():
        print(f"  TARGET KPF EXISTS: {OUTPUT_KPF} ({Path(OUTPUT_KPF).stat().st_size} bytes)")
    else:
        print(f"  TARGET KPF MISSING: {OUTPUT_KPF}")


def m1_direct_run():
    """Method 1: direct subprocess.run with list args"""
    p = subprocess.run(
        [KPV, '-convert', EPUB, '-output', OUTPUT_KPF, '-qualitychecks'],
        capture_output=True, text=True, timeout=180
    )
    return p.returncode, p.stdout, p.stderr


def m2_cmd_c():
    """Method 2: cmd /c wrapper"""
    p = subprocess.run(
        ['cmd', '/c', KPV, '-convert', EPUB, '-output', OUTPUT_KPF, '-qualitychecks'],
        capture_output=True, text=True, timeout=180
    )
    return p.returncode, p.stdout, p.stderr


def m3_powershell_call():
    """Method 3: PowerShell with & call operator"""
    ps = f'& "{KPV}" -convert "{EPUB}" -output "{OUTPUT_KPF}" -qualitychecks; exit $LASTEXITCODE'
    p = subprocess.run(
        ['powershell', '-NoProfile', '-Command', ps],
        capture_output=True, text=True, timeout=180
    )
    return p.returncode, p.stdout, p.stderr


def m4_powershell_start_wait():
    """Method 4: Start-Process -Wait (synchronous, no shell)"""
    ps = f'Start-Process -FilePath "{KPV}" -ArgumentList \'-convert "{EPUB}" -output "{OUTPUT_KPF}" -qualitychecks\' -Wait -NoNewWindow; exit $LASTEXITCODE'
    p = subprocess.run(
        ['powershell', '-NoProfile', '-Command', ps],
        capture_output=True, text=True, timeout=180
    )
    return p.returncode, p.stdout, p.stderr


def m5_kindlepreviewer_bat():
    """Method 5: launcher batch from %APPDATA%/Amazon/"""
    bat = Path(os.environ['APPDATA']) / 'Amazon' / 'kindlepreviewer.bat'
    p = subprocess.run(
        [str(bat), '-convert', EPUB, '-output', OUTPUT_KPF, '-qualitychecks'],
        capture_output=True, text=True, timeout=180, shell=False
    )
    return p.returncode, p.stdout, p.stderr


def m6_subprocess_popen_detached():
    """Method 6: Popen with CREATE_NEW_PROCESS_GROUP + close stdio"""
    CREATE_NEW_PROCESS_GROUP = 0x00000200
    DETACHED_PROCESS = 0x00000008
    proc = subprocess.Popen(
        [KPV, '-convert', EPUB, '-output', OUTPUT_KPF, '-qualitychecks'],
        creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
    )
    try:
        rc = proc.wait(timeout=180)
    except subprocess.TimeoutExpired:
        proc.kill()
        rc = -1
    return rc, "", ""


def m7_no_qualitychecks():
    """Method 7: -convert WITHOUT -qualitychecks via cmd /c"""
    p = subprocess.run(
        ['cmd', '/c', KPV, '-convert', EPUB, '-output', OUTPUT_KPF],
        capture_output=True, text=True, timeout=180
    )
    return p.returncode, p.stdout, p.stderr


def m8_no_output_arg():
    """Method 8: -convert -qualitychecks WITHOUT -output (KPV picks own location)"""
    p = subprocess.run(
        ['cmd', '/c', KPV, '-convert', EPUB, '-qualitychecks'],
        capture_output=True, text=True, timeout=180
    )
    return p.returncode, p.stdout, p.stderr


if __name__ == '__main__':
    only = sys.argv[1] if len(sys.argv) > 1 else None
    methods = [
        ('m1_direct_subprocess_run', m1_direct_run),
        ('m2_cmd_/c', m2_cmd_c),
        ('m3_powershell_call_op', m3_powershell_call),
        ('m4_powershell_Start-Process_-Wait', m4_powershell_start_wait),
        ('m5_kindlepreviewer.bat_launcher', m5_kindlepreviewer_bat),
        ('m6_Popen_DETACHED', m6_subprocess_popen_detached),
        ('m7_no_qualitychecks', m7_no_qualitychecks),
        ('m8_no_output_arg', m8_no_output_arg),
    ]
    for label, fn in methods:
        if only and only not in label:
            continue
        run_test(label, fn)
    print(f"\nFinal KPV processes:\n{list_running_kpv()}")
    print(f"\nWorkspace dir exists: {WORKSPACE.exists()}")
    if WORKSPACE.exists():
        print(f"Workspace contents (sample):")
        for p in list(WORKSPACE.rglob('*'))[:30]:
            print(f"  {p}")
    kill_kpv()
