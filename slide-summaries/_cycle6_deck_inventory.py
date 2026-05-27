#!/usr/bin/env python
"""Cycle 6: build inventory of pedagogy assets in slide decks AND target book sections."""
import json
import re
from pathlib import Path

ROOT = Path(r"E:/Projects/BookBlogsHome/LLMBook")
SS = ROOT / "slide-summaries"

# 30 deck targets: (deck_folder, deck_stem, target_section_paths[])
# Skewed toward LLM-core (1300/1320/1400/1420) + 5xxx audio + 0016 PyTorch.
DECKS = [
    # 1300 series
    ("1300_LLM_TransformersInternals", "1301_Attention", ["part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.2.html", "part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.3.html", "part-1-llm-building-blocks/module-02-sequence-models-attention/section-2.4.html"]),
    ("1300_LLM_TransformersInternals", "1302_Transformer", ["part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html", "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.2.html", "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.3.html", "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.4.html"]),
    ("1300_LLM_TransformersInternals", "1304_SentenceEmbedding", ["part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.5.html", "part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.2.html"]),
    ("1300_LLM_TransformersInternals", "1306_FinetuningHumanFeedback", ["part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.1.html", "part-4-training-adaptation/module-18-alignment-rlhf-dpo/section-18.2.html"]),
    ("1300_LLM_TransformersInternals", "1307_TransformerSeq2Seq", ["part-1-llm-building-blocks/module-03-transformer-architecture/section-3.1.html", "part-1-llm-building-blocks/module-03-transformer-architecture/section-3.5.html"]),
    ("1300_LLM_TransformersInternals", "1308_TransfomerMixtureOfExperts", ["part-1-llm-building-blocks/module-03-transformer-architecture/section-3.8.html"]),
    ("1300_LLM_TransformersInternals", "1310_LLM_ExplainingTransformer", ["part-2-understanding-llms/module-10-interpretability/section-10.4.html"]),
    ("1300_LLM_TransformersInternals", "1311_LLM_MultilinguialEncoder", ["part-2-understanding-llms/module-07-modern-llm-landscape/section-7.4.html"]),
    # 1320 series
    ("1320_LLM_TransferLearning", "1321_PEFT", ["part-4-training-adaptation/module-17-peft/section-17.1.html", "part-4-training-adaptation/module-17-peft/section-17.2.html"]),
    ("1320_LLM_TransferLearning", "1322_PromptTuning", ["part-4-training-adaptation/module-17-peft/section-17.4.html"]),
    ("1320_LLM_TransferLearning", "1324_ClassificationFineTuning", ["part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.6.html"]),
    ("1320_LLM_TransferLearning", "1325_AdaptingForLongText", ["part-4-training-adaptation/module-16-fine-tuning-fundamentals/section-16.7.html"]),
    ("1320_LLM_TransferLearning", "1326_LLMDistilation", ["part-4-training-adaptation/module-17-peft/section-17.5.html", "part-4-training-adaptation/module-17-peft/section-17.6.html"]),
    ("1320_LLM_TransferLearning", "1327_LLMMerge", ["part-4-training-adaptation/module-17-peft/section-17.7.html"]),
    # 1400 RAG
    ("1400_LLM_RAG", "1401_VectorStores", ["part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.5.html"]),
    ("1400_LLM_RAG", "1402_RAG_Intro", ["part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.1.html"]),
    ("1400_LLM_RAG", "1403_RAG_Evaluations", ["part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.2.html"]),
    ("1400_LLM_RAG", "1404_AdvancedRAG", ["part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.1.html", "part-7-retrieval-information-extraction-with-llms/module-35-advanced-rag/section-35.2.html"]),
    # 1420 Agents
    ("1420_LLM_Agents", "1421_Tools_FunctionCalls", ["part-6-agentic-ai/module-27-tool-use-protocols/section-27.1.html"]),
    ("1420_LLM_Agents", "1422_Tools_MCP", ["part-6-agentic-ai/module-27-tool-use-protocols/section-27.2.html"]),
    ("1420_LLM_Agents", "1424_LangGraph_Intro", ["part-6-agentic-ai/module-30-tools-of-the-trade/section-30.2.html"]),
    ("1420_LLM_Agents", "1427_Agents_AgenticRAG", ["part-7-retrieval-information-extraction-with-llms/module-32-rag/section-32.3.html"]),
    ("1420_LLM_Agents", "1428_Agents_Planning", ["part-6-agentic-ai/module-26-ai-agents/section-26.2.html"]),
    # 5xxx audio
    ("5012_Audio_Processing", "5012_Audio_Data", ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.1.html"]),
    ("5012_Audio_Processing", "5013_Audio_VectorQuant", ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.2.html"]),
    ("5015_Audio_FM", "5015_PretrainedAudioModels", ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html"]),
    ("5020_Audio_Encoders", "5021_Audio_Encoders", ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.0.4.html"]),
    ("5040_Audio_Speech2Text", "5041_Audio_Speech2Text", ["part-5-multimodal-llms/module-20-audio-music-generation/section-20.5.html"]),
    # PyTorch
    ("0010_Common_MLDL", "0016_PyTorchTutorial", ["appendices/appendix-e-pytorch-reference/index.html"]),
    # Topic Modeling
    ("1410_LLM_TopicModeling", "1411_BERTTopics", ["part-7-retrieval-information-extraction-with-llms/module-31-embeddings-vector-db/section-31.7.html"]),
]


def count_keywords(text, kws):
    t = text.lower()
    return sum(t.count(k.lower()) for k in kws)


def inventory_slide_md(md_path):
    if not md_path.exists():
        return None
    text = md_path.read_text(encoding="utf-8", errors="replace")
    # crude per-slide split
    slides = re.split(r"^## Slide \d+", text, flags=re.M)
    n_slides = len(slides) - 1
    # heuristic counts
    code_hits = count_keywords(text, ["code snippet", "code block", "python code", "snippet", "```", ".py", "import ", "def ", "torch.", "transformers.", "from "])
    formula_hits = count_keywords(text, ["formula", "equation", "= softmax", "log(", "sqrt(", r"\frac", "loss =", "logit", "softmax(", "exp(", "kl(", "softmax", "cross-entropy", "cross entropy"])
    diagram_hits = count_keywords(text, ["diagram", "architecture", "block diagram", "schematic", "illustration", "figure", "pipeline showing", "graph showing", "tree showing"])
    example_hits = count_keywords(text, ["worked example", "numerical example", "example:", "for example", "concretely", "walkthrough", "trace through", "step by step", "step-by-step"])
    techniques = []
    # marquee technique extraction: capitalized multi-word names + acronyms
    for m in re.finditer(r"\b([A-Z][A-Za-z0-9-]+(?:\s+[A-Z][A-Za-z0-9-]+)*)\b", text):
        t = m.group(1).strip()
        if len(t) >= 3 and t not in {"The", "This", "That", "These", "Section", "Slide", "Source", "Drive", "From"}:
            techniques.append(t)
    # keep most frequent unique
    from collections import Counter
    tech_counter = Counter(techniques)
    top_tech = [t for t, _ in tech_counter.most_common(40)]
    return {
        "path": str(md_path),
        "slides": n_slides,
        "chars": len(text),
        "code_hits": code_hits,
        "formula_hits": formula_hits,
        "diagram_hits": diagram_hits,
        "example_hits": example_hits,
        "top_tech": top_tech,
    }


def inventory_book_html(paths):
    total_text = ""
    code_blocks = 0
    figures = 0
    math_blocks = 0
    callouts = 0
    examined = []
    for p in paths:
        ap = ROOT / p
        if not ap.exists():
            continue
        t = ap.read_text(encoding="utf-8", errors="replace")
        total_text += t + "\n"
        examined.append(p)
        # crude counts
        code_blocks += len(re.findall(r"<pre[^>]*>", t)) + len(re.findall(r"<code[^>]*>(?!.{0,200}</code>)", t))
        figures += len(re.findall(r"<figure[^>]*>", t)) + len(re.findall(r"<svg\b", t)) + len(re.findall(r"<img[^>]*>", t))
        math_blocks += len(re.findall(r"\$\$|\\\[|class=\"katex", t)) + len(re.findall(r"<math\b", t))
        callouts += len(re.findall(r"class=\"[^\"]*callout[^\"]*\"", t)) + len(re.findall(r"class=\"[^\"]*example[^\"]*\"", t))
    return {
        "files": examined,
        "chars": len(total_text),
        "code_blocks": code_blocks,
        "figures": figures,
        "math_blocks": math_blocks,
        "callouts": callouts,
        "text": total_text,
    }


def compare(slide_inv, book_inv, deck_id):
    if slide_inv is None:
        return {"deck": deck_id, "verdict": "SLIDE_MD_MISSING"}
    # Use heuristics: book section should have at least 0.5x slide formulas, ~slide code, and figures >= slide diagrams//4
    # but mainly check missing technique names
    book_text = book_inv["text"].lower()
    missing_tech = []
    for tech in slide_inv["top_tech"][:25]:
        # technique-name check: lowercase substring match anywhere in book text
        if len(tech) < 4:
            continue
        if tech.lower() not in book_text:
            missing_tech.append(tech)
    # asset depth
    needs = []
    if slide_inv["formula_hits"] >= 3 and book_inv["math_blocks"] < 1:
        needs.append("math")
    if slide_inv["diagram_hits"] >= 6 and book_inv["figures"] < 2:
        needs.append("figure")
    if slide_inv["code_hits"] >= 8 and book_inv["code_blocks"] < 1:
        needs.append("code")
    if slide_inv["example_hits"] >= 3 and "example" not in book_text:
        needs.append("example")
    verdict = "MATCH_OR_EXCEEDS"
    if missing_tech or needs:
        verdict = "BOOK_SHALLOWER"
    return {
        "deck": deck_id,
        "verdict": verdict,
        "slide_chars": slide_inv["chars"],
        "book_chars": book_inv["chars"],
        "slide_slides": slide_inv["slides"],
        "slide_code_hits": slide_inv["code_hits"],
        "slide_formula_hits": slide_inv["formula_hits"],
        "slide_diagram_hits": slide_inv["diagram_hits"],
        "slide_example_hits": slide_inv["example_hits"],
        "book_code_blocks": book_inv["code_blocks"],
        "book_figures": book_inv["figures"],
        "book_math_blocks": book_inv["math_blocks"],
        "book_callouts": book_inv["callouts"],
        "missing_tech": missing_tech[:15],
        "needs_dimensions": needs,
        "book_files": book_inv["files"],
    }


def main():
    results = []
    for folder, stem, targets in DECKS:
        md = SS / folder / f"{stem}.md"
        slide_inv = inventory_slide_md(md)
        book_inv = inventory_book_html(targets)
        rec = compare(slide_inv, book_inv, f"{folder}/{stem}")
        results.append(rec)
    out = SS / "_cycle6_slide_vs_book.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out}")
    # quick summary
    n_match = sum(1 for r in results if r["verdict"] == "MATCH_OR_EXCEEDS")
    n_shallow = sum(1 for r in results if r["verdict"] == "BOOK_SHALLOWER")
    n_miss = sum(1 for r in results if r["verdict"] == "SLIDE_MD_MISSING")
    print(f"Decks compared: {len(results)} | match/exceed: {n_match} | book shallower: {n_shallow} | missing: {n_miss}")
    for r in results:
        if r["verdict"] == "BOOK_SHALLOWER":
            tags = ",".join(r.get("needs_dimensions", []))
            n_miss = len(r.get("missing_tech", []))
            print(f"  SHALLOW  {r['deck']:60s}  needs=[{tags}]  miss_tech={n_miss}")
        elif r["verdict"] == "MATCH_OR_EXCEEDS":
            print(f"  OK       {r['deck']}")
        else:
            print(f"  SKIP     {r['deck']} ({r['verdict']})")


if __name__ == "__main__":
    main()
