"""Smoke test: build the tiny_book fixture and assert key invariants."""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

# Add src/ to path so we can run without installing
HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "src"
sys.path.insert(0, str(SRC))

from html2epub import builder, config as config_mod, validators  # noqa: E402

FIXTURE = HERE / "fixtures" / "tiny_book"


def test_build_tiny_book():
    cfg = config_mod.load(FIXTURE)
    warns = validators.validate_pre(cfg)
    assert all("source_dir" not in w for w in warns), warns

    out_path = builder.build(cfg)
    assert out_path.exists(), f"EPUB not produced at {out_path}"
    assert out_path.stat().st_size > 1024, "EPUB suspiciously small"

    report = validators.validate_post(out_path)
    assert report["ok"], f"validation errors: {report['errors']}"
    assert report["stats"]["chapter_count"] >= 3, (
        f"expected >=3 chapters, got {report['stats']['chapter_count']}"
    )

    # Critical regression test: every chapter XHTML must have a stylesheet link
    # in <head>. This guards against the ebooklib EpubHtml.set_content() bug
    # where <link> tags inside content's head are silently stripped.
    with zipfile.ZipFile(out_path) as z:
        chapters = [n for n in z.namelist()
                    if n.startswith("EPUB/chapters/") and n.endswith(".xhtml")]
        assert chapters, "no chapter XHTML found in EPUB"
        for n in chapters:
            data = z.read(n).decode("utf-8")
            head = re.search(r"<head[^>]*>(.*?)</head>", data, re.DOTALL | re.IGNORECASE)
            assert head, f"{n} has no <head>"
            assert 'rel="stylesheet"' in head.group(1) or "rel='stylesheet'" in head.group(1), (
                f"{n} <head> has no stylesheet link -- ebooklib add_link regression!"
            )

        # If math rendering had been on, no raw $$...$$ should remain in chapters.
        # In tiny_book math is OFF so this just asserts the file was built.
        # (We don't assert KaTeX-rendered output here unless math.render = 'katex'.)

        # Stylesheet files should be in EPUB/styles/
        styles = [n for n in z.namelist() if n.startswith("EPUB/styles/")]
        assert any(n.endswith("book.css") for n in styles), "user stylesheet not bundled"
        assert any("epub_overrides.css" in n for n in styles), "default overrides not bundled"


if __name__ == "__main__":
    test_build_tiny_book()
    print("OK: tiny_book builds and validates")
