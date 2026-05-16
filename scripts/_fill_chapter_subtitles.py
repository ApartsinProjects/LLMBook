"""Fill in missing chapter subtitles in book_structure.yaml for the 29
chapters that don't have one. Each subtitle is a curated 1-2 line summary
of the chapter's scope.
"""
from __future__ import annotations
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pyyaml missing", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]

SUBTITLES = {
    # Part I Foundations
    "ml-pytorch-foundations":
        "PyTorch tensors, autograd, and the classical-ML primitives every modern LLM still rests on.",
    "foundations-nlp-text-representation":
        "From bag-of-words to embeddings: how text becomes math.",
    "tokenization-subword-models":
        "BPE, SentencePiece, and the surprisingly hard problem of cutting text into pieces.",
    "sequence-models-attention":
        "RNNs, LSTMs, and the attention breakthrough that made transformers possible.",
    "transformer-architecture":
        "Self-attention, multi-head, residual streams: the architecture that runs the field.",
    "decoding-text-generation":
        "Greedy, beam, temperature, top-k, top-p, and the test-time tricks that shape every output.",

    # Part II Understanding LLMs
    "pretraining-scaling-laws":
        "Data curation, Chinchilla, and what trillion-token training runs actually cost.",
    "modern-llm-landscape":
        "GPT, Claude, Gemini, Llama, Qwen, DeepSeek: the model families that define 2026.",
    "reasoning-test-time-compute":
        "o1-style reasoning, test-time scaling, and how chains of thought become products.",
    "inference-optimization":
        "KV cache, paged attention, speculative decoding, and the kernels behind vLLM-class serving.",
    "interpretability":
        "Probing, mechanistic interpretability, sparse autoencoders, and what we can finally see inside.",

    # Part III Working with LLMs
    "llm-apis":
        "Provider SDKs, streaming, function calling, rate limits: the working developer surface.",
    "prompt-engineering":
        "Templates, few-shot, chain-of-thought, structured output, and prompt-injection defense.",
    "hybrid-ml-llm":
        "When to reach for an LLM and when classical ML or a deterministic pipeline wins.",

    # Part IV Training & Adapting
    "synthetic-data":
        "Generating, validating, and using synthetic data without poisoning your distribution.",
    "fine-tuning-fundamentals":
        "Supervised fine-tuning end-to-end: data, loss, evaluation, infrastructure.",
    "peft":
        "LoRA, QLoRA, adapters, and the parameter-efficient tricks that make tuning affordable.",
    "alignment-rlhf-dpo":
        "Reward models, PPO, DPO, KTO, and the alignment toolchain modern frontier models share.",

    # Part V Retrieval & Conversation
    "embeddings-vector-db":
        "Dense embeddings, vector indexes, and the semantic-search stack that powers RAG.",
    "rag":
        "Retrieval-augmented generation patterns: indexing, retrieval, reranking, and answer synthesis.",
    "conversational-ai":
        "Memory, persona, multi-turn state, and what a production chatbot really has to do.",

    # Part VI Agentic AI
    "ai-agents":
        "The ReAct loop, planning, reflection, and what makes an LLM call an agent.",
    "tool-use-protocols":
        "Function calling, JSON schemas, MCP, A2A, and the protocols every agent now speaks.",
    "multi-agent-systems":
        "Supervisor, hub-and-spoke, swarm, and the coordination patterns for multiple agents.",
    "specialized-agents":
        "Coding agents, research agents, customer-support agents: domain-tuned patterns that ship.",

    # Part VII Multimodal Generation
    "multimodal":
        "Image, audio, video, and unified-omni models: the multimodal-generation foundations.",

    # Part VIII Evaluation & Production
    "evaluation-observability":
        "Eval design, LLM-as-judge, leaderboards, and the observability stack for production traffic.",
    "production-engineering":
        "Deployment, caching, cost control, retries, and the LLMOps patterns that survive 3am pages.",

    # Part IX Safety, Security & Ethics
    "safety-ethics-regulation":
        "Hallucination, bias, privacy, the EU AI Act, and the regulatory framework practitioners must navigate.",
}


def main() -> int:
    p = ROOT / "book_structure.yaml"
    struct = yaml.safe_load(p.read_text(encoding="utf-8"))
    n_filled = 0
    for part in struct["parts"]:
        for c in part.get("chapters", []):
            if c.get("subtitle"):
                continue
            slug = c.get("slug", "")
            if slug in SUBTITLES:
                c["subtitle"] = SUBTITLES[slug]
                n_filled += 1
    p.write_text(
        yaml.dump(struct, default_flow_style=False, sort_keys=False,
                   allow_unicode=True, width=200),
        encoding="utf-8",
    )
    print(f"Filled {n_filled} chapter subtitles")
    return 0


if __name__ == "__main__":
    sys.exit(main())
