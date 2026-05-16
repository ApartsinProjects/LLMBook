"""Fix appendix-o-mlops/index.html section-q.X -> section-o.X refs
(O->Q cascade mistakenly rewrote NEW O appendix's own section links).

Also fix appendix-n-distributed-ml internal section-m.X refs that
should be either section-n.X (within N) or cross-link to
../appendix-m-data-engineering/section-m.X (the actual current home
for old M data sections per the v10 split).

Per the v10 split:
  Old M.1 PySpark              -> new M.1 (Data Engineering)
  Old M.2 Delta Lake           -> new M.2 (Data Engineering)
  Old M.3 Databricks Workspace -> new N.2 (Distributed ML)
  Old M.4 Databricks AI        -> new N.3 (Distributed ML)
  Old M.5 Ray                  -> new N.4 (Distributed ML)
  Old M.6 Feature Stores       -> new M.3 (Data Engineering)
  Old M.7 Production Pipelines -> new M.4 (Data Engineering)

So within appendix-n-distributed-ml/ files, links to:
  section-m.2.html -> ../appendix-m-data-engineering/section-m.2.html (Delta Lake)
  section-m.6.html -> ../appendix-m-data-engineering/section-m.3.html (Feature Stores, was M.6 now M.3)
  section-m.1.html -> ../appendix-m-data-engineering/section-m.1.html (PySpark)
  section-m.7.html -> ../appendix-m-data-engineering/section-m.4.html (Production Pipelines)
  section-m.3.html -> section-n.2.html (within N; Databricks Workspace)
  section-m.4.html -> section-n.3.html (within N; Databricks AI)
  section-m.5.html -> section-n.4.html (within N; Ray)

Idempotent. Run with --apply.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Appendix N internal section-m.X -> rewritten target
N_DIR = ROOT / "appendices" / "appendix-n-distributed-ml"
N_FIXES = {
    'href="section-m.1.html"': 'href="../appendix-m-data-engineering/section-m.1.html"',
    'href="section-m.2.html"': 'href="../appendix-m-data-engineering/section-m.2.html"',
    'href="section-m.6.html"': 'href="../appendix-m-data-engineering/section-m.3.html"',
    'href="section-m.7.html"': 'href="../appendix-m-data-engineering/section-m.4.html"',
    'href="section-m.3.html"': 'href="section-n.2.html"',
    'href="section-m.4.html"': 'href="section-n.3.html"',
    'href="section-m.5.html"': 'href="section-n.4.html"',
}

# Appendix O internal section-q.X -> section-o.X (the v10 cascade mis-renamed
# the O appendix's OWN section links from O.X to Q.X)
O_INDEX = ROOT / "appendices" / "appendix-o-mlops" / "index.html"


def fix_n() -> int:
    if not N_DIR.exists():
        return 0
    edits = 0
    for f in N_DIR.glob("*.html"):
        text = f.read_text(encoding="utf-8")
        orig = text
        for old, new in N_FIXES.items():
            if old in text:
                text = text.replace(old, new)
        if text != orig:
            f.write_text(text, encoding="utf-8")
            edits += 1
    return edits


def fix_o() -> int:
    if not O_INDEX.exists():
        return 0
    text = O_INDEX.read_text(encoding="utf-8")
    orig = text
    # Within appendix-o-mlops/index.html, section-q.X.html should be section-o.X.html
    # AND Section Q.X label should be Section O.X
    for n in range(1, 6):
        text = text.replace(f'href="section-q.{n}.html"', f'href="section-o.{n}.html"')
        text = text.replace(f'Section Q.{n}', f'Section O.{n}')
    if text != orig:
        O_INDEX.write_text(text, encoding="utf-8")
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if args.apply:
        n_edits = fix_n()
        o_edits = fix_o()
        print(f"Appendix N edits: {n_edits}")
        print(f"Appendix O edits: {o_edits}")
    else:
        # Just count
        n_count = 0
        if N_DIR.exists():
            for f in N_DIR.glob("*.html"):
                text = f.read_text(encoding="utf-8")
                for old in N_FIXES:
                    n_count += text.count(old)
        o_count = 0
        if O_INDEX.exists():
            text = O_INDEX.read_text(encoding="utf-8")
            for n in range(1, 6):
                o_count += text.count(f'href="section-q.{n}.html"')
        print(f"DRY-RUN: would fix {n_count} appendix-N refs and {o_count} appendix-O refs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
