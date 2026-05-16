"""Resolve build-time Jinja placeholders directly in source HTML.

Why this exists:
    `_fix_v14_2_templatize_metadata.py` replaced edition/year strings with
    `{{book.edition}}` / `{{book.publication_year}}` so the EPUB build hook
    (`_html2pub_hooks.templatize_metadata`) could substitute them at build
    time. That works for the EPUB pipeline.

    The static web at llmbook.apartsin.com is served directly from these
    source HTML files. There's no equivalent web-build step, so the
    placeholders leak through and readers see literal `{{book.edition}}`
    in every footer (733 occurrences across 388 pages per the audit).

    Two ways to fix:
      A. Resolve the placeholders inline in source HTML now (this script).
         Lossy: a future edition bump must run `_fix_v14_2_templatize_*`
         again to re-templatize, then this script again to re-resolve.
      B. Add a web-build step that mirrors the EPUB hook.

    We're picking A because it's a one-line round-trip and the web
    publishing cadence is slower than the EPUB cadence.

Reads canonical values from html2pub.toml's [book] table; falls back to
hard-coded defaults if the toml is missing or malformed.

Run from project root:
    python scripts/_resolve_template_placeholders.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_canonical_values() -> dict[str, str]:
    """Read [book] section of html2pub.toml. Fall back to defaults if absent."""
    defaults = {
        "edition": "Fourteenth Edition",
        "publication_date": "2026-05-15",
        "title": "Building Conversational AI with LLMs and Agents",
    }
    toml_path = ROOT / "html2pub.toml"
    if not toml_path.exists():
        return defaults
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore
        except ImportError:
            print("warning: no tomllib available; using defaults", file=sys.stderr)
            return defaults
    with toml_path.open("rb") as f:
        cfg = tomllib.load(f)
    book = cfg.get("book", {})
    return {
        "edition": book.get("edition", defaults["edition"]),
        "publication_date": book.get("publication_date", defaults["publication_date"]),
        "title": book.get("title", defaults["title"]),
    }


def build_replacements(values: dict[str, str]) -> dict[str, str]:
    pub_date = values["publication_date"]
    pub_year = pub_date[:4] if pub_date else "2026"
    return {
        "{{book.edition}}":          values["edition"],
        "{{book.publication_year}}": pub_year,
        "{{book.publication_date}}": pub_date,
        "{{book.title}}":            values["title"],
    }


SKIP_PARTS = {"node_modules", ".git", "KDP", "build", "temp_ebook",
              "temp_epub", "source_fix_backups", "pagefind", "templates",
              ".claude"}


def should_skip(p: Path) -> bool:
    parts = set(p.parts)
    return bool(parts & SKIP_PARTS)


def process(dry_run: bool) -> tuple[int, int]:
    values = load_canonical_values()
    repl = build_replacements(values)
    print(f"Canonical values:")
    for k, v in repl.items():
        print(f"  {k} -> {v!r}")
    print()

    files_touched = 0
    subs_total = 0
    for p in ROOT.rglob("*.html"):
        if should_skip(p):
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new_text = text
        n_here = 0
        for ph, val in repl.items():
            if ph in new_text:
                n = new_text.count(ph)
                new_text = new_text.replace(ph, val)
                n_here += n
        if n_here > 0:
            rel = p.relative_to(ROOT)
            print(f"  {rel}: {n_here} substitution(s)")
            if not dry_run:
                p.write_text(new_text, encoding="utf-8")
            files_touched += 1
            subs_total += n_here

    print()
    print(f"TOTAL: {subs_total} substitutions across {files_touched} files")
    if dry_run:
        print("(dry run; nothing written)")
    return files_touched, subs_total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    process(args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
