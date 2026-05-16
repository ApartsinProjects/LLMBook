"""Polish book_structure.yaml metadata for the TOC:
  1. Replace generic Tools-of-the-Trade subtitle with Part-specific one.
  2. Fill appendix subtitles where missing.
  3. Reorder front-matter for natural reader UX flow.

Idempotent. Run once after structural changes.
"""
from __future__ import annotations
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


# Per-Part Tools-of-Trade subtitle
TOOLS_SUBTITLES = {
    1: "PyTorch, NumPy, and the math-and-tokenizer stack every Foundations chapter rests on.",
    2: "The 2026 model zoo: GPT, Claude, Gemini, Llama-4, Qwen3, DeepSeek-V4, plus tokenizers and interp tools.",
    3: "Provider SDKs (OpenAI, Anthropic, Google, litellm), prompt platforms (LangSmith, PromptLayer), and local-inference toolchains.",
    4: "transformers, trl, peft, axolotl, lit-gpt, WandB / MLflow: the SFT + PEFT + alignment stack.",
    5: "Vector DBs (FAISS, Chroma, Pinecone, pgvector), embeddings (sentence-transformers, OpenAI Ada), LangChain, LlamaIndex.",
    6: "LangGraph, CrewAI, AutoGen, smolagents, PydanticAI, plus the MCP / A2A / AG-UI agent protocols.",
    7: "Imagen 4, FLUX.1, Veo, Sora, Suno, Udio, ElevenLabs, Whisper: the multimodal generation + understanding stack.",
    8: "Eval (HELM, lm-evaluation-harness, Inspect AI), observability (Arize, LangSmith, Helicone, Phoenix), inference (vLLM, TGI, SGLang).",
    9: "Llama Guard, NVIDIA NeMo Guardrails, Guardrails AI, Garak, PyRIT, plus the privacy-tech stack.",
    10: "Vibe-coding (Cursor, Claude Code, Cline, Copilot), PM tools (Linear, Notion, Figma+AI), analytics (PostHog, Mixpanel, Amplitude).",
    11: "Per-industry vendors: Harvey, BloombergGPT, Med-PaLM, Khanmigo, Security Copilot, plus regulator and benchmark catalogs.",
    12: "arXiv, Papers with Code, Anthropic Alignment, OpenAI papers, EleutherAI, Nous Research, frontier benchmark portals.",
}

# Appendix subtitles (curated; map by slug)
APPENDIX_SUBTITLES = {
    "mathematical-foundations":
        "The essential linear algebra, probability, calculus, and information theory that power every transformer.",
    "ml-essentials":
        "Learning paradigms, loss functions, optimization, regularization, and evaluation metrics in one place.",
    "python-for-llm":
        "Essential libraries, virtual environments, Jupyter / Colab setup, and the day-to-day Python patterns.",
    "environment-setup":
        "Step-by-step guides for configuring your local development environment and cloud workspaces.",
    "git-collaboration":
        "Version control for code, data, and experiments with Git, DVC, and reproducibility best practices.",
    "huggingface-ecosystem":
        "Practical guide to the HuggingFace ecosystem: loading models, training with Trainer, sharing on the Hub.",
    "langchain":
        "Building LLM applications with LangChain's chain composition, agent framework, and retrieval integration.",
    "tooling-ecosystem":
        "A survey of the broader LLM tooling landscape: evaluation platforms, guardrail libraries, observability tools, emerging frameworks.",
    "hardware-compute":
        "GPU selection, cloud provider comparison, and cost optimization strategies for training and inference.",
    "experiment-tracking":
        "Logging experiments, comparing runs, and managing model artifacts with Weights & Biases and MLflow.",
    "inference-serving":
        "High-throughput LLM serving with continuous batching, PagedAttention, and production deployment patterns.",
    "distributed-ml":
        "Scaling data pipelines and training across clusters with PySpark, Databricks, and Ray.",
    "docker-containers":
        "Containerizing LLM applications with Docker, GPU passthrough, and orchestration with Docker Compose.",
    "master-reference-tables":
        "Fifteen scannable comparison tables for the recurring decisions practitioners make.",
    "production-patterns":
        "Twenty-two engineering patterns for shipping LLM systems at scale, organized by operational problem.",
    "pedagogy-kit":
        "Capstone rubric, three intermediate projects, named production war stories, and per-section reading-pathway upgrades.",
    "problem-solution-key":
        "A lookup table mapping common NLP / ML / AI engineering tasks to the chapters and sections that solve them.",
    "freshness-2026":
        "The 2024-2026 papers, models, protocols, and benchmarks that define the field at publication date.",
}

# Front-matter natural reading order (welcome → orient → who/why → how → instructor/back)
FRONT_MATTER_ORDER = [
    "foreword",
    "fm-what-this-book-covers",
    "fm-who-should-read",
    "look-inside-preview",
    "fm-how-to-use",
    "fm-reading-pathways",
    "fm-course-syllabi",
    "about-authors",
    "copyright",
]


def main() -> int:
    p = ROOT / "book_structure.yaml"
    struct = yaml.safe_load(p.read_text(encoding="utf-8"))

    # 1. Per-Part Tools-of-Trade subtitles
    n_tools = 0
    for part in struct.get("parts", []):
        pnum = part["num"]
        for c in part.get("chapters", []):
            if c.get("slug") == "tools-of-the-trade" and pnum in TOOLS_SUBTITLES:
                if c.get("subtitle") != TOOLS_SUBTITLES[pnum]:
                    c["subtitle"] = TOOLS_SUBTITLES[pnum]
                    n_tools += 1

    # 2. Appendix subtitles + group assignment (5-group structure post
    #    GPU Hardware drop, May 2026; appendices A-Q):
    #
    #    Foundations            (A=Math, B=ML)
    #    Development Setup      (C=Python, D=Env, E=Git/DVC)
    #    Framework Guides       (F=HF, G=LangChain, H=Tooling Ecosystem)
    #    Production Infrastructure  (I=Experiments, J=Inference, K=Distributed,
    #                                L=Docker)
    #    Reference & Pedagogy   (M=Tables, N=Patterns, O=Pedagogy,
    #                                P=Prob-Solution, Q=Freshness)
    APPENDIX_GROUPS = {
        "A": "Foundations", "B": "Foundations",
        "C": "Development Setup", "D": "Development Setup",
        "E": "Development Setup",
        "F": "Framework Guides", "G": "Framework Guides",
        "H": "Framework Guides",
        "I": "Production Infrastructure", "J": "Production Infrastructure",
        "K": "Production Infrastructure", "L": "Production Infrastructure",
        "M": "Reference & Pedagogy", "N": "Reference & Pedagogy",
        "O": "Reference & Pedagogy", "P": "Reference & Pedagogy",
        "Q": "Reference & Pedagogy",
    }
    n_app = 0
    for app in struct.get("appendices", []):
        slug = app.get("slug", "")
        letter = app.get("letter", "")
        if slug in APPENDIX_SUBTITLES:
            new_sub = APPENDIX_SUBTITLES[slug]
            if app.get("subtitle") != new_sub:
                app["subtitle"] = new_sub
                n_app += 1
        if letter in APPENDIX_GROUPS:
            app["group"] = APPENDIX_GROUPS[letter]

    # 3. Reorder front-matter
    fm = struct.get("front_matter", [])
    fm_by_slug = {x["slug"]: x for x in fm}
    new_fm = [fm_by_slug[s] for s in FRONT_MATTER_ORDER if s in fm_by_slug]
    # Append any items not in the canonical order at the end
    for x in fm:
        if x["slug"] not in FRONT_MATTER_ORDER:
            new_fm.append(x)
    struct["front_matter"] = new_fm

    p.write_text(
        yaml.dump(struct, default_flow_style=False, sort_keys=False,
                   allow_unicode=True, width=200),
        encoding="utf-8",
    )
    print(f"Tools subtitles updated: {n_tools}")
    print(f"Appendix subtitles filled: {n_app}")
    print(f"Front-matter reordered: {len(new_fm)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
