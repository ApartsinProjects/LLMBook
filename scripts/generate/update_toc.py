#!/usr/bin/env python3
"""
Regenerate toc.html from the actual file structure.

Scans part-*/module-*/section-*.html, part-*/module-*/index.html,
appendices/appendix-*/section-*.html, and appendices/appendix-*/index.html
to build a complete Table of Contents with both short and detailed views.

Usage:
    /c/Python314/python scripts/generate/update_toc.py
"""

import glob
import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # E:/Projects/LLMCourse


def extract_title(filepath: Path) -> str:
    """Extract the text inside the <title> tag of an HTML file."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    m = re.search(r"<title>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    raw = m.group(1).strip()
    # Strip trailing "| Book Title" suffixes
    raw = re.sub(r"\s*\|.*$", "", raw)
    # Decode HTML entities like &amp; -> &
    raw = html.unescape(raw)
    return raw


def html_escape(text: str) -> str:
    """Escape text for safe HTML output."""
    return html.escape(text, quote=False)


# ─────────────────────────────────────────────────────────────
#  Discover parts
# ─────────────────────────────────────────────────────────────

def sort_key_part(dirname: str):
    """Sort part directories numerically (part-1, part-2, ..., part-10)."""
    m = re.search(r"part-(\d+)", dirname)
    return int(m.group(1)) if m else 999


def sort_key_module(dirname: str):
    """Sort module directories numerically (module-00, module-01, ...)."""
    m = re.search(r"module-(\d+)", dirname)
    return int(m.group(1)) if m else 999


def sort_key_section(filename: str):
    """Sort section files by their numeric id (section-1.2 => (1,2))."""
    m = re.search(r"section-(\d+)\.(\d+)", filename)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (9999, 9999)


def sort_key_appendix_dir(dirname: str):
    """Sort appendix directories by letter (appendix-a, appendix-b, ...)."""
    m = re.search(r"appendix-([a-z])-", dirname)
    return m.group(1) if m else "zzz"


def sort_key_appendix_section(filename: str):
    """Sort appendix sections like section-a.1, section-a.2, ..."""
    m = re.search(r"section-([a-z])\.(\d+)", filename)
    if m:
        return (m.group(1), int(m.group(2)))
    return ("z", 9999)


# ─────────────────────────────────────────────────────────────
#  Data collection
# ─────────────────────────────────────────────────────────────

def collect_parts():
    """Return a list of part dicts with their modules and sections."""
    parts = []
    part_dirs = sorted(glob.glob(str(ROOT / "part-*")), key=lambda p: sort_key_part(os.path.basename(p)))

    for part_dir in part_dirs:
        part_path = Path(part_dir)
        part_index = part_path / "index.html"
        if not part_index.exists():
            continue
        part_title = extract_title(part_index)
        if not part_title:
            part_title = part_path.name
        part_rel = part_path.relative_to(ROOT).as_posix() + "/index.html"

        modules = []
        mod_dirs = sorted(
            glob.glob(str(part_path / "module-*")),
            key=lambda p: sort_key_module(os.path.basename(p)),
        )
        for mod_dir in mod_dirs:
            mod_path = Path(mod_dir)
            mod_index = mod_path / "index.html"
            if not mod_index.exists():
                continue
            mod_title_raw = extract_title(mod_index)
            # Extract chapter number from directory name (canonical, zero-padded)
            dm = re.search(r"module-(\d+)", mod_path.name)
            ch_num = dm.group(1) if dm else ""
            # Extract display title from "Chapter NN: Title" pattern
            mod_title = mod_title_raw
            m = re.match(r"Chapter\s+\d+\s*:\s*(.*)", mod_title_raw)
            if m:
                mod_title = m.group(1).strip()

            mod_rel = mod_path.relative_to(ROOT).as_posix() + "/index.html"

            # Collect sections
            sections = []
            sec_files = sorted(
                glob.glob(str(mod_path / "section-*.html")),
                key=lambda p: sort_key_section(os.path.basename(p)),
            )
            for sec_file in sec_files:
                sec_path = Path(sec_file)
                sec_title_raw = extract_title(sec_path)
                # Strip "Section X.Y: " prefix
                sec_title = sec_title_raw
                sm = re.match(r"Section\s+[\d.]+\s*:\s*(.*)", sec_title_raw)
                if sm:
                    sec_title = sm.group(1).strip()
                # Extract section number from filename
                sec_num = ""
                snm = re.search(r"section-([\d.]+)\.html", sec_path.name)
                if snm:
                    sec_num = snm.group(1)
                sec_rel = sec_path.relative_to(ROOT).as_posix()

                # Build display text: "X.Y Title"
                display = f"{sec_num} {sec_title}" if sec_num else sec_title

                sections.append({
                    "rel": sec_rel,
                    "num": sec_num,
                    "title": sec_title,
                    "display": display,
                })

            modules.append({
                "rel": mod_rel,
                "ch_num": ch_num,
                "title": mod_title,
                "sections": sections,
            })

        parts.append({
            "rel": part_rel,
            "title": part_title,
            "modules": modules,
        })

    return parts


def collect_appendices():
    """Return a list of appendix dicts with their sections."""
    appendices = []
    app_dirs = sorted(
        glob.glob(str(ROOT / "appendices" / "appendix-*")),
        key=lambda p: sort_key_appendix_dir(os.path.basename(p)),
    )
    for app_dir in app_dirs:
        app_path = Path(app_dir)
        app_index = app_path / "index.html"
        if not app_index.exists():
            continue
        app_title_raw = extract_title(app_index)
        # Extract letter and title from "Appendix A: Mathematical Foundations..."
        letter = ""
        app_title = app_title_raw
        am = re.match(r"Appendix\s+([A-Z])\s*:\s*(.*)", app_title_raw, re.IGNORECASE)
        if am:
            letter = am.group(1).upper()
            app_title = am.group(2).strip()
        else:
            # Fallback from dirname
            dm = re.search(r"appendix-([a-z])-", app_path.name)
            if dm:
                letter = dm.group(1).upper()

        app_rel = app_path.relative_to(ROOT).as_posix() + "/index.html"

        # Collect sections
        sections = []
        sec_files = sorted(
            glob.glob(str(app_path / "section-*.html")),
            key=lambda p: sort_key_appendix_section(os.path.basename(p)),
        )
        for sec_file in sec_files:
            sec_path = Path(sec_file)
            sec_title_raw = extract_title(sec_path)
            # Strip "Section A.1: " prefix
            sec_title = sec_title_raw
            sm = re.match(r"Section\s+[A-Za-z]\.\d+\s*:\s*(.*)", sec_title_raw)
            if sm:
                sec_title = sm.group(1).strip()
            # Extract section id from filename (e.g., "a.1")
            sec_num = ""
            snm = re.search(r"section-([a-z]\.\d+)\.html", sec_path.name)
            if snm:
                sec_num = snm.group(1).upper()
            sec_rel = sec_path.relative_to(ROOT).as_posix()

            display = f"{sec_num} {sec_title}" if sec_num else sec_title

            sections.append({
                "rel": sec_rel,
                "num": sec_num,
                "title": sec_title,
                "display": display,
            })

        # Build a short title for the overview ToC (abbreviated)
        short_title = app_title
        # Some appendices have long titles; keep a shorter version for the overview
        # We use the full title for detailed view

        appendices.append({
            "rel": app_rel,
            "letter": letter,
            "title": app_title,
            "short_title": short_title,
            "sections": sections,
        })

    return appendices


# ─────────────────────────────────────────────────────────────
#  HTML generation
# ─────────────────────────────────────────────────────────────

def build_short_toc(parts, appendices):
    """Build the short (overview) ToC HTML."""
    lines = []

    # Front Matter (static, since it is hand-curated)
    lines.append('        <div class="stoc-part">')
    lines.append('            <div class="dense-part-header"><a href="front-matter/index.html">Front Matter</a></div>')
    lines.append('            <div class="stoc-group">')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.0a</span> <a href="front-matter/about-authors.html">About the Authors</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.0b</span> <a href="front-matter/about-book.html">About This Book</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.1</span> <a href="front-matter/section-fm.1a.html">What This Book Covers</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.2</span> <a href="front-matter/section-fm.1b.html">Who Should Read This Book</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.3</span> <a href="front-matter/section-fm.4.html">Conventions, Callouts &amp; Labs</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.4</span> <a href="front-matter/section-fm.8.html">Problem-Solution Key</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.5</span> <a href="front-matter/pathways/index.html">Reading Pathways</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.6</span> <a href="front-matter/syllabi/index.html">Course Syllabi</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.7</span> <a href="front-matter/section-fm.5.html">How This Book Was Created</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.8</span> <a href="front-matter/wisdom-council.html">The Wisdom Council</a></div>')
    lines.append('                <div class="dense-chapter"><span class="dense-ch-num">FM.9</span> <a href="front-matter/section-fm.7.html">The Writing Team</a></div>')
    lines.append('            </div>')
    lines.append('        </div>')

    # Parts with modules (no sections in short view)
    for part in parts:
        lines.append('')
        lines.append('        <div class="stoc-part">')
        lines.append(f'            <div class="dense-part-header"><a href="{part["rel"]}">{html_escape(part["title"])}</a></div>')
        lines.append('            <div class="stoc-group">')
        for mod in part["modules"]:
            ch_label = f'Ch {mod["ch_num"]}'
            lines.append(f'                <div class="dense-chapter"><span class="dense-ch-num">{ch_label}</span> <a href="{mod["rel"]}">{html_escape(mod["title"])}</a></div>')
        lines.append('            </div>')
        lines.append('        </div>')

    # Appendices (short)
    lines.append('')
    lines.append('        <div class="stoc-part">')
    lines.append('            <div class="dense-part-header dense-appendices-header">Appendices</div>')
    lines.append('            <div class="stoc-group">')
    for app in appendices:
        lines.append(f'                <div class="dense-chapter"><span class="dense-ch-num">{app["letter"]}</span> <a href="{app["rel"]}">{html_escape(app["short_title"])}</a></div>')
    lines.append('            </div>')
    lines.append('        </div>')

    return "\n".join(lines)


def build_detailed_toc(parts, appendices):
    """Build the detailed ToC HTML (flat listing with sections)."""
    lines = []

    # Front Matter (static)
    lines.append('<div class="dense-part-header"><a href="front-matter/index.html">Front Matter</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.0a</span> <a href="front-matter/about-authors.html">About the Authors</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.0b</span> <a href="front-matter/about-book.html">About This Book</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.1</span> <a href="front-matter/section-fm.1a.html">What This Book Covers</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.2</span> <a href="front-matter/section-fm.1b.html">Who Should Read This Book</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.3</span> <a href="front-matter/section-fm.4.html">Conventions, Callouts &amp; Labs</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.4</span> <a href="front-matter/section-fm.8.html">Problem-Solution Key</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.5</span> <a href="front-matter/pathways/index.html">Reading Pathways</a></div>')
    lines.append('<div class="dense-sections"><a href="front-matter/pathways/product-builder.html">Build AI Products</a> &middot; <a href="front-matter/pathways/ml-engineer.html">Fine-Tune &amp; Train</a> &middot; <a href="front-matter/pathways/agent-builder.html">Build Agents</a> &middot; <a href="front-matter/pathways/platform-devops.html">Deploy in Production</a> &middot; <a href="front-matter/pathways/researcher.html">Research LLMs</a> &middot; <a href="front-matter/pathways/career-changer.html">New to ML</a> &middot; <a href="front-matter/pathways/data-scientist.html">Data Scientist</a> &middot; <a href="front-matter/pathways/nlp-engineer.html">NLP to LLMs</a> &middot; <a href="front-matter/pathways/fullstack-developer.html">Full-Stack AI</a> &middot; <a href="front-matter/pathways/tech-leader.html">Tech Leader</a> &middot; <a href="front-matter/pathways/domain-expert.html">Domain Expert</a> &middot; <a href="front-matter/pathways/safety-alignment.html">Safety &amp; Alignment</a> &middot; <a href="front-matter/pathways/rag-search.html">RAG &amp; Search</a> &middot; <a href="front-matter/pathways/open-source.html">Open-Source</a> &middot; <a href="front-matter/pathways/hobbyist.html">Weekend Projects</a> &middot; <a href="front-matter/pathways/prompt-engineer.html">Prompt Engineer</a> &middot; <a href="front-matter/pathways/infra-engineer.html">AI Infrastructure</a> &middot; <a href="front-matter/pathways/ai-educator.html">AI Educator</a> &middot; <a href="front-matter/pathways/startup-cto.html">Startup CTO</a> &middot; <a href="front-matter/pathways/multimodal-developer.html">Multimodal Developer</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.6</span> <a href="front-matter/syllabi/index.html">Course Syllabi</a></div>')
    lines.append('<div class="dense-sections"><a href="front-matter/syllabi/undergrad-engineering.html">Undergrad Engineering</a> &middot; <a href="front-matter/syllabi/undergrad-research.html">Undergrad Research</a> &middot; <a href="front-matter/syllabi/grad-engineering.html">Grad Engineering</a> &middot; <a href="front-matter/syllabi/grad-research.html">Grad Research</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.7</span> <a href="front-matter/section-fm.5.html">How This Book Was Created</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.8</span> <a href="front-matter/wisdom-council.html">The Wisdom Council</a></div>')
    lines.append('<div class="dense-chapter"><span class="dense-ch-num">FM.9</span> <a href="front-matter/section-fm.7.html">The Writing Team</a></div>')

    # Parts
    for part in parts:
        lines.append(f'<div class="dense-part-header"><a href="{part["rel"]}">{html_escape(part["title"])}</a></div>')
        for mod in part["modules"]:
            ch_label = f'Ch {mod["ch_num"]}'
            lines.append(f'<div class="dense-chapter"><span class="dense-ch-num">{ch_label}</span> <a href="{mod["rel"]}">{html_escape(mod["title"])}</a></div>')
            if mod["sections"]:
                sec_links = " &middot; ".join(
                    f'<a href="{s["rel"]}">{html_escape(s["display"])}</a>'
                    for s in mod["sections"]
                )
                lines.append(f'<div class="dense-sections">{sec_links}</div>')

    # Appendices
    lines.append('<div class="dense-part-header">Appendices</div>')
    for app in appendices:
        app_label = f'App {app["letter"]}'
        lines.append(f'<div class="dense-chapter"><span class="dense-ch-num">{app_label}</span> <a href="{app["rel"]}">{html_escape(app["title"])}</a></div>')
        if app["sections"]:
            sec_links = " &middot; ".join(
                f'<a href="{s["rel"]}">{html_escape(s["display"])}</a>'
                for s in app["sections"]
            )
            lines.append(f'<div class="dense-sections">{sec_links}</div>')

    return "\n".join(lines)


def build_toc_html(parts, appendices):
    """Assemble the complete toc.html."""
    short_toc = build_short_toc(parts, appendices)
    detailed_toc = build_detailed_toc(parts, appendices)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Table of Contents for Building Conversational AI with LLMs and Agents. Navigate all 10 parts, 36 modules, and appendices.">
    <title>Building Conversational AI with LLMs and Agents</title>
    <link rel="stylesheet" href="styles/book.css">
</head>
<body class="index-page">

<header class="chapter-header">
    <nav class="header-nav">
        <a href="index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <h1>Table of Contents</h1>
</header>

<main class="content">

    <!-- ToC View Toggle -->
    <div class="toc-toggle" style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin: 1.5rem 0 1rem 0;">
        <span id="toc-label-short" style="font-size: 0.82rem; font-weight: 600; color: var(--primary); cursor: pointer;" onclick="showToc('short')">Overview</span>
        <label class="toc-switch" style="position: relative; display: inline-block; width: 44px; height: 24px; cursor: pointer;">
            <input type="checkbox" id="toc-switch-input" style="opacity: 0; width: 0; height: 0;"
                   onchange="showToc(this.checked ? 'detailed' : 'short')">
            <span style="position: absolute; inset: 0; background: #ccc; border-radius: 24px; transition: background 0.3s ease;">
                <span id="toc-switch-dot" style="position: absolute; top: 2px; left: 2px; width: 20px; height: 20px; background: white; border-radius: 50%; transition: transform 0.3s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.2);"></span>
            </span>
        </label>
        <span id="toc-label-detailed" style="font-size: 0.82rem; font-weight: 600; color: #999; cursor: pointer;" onclick="showToc('detailed')">Detailed</span>
    </div>

    <!-- SHORT TOC (default, visible) -->
    <div id="toc-short">

{short_toc}

    </div>

    <!-- DETAILED TOC (hidden by default) -->
    <div id="toc-detailed" style="display: none;">

{detailed_toc}

</div> <!-- end #toc-detailed -->

    <footer>
        <p class="footer-title">Building Conversational AI with LLMs and Agents, Fifth Edition</p>
        <p>&copy; 2026 Alexander Apartsin &amp; Yehudit Aperstein &middot; <a href="toc.html">Contents</a></p>
        <p class="footer-updated">Last updated: <script>document.write(new Date(document.lastModified).toLocaleDateString('en-US', {{year:'numeric', month:'long', day:'numeric'}}))</script></p>
    </footer>

</main>

<script>
    // ToC view switching
    function showToc(view) {{
        const shortEl = document.getElementById('toc-short');
        const detailedEl = document.getElementById('toc-detailed');
        const switchInput = document.getElementById('toc-switch-input');
        const dot = document.getElementById('toc-switch-dot');
        const labelShort = document.getElementById('toc-label-short');
        const labelDetailed = document.getElementById('toc-label-detailed');

        if (view === 'detailed') {{
            shortEl.style.display = 'none';
            detailedEl.style.display = 'block';
            switchInput.checked = true;
            dot.style.transform = 'translateX(20px)';
            dot.parentElement.style.background = 'var(--accent, #0f3460)';
            labelShort.style.color = '#999';
            labelDetailed.style.color = 'var(--primary, #1a365d)';
        }} else {{
            shortEl.style.display = 'block';
            detailedEl.style.display = 'none';
            switchInput.checked = false;
            dot.style.transform = 'translateX(0)';
            dot.parentElement.style.background = '#ccc';
            labelShort.style.color = 'var(--primary, #1a365d)';
            labelDetailed.style.color = '#999';
        }}
    }}

    // No collapse/expand needed: detailed ToC is now a flat dense listing
</script>

</body>
</html>
'''


def main():
    print(f"Scanning from: {ROOT}")
    parts = collect_parts()
    appendices = collect_appendices()

    total_modules = sum(len(p["modules"]) for p in parts)
    total_sections = sum(
        len(m["sections"]) for p in parts for m in p["modules"]
    ) + sum(len(a["sections"]) for a in appendices)

    print(f"Found {len(parts)} parts, {total_modules} modules, {len(appendices)} appendices, {total_sections} sections")

    toc_html = build_toc_html(parts, appendices)
    out_path = ROOT / "toc.html"
    out_path.write_text(toc_html, encoding="utf-8")
    print(f"Wrote {out_path} ({len(toc_html):,} bytes)")


if __name__ == "__main__":
    main()
