# Publishing Pipeline

Repeatable HTML-to-validated-EPUB workflow. Run after any change to source HTML, CSS, metadata, or cover.

## TL;DR

```bash
# From project root, one command:
python KDP/build/publish.py
```

Or use the wrapper of your choice:

| Wrapper | Command | When |
|---------|---------|------|
| Python | `python KDP/build/publish.py` | Cross-platform default |
| Make | `make -C KDP/build build` | Linux/macOS/Git-Bash on Windows |
| PowerShell | `.\KDP\build\publish.ps1` | Windows native |

## Pipeline stages

```
                              ┌──────────────────┐
   source HTML  ───────────►  │ generate_spine   │  →  spine_manifest.json
   (parts/, appendices/,      └────────┬─────────┘
    front-matter/, capstone/)          │
                                       ▼
                              ┌──────────────────┐
   metadata.yaml ──────────►  │   build_epub     │  →  output/*.epub
   cover_kdp.jpg ──────────►  │  - clean HTML    │
   book.css ──────────────►   │  - rewrite links │
   epub_overrides.css ─────►  │  - compress imgs │
                              │  - generate nav  │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ structural_check │  →  validation/structural_report.txt
                              │ (Python; always) │      (PASS / FAIL)
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │   epubcheck      │  →  validation/epubcheck_report.txt
                              │ (Java; optional) │      (full IDPF schema check)
                              └──────────────────┘
```

## Pipeline modes

### Default — full submission build

```bash
python KDP/build/publish.py
```

- Re-uses existing `spine_manifest.json` (fast)
- Builds at full quality (max image side 1600 px, JPEG quality 82)
- Runs structural validation
- Runs epubcheck if Java is installed
- ~30-60 seconds

### Iteration mode — `--quick`

```bash
python KDP/build/publish.py --quick
```

- Smaller images (max 1200 px), lower JPEG quality (70)
- Result is ~60% the size, builds ~30% faster
- **Not for KDP submission** — use only while iterating on HTML/CSS

### Validate-only — `--validate-only`

```bash
python KDP/build/publish.py --validate-only
```

- Skips rebuild; only re-runs validators on existing `output/*.epub`
- ~5 seconds
- Useful after editing the validator itself, or to re-check after a manual EPUB tweak

### Clean rebuild — `--clean --regen-spine`

```bash
python KDP/build/publish.py --clean --regen-spine
```

- Wipes `output/*.epub` and `validation/*_report.txt`
- Re-walks source tree to generate fresh `spine_manifest.json` (catches new chapters)
- Then full build + validate
- Use this when:
  - You added or removed a chapter / section / appendix
  - You're not sure what state the build is in
  - Before a final pre-submission build

## When to run what

| Change you made | Run |
|-----------------|-----|
| Edited prose in 1-5 HTML files | `python KDP/build/publish.py` |
| Added/removed/renamed a chapter | `python KDP/build/publish.py --regen-spine` |
| Edited `book.css` or `epub_overrides.css` | `python KDP/build/publish.py` |
| Updated `metadata.yaml` (title, description, keywords) | `python KDP/build/publish.py` |
| Replaced `cover_kdp.jpg` | `python KDP/build/publish.py` |
| Edited the build script itself | `python KDP/build/publish.py --clean` |
| Just want to revalidate without rebuild | `python KDP/build/publish.py --validate-only` |
| Final pre-KDP-submission build | `python KDP/build/publish.py --clean --regen-spine` (and verify epubcheck is installed) |

## Pre-submission ritual

Before each KDP upload:

```bash
# 1. Regenerate cover if source changed
python KDP/cover/process_cover.py

# 2. Full clean build
python KDP/build/publish.py --clean --regen-spine

# 3. Spot-check the EPUB structure
python KDP/validation/structural_check.py

# 4. (Recommended) Run epubcheck if Java is installed
java -jar epubcheck.jar KDP/output/building-conversational-ai-llms-agents.epub

# 5. (Recommended) Open in Kindle Previewer for visual check
# (https://kdp.amazon.com/en_US/help/topic/G202131170)

# 6. Review the changelog with git diff (if HTML is under version control)
git diff --stat HEAD~1 HEAD -- '*.html' 'styles/' 'KDP/'
```

## CI / scheduled rebuild

The pipeline exits with proper codes for automation:

| Exit code | Meaning | Action |
|-----------|---------|--------|
| 0 | Build + validation passed | Safe to upload |
| 1 | Validation found errors | Check `KDP/validation/*_report.txt` |
| 2 | Build failed | Check `KDP/build/logs/*.log` |
| 3 | Prerequisites missing | Install requirements |

Example GitHub Actions workflow (if you put the project on a repo):

```yaml
name: Build EPUB
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r KDP/build/requirements.txt
      - run: python KDP/build/publish.py --clean --regen-spine --no-epubcheck
      - uses: actions/upload-artifact@v4
        with:
          name: epub
          path: KDP/output/*.epub
```

## Logs

Every build writes a timestamped log to `KDP/build/logs/build_YYYYMMDD-HHMMSS.log`. These accumulate; clear with:

```bash
rm KDP/build/logs/*.log
# or
make -C KDP/build clean
```

## Tuning

The build script has two knobs that trade off file size vs image quality:

- `--max-image-side N` — resize all bundled images to max N pixels on the longest side (default 1600)
- `--jpeg-quality N` — JPEG quality for re-encoded images (default 82)

Examples:

```bash
# Smallest possible EPUB (sacrifices image quality)
python KDP/build/build_epub.py --max-image-side 1000 --jpeg-quality 70

# Highest quality (larger file)
python KDP/build/build_epub.py --max-image-side 2000 --jpeg-quality 90
```

A delivery-fee-friendly target is **under 50 MB**. Above 50 MB, the 70% royalty plan loses too much to per-MB delivery fees and the 35% plan becomes more profitable.

## Files the pipeline reads

| File | Purpose | Edit when |
|------|---------|-----------|
| `KDP/metadata/metadata.yaml` | Title, authors, language, identifier, keywords | Title/author/etc changes |
| `KDP/metadata/description.html` | Embedded as `dc:description` | Description changes |
| `KDP/cover/cover_kdp.jpg` | Cover image | Cover changes |
| `KDP/build/spine_manifest.json` | Ordered spine | Auto-regen with `--regen-spine` |
| `KDP/build/epub_overrides.css` | EPUB-specific CSS overrides | Reader-specific tweaks |
| `styles/book.css` | Main stylesheet (bundled into EPUB) | Site-wide style changes |
| `front-matter/`, `part-N-*/`, `appendices/`, `capstone/` | Source HTML | Content changes |

## Files the pipeline writes

| File | Purpose | Volatile |
|------|---------|----------|
| `KDP/output/building-conversational-ai-llms-agents.epub` | The EPUB | Yes — overwritten each build |
| `KDP/validation/structural_report.txt` | Python validator output | Yes |
| `KDP/validation/epubcheck_report.txt` | epubcheck output (if Java available) | Yes |
| `KDP/build/spine_manifest.json` | Spine derived from source tree | Yes |
| `KDP/build/logs/build_*.log` | Build logs | Accumulating |
| `KDP/cover/cover_source.png` | Copy of source cover | Only via `process_cover.py` |
| `KDP/cover/cover_kdp.jpg` | Processed cover | Only via `process_cover.py` |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `prerequisites failed: missing file: KDP/cover/cover_kdp.jpg` | Cover not yet generated | Run `python KDP/cover/process_cover.py` |
| `ModuleNotFoundError: ebooklib` | Dependencies not installed | `pip install -r KDP/build/requirements.txt` |
| `RESULT: FAIL (N errors)` | Broken refs or missing files | Read `structural_report.txt` for the specific issues |
| EPUB much larger than expected | Spine has duplicates or huge images | Check `--regen-spine`; tune `--max-image-side` |
| `epubcheck not found` | Java/JAR not installed | Optional — see `validation/epubcheck_instructions.md`; KDP runs server-side validation regardless |
| Build crashes on a specific HTML file | Malformed source HTML | The error names the file; fix the HTML, rebuild |
