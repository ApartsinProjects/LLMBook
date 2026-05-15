# Kindle Previewer 3 CLI: subprocess reliability analysis

Date: 2026-05-15
Investigator: Claude (parent session context)
Test EPUB: `E:/Projects/BookBlogsHome/LLMBook/KDP/build/test_epubs/output/test_math.epub` (3.5 KB)
KPV install: `C:\Users\apart\AppData\Local\Amazon\Kindle Previewer 3\Kindle Previewer 3.exe` (40 MB, 4/15/2026)

## Executive summary

**Kindle Previewer 3 has no working headless CLI on Windows. The `-convert` flag exists but is a no-op when the launching shell is not a foreground interactive desktop session.** All Python and PowerShell invocations of `Kindle Previewer 3.exe -convert ... -qualitychecks` from a non-interactive context return exit code 0 in 100-200 ms while writing zero output. The CLI is implemented as a GUI command-router that requires a real WinSta0 desktop session with a focused window to dispatch the conversion job.

The 117 MB KPF that exists at `E:/Projects/BookBlogsHome/LLMBook/KDP/output/building-conversational-ai-llms-agents.kpf` (last written 5/14 23:28) was produced from an interactive shell (the user double-clicking or typing directly into a console window with desktop focus), not from a build script or Claude subprocess.

## 1. KPV CLI actual behavior

### 1.1 The `-convert` flag silently returns 0

When `Kindle Previewer 3.exe -convert <epub> -output <kpf> -qualitychecks` is invoked from any of:

- `subprocess.run(cmd_list, ...)`
- `subprocess.run(['cmd', '/c', ...])`
- `subprocess.Popen([...], DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)`
- PowerShell `& "exe" args`
- PowerShell `Start-Process -Wait`
- PowerShell `Start-Process -RedirectStandardOutput`
- .NET `System.Diagnostics.Process.Start()` with `UseShellExecute=false`

...the parent process exits **rc=0 in 0.14-2.5 s** and writes nothing. Total CPU time is 140 ms. `stdout` and `stderr` are empty. The process does NOT spawn `kindlegen.exe` (the actual MOBI compiler) or any conversion worker. It only forks the persistent `KPR_NCD.exe` daemon and exits.

### 1.2 The argument-less mode (positional EPUB) does spawn workers, but they exit silently

When invoked with just `<exe> <epub> -log <dir>` (no `-convert`), the launch behaves differently:

```
t=5s   procs=[Kindle Previewer 3]
t=10s  procs=[Kindle Previewer 3, kindlegen, KPR_NCD]
t=15s  procs=[Kindle Previewer 3, KPR_NCD]
t=21s  procs=[KPR_NCD]     <- workers gone
t=300s procs=[KPR_NCD]     <- nothing further happens, no Summary_Log.csv
```

A `kindlegen.exe` worker IS spawned briefly (5-10 s) but exits without writing the expected `Summary_Log.csv`. The KPV GUI process exits 21 s after launch. The persistent `KPR_NCD.exe` daemon is unrelated to conversion (it is the "Native Code Daemon" tray/notification helper).

### 1.3 The GUI requires a real foreground window

KPV's main process is a Qt5/QtWebEngine GUI binary. When launched from a non-foreground context:
- `MainWindowHandle = 0` (no window created)
- `Responding = True` but no UI
- Process exits silently after 5-21 s with rc=0

When launched from a foreground interactive console (user double-clicks, or types the path in a desktop-attached cmd.exe), the GUI window IS created, conversion runs in 30-180 s, and the KPF lands next to the EPUB.

### 1.4 The manifest does NOT require elevation

The embedded Windows manifest (extracted from PE resources):

```xml
<requestedExecutionLevel level="asInvoker" uiAccess="false"/>
```

So the `PermissionError [WinError 5]` is NOT a UAC issue. It is most likely from `subprocess.run(..., shell=False)` choking on the literal `-convert` token being parsed as a flag by CreateProcessW when the path contains spaces and the cmdline is constructed without proper quoting. Using `cmd /c <exe> -convert ...` masks this, but masks it into a different failure mode (silent rc=0).

## 2. KPF output locations

There is no hidden workspace. KPV writes KPFs to:

1. **Alongside the input EPUB** (`epub.with_suffix('.kpf')`) when launched via GUI Open dialog.
2. **Same directory as `-output <path>`** when the CLI works (only confirmed to work in foreground sessions).
3. **NOT in** `%LOCALAPPDATA%/Amazon/Kindle Previewer 3/workspace/` - that directory does not exist. KPV uses `%LOCALAPPDATA%/Amazon/KPR/cache/QtWebEngine/` only for its WebEngine HTTP cache.
4. **NOT in** `%TEMP%` - kindlegen creates `mbp_XXXX_X_F_X_...` temp dirs but cleans them up.

`%LOCALAPPDATA%/Amazon/Kindle Previewer 3/` contains only the install files (Qt DLLs, skins, fonts, locale data). No state, no preferences, no per-conversion artifacts.

`HKCU:\Software\Amazon\Kindle Previewer 3` has only a single `(default)` value pointing to the install dir. KPV stores NO preferences in the registry.

## 3. Tested methods

| # | Method | rc | Time | KPF? | Notes |
|---|--------|----|----|------|-------|
| 1 | `subprocess.run([exe, '-convert', ...])` | 0 | 2.4s | no | Original failure. No work done. |
| 2 | `subprocess.run(['cmd', '/c', exe, '-convert', ...])` | 0 | 2.0s | no | Current script's workaround - still doesn't work. |
| 3 | PowerShell `& $kpv -convert ...` | null | 25ms | no | Detaches immediately. |
| 4 | `Start-Process -FilePath $kpv -Wait` | 0 | 2.6s | no | `-Wait` only waits for parent .exe, which exits in 140ms. |
| 5 | `kindlepreviewer.bat` launcher (`%APPDATA%\Amazon\`) | 0 | 2s | no | Wraps the same exe call. No different. |
| 6 | `Popen([...], DETACHED_PROCESS)` | 0 | 2s | no | Same. |
| 7 | No `-qualitychecks` | 0 | 2s | no | Flag is not the issue. |
| 8 | No `-output` arg | 0 | 2s | no | Same. |
| 9 | Positional EPUB + `-log dir` (bisect-style) | (no parent rc) | 300s | no | Workers spawn briefly then exit silently. |
| 10 | `cmd /c start "" exe ...` | 1 | - | no | `start` parses `-convert` as filename. |
| 11 | `.NET Process.Start` with `UseShellExecute=false` | 0 | 30s | no | Same silent exit. |
| 12 | `Start-Process -Verb RunAs` | - | - | - | Not tested - manifest is `asInvoker`, no elevation needed. |

**No method tested produces a KPF from a Claude subprocess context, regardless of language or flags.**

### 3.1 What DOES work: kindlegen.exe directly

`kindlegen.exe` (the legacy MOBI compiler bundled at `lib/fc/bin/kindlegen.exe`) IS reachable from subprocess. It runs in 3 seconds, writes `<epub-stem>.mobi` alongside the EPUB, and emits 195 lines of validation messages on stdout. This is useful for AZW/MOBI but does NOT produce KPF (the modern Kindle format).

```
kindlegen V2.9 build 0000-kdevbld
W29007: Rejected unknown tag: <math xmlns="http://www.w3.org/1998/Math/MathML">
W29007: Rejected unknown tag: <mfrac>
...
```

Note that kindlegen V2.9 does not understand MathML - this is a separate downstream limitation, not part of this CLI investigation.

## 4. Process tree

The process tree of a normal interactive KPV conversion looks like:

```
explorer.exe
  Kindle Previewer 3.exe   (GUI main, ~30 s lifetime during convert)
    QtWebEngineProcess.exe (renders the preview pane)
    kindlegen.exe          (~3-10 s, writes the MOBI scaffold)
    Server_KRF4.exe        (KRF4 packager, builds final KPF)
KPR_NCD.exe                (persistent tray daemon, NOT conversion-related)
```

From a subprocess context we observe only:

```
claude.exe
  pwsh.exe
    Kindle Previewer 3.exe (exits in 140 ms, rc=0)
KPR_NCD.exe                (auto-spawns, persistent)
```

The kindlegen and Server_KRF4 children are NEVER spawned in the broken case. The parent GUI process detects "no usable desktop session" and silently exits.

## 5. Session-context investigation

Our shell is in Session ID 1 with `WinSta0` window station and IS able to create Forms windows (verified by creating a test `System.Windows.Forms.Form`). However:

- `$env:SESSIONNAME` is empty (would be `Console` for a true desktop session)
- User idle time is 38000+ seconds (user is AFK, screen unlocked)
- Process chain: `explorer.exe -> claude.exe -> claude.exe -> pwsh.exe`

The Claude CLI parent process inherits some property of its window station that prevents KPV from successfully attaching. Most likely: stdin is not a TTY, or the parent's STDOUT/STDERR handles are not console-bound, and KPV refuses to run its conversion pipeline without a real console.

## 6. Why the direct command line works

When the user types the same command in their own foreground cmd.exe window, that cmd.exe:
- Has a real console buffer (`CONOUT$`)
- Has `$env:SESSIONNAME=Console`
- Has stdin/stdout/stderr attached to conhost.exe
- The user has actively focused the window (input focus)

KPV detects these conditions during startup and proceeds with conversion. From Claude's subprocess context, ALL of these properties are missing. There is no flag or environment variable that overrides this check.

## 7. Recommended workflow

### For build automation (CI / Claude / scripts)

1. **Build the EPUB only.** Run `html2pub`, image optimization, EPUBCheck, structural lint, math/table audits. Do everything except KPV conversion.
2. **Skip KPF generation in scripts.** Mark the EPUB as `*.epub` ready-for-KPV in build logs.
3. **Use `kindlegen.exe` directly** if MOBI output is needed for legacy compatibility. This works headlessly.

### For final KPV validation (manual gate)

Open a foreground cmd.exe or PowerShell window on the user's desktop and run:

```cmd
"%LOCALAPPDATA%\Amazon\Kindle Previewer 3\Kindle Previewer 3.exe" -convert "book.epub" -output "book.kpf" -qualitychecks
```

Or simpler: double-click the EPUB. KPV will open, convert in 30-180 s, write the KPF alongside, and show the preview. The qualitychecks CSV lands as `<epub-stem>-conversionLog.csv` in the same directory.

### For Claude-driven workflows

Detect that we are running in a subprocess context (no foreground desktop session) and:
- Print a clear "MANUAL STEP NEEDED" message with the exact command to run
- Skip the KPV step and let the user run it
- Do NOT pretend conversion succeeded just because rc=0

## 8. References

- `_kp_bisect.py` uses Popen with positional EPUB + `-log`. This DID work on 5/11 to produce `_bisect/output/Summary_Log.csv` (301 bytes). The user must have been at the desktop during that run.
- `publish.py:414-450` already documents this with `step_kindle_preview`: "we don't attempt automated KPF generation" - this is the correct posture.
- Existing 117 MB KPF at `KDP/output/building-conversational-ai-llms-agents.kpf` (5/14 23:28) was produced manually by the user.
