"""Detect chapter pages that don't connect to LLM / Agent context.

Per user request: chapters not directly about LLMs/Agents (multimodal vision,
3D, audio, document understanding, etc.) should explicitly tell the reader
why they live in an LLM+Agent book. The Big Picture callout is the natural
place: it should mention "LLM", "agent", "multimodal", "vision-language", or
similar bridge terminology.

This check flags any section whose Big Picture callout contains zero
LLM-context words. Authoring task: add a "Why this lives in an LLM book"
paragraph.
"""
import re
from collections import namedtuple

PRIORITY = "P2"
CHECK_ID = "OFFTOPIC_NO_LLM_CONTEXT"
DESCRIPTION = "Big Picture in non-LLM-named section has no bridge to LLM/Agent narrative"

Issue = namedtuple("Issue", ["priority", "check_id", "filepath", "line", "message"])

# LLM-bridge terminology -- any of these in the Big Picture means "ok, the bridge is there"
BRIDGE_TERMS = re.compile(
    r'\b('
    r'LLM|LLMs|language model|chatbot|conversational AI|agent|agents|agentic|'
    r'multimodal|vision-language|VLM|VLA|vision language|cross-modal|'
    r'prompt|RAG|retrieval-augmented|tool use|tool-use|MCP|'
    r'embodied|world model|world-model|policy|reasoning|'
    r'transformer|attention|tokenization|fine-tun|inference|'
    r'chain-of-thought|CoT|in-context|'
    # Bridge terms for retrieval / IE / embeddings chapters
    r'embedding|embeddings|vector|vector index|vector indexes|vector database|'
    r'semantic search|hybrid search|reranker|reranking|knowledge graph|'
    # Bridge terms for evaluation chapters
    r'evaluat|benchmark|hallucinat|judge|grading|grader|'
    # Bridge terms for safety / ethics chapters
    r'safety|guardrail|alignment|jailbreak|red[\s-]team|'
    # Bridge terms for production chapters
    r'production|deployment|observab|monitoring|telemetry|'
    # Bridge terms for training chapters
    r'training|pretraining|alignment|RLHF|DPO|reward'
    r')\b',
    re.IGNORECASE,
)

# Sections that are pure foundation / pre-LLM machinery don't need the bridge
SKIP_SECTIONS = re.compile(
    r'(module-00-ml-pytorch-foundations|module-01-foundations-nlp|appendices)',
    re.IGNORECASE,
)

BIG_PICTURE_RE = re.compile(
    r'<div\s+class="callout\s+big-picture"[^>]*>([\s\S]*?)</div>\s*(?=<div|<h[1-6]|<nav|<details|<section)',
    re.IGNORECASE,
)
TAG_RE = re.compile(r'<[^>]+>')


def _line(html, pos):
    return html.count("\n", 0, pos) + 1


def run(filepath, html, context):
    issues = []
    if filepath.suffix != ".html":
        return issues
    if not filepath.name.startswith("section-"):
        return issues
    # Only flag potentially off-topic parts: multimodal (5), interpretability,
    # 3D, audio. Skip core LLM parts.
    path_str = str(filepath).replace("\\", "/")
    if SKIP_SECTIONS.search(path_str):
        return issues

    bp = BIG_PICTURE_RE.search(html)
    if not bp:
        return issues  # no Big Picture is a different issue, handled by SECTION_STRUCTURE
    text = TAG_RE.sub(' ', bp.group(1))
    if not BRIDGE_TERMS.search(text):
        issues.append(Issue(
            PRIORITY, CHECK_ID, filepath, _line(html, bp.start()),
            'Big Picture has no LLM/Agent bridge term; add a "Why this lives in an LLM and Agents book" paragraph',
        ))
    return issues
