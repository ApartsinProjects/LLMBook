# KDP Publishing Package

This folder contains everything needed to publish **Building Conversational AI with LLMs and Agents** as a Kindle eBook on Amazon KDP.

## Quick start

If you just want to upload the existing build to KDP:

1. Open https://kdp.amazon.com → "Create" → "Kindle eBook"
2. Follow [`metadata/kdp_form_fields.md`](metadata/kdp_form_fields.md) to fill in the three-step web form
3. Upload these two files when prompted:
   - **Manuscript**: [`output/building-conversational-ai-llms-agents.epub`](output/building-conversational-ai-llms-agents.epub) (70.8 MB)
   - **Cover**: [`cover/cover_kdp.jpg`](cover/cover_kdp.jpg) (1600 × 2560, 418 KB)
4. Submit for review (Amazon review takes 24-72 hours)

For the full step-by-step walkthrough, see [`PUBLISHING_GUIDE.md`](PUBLISHING_GUIDE.md).

## Folder structure

```
KDP/
├── README.md                       ← This file
├── PUBLISHING_GUIDE.md             ← Step-by-step KDP web submission
│
├── metadata/                       ← Everything KDP asks for in the web form
│   ├── metadata.yaml               ← Canonical metadata (used by build_epub.py)
│   ├── kdp_form_fields.md          ← Field-by-field mapping for the KDP form
│   ├── description.html            ← KDP-formatted description (HTML, 3359 chars)
│   ├── description.txt             ← Plain text version
│   ├── keywords.txt                ← 7 search keywords
│   ├── categories.txt              ← 3 BISAC categories
│   └── bisac_reference.md          ← Notes on category selection
│
├── cover/                          ← Cover image processing
│   ├── cover_source.png            ← Original cover (896 × 1200 PNG)
│   ├── cover_kdp.jpg               ← KDP-ready cover (1600 × 2560 sRGB JPEG)
│   ├── cover_notes.md              ← What was done; recommendations for production
│   └── process_cover.py            ← Reproducible cover processing script
│
├── build/                          ← EPUB build pipeline
│   ├── build_epub.py               ← Main build script
│   ├── generate_spine.py           ← Walks the source tree to produce spine_manifest.json
│   ├── spine_manifest.json         ← Ordered list of source HTML files
│   ├── epub_overrides.css          ← EPUB-friendly CSS overrides (loaded after book.css)
│   └── requirements.txt            ← Python dependencies
│
├── output/                         ← Build artifacts
│   └── building-conversational-ai-llms-agents.epub
│
└── validation/                     ← Quality checks
    ├── structural_check.py         ← Python-only EPUB validator (run after build)
    ├── structural_report.txt       ← Latest validation output
    ├── kdp_checklist.md            ← Pre-submission checklist
    └── epubcheck_instructions.md   ← How to install and run the official IDPF epubcheck
```

## Rebuilding the EPUB

If you change source HTML, edit metadata, or replace the cover, rebuild:

```bash
# From the project root
python KDP/build/generate_spine.py        # Re-generate spine if you added/removed pages
python KDP/build/build_epub.py            # Build the EPUB (~30 sec)
python KDP/validation/structural_check.py # Validate
```

The build script accepts `--max-image-side` (default 1600 px) and `--jpeg-quality` (default 82) for tuning the size/quality trade-off.

### Dependencies

```bash
pip install -r KDP/build/requirements.txt
```

(The build needs `ebooklib`, `beautifulsoup4`, `lxml`, `Pillow`, `PyYAML`.)

## Build summary (latest)

| Metric | Value |
|--------|-------|
| EPUB size | 70.76 MB |
| Spine entries | 443 |
| Chapters bundled | 441 |
| Images bundled | 499 (compressed from 832 referenced; missing avatar placeholders skipped) |
| Internal links rewritten | 7,829 |
| Internal links resolved at validation | 8,264 (0 broken) |
| Validation result | **PASS** (0 errors, 0 warnings) |

## What's NOT in this package (action items for you)

These are decisions only you can make before submitting:

1. **ISBN** — Optional for Kindle. KDP assigns an ASIN automatically. If you've purchased an ISBN from Bowker (~USD 125 for one, USD 295 for ten), enter it on the KDP web form. Otherwise leave blank.
2. **Cover quality** — The current `cover_kdp.jpg` is an upscaled placeholder. For production, re-render at native 1600 × 2560. See [cover/cover_notes.md](cover/cover_notes.md).
3. **BISAC categories review** — The three pre-selected categories ([categories.txt](metadata/categories.txt)) are educated guesses. KDP's category browser may have changed; verify on the form.
4. **Pricing** — Recommended USD 9.99 (70% royalty, max for that plan) or USD 14.99-19.99 (35% royalty). See [kdp_form_fields.md](metadata/kdp_form_fields.md) Step 3.
5. **DRM** — Recommend leaving disabled (default in this guide). KDP makes this irreversible after first submission.
6. **KDP Select** — Recommend leaving disabled (default). Enrolling locks you to Amazon-only for 90 days at a time.
7. **Tax interview** — KDP requires a W-8BEN (non-US authors) or W-9 (US authors) before publishing. Complete in Account → Tax Information.

## Going further

- **EPUB schema validation**: Run the official IDPF epubcheck for full schema validation before upload. See [validation/epubcheck_instructions.md](validation/epubcheck_instructions.md).
- **Kindle Previewer**: Free tool from Amazon to preview how the EPUB will render on different Kindle devices and apps. https://kdp.amazon.com/en_US/help/topic/G202131170
- **Print version**: This package only addresses the Kindle eBook. For a paperback or hardcover, you would need a print-ready PDF (different trim sizes, bleed, embedded fonts), a separate print cover with spine, and a different KDP submission flow.
