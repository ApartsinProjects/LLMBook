"""
Split FM.2 (Reading Pathways) and FM.3 (Course Syllabi) into individual section files.
Each pathway and each course/track gets its own HTML page.
Updates index.html, toc.html, and the parent FM.2/FM.3 pages.
"""

import html
import os
import re

FM_DIR = r"E:\Projects\LLMCourse\front-matter"
TOC_PATH = r"E:\Projects\LLMCourse\toc.html"

# =============================================================================
# Chapter link mapping: canonical chapter references to actual hrefs
# (relative to front-matter/)
# =============================================================================
CH_LINKS = {
    "00": ("ML and PyTorch Foundations", "../part-1-foundations/module-00-ml-pytorch-foundations/index.html"),
    "01": ("Foundations of NLP and Text Representation", "../part-1-foundations/module-01-foundations-nlp-text-representation/index.html"),
    "02": ("Tokenization and Subword Models", "../part-1-foundations/module-02-tokenization-subword-models/index.html"),
    "03": ("Sequence Models and the Attention Mechanism", "../part-1-foundations/module-03-sequence-models-attention/index.html"),
    "04": ("The Transformer Architecture", "../part-1-foundations/module-04-transformer-architecture/index.html"),
    "05": ("Decoding Strategies and Text Generation", "../part-1-foundations/module-05-decoding-text-generation/index.html"),
    "06": ("Pre-training, Scaling Laws and Data Curation", "../part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html"),
    "07": ("The Modern LLM Landscape", "../part-2-understanding-llms/module-07-modern-llm-landscape/index.html"),
    "08": ("Reasoning Models and Test-Time Compute", "../part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html"),
    "09": ("Inference Optimization and Efficient Serving", "../part-2-understanding-llms/module-09-inference-optimization/index.html"),
    "10": ("Working with LLM APIs", "../part-3-working-with-llms/module-10-llm-apis/index.html"),
    "11": ("Prompt Engineering and Advanced Techniques", "../part-3-working-with-llms/module-11-prompt-engineering/index.html"),
    "12": ("Hybrid ML+LLM Architectures", "../part-3-working-with-llms/module-12-hybrid-ml-llm/index.html"),
    "13": ("Synthetic Data Generation", "../part-4-training-adapting/module-13-synthetic-data/index.html"),
    "14": ("Fine-Tuning Fundamentals", "../part-4-training-adapting/module-14-fine-tuning-fundamentals/index.html"),
    "15": ("Parameter-Efficient Fine-Tuning (PEFT)", "../part-4-training-adapting/module-15-peft/index.html"),
    "16": ("Knowledge Distillation and Model Merging", "../part-4-training-adapting/module-16-distillation-merging/index.html"),
    "17": ("Alignment: RLHF, DPO and Preference Tuning", "../part-4-training-adapting/module-17-alignment-rlhf-dpo/index.html"),
    "18": ("Interpretability and Mechanistic Understanding", "../part-2-understanding-llms/module-18-interpretability/index.html"),
    "19": ("Embeddings, Vector Databases and Semantic Search", "../part-5-retrieval-conversation/module-19-embeddings-vector-db/index.html"),
    "20": ("Retrieval-Augmented Generation (RAG)", "../part-5-retrieval-conversation/module-20-rag/index.html"),
    "21": ("Building Conversational AI Systems", "../part-5-retrieval-conversation/module-21-conversational-ai/index.html"),
    "22": ("AI Agent Foundations", "../part-6-agentic-ai/module-22-ai-agents/index.html"),
    "23": ("Tool Use, Function Calling and Protocols", "../part-6-agentic-ai/module-23-tool-use-protocols/index.html"),
    "24": ("Multi-Agent Systems", "../part-6-agentic-ai/module-24-multi-agent-systems/index.html"),
    "25": ("Specialized Agents", "../part-6-agentic-ai/module-25-specialized-agents/index.html"),
    "26": ("Agent Safety, Production and Operations", "../part-6-agentic-ai/module-26-agent-safety-production/index.html"),
    "27": ("Multimodal Generation", "../part-7-multimodal-applications/module-27-multimodal/index.html"),
    "28": ("LLM Applications Across Industries", "../part-7-multimodal-applications/module-28-llm-applications/index.html"),
    "29": ("Evaluation and Experiment Design", "../part-8-evaluation-production/module-29-evaluation-observability/index.html"),
    "30": ("Observability, Monitoring and MLOps", "../part-8-evaluation-production/module-30-observability-monitoring/index.html"),
    "31": ("Production Engineering and Operations", "../part-8-evaluation-production/module-31-production-engineering/index.html"),
    "32": ("Safety, Ethics and Regulation", "../part-9-safety-strategy/module-32-safety-ethics-regulation/index.html"),
    "33": ("LLM Strategy, Product Management and ROI", "../part-9-safety-strategy/module-33-strategy-product-roi/index.html"),
    "34": ("Emerging Architectures and Scaling Frontiers", "../part-10-frontiers/module-34-emerging-architectures/index.html"),
    "35": ("AI, Society and Open Problems", "../part-10-frontiers/module-35-ai-society/index.html"),
}

# Some special section-level links
SECTION_LINKS = {
    "Section 6.4": ("Data Curation at Scale", "../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.4.html"),
    "Section 9.6": ("Test-Time Compute", "../part-2-understanding-llms/module-09-inference-optimization/section-9.6.html"),
    "Section 11.3": ("DSPy and AutoML for Prompts", "../part-3-working-with-llms/module-11-prompt-engineering/section-11.3.html"),
    "Section 14.6": ("Fine-Tuning for Classification", "../part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.6.html"),
    "Section 19.4": ("Document Processing and Chunking", "../part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.4.html"),
    "Section 28.7": ("Robotics Applications", "../part-7-multimodal-applications/module-28-llm-applications/section-28.7.html"),
    "Sections 14.1 through 14.3": ("Fine-Tuning Basics", "../part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html"),
    "Part X": ("Frontiers: Open Problems and the Road Ahead", "../part-10-frontiers/index.html"),
}


def ch_link(num, custom_title=None):
    """Return an <a> tag linking to a chapter."""
    title, href = CH_LINKS[num]
    display = custom_title if custom_title else f"Chapter {num}: {title}"
    return f'<a href="{href}">{display}</a>'


def ch_short(num):
    """Return a short 'Ch N' link."""
    title, href = CH_LINKS[num]
    return f'<a href="{href}">Ch {num}</a>'


def sec_link(key, custom_title=None):
    """Return an <a> tag linking to a section."""
    title, href = SECTION_LINKS[key]
    display = custom_title if custom_title else f"{key}: {title}"
    return f'<a href="{href}">{display}</a>'


def page_template(title_text, section_num, h1_text, content_html, prev_link, next_link, extra_style=""):
    """Generate a complete HTML page."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title_text)}</title>
    <link rel="stylesheet" href="../styles/book.css">
    <style>
        .pathway-card {{
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1.2rem 0;
            background: #fafafa;
        }}
        .pathway-card h4 {{
            margin-top: 0;
            color: var(--accent);
        }}
        .pathway-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }}
        .pathway-meta span {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }}
        .pathway-meta .label {{
            font-weight: 600;
            color: var(--highlight);
        }}
        .chapter-list {{
            list-style: none;
            padding: 0;
        }}
        .chapter-list li {{
            padding: 0.5rem 0;
            border-bottom: 1px solid #eee;
        }}
        .chapter-list li:last-child {{
            border-bottom: none;
        }}
        .chapter-list .action {{
            display: inline-block;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            margin-right: 0.5rem;
        }}
        .action-focus {{ background: #e8f5e9; color: #2e7d32; }}
        .action-skim {{ background: #fff3e0; color: #e65100; }}
        .action-skip {{ background: #fce4ec; color: #c62828; }}
        .action-start {{ background: #e3f2fd; color: #1565c0; }}
        .action-supplement {{ background: #f3e5f5; color: #6a1b9a; }}
        .syllabus-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        .syllabus-table th, .syllabus-table td {{
            padding: 0.6rem 0.8rem;
            border: 1px solid #ddd;
            text-align: left;
        }}
        .syllabus-table th {{
            background: var(--primary);
            color: white;
            font-weight: 600;
        }}
        .syllabus-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        .track-steps {{
            counter-reset: track-step;
            list-style: none;
            padding: 0;
        }}
        .track-steps li {{
            counter-increment: track-step;
            padding: 0.8rem 0 0.8rem 2.5rem;
            border-bottom: 1px solid #eee;
            position: relative;
        }}
        .track-steps li::before {{
            content: counter(track-step);
            position: absolute;
            left: 0;
            top: 0.7rem;
            width: 1.8rem;
            height: 1.8rem;
            background: var(--accent);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.85rem;
        }}
        .track-steps li:last-child {{
            border-bottom: none;
        }}{extra_style}
    </style>
</head>
<body>
<header class="chapter-header">
    <nav class="header-nav">
        <a href="../index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="../toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <div class="part-label"><a href="index.html">Front Matter</a></div>
    <h1>{h1_text}</h1>
</header>

<main class="content">

{content_html}

    <nav class="chapter-nav" style="margin-top: 3rem; padding-top: 1.5rem; border-top: 2px solid #eee; display: flex; justify-content: space-between;">
        <a href="{prev_link[0]}">&larr; {prev_link[1]}</a>
        <a href="{next_link[0]}">{next_link[1]} &rarr;</a>
    </nav>

    <footer>
        <p>&copy; 2025 Building Conversational AI with LLMs and Agents</p>
    </footer>
</main>
</body>
</html>
'''


# =============================================================================
# PATHWAY DEFINITIONS (15 pathways)
# =============================================================================

pathways = [
    {
        "num": 1,
        "slug": "product-builder",
        "short_title": "Build AI Products",
        "full_title": 'Pathway 1: "I Want to Build AI Products" (Product Manager / Startup Founder)',
        "time": "4 to 6 weeks",
        "difficulty": "Beginner to Intermediate",
        "audience": "Product managers, startup founders, business leaders building AI-powered products",
        "goal": "Understand what LLMs can and cannot do, how to build products around them, and how to evaluate cost, quality, and risk.",
        "chapters": [
            ("skip", "00", "ML and PyTorch Foundations"),
            ("skip", "01", "NLP and Text Representation"),
            ("skip", "02", "Tokenization and Subword Models"),
            ("skip", "03", "Sequence Models and Attention"),
            ("skip", "04", "The Transformer Architecture"),
            ("skip", "05", "Decoding and Text Generation"),
            ("skim", "06", "Pre-training and Scaling Laws"),
            ("skim", "07", "The Modern LLM Landscape"),
            ("skim", "08", "Reasoning Models"),
            ("skim", "09", "Inference Optimization"),
            ("focus", "10", "Working with LLM APIs"),
            ("focus", "11", "Prompt Engineering"),
            ("focus", "12", "Hybrid ML+LLM Architectures"),
            ("skip", "13", "Synthetic Data"),
            ("skip", "14", "Fine-Tuning Fundamentals"),
            ("skip", "15", "PEFT"),
            ("skip", "16", "Distillation and Merging"),
            ("skip", "17", "Alignment"),
            ("skip", "18", "Interpretability"),
            ("focus", "20", "RAG"),
            ("focus", "22", "AI Agents"),
            ("focus", "28", "LLM Applications"),
            ("focus", "29", "Evaluation and Experiment Design"),
            ("focus", "31", "Production Engineering"),
            ("focus", "32", "Safety, Ethics and Regulation"),
            ("focus", "33", "Strategy, Product and ROI"),
        ],
    },
    {
        "num": 2,
        "slug": "ml-engineer",
        "short_title": "Fine-Tune and Train Models",
        "full_title": 'Pathway 2: "I Want to Fine-Tune and Train Models" (ML Engineer)',
        "time": "6 to 8 weeks",
        "difficulty": "Intermediate to Advanced",
        "audience": "ML engineers with existing deep learning experience who want to specialize in LLM training",
        "goal": "Master the full training pipeline from data preparation through alignment, with practical experience on real hardware.",
        "chapters": [
            ("start", "03", "Sequence Models and Attention (start here if you need a transformer refresher; otherwise start at Ch 6)"),
            ("focus", "06", "Pre-training and Scaling Laws"),
            ("focus", "07", "The Modern LLM Landscape"),
            ("focus", "09", f'Inference Optimization (including {sec_link("Section 9.6", "Section 9.6: Test-Time Compute")})'),
            ("focus", "13", "Synthetic Data Generation"),
            ("focus", "14", "Fine-Tuning Fundamentals"),
            ("focus", "15", "PEFT (LoRA, QLoRA)"),
            ("focus", "16", "Knowledge Distillation and Model Merging"),
            ("focus", "17", "Alignment (RLHF, DPO)"),
            ("focus", "29", "Evaluation and Experiment Design"),
        ],
    },
    {
        "num": 3,
        "slug": "agent-builder",
        "short_title": "Build AI Agents",
        "full_title": 'Pathway 3: "I Want to Build AI Agents" (Software Engineer)',
        "time": "4 to 6 weeks",
        "difficulty": "Intermediate",
        "audience": "Software engineers who want to build autonomous AI agent systems",
        "goal": "Build autonomous agents that use tools, maintain state, coordinate with other agents, and interact with users through modern protocols (MCP, AG-UI).",
        "chapters": [
            ("start", "00", "ML and PyTorch Foundations (review if new to ML)"),
            ("start", "01", "NLP and Text Representation (review if new to ML)"),
            ("focus", "10", "Working with LLM APIs"),
            ("focus", "11", "Prompt Engineering"),
            ("focus", "19", "Embeddings and Vector Databases"),
            ("focus", "20", "RAG"),
            ("focus", "21", "Conversational AI"),
            ("focus", "22", "AI Agent Foundations"),
            ("focus", "24", "Multi-Agent Systems"),
            ("focus", "28", "LLM Applications"),
            ("focus", "29", "Evaluation and Experiment Design"),
        ],
    },
    {
        "num": 4,
        "slug": "platform-devops",
        "short_title": "Deploy LLMs in Production",
        "full_title": 'Pathway 4: "I Want to Deploy LLMs in Production" (Platform / DevOps Engineer)',
        "time": "3 to 4 weeks",
        "difficulty": "Intermediate",
        "audience": "Platform engineers, DevOps engineers, and SREs responsible for LLM infrastructure",
        "goal": "Understand how to serve, monitor, scale, and secure LLM-powered systems in production environments.",
        "chapters": [
            ("skim", "06", "Pre-training and Scaling Laws (context on model capabilities and costs)"),
            ("skim", "07", "The Modern LLM Landscape (context on model capabilities and costs)"),
            ("focus", "09", "Inference Optimization"),
            ("focus", "10", "Working with LLM APIs"),
            ("focus", "20", "RAG (infrastructure sections)"),
            ("focus", "29", "Evaluation and Observability"),
            ("focus", "31", "Production Engineering and LLMOps"),
            ("focus", "32", "Safety, Ethics and Security"),
            ("focus", "33", "Strategy and ROI"),
        ],
    },
    {
        "num": 5,
        "slug": "researcher",
        "short_title": "Research LLMs",
        "full_title": 'Pathway 5: "I\'m a Researcher Exploring LLMs" (PhD Student / Researcher)',
        "time": "10 to 12 weeks",
        "difficulty": "Advanced",
        "audience": "PhD students, postdocs, and research scientists studying LLM capabilities and limitations",
        "goal": "Develop both theoretical depth and practical fluency. Use the annotated bibliographies as entry points into the research literature.",
        "chapters": [
            ("focus", "04", "The Transformer Architecture"),
            ("focus", "06", "Pre-training and Scaling Laws"),
            ("focus", "07", "Model Architectures (MoE, SSMs)"),
            ("focus", "09", f'Inference Optimization (especially {sec_link("Section 9.6", "Section 9.6: Test-Time Compute")})'),
            ("focus", "13", "Synthetic Data Generation"),
            ("focus", "17", "Alignment (RLHF, DPO, Constitutional AI)"),
            ("focus", "18", "Interpretability and Mechanistic Understanding"),
        ],
        "extra_note": "Read the full book with particular emphasis on the Research Frontier sections at the end of each chapter.",
    },
    {
        "num": 6,
        "slug": "career-changer",
        "short_title": "New to ML",
        "full_title": 'Pathway 6: "I\'m Completely New to ML" (Career Changer)',
        "time": "16 to 20 weeks",
        "difficulty": "Beginner",
        "audience": "Career changers, bootcamp graduates, and self-taught developers entering the AI field",
        "goal": "Build a complete mental model of the LLM stack, from basic linear algebra through production agent systems, with working code at every step.",
        "chapters": [
            ("start", "00", "ML and PyTorch Foundations (your starting point)"),
            ("focus", "01", "NLP and Text Representation"),
            ("focus", "02", "Tokenization and Subword Models"),
            ("focus", "03", "Sequence Models and Attention"),
            ("focus", "04", "The Transformer Architecture"),
            ("focus", "05", "Decoding and Text Generation"),
        ],
        "extra_note": "Start at Chapter 00 and read sequentially. Do not skip chapters. Complete every lab exercise; the hands-on practice is essential for building genuine understanding. Plan for roughly two chapters per week through Part I, then one chapter per week for the remaining material.",
    },
    {
        "num": 7,
        "slug": "data-scientist",
        "short_title": "Data Scientist Adding LLMs",
        "full_title": 'Pathway 7: "I\'m a Data Scientist Adding LLMs to My Toolkit" (Data Scientist / Analyst)',
        "time": "5 to 7 weeks",
        "difficulty": "Intermediate",
        "audience": "Data scientists and analysts who already know Python, pandas, scikit-learn, and basic deep learning",
        "goal": "Learn where LLMs complement (not replace) your existing ML models, how to build hybrid pipelines, and how to use LLMs for feature engineering, classification, extraction, and analytics.",
        "chapters": [
            ("skim", "00", "ML and PyTorch Foundations (refresh if needed)"),
            ("skim", "01", "NLP and Text Representation (refresh if needed)"),
            ("skim", "02", "Tokenization (refresh if needed)"),
            ("focus", "03", "Sequence Models and Attention"),
            ("skim", "04", "The Transformer Architecture (unless curious about internals)"),
            ("focus", "05", "Decoding and Text Generation"),
            ("focus", "10", "Working with LLM APIs"),
            ("focus", "11", f'Prompt Engineering (including {sec_link("Section 11.3", "Section 11.3: DSPy and AutoML for Prompts")})'),
            ("focus", "12", "Hybrid ML+LLM Architectures"),
            ("focus", "19", "Embeddings and Vector Databases"),
            ("focus", "20", "RAG"),
            ("focus", "28", "LLM Applications"),
            ("focus", "29", "Evaluation and Experiment Design"),
        ],
    },
    {
        "num": 8,
        "slug": "nlp-engineer",
        "short_title": "NLP to LLMs",
        "full_title": 'Pathway 8: "I\'m an NLP Engineer Transitioning to LLMs" (NLP / Text Mining Professional)',
        "time": "4 to 5 weeks",
        "difficulty": "Intermediate",
        "audience": "NLP professionals who know spaCy, NLTK, BERT fine-tuning, NER, and text classification",
        "goal": "Understand how LLMs change the NLP landscape, when to use prompting vs. fine-tuning vs. classical NLP, and how to migrate existing pipelines to LLM-augmented architectures.",
        "chapters": [
            ("skip", "00", "ML and PyTorch Foundations (you know this)"),
            ("skip", "01", "NLP and Text Representation (you know this)"),
            ("skip", "02", "Tokenization (you know this)"),
            ("skim", "03", "Attention (review if needed)"),
            ("focus", "04", "The Transformer Architecture (deeper than BERT)"),
            ("focus", "05", "Decoding Strategies"),
            ("focus", "06", "Pre-training and Scaling Laws"),
            ("focus", "10", "Working with LLM APIs"),
            ("focus", "11", "Prompt Engineering"),
            ("focus", "12", "Hybrid ML+LLM Architectures"),
            ("focus", "14", "Fine-Tuning Fundamentals"),
            ("focus", "15", "PEFT (LoRA, QLoRA)"),
            ("focus", "17", "Alignment (RLHF, DPO)"),
            ("focus", "20", "RAG"),
        ],
    },
    {
        "num": 9,
        "slug": "fullstack-developer",
        "short_title": "Full-Stack AI Features",
        "full_title": 'Pathway 9: "I\'m a Full-Stack Developer Adding AI Features" (Web / App Developer)',
        "time": "3 to 4 weeks",
        "difficulty": "Beginner to Intermediate",
        "audience": "Web and app developers who know JavaScript/Python, REST APIs, databases, and web frameworks",
        "goal": "Add AI-powered features (chat, search, extraction, generation) to your applications using APIs and frameworks, without needing to train any models.",
        "chapters": [
            ("skip", "00", "ML and PyTorch Foundations"),
            ("skip", "01", "NLP and Text Representation"),
            ("skip", "02", "Tokenization"),
            ("skip", "03", "Attention"),
            ("skip", "04", "The Transformer Architecture"),
            ("skip", "05", "Decoding"),
            ("skip", "06", "Pre-training and Scaling Laws"),
            ("skip", "07", "Model Landscape"),
            ("skip", "08", "Reasoning Models"),
            ("skip", "09", "Inference Optimization"),
            ("focus", "10", "Working with LLM APIs (your starting point)"),
            ("focus", "11", "Prompt Engineering"),
            ("focus", "19", "Embeddings and Vector Databases"),
            ("focus", "20", "RAG"),
            ("focus", "21", "Conversational AI"),
            ("focus", "22", "AI Agents"),
            ("focus", "28", "LLM Applications"),
            ("focus", "31", "Production Engineering"),
        ],
    },
    {
        "num": 10,
        "slug": "tech-leader",
        "short_title": "LLM Strategy for Leaders",
        "full_title": 'Pathway 10: "I\'m a Technical Leader Evaluating LLM Strategy" (CTO / Tech Lead / Architect)',
        "time": "2 to 3 weeks",
        "difficulty": "Overview (non-coding)",
        "audience": "CTOs, tech leads, and software architects who need to make informed build-vs-buy decisions",
        "goal": "Develop a mental model for LLM capabilities and limitations, understand cost structures, make architectural decisions, and evaluate vendor solutions with confidence.",
        "chapters": [
            ("skim", "04", "The Transformer Architecture (concepts only)"),
            ("skim", "06", "Pre-training and Scaling Laws (cost implications)"),
            ("skim", "07", "The Modern LLM Landscape (choosing models)"),
            ("skim", "09", "Inference Optimization (cost and latency)"),
            ("focus", "10", "Working with LLM APIs"),
            ("focus", "11", "Prompt Engineering"),
            ("focus", "20", "RAG"),
            ("focus", "29", "Evaluation and Experiment Design"),
            ("focus", "31", "Production Engineering"),
            ("focus", "32", "Safety and Compliance"),
            ("focus", "33", "Strategy, Product and ROI"),
        ],
    },
    {
        "num": 11,
        "slug": "domain-expert",
        "short_title": "Domain Expert Applying LLMs",
        "full_title": 'Pathway 11: "I\'m a Domain Expert Applying LLMs" (Healthcare / Legal / Finance Professional)',
        "time": "4 to 5 weeks",
        "difficulty": "Beginner to Intermediate",
        "audience": "Healthcare, legal, finance, and other domain professionals with deep expertise but limited ML background",
        "goal": "Build LLM applications tailored to your domain while navigating regulatory requirements, ensuring accuracy, and integrating with existing professional workflows.",
        "chapters": [
            ("start", "00", "ML and PyTorch Foundations (if unfamiliar with ML concepts)"),
            ("focus", "10", "Working with LLM APIs (your practical starting point)"),
            ("focus", "11", "Prompt Engineering"),
            ("focus", "12", "Hybrid ML+LLM Architectures"),
            ("focus", "14", "Fine-Tuning Fundamentals"),
            ("focus", "20", "RAG"),
            ("focus", "28", "LLM Applications (healthcare in 28.3, finance in 28.2, legal in 28.6)"),
            ("focus", "32", "Safety, Ethics and Compliance"),
        ],
    },
    {
        "num": 12,
        "slug": "safety-alignment",
        "short_title": "AI Safety and Alignment",
        "full_title": 'Pathway 12: "I Want to Understand AI Safety and Alignment" (Safety Researcher / Policy Analyst)',
        "time": "5 to 6 weeks",
        "difficulty": "Intermediate to Advanced",
        "audience": "AI safety researchers, policy analysts, and ethicists studying LLM risks and alignment",
        "goal": "Understand the technical mechanisms behind LLM safety challenges, current alignment approaches, interpretability tools, and the regulatory landscape.",
        "chapters": [
            ("start", "03", "Sequence Models and Attention (prerequisite)"),
            ("start", "04", "The Transformer Architecture (prerequisite)"),
            ("focus", "06", "Pre-training and Scaling Laws (emergent capabilities)"),
            ("focus", "09", f'Inference Optimization ({sec_link("Section 9.6", "Section 9.6: Test-Time Compute")})'),
            ("focus", "17", "Alignment (RLHF, DPO, Constitutional AI)"),
            ("focus", "18", "Interpretability and Mechanistic Understanding"),
            ("focus", "29", "Evaluation (measuring safety)"),
            ("focus", "32", "Safety, Ethics and Regulation"),
            ("skim", "07", "The Modern LLM Landscape"),
            ("skim", "24", "Multi-Agent Systems (emergent behaviors)"),
        ],
    },
    {
        "num": 13,
        "slug": "rag-search",
        "short_title": "RAG and Search Systems",
        "full_title": 'Pathway 13: "I Want to Build RAG and Search Systems" (Search / Knowledge Engineer)',
        "time": "4 to 5 weeks",
        "difficulty": "Intermediate",
        "audience": "Search engineers, knowledge engineers, and information retrieval professionals",
        "goal": "Master the full retrieval pipeline from document processing through embedding, indexing, retrieval, reranking, and generation, with production evaluation methods.",
        "chapters": [
            ("focus", "01", "Text Representation (foundations for embeddings)"),
            ("focus", "19", "Embeddings and Vector Databases (all sections)"),
            ("focus", "20", "RAG (all 6 sections; your core chapter)"),
            ("focus", "29", "Evaluation (Section 29.3: RAG evaluation)"),
            ("supplement", "10", "Working with LLM APIs"),
            ("supplement", "11", "Prompt Engineering"),
            ("supplement", "12", "Hybrid ML+LLM Architectures"),
        ],
    },
    {
        "num": 14,
        "slug": "open-source",
        "short_title": "Open-Source LLM Contributor",
        "full_title": 'Pathway 14: "I Want to Contribute to Open-Source LLM Projects" (Open-Source Developer)',
        "time": "8 to 10 weeks",
        "difficulty": "Advanced",
        "audience": "Open-source developers who want to contribute to projects like vLLM, llama.cpp, or Hugging Face Transformers",
        "goal": "Understand LLM internals deeply enough to contribute meaningful code to training frameworks, inference engines, and model libraries.",
        "chapters": [
            ("focus", "00", "ML and PyTorch Foundations"),
            ("focus", "04", "The Transformer Architecture"),
            ("focus", "05", "Decoding Strategies"),
            ("focus", "06", "Pre-training and Scaling Laws"),
            ("focus", "07", "The Modern LLM Landscape"),
            ("focus", "09", "Inference Optimization"),
            ("focus", "14", "Fine-Tuning Fundamentals"),
            ("focus", "15", "PEFT (LoRA, QLoRA)"),
            ("focus", "18", "Interpretability"),
            ("supplement", "16", "Knowledge Distillation and Model Merging"),
            ("supplement", "17", "Alignment (RLHF, DPO)"),
        ],
    },
    {
        "num": 15,
        "slug": "hobbyist",
        "short_title": "Weekend Projects",
        "full_title": 'Pathway 15: "I\'m a Hobbyist Building Weekend Projects" (Curious Tinkerer)',
        "time": "3 to 4 weeks (pick and choose)",
        "difficulty": "Beginner",
        "audience": "Hobbyists and curious tinkerers who want to build fun, useful things with LLMs",
        "goal": "Get from idea to working prototype as fast as possible, then go deeper in whichever direction excites you most.",
        "chapters": [
            ("start", "10", "Working with LLM APIs (get something working in 30 minutes)"),
            ("start", "11", "Prompt Engineering (make it work well)"),
        ],
        "adventures": [
            ("Build a chatbot", "21", "Conversational AI"),
            ("Build a personal knowledge base", "19", "Embeddings", "20", "RAG"),
            ("Build an AI agent", "22", "AI Agents"),
            ("Fine-tune a small model", "14", "Fine-Tuning", "15", "PEFT/LoRA"),
        ],
    },
]


# =============================================================================
# COURSE DEFINITIONS (4 courses)
# =============================================================================

courses = [
    {
        "id": "A",
        "slug": "undergrad-engineering",
        "short_title": "Undergraduate Engineering",
        "full_title": "Course A: Undergraduate Engineering",
        "description": "Focus: Foundations, using LLM APIs, building basic agents. Students leave able to build and deploy LLM-powered applications. This pathway spends the first five weeks on foundations because undergraduates typically lack exposure to attention mechanisms and tokenization; skipping this material would leave them unable to debug prompt failures or understand why a model generates unexpected output. The second half jumps to the applied chapters (APIs, RAG, agents) because the goal is practical competency.",
        "weeks": [
            ("1", "00", "ML and PyTorch Foundations", "Build and train an image classifier in PyTorch"),
            ("2", "01", "NLP and Text Representation", "Build a TF-IDF search engine"),
            ("3", "02", "Tokenization and Subword Models", "Train a BPE tokenizer from scratch"),
            ("4", "03", "Attention and Transformers (Ch 3 through 4)", "Implement scaled dot-product attention"),
            ("5", "05", "Decoding and Text Generation", "Compare decoding strategies on GPT-2"),
            ("6", "10", "Working with LLM APIs", "Build a multi-provider API client"),
            ("7", "11", "Prompt Engineering", "Prompt optimization challenge (few-shot, CoT)"),
            ("8", "19", "Embeddings and Vector Databases", "Build a semantic search system"),
            ("9", "20", "RAG Fundamentals", "Build a document QA system with RAG"),
            ("10", "21", "Conversational AI", "Build a multi-turn chatbot with memory"),
            ("11", "22", "AI Agents: Tool Use and Planning", "Build an agent with tool calling"),
            ("12", "29", "Evaluation and Observability", "Evaluate an LLM system with automated metrics"),
            ("13", "31", "Production Engineering", "Deploy an LLM application with monitoring"),
            ("14", None, "Final project presentations", "End-to-end LLM application (team project)"),
        ],
    },
    {
        "id": "B",
        "slug": "undergrad-research",
        "short_title": "Undergraduate Research",
        "full_title": "Course B: Undergraduate Research",
        "description": "Focus: Architecture internals, training methods, interpretability. Students leave with a deep understanding of how LLMs work and how to study them. This pathway trades breadth for depth: it covers the same foundations as Course A but then dives into pre-training, scaling laws, PEFT, and alignment. The reasoning is that future researchers need to understand the training pipeline end to end, since that is where novel contributions happen.",
        "weeks": [
            ("1", "00", "ML and PyTorch Foundations", "Build and train an image classifier in PyTorch"),
            ("2", "01", "NLP, Text Representation, Tokenization (Ch 1 through 2)", "Compare tokenizer vocabulary coverage across languages"),
            ("3", "03", "Sequence Models and Attention", "Implement attention from scratch, visualize attention weights"),
            ("4", "04", "The Transformer Architecture", "Build a minimal transformer (encoder + decoder)"),
            ("5", "05", "Decoding Strategies", "Implement nucleus sampling, measure diversity vs. quality"),
            ("6", "06", "Pre-training and Scaling Laws", "Reproduce a scaling law curve on a small model"),
            ("7", "07", "Modern LLM Landscape", "Compare model architectures (paper reading assignment)"),
            ("8", "09", "Inference Optimization", "Benchmark KV-cache and quantization effects"),
            ("9", "13", "Synthetic Data Generation", "Generate and validate a synthetic training dataset"),
            ("10", "14", "Fine-Tuning Fundamentals", "Fine-tune a small model on a custom task"),
            ("11", "15", "PEFT (LoRA, QLoRA)", "Compare full fine-tuning vs. LoRA on the same task"),
            ("12", "17", "Alignment (RLHF, DPO)", "Implement DPO training on a preference dataset"),
            ("13", "18", "Interpretability", "Probe internal representations with logit lens"),
            ("14", None, "Final project presentations", "Research paper replication or extension (individual project)"),
        ],
    },
    {
        "id": "C",
        "slug": "grad-engineering",
        "short_title": "Graduate Engineering",
        "full_title": "Course C: Graduate Engineering",
        "description": "Focus: Full stack from APIs through production deployment. Students leave able to architect, build, and operate LLM systems at scale. This pathway assumes students already have solid ML fundamentals, so it starts with a transformer review and quickly moves to the practitioner stack. The ordering (inference optimization before APIs, fine-tuning before RAG, agents before production) mirrors the typical system design sequence.",
        "weeks": [
            ("1", "04", "Transformers and Decoding (review, Ch 4 through 5)", "Implement a transformer block with KV-cache"),
            ("2", "06", "Pre-training, Scaling, Model Landscape (Ch 6 through 7)", "Analyze compute-optimal training configurations"),
            ("3", "09", "Inference Optimization", "Profile and optimize inference latency"),
            ("4", "10", "APIs and Prompt Engineering (Ch 10 through 11, incl. DSPy)", "Build a production prompt management system"),
            ("5", "12", "Hybrid ML+LLM Architectures", "Design an ML+LLM pipeline for a real use case"),
            ("6", "14", "Fine-Tuning and PEFT (Ch 14 through 15)", "LoRA fine-tune a 7B model on domain data"),
            ("7", "19", "Embeddings, Vector DBs, RAG (Ch 19 through 20)", "Build a production RAG pipeline with evaluation"),
            ("8", "21", "Conversational AI", "Build a task-oriented dialogue system"),
            ("9", "22", "AI Agents", "Build an agent with MCP tool integration"),
            ("10", "24", "Multi-Agent Systems", "Implement supervisor and debate patterns"),
            ("11", "29", "Evaluation and Observability", "Build an LLM evaluation harness"),
            ("12", "31", "Production Engineering and LLMOps", "Deploy with CI/CD, monitoring, and alerting"),
            ("13", "32", "Safety, Ethics, Strategy (Ch 32 through 33)", "Red-team an LLM application; write a risk assessment"),
            ("14", None, "Final project presentations", "Production-grade LLM system (team project)"),
        ],
    },
    {
        "id": "D",
        "slug": "grad-research",
        "short_title": "Graduate Research",
        "full_title": "Course D: Graduate Research",
        "description": "Focus: Training, alignment, scaling, interpretability, and frontier topics. Students leave prepared to conduct original research in LLM science. This pathway is the most technically demanding. It opens with a deep dive into attention and decoding because graduate researchers need to reason about architectural modifications at the level of individual operations.",
        "weeks": [
            ("1", "03", "Attention and Transformer (deep dive, Ch 3 through 4)", "Implement multi-head attention with rotary embeddings"),
            ("2", "05", "Decoding and Search Algorithms", "Implement beam search, MCTS for LLM reasoning"),
            ("3", "06", "Pre-training and Scaling Laws", "Reproduce Chinchilla scaling law predictions"),
            ("4", "07", "Model Architectures (MoE, SSMs)", "Paper reading: compare MoE routing strategies"),
            ("5", "09", "Inference Optimization, Section 9.6: Test-Time Compute", "Implement speculative decoding; analyze reasoning model compute tradeoffs"),
            ("6", "18", "Interpretability", "Run sparse autoencoder probes on a language model"),
            ("7", "13", "Synthetic Data and Curriculum Design", "Design a synthetic data pipeline for a research task"),
            ("8", "14", "Fine-Tuning and PEFT (Ch 14 through 15)", "Ablation study: rank, target modules, learning rate"),
            ("9", "16", "Distillation and Model Merging", "Distill a large model; merge adapters with TIES/DARE"),
            ("10", "17", "Alignment (RLHF, DPO, Constitutional AI)", "Train a reward model and run DPO"),
            ("11", "22", "Agents and Multi-Agent Systems (Ch 22 through 24)", "Build an agent with reflection and self-critique"),
            ("12", "27", "Multimodal Models", "Fine-tune a vision-language model"),
            ("13", None, "Research Frontier sections across all chapters", "Write a research proposal on an open problem"),
            ("14", None, "Final project presentations", "Novel research contribution (individual or pair)"),
        ],
    },
]


# =============================================================================
# READING TRACKS (5 tracks)
# =============================================================================

tracks = [
    {
        "id": 1,
        "slug": "data-engineering",
        "short_title": "Data Engineering Track",
        "full_title": "Data Engineering Track",
        "description": "Building and curating datasets for LLM training, fine-tuning, and evaluation.",
        "steps": [
            (sec_link("Section 6.4", "Section 6.4: Data Curation at Scale"), "how pre-training corpora like FineWeb and Dolma are assembled"),
            (ch_link("13", "Chapter 13: Synthetic Data Generation"), "full chapter on Evol-Instruct, self-play, quality filtering"),
            (sec_link("Section 19.4", "Section 19.4: Document Processing and Chunking"), "turning raw documents into structured inputs"),
            (sec_link("Section 14.6", "Section 14.6: Fine-Tuning for Classification"), "data quality requirements for supervised fine-tuning"),
            (ch_link("29", "Chapter 29: Evaluation, Experiment Design and Observability"), "benchmarking datasets and measuring model performance"),
        ],
    },
    {
        "id": 2,
        "slug": "agent-builder-track",
        "short_title": "Agent Builder Track",
        "full_title": "Agent Builder Track",
        "description": "Building AI agents from API calls through multi-agent orchestration, with production deployment.",
        "steps": [
            (ch_link("10", "Chapter 10: Working with LLM APIs"), "authentication, streaming, structured outputs"),
            (ch_link("11", "Chapter 11: Prompt Engineering and Advanced Techniques"), "chain-of-thought, few-shot, reflection loops"),
            (ch_link("20", "Chapter 20: Retrieval-Augmented Generation"), "grounding agents in external knowledge"),
            (ch_link("22", "Chapter 22: AI Agent Foundations"), "ReAct, tool calling, sandboxed execution"),
            (ch_link("24", "Chapter 24: Multi-Agent Systems"), "supervisor patterns, debate, pipeline orchestration"),
            (ch_link("31", "Chapter 31: Production Engineering and Operations"), "deploying agents reliably at scale"),
        ],
    },
    {
        "id": 3,
        "slug": "researcher-track",
        "short_title": "Researcher Track",
        "full_title": "Researcher Track",
        "description": "Understanding LLM internals, scaling behavior, and frontier research directions.",
        "steps": [
            (ch_link("04", "Chapter 04: The Transformer Architecture"), "self-attention, positional encoding, layer norms"),
            (ch_link("06", "Chapter 06: Pre-training, Scaling Laws and Data Curation"), "Chinchilla, power laws, compute-optimal training"),
            (ch_link("08", "Chapter 08: Reasoning Models and Test-Time Compute"), "chain-of-thought scaling, verification"),
            (ch_link("17", "Chapter 17: Alignment: RLHF, DPO and Preference Tuning"), "reward modeling, constitutional AI"),
            (ch_link("18", "Chapter 18: Interpretability and Mechanistic Understanding"), "probing, logit lens, superposition"),
            (f'<a href="../part-10-frontiers/index.html">Part X: Frontiers: Open Problems and the Road Ahead</a>', "active research questions for 2025 and beyond"),
        ],
    },
    {
        "id": 4,
        "slug": "mlops-production",
        "short_title": "MLOps / Production Track",
        "full_title": "MLOps / Production Track",
        "description": "Deploying, operating, and maintaining LLM systems in production environments.",
        "steps": [
            (ch_link("09", "Chapter 09: Inference Optimization and Efficient Serving"), "quantization, KV-cache, speculative decoding"),
            (f'<a href="../part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html">Sections 14.1 through 14.3: Fine-Tuning Basics</a>', "when and how to fine-tune for your use case"),
            (ch_link("15", "Chapter 15: Parameter-Efficient Fine-Tuning (PEFT)"), "LoRA, QLoRA, adapter merging"),
            (ch_link("29", "Chapter 29: Evaluation, Experiment Design and Observability"), "LLM-as-judge, drift monitoring, A/B testing"),
            (ch_link("31", "Chapter 31: Production Engineering and Operations"), "CI/CD for LLMs, guardrails, cost management"),
            (ch_link("32", "Chapter 32: Safety, Ethics and Regulation"), "red-teaming, compliance, responsible deployment"),
        ],
    },
    {
        "id": 5,
        "slug": "domain-specialist",
        "short_title": "Domain Specialist Track",
        "full_title": "Domain Specialist Track",
        "description": "Applying LLMs to domain problems (medical, legal, business, education) without requiring deep ML expertise.",
        "steps": [
            (ch_link("00", "Chapter 00: ML and PyTorch Foundations"), "skim for vocabulary; skip the code if needed"),
            (ch_link("10", "Chapter 10: Working with LLM APIs"), "the practical starting point for using LLMs"),
            (ch_link("11", "Chapter 11: Prompt Engineering and Advanced Techniques"), "getting high-quality outputs for your domain"),
            (ch_link("20", "Chapter 20: Retrieval-Augmented Generation"), "connecting LLMs to your organization's data"),
            (ch_link("28", "Chapter 28: LLM Applications"), "code generation, summarization, search, recommendations"),
            (ch_link("33", "Chapter 33: LLM Strategy, Product Management and ROI"), "making the business case, vendor selection, cost planning"),
        ],
    },
]


# =============================================================================
# FILE GENERATION
# =============================================================================

ACTION_LABELS = {
    "focus": ("Focus", "action-focus"),
    "skim": ("Skim", "action-skim"),
    "skip": ("Skip", "action-skip"),
    "start": ("Start", "action-start"),
    "supplement": ("Supplement", "action-supplement"),
}

# Build the ordered list of all new files for navigation
all_pages = []
# Pathways 1-15
for p in pathways:
    all_pages.append(("pathway", p))
# Courses A-D
for c in courses:
    all_pages.append(("course", c))
# Tracks 1-5
for t in tracks:
    all_pages.append(("track", t))


def get_filename(page_type, item):
    if page_type == "pathway":
        return f"section-fm.2-pathway-{item['num']:02d}-{item['slug']}.html"
    elif page_type == "course":
        return f"section-fm.3-course-{item['id'].lower()}-{item['slug']}.html"
    elif page_type == "track":
        return f"section-fm.3-track-{item['id']:02d}-{item['slug']}.html"


def get_section_num(page_type, item):
    if page_type == "pathway":
        return f"FM.2.{item['num']}"
    elif page_type == "course":
        return f"FM.3.{item['id']}"
    elif page_type == "track":
        return f"FM.3.T{item['id']}"


def build_pathway_content(p):
    """Build HTML content for a pathway page."""
    lines = []

    # Metadata box
    lines.append('    <div class="callout pathway">')
    lines.append(f'        <div class="callout-title">{html.escape(p["full_title"])}</div>')
    lines.append('    </div>')
    lines.append('')
    lines.append('    <div class="pathway-meta">')
    lines.append(f'        <span><span class="label">Time estimate:</span> {p["time"]}</span>')
    lines.append(f'        <span><span class="label">Difficulty:</span> {p["difficulty"]}</span>')
    lines.append('    </div>')
    lines.append('')
    lines.append(f'    <p><strong>Target audience:</strong> {p["audience"]}</p>')
    lines.append(f'    <p><strong>Goal:</strong> {p["goal"]}</p>')
    lines.append('')

    if "extra_note" in p:
        lines.append('    <div class="callout note">')
        lines.append('        <div class="callout-title">Approach</div>')
        lines.append(f'        <p>{p["extra_note"]}</p>')
        lines.append('    </div>')
        lines.append('')

    # Chapter list
    lines.append('    <h2>Chapter Guide</h2>')
    lines.append('    <ul class="chapter-list">')
    for ch_entry in p["chapters"]:
        action = ch_entry[0]
        ch_num = ch_entry[1]
        ch_desc = ch_entry[2]
        label_text, label_class = ACTION_LABELS[action]

        # Build the chapter link
        if ch_num in CH_LINKS:
            _, href = CH_LINKS[ch_num]
            ch_link_html = f'<a href="{href}">Ch {ch_num}: {ch_desc}</a>'
        else:
            ch_link_html = f'Ch {ch_num}: {ch_desc}'

        lines.append(f'        <li><span class="action {label_class}">{label_text}</span> {ch_link_html}</li>')
    lines.append('    </ul>')

    # Adventures (pathway 15 only)
    if "adventures" in p:
        lines.append('')
        lines.append('    <h2>Pick Your Adventure</h2>')
        lines.append('    <ul class="chapter-list">')
        for adv in p["adventures"]:
            goal = adv[0]
            ch_links_html = []
            i = 1
            while i < len(adv):
                ch_n = adv[i]
                ch_t = adv[i+1]
                if ch_n in CH_LINKS:
                    _, href = CH_LINKS[ch_n]
                    ch_links_html.append(f'<a href="{href}">Ch {ch_n}: {ch_t}</a>')
                else:
                    ch_links_html.append(f'Ch {ch_n}: {ch_t}')
                i += 2
            lines.append(f'        <li><strong>{goal}:</strong> {", ".join(ch_links_html)}</li>')
        lines.append('    </ul>')

    # What's next
    lines.append('')
    lines.append('    <div class="whats-next">')
    lines.append('        <h2>What\'s Next</h2>')
    lines.append('        <p>Return to the <a href="section-fm.2.html">Reading Pathways overview</a> to explore other pathways, or proceed to <a href="section-fm.4.html">FM.4: How to Use This Book</a> for a quick orientation on conventions and callout types, then start reading.</p>')
    lines.append('    </div>')

    return '\n'.join(lines)


def build_course_content(c):
    """Build HTML content for a course page."""
    lines = []

    lines.append('    <div class="callout practical-example">')
    lines.append(f'        <div class="callout-title">{html.escape(c["full_title"])}</div>')
    lines.append(f'        <p>{c["description"]}</p>')
    lines.append('    </div>')
    lines.append('')
    lines.append('    <h2>14-Week Syllabus</h2>')
    lines.append('    <table class="syllabus-table">')
    lines.append('        <thead><tr><th>Week</th><th>Topics</th><th>Lab / Assignment</th></tr></thead>')
    lines.append('        <tbody>')

    for week_num, ch_num, topic, lab in c["weeks"]:
        if ch_num and ch_num in CH_LINKS:
            _, href = CH_LINKS[ch_num]
            topic_html = f'<a href="{href}">{topic}</a>'
        else:
            topic_html = topic
        lines.append(f'            <tr><td>{week_num}</td><td>{topic_html}</td><td>{lab}</td></tr>')

    lines.append('        </tbody>')
    lines.append('    </table>')
    lines.append('')
    lines.append('    <div class="whats-next">')
    lines.append('        <h2>What\'s Next</h2>')
    lines.append('        <p>Return to the <a href="section-fm.3.html">Course Syllabi overview</a> to explore other courses and reading tracks, or proceed to <a href="section-fm.4.html">FM.4: How to Use This Book</a> for a quick orientation on conventions and callout types.</p>')
    lines.append('    </div>')

    return '\n'.join(lines)


def build_track_content(t):
    """Build HTML content for a reading track page."""
    lines = []

    lines.append('    <div class="callout practical-example">')
    lines.append(f'        <div class="callout-title">{t["full_title"]}</div>')
    lines.append(f'        <p>{t["description"]}</p>')
    lines.append('    </div>')
    lines.append('')
    lines.append('    <h2>Learning Sequence</h2>')
    lines.append('    <p>Follow the numbered steps in order. Each step builds on the previous one to give you a coherent understanding of this topic area.</p>')
    lines.append('')
    lines.append('    <ol class="track-steps">')

    for link_html, desc in t["steps"]:
        lines.append(f'        <li>{link_html} ({desc})</li>')

    lines.append('    </ol>')
    lines.append('')
    lines.append('    <div class="whats-next">')
    lines.append('        <h2>What\'s Next</h2>')
    lines.append('        <p>Return to the <a href="section-fm.3.html">Course Syllabi overview</a> to explore other tracks and courses, or proceed to <a href="section-fm.4.html">FM.4: How to Use This Book</a> for a quick orientation on conventions and callout types.</p>')
    lines.append('    </div>')

    return '\n'.join(lines)


# Generate all individual pages
for idx, (ptype, item) in enumerate(all_pages):
    filename = get_filename(ptype, item)
    sec_num = get_section_num(ptype, item)

    # Determine prev/next navigation
    if idx == 0:
        prev_link = ("section-fm.2.html", "FM.2: Reading Pathways")
    else:
        prev_type, prev_item = all_pages[idx - 1]
        prev_file = get_filename(prev_type, prev_item)
        prev_sec = get_section_num(prev_type, prev_item)
        if prev_type == "pathway":
            prev_title = f'{prev_sec}: {prev_item["short_title"]}'
        elif prev_type == "course":
            prev_title = f'{prev_sec}: {prev_item["short_title"]}'
        else:
            prev_title = f'{prev_sec}: {prev_item["short_title"]}'
        prev_link = (prev_file, prev_title)

    if idx == len(all_pages) - 1:
        next_link = ("section-fm.4.html", "FM.4: How to Use This Book")
    else:
        next_type, next_item = all_pages[idx + 1]
        next_file = get_filename(next_type, next_item)
        next_sec = get_section_num(next_type, next_item)
        if next_type == "pathway":
            next_title = f'{next_sec}: {next_item["short_title"]}'
        elif next_type == "course":
            next_title = f'{next_sec}: {next_item["short_title"]}'
        else:
            next_title = f'{next_sec}: {next_item["short_title"]}'
        next_link = (next_file, next_title)

    if ptype == "pathway":
        title = f'{sec_num}: {item["full_title"]}'
        h1 = item["full_title"]
        content = build_pathway_content(item)
    elif ptype == "course":
        title = f'{sec_num}: {item["full_title"]}'
        h1 = item["full_title"]
        content = build_course_content(item)
    else:
        title = f'{sec_num}: {item["full_title"]}'
        h1 = item["full_title"]
        content = build_track_content(item)

    page_html = page_template(title, sec_num, h1, content, prev_link, next_link)

    filepath = os.path.join(FM_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"  Created: {filename}")


# =============================================================================
# UPDATE section-fm.2.html (Pathways overview/index)
# =============================================================================

print("\nUpdating section-fm.2.html (pathways overview)...")

fm2_lines = []
fm2_lines.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FM.2: Reading Pathways: Reader Profiles &amp; Suggested Paths</title>
    <link rel="stylesheet" href="../styles/book.css">
    <style>
        .pathway-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }
        .pathway-link-card {
            display: block;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 1.2rem;
            background: #fafafa;
            text-decoration: none;
            color: inherit;
            transition: box-shadow 0.2s, border-color 0.2s;
        }
        .pathway-link-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-color: var(--accent);
        }
        .pathway-link-card .pw-num {
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--highlight);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .pathway-link-card h4 {
            margin: 0.3rem 0;
            color: var(--accent);
            font-size: 1rem;
        }
        .pathway-link-card .pw-meta {
            font-size: 0.85rem;
            color: #666;
        }
    </style>
</head>
<body>
<header class="chapter-header">
    <nav class="header-nav">
        <a href="../index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="../toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <div class="part-label"><a href="index.html">Front Matter</a></div>
    <h1>Reading Pathways: Reader Profiles &amp; Suggested Paths</h1>
</header>

<main class="content">

    <div class="prerequisites">
        <h3>How to Use This Section</h3>
        <p>Find the pathway that best matches your background and goals. Each pathway tells you which chapters to focus on, which to skip or skim, and how long to expect the journey to take at 8 to 12 hours per week. You can also combine pathways; see the note at the bottom of this page.</p>
    </div>

    <h2 id="self-study">Self-Study Pathways</h2>

    <p>
        Not everyone will read this book cover to cover, and that is by design. The following pathways are tailored to specific goals and backgrounds. Click any card to see the full chapter guide with hyperlinked chapter references.
    </p>

    <div class="pathway-grid">''')

for p in pathways:
    fname = get_filename("pathway", p)
    fm2_lines.append(f'''        <a href="{fname}" class="pathway-link-card">
            <span class="pw-num">Pathway {p["num"]}</span>
            <h4>{html.escape(p["short_title"])}</h4>
            <div class="pw-meta">{p["time"]} &middot; {p["difficulty"]}</div>
        </a>''')

fm2_lines.append('''    </div>

    <div class="callout note">
        <div class="callout-title">Mixing Pathways</div>
        <p>
            These pathways are suggestions, not prescriptions. Many readers will combine elements of multiple pathways. An ML engineer who also wants to build agents might follow Pathway 2 first, then pivot to the agent chapters from Pathway 3. A data scientist exploring safety might pair Pathway 7 with Pathway 12. The cross-references throughout the book make it easy to jump between chapters while maintaining context.
        </p>
    </div>

    <div class="whats-next">
        <h2>What's Next</h2>
        <p>If you are an instructor or want to see complete week-by-week syllabi, proceed to <a href="section-fm.3.html">FM.3: Course Syllabi</a>. If you already know your path, jump to <a href="section-fm.4.html">FM.4: How to Use This Book</a> for a quick orientation on conventions and callout types, then start reading.</p>
    </div>

    <nav class="chapter-nav" style="margin-top: 3rem; padding-top: 1.5rem; border-top: 2px solid #eee; display: flex; justify-content: space-between;">
        <a href="section-fm.1.html">&larr; FM.1: Introduction</a>
        <a href="section-fm.3.html">FM.3: Course Syllabi &rarr;</a>
    </nav>

    <footer>
        <p>&copy; 2025 Building Conversational AI with LLMs and Agents</p>
    </footer>
</main>
</body>
</html>''')

with open(os.path.join(FM_DIR, "section-fm.2.html"), "w", encoding="utf-8") as f:
    f.write('\n'.join(fm2_lines))
print("  Updated: section-fm.2.html")


# =============================================================================
# UPDATE section-fm.3.html (Courses overview/index)
# =============================================================================

print("Updating section-fm.3.html (courses overview)...")

fm3_lines = []
fm3_lines.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FM.3: Course Syllabi: University &amp; Training Programs</title>
    <link rel="stylesheet" href="../styles/book.css">
    <style>
        .course-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }
        .course-link-card {
            display: block;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 1.2rem;
            background: #fafafa;
            text-decoration: none;
            color: inherit;
            transition: box-shadow 0.2s, border-color 0.2s;
        }
        .course-link-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-color: var(--accent);
        }
        .course-link-card .crs-num {
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--highlight);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .course-link-card h4 {
            margin: 0.3rem 0;
            color: var(--accent);
            font-size: 1rem;
        }
        .course-link-card .crs-desc {
            font-size: 0.85rem;
            color: #666;
            margin-top: 0.3rem;
        }
    </style>
</head>
<body>
<header class="chapter-header">
    <nav class="header-nav">
        <a href="../index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="../toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <div class="part-label"><a href="index.html">Front Matter</a></div>
    <h1>Course Syllabi: University &amp; Training Programs</h1>
</header>

<main class="content">

    <div class="prerequisites">
        <h3>How to Use This Section</h3>
        <p>This section provides four complete 14-week university syllabi and five cross-chapter reading tracks. Instructors can adopt a syllabus directly or mix elements from multiple pathways. All pathways assume a 3-hour weekly session (lecture plus lab). Self-directed learners looking for goal-based paths should see <a href="section-fm.2.html">FM.2: Reading Pathways</a> instead.</p>
    </div>

    <h2>University Course Syllabi</h2>

    <p>
        With 36 chapters, no single semester can cover everything. The following four syllabi are designed for instructors adopting this book for a single-semester (14-week) university course. Click any card for the complete week-by-week syllabus with hyperlinked chapter references.
    </p>

    <div class="course-grid">''')

course_short_descs = {
    "A": "Foundations, LLM APIs, building and deploying basic agents",
    "B": "Architecture internals, training methods, interpretability",
    "C": "Full stack from APIs through production deployment at scale",
    "D": "Training, alignment, scaling, interpretability, frontier topics",
}

for c in courses:
    fname = get_filename("course", c)
    fm3_lines.append(f'''        <a href="{fname}" class="course-link-card">
            <span class="crs-num">Course {c["id"]}</span>
            <h4>{html.escape(c["short_title"])}</h4>
            <div class="crs-desc">{course_short_descs[c["id"]]}</div>
        </a>''')

fm3_lines.append('''    </div>

    <h2>Cross-Chapter Reading Tracks</h2>

    <p>
        If you are reading this book with a specific goal rather than cover to cover, these curated tracks group chapters and sections from across the book into focused learning sequences. Click any card for the full learning sequence with hyperlinked references.
    </p>

    <div class="course-grid">''')

for t in tracks:
    fname = get_filename("track", t)
    fm3_lines.append(f'''        <a href="{fname}" class="course-link-card">
            <span class="crs-num">Track {t["id"]}</span>
            <h4>{html.escape(t["short_title"])}</h4>
            <div class="crs-desc">{html.escape(t["description"])}</div>
        </a>''')

fm3_lines.append('''    </div>

    <div class="whats-next">
        <h2>What's Next</h2>
        <p>Now that you have a syllabus or reading track in mind, proceed to <a href="section-fm.4.html">FM.4: How to Use This Book</a> to learn about the conventions, callout types, and pedagogical patterns you will encounter in every chapter.</p>
    </div>

    <nav class="chapter-nav" style="margin-top: 3rem; padding-top: 1.5rem; border-top: 2px solid #eee; display: flex; justify-content: space-between;">
        <a href="section-fm.2.html">&larr; FM.2: Reading Pathways</a>
        <a href="section-fm.4.html">FM.4: How to Use This Book &rarr;</a>
    </nav>

    <footer>
        <p>&copy; 2025 Building Conversational AI with LLMs and Agents</p>
    </footer>
</main>
</body>
</html>''')

with open(os.path.join(FM_DIR, "section-fm.3.html"), "w", encoding="utf-8") as f:
    f.write('\n'.join(fm3_lines))
print("  Updated: section-fm.3.html")


# =============================================================================
# UPDATE front-matter/index.html
# =============================================================================

print("Updating front-matter/index.html...")

index_path = os.path.join(FM_DIR, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

# Build the new sections list
new_sections = []
new_sections.append('''    <ul class="sections-list">
        <li>
            <a href="section-fm.1.html" class="section-card">
                <span class="section-num">FM.1</span>
                <span class="section-title">Introduction: What This Book Is About &amp; Who It's For</span>
                <span class="section-desc">
                    What the book covers (and what it does not), the seven parts and their dependencies,
                    primary and secondary audiences, assumed background, and what makes this book different from other LLM resources.
                </span>
            </a>
        </li>
        <li>
            <a href="section-fm.2.html" class="section-card">
                <span class="section-num">FM.2</span>
                <span class="section-title">Reading Pathways: Reader Profiles &amp; Suggested Paths</span>
                <span class="section-desc">
                    Fifteen self-study pathways tailored to different backgrounds, each on its own page
                    with hyperlinked chapter references, time estimates, and chapter-by-chapter guidance.
                </span>
            </a>
        </li>''')

# Add individual pathway entries
for p in pathways:
    fname = get_filename("pathway", p)
    sec_num = get_section_num("pathway", p)
    new_sections.append(f'''        <li>
            <a href="{fname}" class="section-card" style="padding-left: 2rem;">
                <span class="section-num">{sec_num}</span>
                <span class="section-title">{html.escape(p["short_title"])}</span>
                <span class="section-desc">{p["time"]} &middot; {p["difficulty"]} &middot; {p["audience"][:80]}...</span>
            </a>
        </li>''')

new_sections.append('''        <li>
            <a href="section-fm.3.html" class="section-card">
                <span class="section-num">FM.3</span>
                <span class="section-title">Course Syllabi: University &amp; Training Programs</span>
                <span class="section-desc">
                    Four complete 14-week university syllabi and five cross-chapter reading tracks,
                    each on its own page with hyperlinked chapter references and week-by-week schedules.
                </span>
            </a>
        </li>''')

# Add individual course entries
for c in courses:
    fname = get_filename("course", c)
    sec_num = get_section_num("course", c)
    new_sections.append(f'''        <li>
            <a href="{fname}" class="section-card" style="padding-left: 2rem;">
                <span class="section-num">{sec_num}</span>
                <span class="section-title">{html.escape(c["short_title"])}</span>
                <span class="section-desc">{course_short_descs[c["id"]]}</span>
            </a>
        </li>''')

# Add individual track entries
for t in tracks:
    fname = get_filename("track", t)
    sec_num = get_section_num("track", t)
    new_sections.append(f'''        <li>
            <a href="{fname}" class="section-card" style="padding-left: 2rem;">
                <span class="section-num">{sec_num}</span>
                <span class="section-title">{html.escape(t["short_title"])}</span>
                <span class="section-desc">{html.escape(t["description"])}</span>
            </a>
        </li>''')

new_sections.append('''        <li>
            <a href="section-fm.4.html" class="section-card">
                <span class="section-num">FM.4</span>
                <span class="section-title">How to Use This Book: Conventions, Callouts &amp; Labs</span>
                <span class="section-desc">
                    The four-phase pedagogical approach (concept, intuition, code, production), callout types
                    (Big Picture, Key Insight, Warning, Fun Note, Research Frontier), code conventions,
                    lab exercises, and how to get started based on your background.
                </span>
            </a>
        </li>
    </ul>''')

# Replace the old sections-list
old_start = index_html.index('    <ul class="sections-list">')
old_end = index_html.index('    </ul>', old_start) + len('    </ul>')
index_html = index_html[:old_start] + '\n'.join(new_sections) + index_html[old_end:]

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_html)
print("  Updated: front-matter/index.html")


# =============================================================================
# UPDATE toc.html (detailed view only, within the FM section)
# =============================================================================

print("Updating toc.html...")

toc_path = TOC_PATH
with open(toc_path, "r", encoding="utf-8") as f:
    toc_html = f.read()

# Build new FM.2 lesson block with sub-items
fm2_lesson = '''            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">FM.2</span> <a href="front-matter/section-fm.2.html">Reading Pathways: Reader Profiles &amp; Suggested Paths</a></div>
                <div class="lesson-topics"><ul>
                    <li>15 self-study pathways, each on a dedicated page:</li>'''

for p in pathways:
    fname = get_filename("pathway", p)
    fm2_lesson += f'\n                    <li><a href="front-matter/{fname}">{get_section_num("pathway", p)}: {html.escape(p["short_title"])}</a> ({p["time"]})</li>'

fm2_lesson += '''
                </ul></div>
            </div>'''

# Build new FM.3 lesson block with sub-items
fm3_lesson = '''            <div class="lesson">
                <div class="lesson-title"><span class="lesson-num">FM.3</span> <a href="front-matter/section-fm.3.html">Course Syllabi: University &amp; Training Programs</a></div>
                <div class="lesson-topics"><ul>
                    <li>4 university course syllabi (14-week), each on a dedicated page:</li>'''

for c in courses:
    fname = get_filename("course", c)
    fm3_lesson += f'\n                    <li><a href="front-matter/{fname}">{get_section_num("course", c)}: {html.escape(c["short_title"])}</a></li>'

fm3_lesson += '''
                    <li>5 cross-chapter reading tracks, each on a dedicated page:</li>'''

for t in tracks:
    fname = get_filename("track", t)
    fm3_lesson += f'\n                    <li><a href="front-matter/{fname}">{get_section_num("track", t)}: {html.escape(t["short_title"])}</a></li>'

fm3_lesson += '''
                </ul></div>
            </div>'''

# Replace the old FM.2 lesson block
old_fm2_start = toc_html.index('            <div class="lesson">\n                <div class="lesson-title"><span class="lesson-num">FM.2</span>')
old_fm2_end = toc_html.index('            <div class="lesson">\n                <div class="lesson-title"><span class="lesson-num">FM.3</span>')
toc_html = toc_html[:old_fm2_start] + fm2_lesson + '\n\n' + toc_html[old_fm2_end:]

# Now replace the old FM.3 lesson block (find it again since offsets changed)
old_fm3_start = toc_html.index('            <div class="lesson">\n                <div class="lesson-title"><span class="lesson-num">FM.3</span>')
old_fm3_end = toc_html.index('            <div class="lesson">\n                <div class="lesson-title"><span class="lesson-num">FM.4</span>')
toc_html = toc_html[:old_fm3_start] + fm3_lesson + '\n\n' + toc_html[old_fm3_end:]

with open(toc_path, "w", encoding="utf-8") as f:
    f.write(toc_html)
print("  Updated: toc.html")


# Also update the SHORT toc to add pathway/course sub-items
with open(toc_path, "r", encoding="utf-8") as f:
    toc_html = f.read()

# Find the FM.2 short-toc entry and add sub-items after it
old_fm2_short = '<a class="toc-item" href="front-matter/section-fm.2.html"><span class="toc-num">FM.2</span> Reading Pathways: Reader Profiles &amp; Suggested Paths</a>'
old_fm3_short = '<a class="toc-item" href="front-matter/section-fm.3.html"><span class="toc-num">FM.3</span> Course Syllabi: University &amp; Training Programs</a>'

# We keep the short TOC as-is (just the 4 main FM entries) since it's meant to be compact.
# The detailed TOC already has the expanded entries.

print("\nDone! Created 24 individual section files and updated 4 existing files.")
print(f"Files in {FM_DIR}:")
for f in sorted(os.listdir(FM_DIR)):
    if f.endswith('.html'):
        print(f"  {f}")
