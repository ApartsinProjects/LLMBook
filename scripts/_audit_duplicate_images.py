"""Duplicate / near-duplicate figure-image audit.

Scope: all .html files under the book root EXCEPT KDP/, .claude/, temp_*,
scripts/, *backups*, node_modules/, pagefind/, templates/.

Detects three categories:

1. Identical ``src=`` referenced from two ``<figcaption>`` figures
   (i.e. two different figures point at the exact same image file path).
2. Bit-identical files at different paths (same SHA-256 over the raw bytes).
3. Near-duplicate raster images (Pillow + imagehash; pHash hamming
   distance <= 4 on resized 8x8 hashes). Skipped silently if imagehash
   is not installed. SVG files are excluded from category 3.

Also detects:

4. Inline ``<svg>`` diagrams whose content is bit-identical between two
   figures in the same HTML file (after stripping IDs and whitespace).
   This catches the Figure 30.4.3 / 30.4.4 anchor case where one SVG was
   pasted twice in the same file with only its ``id`` suffix changed.

Writes the report to ``duplicate-images-audit.md`` at the project root.
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    from PIL import Image  # noqa: F401
    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False

try:
    import imagehash  # type: ignore
    _HAS_IMAGEHASH = True
except ImportError:
    _HAS_IMAGEHASH = False


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "duplicate-images-audit.md"

SKIP_DIR_NAMES = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind", "templates",
    "build", ".git", "source_fix_backups", "__pycache__", "vendor",
    "downloads", "agents",
}
SKIP_PREFIXES = ("temp_",)
SKIP_NAME_FRAGMENTS = ("backups",)

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"}
RASTER_EXTS = {".png", ".jpg", ".jpeg", ".webp"}  # for perceptual hash

# Maximum hamming distance between pHashes to consider a near-duplicate.
NEAR_DUP_HAMMING_THRESHOLD = 4


def should_skip(path: Path) -> bool:
    """Return True if *path* lives under an excluded directory."""
    for part in path.parts:
        if part in SKIP_DIR_NAMES:
            return True
        # Skip any dot-prefixed directory (.git, .claude, .html2pub_cache,
        # .github, .vscode, etc.) — these are tooling/build artifacts.
        if part.startswith(".") and part not in (".", ".."):
            return True
        for prefix in SKIP_PREFIXES:
            if part.startswith(prefix):
                return True
        for frag in SKIP_NAME_FRAGMENTS:
            if frag in part.lower() and part != ROOT.name:
                return True
    return False


# ---------------------------------------------------------------------------
# File hashing
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_image_files() -> list[Path]:
    """All image files under ROOT, minus excluded directories."""
    out: list[Path] = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in IMAGE_EXTS:
            continue
        # Use the path relative to ROOT for the exclusion test, otherwise
        # the project root directory name itself could spuriously match.
        rel = p.relative_to(ROOT)
        if should_skip(rel):
            continue
        out.append(p)
    return out


# ---------------------------------------------------------------------------
# HTML scanning for <figure> elements
# ---------------------------------------------------------------------------

FIGURE_RE = re.compile(
    r"<figure\b[^>]*>(?P<body>.*?)</figure>",
    re.IGNORECASE | re.DOTALL,
)
IMG_SRC_RE = re.compile(
    r"""<img\b[^>]*?\bsrc\s*=\s*['\"](?P<src>[^'\"]+)['\"]""",
    re.IGNORECASE,
)
FIGCAPTION_RE = re.compile(
    r"<figcaption\b[^>]*>(?P<text>.*?)</figcaption>",
    re.IGNORECASE | re.DOTALL,
)
DIAGRAM_CAPTION_RE = re.compile(
    r"<div\s+class\s*=\s*['\"]diagram-caption['\"][^>]*>(?P<text>.*?)</div>",
    re.IGNORECASE | re.DOTALL,
)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
SVG_RE = re.compile(
    r"<svg\b[^>]*>.*?</svg>",
    re.IGNORECASE | re.DOTALL,
)
ID_ATTR_RE = re.compile(r"\b(?:id|filter|url\(#|fill\s*=\s*['\"]url\(#)[^'\"\)]*['\"\)]")
ATTR_VAL_RE = re.compile(r"(['\"])([^'\"]*)\1")


def strip_tags(s: str) -> str:
    return WS_RE.sub(" ", TAG_RE.sub(" ", s)).strip()


def normalize_svg(svg: str) -> str:
    """Normalize an inline ``<svg>`` so that two visually-identical SVGs
    with different ID suffixes hash to the same value.

    Strategy: remove all whitespace, then rewrite every quoted-attribute
    value matching ``id="..."``, ``filter="url(#...)"``, ``fill="url(#...)"``,
    ``stroke="url(#...)"``, mask/clip-path references etc., by mapping each
    distinct local-ID found to a sequential canonical token ``ID0``,
    ``ID1``, ... in order of first appearance. This collapses cosmetic
    suffix renames (e.g. ``stdGrad2`` vs ``stdGrad2_d1``).
    """
    # Collect distinct IDs from id="..." declarations only (definitions).
    id_decls = re.findall(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", svg)
    mapping: dict[str, str] = {}
    for i, ident in enumerate(id_decls):
        if ident not in mapping:
            mapping[ident] = f"ID{i}"
    # Also pull IDs referenced via url(#...) that weren't declared (rare).
    for ident in re.findall(r"url\(#([^)]+)\)", svg):
        if ident not in mapping:
            mapping[ident] = f"ID{len(mapping)}"
    normalized = svg
    # Replace in descending length order so longer IDs are not eaten by
    # a shorter prefix substring of another ID.
    for ident in sorted(mapping, key=len, reverse=True):
        canonical = mapping[ident]
        # id="ident", filter="url(#ident)", href="#ident", fill="url(#ident)"
        normalized = re.sub(
            rf"(['\"#]){re.escape(ident)}(?=['\")\s])",
            rf"\1{canonical}",
            normalized,
        )
    # Collapse whitespace.
    normalized = WS_RE.sub("", normalized)
    return normalized


def extract_figure_label(text: str) -> str:
    """Pull the figure number out of a caption like
    ``Figure 30.4.3 Sector-specific...``."""
    m = re.search(r"(?:Figure|Diagram)\s*([0-9A-Za-z][\w.\-]*)", text)
    if m:
        return f"Figure {m.group(1)}"
    return text[:60].strip()


def scan_html_for_figures() -> tuple[list[dict], list[dict]]:
    """Return (img_records, inline_svg_records).

    Each img_record: ``{file, label, src, abs_src}``.
    Each inline_svg_record: ``{file, label, normalized_hash, raw_svg}``.
    """
    img_records: list[dict] = []
    svg_records: list[dict] = []

    for html_path in ROOT.rglob("*.html"):
        rel = html_path.relative_to(ROOT)
        if should_skip(rel):
            continue
        try:
            text = html_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        # ---- <figure><img src=...><figcaption>...</figcaption></figure> ----
        for m in FIGURE_RE.finditer(text):
            body = m.group("body")
            img_m = IMG_SRC_RE.search(body)
            cap_m = FIGCAPTION_RE.search(body)
            if not img_m:
                continue
            src = img_m.group("src").strip()
            cap_text = strip_tags(cap_m.group("text")) if cap_m else ""
            label = extract_figure_label(cap_text) if cap_text else src
            # Resolve src relative to the HTML file's directory.
            abs_src = None
            if not src.startswith(("http://", "https://", "data:")):
                candidate = (html_path.parent / src).resolve()
                if candidate.exists():
                    abs_src = candidate
            img_records.append({
                "file": str(rel),
                "label": label,
                "src": src,
                "abs_src": abs_src,
            })

        # ---- inline <svg> diagrams paired with a diagram-caption ----
        # We look at occurrences of <svg>...</svg> followed reasonably soon
        # by a <div class="diagram-caption">...</div>. Pair each SVG with
        # the *next* such caption in document order.
        svgs = list(SVG_RE.finditer(text))
        caps = list(DIAGRAM_CAPTION_RE.finditer(text))
        cap_starts = [(c.start(), strip_tags(c.group("text"))) for c in caps]
        for svg_match in svgs:
            svg_body = svg_match.group(0)
            end = svg_match.end()
            # Find first caption whose start is >= end and within 400 chars.
            label = ""
            cap_text_full = ""
            for cap_start, cap_text in cap_starts:
                if cap_start < end:
                    continue
                if cap_start - end > 400:
                    break
                label = extract_figure_label(cap_text)
                cap_text_full = cap_text
                break
            if not label:
                # No caption => not a publication figure, skip.
                continue
            norm = normalize_svg(svg_body)
            h = hashlib.sha256(norm.encode("utf-8")).hexdigest()
            # Caption excerpt for the report (strip the leading "Figure
            # X.Y.Z[: ]" prefix so we don't repeat the label).
            excerpt = re.sub(
                r"^\s*(?:Figure|Diagram)\s+[0-9A-Za-z][\w.\-]*\s*[:.]?\s*",
                "", cap_text_full, count=1).strip()
            excerpt = excerpt[:120] + ("..." if len(excerpt) > 120 else "")
            svg_records.append({
                "file": str(rel),
                "label": label,
                "normalized_hash": h,
                "raw_len": len(svg_body),
                "caption": excerpt,
            })

    return img_records, svg_records


# ---------------------------------------------------------------------------
# Near-duplicate raster detection (optional)
# ---------------------------------------------------------------------------

def compute_phashes(paths: list[Path]) -> dict[Path, "imagehash.ImageHash"]:
    out: dict[Path, "imagehash.ImageHash"] = {}
    if not _HAS_IMAGEHASH:
        return out
    for p in paths:
        if p.suffix.lower() not in RASTER_EXTS:
            continue
        try:
            with Image.open(p) as img:
                # Convert to RGB so we don't break on palette / RGBA edge cases.
                img = img.convert("RGB")
                out[p] = imagehash.phash(img)
        except Exception:
            continue
    return out


def find_near_duplicates(phashes: dict[Path, "imagehash.ImageHash"],
                         exact_hash_groups: dict[str, list[Path]]) -> list[tuple[Path, Path, int]]:
    """Return (a, b, distance) pairs with distance <= threshold, excluding
    pairs that are already exact bit-identical duplicates."""
    # Build a fast lookup: each path's sha256 group, so we can skip pairs
    # already flagged as exact.
    path_to_exact_group: dict[Path, list[Path]] = {}
    for paths in exact_hash_groups.values():
        if len(paths) < 2:
            continue
        for p in paths:
            path_to_exact_group[p] = paths

    items = list(phashes.items())
    pairs: list[tuple[Path, Path, int]] = []
    for i in range(len(items)):
        a_path, a_h = items[i]
        for j in range(i + 1, len(items)):
            b_path, b_h = items[j]
            # Skip if already exact-duplicate of each other.
            grp = path_to_exact_group.get(a_path)
            if grp and b_path in grp:
                continue
            dist = a_h - b_h
            if dist <= NEAR_DUP_HAMMING_THRESHOLD:
                pairs.append((a_path, b_path, dist))
    pairs.sort(key=lambda t: t[2])
    return pairs


# ---------------------------------------------------------------------------
# Report assembly
# ---------------------------------------------------------------------------

def relpath(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def short_hash(h: str) -> str:
    return f"{h[:8]}...{h[-6:]}"


def render_report(image_files: list[Path],
                   hash_groups: dict[str, list[Path]],
                   img_records: list[dict],
                   svg_records: list[dict],
                   near_dup_pairs: list[tuple[Path, Path, int]]) -> str:
    lines: list[str] = []
    lines.append("# Duplicate Images Audit")
    lines.append("")
    lines.append("Auto-generated by `scripts/_audit_duplicate_images.py`. Re-run after edits.")
    lines.append("")

    # ---- Summary ----
    exact_groups = {h: ps for h, ps in hash_groups.items() if len(ps) > 1}
    src_groups: dict[str, list[dict]] = defaultdict(list)
    for r in img_records:
        if r["abs_src"]:
            src_groups[str(r["abs_src"])].append(r)
        else:
            src_groups[r["src"]].append(r)
    dup_src_groups = {k: v for k, v in src_groups.items() if len({(r["file"], r["label"]) for r in v}) > 1}

    svg_groups: dict[str, list[dict]] = defaultdict(list)
    for r in svg_records:
        svg_groups[r["normalized_hash"]].append(r)
    dup_svg_groups = {k: v for k, v in svg_groups.items() if len(v) > 1}

    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("| --- | --- |")
    lines.append(f"| Image files scanned (raster + SVG) | {len(image_files)} |")
    lines.append(f"| Distinct SHA-256 hashes | {len(hash_groups)} |")
    lines.append(f"| Bit-identical file groups (>=2 paths) | {len(exact_groups)} |")
    lines.append(f"| Total redundant image files | {sum(len(ps) - 1 for ps in exact_groups.values())} |")
    lines.append(f"| Figures sharing the same `<img src>` | {sum(len(v) - 1 for v in dup_src_groups.values())} |")
    lines.append(f"| Inline-SVG figure groups with duplicate content | {len(dup_svg_groups)} |")
    if _HAS_IMAGEHASH:
        lines.append(f"| Near-duplicate raster pairs (hamming <= {NEAR_DUP_HAMMING_THRESHOLD}) | {len(near_dup_pairs)} |")
    else:
        lines.append("| Near-duplicate raster pairs | _skipped: imagehash not installed_ |")
    lines.append("")

    # ---- Anchor case: Figure 30.4.3 vs 30.4.4 ----
    lines.append("## Anchor case: Figure 30.4.3 vs Figure 30.4.4")
    lines.append("")
    anchor_file = "part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.4.html"
    anchor_figs = [r for r in svg_records
                   if r["file"].replace("\\", "/") == anchor_file
                   and r["label"] in ("Figure 30.4.3", "Figure 30.4.4")]
    if len(anchor_figs) == 2:
        a, b = anchor_figs
        same = a["normalized_hash"] == b["normalized_hash"]
        lines.append("Both figures use an inline `<svg>` (no `<img src>`), so this is an inline-content duplication, not a file duplication.")
        lines.append("")
        lines.append(f"- **{a['label']}** caption: \"Sector-specific regulations layer on top of general AI regulations...\"")
        lines.append(f"  - File: `{a['file']}`")
        lines.append(f"  - Normalized SVG SHA-256: `{a['normalized_hash']}`")
        lines.append(f"  - Raw SVG length: {a['raw_len']} chars")
        lines.append(f"- **{b['label']}** caption: \"Regulatory approaches vary significantly by jurisdiction...\"")
        lines.append(f"  - File: `{b['file']}`")
        lines.append(f"  - Normalized SVG SHA-256: `{b['normalized_hash']}`")
        lines.append(f"  - Raw SVG length: {b['raw_len']} chars")
        lines.append("")
        lines.append(f"**Verdict:** {'SAME diagram (only `id` suffixes differ)' if same else 'DIFFERENT diagrams'}.")
        lines.append("")
        if same:
            lines.append("The prose before Figure 30.4.4 promises a side-by-side comparison of EU, US, and other major regulatory frameworks, but the SVG actually rendered is the Sector-Specific Regulations diagram (healthcare/finance/education) from Figure 30.4.3 with renamed gradient/filter IDs. **A genuine cross-jurisdiction comparison diagram must be authored to replace the duplicated SVG.**")
            lines.append("")
    else:
        lines.append(f"Could not locate both anchor figures in `{anchor_file}` (found {len(anchor_figs)} matching figcaptions).")
        lines.append("")

    # ---- 1. Figures referencing the same <img src> ----
    lines.append("## 1. Figures referencing the same `<img src>`")
    lines.append("")
    if dup_src_groups:
        lines.append("Two or more `<figure>` elements (or `<figcaption>`-bearing structures) point at the same image. Most legitimate cases are part-opener and chapter-opener images; treat the rest as suspicious.")
        lines.append("")
        for key, group in sorted(dup_src_groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            # Render a short banner for the key.
            try:
                display_key = relpath(Path(key))
            except Exception:
                display_key = key
            lines.append(f"### `{display_key}` — {len(group)} references")
            lines.append("")
            for r in group:
                lines.append(f"- `{r['file']}` — {r['label']}")
            lines.append("")
    else:
        lines.append("None found.")
        lines.append("")

    # ---- 2. Bit-identical files at different paths ----
    lines.append("## 2. Bit-identical files at different paths (SHA-256)")
    lines.append("")
    if exact_groups:
        lines.append("Same bytes stored under multiple paths. Candidates for consolidation.")
        lines.append("")
        for h, ps in sorted(exact_groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            size = ps[0].stat().st_size
            lines.append(f"### {short_hash(h)} ({len(ps)} copies, {size:,} bytes each)")
            lines.append("")
            for p in sorted(ps):
                lines.append(f"- `{relpath(p)}`")
            lines.append("")
    else:
        lines.append("None found.")
        lines.append("")

    # ---- 3. Inline-SVG duplicates ----
    lines.append("## 3. Duplicate inline `<svg>` figures (normalized content)")
    lines.append("")
    if dup_svg_groups:
        lines.append("Inline SVG diagrams whose content is bit-identical after stripping IDs and whitespace. The Figure 30.4.3 / 30.4.4 case is included here.")
        lines.append("")
        for h, group in sorted(dup_svg_groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            lines.append(f"### Normalized SVG hash {short_hash(h)} ({len(group)} occurrences)")
            lines.append("")
            # Detect duplicate labels within this group (figure-numbering conflict).
            label_counts: dict[str, int] = defaultdict(int)
            for r in group:
                label_counts[r["label"]] += 1
            dup_labels = [lbl for lbl, n in label_counts.items() if n > 1]
            if dup_labels:
                lines.append(f"  - **WARNING:** same label used more than once: {', '.join(dup_labels)}")
            for r in group:
                cap = f" — \"{r['caption']}\"" if r.get("caption") else ""
                lines.append(f"- `{r['file']}` — {r['label']}{cap}")
            lines.append("")
        # Also scan for figure-numbering conflicts that are NOT also content
        # duplicates (e.g. the same caption label re-used twice in one file
        # with different inline diagrams).
        per_file_labels: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for r in svg_records:
            per_file_labels[(r["file"], r["label"])].append(r)
        numbering_conflicts = {k: v for k, v in per_file_labels.items() if len(v) > 1}
        if numbering_conflicts:
            lines.append("### Figure-numbering conflicts (same label, possibly different content)")
            lines.append("")
            for (fpath, lbl), rs in sorted(numbering_conflicts.items()):
                hashes = sorted({r["normalized_hash"][:8] for r in rs})
                same_content = "same content" if len(hashes) == 1 else "different content"
                lines.append(f"- `{fpath}` has {len(rs)} figures labeled **{lbl}** ({same_content}, hashes: {', '.join(hashes)})")
            lines.append("")
    else:
        lines.append("None found.")
        lines.append("")

    # ---- 4. Near-duplicate rasters ----
    lines.append("## 4. Near-duplicate raster images (pHash)")
    lines.append("")
    if not _HAS_IMAGEHASH:
        lines.append("Skipped: the `imagehash` package was not available at audit time.")
        lines.append("")
    elif near_dup_pairs:
        lines.append(f"Pairs of raster images with Hamming distance <= {NEAR_DUP_HAMMING_THRESHOLD} on 8x8 perceptual hashes. Excludes pairs already listed as bit-identical above.")
        lines.append("")
        lines.append("| Hamming | File A | File B |")
        lines.append("| --- | --- | --- |")
        for a, b, d in near_dup_pairs[:200]:
            lines.append(f"| {d} | `{relpath(a)}` | `{relpath(b)}` |")
        if len(near_dup_pairs) > 200:
            lines.append("")
            lines.append(f"_({len(near_dup_pairs) - 200} additional pairs omitted)_")
        lines.append("")
    else:
        lines.append("No near-duplicates found within threshold.")
        lines.append("")

    # ---- Recommended fix priority ----
    lines.append("## Recommended fix priority")
    lines.append("")
    fixes: list[str] = []
    anchor_same = (
        len(anchor_figs) == 2
        and anchor_figs[0]["normalized_hash"] == anchor_figs[1]["normalized_hash"]
    )
    if anchor_same:
        fixes.append("**(P0)** Replace the duplicated SVG used as Figure 30.4.4 in `part-9-safety-strategy/module-30-safety-ethics-regulation/section-30.4.html` with an actual EU vs US vs other-jurisdictions comparison diagram. The current SVG is a copy of Figure 30.4.3 with only its gradient/filter IDs renamed.")
    if dup_svg_groups and len(dup_svg_groups) > (1 if anchor_figs else 0):
        fixes.append("**(P1)** Review the other duplicate inline-SVG groups in Section 3; each pair is either a legitimate before/after diagram, or a copy-paste mistake similar to the anchor case.")
    if dup_src_groups:
        fixes.append("**(P2)** Audit Section 1 visually. Chapter / part openers shared across many files are expected; an image shared between two figures in the same chapter usually indicates a missed caption update.")
    if exact_groups:
        fixes.append("**(P3)** Consolidate the bit-identical files in Section 2: keep one canonical location per asset and update references.")
    if _HAS_IMAGEHASH and near_dup_pairs:
        fixes.append("**(P4)** Spot-check the near-duplicate pairs in Section 4: many will be regenerations of the same diagram at different sizes (safe to keep) but some may be unintended reuses.")
    if not fixes:
        fixes.append("No structural issues found.")
    for f in fixes:
        lines.append(f"- {f}")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print(f"Scanning {ROOT}...")
    image_files = scan_image_files()
    print(f"  {len(image_files)} image files found")

    print("Hashing files...")
    hash_groups: dict[str, list[Path]] = defaultdict(list)
    for p in image_files:
        try:
            hash_groups[sha256_file(p)].append(p)
        except OSError as exc:
            print(f"  ! failed to hash {p}: {exc}", file=sys.stderr)

    print("Scanning HTML for <figure> elements...")
    img_records, svg_records = scan_html_for_figures()
    print(f"  {len(img_records)} <figure><img> records, {len(svg_records)} inline-svg figure records")

    near_dup_pairs: list[tuple[Path, Path, int]] = []
    if _HAS_IMAGEHASH and _HAS_PIL:
        print("Computing perceptual hashes for raster images...")
        phashes = compute_phashes(image_files)
        print(f"  {len(phashes)} raster phashes computed")
        near_dup_pairs = find_near_duplicates(phashes, hash_groups)
        print(f"  {len(near_dup_pairs)} near-duplicate pairs (hamming <= {NEAR_DUP_HAMMING_THRESHOLD})")
    else:
        print("(imagehash not available; skipping near-duplicate analysis)")

    report = render_report(image_files, hash_groups, img_records, svg_records, near_dup_pairs)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
