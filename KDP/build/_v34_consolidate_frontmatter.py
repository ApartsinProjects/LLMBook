"""v3.4 #1 (option D): Consolidate front matter pathways + syllabi.

Replaces 19 pathway sub-pages + 8 syllabus sub-pages with two single
comparison-table index pages. Sub-pages are deleted; their inbound
references all redirect to the consolidated index.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCLUDE = {"_archive", "KDP", "node_modules", "vendor", "scripts"}

PATHWAYS_DIR = ROOT / "front-matter/pathways"
SYLLABI_DIR = ROOT / "front-matter/syllabi"

PATHWAYS_INDEX = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Reading pathways for engineers, researchers, founders, data scientists, and newcomers.">
    <title>Reading Pathways: Where to Start</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<header class="chapter-header">
    <nav class="header-nav">
        <a href="../../index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="../../toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <div class="part-label"><a href="../index.html">Front Matter</a></div>
    <h1>Reading Pathways: Where to Start</h1>
</header>

<main class="content">

<p>The book covers a lot. The fastest way to get value is to know which parts to read first. Find the row that fits your goal and start there. Nothing prevents you from reading the rest, but the order below avoids prerequisite gaps and gets you to a useful skill as quickly as possible.</p>

<div class="comparison-table">
<div class="comparison-table-title">Five reader pathways</div>
<table>
<thead>
<tr>
<th scope="col">If you are a...</th>
<th scope="col">Start here</th>
<th scope="col">Then read</th>
<th scope="col">Skip if short on time</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Engineer building AI products and agents</strong></td>
<td>Module 0 (refresher) &rarr; Modules 3 to 5 (sequence models, transformers, decoding) &rarr; Modules 10 to 11 (LLM APIs, prompting)</td>
<td>Modules 19 to 20 (RAG) &rarr; Modules 22 to 26 (Agentic AI) &rarr; Modules 28 to 29 (production + evaluation)</td>
<td>Module 18 (Interpretability), Module 34 (Frontiers)</td>
</tr>
<tr>
<td><strong>Researcher / grad student</strong></td>
<td>Module 0 to Module 5 (full foundations) &rarr; Modules 6 to 9 (Understanding LLMs)</td>
<td>Modules 14 to 17 (training, PEFT, alignment) &rarr; Module 18 (Interpretability) &rarr; Module 34 (Frontiers)</td>
<td>Module 33 (Strategy/ROI), Modules 36 to 38 (Product)</td>
</tr>
<tr>
<td><strong>Founder / Product / Tech lead</strong></td>
<td>Module 7 (Modern LLMs) &rarr; Module 11 (Prompting) &rarr; Module 28 (LLM Applications)</td>
<td>Module 33 (Strategy &amp; ROI) &rarr; Modules 36 to 38 (Product to Production) &rarr; Module 26 (Agent safety)</td>
<td>Math-heavy parts of Module 4 and Module 6</td>
</tr>
<tr>
<td><strong>Data scientist adding LLMs to your stack</strong></td>
<td>Module 0 (ML refresher) &rarr; Module 1 (NLP) &rarr; Module 12 (Hybrid ML + LLM)</td>
<td>Modules 14 to 16 (fine-tuning, PEFT, distillation) &rarr; Modules 19 to 20 (RAG) &rarr; Module 29 (Evaluation)</td>
<td>Module 38 (Shipping), Module 35-equivalent governance content</td>
</tr>
<tr>
<td><strong>Career changer / motivated newcomer</strong></td>
<td>Module 1 (NLP) &rarr; Module 2 (Tokenization) &rarr; Module 3 (Sequence Models)</td>
<td>Module 10 (LLM APIs) &rarr; Module 11 (Prompting) &rarr; into Part 2 at your own pace</td>
<td>Math-heavy parts of Module 4 (read after the conceptual chapters land)</td>
</tr>
</tbody>
</table>
</div>

<p>If your goal is unusual (training your own foundation model, multimodal applications, on-device inference, alignment research), search the table of contents for the closest module title and use it as your starting point. The book's cross-references will pull in any prerequisites you missed.</p>

</main>
</body>
</html>
'''


SYLLABI_INDEX = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Suggested course syllabi using this book for undergraduate, graduate, and professional programs.">
    <title>Course Syllabi</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<header class="chapter-header">
    <nav class="header-nav">
        <a href="../../index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="../../toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <div class="part-label"><a href="../index.html">Front Matter</a></div>
    <h1>Course Syllabi</h1>
</header>

<main class="content">

<p>Five suggested syllabi for using this book in formal courses or self-paced bootcamps. Each row is a tested combination of modules that covers the topic without overloading the term. Mix and match as needed.</p>

<div class="comparison-table">
<div class="comparison-table-title">Five course tracks</div>
<table>
<thead>
<tr>
<th scope="col">Course</th>
<th scope="col">Recommended modules</th>
<th scope="col">Duration</th>
<th scope="col">Capstone</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Undergraduate Engineering</strong></td>
<td>Modules 0 to 5 (foundations) + Modules 10 to 11 (APIs, prompting) + Modules 19 to 20 (embeddings, RAG)</td>
<td>One semester (12 to 14 weeks)</td>
<td>Build a working RAG application</td>
</tr>
<tr>
<td><strong>Undergraduate Research</strong></td>
<td>Modules 0 to 9 (full Foundations + Understanding) + Modules 14 to 15 (fine-tuning, PEFT) + Module 18 (Interpretability)</td>
<td>One semester</td>
<td>Replicate a recent paper or analyze a published model</td>
</tr>
<tr>
<td><strong>Graduate Engineering</strong></td>
<td>All of Undergrad Engineering + Modules 12, 14 to 17 (training, alignment) + Modules 22 to 26 (Agents) + Module 29 (Evaluation)</td>
<td>Two semesters</td>
<td>Multi-agent system with RAG, eval harness, deployment</td>
</tr>
<tr>
<td><strong>Graduate Research</strong></td>
<td>All of Undergrad Research + Modules 14 to 17 + Modules 27 (Multimodal), 32 (Safety), 34 (Frontiers)</td>
<td>Two semesters</td>
<td>Original research project on a frontier topic</td>
</tr>
<tr>
<td><strong>Professional / Bootcamp</strong></td>
<td>Module 7 (Modern LLMs) + Modules 10 to 12 + Modules 19 to 23 + Modules 28 to 29 + Module 33 (Strategy)</td>
<td>8 to 10 weeks intensive</td>
<td>Production-ready agentic application with cost analysis</td>
</tr>
</tbody>
</table>
</div>

<p>For each course, the appendices serve as references rather than required reading: Appendix A (Math Foundations) and Appendix C (Python for LLMs) for foundational gaps; Appendices K (HuggingFace) and L (LangChain) for ecosystem familiarity.</p>

</main>
</body>
</html>
'''


def main() -> int:
    # Step 1: Delete sub-pages (keep index.html in each)
    deleted = 0
    for d in (PATHWAYS_DIR, SYLLABI_DIR):
        if not d.exists():
            continue
        for p in d.glob("*.html"):
            if p.name == "index.html":
                continue
            words = len(re.sub(r"<[^>]+>", " ",
                p.read_text(encoding="utf-8", errors="replace")).split())
            p.unlink()
            deleted += 1
            print(f"  rm {p.relative_to(ROOT).as_posix()}  ({words} words)")

    # Step 2: Rewrite index pages
    (PATHWAYS_DIR / "index.html").write_text(PATHWAYS_INDEX, encoding="utf-8")
    print(f"  rewrote front-matter/pathways/index.html (5-row table)")
    (SYLLABI_DIR / "index.html").write_text(SYLLABI_INDEX, encoding="utf-8")
    print(f"  rewrote front-matter/syllabi/index.html (5-row table)")

    # Step 3: Redirect inbound refs to deleted sub-pages -> index.html
    n_files = 0
    n_links = 0
    for p in ROOT.rglob("*.html"):
        if any(part in p.parts for part in EXCLUDE):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        original = text
        # pathway sub-pages -> pathways/index.html
        text = re.sub(
            r'pathways/(?!index\.html)([\w-]+)\.html',
            r'pathways/index.html',
            text,
        )
        # syllabi sub-pages -> syllabi/index.html
        text = re.sub(
            r'syllabi/(?!index\.html)([\w-]+)\.html',
            r'syllabi/index.html',
            text,
        )
        if text != original:
            p.write_text(text, encoding="utf-8")
            n_files += 1

    print(f"\nDeleted {deleted} sub-pages; redirected refs in {n_files} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
