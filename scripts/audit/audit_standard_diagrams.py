#!/usr/bin/env python3
"""Audit inline SVG diagrams for standard/canonical ML diagrams.

Scans all .html files under part-*/ and appendices/ (skipping _archive),
finds inline <svg> elements, classifies each as "standard" (commonly
reproduced from published papers/textbooks) or "custom" (original to
this book), and reports candidates for replacement with canonical images.
"""

import re
from pathlib import Path

BOOK_ROOT = Path(r"E:/Projects/LLMCourse")

# ---------------------------------------------------------------------------
# Standard diagram patterns: (regex_pattern, human_label, likely_source)
# ---------------------------------------------------------------------------
STANDARD_PATTERNS = [
    # Transformer architecture
    (r"transformer\s+architecture|full\s+transformer|encoder.decoder\s+transformer",
     "Transformer architecture",
     'Vaswani et al. 2017, "Attention Is All You Need"'),
    (r"high.level\s+(?:architecture|view).*(?:encoder.decoder|transformer)",
     "Transformer high-level architecture",
     'Vaswani et al. 2017, "Attention Is All You Need"'),

    # Attention mechanisms
    (r"self.attention\s+mechanism|scaled\s+dot.product\s+attention",
     "Scaled dot-product attention",
     'Vaswani et al. 2017, "Attention Is All You Need"'),
    (r"multi.head\s+attention",
     "Multi-head attention",
     'Vaswani et al. 2017, "Attention Is All You Need"'),
    (r"(?:bahdanau|additive)\s+attention|encoder.decoder\s+(?:with\s+)?attention",
     "Encoder-decoder with attention",
     'Bahdanau et al. 2014, "Neural Machine Translation by Jointly Learning to Align and Translate"'),
    (r"cross.attention",
     "Cross-attention mechanism",
     'Vaswani et al. 2017, "Attention Is All You Need"'),

    # BERT / GPT
    (r"bert\s+(?:pre.?training|architecture|model)",
     "BERT pre-training",
     'Devlin et al. 2018, "BERT: Pre-training of Deep Bidirectional Transformers"'),
    (r"masked\s+language\s+model",
     "Masked language modeling (MLM)",
     'Devlin et al. 2018, "BERT"'),
    (r"gpt\s+architecture|decoder.only\s+transformer",
     "GPT / decoder-only transformer",
     'Radford et al. 2018, "Improving Language Understanding by Generative Pre-Training"'),
    (r"three\s+transformer\s+famil|encoder.only.*decoder.only.*encoder.decoder|transformer\s+(?:family|families|variants)",
     "Three transformer families comparison",
     "Standard textbook comparison (encoder-only, decoder-only, encoder-decoder)"),

    # Word embeddings
    (r"word2vec|skip.?gram|cbow|continuous\s+bag",
     "Word2Vec / Skip-gram / CBOW",
     'Mikolov et al. 2013, "Efficient Estimation of Word Representations in Vector Space"'),
    (r"embedding\s+space|vector\s+similar|word\s+embedding\s+space",
     "Embedding space visualization",
     "Standard textbook diagram"),

    # RNN / LSTM / GRU
    (r"(?:unrolled\s+)?rnn|recurrent\s+neural\s+network",
     "RNN architecture",
     "Standard textbook (Goodfellow et al., Deep Learning)"),
    (r"lstm\s+(?:cell|gate|architecture|unit)",
     "LSTM cell",
     'Hochreiter & Schmidhuber 1997, "Long Short-Term Memory"'),
    (r"gru\s+(?:cell|gate|architecture|unit)",
     "GRU cell",
     'Cho et al. 2014, "Learning Phrase Representations using RNN Encoder-Decoder"'),
    (r"backpropagation\s+through\s+time|bptt",
     "Backpropagation through time",
     "Standard textbook (Goodfellow et al., Deep Learning)"),
    (r"vanishing\s+gradient",
     "Vanishing gradient problem",
     "Standard textbook (Goodfellow et al., Deep Learning)"),

    # Decoding
    (r"beam\s+search",
     "Beam search",
     "Standard textbook diagram"),
    (r"decoding\s+strateg|greedy.*(?:beam|sampling)|sampling\s+strateg",
     "Decoding strategies comparison",
     "Standard textbook diagram"),

    # Tokenization
    (r"(?:byte.pair|bpe)\s+(?:encoding|tokeniz|algorithm|merge)",
     "BPE tokenization",
     'Sennrich et al. 2016, "Neural Machine Translation of Rare Words with Subword Units"'),
    (r"subword\s+(?:tokeniz|segment|pipeline)",
     "Subword tokenization pipeline",
     "Standard NLP textbook diagram"),
    (r"tokeniz(?:ation|er)\s+pipeline",
     "Tokenization pipeline",
     "Standard NLP textbook diagram"),

    # Positional encoding
    (r"positional\s+encoding|sinusoidal\s+(?:encoding|position)",
     "Positional encoding",
     'Vaswani et al. 2017, "Attention Is All You Need"'),

    # KV cache / inference
    (r"kv\s+cache|key.value\s+cache",
     "KV cache",
     "Standard inference optimization diagram"),
    (r"(?:flash|memory)\s+(?:attention|hierarchy)",
     "Flash Attention / memory hierarchy",
     'Dao et al. 2022, "FlashAttention"'),

    # LoRA / PEFT
    (r"lora\s+(?:architecture|adapter|decomposition|diagram|inject)",
     "LoRA architecture",
     'Hu et al. 2021, "LoRA: Low-Rank Adaptation of Large Language Models"'),
    (r"adapter\s+(?:architecture|layer|module|inject)",
     "Adapter architecture",
     'Houlsby et al. 2019, "Parameter-Efficient Transfer Learning for NLP"'),

    # RAG
    (r"rag\s+pipeline|retrieval.augmented\s+generation",
     "RAG pipeline",
     'Lewis et al. 2020, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"'),

    # RLHF / alignment
    (r"rlhf\s+pipeline|rlhf\s+(?:training|process|overview)",
     "RLHF pipeline",
     'Ouyang et al. 2022, "Training language models to follow instructions with human feedback"'),
    (r"reward\s+model\s+(?:training|architecture|pipeline)",
     "Reward model training",
     'Ouyang et al. 2022, "Training language models to follow instructions"'),
    (r"dpo\s+(?:vs|pipeline|training|overview)",
     "DPO training",
     'Rafailov et al. 2023, "Direct Preference Optimization"'),
    (r"ppo\s+(?:training|loop|pipeline)",
     "PPO training loop",
     'Schulman et al. 2017, "Proximal Policy Optimization Algorithms"'),

    # MoE
    (r"mixture\s+of\s+experts|moe\s+(?:routing|layer|architecture|gating)",
     "Mixture of Experts",
     'Shazeer et al. 2017, "Outrageously Large Neural Networks"'),

    # Diffusion
    (r"diffusion\s+(?:model|process)|denoising\s+(?:process|step)",
     "Diffusion model",
     'Ho et al. 2020, "Denoising Diffusion Probabilistic Models"'),

    # Classic ML diagrams
    (r"confusion\s+matrix",
     "Confusion matrix",
     "Standard ML textbook"),
    (r"roc\s+curve|receiver\s+operating",
     "ROC curve",
     "Standard ML textbook"),
    (r"precision.recall\s+(?:curve|tradeoff)",
     "Precision-recall curve",
     "Standard ML textbook"),
    (r"neural\s+network\s+(?:architecture|diagram|layer)|(?:feedforward|feed.forward)\s+network|perceptron",
     "Neural network / feedforward / perceptron",
     "Standard textbook (Goodfellow et al., Deep Learning)"),
    (r"gradient\s+descent|loss\s+landscape|optimization\s+landscape",
     "Gradient descent / loss landscape",
     "Standard textbook (Goodfellow et al., Deep Learning)"),
    (r"dropout\s+(?:diagram|regulariz|illustration)",
     "Dropout regularization",
     'Srivastava et al. 2014, "Dropout: A Simple Way to Prevent Neural Networks from Overfitting"'),
    (r"batch\s+normali[sz]ation|layer\s+normali[sz]ation",
     "Batch/Layer normalization",
     "Standard textbook diagram"),
    (r"(?:residual|skip)\s+connection",
     "Residual / skip connection",
     'He et al. 2016, "Deep Residual Learning for Image Recognition"'),

    # Scaling laws
    (r"scaling\s+law|chinchilla\s+(?:curve|scaling|optimal)",
     "Scaling laws",
     'Kaplan et al. 2020 / Hoffmann et al. 2022, "Training Compute-Optimal Large Language Models"'),

    # Knowledge distillation
    (r"(?:knowledge\s+)?distillation\s+(?:pipeline|diagram|architecture|process)",
     "Knowledge distillation",
     'Hinton et al. 2015, "Distilling the Knowledge in a Neural Network"'),
    (r"teacher.student",
     "Teacher-student distillation",
     'Hinton et al. 2015, "Distilling the Knowledge in a Neural Network"'),

    # Quantization
    (r"quantiz(?:ation|ed)\s+(?:pipeline|process|comparison|diagram)",
     "Quantization pipeline",
     "Standard inference optimization diagram"),

    # Speculative decoding
    (r"speculative\s+decoding",
     "Speculative decoding",
     'Leviathan et al. 2023, "Fast Inference from Transformers via Speculative Decoding"'),
]


def find_html_files():
    """Return all .html files under part-*/ and appendices/, skipping _archive."""
    files = []
    for pattern in ["part-*/**/*.html", "appendices/**/*.html"]:
        for f in BOOK_ROOT.glob(pattern):
            if "_archive" not in str(f):
                files.append(f)
    return sorted(files)


def extract_svgs(filepath):
    """Extract all inline <svg> elements with metadata from an HTML file."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")

    results = []
    # Find each <svg ...> tag
    for match in re.finditer(r"<svg\b[^>]*>", text, re.IGNORECASE):
        start_pos = match.start()
        # Compute line number
        line_num = text[:start_pos].count("\n") + 1

        tag = match.group(0)

        # Extract aria-label
        aria_match = re.search(r'aria-label="([^"]*)"', tag)
        aria_label = aria_match.group(1) if aria_match else ""

        # Extract role
        role_match = re.search(r'role="([^"]*)"', tag)
        role = role_match.group(1) if role_match else ""

        # Find nearest caption: look for <figcaption> or <div class="diagram-caption">
        # within ~100 lines after the SVG start
        caption = ""
        search_start = max(0, line_num - 1)
        search_end = min(len(lines), line_num + 150)
        chunk = "\n".join(lines[search_start:search_end])

        # Try figcaption first
        cap_match = re.search(
            r"<figcaption[^>]*>(.*?)</figcaption>", chunk, re.DOTALL
        )
        if not cap_match:
            cap_match = re.search(
                r'<div\s+class="diagram-caption"[^>]*>(.*?)</div>', chunk, re.DOTALL
            )
        if cap_match:
            caption = re.sub(r"<[^>]+>", "", cap_match.group(1)).strip()
            caption = re.sub(r"\s+", " ", caption)

        results.append({
            "file": str(filepath.relative_to(BOOK_ROOT)),
            "line": line_num,
            "aria_label": aria_label,
            "role": role,
            "caption": caption,
        })

    return results


def classify_svg(svg_info):
    """Classify an SVG as standard or custom based on caption and aria-label."""
    text_to_check = (
        svg_info["aria_label"] + " " + svg_info["caption"]
    ).lower()

    for pattern, label, source in STANDARD_PATTERNS:
        if re.search(pattern, text_to_check, re.IGNORECASE):
            return "standard", label, source

    return "custom", None, None


def main():
    html_files = find_html_files()
    print(f"Scanning {len(html_files)} HTML files...\n")

    all_svgs = []
    for f in html_files:
        svgs = extract_svgs(f)
        all_svgs.extend(svgs)

    print(f"Found {len(all_svgs)} inline SVG diagrams total.\n")

    standard_diagrams = []
    custom_diagrams = []

    for svg in all_svgs:
        kind, label, source = classify_svg(svg)
        if kind == "standard":
            standard_diagrams.append((svg, label, source))
        else:
            custom_diagrams.append(svg)

    # -----------------------------------------------------------------------
    # Report: STANDARD diagrams
    # -----------------------------------------------------------------------
    print("=" * 90)
    print(f"  STANDARD DIAGRAMS (candidates for canonical replacement): {len(standard_diagrams)}")
    print("=" * 90)
    for i, (svg, label, source) in enumerate(standard_diagrams, 1):
        cap_display = svg["caption"][:100] + "..." if len(svg["caption"]) > 100 else svg["caption"]
        print(f"\n  [{i}] {label}")
        print(f"      File:    {svg['file']}  (line {svg['line']})")
        if svg["aria_label"]:
            print(f"      Aria:    {svg['aria_label']}")
        print(f"      Caption: {cap_display}")
        print(f"      Source:  {source}")

    # -----------------------------------------------------------------------
    # Report: CUSTOM diagrams
    # -----------------------------------------------------------------------
    print("\n")
    print("=" * 90)
    print(f"  CUSTOM DIAGRAMS (original to this book): {len(custom_diagrams)}")
    print("=" * 90)
    for i, svg in enumerate(custom_diagrams, 1):
        cap_display = svg["caption"][:110] + "..." if len(svg["caption"]) > 110 else svg["caption"]
        aria_display = svg["aria_label"][:80] if svg["aria_label"] else "(none)"
        print(f"\n  [{i}] {svg['file']}  (line {svg['line']})")
        print(f"      Aria:    {aria_display}")
        print(f"      Caption: {cap_display}")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("\n")
    print("=" * 90)
    print("  SUMMARY")
    print("=" * 90)
    print(f"  Total inline SVGs:     {len(all_svgs)}")
    print(f"  Standard (canonical):  {len(standard_diagrams)}")
    print(f"  Custom (original):     {len(custom_diagrams)}")
    if standard_diagrams:
        # Group by source
        by_source = {}
        for svg, label, source in standard_diagrams:
            by_source.setdefault(source, []).append(label)
        print(f"\n  Standard diagrams by source:")
        for source, labels in sorted(by_source.items(), key=lambda x: -len(x[1])):
            unique_labels = sorted(set(labels))
            print(f"    [{len(labels)}] {source}")
            for lbl in unique_labels:
                count = labels.count(lbl)
                suffix = f" (x{count})" if count > 1 else ""
                print(f"         - {lbl}{suffix}")


if __name__ == "__main__":
    main()
