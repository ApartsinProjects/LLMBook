"""Bibliographies for tools-of-the-trade sections.

These sections already have library-shortcut callouts with inline docs links,
but the audit requires a formal Further Reading block. We add documentation
references for the core libraries discussed in each section.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bib_data import BIBLIOGRAPHIES, bib_block

def add(path, sections):
    BIBLIOGRAPHIES[path] = bib_block(sections)


# ============================================================
# Generic templates per section type
# ============================================================

PYTORCH_REFS = [
    'Paszke, A., Gross, S., Massa, F., et al. (2019). "PyTorch: An Imperative Style, High-Performance Deep Learning Library." <em>NeurIPS 2019</em>. <a href="https://arxiv.org/abs/1912.01703" rel="noopener" target="_blank">arXiv:1912.01703</a>. <span class="bib-note">The reference PyTorch paper.</span>',
    'PyTorch (2024). "PyTorch Documentation." <a href="https://pytorch.org/docs/stable/index.html" rel="noopener" target="_blank">pytorch.org/docs/stable</a>. <span class="bib-note">Authoritative reference for tensor operations, autograd, and distributed primitives.</span>',
]

HF_REFS = [
    'Wolf, T., Debut, L., Sanh, V., et al. (2020). "Transformers: State-of-the-Art Natural Language Processing." <em>EMNLP 2020</em>. <a href="https://arxiv.org/abs/1910.03771" rel="noopener" target="_blank">arXiv:1910.03771</a>. <span class="bib-note">The original Hugging Face Transformers paper.</span>',
    'Hugging Face (2024). "Transformers Documentation." <a href="https://huggingface.co/docs/transformers" rel="noopener" target="_blank">huggingface.co/docs/transformers</a>. <span class="bib-note">Authoritative reference for the de-facto LLM library.</span>',
]

VLLM_REFS = [
    'Kwon, W., Li, Z., Zhuang, S., et al. (2023). "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM). <em>SOSP 2023</em>. <a href="https://arxiv.org/abs/2309.06180" rel="noopener" target="_blank">arXiv:2309.06180</a>. <span class="bib-note">The vLLM paper.</span>',
]

# ============================================================
# Module 5: Foundations Tools
# ============================================================
add('part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.2.html', [
    {
        'h3': 'Deep Learning Libraries',
        'h3_id': 'deep-learning',
        'entries': PYTORCH_REFS + [
            'Bradbury, J., Frostig, R., Hawkins, P., et al. (2018). "JAX: composable transformations of Python+NumPy programs." <a href="https://github.com/jax-ml/jax" rel="noopener" target="_blank">github.com/jax-ml/jax</a>. <span class="bib-note">Reference for the JAX deep-learning engine.</span>',
        ],
    },
    {
        'h3': 'Scientific Python',
        'h3_id': 'scientific',
        'entries': [
            'Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). "Array programming with NumPy." <em>Nature 585</em>. <a href="https://www.nature.com/articles/s41586-020-2649-2" rel="noopener" target="_blank">nature.com/articles/s41586-020-2649-2</a>. <span class="bib-note">The reference NumPy paper.</span>',
            'Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). "Scikit-learn: Machine Learning in Python." <em>JMLR 12</em>. <a href="https://www.jmlr.org/papers/v12/pedregosa11a.html" rel="noopener" target="_blank">jmlr.org/papers/v12/pedregosa11a</a>. <span class="bib-note">The reference scikit-learn paper.</span>',
        ],
    },
])

add('part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.3.html', [
    {
        'h3': 'Foundational Datasets',
        'h3_id': 'datasets',
        'entries': [
            'Gokaslan, A., &amp; Cohen, V. (2019). "OpenWebText Corpus." <a href="https://skylion007.github.io/OpenWebTextCorpus/" rel="noopener" target="_blank">skylion007.github.io/OpenWebTextCorpus</a>. <span class="bib-note">Open replication of GPT-2\'s training corpus; the standard small-LM pretraining dataset.</span>',
            'Gao, L., Biderman, S., Black, S., et al. (2020). "The Pile: An 800GB Dataset of Diverse Text for Language Modeling." <a href="https://arxiv.org/abs/2101.00027" rel="noopener" target="_blank">arXiv:2101.00027</a>. <span class="bib-note">The reference open pretraining corpus.</span>',
            'Hugging Face (2024). "datasets Library Documentation." <a href="https://huggingface.co/docs/datasets" rel="noopener" target="_blank">huggingface.co/docs/datasets</a>. <span class="bib-note">Reference for streaming and memory-mapped dataset loading.</span>',
        ],
    },
    {
        'h3': 'Benchmarks',
        'h3_id': 'benchmarks',
        'entries': [
            'Wang, A., Pruksachatkun, Y., Nangia, N., et al. (2019). "SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems." <em>NeurIPS 2019</em>. <a href="https://arxiv.org/abs/1905.00537" rel="noopener" target="_blank">arXiv:1905.00537</a>. <span class="bib-note">Reference NLP-understanding benchmark.</span>',
            'Hendrycks, D., Burns, C., Basart, S., et al. (2021). "Measuring Massive Multitask Language Understanding" (MMLU). <em>ICLR 2021</em>. <a href="https://arxiv.org/abs/2009.03300" rel="noopener" target="_blank">arXiv:2009.03300</a>. <span class="bib-note">The standard multi-task LLM benchmark.</span>',
        ],
    },
])

add('part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.4.html', HF := [
    {
        'h3': 'Foundational Models',
        'h3_id': 'models',
        'entries': [
            'Touvron, H., Martin, L., Stone, K., et al. (2023). "Llama 2: Open Foundation and Fine-Tuned Chat Models." <a href="https://arxiv.org/abs/2307.09288" rel="noopener" target="_blank">arXiv:2307.09288</a>. <span class="bib-note">Reference open-weight LLM family.</span>',
            'Jiang, A. Q., Sablayrolles, A., Mensch, A., et al. (2023). "Mistral 7B." <a href="https://arxiv.org/abs/2310.06825" rel="noopener" target="_blank">arXiv:2310.06825</a>. <span class="bib-note">Reference for the Mistral architecture; the open-weight small-LM baseline.</span>',
            'DeepSeek-AI (2024). "DeepSeek-V3 Technical Report." <a href="https://arxiv.org/abs/2412.19437" rel="noopener" target="_blank">arXiv:2412.19437</a>. <span class="bib-note">Reference for the 2024-25 open-weight MoE architecture.</span>',
        ],
    },
    {
        'h3': 'Model Hubs',
        'h3_id': 'hubs',
        'entries': [
            'Hugging Face (2024). "HF Hub Documentation." <a href="https://huggingface.co/docs/hub" rel="noopener" target="_blank">huggingface.co/docs/hub</a>. <span class="bib-note">The canonical reference for the open-weight model registry.</span>',
        ],
    },
])

add('part-1-llm-building-blocks/module-05-tools-of-the-trade/section-5.5.html', [
    {
        'h3': 'Communities and Courses',
        'h3_id': 'communities',
        'entries': [
            'Karpathy, A. (2024). "Neural Networks: Zero to Hero." <a href="https://karpathy.ai/zero-to-hero.html" rel="noopener" target="_blank">karpathy.ai/zero-to-hero</a>. <span class="bib-note">The most-recommended LLM-from-scratch video course.</span>',
            'Hugging Face (2024). "NLP Course." <a href="https://huggingface.co/learn/nlp-course" rel="noopener" target="_blank">huggingface.co/learn/nlp-course</a>. <span class="bib-note">Reference open course on transformer-based NLP.</span>',
            'Stanford (2024). "CS224N: Natural Language Processing with Deep Learning." <a href="https://web.stanford.edu/class/cs224n/" rel="noopener" target="_blank">web.stanford.edu/class/cs224n</a>. <span class="bib-note">The standard academic NLP course.</span>',
        ],
    },
    {
        'h3': 'Reference Blogs',
        'h3_id': 'blogs',
        'entries': [
            'Alammar, J. (2018+). "The Illustrated Transformer." <a href="https://jalammar.github.io/illustrated-transformer/" rel="noopener" target="_blank">jalammar.github.io/illustrated-transformer</a>. <span class="bib-note">The most-cited visual explainer for transformer mechanics.</span>',
        ],
    },
])

# ============================================================
# Module 10: Interpretability (10.5-10.8 tools-of-trade-style)
# ============================================================
add('part-2-understanding-llms/module-10-interpretability/section-10.5.html', [
    {
        'h3': 'GPU Rental Markets',
        'h3_id': 'gpu-rentals',
        'entries': [
            'Pope, R., Douglas, S., Chowdhery, A., et al. (2023). "Efficiently Scaling Transformer Inference." <em>MLSys 2023</em>. <a href="https://arxiv.org/abs/2211.05102" rel="noopener" target="_blank">arXiv:2211.05102</a>. <span class="bib-note">Reference for GPU sizing across the inference Pareto frontier.</span>',
            'Hugging Face (2024). "Hugging Face Hub Documentation." <a href="https://huggingface.co/docs/hub" rel="noopener" target="_blank">huggingface.co/docs/hub</a>. <span class="bib-note">The canonical model registry; the primary hub layer of this section.</span>',
        ],
    },
    {
        'h3': 'Hardware References',
        'h3_id': 'hardware',
        'entries': [
            'NVIDIA (2024). "Hopper Architecture Whitepaper (H100/H200)." <a href="https://resources.nvidia.com/en-us-tensor-core" rel="noopener" target="_blank">resources.nvidia.com/en-us-tensor-core</a>. <span class="bib-note">The reference spec for the H100/H200 tier.</span>',
            'Apple (2024). "Apple Silicon Performance Documentation." <a href="https://developer.apple.com/documentation/metal" rel="noopener" target="_blank">developer.apple.com/documentation/metal</a>. <span class="bib-note">Reference for unified-memory Apple GPUs used for local LLM inference.</span>',
        ],
    },
])

add('part-2-understanding-llms/module-10-interpretability/section-10.6.html', [
    {
        'h3': 'Inference Libraries',
        'h3_id': 'inference',
        'entries': VLLM_REFS + HF_REFS,
    },
    {
        'h3': 'Mechanistic Interpretability Libraries',
        'h3_id': 'interp',
        'entries': [
            'Nanda, N., &amp; Bloom, J. (2022). "TransformerLens." <a href="https://github.com/TransformerLensOrg/TransformerLens" rel="noopener" target="_blank">github.com/TransformerLensOrg/TransformerLens</a>. <span class="bib-note">The standard mechanistic-interpretability library.</span>',
            'Conmy, A., Bloom, J., Lieberum, T., et al. (2024). "Sparse Autoencoder Library (SAELens)." <a href="https://github.com/jbloomAus/SAELens" rel="noopener" target="_blank">github.com/jbloomAus/SAELens</a>. <span class="bib-note">Reference SAE library for feature extraction.</span>',
        ],
    },
])

add('part-2-understanding-llms/module-10-interpretability/section-10.7.html', [
    {
        'h3': 'Datasets',
        'h3_id': 'datasets',
        'entries': [
            'Hendrycks, D., Burns, C., Basart, S., et al. (2021). "Measuring Massive Multitask Language Understanding" (MMLU). <em>ICLR 2021</em>. <a href="https://arxiv.org/abs/2009.03300" rel="noopener" target="_blank">arXiv:2009.03300</a>. <span class="bib-note">The standard general-knowledge LLM benchmark.</span>',
            'Biderman, S., Schoelkopf, H., Anthony, Q. G., et al. (2023). "Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling." <em>ICML 2023</em>. <a href="https://arxiv.org/abs/2304.01373" rel="noopener" target="_blank">arXiv:2304.01373</a>. <span class="bib-note">The Pythia model suite that powers most interpretability research.</span>',
        ],
    },
    {
        'h3': 'Interpretability Datasets',
        'h3_id': 'interp-data',
        'entries': [
            'Marks, S., &amp; Tegmark, M. (2023). "The Geometry of Truth: Emergent Linear Structure in Large Language Model Representations of True/False Datasets." <a href="https://arxiv.org/abs/2310.06824" rel="noopener" target="_blank">arXiv:2310.06824</a>. <span class="bib-note">Reference truth-probe dataset used in interpretability work.</span>',
        ],
    },
])

add('part-2-understanding-llms/module-10-interpretability/section-10.8.html', [
    {
        'h3': 'Foundational LLMs',
        'h3_id': 'foundational',
        'entries': [
            'Biderman, S., Schoelkopf, H., Anthony, Q. G., et al. (2023). "Pythia: A Suite for Analyzing Large Language Models." <em>ICML 2023</em>. <a href="https://arxiv.org/abs/2304.01373" rel="noopener" target="_blank">arXiv:2304.01373</a>. <span class="bib-note">The most-used model suite for interpretability research.</span>',
            'Touvron, H., et al. (2023). "Llama 2: Open Foundation and Fine-Tuned Chat Models." <a href="https://arxiv.org/abs/2307.09288" rel="noopener" target="_blank">arXiv:2307.09288</a>. <span class="bib-note">Reference open-weight model with widely-available interpretability hooks.</span>',
            'Groeneveld, D., Beltagy, I., Walsh, P., et al. (2024). "OLMo: Accelerating the Science of Language Models." <em>ACL 2024</em>. <a href="https://arxiv.org/abs/2402.00838" rel="noopener" target="_blank">arXiv:2402.00838</a>. <span class="bib-note">Fully-open LLM with intermediate checkpoints; reference for training-dynamics interpretability.</span>',
        ],
    },
])

# ============================================================
# Module 14: Working with LLMs - Tools
# ============================================================
add('part-3-working-with-llms/module-14-tools-of-the-trade/section-14.2.html', [
    {
        'h3': 'LLM Application Frameworks',
        'h3_id': 'frameworks',
        'entries': [
            'LangChain (2024). "LangChain Documentation." <a href="https://python.langchain.com/docs/get_started/introduction" rel="noopener" target="_blank">python.langchain.com</a>. <span class="bib-note">The most-cited LLM-orchestration framework.</span>',
            'LlamaIndex (2024). "LlamaIndex Documentation." <a href="https://docs.llamaindex.ai/" rel="noopener" target="_blank">docs.llamaindex.ai</a>. <span class="bib-note">Reference RAG and document-indexing framework.</span>',
            'Instructor (Liu, J., 2024). "Instructor: Structured outputs for LLMs." <a href="https://python.useinstructor.com/" rel="noopener" target="_blank">python.useinstructor.com</a>. <span class="bib-note">Reference library for structured output extraction.</span>',
        ],
    },
    {
        'h3': 'Prompt Engineering Tools',
        'h3_id': 'prompt',
        'entries': [
            'DSPy (Khattab, O., 2024). "DSPy: Programming Language for LLM Systems." <a href="https://dspy.ai" rel="noopener" target="_blank">dspy.ai</a>. <span class="bib-note">Reference programmatic-prompt framework that compiles prompts via optimization.</span>',
        ],
    },
])

add('part-3-working-with-llms/module-14-tools-of-the-trade/section-14.3.html', [
    {
        'h3': 'Instruction Datasets',
        'h3_id': 'instruction',
        'entries': [
            'Wang, Y., Mishra, S., Alipoormolabashi, P., et al. (2022). "Super-NaturalInstructions." <em>EMNLP 2022</em>. <a href="https://arxiv.org/abs/2204.07705" rel="noopener" target="_blank">arXiv:2204.07705</a>. <span class="bib-note">Reference large-scale instruction-tuning dataset.</span>',
            'Conover, M., Hayes, M., Mathur, A., et al. (2023). "Free Dolly: Introducing the World\'s First Truly Open Instruction-Tuned LLM." Databricks. <a href="https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm" rel="noopener" target="_blank">databricks.com/blog/dolly</a>. <span class="bib-note">The Dolly-15k dataset; reference for fully-open instruction tuning data.</span>',
        ],
    },
    {
        'h3': 'Evaluation Datasets',
        'h3_id': 'eval',
        'entries': [
            'Hendrycks, D., et al. (2021). "MMLU." <a href="https://arxiv.org/abs/2009.03300" rel="noopener" target="_blank">arXiv:2009.03300</a>. <span class="bib-note">Standard general-knowledge LLM benchmark.</span>',
            'Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). "MT-Bench." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2306.05685" rel="noopener" target="_blank">arXiv:2306.05685</a>. <span class="bib-note">Reference multi-turn LLM benchmark.</span>',
        ],
    },
])

add('part-3-working-with-llms/module-14-tools-of-the-trade/section-14.4.html', [
    {
        'h3': 'Closed-Source Frontier Models',
        'h3_id': 'frontier',
        'entries': [
            'OpenAI (2024). "GPT-4o System Card." <a href="https://openai.com/index/gpt-4o-system-card/" rel="noopener" target="_blank">openai.com/index/gpt-4o-system-card</a>. <span class="bib-note">Reference for GPT-4o capabilities and limitations.</span>',
            'Anthropic (2024). "Claude 3.5 Sonnet Model Card." <a href="https://www.anthropic.com/news/claude-3-5-sonnet" rel="noopener" target="_blank">anthropic.com/news/claude-3-5-sonnet</a>. <span class="bib-note">Reference for Claude 3.5 Sonnet.</span>',
            'Google DeepMind (2024). "Gemini: A Family of Highly Capable Multimodal Models." <a href="https://arxiv.org/abs/2312.11805" rel="noopener" target="_blank">arXiv:2312.11805</a>. <span class="bib-note">Reference for the Gemini model family.</span>',
        ],
    },
    {
        'h3': 'Open Models',
        'h3_id': 'open',
        'entries': [
            'Touvron, H., et al. (2023). "Llama 2." <a href="https://arxiv.org/abs/2307.09288" rel="noopener" target="_blank">arXiv:2307.09288</a>. <span class="bib-note">Reference open-weight LLM family.</span>',
            'DeepSeek-AI (2024). "DeepSeek-V3 Technical Report." <a href="https://arxiv.org/abs/2412.19437" rel="noopener" target="_blank">arXiv:2412.19437</a>. <span class="bib-note">Reference 2024-25 open-weight MoE.</span>',
        ],
    },
])

add('part-3-working-with-llms/module-14-tools-of-the-trade/section-14.5.html', [
    {
        'h3': 'Practitioner Guides',
        'h3_id': 'guides',
        'entries': [
            'Anthropic (2024). "Building Effective Agents." <a href="https://www.anthropic.com/research/building-effective-agents" rel="noopener" target="_blank">anthropic.com/research/building-effective-agents</a>. <span class="bib-note">Reference patterns for LLM application design.</span>',
            'OpenAI (2024). "OpenAI Cookbook." <a href="https://cookbook.openai.com" rel="noopener" target="_blank">cookbook.openai.com</a>. <span class="bib-note">Reference recipes for production LLM API use.</span>',
        ],
    },
    {
        'h3': 'Communities',
        'h3_id': 'communities',
        'entries': [
            'Hugging Face (2024). "HF Forums." <a href="https://discuss.huggingface.co" rel="noopener" target="_blank">discuss.huggingface.co</a>. <span class="bib-note">The largest community forum for open-weight LLM work.</span>',
        ],
    },
])

# ============================================================
# Module 19: Training & Adaptation Stack (large module - 14 sections)
# ============================================================
add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.1.html', [
    {
        'h3': 'Distributed Training Frameworks',
        'h3_id': 'distributed',
        'entries': [
            'Rasley, J., Rajbhandari, S., Ruwase, O., &amp; He, Y. (2020). "DeepSpeed: System Optimizations Enable Training Deep Learning Models with Over 100 Billion Parameters." <em>KDD 2020</em>. <a href="https://dl.acm.org/doi/10.1145/3394486.3406703" rel="noopener" target="_blank">dl.acm.org/doi/10.1145/3394486.3406703</a>. <span class="bib-note">The DeepSpeed paper.</span>',
            'Shoeybi, M., Patwary, M., Puri, R., et al. (2019). "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism." <a href="https://arxiv.org/abs/1909.08053" rel="noopener" target="_blank">arXiv:1909.08053</a>. <span class="bib-note">The Megatron-LM paper.</span>',
            'Zhao, Y., Gu, A., Varma, R., et al. (2023). "PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel." <em>VLDB 2023</em>. <a href="https://arxiv.org/abs/2304.11277" rel="noopener" target="_blank">arXiv:2304.11277</a>. <span class="bib-note">The FSDP paper.</span>',
        ],
    },
    {
        'h3': 'Experiment Tracking',
        'h3_id': 'tracking',
        'entries': [
            'Weights &amp; Biases (2024). "W&amp;B Documentation." <a href="https://docs.wandb.ai/" rel="noopener" target="_blank">docs.wandb.ai</a>. <span class="bib-note">Reference experiment-tracking platform.</span>',
            'MLflow (2024). "MLflow Documentation." <a href="https://mlflow.org/docs/latest/" rel="noopener" target="_blank">mlflow.org/docs/latest</a>. <span class="bib-note">Reference open-source experiment tracker.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.2.html', [
    {
        'h3': 'Training Libraries',
        'h3_id': 'libs',
        'entries': HF_REFS + [
            'Hugging Face (2024). "Accelerate." <a href="https://huggingface.co/docs/accelerate" rel="noopener" target="_blank">huggingface.co/docs/accelerate</a>. <span class="bib-note">Reference thin distributed-training wrapper.</span>',
            'Hugging Face (2024). "TRL: Transformer Reinforcement Learning." <a href="https://huggingface.co/docs/trl" rel="noopener" target="_blank">huggingface.co/docs/trl</a>. <span class="bib-note">Reference library for RLHF, DPO, GRPO training.</span>',
        ],
    },
    {
        'h3': 'PEFT and LoRA',
        'h3_id': 'peft',
        'entries': [
            'Hu, E., Shen, Y., Wallis, P., et al. (2022). "LoRA: Low-Rank Adaptation of Large Language Models." <em>ICLR 2022</em>. <a href="https://arxiv.org/abs/2106.09685" rel="noopener" target="_blank">arXiv:2106.09685</a>. <span class="bib-note">The reference LoRA paper.</span>',
            'Hugging Face (2024). "PEFT Documentation." <a href="https://huggingface.co/docs/peft" rel="noopener" target="_blank">huggingface.co/docs/peft</a>. <span class="bib-note">Reference parameter-efficient fine-tuning library.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.3.html', [
    {
        'h3': 'Training Datasets',
        'h3_id': 'datasets',
        'entries': [
            'Gao, L., et al. (2020). "The Pile." <a href="https://arxiv.org/abs/2101.00027" rel="noopener" target="_blank">arXiv:2101.00027</a>. <span class="bib-note">Reference 800GB pretraining corpus.</span>',
            'Penedo, G., Malartic, Q., Hesslow, D., et al. (2023). "The RefinedWeb Dataset for Falcon LLM." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2306.01116" rel="noopener" target="_blank">arXiv:2306.01116</a>. <span class="bib-note">Reference for the high-quality web-scale pretraining corpus methodology.</span>',
            'Soldaini, L., Kinney, R., Bhagia, A., et al. (2024). "Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research." <em>ACL 2024</em>. <a href="https://arxiv.org/abs/2402.00159" rel="noopener" target="_blank">arXiv:2402.00159</a>. <span class="bib-note">Reference 3T-token open corpus.</span>',
        ],
    },
    {
        'h3': 'Data Pipelines',
        'h3_id': 'pipelines',
        'entries': [
            'Apache Spark (2024). "PySpark Documentation." <a href="https://spark.apache.org/docs/latest/api/python/" rel="noopener" target="_blank">spark.apache.org/docs/latest/api/python</a>. <span class="bib-note">Reference distributed-data-processing framework.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.4.html', [
    {
        'h3': 'Base Models for Fine-Tuning',
        'h3_id': 'base',
        'entries': [
            'Touvron, H., et al. (2023). "Llama 2." <a href="https://arxiv.org/abs/2307.09288" rel="noopener" target="_blank">arXiv:2307.09288</a>. <span class="bib-note">Reference open-weight base model.</span>',
            'Jiang, A. Q., et al. (2024). "Mixtral of Experts." <a href="https://arxiv.org/abs/2401.04088" rel="noopener" target="_blank">arXiv:2401.04088</a>. <span class="bib-note">Reference open-weight MoE.</span>',
            'Qwen Team (2024). "Qwen3 Technical Report." <a href="https://arxiv.org/abs/2412.15115" rel="noopener" target="_blank">arXiv:2412.15115</a>. <span class="bib-note">Reference for the Qwen3 model family.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.5.html', [
    {
        'h3': 'Practitioner Guides',
        'h3_id': 'guides',
        'entries': [
            'Karpathy, A. (2024). "Let\'s build the GPT Tokenizer." <a href="https://www.youtube.com/watch?v=zduSFxRajkE" rel="noopener" target="_blank">YouTube</a>. <span class="bib-note">Reference walkthrough on training a BPE tokenizer.</span>',
            'Karpathy, A. (2024). "Let\'s Reproduce GPT-2 (124M)." <a href="https://www.youtube.com/watch?v=l8pRSuU81PU" rel="noopener" target="_blank">YouTube</a>. <span class="bib-note">Reference end-to-end pretraining walkthrough.</span>',
        ],
    },
    {
        'h3': 'Communities',
        'h3_id': 'communities',
        'entries': [
            'EleutherAI (2024). "EleutherAI Discord and Research Forum." <a href="https://www.eleuther.ai" rel="noopener" target="_blank">eleuther.ai</a>. <span class="bib-note">The largest open-source LLM research community.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.6.html', [
    {
        'h3': 'Hugging Face Stack',
        'h3_id': 'hf',
        'entries': HF_REFS + [
            'Hugging Face (2024). "datasets Documentation." <a href="https://huggingface.co/docs/datasets" rel="noopener" target="_blank">huggingface.co/docs/datasets</a>. <span class="bib-note">Reference for the datasets library used in this section.</span>',
            'Hugging Face (2024). "tokenizers Documentation." <a href="https://huggingface.co/docs/tokenizers" rel="noopener" target="_blank">huggingface.co/docs/tokenizers</a>. <span class="bib-note">Reference for the Rust-backed tokenizers library.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.7.html', [
    {
        'h3': 'Trainer and Accelerate',
        'h3_id': 'trainer',
        'entries': HF_REFS + [
            'Hugging Face (2024). "Trainer Documentation." <a href="https://huggingface.co/docs/transformers/main_classes/trainer" rel="noopener" target="_blank">huggingface.co/docs/transformers/main_classes/trainer</a>. <span class="bib-note">Authoritative reference for the Trainer API used in this section.</span>',
            'Hugging Face (2024). "Accelerate." <a href="https://huggingface.co/docs/accelerate" rel="noopener" target="_blank">huggingface.co/docs/accelerate</a>. <span class="bib-note">Reference distributed-training wrapper.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.8.html', [
    {
        'h3': 'PEFT and RLHF',
        'h3_id': 'peft-rlhf',
        'entries': [
            'Hu, E., et al. (2022). "LoRA: Low-Rank Adaptation of Large Language Models." <em>ICLR 2022</em>. <a href="https://arxiv.org/abs/2106.09685" rel="noopener" target="_blank">arXiv:2106.09685</a>. <span class="bib-note">The reference LoRA paper.</span>',
            'Hugging Face (2024). "PEFT Documentation." <a href="https://huggingface.co/docs/peft" rel="noopener" target="_blank">huggingface.co/docs/peft</a>. <span class="bib-note">Reference parameter-efficient fine-tuning library.</span>',
            'Hugging Face (2024). "TRL: Transformer Reinforcement Learning." <a href="https://huggingface.co/docs/trl" rel="noopener" target="_blank">huggingface.co/docs/trl</a>. <span class="bib-note">Reference RLHF/DPO library used in this section.</span>',
            'Rafailov, R., Sharma, A., Mitchell, E., et al. (2023). "Direct Preference Optimization." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2305.18290" rel="noopener" target="_blank">arXiv:2305.18290</a>. <span class="bib-note">The DPO paper underlying TRL\'s DPO trainer.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.9.html', [
    {
        'h3': 'Reproducibility and MLOps',
        'h3_id': 'reproducibility',
        'entries': [
            'Weights &amp; Biases (2024). "W&amp;B Git Integration." <a href="https://docs.wandb.ai/guides/runs/git-integration" rel="noopener" target="_blank">docs.wandb.ai/guides/runs/git-integration</a>. <span class="bib-note">Reference for linking W&amp;B runs to git commits.</span>',
            'DVC (2024). "Data Version Control Documentation." <a href="https://dvc.org/doc" rel="noopener" target="_blank">dvc.org/doc</a>. <span class="bib-note">Reference for git-based ML data and pipeline versioning.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.10.html', [
    {
        'h3': 'W&amp;B',
        'h3_id': 'wandb',
        'entries': [
            'Weights &amp; Biases (2024). "W&amp;B Documentation." <a href="https://docs.wandb.ai/" rel="noopener" target="_blank">docs.wandb.ai</a>. <span class="bib-note">Authoritative reference for the W&amp;B experiment-tracking platform.</span>',
            'Weights &amp; Biases (2024). "W&amp;B Sweeps." <a href="https://docs.wandb.ai/guides/sweeps" rel="noopener" target="_blank">docs.wandb.ai/guides/sweeps</a>. <span class="bib-note">Reference for hyperparameter-sweep orchestration.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.11.html', [
    {
        'h3': 'MLflow',
        'h3_id': 'mlflow',
        'entries': [
            'MLflow (2024). "MLflow Documentation." <a href="https://mlflow.org/docs/latest/" rel="noopener" target="_blank">mlflow.org/docs/latest</a>. <span class="bib-note">Authoritative reference for the MLflow tracking and registry platform.</span>',
            'Databricks (2018). "MLflow: A Platform for Machine Learning Development." <a href="https://www.databricks.com/blog/2018/06/05/introducing-mlflow-an-open-source-machine-learning-platform.html" rel="noopener" target="_blank">databricks.com/blog/2018/06/05/introducing-mlflow</a>. <span class="bib-note">The original MLflow announcement blog post.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.12.html', [
    {
        'h3': 'Hyperparameter Optimization',
        'h3_id': 'hpo',
        'entries': [
            'Akiba, T., Sano, S., Yanase, T., Ohta, T., &amp; Koyama, M. (2019). "Optuna: A Next-generation Hyperparameter Optimization Framework." <em>KDD 2019</em>. <a href="https://arxiv.org/abs/1907.10902" rel="noopener" target="_blank">arXiv:1907.10902</a>. <span class="bib-note">The Optuna paper; reference for production HPO.</span>',
            'Bergstra, J., &amp; Bengio, Y. (2012). "Random Search for Hyper-Parameter Optimization." <em>JMLR 13</em>. <a href="https://www.jmlr.org/papers/v13/bergstra12a.html" rel="noopener" target="_blank">jmlr.org/papers/v13/bergstra12a</a>. <span class="bib-note">The reference paper showing random search beats grid search.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.13.html', [
    {
        'h3': 'Distributed Training',
        'h3_id': 'distributed',
        'entries': [
            'Rajbhandari, S., Rasley, J., Ruwase, O., &amp; He, Y. (2020). "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models." <em>SC 2020</em>. <a href="https://arxiv.org/abs/1910.02054" rel="noopener" target="_blank">arXiv:1910.02054</a>. <span class="bib-note">The original ZeRO paper that underlies DeepSpeed and FSDP.</span>',
            'Zhao, Y., et al. (2023). "PyTorch FSDP." <em>VLDB 2023</em>. <a href="https://arxiv.org/abs/2304.11277" rel="noopener" target="_blank">arXiv:2304.11277</a>. <span class="bib-note">The FSDP paper.</span>',
            'Shoeybi, M., et al. (2019). "Megatron-LM." <a href="https://arxiv.org/abs/1909.08053" rel="noopener" target="_blank">arXiv:1909.08053</a>. <span class="bib-note">Reference for tensor parallelism.</span>',
            'Huang, Y., Cheng, Y., Bapna, A., et al. (2019). "GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism." <em>NeurIPS 2019</em>. <a href="https://arxiv.org/abs/1811.06965" rel="noopener" target="_blank">arXiv:1811.06965</a>. <span class="bib-note">Reference for pipeline parallelism.</span>',
        ],
    },
])

add('part-4-training-adaptation/module-19-tools-of-the-trade/section-19.14.html', [
    {
        'h3': 'Ray Stack',
        'h3_id': 'ray',
        'entries': [
            'Moritz, P., Nishihara, R., Wang, S., et al. (2018). "Ray: A Distributed Framework for Emerging AI Applications." <em>OSDI 2018</em>. <a href="https://arxiv.org/abs/1712.05889" rel="noopener" target="_blank">arXiv:1712.05889</a>. <span class="bib-note">The Ray paper.</span>',
            'Anyscale (2024). "Ray Documentation." <a href="https://docs.ray.io/en/latest/" rel="noopener" target="_blank">docs.ray.io/en/latest</a>. <span class="bib-note">Authoritative reference for Ray Train, Ray Serve, and Ray Data.</span>',
        ],
    },
])

# ============================================================
# Module 25: Multimodal Tools
# ============================================================
add('part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.1.html', [
    {
        'h3': 'Multimodal Platforms',
        'h3_id': 'platforms',
        'entries': [
            'OpenAI (2024). "GPT-4o System Card." <a href="https://openai.com/index/gpt-4o-system-card/" rel="noopener" target="_blank">openai.com/index/gpt-4o-system-card</a>. <span class="bib-note">Reference multimodal LLM platform.</span>',
            'Google DeepMind (2024). "Gemini." <a href="https://arxiv.org/abs/2312.11805" rel="noopener" target="_blank">arXiv:2312.11805</a>. <span class="bib-note">Reference native-multimodal LLM platform.</span>',
            'Anthropic (2024). "Claude 3.5 Sonnet." <a href="https://www.anthropic.com/news/claude-3-5-sonnet" rel="noopener" target="_blank">anthropic.com/news/claude-3-5-sonnet</a>. <span class="bib-note">Reference vision-capable LLM platform.</span>',
        ],
    },
])

add('part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.2.html', [
    {
        'h3': 'Vision Libraries',
        'h3_id': 'vision',
        'entries': [
            'Radford, A., Kim, J. W., Hallacy, C., et al. (2021). "Learning Transferable Visual Models From Natural Language Supervision" (CLIP). <em>ICML 2021</em>. <a href="https://arxiv.org/abs/2103.00020" rel="noopener" target="_blank">arXiv:2103.00020</a>. <span class="bib-note">The CLIP paper; the foundation of modern vision-language libraries.</span>',
            'Cherti, M., Beaumont, R., Wightman, R., et al. (2023). "Reproducible scaling laws for contrastive language-image learning" (OpenCLIP). <em>CVPR 2023</em>. <a href="https://arxiv.org/abs/2212.07143" rel="noopener" target="_blank">arXiv:2212.07143</a>. <span class="bib-note">OpenCLIP: the reference open-source CLIP library.</span>',
        ],
    },
    {
        'h3': 'Diffusion Libraries',
        'h3_id': 'diffusion',
        'entries': [
            'Hugging Face (2024). "diffusers Library." <a href="https://huggingface.co/docs/diffusers" rel="noopener" target="_blank">huggingface.co/docs/diffusers</a>. <span class="bib-note">Reference diffusion-model library.</span>',
            'Rombach, R., et al. (2022). "Stable Diffusion." <em>CVPR 2022</em>. <a href="https://arxiv.org/abs/2112.10752" rel="noopener" target="_blank">arXiv:2112.10752</a>. <span class="bib-note">The reference latent-diffusion paper.</span>',
        ],
    },
])

add('part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.3.html', [
    {
        'h3': 'Multimodal Datasets',
        'h3_id': 'datasets',
        'entries': [
            'Schuhmann, C., Beaumont, R., Vencu, R., et al. (2022). "LAION-5B: An open large-scale dataset for training next generation image-text models." <em>NeurIPS 2022</em>. <a href="https://arxiv.org/abs/2210.08402" rel="noopener" target="_blank">arXiv:2210.08402</a>. <span class="bib-note">The reference large-scale image-text dataset.</span>',
            'Lin, T.-Y., Maire, M., Belongie, S., et al. (2014). "Microsoft COCO: Common Objects in Context." <em>ECCV 2014</em>. <a href="https://arxiv.org/abs/1405.0312" rel="noopener" target="_blank">arXiv:1405.0312</a>. <span class="bib-note">The reference vision-grounding dataset.</span>',
        ],
    },
    {
        'h3': 'Multimodal Benchmarks',
        'h3_id': 'benchmarks',
        'entries': [
            'Liu, H., Li, C., Wu, Q., &amp; Lee, Y. J. (2024). "Visual Instruction Tuning" (LLaVA). <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2304.08485" rel="noopener" target="_blank">arXiv:2304.08485</a>. <span class="bib-note">Reference vision-instruction model and benchmark.</span>',
        ],
    },
])

add('part-5-multimodal-llms/module-25-tools-of-the-trade/section-25.4.html', [
    {
        'h3': 'Vision-Language Models',
        'h3_id': 'vlm',
        'entries': [
            'Liu, H., Li, C., Wu, Q., &amp; Lee, Y. J. (2024). "Visual Instruction Tuning" (LLaVA). <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2304.08485" rel="noopener" target="_blank">arXiv:2304.08485</a>. <span class="bib-note">Reference open vision-language model.</span>',
            'Beyer, L., Steiner, A., Pinto, A. S., et al. (2024). "PaliGemma: A versatile 3B VLM for transfer." <a href="https://arxiv.org/abs/2407.07726" rel="noopener" target="_blank">arXiv:2407.07726</a>. <span class="bib-note">Reference 2024 open VLM.</span>',
            'Chen, Z., Wu, J., Wang, W., et al. (2024). "InternVL: Scaling up Vision Foundation Models." <em>CVPR 2024</em>. <a href="https://arxiv.org/abs/2312.14238" rel="noopener" target="_blank">arXiv:2312.14238</a>. <span class="bib-note">Reference for large open vision-language model.</span>',
        ],
    },
])

# ============================================================
# Module 30: Agentic AI Tools
# ============================================================
add('part-6-agentic-ai/module-30-tools-of-the-trade/section-30.1.html', [
    {
        'h3': 'Agent Platforms',
        'h3_id': 'platforms',
        'entries': [
            'OpenAI (2024). "Assistants API." <a href="https://platform.openai.com/docs/assistants/overview" rel="noopener" target="_blank">platform.openai.com/docs/assistants/overview</a>. <span class="bib-note">Reference managed-agents platform.</span>',
            'Anthropic (2024). "Tool Use with Claude." <a href="https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview" rel="noopener" target="_blank">docs.claude.com/agents-and-tools/tool-use</a>. <span class="bib-note">Reference tool-use API for agentic LLM systems.</span>',
            'LangGraph (2024). "LangGraph Documentation." <a href="https://langchain-ai.github.io/langgraph/" rel="noopener" target="_blank">langchain-ai.github.io/langgraph</a>. <span class="bib-note">Reference orchestration library for stateful agent graphs.</span>',
        ],
    },
])

add('part-6-agentic-ai/module-30-tools-of-the-trade/section-30.3.html', [
    {
        'h3': 'Agent Benchmarks',
        'h3_id': 'benchmarks',
        'entries': [
            'Liu, X., Yu, H., Zhang, H., et al. (2023). "AgentBench: Evaluating LLMs as Agents." <em>ICLR 2024</em>. <a href="https://arxiv.org/abs/2308.03688" rel="noopener" target="_blank">arXiv:2308.03688</a>. <span class="bib-note">Reference agent benchmark suite.</span>',
            'Yao, S., Chen, H., Yang, J., &amp; Narasimhan, K. (2022). "WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents." <em>NeurIPS 2022</em>. <a href="https://arxiv.org/abs/2207.01206" rel="noopener" target="_blank">arXiv:2207.01206</a>. <span class="bib-note">Reference web-agent benchmark.</span>',
        ],
    },
    {
        'h3': 'Tool-Use Benchmarks',
        'h3_id': 'tool-use',
        'entries': [
            'Qin, Y., Liang, S., Ye, Y., et al. (2024). "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs." <em>ICLR 2024</em>. <a href="https://arxiv.org/abs/2307.16789" rel="noopener" target="_blank">arXiv:2307.16789</a>. <span class="bib-note">Reference large-scale tool-use benchmark.</span>',
        ],
    },
])

add('part-6-agentic-ai/module-30-tools-of-the-trade/section-30.4.html', [
    {
        'h3': 'Agent Models',
        'h3_id': 'models',
        'entries': [
            'OpenAI (2024). "GPT-4o System Card." <a href="https://openai.com/index/gpt-4o-system-card/" rel="noopener" target="_blank">openai.com/index/gpt-4o-system-card</a>. <span class="bib-note">Reference for an agent-capable frontier LLM.</span>',
            'Anthropic (2024). "Claude 3.5 Sonnet." <a href="https://www.anthropic.com/news/claude-3-5-sonnet" rel="noopener" target="_blank">anthropic.com/news/claude-3-5-sonnet</a>. <span class="bib-note">Reference for an agent-capable LLM with computer-use support.</span>',
            'DeepSeek-AI (2024). "DeepSeek-V3 Technical Report." <a href="https://arxiv.org/abs/2412.19437" rel="noopener" target="_blank">arXiv:2412.19437</a>. <span class="bib-note">Reference open-weight agent-capable model.</span>',
        ],
    },
])

add('part-6-agentic-ai/module-30-tools-of-the-trade/section-30.5.html', [
    {
        'h3': 'Practitioner Guides',
        'h3_id': 'guides',
        'entries': [
            'Anthropic (2024). "Building Effective Agents." <a href="https://www.anthropic.com/research/building-effective-agents" rel="noopener" target="_blank">anthropic.com/research/building-effective-agents</a>. <span class="bib-note">Reference practitioner guide on agent design patterns.</span>',
            'OpenAI (2024). "A Practical Guide to Building Agents." <a href="https://openai.com/index/practical-guide-to-building-agents/" rel="noopener" target="_blank">openai.com/index/practical-guide-to-building-agents</a>. <span class="bib-note">Reference industry guide on agent product design.</span>',
        ],
    },
])

# ============================================================
# Module 45: Eval Tools (Part 9)
# ============================================================
add('part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.1.html', [
    {
        'h3': 'Eval Platforms',
        'h3_id': 'platforms',
        'entries': [
            'Hugging Face (2024). "lm-evaluation-harness." <a href="https://github.com/EleutherAI/lm-evaluation-harness" rel="noopener" target="_blank">github.com/EleutherAI/lm-evaluation-harness</a>. <span class="bib-note">The reference open-source LLM evaluation harness.</span>',
            'OpenAI (2024). "OpenAI Evals." <a href="https://github.com/openai/evals" rel="noopener" target="_blank">github.com/openai/evals</a>. <span class="bib-note">Reference evaluation framework from OpenAI.</span>',
            'Langfuse (2024). "Langfuse Documentation." <a href="https://langfuse.com/docs" rel="noopener" target="_blank">langfuse.com/docs</a>. <span class="bib-note">Reference open-source LLM observability platform.</span>',
        ],
    },
])

add('part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.3.html', [
    {
        'h3': 'Eval Benchmarks',
        'h3_id': 'benchmarks',
        'entries': [
            'Hendrycks, D., et al. (2021). "MMLU." <a href="https://arxiv.org/abs/2009.03300" rel="noopener" target="_blank">arXiv:2009.03300</a>. <span class="bib-note">Reference general-knowledge benchmark.</span>',
            'Zheng, L., et al. (2023). "MT-Bench." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2306.05685" rel="noopener" target="_blank">arXiv:2306.05685</a>. <span class="bib-note">Reference multi-turn LLM benchmark.</span>',
            'Chiang, W.-L., Zheng, L., Sheng, Y., et al. (2024). "Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference." <em>ICML 2024</em>. <a href="https://arxiv.org/abs/2403.04132" rel="noopener" target="_blank">arXiv:2403.04132</a>. <span class="bib-note">Reference human-preference leaderboard.</span>',
        ],
    },
])

add('part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.4.html', [
    {
        'h3': 'Judge Models',
        'h3_id': 'judges',
        'entries': [
            'Kim, S., et al. (2024). "Prometheus 2." <em>EMNLP 2024</em>. <a href="https://arxiv.org/abs/2405.01535" rel="noopener" target="_blank">arXiv:2405.01535</a>. <span class="bib-note">Reference open judge model.</span>',
            'Vu, T., Krishna, K., Alzubi, S., et al. (2024). "Foundational Autoraters: Taming Large Language Models for Better Automatic Evaluation." <a href="https://arxiv.org/abs/2407.10817" rel="noopener" target="_blank">arXiv:2407.10817</a>. <span class="bib-note">Reference foundational autorater work from Google.</span>',
        ],
    },
])

add('part-9-llm-evaluation-observability/module-45-tools-of-the-trade/section-45.5.html', [
    {
        'h3': 'External Reading',
        'h3_id': 'reading',
        'entries': [
            'OpenAI (2024). "GPT-4 Technical Report." <a href="https://arxiv.org/abs/2303.08774" rel="noopener" target="_blank">arXiv:2303.08774</a>. <span class="bib-note">Reference for the evaluation methodology used in flagship LLM releases.</span>',
            'Stanford HAI (2024). "HELM: Holistic Evaluation of Language Models." <a href="https://crfm.stanford.edu/helm/" rel="noopener" target="_blank">crfm.stanford.edu/helm</a>. <span class="bib-note">Reference holistic LLM evaluation framework.</span>',
        ],
    },
])

# ============================================================
# Module 51: Security Tools
# ============================================================
add('part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.1.html', [
    {
        'h3': 'Security Platforms',
        'h3_id': 'platforms',
        'entries': [
            'Microsoft (2024). "Microsoft Security Copilot." <a href="https://www.microsoft.com/en-us/security/business/ai-machine-learning/microsoft-security-copilot" rel="noopener" target="_blank">microsoft.com/en-us/security/business/ai-machine-learning/microsoft-security-copilot</a>. <span class="bib-note">Reference enterprise LLM security platform.</span>',
            'Cloudflare (2024). "Cloudflare Workers AI." <a href="https://developers.cloudflare.com/workers-ai/" rel="noopener" target="_blank">developers.cloudflare.com/workers-ai</a>. <span class="bib-note">Reference platform for LLM-edge security including prompt-injection scanning.</span>',
        ],
    },
])

add('part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.2.html', [
    {
        'h3': 'Security Libraries',
        'h3_id': 'libraries',
        'entries': [
            'NVIDIA (2024). "NeMo Guardrails." <a href="https://github.com/NVIDIA/NeMo-Guardrails" rel="noopener" target="_blank">github.com/NVIDIA/NeMo-Guardrails</a>. <span class="bib-note">Reference open-source guardrails framework.</span>',
            'Guardrails AI (2024). "Guardrails Documentation." <a href="https://docs.guardrailsai.com/" rel="noopener" target="_blank">docs.guardrailsai.com</a>. <span class="bib-note">Reference output-validation library.</span>',
            'Microsoft (2024). "Presidio." <a href="https://microsoft.github.io/presidio/" rel="noopener" target="_blank">microsoft.github.io/presidio</a>. <span class="bib-note">Reference PII-detection library.</span>',
        ],
    },
])

add('part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.3.html', [
    {
        'h3': 'Security Benchmarks',
        'h3_id': 'benchmarks',
        'entries': [
            'Bhardwaj, R., &amp; Poria, S. (2023). "Red-Teaming Large Language Models using Chain of Utterances for Safety-Alignment." <a href="https://arxiv.org/abs/2308.09662" rel="noopener" target="_blank">arXiv:2308.09662</a>. <span class="bib-note">Reference red-team benchmark for LLMs.</span>',
            'Zou, A., Wang, Z., Carlini, N., et al. (2023). "Universal and Transferable Adversarial Attacks on Aligned Language Models." <a href="https://arxiv.org/abs/2307.15043" rel="noopener" target="_blank">arXiv:2307.15043</a>. <span class="bib-note">Reference for transferable jailbreaks; defines benchmark adversarial inputs.</span>',
        ],
    },
])

add('part-10-llm-security-runtime-safety/module-51-tools-of-the-trade/section-51.4.html', [
    {
        'h3': 'Safety Models',
        'h3_id': 'safety-models',
        'entries': [
            'Inan, H., Upasani, K., Chi, J., et al. (2023). "Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations." <a href="https://arxiv.org/abs/2312.06674" rel="noopener" target="_blank">arXiv:2312.06674</a>. <span class="bib-note">Reference open-source safety classifier.</span>',
            'OpenAI (2022). "Moderation API." <a href="https://platform.openai.com/docs/guides/moderation" rel="noopener" target="_blank">platform.openai.com/docs/guides/moderation</a>. <span class="bib-note">Reference safety-classification API.</span>',
        ],
    },
])

# ============================================================
# Module 71: Product Design Tools
# ============================================================
add('part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.1.html', [
    {
        'h3': 'Product Platforms',
        'h3_id': 'platforms',
        'entries': [
            'OpenAI (2024). "Custom GPTs." <a href="https://openai.com/index/introducing-the-gpt-store/" rel="noopener" target="_blank">openai.com/index/introducing-the-gpt-store</a>. <span class="bib-note">Reference no-code LLM-product platform.</span>',
            'Anthropic (2024). "Claude API." <a href="https://docs.claude.com/en/api/overview" rel="noopener" target="_blank">docs.claude.com/en/api/overview</a>. <span class="bib-note">Reference for building production LLM products.</span>',
        ],
    },
])

add('part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.2.html', [
    {
        'h3': 'Product Libraries',
        'h3_id': 'libraries',
        'entries': [
            'Vercel (2024). "Vercel AI SDK." <a href="https://sdk.vercel.ai/docs" rel="noopener" target="_blank">sdk.vercel.ai/docs</a>. <span class="bib-note">Reference TypeScript SDK for streaming LLM UIs.</span>',
            'LangChain (2024). "LangChain." <a href="https://python.langchain.com/docs/get_started/introduction" rel="noopener" target="_blank">python.langchain.com</a>. <span class="bib-note">Reference orchestration framework for LLM products.</span>',
        ],
    },
])

add('part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.3.html', [
    {
        'h3': 'Product Datasets',
        'h3_id': 'datasets',
        'entries': [
            'OpenAI (2024). "Evals Dataset Repository." <a href="https://github.com/openai/evals" rel="noopener" target="_blank">github.com/openai/evals</a>. <span class="bib-note">Reference dataset suite for LLM-product evaluation.</span>',
            'Hugging Face (2024). "datasets Hub." <a href="https://huggingface.co/datasets" rel="noopener" target="_blank">huggingface.co/datasets</a>. <span class="bib-note">Reference repository of evaluation datasets.</span>',
        ],
    },
])

add('part-14-designing-llm-agent-products/module-71-tools-of-the-trade/section-71.4.html', [
    {
        'h3': 'Product Models',
        'h3_id': 'models',
        'entries': [
            'OpenAI (2024). "GPT-4o System Card." <a href="https://openai.com/index/gpt-4o-system-card/" rel="noopener" target="_blank">openai.com/index/gpt-4o-system-card</a>. <span class="bib-note">Reference closed-source product LLM.</span>',
            'Anthropic (2024). "Claude 3.5 Sonnet Model Card." <a href="https://www.anthropic.com/news/claude-3-5-sonnet" rel="noopener" target="_blank">anthropic.com/news/claude-3-5-sonnet</a>. <span class="bib-note">Reference closed-source product LLM.</span>',
        ],
    },
])

# ============================================================
# Module 79: Industry App Tools
# ============================================================
add('part-15-applications-of-llms-across-industries/module-79-tools-of-the-trade/section-79.1.html', [
    {
        'h3': 'Industry Platforms',
        'h3_id': 'platforms',
        'entries': [
            'Microsoft (2024). "Azure OpenAI Service." <a href="https://learn.microsoft.com/azure/ai-services/openai/" rel="noopener" target="_blank">learn.microsoft.com/azure/ai-services/openai</a>. <span class="bib-note">Reference enterprise LLM platform with HIPAA/SOC2 compliance.</span>',
            'AWS (2024). "Amazon Bedrock." <a href="https://aws.amazon.com/bedrock/" rel="noopener" target="_blank">aws.amazon.com/bedrock</a>. <span class="bib-note">Reference enterprise multi-model LLM platform.</span>',
            'Google Cloud (2024). "Vertex AI." <a href="https://cloud.google.com/vertex-ai" rel="noopener" target="_blank">cloud.google.com/vertex-ai</a>. <span class="bib-note">Reference enterprise LLM and ML platform.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-79-tools-of-the-trade/section-79.2.html', [
    {
        'h3': 'Industry Libraries',
        'h3_id': 'libraries',
        'entries': [
            'LangChain (2024). "LangChain Industry Templates." <a href="https://python.langchain.com/docs/get_started/introduction" rel="noopener" target="_blank">python.langchain.com</a>. <span class="bib-note">Reference templates for industry-specific RAG and agent flows.</span>',
            'LlamaIndex (2024). "LlamaIndex Documentation." <a href="https://docs.llamaindex.ai/" rel="noopener" target="_blank">docs.llamaindex.ai</a>. <span class="bib-note">Reference framework for document-grounded industry applications.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-79-tools-of-the-trade/section-79.3.html', [
    {
        'h3': 'Industry Benchmarks',
        'h3_id': 'benchmarks',
        'entries': [
            'Guha, N., et al. (2023). "LegalBench." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2308.11462" rel="noopener" target="_blank">arXiv:2308.11462</a>. <span class="bib-note">Reference legal-LLM benchmark.</span>',
            'Singhal, K., et al. (2023). "Med-PaLM Evaluation." <a href="https://arxiv.org/abs/2212.13138" rel="noopener" target="_blank">arXiv:2212.13138</a>. <span class="bib-note">Reference clinical-LLM benchmark methodology.</span>',
            'Xie, Q., et al. (2023). "PIXIU." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2306.05443" rel="noopener" target="_blank">arXiv:2306.05443</a>. <span class="bib-note">Reference finance-LLM benchmark.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-79-tools-of-the-trade/section-79.4.html', [
    {
        'h3': 'Industry Models',
        'h3_id': 'models',
        'entries': [
            'Singhal, K., et al. (2023). "Med-PaLM." <em>Nature 620</em>. <a href="https://arxiv.org/abs/2212.13138" rel="noopener" target="_blank">arXiv:2212.13138</a>. <span class="bib-note">Reference clinical-domain LLM.</span>',
            'Wu, S., et al. (2023). "BloombergGPT." <a href="https://arxiv.org/abs/2303.17564" rel="noopener" target="_blank">arXiv:2303.17564</a>. <span class="bib-note">Reference financial-domain LLM.</span>',
            'Chalkidis, I. (2023). "ChatLAW: Open-Source Legal LLM." <a href="https://arxiv.org/abs/2306.16092" rel="noopener" target="_blank">arXiv:2306.16092</a>. <span class="bib-note">Reference open legal-domain LLM.</span>',
        ],
    },
])
