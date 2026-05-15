"""Parse KPV's qualitychecks CSV log and report findings.

KPV writes <epub-stem>-conversionLog.csv alongside the EPUB when run
with `-qualitychecks`. The format is:
  "Type","Description"
  "Status","Book conversion successful."

For books with issues, additional rows appear:
  "Error","E21018: ..."
  "Warning","..."
  "Notice","..."

This script:
1. Locates the latest conversionLog.csv next to the EPUB
2. Parses rows, counts by Type and known E-code
3. Prints a summary and exits non-zero on errors

Usage:
  python _kpv_parse_log.py <epub-path>
  python _kpv_parse_log.py                    # uses default LLMBook EPUB
"""
import csv
import re
import sys
from pathlib import Path


DEFAULT_EPUB = Path('E:/Projects/BookBlogsHome/LLMBook/KDP/output/'
                    'building-conversational-ai-llms-agents.epub')


def parse_log(log_path: Path) -> dict:
    counts = {'Error': 0, 'Warning': 0, 'Notice': 0, 'Info': 0, 'Status': 0}
    by_code = {}
    rows = []
    with log_path.open(encoding='utf-8-sig', newline='') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            t = row.get('Type', '').strip()
            d = row.get('Description', '').strip()
            counts[t] = counts.get(t, 0) + 1
            # Extract E-code if present (E21018, RSC-005, OPF-029, etc.)
            m = re.match(r'^([A-Z]{1,4}-?\d{3,5})[:\s]', d)
            code = m.group(1) if m else None
            if code:
                by_code[code] = by_code.get(code, 0) + 1
            rows.append({'type': t, 'description': d, 'code': code})
    return {'counts': counts, 'by_code': by_code, 'rows': rows}


def main():
    epub = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_EPUB
    log = epub.parent / f'{epub.stem}-conversionLog.csv'
    if not log.exists():
        print(f'ERROR: log not found at {log}', file=sys.stderr)
        print(f'(KPV writes this file alongside the EPUB when run with '
              f'-qualitychecks. If you ran KPV GUI without that flag, the '
              f'log may not exist.)')
        return 2

    print(f'Parsing: {log}')
    print(f'  Size: {log.stat().st_size} bytes')
    print(f'  Mtime: {log.stat().st_mtime}')
    print()

    result = parse_log(log)
    print('=== Summary by Type ===')
    for t, n in sorted(result['counts'].items(), key=lambda kv: -kv[1]):
        if n > 0:
            print(f'  {t}: {n}')

    if result['by_code']:
        print('\n=== By KPV E-code ===')
        for code, n in sorted(result['by_code'].items(), key=lambda kv: -kv[1]):
            print(f'  {code}: {n}')

    n_errors = result['counts'].get('Error', 0)
    n_warnings = result['counts'].get('Warning', 0)
    n_notices = result['counts'].get('Notice', 0)

    if n_errors > 0:
        print('\n=== Errors (top 30) ===')
        for r in result['rows']:
            if r['type'] == 'Error':
                print(f'  - {r["description"][:200]}')

    if n_warnings > 0 and n_warnings < 20:
        print('\n=== Warnings (top 20) ===')
        for r in result['rows']:
            if r['type'] == 'Warning':
                print(f'  - {r["description"][:200]}')

    print()
    print(f'Total: {n_errors} errors / {n_warnings} warnings / {n_notices} notices')

    if n_errors > 0:
        print('FAIL: errors present')
        return 1
    if n_warnings > 0:
        print('WARN: warnings present (review)')
        return 0
    print('PASS: 0 errors')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
