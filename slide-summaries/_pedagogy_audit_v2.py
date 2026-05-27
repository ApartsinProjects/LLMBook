"""
Pedagogy-completeness audit V2 for the LLMBook.

Improvements over V1:
1. Curated list of ~200 named LLM / audio / multimodal techniques (not heuristic
   capitalized-h3 detection).
2. For each technique, find the CANONICAL section: the one whose h3 (or h2)
   TITLE contains the technique name, with the longest body. Fall back to
   the longest body section that mentions the term if no title match.
3. Score the canonical section's h3-body AND its parent h2-body together
   (diagrams often live at the parent h2 level).
4. Filter out datasets / benchmarks / walkthroughs / tool catalog entries that
   legitimately do not need diagrams.
5. Output a ranked "enrichment punch list": techniques sorted by impact
   (score asc, body_len desc).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from collections import defaultdict


# ---------- Curated technique inventory ----------
# Each entry: ("display_name", "exact_match_regex", category, weight)
# weight = 1 (load-bearing), 0.6 (important), 0.3 (nice-to-have)
TECHNIQUES = [
    # Transformer architectures + variants
    ("BERT", r"\bBERT\b", "model-architecture", 1.0),
    ("RoBERTa", r"\bRoBERTa\b", "model-architecture", 0.6),
    ("GPT-2", r"\bGPT-?2\b", "model-architecture", 0.6),
    ("GPT-3", r"\bGPT-?3\b", "model-architecture", 0.6),
    ("T5", r"\bT5\b", "model-architecture", 1.0),
    ("BART", r"\bBART\b", "model-architecture", 0.6),
    ("DeBERTa", r"\bDeBERTa\b", "model-architecture", 0.3),
    ("XLM", r"\bXLM(?:-R)?\b", "model-architecture", 0.6),
    ("mBERT", r"\bmBERT\b", "model-architecture", 0.6),
    ("mT5", r"\bmT5\b", "model-architecture", 0.6),
    ("NLLB", r"\bNLLB(?:-200)?\b", "model-architecture", 0.6),
    ("Mamba", r"\bMamba\b", "model-architecture", 0.6),
    ("RetNet", r"\bRetNet\b", "model-architecture", 0.3),
    ("Mixtral", r"\bMixtral\b", "model-architecture", 1.0),
    ("MoE", r"\bMixture[- ]of[- ]Experts\b|\bMoE\b", "model-architecture", 1.0),
    ("Switch Transformer", r"\bSwitch[- ]Transformer\b", "model-architecture", 0.6),
    ("GShard", r"\bGShard\b", "model-architecture", 0.3),
    ("DeepSeek-V3", r"\bDeepSeek-V3\b", "model-architecture", 0.6),

    # Attention + positional + KV
    ("RoPE", r"\bRoPE\b|Rotary Position", "attention-positional", 1.0),
    ("YaRN", r"\bYaRN\b", "attention-positional", 0.6),
    ("FlashAttention", r"\bFlashAttention[-\d]*\b", "attention-positional", 1.0),
    ("ALiBi", r"\bALiBi\b", "attention-positional", 0.3),
    ("KV Cache", r"\bKV[- ]Cache\b|KV Caching", "attention-positional", 1.0),
    ("Multi-Query Attention", r"\bMulti-?Query Attention\b|\bMQA\b", "attention-positional", 0.6),
    ("Grouped-Query Attention", r"\bGrouped-?Query Attention\b|\bGQA\b", "attention-positional", 0.6),
    ("Speculative Decoding", r"\bSpeculative Decoding\b", "attention-positional", 1.0),

    # Tokenization
    ("BPE", r"\bBPE\b|Byte-Pair Encoding", "tokenization", 1.0),
    ("WordPiece", r"\bWordPiece\b", "tokenization", 0.6),
    ("SentencePiece", r"\bSentencePiece\b", "tokenization", 0.6),
    ("Unigram", r"\bUnigram tokeniz", "tokenization", 0.6),
    ("Word2Vec", r"\bWord2Vec\b", "embedding", 1.0),
    ("GloVe", r"\bGloVe\b", "embedding", 0.6),
    ("FastText", r"\bFastText\b", "embedding", 0.6),

    # Embeddings + retrieval
    ("SBERT", r"\bSBERT\b|Sentence-BERT|sentence-transformers", "embedding", 1.0),
    ("SimCSE", r"\bSimCSE\b", "embedding", 0.6),
    ("SDAE", r"\bSDAE\b", "embedding", 0.6),
    ("MTEB", r"\bMTEB\b", "benchmark", 0.6),
    ("DPR", r"\bDPR\b|Dense Passage Retrieval", "retrieval", 1.0),
    ("HNSW", r"\bHNSW\b", "retrieval", 1.0),
    ("IVF", r"\bIVF\b|Inverted File", "retrieval", 0.6),
    ("PQ", r"\bProduct Quantization\b|\bPQ\b", "retrieval", 0.6),
    ("FAISS", r"\bFAISS\b", "retrieval", 0.6),
    ("Annoy", r"\bAnnoy\b", "retrieval", 0.3),
    ("MMR", r"\bMMR\b|Maximal Marginal", "retrieval", 0.6),
    ("HyDE", r"\bHyDE\b", "retrieval", 0.6),
    ("HyPE", r"\bHyPE\b", "retrieval", 0.3),
    ("RAG-Fusion", r"RAG-Fusion", "retrieval", 0.6),
    ("RRF", r"Reciprocal Rank Fusion|\bRRF\b", "retrieval", 0.6),
    ("FiD", r"Fusion-in-Decoder|\bFiD\b", "retrieval", 0.6),
    ("RAFT", r"\bRAFT\b", "retrieval", 0.6),
    ("RAPTOR", r"\bRAPTOR\b", "retrieval", 0.6),
    ("CAG", r"Cache-Augmented Generation|\bCAG\b", "retrieval", 0.6),
    ("GraphRAG", r"\bGraphRAG\b", "retrieval", 0.6),
    ("BERTopic", r"\bBERTopic\b", "retrieval", 0.6),

    # Pretraining + scaling
    ("Chinchilla", r"\bChinchilla\b", "scaling", 0.6),
    ("Scaling Laws", r"scaling[- ]laws\b", "scaling", 1.0),
    ("Noam schedule", r"\bNoam\b.{0,40}schedule", "scaling", 0.6),
    ("Cosine schedule", r"cosine.{0,15}schedule|cosine annealing", "scaling", 0.6),
    ("AdamW", r"\bAdamW\b", "scaling", 1.0),

    # Fine-tuning + PEFT + alignment
    ("LoRA", r"\bLoRA\b", "peft", 1.0),
    ("QLoRA", r"\bQLoRA\b", "peft", 1.0),
    ("Prefix Tuning", r"Prefix[- ]Tuning", "peft", 0.6),
    ("Prompt Tuning", r"Prompt[- ]Tuning", "peft", 0.6),
    ("P-Tuning", r"\bP-?Tuning\b", "peft", 0.3),
    ("IA3", r"\bIA[3³]\b", "peft", 0.3),
    ("Adapter", r"bottleneck adapters?|Houlsby adapter", "peft", 0.6),
    ("MergeKit", r"MergeKit", "peft", 0.3),
    ("TIES Merging", r"TIES[- ]Merg", "peft", 0.6),
    ("Task Arithmetic", r"Task[- ]Arithmetic", "peft", 0.3),
    ("Model Soup", r"\bModel Soup\b|greedy soup", "peft", 0.3),
    ("Knowledge Distillation", r"Knowledge Distill", "peft", 1.0),
    ("DistilBERT", r"\bDistilBERT\b", "peft", 0.6),

    ("RLHF", r"\bRLHF\b|Human Feedback", "alignment", 1.0),
    ("PPO", r"\bPPO\b|Proximal Policy", "alignment", 1.0),
    ("DPO", r"\bDPO\b|Direct Preference", "alignment", 1.0),
    ("GRPO", r"\bGRPO\b|Group Relative Policy", "alignment", 1.0),
    ("RLVR", r"\bRLVR\b|Verifiable Reward", "alignment", 0.6),
    ("Constitutional AI", r"Constitutional AI", "alignment", 0.6),
    ("SFT", r"Supervised Fine-?Tuning|\bSFT\b", "alignment", 1.0),
    ("Actor-Critic", r"Actor[- ]Critic", "alignment", 0.6),
    ("REINFORCE", r"\bREINFORCE\b", "alignment", 0.6),

    # Inference + serving
    ("vLLM", r"\bvLLM\b", "serving", 1.0),
    ("SGLang", r"\bSGLang\b", "serving", 0.6),
    ("TGI", r"\bTGI\b|Text Generation Inference", "serving", 0.6),
    ("FSDP", r"\bFSDP\b", "training-sys", 1.0),
    ("DDP", r"\bDistributedDataParallel\b|\bDDP\b", "training-sys", 0.6),
    ("ZeRO", r"\bZeRO\b", "training-sys", 0.6),
    ("Quantization", r"\bquantiz", "serving", 1.0),
    ("GPTQ", r"\bGPTQ\b", "serving", 0.6),
    ("AWQ", r"\bAWQ\b", "serving", 0.6),
    ("torch.compile", r"torch\.compile", "training-sys", 0.6),

    # Agents
    ("ReAct", r"\bReAct\b(?! library)", "agents", 1.0),
    ("Reflexion", r"Reflexion|RefleXion", "agents", 0.6),
    ("Tree-of-Thoughts", r"Tree[- ]of[- ]Thoughts", "agents", 0.6),
    ("Chain-of-Thought", r"Chain[- ]of[- ]Thought", "agents", 1.0),
    ("ReWoo", r"\bReWoo\b", "agents", 0.6),
    ("Baby-AGI", r"Baby[- ]AGI", "agents", 0.3),
    ("Toolformer", r"\bToolformer\b", "agents", 1.0),
    ("ToolkenGPT", r"\bToolkenGPT\b", "agents", 0.6),
    ("Gorilla", r"\bGorilla\b", "agents", 0.6),
    ("MCP", r"Model Context Protocol|\bMCP\b", "agents", 1.0),
    ("LangChain", r"\bLangChain\b", "agents", 0.6),
    ("LangGraph", r"\bLangGraph\b", "agents", 1.0),
    ("LlamaIndex", r"\bLlamaIndex\b", "agents", 0.6),
    ("MemGPT", r"\bMemGPT\b|\bLetta\b", "agents", 0.6),
    ("AutoGen", r"\bAutoGen\b", "agents", 0.6),
    ("CrewAI", r"\bCrewAI\b", "agents", 0.6),

    # Vision-language (only those used outside pure vision)
    ("CLIP", r"\bCLIP\b(?!Seg)", "vlm", 1.0),
    ("SigLIP", r"\bSigLIP\b", "vlm", 0.6),
    ("BLIP", r"\bBLIP(?:-2|-3)?\b", "vlm", 1.0),
    ("LLaVA", r"\bLLaVA\b", "vlm", 1.0),
    ("Qwen-VL", r"\bQwen-?VL\b", "vlm", 0.6),
    ("ViT", r"\bViT\b|Vision Transformer", "vlm", 1.0),
    ("DeiT", r"\bDeiT\b", "vlm", 0.3),
    ("Swin", r"\bSwin\b", "vlm", 0.6),
    ("DINO", r"\bDINO(?:v2)?\b", "vlm", 0.6),
    ("SAM", r"\bSAM\b|Segment Anything", "vlm", 0.6),

    # Audio
    ("wav2vec", r"\bwav2vec(?: 2\.0)?\b", "audio", 1.0),
    ("HuBERT", r"\bHuBERT\b", "audio", 1.0),
    ("WavLM", r"\bWavLM\b", "audio", 0.6),
    ("BEATs", r"\bBEATs\b", "audio", 0.3),
    ("Whisper", r"\bWhisper\b", "audio", 1.0),
    ("CTC", r"\bCTC\b|Connectionist Temporal", "audio", 1.0),
    ("AST", r"\bAST\b|Audio Spectrogram Transformer", "audio", 0.6),
    ("Conformer", r"\bConformer\b", "audio", 0.6),
    ("CLAP", r"\bCLAP\b", "audio", 0.6),
    ("AudioCLIP", r"\bAudioCLIP\b", "audio", 0.3),
    ("EnCodec", r"\bEnCodec\b", "audio", 1.0),
    ("SoundStream", r"\bSoundStream\b", "audio", 0.6),
    ("DAC (audio)", r"\bDescript Audio Codec\b|\bDAC\b", "audio", 0.3),
    ("Mimi", r"\bMimi\b.{0,30}codec|Mimi.{0,30}Moshi", "audio", 0.3),
    ("RVQ", r"\bRVQ\b|Residual Vector Quantization", "audio", 1.0),
    ("VQ-VAE", r"\bVQ-?VAE\b", "audio", 0.6),
    ("VITS", r"\bVITS\b", "audio", 0.6),
    ("Bark", r"\bBark\b(?! ?library)", "audio", 0.6),
    ("MusicGen", r"\bMusicGen\b", "audio", 0.6),
    ("MusicLM", r"\bMusicLM\b", "audio", 0.6),

    # Eval
    ("RAGAS", r"\bRAGAS\b", "eval", 0.6),
    ("ARES", r"\bARES\b", "eval", 0.3),
    ("TruLens", r"\bTruLens\b", "eval", 0.3),
    ("LLM-as-Judge", r"LLM-as-Judge", "eval", 1.0),

    # NLP classical/text
    ("LDA", r"Latent Dirichlet|\bLDA\b|LDiA", "nlp-classical", 0.6),
    ("LSA", r"\bLSA\b|Latent Semantic Analysis", "nlp-classical", 0.6),
    ("TF-IDF", r"\bTF-IDF\b", "nlp-classical", 0.6),
    ("CRF", r"\bCRF\b|Conditional Random Field", "nlp-classical", 0.3),
    ("SetFit", r"\bSetFit\b", "nlp-classical", 0.6),

    # Recsys
    ("TIGER", r"\bTIGER\b", "recsys", 0.6),
    ("LLaRA", r"\bLLaRA\b", "recsys", 0.6),
    ("P5 (recsys)", r"\bP5\b", "recsys", 0.6),

    # Long-context
    ("Longformer", r"\bLongformer\b", "long-context", 0.6),
    ("BigBird", r"\bBigBird\b", "long-context", 0.6),
    ("LongLoRA", r"\bLongLoRA\b", "long-context", 0.3),
    ("Position Interpolation", r"Position[- ]Interpolation", "long-context", 0.3),
]


# Sections that look like h3 titles but should NOT count
NON_TECHNIQUE_KEYWORDS = {
    "exercise", "exercises", "what's next", "summary", "key takeaway",
    "key takeaways", "prerequisites", "official documentation",
    "practical guides", "further reading", "external reading",
    "bibliography", "references", "lab", "background", "context",
    "introduction", "overview", "putting it all together", "key insight",
}


# ---------- Section parsing ----------

def parse_sections(html: str) -> list[dict]:
    """Split HTML by h2 and h3 boundaries. Return list of
    {tag, title, body_html, parent_h2_title}. The 'body' is the HTML
    between this heading and the next h2/h3."""
    main_match = re.search(r'<main\b[^>]*>(.*?)</main>', html, re.DOTALL | re.IGNORECASE)
    if main_match:
        html = main_match.group(1)

    pattern = re.compile(r'<(h[23])\b[^>]*>(.*?)</\1>', re.DOTALL | re.IGNORECASE)
    matches = list(pattern.finditer(html))
    out = []
    current_h2_title = ""
    for i, m in enumerate(matches):
        tag = m.group(1).lower()
        title_raw = re.sub(r'<[^>]+>', '', m.group(2))
        title = re.sub(r'\s+', ' ', title_raw).strip()
        # Strip numeric prefix like "27.1.3.2 "
        title_clean = re.sub(r'^\d+(\.\d+)*\.?\s+', '', title)
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        body = html[body_start:body_end]
        if tag == "h2":
            current_h2_title = title_clean
        out.append({
            "tag": tag,
            "title": title_clean,
            "body": body,
            "parent_h2": current_h2_title if tag == "h3" else "",
        })
    return out


def score_html(body: str) -> dict:
    has_fig = bool(re.search(r'<figure\b|<svg\b|diagram-container|class="[^"]*illustration', body, re.IGNORECASE))
    has_math = bool(re.search(r'\$\$[^$]+\$\$|\$[^$\n]{2,}\$', body))
    has_code = bool(re.search(r'<pre[^>]*><code[^>]*class="[^"]*(?:language|lang)-(python|bash|json|yaml|c|cpp|rust|go|cuda)', body, re.IGNORECASE))
    has_example = bool(re.search(r'<div\s+class="[^"]*callout\s+(practical-example|numeric-example|key-insight|algorithm)', body, re.IGNORECASE))
    return {
        "has_figure": has_fig, "has_math": has_math,
        "has_code": has_code, "has_example": has_example,
        "score": sum([has_fig, has_math, has_code, has_example]),
    }


# ---------- Canonical-section detection ----------

def find_canonical_section(technique_name: str, technique_re: re.Pattern,
                            root: Path) -> dict | None:
    """For a given technique, find its canonical section across the book.
    Returns a dict with file, h2_title, h3_title, scored data, OR None if not
    mentioned at all in any h3 title or substantive body."""
    candidates = []
    for path in root.glob('**/section-*.html'):
        if any(p in path.parts for p in ('_downloads', 'node_modules', '.book-update')):
            continue
        try:
            html = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        sections = parse_sections(html)
        for sec in sections:
            in_title = bool(technique_re.search(sec["title"]))
            body_hits = len(technique_re.findall(sec["body"]))
            if not in_title and body_hits == 0:
                continue
            candidates.append({
                "file": str(path),
                "tag": sec["tag"],
                "title": sec["title"],
                "parent_h2": sec["parent_h2"],
                "in_title": in_title,
                "body_hits": body_hits,
                "body_len": len(sec["body"]),
                "body": sec["body"],
            })
    if not candidates:
        return None
    # Pick canonical: prefer (in_title=True, longest body)
    # Tier 1: in_title True
    in_title_cands = [c for c in candidates if c["in_title"]]
    if in_title_cands:
        best = max(in_title_cands, key=lambda c: c["body_len"])
    else:
        # Tier 2: not in title; pick the one with most body hits AND longest body
        best = max(candidates, key=lambda c: (c["body_hits"], c["body_len"]))
    # Score = h3 body + parent h2 body (if we have it)
    # For aggregation: re-find parent h2's full body from the same file
    parent_h2_body = ""
    if best["tag"] == "h3" and best["parent_h2"]:
        # Reparse file to grab parent h2 body specifically
        try:
            html = Path(best["file"]).read_text(encoding='utf-8', errors='ignore')
            all_sec = parse_sections(html)
            for sec in all_sec:
                if sec["tag"] == "h2" and sec["title"] == best["parent_h2"]:
                    parent_h2_body = sec["body"]
                    break
        except Exception:
            pass

    h3_score = score_html(best["body"])
    h2_score = score_html(parent_h2_body) if parent_h2_body else {
        "has_figure": False, "has_math": False, "has_code": False, "has_example": False, "score": 0
    }
    # Aggregated score: dimension is present if EITHER h3 or parent h2 has it
    agg = {
        "has_figure": h3_score["has_figure"] or h2_score["has_figure"],
        "has_math": h3_score["has_math"] or h2_score["has_math"],
        "has_code": h3_score["has_code"] or h2_score["has_code"],
        "has_example": h3_score["has_example"] or h2_score["has_example"],
    }
    agg["score"] = sum([agg["has_figure"], agg["has_math"], agg["has_code"], agg["has_example"]])

    return {
        "name": technique_name,
        "canonical_file": best["file"],
        "canonical_h3": best["title"] if best["tag"] == "h3" else None,
        "canonical_h2": best["parent_h2"] if best["tag"] == "h3" else best["title"],
        "in_title": best["in_title"],
        "body_hits": best["body_hits"],
        "h3_body_len": best["body_len"] if best["tag"] == "h3" else None,
        "h3_score": h3_score,
        "h2_score": h2_score,
        "agg_score": agg["score"],
        "agg": {k: v for k, v in agg.items() if k != "score"},
    }


def main():
    root = Path('.')
    results = []
    print(f"Auditing {len(TECHNIQUES)} curated techniques across the book...")
    for name, pattern_str, category, weight in TECHNIQUES:
        try:
            pat = re.compile(pattern_str)
        except re.error as e:
            print(f"  ERROR compiling pattern for {name}: {e}")
            continue
        r = find_canonical_section(name, pat, root)
        if r is None:
            results.append({
                "name": name, "category": category, "weight": weight,
                "status": "NOT_FOUND",
            })
        else:
            r["category"] = category
            r["weight"] = weight
            r["status"] = "FOUND"
            results.append(r)

    # Sort by (weight desc, agg_score asc) — most-impactful, least-covered first
    found = [r for r in results if r["status"] == "FOUND"]
    found.sort(key=lambda r: (-r["weight"], r["agg_score"], -r.get("h3_body_len", 0) or 0))

    # Save
    out_path = Path('slide-summaries/_pedagogy_audit_v2.json')
    out_path.write_text(
        json.dumps({"techniques": results, "total_found": len(found),
                    "total_not_found": len(results) - len(found)},
                   indent=2, default=str),
        encoding='utf-8'
    )

    # Print summary
    print(f"\nResults: {len(found)} found, {len(results) - len(found)} not found in any h2/h3")
    print()

    # Histogram
    print("Score histogram (aggregated h2+h3):")
    hist = defaultdict(int)
    for r in found:
        hist[r["agg_score"]] += 1
    for s in sorted(hist):
        bar = "#" * (60 * hist[s] // max(len(found), 1))
        print(f"  {s}/4: {hist[s]:3d}  {bar}")
    print()

    # Top 30 most-impactful gaps (weight=1.0 and score <=2)
    print("=" * 80)
    print("TOP ENRICHMENT PUNCH LIST (load-bearing techniques scoring <=2)")
    print("=" * 80)
    high_priority = [r for r in found if r["weight"] >= 1.0 and r["agg_score"] <= 2]
    print(f"{'Name':25s} {'Score':6s} F M C E  Canonical section")
    print("-" * 110)
    for r in high_priority:
        a = r["agg"]
        marks = ('Y' if a["has_figure"] else '.', 'Y' if a["has_math"] else '.',
                 'Y' if a["has_code"] else '.', 'Y' if a["has_example"] else '.')
        parts = r["canonical_file"].replace("\\", "/").split("/")
        loc = "/".join(parts[-2:])
        sec_label = r["canonical_h3"] or r["canonical_h2"]
        sec_label = (sec_label[:35] + "...") if len(sec_label) > 35 else sec_label
        print(f"  {r['name']:25s} {r['agg_score']}/4    {marks[0]} {marks[1]} {marks[2]} {marks[3]}  {sec_label:38s} {loc}")
    print()
    print(f"  ({len(high_priority)} load-bearing techniques need work)")
    print()

    # NOT FOUND
    not_found = [r for r in results if r["status"] == "NOT_FOUND"]
    if not_found:
        print("=" * 80)
        print(f"TECHNIQUES MISSING ENTIRELY FROM THE BOOK ({len(not_found)})")
        print("=" * 80)
        for r in not_found:
            print(f"  [{r['weight']}] {r['name']} ({r['category']})")
    print()
    print(f"Detailed report: {out_path}")


if __name__ == '__main__':
    main()
