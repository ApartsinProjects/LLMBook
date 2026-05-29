"""Image pointer sweep for the LLMBook (DISCOVERY + OPTIONAL AUTO-FIX).

Scans every *.html under the book root (minus skips) and finds every
`<img src="...">`. For each, it resolves the src relative to the HTML file
location and checks whether the target exists on disk.

Also examines `<figcaption>` and `<div class="figure-caption">` tags for
"Figure N.M.K" / "Diagram N.M.K" / "Image N.M.K" patterns where N does not
match the file's actual module number (caption drift).

Output: a structured catalog at `broken-images-catalog.md` in the book root.

Auto-fix strategies (tried in order):
  1. Same filename, different module dir (renumber drift) -> rewrite src.
  2. Same filename in sibling module/images dir -> rewrite path.
  3. Filename with extension swap (.svg <-> .png) -> rewrite extension.
  4. Caption-driven renumber: caption says "Figure 38.2.1" but src is
     "images/fig-25.3.1.png" -> if any "fig-38.2.1.*" exists in this or
     nearby module images/, rewrite src and (optionally) caption.
  5. Bare filename in wrong dir -> rewrite relative path.

By default this script runs in --report mode (NO writes). Pass --apply to
actually edit HTML files.

Excluded dirs:
  node_modules, .git, KDP, build, temp_ebook, temp_epub, source_fix_backups,
  pagefind, templates, .claude, .book-update, .html2epub_cache, _concept-figs.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Optional

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIR_NAMES = {
    "node_modules", ".git", "KDP", "build",
    "temp_ebook", "temp_epub", "source_fix_backups",
    "pagefind", "templates", ".claude", ".book-update",
    ".html2epub_cache", "_concept-figs", "__pycache__",
    "scripts", "downloads", "agents", "vendor",
    "_imagegen_work",
}
SKIP_PREFIXES = ("temp_", ".cache_", "_orphans_")


def is_skipped(path: Path) -> bool:
    for part in path.parts:
        if part in SKIP_DIR_NAMES:
            return True
        for prefix in SKIP_PREFIXES:
            if part.startswith(prefix):
                return True
    return False


# ---- Discovery ----

IMG_RE = re.compile(
    r"""<img\b[^>]*?\bsrc\s*=\s*["']([^"'>]+)["'][^>]*?>""",
    re.IGNORECASE | re.DOTALL,
)
IMG_ALT_RE = re.compile(
    r"""<img\b[^>]*?\balt\s*=\s*["']([^"']*)["'][^>]*?>""",
    re.IGNORECASE | re.DOTALL,
)
FIGCAPTION_RE = re.compile(
    r"""<figcaption\b[^>]*>(.*?)</figcaption>""",
    re.IGNORECASE | re.DOTALL,
)
DIV_FIGCAP_RE = re.compile(
    r"""<div\s+class=["'][^"']*figure-caption[^"']*["'][^>]*>(.*?)</div>""",
    re.IGNORECASE | re.DOTALL,
)
FIGNUM_IN_CAPTION_RE = re.compile(
    r"""\b(?:Figure|Diagram|Image|Fig\.)\s+(\d+)\.(\d+)(?:\.(\d+))?""",
    re.IGNORECASE,
)
# In an img src filename: fig-NN.M.K-... or figure-NN.M.K... or NN.M.K
FIG_FILENAME_RE = re.compile(
    r"""(fig|figure|diagram|image)[-_](\d+)\.(\d+)(?:\.(\d+))?""",
    re.IGNORECASE,
)
# Module directory inference: module-NN-...
MODULE_DIR_RE = re.compile(r"^module-(\d+)-")
SECTION_FILE_RE = re.compile(r"^section-(\d+)\.(\d+)\.html$", re.IGNORECASE)

# Optional embedded module ids in captions ("Module 38")
MODULE_IN_CAPTION_RE = re.compile(r"""\bModule\s+(\d+)\b""", re.IGNORECASE)


def find_html_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for p in root.rglob("*.html"):
        if is_skipped(p.relative_to(root)):
            continue
        out.append(p)
    return out


def module_num_for_file(p: Path) -> Optional[int]:
    """Walk up the directory tree until we find a module-NN-... dir."""
    for parent in p.parents:
        m = MODULE_DIR_RE.match(parent.name)
        if m:
            return int(m.group(1))
    return None


def is_appendix_file(p: Path) -> bool:
    """True if the file lives under appendices/."""
    return any(part == "appendices" for part in p.parts)


def section_num_for_file(p: Path) -> Optional[tuple[int, int]]:
    """Return (module, sub) if filename is section-N.M.html."""
    m = SECTION_FILE_RE.match(p.name)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def extract_img_tags(html_text: str) -> list[tuple[int, str, str, str]]:
    """Return [(line_no, src, alt, full_tag), ...] for every <img src='...'>."""
    out = []
    for m in IMG_RE.finditer(html_text):
        line_no = html_text.count("\n", 0, m.start()) + 1
        src = m.group(1).strip()
        full_tag = m.group(0)
        alt_m = IMG_ALT_RE.search(full_tag)
        alt = alt_m.group(1).strip() if alt_m else ""
        out.append((line_no, src, alt, full_tag))
    return out


def extract_captions(html_text: str) -> list[tuple[int, str]]:
    """Return [(line_no, caption_text)] for figcaptions and figure-caption divs."""
    out: list[tuple[int, str]] = []
    for m in FIGCAPTION_RE.finditer(html_text):
        ln = html_text.count("\n", 0, m.start()) + 1
        out.append((ln, m.group(1)))
    for m in DIV_FIGCAP_RE.finditer(html_text):
        ln = html_text.count("\n", 0, m.start()) + 1
        out.append((ln, m.group(1)))
    return out


def resolve_src(html_file: Path, src: str) -> Optional[Path]:
    """Resolve a relative src against the HTML file location. Returns None
    for absolute URLs (http/https/data)."""
    if src.startswith(("http://", "https://", "data:", "//")):
        return None
    # Drop URL fragments / queries
    src_clean = src.split("#", 1)[0].split("?", 1)[0]
    return (html_file.parent / src_clean).resolve()


def _relpath_posix(target: Path, start: Path) -> str:
    """Compute a relative path from start to target, posix slashes.
    Uses os.path.relpath to allow ../ traversal."""
    import os
    rp = os.path.relpath(str(target.resolve()), str(start.resolve()))
    return rp.replace("\\", "/")


# ---- Fix strategies ----

def find_renumber_match(broken_src: str, html_file: Path, current_module: int) -> Optional[str]:
    """Strategy 1: if filename has fig-XX.M.K- pattern with XX != current_module,
    try replacing XX with current_module and see if file exists.
    """
    fname = Path(broken_src).name
    m = FIG_FILENAME_RE.search(fname)
    if not m:
        return None
    old_mod = int(m.group(2))
    if old_mod == current_module:
        return None  # already correct module
    new_fname = (
        fname[: m.start(2)] + str(current_module) + fname[m.end(2):]
    )
    candidate = html_file.parent / Path(broken_src).parent / new_fname
    if candidate.exists():
        return str(candidate.relative_to(html_file.parent)).replace("\\", "/")
    return None


def find_sibling_module_match(broken_src: str, html_file: Path) -> list[str]:
    """Strategy 2: search for the exact filename in any sibling module's
    images/ dir. Returns list of relative paths from html_file."""
    fname = Path(broken_src).name
    candidates: list[Path] = []
    # Walk up to part-N-... root, then scan sibling module-MM dirs
    part_root: Optional[Path] = None
    for parent in html_file.parents:
        if parent.name.startswith("part-") or parent.name == "appendices":
            part_root = parent
            break
    if part_root is None:
        return []
    for img_dir in part_root.rglob("images"):
        if not img_dir.is_dir():
            continue
        target = img_dir / fname
        if target.exists():
            candidates.append(target)
    return [_relpath_posix(c, html_file.parent) for c in candidates]


def find_extension_swap(broken_src: str, html_file: Path) -> Optional[str]:
    """Strategy 3: try .svg <-> .png swap (and a few others)."""
    p = Path(broken_src)
    stem = p.stem
    parent_rel = p.parent
    candidates = []
    if p.suffix.lower() == ".svg":
        candidates = [".png", ".jpg", ".jpeg", ".webp"]
    elif p.suffix.lower() == ".png":
        candidates = [".svg", ".jpg", ".jpeg", ".webp"]
    elif p.suffix.lower() in {".jpg", ".jpeg"}:
        candidates = [".png", ".webp"]
    else:
        return None
    for ext in candidates:
        target = (html_file.parent / parent_rel / (stem + ext)).resolve()
        if target.exists():
            return str(parent_rel / (stem + ext)).replace("\\", "/")
    return None


def find_caption_driven_match(
    broken_src: str,
    caption: Optional[str],
    html_file: Path,
    current_module: int,
) -> Optional[str]:
    """Strategy 4: caption says "Figure N.M.K", search for fig-N.M.K.* nearby."""
    if not caption:
        return None
    m = FIGNUM_IN_CAPTION_RE.search(caption)
    if not m:
        return None
    n = m.group(1)
    sub = m.group(2)
    k = m.group(3)
    if k:
        glob_patterns = [
            f"fig-{n}.{sub}.{k}.*",
            f"figure-{n}.{sub}.{k}.*",
            f"fig-{n}_{sub}_{k}.*",
            f"diagram-{n}.{sub}.{k}.*",
        ]
    else:
        glob_patterns = [
            f"fig-{n}.{sub}.*",
            f"figure-{n}.{sub}.*",
            f"fig-{n}_{sub}.*",
        ]
    # Search this dir's images/, then sibling module images/.
    search_dirs: list[Path] = []
    here_images = html_file.parent / "images"
    if here_images.exists():
        search_dirs.append(here_images)
    # Sibling images under same part
    part_root: Optional[Path] = None
    for parent in html_file.parents:
        if parent.name.startswith("part-") or parent.name == "appendices":
            part_root = parent
            break
    if part_root:
        for img_dir in part_root.rglob("images"):
            if img_dir != here_images:
                search_dirs.append(img_dir)
    for d in search_dirs:
        for pat in glob_patterns:
            matches = list(d.glob(pat))
            # Filter out .orig and .bak twins
            matches = [m for m in matches if not m.name.endswith((".orig", ".bak"))]
            if matches:
                rel = matches[0].relative_to(html_file.parent)
                return str(rel).replace("\\", "/")
    return None


def find_bare_filename(broken_src: str, html_file: Path) -> list[str]:
    """Strategy 5: src is just images/foo.png. Try ANY images/ dir under book root."""
    fname = Path(broken_src).name
    candidates: list[Path] = []
    for img_dir in ROOT.rglob("images"):
        rel = img_dir.relative_to(ROOT)
        if is_skipped(rel):
            continue
        if not img_dir.is_dir():
            continue
        target = img_dir / fname
        if target.exists():
            candidates.append(target)
    return [_relpath_posix(c, html_file.parent) for c in candidates]


# Strategy 6: fuzzy filename matching
# Strip stale chapter prefixes like "ch24-", "ch26-", "ch34-", trailing "-v2",
# "-v3", and figure prefixes like "fig-25.1.3-", "figure-30.5.1-". Then look for
# a unique remaining stem-substring match in any images/ dir.

_PREFIX_RE = re.compile(
    r"""^(ch\d+|fig|figure|diagram|image)[-_.](?:\d+\.\d+(?:\.\d+)?[-_.])?""",
    re.IGNORECASE,
)
_VERSION_SUFFIX_RE = re.compile(r"""[-_]v\d+$""", re.IGNORECASE)
_TRAILING_NUM_RE = re.compile(r"""[-_]\d+$""")


def _normalize_stem(fname: str) -> str:
    """Reduce a filename like 'ch26-sandbox-fishbowl.png' to 'sandbox-fishbowl'."""
    stem = Path(fname).stem
    stem = _PREFIX_RE.sub("", stem)
    stem = _VERSION_SUFFIX_RE.sub("", stem)
    return stem.lower()


def _slug_tokens(stem: str) -> set[str]:
    """Tokenize a slug into informative words (3+ chars, alphanumeric)."""
    tokens = re.split(r"[-_.]+", stem)
    return {t for t in tokens if len(t) >= 3 and t.isalnum()}


GENERIC_STEMS = {
    "chapter-opener", "opener", "part-opener", "module-opener",
    "hero", "banner", "cover", "diagram", "figure",
}


def find_fuzzy_match(broken_src: str, html_file: Path) -> list[tuple[float, str]]:
    """Strategy 6: fuzzy match by normalized stem and shared tokens.

    Returns a ranked list of (score, relative_path) tuples. Top match (if any)
    has highest score. Lower-ranked are weaker. Caller decides on threshold.

    Generic stems (e.g. 'chapter-opener') are skipped to avoid cross-module
    false positives.
    """
    broken_stem = _normalize_stem(Path(broken_src).name)
    if broken_stem in GENERIC_STEMS:
        return []
    broken_tokens = _slug_tokens(broken_stem)
    if not broken_tokens:
        return []
    # Collect all candidate image files
    scored: list[tuple[float, Path]] = []
    seen: set[Path] = set()
    for img_dir in ROOT.rglob("images"):
        rel = img_dir.relative_to(ROOT)
        if is_skipped(rel) or not img_dir.is_dir():
            continue
        for candidate in img_dir.iterdir():
            if not candidate.is_file():
                continue
            if candidate.suffix.lower() not in {".png", ".svg", ".jpg", ".jpeg", ".webp"}:
                continue
            if candidate.name.endswith((".orig", ".bak")):
                continue
            if candidate in seen:
                continue
            seen.add(candidate)
            cand_stem = _normalize_stem(candidate.name)
            cand_tokens = _slug_tokens(cand_stem)
            if not cand_tokens:
                continue
            # Exact normalized stem match -> high score
            if cand_stem == broken_stem:
                score = 100.0
            else:
                overlap = len(broken_tokens & cand_tokens)
                if overlap == 0:
                    continue
                # Jaccard-ish similarity
                union = len(broken_tokens | cand_tokens)
                score = (overlap / union) * 100.0
                # Bonus if all broken tokens are in the candidate
                if broken_tokens.issubset(cand_tokens):
                    score += 20.0
                # Small bonus if candidate's tokens are subset of broken's
                # (means candidate is a simpler/more generic name)
                if cand_tokens.issubset(broken_tokens):
                    score += 10.0
            if score >= 40.0:  # threshold for "plausible"
                scored.append((score, candidate))
    scored.sort(key=lambda x: -x[0])
    result: list[tuple[float, str]] = []
    for score, p in scored[:5]:
        try:
            rel = _relpath_posix(p, html_file.parent)
            result.append((score, rel))
        except ValueError:
            result.append((score, str(p).replace("\\", "/")))
    return result


def is_caption_module_stale(caption: str, current_module: int) -> Optional[tuple[int, int, Optional[int]]]:
    """If the caption has a "Figure N.M.K" with N != current_module, return
    (N, M, K). Else None."""
    m = FIGNUM_IN_CAPTION_RE.search(caption)
    if not m:
        return None
    n = int(m.group(1))
    sub = int(m.group(2))
    k = int(m.group(3)) if m.group(3) else None
    if n != current_module:
        return (n, sub, k)
    return None


# ---- Main ----

class BrokenImage:
    __slots__ = (
        "file", "line", "src", "alt", "caption", "current_module",
        "fix_strategy", "fix_target", "fix_caption_from", "fix_caption_to",
        "candidates_ambiguous", "explanation",
    )

    def __init__(self, file: Path, line: int, src: str, alt: str, caption: Optional[str], current_module: Optional[int]):
        self.file = file
        self.line = line
        self.src = src
        self.alt = alt
        self.caption = caption
        self.current_module = current_module
        self.fix_strategy: Optional[str] = None
        self.fix_target: Optional[str] = None
        self.fix_caption_from: Optional[str] = None
        self.fix_caption_to: Optional[str] = None
        self.candidates_ambiguous: list[str] = []
        self.explanation: Optional[str] = None


def discover(root: Path) -> list[BrokenImage]:
    files = find_html_files(root)
    broken: list[BrokenImage] = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"WARN: cannot read {f}: {e}", file=sys.stderr)
            continue
        imgs = extract_img_tags(text)
        if not imgs:
            continue
        # Build caption index by line number
        captions = extract_captions(text)
        caption_by_line: dict[int, str] = {ln: cap for ln, cap in captions}
        current_module = module_num_for_file(f)
        for line, src, alt, _tag in imgs:
            target = resolve_src(f, src)
            if target is None:
                continue  # external URL
            if target.exists():
                continue
            # Find nearest caption (within next 6 lines)
            cap_text = None
            for delta in range(0, 8):
                if (line + delta) in caption_by_line:
                    cap_text = caption_by_line[line + delta]
                    break
            bi = BrokenImage(f, line, src, alt, cap_text, current_module)
            broken.append(bi)
    return broken


def plan_fixes(broken: list[BrokenImage]) -> None:
    """Annotate each BrokenImage with a fix strategy if one is found."""
    for bi in broken:
        # Strategy 1: renumber (requires module number)
        if bi.current_module is not None:
            target = find_renumber_match(bi.src, bi.file, bi.current_module)
            if target is not None:
                bi.fix_strategy = "renumber"
                bi.fix_target = target
                _maybe_fix_caption(bi)
                continue
            # Strategy 4 (caption-driven) often subsumes 2-3 when caption is right.
            target = find_caption_driven_match(bi.src, bi.caption, bi.file, bi.current_module)
            if target is not None:
                bi.fix_strategy = "caption-driven"
                bi.fix_target = target
                _maybe_fix_caption(bi)
                continue
        # Strategy 3: extension swap
        target = find_extension_swap(bi.src, bi.file)
        if target is not None:
            bi.fix_strategy = "extension-swap"
            bi.fix_target = target
            _maybe_fix_caption(bi)
            continue
        # Strategy 2: sibling module
        cands = find_sibling_module_match(bi.src, bi.file)
        if len(cands) == 1:
            bi.fix_strategy = "sibling-module"
            bi.fix_target = cands[0]
            _maybe_fix_caption(bi)
            continue
        elif len(cands) > 1:
            bi.candidates_ambiguous = cands
        # Strategy 5: bare filename anywhere
        cands2 = find_bare_filename(bi.src, bi.file)
        if len(cands2) == 1:
            bi.fix_strategy = "bare-filename"
            bi.fix_target = cands2[0]
            _maybe_fix_caption(bi)
            continue
        elif len(cands2) > 1 and not bi.candidates_ambiguous:
            bi.candidates_ambiguous = cands2
        # Strategy 6: fuzzy stem match
        fuzzy = find_fuzzy_match(bi.src, bi.file)
        if fuzzy:
            top_score, top_path = fuzzy[0]
            # Strongly dominant top hit -> auto-fix
            # Conditions: top score >= 90 (essentially exact normalized stem)
            # OR top score >= 60 AND next-best is at least 25 points worse.
            second_score = fuzzy[1][0] if len(fuzzy) > 1 else 0.0
            if top_score >= 90.0 or (top_score >= 60.0 and (top_score - second_score) >= 25.0):
                bi.fix_strategy = f"fuzzy-stem (score={top_score:.0f})"
                bi.fix_target = top_path
                _maybe_fix_caption(bi)
                continue
            if not bi.candidates_ambiguous:
                bi.candidates_ambiguous = [f"{s:.0f}: {p}" for s, p in fuzzy]
        # No fix possible
        if not bi.explanation:
            target_path = resolve_src(bi.file, bi.src)
            if target_path is not None:
                bi.explanation = f"no candidate file found anywhere under book root for {Path(bi.src).name}"
            else:
                bi.explanation = "external URL or unresolvable src"


def _maybe_fix_caption(bi: BrokenImage) -> None:
    """If caption has stale module number, set fix_caption_from/to."""
    if not bi.caption or bi.current_module is None:
        return
    stale = is_caption_module_stale(bi.caption, bi.current_module)
    if not stale:
        return
    # Compute the section sub-number from the file name; if not available,
    # try to keep the existing sub from caption.
    sec = section_num_for_file(bi.file)
    if not sec:
        return
    _, sub_from_file = sec
    _, old_sub, old_k = stale
    new_sub = sub_from_file
    new_n = bi.current_module
    if old_k is not None:
        old_str = f"Figure {stale[0]}.{old_sub}.{old_k}"
        new_str = f"Figure {new_n}.{new_sub}.{old_k}"
    else:
        old_str = f"Figure {stale[0]}.{old_sub}"
        new_str = f"Figure {new_n}.{new_sub}"
    # Also handle Diagram / Image
    if "Diagram" in bi.caption:
        old_str = old_str.replace("Figure", "Diagram")
        new_str = new_str.replace("Figure", "Diagram")
    elif "Image" in bi.caption:
        old_str = old_str.replace("Figure", "Image")
        new_str = new_str.replace("Figure", "Image")
    bi.fix_caption_from = old_str
    bi.fix_caption_to = new_str


# ---- Apply fixes ----

def apply_fixes(broken: list[BrokenImage]) -> tuple[int, int]:
    """Edit HTML files in-place. Returns (img_fixes_applied, caption_fixes_applied)."""
    # Group by file
    by_file: dict[Path, list[BrokenImage]] = defaultdict(list)
    for bi in broken:
        if bi.fix_strategy:
            by_file[bi.file].append(bi)
    img_count = 0
    cap_count = 0
    for f, items in by_file.items():
        text = f.read_text(encoding="utf-8", errors="replace")
        original = text
        for bi in items:
            # Rewrite src attribute. Use a precise regex tied to the exact src.
            old_src = bi.src
            new_src = bi.fix_target
            if old_src == new_src:
                continue
            # Build a targeted match that only touches the broken src.
            old_pat = re.compile(
                r"""(<img\b[^>]*?\bsrc\s*=\s*["'])""" +
                re.escape(old_src) +
                r"""(["'])""",
                re.IGNORECASE,
            )
            new_text, n = old_pat.subn(r"\g<1>" + new_src + r"\g<2>", text, count=1)
            if n > 0:
                text = new_text
                img_count += 1
            # Caption fix if applicable
            if bi.fix_caption_from and bi.fix_caption_to:
                if bi.fix_caption_from in text:
                    text = text.replace(bi.fix_caption_from, bi.fix_caption_to, 1)
                    cap_count += 1
        if text != original:
            f.write_text(text, encoding="utf-8")
    return img_count, cap_count


# ---- Caption-only stale numbering scan ----

def find_caption_only_drifts(root: Path) -> list[tuple[Path, int, str, str]]:
    """Captions whose Figure N.M.K has N != current module BUT the image src
    actually resolves. We still want to flag these because they're confusing.
    Returns [(file, line, old_caption_phrase, suggested_phrase)]."""
    out: list[tuple[Path, int, str, str]] = []
    for f in find_html_files(root):
        current_module = module_num_for_file(f)
        if current_module is None:
            continue
        sec = section_num_for_file(f)
        if not sec:
            continue
        sub_from_file = sec[1]
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for ln, cap in extract_captions(text):
            stale = is_caption_module_stale(cap, current_module)
            if not stale:
                continue
            old_n, old_sub, old_k = stale
            if old_k is not None:
                old_str = f"Figure {old_n}.{old_sub}.{old_k}"
                new_str = f"Figure {current_module}.{sub_from_file}.{old_k}"
            else:
                old_str = f"Figure {old_n}.{old_sub}"
                new_str = f"Figure {current_module}.{sub_from_file}"
            out.append((f, ln, old_str, new_str))
    return out


# ---- Reporting ----

def render_catalog(
    broken: list[BrokenImage],
    caption_only_drifts: list,
    out_path: Path,
    applied: bool,
    img_applied: int,
    cap_applied: int,
    prior_autofix_count: int = 0,
) -> None:
    lines: list[str] = []
    lines.append("# Broken Images Catalog")
    lines.append("")
    lines.append(f"Generated by `scripts/_image_pointer_sweep.py`.")
    if applied:
        lines.append(f"Mode: **AUTO-FIX APPLIED** ({img_applied} src rewrites, {cap_applied} caption rewrites).")
    else:
        lines.append("Mode: **READ-ONLY** (re-run with `--apply` to write fixes).")
    if prior_autofix_count:
        lines.append("")
        lines.append(
            f"**Note:** {prior_autofix_count} broken image(s) were auto-fixed in a "
            "prior run of this script; they are not listed below because they no "
            "longer point at missing files."
        )
    lines.append("")
    total = len(broken)
    autofixed = sum(1 for b in broken if b.fix_strategy)
    manual = total - autofixed
    by_dir_manual: dict[str, list[BrokenImage]] = defaultdict(list)
    for b in broken:
        if not b.fix_strategy:
            d = str(b.file.parent.relative_to(ROOT)).replace("\\", "/")
            by_dir_manual[d].append(b)
    lines.append("## Summary")
    lines.append("")
    if applied and prior_autofix_count:
        lines.append(f"- Auto-fixed in this run: **{img_applied}** image src rewrites, **{cap_applied}** caption text rewrites.")
        lines.append(f"- Remaining broken: **{total}**")
    else:
        lines.append(f"- Total broken images still on disk: **{total}**")
        lines.append(f"- Auto-fix planned: **{autofixed}**")
    lines.append(f"- Manual queue: **{manual}** across {len(by_dir_manual)} directories")
    lines.append(f"- Caption-text fixes planned: **{sum(1 for b in broken if b.fix_caption_from)}**")
    lines.append(f"- Caption-only drifts (src works, number stale): **{len(caption_only_drifts)}**")
    lines.append("")
    # Catalog table
    lines.append("## Catalog")
    lines.append("")
    lines.append("| File | Line | Broken src | Caption snippet | Likely intended | Action |")
    lines.append("|---|---|---|---|---|---|")
    for b in sorted(broken, key=lambda x: (str(x.file), x.line)):
        rel = str(b.file.relative_to(ROOT)).replace("\\", "/")
        cap_snip = (b.caption[:60].replace("|", "\\|").replace("\n", " ") + "...") if b.caption else ""
        if b.fix_strategy:
            action = f"AUTOFIX ({b.fix_strategy})"
            intended = b.fix_target or ""
        else:
            action = "MANUAL"
            intended = ""
            if b.candidates_ambiguous:
                action = f"MANUAL (ambiguous, {len(b.candidates_ambiguous)} candidates)"
                intended = "; ".join(b.candidates_ambiguous[:3])
            elif b.explanation:
                intended = "(" + b.explanation + ")"
        lines.append(
            f"| `{rel}` | {b.line} | `{b.src}` | {cap_snip} | `{intended}` | {action} |"
        )
    # Manual queue grouped
    if by_dir_manual:
        lines.append("")
        lines.append("## Manual Queue (grouped by directory)")
        lines.append("")
        lines.append(
            "Each entry includes the alt text and caption already in the HTML, "
            "which can be used as a generation prompt (gemini-imagegen skill) "
            "or removed if the figure is not needed."
        )
        lines.append("")
        for d in sorted(by_dir_manual):
            items = by_dir_manual[d]
            lines.append(f"### {d} ({len(items)})")
            for b in items:
                rel = str(b.file.relative_to(ROOT)).replace("\\", "/")
                lines.append(f"- **{rel}:{b.line}** -> `{b.src}`")
                if b.alt:
                    lines.append(f"  - **alt:** {b.alt[:240]}")
                if b.caption:
                    # Strip HTML tags from caption for readability
                    plain = re.sub(r"<[^>]+>", "", b.caption).strip()
                    lines.append(f"  - **caption:** {plain[:240]}")
                lines.append(f"  - reason: {b.explanation or 'no candidate'}")
            lines.append("")
    # Caption-only drift
    if caption_only_drifts:
        lines.append("")
        lines.append("## Caption-only drift (image renders, figure number stale)")
        lines.append("")
        lines.append("| File | Line | Stale phrase | Suggested |")
        lines.append("|---|---|---|---|")
        for f, ln, old, new in sorted(caption_only_drifts, key=lambda x: (str(x[0]), x[1])):
            rel = str(f.relative_to(ROOT)).replace("\\", "/")
            lines.append(f"| `{rel}` | {ln} | `{old}` | `{new}` |")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Actually edit HTML files. Default is read-only.")
    ap.add_argument(
        "--catalog",
        default=str(ROOT / "broken-images-catalog.md"),
        help="Output catalog markdown file path.",
    )
    args = ap.parse_args()

    print(f"Scanning {ROOT}...", file=sys.stderr)
    broken = discover(ROOT)
    print(f"Found {len(broken)} broken image references.", file=sys.stderr)

    plan_fixes(broken)
    caption_drifts = find_caption_only_drifts(ROOT)

    img_applied = 0
    cap_applied = 0
    prior_autofix_count = 0
    if args.apply:
        img_applied, cap_applied = apply_fixes(broken)
        print(f"Applied {img_applied} src rewrites, {cap_applied} caption rewrites.", file=sys.stderr)
        # Re-discover so the catalog only lists what's still broken.
        post_broken = discover(ROOT)
        plan_fixes(post_broken)
        prior_autofix_count = len(broken) - len(post_broken)
        broken = post_broken

    out = Path(args.catalog)
    render_catalog(
        broken,
        caption_drifts,
        out,
        args.apply,
        img_applied,
        cap_applied,
        prior_autofix_count=prior_autofix_count,
    )
    print(f"Wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
