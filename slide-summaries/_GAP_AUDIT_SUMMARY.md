# Gap Audit — Consolidated Summary

## Family A (chapters 1, 2, 3, 4)
- Items: 56 | Present: 22 | Partial: 15 | Missing: 19
- Top must-add items:
  1. Section 1.2: Add a topic-models bridge (BoW -> topic vectors -> LSA via truncated SVD -> LDiA as Bayesian mixture). The single biggest classical-NLP gap in Ch 1; deck 1122 has the full pipeline.
  2. Section 3.8: Add the MoE parameter arithmetic worked example from deck 1308 slides 3-4 (dense 2M -> 16 experts of 130K each). The conceptual gap that makes 'capacity vs compute' click for readers.
  3. Section 3.3 (or appendix): Add the full encoder-decoder reference implementation from deck 1307 (Residual class, DecoderLayer with three residual blocks, dual mask helpers, EncoderDecoderTransformer). Book builds only decoder-only; readers building MT or seq2seq systems need this.
  4. Section 1.4: Add a focused BERT pretraining walkthrough (MLM + NSP + [CLS] as sentence embedding + RoBERTa variant). Currently fragmented across sections; deck 1303 has the clean version.
  5. Section 1.3: Add the 'generalized embeddings' subsection (graph walks, song-recommendation pipeline from deck 1123 slides 18-21). Memorable, non-NLP application that makes the distributional hypothesis click.
- ALL missing items (18):
  * [1.1] (diagram, slide 1012) Healthcare LLM applications, split into professional-facing (clinical documentation, radiology, triage, etc.) vs patient-facing (lab results, symptom assessment, medication adherence, etc.)
    -> Book has no domain-application overview. A short Healthcare/Cybersecurity/Software Engineering tri-domain figure (or callout) would broaden the motivation in Section 1.1.
  * [1.1] (diagram, slide 1012) Cybersecurity LLM applications: nine application families plus 5-branch 'opportunities due to LLMs' tree (vulnerability detection, content classification, explainability, data challenges, LLM-risk mitigation including guardrails/deepfakes/adversarial examples)
    -> Book does not catalogue cybersecurity LLM uses anywhere in Ch 1. Worth a single 'domain panorama' callout that also acknowledges LLMs are part of the attack surface, not only the defense.
  * [1.1] (diagram, slide 1012) Five-petal SE-lifecycle map of LLM use: documentation, code generation, testing/debugging, code review/optimization, synthetic data generation
    -> Book mentions code generation as one task but does not show the full SE-lifecycle decomposition; useful for the 'audience is developers' framing.
  * [1.2] (key technical point, slide 1122) Linear Discriminant Analysis (LDA classifier): find a direction in N-dim space along which classes are maximally separated
    -> Book does not introduce LDA as a classical baseline classifier anywhere in Ch 1. Optional but cheap to add as a one-paragraph mention with the deck's class-separation visualization.
  * [1.2] (key technical point, slide 1122) Confusion matrix, precision, recall as evaluation tools for text classification
    -> Book defers all evaluation metrics to a later chapter. A two-sentence pointer + matrix sketch inside Section 1.2 would close the loop on the classical-NLP narrative without duplicating Part 9.
  * [1.2] (key technical point, slide 1122) Topic-vector representation as denser, semantically-meaningful alternative to BoW (e.g., 80% sport, 20% news); motivation that frequently co-occurring words belong to the same topic
    -> Book skips topic models entirely. This is the single biggest classical-NLP gap in Ch 1. A short subsection (1.2.x or 1.3.0) introducing topic vectors would bridge BoW/TF-IDF to dense embeddings more s
  * [1.2] (key technical point, slide 1122) Document-Term Matrix (DTM) and Latent Semantic Analysis (LSA) via truncated SVD; rank = number of topics; document-topic matrix as input features for LDA classifier
    -> LSA / truncated-SVD topic models are nowhere in the book. Worth a short callout especially since LSA is still actively used in production search and a useful conceptual stepping stone to dense embeddi
  * [1.2] (key technical point, slide 1122) Latent Dirichlet Allocation (LDiA): each topic is a distribution over words; each document is a mixture of topic distributions; number of topics is a hyperparameter swept via coherence/perplexity
    -> LDiA is not in Ch 1 (or anywhere in Part 1). Section 1.2 should briefly mention LDiA, even just as a forward reference, given it remains widely used and is conceptually paired with the Gibbs-sampling 
  * [1.3] (formula, slide 1123) cosmul similarity (Levy-Goldberg analogy scoring): ratio of products of positive to negative cosine distances
    -> Book covers cosine similarity exhaustively but never mentions cosmul. This is a low-cost addition (one formula + one Gensim usage example) that improves analogy demos.
  * [1.3] (code, slide 1123) Generalized embeddings: token sequences beyond language (graphs as node walks, songs as playlist sequences); end-to-end song-recommendation pipeline (build corpus from playlists, train Word2Vec, query nearest songs)
    -> Book misses the generalization angle entirely (graph walks, song recommendation, no-metadata embeddings). This is a memorable application example that would substantially strengthen Section 1.3's 'why
  * [1.4] (key technical point, slide 1303) [CLS] context vector used as a sentence embedding for downstream tasks; alternative is mean pooling of all context vectors
    -> Book does not explicitly cover [CLS] as a sentence embedding mechanism. This is foundational for understanding fine-tuning of BERT-family classifiers and should be added.
  * [1.4] (key technical point, slide 1303) RoBERTa improvements over BERT: MLM-only (no NSP), BPE tokenizer, trained on both single sentences and sentence pairs
    -> Book mentions BERT but not RoBERTa; the slide's concise contrast is useful pedagogy and should be added as a one-paragraph 'BERT variants' note.
  * [3.3] (code, slide 1307) Encoder-decoder PyTorch reference implementation: Residual class wrapping any sub-layer; DecoderLayer with three residual blocks (self-attn, cross-attn, FFN); two masks (tgt_mask causal, src_mask padding); top-level EncoderDecoderTransformer
    -> Section 3.3 builds a decoder-only model from scratch but never assembles the full encoder-decoder reference implementation with separate self/cross/FFN residual blocks and the two-mask pattern. Worth 
  * [3.4] (key technical point, slide 1307) Label smoothing: cross-entropy on one-hot target encourages overconfidence; assigning small probability to other classes acts as regularization
    -> Section 3.4 covers training loop but never mentions label smoothing as a regularizer. Worth a one-paragraph callout, especially since it remains standard practice in MT and helps explain calibration i
  * [3.8] (key technical point, slide 1308) MoE parameter arithmetic: dense FFN 2048*512+512*2048 ~ 2M params; split into 16 experts of hidden 128 each gives 512*128+128*512 ~ 130K per expert (total still 2M but only 1 or few active per token)
    -> Section 3.8.3 introduces MoE conceptually but never shows the parameter arithmetic that makes the case concrete. The slide's step-by-step calc (2M dense -> 16x130K experts) is the single best way to i
  * [4.4] (key technical point, slide 0006) Gibbs sampling / MCMC framework for variational inference: resample one coordinate at a time from its full conditional p(z_i | z_{-i}); applied to latent-variable models like Naive Bayes mixtures and LDiA
    -> Section 4.4 covers diffusion LMs but does not connect them to the broader iterative-refinement / MCMC family. A short callout linking discrete-diffusion denoising to Gibbs sampling (each step resample
  * [4.4] (key technical point, slide 0006) Beta and Dirichlet as conjugate priors for Bernoulli and multinomial; conjugacy enables closed-form integration and 'add counters' update rule
    -> Outside the immediate scope of Ch 4.4 (decoding), but worth flagging for any future topic-models / Bayesian-NLP appendix. The Gibbs deck is essentially LDiA inference, which the book never covers.
  * [4.4] (key technical point, slide 0006) MCMC practical caveats: burn-in (discard first B iterations), lag (take every Lth sample to reduce autocorrelation), multiple chains from different starts
    -> Useful context for understanding why diffusion LMs need 20-50 denoising steps (analog of burn-in) and why temperature/parallel chains are used. Add as a 'Note: Connection to MCMC' callout in Section 4

## Family B (chapters 6, 7, 10)
- Items: 38 | Present: 11 | Partial: 11 | Missing: 16
- Top must-add items:
  1. Add a 'Foundation Models' framing callout in section 6.1 that contrasts one-model-per-task with one FM serving many tasks, names the three adaptation strategies (composition with frozen FM + task head, fine-tuning, prompting/ICL), and points to where each is covered later (chapters 12, 16, 17).
  2. Add coverage of BERT's Next Sentence Prediction objective, the [CLS] sentence-embedding pattern, the mean-pooling alternative, and the joint MLM + NSP loss in section 6.2 (currently essentially absent across chapter 6 and 7).
  3. Add a 'multilingual pretraining objectives' subsection in section 7.4 that introduces the original XLM model and the three losses (MLM, CLM, TLM = Translation Language Modeling), with the MLM vs TLM contrast diagram (slide 1311-3); currently only XLM-R is mentioned.
  4. Add the Noam learning-rate schedule (linear warmup + inverse-square-root decay) to section 6.5.5 alongside cosine and WSD, with a short PyTorch implementation; it is the historical reference schedule from 'Attention Is All You Need' and is currently missing.
  5. Strengthen section 10.3 SHAP coverage with the 'not bad' single-token-masking failure walkthrough (slide 1310-12), a tabular waterfall plot example, and a beeswarm visualization; also add a one-paragraph mention of transformer-interpret as a minimal HF wrapper around Captum IG.
- ALL missing items (15):
  * [6.1] (key_point, slide 1141_FM_Intro) Image-side analogs: fine-tuning images, in-context/zero-shot classification by similarity to class prototypes
    -> Slides 4 and 7 show that the three adaptation strategies are modality-agnostic; Part II focuses on text. Could cite as a cross-reference to Part 5 (multimodal) but currently absent.
  * [6.1] (key_point, slide 1303_TransformerPretraining) Next Sentence Prediction (NSP) and [CLS] token mechanics
    -> NSP and [CLS] are essentially absent from chapter 6/7 (only one stray '[CLS]' mention in 10.5 output). Slide 3, 5, 6, 7 describe [CLS] as sentence embedding via NSP loss; this foundational mechanism i
  * [6.1] (key_point, slide 1303_TransformerPretraining) [CLS] context vector reused as sentence embedding for downstream tasks; mean pooling as alternative
    -> Slide 6 explicitly explains the [CLS]-as-sentence-embedding pattern and mean-pooling alternative. Book does not mention this pooling strategy for sentence embeddings in chapter 6 or 7; embeddings come
  * [6.2] (formula, slide 1303_TransformerPretraining) Joint BERT loss: L = L_MLM + L_NSP
    -> Slide 7 shows the combined loss. Book covers MLM and CLM formulas but does not show the BERT joint objective.
  * [10.3] (key_point, slide 1310_LLM_ExplainingTransformer) Naive single-token masking fails: 'not bad' worked example showing interaction invisibility
    -> Slide 12 has a memorable 'not bad' walkthrough showing why single-token masking misses interactions and motivates SHAP. Book covers SHAP but lacks this specific pedagogical example.
  * [10.3] (diagram, slide 1310_LLM_ExplainingTransformer) SHAP waterfall plot for house-price prediction: base 2.215 -> f(x) 2.846 read bottom-up
    -> Slide 14's concrete waterfall plot from home-price tabular SHAP is a memorable bridge; book talks about SHAP for LMs but does not show the canonical tabular waterfall illustration.
  * [10.3] (diagram, slide 1310_LLM_ExplainingTransformer) SHAP beeswarm plot across dataset: X = SHAP value, color = normalized feature value
    -> Slide 15's beeswarm view of dataset-level SHAP is not in the book; would strengthen 10.3.
  * [7.4] (key_point, slide 1311_LLM_MultilinguialEncoder) Original XLM model (Lample and Conneau 2019) as a multilingual encoder distinct from XLM-R
    -> Section 7.4 mentions only XLM-R (Conneau 2020). The earlier XLM with the explicit MLM + CLM + TLM training recipe (which slides 2-3 describe in detail) is not covered.
  * [7.4] (key_point, slide 1311_LLM_MultilinguialEncoder) Three XLM losses: MLM (single-sentence), CLM (single-sentence next-token), TLM (Translation Language Modeling, mask token in one language recovered using the other)
    -> Slide 2-3 describe TLM as the key cross-lingual signal. Book does not introduce TLM as a pretraining objective in 6.2 or 7.4.
  * [7.4] (diagram, slide 1311_LLM_MultilinguialEncoder) MLM vs TLM contrast figure: same-sentence recovery vs cross-lingual recovery
    -> Slide 3 has a clean side-by-side. Section 7.4 talks about cross-lingual transfer at the representation level but not the explicit pretraining objective comparison.
  * [6.5] (key_point, slide 1311_LLM_MultilinguialEncoder) Noam learning-rate schedule (Vaswani et al.): linear warmup then inverse-square-root decay
    -> Section 6.5.5 covers warmup, cosine decay, and WSD schedules but does not mention the original Noam schedule from 'Attention Is All You Need', which slide 6 highlights. This is a historical/pedagogica
  * [6.5] (code, slide 1311_LLM_MultilinguialEncoder) Noam scheduler PyTorch implementation
    -> No code example for Noam scheduler in book. Slide 7 shows the canonical reference implementation.
  * [6.9] (code, slide 1311_LLM_MultilinguialEncoder) Batch class bundling source, target, and masks for translation training
    -> The classic Annotated Transformer Batch class (slide 9) is a useful pedagogical pattern; section 6.9 lab covers tiny GPT but not seq2seq translation.
  * [6.9] (code, slide 1311_LLM_MultilinguialEncoder) End-to-end multilingual training loop with Batch + Noam optimizer
    -> No multilingual/seq2seq lab in chapter 6 or 7. Slide 10 walks through a translation training loop; could be appendix-grade material.
  * [7.4] (code, slide 1311_LLM_MultilinguialEncoder) Translation inference and concrete example outputs
    -> Slides 11-12 show end-to-end translation examples; section 7.4 is largely conceptual on multilingual issues with no translation-specific runnable example.

## Family C (chapters 0.5, 16, 17, 18)
- Items: 82 | Present: 32 | Partial: 19 | Missing: 31
- Top must-add items:
  1. {'rank': 1, 'title': 'Actor-Critic and advantage baseline in Section 0.5', 'rationale': "Without Actor-Critic and the R - V(s) advantage formulation, the four-model PPO setup (policy / reference / reward / value head) introduced in 18.1.3 lacks its pedagogical bridge. Currently the reader leaps from vanilla REINFORCE to PPO with no explanation of why a value network appears alongside the policy. Adding a 0.5.4b subsection on actor-critic and one-step TD (r + gamma V(s') - V(s)) would make the value head, GAE, and the entire RLHF stack feel inevitable rather than introduced ad hoc."}
  2. {'rank': 2, 'title': 'Multi-armed bandit, contextual bandit, and Markov property in Section 0.5', 'rationale': "Section 0.5 currently invokes states, actions, and Q-values without first defining the Markov property or building intuition from the simpler MAB and contextual bandit. The slide deck progression (MAB to contextual bandit to MDP) is pedagogically tight. Add a short 0.5.1.x subsection covering bandits, the explore-exploit tradeoff, epsilon-greedy and softmax-with-temperature, then state Markov property and transition kernel P(s' | s, a) before V and Q."}
  3. {'rank': 3, 'title': 'Sentence-embedding domain-adaptation recipes (SBERT name + bootstrapping, SDAE, SimCSE) in Section 16.5', 'rationale': 'Section 16.5 covers contrastive learning generically but skips the three canonical recipes that practitioners actually search for: SBERT siamese bi-encoder with NLI, semi-supervised gold-to-silver bootstrapping with balanced nearest-neighbor sampling, SDAE unsupervised denoising, and SimCSE dropout-as-augmentation. Add these as named subsections in 16.5 with code; also add STSB and MTEB as evaluation benchmarks.'}
  4. {'rank': 4, 'title': 'NER fine-tuning subsection and SetFit in Section 16.6', 'rationale': 'Section 16.6 covers single-label and sequence-pair classification but treats NER only as an exercise. The slide deck has a full NER pipeline (CoNLL-2003, B/I tagging, word-to-subword label inheritance, seqeval entity-level metric). SetFit (few-shot binary-pair contrastive fine-tuning of sentence transformer plus classifier head) is also absent and is the production-default few-shot recipe. Add 16.6.x NER subsection and 16.6.y SetFit subsection.'}
  5. {'rank': 5, 'title': 'Long-document classification strategy catalog in Section 16.7', 'rationale': 'Section 16.7 frames long context as a generative problem with RoPE scaling. The classification-specific catalog (truncate, sliding-window + aggregate, hierarchical transformer, Longformer/BigBird long-sequence attention, summarize-first, zero-shot generative, retrieval-augmented classification) is missing entirely. Add a 16.7.x subsection enumerating the seven strategies with a decision table, since this is one of the most frequent practitioner questions for long-document NLP.'}
- ALL missing items (33):
  * [?] (?, slide ?) ?
    -> Section 16.5 mentions evaluation generically but never names STSB or explains the Mean Opinion Score and Spearman correlation protocol for embedding quality.
  * [?] (?, slide ?) ?
    -> MTEB is the canonical benchmark for foundation embedding models but is not mentioned in the embedding fine-tuning section. Should be added to 16.5.
  * [?] (?, slide ?) ?
    -> Book covers chat templates and apply_chat_template but does not explicitly explain the role of EOS / <|endoftext|> in training the model when to stop and how this connects to autoregressive generation
  * [?] (?, slide ?) ?
    -> The book presents only the standard mask-prompt-to-zero approach. Prompt dampening as a softer alternative is not mentioned and would fit as a short callout in 16.3.
  * [?] (?, slide ?) ?
    -> Book jumps directly to NF4 and bytes-per-precision tables without explaining how FP16 vs BF16 vs INT8 differ at the representation level. Acceptable for an LLM book, but a short callout could improve 
  * [?] (?, slide ?) ?
    -> The slide deck lists the explicit NF4 anchor values that motivate the 4-bit normal-aware design. Book treats NF4 as a black box invoked via config. A diagram or table of the 16 anchors would deepen th
  * [?] (?, slide ?) ?
    -> The whole bootstrap recipe (gold cross-encoder, balanced silver generation via nearest-neighbour sampling, SBERT training on silver) is absent from the embedding-fine-tuning chapter. This is a high-va
  * [?] (?, slide ?) ?
    -> SDAE for unsupervised sentence-embedding domain adaptation is a recognized recipe but not in the book. Should be added as a method in 16.5 alongside contrastive learning.
  * [?] (?, slide ?) ?
    -> SimCSE is the standard unsupervised baseline for sentence embeddings (huge in the literature) but is absent from 16.5. Worth at least a paragraph and code snippet.
  * [?] (?, slide ?) ?
    -> Critical practical detail for any NER fine-tuning. Absent.
  * [?] (?, slide ?) ?
    -> Entity-level vs token-level F1 distinction is important for NER reporting. Not in the book.
  * [?] (?, slide ?) ?
    -> SetFit is the standard few-shot text-classification recipe and is fully absent from the book. Should be added to 16.6 with a short callout and code, especially as it pairs well with sentence-transform
  * [?] (?, slide ?) ?
    -> Section 16.7 covers chunking for generation (with overlap and semantic splits) but not the classification pattern of per-chunk inference plus aggregation.
  * [?] (?, slide ?) ?
    -> A standard architecture choice for long-document classification that is fully absent.
  * [?] (?, slide ?) ?
    -> Longformer and BigBird are referenced obliquely in long-context discussion but not given dedicated treatment with their attention-pattern diagrams. RoPE-based extension is the only long-context story 
  * [?] (?, slide ?) ?
    -> A pragmatic but commonly used pattern; should be added either to 16.6 or 16.7.
  * [?] (?, slide ?) ?
    -> Perceiver-AR is missing from the long-context architecture survey.
  * [?] (?, slide ?) ?
    -> MergeKit supports pass-through but Frankenmerging as a flow-space strategy distinct from parameter-space approaches is not enumerated. Should add as a short subsection.
  * [?] (?, slide ?) ?
    -> Book treats merging optimistically with research-frontier framing. The slide deck's honest reality-check (most merging gains turned out modest, primarily checkpoint-averaging value) is absent. Worth a
  * [?] (?, slide ?) ?
    -> The book never makes the state-space argument that motivates 'why deep'. This is the canonical pedagogical hook of the RL intro deck and is missing.
  * [?] (?, slide ?) ?
    -> Book uses a custom SimpleGridWorld but never names Gym/Gymnasium as the ecosystem the reader will find in the wild. Worth a short pointer plus a CartPole or MountainCar example.
  * [?] (?, slide ?) ?
    -> DQN is the historical anchor for deep RL but not discussed in 0.5. The Q-learning exercise is tabular only. Adding a one-paragraph DQN sketch (CNN over screen pixels, replay buffer, target network) wo
  * [?] (?, slide ?) ?
    -> MAB is the canonical stateless RL problem and the entry point used in the slide deck. Book jumps straight to full MDP / policy gradient without the bandit warm-up. Adding even a short MAB subsection w
  * [?] (?, slide ?) ?
    -> The Boltzmann / softmax selection policy and the temperature parameter are missing. This is a key concept that connects directly to LLM sampling (same softmax-over-logits with temperature).
  * [?] (?, slide ?) ?
    -> Contextual bandit is the bridge from MAB to MDP and is absent. Adding it (with the ad-placement example) would make the leap from bandit Q to deep contextual-bandit network natural before introducing 
  * [?] (?, slide ?) ?
    -> Markov property as a modeling choice (with concrete examples like medical treatment vs diagnosis) is missing. Section 0.5 should at minimum define it before invoking V/Q.
  * [?] (?, slide ?) ?
    -> Transition kernel notation absent. Add definition to 0.5.1 or 0.5.3.
  * [?] (?, slide ?) ?
    -> Book uses sampling but never warns that gradient descent in a stationary environment can collapse the distribution to a near-degenerate one. Worth a short note.
  * [?] (?, slide ?) ?
    -> CartPole is the canonical RL pedagogical environment and a results-curve plot would visualize learning progress. Worth using as an alternative or supplementary example.
  * [?] (?, slide ?) ?
    -> Actor-Critic is the bridge from REINFORCE to PPO (PPO uses an actor-critic architecture with the value head). Currently 0.5 jumps from vanilla REINFORCE straight to PPO without explaining the advantag
  * [?] (?, slide ?) ?
    -> TD-style advantage is the building block of GAE referenced in 18.1.3. Currently the reader sees GAE as a callout without the underlying 1-step TD intuition.
  * [?] (?, slide ?) ?
    -> Distributed AC is an advanced topic; arguably out of scope for 0.5 but a forward pointer would help readers when they see vLLM rollout + FSDP trainer hybrid engines referenced in 18.5.
  * [?] (?, slide ?) ?
    -> N-step methods are the standard variance/bias trade-off lever in modern RL. Should at minimum get a sentence in 0.5.

## Family D (chapters 22)
- Items: 27 | Present: 12 | Partial: 10 | Missing: 5
- Top must-add items:
  1. {'id': 'D-22', 'topic': 'Swin Transformer: shifted windows, W-MSA/SW-MSA, hierarchical patch merging', 'where': 'New sub-section in 22.1 (between 22.1.6 and 22.1.7) or a row in the ViT-zoo table', 'rationale': 'Swin is a foundational ViT variant used as a backbone in most production detection and segmentation stacks; its absence is a notable gap in a chapter that aims to be the canonical VLM reference.'}
  2. {'id': 'D-19', 'topic': 'DeiT: data-efficient ViT via CNN-teacher distillation token', 'where': 'New paragraph or sidebar in 22.1.5 (pretraining objectives) covering the distillation-token recipe', 'rationale': 'DeiT is the ImageNet-1K bridge that made ViTs trainable without JFT-300M; its distillation-token pattern is also pedagogically useful as a stepping stone to DINO self-distillation.'}
  3. {'id': 'D-06', 'topic': 'VisualBERT and the R-CNN region-feature lineage of VLMs', 'where': 'Historical-roots sidebar in 22.3 (before the LLaVA recipe), or in 22.7 (early fusion variants)', 'rationale': 'VisualBERT plus MLM + SIA training is the pre-CLIP VLM lineage that the slides cover in detail; including it gives the chapter the contrast that explains why patch-token VLMs replaced region-feature VLMs.'}
  4. {'id': 'D-20', 'topic': 'Original DINO recipe: local vs global crops, multi-crop targeting, EMA teacher', 'where': 'Expand the DINOv2 note callout in 22.1.5 to cover the original DINO multi-crop strategy', 'rationale': 'The book covers DINOv2 EMA centering but skips the local/global crop construction that is the conceptual heart of self-distillation. Two paragraphs would close the loop.'}
  5. {'id': 'D-12', 'topic': 'Four-bucket pretrained-vision-models taxonomy (task-specific, representation, multimodal, generative)', 'where': 'Reframing paragraph or four-row table at the top of 22.1 or in chapter introduction', 'rationale': 'Slide deck 2221 uses this taxonomy as scaffolding before any specific model. The chapter would benefit from giving readers the same mental shelf so later models (CLIP, BLIP, DINO, SAM, diffusion) drop into clear buckets.'}
- ALL missing items (6):
  * [?] (?, slide ?) ?
    -> VisualBERT, R-CNN-based region features, Sentence-Image Alignment, and closed-vocabulary VQA classification heads are not discussed anywhere in Chapter 22. Could fit as a historical-roots note in 22.3
  * [?] (?, slide ?) ?
    -> Open-ended VQA recipe (embed image + question + candidate, binary head per candidate) is absent. Could land in 22.3 with a brief note on classical VQA evaluation versus generative VLMs.
  * [?] (?, slide ?) ?
    -> The chapter has a LLaVA-NeXT generate() example but no BLIP-2 / BLIP-3 inference snippet. A short code fragment showing AutoProcessor + Blip2ForConditionalGeneration on a captioning task and a multi-t
  * [?] (?, slide ?) ?
    -> DeiT and its distillation token (ImageNet-1K versus ImageNet-21K) are not covered in Chapter 22. Could fit in 22.1 as a sidebar on data efficiency for ViTs, or in a new sub-section on the ViT family. 
  * [?] (?, slide ?) ?
    -> Swin Transformer is entirely absent from Chapter 22, despite being a foundational ViT variant for dense prediction (detection, segmentation), with its W-MSA/SW-MSA alternation and FPN-style hierarchic
  * [?] (?, slide ?) ?
    -> The book briefly hints at DINOv2 features being good for segmentation but does not discuss multi-scale hierarchical representations suitable as detection/segmentation backbones (the Swin/FPN pattern).

## Family E (chapters 20)
- Items: 73 | Present: 4 | Partial: 16 | Missing: 53
- Top must-add items:
  1. Section 20.0.1 (NEW): Audio Data & Representations end-to-end primer (sampling, dB, FFT, STFT, mel scale, log-mel spectrogram, MFCC pipeline) with librosa code (covers 5012_Audio_Data slides 4-21).
  2. Section 20.0.2 (NEW): Audio Codec Models & Vector Quantization (VQ, RVQ chain math, Product Quantization, EnCodec full system diagram with multi-loss training, STT estimator + EMA, EnCodec inference code with 1s/75/128/8/1024 anchor, three-applications taxonomy) absorbing 5013_Audio_VectorQuant + EnCodec slides 28-34.
  3. Section 20.0.3 (NEW): Audio & Speech Transformer Architectures (waveform vs spectrogram inputs, AST spectrogram-as-image, CTC theory: aligned vs misaligned seq2seq, repeat+separator trick, forward-backward CTC loss, beam search) absorbing 5014 + slides 1-14 of 5021_Audio_Encoders.
  4. Section 20.0.4 (NEW): Self-Supervised Audio Encoders (HuBERT iterative kmeans+masked cluster prediction + Wav2Vec 2.0 contrastive + Gumbel quantizer + the comparison cheat-sheet table) absorbing slides 15-27 of 5021_Audio_Encoders + 5013 slides 7-13 (Gumbel theory).
  5. Section 20.x.5 (NEW): Audio Classification (4-flavor taxonomy, AST inference recipe, KWS on Speech Commands, intent on MINDS-14, LangID on FLEURS, CLAP zero-shot, full DistilHuBERT GTZAN fine-tune lab) absorbing 5031_Audio_Classification + relevant slides of 5011/5015/5021_MultimodalAudio.
  6. CLAP standalone coverage (architecture, InfoNCE loss, chunk-and-fuse for variable-length audio, T5 keyword-to-sentence augmentation, zero-shot pipeline code) currently entirely missing.
  7. Whisper multitask training format directed graph (SOT -> Language -> Transcribe/Translate/NoSpeech -> Timestamps/Text-only -> EOT) plus lower-level HF processor+generate+batch_decode example showing the <|startoftranscript|><|en|><|transcribe|> control tokens; add to Section 20.5.
  8. Whisper Seq2SeqTrainer fine-tuning recipe on Common Voice with metric_for_best_model='wer'; missing from Section 20.5.11 (would be new subsection).
  9. Vocoder pedagogy (MelGAN/HiFi-GAN as standalone modules turning phaseless spectrograms into waveform, SpeechT5HifiGan example) currently a gap in Section 20.1 between TTS spectrogram outputs and final audio.
  10. Text-to-audio (non-music) sound-effect generation (AudioLDM + TANGO architecture: FLAN-T5 text encoder -> diffusion -> audio decoder -> HiFi-GAN, with train/inference/frozen legend) currently entirely missing; either deepen 20.3 to include Foley/SFX or add a new sub-section between 20.3 and 20.4.
- ALL missing items (66):
  * [20.0 (NEW intro / chapter opener)] (concept, slide 5011_Audio_TypicalTasks) Bipartite Understand/Generate taxonomy of audio tasks (classify events/music, KWS, intent, ASR vs TTS, music gen, noise/event gen)
    -> Chapter currently opens directly into Section 20.1 TTS. Slide 2's Understand/Generate framing is a perfect chapter opener.
  * [20.x.5 Audio Classification (NEW)] (concept, slide 5011_Audio_TypicalTasks) Four flavors of audio classification: content (speech/music/noise), event (alarm/glass/gunfire), speech intent, keyword spotting
    -> Not covered in Chapter 20 at all. Section 20.1-20.5 ignore classification entirely; 20.4 touches on event-removal but not event classification taxonomy.
  * [20.x.5 Audio Classification (NEW)] (code_example, slide 5011_Audio_TypicalTasks) HF `pipeline('audio-classification')` 3-line intent classifier demo
    -> Pipeline-style 3-liner is missing; book only shows TTS/ASR HF examples.
  * [20.0.1 Audio Data & Representations (NEW)] (concept, slide 5012_Audio_Data) Digital audio fundamentals: sampling rate, bit depth, S(t) -> S_i sampling diagram
    -> Book assumes audio fundamentals; nowhere covers sampling/bit depth basics.
  * [20.0.1 (NEW)] (code_example, slide 5012_Audio_Data) librosa.load + waveshow trumpet waveform demo
    -> No librosa onboarding anywhere in Chapter 20.
  * [20.0.1 (NEW)] (concept, slide 5012_Audio_Data) Time vs frequency domain duality, A sin(omega t - phi), single-tone spectra, 3D decomposition
    -> Fourier intuition entirely absent.
  * [20.0.1 (NEW)] (concept, slide 5012_Audio_Data) Decibel scale: N_dB = 10 log10(P / 10^-12), dB ladder (silence/speech/concert/jet)
    -> dB scale never introduced.
  * [20.0.1 (NEW)] (code_example, slide 5012_Audio_Data) Hanning-windowed DFT + amplitude_to_db plot of trumpet harmonics
    -> No DFT/FFT example anywhere.
  * [20.0.1 (NEW)] (concept, slide 5012_Audio_Data) Short-Time Fourier Transform (STFT): window length, hop length, sliding spectrogram construction
    -> STFT mechanics never explained. Section 20.1 mentions multi-scale STFT loss in passing but no construction.
  * [20.0.1 (NEW)] (code_example, slide 5012_Audio_Data) librosa.stft + specshow for 'twinkle twinkle' utterance
    -> No spectrogram visualization examples.
  * [20.0.1 (NEW)] (concept, slide 5012_Audio_Data) Mel scale: perceptual frequency warping, denser low / broader high triangular filterbank
    -> Mel scale referenced as 'log-mel' in 20.1/20.5 but never defined.
  * [20.0.1 (NEW)] (concept, slide 5012_Audio_Data) MFCC pipeline: speech frame -> FFT -> mel filterbank -> log -> DCT -> MFCC coefficients
    -> MFCC is referenced as HuBERT input feature in 20.0.4 plan but classical front-end never explained.
  * [20.0.1 (NEW) or 20.x.5] (code_example, slide 5012_Audio_Data) HF datasets MINDS-14 load + audio/transcription/intent_class schema walkthrough
    -> Dataset onboarding pattern not present.
  * [20.0.1 (NEW)] (concept, slide 5012_Audio_Data) Resampling with cast_column(Audio(sampling_rate=16_000)); nearest/linear/cubic interpolation comparison
    -> Resampling is referenced inside code fragments but never explained.
  * [20.0.2 Audio Codec Models & VQ (NEW)] (concept, slide 5013_Audio_VectorQuant) Vector quantization fundamentals: 80-D 20ms window, 1024 codebook, Voronoi cells diagram
    -> VQ basics nowhere in book; 20.1 dives into RVQ at full speed without VQ scaffolding.
  * [20.0.2 (NEW) or 20.1] (concept, slide 5013_Audio_VectorQuant) RVQ + autoregressive generation: flattening, parallel, VALL-E, delay token-layout patterns
    -> Four token-layout patterns never named. 20.1.3 references Bark's three-stage decomposition but does not discuss the general flatten/parallel/VALL-E/delay design space.
  * [20.0.2 (NEW)] (concept, slide 5013_Audio_VectorQuant) Product Quantization: G groups x K codewords, effective vocab K^G
    -> Product Quantization never mentioned. Needed before Wav2Vec 2.0 quantizer slide 13.
  * [20.0.2 (NEW) or 20.0.4] (concept, slide 5013_Audio_VectorQuant) Differentiable quantization challenge: argmax non-differentiable
    -> The argmax problem and three-trick solution (one-hot reformulation, softmax relaxation, Gumbel sampling) entirely absent.
  * [20.0.2 (NEW)] (concept, slide 5013_Audio_VectorQuant) Reparameterization trick (z = mu + sigma*epsilon)
    -> Concept used elsewhere in book (VAE), but the audio-specific Gumbel build-up is missing.
  * [20.0.2 (NEW)] (concept, slide 5013_Audio_VectorQuant) Gumbel-Max trick + Gumbel-Softmax low-temperature relaxation; plain vs Gumbel softmax density comparison
    -> Needed to explain Wav2Vec 2.0 codebook training.
  * [20.0.4 SSL Audio Encoders (NEW)] (model, slide 5013_Audio_VectorQuant) Wav2Vec 2.0 quantization module: 2 groups x 2 codebooks, projection matrices, Gumbel selection
    -> Slide 13 ties theory to wav2vec 2.0 with the trainable quantization+projection matrices; book never shows this.
  * [20.0.3 Audio Transformers (NEW) or 20.x.5] (model, slide 5014_AudioSpeechTransformers) AST (Audio Spectrogram Transformer): 16x16 overlapped patches, ViT-style encoder, [CLS] token, AudioSet 527 classes
    -> AST entirely absent from Chapter 20. Plan moves AST into 20.0.3 NEW section.
  * [20.0.3 (NEW)] (concept, slide 5014_AudioSpeechTransformers) AST mental model: ViT-on-spectrograms; same recipe (patchify, project, PE, encoder, classify)
    -> Important pedagogical hook tying audio to vision chapters.
  * [20.x.5 Audio Classification (NEW)] (concept, slide 5014_AudioSpeechTransformers) AudioSet coarse classes (Speech/Animal/Music/Human/Tools/Engine...)
    -> AudioSet vocabulary never introduced.
  * [20.x.5 (NEW)] (code_example, slide 5014_AudioSpeechTransformers) AutoFeatureExtractor + ASTForAudioClassification.from_pretrained('MIT/ast-finetuned-audioset-10-10-0.4593') inference recipe
    -> Canonical AST inference 3-liner missing.
  * [20.x.5 (NEW)] (concept, slide 5015_PretrainedAudioModels) Keyword spotting (KWS) closed-vocab classification on Speech Commands
    -> KWS task never introduced.
  * [20.x.5 (NEW)] (code_example, slide 5015_PretrainedAudioModels) AST KWS pipeline with MIT/ast-finetuned-speech-commands-v2
    -> Concrete KWS HF call missing.
  * [20.x.5 (NEW)] (code_example, slide 5015_PretrainedAudioModels) wav2vec2-based intent classification on MINDS-14
    -> Pretrained intent recipe missing.
  * [20.0.4 (NEW)] (model, slide 5015_PretrainedAudioModels) HuBERT representation model: Wav2Vec2Processor + HubertModel + frozen embed extraction + mean pool
    -> HuBERT only mentioned in passing in 20.1 (Mimi distillation) and 20.2 (VC); never trained or explained.
  * [20.0.4 (NEW) or 20.x.5] (concept, slide 5015_PretrainedAudioModels) Linear-probe pattern: frozen HuBERT + small classification head
    -> Standard SSL recipe absent from Chapter 20.
  * [20.x.5 (NEW)] (model, slide 5015_PretrainedAudioModels) CLAP: zero-shot audio classification with shared text-audio embedding space (laion/clap-htsat-unfused)
    -> CLAP entirely absent. Major gap given CLAP is heavily used in TANGO (20.3) and audio-text retrieval.
  * [20.1] (code_example, slide 5015_PretrainedAudioModels) SpeechT5HifiGan loading + vocoder(spectrogram) call
    -> Standalone vocoder code example missing.
  * [20.3 or 20.x.NEW] (model, slide 5015_PretrainedAudioModels) AudioLDM text-to-audio diffusion (cvssp/audioldm-s-full-v2) for non-speech events
    -> Sound-effects/audio-event generation (Foley) not covered; 20.3 is music-only.
  * [20.3 or 20.x.NEW] (model, slide 5015_PretrainedAudioModels) TANGO: FLAN-T5 + diffusion + audio decoder + HiFi-GAN; legend of train/inference/frozen paths
    -> TANGO architecture diagram missing; key reference for text-to-audio diffusion.
  * [20.0.3 (NEW)] (concept, slide 5021_Audio_Encoders) Transformer roles recap (encoder, decoder, encoder-decoder) for audio
    -> Useful scaffolding before introducing audio variants.
  * [20.0.3 (NEW)] (concept, slide 5021_Audio_Encoders) Modality-specific vs multimodal audio transformer taxonomy
    -> Family taxonomy absent.
  * [20.0.3 (NEW) or 20.0.4] (concept, slide 5021_Audio_Encoders) Waveform input embedding: zero-mean/unit-variance normalization, CNN downsample to 512-D / 25ms frames
    -> Wav2Vec2/HuBERT input pipeline never described.
  * [20.0.3 (NEW) or 20.5] (concept, slide 5021_Audio_Encoders) CTC (Connectionist Temporal Classification): aligned vs misaligned seq2seq
    -> CTC never explained. Critical for HuBERT/wav2vec ASR fine-tuning.
  * [20.0.3 (NEW)] (concept, slide 5021_Audio_Encoders) CTC trick: predict character sequences with repetitions + separator + word-break; collapse to clean text
    -> CTC decoding rule absent.
  * [20.0.3 (NEW)] (concept, slide 5021_Audio_Encoders) CTC loss as marginalization over all alignments via forward-backward DP
    -> CTC loss formula missing.
  * [20.0.4 (NEW)] (figure, slide 5021_Audio_Encoders) Encoder comparison table: HuBERT vs Wave2Vec vs EnCodec (input, pretraining, fine-tune, representation)
    -> The cheat-sheet comparison table is missing; would be excellent figure for 20.0.4.
  * [20.0.4 (NEW)] (concept, slide 5021_Audio_Encoders) HuBERT iterative tokenize-via-MFCC->kmeans clustering, then refine via intermediate BERT outputs
    -> Iterative clustering scheme missing.
  * [20.0.4 (NEW)] (concept, slide 5021_Audio_Encoders) HuBERT clustering step + cosine-similarity codeword projection
    -> Mechanics absent.
  * [20.0.4 (NEW)] (concept, slide 5021_Audio_Encoders) HuBERT masked prediction: 50% mask, trained mask vector, cross-entropy on cluster id
    -> Training objective absent.
  * [20.0.4 (NEW) or 20.5] (code_example, slide 5021_Audio_Encoders) HubertForCTC.from_pretrained('facebook/hubert-large-ls960-ft') ASR inference + greedy collapse
    -> HuBERT-CTC end-to-end recipe missing.
  * [20.0.4 (NEW)] (concept, slide 5021_Audio_Encoders) Wav2Vec vs HuBERT contrast: contrastive loss vs cross-entropy on cluster IDs
    -> The pedagogical contrast is the single most important learning outcome of the slide deck; not present.
  * [20.0.4 (NEW) or 20.5] (code_example, slide 5021_Audio_Encoders) Wav2Vec2Processor + Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-base-960h') transcription recipe
    -> Standard wav2vec 2 inference call missing.
  * [20.0.2 (NEW)] (concept, slide 5021_Audio_Encoders) Straight-Through Training (STT) estimator + EMA codebook updates
    -> STT estimator never described; only Gumbel approach hinted at. EMA discussed in 20.1 callout for EnCodec briefly.
  * [20.0.2 (NEW)] (figure, slide 5021_Audio_Encoders) EnCodec full system diagram: convolutional encoder + RVQ + decoder + discriminator with losses (l_w, l_l, l_d, l_g, l_a, l_t)
    -> Full system diagram missing.
  * [20.0.2 (NEW)] (code_example, slide 5021_Audio_Encoders) EncodecModel.from_pretrained('facebook/encodec_24khz') encode/decode example; 1s -> 75 frames x 128-D vec, 8 codebooks x 1024 entries
    -> Concrete EnCodec HF code missing; the 1s/75/128/8/1024 numbers anchor mental model.
  * [20.x.5 (NEW) or 20.0.3] (model, slide 5021_MultimodalAudio) CLAP: Contrastive Language-Audio Pretraining; CNN audio encoder + BERT text encoder
    -> Section 20.3 references CLAP only in passing as 'text-music joint embedding (MuLan)'. Stand-alone CLAP coverage missing.
  * [20.x.5 (NEW)] (concept, slide 5021_MultimodalAudio) InfoNCE symmetric loss L = -1/N sum_i [log(exp(sim(a_i,t_i)/tau)/sum_j ...) + text-to-audio direction]
    -> Formal InfoNCE loss for audio missing.
  * [20.x.5 (NEW)] (concept, slide 5021_MultimodalAudio) Variable-length audio: 3 random 10s chunks + downsampled global rep, attention feature fusion
    -> Chunk-and-fuse trick missing.
  * [20.x.5 (NEW)] (concept, slide 5021_MultimodalAudio) Caption vs keyword text handling: T5-based keyword-to-sentence augmentation
    -> Important data engineering detail missing.
  * [20.x.5 (NEW)] (code_example, slide 5021_MultimodalAudio) HF pipeline('zero-shot-audio-classification', model='laion/clap-htsat-unfused') with candidate_labels
    -> Zero-shot audio classification recipe missing.
  * [20.x.5 (NEW)] (concept, slide 5031_Audio_Classification) AST recipe as classifier: any transformer + classification head + cross-entropy
    -> Pedagogical bridge from AST to general classification fine-tuning missing.
  * [20.x.5 (NEW)] (model, slide 5031_Audio_Classification) anton-l/xtreme_s_xlsr_300m_minds14 intent classifier (XLS-R based)
    -> XLS-R intent classifier model card absent.
  * [20.x.5 (NEW) or 20.5.6] (model, slide 5031_Audio_Classification) sanchit-gandhi/whisper-medium-fleurs-lang-id LangID classifier
    -> Whisper-as-LangID-classifier missing.
  * [20.x.5 (NEW)] (concept, slide 5031_Audio_Classification) GTZAN music-genre dataset (marsyas/gtzan, 999 records, train_test_split)
    -> Canonical genre-classification dataset absent.
  * [20.x.5 (NEW)] (model, slide 5031_Audio_Classification) DistilHuBERT (ntu-spml/distilhubert) as fine-tuning base
    -> DistilHuBERT not mentioned; ideal smaller-model base for the fine-tuning lab.
  * [20.x.5 (NEW)] (code_example, slide 5031_Audio_Classification) AutoFeatureExtractor + AutoModelForAudioClassification + TrainingArguments + Trainer fine-tuning loop with compute_metrics=accuracy
    -> Full HF audio fine-tuning recipe missing from Chapter 20. The plan calls for an end-to-end lab; this slide deck provides it verbatim.
  * [20.5] (concept, slide 5041_Audio_Speech2Text) Whisper multitask training format graph: SOT -> Language tag -> Transcribe/Translate/NoSpeech -> Timestamps/Text-only -> EOT
    -> The directed graph of special tokens is the single most pedagogically valuable Whisper artifact and is absent.
  * [20.5] (code_example, slide 5041_Audio_Speech2Text) Lower-level WhisperProcessor + generate + batch_decode(skip_special_tokens=False) showing control tokens
    -> 20.5 uses high-level faster-whisper API; the bare HF interaction with visible control tokens is missing.
  * [20.5] (code_example, slide 5041_Audio_Speech2Text) Multilingual ASR via generate_kwargs={'task': 'transcribe', 'language': 'fr'}
    -> Language-switching code pattern missing.
  * [20.5] (concept, slide 5041_Audio_Speech2Text) Whisper output format: chunks list of (text, timestamp) pairs + concatenated text
    -> Output schema with timestamps not shown.
  * [20.5] (code_example, slide 5041_Audio_Speech2Text) Seq2SeqTrainingArguments + Seq2SeqTrainer Whisper fine-tuning recipe (output_dir, lr_scheduler_type, fp16, generation_max_length, metric_for_best_model='wer')
    -> Whisper fine-tuning recipe missing. Plan should add the canonical Common Voice fine-tune.

## Family F (chapters 26, 27, 28, 30)
- Items: 33 | Present: 7 | Partial: 13 | Missing: 13
- Top must-add items:
  1. F-1424-01: Create NEW Section 30.2.5 'LangGraph Tutorial: From Chain to ReAct Agent' that mirrors the 1424 slide deck end-to-end (state+reducer, chain graph, tools_condition router, full ReAct agent, checkpoints+threads, streaming modes, HITL interrupt, LangGraph Studio). This is the single biggest pedagogical gap in family F
  2. F-1422-02 + F-1422-03: Refresh MCP section 27.2 to FOUR primitives (add Sampling) and the controller-taxonomy table (model-controlled / app-controlled / user-controlled / server-initiated). Spec-currency fix
  3. F-1421-04 + F-1421-05: Add Toolformer and ToolkenGPT body coverage in 27.1.3 (self-supervised tool training with loss-reduction filter; vocabulary extension with frozen LM). Both are bibliography-only today
  4. F-1428-01 + F-1428-03: Add ReWoo (single-pass plan with variables) and Baby-AGI (historical anchor) to 26.2. ReWoo plugs a real algorithmic gap in the planning section; Baby-AGI provides historical grounding
  5. F-1426-02: Add a worked RefleXion example in 26.2.3 with Responder+Revisor pair, structured JSON output, and tool-augmented citations. Today only the citation exists
- ALL missing items (11):
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?

## Family G (chapters 31, 32, 33, 35)
- Items: 56 | Present: 31 | Partial: 8 | Missing: 17
- Top must-add items:
  1. {'id': 'G-012', 'title': 'RAPTOR (recursive cluster-and-summarize tree retrieval)', 'where': 'section-32.2.html or section-31.7.html', 'why': "Slide 1401 dedicates 3 slides to RAPTOR by name (Sarthi et al. ICLR 2024); the book has generic hierarchical indexing but never names or describes RAPTOR's recursive embed-cluster-summarize-recurse algorithm or tree traversal retrieval."}
  2. {'id': 'G-053', 'title': 'CLAP (Contrastive Language-Audio Pretraining) body coverage in Section 33.1', 'where': "section-33.1.html (new 33.1.7 'Audio-text joint embeddings: CLAP')", 'why': "Task brief specifically asks 'is audio-text joint embedding (CLAP, AudioCLIP) present in Section 33.1?' Answer: only table+bib mention; no architecture, no symmetric InfoNCE math, no chunk-and-fuse audio encoder, no T5 keyword augmentation, no zero-shot HF code. Slide deck 5021_MM is 5 slides entirely about this topic."}
  3. {'id': 'G-042', 'title': 'RAFT (Retrieval-Augmented Fine-Tuning) with distractor-aware CoT training', 'where': 'section-35.2.html or section-35.5.html (new RAFT subsection)', 'why': "Slide 1404 dedicates an entire 'pillar 5: generator fine-tuning' to RAFT (Zhang et al. 2024) covering QA-from-docs generation, distractor mixing, CoT answer prompt, LlamaIndex RAFT dataset prep. Entire technique missing from book. Naturally extends Ch 16 fine-tuning."}
  4. {'id': 'G-034', 'title': 'MMR (Maximal Marginal Relevance) for diverse retrieval AND topic keywords', 'where': 'section-35.2.html (retrieval) and section-31.7.html (BERTopic keywords)', 'why': "MMR is referenced in two separate slide decks (1404 advanced RAG, 1411 BERTopic) and is a canonical algorithm with one-line LangChain support (as_retriever(search_type='mmr')). Currently 0 hits across Part 7. High value-to-effort ratio."}
  5. {'id': 'G-043', 'title': 'Cache-Augmented Generation (CAG) as the production middle ground between RAG and long context', 'where': 'section-32.2.html (32.2.3 RAG vs Long Context)', 'why': "Slide 1404 closes with CAG as a named pattern (preload KV cache, cross-attend). Bridges naturally with the existing 'RAG vs Long Context' comparison table; Gemini context caching is the production realization the book should connect to."}
- ALL missing items (16):
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?

## Family H (chapters A, 0.1, 0.2, 1.1)
- Items: 40 | Present: 22 | Partial: 9 | Missing: 9
- Top must-add items:
  1. {'id': 'H-17', 'title': 'Joint Gaussian conditioning identity (mean shift + Schur complement) in Appendix A.2', 'why': 'Required for principled treatment of VAE posterior, diffusion forward/reverse process, Gaussian-process retrieval, and linear MMSE; currently absent everywhere in the book. Half-page subsection in A.2 with forward pointer to multimodal/diffusion chapters.'}
  2. {'id': 'H-29', 'title': 'Expand Section 1.1 NLP task taxonomy from 9 to 19 task families', 'why': 'Slide 1012 catalogues 19 task families; current Table 1.1.1 covers 9. Missing: Topic Modeling, Text Similarity, Dialog Systems, Normalization, Relation Extraction, Code Generation, Style Transfer, Knowledge-Augmented Generation (RAG), Simplification, Multimodal Generation, Emotion Recognition, Role Playing. Several of these (RAG, Code Gen, Style Transfer) are major LLM applications and deserve early enumeration even if covered in depth later.'}
  3. {'id': 'H-25', 'title': 'Introduce AdamW and the SGD -> Momentum -> Adagrad -> RMSprop -> Adam -> AdamW genealogy in Section 0.2.5', 'why': 'AdamW is the de facto LLM optimizer but is only mentioned in passing in 0.1 ex 1.3 and 0.2; full coverage waits until 6.5, which is far downstream. A short table in 0.2.5 plus a 3-line code example would let early readers reason about optimizer choices.'}
  4. {'id': 'H-33', 'title': 'Add MLE framing of cross-entropy LM training in A.6.2.2', 'why': "The identity 'minimizing cross-entropy on training tokens equals maximizing log-likelihood under the model' is a 2-sentence add but anchors the connection between probability theory and the actual training objective. Readers who studied stats first expect to see this."}
  5. {'id': 'H-16', 'title': 'Add multivariate Gaussian density and N(mu, Sigma) notation to Appendix A.2', 'why': 'Section A.2 lists Gaussian as a distribution but never writes the multivariate density or the (mu, Sigma) parameterization that subsequent chapters use freely (weight init analysis, diffusion noise, VAE prior). One short subsection with the density and Sigma = A A^T construction would unblock several downstream chapters.'}
- ALL missing items (9):
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?
  * [?] (?, slide ?) ?


## OVERALL

- Total items: 405
- Present: 141 (34.8%)
- Partial: 101 (24.9%)
- Missing: 163 (40.2%)
