"""Add Defender exclusions + open ACLs for KPV3 (triggers ONE UAC prompt).

Run this once after KPV3 install. After approval:
  * KPV3 install dir whitelisted from Defender real-time scan
  * KPR_NCD.exe + Kindle Previewer 3.exe + kindlegen.exe + bundled java.exe
    whitelisted as processes (known AV false-positive vectors)
  * %TEMP%, ~/.kindle/KPR/, %LOCALAPPDATA%/Amazon/KPR/ excluded from scan

Why: KPR_NCD.exe is documented on file.net as a recurring AV false-positive.
Even with no quarantine events, real-time scanning can slow per-file open()
calls enough that KPV3's converter hits internal timeouts. Whitelisting
removes that risk.

Output is written to KDP/build/_kpv_debug_archive/defender_exclusions.txt.
"""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
JOURNAL = ROOT / "KDP" / "build" / "_kpv_debug_archive"
JOURNAL.mkdir(parents=True, exist_ok=True)
REPORT = JOURNAL / "defender_exclusions.txt"


def build_ps_script() -> str:
    """Build the elevated PowerShell payload as a single script string."""
    appdata = os.environ.get("LOCALAPPDATA", "")
    userprof = os.environ.get("USERPROFILE", "")
    temp_dir = os.environ.get("TEMP", "")

    paths = [
        rf"{appdata}\Amazon\Kindle Previewer 3",
        rf"{appdata}\Amazon\KPR",
        rf"{userprof}\.kindle\KPR",
        temp_dir,
    ]
    proc_names = ["KPR_NCD.exe", "Kindle Previewer 3.exe", "kindlegen.exe"]
    proc_paths = [
        rf"{appdata}\Amazon\Kindle Previewer 3\lib\fc\jre\bin\java.exe",
    ]

    lines = ["Write-Host '[admin] Adding Defender exclusions for KPV3'"]
    for p in paths:
        if not p:
            continue
        lines.append(f"Add-MpPreference -ExclusionPath '{p}' -ErrorAction SilentlyContinue")
        lines.append(f"Write-Host '  + ExclusionPath: {p}'")
    for n in proc_names:
        lines.append(f"Add-MpPreference -ExclusionProcess '{n}' -ErrorAction SilentlyContinue")
        lines.append(f"Write-Host '  + ExclusionProcess: {n}'")
    for pp in proc_paths:
        lines.append(f"Add-MpPreference -ExclusionProcess '{pp}' -ErrorAction SilentlyContinue")
        lines.append(f"Write-Host '  + ExclusionProcess: {pp}'")

    # Dump current exclusions to file so caller can verify
    lines.append(
        f"Get-MpPreference | Select-Object ExclusionPath, ExclusionProcess "
        f"| Format-List | Out-File -Encoding utf8 '{REPORT}'"
    )
    lines.append("Write-Host '[admin] Done; verification written to KDP/build/_kpv_debug_archive/defender_exclusions.txt'")
    return "\n".join(lines)


def main() -> int:
    if not sys.platform.startswith("win"):
        print("ERROR: this script is Windows-only.", file=sys.stderr)
        return 2

    ps_script = build_ps_script()
    # Write payload to a temp .ps1 so we don't blow up with command-line length
    # or quoting limits in Start-Process arglist
    payload = JOURNAL / "_defender_payload.ps1"
    payload.write_text(ps_script, encoding="utf-8")
    print(f"Payload written to: {payload}")
    print()
    print(">>> A Windows UAC dialog will appear. Click YES to approve. <<<")
    print()

    # Outer non-elevated PowerShell that re-launches itself elevated to run our payload.
    # -Verb RunAs triggers UAC. -Wait blocks here until the elevated process exits.
    launch = (
        f"Start-Process powershell -Verb RunAs -Wait "
        f"-ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','{payload}'"
    )
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", launch],
            capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            print(f"Outer PowerShell exit code: {proc.returncode}")
            if proc.stderr:
                print("stderr:", proc.stderr[:500])
            return 1
    except subprocess.TimeoutExpired:
        print("ERROR: UAC dialog timeout (120s). Did you approve it?")
        return 1
    except Exception as e:
        print(f"ERROR launching elevation: {e}")
        return 1

    # Read verification file
    if REPORT.exists():
        print()
        print("=" * 60)
        print(f"Verification ({REPORT}):")
        print("=" * 60)
        print(REPORT.read_text(encoding="utf-8")[:2000])
    else:
        print("WARNING: verification file not written. UAC may have been denied.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
