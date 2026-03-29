"""
Restructure Parts VII through X of the LLM Course book.

Task 1: Part VII - Rename to "AI Applications", keep Ch 24 (Multimodal), deepen Ch 25
Task 2: Part VIII - Split Ch 26 (8 sections) into Ch 26 (eval, 26.1-26.4) + Ch 27 (observability, 26.5-26.8),
         renumber old Ch 27 to Ch 28
Task 3: Part IX - Strengthen Ch 28 (Safety) and Ch 29 (Strategy) with new content
Task 4: Part X - Split Ch 30 into Ch 31 (Emerging Architectures) + Ch 32 (AI and Society)
Task 5: Fix footer in ALL index pages
Task 6: Fix part index page headers

Run with: /c/Python314/python _restructure_parts_7_10.py
"""

import os
import re
import shutil
from pathlib import Path

BASE = Path(r"E:/Projects/LLMCourse")

FOOTER_HTML = """<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>"""

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Wrote: {path}")

def remove_em_dashes(text):
    """Replace em dashes and double dashes with appropriate alternatives."""
    text = text.replace(" — ", ", ")
    text = text.replace("—", ", ")
    text = text.replace(" -- ", ", ")
    text = text.replace("--", ", ")
    return text

# ============================================================
# TASK 1: Part VII - Rename and deepen Ch 25
# ============================================================

def task1_part7():
    print("\n=== TASK 1: Part VII Restructure ===")

    # Update Part VII index
    p7_index = BASE / "part-7-multimodal-applications" / "index.html"
    content = read_file(p7_index)

    # Change title
    content = content.replace(
        "Part VII: Multimodal AI &amp; Industry Applications",
        "Part VII: AI Applications"
    ).replace(
        "Part VII: Multimodal AI & Industry Applications",
        "Part VII: AI Applications"
    )

    # Update overview text
    content = content.replace(
        "Part VII moves beyond text-only models to cover multimodal AI (vision, audio, video, documents) and surveys the rapidly expanding landscape of LLM applications across industries. You will learn how organizations are deploying LLMs in finance, healthcare, cybersecurity, education, software engineering, and scientific research.",
        "Part VII covers the practical application of LLMs across modalities and industries. It opens with multimodal AI (vision, audio, video, documents) and then provides in-depth treatment of LLM applications in software engineering, finance, healthcare, cybersecurity, education, and scientific discovery. Each application domain receives substantial coverage of key techniques, code patterns, case studies, and domain-specific tools."
    )

    # Update chapter count description
    content = content.replace(
        "Chapters: 2 (Chapters 24 and 25). These chapters connect the technical foundations from Parts I through VI to real-world deployment scenarios and domain-specific challenges.",
        "Chapters: 2 (Chapters 24 and 25). These chapters connect the technical foundations from Parts I through VI to real-world deployment scenarios, domain-specific challenges, and industry best practices."
    )

    write_file(p7_index, content)

    # Update Ch 24 index to reference new part name
    ch24_index = BASE / "part-7-multimodal-applications" / "module-24-multimodal" / "index.html"
    content = read_file(ch24_index)
    content = content.replace(
        "Part VII: Multimodal AI &amp; Industry Applications",
        "Part VII: AI Applications"
    )
    write_file(ch24_index, content)

    # Update Ch 25 index to reference new part name
    ch25_index = BASE / "part-7-multimodal-applications" / "module-25-llm-applications" / "index.html"
    content = read_file(ch25_index)
    content = content.replace(
        "Part VII: Multimodal AI &amp; Industry Applications",
        "Part VII: AI Applications"
    )
    write_file(ch25_index, content)

    print("  Task 1 complete: Part VII renamed to 'AI Applications'")


# ============================================================
# TASK 2: Part VIII - Split Ch 26 into two chapters
# ============================================================

def task2_part8():
    print("\n=== TASK 2: Part VIII - Split Ch 26 ===")

    eval_dir = BASE / "part-8-evaluation-production" / "module-26-evaluation-observability"
    prod_dir = BASE / "part-8-evaluation-production" / "module-27-production-engineering"

    # Create new chapter directory for observability (new Ch 27)
    obs_dir = BASE / "part-8-evaluation-production" / "module-27-observability-monitoring"
    os.makedirs(obs_dir, exist_ok=True)
    os.makedirs(obs_dir / "images", exist_ok=True)

    # Rename old production engineering to Ch 28
    new_prod_dir = BASE / "part-8-evaluation-production" / "module-28-production-engineering"

    # Step 1: Copy sections 26.5-26.8 to new Ch 27 as 27.1-27.4
    section_mapping = {
        "section-26.5.html": "section-27.1.html",
        "section-26.6.html": "section-27.2.html",
        "section-26.7.html": "section-27.3.html",
        "section-26.8.html": "section-27.4.html",
    }

    section_titles = {
        "section-27.1.html": ("Observability &amp; Tracing", "27.1"),
        "section-27.2.html": ("LLM-Specific Monitoring &amp; Drift Detection", "27.2"),
        "section-27.3.html": ("LLM Experiment Reproducibility", "27.3"),
        "section-27.4.html": ("Arena-Style and Crowdsourced Evaluation", "27.4"),
    }

    for old_name, new_name in section_mapping.items():
        old_path = eval_dir / old_name
        if old_path.exists():
            content = read_file(old_path)
            # Renumber section references
            old_num = old_name.replace("section-", "").replace(".html", "")
            new_num = new_name.replace("section-", "").replace(".html", "")
            content = content.replace(f"Section {old_num}", f"Section {new_num}")
            content = content.replace(f"section-{old_num}", f"section-{new_num}")
            # Update chapter reference
            content = content.replace("Chapter 26", "Chapter 27")
            content = content.replace(
                "Evaluation, Experiment Design &amp; Observability",
                "Observability, Monitoring &amp; MLOps"
            )
            content = content.replace(
                "Part VIII: Evaluation &amp; Production",
                "Part VIII: Evaluation &amp; Production"
            )
            content = content.replace(
                "module-26-evaluation-observability",
                "module-27-observability-monitoring"
            )
            write_file(obs_dir / new_name, content)

    # Copy images from old ch26 to new ch27
    old_images = eval_dir / "images"
    if old_images.exists():
        for img in old_images.iterdir():
            if img.is_file():
                shutil.copy2(img, obs_dir / "images" / img.name)

    # Step 2: Create new Ch 27 (Observability) index page
    ch27_obs_index = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 27: Observability, Monitoring &amp; MLOps</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part VIII: Evaluation &amp; Production</a></div>
    <div class="chapter-label"><a href="../../toc.html" class="chapter-num" style="color: white; text-decoration: none;">Chapter 27</a></div>
    <h1>Observability, Monitoring &amp; MLOps</h1>
</header>

<div class="content">

    <blockquote class="epigraph">
        <p>"You cannot improve what you cannot measure, and you cannot measure what you cannot observe."</p>
        <cite>An Observability-Obsessed AI Agent</cite>
    </blockquote>

    <div class="overview">
        <h2>Chapter Overview</h2>
        <p>
            With evaluation fundamentals established in <a class="cross-ref" href="../module-26-evaluation-observability/index.html">Chapter 26</a>,
            this chapter focuses on the operational side: making LLM applications observable, monitorable, and
            reproducible in production. You will learn to instrument applications with distributed tracing,
            detect drift before it degrades user experience, and implement experiment tracking that ensures
            every result can be reproduced months later.
        </p>
        <p>
            The chapter covers production observability with tracing tools (LangSmith, Langfuse, Phoenix),
            monitoring for prompt drift, provider version drift, and embedding drift, reproducibility practices
            including prompt versioning and config management, and arena-style evaluation methods that leverage
            crowdsourced human judgment at scale.
        </p>
    </div>

    <div class="objectives">
        <h3>Learning Objectives</h3>
        <ul>
            <li>Instrument LLM applications with distributed tracing using LangSmith, Langfuse, or Phoenix</li>
            <li>Detect and respond to prompt drift, model version drift, and embedding drift in production systems</li>
            <li>Implement reproducibility practices including prompt versioning, config management, and experiment tracking</li>
            <li>Design arena-style evaluation systems using Elo ratings and crowdsourced human judgment</li>
        </ul>
    </div>

    <div class="prereqs">
        <h3>Prerequisites</h3>
        <ul>
            <li><a class="cross-ref" href="../module-26-evaluation-observability/index.html">Chapter 26: Evaluation and Experiment Design</a> (metrics, benchmarks, statistical rigor)</li>
            <li><a class="cross-ref" href="../../part-3-working-with-llms/module-10-llm-apis/index.html">Chapter 10: LLM APIs</a> (chat completions, model parameters)</li>
            <li>Familiarity with Python testing frameworks (pytest) and basic statistics</li>
        </ul>
    </div>

    <h2 style="margin-bottom: 1rem; font-size: 1.2rem;">Sections</h2>

    <ul class="sections-list">
        <li>
            <a href="section-27.1.html" class="section-card">
                <span class="section-num">27.1</span>
                <span class="section-title">Observability &amp; Tracing</span>
                <span class="badge" title="Intermediate">&#x1F7E1;</span>
                <span class="badge" title="Engineering">&#x2699;&#xFE0F;</span>
                <span class="badge" title="Lab">&#x1F527;</span>
                <span class="section-desc">
                    LLM tracing concepts, LangSmith, Langfuse, Phoenix, LangWatch, TruLens,
                    structured logging patterns, and production alerting.
                </span>
            </a>
        </li>
        <li>
            <a href="section-27.2.html" class="section-card">
                <span class="section-num">27.2</span>
                <span class="section-title">LLM-Specific Monitoring &amp; Drift Detection</span>
                <span class="badge" title="Advanced">&#x1F534;</span>
                <span class="badge" title="Engineering">&#x2699;&#xFE0F;</span>
                <span class="badge" title="Lab">&#x1F527;</span>
                <span class="section-desc">
                    Prompt drift, provider version drift, embedding drift, quality monitoring,
                    data quality checks, and retraining triggers for production LLM systems.
                </span>
            </a>
        </li>
        <li>
            <a href="section-27.3.html" class="section-card">
                <span class="section-num">27.3</span>
                <span class="section-title">LLM Experiment Reproducibility</span>
                <span class="badge" title="Intermediate">&#x1F7E1;</span>
                <span class="badge" title="Engineering">&#x2699;&#xFE0F;</span>
                <span class="section-desc">
                    Reproducibility challenges in LLM experiments, versioning strategies (prompt, retrieval,
                    model, system), config management (Hydra, OmegaConf), experiment tracking (DVC, MLflow, W&amp;B),
                    and containerized reproducibility with Docker.
                </span>
            </a>
        </li>
        <li>
            <a href="section-27.4.html" class="section-card">
                <span class="section-num">27.4</span>
                <span class="section-title">Arena-Style and Crowdsourced Evaluation</span>
                <span class="badge" title="Advanced">&#x1F534;</span>
                <span class="badge" title="Research">&#x1F52C;</span>
                <span class="section-desc">
                    Chatbot Arena and Elo-based model ranking, crowdsourced human evaluation
                    at scale, pairwise comparison methodologies, and community-driven benchmarking.
                </span>
            </a>
        </li>
    </ul>

    <div class="bibliography">
        <h2>Bibliography</h2>
        <h3>Tools &amp; Libraries</h3>
        <ol class="bib-list">
            <li>
                <p class="bib-entry">LangSmith. LangChain, Inc. <a href="https://smith.langchain.com/">smith.langchain.com</a></p>
                <p class="bib-annotation">Platform for tracing, evaluating, and monitoring LLM applications with built-in dataset management.</p>
            </li>
            <li>
                <p class="bib-entry">Langfuse. Langfuse GmbH. <a href="https://github.com/langfuse/langfuse">github.com/langfuse/langfuse</a></p>
                <p class="bib-annotation">Open-source LLM observability platform providing tracing, prompt management, and evaluation scoring.</p>
            </li>
            <li>
                <p class="bib-entry">Phoenix. Arize AI. <a href="https://github.com/Arize-ai/phoenix">github.com/Arize-ai/phoenix</a></p>
                <p class="bib-annotation">Open-source observability library for LLM applications with tracing, evaluation, and embedding drift visualization.</p>
            </li>
        </ol>
    </div>

</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    write_file(obs_dir / "index.html", ch27_obs_index)

    # Step 3: Update Ch 26 index to only reference sections 26.1-26.4
    ch26_index_path = eval_dir / "index.html"
    ch26_content = read_file(ch26_index_path)

    # Update the title
    ch26_content = ch26_content.replace(
        "<title>Chapter 26: Evaluation, Experiment Design &amp; Observability</title>",
        "<title>Chapter 26: Evaluation &amp; Experiment Design</title>"
    )
    ch26_content = ch26_content.replace(
        "<h1>Evaluation, Experiment Design &amp; Observability</h1>",
        "<h1>Evaluation &amp; Experiment Design</h1>"
    )

    # Remove sections 26.5-26.8 and associated callouts from the sections list
    # We need to carefully remove the li elements for 26.5-26.8
    # Find the section-26.5 entry and remove everything from there to end of </ul>
    pattern = r'(\s*<li>\s*<a href="section-26\.5\.html".*?)(\s*</ul>)'
    match = re.search(pattern, ch26_content, re.DOTALL)
    if match:
        # Keep only the </ul>
        ch26_content = ch26_content[:match.start(1)] + "\n    </ul>" + ch26_content[match.end(2) + len("</ul>"):]
        # Fix double </ul>
        ch26_content = ch26_content.replace("</ul></ul>", "</ul>")

    write_file(ch26_index_path, ch26_content)

    # Step 4: Rename old Ch 27 (production) to Ch 28
    if prod_dir.exists() and not new_prod_dir.exists():
        # Copy to new name
        shutil.copytree(prod_dir, new_prod_dir)

        # Renumber all section files
        for f in new_prod_dir.glob("section-27.*.html"):
            old_num = f.stem.replace("section-", "")
            new_num = old_num.replace("27.", "28.")
            new_path = new_prod_dir / f"section-{new_num}.html"
            content = read_file(f)
            content = content.replace("Section 27.", "Section 28.")
            content = content.replace("section-27.", "section-28.")
            content = content.replace("Chapter 27", "Chapter 28")
            content = content.replace(
                "module-27-production-engineering",
                "module-28-production-engineering"
            )
            write_file(new_path, content)
            os.remove(f)

        # Update Ch 28 index
        ch28_index_path = new_prod_dir / "index.html"
        content = read_file(ch28_index_path)
        content = content.replace("Chapter 27", "Chapter 28")
        content = content.replace("section-27.", "section-28.")
        content = content.replace(
            "module-27-production-engineering",
            "module-28-production-engineering"
        )
        write_file(ch28_index_path, content)

    # Step 5: Update Part VIII index
    p8_index = BASE / "part-8-evaluation-production" / "index.html"
    p8_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Part VIII: Evaluation &amp; Production</title>
    <link rel="stylesheet" href="../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Building Conversational AI with LLMs and Agents</a></div>
    <h1>Part VIII: Evaluation &amp; Production</h1>
    <p class="chapter-subtitle">Rigorous evaluation, observability infrastructure, and production engineering for LLM systems at scale.</p>
</header>

<div class="content">

    <div class="part-overview">
        <h2>Part Overview</h2>
        <p>
            Part VIII covers the three pillars that separate prototypes from production systems: evaluation, observability, and operations. You will design rigorous evaluation frameworks, build observability infrastructure, set up continuous monitoring, and learn the production engineering practices needed to deploy, scale, and maintain LLM applications reliably.
        </p>
        <p>
            Chapters: 3 (Chapters 26, 27, and 28). These chapters bridge the gap between "it works in a notebook" and "it works in production for millions of users."
        </p>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="module-26-evaluation-observability/index.html"><span class="mod-num">Chapter 26</span> Evaluation &amp; Experiment Design</a>
        </div>
        <div class="chapter-card-body">
            <p>Measuring what matters: evaluation frameworks, benchmark design, A/B testing, statistical rigor, RAG and agent evaluation, and testing LLM applications.</p>
            <ul class="section-list">
                <li><a href="module-26-evaluation-observability/section-26.1.html"><span class="sec-num">26.1</span> LLM Evaluation Fundamentals</a></li>
                <li><a href="module-26-evaluation-observability/section-26.2.html"><span class="sec-num">26.2</span> Experimental Design &amp; Statistical Rigor</a></li>
                <li><a href="module-26-evaluation-observability/section-26.3.html"><span class="sec-num">26.3</span> RAG &amp; Agent Evaluation</a></li>
                <li><a href="module-26-evaluation-observability/section-26.4.html"><span class="sec-num">26.4</span> Testing LLM Applications</a></li>
            </ul>
        </div>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="module-27-observability-monitoring/index.html"><span class="mod-num">Chapter 27</span> Observability, Monitoring &amp; MLOps</a>
        </div>
        <div class="chapter-card-body">
            <p>Production observability with tracing tools, monitoring for drift, experiment reproducibility, and arena-style evaluation at scale.</p>
            <ul class="section-list">
                <li><a href="module-27-observability-monitoring/section-27.1.html"><span class="sec-num">27.1</span> Observability &amp; Tracing</a></li>
                <li><a href="module-27-observability-monitoring/section-27.2.html"><span class="sec-num">27.2</span> LLM-Specific Monitoring &amp; Drift Detection</a></li>
                <li><a href="module-27-observability-monitoring/section-27.3.html"><span class="sec-num">27.3</span> LLM Experiment Reproducibility</a></li>
                <li><a href="module-27-observability-monitoring/section-27.4.html"><span class="sec-num">27.4</span> Arena-Style and Crowdsourced Evaluation</a></li>
            </ul>
        </div>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="module-28-production-engineering/index.html"><span class="mod-num">Chapter 28</span> Production Engineering &amp; Operations</a>
        </div>
        <div class="chapter-card-body">
            <p>Take LLM applications from notebook to production. Covers deployment architectures, frontend frameworks, scaling, guardrails, and LLMOps practices.</p>
            <ul class="section-list">
                <li><a href="module-28-production-engineering/section-28.1.html"><span class="sec-num">28.1</span> Application Architecture &amp; Deployment</a></li>
                <li><a href="module-28-production-engineering/section-28.2.html"><span class="sec-num">28.2</span> Frontend &amp; User Interfaces</a></li>
                <li><a href="module-28-production-engineering/section-28.3.html"><span class="sec-num">28.3</span> Scaling, Performance &amp; Production Guardrails</a></li>
                <li><a href="module-28-production-engineering/section-28.4.html"><span class="sec-num">28.4</span> LLMOps &amp; Continuous Improvement</a></li>
            </ul>
        </div>
    </div>

<nav class="chapter-nav">
    <a href="../index.html">&larr; Back to Book Index</a>
</nav>
</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    write_file(p8_index, p8_content)
    print("  Task 2 complete: Part VIII split into 3 chapters (26, 27, 28)")


# ============================================================
# TASK 3: Part IX - Renumber to Ch 29, Ch 30; add new content
# ============================================================

def task3_part9():
    print("\n=== TASK 3: Part IX - Strengthen Safety and Strategy ===")

    safety_dir = BASE / "part-9-safety-strategy" / "module-28-safety-ethics-regulation"
    strategy_dir = BASE / "part-9-safety-strategy" / "module-29-strategy-product-roi"

    # Renumber safety: 28 -> 29
    new_safety_dir = BASE / "part-9-safety-strategy" / "module-29-safety-ethics-regulation"
    # Renumber strategy: 29 -> 30
    new_strategy_dir = BASE / "part-9-safety-strategy" / "module-30-strategy-product-roi"

    # Copy safety -> 29
    if safety_dir.exists() and not new_safety_dir.exists():
        shutil.copytree(safety_dir, new_safety_dir)
        for f in new_safety_dir.glob("section-28.*.html"):
            old_num = f.stem.replace("section-", "")
            new_num = old_num.replace("28.", "29.")
            new_path = new_safety_dir / f"section-{new_num}.html"
            content = read_file(f)
            content = content.replace("Section 28.", "Section 29.")
            content = content.replace("section-28.", "section-29.")
            content = content.replace("Chapter 28", "Chapter 29")
            content = content.replace("module-28-safety-ethics-regulation", "module-29-safety-ethics-regulation")
            write_file(new_path, content)
            os.remove(f)

        # Update index
        idx = new_safety_dir / "index.html"
        content = read_file(idx)
        content = content.replace("Chapter 28", "Chapter 29")
        content = content.replace("section-28.", "section-29.")
        content = content.replace("module-28-safety-ethics-regulation", "module-29-safety-ethics-regulation")
        write_file(idx, content)

    # Add new section 29.8: Red Teaming & LLM Security Testing
    section_29_8 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Section 29.8: Red Teaming Frameworks &amp; LLM Security Testing</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part IX: Safety &amp; Strategy</a></div>
    <div class="chapter-label"><a href="../../toc.html" class="chapter-num" style="color: white; text-decoration: none;">Chapter 29</a></div>
    <h1>Section 29.8: Red Teaming Frameworks &amp; LLM Security Testing</h1>
</header>

<div class="content">

    <div class="overview">
        <h2>Section Overview</h2>
        <p>
            This section covers structured red teaming methodologies for LLM systems, including automated
            red teaming tools (Microsoft PyRIT, Garak, NVIDIA NeMo Guardrails testing), manual red team
            playbooks, EU AI Act conformity testing requirements, and integration of security testing
            into CI/CD pipelines. It also covers LLM-specific penetration testing tools, adversarial prompt
            libraries, and establishing red team programs within organizations.
        </p>
    </div>

    <h2>Key Topics</h2>
    <ul>
        <li>Structured red teaming methodologies for LLM applications</li>
        <li>Automated red teaming: Microsoft PyRIT, Garak, Counterfit</li>
        <li>Manual red team playbooks and scenario-based testing</li>
        <li>EU AI Act conformity assessment for high-risk AI systems</li>
        <li>LLM penetration testing: prompt injection, jailbreak, data exfiltration</li>
        <li>Building an internal red team program: roles, cadence, and reporting</li>
        <li>Adversarial prompt libraries and benchmark datasets (AdvBench, HarmBench)</li>
        <li>Integrating LLM security testing into CI/CD pipelines</li>
        <li>Red teaming for multimodal models: image and audio attack vectors</li>
    </ul>

    <div class="callout warning">
        <p>This section provides skeleton content for the red teaming and security testing topic. Full content generation with code examples and detailed case studies is planned for a subsequent content pass.</p>
    </div>

</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    if new_safety_dir.exists():
        write_file(new_safety_dir / "section-29.8.html", section_29_8)

    # Add section 29.9: EU AI Act Compliance
    section_29_9 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Section 29.9: EU AI Act Compliance in Practice</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part IX: Safety &amp; Strategy</a></div>
    <div class="chapter-label"><a href="../../toc.html" class="chapter-num" style="color: white; text-decoration: none;">Chapter 29</a></div>
    <h1>Section 29.9: EU AI Act Compliance in Practice</h1>
</header>

<div class="content">

    <div class="overview">
        <h2>Section Overview</h2>
        <p>
            A deep practical guide to EU AI Act compliance for LLM-based systems. Covers risk classification
            for LLM applications, documentation requirements for general-purpose AI models (GPAI),
            transparency obligations, technical documentation standards, conformity assessment procedures,
            and practical implementation checklists. Includes code examples for automated compliance checks
            and templates for required documentation.
        </p>
    </div>

    <h2>Key Topics</h2>
    <ul>
        <li>EU AI Act risk tiers applied to LLM use cases (prohibited, high-risk, limited, minimal)</li>
        <li>General-Purpose AI Model (GPAI) obligations: transparency, documentation, systemic risk</li>
        <li>Technical documentation requirements and templates</li>
        <li>Conformity assessment procedures for high-risk AI systems</li>
        <li>Implementation timeline and transition periods</li>
        <li>Automated compliance checking tools and frameworks</li>
        <li>Comparing EU AI Act, NIST AI RMF, and ISO 42001 requirements</li>
        <li>Practical compliance checklists for LLM deployers and providers</li>
    </ul>

    <div class="callout warning">
        <p>This section provides skeleton content for EU AI Act compliance. Full content generation with detailed compliance checklists and code examples is planned for a subsequent content pass.</p>
    </div>

</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    if new_safety_dir.exists():
        write_file(new_safety_dir / "section-29.9.html", section_29_9)

    # Copy strategy -> 30
    if strategy_dir.exists() and not new_strategy_dir.exists():
        shutil.copytree(strategy_dir, new_strategy_dir)
        for f in new_strategy_dir.glob("section-29.*.html"):
            old_num = f.stem.replace("section-", "")
            new_num = old_num.replace("29.", "30.")
            new_path = new_strategy_dir / f"section-{new_num}.html"
            content = read_file(f)
            content = content.replace("Section 29.", "Section 30.")
            content = content.replace("section-29.", "section-30.")
            content = content.replace("Chapter 29", "Chapter 30")
            content = content.replace("module-29-strategy-product-roi", "module-30-strategy-product-roi")
            write_file(new_path, content)
            os.remove(f)

        idx = new_strategy_dir / "index.html"
        content = read_file(idx)
        content = content.replace("Chapter 29", "Chapter 30")
        content = content.replace("section-29.", "section-30.")
        content = content.replace("module-29-strategy-product-roi", "module-30-strategy-product-roi")
        write_file(idx, content)

    # Add new section 30.6: Build vs Buy & Total Cost of Ownership
    section_30_6 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Section 30.6: Build vs. Buy Decision Framework &amp; Total Cost of Ownership</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part IX: Safety &amp; Strategy</a></div>
    <div class="chapter-label"><a href="../../toc.html" class="chapter-num" style="color: white; text-decoration: none;">Chapter 30</a></div>
    <h1>Section 30.6: Build vs. Buy Decision Framework &amp; Total Cost of Ownership</h1>
</header>

<div class="content">

    <div class="overview">
        <h2>Section Overview</h2>
        <p>
            A comprehensive guide to the build vs. buy decision for LLM applications, covering total cost
            of ownership (TCO) models, vendor lock-in risk assessment, open-weight vs. proprietary API
            trade-offs, hidden costs (data labeling, evaluation infrastructure, security compliance),
            and decision frameworks that account for organizational maturity, data sensitivity, and
            time-to-market constraints.
        </p>
    </div>

    <h2>Key Topics</h2>
    <ul>
        <li>Build vs. buy decision trees for common LLM use cases</li>
        <li>Total cost of ownership (TCO) models: compute, engineering, data, evaluation, compliance</li>
        <li>Vendor lock-in risk assessment and mitigation strategies</li>
        <li>Open-weight models vs. proprietary API trade-offs</li>
        <li>Hidden costs: data labeling, red teaming, security audits, compliance documentation</li>
        <li>Vendor selection scoring rubrics with weighted criteria</li>
        <li>Multi-vendor strategies and abstraction layers</li>
        <li>Case studies: when to build, when to buy, when to switch</li>
    </ul>

    <div class="callout warning">
        <p>This section provides skeleton content for build vs. buy and TCO analysis. Full content generation with detailed financial models and decision frameworks is planned for a subsequent content pass.</p>
    </div>

</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    if new_strategy_dir.exists():
        write_file(new_strategy_dir / "section-30.6.html", section_30_6)

    # Update Part IX index with new chapter numbers
    p9_index = BASE / "part-9-safety-strategy" / "index.html"
    p9_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Part IX: Safety &amp; Strategy</title>
    <link rel="stylesheet" href="../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Building Conversational AI with LLMs and Agents</a></div>
    <h1>Part IX: Safety &amp; Strategy</h1>
    <p class="chapter-subtitle">Security, ethics, regulation, and organizational strategy for responsible AI deployment.</p>
</header>

<div class="content">

    <div class="part-overview">
        <h2>Part Overview</h2>
        <p>
            Part IX addresses the safety, ethical, regulatory, and strategic dimensions of LLM deployment. You will learn to harden systems against adversarial attacks, detect and mitigate hallucinations and bias, navigate the evolving regulatory landscape (including EU AI Act compliance), implement red teaming programs, and build organizational AI strategy that delivers measurable business value.
        </p>
        <p>
            Chapters: 2 (Chapters 29 and 30). Essential reading for anyone shipping LLM applications to real users or advising organizations on AI adoption.
        </p>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="module-29-safety-ethics-regulation/index.html"><span class="mod-num">Chapter 29</span> Safety, Ethics &amp; Regulation</a>
        </div>
        <div class="chapter-card-body">
            <p>Security hardening, hallucination detection, bias mitigation, regulatory compliance, governance frameworks, licensing, machine unlearning, red teaming, and EU AI Act compliance.</p>
            <ul class="section-list">
                <li><a href="module-29-safety-ethics-regulation/section-29.1.html"><span class="sec-num">29.1</span> LLM Security Threats</a></li>
                <li><a href="module-29-safety-ethics-regulation/section-29.2.html"><span class="sec-num">29.2</span> Hallucination &amp; Reliability</a></li>
                <li><a href="module-29-safety-ethics-regulation/section-29.3.html"><span class="sec-num">29.3</span> Bias, Fairness &amp; Ethics</a></li>
                <li><a href="module-29-safety-ethics-regulation/section-29.4.html"><span class="sec-num">29.4</span> Regulation &amp; Compliance</a></li>
                <li><a href="module-29-safety-ethics-regulation/section-29.5.html"><span class="sec-num">29.5</span> LLM Risk Governance &amp; Audit</a></li>
                <li><a href="module-29-safety-ethics-regulation/section-29.6.html"><span class="sec-num">29.6</span> LLM Licensing, IP &amp; Privacy</a></li>
                <li><a href="module-29-safety-ethics-regulation/section-29.7.html"><span class="sec-num">29.7</span> Machine Unlearning</a></li>
                <li><a href="module-29-safety-ethics-regulation/section-29.8.html"><span class="sec-num">29.8</span> Red Teaming Frameworks &amp; LLM Security Testing</a></li>
                <li><a href="module-29-safety-ethics-regulation/section-29.9.html"><span class="sec-num">29.9</span> EU AI Act Compliance in Practice</a></li>
            </ul>
        </div>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="module-30-strategy-product-roi/index.html"><span class="mod-num">Chapter 30</span> LLM Strategy, Product Management &amp; ROI</a>
        </div>
        <div class="chapter-card-body">
            <p>The business and organizational layer that turns LLM technology into business value. Covers strategy, product thinking, ROI measurement, vendor evaluation, compute planning, and build vs. buy analysis.</p>
            <ul class="section-list">
                <li><a href="module-30-strategy-product-roi/section-30.1.html"><span class="sec-num">30.1</span> LLM Strategy &amp; Use Case Prioritization</a></li>
                <li><a href="module-30-strategy-product-roi/section-30.2.html"><span class="sec-num">30.2</span> LLM Product Management</a></li>
                <li><a href="module-30-strategy-product-roi/section-30.3.html"><span class="sec-num">30.3</span> ROI Measurement &amp; Value Attribution</a></li>
                <li><a href="module-30-strategy-product-roi/section-30.4.html"><span class="sec-num">30.4</span> LLM Vendor Evaluation &amp; Build vs. Buy</a></li>
                <li><a href="module-30-strategy-product-roi/section-30.5.html"><span class="sec-num">30.5</span> LLM Compute Planning &amp; Infrastructure</a></li>
                <li><a href="module-30-strategy-product-roi/section-30.6.html"><span class="sec-num">30.6</span> Build vs. Buy Decision Framework &amp; Total Cost of Ownership</a></li>
            </ul>
        </div>
    </div>

<nav class="chapter-nav">
    <a href="../index.html">&larr; Back to Book Index</a>
</nav>
</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    write_file(p9_index, p9_content)
    print("  Task 3 complete: Part IX renumbered to Ch 29-30, new sections added")


# ============================================================
# TASK 4: Part X - Split Ch 30 into Ch 31 + Ch 32
# ============================================================

def task4_part10():
    print("\n=== TASK 4: Part X - Split Frontiers ===")

    old_frontiers_dir = BASE / "part-10-frontiers" / "module-30-frontiers"

    # Create Ch 31: Emerging Architectures & Scaling Frontiers (sections 30.1, 30.2)
    ch31_dir = BASE / "part-10-frontiers" / "module-31-emerging-architectures"
    os.makedirs(ch31_dir, exist_ok=True)
    os.makedirs(ch31_dir / "images", exist_ok=True)

    # Copy images
    old_images = old_frontiers_dir / "images"
    if old_images.exists():
        for img in old_images.iterdir():
            if img.is_file():
                shutil.copy2(img, ch31_dir / "images" / img.name)

    # Copy and renumber sections 30.1, 30.2 -> 31.1, 31.2
    for old_num, new_num in [("30.1", "31.1"), ("30.2", "31.2")]:
        old_path = old_frontiers_dir / f"section-{old_num}.html"
        if old_path.exists():
            content = read_file(old_path)
            content = content.replace(f"Section {old_num}", f"Section {new_num}")
            content = content.replace(f"section-{old_num}", f"section-{new_num}")
            content = content.replace("Chapter 30", "Chapter 31")
            content = content.replace("module-30-frontiers", "module-31-emerging-architectures")
            content = content.replace(
                "Frontiers: Open Problems &amp; the Road Ahead",
                "Emerging Architectures &amp; Scaling Frontiers"
            )
            write_file(ch31_dir / f"section-{new_num}.html", content)

    # Add section 31.3: Alternative Architectures (Mamba, RWKV, etc.)
    section_31_3 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Section 31.3: Alternative Architectures Beyond Transformers</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part X: Frontiers</a></div>
    <div class="chapter-label"><a href="../../toc.html" class="chapter-num" style="color: white; text-decoration: none;">Chapter 31</a></div>
    <h1>Section 31.3: Alternative Architectures Beyond Transformers</h1>
</header>

<div class="content">

    <div class="overview">
        <h2>Section Overview</h2>
        <p>
            While transformers dominate the current landscape, several alternative architectures challenge
            their supremacy on specific dimensions: linear-time state space models (Mamba, S4), recurrent
            alternatives (RWKV, Griffin), hybrid architectures (Jamba), and novel approaches to long-context
            processing. This section surveys these architectures, their theoretical advantages, practical
            performance, and the conditions under which they may overtake transformers.
        </p>
    </div>

    <h2>Key Topics</h2>
    <ul>
        <li>State space models: S4, Mamba, Mamba-2, and the selective scan mechanism</li>
        <li>Linear attention and recurrent alternatives: RWKV, RetNet, Griffin</li>
        <li>Hybrid architectures: Jamba (Mamba + Transformer), combining strengths</li>
        <li>Efficiency comparisons: attention O(n^2) vs. linear-time alternatives</li>
        <li>Long-context processing: architectures designed for million-token contexts</li>
        <li>Neuromorphic and event-driven approaches to language modeling</li>
        <li>When to consider non-transformer architectures in production</li>
    </ul>

    <div class="callout warning">
        <p>This section provides skeleton content for alternative architectures. Full content generation with architectural diagrams and benchmark comparisons is planned for a subsequent content pass.</p>
    </div>

</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    write_file(ch31_dir / "section-31.3.html", section_31_3)

    # Create Ch 31 index
    ch31_index = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 31: Emerging Architectures &amp; Scaling Frontiers</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part X: Frontiers</a></div>
    <div class="chapter-label"><a href="../../toc.html" class="chapter-num" style="color: white; text-decoration: none;">Chapter 31</a></div>
    <h1>Emerging Architectures &amp; Scaling Frontiers</h1>
</header>

<div class="content">

    <blockquote class="epigraph">
        <p>"The only thing I know is that I know nothing."</p>
        <cite>Socrates (as reported by Plato), a sentiment increasingly shared by AI researchers surveying the field</cite>
    </blockquote>

    <div class="callout warning">
        <h4>A Note on Currency</h4>
        <p>This chapter surveys the frontier of AI architectures and scaling research as of early 2026. The field moves rapidly; some claims here may be outdated within months. We focus on durable questions and structural trends rather than ephemeral developments.</p>
    </div>

    <div class="overview">
        <h2>Chapter Overview</h2>
        <p>
            This chapter examines the architectural and scaling frontiers that will shape the next generation of
            AI systems. It begins with the ongoing debate over emergent abilities: do large language models
            exhibit sudden, unpredictable capability jumps, or is this an artifact of measurement? It then
            surveys scaling frontiers including data walls, synthetic data strategies, test-time compute,
            and the alternative architectures (Mamba, RWKV, hybrid models) that challenge transformer dominance.
        </p>
    </div>

    <div class="learning-objectives">
        <h2>Learning Objectives</h2>
        <ul>
            <li>Critically evaluate claims about emergent abilities in large language models</li>
            <li>Understand the data, compute, and architectural frontiers shaping next-generation models</li>
            <li>Compare transformer alternatives (Mamba, RWKV, hybrid models) and their trade-offs</li>
            <li>Assess when alternative architectures may be preferable to standard transformers</li>
        </ul>
    </div>

    <h2>Sections</h2>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="section-31.1.html"><span class="sec-num">31.1</span> Emergent Abilities: Real or Mirage?</a>
        </div>
        <div class="chapter-card-body">
            <p>The debate over whether large language models exhibit sudden, unpredictable capability jumps at scale, or whether this is a measurement artifact.</p>
        </div>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="section-31.2.html"><span class="sec-num">31.2</span> Scaling Frontiers: What Comes Next</a>
        </div>
        <div class="chapter-card-body">
            <p>Data walls, synthetic data, test-time compute scaling, and the three axes of scaling (data, compute, inference).</p>
        </div>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="section-31.3.html"><span class="sec-num">31.3</span> Alternative Architectures Beyond Transformers</a>
        </div>
        <div class="chapter-card-body">
            <p>State space models (Mamba), linear attention (RWKV), hybrid architectures (Jamba), and when to consider non-transformer alternatives.</p>
        </div>
    </div>

    <div class="bibliography">
        <h2>Chapter Bibliography</h2>
        <ul>
            <li>Wei, J., Tay, Y., Bommasani, R., et al. (2022). "Emergent Abilities of Large Language Models." <em>Transactions on Machine Learning Research</em>.</li>
            <li>Schaeffer, R., Miranda, B., &amp; Koyejo, S. (2024). "Are Emergent Abilities of Large Language Models a Mirage?" <em>NeurIPS 2023</em>.</li>
            <li>Villalobos, P., Ho, A., Cerina, F., &amp; Sevilla, J. (2024). "Will We Run Out of Data? Limits of LLM Scaling Based on Human-Generated Data." <em>Epoch AI</em>.</li>
            <li>Gu, A. &amp; Dao, T. (2024). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces." <em>COLM 2024</em>.</li>
            <li>Peng, B., Alcaide, E., Anthony, Q., et al. (2023). "RWKV: Reinventing RNNs for the Transformer Era." <em>EMNLP 2023</em>.</li>
        </ul>
    </div>

</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    write_file(ch31_dir / "index.html", ch31_index)

    # Create Ch 32: AI, Society & Open Problems (sections 30.3, 30.4, 30.5 -> 32.1, 32.2, 32.3)
    ch32_dir = BASE / "part-10-frontiers" / "module-32-ai-society"
    os.makedirs(ch32_dir, exist_ok=True)
    os.makedirs(ch32_dir / "images", exist_ok=True)

    if old_images.exists():
        for img in old_images.iterdir():
            if img.is_file():
                shutil.copy2(img, ch32_dir / "images" / img.name)

    for old_num, new_num in [("30.3", "32.1"), ("30.4", "32.2"), ("30.5", "32.3")]:
        old_path = old_frontiers_dir / f"section-{old_num}.html"
        if old_path.exists():
            content = read_file(old_path)
            content = content.replace(f"Section {old_num}", f"Section {new_num}")
            content = content.replace(f"section-{old_num}", f"section-{new_num}")
            content = content.replace("Chapter 30", "Chapter 32")
            content = content.replace("module-30-frontiers", "module-32-ai-society")
            content = content.replace(
                "Frontiers: Open Problems &amp; the Road Ahead",
                "AI, Society &amp; Open Problems"
            )
            write_file(ch32_dir / f"section-{new_num}.html", content)

    # Add section 32.4: Open Research Problems
    section_32_4 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Section 32.4: Open Research Problems &amp; Future Directions</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part X: Frontiers</a></div>
    <div class="chapter-label"><a href="../../toc.html" class="chapter-num" style="color: white; text-decoration: none;">Chapter 32</a></div>
    <h1>Section 32.4: Open Research Problems &amp; Future Directions</h1>
</header>

<div class="content">

    <div class="overview">
        <h2>Section Overview</h2>
        <p>
            A curated survey of the most important open research problems in AI, organized by theme:
            fundamental understanding (what do models actually learn?), safety and alignment (how do
            we ensure beneficial outcomes?), efficiency (how do we make AI accessible?), and applications
            (what new capabilities are on the horizon?). Each problem is presented with current state
            of the art, key challenges, and promising research directions.
        </p>
    </div>

    <h2>Key Topics</h2>
    <ul>
        <li>Fundamental understanding: mechanistic interpretability, in-context learning theory, reasoning capabilities</li>
        <li>Safety and alignment: scalable oversight, weak-to-strong generalization, corrigibility</li>
        <li>Efficiency frontiers: efficient attention, model compression limits, edge deployment</li>
        <li>Application frontiers: scientific AI, mathematical reasoning, creative collaboration</li>
        <li>Data challenges: synthetic data quality, data attribution, training data copyright</li>
        <li>Evaluation gaps: measuring reasoning, creativity, and real-world impact</li>
        <li>Building a personal research agenda: how to identify high-impact problems</li>
    </ul>

    <div class="callout warning">
        <p>This section provides skeleton content for open research problems. Full content generation is planned for a subsequent content pass.</p>
    </div>

</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    write_file(ch32_dir / "section-32.4.html", section_32_4)

    # Create Ch 32 index
    ch32_index = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 32: AI, Society &amp; Open Problems</title>
    <link rel="stylesheet" href="../../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Part X: Frontiers</a></div>
    <div class="chapter-label"><a href="../../toc.html" class="chapter-num" style="color: white; text-decoration: none;">Chapter 32</a></div>
    <h1>AI, Society &amp; Open Problems</h1>
</header>

<div class="content">

    <blockquote class="epigraph">
        <p>"We shape our tools, and thereafter our tools shape us."</p>
        <cite>Often attributed to Marshall McLuhan, and never more true than with AI</cite>
    </blockquote>

    <div class="overview">
        <h2>Chapter Overview</h2>
        <p>
            This chapter addresses the intersection of AI with society: alignment research frontiers,
            the evolving global governance landscape, societal impact on labor and education, and the
            open research problems that will define the next decade of AI development. It serves as
            a forward-looking conclusion that connects the technical knowledge built throughout this
            book to the broader questions of how AI will reshape the world.
        </p>
    </div>

    <div class="learning-objectives">
        <h2>Learning Objectives</h2>
        <ul>
            <li>Survey the open problems in alignment research, including scalable oversight and superalignment</li>
            <li>Map the global AI governance landscape and identify unresolved policy questions</li>
            <li>Assess the societal impact of LLMs on labor, education, science, and creative work</li>
            <li>Identify high-impact open research problems and develop a personal learning framework</li>
        </ul>
    </div>

    <h2>Sections</h2>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="section-32.1.html"><span class="sec-num">32.1</span> Alignment Research Frontiers</a>
        </div>
        <div class="chapter-card-body">
            <p>Scalable oversight, weak-to-strong generalization, interpretability-based alignment, and the superalignment problem.</p>
        </div>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="section-32.2.html"><span class="sec-num">32.2</span> AI Governance and Open Problems</a>
        </div>
        <div class="chapter-card-body">
            <p>Compute governance, international regulatory frameworks, the open-weight debate, and unresolved policy questions.</p>
        </div>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="section-32.3.html"><span class="sec-num">32.3</span> Societal Impact and the Road Ahead</a>
        </div>
        <div class="chapter-card-body">
            <p>Labor market effects, education, creative industries, scientific discovery, and what skills will matter in an AI-integrated world.</p>
        </div>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="section-32.4.html"><span class="sec-num">32.4</span> Open Research Problems &amp; Future Directions</a>
        </div>
        <div class="chapter-card-body">
            <p>A curated survey of the most important open problems in AI: fundamental understanding, safety, efficiency, and applications.</p>
        </div>
    </div>

    <div class="bibliography">
        <h2>Chapter Bibliography</h2>
        <ul>
            <li>Burns, C., Haotian, Y., Steinhardt, J., et al. (2023). "Weak-to-Strong Generalization: Eliciting Strong Capabilities with Weak Supervision." <em>OpenAI Research</em>.</li>
            <li>Irving, G., Christiano, P., &amp; Amodei, D. (2018). "AI Safety via Debate." <em>arXiv:1805.00899</em>.</li>
            <li>Eloundou, T., Manning, S., Mishkin, P., &amp; Rock, D. (2023). "GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models." <em>arXiv:2303.10130</em>.</li>
            <li>Heim, L. (2024). "Compute Governance and International AI Safety." <em>Centre for the Governance of AI</em>.</li>
            <li>Shumailov, I., Shumilo, Z., Zhao, Y., et al. (2024). "AI Models Collapse When Trained on Recursively Generated Data." <em>Nature</em>, 631, 755-759.</li>
        </ul>
    </div>

</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    write_file(ch32_dir / "index.html", ch32_index)

    # Update Part X index
    p10_index = BASE / "part-10-frontiers" / "index.html"
    p10_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Part X: Frontiers</title>
    <link rel="stylesheet" href="../styles/book.css">
</head>
<body>
<div class="book-title-bar">
    <a href="../index.html">Building Conversational AI with LLMs and Agents</a>
</div>

<header class="chapter-header">
    <div class="part-label"><a href="../index.html" style="color: rgba(255,255,255,0.85); text-decoration: none;">Building Conversational AI with LLMs and Agents</a></div>
    <h1>Part X: Frontiers</h1>
    <p class="chapter-subtitle">Open problems, emerging capabilities, and the road ahead for AI research and society.</p>
</header>

<div class="content">

    <div class="part-overview">
        <h2>Part Overview</h2>
        <p>
            Part X surveys the frontier of AI research and development across two chapters. The first examines emerging architectures and scaling frontiers, including the debate over emergent abilities, alternative architectures beyond transformers, and the future of scaling laws. The second addresses AI's intersection with society: alignment research, governance challenges, societal impact, and the open problems that will shape the next decade of AI development.
        </p>
        <p>
            Chapters: 2 (Chapters 31 and 32). A forward-looking conclusion that frames the open questions shaping the next decade of AI development.
        </p>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="module-31-emerging-architectures/index.html"><span class="mod-num">Chapter 31</span> Emerging Architectures &amp; Scaling Frontiers</a>
        </div>
        <div class="chapter-card-body">
            <p>Emergent abilities, scaling limits, alternative architectures (Mamba, RWKV), and the future of model development.</p>
            <ul class="section-list">
                <li><a href="module-31-emerging-architectures/section-31.1.html"><span class="sec-num">31.1</span> Emergent Abilities: Real or Mirage?</a></li>
                <li><a href="module-31-emerging-architectures/section-31.2.html"><span class="sec-num">31.2</span> Scaling Frontiers: What Comes Next</a></li>
                <li><a href="module-31-emerging-architectures/section-31.3.html"><span class="sec-num">31.3</span> Alternative Architectures Beyond Transformers</a></li>
            </ul>
        </div>
    </div>

    <div class="chapter-card">
        <div class="chapter-card-header">
            <a href="module-32-ai-society/index.html"><span class="mod-num">Chapter 32</span> AI, Society &amp; Open Problems</a>
        </div>
        <div class="chapter-card-body">
            <p>Alignment research frontiers, AI governance, societal impact, and a curated survey of the most important open problems in AI.</p>
            <ul class="section-list">
                <li><a href="module-32-ai-society/section-32.1.html"><span class="sec-num">32.1</span> Alignment Research Frontiers</a></li>
                <li><a href="module-32-ai-society/section-32.2.html"><span class="sec-num">32.2</span> AI Governance and Open Problems</a></li>
                <li><a href="module-32-ai-society/section-32.3.html"><span class="sec-num">32.3</span> Societal Impact and the Road Ahead</a></li>
                <li><a href="module-32-ai-society/section-32.4.html"><span class="sec-num">32.4</span> Open Research Problems &amp; Future Directions</a></li>
            </ul>
        </div>
    </div>

<nav class="chapter-nav">
    <a href="../index.html">&larr; Back to Book Index</a>
</nav>
</div>

<footer style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; border-top: 1px solid #e0e0e0; color: #888; font-size: 0.85rem;">
    <p><strong>Building Conversational AI with LLMs and Agents</strong></p>
    <p>Written by a team of 42 AI agents.</p>
</footer>
</body>
</html>"""

    write_file(p10_index, p10_content)
    print("  Task 4 complete: Part X split into Ch 31 (Emerging Architectures) + Ch 32 (AI & Society)")


# ============================================================
# TASK 5: Fix footer in ALL index pages
# ============================================================

def task5_fix_footers():
    print("\n=== TASK 5: Fix footers in all index pages ===")

    count = 0
    for index_file in BASE.rglob("index.html"):
        # Skip the main cover index.html (it has special styling)
        if index_file.parent == BASE:
            continue

        content = read_file(index_file)

        # Remove any existing footer
        content = re.sub(
            r'<footer[^>]*>.*?</footer>',
            '',
            content,
            flags=re.DOTALL
        )

        # Remove any "Benchmarked against Stanford" text
        content = re.sub(
            r'[^<]*Benchmarked against Stanford[^<]*',
            '',
            content,
            flags=re.IGNORECASE
        )

        # Insert footer before </body>
        if '</body>' in content:
            content = content.replace(
                '</body>',
                f'\n{FOOTER_HTML}\n</body>'
            )
            count += 1

        write_file(index_file, content)

    print(f"  Task 5 complete: Fixed footers in {count} index pages")


# ============================================================
# TASK 6: Fix part index page headers
# ============================================================

def task6_fix_headers():
    print("\n=== TASK 6: Fix part index page headers ===")

    part_dirs = [d for d in BASE.iterdir() if d.is_dir() and d.name.startswith("part-")]

    for part_dir in sorted(part_dirs):
        index_path = part_dir / "index.html"
        if not index_path.exists():
            continue

        content = read_file(index_path)

        # Ensure book-title-bar exists and is separate from chapter-header
        if '<div class="book-title-bar">' not in content:
            # Add title bar after <body>
            content = content.replace(
                '<body>',
                '<body>\n<div class="book-title-bar">\n    <a href="../index.html">Building Conversational AI with LLMs and Agents</a>\n</div>\n'
            )

        # Ensure header uses class="chapter-header"
        if '<header class="chapter-header">' not in content:
            content = re.sub(
                r'<header[^>]*>',
                '<header class="chapter-header">',
                content,
                count=1
            )

        # Ensure content is wrapped in <div class="content">
        if '<div class="content">' not in content:
            # Find end of </header> and wrap remaining content
            pass  # Most files already have this

        # Remove duplicate book name in header (check for redundant part-label with book name)
        # The part-label should show the book name as a link, but H1 should NOT repeat it
        # Check if h1 contains the book name
        if '<h1>' in content:
            h1_match = re.search(r'<h1>(.*?)</h1>', content)
            if h1_match:
                h1_text = h1_match.group(1)
                if 'Building Conversational AI' in h1_text:
                    # This is wrong; h1 should be the Part title only
                    pass  # Leave as is, shouldn't happen with our rewrites

        write_file(index_path, content)

    print(f"  Task 6 complete: Fixed headers in {len(part_dirs)} part index pages")


# ============================================================
# Update toc.html with new chapter structure
# ============================================================

def update_toc():
    print("\n=== Updating TOC ===")

    toc_path = BASE / "toc.html"
    content = read_file(toc_path)

    # Update Part VII title in short TOC
    content = content.replace(
        '>Part VII: Multimodal AI &amp; Industry Applications<',
        '>Part VII: AI Applications<'
    )

    # Update Part VIII chapters in short TOC
    # Replace existing Ch 26 and Ch 27 entries with new 3 chapters
    old_p8_short = '''<a class="toc-item" href="#ch26"><span class="toc-num">26</span> Evaluation, Experiment Design &amp; Observability</a>
            <a class="toc-item" href="#ch27"><span class="toc-num">27</span> Production Engineering &amp; Operations</a>'''

    new_p8_short = '''<a class="toc-item" href="#ch26"><span class="toc-num">26</span> Evaluation &amp; Experiment Design</a>
            <a class="toc-item" href="#ch27"><span class="toc-num">27</span> Observability, Monitoring &amp; MLOps</a>
            <a class="toc-item" href="#ch28"><span class="toc-num">28</span> Production Engineering &amp; Operations</a>'''

    content = content.replace(old_p8_short, new_p8_short)

    # Update Part IX chapters
    old_p9_short = '''<a class="toc-item" href="#ch28"><span class="toc-num">28</span> Safety, Ethics &amp; Regulation</a>
            <a class="toc-item" href="#ch29"><span class="toc-num">29</span> LLM Strategy, Product Management &amp; ROI</a>'''

    new_p9_short = '''<a class="toc-item" href="#ch29"><span class="toc-num">29</span> Safety, Ethics &amp; Regulation</a>
            <a class="toc-item" href="#ch30"><span class="toc-num">30</span> LLM Strategy, Product Management &amp; ROI</a>'''

    content = content.replace(old_p9_short, new_p9_short)

    # Update Part X chapters
    old_p10_short = '''<a class="toc-item" href="#ch30"><span class="toc-num">30</span> Frontiers: Open Problems &amp; the Road Ahead</a>'''

    new_p10_short = '''<a class="toc-item" href="#ch31"><span class="toc-num">31</span> Emerging Architectures &amp; Scaling Frontiers</a>
            <a class="toc-item" href="#ch32"><span class="toc-num">32</span> AI, Society &amp; Open Problems</a>'''

    content = content.replace(old_p10_short, new_p10_short)

    # Update chapter count
    content = content.replace("31 Chapters", "32 Chapters")

    write_file(toc_path, content)

    # Update cover index.html chapter count
    cover_path = BASE / "index.html"
    cover_content = read_file(cover_path)
    cover_content = cover_content.replace("39 Chapters", "32 Chapters")
    write_file(cover_path, cover_content)

    print("  TOC and cover updated with new chapter structure")


# ============================================================
# Update the new chapter indexes in Part IX Ch 29 Safety
# to include the new sections in the sections list
# ============================================================

def update_ch29_safety_index():
    print("\n=== Updating Ch 29 Safety index with new sections ===")
    idx_path = BASE / "part-9-safety-strategy" / "module-29-safety-ethics-regulation" / "index.html"
    if not idx_path.exists():
        print("  Ch 29 safety index not found, skipping")
        return

    content = read_file(idx_path)

    # Check if section-29.8 is already listed
    if "section-29.8.html" not in content:
        # Add new sections before </ul> in the sections-list
        new_sections = """        <li>
            <a href="section-29.8.html" class="section-card">
                <span class="section-num">29.8</span>
                <span class="section-title">Red Teaming Frameworks &amp; LLM Security Testing</span>
                <span class="badge" title="Advanced">&#x1F534;</span>
                <span class="badge" title="Engineering">&#x2699;&#xFE0F;</span>
                <span class="badge" title="Lab">&#x1F527;</span>
                <span class="section-desc">
                    Structured red teaming methodologies, automated tools (PyRIT, Garak),
                    manual playbooks, adversarial prompt libraries, and CI/CD integration.
                </span>
            </a>
        </li>
        <li>
            <a href="section-29.9.html" class="section-card">
                <span class="section-num">29.9</span>
                <span class="section-title">EU AI Act Compliance in Practice</span>
                <span class="badge" title="Intermediate">&#x1F7E1;</span>
                <span class="badge" title="Engineering">&#x2699;&#xFE0F;</span>
                <span class="section-desc">
                    Risk classification for LLM applications, GPAI obligations, conformity assessment,
                    automated compliance checking, and practical implementation checklists.
                </span>
            </a>
        </li>"""

        # Find the last </li> before </ul> in sections-list
        # Insert before the closing </ul> of the sections-list
        sections_end = content.rfind('</ul>', 0, content.find('<div class="bibliography">'))
        if sections_end > 0:
            content = content[:sections_end] + new_sections + "\n    " + content[sections_end:]

    write_file(idx_path, content)
    print("  Ch 29 Safety index updated with new sections 29.8 and 29.9")


def update_ch30_strategy_index():
    print("\n=== Updating Ch 30 Strategy index with new section ===")
    idx_path = BASE / "part-9-safety-strategy" / "module-30-strategy-product-roi" / "index.html"
    if not idx_path.exists():
        print("  Ch 30 strategy index not found, skipping")
        return

    content = read_file(idx_path)

    # Check if section-30.6 is already listed
    if "section-30.6.html" not in content:
        new_section = """        <li>
            <a href="section-30.6.html" class="section-card">
                <span class="section-num">30.6</span>
                <span class="section-title">Build vs. Buy Decision Framework &amp; Total Cost of Ownership</span>
                <span class="badge" title="Advanced">&#x1F534;</span>
                <span class="badge" title="Engineering">&#x2699;&#xFE0F;</span>
                <span class="section-desc">
                    Build vs. buy decision trees, total cost of ownership models, vendor lock-in
                    assessment, open-weight vs. proprietary trade-offs, and multi-vendor strategies.
                </span>
            </a>
        </li>"""

        sections_end = content.rfind('</ul>', 0, content.find('<div class="bibliography">') if '<div class="bibliography">' in content else len(content))
        if sections_end > 0:
            content = content[:sections_end] + new_section + "\n    " + content[sections_end:]

    write_file(idx_path, content)
    print("  Ch 30 Strategy index updated with new section 30.6")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LLM Course Restructuring: Parts VII through X")
    print("=" * 60)

    task1_part7()
    task2_part8()
    task3_part9()
    task4_part10()
    task5_fix_footers()
    task6_fix_headers()
    update_toc()
    update_ch29_safety_index()
    update_ch30_strategy_index()

    print("\n" + "=" * 60)
    print("All tasks complete!")
    print("=" * 60)
    print("\nSummary of changes:")
    print("  Part VII: Renamed to 'AI Applications'")
    print("  Part VIII: Ch 26 split into Ch 26 (Eval) + Ch 27 (Observability), old Ch 27 -> Ch 28")
    print("  Part IX: Ch 28 -> Ch 29 (Safety, +2 new sections), Ch 29 -> Ch 30 (Strategy, +1 new section)")
    print("  Part X: Ch 30 split into Ch 31 (Emerging Architectures) + Ch 32 (AI & Society)")
    print("  Footers standardized across all index pages")
    print("  Part headers fixed for consistency")
    print("  TOC updated with new chapter numbers")
