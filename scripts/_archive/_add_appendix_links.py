"""
Sweep all appendix HTML files and add hyperlinks to external products,
libraries, datasets, and benchmarks. Links only the FIRST unlinked mention
per file, uses target="_blank", and skips text already inside <a> tags or
<code>/<pre> blocks.
"""

import re, glob, os

# ── link map ────────────────────────────────────────────────────────────
LINKS = [
    # Libraries / Frameworks  (order matters: longer / more-specific first)
    ("Hugging Face Transformers", "https://huggingface.co/docs/transformers"),
    ("Hugging Face", "https://huggingface.co/"),
    ("Weights & Biases", "https://wandb.ai/"),
    ("Weights &amp; Biases", "https://wandb.ai/"),
    ("scikit-learn", "https://scikit-learn.org/"),
    ("TensorFlow", "https://www.tensorflow.org/"),
    ("PyTorch", "https://pytorch.org/"),
    ("LangChain", "https://python.langchain.com/"),
    ("LlamaIndex", "https://docs.llamaindex.ai/"),
    ("DeepSpeed", "https://www.deepspeed.ai/"),
    ("llama.cpp", "https://github.com/ggml-org/llama.cpp"),
    ("ChromaDB", "https://docs.trychroma.com/"),
    ("Chroma", "https://docs.trychroma.com/"),
    ("Pinecone", "https://www.pinecone.io/"),
    ("Weaviate", "https://weaviate.io/"),
    ("Ollama", "https://ollama.com/"),
    ("MLflow", "https://mlflow.org/"),
    ("NumPy", "https://numpy.org/"),
    ("pandas", "https://pandas.pydata.org/"),
    ("spaCy", "https://spacy.io/"),
    ("NLTK", "https://www.nltk.org/"),
    ("FAISS", "https://github.com/facebookresearch/faiss"),
    ("vLLM", "https://docs.vllm.ai/"),
    ("OpenAI API", "https://platform.openai.com/"),
    ("OpenAI", "https://platform.openai.com/"),
    ("Anthropic API", "https://docs.anthropic.com/"),
    ("Anthropic", "https://docs.anthropic.com/"),
    ("Google AI", "https://ai.google.dev/"),

    # Datasets / Benchmarks
    ("SuperGLUE", "https://gluebenchmark.com/"),
    ("GLUE", "https://gluebenchmark.com/"),
    ("MMLU", "https://github.com/hendrycks/test"),
    ("HellaSwag", "https://rowanzellers.com/hellaswag/"),
    ("HumanEval", "https://github.com/openai/human-eval"),
    ("SQuAD", "https://rajpurkar.github.io/SQuAD-explorer/"),
    ("Common Crawl", "https://commoncrawl.org/"),
    ("The Pile", "https://pile.eleuther.ai/"),
    ("RedPajama", "https://github.com/togethercomputer/RedPajama-Data"),
    ("LMSYS Chatbot Arena", "https://chat.lmsys.org/"),
    ("Chatbot Arena", "https://chat.lmsys.org/"),

    # Cloud / Hardware
    ("Lambda Labs", "https://lambdalabs.com/"),
    ("RunPod", "https://www.runpod.io/"),
    ("Google Cloud", "https://cloud.google.com/"),
    ("Azure", "https://azure.microsoft.com/"),
    ("AWS", "https://aws.amazon.com/"),
    ("NVIDIA", "https://www.nvidia.com/"),
]


def is_inside_tag(html, match_start, match_end):
    """Return True if the match sits inside an <a …>…</a>, <code>, or <pre> block."""
    # Check if inside an <a> tag
    # Walk backwards to find the nearest unmatched <a or </a>
    before = html[:match_start]

    # Check for <a> context
    last_a_open = before.rfind("<a ")
    if last_a_open == -1:
        last_a_open = before.rfind("<a\t")
    if last_a_open == -1:
        last_a_open = before.rfind("<a\n")
    last_a_close = before.rfind("</a>")
    if last_a_open > last_a_close:
        return True   # we're inside an <a> tag

    # Check for <code> context
    last_code_open = before.rfind("<code")
    last_code_close = before.rfind("</code>")
    if last_code_open > last_code_close:
        return True

    # Check for <pre> context
    last_pre_open = before.rfind("<pre")
    last_pre_close = before.rfind("</pre>")
    if last_pre_open > last_pre_close:
        return True

    # Check if inside an HTML tag attribute (e.g., alt="..PyTorch..")
    # Find nearest '<' that isn't closed by '>'
    last_lt = before.rfind("<")
    last_gt = before.rfind(">")
    if last_lt > last_gt:
        return True  # inside an HTML tag

    return False


def add_links_to_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    original = html
    linked_keys = set()   # track which keys have been linked in this file

    for name, url in LINKS:
        if name in linked_keys:
            continue

        # Build a pattern that matches the name as a whole word,
        # but NOT when it's already the text of a link.
        # Use word boundaries; for names starting/ending with special chars, be flexible.
        escaped = re.escape(name)
        pattern = re.compile(r'(?<!["\w/\-])' + escaped + r'(?!["\w/\-])', re.IGNORECASE if name.isupper() or name == "pandas" else 0)

        for m in pattern.finditer(html):
            start, end = m.start(), m.end()
            if is_inside_tag(html, start, end):
                continue
            # Make the replacement
            matched_text = m.group()
            replacement = f'<a href="{url}" target="_blank">{matched_text}</a>'
            html = html[:start] + replacement + html[end:]
            linked_keys.add(name)
            # Also mark sub-keys as linked so we don't double-link
            # e.g., if we linked "Hugging Face Transformers", skip "Hugging Face"
            for other_name, _ in LINKS:
                if other_name != name and other_name in name:
                    linked_keys.add(other_name)
            break  # only first occurrence

    if html != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False


def main():
    base = r"E:\Projects\LLMCourse\appendices"
    files = sorted(glob.glob(os.path.join(base, "**", "*.html"), recursive=True))
    print(f"Found {len(files)} HTML files in appendices/")

    changed = 0
    for fp in files:
        rel = os.path.relpath(fp, base)
        modified = add_links_to_file(fp)
        if modified:
            changed += 1
            print(f"  LINKED: {rel}")
        else:
            print(f"  (skip): {rel}")

    print(f"\nDone. Modified {changed} of {len(files)} files.")


if __name__ == "__main__":
    main()
