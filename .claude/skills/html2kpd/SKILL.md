---
name: html2kpd
description: Convert HTML book sources into a Kindle-validated KPF file via the EPUB to KPF pipeline (html2pub + Kindle Previewer 3 + EPUBCheck + KPV qualitychecks). Use when the user has built an EPUB and needs to ship to Amazon KDP, or wants to ensure KPV passes 0 errors. Triggers on "convert to KPF", "kindle previewer", "ship to KDP", "html2kpd", "qualitychecks", or any time the build needs to pass Kindle validation.
version: 1.0
---

# html2kpd Skill

## What this skill does

Converts HTML book sources (already organized into a tree of part / module / section pages) into a **Kindle-validated KPF (.kpf) file** by orchestrating the full pipeline:

```
HTML sources  -- html2pub -->   EPUB 3        (validated by EPUBCheck)
                                  |
                                  v
                          Kindle Previewer 3
                          (-convert -qualitychecks)
                                  |
                                  v
                                .kpf           (validated by KPV qualitychecks)
                                  |
                                  v
                           Amazon KDP upload
```

The skill exists because Kindle's KFX/Mobi converter is significantly stricter than EPUBCheck. An EPUB that passes EPUBCheck cleanly may still produce dozens of E21018, E3005, RSC-005, OPF-029 errors when fed to Kindle Previewer. This skill captures the lessons learned across many KPV-iteration cycles so that the next book ships smoothly.

## Overview: what is a KPF?

- **KPF (.kpf)** is Amazon's enhanced typesetting format produced by Kindle Previewer 3. Upload one to KDP for the highest-fidelity ebook delivery (vs. uploading an EPUB and letting KDP convert).
- KPV (Kindle Previewer) bundles a **qualitychecks** engine that runs against the converted .kpf. Common error codes:
  - **E21018**: invalid attribute / unparseable HTML inside an element
  - **E3005**: malformed XHTML (entity, self-closing non-void, etc.)
  - **E25001**: malformed or unsupported image
  - **RSC-005**: schema violation (MathML attribute, missing required attr)
  - **OPF-029**: manifest item href and media-type mismatch
  - **HTM-009**: invalid CSS property
  - **NCX-001 / NAV-001**: navigation document issues

## Common KPV errors and their fixes

| Code | Symptom | Fix |
|---|---|---|
| E21018 | `<img style="height: auto">` | Strip inline `style` from `<img>` (see `fix_img_for_kindle`) |
| E21018 | `<span class="x"/>` self-closing | Post-write XHTML pass: `<(span\|div\|p\|a\|td\|th\|li\|strong\|em\|b\|i\|sub\|sup\|small\|code\|pre)(\s[^>]*\|)/>` to expand |
| E21018 | HTML entity in `alt` attr (`-&gt;`) | Replace `->` with `→` in alt before serialization |
| E3005 | KaTeX MathML `<mtable columnspacing="">` | Drop empty layout attrs on `<mtable>` |
| E3005 | KaTeX `\max`/`\min` in subscript: `<msub>...<mo>&#x2061;</mo></msub>` | Strip invisible operators (U+2061..U+2064) as direct children of `msub`/`msup`/`msubsup` |
| RSC-005 | `viewbox` lowercase on `<svg>` | Rename to `viewBox` (camelCase) |
| OPF-029 | `<item href="x.jpg" media-type="image/png">` | Sync media-type when post-processor converts PNG to JPG; remember OPF hrefs are relative, ZIP entries are absolute |
| HTM-009 | `padding: nullem` / `nanem` | CSS sanitizer: replace `(null\|nan\|undefined)em` with `0`, `min/max/fit-content` with `auto`, drop `box-shadow`/`gap`/`transition`/`transform` |
| E25001 | RGBA PNG with alpha=255 everywhere | Convert to JPEG; update OPF media-type |

## Tooling

### Kindle Previewer 3

Locate it via env or known paths:

```python
candidates = [
    Path(os.environ.get("KINDLE_PREVIEWER", "")),  # if set
    Path(os.environ.get("LOCALAPPDATA", "")) / "Amazon" / "Kindle Previewer 3" / "Kindle Previewer 3.exe",
    Path("C:/Program Files/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe"),
    Path("C:/Program Files (x86)/Amazon/Kindle Previewer 3/Kindle Previewer 3.exe"),
]
```

KPV has a headless CLI (since v3.32). **Argument order is strict and is the #1 cause of silent failure** (see LESSONS L-KPV-CLI):

```
"Kindle Previewer 3.exe" <input.epub> -convert -output <OUTPUT_FOLDER> -qualitychecks
```

- INPUT PATH COMES FIRST. `-convert` is a BARE command (no filename). `-output` takes a **FOLDER**, not a `.kpf` file.
- Wrong order (e.g. `-convert input.epub -output out.kpf`) -> KPV no-ops, exits rc=0 in ~2s, produces nothing. That's the silent trap.
- Do NOT launch through Git Bash/MSYS (worker `KPR_NCD.exe` hangs with no real console). Use PowerShell `Start-Process -Wait -NoNewWindow`, `cmd.exe`, or a direct Python `subprocess.run` (NOT via a bash shim). Kill stale `KPR_NCD.exe` before each run.

Outputs land UNDER the output folder (NOT the workspace):

```
<out>/KPF/<name>.kpf
<out>/Logs/<name>_log.csv            (errors/warnings)
<out>/Logs/<name>_QualityReport.csv  (quality issues)
<out>/Summary_Log.csv                (Conversion Status, Error Count, Quality Issue Count)
```

Gate publishing on `Summary_Log.csv` `Error Count` == 0. (`scripts/kpv_convert.py` does all of this.)
KindleGen is retired (2020) and KDP no longer accepts MOBI -- don't use it. KDP DOES accept EPUB and KPF; an EPUBCheck-clean EPUB uploaded to KDP (Amazon converts to KFX server-side) is a valid fallback if KPV CLI misbehaves in CI.

The output filename is derived from the input name. The exit code is 0 even on errors; parse the workspace log to detect failures.

### EPUBCheck

Bundled IDPF validator. Locate via:

```python
candidate_dirs = [
    Path(os.environ.get("EPUBCHECK_HOME", "")),
    Path("E:/Tools/epubcheck"),
    Path.home() / "epubcheck",
    Path.home() / ".local" / "share" / "epubcheck",
    Path("C:/Program Files/epubcheck"),
    Path("/usr/local/share/epubcheck"),
]
# look for epubcheck-*/epubcheck.jar inside, plus bundled jdk-*/bin/java(.exe)
```

Invoke:

```
java -Djava.io.tmpdir=<tmp> -jar epubcheck.jar <input.epub>
```

Exit code 0 = clean. Output report is plain text.

## Workflow

The recommended pipeline order:

1. **Source audit pass** (read-only): run the `audit_*.py` scripts to flag KPV-risky patterns BEFORE building. Cheap to fix in source HTML; expensive to chase after KPF conversion.
2. **EPUB build** (`html2pub`): see the `html2pub` skill. Wire the project's `_html2pub_hooks.py` with `fix_math_alignment`, `fix_svg_viewbox`, `fix_img_for_kindle`, `wrap_wide_tables`, `strip_code_block_whitespace`, etc.
3. **EPUB optimize** (Python ZIP rewrite): apply the CSS sanitizer (`replace_kindle_unsupported_css`), entity repair (`&apos;` to `&apos;`), self-close expansion. The output remains a valid EPUB.
4. **EPUBCheck**: 0 errors. Warnings tolerable.
5. **KPF conversion** (`kpv_convert.py`): call Kindle Previewer with `-convert -qualitychecks`.
6. **KPV qualitychecks parse**: parse the workspace log for E-codes. 0 errors required to ship.
7. **Smoke test** (`kpv_smoke_test.py`): on a 20-page subset first; if clean, proceed to full conversion.

### Sequencing notes

- **Hook order matters**. In `_html2pub_hooks.py`, run `math_render` BEFORE `post_process_html` so KaTeX artifacts (ZWSPs, empty .vlist-s) are cleaned up. Reverse order silently leaves tofu in the output.
- **OPF media-type sync** must happen AFTER any image-rename step (PNG to JPG). OPF refs are relative (`styles/icons/foo.jpg`), ZIP entries are absolute (`EPUB/styles/icons/foo.jpg`); build the rename map keyed by both.
- **CSS sanitizer** runs on the OPTIMIZED EPUB, not the source CSS. Replace `nullem`/`nanem`/`min-content`/`box-shadow`/`gap`/`transition`/`transform` with neutral values; don't delete declarations (breaks CSS syntax).
- **ZIP rewrite preserves mimetype-first-uncompressed**: the first file in any EPUB must be `mimetype` with `ZIP_STORED` (no compression). All other files use `ZIP_DEFLATED`.

## Validation checks beyond KPV

These are the source-level checks worth running BEFORE the KPV step. Skipping them means you spend hours debugging KPV reports of issues that audit scripts would have caught in 30 seconds.

- **Navigation chain integrity** (`audit_navigation.py`): every prev href points to an existing file; A.next = B implies B.prev = A; no cross-part backwards loops.
- **Phantom index cards** (`audit_phantom_cards.py`): duplicate resolved hrefs in `<a class="section-card">` lists; cards pointing to non-existent files; mismatch between card title and target file `<h1>`.
- **Stale section number labels** (`audit_stale_refs.py`): subsection labels "32.1.x" inside `section-30.1.html` after a renumber; inline "Section X.Y" refs where X.Y does not exist.
- **Math KPV risks** (`audit_math_kpv.py`): MathML wrapped in non-empty `<p>` (HTML5 auto-close bug); `<mtable columnspacing="">`; invisible function-application `<mo>` as third `<msub>` child; deeply nested mfrac.
- **Table KPV risks** (`audit_tables_kpv.py`): wide tables (>=6 cols, sometimes >=4 cols); tables with images/code inside; tables with rowspan/colspan; tables not wrapped in `.comparison-table` or `.table-wrapper`.
- **Code block whitespace** (`audit_code_indent.py`): leading/trailing blank lines in `<pre><code>` (renders as visible empty space at top of code panels); mixed tab/space.

## Image format economics

For KDP 70% royalty plan:

- `delivery_fee_per_sale = 0.15 × size_MB`
- `net_royalty = 0.70 × (list_price − delivery_fee_per_sale)`
- At $9.99 list: 50 MB ships at $1.74/sale; 30 MB at $3.84/sale.
- Above ~67 MB the curve goes negative.

Tactics:
- PNG to JPEG when alpha is binary (matplotlib/Mermaid white-bg). Many "RGBA" PNGs have alpha=255 everywhere.
- JPEG re-encode at q=72 (visually indistinguishable from q=82).
- `max_side` cap at 1400 for diagrams, 1000 for photos.
- After PNG to JPG rename, both `<item href>` AND `media-type` in `content.opf` need updating, keyed by the OPF-relative form.

## Trigger keywords

This skill activates when the user mentions:

- "convert to KPF" / "build KPF" / "make KPF"
- "kindle previewer" / "KPV"
- "qualitychecks" / "kpv qualitychecks"
- "ship to KDP" / "KDP submission" / "amazon KDP"
- "html2kpd"
- "validate kindle" / "kindle validation"
- "fix E21018" / "fix RSC-005" / any KPV error code
- "phantom cards" / "broken nav chain" / "stale section numbers"

## When to NOT use this skill

- Plain HTML to EPUB only (no Kindle target) -> use `html2pub` directly.
- One-shot Markdown to EPUB -> use `pandoc`.
- PDF generation -> separate tool (Edge headless, Chromium, Prince).
- Reflow audit on web book -> standard accessibility tools.

## Reference: the package files

- `SKILL.md` (this file): overview, error map, workflow.
- `LESSONS.md`: 25+ specific lessons extracted from production builds.
- `CSS_SNIPPETS.md`: copy-paste CSS patterns that fix common Kindle layout issues.
- `scripts/`:
  - `audit_navigation.py`: prev/next chain integrity (cross-module, cross-part).
  - `audit_phantom_cards.py`: duplicate index-card hrefs.
  - `audit_math_kpv.py`: math patterns that trip KPV.
  - `audit_tables_kpv.py`: wide tables, math-in-tables, code-in-tables.
  - `audit_code_indent.py`: leading/trailing blank lines, over-indent.
  - `audit_stale_refs.py`: Section X.Y where X.Y has no file.
  - `fix_nav_chain.py`: sequential prev/next rebuild.
  - `fix_phantom_cards.py`: dedup + reorder.
  - `kpv_convert.py`: wrapper around Kindle Previewer CLI.
  - `kpv_smoke_test.py`: small subset test before full conversion.

## Quick start

```bash
# 1. Audit source (find KPV-risky patterns before build)
python <skill>/scripts/audit_navigation.py --root <book-root>
python <skill>/scripts/audit_phantom_cards.py --root <book-root>
python <skill>/scripts/audit_math_kpv.py --root <book-root>
python <skill>/scripts/audit_tables_kpv.py --root <book-root>
python <skill>/scripts/audit_code_indent.py --root <book-root>
python <skill>/scripts/audit_stale_refs.py --root <book-root>

# 2. Apply fixes (read-only by default; --apply to write)
python <skill>/scripts/fix_nav_chain.py --root <book-root> --apply
python <skill>/scripts/fix_phantom_cards.py --root <book-root> --apply

# 3. Build EPUB (assumes html2pub.toml is configured)
python -m html2pub build <book-root>

# 4. Run EPUBCheck
java -jar <epubcheck.jar> <output-dir>/book.epub

# 5. KPV smoke test (small subset first)
python <skill>/scripts/kpv_smoke_test.py --epub <output-dir>/book.epub

# 6. Full KPV conversion + qualitychecks
python <skill>/scripts/kpv_convert.py --epub <output-dir>/book.epub --output <output-dir>/book.kpf
```
