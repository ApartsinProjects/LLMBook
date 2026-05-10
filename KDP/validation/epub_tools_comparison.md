# EPUB Validation & Quality Tools (2026)

A practical comparison of the tools that can scan an EPUB for problems before KDP submission.

## Tier 1: Run before every submission

### 1. EPUBCheck (W3C / DAISY) — **the canonical validator**

The official conformance checker maintained by the [DAISY Consortium](https://daisy.org) under W3C governance. MIT-licensed Java application. **Every EPUB validator and every retailer (Amazon, Apple, Kobo, B&N) uses EPUBCheck under the hood.** If your file passes EPUBCheck cleanly, no retailer will reject it for structural reasons.

| | |
|---|---|
| Cost | Free, open source |
| Platform | Java (Windows / macOS / Linux) |
| Runs | CLI: `java -jar epubcheck.jar book.epub` |
| Output | Text or JSON or XML |
| Coverage | EPUB 2 + EPUB 3.0 + EPUB 3.3, full schema, links, metadata, fonts, CSS subset, accessibility hints |
| Get it | https://www.w3.org/publishing/epubcheck/ |
| Install (this project) | See [`epubcheck_instructions.md`](epubcheck_instructions.md) |

**This is the most important tool to install.** Already documented in this package.

### 2. The Python `structural_check.py` (this package)

A fast Python-only structural validator that catches the **defects most likely to break a KDP build** without requiring Java. Already wired into the pipeline.

| | |
|---|---|
| Cost | Free, in this repo |
| Platform | Python 3.11+ |
| Runs | `python KDP/validation/structural_check.py` |
| Coverage | ZIP, mimetype, OPF, manifest/spine integrity, internal link resolution, image existence, file-size check, KDP-specific limits |
| Time | ~2-5 seconds for the full 70 MB book |
| Catches | Missing files, broken links, missing metadata fields, oversized images |
| Misses | XHTML schema details, CSS validation, font issues, semantic accessibility |

## Tier 2: Run before launch / for quality polish

### 3. Kindle Previewer (Amazon, free) — **the Amazon-specific check**

Amazon's official tool for previewing how an EPUB will render on Kindle devices. **Required step** before any KDP submission you care about — KDP's web previewer is a less-thorough subset.

| | |
|---|---|
| Cost | Free |
| Platform | Windows + macOS desktop (no Linux native; runs in Wine) |
| Runs | GUI: drag-and-drop the EPUB, switch device profiles |
| Coverage | Visual rendering, layout reflow, font sizing, table of contents navigation, cover display, code block wrapping, image sizing |
| Get it | https://kdp.amazon.com/en_US/help/topic/G202131170 |
| Note | Renders for Kindle Paperwhite, Oasis, Scribe, Fire tablet, Kindle for iOS/Android, and the Kindle web reader |

### 4. Ace by DAISY (accessibility checker)

The accessibility-equivalent of epubcheck. Catches issues that affect screen-reader users, EU Accessibility Act compliance, and library distribution.

| | |
|---|---|
| Cost | Free, open source |
| Platform | Node.js (CLI + GUI app called "Ace") |
| Runs | `ace book.epub` — generates a HTML report |
| Coverage | WCAG 2.1, alt-text presence, heading hierarchy, language declarations, table accessibility, color contrast, navigation completeness |
| Get it | https://daisy.github.io/ace/ |
| Why care | EU's European Accessibility Act takes effect for digital products in 2025-2026; Amazon and other retailers will increasingly require accessibility metadata |

### 5. Calibre (free, open source) — **the swiss-army-knife reader/editor**

Calibre's "Check Book" feature wraps EPUBCheck plus its own additional checks. Also gives you a **visual editor** to fix problems on the spot.

| | |
|---|---|
| Cost | Free, open source |
| Platform | Windows / macOS / Linux GUI |
| Runs | Open EPUB → Edit Book → Tools → Check Book |
| Coverage | EPUBCheck output + Calibre's own integrity checks, image quality, navigation issues |
| Get it | https://calibre-ebook.com |
| Why use | When EPUBCheck reports an error, Calibre's editor can navigate to the exact line and fix in place |

## Tier 3: Browser-based, no install

### 6. Pagina EPUB-Checker (free GUI wrapper for EPUBCheck)

A native GUI front-end for EPUBCheck. If you don't want to deal with the Java CLI, this is the easiest install. Localized in 12 languages.

| | |
|---|---|
| Cost | Free |
| Platform | Windows / macOS / Linux |
| Runs | GUI: drag EPUB onto window, see report |
| Get it | http://download.pagina.gmbh/epubchecker/ |

### 7. HMD Publishing EPUB Validator (online)

Browser-based EPUBCheck. Upload, get report. No install. Use when you need a quick check on a machine without Java.

| | |
|---|---|
| Cost | Free |
| Platform | Web |
| Runs | https://hmdpublishing.com/education/tools/epub-validator |
| Caveat | Uploads your full EPUB to their server. **Do not use** for unpublished commercial work where confidentiality matters. |

### 8. Draft2Digital EPUB Validator (online)

Same idea as HMD — browser-based EPUBCheck. Operated by a competing self-publishing platform.

| | |
|---|---|
| Cost | Free (Draft2Digital is a Smashwords-acquired self-publishing platform; they offer this as a public service) |
| Runs | https://draft2digital.com/book/epubcheck/upload |
| Caveat | Same upload-trust issue as HMD |

## Tier 4: Editor / repair tools

### 9. Sigil — **EPUB editor with built-in validation**

A WYSIWYG-ish EPUB editor. Less flexible than Calibre's editor but more focused on EPUB editing as a primary task. Has an integrated EPUBCheck button.

| | |
|---|---|
| Cost | Free, open source |
| Platform | Windows / macOS / Linux |
| Runs | Open EPUB → Tools → Validate EPUB |
| Get it | https://sigil-ebook.com |
| Use case | When you need to hand-edit the OPF or manifest of a built EPUB without rebuilding from source |

### 10. FlightDeck (Firebrand Technologies)

Commercial QA tool for publishers. Aggregates EPUBCheck plus Firebrand's proprietary tests. Mostly used by traditional publishers; likely overkill for one self-published book.

| | |
|---|---|
| Cost | Subscription (USD ~$30-100/title or volume pricing) |
| Platform | Web |
| Get it | https://flightdeck.firebrandtech.com |
| When | Skip unless you're publishing dozens of titles a year |

## Recommended workflow for this book

```
Local pipeline:
  python KDP/build/publish.py
  └─> structural_check.py        (always; catches structural defects)
  └─> epubcheck                  (always, if Java installed; catches schema defects)

Pre-launch quality polish (one-time before first KDP upload):
  ├─> Kindle Previewer           (always; catches visual/layout defects on Kindle)
  ├─> Ace by DAISY               (recommended; accessibility audit, future-proofs for EU AAA)
  └─> Open in Calibre            (optional; spot-check on actual reading device emulator)

Re-runs after content updates:
  python KDP/build/publish.py    (everything in this pipeline runs in <60 sec)
  Kindle Previewer               (skim 5-10 pages to catch regressions)
```

## Quick-reference install commands

```bash
# EPUBCheck (Windows)
winget install Microsoft.OpenJDK.17
# Then download epubcheck-X.Y.Z.zip from https://www.w3.org/publishing/epubcheck/

# Ace by DAISY (any platform with Node.js)
npm install -g @daisy/ace

# Calibre (any platform)
# https://calibre-ebook.com/download

# Pagina EPUB-Checker (Windows GUI)
# http://download.pagina.gmbh/epubchecker/

# Sigil (any platform)
# https://sigil-ebook.com/
```

## Sources

- [EPUBCheck official site (W3C)](https://www.w3.org/publishing/epubcheck/)
- [EPUBCheck GitHub](https://github.com/w3c/epubcheck)
- [EPUBCheck Apps and Tools](https://www.w3.org/publishing/epubcheck/docs/apps-and-tools/)
- [DAISY EPUBCheck KB](https://kb.daisy.org/publishing/docs/epub/validation/epubcheck.html)
- [Ace by DAISY](https://daisy.github.io/ace/)
- [Validate EPUB before upload guide](https://www.ebookpbook.com/2026/03/22/validate-epub-before-upload/)
- [HMD Publishing EPUB Validator](https://hmdpublishing.com/education/tools/epub-validator)
- [Draft2Digital EPUB Validator](https://draft2digital.com/book/epubcheck/upload)
- [PubCoder EPUB Accessibility Checker](https://www.pubcoder.com/epub-accessibility-checker)
- [Vancouver Public Library validation guide](https://www.vpl.ca/guide/inspiration-lab-self-publishing-ebook-format/validating-your-ebook)
