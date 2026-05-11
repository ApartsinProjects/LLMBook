"""v6.8: Fill the 13 remaining orphan code captions that the prior
JSON batches missed due to case-variant cap numbers (b.4.1, c.1.5,
j.1.1, etc.) or because they weren't in the initial audit window.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def anchor(cap_num: str) -> str:
    return f'<div class="code-caption"><strong>Code Fragment {cap_num}:</strong>'


def cb(lang: str, body: str) -> str:
    return (
        '<div class="code-block-wrapper">\n'
        f'<pre><code class="lang-{lang}">{body}</code></pre>\n'
        '</div>\n'
    )


BLOCKS = [
    # b.4.1 — BLEU + ROUGE with HF evaluate
    ('appendices/appendix-b-ml-essentials/section-b.4.html', 'b.4.1', cb('python', '''# BLEU + ROUGE with Hugging Face evaluate library.
# BLEU measures n-gram precision (good for MT); ROUGE measures n-gram recall (good for summarization).
import evaluate

bleu = evaluate.load("bleu")
rouge = evaluate.load("rouge")

predictions = ["the cat sat on the mat",
               "transformers use self-attention"]
references  = [["a cat is sitting on the mat"],
               ["transformers rely on self-attention"]]

bleu_result  = bleu.compute(predictions=predictions, references=references)
rouge_result = rouge.compute(predictions=predictions,
                              references=[r[0] for r in references])

print(f"BLEU-4   : {bleu_result['bleu']:.3f}")
print(f"ROUGE-1  : {rouge_result['rouge1']:.3f}")
print(f"ROUGE-L  : {rouge_result['rougeL']:.3f}")''')),

    # c.1.5 — SFTTrainer
    ('appendices/appendix-c-python-for-llm/section-c.1.html', 'c.1.5', cb('python', '''# Supervised fine-tuning with TRL's SFTTrainer.
# Handles chat-template formatting, packing, and the entire training loop.
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "meta-llama/Llama-3.2-1B"
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="bfloat16")
tokenizer = AutoTokenizer.from_pretrained(model_id)

dataset = load_dataset("HuggingFaceH4/ultrachat_200k", split="train_sft[:5000]")

config = SFTConfig(
    output_dir="./sft-llama-3.2-1b",
    max_seq_length=2048,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    num_train_epochs=1,
    bf16=True,
    logging_steps=10,
    save_strategy="epoch",
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    args=config,
    train_dataset=dataset,
    dataset_text_field="messages",  # SFTTrainer reads chat-formatted messages
)
trainer.train()''')),

    # C.2.3 — uv setup
    ('appendices/appendix-c-python-for-llm/section-c.2.html', 'C.2.3', cb('bash', '''# Create a virtual environment with uv (Rust-based, ~10x faster than pip)
# uv resolves and installs hundreds of packages in seconds.
# Install uv itself first:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Then create + activate the venv
uv venv llm-env
source llm-env/bin/activate   # Linux/macOS
# llm-env\\Scripts\\activate    # Windows

# Install dependencies (uv reads pyproject.toml or requirements.txt)
uv pip install torch transformers datasets accelerate''')),

    # D.3.2 — venv + pip + CUDA wheels
    ('appendices/appendix-d-environment-setup/section-d.3.html', 'D.3.2', cb('bash', '''# Standard Python venv + pip path; works on every platform.
# Specify the CUDA wheel index so pip pulls a GPU-enabled PyTorch build.
python -m venv llm-env
source llm-env/bin/activate   # Linux/macOS
# llm-env\\Scripts\\activate    # Windows

# CUDA 12.4 wheels; check pytorch.org for the current command
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Verify
python -c "import torch; print(torch.cuda.is_available(), torch.version.cuda)"''')),

    # E.1.2 — Git LFS
    ('appendices/appendix-e-git-collaboration/section-e.1.html', 'E.1.2', cb('bash', '''# Configure Git LFS to track large model files.
# LFS replaces large binaries with lightweight pointers in your repo and
# stores the actual blobs in remote LFS storage.
git lfs install

# Track common ML weight formats. Edit .gitattributes after running these.
git lfs track "*.safetensors"
git lfs track "*.bin"
git lfs track "*.pt"
git lfs track "*.ckpt"

# Commit the .gitattributes config so collaborators inherit it
git add .gitattributes
git commit -m "Track large model files with Git LFS"

# Normal workflow continues; LFS handles the size-aware upload/download
git add my-finetuned-model/model.safetensors
git commit -m "Add fine-tuned model"
git push''')),

    # E.2.2 — DVC repro
    ('appendices/appendix-e-git-collaboration/section-e.2.html', 'E.2.2', cb('bash', '''# DVC: data + model pipeline versioning.
# `dvc repro` re-runs ONLY the pipeline stages whose dependencies have changed.
# Tags let you bookmark milestones; `dvc exp` runs reproducible experiments.

# Re-execute the pipeline (only stages with stale inputs run)
dvc repro

# Tag a milestone so you can return to it later
git tag v1.0-baseline
dvc push   # upload data + artifacts to the remote DVC storage

# Compare current artifacts vs a tagged baseline
dvc exp diff v1.0-baseline HEAD

# Promote an experiment branch's results back to main
dvc exp apply $(dvc exp show --csv | grep best-loss | cut -d, -f1)''')),

    # j.1.1 — FineWeb-Edu streaming
    ('appendices/appendix-j-datasets-benchmarks/section-j.1.html', 'j.1.1', cb('python', '''# Stream FineWeb-Edu without downloading the full 1.3 trillion token dataset.
# streaming=True yields examples on demand from the Hugging Face Hub.
from datasets import load_dataset

# Loads a streaming iterator; nothing is downloaded yet
ds = load_dataset(
    "HuggingFaceFW/fineweb-edu",
    name="sample-10BT",      # ~10B-token sample; use "default" for the full set
    split="train",
    streaming=True,
)

# Filter to high-educational-quality documents on the fly
high_quality = ds.filter(lambda ex: ex["score"] >= 4)

# Take just the first 1000 for a quick smoke test
for i, example in enumerate(high_quality.take(1000)):
    if i < 3:
        print(f"#{i}  score={example['score']}  url={example['url'][:60]}")
        print(f"   text[:200] = {example['text'][:200]!r}\\n")

# For training, pipe directly into a tokenizer + DataLoader:
# tokenized = high_quality.map(lambda ex: tok(ex['text'], truncation=True, max_length=2048))
# for batch in tokenized.iter(batch_size=8):
#     train_step(batch)''')),

    # j.3.1 — lm-eval-harness CLI
    ('appendices/appendix-j-datasets-benchmarks/section-j.3.html', 'j.3.1', cb('bash', '''# Run lm-evaluation-harness on standard benchmarks.
# The framework downloads the dataset, builds prompts, runs the model,
# and scores responses with the canonical metric per task.

# Install once
pip install lm-eval

# 5-shot MMLU + HellaSwag on a HuggingFace model
lm_eval \\
    --model hf \\
    --model_args pretrained=meta-llama/Llama-3.2-1B,dtype=bfloat16 \\
    --tasks mmlu,hellaswag \\
    --num_fewshot 5 \\
    --batch_size auto \\
    --output_path ./eval_results

# For a hosted API (OpenAI-compatible), use the `openai-completions` backend
lm_eval \\
    --model openai-completions \\
    --model_args model=gpt-4o-mini \\
    --tasks gsm8k_cot \\
    --output_path ./gpt4o_gsm8k''')),

    # 18.1.6 — tokenization pipeline
    ('part-10-frontiers/module-18-interpretability/section-18.1.html', '18.1.6', cb('python', '''# Tokenization pipeline: text -> token IDs -> embeddings.
# The tokenizer adds special tokens (BOS/EOS) and handles padding/truncation.
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "gpt2"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, output_hidden_states=True)
model.eval()

text = "The Eiffel Tower is located in"
encoded = tok(text, return_tensors="pt")
print(f"Tokens : {tok.convert_ids_to_tokens(encoded.input_ids[0])}")
print(f"IDs    : {encoded.input_ids[0].tolist()}")
print(f"Attn   : {encoded.attention_mask[0].tolist()}")

with torch.no_grad():
    out = model(**encoded)
# Last hidden state shape: (batch, seq_len, d_model)
print(f"Hidden : {out.hidden_states[-1].shape}")  # e.g. (1, 7, 768)''')),

    # 6.3.1 — Mixtral 4-bit
    ('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.3.html', '6.3.1', cb('python', '''# Load Mixtral 8x7B with 4-bit quantization (~25 GB vs ~94 GB at FP16).
# device_map="auto" distributes layers across all available GPUs / RAM.
# Requires: pip install transformers accelerate bitsandbytes
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",          # NormalFloat4 (best for LLM weights)
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,     # second-level quant on the constants
)

model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
)

prompt = "Explain mixture-of-experts in two sentences."
inputs = tok(prompt, return_tensors="pt").to(model.device)
output = model.generate(**inputs, max_new_tokens=200, temperature=0.7, do_sample=True)
print(tok.decode(output[0], skip_special_tokens=True))''')),

    # 10.1.7 — LiteLLM unified abstraction
    ('part-3-working-with-llms/module-10-llm-apis/section-10.1.html', '10.1.7', cb('python', '''# LiteLLM: one client interface, every major provider.
# Switch from OpenAI to Anthropic to Llama just by changing the model string.
import litellm

# Same call signature everywhere
def ask(model: str, prompt: str) -> str:
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return response.choices[0].message.content.strip()

# Direct provider calls, all routed by LiteLLM
print(ask("gpt-4o-mini",                                  "What is RAG?"))
print(ask("anthropic/claude-3-5-haiku-20241022",          "What is RAG?"))
print(ask("together_ai/meta-llama/Llama-3.1-8B-Instruct-Turbo", "What is RAG?"))
print(ask("groq/llama-3.1-8b-instant",                    "What is RAG?"))

# Automatic fallbacks: try the cheap model, then escalate on failure
response = litellm.completion(
    model="gpt-4o-mini",
    fallbacks=["anthropic/claude-3-5-haiku-20241022", "groq/llama-3.1-8b-instant"],
    messages=[{"role": "user", "content": "summarize attention"}],
)
print(response.choices[0].message.content)''')),

    # 14.5.2 — sentence-transformers training
    ('part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.5.html', '14.5.2', cb('python', '''# Fine-tune a sentence-transformer to your domain.
# CosineSimilarityLoss pulls similar-pair embeddings together and pushes
# dissimilar-pair embeddings apart.
from sentence_transformers import SentenceTransformer, losses, InputExample
from sentence_transformers.training_args import SentenceTransformerTrainingArguments
from sentence_transformers.trainer import SentenceTransformerTrainer
from torch.utils.data import DataLoader

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Each example: two sentences plus a similarity label in [0, 1]
train_examples = [
    InputExample(texts=["The cat sits on the mat.",
                        "A cat is on the rug."],            label=0.92),
    InputExample(texts=["The cat sits on the mat.",
                        "Stock prices fell sharply today."], label=0.05),
    InputExample(texts=["BERT uses masked language modeling.",
                        "BERT trains by predicting masked tokens."], label=0.95),
]

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
train_loss = losses.CosineSimilarityLoss(model)

args = SentenceTransformerTrainingArguments(
    output_dir="./tuned-embedder",
    num_train_epochs=4,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    warmup_ratio=0.1,
)
trainer = SentenceTransformerTrainer(model=model, args=args,
                                     train_dataset=train_examples, loss=train_loss)
trainer.train()
model.save_pretrained("./tuned-embedder")''')),

    # 20.4.5 — LlamaIndex agentic RAG
    ('part-5-retrieval-conversation/module-20-rag/section-20.4.html', '20.4.5', cb('python', '''# Agentic RAG with LlamaIndex: a router agent picks WHICH index to query.
# Two indices (SEC filings + news) are exposed as tools; the agent decides
# whether each user query needs filings, news, both, or neither.
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

# Build two separate indices over different document sets
sec_index  = VectorStoreIndex.from_documents(SimpleDirectoryReader("./sec_filings").load_data())
news_index = VectorStoreIndex.from_documents(SimpleDirectoryReader("./news").load_data())

# Wrap each as a tool the agent can call
tools = [
    QueryEngineTool(
        query_engine=sec_index.as_query_engine(similarity_top_k=5),
        metadata=ToolMetadata(
            name="sec_filings",
            description="Search SEC 10-K/10-Q filings for financial statements, risks, governance.",
        ),
    ),
    QueryEngineTool(
        query_engine=news_index.as_query_engine(similarity_top_k=5),
        metadata=ToolMetadata(
            name="news",
            description="Search recent news articles for analyst opinions, market events, breaking news.",
        ),
    ),
]

llm = OpenAI(model="gpt-4o-mini", temperature=0.0)
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True)

# Agent decides which tool(s) to call and synthesizes a citation-grounded answer
response = agent.chat("How did NVIDIA's data-center revenue change in Q3, and what do analysts attribute it to?")
print(response)''')),
]


def main() -> int:
    fixed = skipped = 0
    for rel, cap_num, block in BLOCKS:
        p = ROOT / rel
        if not p.exists():
            print(f'  MISSING file: {rel}')
            continue
        text = p.read_text(encoding='utf-8')
        anc = anchor(cap_num)
        if anc not in text:
            print(f'  NO ANCHOR for CF {cap_num} in {rel}')
            continue
        sig = block.split('\n', 2)[1][:50]
        if sig in text:
            print(f'  already inserted: CF {cap_num}')
            skipped += 1
            continue
        new_text = text.replace(anc, block + anc, 1)
        p.write_text(new_text, encoding='utf-8')
        print(f'  + CF {cap_num} in {rel.rsplit("/", 1)[-1]}')
        fixed += 1
    print(f'\nInserted {fixed} blocks; skipped {skipped} already-present.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
