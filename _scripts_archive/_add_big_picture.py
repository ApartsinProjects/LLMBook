#!/usr/bin/env python3
"""Add big-picture callouts to all chapter/part/appendix index pages that lack them."""

import re
import os

BASE = r"E:\Projects\LLMCourse"

# Map of relative path -> big-picture blurb text
# Each blurb: 2-3 sentences, no em dashes or double dashes
BLURBS = {
    # ============ PART INDEX PAGES ============
    "part-1-foundations/index.html": (
        "Every advanced topic in this book, from fine-tuning to agentic systems, "
        "rests on the ideas introduced here. Part I gives you the mathematical intuition, "
        "NLP vocabulary, and architectural understanding that make the rest of the book accessible. "
        "If you invest time here, every subsequent chapter will reward you with deeper comprehension."
    ),
    "part-2-understanding-llms/index.html": (
        "Part I taught you how Transformers work; Part II reveals how they become powerful at scale. "
        "Understanding pretraining, scaling laws, reasoning capabilities, inference optimization, and "
        "interpretability equips you to make informed decisions about which models to use, how to deploy "
        "them efficiently, and why they behave the way they do."
    ),
    "part-3-working-with-llms/index.html": (
        "Knowing how LLMs work is necessary but not sufficient; you also need to know how to use them "
        "effectively. Part III bridges theory and practice by teaching you to call LLM APIs, craft "
        "high-quality prompts, and combine classical ML with LLM capabilities to build practical systems."
    ),
    "part-4-training-adapting/index.html": (
        "Off-the-shelf models rarely fit production needs perfectly. Part IV teaches you to generate "
        "training data, fine-tune models, apply parameter-efficient methods like LoRA, compress models "
        "through distillation, and align them with human preferences. These techniques let you customize "
        "LLMs for your specific domain without starting from scratch."
    ),
    "part-5-retrieval-conversation/index.html": (
        "LLMs have limited context windows and can hallucinate facts they were not trained on. "
        "Part V shows you how to ground models in external knowledge through embeddings, vector databases, "
        "and retrieval-augmented generation, then build conversational systems that maintain coherent "
        "multi-turn dialogue."
    ),
    "part-6-agentic-ai/index.html": (
        "Moving beyond single-turn question answering, Part VI covers the rapidly evolving field of "
        "AI agents: systems that plan, use tools, collaborate with other agents, and take actions in "
        "the real world. This part connects everything you have learned so far into autonomous, "
        "production-ready systems."
    ),
    "part-7-multimodal-applications/index.html": (
        "Language is just one modality. Part VII extends your LLM knowledge to vision, audio, and "
        "cross-modal systems, then surveys the rich landscape of LLM-powered applications from code "
        "generation to healthcare. Understanding multimodal capabilities prepares you for the convergence "
        "of AI modalities that is shaping the next generation of products."
    ),
    "part-8-evaluation-production/index.html": (
        "Building an LLM application is only half the battle; measuring its quality and keeping it "
        "running reliably is the other half. Part VIII gives you the evaluation frameworks, observability "
        "tools, and production engineering patterns needed to deploy LLM systems with confidence and "
        "maintain them over time."
    ),
    "part-9-safety-strategy/index.html": (
        "Technical excellence means little without responsible deployment and business justification. "
        "Part IX addresses the ethical, regulatory, and strategic dimensions of LLM adoption, helping you "
        "navigate safety requirements, bias mitigation, and ROI analysis so your AI projects succeed "
        "both technically and organizationally."
    ),
    "part-10-frontiers/index.html": (
        "The field of large language models evolves faster than any textbook can fully capture. Part X "
        "looks ahead at emerging architectures, research directions, and the broader societal implications "
        "of AI. This final part helps you develop the forward-looking perspective needed to stay current "
        "as the technology continues to advance."
    ),

    # ============ CHAPTER (MODULE) INDEX PAGES ============
    # Part 1
    "part-1-foundations/module-00-ml-pytorch-foundations/index.html": (
        "This chapter provides the prerequisite knowledge that every other chapter depends on. "
        "The machine learning concepts, neural network mechanics, and PyTorch skills introduced here "
        "will resurface repeatedly, from training Transformers in Chapter 4 to fine-tuning with LoRA "
        "in Chapter 15 and building RLHF pipelines in Chapter 17."
    ),
    "part-1-foundations/module-01-foundations-nlp-text-representation/index.html": (
        "Before LLMs, NLP researchers spent decades developing techniques to represent text numerically. "
        "This chapter traces that evolution from bag-of-words to contextual embeddings, building the "
        "intuition you need to understand why Transformer-based representations in later chapters are "
        "so much more powerful."
    ),
    "part-1-foundations/module-02-tokenization-subword-models/index.html": (
        "Tokenization is the first step in every LLM pipeline, and its design choices ripple through "
        "everything from model vocabulary size to multilingual performance. Understanding BPE, WordPiece, "
        "and SentencePiece here will help you diagnose issues in fine-tuning (Chapter 14), prompt "
        "engineering (Chapter 11), and inference optimization (Chapter 9)."
    ),
    "part-1-foundations/module-03-sequence-models-attention/index.html": (
        "Sequence models and attention mechanisms are the direct predecessors of the Transformer. "
        "By understanding RNNs, LSTMs, and the original attention mechanism, you gain insight into "
        "why the Transformer architecture (Chapter 4) was such a breakthrough and what limitations "
        "it was designed to overcome."
    ),
    "part-1-foundations/module-04-transformer-architecture/index.html": (
        "The Transformer is the architectural foundation of every modern LLM. This chapter is arguably "
        "the most important in the entire book: the self-attention mechanism, positional encodings, "
        "and encoder-decoder structure you learn here will appear in virtually every subsequent chapter, "
        "from pretraining to alignment to agent design."
    ),
    "part-1-foundations/module-05-decoding-text-generation/index.html": (
        "Understanding how models generate text, token by token, is essential for prompt engineering, "
        "inference optimization, and building conversational systems. The decoding strategies covered "
        "here (greedy, beam search, nucleus sampling) directly influence output quality in every "
        "application you will build in Parts III through VI."
    ),

    # Part 2
    "part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html": (
        "Pretraining is where LLMs acquire their broad capabilities, and scaling laws tell us how "
        "to allocate compute, data, and parameters efficiently. This chapter explains the trillion-dollar "
        "decisions behind models like GPT-4 and Llama, knowledge you need to evaluate model choices "
        "and understand the economics of AI throughout the rest of the book."
    ),
    "part-2-understanding-llms/module-07-modern-llm-landscape/index.html": (
        "The LLM ecosystem is crowded and fast-moving. This chapter maps the key model families, "
        "their architectures, and their trade-offs, giving you a practical framework for choosing "
        "which models to use in the API, fine-tuning, and deployment chapters that follow."
    ),
    "part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html": (
        "Recent breakthroughs show that LLMs can improve their outputs by \"thinking longer\" at "
        "inference time. Understanding chain-of-thought reasoning, test-time compute scaling, and "
        "verification strategies is increasingly central to building reliable AI systems, especially "
        "the agent architectures covered in Part VI."
    ),
    "part-2-understanding-llms/module-09-inference-optimization/index.html": (
        "Even the most capable model is useless if it is too slow or too expensive to serve. "
        "This chapter covers quantization, KV-cache optimization, speculative decoding, and other "
        "techniques that determine whether your LLM application can meet real-world latency and "
        "cost requirements in production (Part VIII)."
    ),
    "part-2-understanding-llms/module-18-interpretability/index.html": (
        "As LLMs become more capable, understanding what they have learned and why they produce "
        "specific outputs becomes critical. Interpretability tools like probing, attention analysis, "
        "and mechanistic interpretability complement the safety and alignment techniques in Chapters 17 "
        "and 32, helping you build systems you can trust and debug."
    ),

    # Part 3
    "part-3-working-with-llms/module-10-llm-apis/index.html": (
        "For most practitioners, LLM APIs are the primary interface to model capabilities. "
        "This chapter teaches you to work with chat completions, manage rate limits, handle errors "
        "gracefully, and optimize costs. These API patterns form the backbone of every application "
        "built in Parts V and VI."
    ),
    "part-3-working-with-llms/module-11-prompt-engineering/index.html": (
        "Prompt engineering is the most accessible and often the most cost-effective way to improve "
        "LLM output quality. The techniques here, including few-shot prompting, chain-of-thought, "
        "and structured output generation, apply directly to RAG systems (Chapter 20), agents "
        "(Chapter 22), and evaluation (Chapter 29)."
    ),
    "part-3-working-with-llms/module-12-hybrid-ml-llm/index.html": (
        "Not every problem needs a large language model, and not every LLM output should be trusted "
        "without verification. This chapter shows you when to combine classical ML with LLMs, "
        "building hybrid pipelines that are more accurate, faster, and cheaper than either approach "
        "alone. This pragmatic mindset carries through to the production chapters in Part VIII."
    ),

    # Part 4
    "part-4-training-adapting/module-13-synthetic-data/index.html": (
        "High-quality training data is the bottleneck for most fine-tuning projects. This chapter "
        "teaches you to generate, filter, and validate synthetic data using LLMs themselves, a "
        "technique that directly enables the fine-tuning workflows in Chapters 14 and 15 and the "
        "alignment pipelines in Chapter 17."
    ),
    "part-4-training-adapting/module-14-fine-tuning-fundamentals/index.html": (
        "Fine-tuning transforms a general-purpose LLM into a specialist for your domain. "
        "This chapter covers the full workflow: data preparation, training configuration, "
        "catastrophic forgetting mitigation, and evaluation. It provides the foundation for the "
        "parameter-efficient methods in Chapter 15 and alignment techniques in Chapter 17."
    ),
    "part-4-training-adapting/module-15-peft/index.html": (
        "Full fine-tuning is expensive and often unnecessary. Parameter-efficient methods like LoRA "
        "and QLoRA let you adapt large models by training only a small fraction of their parameters, "
        "dramatically reducing compute costs. These techniques make fine-tuning accessible even on "
        "consumer hardware, a practical skill used throughout Parts V and VI."
    ),
    "part-4-training-adapting/module-16-distillation-merging/index.html": (
        "Sometimes you need a smaller, faster model that retains the quality of a larger one. "
        "Knowledge distillation and model merging let you compress capabilities or combine "
        "specialized models, techniques that directly support the inference optimization goals "
        "of Chapter 9 and the production deployment patterns of Part VIII."
    ),
    "part-4-training-adapting/module-17-alignment-rlhf-dpo/index.html": (
        "Alignment is what separates a raw language model from a helpful, harmless assistant. "
        "This chapter covers RLHF, DPO, and constitutional AI, the techniques that shaped models "
        "like ChatGPT and Claude. Understanding alignment is essential for the safety discussions "
        "in Chapter 32 and for anyone building user-facing AI systems."
    ),

    # Part 5
    "part-5-retrieval-conversation/module-19-embeddings-vector-db/index.html": (
        "Embeddings transform text into dense vectors that capture semantic meaning, and vector "
        "databases make those vectors searchable at scale. This chapter provides the retrieval "
        "infrastructure that powers RAG systems in Chapter 20 and grounds the conversational "
        "AI systems in Chapter 21."
    ),
    "part-5-retrieval-conversation/module-20-rag/index.html": (
        "Retrieval-augmented generation is one of the most widely deployed LLM patterns in production. "
        "By combining retrieval with generation, you can reduce hallucinations, keep responses current, "
        "and ground outputs in authoritative sources. This chapter is central to building the "
        "knowledge-intensive applications covered in Part VI and Part VIII."
    ),
    "part-5-retrieval-conversation/module-21-conversational-ai/index.html": (
        "Conversational AI brings together everything from prompt engineering to memory management "
        "to retrieval. This chapter teaches you to build multi-turn dialogue systems that maintain "
        "context, manage state, and deliver coherent user experiences, skills that connect directly "
        "to the agent architectures in Part VI."
    ),

    # Part 6
    "part-6-agentic-ai/module-22-ai-agents/index.html": (
        "AI agents represent a paradigm shift from reactive question-answering to proactive "
        "problem-solving. This chapter introduces the core agent loop: perceive, reason, plan, "
        "and act. The architectural patterns here form the foundation for tool use (Chapter 23), "
        "multi-agent systems (Chapter 24), and production agent deployment (Chapter 26)."
    ),
    "part-6-agentic-ai/module-23-tool-use-protocols/index.html": (
        "Agents become truly powerful when they can call external tools: APIs, databases, code "
        "interpreters, and more. This chapter covers function calling, tool protocols like MCP, "
        "and structured output formats that enable reliable tool use. These capabilities are "
        "prerequisites for the specialized and multi-agent systems in Chapters 24 and 25."
    ),
    "part-6-agentic-ai/module-24-multi-agent-systems/index.html": (
        "Complex tasks often exceed what a single agent can handle. Multi-agent systems use "
        "collaboration patterns like supervisor hierarchies, debate, and pipeline architectures "
        "to decompose problems. This chapter builds on the single-agent foundations of Chapter 22 "
        "and connects to the safety considerations of Chapter 26."
    ),
    "part-6-agentic-ai/module-25-specialized-agents/index.html": (
        "While Chapters 22 through 24 cover general agent principles, this chapter focuses on "
        "domain-specific agent types: coding assistants, research agents, data analysis agents, "
        "and more. Understanding specialization patterns helps you design agents that excel at "
        "specific tasks rather than being mediocre generalists."
    ),
    "part-6-agentic-ai/module-26-agent-safety-production/index.html": (
        "Autonomous agents introduce unique risks: uncontrolled tool execution, cascading failures, "
        "and unexpected behaviors. This chapter covers sandboxing, human-in-the-loop patterns, "
        "cost controls, and monitoring strategies that make agents safe for production. It bridges "
        "the agentic techniques of Part VI with the broader safety discussion in Chapter 32."
    ),

    # Part 7
    "part-7-multimodal-applications/module-27-multimodal/index.html": (
        "Modern LLMs increasingly process images, audio, and video alongside text. This chapter "
        "covers vision-language models, document AI, and cross-modal architectures, extending your "
        "understanding of Transformers (Chapter 4) into the multimodal domain. These capabilities "
        "unlock the application patterns surveyed in Chapter 28."
    ),
    "part-7-multimodal-applications/module-28-llm-applications/index.html": (
        "This chapter surveys the rich landscape of LLM applications, from code generation and "
        "creative writing to healthcare and legal analysis. By examining real-world use cases, you "
        "can identify which techniques from earlier chapters (RAG, fine-tuning, agents) best fit "
        "each application domain."
    ),

    # Part 8
    "part-8-evaluation-production/module-29-evaluation-observability/index.html": (
        "You cannot improve what you cannot measure. This chapter covers LLM evaluation methods "
        "including automated metrics, human evaluation, and LLM-as-judge approaches. The evaluation "
        "frameworks here apply to every system built in this book, from simple API calls to complex "
        "multi-agent pipelines."
    ),
    "part-8-evaluation-production/module-30-observability-monitoring/index.html": (
        "Production LLM systems require continuous monitoring of latency, cost, quality, and "
        "safety metrics. This chapter teaches you to instrument your systems with tracing, logging, "
        "and alerting, ensuring you can detect and respond to issues before they affect users. "
        "These practices complement the evaluation methods of Chapter 29."
    ),
    "part-8-evaluation-production/module-31-production-engineering/index.html": (
        "Taking an LLM prototype to production involves infrastructure decisions, scaling strategies, "
        "and reliability patterns that go beyond model quality. This chapter covers deployment "
        "architectures, caching, load balancing, and CI/CD for LLM systems, bringing together "
        "techniques from across the book into production-ready implementations."
    ),

    # Part 9
    "part-9-safety-strategy/module-32-safety-ethics-regulation/index.html": (
        "As LLMs become embedded in high-stakes decisions, safety and ethics move from nice-to-have "
        "to regulatory requirements. This chapter covers bias detection, content filtering, red-teaming, "
        "and emerging AI regulations. It builds on the alignment techniques of Chapter 17 and applies "
        "to every system deployed in production."
    ),
    "part-9-safety-strategy/module-33-strategy-product-roi/index.html": (
        "Technical capability alone does not guarantee business success. This chapter helps you build "
        "the business case for LLM adoption, estimate ROI, navigate build-versus-buy decisions, "
        "and align AI strategy with organizational goals. It provides the strategic lens needed to "
        "turn the technical skills from earlier chapters into real-world impact."
    ),

    # Part 10
    "part-10-frontiers/module-34-emerging-architectures/index.html": (
        "The Transformer may not be the final word in sequence modeling. This chapter explores "
        "emerging architectures like state-space models, mixture-of-experts variants, and "
        "retrieval-augmented pretraining that may shape the next generation of language models. "
        "Understanding these trends helps you future-proof the skills built throughout this book."
    ),
    "part-10-frontiers/module-35-ai-society/index.html": (
        "AI does not exist in a vacuum. This chapter examines the societal implications of LLMs: "
        "labor market effects, educational transformation, geopolitical competition, and long-term "
        "safety considerations. It provides the broader context needed to deploy AI responsibly "
        "and contribute to the ongoing conversation about AI governance."
    ),

    # Appendix A (the only appendix missing)
    "appendices/appendix-a-mathematical-foundations/index.html": (
        "Mathematics is the language in which neural networks are expressed. This appendix covers "
        "the linear algebra, calculus, probability, and information theory concepts that appear "
        "throughout the book, from attention score computation in Chapter 4 to loss functions in "
        "Chapter 14. Use it as a reference whenever the math in the main chapters feels unfamiliar."
    ),
}


def find_insertion_point(content):
    """Find where to insert the big-picture callout.

    Priority:
    1. After </div> closing of .overview or .part-overview div
    2. After </figure> of .illustration
    3. After </blockquote> of .epigraph
    4. After first <div class="content"> opening
    """
    # Strategy: find the overview/part-overview div closing
    # We need to find the closing </div> of the overview

    # Look for part-overview or overview div
    overview_patterns = [
        r'<div class="part-overview">',
        r'<div class="overview">',
    ]

    for pat in overview_patterns:
        match = re.search(pat, content)
        if match:
            # Find the closing </div> for this div
            start = match.start()
            depth = 0
            i = start
            while i < len(content):
                if content[i:i+4] == '<div':
                    depth += 1
                elif content[i:i+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        return i + 6  # after </div>
                i += 1

    # Look for illustration figure
    fig_match = re.search(r'</figure>', content)
    if fig_match:
        return fig_match.end()

    # Look for epigraph
    epigraph_match = re.search(r'</blockquote>', content)
    if epigraph_match:
        return epigraph_match.end()

    # Fallback: after <div class="content">
    content_match = re.search(r'<div class="content">\s*\n', content)
    if content_match:
        return content_match.end()

    return None


def add_big_picture(filepath, blurb):
    """Add a big-picture callout to the given file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'big-picture' in content:
        print(f"  SKIP (already has big-picture): {filepath}")
        return False

    pos = find_insertion_point(content)
    if pos is None:
        print(f"  ERROR: Could not find insertion point in {filepath}")
        return False

    callout = f"""
<div class="callout big-picture">
    <h4>The Big Picture</h4>
    <p>{blurb}</p>
</div>
"""

    new_content = content[:pos] + "\n" + callout + content[pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ADDED: {filepath}")
    return True


def main():
    added = 0
    errors = 0
    skipped = 0

    for relpath, blurb in BLURBS.items():
        filepath = os.path.join(BASE, relpath)
        if not os.path.exists(filepath):
            print(f"  NOT FOUND: {filepath}")
            errors += 1
            continue

        result = add_big_picture(filepath, blurb)
        if result:
            added += 1
        elif result is False:
            skipped += 1

    print(f"\nDone: {added} added, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
