# Kindle Previewer 3: troubleshooting + reinstall guide

## ⚠️ FIRST THING TO TRY: Launch the GUI once

If KPV3 CLI conversions fail with:

```
[ERROR] Failed to ProcessEpub
[ERROR] Failed to create temp directory
[ERROR] Failed to create tmp directory for mobiMetadataDetection
```

…and you've never opened the GUI on this user profile, **that's almost certainly the cause**. KPV3's CLI mode silently requires per-user state that only the GUI creates on first launch. The installer doesn't do it.

**Fix**:
```powershell
# Launch the GUI for 5-10 seconds, then close the window. You don't need
# to convert anything, just let the GUI initialize.
Start-Process "$env:LOCALAPPDATA\Amazon\Kindle Previewer 3\Kindle Previewer 3.exe"
```

After the GUI has launched once, CLI conversions work normally. This persists across reboots; you only need to do it once per Windows user profile.

This was discovered on 2026-05-30 after three weeks of "every conversion fails" symptoms that mimicked install corruption. A clean reinstall did NOT fix it. Launching the GUI once did.

## How we proved it

We built a cycle-based repair orchestrator: `KDP/build/kpv_repair_cycles.py`. Cycle C0 (the baseline reproduction with no repair) was meant to confirm the failure before applying fixes. But because the user had just launched the GUI manually, C0 PASSED, producing a valid KPF in 20 seconds.

```
>>> Cycle C0: Baseline (no repair)
[PASS] cycle 0 | Baseline (no repair) | 20.0s
      summary: status=Success errors=0 output='...\KPF\math-recipe.kpf'
      KPF produced: ...\KPF\math-recipe.kpf
```

The GUI-launch-once requirement is undocumented by Amazon and unindexed in community forums.

## If the GUI-launch trick doesn't help

Then the install IS broken. Reinstall steps:

### 1. Uninstall current KPV3

```powershell
# Kill running processes
Get-Process 'Kindle Previewer 3','KPR_NCD','java' -ErrorAction SilentlyContinue | Stop-Process -Force

# Run silent uninstaller (NSIS-style, /S = silent)
& "$env:LOCALAPPDATA\Amazon\Kindle Previewer 3\Uninstall.exe" /S
# Wait for uninstall to complete (usually <5 seconds)
Start-Sleep -Seconds 10
```

### 2. Clean leftover support dirs

```powershell
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\Amazon\KPR" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$env:USERPROFILE\.kindle\KPR" -ErrorAction SilentlyContinue
```

### 3. Download fresh installer

Official URL (372 MB):
```powershell
Invoke-WebRequest -Uri "https://d2bzeorukaqrvt.cloudfront.net/KindlePreviewerInstaller.exe" `
                  -OutFile "$env:TEMP\KindlePreviewerInstaller.exe"
```

### 4. Install with admin elevation, silent

```powershell
Start-Process -FilePath "$env:TEMP\KindlePreviewerInstaller.exe" `
              -ArgumentList "/S" -Verb RunAs -Wait
```

### 5. ⚠️ DO NOT FORGET: Launch the GUI once

```powershell
Start-Process "$env:LOCALAPPDATA\Amazon\Kindle Previewer 3\Kindle Previewer 3.exe"
# Wait 10 seconds, then close the window.
```

### 6. Sanity test with the cycle runner

```bash
python KDP/build/kpv_repair_cycles.py --only 0
```

Should report `[PASS] cycle 0 | Baseline (no repair) | ~20s` with a KPF produced.

### 7. Re-run the build

```bash
python KDP/build/publish.py
```

The KPV gate is wired to be default-on again. It will catch any Kindle-specific issues EPUBCheck misses.

## Reference: what we ruled out before finding the fix

Confirmed NOT to be the cause of the "Failed to create temp directory" error:
- Install corruption (fresh reinstall failed identically until GUI was launched)
- Disk space (had 30 GB free)
- File permissions (user had FullControl on %TEMP%, manual mkdir of UUID-style dirs worked)
- OneDrive sync of AppData (no OneDrive installed)
- Missing VC++ Redistributable (all generations 2005-2022 installed)
- Defender quarantine of KPR_NCD.exe (no events)
- Java GC bug in bundled JRE 8.0_241 (ParallelGC DOES crash on large books but it's a separate issue, fixable by `_JAVA_OPTIONS=-XX:+UseG1GC`)
- Non-ASCII or spaces in %TEMP% path (path was clean)
- Long-path / MAX_PATH limit (paths were short)

## Related useful files

- `KDP/build/run_kpv_debug.py` — KPV3 wrapper with JVM-level diagnostics
- `KDP/build/kpv_repair_cycles.py` — automated repair cycle orchestrator
- `KDP/build/_kpv_debug_archive/` — archived KPR.Log snapshots + journal
- `KDP/build/KPV_CLI_ANALYSIS.md` — earlier notes on KPV3 CLI behavior
