# Running the official IDPF epubcheck

The Python `structural_check.py` in this folder catches the most common defects (broken zip, missing files, broken links, missing metadata, oversized images). It does **NOT** validate against the full EPUB 3 schema, which the official **epubcheck** tool does.

KDP runs its own validator server-side, but running epubcheck locally before upload is faster than waiting for KDP to reject and retrying.

## What epubcheck catches that structural_check.py does not

- XHTML schema validation (e.g., illegal nesting, missing required attributes)
- OPF schema validation (e.g., wrong cardinality of metadata)
- NCX/nav consistency
- CSS validation against EPUB-allowed property subset
- Font and media-type sanity
- ID uniqueness across the OPF
- Encoding issues

## Installation

epubcheck is a Java application. You need:

1. **Java 11 or later** (Java 17 LTS recommended)
2. **The epubcheck JAR** from https://www.w3.org/publishing/epubcheck/

### Windows (recommended path)

```powershell
# 1. Install Java (Microsoft Build of OpenJDK is free)
winget install Microsoft.OpenJDK.17

# 2. Verify Java
java -version

# 3. Download epubcheck (latest release as of 2026)
$url = "https://github.com/w3c/epubcheck/releases/download/v5.1.0/epubcheck-5.1.0.zip"
Invoke-WebRequest -Uri $url -OutFile "$env:USERPROFILE\Downloads\epubcheck.zip"
Expand-Archive "$env:USERPROFILE\Downloads\epubcheck.zip" -DestinationPath "$env:USERPROFILE\epubcheck" -Force

# 4. Add a function or alias for convenience (optional)
Add-Content $PROFILE @'
function epubcheck { java -jar "$env:USERPROFILE\epubcheck\epubcheck-5.1.0\epubcheck.jar" $args }
'@
```

### macOS / Linux

```bash
# 1. Install Java
brew install openjdk@17        # macOS
# or: sudo apt install openjdk-17-jre  # Debian/Ubuntu

# 2. Download epubcheck
curl -L -o epubcheck.zip https://github.com/w3c/epubcheck/releases/download/v5.1.0/epubcheck-5.1.0.zip
unzip epubcheck.zip -d ~/epubcheck

# 3. Convenience alias
echo 'alias epubcheck="java -jar ~/epubcheck/epubcheck-5.1.0/epubcheck.jar"' >> ~/.zshrc
source ~/.zshrc
```

### Python wrapper alternative

There's a Python wrapper called `epubcheck` on PyPI, but it still requires Java to be installed (it just bundles the JAR for you):

```bash
pip install epubcheck
python -c "from epubcheck import EpubCheck; r = EpubCheck('KDP/output/building-conversational-ai-llms-agents.epub'); print(r)"
```

## Running it

```bash
# From the project root
java -jar epubcheck.jar KDP/output/building-conversational-ai-llms-agents.epub

# or with the alias from above
epubcheck KDP/output/building-conversational-ai-llms-agents.epub
```

## Reading the output

epubcheck prints one line per issue:

```
ERROR(MSG_ID): file:line:col: explanation
WARNING(MSG_ID): file:line:col: explanation
INFO(MSG_ID): file:line:col: explanation
```

A clean run ends with:

```
No errors or warnings detected.
Messages: 0 fatals / 0 errors / 0 warnings / 0 infos
```

## Common errors you might see (and what to do)

| MSG_ID | Meaning | Likely cause | Fix |
|--------|---------|--------------|-----|
| `RSC-005` | Element not allowed here | XHTML schema violation in source HTML | Find the offending file with the line number; fix the source HTML; rebuild |
| `OPF-014` | Attribute not allowed | Wrong attribute on a manifest item | Should not occur with `build_epub.py`'s output; report a bug if it does |
| `CSS-008` | Unknown CSS property | EPUB readers reject some non-standard CSS | Add the property to a `@supports` block or remove it; usually safe to ignore |
| `HTM-009` | XHTML element does not satisfy content model | E.g., `<p>` containing `<div>` | Find and fix in source HTML; rebuild |
| `RSC-007` | Referenced resource missing | A href or src points to a file not in the EPUB | Re-run `build_epub.py`; confirm the source file exists |
| `RSC-014` | Image dimensions exceed maximum | Image larger than ~3 megapixels for Kindle | Reduce `--max-image-side` and rebuild |

## When epubcheck warnings are acceptable

Some warnings are unavoidable for richly-styled books and **don't block KDP**:

- `CSS-008` warnings about modern CSS properties (CSS Grid, custom properties, animations) — KDP's renderer ignores these gracefully
- `RSC-013` warnings about font subsetting recommendations — only matters if you embed fonts; this build doesn't
- `OPF-073` deprecated metadata expression — only matters for newer EPUB 3.3 readers

## When you should NOT proceed to KDP submission

- Any `FATAL` message
- `ERROR` messages other than the false-positive categories noted above
- More than 5-10 warnings of the same type (suggests a systemic issue)

## Useful command-line flags

```bash
# Verbose output (show all checks, even passing ones)
epubcheck -v PATH

# Output JSON for programmatic processing
epubcheck -j report.json PATH

# Output XML
epubcheck -o report.xml PATH

# Save text output to file
epubcheck PATH > epubcheck_report.txt 2>&1
```

## Reference

- epubcheck on GitHub: https://github.com/w3c/epubcheck
- All message codes: https://github.com/w3c/epubcheck/wiki/messages
- EPUB 3.3 specification: https://www.w3.org/TR/epub-33/
