"""TOML config loader and validator for html2pub."""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib


CONFIG_FILENAME = "html2pub.toml"


@dataclass
class BookMeta:
    title: str = "Untitled"
    subtitle: str = ""
    authors: list[dict] = field(default_factory=list)  # [{name, file_as, role}]
    language: str = "en"
    identifier: str = ""  # urn:isbn:... or urn:uuid:...
    publisher: str = ""
    rights: str = ""
    publication_date: str = ""
    description: str = ""
    keywords: list[str] = field(default_factory=list)


@dataclass
class ContentSpec:
    source_dir: Path = Path(".")
    spine: Any = "auto"  # "auto" | path-to-manifest | list of globs
    front_matter_dir: str = "front-matter"
    parts_glob: str = "part-*"
    capstone_dir: str = "capstone"
    appendices_dir: str = "appendices"
    section_glob: str = "section-*.html"
    module_glob: str = "module-*"
    # Explicit FM ordering (filenames inside front_matter_dir, no path prefix).
    # Files not listed here are appended in alphabetical order after the
    # explicit ones. Without this, the FM spine defaults to alphabetical,
    # which puts about-authors right after the FM index.
    fm_order: list[str] = field(default_factory=list)


@dataclass
class StylingSpec:
    stylesheets: list[str] = field(default_factory=list)
    blitz: bool = False
    blitz_path: str = ""
    epub_overrides: str = ""  # path to overrides CSS; empty means use built-in


@dataclass
class FontsSpec:
    include: list[str] = field(default_factory=list)  # glob patterns
    rewrite_katex_to_woff2_only: bool = True


@dataclass
class MathSpec:
    render: str = "off"   # "katex" | "off"
    katex_path: str = ""  # node_modules root containing 'katex'
    node_exe: str = "node"
    # Optional: project-relative dir of pre-rendered math PNGs. When set, a
    # build step swaps complex/display MathML for <img> (Kindle MathML is
    # unreliable). Cache is keyed by sha1(tex|display); see
    # scripts/build_math_png_cache.py. Empty = keep MathML.
    png_cache: str = ""
    # Bundle katex.min.css + its woff2 fonts into the EPUB and <link> them from
    # every chapter. Needed only if any live KaTeX/MathML survives to the EPUB.
    # When math is fully pre-rendered to PNG (png_cache set), no chapter has a
    # `.katex`/`<math>` node, so the CSS + 24 fonts are dead weight (~2 MB and
    # 24 @font-face rules); set false to drop them.
    bundle_css: bool = True


@dataclass
class ImagesSpec:
    max_side: int = 1280
    jpeg_quality: int = 78
    compress_pngs: bool = True


@dataclass
class CoverSpec:
    path: str = ""


@dataclass
class TransformsSpec:
    drop_selectors: list[str] = field(default_factory=list)
    avatar_sizes: dict[str, list[int]] = field(default_factory=dict)
    wide_table_min_cols: int = 6
    slim_index_lists: bool = False
    fragment_drop: dict[str, list[str]] = field(default_factory=dict)
    drop_inline_style_over: int = 1500


@dataclass
class OutputSpec:
    epub: str = "output/book.epub"


@dataclass
class OptimizeSpec:
    epub_optimizer: bool = False
    epub_optimizer_path: str = ""
    repair_entities: bool = True


@dataclass
class Config:
    project_root: Path
    book: BookMeta
    content: ContentSpec
    styling: StylingSpec
    fonts: FontsSpec
    math: MathSpec
    images: ImagesSpec
    cover: CoverSpec
    transforms: TransformsSpec
    output: OutputSpec
    optimize: OptimizeSpec
    raw: dict


def load(project_dir: Path | str) -> Config:
    project_dir = Path(project_dir).resolve()
    config_file = project_dir / CONFIG_FILENAME
    if not config_file.exists():
        raise FileNotFoundError(f"No {CONFIG_FILENAME} in {project_dir}")
    with config_file.open("rb") as f:
        data = tomllib.load(f)

    book_data = data.get("book", {})
    book = BookMeta(
        title=book_data.get("title", "Untitled"),
        subtitle=book_data.get("subtitle", ""),
        authors=_normalize_authors(book_data.get("authors", [])),
        language=book_data.get("language", "en"),
        identifier=book_data.get("identifier", ""),
        publisher=book_data.get("publisher", ""),
        rights=book_data.get("rights", ""),
        publication_date=book_data.get("publication_date", ""),
        description=book_data.get("description", ""),
        keywords=list(book_data.get("keywords", [])),
    )

    cdata = data.get("content", {})
    content = ContentSpec(
        source_dir=(project_dir / cdata.get("source_dir", ".")).resolve(),
        spine=cdata.get("spine", "auto"),
        front_matter_dir=cdata.get("front_matter_dir", "front-matter"),
        parts_glob=cdata.get("parts_glob", "part-*"),
        capstone_dir=cdata.get("capstone_dir", "capstone"),
        appendices_dir=cdata.get("appendices_dir", "appendices"),
        section_glob=cdata.get("section_glob", "section-*.html"),
        module_glob=cdata.get("module_glob", "module-*"),
        fm_order=list(cdata.get("fm_order", [])),
    )

    sdata = data.get("styling", {})
    styling = StylingSpec(
        stylesheets=list(sdata.get("stylesheets", [])),
        blitz=sdata.get("blitz", False),
        blitz_path=sdata.get("blitz_path", ""),
        epub_overrides=sdata.get("epub_overrides", ""),
    )

    fdata = data.get("fonts", {})
    fonts = FontsSpec(
        include=list(fdata.get("include", [])),
        rewrite_katex_to_woff2_only=fdata.get("rewrite_katex_to_woff2_only", True),
    )

    mdata = data.get("math", {})
    math = MathSpec(
        render=mdata.get("render", "off"),
        katex_path=mdata.get("katex_path", ""),
        node_exe=mdata.get("node_exe", "node"),
        png_cache=mdata.get("png_cache", ""),
        bundle_css=mdata.get("bundle_css", True),
    )

    idata = data.get("images", {})
    images = ImagesSpec(
        max_side=int(idata.get("max_side", 1280)),
        jpeg_quality=int(idata.get("jpeg_quality", 78)),
        compress_pngs=idata.get("compress_pngs", True),
    )

    cov = data.get("cover", {})
    cover = CoverSpec(path=cov.get("path", ""))

    tdata = data.get("transforms", {})
    transforms = TransformsSpec(
        drop_selectors=list(tdata.get("drop_selectors", [])),
        avatar_sizes={k: list(v) for k, v in tdata.get("avatar_sizes", {}).items()},
        wide_table_min_cols=int(tdata.get("wide_table_min_cols", 6)),
        slim_index_lists=tdata.get("slim_index_lists", False),
        fragment_drop={k: list(v) for k, v in tdata.get("fragment_drop", {}).items()},
        drop_inline_style_over=int(tdata.get("drop_inline_style_over", 1500)),
    )

    odata = data.get("output", {})
    output = OutputSpec(epub=odata.get("epub", "output/book.epub"))

    opdata = data.get("optimize", {})
    optimize = OptimizeSpec(
        epub_optimizer=opdata.get("epub_optimizer", False),
        epub_optimizer_path=opdata.get("epub_optimizer_path", ""),
        repair_entities=opdata.get("repair_entities", True),
    )

    return Config(
        project_root=project_dir,
        book=book, content=content, styling=styling,
        fonts=fonts, math=math, images=images, cover=cover,
        transforms=transforms, output=output, optimize=optimize,
        raw=data,
    )


def _normalize_authors(raw) -> list[dict]:
    out = []
    for a in raw or []:
        if isinstance(a, str):
            out.append({"name": a, "file_as": _file_as(a), "role": "aut"})
        elif isinstance(a, dict):
            name = a.get("name", "")
            out.append({
                "name": name,
                "file_as": a.get("file_as") or _file_as(name),
                "role": a.get("role", "aut"),
            })
    return out


def _file_as(name: str) -> str:
    parts = name.strip().rsplit(" ", 1)
    if len(parts) == 2:
        return f"{parts[1]}, {parts[0]}"
    return name
