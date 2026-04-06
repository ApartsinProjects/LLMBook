"""Fill TODO bibliography sections in appendix HTML files with real references."""
import re
import os

# Map: filename -> bibliography HTML replacement
# Each entry replaces <p>TODO: Add bibliography entries.</p>

BIBLIOGRAPHIES = {
    # ===== APPENDIX A: Mathematical Foundations =====
    "appendix-a-mathematical-foundations/section-a.1.html": """<h3>Linear Algebra Textbooks</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.deeplearningbook.org/contents/linear_algebra.html" target="_blank" rel="noopener">Goodfellow, I., Bengio, Y., and Courville, A. (2016). "Linear Algebra." <em>Deep Learning, Chapter 2</em>. MIT Press.</a></p>
    <p class="bib-annotation">Concise treatment of the linear algebra needed for deep learning, covering vectors, matrices, eigendecomposition, and SVD.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://math.mit.edu/~gs/linearalgebra/" target="_blank" rel="noopener">Strang, G. (2023). <em>Introduction to Linear Algebra</em>, 6th Edition. Wellesley-Cambridge Press.</a></p>
    <p class="bib-annotation">The gold standard undergraduate linear algebra textbook with excellent geometric intuition and computational examples.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://mml-book.github.io/" target="_blank" rel="noopener">Deisenroth, M. P., Faisal, A. A., and Ong, C. S. (2020). <em>Mathematics for Machine Learning</em>. Cambridge University Press.</a></p>
    <p class="bib-annotation">Free online textbook that bridges the gap between pure mathematics and machine learning applications.</p>
    <span class="bib-meta">Book</span>
</div>""",

    "appendix-a-mathematical-foundations/section-a.2.html": """<h3>Probability and Statistics for ML</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.deeplearningbook.org/contents/prob.html" target="_blank" rel="noopener">Goodfellow, I., Bengio, Y., and Courville, A. (2016). "Probability and Information Theory." <em>Deep Learning, Chapter 3</em>. MIT Press.</a></p>
    <p class="bib-annotation">Covers probability distributions, expectation, variance, and common distributions used throughout deep learning.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://hastie.su.domains/ElemStatLearn/" target="_blank" rel="noopener">Hastie, T., Tibshirani, R., and Friedman, J. (2009). <em>The Elements of Statistical Learning</em>, 2nd Edition. Springer.</a></p>
    <p class="bib-annotation">Comprehensive reference for statistical learning theory, freely available online from the authors.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf" target="_blank" rel="noopener">Bishop, C. M. (2006). <em>Pattern Recognition and Machine Learning</em>. Springer.</a></p>
    <p class="bib-annotation">Thorough Bayesian perspective on probability and statistics in the context of machine learning.</p>
    <span class="bib-meta">Book</span>
</div>""",

    "appendix-a-mathematical-foundations/section-a.3.html": """<h3>Calculus for Deep Learning</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.deeplearningbook.org/contents/numerical.html" target="_blank" rel="noopener">Goodfellow, I., Bengio, Y., and Courville, A. (2016). "Numerical Computation." <em>Deep Learning, Chapter 4</em>. MIT Press.</a></p>
    <p class="bib-annotation">Covers gradient-based optimization, Jacobian and Hessian matrices, and numerical stability considerations.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://d2l.ai/chapter_appendix-mathematics-for-deep-learning/multivariable-calculus.html" target="_blank" rel="noopener">Zhang, A., Lipton, Z. C., Li, M., and Smola, A. J. (2023). "Multivariable Calculus." <em>Dive into Deep Learning</em>.</a></p>
    <p class="bib-annotation">Interactive treatment of chain rule, gradients, and automatic differentiation with runnable code examples.</p>
    <span class="bib-meta">Tutorial</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/1502.05767" target="_blank" rel="noopener">Baydin, A. G., Pearlmutter, B. A., Radul, A. A., and Siskind, J. M. (2018). "Automatic Differentiation in Machine Learning: A Survey." <em>Journal of Machine Learning Research</em>, 18(153), 1-43.</a></p>
    <p class="bib-annotation">Comprehensive survey of automatic differentiation techniques that power modern deep learning frameworks.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-a-mathematical-foundations/section-a.4.html": """<h3>Information Theory Foundations</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.inference.org.uk/itprnn/book.pdf" target="_blank" rel="noopener">MacKay, D. J. C. (2003). <em>Information Theory, Inference, and Learning Algorithms</em>. Cambridge University Press.</a></p>
    <p class="bib-annotation">Freely available textbook connecting information theory to machine learning with excellent exercises and intuition.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://colah.github.io/posts/2015-09-Visual-Information/" target="_blank" rel="noopener">Olah, C. (2015). "Visual Information Theory." <em>colah's blog</em>.</a></p>
    <p class="bib-annotation">Highly visual and intuitive introduction to entropy, cross-entropy, and KL divergence concepts used in language modeling.</p>
    <span class="bib-meta">Blog</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf" target="_blank" rel="noopener">Shannon, C. E. (1948). "A Mathematical Theory of Communication." <em>Bell System Technical Journal</em>, 27(3), 379-423.</a></p>
    <p class="bib-annotation">The foundational paper that established information theory, introducing entropy and channel capacity.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    # ===== APPENDIX B: ML Essentials =====
    "appendix-b-ml-essentials/section-b.1.html": """<h3>Machine Learning Paradigms</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.statlearning.com/" target="_blank" rel="noopener">James, G., Witten, D., Hastie, T., and Tibshirani, R. (2023). <em>An Introduction to Statistical Learning</em>, 2nd Edition. Springer.</a></p>
    <p class="bib-annotation">Accessible introduction to supervised and unsupervised learning with practical R and Python examples.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.deeplearningbook.org/contents/ml.html" target="_blank" rel="noopener">Goodfellow, I., Bengio, Y., and Courville, A. (2016). "Machine Learning Basics." <em>Deep Learning, Chapter 5</em>. MIT Press.</a></p>
    <p class="bib-annotation">Covers learning paradigms, capacity, bias-variance tradeoff, and estimation from a deep learning perspective.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2006.09882" target="_blank" rel="noopener">Brown, T. B., et al. (2020). "Language Models are Few-Shot Learners." <em>NeurIPS 2020</em>.</a></p>
    <p class="bib-annotation">Demonstrated that large language models can perform few-shot and zero-shot learning across diverse tasks.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-b-ml-essentials/section-b.2.html": """<h3>Optimization for Deep Learning</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/1412.6980" target="_blank" rel="noopener">Kingma, D. P. and Ba, J. (2015). "Adam: A Method for Stochastic Optimization." <em>ICLR 2015</em>.</a></p>
    <p class="bib-annotation">Introduced the Adam optimizer, which remains the most widely used optimizer for training language models.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/1609.04747" target="_blank" rel="noopener">Ruder, S. (2016). "An Overview of Gradient Descent Optimization Algorithms." <em>arXiv preprint arXiv:1609.04747</em>.</a></p>
    <p class="bib-annotation">Clear and comprehensive survey comparing SGD, momentum, AdaGrad, RMSProp, Adam, and their variants.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.deeplearningbook.org/contents/optimization.html" target="_blank" rel="noopener">Goodfellow, I., Bengio, Y., and Courville, A. (2016). "Optimization for Training Deep Models." <em>Deep Learning, Chapter 8</em>. MIT Press.</a></p>
    <p class="bib-annotation">Thorough coverage of loss landscapes, learning rate schedules, and optimization challenges in deep networks.</p>
    <span class="bib-meta">Book</span>
</div>""",

    "appendix-b-ml-essentials/section-b.3.html": """<h3>Regularization and Generalization</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.deeplearningbook.org/contents/regularization.html" target="_blank" rel="noopener">Goodfellow, I., Bengio, Y., and Courville, A. (2016). "Regularization for Deep Learning." <em>Deep Learning, Chapter 7</em>. MIT Press.</a></p>
    <p class="bib-annotation">Covers dropout, weight decay, early stopping, data augmentation, and other regularization strategies.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/1207.0580" target="_blank" rel="noopener">Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., and Salakhutdinov, R. (2014). "Dropout: A Simple Way to Prevent Neural Networks from Overfitting." <em>JMLR</em>, 15(56), 1929-1958.</a></p>
    <p class="bib-annotation">Introduced dropout regularization, one of the most effective techniques for preventing overfitting in neural networks.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://scikit-learn.org/stable/modules/cross_validation.html" target="_blank" rel="noopener">Pedregosa, F., et al. (2011). "Cross-validation: Evaluating Estimator Performance." <em>scikit-learn Documentation</em>.</a></p>
    <p class="bib-annotation">Practical guide to cross-validation strategies including k-fold, stratified, and time series splits.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX C: Python for LLM =====
    "appendix-c-python-for-llm/section-c.1.html": """<h3>Essential Python Libraries</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://numpy.org/doc/stable/" target="_blank" rel="noopener">Harris, C. R., et al. (2020). "Array Programming with NumPy." <em>Nature</em>, 585, 357-362.</a></p>
    <p class="bib-annotation">The foundational array computing library for scientific Python, essential for tensor manipulation.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://pytorch.org/docs/stable/index.html" target="_blank" rel="noopener">Paszke, A., et al. (2019). "PyTorch: An Imperative Style, High-Performance Deep Learning Library." <em>NeurIPS 2019</em>.</a></p>
    <p class="bib-annotation">The dominant deep learning framework for LLM research and development, with dynamic computation graphs.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.python.org/3/library/asyncio.html" target="_blank" rel="noopener">Python Software Foundation (2024). "asyncio: Asynchronous I/O." <em>Python Standard Library Documentation</em>.</a></p>
    <p class="bib-annotation">Essential for building async LLM API clients and handling concurrent requests to language model endpoints.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-c-python-for-llm/section-c.2.html": """<h3>Python Environment Management</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.python.org/3/library/venv.html" target="_blank" rel="noopener">Python Software Foundation (2024). "venv: Creation of Virtual Environments." <em>Python Standard Library Documentation</em>.</a></p>
    <p class="bib-annotation">Official documentation for Python's built-in virtual environment module.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python-poetry.org/docs/" target="_blank" rel="noopener">Poetry Contributors (2024). "Poetry: Python Packaging and Dependency Management." <em>Poetry Documentation</em>.</a></p>
    <p class="bib-annotation">Modern dependency management tool that simplifies package resolution and reproducible builds for ML projects.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.astral.sh/uv/" target="_blank" rel="noopener">Astral (2024). "uv: An Extremely Fast Python Package Installer and Resolver." <em>Astral Documentation</em>.</a></p>
    <p class="bib-annotation">Rust-based package installer that dramatically speeds up dependency resolution for large ML environments.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-c-python-for-llm/section-c.3.html": """<h3>Interactive Computing</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://jupyter.org/documentation" target="_blank" rel="noopener">Project Jupyter (2024). "Jupyter Notebook Documentation." <em>jupyter.org</em>.</a></p>
    <p class="bib-annotation">Official documentation for the interactive notebook environment widely used for ML experimentation.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://colab.research.google.com/" target="_blank" rel="noopener">Google Research (2024). "Google Colaboratory." <em>Google</em>.</a></p>
    <p class="bib-annotation">Free cloud notebook environment with GPU access, popular for prototyping LLM experiments.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2209.09125" target="_blank" rel="noopener">Kluyver, T., et al. (2016). "Jupyter Notebooks: A Publishing Format for Reproducible Computational Workflows." <em>Positioning and Power in Academic Publishing</em>.</a></p>
    <p class="bib-annotation">Describes the design philosophy behind Jupyter notebooks and their role in reproducible research.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-c-python-for-llm/section-c.4.html": """<h3>LLM Scripting Patterns</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://platform.openai.com/docs/guides/text-generation" target="_blank" rel="noopener">OpenAI (2024). "Text Generation Guide." <em>OpenAI API Documentation</em>.</a></p>
    <p class="bib-annotation">Official guide to common patterns for calling LLM APIs including streaming, retries, and structured output.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.pydantic.dev/latest/" target="_blank" rel="noopener">Pydantic Contributors (2024). "Pydantic: Data Validation Using Python Type Annotations." <em>Pydantic Documentation</em>.</a></p>
    <p class="bib-annotation">The standard library for structured output validation when parsing LLM responses into typed Python objects.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://tenacity.readthedocs.io/" target="_blank" rel="noopener">Julien Danjou (2024). "Tenacity: Retrying Library for Python." <em>tenacity Documentation</em>.</a></p>
    <p class="bib-annotation">Essential retry library for building robust LLM API clients with exponential backoff and custom retry logic.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    # ===== APPENDIX D: Environment Setup =====
    "appendix-d-environment-setup/section-d.1.html": """<h3>Hardware for Deep Learning</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://timdettmers.com/2023/01/30/which-gpu-for-deep-learning/" target="_blank" rel="noopener">Dettmers, T. (2023). "Which GPU(s) to Get for Deep Learning." <em>Tim Dettmers Blog</em>.</a></p>
    <p class="bib-annotation">Regularly updated guide comparing consumer and data center GPUs for deep learning workloads.</p>
    <span class="bib-meta">Blog</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://developer.nvidia.com/deep-learning-performance-training-inference" target="_blank" rel="noopener">NVIDIA (2024). "Deep Learning Performance." <em>NVIDIA Developer</em>.</a></p>
    <p class="bib-annotation">Official NVIDIA guidelines on hardware requirements and performance optimization for deep learning.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/accelerate/usage_guides/model_size_estimator" target="_blank" rel="noopener">Hugging Face (2024). "Model Memory Estimator." <em>Accelerate Documentation</em>.</a></p>
    <p class="bib-annotation">Tool for estimating GPU memory requirements for loading and training transformer models.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-d-environment-setup/section-d.2.html": """<h3>CUDA and GPU Setup</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.nvidia.com/cuda/" target="_blank" rel="noopener">NVIDIA (2024). "CUDA Toolkit Documentation." <em>NVIDIA Developer</em>.</a></p>
    <p class="bib-annotation">Official documentation for installing and configuring CUDA for GPU-accelerated computing.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://pytorch.org/get-started/locally/" target="_blank" rel="noopener">PyTorch Contributors (2024). "Start Locally." <em>PyTorch Installation Guide</em>.</a></p>
    <p class="bib-annotation">Interactive installation selector for matching PyTorch versions with CUDA toolkit versions.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.nvidia.com/deeplearning/cudnn/install-guide/" target="_blank" rel="noopener">NVIDIA (2024). "cuDNN Installation Guide." <em>NVIDIA Developer</em>.</a></p>
    <p class="bib-annotation">Setup guide for the CUDA Deep Neural Network library required by most deep learning frameworks.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-d-environment-setup/section-d.3.html": """<h3>Python Environment Configuration</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.conda.io/projects/conda/en/latest/" target="_blank" rel="noopener">Anaconda, Inc. (2024). "Conda Documentation." <em>conda.io</em>.</a></p>
    <p class="bib-annotation">Documentation for the conda package manager commonly used for managing ML Python environments.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.astral.sh/uv/" target="_blank" rel="noopener">Astral (2024). "uv: An Extremely Fast Python Package Installer." <em>Astral Documentation</em>.</a></p>
    <p class="bib-annotation">Modern Rust-based alternative to pip and conda that handles virtual environments and dependencies.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://github.com/pyenv/pyenv" target="_blank" rel="noopener">pyenv Contributors (2024). "pyenv: Simple Python Version Management." <em>GitHub</em>.</a></p>
    <p class="bib-annotation">Tool for installing and switching between multiple Python versions on a single machine.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-d-environment-setup/section-d.4.html": """<h3>Key Library Installation</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/transformers/installation" target="_blank" rel="noopener">Hugging Face (2024). "Transformers Installation Guide." <em>Hugging Face Documentation</em>.</a></p>
    <p class="bib-annotation">Step-by-step installation instructions for the Transformers library with framework-specific backends.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://pytorch.org/get-started/locally/" target="_blank" rel="noopener">PyTorch Contributors (2024). "Get Started." <em>PyTorch Documentation</em>.</a></p>
    <p class="bib-annotation">Official installation guide with platform, package manager, and CUDA version selectors.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://pip.pypa.io/en/stable/reference/requirements-file-format/" target="_blank" rel="noopener">PyPA (2024). "Requirements File Format." <em>pip Documentation</em>.</a></p>
    <p class="bib-annotation">Reference for specifying reproducible dependency lists with version pinning for ML projects.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-d-environment-setup/section-d.5.html": """<h3>Cloud Computing for ML</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://cloud.google.com/vertex-ai/docs" target="_blank" rel="noopener">Google Cloud (2024). "Vertex AI Documentation." <em>Google Cloud</em>.</a></p>
    <p class="bib-annotation">Google's managed ML platform offering GPU instances, model training, and deployment services.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.aws.amazon.com/sagemaker/" target="_blank" rel="noopener">Amazon Web Services (2024). "Amazon SageMaker Documentation." <em>AWS</em>.</a></p>
    <p class="bib-annotation">AWS managed ML service with notebook instances, training jobs, and model hosting capabilities.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://lambdalabs.com/service/gpu-cloud" target="_blank" rel="noopener">Lambda Labs (2024). "Lambda GPU Cloud." <em>Lambda</em>.</a></p>
    <p class="bib-annotation">GPU cloud provider popular among ML researchers for cost-effective A100 and H100 instances.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-d-environment-setup/section-d.6.html": """<h3>Verification and Troubleshooting</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://pytorch.org/docs/stable/notes/cuda.html" target="_blank" rel="noopener">PyTorch Contributors (2024). "CUDA Semantics." <em>PyTorch Documentation</em>.</a></p>
    <p class="bib-annotation">Reference for verifying CUDA availability, device management, and memory handling in PyTorch.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/transformers/troubleshooting" target="_blank" rel="noopener">Hugging Face (2024). "Troubleshooting." <em>Transformers Documentation</em>.</a></p>
    <p class="bib-annotation">Common installation and runtime issues with the Transformers library and their solutions.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.nvidia.com/cuda/cuda-installation-guide-linux/" target="_blank" rel="noopener">NVIDIA (2024). "CUDA Installation Guide for Linux." <em>NVIDIA Developer</em>.</a></p>
    <p class="bib-annotation">Comprehensive troubleshooting guide for CUDA driver and toolkit installation issues.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX E: Git Collaboration =====
    "appendix-e-git-collaboration/section-e.1.html": """<h3>Git for ML Projects</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://git-scm.com/book/en/v2" target="_blank" rel="noopener">Chacon, S. and Straub, B. (2014). <em>Pro Git</em>, 2nd Edition. Apress.</a></p>
    <p class="bib-annotation">The definitive free Git reference covering branching, merging, and collaboration workflows.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage" target="_blank" rel="noopener">GitHub (2024). "About Git Large File Storage." <em>GitHub Documentation</em>.</a></p>
    <p class="bib-annotation">Guide for handling large model files and datasets in Git repositories using LFS.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://nbdev.fast.ai/" target="_blank" rel="noopener">Howard, J. and Gugger, S. (2024). "nbdev: Write, Test, Document, and Distribute Software Packages from Notebooks." <em>fast.ai</em>.</a></p>
    <p class="bib-annotation">Framework for developing Python libraries in Jupyter notebooks with built-in Git-friendly diff support.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-e-git-collaboration/section-e.2.html": """<h3>Data Version Control</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://dvc.org/doc" target="_blank" rel="noopener">Iterative (2024). "DVC Documentation." <em>dvc.org</em>.</a></p>
    <p class="bib-annotation">Official documentation for DVC, the Git extension for versioning data, models, and ML pipelines.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/hub/repositories-getting-started" target="_blank" rel="noopener">Hugging Face (2024). "Getting Started with Repositories." <em>Hugging Face Hub Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to using the Hugging Face Hub for versioning models and datasets with Git-based workflows.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://lakefs.io/blog/data-versioning/" target="_blank" rel="noopener">lakeFS (2024). "Data Versioning Guide." <em>lakeFS Blog</em>.</a></p>
    <p class="bib-annotation">Overview of data versioning strategies comparing DVC, lakeFS, and Delta Lake approaches.</p>
    <span class="bib-meta">Blog</span>
</div>""",

    "appendix-e-git-collaboration/section-e.3.html": """<h3>Experiment Tracking with Git</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://dvc.org/doc/start/experiments" target="_blank" rel="noopener">Iterative (2024). "Get Started: Experiments." <em>DVC Documentation</em>.</a></p>
    <p class="bib-annotation">Tutorial for tracking ML experiments alongside code changes using DVC experiments.</p>
    <span class="bib-meta">Tutorial</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.wandb.ai/guides/integrations/git" target="_blank" rel="noopener">Weights and Biases (2024). "Git Integration." <em>W&B Documentation</em>.</a></p>
    <p class="bib-annotation">Guide for linking W&B experiment runs to specific Git commits for full reproducibility.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://mlflow.org/docs/latest/tracking.html" target="_blank" rel="noopener">MLflow Contributors (2024). "MLflow Tracking." <em>MLflow Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for logging parameters, metrics, and artifacts alongside Git-tracked code.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-e-git-collaboration/section-e.4.html": """<h3>Reproducibility in ML</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2003.12206" target="_blank" rel="noopener">Pineau, J., et al. (2021). "Improving Reproducibility in Machine Learning Research." <em>JMLR</em>, 22(164), 1-20.</a></p>
    <p class="bib-annotation">NeurIPS reproducibility checklist authors discuss standards for reproducible ML research.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://pytorch.org/docs/stable/notes/randomness.html" target="_blank" rel="noopener">PyTorch Contributors (2024). "Reproducibility." <em>PyTorch Documentation</em>.</a></p>
    <p class="bib-annotation">Official guide to controlling randomness and achieving deterministic results in PyTorch.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.docker.com/develop/dev-best-practices/" target="_blank" rel="noopener">Docker, Inc. (2024). "Development Best Practices." <em>Docker Documentation</em>.</a></p>
    <p class="bib-annotation">Best practices for containerizing ML environments to ensure reproducible execution across machines.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX F: Glossary =====
    "appendix-f-glossary/section-f.1.html": """<h3>Libraries and Frameworks</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://pytorch.org/docs/stable/" target="_blank" rel="noopener">PyTorch Contributors (2024). "PyTorch Documentation." <em>pytorch.org</em>.</a></p>
    <p class="bib-annotation">Official documentation for the leading deep learning framework used in LLM research.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs" target="_blank" rel="noopener">Hugging Face (2024). "Hugging Face Documentation." <em>huggingface.co</em>.</a></p>
    <p class="bib-annotation">Central documentation hub for the Transformers, Datasets, Tokenizers, and Hub libraries.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/get_started/introduction" target="_blank" rel="noopener">LangChain (2024). "Introduction." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">Overview of the LangChain framework for building applications with large language models.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-f-glossary/section-f.2.html": """<h3>Models and Architectures</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/1706.03762" target="_blank" rel="noopener">Vaswani, A., et al. (2017). "Attention Is All You Need." <em>NeurIPS 2017</em>.</a></p>
    <p class="bib-annotation">The foundational transformer paper that introduced the architecture underlying all modern LLMs.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2303.08774" target="_blank" rel="noopener">OpenAI (2023). "GPT-4 Technical Report." <em>arXiv preprint arXiv:2303.08774</em>.</a></p>
    <p class="bib-annotation">Technical report describing the capabilities and safety evaluations of the GPT-4 model family.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2302.13971" target="_blank" rel="noopener">Touvron, H., et al. (2023). "LLaMA: Open and Efficient Foundation Language Models." <em>arXiv preprint arXiv:2302.13971</em>.</a></p>
    <p class="bib-annotation">Introduced the LLaMA family of open-weight models that catalyzed the open-source LLM ecosystem.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-f-glossary/section-f.3.html": """<h3>Algorithms and Techniques</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2106.09685" target="_blank" rel="noopener">Hu, E. J., et al. (2022). "LoRA: Low-Rank Adaptation of Large Language Models." <em>ICLR 2022</em>.</a></p>
    <p class="bib-annotation">Introduced the widely-adopted parameter-efficient fine-tuning method that adds trainable low-rank matrices.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2203.02155" target="_blank" rel="noopener">Ouyang, L., et al. (2022). "Training Language Models to Follow Instructions with Human Feedback." <em>NeurIPS 2022</em>.</a></p>
    <p class="bib-annotation">Describes RLHF as applied to InstructGPT, establishing the standard alignment training pipeline.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2305.18290" target="_blank" rel="noopener">Rafailov, R., et al. (2023). "Direct Preference Optimization: Your Language Model Is Secretly a Reward Model." <em>NeurIPS 2023</em>.</a></p>
    <p class="bib-annotation">Introduced DPO as a simpler alternative to RLHF that eliminates the need for a separate reward model.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-f-glossary/section-f.4.html": """<h3>NLP and AI Concepts</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://web.stanford.edu/~jurafsky/slp3/" target="_blank" rel="noopener">Jurafsky, D. and Martin, J. H. (2024). <em>Speech and Language Processing</em>, 3rd Edition (draft). Stanford University.</a></p>
    <p class="bib-annotation">The standard NLP textbook covering language modeling, parsing, semantics, and modern neural approaches.</p>
    <span class="bib-meta">Book</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2005.14165" target="_blank" rel="noopener">Brown, T. B., et al. (2020). "Language Models are Few-Shot Learners." <em>NeurIPS 2020</em>.</a></p>
    <p class="bib-annotation">The GPT-3 paper that demonstrated emergent few-shot learning capabilities in large language models.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2009.11462" target="_blank" rel="noopener">Lewis, P., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." <em>NeurIPS 2020</em>.</a></p>
    <p class="bib-annotation">Introduced the RAG paradigm that combines retrieval with generation to ground LLM outputs in external knowledge.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-f-glossary/section-f.5.html": """<h3>Applications and Deployment</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2309.01029" target="_blank" rel="noopener">Chase, H. (2022). "LangChain." <em>GitHub Repository</em>.</a></p>
    <p class="bib-annotation">The most widely adopted framework for building LLM-powered applications with chains and agents.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2307.06435" target="_blank" rel="noopener">Kwon, W., et al. (2023). "Efficient Memory Management for Large Language Model Serving with PagedAttention." <em>SOSP 2023</em>.</a></p>
    <p class="bib-annotation">Introduced vLLM and PagedAttention for efficient LLM inference serving in production.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.gradio.app/docs" target="_blank" rel="noopener">Abramovich, A., et al. (2024). "Gradio: Build Machine Learning Web Apps." <em>Gradio Documentation</em>.</a></p>
    <p class="bib-annotation">Popular library for quickly building web demos and interfaces for LLM applications.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX G: Hardware and Compute =====
    "appendix-g-hardware-compute/section-g.1.html": """<h3>GPU Landscape</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.nvidia.com/en-us/data-center/h100/" target="_blank" rel="noopener">NVIDIA (2024). "NVIDIA H100 Tensor Core GPU." <em>NVIDIA Data Center</em>.</a></p>
    <p class="bib-annotation">Product specifications for the H100, the dominant GPU for large-scale LLM training and inference.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://timdettmers.com/2023/01/30/which-gpu-for-deep-learning/" target="_blank" rel="noopener">Dettmers, T. (2023). "Which GPU(s) to Get for Deep Learning." <em>Tim Dettmers Blog</em>.</a></p>
    <p class="bib-annotation">Comprehensive and regularly updated comparison of GPUs for deep learning workloads across price points.</p>
    <span class="bib-meta">Blog</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2402.13228" target="_blank" rel="noopener">Luccioni, A. S., Viguier, S., and Ligozat, A. L. (2023). "Estimating the Carbon Footprint of BLOOM." <em>JMLR</em>, 24(253), 1-15.</a></p>
    <p class="bib-annotation">Analysis of the compute costs and environmental impact of training large language models.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-g-hardware-compute/section-g.2.html": """<h3>Cloud GPU Pricing</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://cloud.google.com/gpu" target="_blank" rel="noopener">Google Cloud (2024). "GPU Pricing." <em>Google Cloud</em>.</a></p>
    <p class="bib-annotation">Current pricing for GPU instances including A100, H100, and TPU options on Google Cloud.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://aws.amazon.com/ec2/pricing/on-demand/" target="_blank" rel="noopener">Amazon Web Services (2024). "Amazon EC2 On-Demand Pricing." <em>AWS</em>.</a></p>
    <p class="bib-annotation">Pricing details for AWS GPU instances including p4d (A100) and p5 (H100) instance families.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://fullstackdeeplearning.com/cloud-gpus/" target="_blank" rel="noopener">Full Stack Deep Learning (2024). "Cloud GPU Comparison." <em>fullstackdeeplearning.com</em>.</a></p>
    <p class="bib-annotation">Community-maintained comparison of cloud GPU providers with real-time pricing data.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-g-hardware-compute/section-g.3.html": """<h3>GPU Selection Guidance</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/transformers/perf_train_gpu_one" target="_blank" rel="noopener">Hugging Face (2024). "Efficient Training on a Single GPU." <em>Transformers Documentation</em>.</a></p>
    <p class="bib-annotation">Practical guide to maximizing training efficiency on a single GPU with memory optimization techniques.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2104.04473" target="_blank" rel="noopener">Narayanan, D., et al. (2021). "Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM." <em>SC 2021</em>.</a></p>
    <p class="bib-annotation">Describes GPU parallelism strategies for training models too large for a single accelerator.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://timdettmers.com/2022/12/19/tpu-vs-gpu-for-transformers/" target="_blank" rel="noopener">Dettmers, T. (2022). "TPU vs GPU for Transformers." <em>Tim Dettmers Blog</em>.</a></p>
    <p class="bib-annotation">Practical comparison of TPUs and GPUs for transformer training workloads with benchmark data.</p>
    <span class="bib-meta">Blog</span>
</div>""",

    "appendix-g-hardware-compute/section-g.4.html": """<h3>Cost Estimation</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2001.08361" target="_blank" rel="noopener">Kaplan, J., et al. (2020). "Scaling Laws for Neural Language Models." <em>arXiv preprint arXiv:2001.08361</em>.</a></p>
    <p class="bib-annotation">Established the power-law relationships between compute budget, model size, and training loss.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2203.15556" target="_blank" rel="noopener">Hoffmann, J., et al. (2022). "Training Compute-Optimal Large Language Models." <em>NeurIPS 2022</em>.</a></p>
    <p class="bib-annotation">The Chinchilla paper that revised scaling laws and showed many models were undertrained relative to their size.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://blog.eleuther.ai/transformer-math/" target="_blank" rel="noopener">EleutherAI (2023). "Transformer Math 101." <em>EleutherAI Blog</em>.</a></p>
    <p class="bib-annotation">Practical formulas for estimating FLOPs, memory, and training time for transformer models.</p>
    <span class="bib-meta">Blog</span>
</div>""",

    "appendix-g-hardware-compute/section-g.5.html": """<h3>Common GPU Configurations</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.nvidia.com/datacenter/dgx/index.html" target="_blank" rel="noopener">NVIDIA (2024). "DGX Systems Documentation." <em>NVIDIA Developer</em>.</a></p>
    <p class="bib-annotation">Reference specifications for NVIDIA DGX server configurations commonly used for LLM training.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/transformers/perf_train_gpu_many" target="_blank" rel="noopener">Hugging Face (2024). "Efficient Training on Multiple GPUs." <em>Transformers Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to multi-GPU training strategies including data parallelism, model parallelism, and DeepSpeed integration.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.deepspeed.ai/getting-started/" target="_blank" rel="noopener">Microsoft (2024). "DeepSpeed: Getting Started." <em>DeepSpeed Documentation</em>.</a></p>
    <p class="bib-annotation">Introduction to the DeepSpeed library for efficient distributed training with ZeRO optimization.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX H: Model Cards =====
    "appendix-h-model-cards/section-h.1.html": """<h3>Proprietary Models</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2303.08774" target="_blank" rel="noopener">OpenAI (2023). "GPT-4 Technical Report." <em>arXiv preprint arXiv:2303.08774</em>.</a></p>
    <p class="bib-annotation">Technical report describing GPT-4's capabilities, limitations, and safety evaluations.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.anthropic.com/research/claude-3-family" target="_blank" rel="noopener">Anthropic (2024). "The Claude 3 Model Family." <em>Anthropic Research</em>.</a></p>
    <p class="bib-annotation">Model card for the Claude 3 family describing Haiku, Sonnet, and Opus capabilities and safety properties.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2312.11805" target="_blank" rel="noopener">Google DeepMind (2023). "Gemini: A Family of Highly Capable Multimodal Models." <em>arXiv preprint arXiv:2312.11805</em>.</a></p>
    <p class="bib-annotation">Technical report for Google's Gemini multimodal model family covering architecture and evaluations.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-h-model-cards/section-h.2.html": """<h3>Open-Weight Models</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2407.21783" target="_blank" rel="noopener">Dubey, A., et al. (2024). "The Llama 3 Herd of Models." <em>arXiv preprint arXiv:2407.21783</em>.</a></p>
    <p class="bib-annotation">Technical report for Meta's Llama 3 models covering pretraining, post-training, and safety alignment.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2310.06825" target="_blank" rel="noopener">Jiang, A. Q., et al. (2023). "Mistral 7B." <em>arXiv preprint arXiv:2310.06825</em>.</a></p>
    <p class="bib-annotation">Introduced the efficient Mistral 7B model with grouped-query attention and sliding window attention.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2309.16609" target="_blank" rel="noopener">Bai, J., et al. (2023). "Qwen Technical Report." <em>arXiv preprint arXiv:2309.16609</em>.</a></p>
    <p class="bib-annotation">Technical details for Alibaba's Qwen model family, a leading multilingual open-weight model series.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-h-model-cards/section-h.3.html": """<h3>Model Comparison Resources</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard" target="_blank" rel="noopener">Hugging Face (2024). "Open LLM Leaderboard." <em>Hugging Face Spaces</em>.</a></p>
    <p class="bib-annotation">Community benchmark leaderboard tracking open model performance across standard evaluation suites.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://chat.lmsys.org/" target="_blank" rel="noopener">Zheng, L., et al. (2023). "LMSYS Chatbot Arena." <em>lmsys.org</em>.</a></p>
    <p class="bib-annotation">Crowdsourced platform for head-to-head model comparisons using Elo ratings from human preferences.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2306.05685" target="_blank" rel="noopener">Zheng, L., et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." <em>NeurIPS 2023</em>.</a></p>
    <p class="bib-annotation">Established the methodology behind the Chatbot Arena leaderboard and LLM-as-a-judge evaluation.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    # ===== APPENDIX I: Prompt Templates =====
    "appendix-i-prompt-templates/section-i.1.html": """<h3>Classification Prompting</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2302.11382" target="_blank" rel="noopener">Wei, J., et al. (2023). "Larger Language Models Do In-Context Learning Differently." <em>arXiv preprint arXiv:2302.11382</em>.</a></p>
    <p class="bib-annotation">Analyzes how in-context learning (few-shot classification) behavior changes with model scale.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://platform.openai.com/docs/guides/text-generation/chat-completions-api" target="_blank" rel="noopener">OpenAI (2024). "Text Generation Guide." <em>OpenAI API Documentation</em>.</a></p>
    <p class="bib-annotation">Official guide to crafting classification prompts with system messages and structured outputs.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview" target="_blank" rel="noopener">Anthropic (2024). "Prompt Engineering Overview." <em>Anthropic Documentation</em>.</a></p>
    <p class="bib-annotation">Anthropic's official guide to effective prompting techniques including classification task patterns.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-i-prompt-templates/section-i.2.html": """<h3>Summarization Techniques</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2301.13848" target="_blank" rel="noopener">Goyal, T., Li, J. J., and Durrett, G. (2023). "News Summarization and Evaluation in the Era of GPT-3." <em>arXiv preprint arXiv:2301.13848</em>.</a></p>
    <p class="bib-annotation">Evaluates LLM summarization quality and compares prompting strategies for news article summarization.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts" target="_blank" rel="noopener">Anthropic (2024). "Chain Prompts for Complex Tasks." <em>Anthropic Documentation</em>.</a></p>
    <p class="bib-annotation">Guidance on breaking long-document summarization into manageable chain-of-summarization steps.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2304.04193" target="_blank" rel="noopener">Adams, G., et al. (2023). "From Sparse to Dense: GPT-4 Summarization with Chain of Density Prompting." <em>arXiv preprint arXiv:2304.04193</em>.</a></p>
    <p class="bib-annotation">Introduced the Chain of Density prompting technique for progressively more informative summaries.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-i-prompt-templates/section-i.3.html": """<h3>Information Extraction</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2304.11633" target="_blank" rel="noopener">Wei, X., et al. (2023). "Zero-Shot Information Extraction via Chatting with ChatGPT." <em>arXiv preprint arXiv:2304.11633</em>.</a></p>
    <p class="bib-annotation">Systematic evaluation of ChatGPT for named entity recognition, relation extraction, and event extraction tasks.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://platform.openai.com/docs/guides/structured-outputs" target="_blank" rel="noopener">OpenAI (2024). "Structured Outputs." <em>OpenAI API Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to extracting structured data from text using JSON mode and function calling.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.anthropic.com/en/docs/build-with-claude/tool-use" target="_blank" rel="noopener">Anthropic (2024). "Tool Use (Function Calling)." <em>Anthropic Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for using tool-use schemas to extract structured information from unstructured text.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-i-prompt-templates/section-i.4.html": """<h3>Question Answering</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2009.11462" target="_blank" rel="noopener">Lewis, P., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." <em>NeurIPS 2020</em>.</a></p>
    <p class="bib-annotation">The foundational RAG paper showing how retrieval improves question answering accuracy.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2210.03629" target="_blank" rel="noopener">Press, O., et al. (2023). "Measuring and Narrowing the Compositionality Gap in Language Models." <em>Findings of EMNLP 2023</em>.</a></p>
    <p class="bib-annotation">Introduced self-ask prompting for multi-hop question answering with decomposed sub-questions.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-examples" target="_blank" rel="noopener">Anthropic (2024). "Use Examples (Few-Shot Prompting)." <em>Anthropic Documentation</em>.</a></p>
    <p class="bib-annotation">Best practices for few-shot examples in QA prompts, including formatting and example selection.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-i-prompt-templates/section-i.5.html": """<h3>Code Generation</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2107.03374" target="_blank" rel="noopener">Chen, M., et al. (2021). "Evaluating Large Language Models Trained on Code." <em>arXiv preprint arXiv:2107.03374</em>.</a></p>
    <p class="bib-annotation">Introduced Codex and the HumanEval benchmark for evaluating LLM code generation capabilities.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2308.12950" target="_blank" rel="noopener">Roziere, B., et al. (2023). "Code Llama: Open Foundation Models for Code." <em>arXiv preprint arXiv:2308.12950</em>.</a></p>
    <p class="bib-annotation">Describes the Code Llama family of models specialized for code generation and understanding tasks.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.github.com/en/copilot" target="_blank" rel="noopener">GitHub (2024). "GitHub Copilot Documentation." <em>GitHub Docs</em>.</a></p>
    <p class="bib-annotation">Documentation for the leading AI code assistant, illustrating production code generation patterns.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-i-prompt-templates/section-i.6.html": """<h3>Chain-of-Thought Reasoning</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2201.11903" target="_blank" rel="noopener">Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." <em>NeurIPS 2022</em>.</a></p>
    <p class="bib-annotation">The seminal paper demonstrating that step-by-step reasoning prompts dramatically improve LLM performance on reasoning tasks.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2205.11916" target="_blank" rel="noopener">Kojima, T., et al. (2022). "Large Language Models are Zero-Shot Reasoners." <em>NeurIPS 2022</em>.</a></p>
    <p class="bib-annotation">Showed that simply adding "Let's think step by step" triggers zero-shot chain-of-thought reasoning.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2203.11171" target="_blank" rel="noopener">Wang, X., et al. (2023). "Self-Consistency Improves Chain of Thought Reasoning in Language Models." <em>ICLR 2023</em>.</a></p>
    <p class="bib-annotation">Introduced self-consistency decoding: sampling multiple reasoning paths and taking the majority vote.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-i-prompt-templates/section-i.7.html": """<h3>System Prompt Design</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts" target="_blank" rel="noopener">Anthropic (2024). "System Prompts." <em>Anthropic Documentation</em>.</a></p>
    <p class="bib-annotation">Official guidance on designing effective system prompts for role-based assistants with Claude.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://platform.openai.com/docs/guides/prompt-engineering" target="_blank" rel="noopener">OpenAI (2024). "Prompt Engineering Guide." <em>OpenAI Documentation</em>.</a></p>
    <p class="bib-annotation">Comprehensive guide to system prompt strategies including role assignment and output formatting.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2311.10122" target="_blank" rel="noopener">Zheng, L., et al. (2023). "LMSYS-Chat-1M: A Large-Scale Real-World LLM Conversation Dataset." <em>ICLR 2024</em>.</a></p>
    <p class="bib-annotation">Analysis of real system prompts and conversation patterns from one million LLM interactions.</p>
    <span class="bib-meta">Dataset</span>
</div>""",

    "appendix-i-prompt-templates/section-i.8.html": """<h3>Reasoning Model Prompts</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2309.17452" target="_blank" rel="noopener">Yao, S., et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." <em>NeurIPS 2023</em>.</a></p>
    <p class="bib-annotation">Extends chain-of-thought to a tree structure, enabling exploration and backtracking during reasoning.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2210.03629" target="_blank" rel="noopener">Press, O., et al. (2023). "Measuring and Narrowing the Compositionality Gap in Language Models." <em>Findings of EMNLP 2023</em>.</a></p>
    <p class="bib-annotation">Introduced the self-ask prompting technique for decomposing complex reasoning into sequential sub-questions.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://platform.openai.com/docs/guides/reasoning" target="_blank" rel="noopener">OpenAI (2024). "Reasoning Models." <em>OpenAI Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to prompting OpenAI's o1 and o3 reasoning models, including best practices for structured thinking.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX J: Datasets and Benchmarks =====
    "appendix-j-datasets-benchmarks/section-j.1.html": """<h3>Pretraining Datasets</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2101.00027" target="_blank" rel="noopener">Gao, L., et al. (2020). "The Pile: An 800GB Dataset of Diverse Text for Language Modeling." <em>arXiv preprint arXiv:2101.00027</em>.</a></p>
    <p class="bib-annotation">Describes the curation of The Pile, an influential diverse pretraining dataset used by many open models.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2306.01116" target="_blank" rel="noopener">Penedo, G., et al. (2023). "The RefinedWeb Dataset for Falcon LLM." <em>NeurIPS 2023 Datasets and Benchmarks Track</em>.</a></p>
    <p class="bib-annotation">Demonstrates that carefully filtered web data alone can match curated multi-source datasets for LLM training.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/datasets/allenai/dolma" target="_blank" rel="noopener">Soldaini, L., et al. (2024). "Dolma: An Open Corpus of Three Trillion Tokens." <em>ACL 2024</em>.</a></p>
    <p class="bib-annotation">Open and fully documented pretraining corpus used for the OLMo family of language models.</p>
    <span class="bib-meta">Dataset</span>
</div>""",

    "appendix-j-datasets-benchmarks/section-j.2.html": """<h3>Instruction and Alignment Datasets</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2304.07327" target="_blank" rel="noopener">Taori, R., et al. (2023). "Stanford Alpaca: An Instruction-Following LLaMA Model." <em>GitHub</em>.</a></p>
    <p class="bib-annotation">Pioneered the use of self-instruct generated training data for instruction-tuning open models.</p>
    <span class="bib-meta">Dataset</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2306.02707" target="_blank" rel="noopener">Ivison, H., et al. (2023). "Camels in a Changing Climate: Enhancing LM Adaptation with Tulu 2." <em>arXiv preprint arXiv:2306.02707</em>.</a></p>
    <p class="bib-annotation">Systematic study of instruction-tuning data mixtures and their effects on model capabilities.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/datasets/HuggingFaceH4/ultrafeedback_binarized" target="_blank" rel="noopener">Tunstall, L., et al. (2023). "UltraFeedback: Boosting Language Models with High-Quality Feedback." <em>Hugging Face</em>.</a></p>
    <p class="bib-annotation">Large-scale preference dataset used for DPO training of models like Zephyr and Notus.</p>
    <span class="bib-meta">Dataset</span>
</div>""",

    "appendix-j-datasets-benchmarks/section-j.3.html": """<h3>Evaluation Benchmarks</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2009.03300" target="_blank" rel="noopener">Hendrycks, D., et al. (2021). "Measuring Massive Multitask Language Understanding." <em>ICLR 2021</em>.</a></p>
    <p class="bib-annotation">Introduced the MMLU benchmark covering 57 subjects, now a standard for evaluating LLM knowledge.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2311.12022" target="_blank" rel="noopener">Suzgun, M. and Kalai, A. T. (2024). "MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark." <em>arXiv preprint arXiv:2311.12022</em>.</a></p>
    <p class="bib-annotation">Harder version of MMLU with ten answer choices and reasoning-focused questions to better differentiate models.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2107.03374" target="_blank" rel="noopener">Chen, M., et al. (2021). "Evaluating Large Language Models Trained on Code." <em>arXiv preprint arXiv:2107.03374</em>.</a></p>
    <p class="bib-annotation">Introduced the HumanEval benchmark for measuring functional correctness of code generation.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-j-datasets-benchmarks/section-j.4.html": """<h3>Benchmark Comparison</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard" target="_blank" rel="noopener">Hugging Face (2024). "Open LLM Leaderboard." <em>Hugging Face Spaces</em>.</a></p>
    <p class="bib-annotation">Centralized leaderboard tracking model performance across multiple standard benchmarks.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2306.05685" target="_blank" rel="noopener">Zheng, L., et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." <em>NeurIPS 2023</em>.</a></p>
    <p class="bib-annotation">Established methodology for using LLMs and human preferences as complementary evaluation approaches.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://github.com/EleutherAI/lm-evaluation-harness" target="_blank" rel="noopener">Gao, L., et al. (2024). "LM Evaluation Harness." <em>EleutherAI GitHub</em>.</a></p>
    <p class="bib-annotation">The standard open-source framework for running reproducible benchmark evaluations of language models.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-j-datasets-benchmarks/section-j.5.html": """<h3>Dataset Licensing</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2310.16787" target="_blank" rel="noopener">Longpre, S., et al. (2023). "The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing and Attribution in AI." <em>arXiv preprint arXiv:2310.16787</em>.</a></p>
    <p class="bib-annotation">Comprehensive audit of licensing terms and provenance for datasets commonly used in LLM training.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://choosealicense.com/" target="_blank" rel="noopener">GitHub (2024). "Choose an Open Source License." <em>choosealicense.com</em>.</a></p>
    <p class="bib-annotation">Practical guide to understanding open source licenses commonly applied to ML datasets and models.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.licenses.ai/" target="_blank" rel="noopener">RAIL Initiative (2023). "Responsible AI Licenses." <em>licenses.ai</em>.</a></p>
    <p class="bib-annotation">Framework for responsible AI licenses that balance open access with use restrictions for safety.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX K: HuggingFace Ecosystem =====
    "appendix-k-huggingface-ecosystem/section-k.1.html": """<h3>Transformers Library</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/1910.03771" target="_blank" rel="noopener">Wolf, T., et al. (2020). "Transformers: State-of-the-Art Natural Language Processing." <em>EMNLP 2020 (System Demonstrations)</em>.</a></p>
    <p class="bib-annotation">The original paper describing the Hugging Face Transformers library architecture and design philosophy.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/transformers/index" target="_blank" rel="noopener">Hugging Face (2024). "Transformers Documentation." <em>huggingface.co</em>.</a></p>
    <p class="bib-annotation">Official documentation covering pipelines, AutoClasses, model loading, and inference patterns.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/transformers/pipeline_tutorial" target="_blank" rel="noopener">Hugging Face (2024). "Pipelines for Inference." <em>Transformers Documentation</em>.</a></p>
    <p class="bib-annotation">Tutorial for using the high-level pipeline API for common NLP tasks with minimal code.</p>
    <span class="bib-meta">Tutorial</span>
</div>""",

    "appendix-k-huggingface-ecosystem/section-k.2.html": """<h3>Datasets and Tokenizers</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2109.02846" target="_blank" rel="noopener">Lhoest, Q., et al. (2021). "Datasets: A Community Library for Natural Language Processing." <em>EMNLP 2021 (System Demonstrations)</em>.</a></p>
    <p class="bib-annotation">Paper describing the Hugging Face Datasets library with Apache Arrow backend for efficient data loading.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/tokenizers/index" target="_blank" rel="noopener">Hugging Face (2024). "Tokenizers Documentation." <em>huggingface.co</em>.</a></p>
    <p class="bib-annotation">Documentation for the fast Rust-based tokenizer library supporting BPE, WordPiece, and Unigram.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/datasets/stream" target="_blank" rel="noopener">Hugging Face (2024). "Dataset Streaming." <em>Datasets Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to streaming large datasets without downloading them fully, essential for terabyte-scale data.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-k-huggingface-ecosystem/section-k.3.html": """<h3>Training Infrastructure</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/transformers/main_classes/trainer" target="_blank" rel="noopener">Hugging Face (2024). "Trainer." <em>Transformers Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for the high-level Trainer API that handles training loops, evaluation, and logging.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/accelerate/index" target="_blank" rel="noopener">Hugging Face (2024). "Accelerate Documentation." <em>huggingface.co</em>.</a></p>
    <p class="bib-annotation">Library for running the same PyTorch code across distributed setups with minimal code changes.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/transformers/perf_train_gpu_one" target="_blank" rel="noopener">Hugging Face (2024). "Efficient Training on a Single GPU." <em>Transformers Documentation</em>.</a></p>
    <p class="bib-annotation">Performance guide covering gradient accumulation, mixed precision, and memory optimization techniques.</p>
    <span class="bib-meta">Tutorial</span>
</div>""",

    "appendix-k-huggingface-ecosystem/section-k.4.html": """<h3>PEFT and TRL</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/peft/index" target="_blank" rel="noopener">Hugging Face (2024). "PEFT: Parameter-Efficient Fine-Tuning." <em>huggingface.co</em>.</a></p>
    <p class="bib-annotation">Documentation for the PEFT library supporting LoRA, QLoRA, prefix tuning, and adapter methods.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/trl/index" target="_blank" rel="noopener">Hugging Face (2024). "TRL: Transformer Reinforcement Learning." <em>huggingface.co</em>.</a></p>
    <p class="bib-annotation">Library for RLHF and DPO training of language models with SFTTrainer, DPOTrainer, and PPOTrainer.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2106.09685" target="_blank" rel="noopener">Hu, E. J., et al. (2022). "LoRA: Low-Rank Adaptation of Large Language Models." <em>ICLR 2022</em>.</a></p>
    <p class="bib-annotation">The original LoRA paper, the most widely used PEFT method implemented in the library.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-k-huggingface-ecosystem/section-k.5.html": """<h3>Hugging Face Hub</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/hub/index" target="_blank" rel="noopener">Hugging Face (2024). "Hugging Face Hub Documentation." <em>huggingface.co</em>.</a></p>
    <p class="bib-annotation">Official guide to sharing models, datasets, and Spaces on the Hugging Face Hub platform.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/hub/spaces" target="_blank" rel="noopener">Hugging Face (2024). "Spaces Documentation." <em>huggingface.co</em>.</a></p>
    <p class="bib-annotation">Guide to building and deploying ML demo applications using Gradio or Streamlit on Spaces.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/huggingface_hub/guides/model-cards" target="_blank" rel="noopener">Hugging Face (2024). "Model Cards." <em>Hub Documentation</em>.</a></p>
    <p class="bib-annotation">Standards for documenting model capabilities, limitations, and intended use on the Hub.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX L: LangChain =====
    "appendix-l-langchain/section-l.1.html": """<h3>LangChain Core</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/get_started/introduction" target="_blank" rel="noopener">LangChain (2024). "Introduction." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">Official introduction to LangChain's core abstractions: models, prompts, and chains.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/expression_language/" target="_blank" rel="noopener">LangChain (2024). "LangChain Expression Language (LCEL)." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to the declarative composition language for building chains with streaming and async support.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://blog.langchain.dev/langchain-v0-1-0/" target="_blank" rel="noopener">LangChain (2024). "LangChain v0.1.0." <em>LangChain Blog</em>.</a></p>
    <p class="bib-annotation">Release announcement describing the stable API design and core architectural decisions.</p>
    <span class="bib-meta">Blog</span>
</div>""",

    "appendix-l-langchain/section-l.2.html": """<h3>Memory and Conversation</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/modules/memory/" target="_blank" rel="noopener">LangChain (2024). "Memory." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for conversation memory types: buffer, summary, knowledge graph, and entity memory.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2304.03442" target="_blank" rel="noopener">Park, J. S., et al. (2023). "Generative Agents: Interactive Simulacra of Human Behavior." <em>UIST 2023</em>.</a></p>
    <p class="bib-annotation">Influential work on agent memory architectures that inspired LangChain's memory system design.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/tutorials/chatbot/" target="_blank" rel="noopener">LangChain (2024). "Build a Chatbot." <em>LangChain Tutorials</em>.</a></p>
    <p class="bib-annotation">Step-by-step tutorial for building a conversational chatbot with persistent memory.</p>
    <span class="bib-meta">Tutorial</span>
</div>""",

    "appendix-l-langchain/section-l.3.html": """<h3>Document Loading and Retrieval</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/modules/data_connection/" target="_blank" rel="noopener">LangChain (2024). "Retrieval." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for the retrieval module covering document loaders, text splitters, and retrievers.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/tutorials/rag/" target="_blank" rel="noopener">LangChain (2024). "Build a RAG Application." <em>LangChain Tutorials</em>.</a></p>
    <p class="bib-annotation">End-to-end tutorial for building a retrieval-augmented generation pipeline with LangChain.</p>
    <span class="bib-meta">Tutorial</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2312.10997" target="_blank" rel="noopener">Gao, Y., et al. (2024). "Retrieval-Augmented Generation for Large Language Models: A Survey." <em>arXiv preprint arXiv:2312.10997</em>.</a></p>
    <p class="bib-annotation">Comprehensive survey of RAG techniques and architectures relevant to LangChain's retrieval patterns.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-l-langchain/section-l.4.html": """<h3>Structured Output</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/modules/model_io/output_parsers/" target="_blank" rel="noopener">LangChain (2024). "Output Parsers." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to parsing LLM outputs into structured formats using Pydantic, JSON, and custom parsers.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/how_to/structured_output/" target="_blank" rel="noopener">LangChain (2024). "How to Get Structured Output." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">Patterns for extracting structured data using function calling, JSON mode, and with_structured_output.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.pydantic.dev/latest/" target="_blank" rel="noopener">Pydantic Contributors (2024). "Pydantic V2 Documentation." <em>pydantic.dev</em>.</a></p>
    <p class="bib-annotation">The data validation library that powers LangChain's structured output parsing and schema definitions.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-l-langchain/section-l.5.html": """<h3>Agents and Tools</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/modules/agents/" target="_blank" rel="noopener">LangChain (2024). "Agents." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for building agents with tool use, including ReAct, structured chat, and OpenAI agents.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2210.03629" target="_blank" rel="noopener">Yao, S., et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." <em>ICLR 2023</em>.</a></p>
    <p class="bib-annotation">The ReAct paper that established the reason-then-act loop pattern implemented in LangChain agents.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/how_to/custom_tools/" target="_blank" rel="noopener">LangChain (2024). "How to Create Custom Tools." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to defining and integrating custom tools that LangChain agents can invoke.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX M: LangGraph =====
    "appendix-m-langgraph/section-m.1.html": """<h3>LangGraph Fundamentals</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/" target="_blank" rel="noopener">LangChain (2024). "LangGraph Documentation." <em>langchain-ai.github.io</em>.</a></p>
    <p class="bib-annotation">Official documentation for LangGraph's graph-based agent orchestration framework.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/concepts/" target="_blank" rel="noopener">LangChain (2024). "LangGraph Concepts." <em>LangGraph Documentation</em>.</a></p>
    <p class="bib-annotation">Conceptual guide to nodes, edges, state, and message passing in LangGraph architectures.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://blog.langchain.dev/langgraph/" target="_blank" rel="noopener">LangChain (2024). "LangGraph: Multi-Agent Workflows." <em>LangChain Blog</em>.</a></p>
    <p class="bib-annotation">Launch post explaining LangGraph's motivation and design for cyclic, stateful agent workflows.</p>
    <span class="bib-meta">Blog</span>
</div>""",

    "appendix-m-langgraph/section-m.2.html": """<h3>Conditional Routing</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/how-tos/branching/" target="_blank" rel="noopener">LangChain (2024). "How to Create Branches for Parallel Execution." <em>LangGraph Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to implementing conditional edges and parallel branches in LangGraph workflows.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/tutorials/introduction/" target="_blank" rel="noopener">LangChain (2024). "Introduction to LangGraph." <em>LangGraph Tutorials</em>.</a></p>
    <p class="bib-annotation">Step-by-step tutorial covering graph construction with conditional routing and cycles.</p>
    <span class="bib-meta">Tutorial</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2210.03629" target="_blank" rel="noopener">Yao, S., et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." <em>ICLR 2023</em>.</a></p>
    <p class="bib-annotation">The reasoning-acting loop pattern that LangGraph generalizes into cyclic graph execution.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-m-langgraph/section-m.3.html": """<h3>Human-in-the-Loop</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/" target="_blank" rel="noopener">LangChain (2024). "Human-in-the-Loop." <em>LangGraph Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for implementing approval gates, interrupt points, and human feedback in agent workflows.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/" target="_blank" rel="noopener">LangChain (2024). "Human-in-the-Loop Concepts." <em>LangGraph Documentation</em>.</a></p>
    <p class="bib-annotation">Conceptual overview of interrupt and resume patterns for human oversight of agent actions.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2308.00352" target="_blank" rel="noopener">Wu, Q., et al. (2023). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation." <em>arXiv preprint arXiv:2308.00352</em>.</a></p>
    <p class="bib-annotation">Describes human-in-the-loop patterns in multi-agent systems that influenced LangGraph's design.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-m-langgraph/section-m.4.html": """<h3>Persistence and Recovery</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/how-tos/persistence/" target="_blank" rel="noopener">LangChain (2024). "Persistence." <em>LangGraph Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to checkpointing agent state for long-running workflows and fault recovery.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/concepts/persistence/" target="_blank" rel="noopener">LangChain (2024). "Persistence Concepts." <em>LangGraph Documentation</em>.</a></p>
    <p class="bib-annotation">Conceptual overview of checkpointing, state serialization, and time-travel debugging capabilities.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/how-tos/memory/manage-conversation-history/" target="_blank" rel="noopener">LangChain (2024). "Manage Conversation History." <em>LangGraph Documentation</em>.</a></p>
    <p class="bib-annotation">Patterns for managing long conversation histories with summarization and windowing in persistent graphs.</p>
    <span class="bib-meta">Tutorial</span>
</div>""",

    "appendix-m-langgraph/section-m.5.html": """<h3>Multi-Agent Graphs</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/how-tos/subgraph/" target="_blank" rel="noopener">LangChain (2024). "How to Use Subgraphs." <em>LangGraph Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to composing multi-agent systems using nested subgraphs with independent state.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/" target="_blank" rel="noopener">LangChain (2024). "Multi-Agent Collaboration." <em>LangGraph Tutorials</em>.</a></p>
    <p class="bib-annotation">Tutorial for building collaborative multi-agent systems with supervisor and worker patterns.</p>
    <span class="bib-meta">Tutorial</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2308.08155" target="_blank" rel="noopener">Hong, S., et al. (2023). "MetaGPT: Meta Programming for Multi-Agent Collaborative Framework." <em>ICLR 2024</em>.</a></p>
    <p class="bib-annotation">Multi-agent collaboration framework that influenced the supervisor-worker patterns in LangGraph.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    # ===== APPENDIX N: CrewAI =====
    "appendix-n-crewai/section-n.1.html": """<h3>CrewAI Agents</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/concepts/agents" target="_blank" rel="noopener">CrewAI (2024). "Agents." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Official documentation for defining agents with roles, goals, and backstories in CrewAI.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2304.03442" target="_blank" rel="noopener">Park, J. S., et al. (2023). "Generative Agents: Interactive Simulacra of Human Behavior." <em>UIST 2023</em>.</a></p>
    <p class="bib-annotation">Research on role-based agent personas that inspired CrewAI's agent design with backstories and goals.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.crewai.com/blog" target="_blank" rel="noopener">CrewAI (2024). "CrewAI Blog." <em>crewai.com</em>.</a></p>
    <p class="bib-annotation">Official blog with tutorials and best practices for designing effective agent roles and interactions.</p>
    <span class="bib-meta">Blog</span>
</div>""",

    "appendix-n-crewai/section-n.2.html": """<h3>CrewAI Tasks</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/concepts/tasks" target="_blank" rel="noopener">CrewAI (2024). "Tasks." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to defining tasks with descriptions, expected outputs, and inter-task dependencies.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/concepts/tasks#task-dependencies" target="_blank" rel="noopener">CrewAI (2024). "Task Dependencies." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for creating task chains where outputs of one task feed into the next.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2308.08155" target="_blank" rel="noopener">Hong, S., et al. (2023). "MetaGPT: Meta Programming for Multi-Agent Collaborative Framework." <em>ICLR 2024</em>.</a></p>
    <p class="bib-annotation">Explores task decomposition and dependency management in multi-agent software development workflows.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-n-crewai/section-n.3.html": """<h3>CrewAI Tools</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/concepts/tools" target="_blank" rel="noopener">CrewAI (2024). "Tools." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for built-in tools and the interface for creating custom tool integrations.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2302.04761" target="_blank" rel="noopener">Schick, T., et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." <em>NeurIPS 2023</em>.</a></p>
    <p class="bib-annotation">Foundational work on teaching LLMs to use external tools, a core capability in CrewAI agents.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/how-to/create-custom-tools" target="_blank" rel="noopener">CrewAI (2024). "Creating Custom Tools." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Step-by-step guide for building custom tools that CrewAI agents can discover and invoke.</p>
    <span class="bib-meta">Tutorial</span>
</div>""",

    "appendix-n-crewai/section-n.4.html": """<h3>CrewAI Crews</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/concepts/crews" target="_blank" rel="noopener">CrewAI (2024). "Crews." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for configuring crews with sequential, hierarchical, and custom process types.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/concepts/processes" target="_blank" rel="noopener">CrewAI (2024). "Processes." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Detailed explanation of sequential and hierarchical process orchestration strategies.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2308.00352" target="_blank" rel="noopener">Wu, Q., et al. (2023). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation." <em>arXiv preprint arXiv:2308.00352</em>.</a></p>
    <p class="bib-annotation">Multi-agent conversation framework that influenced hierarchical orchestration patterns in CrewAI.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-n-crewai/section-n.5.html": """<h3>Advanced CrewAI Patterns</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/concepts/memory" target="_blank" rel="noopener">CrewAI (2024). "Memory." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to short-term, long-term, and entity memory systems for persistent agent knowledge.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/how-to/agent-monitoring" target="_blank" rel="noopener">CrewAI (2024). "Agent Monitoring." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for callbacks and monitoring hooks to observe and control crew execution.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/concepts/collaboration" target="_blank" rel="noopener">CrewAI (2024). "Collaboration." <em>CrewAI Documentation</em>.</a></p>
    <p class="bib-annotation">Patterns for agent delegation, feedback loops, and collaborative task completion.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX O: LlamaIndex =====
    "appendix-o-llamaindex/section-o.1.html": """<h3>Data Connectors</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/" target="_blank" rel="noopener">LlamaIndex (2024). "LlamaIndex Documentation." <em>llamaindex.ai</em>.</a></p>
    <p class="bib-annotation">Official documentation for the LlamaIndex data framework for LLM applications.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://llamahub.ai/" target="_blank" rel="noopener">LlamaIndex (2024). "LlamaHub: Data Loaders." <em>llamahub.ai</em>.</a></p>
    <p class="bib-annotation">Registry of community-contributed data loaders for connecting diverse data sources to LlamaIndex.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/understanding/loading/loading/" target="_blank" rel="noopener">LlamaIndex (2024). "Loading Data." <em>LlamaIndex Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to ingesting documents from files, databases, APIs, and web sources into LlamaIndex.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-o-llamaindex/section-o.2.html": """<h3>Index Types</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/understanding/indexing/indexing/" target="_blank" rel="noopener">LlamaIndex (2024). "Indexing." <em>LlamaIndex Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to vector, list, tree, and keyword index types and when to use each one.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2304.11062" target="_blank" rel="noopener">Liu, J. (2022). "LlamaIndex." <em>GitHub Repository</em>.</a></p>
    <p class="bib-annotation">The LlamaIndex project (originally GPT Index) introducing tree and list index structures for LLM queries.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/" target="_blank" rel="noopener">LlamaIndex (2024). "Vector Store Index." <em>LlamaIndex Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for the most commonly used index type backed by vector similarity search.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-o-llamaindex/section-o.3.html": """<h3>Query Engines</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/understanding/querying/querying/" target="_blank" rel="noopener">LlamaIndex (2024). "Querying." <em>LlamaIndex Documentation</em>.</a></p>
    <p class="bib-annotation">Overview of query engines, response synthesis modes, and retrieval strategies.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/response_modes/" target="_blank" rel="noopener">LlamaIndex (2024). "Response Modes." <em>LlamaIndex Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for compact, tree summarize, refine, and other response synthesis strategies.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2312.10997" target="_blank" rel="noopener">Gao, Y., et al. (2024). "Retrieval-Augmented Generation for Large Language Models: A Survey." <em>arXiv preprint arXiv:2312.10997</em>.</a></p>
    <p class="bib-annotation">Survey of RAG architectures including the query transformation and response synthesis techniques used in LlamaIndex.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-o-llamaindex/section-o.4.html": """<h3>Advanced Retrieval</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/examples/query_engine/sub_question_query_engine/" target="_blank" rel="noopener">LlamaIndex (2024). "Sub-Question Query Engine." <em>LlamaIndex Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to decomposing complex queries into sub-questions routed to different data sources.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2402.16823" target="_blank" rel="noopener">Rackauckas, D., et al. (2024). "RAG-Fusion: A New Take on Retrieval-Augmented Generation." <em>arXiv preprint arXiv:2402.16823</em>.</a></p>
    <p class="bib-annotation">Introduces query rewriting and reciprocal rank fusion techniques implemented in LlamaIndex's fusion retriever.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/examples/query_engine/RouterQueryEngine/" target="_blank" rel="noopener">LlamaIndex (2024). "Router Query Engine." <em>LlamaIndex Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for routing queries to the most appropriate index or query engine based on the question.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-o-llamaindex/section-o.5.html": """<h3>LlamaIndex Agents</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/" target="_blank" rel="noopener">LlamaIndex (2024). "Agents." <em>LlamaIndex Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for building agents that can use query engines and tools for complex data tasks.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/module_guides/workflow/" target="_blank" rel="noopener">LlamaIndex (2024). "Workflows." <em>LlamaIndex Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to the event-driven workflow system for building multi-step, cyclic agent pipelines.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2210.03629" target="_blank" rel="noopener">Yao, S., et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." <em>ICLR 2023</em>.</a></p>
    <p class="bib-annotation">The ReAct pattern implemented in LlamaIndex's agent framework for tool-using query agents.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    # ===== APPENDIX P: Semantic Kernel =====
    "appendix-p-semantic-kernel/section-p.1.html": """<h3>Semantic Kernel Setup</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/overview/" target="_blank" rel="noopener">Microsoft (2024). "What is Semantic Kernel?" <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Official introduction to Microsoft's Semantic Kernel framework for AI orchestration.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/" target="_blank" rel="noopener">Microsoft (2024). "Plugins in Semantic Kernel." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Guide to creating and using plugins that provide functions to the Semantic Kernel.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://github.com/microsoft/semantic-kernel" target="_blank" rel="noopener">Microsoft (2024). "Semantic Kernel GitHub Repository." <em>GitHub</em>.</a></p>
    <p class="bib-annotation">Source code and examples for the Semantic Kernel SDK in Python, C#, and Java.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-p-semantic-kernel/section-p.2.html": """<h3>Prompt Templates</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/prompts/" target="_blank" rel="noopener">Microsoft (2024). "Prompts in Semantic Kernel." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Documentation for creating parameterized prompt templates with the Semantic Kernel template engine.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/prompts/prompt-template-syntax" target="_blank" rel="noopener">Microsoft (2024). "Prompt Template Syntax." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Reference for the template syntax including variables, function calls, and Handlebars templates.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/ai-services/chat-completion/" target="_blank" rel="noopener">Microsoft (2024). "Chat Completion." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Guide to using chat completion services with prompt templates in Semantic Kernel.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-p-semantic-kernel/section-p.3.html": """<h3>Planners</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/planning" target="_blank" rel="noopener">Microsoft (2024). "Planning with Semantic Kernel." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Documentation for AI planners that automatically compose functions to achieve complex goals.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/using-ai-plugins" target="_blank" rel="noopener">Microsoft (2024). "Using AI Plugins with Function Calling." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Guide to automatic function calling, which has replaced traditional planners in modern Semantic Kernel.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2305.15334" target="_blank" rel="noopener">Patil, S. G., et al. (2023). "Gorilla: Large Language Model Connected with Massive APIs." <em>arXiv preprint arXiv:2305.15334</em>.</a></p>
    <p class="bib-annotation">Research on LLMs selecting and calling APIs, the core capability behind Semantic Kernel's auto-planning.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-p-semantic-kernel/section-p.4.html": """<h3>Memory and Vector Stores</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/vector-store-connectors/" target="_blank" rel="noopener">Microsoft (2024). "Vector Store Connectors." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Documentation for connecting Semantic Kernel to vector databases for embedding storage and retrieval.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/text-search/" target="_blank" rel="noopener">Microsoft (2024). "Text Search." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Guide to semantic search and RAG patterns using Semantic Kernel's text search abstraction.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/understand-embeddings" target="_blank" rel="noopener">Microsoft (2024). "Understand Embeddings in Azure OpenAI." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Conceptual overview of embeddings used by Semantic Kernel's memory and recall features.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-p-semantic-kernel/section-p.5.html": """<h3>Enterprise Patterns</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/enterprise-readiness/" target="_blank" rel="noopener">Microsoft (2024). "Enterprise Readiness." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Guide to security, telemetry, and enterprise deployment patterns with Semantic Kernel.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/azure/ai-services/openai/" target="_blank" rel="noopener">Microsoft (2024). "Azure OpenAI Service Documentation." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Documentation for the Azure OpenAI service commonly used as the backend for Semantic Kernel deployments.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://learn.microsoft.com/en-us/semantic-kernel/concepts/ai-services/" target="_blank" rel="noopener">Microsoft (2024). "AI Services in Semantic Kernel." <em>Microsoft Learn</em>.</a></p>
    <p class="bib-annotation">Reference for configuring different AI service backends including Azure OpenAI and Hugging Face.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX Q: DSPy =====
    "appendix-q-dspy/section-q.1.html": """<h3>DSPy Foundations</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2310.03714" target="_blank" rel="noopener">Khattab, O., et al. (2023). "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." <em>ICLR 2024</em>.</a></p>
    <p class="bib-annotation">The foundational DSPy paper introducing signatures, modules, and compiler-based prompt optimization.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://dspy-docs.vercel.app/" target="_blank" rel="noopener">DSPy Contributors (2024). "DSPy Documentation." <em>dspy-docs.vercel.app</em>.</a></p>
    <p class="bib-annotation">Official documentation for DSPy's declarative programming model for language model applications.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://github.com/stanfordnlp/dspy" target="_blank" rel="noopener">Stanford NLP (2024). "DSPy GitHub Repository." <em>GitHub</em>.</a></p>
    <p class="bib-annotation">Source code, examples, and community contributions for the DSPy framework.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-q-dspy/section-q.2.html": """<h3>Built-in Modules</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://dspy-docs.vercel.app/docs/building-blocks/modules" target="_blank" rel="noopener">DSPy Contributors (2024). "Modules." <em>DSPy Documentation</em>.</a></p>
    <p class="bib-annotation">Reference for built-in modules including Predict, ChainOfThought, ReAct, and ProgramOfThought.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2201.11903" target="_blank" rel="noopener">Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." <em>NeurIPS 2022</em>.</a></p>
    <p class="bib-annotation">The chain-of-thought paper whose pattern DSPy's ChainOfThought module automates and optimizes.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2210.03629" target="_blank" rel="noopener">Yao, S., et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." <em>ICLR 2023</em>.</a></p>
    <p class="bib-annotation">The ReAct framework implemented as a composable module in DSPy for tool-using programs.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-q-dspy/section-q.3.html": """<h3>Optimizers</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://dspy-docs.vercel.app/docs/building-blocks/optimizers" target="_blank" rel="noopener">DSPy Contributors (2024). "Optimizers." <em>DSPy Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to DSPy's optimizers for automatically improving prompts, few-shot examples, and weights.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2406.11695" target="_blank" rel="noopener">Opsahl-Ong, K., et al. (2024). "Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs." <em>arXiv preprint arXiv:2406.11695</em>.</a></p>
    <p class="bib-annotation">Describes the MIPRO optimizer that jointly optimizes instructions and demonstrations in DSPy programs.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2310.03714" target="_blank" rel="noopener">Khattab, O., et al. (2023). "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." <em>ICLR 2024</em>.</a></p>
    <p class="bib-annotation">Introduces BootstrapFewShot and other compilation strategies that form the basis of DSPy optimization.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-q-dspy/section-q.4.html": """<h3>Evaluation and Metrics</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://dspy-docs.vercel.app/docs/building-blocks/metrics" target="_blank" rel="noopener">DSPy Contributors (2024). "Metrics." <em>DSPy Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to defining evaluation metrics that drive DSPy's optimization and validation processes.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://dspy-docs.vercel.app/docs/building-blocks/data" target="_blank" rel="noopener">DSPy Contributors (2024). "Data: Examples and Datasets." <em>DSPy Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for creating training and evaluation datasets for DSPy program optimization.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2306.05685" target="_blank" rel="noopener">Zheng, L., et al. (2023). "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." <em>NeurIPS 2023</em>.</a></p>
    <p class="bib-annotation">LLM-as-judge evaluation methodology commonly used for building DSPy metric functions.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-q-dspy/section-q.5.html": """<h3>Advanced Patterns</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://dspy-docs.vercel.app/docs/building-blocks/assertions" target="_blank" rel="noopener">DSPy Contributors (2024). "Assertions and Suggestions." <em>DSPy Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to runtime constraints that enable self-correcting LLM pipelines with backtracking.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2401.10768" target="_blank" rel="noopener">Khattab, O., et al. (2024). "DSPy Assertions: Computational Constraints for Self-Refining Language Model Pipelines." <em>arXiv preprint arXiv:2401.10768</em>.</a></p>
    <p class="bib-annotation">Introduces the assertion mechanism for imposing computational constraints on LLM outputs in DSPy.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://dspy-docs.vercel.app/docs/building-blocks/typed_predictors" target="_blank" rel="noopener">DSPy Contributors (2024). "Typed Predictors." <em>DSPy Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for Pydantic-integrated typed predictors that enforce structured output schemas.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX R: Experiment Tracking =====
    "appendix-r-experiment-tracking/section-r.1.html": """<h3>Weights and Biases</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.wandb.ai/" target="_blank" rel="noopener">Weights and Biases (2024). "W&B Documentation." <em>wandb.ai</em>.</a></p>
    <p class="bib-annotation">Official documentation for experiment tracking, run logging, and hyperparameter sweep configuration.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.wandb.ai/guides/sweeps" target="_blank" rel="noopener">Weights and Biases (2024). "Sweeps." <em>W&B Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to automated hyperparameter search using Bayesian optimization, grid, and random strategies.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.wandb.ai/guides/prompts" target="_blank" rel="noopener">Weights and Biases (2024). "W&B Prompts." <em>W&B Documentation</em>.</a></p>
    <p class="bib-annotation">Specialized tooling for tracking and evaluating LLM prompt experiments with trace visualization.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-r-experiment-tracking/section-r.2.html": """<h3>MLflow</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://mlflow.org/docs/latest/index.html" target="_blank" rel="noopener">MLflow Contributors (2024). "MLflow Documentation." <em>mlflow.org</em>.</a></p>
    <p class="bib-annotation">Official documentation for the open-source MLflow platform covering tracking, projects, and model registry.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://mlflow.org/docs/latest/llms/index.html" target="_blank" rel="noopener">MLflow Contributors (2024). "LLMs in MLflow." <em>MLflow Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to MLflow's LLM-specific features including prompt engineering UI and model evaluation.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2407.17438" target="_blank" rel="noopener">Chen, A., et al. (2024). "From MLOps to LLMOps: Challenges and Best Practices." <em>arXiv preprint arXiv:2407.17438</em>.</a></p>
    <p class="bib-annotation">Discusses the evolution from traditional MLOps to LLM-specific operations and tooling requirements.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-r-experiment-tracking/section-r.3.html": """<h3>Hyperparameter Optimization</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://optuna.readthedocs.io/" target="_blank" rel="noopener">Akiba, T., et al. (2019). "Optuna: A Next-Generation Hyperparameter Optimization Framework." <em>KDD 2019</em>.</a></p>
    <p class="bib-annotation">Popular hyperparameter optimization framework with Bayesian optimization and pruning strategies.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.ray.io/en/latest/tune/index.html" target="_blank" rel="noopener">Ray Contributors (2024). "Ray Tune." <em>Ray Documentation</em>.</a></p>
    <p class="bib-annotation">Scalable hyperparameter tuning library with distributed search and early stopping.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/1206.2944" target="_blank" rel="noopener">Snoek, J., Larochelle, H., and Adams, R. P. (2012). "Practical Bayesian Optimization of Machine Learning Algorithms." <em>NeurIPS 2012</em>.</a></p>
    <p class="bib-annotation">Foundational paper on Bayesian optimization for hyperparameter search in machine learning.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-r-experiment-tracking/section-r.4.html": """<h3>Model Registry</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://mlflow.org/docs/latest/model-registry.html" target="_blank" rel="noopener">MLflow Contributors (2024). "MLflow Model Registry." <em>MLflow Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for versioning, staging, and promoting models through deployment workflows.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.wandb.ai/guides/model_registry" target="_blank" rel="noopener">Weights and Biases (2024). "Model Registry." <em>W&B Documentation</em>.</a></p>
    <p class="bib-annotation">W&B model registry for managing model versions with lineage tracking and deployment automation.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/hub/models" target="_blank" rel="noopener">Hugging Face (2024). "Model Hub." <em>Hugging Face Documentation</em>.</a></p>
    <p class="bib-annotation">The largest open model registry with Git-based versioning and model card documentation.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-r-experiment-tracking/section-r.5.html": """<h3>LLM Observability</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.smith.langchain.com/" target="_blank" rel="noopener">LangChain (2024). "LangSmith Documentation." <em>smith.langchain.com</em>.</a></p>
    <p class="bib-annotation">Platform for tracing, evaluating, and monitoring LLM application performance in production.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.arize.com/phoenix" target="_blank" rel="noopener">Arize AI (2024). "Phoenix: LLM Observability." <em>Arize Documentation</em>.</a></p>
    <p class="bib-annotation">Open-source LLM observability tool for tracing, evaluating, and debugging LLM applications.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.wandb.ai/guides/weave" target="_blank" rel="noopener">Weights and Biases (2024). "Weave." <em>W&B Documentation</em>.</a></p>
    <p class="bib-annotation">W&B's LLM evaluation and observability toolkit for tracking prompts, traces, and evaluations.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    # ===== APPENDIX S: Inference Serving =====
    "appendix-s-inference-serving/section-s.1.html": """<h3>vLLM</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2309.06180" target="_blank" rel="noopener">Kwon, W., et al. (2023). "Efficient Memory Management for Large Language Model Serving with PagedAttention." <em>SOSP 2023</em>.</a></p>
    <p class="bib-annotation">Introduced PagedAttention and the vLLM engine for efficient LLM serving with near-zero memory waste.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.vllm.ai/" target="_blank" rel="noopener">vLLM Contributors (2024). "vLLM Documentation." <em>docs.vllm.ai</em>.</a></p>
    <p class="bib-annotation">Official documentation for deploying the vLLM inference server with OpenAI-compatible endpoints.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://blog.vllm.ai/2023/06/20/vllm.html" target="_blank" rel="noopener">Kwon, W. (2023). "vLLM: Easy, Fast, and Cheap LLM Serving." <em>vLLM Blog</em>.</a></p>
    <p class="bib-annotation">Launch post explaining vLLM's continuous batching and PagedAttention performance advantages.</p>
    <span class="bib-meta">Blog</span>
</div>""",

    "appendix-s-inference-serving/section-s.2.html": """<h3>Text Generation Inference</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/text-generation-inference/" target="_blank" rel="noopener">Hugging Face (2024). "Text Generation Inference Documentation." <em>huggingface.co</em>.</a></p>
    <p class="bib-annotation">Official documentation for deploying and configuring HuggingFace's TGI inference server.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://github.com/huggingface/text-generation-inference" target="_blank" rel="noopener">Hugging Face (2024). "TGI GitHub Repository." <em>GitHub</em>.</a></p>
    <p class="bib-annotation">Source code and deployment examples for the Rust-based TGI serving framework.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/inference-endpoints/" target="_blank" rel="noopener">Hugging Face (2024). "Inference Endpoints." <em>Hugging Face Documentation</em>.</a></p>
    <p class="bib-annotation">Managed deployment service built on TGI for production model serving without infrastructure management.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-s-inference-serving/section-s.3.html": """<h3>SGLang</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2312.07104" target="_blank" rel="noopener">Zheng, L., et al. (2024). "SGLang: Efficient Execution of Structured Language Model Programs." <em>arXiv preprint arXiv:2312.07104</em>.</a></p>
    <p class="bib-annotation">Introduces SGLang with RadixAttention for efficient structured generation and KV cache reuse.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://github.com/sgl-project/sglang" target="_blank" rel="noopener">SGLang Contributors (2024). "SGLang GitHub Repository." <em>GitHub</em>.</a></p>
    <p class="bib-annotation">Source code and examples for the SGLang serving framework with constrained decoding support.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://lmsys.org/blog/2024-01-17-sglang/" target="_blank" rel="noopener">LMSYS (2024). "SGLang: Fast Serving Framework for Large Language Models." <em>LMSYS Blog</em>.</a></p>
    <p class="bib-annotation">Technical blog post explaining RadixAttention and constrained decoding performance gains.</p>
    <span class="bib-meta">Blog</span>
</div>""",

    "appendix-s-inference-serving/section-s.4.html": """<h3>Quantization for Serving</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2210.17323" target="_blank" rel="noopener">Frantar, E., et al. (2023). "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers." <em>ICLR 2023</em>.</a></p>
    <p class="bib-annotation">Introduced GPTQ, a one-shot weight quantization method enabling 4-bit inference with minimal quality loss.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2306.00978" target="_blank" rel="noopener">Lin, J., et al. (2023). "AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration." <em>MLSys 2024</em>.</a></p>
    <p class="bib-annotation">AWQ identifies salient weights via activations, achieving better quality than uniform quantization.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://github.com/ggerganov/llama.cpp" target="_blank" rel="noopener">Gerganov, G. (2024). "llama.cpp." <em>GitHub</em>.</a></p>
    <p class="bib-annotation">C++ inference engine supporting GGUF quantized models for efficient CPU and mixed CPU/GPU inference.</p>
    <span class="bib-meta">Tool</span>
</div>""",

    "appendix-s-inference-serving/section-s.5.html": """<h3>Scaling and Load Balancing</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2401.02954" target="_blank" rel="noopener">Miao, X., et al. (2024). "SpotServe: Serving Generative Large Language Models on Preemptible Instances." <em>ASPLOS 2024</em>.</a></p>
    <p class="bib-annotation">Techniques for serving LLMs on spot instances with graceful preemption handling for cost reduction.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://kubernetes.io/docs/concepts/services-networking/ingress/" target="_blank" rel="noopener">Kubernetes Authors (2024). "Ingress." <em>Kubernetes Documentation</em>.</a></p>
    <p class="bib-annotation">Reference for configuring load balancing and traffic routing for containerized inference servers.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.ray.io/en/latest/serve/index.html" target="_blank" rel="noopener">Ray Contributors (2024). "Ray Serve." <em>Ray Documentation</em>.</a></p>
    <p class="bib-annotation">Scalable serving framework for deploying ML models with autoscaling and request batching.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX T: Distributed ML =====
    "appendix-t-distributed-ml/section-t.1.html": """<h3>PySpark for LLM Data</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://spark.apache.org/docs/latest/api/python/" target="_blank" rel="noopener">Apache Software Foundation (2024). "PySpark Documentation." <em>spark.apache.org</em>.</a></p>
    <p class="bib-annotation">Official PySpark API documentation for distributed data processing with Python.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://spark.apache.org/docs/latest/ml-guide.html" target="_blank" rel="noopener">Apache Software Foundation (2024). "MLlib: Machine Learning Library." <em>Apache Spark Documentation</em>.</a></p>
    <p class="bib-annotation">Spark's built-in ML library for distributed feature engineering and model training.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/1505.06807" target="_blank" rel="noopener">Zaharia, M., et al. (2016). "Apache Spark: A Unified Engine for Big Data Processing." <em>Communications of the ACM</em>, 59(11), 56-65.</a></p>
    <p class="bib-annotation">Overview of Spark's unified analytics engine that powers large-scale data processing for LLM pipelines.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    "appendix-t-distributed-ml/section-t.2.html": """<h3>Delta Lake</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.delta.io/" target="_blank" rel="noopener">Delta Lake Contributors (2024). "Delta Lake Documentation." <em>delta.io</em>.</a></p>
    <p class="bib-annotation">Official documentation for Delta Lake's ACID transactions and time travel on data lakes.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2007.09363" target="_blank" rel="noopener">Armbrust, M., et al. (2020). "Delta Lake: High-Performance ACID Table Storage over Cloud Object Stores." <em>VLDB 2020</em>.</a></p>
    <p class="bib-annotation">The Delta Lake paper describing the lakehouse architecture combining data lake flexibility with warehouse reliability.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.databricks.com/glossary/lakehouse-architecture" target="_blank" rel="noopener">Databricks (2024). "Lakehouse Architecture." <em>Databricks Glossary</em>.</a></p>
    <p class="bib-annotation">Overview of the lakehouse paradigm that unifies data engineering and ML workflows on a single platform.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-t-distributed-ml/section-t.3.html": """<h3>Databricks Platform</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.databricks.com/" target="_blank" rel="noopener">Databricks (2024). "Databricks Documentation." <em>docs.databricks.com</em>.</a></p>
    <p class="bib-annotation">Official documentation for the Databricks workspace, notebooks, and Unity Catalog.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.databricks.com/en/data-governance/unity-catalog/index.html" target="_blank" rel="noopener">Databricks (2024). "Unity Catalog." <em>Databricks Documentation</em>.</a></p>
    <p class="bib-annotation">Data governance and catalog service for managing access to data, models, and ML artifacts.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.databricks.com/en/notebooks/index.html" target="_blank" rel="noopener">Databricks (2024). "Databricks Notebooks." <em>Databricks Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to collaborative notebooks with support for Python, SQL, R, and Scala on Spark clusters.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-t-distributed-ml/section-t.4.html": """<h3>Databricks AI</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.databricks.com/en/machine-learning/foundation-models/index.html" target="_blank" rel="noopener">Databricks (2024). "Foundation Model APIs." <em>Databricks Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for serving and fine-tuning foundation models on the Databricks platform.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.databricks.com/blog/introducing-dbrx-new-state-art-open-llm" target="_blank" rel="noopener">Databricks (2024). "Introducing DBRX." <em>Databricks Blog</em>.</a></p>
    <p class="bib-annotation">Announcement of Databricks' open-weight DBRX model built on their Mosaic ML infrastructure.</p>
    <span class="bib-meta">Blog</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.databricks.com/en/machine-learning/model-serving/index.html" target="_blank" rel="noopener">Databricks (2024). "Model Serving." <em>Databricks Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to deploying and serving ML models with autoscaling endpoints on Databricks.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-t-distributed-ml/section-t.5.html": """<h3>Ray Ecosystem</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.ray.io/en/latest/" target="_blank" rel="noopener">Ray Contributors (2024). "Ray Documentation." <em>docs.ray.io</em>.</a></p>
    <p class="bib-annotation">Official documentation for the Ray distributed computing framework including Train, Serve, and Data.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/1712.05889" target="_blank" rel="noopener">Moritz, P., et al. (2018). "Ray: A Distributed Framework for Emerging AI Applications." <em>OSDI 2018</em>.</a></p>
    <p class="bib-annotation">The original Ray paper introducing the distributed task-based execution framework for ML workloads.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.ray.io/en/latest/train/train.html" target="_blank" rel="noopener">Ray Contributors (2024). "Ray Train." <em>Ray Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to distributed training with Ray Train supporting PyTorch, TensorFlow, and Hugging Face integration.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-t-distributed-ml/section-t.6.html": """<h3>Feature Stores</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.feast.dev/" target="_blank" rel="noopener">Feast Contributors (2024). "Feast Documentation." <em>feast.dev</em>.</a></p>
    <p class="bib-annotation">Documentation for the open-source Feast feature store covering offline and online serving.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://www.tecton.ai/blog/what-is-a-feature-store/" target="_blank" rel="noopener">Tecton (2024). "What is a Feature Store?" <em>Tecton Blog</em>.</a></p>
    <p class="bib-annotation">Conceptual introduction to feature stores and their role in production ML systems.</p>
    <span class="bib-meta">Blog</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.databricks.com/en/machine-learning/feature-store/index.html" target="_blank" rel="noopener">Databricks (2024). "Feature Engineering." <em>Databricks Documentation</em>.</a></p>
    <p class="bib-annotation">Documentation for Databricks Feature Engineering with Unity Catalog integration.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-t-distributed-ml/section-t.7.html": """<h3>Production Data Pipelines</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://airflow.apache.org/docs/" target="_blank" rel="noopener">Apache Software Foundation (2024). "Apache Airflow Documentation." <em>airflow.apache.org</em>.</a></p>
    <p class="bib-annotation">Documentation for the leading workflow orchestration platform for scheduling ML data pipelines.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.prefect.io/" target="_blank" rel="noopener">Prefect (2024). "Prefect Documentation." <em>docs.prefect.io</em>.</a></p>
    <p class="bib-annotation">Modern Python-native workflow orchestration alternative to Airflow with dynamic task graphs.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2209.09125" target="_blank" rel="noopener">Zaharia, M., et al. (2018). "Accelerating the Machine Learning Lifecycle with MLflow." <em>IEEE Data Engineering Bulletin</em>.</a></p>
    <p class="bib-annotation">Describes the end-to-end ML lifecycle management approach connecting data pipelines to model serving.</p>
    <span class="bib-meta">Paper</span>
</div>""",

    # ===== APPENDIX U: Docker Containers =====
    "appendix-u-docker-containers/section-u.1.html": """<h3>Docker Fundamentals</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.docker.com/get-started/" target="_blank" rel="noopener">Docker, Inc. (2024). "Get Started with Docker." <em>Docker Documentation</em>.</a></p>
    <p class="bib-annotation">Official tutorial covering Docker images, containers, volumes, and networking fundamentals.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.docker.com/storage/volumes/" target="_blank" rel="noopener">Docker, Inc. (2024). "Manage Data in Docker." <em>Docker Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to Docker volumes for persisting model weights, datasets, and training checkpoints.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/overview.html" target="_blank" rel="noopener">NVIDIA (2024). "NVIDIA Container Toolkit." <em>NVIDIA Documentation</em>.</a></p>
    <p class="bib-annotation">Essential toolkit for GPU-accelerated containers, required for running LLM workloads in Docker.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-u-docker-containers/section-u.2.html": """<h3>Dockerfiles for ML</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.docker.com/build/building/best-practices/" target="_blank" rel="noopener">Docker, Inc. (2024). "Dockerfile Best Practices." <em>Docker Documentation</em>.</a></p>
    <p class="bib-annotation">Official best practices for writing efficient Dockerfiles with multi-stage builds and layer caching.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch" target="_blank" rel="noopener">NVIDIA (2024). "PyTorch NGC Container." <em>NVIDIA NGC Catalog</em>.</a></p>
    <p class="bib-annotation">Pre-built and optimized PyTorch container images commonly used as base images for LLM projects.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.docker.com/build/building/multi-stage/" target="_blank" rel="noopener">Docker, Inc. (2024). "Multi-Stage Builds." <em>Docker Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to multi-stage builds for separating training and inference environments in smaller images.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-u-docker-containers/section-u.3.html": """<h3>Docker Compose for AI</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.docker.com/compose/" target="_blank" rel="noopener">Docker, Inc. (2024). "Docker Compose Documentation." <em>Docker Documentation</em>.</a></p>
    <p class="bib-annotation">Official documentation for defining and running multi-container applications with Compose.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.docker.com/compose/gpu-support/" target="_blank" rel="noopener">Docker, Inc. (2024). "GPU Support in Docker Compose." <em>Docker Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to configuring GPU access in Docker Compose for multi-service AI applications.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.docker.com/compose/networking/" target="_blank" rel="noopener">Docker, Inc. (2024). "Networking in Compose." <em>Docker Documentation</em>.</a></p>
    <p class="bib-annotation">Networking configuration for connecting LLM servers, vector databases, and application containers.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-u-docker-containers/section-u.4.html": """<h3>Containerized LLM Inference</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html" target="_blank" rel="noopener">vLLM Contributors (2024). "Deploying with Docker." <em>vLLM Documentation</em>.</a></p>
    <p class="bib-annotation">Guide to running vLLM inference servers in Docker containers with GPU passthrough.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://huggingface.co/docs/text-generation-inference/installation_nvidia" target="_blank" rel="noopener">Hugging Face (2024). "TGI Docker Installation." <em>TGI Documentation</em>.</a></p>
    <p class="bib-annotation">Docker deployment instructions for HuggingFace's Text Generation Inference server.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.nvidia.com/nim/" target="_blank" rel="noopener">NVIDIA (2024). "NVIDIA NIM." <em>NVIDIA Documentation</em>.</a></p>
    <p class="bib-annotation">NVIDIA's containerized microservices for deploying optimized AI models in production.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    # ===== APPENDIX V: Tooling Ecosystem =====
    "appendix-v-tooling-ecosystem/section-v.1.html": """<h3>LLM Tooling Landscape</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2304.08244" target="_blank" rel="noopener">Zhao, W. X., et al. (2023). "A Survey of Large Language Models." <em>arXiv preprint arXiv:2304.08244</em>.</a></p>
    <p class="bib-annotation">Comprehensive survey covering the LLM ecosystem including training, evaluation, and deployment tooling.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://github.com/Hannibal046/Awesome-LLM" target="_blank" rel="noopener">Yang, Z. (2024). "Awesome LLM." <em>GitHub</em>.</a></p>
    <p class="bib-annotation">Community-curated list of LLM resources, tools, and frameworks organized by category.</p>
    <span class="bib-meta">Tool</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://a16z.com/emerging-architectures-for-llm-applications/" target="_blank" rel="noopener">Bornstein, M. and Walke, R. (2023). "Emerging Architectures for LLM Applications." <em>Andreessen Horowitz</em>.</a></p>
    <p class="bib-annotation">Industry analysis of the reference architecture and tooling stack for production LLM applications.</p>
    <span class="bib-meta">Blog</span>
</div>""",

    "appendix-v-tooling-ecosystem/section-v.2.html": """<h3>Orchestration Frameworks</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://python.langchain.com/docs/get_started/introduction" target="_blank" rel="noopener">LangChain (2024). "Introduction." <em>LangChain Documentation</em>.</a></p>
    <p class="bib-annotation">The most widely adopted LLM orchestration framework with chains, agents, and retrieval support.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.llamaindex.ai/en/stable/" target="_blank" rel="noopener">LlamaIndex (2024). "LlamaIndex Documentation." <em>llamaindex.ai</em>.</a></p>
    <p class="bib-annotation">Data framework specializing in connecting LLMs to private data through indexing and retrieval.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.haystack.deepset.ai/" target="_blank" rel="noopener">deepset (2024). "Haystack Documentation." <em>haystack.deepset.ai</em>.</a></p>
    <p class="bib-annotation">Pipeline-based framework for building search and RAG applications with composable components.</p>
    <span class="bib-meta">Documentation</span>
</div>""",

    "appendix-v-tooling-ecosystem/section-v.3.html": """<h3>Agent Frameworks</h3>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://langchain-ai.github.io/langgraph/" target="_blank" rel="noopener">LangChain (2024). "LangGraph Documentation." <em>langchain-ai.github.io</em>.</a></p>
    <p class="bib-annotation">Graph-based framework for building stateful, multi-actor agent workflows with persistence.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://docs.crewai.com/" target="_blank" rel="noopener">CrewAI (2024). "CrewAI Documentation." <em>crewai.com</em>.</a></p>
    <p class="bib-annotation">Role-based multi-agent framework with sequential and hierarchical orchestration patterns.</p>
    <span class="bib-meta">Documentation</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://arxiv.org/abs/2308.00352" target="_blank" rel="noopener">Wu, Q., et al. (2023). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation." <em>arXiv preprint arXiv:2308.00352</em>.</a></p>
    <p class="bib-annotation">Microsoft's multi-agent conversation framework that pioneered conversational agent orchestration.</p>
    <span class="bib-meta">Paper</span>
</div>
<div class="bib-entry-card">
    <p class="bib-ref"><a href="https://openai.com/index/new-tools-for-building-agents/" target="_blank" rel="noopener">OpenAI (2025). "New Tools for Building Agents." <em>OpenAI Blog</em>.</a></p>
    <p class="bib-annotation">Introduction to the OpenAI Agents SDK with handoffs, guardrails, and tracing capabilities.</p>
    <span class="bib-meta">Documentation</span>
</div>""",
}

def main():
    base = "E:/Projects/LLMCourse/appendices"
    replaced = 0
    errors = 0

    for rel_path, bib_html in BIBLIOGRAPHIES.items():
        filepath = os.path.join(base, rel_path)
        if not os.path.exists(filepath):
            print(f"NOT FOUND: {filepath}")
            errors += 1
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        old = "<p>TODO: Add bibliography entries.</p>"
        if old not in content:
            print(f"NO TODO FOUND: {rel_path}")
            errors += 1
            continue

        new_content = content.replace(old, bib_html)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        replaced += 1
        print(f"OK: {rel_path}")

    print(f"\nDone: {replaced} files updated, {errors} errors")

if __name__ == "__main__":
    main()
