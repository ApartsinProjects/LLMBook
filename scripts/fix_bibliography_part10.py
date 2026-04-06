"""
Fix all bibliography sections in Part 10 (Frontiers):
1. Add bib-annotation elements to every bib-entry-card
2. Regroup references into meaningful subject categories
3. Add hyperlinks to references where possible
"""

import re
import os

# Each file maps to its replacement bibliography HTML
# Format: file_path -> new bibliography section (from <section class="bibliography"> to </section>)

PART10_DIR = r"E:\Projects\LLMCourse\part-10-frontiers"

bibliographies = {}

# ============================================================
# Section 34.1: Emergent Abilities: Real or Mirage?
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.1.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Foundational Papers on Emergence</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2206.07682" target="_blank" rel="noopener">Wei, J., Tay, Y., Bommasani, R., et al. (2022). "Emergent Abilities of Large Language Models." <em>Transactions on Machine Learning Research</em>.</a></p>
 <p class="bib-annotation">The paper that catalyzed the emergence debate, documenting abilities that appear abruptly as models scale. Essential context for understanding the claims and counter-claims explored throughout this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2304.15004" target="_blank" rel="noopener">Schaeffer, R., Miranda, B., &amp; Koyejo, S. (2024). "Are Emergent Abilities of Large Language Models a Mirage?" <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Argues that emergent abilities are artifacts of metric choice rather than fundamental phase transitions. This influential rebuttal reshaped how the field interprets scaling curves.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2307.15936" target="_blank" rel="noopener">Arora, S. &amp; Goyal, A. (2023). "A Theory for Emergence of Complex Skills in Language Models." <em>arXiv:2307.15936</em>.</a></p>
 <p class="bib-annotation">Proposes a formal theoretical framework explaining how complex skills emerge from the combination of simpler sub-skills during scaling. Provides mathematical grounding for the intuitions discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Empirical Studies &amp; Benchmarks</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2206.04615" target="_blank" rel="noopener">Srivastava, A., et al. (2023). "Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models." <em>Transactions on Machine Learning Research</em>.</a></p>
 <p class="bib-annotation">Introduces the BIG-Bench benchmark suite covering 204 tasks, providing the empirical foundation on which many emergence claims rest. Useful for understanding how emergence is measured in practice.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.01208" target="_blank" rel="noopener">Lu, S., Bigoulaeva, I., Sachdeva, R., Madabushi, H. T., &amp; Gurevych, I. (2024). "Are Emergent Abilities in Large Language Models Just In-Context Learning?" <em>ACL 2024</em>.</a></p>
 <p class="bib-annotation">Investigates whether apparent emergence can be explained by improvements in in-context learning rather than truly novel capabilities. Offers a more nuanced view of what "emergence" means operationally.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2405.10938" target="_blank" rel="noopener">Ruan, Y., Maddison, C. J., &amp; Tong, S. (2024). "Observational Scaling Laws and the Predictability of Language Model Performance." <em>arXiv:2405.10938</em>.</a></p>
 <p class="bib-annotation">Demonstrates that model performance can be predicted across scales using observational data alone, without expensive training runs. Directly relevant to the practical question of forecasting model capabilities.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Real-World Impact</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573321" target="_blank" rel="noopener">Dell'Acqua, F., McFowland, E., Mollick, E., et al. (2023). "Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of AI on Knowledge Worker Productivity and Quality." <em>Harvard Business School Working Paper</em>.</a></p>
 <p class="bib-annotation">A rigorous field experiment with BCG consultants showing that AI capabilities have a "jagged" boundary: strong on some tasks and surprisingly weak on others. Grounds the abstract emergence discussion in observable workplace outcomes.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 34.2: Scaling Frontiers: What Comes Next
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.2.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Scaling Laws &amp; Compute Optimization</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2203.15556" target="_blank" rel="noopener">Hoffmann, J., Borgeaud, S., Mensch, A., et al. (2022). "Training Compute-Optimal Large Language Models." <em>NeurIPS 2022</em>.</a></p>
 <p class="bib-annotation">The Chinchilla paper that redefined compute-optimal training by showing that data and parameters should scale equally. This directly motivates the data wall problem discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.16264" target="_blank" rel="noopener">Muennighoff, N., Rush, A., Barak, B., et al. (2023). "Scaling Data-Constrained Language Models." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Systematically studies what happens when training data is limited, showing that data repetition and augmentation can partially compensate. Essential reading for understanding strategies to push past the data wall.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">The Data Wall</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://epochai.org/blog/will-we-run-out-of-data" target="_blank" rel="noopener">Villalobos, P., Ho, A., Cerina, F., &amp; Sevilla, J. (2024). "Will We Run Out of Data? Limits of LLM Scaling Based on Human-Generated Data." <em>Epoch AI</em>.</a></p>
 <p class="bib-annotation">Quantifies the timeline for exhausting publicly available training data, projecting when the data wall becomes binding. The central empirical reference for the data scarcity arguments in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41586-024-07566-y" target="_blank" rel="noopener">Shumailov, I., Shumilo, Z., Zhao, Y., et al. (2024). "AI Models Collapse When Trained on Recursively Generated Data." <em>Nature</em>, 631, 755-759.</a></p>
 <p class="bib-annotation">Demonstrates that training on synthetic data from previous model generations leads to model collapse, where output diversity degrades irreversibly. A key cautionary result for synthetic data strategies.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2306.11644" target="_blank" rel="noopener">Penedo, G., Malartic, Q., Hesslow, D., et al. (2024). "The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale." <em>Hugging Face Technical Report</em>.</a></p>
 <p class="bib-annotation">Documents the curation of a high-quality 15-trillion-token web dataset, illustrating the data quality engineering that extends the useful life of web-sourced training data.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Architecture Innovations</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2302.13971" target="_blank" rel="noopener">Touvron, H., Lavril, T., Izacard, G., et al. (2023). "LLaMA: Open and Efficient Foundation Language Models." <em>arXiv:2302.13971</em>.</a></p>
 <p class="bib-annotation">Showed that smaller, well-trained models can match much larger ones, catalyzing the open-source LLM ecosystem. Exemplifies the "train longer on more data" approach to scaling efficiency.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2312.00752" target="_blank" rel="noopener">Gu, A. &amp; Dao, T. (2023). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces." <em>arXiv:2312.00752</em>.</a></p>
 <p class="bib-annotation">Introduces a selective state space model that achieves transformer-level quality with linear-time inference. Represents the leading alternative architecture for addressing the quadratic cost of attention.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2401.04088" target="_blank" rel="noopener">Jiang, A. Q., Sablayrolles, A., Roux, A., et al. (2024). "Mixtral of Experts." <em>arXiv:2401.04088</em>.</a></p>
 <p class="bib-annotation">Demonstrates that mixture-of-experts architectures can deliver frontier performance at a fraction of the inference cost. Directly relevant to the section's discussion of compute economics.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Emerging Paradigms</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2406.07524" target="_blank" rel="noopener">Sahoo, S., Arriola, M., Schiff, Y., et al. (2024). "Simple and Effective Masked Diffusion Language Models." <em>NeurIPS 2024</em>.</a></p>
 <p class="bib-annotation">Presents a diffusion-based approach to language modeling that generates text in parallel rather than autoregressively. Illustrates the new generation paradigms discussed as alternatives to traditional scaling.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2304.12244" target="_blank" rel="noopener">Xu, C., Sun, Q., Zheng, K., et al. (2023). "WizardLM: Empowering Large Language Models to Follow Complex Instructions." <em>arXiv:2304.12244</em>.</a></p>
 <p class="bib-annotation">Shows how synthetic instruction data generated through "Evol-Instruct" can improve model capability without more pretraining data. Exemplifies the synthetic data strategies discussed as a response to the data wall.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 34.3: Alternative Architectures Beyond Transformers
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.3.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">State Space Models</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2111.00396" target="_blank" rel="noopener">Gu, A., Goel, K., and Re, C. (2022). "Efficiently Modeling Long Sequences with Structured State Spaces." <em>ICLR 2022</em>.</a></p>
 <p class="bib-annotation">The foundational S4 paper that introduced structured state spaces for sequence modeling. This work laid the mathematical groundwork for all subsequent SSM architectures discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2312.00752" target="_blank" rel="noopener">Gu, A. and Dao, T. (2023). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces." <em>arXiv:2312.00752</em>.</a></p>
 <p class="bib-annotation">Introduces input-dependent selection into state space models, achieving transformer-quality language modeling with linear scaling. The most widely adopted pure SSM architecture at the time of writing.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2405.21060" target="_blank" rel="noopener">Dao, T. and Gu, A. (2024). "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality." <em>ICML 2024</em>.</a></p>
 <p class="bib-annotation">Reveals a deep mathematical duality between transformers and state space models, unifying the two paradigms under a single framework. This Mamba-2 paper simplifies understanding of when each approach excels.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Linear Attention &amp; RNN Revivals</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.13048" target="_blank" rel="noopener">Peng, B. et al. (2023). "RWKV: Reinventing RNNs for the Transformer Era." <em>EMNLP 2023 Findings</em>.</a></p>
 <p class="bib-annotation">Demonstrates that a carefully designed RNN can match transformer quality at multi-billion parameter scale while maintaining constant memory during inference. A key data point for the viability of non-attention architectures.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2307.08621" target="_blank" rel="noopener">Sun, Y. et al. (2023). "Retentive Network: A Successor to Transformer for Large Language Models." <em>arXiv:2307.08621</em>.</a></p>
 <p class="bib-annotation">Proposes retention mechanisms that combine the training parallelism of transformers with the constant-cost inference of RNNs. Illustrates the design space between pure attention and pure recurrence.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2006.16236" target="_blank" rel="noopener">Katharopoulos, A. et al. (2020). "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention." <em>ICML 2020</em>.</a></p>
 <p class="bib-annotation">An early and influential paper showing that attention can be linearized by kernel approximation, enabling RNN-like inference. This theoretical insight motivates much of the linear attention research covered in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Hybrid Architectures</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2402.19427" target="_blank" rel="noopener">De, S. et al. (2024). "Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models." <em>arXiv:2402.19427</em>.</a></p>
 <p class="bib-annotation">Shows that interleaving gated linear recurrence layers with local attention windows outperforms pure approaches at scale. Represents the hybrid design philosophy that is emerging as the practical consensus.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2403.19887" target="_blank" rel="noopener">Lieber, O. et al. (2024). "Jamba: A Hybrid Transformer-Mamba Language Model." <em>arXiv:2403.19887</em>.</a></p>
 <p class="bib-annotation">The first production-scale hybrid combining Mamba layers, attention layers, and mixture-of-experts in a single 52B-parameter model. Demonstrates that hybrid architectures can be deployed at frontier scale.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 34.4: World Models
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.4.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Foundational Work</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/1803.10122" target="_blank" rel="noopener">Ha, D. and Schmidhuber, J. (2018). "World Models." <em>arXiv:1803.10122</em>. NeurIPS 2018 oral presentation.</a></p>
 <p class="bib-annotation">The seminal paper that introduced the modern concept of learned world models for agent planning, combining a variational autoencoder with an RNN controller. This work set the conceptual foundation for all systems discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2301.04104" target="_blank" rel="noopener">Hafner, D. et al. (2023). "Mastering Diverse Domains through World Models." <em>arXiv:2301.04104</em>. (DreamerV3)</a></p>
 <p class="bib-annotation">Demonstrates a single world model agent that masters diverse tasks from video pixels alone, including Minecraft diamond collection. Shows the maturation of world model approaches for general-purpose reinforcement learning.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Video Generation as World Simulation</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://openai.com/index/video-generation-models-as-world-simulators/" target="_blank" rel="noopener">OpenAI Sora Team (2024). "Video Generation Models as World Simulators." <em>OpenAI Technical Report</em>.</a></p>
 <p class="bib-annotation">Articulates the vision that video generation models can serve as general-purpose simulators of the physical world. This report reframed video generation as a path toward world understanding rather than a purely creative tool.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.06114" target="_blank" rel="noopener">Yang, Z. et al. (2023). "UniSim: Learning Interactive Real-World Simulators." <em>arXiv:2310.06114</em>.</a></p>
 <p class="bib-annotation">Presents a unified simulator that can generate realistic interactive experiences from diverse inputs including text, images, and actions. Bridges the gap between passive video generation and interactive world modeling.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Interactive Environments &amp; Gaming</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2312.09993" target="_blank" rel="noopener">Bruce, J. et al. (2024). "Genie: Generative Interactive Environments." <em>ICML 2024</em>.</a></p>
 <p class="bib-annotation">Learns to generate entire playable 2D environments from a single image, without requiring action labels during training. Demonstrates that world models can emerge from observation alone.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/" target="_blank" rel="noopener">Google DeepMind (2024). "Genie 2: A Large-Scale Foundation World Model." <em>DeepMind Technical Report</em>.</a></p>
 <p class="bib-annotation">Scales the Genie approach to 3D environments, generating consistent, explorable worlds from single images. Represents the current frontier of interactive world generation.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2408.14837" target="_blank" rel="noopener">Valevski, D. et al. (2024). "Diffusion Models Are Real-Time Game Engines." <em>arXiv:2408.14837</em>. (GameNGen)</a></p>
 <p class="bib-annotation">Demonstrates a neural network running the game DOOM at interactive frame rates purely through diffusion, with no game engine. A striking proof that learned world models can replace hand-coded simulation.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2211.14560" target="_blank" rel="noopener">Micheli, V. et al. (2023). "Transformers are Sample-Efficient World Models." <em>ICLR 2023</em>. (IRIS)</a></p>
 <p class="bib-annotation">Shows that transformer-based world models can achieve strong Atari performance from limited experience. Connects the transformer architecture to the world model paradigm.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Autonomous Driving &amp; Robotics</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2309.17080" target="_blank" rel="noopener">Hu, A. et al. (2023). "GAIA-1: A Generative World Model for Autonomous Driving." <em>arXiv:2309.17080</em>.</a></p>
 <p class="bib-annotation">Applies the world model paradigm to autonomous driving, generating realistic driving scenarios for training and testing. Shows how world models address the data scarcity problem in safety-critical domains.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2309.09777" target="_blank" rel="noopener">Wang, Y. et al. (2023). "DriveDreamer: Towards Real-World-Driven World Models for Autonomous Driving." <em>arXiv:2309.09777</em>.</a></p>
 <p class="bib-annotation">Generates driving videos conditioned on structured traffic constraints, enabling more controllable scenario generation than unconditioned approaches.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://research.nvidia.com/labs/dir/cosmos/" target="_blank" rel="noopener">NVIDIA (2025). "Cosmos: A Platform for World Foundation Models for Physical AI." <em>NVIDIA Technical Report</em>.</a></p>
 <p class="bib-annotation">An open platform providing pre-trained world foundation models and tokenizers for physical AI development. The most comprehensive industry toolkit for building domain-specific world models.</p>
 <span class="bib-meta">&#128736; Tool</span>
 </div>

 </section>"""

# ============================================================
# Section 34.5: A Theory of Reasoning in LLMs
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.5.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Theoretical Foundations of Reasoning</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.18654" target="_blank" rel="noopener">Feng, G., Zhang, B., Gu, Y., et al. (2023). "Towards Revealing the Mystery behind Chain of Thought: A Theoretical Perspective." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Provides formal proofs that chain-of-thought extends the computational class of problems transformers can solve. The key theoretical reference for understanding why intermediate steps help reasoning.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.07923" target="_blank" rel="noopener">Merrill, W. and Sabharwal, A. (2024). "The Expressive Power of Transformers with Chain of Thought." <em>ICLR 2024</em>.</a></p>
 <p class="bib-annotation">Proves that constant-depth transformers with polynomial chain-of-thought steps can solve any problem in the complexity class P. Establishes the theoretical ceiling for chain-of-thought augmented transformers.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref">Kahneman, D. (2011). <em>Thinking, Fast and Slow</em>. Farrar, Straus and Giroux.</p>
 <p class="bib-annotation">The classic work on dual-process theory that inspired the System 1/System 2 framing widely used in reasoning research. Provides the cognitive science background for understanding why chain-of-thought helps.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 <div class="bib-category">Process Reward &amp; Verification</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.20050" target="_blank" rel="noopener">Lightman, H., Kosaraju, V., Burda, Y., et al. (2023). "Let's Verify Step by Step." <em>arXiv:2305.20050</em>.</a></p>
 <p class="bib-annotation">Demonstrates that process-based reward models (verifying each reasoning step) significantly outperform outcome-based models. Essential reading for understanding how reward signals shape reasoning quality.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.10601" target="_blank" rel="noopener">Yao, S., Yu, D., Zhao, J., et al. (2023). "Tree of Thoughts: Deliberate Problem Solving with Large Language Models." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Extends chain-of-thought to a tree-structured search over reasoning paths, enabling backtracking and deliberate exploration. Bridges the gap between language model reasoning and classical search algorithms.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Limitations &amp; Failure Modes</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2210.03350" target="_blank" rel="noopener">Press, O., Zhang, M., Min, S., et al. (2023). "Measuring and Narrowing the Compositionality Gap in Language Models." <em>Findings of EMNLP 2023</em>.</a></p>
 <p class="bib-annotation">Quantifies the "compositionality gap" where models know individual facts but fail to compose them into multi-step answers. Motivates the decomposition strategies discussed for improving reasoning reliability.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.18654" target="_blank" rel="noopener">Dziri, N., Lu, X., Sclar, M., et al. (2024). "Faith and Fate: Limits of Transformers on Compositionality." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Shows that transformers rely on linearized shortcuts for compositional tasks and fail when problem complexity exceeds these shortcuts. Provides rigorous evidence for the compositional limitations discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.04388" target="_blank" rel="noopener">Turpin, M., Michael, J., Perez, E., and Bowman, S. R. (2024). "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Reveals that chain-of-thought explanations can be systematically unfaithful to the model's actual reasoning process. Raises critical questions about the reliability of reasoning traces for interpretability.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2302.00093" target="_blank" rel="noopener">Shi, F., Chen, X., Misra, K., et al. (2023). "Large Language Models Can Be Easily Distracted by Irrelevant Context." <em>ICML 2023</em>.</a></p>
 <p class="bib-annotation">Shows that adding irrelevant information to prompts significantly degrades reasoning accuracy, even when the core problem is simple. Highlights a practical brittleness in current reasoning capabilities.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2309.12288" target="_blank" rel="noopener">Berglund, L., Tong, M., Kaufmann, M., et al. (2024). "The Reversal Curse: LLMs Trained on 'A is B' Fail to Learn 'B is A'." <em>ICLR 2024</em>.</a></p>
 <p class="bib-annotation">Demonstrates a surprising asymmetry in learned knowledge, where models cannot reverse the direction of learned associations. Reveals a fundamental limitation in how transformers represent relational knowledge.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 34.6: Memory as a Computational Primitive
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.6.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Memory-Augmented Architectures</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.08560" target="_blank" rel="noopener">Packer, C., Wooders, S., Lin, K., et al. (2023). "MemGPT: Towards LLMs as Operating Systems." <em>arXiv:2310.08560</em>.</a></p>
 <p class="bib-annotation">Introduces an operating-system inspired approach to LLM memory management, using virtual context and paging to handle conversations far exceeding the context window. The primary reference for the OS analogy developed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2203.08913" target="_blank" rel="noopener">Wu, Y., Rabe, M. N., Hutchins, D., and Szegedy, C. (2022). "Memorizing Transformers." <em>ICLR 2022</em>.</a></p>
 <p class="bib-annotation">Augments transformers with a kNN-based external memory that the model can attend to during inference. Demonstrates that explicit retrieval from stored representations improves factual accuracy on long documents.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2304.11062" target="_blank" rel="noopener">Bulatov, A., Kuratov, Y., and Burtsev, M. (2023). "Scaling Transformer to 1M Tokens and Beyond with RMT." <em>arXiv:2304.11062</em>.</a></p>
 <p class="bib-annotation">Proposes Recurrent Memory Transformer, which uses special memory tokens that persist across segments. Shows how to extend effective context length to millions of tokens with bounded compute.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2404.07143" target="_blank" rel="noopener">Munkhdalai, T., Faruqui, M., and Gopal, S. (2024). "Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention." <em>arXiv:2404.07143</em>.</a></p>
 <p class="bib-annotation">Introduces a compressive memory mechanism that integrates into standard attention, enabling bounded-memory processing of unbounded sequences. Represents a particularly elegant approach to the infinite context problem.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Foundational Theory</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/1410.5401" target="_blank" rel="noopener">Graves, A., Wayne, G., and Danihelka, I. (2014). "Neural Turing Machines." <em>arXiv:1410.5401</em>.</a></p>
 <p class="bib-annotation">The pioneering work on differentiable external memory for neural networks, establishing the paradigm of learned read/write operations. This paper provides the historical foundation for all memory-augmented architectures discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://aclanthology.org/2023.emnlp-tutorial.5/" target="_blank" rel="noopener">Merrill, W. (2023). "Formal Languages and the NLP Black Box." <em>EMNLP Tutorial</em>.</a></p>
 <p class="bib-annotation">A comprehensive tutorial on the formal language theory perspective on neural networks, connecting computational complexity to architectural choices. Provides the theoretical tools for analyzing whether memory extensions push models toward Turing completeness.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref">Ebbinghaus, H. (1885). <em>Memory: A Contribution to Experimental Psychology</em>. (Translated by Ruger and Bussenius, 1913.)</p>
 <p class="bib-annotation">The classic study establishing the forgetting curve and spacing effect in human memory. Provides the cognitive science analogy that motivates the distinction between working memory and long-term memory in AI systems.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 </section>"""

# ============================================================
# Section 34.7: Mechanistic Interpretability at Scale
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.7.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Superposition &amp; Feature Discovery</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://transformer-circuits.pub/2022/toy_model/index.html" target="_blank" rel="noopener">Elhage, N., Hume, T., Olsson, C., et al. (2022). "Toy Models of Superposition." <em>Transformer Circuits Thread, Anthropic</em>.</a></p>
 <p class="bib-annotation">Provides the theoretical framework for understanding superposition, where neural networks represent more features than they have dimensions. This foundational work explains why individual neurons are often uninterpretable.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://transformer-circuits.pub/2023/monosemantic-features/index.html" target="_blank" rel="noopener">Bricken, T., Templeton, A., Batson, J., et al. (2023). "Towards Monosemanticity: Decomposing Language Models with Dictionary Learning." <em>Transformer Circuits Thread, Anthropic</em>.</a></p>
 <p class="bib-annotation">Demonstrates that sparse autoencoders can decompose neural network activations into interpretable, monosemantic features. The paper that launched the current wave of dictionary learning approaches to interpretability.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html" target="_blank" rel="noopener">Templeton, A., Conerly, T., Marcus, J., et al. (2024). "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet." <em>Transformer Circuits Thread, Anthropic</em>.</a></p>
 <p class="bib-annotation">Scales sparse autoencoders to a production frontier model, finding millions of interpretable features including abstract concepts and multilingual representations. Demonstrates that mechanistic interpretability works at realistic scale.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2309.08600" target="_blank" rel="noopener">Cunningham, H., Ewart, A., Riggs, L., Huben, R., and Sharkey, L. (2023). "Sparse Autoencoders Find Highly Interpretable Features in Language Models." <em>ICLR 2024</em>.</a></p>
 <p class="bib-annotation">Independently validates the sparse autoencoder approach and provides systematic evaluation of feature quality. Offers complementary evidence to the Anthropic line of work on dictionary learning.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Circuit Analysis</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2211.00593" target="_blank" rel="noopener">Wang, K., Variengien, A., Conmy, A., Shlegeris, B., and Steinhardt, J. (2023). "Interpretability in the Wild: A Circuit for Indirect Object Identification in GPT-2 Small." <em>ICLR 2023</em>.</a></p>
 <p class="bib-annotation">The most detailed circuit-level analysis of a real language model behavior, tracing how GPT-2 resolves indirect object references. Sets the gold standard for what a complete mechanistic explanation looks like.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2304.14997" target="_blank" rel="noopener">Conmy, A., Mavor-Parker, A., Lynch, A., Heimersheim, S., and Garriga-Alonso, A. (2023). "Towards Automated Circuit Discovery for Mechanistic Interpretability." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Introduces ACDC, an algorithm for automatically identifying computational circuits in neural networks. Essential reading for understanding how circuit analysis can scale beyond manual investigation.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Automated Interpretability</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html" target="_blank" rel="noopener">Bills, S., Cammarata, N., Mossing, D., et al. (2023). "Language Models Can Explain Neurons in Language Models." <em>OpenAI Blog</em>.</a></p>
 <p class="bib-annotation">Pioneers the use of LLMs to automatically generate and score natural language explanations of individual neurons. Demonstrates the potential (and current limitations) of using AI to interpret AI.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 34.8: The Nature of Agency
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.8.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Foundational Frameworks</div>

 <div class="bib-entry-card">
 <p class="bib-ref">Russell, S. and Norvig, P. (2021). <em>Artificial Intelligence: A Modern Approach</em>, 4th edition. Pearson. (Chapter 2: Intelligent Agents.)</p>
 <p class="bib-annotation">The standard textbook treatment of agent architectures, defining the perceive-reason-act loop and the taxonomy of agent types. Provides the formal definitions of agency that this section builds upon.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://selfawarepatterns.com/2008/01/22/the-basic-ai-drives/" target="_blank" rel="noopener">Omohundro, S. (2008). "The Basic AI Drives." <em>Proceedings of the First AGI Conference</em>.</a></p>
 <p class="bib-annotation">Argues that sufficiently advanced AI systems will develop convergent instrumental goals such as self-preservation and resource acquisition. A foundational reference for the safety implications of agency discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://intelligence.org/files/PhilosophicalProblems.pdf" target="_blank" rel="noopener">McCarthy, J. and Hayes, P. J. (1969). "Some Philosophical Problems from the Standpoint of Artificial Intelligence." <em>Machine Intelligence 4</em>.</a></p>
 <p class="bib-annotation">The classic paper that formalized the frame problem and the challenge of representing common-sense knowledge for agents. Provides historical context for understanding why agency remains difficult despite decades of research.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Safety &amp; Risk Analysis</div>

 <div class="bib-entry-card">
 <p class="bib-ref">Bostrom, N. (2014). <em>Superintelligence: Paths, Dangers, Strategies</em>. Oxford University Press.</p>
 <p class="bib-annotation">The influential book that systematized arguments about risks from advanced AI agents, including instrumental convergence and the control problem. Essential background for the safety discussion in this section.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/1906.01820" target="_blank" rel="noopener">Hubinger, E., van Merwijk, C., Mikulik, V., Skalse, J., and Garrabrant, S. (2019). "Risks from Learned Optimization in Advanced Machine Learning Systems." <em>arXiv:1906.01820</em>.</a></p>
 <p class="bib-annotation">Introduces the concept of mesa-optimization, where learned models develop their own internal objectives that may differ from the training objective. Directly relevant to understanding how agency can emerge unintentionally.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2401.13138" target="_blank" rel="noopener">Chan, A., Salganik, R., Markel, A., et al. (2024). "Harms from Increasingly Agentic Algorithmic Systems." <em>FAccT 2024</em>.</a></p>
 <p class="bib-annotation">Provides a systematic taxonomy of harms that increase as AI systems become more autonomous, spanning economic, social, and political dimensions. Grounds the theoretical safety concerns in concrete, observable risks.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Agentic Systems in Practice</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.11453" target="_blank" rel="noopener">Shinn, N., Cassano, F., Gopinath, A., et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Demonstrates agents that improve through verbal self-reflection rather than weight updates, achieving strong performance on coding and reasoning tasks. Illustrates the practical spectrum of agency discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.16291" target="_blank" rel="noopener">Wang, G., Xie, Y., Jiang, Y., et al. (2023). "Voyager: An Open-Ended Embodied Agent with Large Language Models." <em>arXiv:2305.16291</em>.</a></p>
 <p class="bib-annotation">An LLM-powered agent that autonomously explores, acquires skills, and builds a reusable skill library in Minecraft. Exemplifies the highest degree of open-ended autonomy in current language model agents.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 34.9: Efficient Multi-Tool Orchestration and Tool Economy
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.9.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Foundational Tool Use</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2302.04761" target="_blank" rel="noopener">Schick, T., Dwivedi-Yu, J., Dess\u00ec, R., et al. (2023). "Toolformer: Language Models Can Teach Themselves to Use Tools." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">The seminal paper showing that language models can learn when and how to call external tools through self-supervised training. Established the paradigm of tool-augmented language models discussed throughout this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.15334" target="_blank" rel="noopener">Patil, S. G., Zhang, T., Wang, X., and Gonzalez, J. E. (2023). "Gorilla: Large Language Model Connected with Massive APIs." <em>arXiv:2305.15334</em>.</a></p>
 <p class="bib-annotation">Fine-tunes an LLM to accurately generate API calls from documentation, dramatically reducing hallucination in tool invocations. Demonstrates that retrieval-augmented fine-tuning improves tool-use reliability.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Tool Benchmarks &amp; Scaling</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2307.16789" target="_blank" rel="noopener">Qin, Y., Liang, S., Ye, Y., et al. (2024). "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-World APIs." <em>ICLR 2024</em>.</a></p>
 <p class="bib-annotation">Constructs a dataset and framework for training models to use over 16,000 real-world APIs, introducing depth-first search for multi-step tool planning. The primary reference for scaling tool use to realistic complexity.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2306.09299" target="_blank" rel="noopener">Li, M., Song, F., Yu, B., et al. (2023). "API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs." <em>EMNLP 2023</em>.</a></p>
 <p class="bib-annotation">Provides a systematic benchmark for evaluating LLM tool use across planning, retrieval, and calling stages. Useful for understanding how tool-use capabilities are measured and compared.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2406.10573" target="_blank" rel="noopener">Wang, X., Ma, W., Meng, Y., et al. (2024). "T-Bench: Benchmarking Tool Use of Large Language Models." <em>arXiv:2406.10573</em>.</a></p>
 <p class="bib-annotation">Evaluates tool use across diverse scenarios including multi-tool chains and error recovery. Highlights the gap between single-tool and multi-tool orchestration performance.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Protocols &amp; Infrastructure</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://modelcontextprotocol.io/specification" target="_blank" rel="noopener">Anthropic (2024). "Model Context Protocol (MCP) Specification." <em>Anthropic Technical Documentation</em>.</a></p>
 <p class="bib-annotation">Defines an open standard for connecting AI models to external tools and data sources through a unified protocol. The leading candidate for standardizing tool integration discussed in this section's coverage of tool economy.</p>
 <span class="bib-meta">&#128736; Tool</span>
 </div>

 </section>"""

# ============================================================
# Section 34.10: Beyond Text: LLMs as Universal Sequence Machines
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-34-emerging-architectures", "section-34.10.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Genomics</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2306.15006" target="_blank" rel="noopener">Zhou, Z., et al. (2024). "DNABERT-2: Efficient Foundation Model and Benchmark for Multi-Species Genome." <em>ICLR 2024</em>.</a></p>
 <p class="bib-annotation">Introduces byte-pair encoding tokenization for DNA sequences, replacing fixed k-mer approaches and achieving state-of-the-art on genomic benchmarks across species. Shows how NLP tokenization innovations transfer directly to biology.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41592-023-02106-w" target="_blank" rel="noopener">Dalla-Torre, H., et al. (2024). "The Nucleotide Transformer: Building and Evaluating Robust Foundation Models for Human Genomics." <em>Nature Methods</em>.</a></p>
 <p class="bib-annotation">Trains transformer models on 3,200 diverse genomes, achieving strong zero-shot performance on downstream tasks. Demonstrates that the pretraining paradigm scales to genomic data at the multi-species level.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41586-025-08774-2" target="_blank" rel="noopener">Brixi, G., et al. (2025). "Genome modeling and design across all domains of life with Evo 2." <em>Nature</em>.</a></p>
 <p class="bib-annotation">A 7-billion-parameter model trained on 9.3 trillion nucleotide tokens spanning all domains of life. Represents the current frontier of genomic foundation models, capable of generating functional DNA sequences.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Proteins</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1126/science.ade2574" target="_blank" rel="noopener">Lin, Z., et al. (2023). "Evolutionary-scale prediction of atomic-level protein structure with a language model." <em>Science</em>.</a></p>
 <p class="bib-annotation">Shows that protein language models trained on evolutionary sequences alone can predict 3D structure, rivaling specialized structure prediction methods. Demonstrates that self-supervised pretraining captures deep biological knowledge.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1101/2024.03.14.585085" target="_blank" rel="noopener">Hayes, T., et al. (2024). "Simulating 500 million years of evolution with a language model." <em>bioRxiv</em> (ESM-3).</a></p>
 <p class="bib-annotation">Scales protein language models to jointly reason over sequence, structure, and function, generating novel fluorescent proteins not found in nature. The most ambitious protein generation result at the time of writing.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Molecules</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1021/acs.jcim.1c00600" target="_blank" rel="noopener">Bagal, V., et al. (2021). "MolGPT: Molecular Generation Using a Transformer-Decoder Model." <em>J. Chem. Inf. Model.</em></a></p>
 <p class="bib-annotation">Applies GPT-style autoregressive generation to SMILES molecular strings, producing valid and drug-like molecules. An early and influential demonstration that text generation architectures work for molecular design.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2209.01712" target="_blank" rel="noopener">Ahmad, W., et al. (2022). "ChemBERTa-2: Towards Chemical Foundation Models." <em>arXiv:2209.01712</em>.</a></p>
 <p class="bib-annotation">Applies masked language modeling to chemical SMILES representations, creating foundation models for molecular property prediction. Extends the BERT pretraining paradigm to chemistry.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Time Series</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2403.07815" target="_blank" rel="noopener">Ansari, A. F., et al. (2024). "Chronos: Learning the Language of Time Series." <em>arXiv:2403.07815</em>.</a></p>
 <p class="bib-annotation">Tokenizes real-valued time series into discrete bins and trains a language model on them, achieving strong zero-shot forecasting. A clean demonstration of the "tokenize anything" philosophy discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.08278" target="_blank" rel="noopener">Rasul, K., et al. (2024). "Lag-Llama: Towards Foundation Models for Probabilistic Time Series Forecasting." <em>arXiv:2310.08278</em>.</a></p>
 <p class="bib-annotation">Builds a foundation model for time series using a decoder-only transformer with lagged features. Shows that the LLM pretraining recipe transfers to probabilistic forecasting.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.01728" target="_blank" rel="noopener">Jin, M., et al. (2024). "Time-LLM: Time Series Forecasting by Reprogramming Large Language Models." <em>ICLR 2024</em>.</a></p>
 <p class="bib-annotation">Reprograms frozen text LLMs to process time series through learned input transformations, avoiding expensive retraining. Demonstrates that existing language model knowledge can be leveraged for entirely non-linguistic domains.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Audio and Music</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2209.03143" target="_blank" rel="noopener">Borsos, Z., et al. (2023). "AudioLM: a Language Modeling Approach to Audio Generation." <em>IEEE/ACM TASLP</em>.</a></p>
 <p class="bib-annotation">Treats audio generation as language modeling over discrete audio tokens, producing speech and music with remarkable coherence. The foundational work that established the codec language model paradigm for audio.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2306.05284" target="_blank" rel="noopener">Copet, J., et al. (2023). "Simple and Controllable Music Generation." <em>NeurIPS 2023</em> (MusicGen).</a></p>
 <p class="bib-annotation">Generates high-quality music from text descriptions using a single-stage transformer over compressed audio tokens. Demonstrates that text-conditioned generation works across creative audio domains.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2301.02111" target="_blank" rel="noopener">Wang, C., et al. (2023). "Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers." <em>arXiv:2301.02111</em> (VALL-E).</a></p>
 <p class="bib-annotation">Achieves zero-shot voice cloning from a 3-second sample by treating speech synthesis as conditional language modeling over codec tokens. A breakthrough in applying the in-context learning paradigm to speech.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">EHR and Medical</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41598-020-62922-y" target="_blank" rel="noopener">Li, Y., et al. (2020). "BEHRT: Transformer for Electronic Health Records." <em>Scientific Reports</em>.</a></p>
 <p class="bib-annotation">Applies BERT-style pretraining to sequences of medical codes from electronic health records, predicting future diagnoses. An early and influential example of treating patient histories as a "language" for transformers.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Robotics and Actions</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2307.15818" target="_blank" rel="noopener">Brohan, A., et al. (2023). "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control." <em>arXiv:2307.15818</em>.</a></p>
 <p class="bib-annotation">Directly outputs robot actions as text tokens from a vision-language model, transferring web-scale knowledge to physical manipulation. Demonstrates the strongest evidence that language model pretraining aids robotic reasoning.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2406.09246" target="_blank" rel="noopener">Kim, M., et al. (2024). "OpenVLA: An Open-Source Vision-Language-Action Model." <em>arXiv:2406.09246</em>.</a></p>
 <p class="bib-annotation">Provides an open-source 7B vision-language-action model for robotic manipulation, making frontier robotic AI accessible to the research community. The leading open alternative to proprietary robotic foundation models.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2205.06175" target="_blank" rel="noopener">Reed, S., et al. (2022). "A Generalist Agent." <em>arXiv:2205.06175</em> (Gato).</a></p>
 <p class="bib-annotation">The first model to handle text, images, and robot actions within a single transformer, playing games, chatting, and stacking blocks. A proof of concept for the "one model, many modalities" vision.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Tabular, Weather, and Mathematics</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41586-024-08328-6" target="_blank" rel="noopener">Hollmann, N., et al. (2024). "Accurate predictions on small data with a tabular foundation model." <em>Nature</em> (TabPFN-2).</a></p>
 <p class="bib-annotation">A transformer foundation model for tabular prediction that achieves strong performance with no gradient-based training on new datasets. Challenges the assumption that tabular data requires specialized algorithms like gradient boosting.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41586-025-08897-6" target="_blank" rel="noopener">Bodnar, C., et al. (2025). "Aurora: A Foundation Model of the Atmosphere." <em>Nature</em>.</a></p>
 <p class="bib-annotation">Applies transformer-based foundation models to weather prediction, matching or exceeding specialized numerical weather models. Demonstrates that the foundation model paradigm works for complex physical simulations.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41586-025-08911-x" target="_blank" rel="noopener">AlphaProof team (2025). "Formal Mathematical Reasoning: A New Frontier in AI." <em>Nature</em>.</a></p>
 <p class="bib-annotation">Combines language models with formal proof verification to solve International Mathematical Olympiad problems. Represents the frontier of AI mathematical reasoning, connecting natural language and formal logic.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

</section>"""

# ============================================================
# Section 35.1: Alignment Research Frontiers
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-35-ai-society", "section-35.1.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Scalable Oversight</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2212.08073" target="_blank" rel="noopener">Bai, Y., Kadavath, S., Kundu, S., et al. (2022). "Constitutional AI: Harmlessness from AI Feedback." <em>arXiv:2212.08073</em>.</a></p>
 <p class="bib-annotation">Introduces constitutional AI, where the model critiques and revises its own outputs guided by a set of principles rather than human labels. The primary practical implementation of scalable oversight discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/1805.00899" target="_blank" rel="noopener">Irving, G., Christiano, P., &amp; Amodei, D. (2018). "AI Safety via Debate." <em>arXiv:1805.00899</em>.</a></p>
 <p class="bib-annotation">Proposes a debate framework where two AI systems argue for opposing positions and a human judge selects the more truthful argument. Foundational work on using adversarial dynamics to align AI with truth.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2312.09390" target="_blank" rel="noopener">Burns, C., Haotian, Y., Steinhardt, J., et al. (2023). "Weak-to-Strong Generalization: Eliciting Strong Capabilities with Weak Supervision." <em>OpenAI Research</em>.</a></p>
 <p class="bib-annotation">Investigates whether weak supervisors can elicit the full capabilities of stronger models, finding partial but incomplete success. Directly addresses the core challenge of supervising superhuman AI systems.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2402.06782" target="_blank" rel="noopener">Khan, A., Hughes, J., Valentine, D., et al. (2024). "Debating with More Persuasive LLMs Leads to More Truthful Answers." <em>arXiv:2402.06782</em>.</a></p>
 <p class="bib-annotation">Provides empirical evidence that AI debate actually helps human judges reach correct answers, even when one debater is more persuasive. Validates the debate approach as a practical alignment strategy.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Reward Modeling &amp; RLHF Foundations</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/1811.07871" target="_blank" rel="noopener">Leike, J., Krueger, D., Everitt, T., et al. (2018). "Scalable Agent Alignment via Reward Modeling: A Research Direction." <em>arXiv:1811.07871</em>.</a></p>
 <p class="bib-annotation">Lays out the research agenda for aligning AI through learned reward models, identifying key challenges including reward hacking and distributional shift. The conceptual roadmap that guided much of the subsequent RLHF work.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/1706.03741" target="_blank" rel="noopener">Christiano, P., Leike, J., Brown, T., et al. (2017). "Deep Reinforcement Learning from Human Preferences." <em>NeurIPS 2017</em>.</a></p>
 <p class="bib-annotation">The original paper demonstrating that RL agents can be trained from human preference comparisons rather than hand-crafted reward functions. This work established the RLHF methodology that underpins modern alignment.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.20050" target="_blank" rel="noopener">Lightman, H., Kosaraju, V., Burda, Y., et al. (2023). "Let's Verify Step by Step." <em>arXiv:2305.20050</em>.</a></p>
 <p class="bib-annotation">Shows that process-based reward models outperform outcome-based ones for math reasoning, rewarding correct intermediate steps. Demonstrates a path toward more robust reward signals that are harder to hack.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Interpretability for Alignment</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2309.08600" target="_blank" rel="noopener">Cunningham, H., Ewart, A., Riggs, L., Huben, R., &amp; Sharkey, L. (2023). "Sparse Autoencoders Find Highly Interpretable Features in Language Models." <em>arXiv:2309.08600</em>.</a></p>
 <p class="bib-annotation">Demonstrates that sparse autoencoders can extract interpretable features from model internals, enabling inspection of what models have learned. Relevant to this section's discussion of using interpretability as a safety tool.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://transformer-circuits.pub/2023/monosemantic-features/index.html" target="_blank" rel="noopener">Bricken, T., Templeton, A., Batson, J., et al. (2023). "Towards Monosemanticity: Decomposing Language Models with Dictionary Learning." <em>Anthropic Research</em>.</a></p>
 <p class="bib-annotation">Shows that dictionary learning can decompose model representations into individual, interpretable features. This line of research provides the technical foundation for using interpretability to verify alignment properties.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 35.2: AI Governance and Open Problems
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-35-ai-society", "section-35.2.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Regulatory Frameworks</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://eur-lex.europa.eu/eli/reg/2024/1689/oj" target="_blank" rel="noopener">European Parliament. (2024). "Regulation (EU) 2024/1689: Artificial Intelligence Act." <em>Official Journal of the European Union</em>.</a></p>
 <p class="bib-annotation">The world's first comprehensive AI regulation, establishing a risk-based framework that categorizes AI systems by their potential for harm. The primary legal text for understanding the EU's regulatory approach discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/" target="_blank" rel="noopener">White House. (2023). "Executive Order 14110 on the Safe, Secure, and Trustworthy Development and Use of Artificial Intelligence."</a></p>
 <p class="bib-annotation">Established reporting requirements for frontier model training and directed federal agencies to develop AI safety standards. The key US policy document discussed in this section's comparison of governance approaches.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2307.03718" target="_blank" rel="noopener">Anderljung, M., Barnhart, J., Korber, A., et al. (2023). "Frontier AI Regulation: Managing Emerging Risks to Public Safety." <em>arXiv:2307.03718</em>.</a></p>
 <p class="bib-annotation">A comprehensive framework for regulating frontier AI systems, proposing safety evaluations and deployment oversight. Bridges the gap between technical safety research and practical policy design.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Compute Governance &amp; Verification</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://www.governance.ai/post/compute-governance-and-international-ai-safety" target="_blank" rel="noopener">Heim, L. (2024). "Compute Governance and International AI Safety." <em>Centre for the Governance of AI</em>.</a></p>
 <p class="bib-annotation">Argues that compute is the most measurable and controllable input to AI development, making it the natural lever for governance. Provides the analytical framework for the compute governance discussion in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2303.11341" target="_blank" rel="noopener">Shavit, Y. (2023). "What Does It Take to Catch a Chinchilla? Verifying Rules on Large-Scale Neural Network Training via Compute Monitoring." <em>arXiv:2303.11341</em>.</a></p>
 <p class="bib-annotation">Proposes technical mechanisms for verifying compliance with compute thresholds through hardware monitoring. Demonstrates that compute governance can be technically implemented, not just theoretically discussed.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Open Source &amp; Capability Assessment</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2311.09227" target="_blank" rel="noopener">Seger, E., Dreksler, N., Moulange, R., et al. (2023). "Open-Sourcing Highly Capable Foundation Models: An Evaluation of Risks, Benefits, and Alternative Methods for Pursuing Open-Source Objectives." <em>Centre for the Governance of AI</em>.</a></p>
 <p class="bib-annotation">Systematically analyzes the risks and benefits of open-sourcing powerful AI models, proposing structured release strategies. Essential reading for the open vs. closed debate in AI governance.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arcprize.org/" target="_blank" rel="noopener">Chollet, F. (2024). "ARC-AGI: A Formal Measure of Intelligence." <em>ARC Prize Foundation</em>.</a></p>
 <p class="bib-annotation">Proposes the Abstraction and Reasoning Corpus as a benchmark for measuring genuine intelligence rather than memorization. Relevant to the governance challenge of assessing when models reach concerning capability levels.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2004.07213" target="_blank" rel="noopener">Brundage, M., Avin, S., Wang, J., et al. (2020). "Toward Trustworthy AI Development: Mechanisms for Supporting Verifiable Claims." <em>arXiv:2004.07213</em>.</a></p>
 <p class="bib-annotation">Proposes institutional and technical mechanisms for verifying safety claims made by AI developers. Connects the abstract goal of trustworthy AI to concrete organizational and auditing practices.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 35.3: Societal Impact and the Road Ahead
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-35-ai-society", "section-35.3.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Labor Market Impact</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2303.10130" target="_blank" rel="noopener">Eloundou, T., Manning, S., Mishkin, P., &amp; Rock, D. (2023). "GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models." <em>arXiv:2303.10130</em>.</a></p>
 <p class="bib-annotation">Estimates that roughly 80% of US workers have at least 10% of their tasks exposed to LLMs, with higher-income knowledge workers most affected. The most cited analysis of AI labor exposure discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://www.nber.org/papers/w31161" target="_blank" rel="noopener">Brynjolfsson, E., Li, D., &amp; Raymond, L. (2023). "Generative AI at Work." <em>NBER Working Paper No. 31161</em>.</a></p>
 <p class="bib-annotation">Studies AI-assisted customer service agents, finding that the largest productivity gains accrue to the least experienced workers. Provides real-world evidence for the skill-leveling effects discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1126/science.adh2586" target="_blank" rel="noopener">Noy, S. &amp; Zhang, W. (2023). "Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence." <em>Science</em>, 381(6654), 187-192.</a></p>
 <p class="bib-annotation">A controlled experiment showing that ChatGPT increases writing productivity by 37% while improving output quality, with larger gains for lower-ability workers. Rigorous experimental evidence for the productivity claims in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2302.06590" target="_blank" rel="noopener">Peng, S., Kalliamvakou, E., Cihon, P., &amp; Demirer, M. (2023). "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot." <em>arXiv:2302.06590</em>.</a></p>
 <p class="bib-annotation">A randomized controlled trial showing that developers using Copilot completed tasks 55% faster. The most rigorous study of AI-assisted software development productivity.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4573321" target="_blank" rel="noopener">Dell'Acqua, F., McFowland, E., Mollick, E., et al. (2023). "Navigating the Jagged Technological Frontier." <em>Harvard Business School Working Paper</em>.</a></p>
 <p class="bib-annotation">Reveals that AI augmentation boosts performance on some consulting tasks while degrading it on others, creating a "jagged" capability frontier. Cautions against uniform AI adoption without understanding task-specific effects.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Scientific Discovery</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41586-021-03819-2" target="_blank" rel="noopener">Jumper, J., Evans, R., Pritzel, A., et al. (2021). "Highly Accurate Protein Structure Prediction with AlphaFold." <em>Nature</em>, 596(7873), 583-589.</a></p>
 <p class="bib-annotation">Solved the 50-year protein folding problem, demonstrating that AI can achieve breakthrough scientific results. The landmark example of AI-accelerated discovery referenced throughout this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41586-023-06735-9" target="_blank" rel="noopener">Merchant, A., Batzner, S., Schoenholz, S. S., et al. (2023). "Scaling Deep Learning for Materials Discovery." <em>Nature</em>, 624, 80-85.</a></p>
 <p class="bib-annotation">Uses graph neural networks to discover 2.2 million stable crystal structures, vastly expanding the known materials space. Illustrates how AI accelerates discovery across scientific domains beyond biology.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Education &amp; Economics</div>

 <div class="bib-entry-card">
 <p class="bib-ref">Bloom, B. S. (1984). "The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring." <em>Educational Researcher</em>, 13(6), 4-16.</p>
 <p class="bib-annotation">The classic study showing that one-on-one tutoring improves student performance by two standard deviations over classroom instruction. Provides the benchmark against which AI tutoring systems are evaluated in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://www.nber.org/papers/w32487" target="_blank" rel="noopener">Acemoglu, D. (2024). "The Simple Macroeconomics of AI." <em>NBER Working Paper No. 32487</em>.</a></p>
 <p class="bib-annotation">Provides a skeptical macroeconomic analysis suggesting that AI's GDP impact may be more modest than commonly projected if it primarily automates easy tasks. An important counterweight to optimistic forecasts.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 35.4: Open Research Problems & Future Directions
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-35-ai-society", "section-35.4.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Understanding LLM Capabilities</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2206.07682" target="_blank" rel="noopener">Wei, J. et al. (2022). "Emergent Abilities of Large Language Models." <em>TMLR</em>.</a></p>
 <p class="bib-annotation">Documents abilities that appear abruptly at scale, framing one of the central open problems: can we predict and control capability emergence? Provides the empirical basis for emergence as a research frontier.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.02207" target="_blank" rel="noopener">Gurnee, W. and Tegmark, M. (2023). "Language Models Represent Space and Time." <em>arXiv:2310.02207</em>.</a></p>
 <p class="bib-annotation">Discovers linear representations of spatial and temporal concepts within LLM activations, suggesting models build structured world knowledge. Connects to the open question of whether LLMs develop genuine understanding.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2111.02080" target="_blank" rel="noopener">Xie, S. M. et al. (2022). "An Explanation of In-context Learning as Implicit Bayesian Inference." <em>ICLR 2022</em>.</a></p>
 <p class="bib-annotation">Proposes a theoretical explanation for in-context learning as implicit Bayesian inference over latent concepts. Addresses one of the deepest open questions in LLM research: how does learning happen without gradient updates?</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1145/3624724" target="_blank" rel="noopener">Shanahan, M. (2024). "Talking About Large Language Models." <em>Communications of the ACM</em>, 67(2).</a></p>
 <p class="bib-annotation">A philosophical analysis of what it means to say LLMs "know," "understand," or "believe" things. Clarifies conceptual confusions that obstruct progress on open research questions about LLM cognition.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Safety &amp; Alignment Frontiers</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2212.08073" target="_blank" rel="noopener">Bai, Y. et al. (2022). "Constitutional AI: Harmlessness from AI Feedback." <em>arXiv:2212.08073</em>.</a></p>
 <p class="bib-annotation">Demonstrates alignment through AI self-critique guided by explicit principles, reducing dependence on human labelers. An active research direction for making alignment scalable and reproducible.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2312.09390" target="_blank" rel="noopener">Burns, C. et al. (2023). "Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision." <em>OpenAI Technical Report</em>.</a></p>
 <p class="bib-annotation">Investigates the fundamental challenge of supervising AI systems smarter than the supervisor. Frames one of the most important open problems for the next generation of alignment research.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1016/j.patter.2023.100835" target="_blank" rel="noopener">Park, S. et al. (2023). "AI Deception: A Survey of Examples, Risks, and Potential Solutions." <em>Patterns</em>, 4(10).</a></p>
 <p class="bib-annotation">Catalogs known examples of AI systems exhibiting deceptive behavior and proposes detection strategies. Highlights deception as an underexplored but critical safety frontier.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Measuring Intelligence</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://distill.pub/2020/circuits/zoom-in/" target="_blank" rel="noopener">Olah, C. et al. (2020). "Zoom In: An Introduction to Circuits." <em>Distill</em>.</a></p>
 <p class="bib-annotation">The influential piece that proposed viewing neural networks as compositions of interpretable circuits. Established the conceptual vocabulary and research agenda for mechanistic interpretability.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/1911.01547" target="_blank" rel="noopener">Chollet, F. (2019). "On the Measure of Intelligence." <em>arXiv:1911.01547</em>.</a></p>
 <p class="bib-annotation">Argues that intelligence should be measured by skill-acquisition efficiency rather than task performance. Provides the theoretical framework for evaluating whether AI systems are genuinely becoming more capable.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1038/s41586-024-07566-y" target="_blank" rel="noopener">Shumailov, I., Shumilo, Z., Zhao, Y., et al. (2024). "AI Models Collapse When Trained on Recursively Generated Data." <em>Nature</em>, 631, 755-759.</a></p>
 <p class="bib-annotation">Shows that recursive self-training degrades model quality irreversibly. An important open problem for the field: how to sustain improvement as synthetic data becomes prevalent on the internet.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 35.5: Reliability Engineering for Agents Under Production Stress
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-35-ai-society", "section-35.5.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Reliability Engineering Foundations</div>

 <div class="bib-entry-card">
 <p class="bib-ref">Nygard, M. (2018). <em>Release It! Design and Deploy Production-Ready Software</em>, 2nd ed. Pragmatic Bookshelf.</p>
 <p class="bib-annotation">The definitive practitioner's guide to building resilient production systems, covering circuit breakers, bulkheads, and timeout patterns. Provides the software engineering patterns that this section adapts for agent architectures.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1109/MS.2016.60" target="_blank" rel="noopener">Basiri, A. et al. (2016). "Chaos Engineering." <em>IEEE Software</em>, 33(3), 35-41.</a></p>
 <p class="bib-annotation">Introduces the discipline of deliberately injecting failures to test system resilience, pioneered at Netflix. The methodology this section recommends applying to AI agent testing in production.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://sre.google/sre-book/table-of-contents/" target="_blank" rel="noopener">Beyer, B. et al. (2016). <em>Site Reliability Engineering: How Google Runs Production Systems</em>. O'Reilly.</a></p>
 <p class="bib-annotation">Google's comprehensive guide to SRE practices including error budgets, SLOs, and incident management. Provides the operational framework that this section adapts for monitoring agent reliability.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 <div class="bib-category">Agent Architectures &amp; Patterns</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2210.03629" target="_blank" rel="noopener">Yao, S. et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." <em>ICLR 2023</em>.</a></p>
 <p class="bib-annotation">Introduces the ReAct pattern of interleaving reasoning traces with actions, which forms the basis of most agent architectures discussed in this section. Understanding ReAct is prerequisite for designing agent reliability patterns.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://github.com/Significant-Gravitas/AutoGPT" target="_blank" rel="noopener">Significant Gravitas. (2023). "AutoGPT: An Autonomous GPT-4 Experiment." <em>GitHub Repository</em>.</a></p>
 <p class="bib-annotation">The viral open-source project that demonstrated both the potential and fragility of fully autonomous LLM agents. Serves as a case study in why the reliability patterns discussed in this section are necessary.</p>
 <span class="bib-meta">&#128736; Tool</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2308.11432" target="_blank" rel="noopener">Wang, L. et al. (2024). "A Survey on Large Language Model Based Autonomous Agents." <em>Frontiers of Computer Science</em>, 18(6).</a></p>
 <p class="bib-annotation">A comprehensive survey covering agent architectures, capabilities, and evaluation methods. Useful as a reference for the full landscape of agent designs that reliability engineering must accommodate.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 35.6: Observability, Testing, and CI/CD for Agent Workflows
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-35-ai-society", "section-35.6.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Observability Tools</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://opentelemetry.io/docs/specs/" target="_blank" rel="noopener">OpenTelemetry Authors. (2024). "OpenTelemetry Specification." <em>opentelemetry.io</em>.</a></p>
 <p class="bib-annotation">The vendor-neutral open standard for distributed tracing, metrics, and logging that this section recommends as the foundation for agent observability. Enables consistent instrumentation across heterogeneous agent components.</p>
 <span class="bib-meta">&#128736; Tool</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://langfuse.com" target="_blank" rel="noopener">Langfuse Team. (2024). "Open Source LLM Engineering Platform." <em>langfuse.com</em>.</a></p>
 <p class="bib-annotation">An open-source platform purpose-built for tracing and evaluating LLM applications, with support for prompt versioning and cost tracking. The most mature open-source LLM observability tool at the time of writing.</p>
 <span class="bib-meta">&#128736; Tool</span>
 </div>

 <div class="bib-category">Testing &amp; Evaluation</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1109/BigData.2017.8258038" target="_blank" rel="noopener">Breck, E. et al. (2017). "The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction." <em>IEEE International Conference on Big Data</em>.</a></p>
 <p class="bib-annotation">Proposes a practical rubric for assessing ML system readiness across data, model, infrastructure, and monitoring dimensions. Provides the quality framework adapted for agent systems in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2404.12272" target="_blank" rel="noopener">Shankar, S. et al. (2024). "Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences." <em>arXiv:2404.12272</em>.</a></p>
 <p class="bib-annotation">Examines the reliability of using LLMs to evaluate other LLMs, finding significant alignment gaps with human judgment. Directly relevant to this section's discussion of automated testing for agent outputs.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Continuous Delivery</div>

 <div class="bib-entry-card">
 <p class="bib-ref">Humble, J. and Farley, D. (2010). <em>Continuous Delivery</em>. Addison-Wesley.</p>
 <p class="bib-annotation">The foundational text on continuous delivery practices including deployment pipelines, automated testing, and release strategies. Provides the CI/CD principles that this section adapts for agent deployment workflows.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 </section>"""

# ============================================================
# Section 35.7: Memory Architectures That Improve Execution
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-35-ai-society", "section-35.7.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Memory Systems for Agents</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.08560" target="_blank" rel="noopener">Packer, C. et al. (2023). "MemGPT: Towards LLMs as Operating Systems." <em>arXiv:2310.08560</em>.</a></p>
 <p class="bib-annotation">Introduces an OS-inspired memory management system with virtual context paging for LLMs. The primary architectural reference for the memory hierarchy discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2404.13501" target="_blank" rel="noopener">Zhang, Z. et al. (2024). "A Survey on the Memory Mechanism of Large Language Model Based Agents." <em>arXiv:2404.13501</em>.</a></p>
 <p class="bib-annotation">Comprehensive survey categorizing memory mechanisms into sensory, short-term, and long-term types across agent frameworks. Provides the taxonomic framework used to organize memory architectures in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2304.03442" target="_blank" rel="noopener">Park, J. S. et al. (2023). "Generative Agents: Interactive Simulacra of Human Behavior." <em>UIST 2023</em>.</a></p>
 <p class="bib-annotation">Creates believable agents that maintain memory streams with reflection, planning, and retrieval. Demonstrates how structured memory enables coherent long-term agent behavior in simulated environments.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Tools &amp; Platforms</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://www.getzep.com" target="_blank" rel="noopener">Zep AI. (2024). "Zep: Long-Term Memory for AI Assistants." <em>getzep.com</em>.</a></p>
 <p class="bib-annotation">A production memory layer that automatically extracts, embeds, and retrieves facts and conversation history. Represents the most mature commercial solution for the agent memory problem.</p>
 <span class="bib-meta">&#128736; Tool</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://mem0.ai" target="_blank" rel="noopener">Mem0 AI. (2024). "Mem0: The Memory Layer for Personalized AI." <em>mem0.ai</em>.</a></p>
 <p class="bib-annotation">An open-source memory framework that provides automatic memory extraction and retrieval for personalized AI interactions. Offers a lightweight alternative to Zep for developers building memory-enabled agents.</p>
 <span class="bib-meta">&#128736; Tool</span>
 </div>

 <div class="bib-category">Retrieval-Augmented Approaches</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2005.11401" target="_blank" rel="noopener">Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." <em>NeurIPS 2020</em>.</a></p>
 <p class="bib-annotation">The foundational RAG paper showing that retrieval over external knowledge dramatically improves factual accuracy. Provides the retrieval-based memory foundation on which many agent memory systems build.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 35.8: Self-Improving and Adaptive Agents in Deployment Loops
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-35-ai-society", "section-35.8.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Pipeline Optimization</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.03714" target="_blank" rel="noopener">Khattab, O. et al. (2023). "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." <em>arXiv:2310.03714</em>.</a></p>
 <p class="bib-annotation">Introduces a programming framework that automatically optimizes prompts and few-shot examples through compilation. The primary reference for the systematic prompt optimization approaches discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2406.07496" target="_blank" rel="noopener">Yuksekgonul, M. et al. (2024). "TextGrad: Automatic Differentiation via Text." <em>arXiv:2406.07496</em>.</a></p>
 <p class="bib-annotation">Proposes treating LLM calls as differentiable operations with text-based gradients, enabling backpropagation through complex AI systems. Represents the frontier of automated optimization for compound AI systems.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2305.03495" target="_blank" rel="noopener">Pryzant, R. et al. (2023). "Automatic Prompt Optimization with Gradient Descent and Beam Search." <em>EMNLP 2023</em>.</a></p>
 <p class="bib-annotation">Uses gradient-guided search to automatically improve prompt text, achieving performance comparable to expert-written prompts. Demonstrates that prompt engineering can be systematically automated.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Self-Reflection &amp; Improvement</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2310.11453" target="_blank" rel="noopener">Shinn, N. et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Agents learn from failure by generating verbal self-reflections stored in memory, improving on subsequent attempts without weight updates. The seminal work on experience-driven agent improvement discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2303.17651" target="_blank" rel="noopener">Madaan, A. et al. (2023). "Self-Refine: Iterative Refinement with Self-Feedback." <em>NeurIPS 2023</em>.</a></p>
 <p class="bib-annotation">Shows that LLMs can iteratively improve their own outputs through self-generated feedback, without external signals. Demonstrates the simplest form of self-improvement loop applicable to deployed agents.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Prompt Evolution</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://arxiv.org/abs/2309.16797" target="_blank" rel="noopener">Fernando, C. et al. (2023). "Promptbreeder: Self-Referential Self-Improvement via Prompt Evolution." <em>arXiv:2309.16797</em>.</a></p>
 <p class="bib-annotation">Applies evolutionary algorithms to prompts, evolving both task prompts and mutation prompts in a self-referential loop. Explores the frontier of autonomous prompt optimization that pushes beyond gradient-based methods.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""

# ============================================================
# Section 35.9: The Future of Human-AI Collaboration
# ============================================================
bibliographies[os.path.join(PART10_DIR, "module-35-ai-society", "section-35.9.html")] = """<section class="bibliography">
 <div class="bibliography-title">References &amp; Further Reading</div>

 <div class="bib-category">Key Books &amp; Frameworks</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://wwnorton.com/books/The-Second-Machine-Age/" target="_blank" rel="noopener">Brynjolfsson, E. and McAfee, A. (2014). <em>The Second Machine Age: Work, Progress, and Prosperity in a Time of Brilliant Technologies</em>. W.W. Norton.</a></p>
 <p class="bib-annotation">Frames the current AI era as a fundamental economic transformation comparable to the industrial revolution. Provides the macroeconomic perspective on human-AI collaboration that grounds this section's discussion.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref">Agrawal, A., Gans, J., and Goldfarb, A. (2018). <em>Prediction Machines: The Simple Economics of Artificial Intelligence</em>. Harvard Business Review Press.</p>
 <p class="bib-annotation">Reframes AI as a tool that dramatically reduces the cost of prediction, making previously impractical decisions economically viable. Provides the economic reasoning for how AI changes the value of human judgment.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://global.oup.com/academic/product/human-centered-ai-9780192845290" target="_blank" rel="noopener">Shneiderman, B. (2022). <em>Human-Centered AI</em>. Oxford University Press.</a></p>
 <p class="bib-annotation">Advocates for AI design that amplifies human capabilities rather than replacing human agency. The primary reference for the human-centered design philosophy advocated in this section.</p>
 <span class="bib-meta">&#128214; Book</span>
 </div>

 <div class="bib-category">Human-AI Interaction Research</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1145/3290605.3300233" target="_blank" rel="noopener">Amershi, S. et al. (2019). "Guidelines for Human-AI Interaction." <em>CHI 2019</em>.</a></p>
 <p class="bib-annotation">Distills 18 design guidelines for AI-powered products, validated through a large-scale heuristic evaluation. The most widely cited practical guide for designing human-AI collaboration interfaces.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1145/3411764.3445717" target="_blank" rel="noopener">Bansal, G. et al. (2021). "Does the Whole Exceed Its Parts? The Effect of AI Explanations on Complementary Team Performance." <em>CHI 2021</em>.</a></p>
 <p class="bib-annotation">Finds that AI explanations do not always improve human-AI team performance and can sometimes harm it. A cautionary result for the design of explainable AI systems in collaborative settings.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://doi.org/10.1518/001872097778543886" target="_blank" rel="noopener">Parasuraman, R. and Riley, V. (1997). "Humans and Automation: Use, Misuse, Disuse, Abuse." <em>Human Factors</em>, 39(2), 230-253.</a></p>
 <p class="bib-annotation">The classic taxonomy of automation failures: overreliance (misuse), underutilization (disuse), and inappropriate deployment (abuse). Provides the conceptual framework for understanding trust calibration in human-AI teams.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-category">Governance &amp; Standards</div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://eur-lex.europa.eu/eli/reg/2024/1689/oj" target="_blank" rel="noopener">European Parliament and Council. (2024). "Regulation (EU) 2024/1689 (AI Act)." <em>Official Journal of the European Union</em>.</a></p>
 <p class="bib-annotation">The EU's comprehensive AI regulation requiring transparency and human oversight for high-risk AI systems. Sets the legal context for the human-in-the-loop requirements discussed in this section.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 <div class="bib-entry-card">
 <p class="bib-ref"><a href="https://www.sae.org/standards/content/j3016_202104/" target="_blank" rel="noopener">SAE International. (2021). "J3016: Taxonomy and Definitions for Terms Related to Driving Automation Systems." <em>SAE Standard</em>.</a></p>
 <p class="bib-annotation">Defines the six levels of driving automation from Level 0 (no automation) to Level 5 (full automation). This taxonomy of autonomy levels is widely adapted for describing AI agent autonomy in general settings.</p>
 <span class="bib-meta">&#128196; Paper</span>
 </div>

 </section>"""


def replace_bibliography(filepath, new_bib):
    """Replace the bibliography section in the given file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace the bibliography section
    pattern = r'<section class="bibliography">.*?</section>'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"WARNING: No bibliography found in {os.path.basename(filepath)}")
        return False

    new_content = content[:match.start()] + new_bib + content[match.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # Count annotations in new bibliography
    annotation_count = new_bib.count('bib-annotation')
    entry_count = new_bib.count('bib-entry-card')
    category_count = new_bib.count('bib-category')
    print(f"OK: {os.path.basename(filepath)} - {entry_count} entries, {annotation_count} annotations, {category_count} categories")
    return True


def main():
    total_files = 0
    total_entries = 0
    total_annotations = 0

    for filepath, new_bib in bibliographies.items():
        if replace_bibliography(filepath, new_bib):
            total_files += 1
            total_entries += new_bib.count('bib-entry-card')
            total_annotations += new_bib.count('bib-annotation')

    print(f"\nSummary: {total_files} files processed, {total_entries} entries, {total_annotations} annotations added")


if __name__ == '__main__':
    main()
