"""Wrapper around Kindle Previewer 3 CLI for headless EPUB -> KPF conversion
+ qualitychecks (the strict Kindle/KFX validator, much stricter than EPUBCheck).

CRITICAL CLI SYNTAX (this tripped us up for a while -- see LESSONS L-KPV-CLI):
    "Kindle Previewer 3.exe" <input.epub> -convert -output <OUTPUT_FOLDER> -qualitychecks
  * The INPUT PATH COMES FIRST.
  * `-convert` is a BARE command (takes no filename).
  * `-output` takes a FOLDER, not a .kpf filename.
Getting the order wrong makes KPV no-op and exit rc=0 in ~2s with no output
(the classic silent failure). Also: do NOT launch it through Git Bash/MSYS --
the worker (KPR_NCD.exe) can hang with no real Windows console. Run it from
PowerShell/cmd or a normal Python subprocess (which spawns the exe directly).

Outputs land UNDER the output folder:
    <out>/KPF/<name>.kpf
    <out>/Logs/<name>_log.csv            (per-book errors/warnings)
    <out>/Logs/<name>_QualityReport.csv  (quality issues / "No issues found.")
    <out>/Summary_Log.csv                (Conversion Status, Error Count, Quality Issue Count)

Usage:
    python kpv_convert.py --epub <input.epub> [--output <folder>] [--timeout 2400]
    python kpv_convert.py --epub <input.epub> --no-qualitychecks

Env override: KINDLE_PREVIEWER = full path to "Kindle Previewer 3.exe"
"""
from __future__ import annotations
import argparse
import csv
import os
import subprocess
import sys
import time
from pathlib import Path


KPV_DEFAULT_PATHS = [
    Path(os.environ.get('KINDLE_PREVIEWER', '')),
    Path(os.environ.get('LOCALAPPDATA', '')) / 'Amazon' / 'Kindle Previewer 3' / 'Kindle Previewer 3.exe',
    Path('C:/Program Files/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe'),
    Path('C:/Program Files (x86)/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe'),
]


def find_kpv() -> Path | None:
    for p in KPV_DEFAULT_PATHS:
        if p and str(p) and p.exists():
            return p
    return None


def kill_stale_workers() -> None:
    """A KPR_NCD.exe ghost from a prior bad launch can wedge the next run."""
    if os.name == 'nt':
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'KPR_NCD.exe'],
                           capture_output=True)
        except Exception:
            pass


def _read_csv_rows(path: Path) -> list[dict]:
    try:
        with path.open(encoding='utf-8-sig', newline='') as f:
            return list(csv.DictReader(f))
    except Exception:
        try:
            with path.open(encoding='utf-8', errors='replace', newline='') as f:
                return list(csv.DictReader(f))
        except Exception:
            return []


def summarize(out_dir: Path) -> dict:
    """Parse Summary_Log.csv + Logs/*.csv under the KPV output folder."""
    res = {'conversion_status': '?', 'error_count': None, 'quality_count': None,
           'errors': [], 'warnings': [], 'quality': [], 'kpf': None}
    kpf_dir = out_dir / 'KPF'
    if kpf_dir.is_dir():
        kpfs = sorted(kpf_dir.glob('*.kpf'))
        if kpfs:
            res['kpf'] = kpfs[0]
    summary = out_dir / 'Summary_Log.csv'
    if summary.exists():
        for row in _read_csv_rows(summary):
            res['conversion_status'] = (row.get('Conversion Status')
                                        or row.get('Status') or res['conversion_status'])
            for k in ('Error Count', 'Errors'):
                if row.get(k) not in (None, ''):
                    try: res['error_count'] = int(row[k])
                    except ValueError: pass
            for k in ('Quality Issue Count', 'Quality Issues', 'Warning Count'):
                if row.get(k) not in (None, ''):
                    try: res['quality_count'] = int(row[k])
                    except ValueError: pass
    logs = out_dir / 'Logs'
    if logs.is_dir():
        for p in logs.glob('*.csv'):
            for row in _read_csv_rows(p):
                sev = (row.get('Type') or row.get('Severity') or '').lower()
                rec = {'code': (row.get('Error Code') or row.get('Code') or '').strip(),
                       'message': (row.get('Description') or row.get('Message') or '').strip(),
                       'location': (row.get('File Name') or row.get('Location') or row.get('File') or '').strip()}
                if 'quality' in p.name.lower():
                    res['quality'].append(rec)
                elif 'error' in sev:
                    res['errors'].append(rec)
                elif 'warn' in sev:
                    res['warnings'].append(rec)
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--epub', type=Path, required=True, help='Input EPUB file')
    ap.add_argument('--output', type=Path, default=None,
                    help='Output FOLDER (default: <epub-dir>/kpv-out)')
    ap.add_argument('--timeout', type=int, default=2400, help='Timeout seconds (default 2400)')
    ap.add_argument('--no-qualitychecks', action='store_true', help='Skip qualitychecks')
    args = ap.parse_args(argv)

    if not args.epub.exists():
        print(f'ERROR: EPUB not found: {args.epub}', file=sys.stderr)
        return 2
    kpv = find_kpv()
    if kpv is None:
        print('ERROR: Kindle Previewer 3 not found. Set KINDLE_PREVIEWER or install it.',
              file=sys.stderr)
        return 3

    out_dir = args.output or (args.epub.parent / 'kpv-out')
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f'Kindle Previewer: {kpv}')
    print(f'EPUB:             {args.epub}')
    print(f'Output folder:    {out_dir}')

    kill_stale_workers()
    # CORRECT order: <input> -convert -output <folder> [-qualitychecks]
    cmd = [str(kpv), str(args.epub), '-convert', '-output', str(out_dir)]
    if not args.no_qualitychecks:
        cmd.append('-qualitychecks')
    print(f'\nRunning: {" ".join(cmd)}')
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=args.timeout)
    except subprocess.TimeoutExpired:
        print(f'\nERROR: KPV timed out after {args.timeout}s', file=sys.stderr)
        kill_stale_workers()
        return 4
    print(f'KPV exited rc={proc.returncode} in {time.time()-t0:.1f}s')

    res = summarize(out_dir)
    print('\n=== KPV CONVERSION + QUALITYCHECKS ===')
    print(f'Conversion status: {res["conversion_status"]}')
    print(f'KPF:               {res["kpf"] or "(none produced)"}')
    if res['error_count'] is not None:
        print(f'Error count:       {res["error_count"]}')
    if res['quality_count'] is not None:
        print(f'Quality issues:    {res["quality_count"]}')
    print(f'Parsed errors={len(res["errors"])} warnings={len(res["warnings"])} quality={len(res["quality"])}')
    for label, items in (('ERROR', res['errors']), ('QUALITY', res['quality'])):
        for r in items[:25]:
            loc = f' @ {r["location"]}' if r['location'] else ''
            print(f'  [{label}{(" "+r["code"]) if r["code"] else ""}] {r["message"][:140]}{loc}')

    # PASS keys on the converter's own verdict + error count, NOT on a .kpf
    # file: KPV's CLI does not always emit a standalone KPF (e.g. KF8 / ET-not-
    # supported books) even when "Conversion Status: Success". The Summary_Log
    # is authoritative; for KDP you upload the EPUB (Amazon converts server-side).
    status_ok = str(res['conversion_status']).strip().lower().startswith('success')
    ok = status_ok and (res['error_count'] in (0, None)) and not res['errors']
    print('\nRESULT:', 'PASS' if ok else 'ISSUES FOUND')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
