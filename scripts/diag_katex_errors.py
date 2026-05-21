"""Find every equation in the book that KaTeX fails to render.

Replicates html2pub.math_render's extraction (branch 1: span/div.math /
.math-block via get_text; branch 2: $$..$$ / \\(..\\) / \\[..\\] in text nodes)
and the _rewrite_tex pre-pass, then runs each through the SAME render_math.js.
Reports items whose output contains class="katex-error" (KaTeX could not parse).

These are exactly the equations that render as an EMPTY box in the EPUB, because
render() drops katex-error output for placeholder-kind math.

Usage: py -3 scripts/diag_katex_errors.py
"""
import sys, json, subprocess, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "KDP/html2pub/src"))

from bs4 import BeautifulSoup  # noqa: E402
from html2pub.math_render import _rewrite_tex, _strip_delim, RENDER_SCRIPT  # noqa: E402

KATEX = ROOT / "KDP/build/node_modules"

def make_soup(text):
    try:
        return BeautifulSoup(text, "lxml")
    except Exception:
        return BeautifulSoup(text, "html.parser")

items = []   # {id, tex, display}
meta = []    # parallel: {file, raw}

def collect(path: Path):
    soup = make_soup(path.read_text(encoding="utf-8", errors="replace"))
    rel = path.relative_to(ROOT).as_posix()
    # branch 1: span/div whose class contains exactly "math"
    for el in soup.find_all(attrs={"class": True}):
        cls = el.get("class") or []
        if "math" in cls and el.name in ("span", "div"):
            tex_raw = el.get_text()
            tex = _strip_delim(tex_raw)
            if not tex:
                continue
            display = ("math-block" in cls) or tex_raw.strip().startswith("$$")
            mid = str(len(items))
            items.append({"id": mid, "tex": _rewrite_tex(tex, display=display), "display": display})
            meta.append({"file": rel, "raw": tex})
    # branch 2: $$..$$, \(..\), \[..\] in text nodes (skip code/pre/script/style/.math)
    for tn in list(soup.find_all(string=True)):
        parent = tn.parent
        if parent is None:
            continue
        skip = False
        for anc in parent.parents:
            if anc.name in ("code", "pre", "script", "style"):
                skip = True; break
            c = anc.get("class") if anc.name else None
            if c and "math" in c:
                skip = True; break
        if skip:
            continue
        s = str(tn)
        if "$$" not in s and "\\(" not in s and "\\[" not in s:
            continue
        # crude split mirroring _split_text
        pos = 0
        while pos < len(s):
            markers = [(s.find("$$", pos), "$$", "$$", True),
                       (s.find("\\(", pos), "\\(", "\\)", False),
                       (s.find("\\[", pos), "\\[", "\\]", True)]
            markers = [m for m in markers if m[0] >= 0]
            if not markers:
                break
            markers.sort(key=lambda m: m[0])
            start, od, cd, disp = markers[0]
            cp = s.find(cd, start + len(od))
            if cp < 0:
                break
            tex = s[start + len(od):cp].strip()
            if tex:
                mid = str(len(items))
                items.append({"id": mid, "tex": _rewrite_tex(tex, display=disp), "display": disp})
                meta.append({"file": rel, "raw": tex})
            pos = cp + len(cd)

for p in sorted(ROOT.rglob("*.html")):
    sp = p.as_posix()
    if "/_archive/" in sp or "/KDP/" in sp or "/node_modules/" in sp:
        continue
    collect(p)

print(f"collected {len(items)} equations from book HTML")

env = os.environ.copy()
env["NODE_PATH"] = str(KATEX)
proc = subprocess.run(["node", str(RENDER_SCRIPT)], input=json.dumps(items),
                      capture_output=True, text=True, env=env, encoding="utf-8")
if proc.returncode != 0:
    print("render_math.js failed:", proc.stderr[:2000]); sys.exit(1)
rendered = {r["id"]: r for r in json.loads(proc.stdout)}

errors = []
for it in items:
    r = rendered.get(it["id"], {})
    html = r.get("html", "")
    if 'katex-error' in html or r.get("error"):
        errors.append((it, r))

print(f"\n=== {len(errors)} equations FAIL KaTeX (render as empty box) ===\n")
for it, r in errors:
    m = meta[int(it["id"])]
    print(f"FILE: {m['file']}  display={it['display']}")
    print(f"  RAW   : {m['raw'][:200]}")
    print(f"  REWRIT: {it['tex'][:200]}")
    if r.get("error"):
        print(f"  ERROR : {r['error'][:200]}")
    print()
