#!/usr/bin/env python3
"""Run misplacement-detection heuristics on the section inventory and write the audit report."""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
INV = ROOT / "docs" / "content-audit" / "_placement_inventory.json"
OUT = ROOT / "docs" / "content-audit" / "CONTENT_PLACEMENT_AUDIT.md"

with open(INV) as f:
    D = json.load(f)

TOOLS_MODS = {"05", "14", "19", "25", "30", "36", "41", "45", "51", "56", "61", "71", "79", "83"}

# Canonical homes: topic-keyword (lowercase) -> (canonical-module, part-num, descriptor)
CANONICAL = {
    # Foundations Part I
    "tokenization": ("01", "1", "NLP & Text Representation"),
    "byte pair encoding": ("01", "1", "NLP & Text Representation"),
    "bpe ": ("01", "1", "NLP & Text Representation"),
    "self-attention": ("02", "1", "Sequence Models & Attention"),
    "attention mechanism": ("02", "1", "Sequence Models & Attention"),
    "rnn ": ("02", "1", "Sequence Models & Attention"),
    "lstm": ("02", "1", "Sequence Models & Attention"),
    "transformer architecture": ("03", "1", "Transformer Architecture"),
    "positional encoding": ("03", "1", "Transformer Architecture"),
    "rope ": ("03", "1", "Transformer Architecture"),
    "rotary": ("03", "1", "Transformer Architecture"),
    "layernorm": ("03", "1", "Transformer Architecture"),
    "beam search": ("04", "1", "Decoding & Text Generation"),
    "top-k sampling": ("04", "1", "Decoding & Text Generation"),
    "nucleus sampling": ("04", "1", "Decoding & Text Generation"),
    "decoding strategy": ("04", "1", "Decoding & Text Generation"),

    # Part II
    "scaling law": ("06", "2", "Pre-training & Scaling Laws"),
    "chinchilla": ("06", "2", "Pre-training & Scaling Laws"),
    "data curation": ("06", "2", "Pre-training & Scaling Laws"),
    "chain-of-thought": ("08", "2", "Reasoning & Test-Time Compute"),
    "test-time compute": ("08", "2", "Reasoning & Test-Time Compute"),
    "flash attention": ("09", "2", "Inference Optimization"),
    "kv cache": ("09", "2", "Inference Optimization"),
    "paged attention": ("09", "2", "Inference Optimization"),
    "quantization": ("09", "2", "Inference Optimization"),
    "speculative decoding": ("09", "2", "Inference Optimization"),
    "vllm": ("09", "2", "Inference Optimization"),
    "interpretability": ("10", "2", "Interpretability"),
    "circuit analysis": ("10", "2", "Interpretability"),
    "probing": ("10", "2", "Interpretability"),

    # Part III
    "openai api": ("11", "3", "LLM APIs"),
    "anthropic api": ("11", "3", "LLM APIs"),
    "few-shot prompt": ("12", "3", "Prompt Engineering"),
    "prompt engineering": ("12", "3", "Prompt Engineering"),
    "chain of thought prompting": ("12", "3", "Prompt Engineering"),

    # Part IV
    "synthetic data": ("15", "4", "Synthetic Data Generation"),
    "instruction tuning": ("16", "4", "Fine-Tuning Fundamentals"),
    "supervised fine-tuning": ("16", "4", "Fine-Tuning Fundamentals"),
    "sft ": ("16", "4", "Fine-Tuning Fundamentals"),
    "lora": ("17", "4", "PEFT"),
    "qlora": ("17", "4", "PEFT"),
    "adapter": ("17", "4", "PEFT"),
    "prefix tuning": ("17", "4", "PEFT"),
    "rlhf": ("18", "4", "Alignment / RLHF / DPO"),
    "ppo ": ("18", "4", "Alignment / RLHF / DPO"),
    "dpo ": ("18", "4", "Alignment / RLHF / DPO"),
    "direct preference optimization": ("18", "4", "Alignment / RLHF / DPO"),
    "preference tuning": ("18", "4", "Alignment / RLHF / DPO"),
    "rlaif": ("18", "4", "Alignment / RLHF / DPO"),
    "reward model": ("18", "4", "Alignment / RLHF / DPO"),

    # Part V
    "clip": ("22", "5", "Vision-Language Models"),
    "vit ": ("22", "5", "Vision-Language Models"),
    "llava": ("22", "5", "Vision-Language Models"),
    "tts ": ("20", "5", "Audio & Music Generation"),
    "voice cloning": ("20", "5", "Audio & Music Generation"),
    "trocr": ("21", "5", "Document Understanding & OCR"),
    "ocr ": ("21", "5", "Document Understanding & OCR"),
    "nerf": ("23", "5", "3D Generation"),
    "gaussian splatting": ("23", "5", "3D Generation"),
    "vla ": ("24", "5", "Vision-Language-Action"),
    "openvla": ("24", "5", "Vision-Language-Action"),

    # Part VI
    "react agent": ("26", "6", "AI Agent Foundations"),
    "agent planning": ("26", "6", "AI Agent Foundations"),
    "function calling": ("27", "6", "Tool Use & Protocols"),
    "tool calling": ("27", "6", "Tool Use & Protocols"),
    "mcp ": ("27", "6", "Tool Use & Protocols"),
    "model context protocol": ("27", "6", "Tool Use & Protocols"),
    "a2a protocol": ("27", "6", "Tool Use & Protocols"),
    "multi-agent": ("28", "6", "Multi-Agent Systems"),
    "agent orchestration": ("28", "6", "Multi-Agent Systems"),
    "coding agent": ("29", "6", "Specialized Agents"),

    # Part VII
    "embeddings": ("31", "7", "Embeddings, Vector DBs"),
    "vector database": ("31", "7", "Embeddings, Vector DBs"),
    "hnsw": ("31", "7", "Embeddings, Vector DBs"),
    "faiss": ("31", "7", "Embeddings, Vector DBs"),
    "chromadb": ("31", "7", "Embeddings, Vector DBs"),
    "chunking": ("31", "7", "Embeddings, Vector DBs"),
    "retrieval-augmented generation": ("32", "7", "RAG Fundamentals"),
    "rag pipeline": ("32", "7", "RAG Fundamentals"),
    "agentic rag": ("32", "7", "RAG Fundamentals"),
    "crag": ("32", "7", "RAG Fundamentals"),
    "ner ": ("34", "7", "Structured Extraction & NER"),
    "named entity recognition": ("34", "7", "Structured Extraction & NER"),
    "coreference": ("34", "7", "Structured Extraction & NER"),
    "knowledge graph": ("35", "7", "Advanced RAG (KGs)"),
    "graphrag": ("35", "7", "Advanced RAG (KGs)"),
    "ndcg": ("36", "7", "Retrieval Tools (IR metrics)"),
    "mrr ": ("36", "7", "Retrieval Tools (IR metrics)"),
    "bm25": ("36", "7", "Retrieval Tools (IR metrics)"),
    "reranking": ("31", "7", "Embeddings (reranking)"),
    "colbert": ("31", "7", "Embeddings (late interaction)"),

    # Part VIII
    "dialogue system": ("37", "8", "Conversational AI"),
    "conversational memory": ("37", "8", "Conversational AI"),
    "voice assistant": ("40", "8", "Voice & Realtime"),
    "speech-to-text": ("40", "8", "Voice & Realtime"),
    "whisper": ("40", "8", "Voice & Realtime"),
    "realtime api": ("40", "8", "Voice & Realtime"),

    # Part IX
    "rouge": ("42", "9", "Evaluation & Quality Metrics"),
    "bleu": ("42", "9", "Evaluation & Quality Metrics"),
    "g-eval": ("46", "9", "LLM-as-Judge"),
    "llm-as-judge": ("46", "9", "LLM-as-Judge"),
    "llm-as-a-judge": ("46", "9", "LLM-as-Judge"),
    "judge model": ("46", "9", "LLM-as-Judge"),
    "ragas": ("43", "9", "Specialized Eval (RAG)"),
    "ragas score": ("43", "9", "Specialized Eval (RAG)"),
    "opentelemetry": ("44", "9", "Online Eval & Observability"),
    "langfuse": ("44", "9", "Online Eval & Observability"),

    # Part X
    "prompt injection": ("47", "10", "Adversarial Security"),
    "jailbreak": ("47", "10", "Adversarial Security"),
    "red team": ("47", "10", "Adversarial Security"),
    "guardrail": ("48", "10", "Guardrails"),
    "output filter": ("48", "10", "Guardrails"),
    "differential privacy": ("50", "10", "Privacy"),
    "membership inference": ("50", "10", "Privacy"),

    # Part XI
    "bias measurement": ("52", "11", "Bias & Fairness"),
    "fairness metric": ("52", "11", "Bias & Fairness"),
    "eu ai act": ("53", "11", "Regulation & Compliance"),
    "gdpr": ("53", "11", "Regulation & Compliance"),
    "watermark": ("54", "11", "Watermarking & Provenance"),
    "c2pa": ("54", "11", "Watermarking & Provenance"),
    "model card": ("54b", "11", "Transparency & Disclosure"),
    "datasheet": ("54b", "11", "Transparency & Disclosure"),
    "carbon": ("55", "11", "Environmental Impact"),
    "codecarbon": ("55", "11", "Environmental Impact"),

    # Part XII
    "tensor parallel": ("59", "12", "Distributed Training"),
    "pipeline parallel": ("59", "12", "Distributed Training"),
    "fsdp": ("59", "12", "Distributed Training"),
    "deepspeed": ("59", "12", "Distributed Training"),
    "megatron": ("59", "12", "Distributed Training"),
    "edge deployment": ("60", "12", "Edge & On-Device"),
    "on-device": ("60", "12", "Edge & On-Device"),
    "llama.cpp": ("60", "12", "Edge & On-Device"),

    # Part XIII
    "ai gateway": ("63", "13", "AI Gateways & Routing"),
    "model routing": ("63", "13", "AI Gateways & Routing"),
    "kubernetes": ("65", "13", "Containers & Kubernetes"),
    "temporal": ("64", "13", "Workflow Orchestration"),
    "durable execution": ("64", "13", "Workflow Orchestration"),
    "slo": ("66", "13", "Reliability & SLOs"),
    "model registry": ("66", "13", "Reliability & SLOs"),

    # Part XIV
    "product-market fit": ("67", "14", "Ideation"),
    "vibe coding": ("68", "14", "Vibe-Coding"),
    "vibe-coding": ("68", "14", "Vibe-Coding"),
    "unit economics": ("69", "14", "LLM Economics"),
    "cost per request": ("69", "14", "LLM Economics"),

    # Part XV
    "contract review": ("72", "15", "LLMs in Legal"),
    "discovery": ("72", "15", "LLMs in Legal"),
    "alphafold": ("74", "15", "LLMs in Healthcare & Bio"),
    "hipaa": ("74", "15", "LLMs in Healthcare & Bio"),
    "fda": ("74", "15", "LLMs in Healthcare & Bio"),
    "edgar": ("73", "15", "LLMs in Finance"),

    # Part XVI
    "emergent abilities": ("80", "16", "Frontier Architectures"),
    "mamba": ("80", "16", "Frontier Architectures"),
    "state space model": ("80", "16", "Frontier Architectures"),
    "moe ": ("80", "16", "Frontier Architectures"),
    "mixture of experts": ("80", "16", "Frontier Architectures"),
    "agi ": ("82", "16", "AGI Trajectories"),
}


def topic_match(section):
    """Return list of (topic_keyword, canonical_mod, canonical_part, descriptor) hits in section h1/h2/subtitle."""
    hits = []
    haystack = " ".join([
        section["h1"].lower(),
        section["subtitle"].lower(),
        " ".join(section["h2_list"]).lower(),
        " ".join(section["h3_list"]).lower(),
    ])
    # Augment with first 400 chars of intro
    haystack += " " + section.get("intro", "")[:400].lower()
    for kw, (mod, part, desc) in CANONICAL.items():
        if kw in haystack:
            hits.append((kw, mod, part, desc))
    return hits


def main():
    findings = []

    # --- Detection 1: theoretical content in tools-of-the-trade modules ---
    for s in D["sections"]:
        if s["module_num"] not in TOOLS_MODS:
            continue
        algo_n = s["callouts"].get("algorithm", 0)
        proof_n = s["callouts"].get("proof", 0)
        # We don't flag plain key-insight inside a tools module (intentional), only algorithm or proof.
        if algo_n + proof_n == 0:
            continue
        # Identify where this content likely belongs
        hits = topic_match(s)
        target = None
        if hits:
            # Pick the first non-tools target
            for kw, mod, part, desc in hits:
                if mod not in TOOLS_MODS:
                    target = (kw, mod, part, desc)
                    break
        findings.append({
            "signal": "theoretical-in-tools",
            "path": s["path"],
            "section_num": s["section_num"],
            "h1": s["h1"],
            "claim": f"contains {algo_n} algorithm callout(s) + {proof_n} proof callout(s) inside tools-of-the-trade module {s['module_num']}",
            "callouts": s["callouts"],
            "target": target,
            "action": ("MOVE_TO_X" if target else "NEEDS_DECISION"),
            "h2_list": s["h2_list"][:3],
        })

    # --- Detection 2: topic-vs-path mismatch (canonical home different module) ---
    for s in D["sections"]:
        mod = s["module_num"]
        if mod in TOOLS_MODS:
            continue  # already covered above
        hits = topic_match(s)
        if not hits:
            continue
        # Group hits by canonical module
        canonical_mods = Counter([h[1] for h in hits])
        if mod in canonical_mods:
            # The section's home is itself canonical for one of its topics, OK
            continue
        # If multiple hits, get the dominant canonical
        # But filter out single-hit matches with very common keywords (likely passing reference)
        # Use heuristic: only flag if topic-keyword appears in h1 or first h2
        h1_lc = s["h1"].lower()
        h2_lc = " ".join(s["h2_list"][:2]).lower() if s["h2_list"] else ""
        subtitle_lc = s["subtitle"].lower()
        primary_hits = [h for h in hits if h[0] in h1_lc or h[0] in h2_lc or h[0] in subtitle_lc]
        if not primary_hits:
            continue
        # Find the dominant canonical
        top_canonical = Counter([(h[1], h[2], h[3]) for h in primary_hits]).most_common(1)[0][0]
        if top_canonical[0] == mod:
            continue
        # Skip if section is in a tightly related cluster (adjacent module in same part)
        # E.g., section in 32 mentioning embeddings (mod 31) is fine - it's intra-part
        sec_part_m = D["modules"].get(mod, {}).get("part", "?")
        targ_part = top_canonical[1]
        # Heuristic: only flag cross-part contamination as high-confidence
        cross_part = (sec_part_m != targ_part)
        findings.append({
            "signal": "topic-path-mismatch",
            "path": s["path"],
            "section_num": s["section_num"],
            "h1": s["h1"],
            "h2_list": s["h2_list"][:3],
            "claim": f"primary topic ({top_canonical[2]}) belongs to module {top_canonical[0]} (Part {targ_part}); section lives in module {mod} (Part {sec_part_m})",
            "target": (None, top_canonical[0], top_canonical[1], top_canonical[2]),
            "action": ("MOVE_TO_X" if cross_part else "NEEDS_DECISION"),
            "primary_hits": [h[0] for h in primary_hits[:5]],
            "cross_part": cross_part,
        })

    # --- Detection 3: section in a non-existent / odd module slot (e.g., 38, 39 — missing modules) ---
    # Note 38 and 39 missing from Part 8. Already flagged by part audit.

    # --- Detection 4: long tool-library API discussion inside a main chapter ---
    # Heuristic: section contains library-shortcut + multiple code fragments + h1 named after a library
    LIB_NAMES = {"vllm", "peft", "trl", "langchain", "llamaindex", "haystack", "deepspeed", "transformers", "openai-sdk", "anthropic-sdk", "litellm", "mlflow", "weights and biases", "wandb"}
    for s in D["sections"]:
        if s["module_num"] in TOOLS_MODS:
            continue
        if s["callouts"].get("library-shortcut", 0) < 3:
            continue
        title_blob = (s["h1"] + " " + " ".join(s["h2_list"])).lower()
        lib_hits = [lib for lib in LIB_NAMES if lib in title_blob]
        if not lib_hits:
            continue
        sec_part = D["modules"].get(s["module_num"], {}).get("part", "?")
        # Identify the tools module for this part
        # Use BOOK mapping: part -> tools module
        part_tools_map = {"1":"05","2":None,"3":"14","4":"19","5":"25","6":"30","7":"36","8":"41","9":"45","10":"51","11":"56","12":"61","13":None,"14":"71","15":"79","16":"83"}
        tools_mod = part_tools_map.get(sec_part)
        if not tools_mod:
            continue
        findings.append({
            "signal": "library-deep-dive-in-main",
            "path": s["path"],
            "section_num": s["section_num"],
            "h1": s["h1"],
            "claim": f"library API deep-dive ({', '.join(lib_hits)}) inside main chapter; >=3 library-shortcut callouts",
            "target": (None, tools_mod, sec_part, f"Tools-of-the-Trade (mod {tools_mod})"),
            "action": "NEEDS_DECISION",
            "h2_list": s["h2_list"][:3],
        })

    # --- Detection 5: section.h1/h2 mention "Tools" but section is in a main chapter ---
    # (Rare; not flagging as separate signal.)

    # Save raw findings
    raw = ROOT / "docs" / "content-audit" / "_placement_findings.json"
    with open(raw, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2)

    # Aggregate by signal
    by_signal = Counter([f["signal"] for f in findings])
    by_action = Counter([f["action"] for f in findings])
    print(f"Total findings: {len(findings)}")
    print(f"By signal: {dict(by_signal)}")
    print(f"By action: {dict(by_action)}")
    return findings


if __name__ == "__main__":
    main()
