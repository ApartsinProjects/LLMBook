"""Hierarchical TOC + EPUB 3 landmarks builder."""
from __future__ import annotations


def escape_xml(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))


def build_nav_xhtml(spine_entries, chapter_map, book_title: str) -> str:
    toc_html = _build_toc_ol(spine_entries, chapter_map)
    landmarks = _build_landmarks(spine_entries, chapter_map)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head>
<meta charset="utf-8" />
<title>Contents</title>
</head>
<body>
<nav epub:type="toc" id="toc" role="doc-toc">
<h1>Contents</h1>
{toc_html}
</nav>
<nav epub:type="landmarks" id="landmarks" hidden="">
<h2>Guide</h2>
<ol>
{landmarks}
</ol>
</nav>
</body>
</html>
"""


def _build_toc_ol(spine_entries, chapter_map) -> str:
    front_matter: list[dict] = []
    parts: dict[str, dict] = {}
    capstone: list[dict] = []
    appx_root_info: dict | None = None
    appendices: list[dict] = []

    cur_part_name = None
    cur_module = None
    cur_appendix = None

    for entry in spine_entries:
        info = chapter_map.get(entry["path"])
        if not info:
            continue
        kind = entry["kind"]
        path_parts = entry["path"].split("/")

        if kind == "front-matter":
            front_matter.append(info)
        elif kind == "part-index":
            cur_part_name = path_parts[0]
            parts[cur_part_name] = {"info": info, "modules": [], "loose": []}
            cur_module = None
        elif kind == "module-index":
            cur_module = {"info": info, "sections": []}
            if cur_part_name in parts:
                parts[cur_part_name]["modules"].append(cur_module)
        elif kind == "section":
            if cur_module is not None:
                cur_module["sections"].append(info)
            elif cur_part_name in parts:
                parts[cur_part_name]["loose"].append(info)
        elif kind in ("capstone-index", "capstone"):
            capstone.append(info)
        elif kind == "appendix-index":
            appx_root_info = info
            cur_appendix = None
        elif kind == "appendix":
            cur_appendix = {"info": info, "sections": []}
            appendices.append(cur_appendix)
        elif kind == "appendix-section":
            if cur_appendix is not None:
                cur_appendix["sections"].append(info)

    L: list[str] = ["<ol>"]

    if front_matter:
        L.append("<li>")
        L.append(f'<a href="{escape_xml(front_matter[0]["file"])}">Front Matter</a>')
        L.append("<ol>")
        for info in front_matter:
            L.append(f'<li><a href="{escape_xml(info["file"])}">{escape_xml(info["title"])}</a></li>')
        L.append("</ol></li>")

    for part_data in parts.values():
        pinfo = part_data["info"]
        L.append("<li>")
        L.append(f'<a href="{escape_xml(pinfo["file"])}">{escape_xml(pinfo["title"])}</a>')
        if part_data["modules"] or part_data["loose"]:
            L.append("<ol>")
            for mod in part_data["modules"]:
                minfo = mod["info"]
                L.append("<li>")
                L.append(f'<a href="{escape_xml(minfo["file"])}">{escape_xml(minfo["title"])}</a>')
                if mod["sections"]:
                    L.append("<ol>")
                    for sec in mod["sections"]:
                        L.append(f'<li><a href="{escape_xml(sec["file"])}">{escape_xml(sec["title"])}</a></li>')
                    L.append("</ol>")
                L.append("</li>")
            for sec in part_data["loose"]:
                L.append(f'<li><a href="{escape_xml(sec["file"])}">{escape_xml(sec["title"])}</a></li>')
            L.append("</ol>")
        L.append("</li>")

    if capstone:
        L.append("<li>")
        L.append(f'<a href="{escape_xml(capstone[0]["file"])}">Capstone</a>')
        if len(capstone) > 1:
            L.append("<ol>")
            for info in capstone[1:]:
                L.append(f'<li><a href="{escape_xml(info["file"])}">{escape_xml(info["title"])}</a></li>')
            L.append("</ol>")
        L.append("</li>")

    if appx_root_info or appendices:
        L.append("<li>")
        target = appx_root_info["file"] if appx_root_info else appendices[0]["info"]["file"]
        L.append(f'<a href="{escape_xml(target)}">Appendices</a>')
        if appendices:
            L.append("<ol>")
            for apx in appendices:
                ainfo = apx["info"]
                L.append("<li>")
                L.append(f'<a href="{escape_xml(ainfo["file"])}">{escape_xml(ainfo["title"])}</a>')
                if apx["sections"]:
                    L.append("<ol>")
                    for sec in apx["sections"]:
                        L.append(f'<li><a href="{escape_xml(sec["file"])}">{escape_xml(sec["title"])}</a></li>')
                    L.append("</ol>")
                L.append("</li>")
            L.append("</ol>")
        L.append("</li>")

    L.append("</ol>")
    return "\n".join(L)


def _build_landmarks(spine_entries, chapter_map) -> str:
    lines: list[str] = []
    lines.append('<li><a epub:type="cover" href="cover.xhtml">Cover</a></li>')
    lines.append('<li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>')

    fm = next((chapter_map.get(e["path"]) for e in spine_entries
               if e["kind"] == "front-matter" and e["path"] in chapter_map), None)
    if fm:
        lines.append(f'<li><a epub:type="frontmatter" href="{escape_xml(fm["file"])}">Front Matter</a></li>')

    fw = next((chapter_map.get(e["path"]) for e in spine_entries
               if e["path"].endswith("foreword.html") and e["path"] in chapter_map), None)
    if fw:
        lines.append(f'<li><a epub:type="foreword" href="{escape_xml(fw["file"])}">Foreword</a></li>')

    body = next((chapter_map.get(e["path"]) for e in spine_entries
                 if e["kind"] == "part-index" and e["path"] in chapter_map), None)
    if body:
        lines.append(f'<li><a epub:type="bodymatter" href="{escape_xml(body["file"])}">Begin Reading</a></li>')

    cs = next((chapter_map.get(e["path"]) for e in spine_entries
               if e["kind"] == "capstone-index" and e["path"] in chapter_map), None)
    if cs:
        lines.append(f'<li><a epub:type="afterword" href="{escape_xml(cs["file"])}">Capstone</a></li>')

    apx = next((chapter_map.get(e["path"]) for e in spine_entries
                if e["kind"] == "appendix-index" and e["path"] in chapter_map), None)
    if apx:
        lines.append(f'<li><a epub:type="backmatter" href="{escape_xml(apx["file"])}">Appendices</a></li>')

    return "\n".join(lines)
