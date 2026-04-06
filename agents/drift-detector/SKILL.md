---
name: drift-detector
description: >
  Detect and fix structural drift in HTML textbooks: ToC/index vs files,
  navigation chains, cross-references, caption numbering, section numbering,
  and part/chapter labels. Use when the user asks to "check for drift",
  "audit consistency", "validate navigation", "fix broken links", "check
  numbering", or any request to find mismatches between the book's structural
  metadata and its actual content.
---

# Drift Detector

Comprehensive structural consistency checker for HTML textbooks.
Detects mismatches between what the book *claims* (ToC, indices, nav links,
captions, labels) and what actually *exists* (files on disk, headings, IDs).

## When to Use

- After adding, removing, or renaming sections/chapters
- After a major restructure (renumbering, reordering parts)
- Before a release tag
- As part of a periodic QA sweep

## Configuration

The detector needs one setting: the book root directory. Set `BOOK_ROOT` at
the top of each script, or pass it as a CLI argument.

Default: the parent of the `agents/` directory (i.e., the repository root).

## Drift Categories

| # | Category | Script | What it checks |
|---|----------|--------|----------------|
| 1 | **ToC drift** | `detect_toc_drift.py` | toc.html links vs files on disk; title mismatches; unlisted sections |
| 2 | **Index drift** | `detect_index_drift.py` | Part/chapter index cards vs actual section files and titles |
| 3 | **Navigation drift** | `detect_nav_drift.py` | Prev/next/up bidirectional consistency; orphaned pages; missing nav blocks |
| 4 | **Cross-reference drift** | `detect_xref_drift.py` | Broken internal hrefs; broken #fragment anchors; template placeholders |
| 5 | **Caption numbering drift** | `detect_caption_drift.py` | Figure/Table/Code/Exercise numbering: gaps, duplicates, wrong chapter prefix |
| 6 | **Section numbering drift** | `detect_section_drift.py` | Filename vs h1 number; part/chapter label correctness; missing section gaps |

## Usage

Run all checks:
```bash
python agents/drift-detector/scripts/run_all.py
```

Run a single check:
```bash
python agents/drift-detector/scripts/detect_toc_drift.py
python agents/drift-detector/scripts/detect_nav_drift.py
```

Fix navigation chains after adding sections:
```bash
python agents/drift-detector/scripts/fix_nav_chain.py
```

Fix part/chapter labels:
```bash
python agents/drift-detector/scripts/fix_labels.py
```

## Output Format

Each script prints a structured report to stdout:

```
=== DRIFT CATEGORY NAME ===
[SEVERITY] source_file: description
  Expected: ...
  Actual: ...

Summary: X issues found (Y errors, Z warnings)
```

Severity levels:
- `[ERROR]` : Broken link, missing file, unreachable page
- `[WARN]`  : Title mismatch, numbering gap, stale label
- `[INFO]`  : Cosmetic (case differences, optional fields)

## Architecture

All scripts share a common `book_utils.py` module that provides:
- File discovery (glob patterns for parts, chapters, appendices, front-matter)
- HTML parsing helpers (extract h1, nav links, captions, labels)
- Path resolution (relative href to absolute path)
- Section number extraction (from filenames and headings)

Scripts are stateless and read-only by default. Fix scripts require `--apply`
to write changes (dry-run by default).

## Adapting for Another Book

1. Copy the `agents/drift-detector/` directory to the new project
2. Update `BOOK_ROOT` or pass it as an argument
3. Adjust glob patterns in `book_utils.py` if the directory structure differs
   (e.g., different naming for parts/modules/appendices)
