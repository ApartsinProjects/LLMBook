"""Fix all 'Chapter opener illustration for...' captions in HTML files."""
import re
import os
import glob

BASE = r"E:\Projects\LLMCourse"

# Map of path fragment -> new caption
REPLACEMENTS = {
    "appendix-a-mathematical-foundations": "The equations behind the magic: where vectors, gradients, and probability distributions quietly run the show.",
    "appendix-b-ml-essentials": "A quick refresher on the building blocks that make everything else in this book possible.",
    "appendix-c-python-for-llm": "Your Swiss Army knife for the LLM era: Python, configured and ready to build.",
    "appendix-d-environment-setup": "Getting your workstation ready is half the battle; the other half is remembering which CUDA version you installed.",
    "appendix-e-git-collaboration": "Version control: because 'final_model_v3_REAL_final.pt' is not a naming convention.",
    "appendix-f-glossary": "Every field has its jargon; here is your decoder ring.",
    "appendix-g-hardware-compute": "The silicon that powers the intelligence: GPUs, TPUs, and the electricity bills that come with them.",
    "appendix-h-model-cards": "A field guide to the models you will meet on your journey.",
    "appendix-i-prompt-templates": "Copy, paste, customize: prompt patterns that work out of the box.",
    "appendix-j-datasets-benchmarks": "The training grounds and scoreboards that shape modern AI.",
    "module-00-ml-pytorch-foundations": "From tensors to training loops: the foundation every AI practitioner needs.",
    "module-02-tokenization-subword-models": "The art of slicing text into just the right pieces.",
    "module-03-sequence-models-attention": "Teaching machines to remember what came before, one hidden state at a time.",
    "module-04-transformer-architecture": "The architecture that changed everything: attention, parallelism, and a lot of matrix multiplications.",
    "module-05-decoding-text-generation": "Choosing the next word is harder than it sounds; here is how models make that choice.",
    "module-06-pretraining-scaling-laws": "Scaling up: more data, more compute, more emergent abilities.",
    "module-07-modern-llm-landscape": "A tour of the models that define the current era.",
}

# Pattern to match the full figcaption containing "Chapter opener illustration"
PATTERN = re.compile(
    r'(<figcaption[^>]*>)\s*Chapter opener illustration for[^<]*(<\/figcaption>)',
    re.IGNORECASE
)

fixed = 0
not_matched = []

for html_path in glob.glob(os.path.join(BASE, "**", "*.html"), recursive=True):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "Chapter opener illustration" not in content:
        continue

    # Determine which replacement to use
    rel = os.path.relpath(html_path, BASE).replace("\\", "/")
    new_caption = None
    for key, caption in REPLACEMENTS.items():
        if key in rel:
            new_caption = caption
            break

    if new_caption is None:
        not_matched.append(rel)
        continue

    new_content = PATTERN.sub(
        lambda m: f'{m.group(1)}{new_caption}{m.group(2)}',
        content
    )

    if new_content != content:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        fixed += 1
        print(f"FIXED: {rel}")
    else:
        print(f"NO MATCH (regex): {rel}")

print(f"\nTotal fixed: {fixed}")
if not_matched:
    print(f"Files with no replacement mapping: {not_matched}")
