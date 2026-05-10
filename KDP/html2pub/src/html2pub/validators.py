"""Pre and post EPUB validation."""
from __future__ import annotations

import re
import zipfile
from pathlib import Path


def validate_pre(cfg) -> list[str]:
    """Return a list of warning strings; raise on hard errors."""
    warnings: list[str] = []
    if not cfg.content.source_dir.exists():
        raise FileNotFoundError(f"source_dir does not exist: {cfg.content.source_dir}")
    if cfg.cover.path:
        cp = (cfg.project_root / cfg.cover.path)
        if not cp.exists():
            warnings.append(f"cover image missing: {cp}")
    if cfg.math.render == "katex":
        if not cfg.math.katex_path:
            warnings.append("[math].render = 'katex' but [math].katex_path is empty")
        elif not Path(cfg.math.katex_path).exists():
            warnings.append(f"katex node_modules root missing: {cfg.math.katex_path}")
    return warnings


def validate_post(epub_path: Path) -> dict:
    """Open the EPUB and check basic invariants. Returns a report dict."""
    report: dict = {"ok": True, "errors": [], "warnings": [], "stats": {}}
    if not epub_path.exists():
        report["ok"] = False
        report["errors"].append(f"output file missing: {epub_path}")
        return report

    with zipfile.ZipFile(epub_path) as z:
        names = z.namelist()
        chapters = [n for n in names if n.startswith("EPUB/chapters/") and n.endswith(".xhtml")]
        report["stats"]["chapter_count"] = len(chapters)

        # Each chapter must have at least one stylesheet link in head (the critical
        # regression test for ebooklib's set_content stripping <link> tags).
        missing_css = []
        raw_math = []
        for n in chapters:
            data = z.read(n).decode("utf-8", errors="replace")
            head_match = re.search(r"<head[^>]*>(.*?)</head>", data, re.DOTALL | re.IGNORECASE)
            head = head_match.group(1) if head_match else ""
            if 'rel="stylesheet"' not in head and "rel='stylesheet'" not in head:
                missing_css.append(n)
            # Detect raw $$...$$ math that didn't get rendered (only flag if
            # there are at least two $$ markers separated by content).
            if re.search(r"\$\$[^$\n]+\$\$", data):
                raw_math.append(n)

        if missing_css:
            report["ok"] = False
            report["errors"].append(
                f"{len(missing_css)} chapter(s) have no <link rel='stylesheet'> in head "
                f"(ebooklib add_link regression). First: {missing_css[0]}"
            )
        if raw_math:
            report["warnings"].append(
                f"{len(raw_math)} chapter(s) contain raw $$...$$ math (consider [math].render='katex')"
            )

        if "EPUB/nav.xhtml" not in names and not any("nav.xhtml" in n for n in names):
            report["warnings"].append("no nav.xhtml found")

    return report
