"""
Create new appendix directories (K through T) with index pages
for framework tutorials.
"""

from pathlib import Path

ROOT = Path(r"E:\Projects\LLMCourse\appendices")

# Each appendix: (letter, slug, title, description, sections)
APPENDICES = [
    ("k", "huggingface-ecosystem", "HuggingFace Ecosystem",
     "A hands-on tutorial covering the HuggingFace ecosystem: Transformers, Datasets, Tokenizers, PEFT, TRL, Accelerate, and the Hub. Covers model loading, fine-tuning workflows, dataset preparation, and model sharing.",
     [
         ("k.1", "Transformers Library: Models, Pipelines, and AutoClasses"),
         ("k.2", "Datasets and Tokenizers: Loading, Preprocessing, and Streaming"),
         ("k.3", "Training with Trainer and Accelerate"),
         ("k.4", "PEFT and TRL: Parameter-Efficient Fine-Tuning and RLHF"),
         ("k.5", "The HuggingFace Hub: Sharing, Versioning, and Spaces"),
     ]),
    ("l", "langchain", "LangChain",
     "A practical guide to LangChain: building chains, managing memory, connecting to data sources, parsing structured outputs, and orchestrating LLM-powered applications.",
     [
         ("l.1", "Core Abstractions: Models, Prompts, and Chains"),
         ("l.2", "Memory and Conversation Management"),
         ("l.3", "Document Loaders, Splitters, and Retrievers"),
         ("l.4", "Output Parsers and Structured Output"),
         ("l.5", "Agents, Tools, and Callbacks"),
     ]),
    ("m", "langgraph", "LangGraph",
     "Building stateful, multi-step agent workflows with LangGraph: graph construction, state management, cycles, human-in-the-loop patterns, and persistence.",
     [
         ("m.1", "Graph Fundamentals: Nodes, Edges, and State"),
         ("m.2", "Conditional Routing and Cycles"),
         ("m.3", "Human-in-the-Loop and Interrupts"),
         ("m.4", "Persistence, Checkpointing, and Recovery"),
         ("m.5", "Multi-Agent Graphs and Subgraphs"),
     ]),
    ("n", "crewai", "CrewAI",
     "Multi-agent orchestration with CrewAI: defining agents with roles and goals, creating tasks, configuring tools, and building collaborative agent crews.",
     [
         ("n.1", "Agents: Roles, Goals, and Backstories"),
         ("n.2", "Tasks: Descriptions, Expected Outputs, and Dependencies"),
         ("n.3", "Tools: Built-in and Custom Tool Integration"),
         ("n.4", "Crews: Sequential and Hierarchical Processes"),
         ("n.5", "Advanced Patterns: Delegation, Memory, and Callbacks"),
     ]),
    ("o", "llamaindex", "LlamaIndex",
     "Building RAG applications with LlamaIndex: data connectors, indexing strategies, query engines, response synthesis, and advanced retrieval patterns.",
     [
         ("o.1", "Data Connectors and Document Loading"),
         ("o.2", "Indexes: Vector, List, Tree, and Keyword"),
         ("o.3", "Query Engines and Response Synthesis"),
         ("o.4", "Advanced Retrieval: Routing, Sub-Questions, and Fusion"),
         ("o.5", "Agents, Tools, and Workflows in LlamaIndex"),
     ]),
    ("p", "semantic-kernel", "Semantic Kernel",
     "Microsoft's AI orchestration SDK: plugins, planners, memory connectors, and enterprise integration patterns for building AI applications.",
     [
         ("p.1", "Kernel Setup, Plugins, and Functions"),
         ("p.2", "Prompt Templates and Semantic Functions"),
         ("p.3", "Planners: Sequential, Stepwise, and Handlebars"),
         ("p.4", "Memory: Embeddings, Vector Stores, and Recall"),
         ("p.5", "Enterprise Patterns: Azure OpenAI, Authentication, and Logging"),
     ]),
    ("q", "dspy", "DSPy",
     "Programmatic prompt optimization with DSPy: signatures, modules, optimizers (compilers), and systematic evaluation for building reliable LLM pipelines.",
     [
         ("q.1", "Signatures and Modules: Declarative LLM Programming"),
         ("q.2", "Built-in Modules: ChainOfThought, ReAct, and Retrieval"),
         ("q.3", "Optimizers: BootstrapFewShot, MIPRO, and BayesianSignatureOptimizer"),
         ("q.4", "Evaluation and Metrics"),
         ("q.5", "Advanced Patterns: Assertions, Typed Predictors, and Multi-Hop"),
     ]),
    ("r", "experiment-tracking", "Experiment Tracking: W&B and MLflow",
     "Tracking experiments, managing model registries, and building evaluation dashboards with Weights and Biases and MLflow.",
     [
         ("r.1", "Weights and Biases: Runs, Logging, and Sweeps"),
         ("r.2", "MLflow: Tracking, Projects, and Model Registry"),
         ("r.3", "Experiment Comparison and Hyperparameter Optimization"),
         ("r.4", "Model Registry and Deployment Workflows"),
         ("r.5", "LLM Evaluation Dashboards and Observability"),
     ]),
    ("s", "inference-serving", "Inference Serving: vLLM, TGI, and SGLang",
     "Deploying LLMs for production inference: vLLM continuous batching, HuggingFace Text Generation Inference, SGLang structured generation, quantization, and scaling strategies.",
     [
         ("s.1", "vLLM: PagedAttention, Continuous Batching, and OpenAI-Compatible API"),
         ("s.2", "Text Generation Inference (TGI): Deployment and Configuration"),
         ("s.3", "SGLang: Structured Generation and RadixAttention"),
         ("s.4", "Quantization for Serving: GPTQ, AWQ, and GGUF"),
         ("s.5", "Scaling and Load Balancing for Production"),
     ]),
    ("t", "distributed-ml", "Distributed ML: Databricks, Ray, and Data Infrastructure",
     "Large-scale ML infrastructure: Databricks for data engineering and model training, Ray for distributed compute, data lakes, feature stores, and production data pipelines.",
     [
         ("t.1", "Databricks: Workspace, Notebooks, and Unity Catalog"),
         ("t.2", "Delta Lake and Lakehouse Architecture"),
         ("t.3", "Ray Train, Ray Serve, and Ray Data"),
         ("t.4", "Feature Stores: Feast, Tecton, and Databricks Feature Engineering"),
         ("t.5", "Production Data Pipelines and Model Serving at Scale"),
     ]),
]


HEADER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Appendix {letter_upper}: {title} | Building Conversational AI with LLMs and Agents</title>
    <link rel="stylesheet" href="../../styles/book.css">
    <link rel="stylesheet" href="../../vendor/katex/katex.min.css">
    <script defer src="../../vendor/katex/katex.min.js"></script>
    <script defer src="../../vendor/katex/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}}
            ],
            throwOnError: false
        }});"></script>
    <link rel="stylesheet" href="../../vendor/prism/prism-theme.css">
    <script defer src="../../vendor/prism/prism-bundle.min.js"></script>
</head>
<body>
<header class="chapter-header">
    <nav class="header-nav">
        <a href="../../index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="../../toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <div class="part-label"><a href="../../toc.html">Appendices</a></div>
    <div class="chapter-label"><a href="index.html">Appendix {letter_upper}</a></div>
    <h1>{title}</h1>
</header>

<main class="content">

    <div class="callout big-picture">
        <div class="callout-title">Big Picture</div>
        <p>{description}</p>
    </div>

    <h2>Sections</h2>
    <div class="section-cards">
{section_links}
    </div>

    <nav class="chapter-nav">
        <a class="prev" href="{prev_link}">{prev_title}</a>
        <a class="up" href="../../toc.html">Appendices</a>
        <a class="next" href="{next_link}">{next_title}</a>
    </nav>

    <footer>
        <p class="footer-title">Building Conversational AI with LLMs and Agents, Fifth Edition</p>
        <p>&copy; 2026 Alexander Apartsin &amp; Yehudit Aperstein &middot; <a href="../../toc.html">Contents</a></p>
        <p class="footer-updated">Last updated: <script>document.write(new Date(document.lastModified).toLocaleDateString('en-US', {{year:'numeric', month:'long', day:'numeric'}}))</script></p>
    </footer>
</main>
</body>
</html>"""

SECTION_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Section {sec_id}: {sec_title} | Building Conversational AI with LLMs and Agents</title>
    <link rel="stylesheet" href="../../styles/book.css">
    <link rel="stylesheet" href="../../vendor/katex/katex.min.css">
    <script defer src="../../vendor/katex/katex.min.js"></script>
    <script defer src="../../vendor/katex/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}}
            ],
            throwOnError: false
        }});"></script>
    <link rel="stylesheet" href="../../vendor/prism/prism-theme.css">
    <script defer src="../../vendor/prism/prism-bundle.min.js"></script>
</head>
<body>
<header class="chapter-header">
    <nav class="header-nav">
        <a href="../../index.html" class="book-title-link">Building Conversational AI with LLMs and Agents</a>
        <a href="../../toc.html" class="toc-link" title="Table of Contents"><span class="toc-icon">&#9776;</span> Contents</a>
    </nav>
    <div class="part-label"><a href="../../toc.html">Appendices</a></div>
    <div class="chapter-label"><a href="index.html">Appendix {letter_upper}: {appendix_title}</a></div>
    <h1>{sec_title}</h1>
</header>

<main class="content">

    <div class="callout big-picture">
        <div class="callout-title">Big Picture</div>
        <p>This section covers {sec_title_lower}. Content will be generated using the book production pipeline.</p>
    </div>

    <p><em>Content pending: this section will be produced by the book-writers agent pipeline.</em></p>

    <nav class="chapter-nav">
        <a class="prev" href="{sec_prev_link}">{sec_prev_title}</a>
        <a class="up" href="index.html">Appendix {letter_upper}: {appendix_title}</a>
        <a class="next" href="{sec_next_link}">{sec_next_title}</a>
    </nav>

    <footer>
        <p class="footer-title">Building Conversational AI with LLMs and Agents, Fifth Edition</p>
        <p>&copy; 2026 Alexander Apartsin &amp; Yehudit Aperstein &middot; <a href="../../toc.html">Contents</a></p>
        <p class="footer-updated">Last updated: <script>document.write(new Date(document.lastModified).toLocaleDateString('en-US', {{year:'numeric', month:'long', day:'numeric'}}))</script></p>
    </footer>
</main>
</body>
</html>"""


def make_section_filename(sec_id):
    return f"section-{sec_id}.html"


def main():
    created_dirs = 0
    created_files = 0

    for i, (letter, slug, title, description, sections) in enumerate(APPENDICES):
        letter_upper = letter.upper()
        dir_path = ROOT / f"appendix-{letter}-{slug}"
        dir_path.mkdir(exist_ok=True)
        created_dirs += 1

        # Compute prev/next for index
        if i == 0:
            prev_link = "../appendix-j-datasets-benchmarks/index.html"
            prev_title = "Appendix J: Datasets &amp; Benchmarks"
        else:
            prev_letter, prev_slug, prev_title_raw = APPENDICES[i-1][0], APPENDICES[i-1][1], APPENDICES[i-1][2]
            prev_link = f"../appendix-{prev_letter}-{prev_slug}/index.html"
            prev_title = f"Appendix {prev_letter.upper()}: {prev_title_raw}"

        if i < len(APPENDICES) - 1:
            next_letter, next_slug, next_title_raw = APPENDICES[i+1][0], APPENDICES[i+1][1], APPENDICES[i+1][2]
            next_link = f"../appendix-{next_letter}-{next_slug}/index.html"
            next_title = f"Appendix {next_letter.upper()}: {next_title_raw}"
        else:
            next_link = "../../toc.html"
            next_title = "Table of Contents"

        # Build section links for index
        section_links = ""
        for sec_id, sec_title in sections:
            sec_file = make_section_filename(sec_id)
            section_links += f'        <a href="{sec_file}" class="section-card">\n'
            section_links += f'            <span class="section-number">{sec_id.upper()}</span>\n'
            section_links += f'            <span class="section-title">{sec_title}</span>\n'
            section_links += f'        </a>\n'

        # Write index.html
        index_html = HEADER_TEMPLATE.format(
            letter_upper=letter_upper,
            title=title,
            description=description,
            section_links=section_links.rstrip(),
            prev_link=prev_link,
            prev_title=prev_title,
            next_link=next_link,
            next_title=next_title,
        )
        (dir_path / "index.html").write_text(index_html, encoding="utf-8")
        created_files += 1

        # Write section files
        for j, (sec_id, sec_title) in enumerate(sections):
            sec_file = make_section_filename(sec_id)

            # prev/next within sections
            if j == 0:
                sec_prev_link = "index.html"
                sec_prev_title = f"Appendix {letter_upper}: {title}"
            else:
                sec_prev_link = make_section_filename(sections[j-1][0])
                sec_prev_title = f"{sections[j-1][0].upper()}: {sections[j-1][1]}"

            if j < len(sections) - 1:
                sec_next_link = make_section_filename(sections[j+1][0])
                sec_next_title = f"{sections[j+1][0].upper()}: {sections[j+1][1]}"
            else:
                # Next appendix index or TOC
                sec_next_link = next_link
                sec_next_title = next_title

            sec_html = SECTION_TEMPLATE.format(
                sec_id=sec_id.upper(),
                sec_title=sec_title,
                sec_title_lower=sec_title[0].lower() + sec_title[1:],
                letter_upper=letter_upper,
                appendix_title=title,
                sec_prev_link=sec_prev_link,
                sec_prev_title=sec_prev_title,
                sec_next_link=sec_next_link,
                sec_next_title=sec_next_title,
            )
            (dir_path / sec_file).write_text(sec_html, encoding="utf-8")
            created_files += 1

    print(f"Created {created_dirs} appendix directories and {created_files} HTML files.")
    for letter, slug, title, _, sections in APPENDICES:
        print(f"  Appendix {letter.upper()}: {title} ({len(sections)} sections)")


if __name__ == "__main__":
    main()
