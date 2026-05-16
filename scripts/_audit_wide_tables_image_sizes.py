"""Wide-cell tables + image-size audit.

READ-ONLY combined audit that produces a single report covering:

1. Wide-cell tables. After the global `table-layout: fixed` -> `auto` change,
   a content-aware browser layout may give one cell most of the table width
   if its text is much longer than the other cells in the same column. For
   every `<table>` in content HTML (excluding KDP/, .claude/, temp_*, scripts/,
   *backups*, node_modules/, pagefind/, templates/), this audit measures the
   rendered text length of every cell, computes a per-column maximum, and
   flags tables where one column's max-length is at least 3x the
   next-largest column's max-length AND the table has at least 3 columns.

2. Oversized images. For every `.png`, `.jpg`, `.jpeg`, `.webp` and `.svg`
   under the project (same skip set), records on-disk size, raster dimensions
   (PIL), SVG byte length, and the presence of embedded base64 data URIs.
   Flags raster > 1 MB OR longest edge > 2000 px, SVG > 100 KB, or any SVG
   that contains `data:image/...;base64,`.

Run from the project root:

    /c/Python314/python scripts/_audit_wide_tables_image_sizes.py

The audit writes findings to `wide-table-image-audit.md` at the project root.
"""
from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup, NavigableString, Tag

try:
    from PIL import Image  # type: ignore
    HAS_PIL = True
except Exception:  # pragma: no cover
    HAS_PIL = False


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "wide-table-image-audit.md"

SKIP_DIR_NAMES = {
    "KDP", ".claude", "scripts", "node_modules", "pagefind", "templates",
    "build", ".git", "__pycache__", "agents", "vendor",
    "source_fix_backups",
}
SKIP_PREFIXES = ("temp_",)
SKIP_NAME_FRAGMENTS = ("backups",)

RASTER_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
ALL_IMG_EXTS = RASTER_EXTS | {".svg"}

# Wide-cell heuristic config.
MIN_COLUMNS = 3
RATIO_THRESHOLD = 3.0
MIN_OUTLIER_CHARS = 60  # don't flag a column that's only "long" by a few chars
SAMPLE_CHAR_LIMIT = 200

# Image flag thresholds.
RASTER_BYTES_LIMIT = 1 * 1024 * 1024  # 1 MB
RASTER_PIXEL_LIMIT = 2000  # longest edge
SVG_BYTES_LIMIT = 100 * 1024  # 100 KB

EMBEDDED_RASTER_RE = re.compile(rb"data:image/[^;]+;base64,", re.IGNORECASE)


def should_skip(p: Path) -> bool:
    parts = set(p.parts)
    if parts & SKIP_DIR_NAMES:
        return True
    for part in p.parts:
        if part.startswith(SKIP_PREFIXES):
            return True
        if any(frag in part for frag in SKIP_NAME_FRAGMENTS):
            return True
    return False


def collect_html_files() -> list[Path]:
    return [p for p in sorted(ROOT.rglob("*.html")) if not should_skip(p)]


def collect_image_files() -> list[Path]:
    out: list[Path] = []
    for ext in ALL_IMG_EXTS:
        out.extend(p for p in ROOT.rglob(f"*{ext}") if not should_skip(p))
    return sorted(set(out))


# ---------------------------------------------------------------------------
# Wide-cell table audit
# ---------------------------------------------------------------------------

@dataclass
class WideFinding:
    file: Path
    line: int
    n_cols: int
    column_index: int  # zero-based
    column_header: str
    column_max_chars: int
    next_max_chars: int
    ratio: float
    sample_text: str


def cell_text(cell: Tag) -> str:
    """Return rendered text length proxy. Strip tags, decode entities,
    collapse whitespace. Long code spans count as their full text since
    they don't wrap by default in `<code>`/`<pre>` (worst case)."""
    text = cell.get_text(separator=" ", strip=True)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def column_count(rows: list[Tag]) -> int:
    n = 0
    for row in rows:
        cells = row.find_all(["td", "th"], recursive=False)
        # account for colspan
        cur = 0
        for c in cells:
            try:
                cur += int(c.get("colspan", 1))
            except (TypeError, ValueError):
                cur += 1
        n = max(n, cur)
    return n


def header_for_column(table: Tag, col_idx: int) -> str:
    """Best-effort: take the column header from the first row that has any
    <th>, or fall back to "(col N)"."""
    for row in table.find_all("tr"):
        ths = row.find_all("th", recursive=False)
        if not ths:
            continue
        # build header row honoring colspan
        expanded: list[str] = []
        for th in ths:
            txt = cell_text(th) or "(blank)"
            try:
                span = int(th.get("colspan", 1))
            except (TypeError, ValueError):
                span = 1
            for _ in range(max(span, 1)):
                expanded.append(txt)
        if col_idx < len(expanded):
            return expanded[col_idx]
        return f"(col {col_idx + 1})"
    return f"(col {col_idx + 1})"


def analyse_table(table: Tag) -> tuple[int, list[int], list[str]] | None:
    """Return (n_cols, per_column_max_chars, per_column_longest_sample).

    Returns None if the table is too small or malformed."""
    rows = table.find_all("tr")
    if not rows:
        return None
    n_cols = column_count(rows)
    if n_cols < MIN_COLUMNS:
        return None

    col_max = [0] * n_cols
    col_sample = [""] * n_cols
    for row in rows:
        cells = row.find_all(["td", "th"], recursive=False)
        col = 0
        for cell in cells:
            try:
                span = int(cell.get("colspan", 1))
            except (TypeError, ValueError):
                span = 1
            if col >= n_cols:
                break
            text = cell_text(cell)
            if len(text) > col_max[col]:
                col_max[col] = len(text)
                col_sample[col] = text
            col += span
    return n_cols, col_max, col_sample


def find_wide_tables(path: Path) -> list[WideFinding]:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    if "<table" not in raw.lower():
        return []
    soup = BeautifulSoup(raw, "html.parser")
    findings: list[WideFinding] = []
    for table in soup.find_all("table"):
        info = analyse_table(table)
        if info is None:
            continue
        n_cols, col_max, col_sample = info
        if not any(col_max):
            continue
        # rank columns by their max char count
        ranked = sorted(range(n_cols), key=lambda i: col_max[i], reverse=True)
        first_idx = ranked[0]
        first_max = col_max[first_idx]
        if first_max < MIN_OUTLIER_CHARS:
            continue
        # find next-largest column that has any content
        runner_up_max = 0
        for idx in ranked[1:]:
            if col_max[idx] > runner_up_max:
                runner_up_max = col_max[idx]
        if runner_up_max == 0:
            ratio = float("inf")
        else:
            ratio = first_max / runner_up_max
        if ratio < RATIO_THRESHOLD:
            continue

        # locate source line of the <table> tag
        line = getattr(table, "sourceline", None) or 0
        header = header_for_column(table, first_idx)
        sample = col_sample[first_idx]
        if len(sample) > SAMPLE_CHAR_LIMIT:
            sample = sample[:SAMPLE_CHAR_LIMIT] + "..."
        findings.append(WideFinding(
            file=path,
            line=line,
            n_cols=n_cols,
            column_index=first_idx,
            column_header=header,
            column_max_chars=first_max,
            next_max_chars=runner_up_max,
            ratio=ratio,
            sample_text=sample,
        ))
    return findings


# ---------------------------------------------------------------------------
# Image audit
# ---------------------------------------------------------------------------

@dataclass
class ImageFinding:
    path: Path
    size_bytes: int
    is_svg: bool
    dimensions: tuple[int, int] | None = None  # (w, h)
    embedded_raster: bool = False
    reasons: list[str] = field(default_factory=list)

    @property
    def longest_edge(self) -> int:
        if not self.dimensions:
            return 0
        return max(self.dimensions)

    @property
    def suggested_action(self) -> str:
        acts: list[str] = []
        if self.is_svg:
            if self.embedded_raster:
                acts.append("extract embedded raster -> external .png/.webp")
            if self.size_bytes > SVG_BYTES_LIMIT and not self.embedded_raster:
                acts.append("minify / simplify paths (svgo)")
            if self.size_bytes > SVG_BYTES_LIMIT and self.embedded_raster:
                acts.append("minify wrapper after extraction")
        else:
            if self.size_bytes > RASTER_BYTES_LIMIT:
                acts.append("re-encode (pngquant / cwebp)")
            if self.longest_edge > RASTER_PIXEL_LIMIT:
                acts.append(f"resize to <= {RASTER_PIXEL_LIMIT}px on longest edge")
        return "; ".join(acts) if acts else "(none)"


def humanise_bytes(n: int) -> str:
    if n >= 1024 * 1024:
        return f"{n / (1024 * 1024):.2f} MB"
    if n >= 1024:
        return f"{n / 1024:.1f} KB"
    return f"{n} B"


def audit_image(p: Path) -> ImageFinding | None:
    try:
        size = p.stat().st_size
    except OSError:
        return None
    ext = p.suffix.lower()
    is_svg = ext == ".svg"
    finding = ImageFinding(path=p, size_bytes=size, is_svg=is_svg)
    if is_svg:
        try:
            data = p.read_bytes()
        except Exception:
            data = b""
        if EMBEDDED_RASTER_RE.search(data):
            finding.embedded_raster = True
            finding.reasons.append("svg-embedded-raster")
        if size > SVG_BYTES_LIMIT:
            finding.reasons.append(f"svg-bytes>{humanise_bytes(SVG_BYTES_LIMIT)}")
    else:
        if HAS_PIL:
            try:
                with Image.open(p) as im:
                    finding.dimensions = im.size  # (w, h)
            except Exception:
                finding.dimensions = None
        if size > RASTER_BYTES_LIMIT:
            finding.reasons.append(f"raster-bytes>{humanise_bytes(RASTER_BYTES_LIMIT)}")
        if finding.longest_edge > RASTER_PIXEL_LIMIT:
            finding.reasons.append(f"raster-edge>{RASTER_PIXEL_LIMIT}px")
    if not finding.reasons:
        return None
    return finding


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def md_escape(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def relpath(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def write_report(
    wide: list[WideFinding],
    images: list[ImageFinding],
    html_count: int,
    image_count: int,
) -> None:
    raster_flags = [i for i in images if not i.is_svg]
    svg_flags = [i for i in images if i.is_svg]
    embedded_svgs = [i for i in svg_flags if i.embedded_raster]

    lines: list[str] = []
    lines.append("# Wide-cell tables and oversized image audit")
    lines.append("")
    lines.append(
        f"Scanned {html_count} HTML files and {image_count} image files. "
        f"Wide-table heuristic: table has at least {MIN_COLUMNS} columns AND "
        f"one column's longest cell is at least {RATIO_THRESHOLD:.0f}x the next-largest "
        f"column's longest cell AND that longest cell has at least {MIN_OUTLIER_CHARS} "
        "characters of rendered text."
    )
    lines.append("")

    # --- Summary tables --------------------------------------------------
    lines.append("## 1. Summary")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("| --- | ---: |")
    lines.append(f"| Wide-cell table findings | {len(wide)} |")
    lines.append(
        f"| Files with at least one wide-cell finding | {len({f.file for f in wide})} |"
    )
    lines.append(f"| Oversized raster images | {len(raster_flags)} |")
    lines.append(f"| Oversized / problematic SVGs | {len(svg_flags)} |")
    lines.append(f"| SVGs with embedded base64 raster | {len(embedded_svgs)} |")
    lines.append("")

    # --- Wide tables -----------------------------------------------------
    lines.append("## 2. Wide-cell tables")
    lines.append("")
    if not wide:
        lines.append("None found.")
        lines.append("")
    else:
        wide_sorted = sorted(wide, key=lambda f: (-f.ratio, str(f.file)))
        lines.append(
            "| File:Line | Cols | Outlier column | Outlier max | Next max | Ratio |"
        )
        lines.append("| --- | ---: | --- | ---: | ---: | ---: |")
        for f in wide_sorted:
            header = md_escape(f.column_header)
            if len(header) > 60:
                header = header[:57] + "..."
            ratio = "inf" if f.ratio == float("inf") else f"{f.ratio:.1f}x"
            lines.append(
                f"| {relpath(f.file)}:{f.line} | {f.n_cols} | "
                f"#{f.column_index + 1} {header} | "
                f"{f.column_max_chars} | {f.next_max_chars} | {ratio} |"
            )
        lines.append("")
        lines.append("### Wide-cell findings (offending text)")
        lines.append("")
        for f in wide_sorted:
            ratio = "inf" if f.ratio == float("inf") else f"{f.ratio:.1f}x"
            lines.append(
                f"- `{relpath(f.file)}:{f.line}` col #{f.column_index + 1} "
                f"`{md_escape(f.column_header)}` (ratio {ratio}, "
                f"{f.column_max_chars} vs {f.next_max_chars} chars):"
            )
            lines.append(f"  > {md_escape(f.sample_text)}")
        lines.append("")

    # --- Oversized images -----------------------------------------------
    lines.append("## 3. Oversized images")
    lines.append("")
    if not raster_flags and not svg_flags:
        lines.append("None found.")
        lines.append("")
    else:
        all_flags = sorted(images, key=lambda i: -i.size_bytes)
        lines.append("| Path | Size | Dimensions | Flags | Suggested action |")
        lines.append("| --- | ---: | --- | --- | --- |")
        for f in all_flags:
            dims = (
                f"{f.dimensions[0]}x{f.dimensions[1]}"
                if f.dimensions else
                ("(svg)" if f.is_svg else "(unknown)")
            )
            reasons = md_escape(", ".join(f.reasons))
            lines.append(
                f"| {relpath(f.path)} | {humanise_bytes(f.size_bytes)} | {dims} | "
                f"{reasons} | {md_escape(f.suggested_action)} |"
            )
        lines.append("")

    # --- Embedded-raster SVGs -------------------------------------------
    lines.append("## 4. Embedded-raster SVGs")
    lines.append("")
    if not embedded_svgs:
        lines.append("None found.")
        lines.append("")
    else:
        lines.append("These SVGs carry one or more `data:image/...;base64,` payloads.")
        lines.append("Extract the raster to a side-car file unless it's intentional.")
        lines.append("")
        lines.append("| Path | SVG size |")
        lines.append("| --- | ---: |")
        for f in sorted(embedded_svgs, key=lambda i: -i.size_bytes):
            lines.append(f"| {relpath(f.path)} | {humanise_bytes(f.size_bytes)} |")
        lines.append("")

    # --- Priority recommendation ----------------------------------------
    lines.append("## 5. Recommended fix priority")
    lines.append("")
    biggest_raster = max(raster_flags, key=lambda i: i.size_bytes, default=None)
    biggest_svg = max(svg_flags, key=lambda i: i.size_bytes, default=None)
    worst_table = max(wide, key=lambda f: f.ratio, default=None)

    bullets: list[str] = []
    bullets.append(
        "1. **Embedded-raster SVGs first**: these are 'silent' bloat. "
        "extract the base64 payload to an external .png/.webp and reference it. "
        f"Currently {len(embedded_svgs)} SVG(s) contain a base64 data URI."
    )
    if biggest_raster is not None:
        bullets.append(
            f"2. **Re-encode the largest rasters** (start with "
            f"`{relpath(biggest_raster.path)}` at {humanise_bytes(biggest_raster.size_bytes)}). "
            "Use `pngquant --quality=70-90 in.png` or convert to `.webp` "
            "(`cwebp -q 80`); aim to halve the bytes per image."
        )
    if any(i.longest_edge > RASTER_PIXEL_LIMIT for i in raster_flags):
        bullets.append(
            f"3. **Downscale anything wider/taller than {RASTER_PIXEL_LIMIT}px** "
            "before re-encoding; Kindle/EPUB readers cap effective resolution near "
            "1200-1600px so larger images just waste bytes."
        )
    if biggest_svg is not None:
        bullets.append(
            f"4. **Minify oversized SVGs** (start with "
            f"`{relpath(biggest_svg.path)}` at {humanise_bytes(biggest_svg.size_bytes)}). "
            "Run through `svgo --multipass`, then re-check for any leftover "
            "embedded raster."
        )
    if worst_table is not None:
        ratio = "inf" if worst_table.ratio == float("inf") else f"{worst_table.ratio:.1f}x"
        bullets.append(
            f"5. **Tackle the worst column-imbalance table next**: "
            f"`{relpath(worst_table.file)}:{worst_table.line}` "
            f"(column #{worst_table.column_index + 1}, ratio {ratio}). "
            "Options: shorten the cell, wrap it in `<div style=\"max-width: 36ch\">`, "
            "or split the content into a follow-up paragraph below the table."
        )
    bullets.append(
        "6. **Adopt a CSS guardrail** for newly-authored tables: add a sensible "
        "`max-width` (e.g. `36ch`-`60ch`) on `<td>`/`<th>` that hold long prose, "
        "so future content-aware layouts don't collapse the other columns."
    )
    bullets.append(
        "7. **Lock the budget**: keep the per-image ceiling at 1 MB raster / "
        "100 KB SVG, and re-run this audit in CI so regressions surface before "
        "the EPUB build trips the ~50 MB KDP cap."
    )

    lines.extend(bullets)
    lines.append("")
    lines.append(f"_Report generated by `scripts/{Path(__file__).name}`._")
    lines.append("")

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    html_files = collect_html_files()
    image_files = collect_image_files()

    print(f"Scanning {len(html_files)} HTML files for wide-cell tables...")
    wide: list[WideFinding] = []
    for i, p in enumerate(html_files, 1):
        if i % 200 == 0:
            print(f"  ... {i}/{len(html_files)}")
        wide.extend(find_wide_tables(p))
    print(f"  -> {len(wide)} wide-cell findings")

    print(f"Scanning {len(image_files)} image files for size/dimension issues...")
    images: list[ImageFinding] = []
    for i, p in enumerate(image_files, 1):
        if i % 500 == 0:
            print(f"  ... {i}/{len(image_files)}")
        f = audit_image(p)
        if f is not None:
            images.append(f)
    print(f"  -> {len(images)} oversized image findings")

    write_report(wide, images, len(html_files), len(image_files))
    print(f"\nReport written to {OUT_PATH}")
    print(
        f"  wide-cell tables: {len(wide)}  "
        f"oversized raster: {sum(1 for i in images if not i.is_svg)}  "
        f"oversized svg: {sum(1 for i in images if i.is_svg)}  "
        f"embedded-raster svg: {sum(1 for i in images if i.is_svg and i.embedded_raster)}"
    )


if __name__ == "__main__":
    main()
