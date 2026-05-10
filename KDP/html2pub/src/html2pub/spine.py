"""Source-tree -> ordered spine builder."""
from __future__ import annotations

import json
import re
from pathlib import Path

from html2pub.config import Config


_SECTION_RE = re.compile(r"section-(?:fm\.)?(\d+)\.(\d+)([a-z]?)$")


def section_sort_key(p: Path) -> tuple:
    name = p.stem
    m = _SECTION_RE.match(name)
    if not m:
        return (999, 999, name)
    if "fm" in name:
        major = -1
    else:
        major = int(m.group(1))
    minor = int(m.group(2))
    suffix = m.group(3)
    return (major, minor, suffix)


def build_spine(cfg: Config) -> list[dict]:
    """Return [{path, kind, title_hint}] in EPUB read order."""
    if isinstance(cfg.content.spine, list) and cfg.content.spine:
        return _spine_from_globs(cfg, cfg.content.spine)
    if isinstance(cfg.content.spine, str) and cfg.content.spine != "auto":
        manifest_path = (cfg.project_root / cfg.content.spine).resolve()
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    return _autodiscover(cfg)


def _spine_from_globs(cfg: Config, patterns: list[str]) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    src = cfg.content.source_dir
    for pat in patterns:
        for p in sorted(src.glob(pat)):
            if not p.is_file():
                continue
            rel = p.relative_to(src).as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            out.append({"path": rel, "kind": "section", "title_hint": p.stem})
    return out


def _autodiscover(cfg: Config) -> list[dict]:
    src = cfg.content.source_dir
    spine: list[dict] = []

    def add(rel: str, kind: str, hint: str = "") -> None:
        full = src / rel
        if full.exists() and full.is_file():
            spine.append({"path": rel.replace("\\", "/"), "kind": kind, "title_hint": hint or full.stem})

    fm_dir = src / cfg.content.front_matter_dir
    if fm_dir.is_dir():
        idx = fm_dir / "index.html"
        if idx.exists():
            add(f"{cfg.content.front_matter_dir}/index.html", "front-matter")
        for h in sorted(fm_dir.glob("*.html")):
            if h.name == "index.html":
                continue
            add(f"{cfg.content.front_matter_dir}/{h.name}", "front-matter")

    parts = sorted(
        [p for p in src.glob(cfg.content.parts_glob) if p.is_dir()],
        key=lambda p: _natural_key(p.name),
    )
    for part in parts:
        pidx = part / "index.html"
        if pidx.exists():
            add(f"{part.name}/index.html", "part-index", part.name)
        modules = sorted(
            [m for m in part.glob(cfg.content.module_glob) if m.is_dir()],
            key=lambda p: _natural_key(p.name),
        )
        if modules:
            for mod in modules:
                midx = mod / "index.html"
                if midx.exists():
                    add(f"{part.name}/{mod.name}/index.html", "module-index", mod.name)
                for sec in sorted(mod.glob(cfg.content.section_glob), key=section_sort_key):
                    add(f"{part.name}/{mod.name}/{sec.name}", "section", sec.stem)
        else:
            # Flat parts: chapters live directly under the part
            for h in sorted(part.glob("*.html")):
                if h.name == "index.html":
                    continue
                add(f"{part.name}/{h.name}", "section", h.stem)

    cap = src / cfg.content.capstone_dir
    if cap.is_dir():
        for h in sorted(cap.glob("*.html")):
            kind = "capstone-index" if h.name == "index.html" else "capstone"
            add(f"{cfg.content.capstone_dir}/{h.name}", kind, h.stem)

    apx_root = src / cfg.content.appendices_dir
    if apx_root.is_dir():
        if (apx_root / "index.html").exists():
            add(f"{cfg.content.appendices_dir}/index.html", "appendix-index", "appendices")
        for apx_dir in sorted([p for p in apx_root.iterdir() if p.is_dir()], key=lambda p: p.name):
            if (apx_dir / "index.html").exists():
                add(f"{cfg.content.appendices_dir}/{apx_dir.name}/index.html", "appendix", apx_dir.name)
            for sec in sorted(apx_dir.glob(cfg.content.section_glob), key=section_sort_key):
                add(f"{cfg.content.appendices_dir}/{apx_dir.name}/{sec.name}", "appendix-section", sec.stem)
        for h in sorted(apx_root.glob("*.html")):
            if h.name == "index.html":
                continue
            add(f"{cfg.content.appendices_dir}/{h.name}", "appendix", h.stem)

    return spine


def _natural_key(name: str):
    m = re.match(r"[a-zA-Z-]*?(\d+)", name)
    return (int(m.group(1)) if m else 0, name)
