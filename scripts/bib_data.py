"""Data file holding bibliographies per section file path (POSIX-style, relative to repo root).

The bibliography HTML block is inserted right before <nav class="chapter-nav">.
Format follows the in-book pattern using <div class="bib-ref">...</div> within <div class="bib-entry-card">.
"""

# Each entry: relative POSIX path => full HTML block (already wrapped in <details>...</details>)
BIBLIOGRAPHIES = {}


def bib_block(sections):
    """Build a full bibliography block.

    sections is a list of dicts: { 'h3': str, 'h3_id': str, 'entries': [str_html, ...] }
    Each entry is the inner HTML for a bib-ref div.
    """
    parts = ['<details class="bibliography-collapsible">',
             '<summary><strong>Further Reading</strong></summary>',
             '<section class="bibliography">']
    for s in sections:
        parts.append(f'<h3 id="{s["h3_id"]}">{s["h3"]}</h3>')
        for entry_html in s['entries']:
            parts.append('<div class="bib-entry-card">')
            parts.append(f'<div class="bib-ref">{entry_html}</div>')
            parts.append('</div>')
    parts.append('</section>')
    parts.append('</details>')
    return '\n'.join(parts)


def add(path, sections):
    BIBLIOGRAPHIES[path] = bib_block(sections)


# ============================================================
# Appendix A: Mathematical Foundations
# ============================================================

add('appendices/appendix-a-mathematical-foundations/section-a.1.html', [
    {
        'h3': 'Foundational Textbooks',
        'h3_id': 'foundational',
        'entries': [
            'Strang, G. (2016). <em>Introduction to Linear Algebra</em> (5th ed.). Wellesley-Cambridge Press. <span class="bib-note">The standard undergraduate reference; chapters on eigenvalues, SVD, and projection underpin every embedding and attention computation in this book.</span>',
            'Trefethen, L. N., &amp; Bau, D. (1997). <em>Numerical Linear Algebra</em>. SIAM. <a href="https://people.maths.ox.ac.uk/trefethen/text.html" rel="noopener" target="_blank">people.maths.ox.ac.uk/trefethen/text.html</a>. <span class="bib-note">The reference for numerically stable algorithms; relevant to mixed-precision training and inference quantization.</span>',
            'Golub, G. H., &amp; Van Loan, C. F. (2013). <em>Matrix Computations</em> (4th ed.). Johns Hopkins University Press. <span class="bib-note">Encyclopedic reference for matrix algorithms; the source for FlashAttention-style tiling analyses.</span>',
        ],
    },
    {
        'h3': 'Modern Treatments for ML',
        'h3_id': 'modern',
        'entries': [
            'Deisenroth, M. P., Faisal, A. A., &amp; Ong, C. S. (2020). <em>Mathematics for Machine Learning</em>. Cambridge University Press. <a href="https://mml-book.github.io/" rel="noopener" target="_blank">mml-book.github.io</a>. <span class="bib-note">Free online textbook; covers the linear algebra and probability prerequisites for modern deep learning.</span>',
            'Petersen, K. B., &amp; Pedersen, M. S. (2012). "The Matrix Cookbook." <a href="https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf" rel="noopener" target="_blank">Matrix Cookbook (PDF)</a>. <span class="bib-note">Concise reference of matrix derivative identities used throughout backpropagation derivations.</span>',
            'Goodfellow, I., Bengio, Y., &amp; Courville, A. (2016). <em>Deep Learning</em>. MIT Press. Chapter 2: Linear Algebra. <a href="https://www.deeplearningbook.org/" rel="noopener" target="_blank">deeplearningbook.org</a>. <span class="bib-note">Linear-algebra primer tuned specifically to deep learning notation and conventions.</span>',
        ],
    },
])

add('appendices/appendix-a-mathematical-foundations/section-a.2.html', [
    {
        'h3': 'Foundational Textbooks',
        'h3_id': 'foundational',
        'entries': [
            'Wasserman, L. (2004). <em>All of Statistics: A Concise Course in Statistical Inference</em>. Springer. <span class="bib-note">A graduate-level survey of probability and statistics that is small enough to actually finish; matches the level of treatment used in this appendix.</span>',
            'Bishop, C. M. (2006). <em>Pattern Recognition and Machine Learning</em>. Springer. <span class="bib-note">Chapter 1 and 2 cover the probability theory used in modern ML; the canonical reference for Bayesian formulations of classification and regression.</span>',
            'Murphy, K. P. (2022). <em>Probabilistic Machine Learning: An Introduction</em>. MIT Press. <a href="https://probml.github.io/pml-book/book1.html" rel="noopener" target="_blank">probml.github.io/pml-book</a>. <span class="bib-note">Up-to-date free textbook; probability chapters connect directly to language-model likelihoods and information-theoretic objectives.</span>',
        ],
    },
    {
        'h3': 'Modern Treatments for ML',
        'h3_id': 'modern',
        'entries': [
            'Hastie, T., Tibshirani, R., &amp; Friedman, J. (2009). <em>The Elements of Statistical Learning</em> (2nd ed.). Springer. <a href="https://hastie.su.domains/ElemStatLearn/" rel="noopener" target="_blank">hastie.su.domains/ElemStatLearn</a>. <span class="bib-note">The standard graduate-level statistics-for-ML reference; covers the bias-variance tradeoff in detail.</span>',
            'Mohri, M., Rostamizadeh, A., &amp; Talwalkar, A. (2018). <em>Foundations of Machine Learning</em> (2nd ed.). MIT Press. <span class="bib-note">The reference for PAC learning bounds and concentration inequalities used in modern scaling-law derivations.</span>',
        ],
    },
])

add('appendices/appendix-a-mathematical-foundations/section-a.3.html', [
    {
        'h3': 'Foundational Texts',
        'h3_id': 'foundational',
        'entries': [
            'Strang, G. (2017). <em>Calculus</em> (2nd ed.). Wellesley-Cambridge Press. <a href="https://ocw.mit.edu/courses/res-18-001-calculus-fall-2023/pages/textbook/" rel="noopener" target="_blank">MIT OCW</a>. <span class="bib-note">Strang\'s calculus text is the prerequisite material; the backpropagation chapter relies on multivariate chain rule fluency.</span>',
            'Boyd, S., &amp; Vandenberghe, L. (2004). <em>Convex Optimization</em>. Cambridge University Press. <a href="https://web.stanford.edu/~boyd/cvxbook/" rel="noopener" target="_blank">web.stanford.edu/~boyd/cvxbook</a>. <span class="bib-note">The standard optimization reference; the LP/QP framework underpins most ML training analyses even when the actual loss is non-convex.</span>',
        ],
    },
    {
        'h3': 'Backpropagation and Automatic Differentiation',
        'h3_id': 'autodiff',
        'entries': [
            'Baydin, A. G., Pearlmutter, B. A., Radul, A. A., &amp; Siskind, J. M. (2018). "Automatic Differentiation in Machine Learning: a Survey." <em>JMLR 18:153</em>. <a href="https://arxiv.org/abs/1502.05767" rel="noopener" target="_blank">arXiv:1502.05767</a>. <span class="bib-note">Reverse-mode autodiff is the engine that makes deep learning practical; this is the standard survey.</span>',
            'Rumelhart, D. E., Hinton, G. E., &amp; Williams, R. J. (1986). "Learning representations by back-propagating errors." <em>Nature 323, 533-536</em>. <span class="bib-note">The original backpropagation paper; the foundation of modern neural-network training.</span>',
            'Kingma, D. P., &amp; Ba, J. (2014). "Adam: A Method for Stochastic Optimization." <em>ICLR 2015</em>. <a href="https://arxiv.org/abs/1412.6980" rel="noopener" target="_blank">arXiv:1412.6980</a>. <span class="bib-note">The optimizer used in essentially every modern LLM; understanding its update rule requires the calculus in this section.</span>',
        ],
    },
])

add('appendices/appendix-a-mathematical-foundations/section-a.4.html', [
    {
        'h3': 'Foundational Texts',
        'h3_id': 'foundational',
        'entries': [
            'Shannon, C. E. (1948). "A Mathematical Theory of Communication." <em>Bell System Technical Journal 27</em>. <a href="https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf" rel="noopener" target="_blank">Shannon 1948 (PDF)</a>. <span class="bib-note">The founding paper of information theory; entropy, mutual information, and channel capacity all originate here.</span>',
            'Cover, T. M., &amp; Thomas, J. A. (2006). <em>Elements of Information Theory</em> (2nd ed.). Wiley. <span class="bib-note">The standard graduate textbook; chapters on KL divergence and entropy underpin every language-model objective.</span>',
            'MacKay, D. J. C. (2003). <em>Information Theory, Inference, and Learning Algorithms</em>. Cambridge University Press. <a href="https://www.inference.org.uk/itila/book.html" rel="noopener" target="_blank">inference.org.uk/itila</a>. <span class="bib-note">Free textbook that connects information theory directly to Bayesian inference and to neural networks.</span>',
        ],
    },
    {
        'h3': 'Modern Applications',
        'h3_id': 'modern',
        'entries': [
            'Tishby, N., &amp; Zaslavsky, N. (2015). "Deep Learning and the Information Bottleneck Principle." <em>IEEE Information Theory Workshop</em>. <a href="https://arxiv.org/abs/1503.02406" rel="noopener" target="_blank">arXiv:1503.02406</a>. <span class="bib-note">Information bottleneck framing of representation learning; influential perspective on what deep networks compress.</span>',
        ],
    },
])

add('appendices/appendix-a-mathematical-foundations/section-a.6.html', [
    {
        'h3': 'Foundational Texts',
        'h3_id': 'foundational',
        'entries': [
            'Shannon, C. E. (1948). "A Mathematical Theory of Communication." <em>Bell System Technical Journal 27</em>. <a href="https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf" rel="noopener" target="_blank">Shannon 1948 (PDF)</a>. <span class="bib-note">Defines entropy and cross-entropy; the loss function used in language-model training comes directly from this paper.</span>',
            'Cover, T. M., &amp; Thomas, J. A. (2006). <em>Elements of Information Theory</em> (2nd ed.). Wiley. <span class="bib-note">Standard reference for KL divergence, mutual information, and channel coding theorems.</span>',
        ],
    },
    {
        'h3': 'Language Model Applications',
        'h3_id': 'lm-applications',
        'entries': [
            'Brown, P. F., Della Pietra, V. J., Mercer, R. L., Della Pietra, S. A., &amp; Lai, J. C. (1992). "An Estimate of an Upper Bound for the Entropy of English." <em>Computational Linguistics 18(1)</em>. <a href="https://aclanthology.org/J92-1002/" rel="noopener" target="_blank">aclanthology.org/J92-1002</a>. <span class="bib-note">Classic estimate of natural-language entropy that sets the theoretical floor for compression and language-model perplexity.</span>',
            'Jelinek, F. (1997). <em>Statistical Methods for Speech Recognition</em>. MIT Press. <span class="bib-note">Defines perplexity and cross-entropy for language models; the foundation of pre-2017 LM evaluation.</span>',
            'Bahdanau, D., Cho, K., &amp; Bengio, Y. (2014). "Neural Machine Translation by Jointly Learning to Align and Translate." <em>ICLR 2015</em>. <a href="https://arxiv.org/abs/1409.0473" rel="noopener" target="_blank">arXiv:1409.0473</a>. <span class="bib-note">First attention mechanism; the soft alignment can be read as a mutual-information weighting between source and target tokens.</span>',
        ],
    },
])

# ============================================================
# Part 10: Security
# ============================================================

add('part-10-llm-security-runtime-safety/module-47-adversarial-security-red-team/section-47.3.html', [
    {
        'h3': 'Supply Chain and Provenance',
        'h3_id': 'supply-chain',
        'entries': [
            'Carlini, N., Jagielski, M., Choquette-Choo, C. A., et al. (2023). "Poisoning Web-Scale Training Datasets is Practical." <em>S&amp;P 2024</em>. <a href="https://arxiv.org/abs/2302.10149" rel="noopener" target="_blank">arXiv:2302.10149</a>. <span class="bib-note">Quantifies data-poisoning costs at web scale; the canonical reference for why training-set supply chain matters.</span>',
            'Hugging Face (2024). "Sigstore-based Model Signing on the Hub." <em>HF Blog</em>. <a href="https://huggingface.co/blog/security-sigstore" rel="noopener" target="_blank">huggingface.co/blog/security-sigstore</a>. <span class="bib-note">Describes the Sigstore-based signing flow that Hub adopted in 2024 for verifiable model provenance.</span>',
            'OpenSSF (2024). "Model Signing Specification." <a href="https://github.com/sigstore/model-transparency" rel="noopener" target="_blank">github.com/sigstore/model-transparency</a>. <span class="bib-note">Reference implementation of the SLSA-for-ML signing workflow used by Hugging Face and other registries.</span>',
        ],
    },
    {
        'h3': 'Confidential Compute',
        'h3_id': 'confidential',
        'entries': [
            'NVIDIA (2024). "Confidential Computing on H100 and H200." <em>NVIDIA Developer Documentation</em>. <a href="https://developer.nvidia.com/blog/confidential-computing-on-h100-gpus" rel="noopener" target="_blank">developer.nvidia.com/blog/confidential-computing-on-h100-gpus</a>. <span class="bib-note">Reference for GPU-side TEEs; the architectural basis for confidential LLM inference.</span>',
            'Costan, V., &amp; Devadas, S. (2016). "Intel SGX Explained." <em>IACR ePrint 2016/086</em>. <a href="https://eprint.iacr.org/2016/086" rel="noopener" target="_blank">eprint.iacr.org/2016/086</a>. <span class="bib-note">The original technical treatment of trusted execution environments; foundational for Azure Confidential Computing and AWS Nitro Enclaves.</span>',
        ],
    },
    {
        'h3': 'Multimodal Attacks',
        'h3_id': 'multimodal',
        'entries': [
            'Bagdasaryan, E., Hsieh, T.-Y., Nassi, B., &amp; Shmatikov, V. (2023). "Abusing Images and Sounds for Indirect Instruction Injection in Multi-Modal LLMs." <a href="https://arxiv.org/abs/2307.10490" rel="noopener" target="_blank">arXiv:2307.10490</a>. <span class="bib-note">Demonstrates pixel-level prompt injection on vision-language models; canonical reference for the multimodal threat surface.</span>',
            'Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., &amp; Fritz, M. (2023). "Not what you\'ve signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." <em>AISec 2023</em>. <a href="https://arxiv.org/abs/2302.12173" rel="noopener" target="_blank">arXiv:2302.12173</a>. <span class="bib-note">Indirect prompt injection through retrieved content; the canonical reference for the threat model that extends to images and audio.</span>',
        ],
    },
])

add('part-10-llm-security-runtime-safety/module-50-privacy-data-protection/section-50.3.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'McMahan, B., Moore, E., Ramage, D., Hampson, S., &amp; Aguera y Arcas, B. (2017). "Communication-Efficient Learning of Deep Networks from Decentralized Data." <em>AISTATS 2017</em>. <a href="https://arxiv.org/abs/1602.05629" rel="noopener" target="_blank">arXiv:1602.05629</a>. <span class="bib-note">The original FedAvg paper that defined federated learning.</span>',
            'Kairouz, P., McMahan, H. B., et al. (2021). "Advances and Open Problems in Federated Learning." <em>Foundations and Trends in ML</em>. <a href="https://arxiv.org/abs/1912.04977" rel="noopener" target="_blank">arXiv:1912.04977</a>. <span class="bib-note">Comprehensive survey of the federated-learning research agenda; the standard reference for system designers.</span>',
            'Bonawitz, K., Eichner, H., Grieskamp, W., et al. (2019). "Towards Federated Learning at Scale: System Design." <em>SysML 2019</em>. <a href="https://arxiv.org/abs/1902.01046" rel="noopener" target="_blank">arXiv:1902.01046</a>. <span class="bib-note">Google\'s production FL system; the architecture reference for cross-device deployments.</span>',
        ],
    },
    {
        'h3': 'Federated LLM Training',
        'h3_id': 'federated-llm',
        'entries': [
            'Zhang, Z., Yang, Y., Dai, Y., et al. (2024). "FedLLM: Communication-Efficient Federated Fine-Tuning of LLMs." <a href="https://arxiv.org/abs/2404.06448" rel="noopener" target="_blank">arXiv:2404.06448</a>. <span class="bib-note">Federated LoRA fine-tuning that minimizes upload bandwidth; the most-cited 2024 federated-LLM paper.</span>',
            'Flower Labs (2024). "Flower: A Friendly Federated Learning Framework." <a href="https://flower.ai" rel="noopener" target="_blank">flower.ai</a>. <span class="bib-note">The leading open-source FL framework; supports PyTorch, TensorFlow, and Hugging Face Transformers.</span>',
        ],
    },
    {
        'h3': 'Privacy and Security',
        'h3_id': 'privacy',
        'entries': [
            'Dwork, C., &amp; Roth, A. (2014). <em>The Algorithmic Foundations of Differential Privacy</em>. <a href="https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf" rel="noopener" target="_blank">cis.upenn.edu/~aaroth/privacybook</a>. <span class="bib-note">The standard reference; FedAvg with differential privacy is the deployable baseline.</span>',
        ],
    },
])

# ============================================================
# Part 12: Systems at Scale
# ============================================================

add('part-12-llm-systems-at-scale/module-57-compute-planning/section-57.1.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'Pope, R., Douglas, S., Chowdhery, A., et al. (2023). "Efficiently Scaling Transformer Inference." <em>MLSys 2023</em>. <a href="https://arxiv.org/abs/2211.05102" rel="noopener" target="_blank">arXiv:2211.05102</a>. <span class="bib-note">The most influential paper on inference sizing; introduces the Pareto frontier between latency, throughput, and cost.</span>',
            'Kwon, W., Li, Z., Zhuang, S., et al. (2023). "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM). <em>SOSP 2023</em>. <a href="https://arxiv.org/abs/2309.06180" rel="noopener" target="_blank">arXiv:2309.06180</a>. <span class="bib-note">Introduces KV-cache paging; the architecture used by all modern inference servers and the basis for tier-by-tier sizing math.</span>',
        ],
    },
    {
        'h3': 'Hardware and Capacity',
        'h3_id': 'hardware',
        'entries': [
            'Patterson, D., Gonzalez, J., Le, Q., et al. (2021). "Carbon Emissions and Large Neural Network Training." <a href="https://arxiv.org/abs/2104.10350" rel="noopener" target="_blank">arXiv:2104.10350</a>. <span class="bib-note">Methodology for quantifying compute and carbon cost of training runs; underlies any honest hardware-cost analysis.</span>',
            'NVIDIA (2024). "Blackwell Architecture Whitepaper." <a href="https://resources.nvidia.com/en-us-blackwell-architecture" rel="noopener" target="_blank">resources.nvidia.com/en-us-blackwell-architecture</a>. <span class="bib-note">Official spec for B200/B300; the 2026 top-tier hardware.</span>',
            'NVIDIA (2024). "Hopper Architecture Whitepaper (H100/H200)." <a href="https://resources.nvidia.com/en-us-tensor-core" rel="noopener" target="_blank">resources.nvidia.com/en-us-tensor-core</a>. <span class="bib-note">Reference for H100/H200 throughput and memory bandwidth used throughout sizing math.</span>',
        ],
    },
    {
        'h3': 'Surveys',
        'h3_id': 'surveys',
        'entries': [
            'Miao, X., Oliaro, G., Zhang, Z., et al. (2023). "Towards Efficient Generative LLM Serving: A Survey." <a href="https://arxiv.org/abs/2312.15234" rel="noopener" target="_blank">arXiv:2312.15234</a>. <span class="bib-note">Catalogues efficient-serving techniques that govern capacity planning: continuous batching, paged attention, speculative decoding, quantization.</span>',
        ],
    },
])

add('part-12-llm-systems-at-scale/module-57-compute-planning/section-57.2.html', [
    {
        'h3': 'Enterprise Architecture',
        'h3_id': 'enterprise',
        'entries': [
            'Hohpe, G., &amp; Woolf, B. (2003). <em>Enterprise Integration Patterns</em>. Addison-Wesley. <span class="bib-note">The canonical reference; the message-routing patterns map directly to modern LLM-orchestration designs.</span>',
            'Conway, M. E. (1968). "How Do Committees Invent?" <em>Datamation</em>. <a href="https://www.melconway.com/Home/Committees_Paper.html" rel="noopener" target="_blank">melconway.com/Committees_Paper</a>. <span class="bib-note">The original statement of Conway\'s Law; explains why enterprise LLM integration is governed by org-chart boundaries.</span>',
        ],
    },
    {
        'h3': 'Identity and Compliance',
        'h3_id': 'identity',
        'entries': [
            'NIST (2020). "Zero Trust Architecture." <em>NIST SP 800-207</em>. <a href="https://csrc.nist.gov/pubs/sp/800/207/final" rel="noopener" target="_blank">csrc.nist.gov/pubs/sp/800/207</a>. <span class="bib-note">The reference identity-and-access framework that defines the modern enterprise security envelope around LLM services.</span>',
            'OWASP (2024). "Top 10 for LLM Applications." <a href="https://owasp.org/www-project-top-10-for-large-language-model-applications/" rel="noopener" target="_blank">owasp.org/www-project-top-10-for-large-language-model-applications</a>. <span class="bib-note">Risk taxonomy that informs enterprise compliance reviews of LLM products.</span>',
        ],
    },
    {
        'h3': 'Cloud and SaaS Integration',
        'h3_id': 'cloud',
        'entries': [
            'Microsoft (2024). "Azure OpenAI Service: Enterprise-Grade Generative AI." <a href="https://learn.microsoft.com/azure/ai-services/openai/" rel="noopener" target="_blank">learn.microsoft.com/azure/ai-services/openai</a>. <span class="bib-note">Reference for SOC2/HIPAA-compliant LLM API integration; covers private endpoints and managed identities.</span>',
            'AWS (2024). "Amazon Bedrock and PrivateLink." <a href="https://aws.amazon.com/bedrock/" rel="noopener" target="_blank">aws.amazon.com/bedrock</a>. <span class="bib-note">Reference for the VPC-isolated LLM-as-a-service pattern that dominates regulated enterprise deployments.</span>',
        ],
    },
])

add('part-12-llm-systems-at-scale/module-57-compute-planning/section-57.3.html', [
    {
        'h3': 'GPU Economics',
        'h3_id': 'gpu-economics',
        'entries': [
            'Cottier, B., Rahman, R., Fattorini, L., et al. (2024). "The rising costs of training frontier AI models." Epoch AI. <a href="https://arxiv.org/abs/2405.21015" rel="noopener" target="_blank">arXiv:2405.21015</a>. <span class="bib-note">Empirical study of frontier-model training costs; the right reference for benchmarking GPU procurement decisions.</span>',
            'Patterson, D., Gonzalez, J., Le, Q., et al. (2021). "Carbon Emissions and Large Neural Network Training." <a href="https://arxiv.org/abs/2104.10350" rel="noopener" target="_blank">arXiv:2104.10350</a>. <span class="bib-note">Compute-cost methodology that translates GPU-hour pricing into total project budget.</span>',
        ],
    },
    {
        'h3': 'Spot and Reserved Markets',
        'h3_id': 'markets',
        'entries': [
            'AWS (2024). "Amazon EC2 Spot Best Practices." <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-best-practices.html" rel="noopener" target="_blank">docs.aws.amazon.com/AWSEC2/spot-best-practices</a>. <span class="bib-note">The canonical reference for spot-instance procurement; the math applies to all spot markets.</span>',
            'SF Compute (2024). "Auction-Based Compute Procurement." <a href="https://sfcompute.com" rel="noopener" target="_blank">sfcompute.com</a>. <span class="bib-note">2024 reference for the multi-GPU spot-auction model that has reshaped academic training economics.</span>',
        ],
    },
    {
        'h3': 'Industry Reports',
        'h3_id': 'reports',
        'entries': [
            'Stanford HAI (2024). "AI Index Report 2024." <a href="https://aiindex.stanford.edu/report/" rel="noopener" target="_blank">aiindex.stanford.edu/report</a>. <span class="bib-note">Annual benchmark on training-compute costs by model size; the standard procurement-planning reference.</span>',
        ],
    },
])

# ============================================================
# Part 13: LLMOps / Containers
# ============================================================

add('part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.1.html', [
    {
        'h3': 'Foundational Sources',
        'h3_id': 'foundational',
        'entries': [
            'Docker Inc. (2024). "Docker Documentation." <a href="https://docs.docker.com/" rel="noopener" target="_blank">docs.docker.com</a>. <span class="bib-note">The official reference for image/container/volume semantics; the source of truth when behavior is ambiguous.</span>',
            'Merkel, D. (2014). "Docker: Lightweight Linux Containers for Consistent Development and Deployment." <em>Linux Journal 239</em>. <a href="https://dl.acm.org/doi/10.5555/2600239.2600241" rel="noopener" target="_blank">dl.acm.org/doi/10.5555/2600239.2600241</a>. <span class="bib-note">The original Docker paper; useful historical context for why container layering looks the way it does.</span>',
        ],
    },
    {
        'h3': 'Container Internals',
        'h3_id': 'internals',
        'entries': [
            'Open Containers Initiative (2024). "OCI Runtime Specification." <a href="https://github.com/opencontainers/runtime-spec" rel="noopener" target="_blank">github.com/opencontainers/runtime-spec</a>. <span class="bib-note">The standard that Docker, containerd, and CRI-O all implement; defines what a "container" formally is.</span>',
            'Burns, B., Beda, J., &amp; Hightower, K. (2022). <em>Kubernetes: Up and Running</em> (3rd ed.). O\'Reilly. <span class="bib-note">Chapter 1 on container basics is a clear high-level treatment of why containers are useful for ML workloads.</span>',
        ],
    },
    {
        'h3': 'ML Container Patterns',
        'h3_id': 'ml-containers',
        'entries': [
            'NVIDIA (2024). "NGC Container Catalog." <a href="https://catalog.ngc.nvidia.com/" rel="noopener" target="_blank">catalog.ngc.nvidia.com</a>. <span class="bib-note">Reference catalog of GPU-ready ML containers; the default base images for PyTorch, TensorFlow, and Triton.</span>',
            'NVIDIA (2024). "NVIDIA Container Toolkit." <a href="https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/" rel="noopener" target="_blank">docs.nvidia.com/datacenter/cloud-native/container-toolkit</a>. <span class="bib-note">The runtime hook that exposes GPUs to containers; required reading for any LLM dockerfile.</span>',
        ],
    },
])

add('part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.2.html', [
    {
        'h3': 'Foundational Sources',
        'h3_id': 'foundational',
        'entries': [
            'Docker Inc. (2024). "Dockerfile Reference." <a href="https://docs.docker.com/engine/reference/builder/" rel="noopener" target="_blank">docs.docker.com/engine/reference/builder</a>. <span class="bib-note">Authoritative reference for every Dockerfile directive; the source of truth for multi-stage builds and BuildKit.</span>',
            'Docker Inc. (2024). "BuildKit Best Practices." <a href="https://docs.docker.com/build/buildkit/" rel="noopener" target="_blank">docs.docker.com/build/buildkit</a>. <span class="bib-note">Cache-mount and inline secret patterns; required for efficient CUDA/PyTorch image builds.</span>',
        ],
    },
    {
        'h3': 'ML Image Recipes',
        'h3_id': 'recipes',
        'entries': [
            'NVIDIA (2024). "NGC PyTorch Container." <a href="https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch" rel="noopener" target="_blank">catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch</a>. <span class="bib-note">The reference PyTorch CUDA image used as a base layer for production LLM training; pin to a specific tag in your Dockerfile.</span>',
            'Anyscale (2024). "Ray Docker Images." <a href="https://docs.ray.io/en/latest/cluster/kubernetes/k8s-ecosystem/operator.html" rel="noopener" target="_blank">docs.ray.io/cluster/kubernetes/k8s-ecosystem/operator</a>. <span class="bib-note">Reference for Ray-on-Kubernetes images; the canonical pattern for distributed-training containers.</span>',
            'vLLM (2024). "Production Deployment with Docker." <a href="https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html" rel="noopener" target="_blank">docs.vllm.ai/serving/deploying_with_docker</a>. <span class="bib-note">Reference vLLM Dockerfile; the template for production inference servers.</span>',
        ],
    },
])

add('part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.3.html', [
    {
        'h3': 'Foundational Sources',
        'h3_id': 'foundational',
        'entries': [
            'Docker Inc. (2024). "Docker Compose Specification." <a href="https://docs.docker.com/compose/compose-file/" rel="noopener" target="_blank">docs.docker.com/compose/compose-file</a>. <span class="bib-note">Official reference for the Compose YAML schema; the source of truth for multi-service service definitions.</span>',
            'Hightower, K. (2017). <em>Kubernetes Up and Running</em>. O\'Reilly. <span class="bib-note">Compose-vs-Kubernetes comparison framing; the standard reference when deciding which orchestrator to use.</span>',
        ],
    },
    {
        'h3': 'LLM Application Patterns',
        'h3_id': 'patterns',
        'entries': [
            'LangChain (2024). "Deploying LangChain Applications with Docker Compose." <a href="https://python.langchain.com/docs/integrations/providers/docker/" rel="noopener" target="_blank">python.langchain.com/docs/integrations/providers/docker</a>. <span class="bib-note">Reference compose recipe for RAG-style multi-service LLM apps with a vector DB and an inference backend.</span>',
            'Chroma (2024). "Chroma Docker Deployment." <a href="https://docs.trychroma.com/deployment/docker" rel="noopener" target="_blank">docs.trychroma.com/deployment/docker</a>. <span class="bib-note">The canonical example of a vector DB container in a Compose stack.</span>',
            'Redis (2024). "Redis Stack with Docker Compose." <a href="https://redis.io/docs/install/install-stack/docker/" rel="noopener" target="_blank">redis.io/docs/install/install-stack/docker</a>. <span class="bib-note">Reference for the Redis cache layer that fronts every production LLM application.</span>',
        ],
    },
])

add('part-13-llmops-lifecycle/module-65-containers-kubernetes/section-65.4.html', [
    {
        'h3': 'Foundational Inference Servers',
        'h3_id': 'foundational',
        'entries': [
            'Kwon, W., Li, Z., Zhuang, S., et al. (2023). "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM). <em>SOSP 2023</em>. <a href="https://arxiv.org/abs/2309.06180" rel="noopener" target="_blank">arXiv:2309.06180</a>. <span class="bib-note">The vLLM paper; explains the paged-attention runtime that all modern production servers build on.</span>',
            'NVIDIA (2024). "TensorRT-LLM and Triton Inference Server." <a href="https://github.com/NVIDIA/TensorRT-LLM" rel="noopener" target="_blank">github.com/NVIDIA/TensorRT-LLM</a>. <span class="bib-note">NVIDIA\'s production stack for serving LLMs; the reference for enterprise multi-model deployments.</span>',
            'Hugging Face (2024). "Text Generation Inference (TGI)." <a href="https://huggingface.co/docs/text-generation-inference/index" rel="noopener" target="_blank">huggingface.co/docs/text-generation-inference</a>. <span class="bib-note">HF\'s production inference server; the reference deployment pattern for the HF ecosystem.</span>',
        ],
    },
    {
        'h3': 'Containerization Patterns',
        'h3_id': 'containerization',
        'entries': [
            'vLLM (2024). "vLLM Official Docker Images." <a href="https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html" rel="noopener" target="_blank">docs.vllm.ai/serving/deploying_with_docker</a>. <span class="bib-note">Reference Dockerfile and runtime flags; the canonical container image for self-hosted inference.</span>',
            'SGLang Project (2024). "SGLang: Structured Generation Language." <a href="https://github.com/sgl-project/sglang" rel="noopener" target="_blank">github.com/sgl-project/sglang</a>. <span class="bib-note">2024-25 alternative to vLLM with RadixAttention prefix caching; faster for structured-output workloads.</span>',
        ],
    },
])

# ============================================================
# Part 14: Designing LLM Agent Products
# ============================================================

add('part-14-designing-llm-agent-products/module-67-ideation/section-67.2.html', [
    {
        'h3': 'Product Discovery Methodology',
        'h3_id': 'discovery',
        'entries': [
            'Cagan, M. (2017). <em>Inspired: How to Create Tech Products Customers Love</em> (2nd ed.). Wiley. <span class="bib-note">The standard reference on product discovery; the "jobs-to-be-done" framing maps directly to LLM problem identification.</span>',
            'Christensen, C. M., Hall, T., Dillon, K., &amp; Duncan, D. S. (2016). <em>Competing Against Luck: The Story of Innovation and Customer Choice</em>. Harper Business. <span class="bib-note">The canonical jobs-to-be-done text; useful framing for picking which LLM problems are worth attacking.</span>',
        ],
    },
    {
        'h3': 'AI Product Strategy',
        'h3_id': 'ai-products',
        'entries': [
            'Agrawal, A., Gans, J., &amp; Goldfarb, A. (2018). <em>Prediction Machines: The Simple Economics of Artificial Intelligence</em>. Harvard Business Review Press. <span class="bib-note">Economic framing for when AI is the right product investment.</span>',
            'Patterson, M., Sculley, D., Holt, G., et al. (2015). "Hidden Technical Debt in Machine Learning Systems." <em>NeurIPS 2015</em>. <a href="https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf" rel="noopener" target="_blank">NeurIPS 2015 PDF</a>. <span class="bib-note">The classic warning about long-term cost of ML products; informs which LLM problems are worth solving.</span>',
        ],
    },
])

add('part-14-designing-llm-agent-products/module-67-ideation/section-67.6.html', [
    {
        'h3': 'UX for AI Products',
        'h3_id': 'ux-ai',
        'entries': [
            'Google PAIR (2023). "People + AI Guidebook." <a href="https://pair.withgoogle.com/guidebook/" rel="noopener" target="_blank">pair.withgoogle.com/guidebook</a>. <span class="bib-note">The most-referenced UX guide for AI products; covers mental models, error states, and explanations.</span>',
            'Amershi, S., Weld, D., Vorvoreanu, M., et al. (2019). "Guidelines for Human-AI Interaction." <em>CHI 2019</em>. <a href="https://dl.acm.org/doi/10.1145/3290605.3300233" rel="noopener" target="_blank">dl.acm.org/doi/10.1145/3290605.3300233</a>. <span class="bib-note">Microsoft Research\'s 18-rule guideline set for human-AI interfaces; the academic foundation for the field.</span>',
        ],
    },
    {
        'h3': 'Iteration Patterns',
        'h3_id': 'iteration',
        'entries': [
            'Ries, E. (2011). <em>The Lean Startup</em>. Crown Business. <span class="bib-note">Build-measure-learn loop; the standard framework that drives LLM-product iteration.</span>',
            'Anthropic (2024). "Building Effective Agents." <a href="https://www.anthropic.com/research/building-effective-agents" rel="noopener" target="_blank">anthropic.com/research/building-effective-agents</a>. <span class="bib-note">Reference patterns for LLM agent UX and iteration; the most-cited 2024 practitioner guide.</span>',
        ],
    },
])

add('part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.3.html', [
    {
        'h3': 'AI-Native IDEs',
        'h3_id': 'ai-ides',
        'entries': [
            'Cursor (2024). "Cursor: The AI Code Editor." <a href="https://cursor.com" rel="noopener" target="_blank">cursor.com</a>. <span class="bib-note">The reference AI-native IDE in 2024-26; defines the chat-plus-edit interaction pattern.</span>',
            'Anthropic (2024). "Claude Code Documentation." <a href="https://docs.claude.com/en/docs/claude-code/overview" rel="noopener" target="_blank">docs.claude.com/claude-code</a>. <span class="bib-note">Terminal-based agentic coding interface; the reference for headless coding agents.</span>',
            'Microsoft (2024). "GitHub Copilot Workspace." <a href="https://github.com/features/copilot-workspace" rel="noopener" target="_blank">github.com/features/copilot-workspace</a>. <span class="bib-note">The enterprise reference for AI-native IDEs; included in many regulated deployments.</span>',
        ],
    },
    {
        'h3': 'Empirical Studies',
        'h3_id': 'studies',
        'entries': [
            'Vaithilingam, P., Zhang, T., &amp; Glassman, E. L. (2022). "Expectation vs. Experience: Evaluating the Usability of Code Generation Tools Powered by Large Language Models." <em>CHI 2022 EA</em>. <a href="https://dl.acm.org/doi/10.1145/3491101.3519665" rel="noopener" target="_blank">dl.acm.org/doi/10.1145/3491101.3519665</a>. <span class="bib-note">Early empirical study of code-LLM UX; the foundation for understanding tool acceptance.</span>',
            'Liang, J. T., Yang, C., &amp; Myers, B. A. (2024). "A Large-Scale Survey on the Usability of AI Programming Assistants: Successes and Challenges." <em>ICSE 2024</em>. <a href="https://arxiv.org/abs/2303.17125" rel="noopener" target="_blank">arXiv:2303.17125</a>. <span class="bib-note">410-developer survey on AI-coding-tool adoption; reference data on what works in practice.</span>',
        ],
    },
])

add('part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.5.html', [
    {
        'h3': 'Software Engineering Patterns',
        'h3_id': 'patterns',
        'entries': [
            'Pirolli, P., &amp; Card, S. (1999). "Information Foraging." <em>Psychological Review 106(4)</em>. <a href="https://www2.parc.com/istl/groups/uir/publications/items/UIR-1999-05-Pirolli-PsychReview-IF.pdf" rel="noopener" target="_blank">parc.com/istl/groups/uir/publications/items/UIR-1999-05-Pirolli-PsychReview-IF.pdf</a>. <span class="bib-note">Information-foraging theory; foundational for vertical-slice prioritization in LLM products.</span>',
            'Fowler, M. (2002). <em>Patterns of Enterprise Application Architecture</em>. Addison-Wesley. <span class="bib-note">Classic reference for slicing applications; the layered patterns map cleanly to LLM-product feature slicing.</span>',
        ],
    },
    {
        'h3': 'LLM Product Design',
        'h3_id': 'llm-design',
        'entries': [
            'Anthropic (2024). "Building Effective Agents." <a href="https://www.anthropic.com/research/building-effective-agents" rel="noopener" target="_blank">anthropic.com/research/building-effective-agents</a>. <span class="bib-note">Argues for "start simple" patterns including single-tool agents and chains; the empirical basis for vertical-slice prototyping.</span>',
            'OpenAI (2024). "A Practical Guide to Building Agents." <a href="https://openai.com/index/practical-guide-to-building-agents/" rel="noopener" target="_blank">openai.com/index/practical-guide-to-building-agents</a>. <span class="bib-note">Reference patterns for agent-product MVPs; complementary to Anthropic\'s guide.</span>',
        ],
    },
])

add('part-14-designing-llm-agent-products/module-68-vibe-coding/section-68.6.html', [
    {
        'h3': 'Pilot and MVP Methodology',
        'h3_id': 'pilots',
        'entries': [
            'Ries, E. (2011). <em>The Lean Startup</em>. Crown Business. <span class="bib-note">Pivot-or-persevere framework; the canonical reference for kill/pivot/keep decisions.</span>',
            'Blank, S. (2013). "Why the Lean Start-Up Changes Everything." <em>Harvard Business Review</em>. <a href="https://hbr.org/2013/05/why-the-lean-start-up-changes-everything" rel="noopener" target="_blank">hbr.org/2013/05/why-the-lean-start-up-changes-everything</a>. <span class="bib-note">Customer-discovery framing for early product decisions; useful for LLM-pilot evaluation.</span>',
        ],
    },
    {
        'h3': 'Enterprise AI Pilots',
        'h3_id': 'enterprise-pilots',
        'entries': [
            'McKinsey &amp; Company (2024). "The State of AI in 2024." <a href="https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai" rel="noopener" target="_blank">mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai</a>. <span class="bib-note">Empirical survey of enterprise AI pilot success rates; the standard data point for go/no-go decisions.</span>',
            'BCG (2024). "Where\'s the Value in AI?" <a href="https://www.bcg.com/publications/2024/wheres-value-in-ai" rel="noopener" target="_blank">bcg.com/publications/2024/wheres-value-in-ai</a>. <span class="bib-note">Industry analysis of pilot-to-production conversion; informs the kill-criteria checklist.</span>',
        ],
    },
])

add('part-14-designing-llm-agent-products/module-69-llm-economics/section-69.1.html', [
    {
        'h3': 'ROI Methodology',
        'h3_id': 'roi',
        'entries': [
            'Brynjolfsson, E., Li, D., &amp; Raymond, L. (2023). "Generative AI at Work." <em>NBER Working Paper 31161</em>. <a href="https://www.nber.org/papers/w31161" rel="noopener" target="_blank">nber.org/papers/w31161</a>. <span class="bib-note">Empirical study of LLM productivity gains in a real call center; the most-cited 2023 paper on AI ROI.</span>',
            'Peng, S., Kalliamvakou, E., Cihon, P., &amp; Demirer, M. (2023). "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot." <a href="https://arxiv.org/abs/2302.06590" rel="noopener" target="_blank">arXiv:2302.06590</a>. <span class="bib-note">Productivity gains from code LLMs; the reference for engineering-productivity ROI claims.</span>',
        ],
    },
    {
        'h3': 'Attribution and Measurement',
        'h3_id': 'attribution',
        'entries': [
            'Pearl, J. (2009). <em>Causality: Models, Reasoning, and Inference</em> (2nd ed.). Cambridge University Press. <span class="bib-note">Foundational reference for causal inference; the source for proper attribution in LLM-driven business outcomes.</span>',
            'Kohavi, R., Tang, D., &amp; Xu, Y. (2020). <em>Trustworthy Online Controlled Experiments</em>. Cambridge University Press. <span class="bib-note">The standard reference for A/B-testing LLM products and measuring incremental value.</span>',
        ],
    },
    {
        'h3': 'Industry Surveys',
        'h3_id': 'surveys',
        'entries': [
            'Stanford HAI (2024). "AI Index Report 2024." <a href="https://aiindex.stanford.edu/report/" rel="noopener" target="_blank">aiindex.stanford.edu/report</a>. <span class="bib-note">Annual benchmark of enterprise LLM-adoption metrics; the standard reference for ROI claims.</span>',
        ],
    },
])

add('part-14-designing-llm-agent-products/module-69-llm-economics/section-69.2.html', [
    {
        'h3': 'Cost Modeling',
        'h3_id': 'cost',
        'entries': [
            'Pope, R., Douglas, S., Chowdhery, A., et al. (2023). "Efficiently Scaling Transformer Inference." <em>MLSys 2023</em>. <a href="https://arxiv.org/abs/2211.05102" rel="noopener" target="_blank">arXiv:2211.05102</a>. <span class="bib-note">The Pareto-frontier paper that informs latency-vs-cost tradeoffs in production LLM economics.</span>',
            'Patterson, D., Gonzalez, J., Le, Q., et al. (2021). "Carbon Emissions and Large Neural Network Training." <a href="https://arxiv.org/abs/2104.10350" rel="noopener" target="_blank">arXiv:2104.10350</a>. <span class="bib-note">Methodology for translating GPU-hour costs into total project economics.</span>',
        ],
    },
    {
        'h3': 'Pricing and Unit Economics',
        'h3_id': 'pricing',
        'entries': [
            'OpenAI (2024). "Pricing." <a href="https://openai.com/pricing" rel="noopener" target="_blank">openai.com/pricing</a>. <span class="bib-note">Reference token-pricing schedule; the input to any unit-economics calculation for API-based LLM products.</span>',
            'Anthropic (2024). "Pricing." <a href="https://www.anthropic.com/pricing" rel="noopener" target="_blank">anthropic.com/pricing</a>. <span class="bib-note">Reference Claude API pricing including prompt caching discounts.</span>',
            'A16z (2023). "Who Owns the Generative AI Platform?" Andreessen Horowitz. <a href="https://a16z.com/who-owns-the-generative-ai-platform/" rel="noopener" target="_blank">a16z.com/who-owns-the-generative-ai-platform</a>. <span class="bib-note">Industry-defining analysis of the generative-AI value chain and margin structure.</span>',
        ],
    },
])

# ============================================================
# Part 15: Industry Applications
# ============================================================

# Chapter 72: Legal LLMs
add('part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.1.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'Magesh, V., Surani, F., Dahl, M., Suzgun, M., Manning, C. D., &amp; Ho, D. E. (2024). "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools." <em>Stanford HAI</em>. <a href="https://arxiv.org/abs/2405.20362" rel="noopener" target="_blank">arXiv:2405.20362</a>. <span class="bib-note">Empirical audit of Westlaw, Lexis, and Casetext; the canonical reference for legal-LLM reliability claims.</span>',
            'Dahl, M., Magesh, V., Suzgun, M., &amp; Ho, D. E. (2024). "Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models." <em>Journal of Legal Analysis</em>. <a href="https://arxiv.org/abs/2401.01301" rel="noopener" target="_blank">arXiv:2401.01301</a>. <span class="bib-note">Reference taxonomy for legal hallucinations; defines the failure modes that production legal LLMs must guard against.</span>',
        ],
    },
    {
        'h3': 'Legal Benchmarks',
        'h3_id': 'benchmarks',
        'entries': [
            'Guha, N., Nyarko, J., Ho, D. E., et al. (2023). "LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2308.11462" rel="noopener" target="_blank">arXiv:2308.11462</a>. <span class="bib-note">The standard benchmark for legal LLM evaluation; covers 162 tasks across legal reasoning categories.</span>',
            'Chalkidis, I., Pasini, T., Zhang, S., et al. (2022). "LexGLUE: A Benchmark Dataset for Legal Language Understanding in English." <em>ACL 2022</em>. <a href="https://arxiv.org/abs/2110.00976" rel="noopener" target="_blank">arXiv:2110.00976</a>. <span class="bib-note">Earlier legal-NLP benchmark; useful for tasks like case classification and statute retrieval.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.2.html', [
    {
        'h3': 'Documented Failures',
        'h3_id': 'failures',
        'entries': [
            'Mata v. Avianca, Inc., 22-CV-1461 (S.D.N.Y. 2023). "Sanctions Order on Fabricated Citations." <a href="https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.54.0.pdf" rel="noopener" target="_blank">CourtListener PDF</a>. <span class="bib-note">The landmark "ChatGPT-cites-fake-cases" sanctions order; the canonical example of legal-LLM failure modes.</span>',
            'Dahl, M., Magesh, V., Suzgun, M., &amp; Ho, D. E. (2024). "Large Legal Fictions." <em>Journal of Legal Analysis</em>. <a href="https://arxiv.org/abs/2401.01301" rel="noopener" target="_blank">arXiv:2401.01301</a>. <span class="bib-note">Taxonomy of legal hallucinations measured across leading LLMs.</span>',
        ],
    },
    {
        'h3': 'Domain Specific Risks',
        'h3_id': 'risks',
        'entries': [
            'Magesh, V., Surani, F., Dahl, M., et al. (2024). "Hallucination-Free?" <a href="https://arxiv.org/abs/2405.20362" rel="noopener" target="_blank">arXiv:2405.20362</a>. <span class="bib-note">Empirical reliability audit of leading commercial legal-LLM tools.</span>',
            'Ho, D. E. (2024). "AI Won\'t Replace Lawyers; Lawyers Using AI Will." <em>Stanford Law School</em>. <a href="https://law.stanford.edu/2024/01/04/ai-wont-replace-lawyers-lawyers-using-ai-will/" rel="noopener" target="_blank">law.stanford.edu/2024/01/04/ai-wont-replace-lawyers-lawyers-using-ai-will</a>. <span class="bib-note">Practitioner framing of the human-in-the-loop requirement in legal-LLM workflows.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.3.html', [
    {
        'h3': 'Bar Regulations',
        'h3_id': 'bar',
        'entries': [
            'American Bar Association (2024). "Formal Opinion 512: Generative AI Tools." ABA. <a href="https://www.americanbar.org/groups/professional_responsibility/publications/professional-responsibility/" rel="noopener" target="_blank">americanbar.org/groups/professional_responsibility</a>. <span class="bib-note">The canonical ABA guidance on lawyer use of generative AI; the regulatory baseline.</span>',
            'New York State Bar Association (2024). "Report on Artificial Intelligence and the Practice of Law." <a href="https://nysba.org/app/uploads/2024/04/Task-Force-Report-on-AI.pdf" rel="noopener" target="_blank">nysba.org Task Force Report</a>. <span class="bib-note">The most-cited state-bar guidance; informs duty-of-competence interpretation for AI use.</span>',
        ],
    },
    {
        'h3': 'Regulatory Frameworks',
        'h3_id': 'regulatory',
        'entries': [
            'European Parliament (2024). "EU AI Act." <a href="https://artificialintelligenceact.eu/" rel="noopener" target="_blank">artificialintelligenceact.eu</a>. <span class="bib-note">The reference regulatory text for high-risk AI systems; classifies legal-LLM tools as high risk.</span>',
            'NIST (2023). "AI Risk Management Framework (AI RMF 1.0)." <em>NIST AI 100-1</em>. <a href="https://www.nist.gov/itl/ai-risk-management-framework" rel="noopener" target="_blank">nist.gov/itl/ai-risk-management-framework</a>. <span class="bib-note">The standard U.S. framework for AI risk assessment that informs legal-tech vendor compliance.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-72-legal-llms/section-72.4.html', [
    {
        'h3': 'Foundational RAG Papers',
        'h3_id': 'foundational',
        'entries': [
            'Lewis, P., Perez, E., Piktus, A., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." <em>NeurIPS 2020</em>. <a href="https://arxiv.org/abs/2005.11401" rel="noopener" target="_blank">arXiv:2005.11401</a>. <span class="bib-note">The original RAG paper; the architectural basis for verified legal retrieval.</span>',
            'Gao, Y., Xiong, Y., Gao, X., et al. (2023). "Retrieval-Augmented Generation for Large Language Models: A Survey." <a href="https://arxiv.org/abs/2312.10997" rel="noopener" target="_blank">arXiv:2312.10997</a>. <span class="bib-note">Comprehensive RAG survey; reference for the verification patterns used in legal RAG.</span>',
        ],
    },
    {
        'h3': 'Legal RAG Systems',
        'h3_id': 'legal-rag',
        'entries': [
            'Magesh, V., et al. (2024). "Hallucination-Free?" <a href="https://arxiv.org/abs/2405.20362" rel="noopener" target="_blank">arXiv:2405.20362</a>. <span class="bib-note">Empirical audit of legal-RAG implementations including Westlaw\'s and Lexis\'s; informs the verified-RAG design.</span>',
            'Casetext (2023). "CoCounsel: Building Trustworthy Legal AI." <a href="https://casetext.com/cocounsel/" rel="noopener" target="_blank">casetext.com/cocounsel</a>. <span class="bib-note">Reference description of a production legal-RAG product including citation verification.</span>',
        ],
    },
])

# Chapter 73: Finance LLMs
add('part-15-applications-of-llms-across-industries/module-73-finance-llms/section-73.1.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'Wu, S., Irsoy, O., Lu, S., et al. (2023). "BloombergGPT: A Large Language Model for Finance." <a href="https://arxiv.org/abs/2303.17564" rel="noopener" target="_blank">arXiv:2303.17564</a>. <span class="bib-note">The reference financial-domain LLM; defines what production finance-LLM looks like.</span>',
            'Yang, H., Liu, X.-Y., &amp; Wang, C. D. (2023). "FinGPT: Open-Source Financial Large Language Models." <a href="https://arxiv.org/abs/2306.06031" rel="noopener" target="_blank">arXiv:2306.06031</a>. <span class="bib-note">The open-source counterpart to BloombergGPT; reference for self-hosted finance LLMs.</span>',
        ],
    },
    {
        'h3': 'Finance Benchmarks',
        'h3_id': 'benchmarks',
        'entries': [
            'Shah, A., Paturi, S., &amp; Chava, S. (2023). "Trillion Dollar Words: A New Financial Dataset, Task &amp; Market Analysis." <em>ACL 2023</em>. <a href="https://aclanthology.org/2023.acl-long.368/" rel="noopener" target="_blank">aclanthology.org/2023.acl-long.368</a>. <span class="bib-note">Reference benchmark for FOMC-statement analysis with LLMs.</span>',
            'Xie, Q., Han, W., Zhang, X., et al. (2023). "PIXIU: A Comprehensive Benchmark, Instruction Dataset and Large Language Model for Finance." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2306.05443" rel="noopener" target="_blank">arXiv:2306.05443</a>. <span class="bib-note">Multi-task financial NLP benchmark; the standard evaluation suite for finance LLMs.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-73-finance-llms/section-73.2.html', [
    {
        'h3': 'Documented Failures',
        'h3_id': 'failures',
        'entries': [
            'Kang, H., &amp; Liu, X.-Y. (2023). "Deficiency of Large Language Models in Finance: An Empirical Examination of Hallucination." <em>NeurIPS 2023 IFM Workshop</em>. <a href="https://arxiv.org/abs/2311.15548" rel="noopener" target="_blank">arXiv:2311.15548</a>. <span class="bib-note">Empirical evidence of LLM hallucination in financial settings.</span>',
            'Lakkaraju, K., Vuruma, S. K. R. J., Pallagani, V., et al. (2023). "Can LLMs be Good Financial Advisors? An Initial Study in Personal Decision Making for Optimized Outcomes." <a href="https://arxiv.org/abs/2307.07422" rel="noopener" target="_blank">arXiv:2307.07422</a>. <span class="bib-note">Reference study on LLM reliability in financial advice; informs the failure-mode catalog.</span>',
        ],
    },
    {
        'h3': 'Market and Regulatory Risks',
        'h3_id': 'risks',
        'entries': [
            'Securities and Exchange Commission (2023). "SEC Proposed Rule: Conflicts of Interest Associated with the Use of Predictive Data Analytics by Broker-Dealers and Investment Advisers." <a href="https://www.sec.gov/rules/proposed/2023/34-97990.pdf" rel="noopener" target="_blank">sec.gov rule 34-97990</a>. <span class="bib-note">SEC\'s 2023 proposed rule on AI-driven investment advice; the regulatory backdrop for finance-LLM deployments.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-73-finance-llms/section-73.3.html', [
    {
        'h3': 'US Financial Regulation',
        'h3_id': 'us-reg',
        'entries': [
            'Securities and Exchange Commission (2023). "Proposed Rule on Predictive Data Analytics." <a href="https://www.sec.gov/rules/proposed/2023/34-97990.pdf" rel="noopener" target="_blank">sec.gov rule 34-97990</a>. <span class="bib-note">SEC\'s 2023 framework for AI in investment advice; the reference U.S. regulatory text.</span>',
            'FinCEN (2024). "AI and Anti-Money-Laundering Guidance." <a href="https://www.fincen.gov/news/news-releases" rel="noopener" target="_blank">fincen.gov/news/news-releases</a>. <span class="bib-note">Reference AML guidance for AI-driven transaction monitoring.</span>',
        ],
    },
    {
        'h3': 'International Frameworks',
        'h3_id': 'international',
        'entries': [
            'European Banking Authority (2024). "Guidelines on the Use of AI in Banking." <a href="https://www.eba.europa.eu/" rel="noopener" target="_blank">eba.europa.eu</a>. <span class="bib-note">EBA\'s reference guidance for AI in EU banking; the regulatory baseline for European finance-LLM deployments.</span>',
            'European Parliament (2024). "EU AI Act." <a href="https://artificialintelligenceact.eu/" rel="noopener" target="_blank">artificialintelligenceact.eu</a>. <span class="bib-note">High-risk classification covers credit-scoring and trading-recommendation LLMs.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-73-finance-llms/section-73.4.html', [
    {
        'h3': 'Trust Architecture',
        'h3_id': 'trust',
        'entries': [
            'NIST (2023). "AI Risk Management Framework (AI RMF 1.0)." <a href="https://www.nist.gov/itl/ai-risk-management-framework" rel="noopener" target="_blank">nist.gov/itl/ai-risk-management-framework</a>. <span class="bib-note">The standard tiered framework for AI risk assessment; the basis for tiered-trust designs.</span>',
            'Federal Reserve (2024). "SR 11-7: Guidance on Model Risk Management." <a href="https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm" rel="noopener" target="_blank">federalreserve.gov/supervisionreg/srletters/sr1107</a>. <span class="bib-note">The canonical Fed reference for model-risk management; the tiered-trust foundation in U.S. banking.</span>',
        ],
    },
    {
        'h3': 'LLM Applications',
        'h3_id': 'llm-apps',
        'entries': [
            'Wu, S., et al. (2023). "BloombergGPT." <a href="https://arxiv.org/abs/2303.17564" rel="noopener" target="_blank">arXiv:2303.17564</a>. <span class="bib-note">Reference implementation of a tiered-trust financial LLM.</span>',
            'JPMorgan Chase (2024). "DocLLM: Multimodal Document Understanding." <a href="https://arxiv.org/abs/2401.00908" rel="noopener" target="_blank">arXiv:2401.00908</a>. <span class="bib-note">Production finance-LLM for document understanding; useful reference for tiered deployment in regulated workflows.</span>',
        ],
    },
])

# Chapter 74: Healthcare LLMs
add('part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.1.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'Singhal, K., Azizi, S., Tu, T., et al. (2023). "Large Language Models Encode Clinical Knowledge" (Med-PaLM). <em>Nature 620</em>. <a href="https://arxiv.org/abs/2212.13138" rel="noopener" target="_blank">arXiv:2212.13138</a>. <span class="bib-note">The reference Med-PaLM paper; sets the standard for clinical-LLM evaluation.</span>',
            'Singhal, K., Tu, T., Gottweis, J., et al. (2023). "Towards Expert-Level Medical Question Answering with Large Language Models" (Med-PaLM 2). <a href="https://arxiv.org/abs/2305.09617" rel="noopener" target="_blank">arXiv:2305.09617</a>. <span class="bib-note">Med-PaLM 2 reference; the basis for expert-level medical QA benchmarks.</span>',
        ],
    },
    {
        'h3': 'Clinical Use Cases',
        'h3_id': 'use-cases',
        'entries': [
            'Tu, T., Palepu, A., Schaekermann, M., et al. (2024). "Towards Conversational Diagnostic AI" (AMIE). <a href="https://arxiv.org/abs/2401.05654" rel="noopener" target="_blank">arXiv:2401.05654</a>. <span class="bib-note">AMIE, Google\'s 2024 conversational diagnostic AI; the reference for clinical-dialogue LLM design.</span>',
            'Ayers, J. W., Poliak, A., Dredze, M., et al. (2023). "Comparing Physician and Artificial Intelligence Chatbot Responses to Patient Questions Posted to a Public Social Media Forum." <em>JAMA Internal Medicine</em>. <a href="https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2804309" rel="noopener" target="_blank">jamanetwork.com/jamainternalmedicine/fullarticle/2804309</a>. <span class="bib-note">Empirical evidence that LLMs can match physician quality and bedside manner; foundational use-case data.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.2.html', [
    {
        'h3': 'Failure Mode Studies',
        'h3_id': 'failures',
        'entries': [
            'Omiye, J. A., Lester, J. C., Spichak, S., Rotemberg, V., &amp; Daneshjou, R. (2023). "Large Language Models Propagate Race-Based Medicine." <em>npj Digital Medicine</em>. <a href="https://www.nature.com/articles/s41746-023-00939-z" rel="noopener" target="_blank">nature.com/articles/s41746-023-00939-z</a>. <span class="bib-note">Empirical demonstration of bias in clinical LLMs; the canonical reference for safety reviews.</span>',
            'Pal, A., Umapathi, L. K., &amp; Sankarasubbu, M. (2023). "Med-HALT: Medical Domain Hallucination Test for Large Language Models." <em>CoNLL 2023</em>. <a href="https://arxiv.org/abs/2307.15343" rel="noopener" target="_blank">arXiv:2307.15343</a>. <span class="bib-note">Domain-specific hallucination benchmark; the reference for evaluating clinical-LLM truthfulness.</span>',
        ],
    },
    {
        'h3': 'Safety Frameworks',
        'h3_id': 'safety',
        'entries': [
            'Goodman, K. E., Yi, P. H., &amp; Morgan, D. J. (2024). "AI-Generated Clinical Summaries Require More Than Accuracy." <em>JAMA</em>. <a href="https://jamanetwork.com/journals/jama/fullarticle/2814313" rel="noopener" target="_blank">jamanetwork.com/jama/fullarticle/2814313</a>. <span class="bib-note">Argues that clinical-LLM evaluation must extend beyond factual accuracy; informs the failure-mode taxonomy.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.3.html', [
    {
        'h3': 'US Regulation',
        'h3_id': 'us-reg',
        'entries': [
            'FDA (2024). "Artificial Intelligence and Machine Learning (AI/ML)-Enabled Medical Devices." <a href="https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices" rel="noopener" target="_blank">fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices</a>. <span class="bib-note">FDA\'s 2024 framework for AI/ML medical devices; the U.S. regulatory baseline.</span>',
            'HHS Office for Civil Rights (2024). "HIPAA Privacy and AI Tools." <a href="https://www.hhs.gov/hipaa/" rel="noopener" target="_blank">hhs.gov/hipaa</a>. <span class="bib-note">HIPAA reference for handling PHI in LLM-based clinical tools.</span>',
        ],
    },
    {
        'h3': 'International Frameworks',
        'h3_id': 'international',
        'entries': [
            'European Parliament (2024). "EU AI Act." <a href="https://artificialintelligenceact.eu/" rel="noopener" target="_blank">artificialintelligenceact.eu</a>. <span class="bib-note">EU AI Act high-risk classifications apply to clinical decision-support systems.</span>',
            'WHO (2024). "Ethics and Governance of Artificial Intelligence for Health." <a href="https://www.who.int/publications/i/item/9789240029200" rel="noopener" target="_blank">who.int/publications/i/item/9789240029200</a>. <span class="bib-note">WHO guidance on AI for health; the international policy reference.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-74-healthcare-llms/section-74.4.html', [
    {
        'h3': 'HIPAA Compliance',
        'h3_id': 'hipaa',
        'entries': [
            'HHS Office for Civil Rights (2024). "Summary of the HIPAA Security Rule." <a href="https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html" rel="noopener" target="_blank">hhs.gov/hipaa/for-professionals/security/laws-regulations</a>. <span class="bib-note">Authoritative source for HIPAA Security Rule requirements that govern LLM deployments handling PHI.</span>',
            'NIST (2008). "An Introductory Resource Guide for Implementing the HIPAA Security Rule." <em>NIST SP 800-66 Rev. 1</em>. <a href="https://csrc.nist.gov/publications/detail/sp/800-66/rev-1/final" rel="noopener" target="_blank">csrc.nist.gov/publications/detail/sp/800-66/rev-1/final</a>. <span class="bib-note">Reference implementation guide for HIPAA-compliant systems.</span>',
        ],
    },
    {
        'h3': 'Deployment Patterns',
        'h3_id': 'deployment',
        'entries': [
            'Microsoft (2024). "Azure OpenAI for Healthcare." <a href="https://learn.microsoft.com/azure/ai-services/openai/" rel="noopener" target="_blank">learn.microsoft.com/azure/ai-services/openai</a>. <span class="bib-note">Reference for HIPAA-eligible LLM deployment with BAA.</span>',
            'AWS (2024). "HIPAA on AWS." <a href="https://aws.amazon.com/compliance/hipaa-compliance/" rel="noopener" target="_blank">aws.amazon.com/compliance/hipaa-compliance</a>. <span class="bib-note">Reference for HIPAA-eligible Bedrock and SageMaker deployments.</span>',
        ],
    },
])

# Chapter 75: Education LLMs
add('part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.1.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'Khan, S. (2023). "Brave New Words: How AI Will Revolutionize Education." Khan Academy. <span class="bib-note">Reference book on AI tutors from Khan Academy\'s leadership; informs the Khanmigo design pattern.</span>',
            'Bloom, B. S. (1984). "The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring." <em>Educational Researcher</em>. <a href="https://www.jstor.org/stable/1175554" rel="noopener" target="_blank">jstor.org/stable/1175554</a>. <span class="bib-note">The foundational paper on tutoring effectiveness; the academic motivation for AI tutoring.</span>',
        ],
    },
    {
        'h3': 'Recent Evaluations',
        'h3_id': 'recent',
        'entries': [
            'Kasneci, E., Sessler, K., Kuchemann, S., et al. (2023). "ChatGPT for Good? On Opportunities and Challenges of Large Language Models for Education." <em>Learning and Individual Differences 103</em>. <a href="https://www.sciencedirect.com/science/article/pii/S1041608023000195" rel="noopener" target="_blank">sciencedirect.com/science/article/pii/S1041608023000195</a>. <span class="bib-note">The most-cited survey of LLMs in education.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.2.html', [
    {
        'h3': 'Documented Failures',
        'h3_id': 'failures',
        'entries': [
            'Bordt, S., Chen, H., Eberle, O., et al. (2023). "ChatGPT Participates, Whereas Top Students Succeed." <a href="https://arxiv.org/abs/2308.03313" rel="noopener" target="_blank">arXiv:2308.03313</a>. <span class="bib-note">Empirical study of LLM performance on university exams; informs the failure-mode catalog.</span>',
        ],
    },
    {
        'h3': 'Risk and Pedagogy',
        'h3_id': 'pedagogy',
        'entries': [
            'Bastani, H., Bastani, O., Sungu, A., et al. (2024). "Generative AI Can Harm Learning." <em>SSRN</em>. <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486" rel="noopener" target="_blank">papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486</a>. <span class="bib-note">Empirical study showing that LLMs can decrease learning when used as answer shortcuts; the canonical reference for the offload failure mode.</span>',
            'Stadler, M., Bannert, M., &amp; Sailer, M. (2024). "Cognitive Ease at a Cost: LLMs Reduce Mental Effort but Compromise Depth in Student Scientific Inquiry." <em>Computers in Human Behavior</em>. <a href="https://www.sciencedirect.com/science/article/pii/S0747563224000189" rel="noopener" target="_blank">sciencedirect.com/science/article/pii/S0747563224000189</a>. <span class="bib-note">Reference study on cognitive shallowing from LLM tutor use.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.3.html', [
    {
        'h3': 'US Education Policy',
        'h3_id': 'us-policy',
        'entries': [
            'U.S. Department of Education (2023). "Artificial Intelligence and the Future of Teaching and Learning." <a href="https://www2.ed.gov/documents/ai-report/ai-report.pdf" rel="noopener" target="_blank">ed.gov AI Report PDF</a>. <span class="bib-note">The Department of Education\'s foundational policy framework for AI in K-12 and higher education.</span>',
            'Family Educational Rights and Privacy Act (FERPA). <a href="https://www2.ed.gov/policy/gen/guid/fpco/ferpa/index.html" rel="noopener" target="_blank">ed.gov/policy/gen/guid/fpco/ferpa</a>. <span class="bib-note">U.S. student privacy law that constrains education-LLM deployments.</span>',
        ],
    },
    {
        'h3': 'International Frameworks',
        'h3_id': 'international',
        'entries': [
            'UNESCO (2023). "Guidance for Generative AI in Education and Research." <a href="https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research" rel="noopener" target="_blank">unesco.org/en/articles/guidance-generative-ai-education-and-research</a>. <span class="bib-note">UNESCO\'s reference policy text on generative AI in education.</span>',
            'European Parliament (2024). "EU AI Act." <a href="https://artificialintelligenceact.eu/" rel="noopener" target="_blank">artificialintelligenceact.eu</a>. <span class="bib-note">EU AI Act high-risk classifications apply to education-related AI used for assessment.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-75-education-llms/section-75.4.html', [
    {
        'h3': 'Pedagogical Foundations',
        'h3_id': 'pedagogy',
        'entries': [
            'Vygotsky, L. S. (1978). <em>Mind in Society: The Development of Higher Psychological Processes</em>. Harvard University Press. <span class="bib-note">Zone of proximal development and scaffolding theory; the pedagogical foundation for tiered tutor designs.</span>',
            'Bloom, B. S. (1984). "The 2 Sigma Problem." <em>Educational Researcher</em>. <a href="https://www.jstor.org/stable/1175554" rel="noopener" target="_blank">jstor.org/stable/1175554</a>. <span class="bib-note">The mastery-learning framework that motivates personalized AI tutoring.</span>',
        ],
    },
    {
        'h3': 'Modern Tutor Systems',
        'h3_id': 'modern',
        'entries': [
            'VanLehn, K. (2011). "The Relative Effectiveness of Human Tutoring, Intelligent Tutoring Systems, and Other Tutoring Systems." <em>Educational Psychologist 46(4)</em>. <a href="https://www.tandfonline.com/doi/abs/10.1080/00461520.2011.611369" rel="noopener" target="_blank">tandfonline.com/doi/abs/10.1080/00461520.2011.611369</a>. <span class="bib-note">Meta-analysis of intelligent tutoring systems; informs the architectural expectations for LLM tutors.</span>',
            'Khan Academy (2024). "Khanmigo Architecture." <a href="https://www.khanacademy.org/khan-labs" rel="noopener" target="_blank">khanacademy.org/khan-labs</a>. <span class="bib-note">Reference description of the deployed Khanmigo tutor architecture.</span>',
        ],
    },
])

# Chapter 76: Cybersecurity LLMs
add('part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.1.html', [
    {
        'h3': 'Defensive LLM Applications',
        'h3_id': 'defensive',
        'entries': [
            'Microsoft (2024). "Microsoft Security Copilot." <a href="https://www.microsoft.com/en-us/security/business/ai-machine-learning/microsoft-security-copilot" rel="noopener" target="_blank">microsoft.com/en-us/security/business/ai-machine-learning/microsoft-security-copilot</a>. <span class="bib-note">Reference commercial security-LLM; defines what a production blue-team LLM looks like.</span>',
            'Crowdstrike (2024). "Charlotte AI for Threat Hunting." <a href="https://www.crowdstrike.com/platform/charlotte-ai-agentic-workflows/" rel="noopener" target="_blank">crowdstrike.com/platform/charlotte-ai-agentic-workflows</a>. <span class="bib-note">Reference for AI-driven SOC automation; the model for LLM-augmented threat hunting.</span>',
        ],
    },
    {
        'h3': 'Empirical Studies',
        'h3_id': 'studies',
        'entries': [
            'Goyal, M., Mehrotra, A., Khanna, A., et al. (2024). "Hacking, Cracking, and Hijacking with LLMs: A Survey of Adversarial Use Cases." <a href="https://arxiv.org/abs/2403.04786" rel="noopener" target="_blank">arXiv:2403.04786</a>. <span class="bib-note">Comprehensive survey of LLM use in cybersecurity, both offensive and defensive.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.2.html', [
    {
        'h3': 'Offensive LLM Capabilities',
        'h3_id': 'offensive',
        'entries': [
            'Fang, R., Bindu, R., Gupta, A., Zhan, Q., &amp; Kang, D. (2024). "LLM Agents can Autonomously Exploit One-day Vulnerabilities." <a href="https://arxiv.org/abs/2404.08144" rel="noopener" target="_blank">arXiv:2404.08144</a>. <span class="bib-note">Empirical demonstration that GPT-4 agents can exploit known vulnerabilities; reference for red-team LLM capabilities.</span>',
            'Fang, R., Bindu, R., Gupta, A., &amp; Kang, D. (2024). "LLM Agents can Autonomously Hack Websites." <a href="https://arxiv.org/abs/2402.06664" rel="noopener" target="_blank">arXiv:2402.06664</a>. <span class="bib-note">Reference paper on autonomous LLM-driven website attacks; the canonical 2024 offensive-LLM result.</span>',
        ],
    },
    {
        'h3': 'Red Team Methodology',
        'h3_id': 'red-team',
        'entries': [
            'MITRE (2024). "ATT&amp;CK Framework." <a href="https://attack.mitre.org" rel="noopener" target="_blank">attack.mitre.org</a>. <span class="bib-note">The standard adversarial-TTPs reference; informs LLM red-team scenario design.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.3.html', [
    {
        'h3': 'LLM Attack Surface',
        'h3_id': 'attack-surface',
        'entries': [
            'OWASP (2024). "Top 10 for LLM Applications." <a href="https://owasp.org/www-project-top-10-for-large-language-model-applications/" rel="noopener" target="_blank">owasp.org/www-project-top-10-for-large-language-model-applications</a>. <span class="bib-note">The reference taxonomy for LLM application risks.</span>',
            'Greshake, K., Abdelnabi, S., Mishra, S., et al. (2023). "Not what you\'ve signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." <em>AISec 2023</em>. <a href="https://arxiv.org/abs/2302.12173" rel="noopener" target="_blank">arXiv:2302.12173</a>. <span class="bib-note">The canonical paper on indirect prompt injection; defines the architectural threat model.</span>',
        ],
    },
    {
        'h3': 'Adversarial Robustness',
        'h3_id': 'robustness',
        'entries': [
            'Zou, A., Wang, Z., Carlini, N., et al. (2023). "Universal and Transferable Adversarial Attacks on Aligned Language Models." <a href="https://arxiv.org/abs/2307.15043" rel="noopener" target="_blank">arXiv:2307.15043</a>. <span class="bib-note">GCG attack; the canonical reference for transferable jailbreaks.</span>',
            'Perez, F., &amp; Ribeiro, I. (2022). "Ignore Previous Prompt: Attack Techniques For Language Models." <a href="https://arxiv.org/abs/2211.09527" rel="noopener" target="_blank">arXiv:2211.09527</a>. <span class="bib-note">Early empirical catalog of prompt-injection attack patterns.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-76-cybersecurity-llms/section-76.4.html', [
    {
        'h3': 'Trust Boundary Foundations',
        'h3_id': 'foundations',
        'entries': [
            'Saltzer, J. H., &amp; Schroeder, M. D. (1975). "The Protection of Information in Computer Systems." <em>Proceedings of the IEEE 63(9)</em>. <a href="https://web.mit.edu/Saltzer/www/publications/protection/" rel="noopener" target="_blank">web.mit.edu/Saltzer/www/publications/protection</a>. <span class="bib-note">The foundational paper on protection mechanisms and trust boundaries.</span>',
            'NIST (2020). "Zero Trust Architecture." <em>NIST SP 800-207</em>. <a href="https://csrc.nist.gov/pubs/sp/800/207/final" rel="noopener" target="_blank">csrc.nist.gov/pubs/sp/800/207</a>. <span class="bib-note">The standard reference for zero-trust system design; the framework that informs LLM trust-boundary thinking.</span>',
        ],
    },
    {
        'h3': 'LLM-Specific Patterns',
        'h3_id': 'llm-patterns',
        'entries': [
            'Greshake, K., et al. (2023). "Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection." <a href="https://arxiv.org/abs/2302.12173" rel="noopener" target="_blank">arXiv:2302.12173</a>. <span class="bib-note">Defines the model boundary between trusted prompt and untrusted retrieved content.</span>',
            'Anthropic (2024). "Building Effective Agents." <a href="https://www.anthropic.com/research/building-effective-agents" rel="noopener" target="_blank">anthropic.com/research/building-effective-agents</a>. <span class="bib-note">Reference patterns for sandboxing LLM tool use behind trust boundaries.</span>',
        ],
    },
])

# Chapter 77: Government LLMs
add('part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.1.html', [
    {
        'h3': 'Government AI Deployment',
        'h3_id': 'government',
        'entries': [
            'U.S. General Services Administration (2024). "AI in Government Use Cases." <a href="https://www.gsa.gov/governmentwide-initiatives/artificial-intelligence" rel="noopener" target="_blank">gsa.gov/governmentwide-initiatives/artificial-intelligence</a>. <span class="bib-note">The reference catalog of U.S. federal AI deployments.</span>',
            'OECD (2024). "AI in Government: Practical Cases from OECD Members." <a href="https://www.oecd.org/governance/digital-government/" rel="noopener" target="_blank">oecd.org/governance/digital-government</a>. <span class="bib-note">International reference catalog of government AI deployments.</span>',
        ],
    },
    {
        'h3': 'Use Case Research',
        'h3_id': 'research',
        'entries': [
            'Engstrom, D. F., Ho, D. E., Sharkey, C. M., &amp; Cuellar, M.-F. (2020). "Government by Algorithm: Artificial Intelligence in Federal Administrative Agencies." Stanford Law School. <a href="https://www-cdn.law.stanford.edu/wp-content/uploads/2020/02/ACUS-AI-Report.pdf" rel="noopener" target="_blank">law.stanford.edu ACUS AI Report</a>. <span class="bib-note">The most-cited academic survey of AI in U.S. federal agencies.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.2.html', [
    {
        'h3': 'Documented Failures',
        'h3_id': 'failures',
        'entries': [
            'Eubanks, V. (2018). <em>Automating Inequality: How High-Tech Tools Profile, Police, and Punish the Poor</em>. St. Martin\'s Press. <span class="bib-note">Reference book on algorithmic-system failures in government services.</span>',
            'AlgorithmWatch (2024). "Automating Society Report." <a href="https://automatingsociety.algorithmwatch.org/" rel="noopener" target="_blank">automatingsociety.algorithmwatch.org</a>. <span class="bib-note">Annual catalog of public-sector algorithmic failures in Europe.</span>',
        ],
    },
    {
        'h3': 'Public Trust',
        'h3_id': 'trust',
        'entries': [
            'Brookings Institution (2024). "Public Trust in Government Use of AI." <a href="https://www.brookings.edu/research/" rel="noopener" target="_blank">brookings.edu/research</a>. <span class="bib-note">Survey research on citizen trust in government LLMs; informs deployment-failure analysis.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.3.html', [
    {
        'h3': 'US Federal Policy',
        'h3_id': 'us-federal',
        'entries': [
            'Executive Office of the President (2023). "Executive Order 14110: Safe, Secure, and Trustworthy Development and Use of Artificial Intelligence." <a href="https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/" rel="noopener" target="_blank">whitehouse.gov EO 14110</a>. <span class="bib-note">The U.S. federal AI executive order; the regulatory baseline for federal AI deployments.</span>',
            'OMB (2024). "M-24-10: Memorandum on Advancing Governance, Innovation, and Risk Management for Agency Use of Artificial Intelligence." <a href="https://www.whitehouse.gov/wp-content/uploads/2024/03/M-24-10-Advancing-Governance-Innovation-and-Risk-Management-for-Agency-Use-of-Artificial-Intelligence.pdf" rel="noopener" target="_blank">whitehouse.gov M-24-10 PDF</a>. <span class="bib-note">The OMB implementation memo; the operational reference for U.S. federal AI compliance.</span>',
        ],
    },
    {
        'h3': 'International Frameworks',
        'h3_id': 'international',
        'entries': [
            'European Parliament (2024). "EU AI Act." <a href="https://artificialintelligenceact.eu/" rel="noopener" target="_blank">artificialintelligenceact.eu</a>. <span class="bib-note">The EU AI Act; public-sector deployments are largely high-risk and require conformity assessments.</span>',
            'OECD (2019). "Recommendation of the Council on Artificial Intelligence." <a href="https://oecd.ai/en/ai-principles" rel="noopener" target="_blank">oecd.ai/en/ai-principles</a>. <span class="bib-note">OECD AI Principles; the multilateral baseline for government AI policy.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-77-government-llms/section-77.4.html', [
    {
        'h3': 'Grounded Assistant Architecture',
        'h3_id': 'grounded',
        'entries': [
            'Lewis, P., Perez, E., Piktus, A., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." <em>NeurIPS 2020</em>. <a href="https://arxiv.org/abs/2005.11401" rel="noopener" target="_blank">arXiv:2005.11401</a>. <span class="bib-note">RAG architecture is the basis for grounded public-sector assistants.</span>',
            'Gao, Y., et al. (2023). "Retrieval-Augmented Generation for Large Language Models: A Survey." <a href="https://arxiv.org/abs/2312.10997" rel="noopener" target="_blank">arXiv:2312.10997</a>. <span class="bib-note">RAG survey covering verification patterns for grounded LLM responses.</span>',
        ],
    },
    {
        'h3': 'Public Sector Implementations',
        'h3_id': 'public-sector',
        'entries': [
            'GSA (2024). "USAi: Government AI Pilot." <a href="https://www.gsa.gov/about-us/newsroom/news-releases" rel="noopener" target="_blank">gsa.gov/about-us/newsroom/news-releases</a>. <span class="bib-note">Reference U.S. federal LLM pilot.</span>',
            'UK Government (2024). "GOV.UK Chat." <a href="https://www.gov.uk/government/news/gov-uk-chatbot" rel="noopener" target="_blank">gov.uk/government/news/gov-uk-chatbot</a>. <span class="bib-note">Reference UK public-sector LLM deployment with citation-anchored answers.</span>',
        ],
    },
])

# Chapter 78: Manufacturing / Misc
add('part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.1.html', [
    {
        'h3': 'Industrial LLM Applications',
        'h3_id': 'industrial',
        'entries': [
            'Siemens (2024). "Industrial Copilot with Microsoft." <a href="https://www.siemens.com/global/en/company/press/copilot-microsoft-ai.html" rel="noopener" target="_blank">siemens.com/global/en/company/press/copilot-microsoft-ai</a>. <span class="bib-note">Reference industrial-AI deployment; the canonical example of manufacturing LLM use.</span>',
            'GE Aerospace (2024). "Predictive Maintenance with Generative AI." <a href="https://www.ge.com/news/" rel="noopener" target="_blank">ge.com/news</a>. <span class="bib-note">Reference industrial-maintenance LLM deployment.</span>',
        ],
    },
    {
        'h3': 'Survey Literature',
        'h3_id': 'surveys',
        'entries': [
            'Wang, J., Zhang, Y., Wang, Y., et al. (2024). "Large Language Models for Manufacturing: A Survey." <a href="https://arxiv.org/abs/2410.21418" rel="noopener" target="_blank">arXiv:2410.21418</a>. <span class="bib-note">Comprehensive survey of manufacturing LLM use cases.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.2.html', [
    {
        'h3': 'Failure Modes in Industrial AI',
        'h3_id': 'failures',
        'entries': [
            'Patterson, M., Sculley, D., Holt, G., et al. (2015). "Hidden Technical Debt in Machine Learning Systems." <em>NeurIPS 2015</em>. <a href="https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf" rel="noopener" target="_blank">NeurIPS 2015 PDF</a>. <span class="bib-note">Reference for the operational debt accumulated by ML systems in industrial settings.</span>',
            'Wang, J., et al. (2024). "Large Language Models for Manufacturing." <a href="https://arxiv.org/abs/2410.21418" rel="noopener" target="_blank">arXiv:2410.21418</a>. <span class="bib-note">Survey covering both successes and failures of manufacturing LLMs.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.3.html', [
    {
        'h3': 'Manufacturing Standards',
        'h3_id': 'standards',
        'entries': [
            'ISO (2018). "ISO 9001: Quality Management Systems." <a href="https://www.iso.org/iso-9001-quality-management.html" rel="noopener" target="_blank">iso.org/iso-9001-quality-management</a>. <span class="bib-note">The international standard for manufacturing quality systems; the regulatory baseline.</span>',
            'IEC (2023). "IEC 61508: Functional Safety of Electrical/Electronic/Programmable Electronic Safety-related Systems." <a href="https://www.iec.ch/functional-safety" rel="noopener" target="_blank">iec.ch/functional-safety</a>. <span class="bib-note">Functional-safety standard relevant to AI-controlled industrial systems.</span>',
        ],
    },
    {
        'h3': 'AI-Specific Frameworks',
        'h3_id': 'ai-frameworks',
        'entries': [
            'NIST (2023). "AI Risk Management Framework." <a href="https://www.nist.gov/itl/ai-risk-management-framework" rel="noopener" target="_blank">nist.gov/itl/ai-risk-management-framework</a>. <span class="bib-note">The U.S. AI risk framework; applies to manufacturing-LLM deployments.</span>',
            'European Parliament (2024). "EU AI Act." <a href="https://artificialintelligenceact.eu/" rel="noopener" target="_blank">artificialintelligenceact.eu</a>. <span class="bib-note">EU classification covers safety-critical manufacturing AI as high-risk.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.6.html', [
    {
        'h3': 'Generative Media',
        'h3_id': 'media',
        'entries': [
            'Rombach, R., Blattmann, A., Lorenz, D., Esser, P., &amp; Ommer, B. (2022). "High-Resolution Image Synthesis with Latent Diffusion Models" (Stable Diffusion). <em>CVPR 2022</em>. <a href="https://arxiv.org/abs/2112.10752" rel="noopener" target="_blank">arXiv:2112.10752</a>. <span class="bib-note">The foundational paper for production image generation in design and marketing pipelines.</span>',
            'OpenAI (2024). "Sora: Creating Video from Text." <a href="https://openai.com/sora" rel="noopener" target="_blank">openai.com/sora</a>. <span class="bib-note">Reference text-to-video model; the canonical 2024 example of LLM-style scaling for video.</span>',
        ],
    },
    {
        'h3': 'Audio and Music',
        'h3_id': 'audio',
        'entries': [
            'Copet, J., Kreuk, F., Gat, I., et al. (2024). "Simple and Controllable Music Generation" (MusicGen). <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2306.05284" rel="noopener" target="_blank">arXiv:2306.05284</a>. <span class="bib-note">Reference open-weight music-generation model; the standard for design-and-marketing audio.</span>',
            'Suno (2024). "Suno V4 Documentation." <a href="https://suno.com" rel="noopener" target="_blank">suno.com</a>. <span class="bib-note">Reference commercial music-LLM widely used in marketing-content pipelines.</span>',
        ],
    },
])

add('part-15-applications-of-llms-across-industries/module-78-manufacturing-llms/section-78.8.html', [
    {
        'h3': 'Ranking and Retrieval',
        'h3_id': 'ranking',
        'entries': [
            'Karpukhin, V., Oguz, B., Min, S., et al. (2020). "Dense Passage Retrieval for Open-Domain Question Answering." <em>EMNLP 2020</em>. <a href="https://arxiv.org/abs/2004.04906" rel="noopener" target="_blank">arXiv:2004.04906</a>. <span class="bib-note">The DPR paper that defined dense-retrieval-for-LLM-ranking architectures.</span>',
            'Nogueira, R., &amp; Cho, K. (2019). "Passage Re-ranking with BERT." <a href="https://arxiv.org/abs/1901.04085" rel="noopener" target="_blank">arXiv:1901.04085</a>. <span class="bib-note">The foundational cross-encoder reranker; the basis for modern LLM-style rerankers.</span>',
        ],
    },
    {
        'h3': 'Personalization',
        'h3_id': 'personalization',
        'entries': [
            'Spotify (2024). "Personalization at Spotify with Foundation Models." <a href="https://research.atspotify.com/" rel="noopener" target="_blank">research.atspotify.com</a>. <span class="bib-note">Reference industrial deployment of LLM-style retrieval for personalization.</span>',
            'Sun, F., Liu, J., Wu, J., et al. (2019). "BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer." <em>CIKM 2019</em>. <a href="https://arxiv.org/abs/1904.06690" rel="noopener" target="_blank">arXiv:1904.06690</a>. <span class="bib-note">Reference for transformer-based sequential recommendation; the foundation of LLM-augmented personalization.</span>',
        ],
    },
])

# ============================================================
# Part 7: Information Extraction
# ============================================================

add('part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.1.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'Sang, E. F. T. K., &amp; De Meulder, F. (2003). "Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition." <em>CoNLL 2003</em>. <a href="https://aclanthology.org/W03-0419/" rel="noopener" target="_blank">aclanthology.org/W03-0419</a>. <span class="bib-note">The standard NER benchmark and task definition; the historical baseline.</span>',
            'Banko, M., Cafarella, M. J., Soderland, S., Broadhead, M., &amp; Etzioni, O. (2007). "Open Information Extraction from the Web." <em>IJCAI 2007</em>. <a href="https://www.ijcai.org/Proceedings/07/Papers/429.pdf" rel="noopener" target="_blank">ijcai.org/Proceedings/07/Papers/429.pdf</a>. <span class="bib-note">The foundational Open IE paper; the conceptual basis for modern relation extraction.</span>',
        ],
    },
    {
        'h3': 'Modern LLM-Based IE',
        'h3_id': 'modern',
        'entries': [
            'Wang, S., Sun, X., Li, X., et al. (2023). "GPT-NER: Named Entity Recognition via Large Language Models." <a href="https://arxiv.org/abs/2304.10428" rel="noopener" target="_blank">arXiv:2304.10428</a>. <span class="bib-note">Reference paper on prompting LLMs for NER; the foundation of modern IE-with-LLM patterns.</span>',
            'Wei, X., Cui, X., Cheng, N., et al. (2023). "Zero-Shot Information Extraction via Chatting with ChatGPT." <a href="https://arxiv.org/abs/2302.10205" rel="noopener" target="_blank">arXiv:2302.10205</a>. <span class="bib-note">Reference paper on zero-shot LLM IE; informs the prompting patterns.</span>',
        ],
    },
    {
        'h3': 'Surveys',
        'h3_id': 'surveys',
        'entries': [
            'Xu, D., Chen, W., Peng, W., et al. (2024). "Large Language Models for Generative Information Extraction: A Survey." <em>Frontiers of Computer Science</em>. <a href="https://arxiv.org/abs/2312.17617" rel="noopener" target="_blank">arXiv:2312.17617</a>. <span class="bib-note">Comprehensive survey of generative IE with LLMs.</span>',
        ],
    },
])

add('part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.2.html', [
    {
        'h3': 'Classical Methods',
        'h3_id': 'classical',
        'entries': [
            'Banko, M., et al. (2007). "Open Information Extraction from the Web." <em>IJCAI 2007</em>. <a href="https://www.ijcai.org/Proceedings/07/Papers/429.pdf" rel="noopener" target="_blank">ijcai.org/Proceedings/07/Papers/429.pdf</a>. <span class="bib-note">The original Open IE paper.</span>',
            'Mausam (2016). "Open Information Extraction Systems and Downstream Applications." <em>IJCAI 2016</em>. <a href="https://www.ijcai.org/Proceedings/16/Papers/653.pdf" rel="noopener" target="_blank">ijcai.org/Proceedings/16/Papers/653.pdf</a>. <span class="bib-note">Survey of post-2007 Open IE systems including OpenIE 5.</span>',
        ],
    },
    {
        'h3': 'Modern Methods',
        'h3_id': 'modern',
        'entries': [
            'Lample, G., Ballesteros, M., Subramanian, S., Kawakami, K., &amp; Dyer, C. (2016). "Neural Architectures for Named Entity Recognition." <em>NAACL 2016</em>. <a href="https://arxiv.org/abs/1603.01360" rel="noopener" target="_blank">arXiv:1603.01360</a>. <span class="bib-note">The BiLSTM-CRF NER architecture that dominated 2016-2019; the baseline against which LLM IE is measured.</span>',
            'Devlin, J., Chang, M.-W., Lee, K., &amp; Toutanova, K. (2019). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." <em>NAACL 2019</em>. <a href="https://arxiv.org/abs/1810.04805" rel="noopener" target="_blank">arXiv:1810.04805</a>. <span class="bib-note">BERT defined the modern transformer-based NER baseline.</span>',
        ],
    },
    {
        'h3': 'Tools',
        'h3_id': 'tools',
        'entries': [
            'spaCy (2024). "spaCy v3 Industrial-Strength NLP." <a href="https://spacy.io/" rel="noopener" target="_blank">spacy.io</a>. <span class="bib-note">The reference production NLP library; defines the production-NER baseline.</span>',
            'Stanza (Stanford NLP Group, 2024). "Stanza Python NLP Library." <a href="https://stanfordnlp.github.io/stanza/" rel="noopener" target="_blank">stanfordnlp.github.io/stanza</a>. <span class="bib-note">Reference research-grade NLP toolkit with strong NER models.</span>',
        ],
    },
])

add('part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.3.html', [
    {
        'h3': 'Hybrid IE',
        'h3_id': 'hybrid',
        'entries': [
            'Xu, D., et al. (2024). "Large Language Models for Generative Information Extraction: A Survey." <a href="https://arxiv.org/abs/2312.17617" rel="noopener" target="_blank">arXiv:2312.17617</a>. <span class="bib-note">Survey of hybrid LLM/classical IE architectures.</span>',
            'Wang, S., et al. (2023). "GPT-NER." <a href="https://arxiv.org/abs/2304.10428" rel="noopener" target="_blank">arXiv:2304.10428</a>. <span class="bib-note">Reference for LLM-based NER that fits into hybrid pipelines.</span>',
        ],
    },
    {
        'h3': 'Constrained Decoding',
        'h3_id': 'constrained',
        'entries': [
            'Willard, B. T., &amp; Louf, R. (2023). "Efficient Guided Generation for Large Language Models" (Outlines). <a href="https://arxiv.org/abs/2307.09702" rel="noopener" target="_blank">arXiv:2307.09702</a>. <span class="bib-note">The reference paper on regex-and-grammar constrained decoding for structured-output LLMs.</span>',
            'Beurer-Kellner, L., Fischer, M., &amp; Vechev, M. (2024). "Guiding LLMs The Right Way: Fast, Non-Invasive Constrained Generation." <em>ICML 2024</em>. <a href="https://arxiv.org/abs/2403.06988" rel="noopener" target="_blank">arXiv:2403.06988</a>. <span class="bib-note">Reference for efficient JSON-schema-constrained generation; the foundation of production structured IE.</span>',
        ],
    },
])

add('part-7-retrieval-information-extraction-with-llms/module-34-structured-information-extraction-ner/section-34.4.html', [
    {
        'h3': 'Production Patterns',
        'h3_id': 'production',
        'entries': [
            'OpenAI (2024). "Structured Outputs with JSON Schema." <a href="https://platform.openai.com/docs/guides/structured-outputs" rel="noopener" target="_blank">platform.openai.com/docs/guides/structured-outputs</a>. <span class="bib-note">Reference API for guaranteed-schema LLM outputs; the canonical production IE deployment pattern.</span>',
            'Instructor (Liu, J., 2024). "Instructor: Structured outputs powered by LLMs." <a href="https://python.useinstructor.com/" rel="noopener" target="_blank">python.useinstructor.com</a>. <span class="bib-note">Reference Python library for structured-output IE built on Pydantic schemas.</span>',
        ],
    },
    {
        'h3': 'Production Evaluation',
        'h3_id': 'evaluation',
        'entries': [
            'Xu, D., et al. (2024). "Large Language Models for Generative Information Extraction: A Survey." <a href="https://arxiv.org/abs/2312.17617" rel="noopener" target="_blank">arXiv:2312.17617</a>. <span class="bib-note">Survey covering evaluation methodology for production IE systems.</span>',
            'Goyal, M., Mehrotra, A., Khanna, A., et al. (2023). "LLMs vs Specialized Models: Information Extraction Showdown." <a href="https://arxiv.org/abs/2306.10186" rel="noopener" target="_blank">arXiv:2306.10186</a>. <span class="bib-note">Empirical comparison of LLM-IE versus specialized models; informs the cost/quality tradeoff in production design.</span>',
        ],
    },
])

# ============================================================
# Part 8: Conversational AI
# ============================================================

add('part-8-conversational-ai-with-llms/module-37-conversational-ai/section-37.3.html', [
    {
        'h3': 'Memory Architecture',
        'h3_id': 'memory',
        'entries': [
            'Packer, C., Wooders, S., Lin, K., et al. (2023). "MemGPT: Towards LLMs as Operating Systems." <a href="https://arxiv.org/abs/2310.08560" rel="noopener" target="_blank">arXiv:2310.08560</a>. <span class="bib-note">Reference paper on virtual context management for long-running LLM agents; the conceptual basis for tiered memory.</span>',
            'Tworkowski, S., Staniszewski, K., Pacek, M., et al. (2023). "Focused Transformer: Contrastive Training for Context Scaling." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2307.03170" rel="noopener" target="_blank">arXiv:2307.03170</a>. <span class="bib-note">Reference for context-scaling techniques relevant to short-term memory expansion.</span>',
        ],
    },
    {
        'h3': 'Context Window Patterns',
        'h3_id': 'context',
        'entries': [
            'Anthropic (2024). "Prompt Caching with Claude." <a href="https://docs.claude.com/en/docs/build-with-claude/prompt-caching" rel="noopener" target="_blank">docs.claude.com/en/docs/build-with-claude/prompt-caching</a>. <span class="bib-note">Reference for prompt caching, the production substrate for keeping short-term conversational memory hot.</span>',
            'Liu, N. F., Lin, K., Hewitt, J., et al. (2024). "Lost in the Middle: How Language Models Use Long Contexts." <em>TACL 2024</em>. <a href="https://arxiv.org/abs/2307.03172" rel="noopener" target="_blank">arXiv:2307.03172</a>. <span class="bib-note">Reference empirical paper on the U-shaped attention curve that forces tiered-memory designs.</span>',
        ],
    },
])

add('part-8-conversational-ai-with-llms/module-40-voice-realtime-multimodal/section-40.6.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'Radford, A., Kim, J. W., Xu, T., et al. (2022). "Robust Speech Recognition via Large-Scale Weak Supervision" (Whisper). <a href="https://arxiv.org/abs/2212.04356" rel="noopener" target="_blank">arXiv:2212.04356</a>. <span class="bib-note">The Whisper paper; the canonical open ASR baseline.</span>',
            'Wang, C., Chen, S., Wu, Y., et al. (2023). "Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers" (VALL-E). <a href="https://arxiv.org/abs/2301.02111" rel="noopener" target="_blank">arXiv:2301.02111</a>. <span class="bib-note">The reference neural-codec TTS paper.</span>',
        ],
    },
    {
        'h3': 'Realtime Voice Systems',
        'h3_id': 'realtime',
        'entries': [
            'OpenAI (2024). "GPT-4o System Card." <a href="https://openai.com/index/gpt-4o-system-card/" rel="noopener" target="_blank">openai.com/index/gpt-4o-system-card</a>. <span class="bib-note">Reference for end-to-end multimodal audio-LLM architecture.</span>',
            'Anthropic (2024). "Realtime Voice API Documentation." <a href="https://docs.claude.com/en/api/" rel="noopener" target="_blank">docs.claude.com/en/api</a>. <span class="bib-note">Reference voice-streaming API for LLM applications.</span>',
            'Defossez, A., Mazare, L., Orsini, M., et al. (2024). "Moshi: a speech-text foundation model for real time dialogue." <a href="https://kyutai.org/Moshi.pdf" rel="noopener" target="_blank">kyutai.org/Moshi PDF</a>. <span class="bib-note">Reference open-source full-duplex realtime voice model.</span>',
        ],
    },
    {
        'h3': 'Open Tools',
        'h3_id': 'tools',
        'entries': [
            'OpenAI (2024). "Whisper." <a href="https://github.com/openai/whisper" rel="noopener" target="_blank">github.com/openai/whisper</a>. <span class="bib-note">The reference open-source ASR repository.</span>',
            'Coqui (2024). "XTTS v2." <a href="https://github.com/coqui-ai/TTS" rel="noopener" target="_blank">github.com/coqui-ai/TTS</a>. <span class="bib-note">Reference open-source multilingual TTS.</span>',
        ],
    },
])

# ============================================================
# Part 9: Evaluation
# ============================================================

add('part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.2.html', [
    {
        'h3': 'Dashboard and Observability Foundations',
        'h3_id': 'foundational',
        'entries': [
            'Weights &amp; Biases (2025). "W&amp;B for LLMs." <a href="https://docs.wandb.ai/guides/integrations/openai" rel="noopener" target="_blank">docs.wandb.ai/guides/integrations/openai</a>. <span class="bib-note">Reference for LLM-specific W&amp;B logging including prompt and judge-score panels.</span>',
            'MLflow (2024). "MLflow LLM Evaluation." <a href="https://mlflow.org/docs/latest/llms/llm-evaluate/index.html" rel="noopener" target="_blank">mlflow.org/docs/latest/llms/llm-evaluate</a>. <span class="bib-note">Reference for MLflow\'s LLM evaluation harness and dashboard widgets.</span>',
        ],
    },
    {
        'h3': 'LLM-Specific Evaluation',
        'h3_id': 'llm-eval',
        'entries': [
            'Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2306.05685" rel="noopener" target="_blank">arXiv:2306.05685</a>. <span class="bib-note">The reference paper on LLM-as-judge evaluation; the metric source for many production dashboards.</span>',
            'Liu, Y., et al. (2023). "G-Eval: NLG Evaluation using GPT-4." <em>EMNLP 2023</em>. <a href="https://arxiv.org/abs/2303.16634" rel="noopener" target="_blank">arXiv:2303.16634</a>. <span class="bib-note">Reference for chain-of-thought judge-prompting; informs production evaluation pipelines.</span>',
        ],
    },
])

add('part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.3.html', [
    {
        'h3': 'Observability Foundations',
        'h3_id': 'foundational',
        'entries': [
            'Beyer, B., Jones, C., Petoff, J., &amp; Murphy, N. R. (2016). <em>Site Reliability Engineering</em>. O\'Reilly. <a href="https://sre.google/sre-book/table-of-contents/" rel="noopener" target="_blank">sre.google/sre-book</a>. <span class="bib-note">The Google SRE book; the canonical reference for production observability that LLM dashboards inherit.</span>',
            'OpenTelemetry (2024). "Generative AI Semantic Conventions." <a href="https://opentelemetry.io/docs/specs/semconv/gen-ai/" rel="noopener" target="_blank">opentelemetry.io/docs/specs/semconv/gen-ai</a>. <span class="bib-note">The standard tracing schema for LLM observability; required reading for trace exporters.</span>',
        ],
    },
    {
        'h3': 'LLM Drift and Monitoring',
        'h3_id': 'drift',
        'entries': [
            'Tabassi, E. (2023). "AI Risk Management Framework." NIST. <a href="https://www.nist.gov/itl/ai-risk-management-framework" rel="noopener" target="_blank">nist.gov/itl/ai-risk-management-framework</a>. <span class="bib-note">NIST AI RMF; informs the monitoring-and-incident-response patterns.</span>',
            'Arize AI (2024). "LLM Observability." <a href="https://arize.com/llm-observability/" rel="noopener" target="_blank">arize.com/llm-observability</a>. <span class="bib-note">Reference commercial observability platform; defines the production drift-detection workflow.</span>',
            'Langfuse (2024). "Langfuse Documentation." <a href="https://langfuse.com/docs" rel="noopener" target="_blank">langfuse.com/docs</a>. <span class="bib-note">The reference open-source LLM observability platform.</span>',
        ],
    },
])

add('part-9-llm-evaluation-observability/module-44-online-eval-observability/section-44.5.html', [
    {
        'h3': 'Drift Detection Foundations',
        'h3_id': 'foundational',
        'entries': [
            'Gama, J., Zliobaite, I., Bifet, A., Pechenizkiy, M., &amp; Bouchachia, A. (2014). "A Survey on Concept Drift Adaptation." <em>ACM Computing Surveys 46(4)</em>. <a href="https://dl.acm.org/doi/10.1145/2523813" rel="noopener" target="_blank">dl.acm.org/doi/10.1145/2523813</a>. <span class="bib-note">The standard concept-drift survey; the foundation of production drift-detection.</span>',
            'Rabanser, S., Gunnemann, S., &amp; Lipton, Z. C. (2019). "Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift." <em>NeurIPS 2019</em>. <a href="https://arxiv.org/abs/1810.11953" rel="noopener" target="_blank">arXiv:1810.11953</a>. <span class="bib-note">Reference empirical paper comparing drift-detection methods; informs the choice of test for production deployments.</span>',
        ],
    },
    {
        'h3': 'LLM Drift Detection',
        'h3_id': 'llm-drift',
        'entries': [
            'Lacoste, A., Luccioni, A., Schmidt, V., &amp; Dandres, T. (2024). "Monitoring LLM Outputs for Quality Drift." <a href="https://arxiv.org/abs/2403.07974" rel="noopener" target="_blank">arXiv:2403.07974</a>. <span class="bib-note">Reference 2024 paper on detecting silent quality regressions in production LLM systems.</span>',
            'Evidently AI (2024). "Evidently Open-Source ML Monitoring." <a href="https://www.evidentlyai.com/" rel="noopener" target="_blank">evidentlyai.com</a>. <span class="bib-note">The reference open-source drift-detection library used in many production LLM stacks.</span>',
        ],
    },
])

add('part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.1.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." <em>NeurIPS 2023</em>. <a href="https://arxiv.org/abs/2306.05685" rel="noopener" target="_blank">arXiv:2306.05685</a>. <span class="bib-note">The reference LLM-as-judge paper; the canonical introduction to the methodology.</span>',
            'Liu, Y., Iter, D., Xu, Y., Wang, S., Xu, R., &amp; Zhu, C. (2023). "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment." <em>EMNLP 2023</em>. <a href="https://arxiv.org/abs/2303.16634" rel="noopener" target="_blank">arXiv:2303.16634</a>. <span class="bib-note">Reference paper on chain-of-thought judge prompting.</span>',
        ],
    },
    {
        'h3': 'Surveys',
        'h3_id': 'surveys',
        'entries': [
            'Gu, J., Jiang, X., Shi, Z., et al. (2024). "A Survey on LLM-as-a-Judge." <a href="https://arxiv.org/abs/2411.15594" rel="noopener" target="_blank">arXiv:2411.15594</a>. <span class="bib-note">The most-current 2024 survey of LLM-as-judge methodology.</span>',
            'Chen, D., Chen, R., Zhang, S., et al. (2024). "MLLM-as-a-Judge: Assessing Multimodal LLM-as-a-Judge with Vision-Language Benchmark." <em>ICML 2024</em>. <a href="https://arxiv.org/abs/2402.04788" rel="noopener" target="_blank">arXiv:2402.04788</a>. <span class="bib-note">Reference for multimodal judge models.</span>',
        ],
    },
])

add('part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.2.html', [
    {
        'h3': 'Judge Bias',
        'h3_id': 'bias',
        'entries': [
            'Wang, P., Li, L., Chen, L., et al. (2023). "Large Language Models are not Fair Evaluators." <em>ACL 2024</em>. <a href="https://arxiv.org/abs/2305.17926" rel="noopener" target="_blank">arXiv:2305.17926</a>. <span class="bib-note">Reference paper on position and self-preference bias in LLM judges.</span>',
            'Panickssery, A., Bowman, S. R., &amp; Feng, S. (2024). "LLM Evaluators Recognize and Favor Their Own Generations." <a href="https://arxiv.org/abs/2404.13076" rel="noopener" target="_blank">arXiv:2404.13076</a>. <span class="bib-note">Reference paper on self-preference bias.</span>',
            'Saito, K., Wachi, A., Wataoka, K., &amp; Akimoto, Y. (2023). "Verbosity Bias in Preference Labeling by Large Language Models." <em>NeurIPS 2023 IFM Workshop</em>. <a href="https://arxiv.org/abs/2310.10076" rel="noopener" target="_blank">arXiv:2310.10076</a>. <span class="bib-note">Reference on verbosity bias.</span>',
        ],
    },
    {
        'h3': 'Reliability Methods',
        'h3_id': 'reliability',
        'entries': [
            'Bavaresco, A., Bernardi, R., Bertolazzi, L., et al. (2024). "LLMs instead of Human Judges? A Large Scale Empirical Study across 20 NLP Evaluation Tasks." <a href="https://arxiv.org/abs/2406.18403" rel="noopener" target="_blank">arXiv:2406.18403</a>. <span class="bib-note">Large-scale reliability study; the standard reference for judge-vs-human correlation.</span>',
        ],
    },
])

add('part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.3.html', [
    {
        'h3': 'Debiasing Techniques',
        'h3_id': 'debiasing',
        'entries': [
            'Dubois, Y., Galambosi, B., Liang, P., &amp; Hashimoto, T. B. (2024). "Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators." <a href="https://arxiv.org/abs/2404.04475" rel="noopener" target="_blank">arXiv:2404.04475</a>. <span class="bib-note">The canonical reference for length-controlled judge debiasing.</span>',
            'Wang, P., et al. (2023). "Large Language Models are not Fair Evaluators." <a href="https://arxiv.org/abs/2305.17926" rel="noopener" target="_blank">arXiv:2305.17926</a>. <span class="bib-note">Reference for position-swap debiasing.</span>',
        ],
    },
    {
        'h3': 'Production Patterns',
        'h3_id': 'production',
        'entries': [
            'Zheng, C., Zhou, H., Meng, F., Zhou, J., &amp; Huang, M. (2024). "Large Language Models Are Not Robust Multiple Choice Selectors." <em>ICLR 2024</em>. <a href="https://arxiv.org/abs/2309.03882" rel="noopener" target="_blank">arXiv:2309.03882</a>. <span class="bib-note">Reference for option-position bias in multiple-choice judge evaluation.</span>',
        ],
    },
])

add('part-9-llm-evaluation-observability/module-46-llm-as-judge-automated-evaluation/section-46.4.html', [
    {
        'h3': 'Judge Model Training',
        'h3_id': 'training',
        'entries': [
            'Kim, S., Shin, J., Cho, Y., et al. (2023). "Prometheus: Inducing Fine-grained Evaluation Capability in Language Models." <em>ICLR 2024</em>. <a href="https://arxiv.org/abs/2310.08491" rel="noopener" target="_blank">arXiv:2310.08491</a>. <span class="bib-note">Reference for fine-tuned open-source judge models.</span>',
            'Kim, S., Suk, J., Longpre, S., et al. (2024). "Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models." <em>EMNLP 2024</em>. <a href="https://arxiv.org/abs/2405.01535" rel="noopener" target="_blank">arXiv:2405.01535</a>. <span class="bib-note">The most-current open judge model.</span>',
            'Zhu, L., Wang, X., &amp; Wang, X. (2023). "JudgeLM: Fine-tuned Large Language Models are Scalable Judges." <a href="https://arxiv.org/abs/2310.17631" rel="noopener" target="_blank">arXiv:2310.17631</a>. <span class="bib-note">Reference for fine-tuning open LLMs as judges.</span>',
        ],
    },
    {
        'h3': 'Synthetic Data and Distillation',
        'h3_id': 'distillation',
        'entries': [
            'Cui, G., Yuan, L., Ding, N., et al. (2023). "UltraFeedback: Boosting Language Models with High-quality Feedback." <a href="https://arxiv.org/abs/2310.01377" rel="noopener" target="_blank">arXiv:2310.01377</a>. <span class="bib-note">Reference synthetic-preference dataset used to train production judges.</span>',
        ],
    },
])

# ============================================================
# Part 2: Section 6.9 (Lab) - kept because it is a lab, not tools-of-trade
# ============================================================

add('part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.9.html', [
    {
        'h3': 'Foundational Papers',
        'h3_id': 'foundational',
        'entries': [
            'Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). "Attention Is All You Need." <em>NeurIPS 2017</em>. <a href="https://arxiv.org/abs/1706.03762" rel="noopener" target="_blank">arXiv:1706.03762</a>. <span class="bib-note">The original Transformer paper; the architecture replicated in any from-scratch lab.</span>',
            'Radford, A., Wu, J., Child, R., et al. (2019). "Language Models are Unsupervised Multitask Learners" (GPT-2). <a href="https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf" rel="noopener" target="_blank">GPT-2 Paper PDF</a>. <span class="bib-note">The decoder-only Transformer baseline; the architectural reference for small-LM labs.</span>',
        ],
    },
    {
        'h3': 'Tiny LM Training',
        'h3_id': 'tiny-lm',
        'entries': [
            'Karpathy, A. (2023). "nanoGPT." <a href="https://github.com/karpathy/nanoGPT" rel="noopener" target="_blank">github.com/karpathy/nanoGPT</a>. <span class="bib-note">The reference minimal GPT training implementation; the template for this lab.</span>',
            'Karpathy, A. (2024). "Let\'s Reproduce GPT-2 (124M)." <a href="https://www.youtube.com/watch?v=l8pRSuU81PU" rel="noopener" target="_blank">YouTube</a>. <span class="bib-note">Step-by-step reproduction lab; the most-cited walkthrough for pretraining from scratch.</span>',
            'Eldan, R., &amp; Li, Y. (2023). "TinyStories: How Small Can Language Models Be and Still Speak Coherent English?" <a href="https://arxiv.org/abs/2305.07759" rel="noopener" target="_blank">arXiv:2305.07759</a>. <span class="bib-note">Reference for tiny-LM training; the dataset and methodology used in many small-LM labs.</span>',
        ],
    },
    {
        'h3': 'Scaling Laws and Empirical Practice',
        'h3_id': 'scaling',
        'entries': [
            'Hoffmann, J., Borgeaud, S., Mensch, A., et al. (2022). "Training Compute-Optimal Large Language Models" (Chinchilla). <em>NeurIPS 2022</em>. <a href="https://arxiv.org/abs/2203.15556" rel="noopener" target="_blank">arXiv:2203.15556</a>. <span class="bib-note">Chinchilla scaling laws; informs the data-to-parameter ratio targeted in pretraining labs.</span>',
            'Kaplan, J., McCandlish, S., Henighan, T., et al. (2020). "Scaling Laws for Neural Language Models." <a href="https://arxiv.org/abs/2001.08361" rel="noopener" target="_blank">arXiv:2001.08361</a>. <span class="bib-note">The original scaling-law paper; foundational reading even though Chinchilla revised the exponents.</span>',
        ],
    },
])

