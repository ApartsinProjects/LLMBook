"""9th edition Wave A4: insert "Looking Back" recap callouts at the top
of each chapter index page (right after the chapter-opener illustration,
just before the Chapter Overview). The recap is 3-5 sentences that
rebuild context from prior chapters so readers returning after a break
can pick up without re-reading.

Each entry is hand-written for its specific chapter; the script just
applies the canonical insertion pattern.

Idempotent: looks for sentinel `<!-- v710-looking-back -->` and skips
files that already have it.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

SENTINEL = '<!-- v710-looking-back -->'

# (chapter_index_path, body_html) — body_html is the inner content
# (paragraph + optional bullet list). Recaps are tailored per chapter.
RECAPS: dict[str, str] = {
    'part-1-foundations/module-00-ml-pytorch-foundations/index.html':
        '<p>This is where the book begins. You arrive with Python, curiosity, and (we assume) some prior exposure to machine learning. Everything before this chapter is the front matter that told you what the book covers, who it is for, and how to read it. From here on, every chapter <em>builds</em>: by the end of Part I you will have written a working Transformer; by the end of the book you will have shipped an agent into production.</p>',

    'part-1-foundations/module-01-foundations-nlp-text-representation/index.html':
        '<p>Chapter 0 gave you the PyTorch foundations: tensors, autograd, the training loop. Now we turn from generic deep learning to the specific problem this book is about: how do you represent <em>text</em> as numbers a model can learn from? The chapter starts with the classical answers (bag-of-words, n-grams, TF-IDF), shows what they got wrong, and ends with the embedding revolution (Word2Vec, GloVe) that made transformers possible.</p>',

    'part-1-foundations/module-02-tokenization-subword-models/index.html':
        '<p>Chapter 1 showed that words are not the right unit of text for modern models: vocabulary explodes, rare words become &lt;UNK&gt;, and you cannot generalize from "running" to "ran." This chapter introduces the answer the field converged on: <em>subword tokenization</em>. Byte-Pair Encoding (BPE), WordPiece, and SentencePiece all share one trick — compose any word from a fixed vocabulary of frequent fragments. Every modern LLM tokenizes this way; understanding it explains a lot of LLM behavior you will see later.</p>',

    'part-1-foundations/module-03-sequence-models-attention/index.html':
        '<p>You now have tokens (Chapter 2) and you know how to embed them (Chapter 1). The remaining question is the architectural one: how do you process a <em>sequence</em> of tokens? This chapter walks through the answer the field gave (RNNs and LSTMs) and the answer that won (the attention mechanism). By the end you will understand why "Attention Is All You Need" was such a watershed moment.</p>',

    'part-1-foundations/module-04-transformer-architecture/index.html':
        '<p>Chapter 3 introduced attention as a mechanism. This chapter assembles attention into the <strong>Transformer</strong> — the architecture every modern LLM is built on. You will see how one token gets computed end-to-end (Section 4.1), then build a working decoder-only Transformer from scratch in PyTorch (Section 4.2). The 300 lines of code at the end of this chapter are the most important code in the book; everything from here on is engineering on top of this core.</p>',

    'part-1-foundations/module-05-decoding-text-generation/index.html':
        '<p>You built a Transformer in Chapter 4. It produces a probability distribution over the next token. This chapter answers the question the architecture left open: <em>which token do you actually pick?</em> Greedy, beam search, temperature sampling, top-k, top-p (nucleus), and how each one shapes the output. Understanding decoding is the difference between a model that confidently hallucinates and one that knows when to say "I don\'t know."</p>',

    'part-2-understanding-llms/module-06-pretraining-scaling-laws/index.html':
        '<p>Part I built up to a working Transformer. That Transformer needs to be <em>trained</em> on something — and the something is "most of the internet, plus everything we could license or scrape." This chapter zooms out from the architecture to the training recipe: what data goes in (and how it is cleaned), what objective the model optimizes, and the <strong>scaling laws</strong> that predict performance before you spend a million dollars on compute. Chinchilla, Kaplan, and the Chinchilla-vs-Kaplan reconciliation all live here.</p>',

    'part-2-understanding-llms/module-07-modern-llm-landscape/index.html':
        '<p>Chapter 6 told you <em>how</em> LLMs are trained. This chapter tells you <em>which</em> LLMs to actually use. The frontier (GPT, Claude, Gemini), the open-weight winners (Llama, Mistral, DeepSeek, Qwen, Gemma), and the architectural innovations that distinguish them (MoE vs. dense, GQA, sliding-window attention). This is the chapter to come back to whenever the question is "which model should I use for this task?"</p>',

    'part-2-understanding-llms/module-08-reasoning-test-time-compute/index.html':
        '<p>The model landscape from Chapter 7 includes a new category that didn\'t exist two years ago: <strong>reasoning models</strong>. o1, o3, DeepSeek-R1, and QwQ trade tokens for IQ — they "think out loud" before answering, and the extra computation buys real accuracy on hard problems. This chapter explains the paradigm (test-time compute), how these models are trained (RLVR, GRPO, PRM), and when paying for thinking actually pays off.</p>',

    'part-2-understanding-llms/module-09-inference-optimization/index.html':
        '<p>So far you know how LLMs are built (Chapter 6), which ones to use (Chapter 7), and how reasoning models trade compute for quality (Chapter 8). This chapter is the engineering chapter: how do you make any of them <em>fast and cheap</em> at inference? Quantization, KV-cache management, continuous batching, speculative decoding, and the serving frameworks (vLLM, TGI, SGLang) that put it all together. By the end you will know why a 70B model can be served on consumer hardware.</p>',

    'part-2-understanding-llms/module-31-interpretability/index.html':
        '<p>Part II so far has been about LLMs as <em>systems</em>: how they are trained, what families exist, how they reason, how they are served. This chapter turns inward: what is actually happening inside the weights? You will learn how to read attention patterns, run probing classifiers, identify circuits and induction heads, and use sparse autoencoders to find interpretable features. Interpretability sits in Part II because every Part-III-onward chapter implicitly assumes the model behaves predictably, and this chapter is where you learn the tools to verify that.</p>',

    'part-3-working-with-llms/module-10-llm-apis/index.html':
        '<p>Part II ended with you understanding LLMs from the inside. Part III turns to using them from the outside. The starting point is the simplest possible interface: <strong>an API call</strong>. This chapter covers how the major providers expose their models (OpenAI, Anthropic, Google), the patterns they share (chat completions, function calling, streaming, structured output), and the patterns that distinguish them. By the end you can swap providers in an afternoon.</p>',

    'part-3-working-with-llms/module-11-prompt-engineering/index.html':
        '<p>You can call an API (Chapter 10). The question is what to put in the prompt. This chapter is the craft of prompt engineering: zero-shot vs. few-shot, role prompts, chain-of-thought, self-consistency, ReAct, and the prompt patterns that actually move the needle in production. Prompt engineering is not over — it is the lowest-cost knob you have, and this chapter teaches you when to turn it before reaching for fine-tuning.</p>',

    'part-3-working-with-llms/module-12-hybrid-ml-llm/index.html':
        '<p>An LLM is not always the right tool. This chapter is about <strong>combining</strong> LLMs with classical ML, when classical ML alone is better, and how to use LLMs as a feature engine inside a traditional pipeline. The decision frameworks here are some of the most reused tables in the book; come back when you need to defend an architecture choice in a design review.</p>',

    'part-4-training-adapting/module-13-synthetic-data/index.html':
        '<p>Part III used LLMs as they came from the lab. Part IV is where you <em>adapt</em> them. The first prerequisite for adaptation is data — and the field has discovered that synthetic data, generated by larger models, can replace huge fractions of human-labeled data. This chapter covers Self-Instruct, Evol-Instruct, Magpie, distillation pipelines, and the quality controls that prevent synthetic data from poisoning your model.</p>',

    'part-4-training-adapting/module-14-fine-tuning-fundamentals/index.html':
        '<p>You have data (Chapter 13). Now you fine-tune. This chapter is the canonical home for fine-tuning fundamentals: when to fine-tune at all (vs. prompting or RAG), full fine-tuning vs. parameter-efficient methods, catastrophic forgetting, and the 5-question decision tree (Figure 14.1.3) that the rest of the book cross-references when fine-tuning comes up.</p>',

    'part-4-training-adapting/module-15-peft/index.html':
        '<p>Chapter 14 introduced fine-tuning. This chapter covers what most practitioners actually do instead: <strong>parameter-efficient fine-tuning</strong>. LoRA, QLoRA, IA<sup>3</sup>, prefix tuning, prompt tuning, and the merging tricks (DARE, TIES) that let you stack multiple adapters. PEFT is the reason fine-tuning a 70B model on one GPU is possible.</p>',

    'part-4-training-adapting/module-16-alignment-rlhf-dpo/index.html':
        '<p>Fine-tuning (Chapter 14) and PEFT (Chapter 15) teach a model new capabilities. <strong>Alignment</strong> teaches it new <em>preferences</em>. RLHF, DPO, IPO, KTO, ORPO — this chapter is the alignment buffet: how preference data is collected, how the algorithms differ, and which one you reach for depending on your data and compute budget.</p>',

    'part-5-retrieval-conversation/module-17-embeddings-vector-db/index.html':
        '<p>Part IV adapted the model. Part V gives the model <em>memory</em>. This chapter is the foundation: embeddings (how text becomes vectors), vector databases (how vectors become searchable), and semantic search (how the two combine into "find the most relevant chunk for this query"). Everything in Chapter 18 (RAG) and Chapter 19 (Conversational AI) sits on this layer.</p>',

    'part-5-retrieval-conversation/module-18-rag/index.html':
        '<p>You can find relevant chunks (Chapter 17). Now you feed them to an LLM. This chapter is <strong>retrieval-augmented generation</strong>: the architecture, the failure modes (lost-in-the-middle, irrelevant retrievals, conflicting sources), the advanced patterns (HyDE, multi-query, query rewriting, reranking, parent-doc retrieval), and when long-context windows make RAG obsolete (rarely, it turns out).</p>',

    'part-5-retrieval-conversation/module-19-conversational-ai/index.html':
        '<p>RAG (Chapter 18) handles a single question. <strong>Conversation</strong> handles many. This chapter is about the engineering of multi-turn dialogue: memory architectures, summarization, slot tracking, persona management, and the safety patterns specific to chat (toxic-input guards, jailbreak resistance, identity stability). The patterns here apply equally to customer-support bots and the persistent agents in Part VI.</p>',

    'part-6-agentic-ai/module-20-ai-agents/index.html':
        '<p>Parts I through V built up to "an LLM that retrieves, fine-tunes, and converses." Part VI takes the final step: an LLM that <em>acts</em>. This chapter is the canonical home for the agent loop (perception, reasoning, action, observation) — the four-step pattern that everything in Chapters 21 through 24 specializes. ReAct, planning loops, reflection, the AutoGPT lineage; this is where the prompt patterns from Chapter 11 become full systems.</p>',

    'part-6-agentic-ai/module-21-tool-use-protocols/index.html':
        '<p>An agent loop (Chapter 20) needs <em>tools</em>. This chapter is the canonical home for function calling: JSON schema mechanics, error handling, parallel tool calls, the Model Context Protocol (MCP), and the A2A protocols that let agents talk to each other. By the end you can wire any agent up to any tool, and you understand what 2025 settled about how agents should expose capabilities.</p>',

    'part-6-agentic-ai/module-22-multi-agent-systems/index.html':
        '<p>One agent (Chapter 20) with tools (Chapter 21) handles most production tasks. Some tasks need <em>several</em> agents. This chapter covers the framework landscape (LangGraph, CrewAI, AutoGen, Swarm), the architectural patterns (supervisor, hierarchical, debate, ensemble), and the engineering reality: most "multi-agent" systems work because they replicate one good agent with role-specific prompts, not because of any deep coordination magic.</p>',

    'part-6-agentic-ai/module-23-specialized-agents/index.html':
        '<p>Chapters 20-22 covered agents as a general pattern. This chapter zooms in on the specializations that actually ship: <strong>code agents</strong> (Cursor, Claude Code, Devin), <strong>browser agents</strong> (web navigation, form-filling), <strong>research agents</strong> (deep research, Open Deep Research), and the benchmarks that measure them (SWE-bench, WebArena, GAIA). The patterns here are the most production-grade in the book.</p>',

    'part-6-agentic-ai/module-24-agent-safety-production/index.html':
        '<p>You have built an agent (Chapters 20-23). Now you have to <em>operate</em> it. This chapter is the canonical home for agent safety, sandboxing, prompt-injection defense, observability, cost control, and graceful degradation. The patterns here are why a code-execution agent doesn\'t rm -rf the host and why a customer-service agent doesn\'t leak everyone\'s past tickets.</p>',

    'part-7-multimodal-applications/module-25-multimodal/index.html':
        '<p>Parts I-VI built text-only systems. Part VII opens the modality. This chapter covers vision-language models (Flamingo lineage to GPT-4V to Claude 3.5), audio + music generation, video generation (Sora, Veo), document understanding, embodied multimodal agents, and the 3D representations (Gaussian splatting) that may become the next standard. Multimodal is no longer "research" — it is the default product surface for 2026.</p>',

    'part-7-multimodal-applications/module-26-llm-applications/index.html':
        '<p>The previous 25 chapters built the toolkit. This chapter is the application showcase: <strong>where the toolkit actually gets used</strong>. Vibe-coding and AI-assisted software engineering, finance and trading, healthcare and biomedical, recommendation and search, cybersecurity, education, legal, creative industries, and robotics. Each section is a quick deep-dive into one industry\'s LLM playbook.</p>',

    'part-8-evaluation-production/module-27-evaluation-observability/index.html':
        '<p>You have built something (Parts III-VII). How do you know if it works? This chapter is the eval chapter: classical metrics, LLM-as-judge, eval-driven quality gates, observability, OpenTelemetry, long-context benchmarks, and the experimental rigor that separates "ships features" from "ships <em>working</em> features." Eval is the most under-invested part of every team\'s LLM stack; this chapter is the corrective.</p>',

    'part-8-evaluation-production/module-28-production-engineering/index.html':
        '<p>Eval (Chapter 27) tells you what\'s working. This chapter is everything else about running an LLM in production: application architecture, deployment, frontends, scaling, guardrails, LLMOps, AI gateways, workflow orchestration, edge deployment, reliability engineering, and Kubernetes-native LLM operations. The patterns here are why a customer-facing AI feature stays up for years, not weeks.</p>',

    'part-9-safety-strategy/module-29-safety-ethics-regulation/index.html':
        '<p>Parts III-VIII built and operated LLM systems. Part IX zooms out to the questions that determine whether those systems are <em>allowed to exist</em>: safety threats, hallucination defense, bias and fairness, regulation (the EU AI Act in particular), licensing and IP, machine unlearning, red-teaming frameworks, environmental impact, and privacy attacks. The compliance chapter is the one you read before launch, not after.</p>',

    'part-9-safety-strategy/module-30-strategy-product-roi/index.html':
        '<p>Chapter 29 covered the regulatory and ethical floor. This chapter covers the strategic ceiling: how to <em>decide</em> what to build with LLMs, how to manage the product, how to measure ROI, how to evaluate vendors, how to plan compute, and how to think about LLM unit economics. The audience here shifts from engineers to engineering leaders — but engineers shipping LLM features benefit from reading their boss\'s playbook.</p>',

    'part-10-frontiers/module-32-emerging-architectures/index.html':
        '<p>The previous chapters cover what the field has settled on. Part X covers what it has not. Emergent abilities (real or mirage?), alternative architectures (Mamba, RWKV, state-space models), world models, theory of reasoning in LLMs, the agency question, multi-tool orchestration economies, and LLMs as universal sequence machines. This chapter is what to read if you are a researcher choosing a thesis topic, or a founder choosing a moat that won\'t evaporate in 18 months.</p>',

    'part-11-idea-to-product/module-33-idea-to-product/index.html':
        '<p>Part X looked forward in time; Part XI looks forward in your project. This chapter is for someone with an <em>idea</em> for an LLM product, asking: how do you go from "what if we used an LLM to do X" to a validated, scoped prototype? Choosing the model\'s role, risk and feasibility assessment, the observe-steer development loop, the founder\'s prototype loop, and documentation as a control surface. The shortest path from idea to MVP in this field is rarely a straight line; this chapter shows the curves.</p>',

    'part-11-idea-to-product/module-34-shipping-scaling/index.html':
        '<p>Chapter 33 took you to a prototype. This chapter takes you the rest of the way: launch constraints, AI unit economics, AI copilots across the product lifecycle, multi-provider strategy and lock-in, and post-launch monitoring. This is the final chapter of the main book; after it you reach the appendices (and the capstone project, which makes you build something using everything you\'ve learned).</p>',
}


def make_callout(body_html: str) -> str:
    return (
        f'<div class="callout looking-back">{SENTINEL}\n'
        f'<div class="callout-title">Looking Back</div>\n'
        f'{body_html}\n'
        f'</div>\n'
    )


def main() -> int:
    n_added = 0
    n_skip = 0
    n_missing = 0
    for rel_path, body in RECAPS.items():
        p = ROOT / rel_path
        if not p.exists():
            print(f'  MISSING: {rel_path}')
            n_missing += 1
            continue
        text = p.read_text(encoding='utf-8', errors='replace')
        if SENTINEL in text:
            n_skip += 1
            continue
        callout = make_callout(body)
        # Insert right after the chapter-opener figure (which lives inside
        # <main class="content"> and right before <div class="overview">),
        # OR right after <main class="content"> opening if no figure.
        # Find <div class="overview"> and insert before it.
        overview_match = re.search(
            r'<div\s+class="overview"\s*>', text, re.IGNORECASE)
        if overview_match:
            ins = overview_match.start()
        else:
            # Fallback: insert right after <main class="content">
            main_match = re.search(r'<main\s+class="content"[^>]*>', text,
                                   re.IGNORECASE)
            if not main_match:
                print(f'  SKIP (no <main> or <overview>): {rel_path}')
                continue
            # Skip past the meta-injected span if present
            after_main = text[main_match.end():]
            inj = re.match(r'\s*<span\s+class="pagefind-meta-injected"[^>]*>'
                           r'</span>(\s*<span[^>]*></span>)*\s*',
                           after_main, re.IGNORECASE)
            ins = main_match.end() + (inj.end() if inj else 0)
        new_text = text[:ins] + callout + '\n    ' + text[ins:]
        p.write_text(new_text, encoding='utf-8')
        n_added += 1
        print(f'  added: {rel_path}')

    print(f'\nAdded {n_added}; skipped {n_skip} (already present); missing {n_missing}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
