"""Fix letter-prefix drift in section <title> and <h1> text across appendices.

After v9 renames, many appendix section files like
`appendices/appendix-m-distributed-ml/section-m.2.html` have:

  <title>Section N.2: Delta Lake and Lakehouse Architecture | ...</title>
  <h1>N.2 Delta Lake and Lakehouse Architecture</h1>
  <meta content="Section N.2: ..." name="description">

while the file is now Section M.2 (the directory is appendix-m-, the
filename is section-m.2.html, the page-current div correctly says
'Section M.2'). The h1 and title carry the OLD letter prefix from
before the rename.

This script:
  1. Walks every appendices/appendix-{letter}-{slug}/section-{letter}.{n}.html
  2. Finds <title>, <h1>, and meta-description text with a letter prefix
     that doesn't match the file's actual letter
  3. Rewrites:
     - <title>Section X.N: Title | ...</title>   (X corrected)
     - <h1>Title</h1>                            (prefix stripped entirely;
                                                  page-current div already
                                                  shows the section number)
     - <meta ... content="Section X.N: ...">     (X corrected)

Skips files where the prefix is already correct.

Idempotent. Run once with --apply.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS = ROOT / "appendices"

SECTION_FILE_RE = re.compile(r"section-([a-z])\.(\d+)\.html$")
APP_DIR_RE = re.compile(r"appendix-([a-z])-")


def fix_file(p: Path, letter: str, num: str, dry_run: bool) -> dict[str, int]:
    """Fix one section file. Returns {'title': N, 'h1': N, 'meta': N}."""
    text = p.read_text(encoding="utf-8")
    orig = text
    changes = {"title": 0, "h1": 0, "meta": 0}
    upper = letter.upper()

    # 1. <title>Section X.N: ... | Building Conversational AI...</title>
    #    Match any single uppercase letter A-Z (or lowercase, just in case)
    def title_repl(m: re.Match) -> str:
        wrong = m.group(1).upper()
        if wrong == upper:
            return m.group(0)
        changes["title"] += 1
        return f'<title>Section {upper}.{num}:{m.group(2)}</title>'
    text = re.sub(
        rf'<title>Section ([A-Za-z])\.{re.escape(num)}:([^<]*)</title>',
        title_repl,
        text,
    )

    # 2. <h1>X.N Title</h1>  ->  <h1>Title</h1>   (strip the wrong prefix
    #    entirely; the page-current div already shows "Section M.N")
    def h1_repl(m: re.Match) -> str:
        wrong = m.group(1).upper()
        rest = m.group(2).strip()
        if wrong == upper:
            # Even if correct, strip the redundant prefix for consistency
            # with chapter index style (h1 = title only).
            changes["h1"] += 1
            return f'<h1>{rest}</h1>'
        changes["h1"] += 1
        return f'<h1>{rest}</h1>'
    text = re.sub(
        rf'<h1>([A-Za-z])\.{re.escape(num)}\s+([^<]*)</h1>',
        h1_repl,
        text,
    )

    # 3. <meta ... content="Section X.N: ...">
    def meta_repl(m: re.Match) -> str:
        wrong = m.group(1).upper()
        if wrong == upper:
            return m.group(0)
        changes["meta"] += 1
        return (f'<meta content="Section {upper}.{num}:{m.group(2)}" '
                f'name="description"/>')
    text = re.sub(
        rf'<meta content="Section ([A-Za-z])\.{re.escape(num)}:([^"]*)" '
        rf'name="description"/>',
        meta_repl,
        text,
    )

    if text != orig and not dry_run:
        p.write_text(text, encoding="utf-8")
    return changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    dry_run = not args.apply

    total = {"title": 0, "h1": 0, "meta": 0}
    n_files = 0
    files_edited = 0

    for app_dir in sorted(APPS.iterdir()):
        if not app_dir.is_dir():
            continue
        adm = APP_DIR_RE.match(app_dir.name)
        if not adm:
            continue
        letter = adm.group(1)

        for sec in sorted(app_dir.glob(f"section-{letter}.*.html")):
            sm = SECTION_FILE_RE.search(sec.name)
            if not sm:
                continue
            file_letter = sm.group(1)
            file_num = sm.group(2)
            # Cross-check: section filename letter must match appendix letter
            if file_letter != letter:
                print(f"WARN: {sec.name} in appendix-{letter}- (skipped)")
                continue
            n_files += 1
            changes = fix_file(sec, letter, file_num, dry_run)
            if any(changes.values()):
                files_edited += 1
                if dry_run:
                    print(f"WOULD fix {sec.relative_to(ROOT)}: {changes}")
            for k in total:
                total[k] += changes[k]

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n=== {mode} ===")
    print(f"Section files scanned: {n_files}")
    print(f"Files with drift:      {files_edited}")
    print(f"Title rewrites:        {total['title']}")
    print(f"h1 rewrites:           {total['h1']}")
    print(f"Meta rewrites:         {total['meta']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
