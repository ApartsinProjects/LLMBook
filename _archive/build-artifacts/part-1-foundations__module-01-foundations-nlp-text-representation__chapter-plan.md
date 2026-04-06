# Chapter Plan: Module 01, Foundations of NLP & Text Representation

## Scope

**What this chapter covers:**
This chapter traces the entire evolution of text representation, from raw text to contextual embeddings. It answers the central question: how do we turn human language into numbers that machines can process? The chapter moves from the simplest approaches (counting words) through dense vector embeddings (Word2Vec, GloVe, FastText) to contextual representations (ELMo), establishing the conceptual and practical foundation for the transformer-based models covered in later modules.

**What this chapter explicitly does NOT cover:**
- Tokenization algorithms (BPE, WordPiece, SentencePiece) are deferred to Module 02
- Attention mechanisms are deferred to Module 03
- Transformer architecture is deferred to Module 04
- Sentence-level embeddings (Sentence-BERT, etc.) belong to later modules
- Fine-tuning pre-trained models in depth (mentioned conceptually here, detailed later)
- Production deployment of embedding pipelines

## Learning Objectives

1. Describe the four eras of NLP (rule-based, statistical, neural, LLM) and explain why each transition happened
2. Identify the six core NLP tasks and their input/output structure
3. Build a complete text preprocessing pipeline using both NLTK and spaCy
4. Implement and compare Bag-of-Words, TF-IDF, and one-hot encoding; articulate their limitations
5. Explain the distributional hypothesis and how Word2Vec, GloVe, and FastText create dense word representations
6. Train a Word2Vec model from scratch and explore word analogies via vector arithmetic
7. Compute cosine similarity and explain why it is preferred over Euclidean distance for embeddings
8. Explain why static embeddings fail for polysemous words and how ELMo introduced contextual embeddings
9. Articulate the "pre-train, then fine-tune" paradigm and trace the path from ELMo to transformers

## Prerequisites

From Module 00 (ML & PyTorch Foundations):
- Neural network basics: forward pass, loss functions, gradient descent, backpropagation
- PyTorch fundamentals: tensors, autograd, building simple models
- Python proficiency: functions, classes, list comprehensions, f-strings
- Basic linear algebra: vectors, dot products, matrix multiplication
- Familiarity with NumPy and basic scikit-learn usage

## Chapter Structure

### Section 1.1: Introduction to NLP & the LLM Revolution (~2,500 words)

**Role:** Motivational overview and historical framing. Sets the stage for the entire module by explaining why representation quality is the central theme of NLP history.

**Key concepts:**
- The four eras of NLP: rule-based, statistical, neural, LLM
- The six core NLP tasks: classification, NER, sentiment, translation, summarization, QA
- Why language is hard: ambiguity, coreference, compositionality, world knowledge, pragmatics
- Layers of language complexity: morphology, syntax, semantics, pragmatics
- The "representation thread" connecting all four eras

**Diagrams present:**
- Four Eras timeline (SVG with era boxes and representation labels)
- Task categories: Understanding vs. Generation (SVG)
- Concentric layers of language difficulty (SVG ellipses)

**Code examples:** None (conceptual section)

**Exercises:** 1 inline quick-check (match-the-era quiz with reveal)

**Callouts present:** 3 (The Big Picture insight, Key Insight on representations, Warning on why this matters for the course)

**Pedagogical assessment:** Strong opening section. The thought experiment opening is engaging. The four-eras framework provides a clear mental model. The representation thread table at the end ties everything together effectively.

**Potential improvements:**
- Could benefit from a brief "what you will build in this chapter" preview at the very end to set expectations
- The connection to Module 00 prerequisites is implicit; a brief bridge sentence referencing neural networks from Module 00 would smooth the transition

---

### Section 1.2: Text Preprocessing & Classical Representations (~3,500 words)

**Role:** First hands-on section. Transitions from conceptual overview to practical implementation. Covers the entire classical NLP pipeline from raw text to sparse feature vectors.

**Key concepts:**
- The text preprocessing pipeline: Unicode normalization, lowercasing, tokenization, stop word removal, stemming vs. lemmatization
- Bag-of-Words: vocabulary construction, document-term matrix, sparsity
- N-grams: partial word-order solution, vocabulary explosion tradeoff
- TF-IDF: term frequency, inverse document frequency, worked example
- One-hot encoding and its limitations (every word equidistant)
- The three fatal flaws of sparse representations (no word order, no semantics, massive dimensionality)

**Diagrams present:**
- Preprocessing pipeline flow (SVG: Raw Text through Features)
- Stemming vs. Lemmatization side-by-side comparison (SVG)
- BoW matrix heatmap (SVG showing sparse document-term matrix)
- TF-IDF bar chart for Document 3 (SVG)

**Code examples:**
1. Full preprocessing pipeline with NLTK (preprocess function)
2. Same pipeline using spaCy (preprocess_spacy function, plus NER bonus)
3. Bag-of-Words with scikit-learn CountVectorizer
4. Bigram CountVectorizer (n-grams)
5. TF-IDF with scikit-learn TfidfVectorizer
6. One-hot encoding with scikit-learn

**Exercises:** Inline "Try It Yourself" prompt for preprocessing exploration

**Callouts present:**
- "The Big Picture" (preprocessing is about reducing noise while preserving signal)
- "Modern vs. Classical Preprocessing" (LLMs vs. classical pipelines)
- "Checkpoint: What Can We Do So Far?" (capabilities and limitations summary)
- "Mental Model: The Filing Cabinet vs. the Color Mixer" (analogy bridging to embeddings)

**Pedagogical assessment:** Well-structured progression from raw text through increasingly sophisticated representations. The worked examples (BoW matrix, TF-IDF calculation) are excellent. The spaCy/NLTK dual implementation is practical. The "filing cabinet vs. color mixer" analogy at the end is a strong bridge to Section 1.3.

**Potential improvements:**
- The section could explicitly note that the preprocessing pipeline shown here is for classical NLP; modern tokenizers (Module 02) replace most of it
- A summary table at the end comparing BoW, TF-IDF, and one-hot side by side would reinforce the progression

---

### Section 1.3: Word Embeddings: Word2Vec, GloVe & FastText (~4,000 words)

**Role:** Core technical section. Introduces the dense embedding revolution. The heaviest section in terms of both concepts and code, containing the module's most important hands-on labs.

**Key concepts:**
- The distributional hypothesis: "you shall know a word by the company it keeps"
- Word2Vec Skip-gram architecture: center word predicts context words
- CBOW vs. Skip-gram comparison
- Negative sampling: making training tractable
- Cosine similarity: geometric intuition (angle between vectors), why not Euclidean
- Word analogies: king minus man plus woman equals queen (vector arithmetic)
- Why analogies work: linear structure encoding semantic relationships
- GloVe: global co-occurrence matrix factorization, co-occurrence ratio insight
- FastText: subword n-gram decomposition, handling OOV words
- Comparing all three approaches (comparison table)
- Visualization with t-SNE and similarity heatmaps

**Diagrams present:**
- Skip-gram architecture (SVG showing center word to context predictions)
- Embedding matrix structure (SVG)
- Cosine similarity geometric intuition (SVG with king/queen/refrigerator vectors)
- FastText subword decomposition (SVG showing "running" split into n-grams)

**Code examples:**
1. Training Word2Vec from scratch with Gensim (corpus, training, exploration)
2. Cosine similarity implementation (manual with numpy)
3. Word analogy queries (king/queen, paris/berlin, walking/walked)
4. Loading pre-trained GloVe vectors
5. Training FastText model (with OOV word demonstration)
6. t-SNE visualization of word embeddings
7. Cosine similarity heatmap with seaborn

**Exercises:** None inline (exercises consolidated in Section 1.4)

**Callouts present:**
- "Why This Matters" (distributional hypothesis)
- "Mental Model: GPS Coordinates for Words"
- "CBOW vs. Skip-gram" (note)
- "Connection to Modern LLMs" (embedding layers in GPT-4/Claude)
- "Deep Insight: Why Analogies Work" (linear structure)
- "The Shared Limitation" (one vector per word)
- "Why Cosine, Not Euclidean Distance?"
- "Visualization Warning" (t-SNE is lossy)

**Key Takeaways box:** 5-point summary at section end

**Pedagogical assessment:** This is the strongest section in terms of depth and hands-on practice. The progression from distributional hypothesis through Skip-gram architecture to trained model to analogies is natural and compelling. The "Connection to Modern LLMs" callout is excellent for showing relevance. The three-way comparison table is a clear reference.

**Potential improvements:**
- The GloVe section is lighter than Word2Vec; the co-occurrence ratio table is good but a brief code example showing GloVe analogy performance alongside Word2Vec would strengthen the comparison
- The negative sampling math formula could use a plain-English walkthrough (partially present but could be expanded)
- Consider adding a brief note on embedding dimensions (why 300? empirical sweet spot)

---

### Section 1.4: Contextual Embeddings: ELMo & the Path to Transformers (~3,000 words)

**Role:** Capstone section. Identifies the fatal flaw of static embeddings (polysemy), introduces the solution (contextual embeddings via ELMo), and bridges to the transformer modules that follow.

**Key concepts:**
- The polysemy problem: "bank" in three contexts, "run" in four contexts
- ELMo architecture: bidirectional LSTMs, layer-wise representations
- Why different layers capture different information (lower: syntax, upper: semantics)
- The pre-train/fine-tune paradigm
- Contextual embeddings in practice (BERT code demonstration)
- Comparison table: Word2Vec/GloVe vs. ELMo vs. BERT/GPT
- The representation journey summary (full progression diagram)
- Forward references to Modules 2, 3, and 4

**Diagrams present:**
- Static vs. Contextual embeddings comparison (SVG)
- ELMo architecture (SVG showing bidirectional LSTM layers)
- Representation journey summary (SVG: BoW to TF-IDF to Word2Vec to ELMo to Transformers to LLMs)

**Code examples:**
1. Contextual embeddings extraction using BERT via Hugging Face (get_word_embedding function)
2. Demonstrating that "bank" gets different vectors in different contexts (cosine distance comparison)

**Exercises (consolidated for full module):**
- 5 conceptual questions (representation evolution, distributional hypothesis, static vs. contextual, why pre-train, TF-IDF vs. embeddings tradeoffs)
- 4 coding exercises (preprocessing exploration, analogy hunting, similarity exploration, Word2Vec from scratch in PyTorch)

**Further Reading table:** 6 entries (Word2Vec, GloVe, FastText, ELMo papers, Jay Alammar visual guide, Levy & Goldberg matrix factorization connection)

**"What You Built" summary box:** Lists 8 concrete artifacts built across the chapter

**Callouts present:**
- "Historical Context" (ELMo's impact on benchmarks)
- "The Paradigm Shift: Pre-train, Then Fine-tune"
- "Why We Used BERT Instead of ELMo"
- "The Thread That Connects Everything" (closing insight)

**Pedagogical assessment:** Effective capstone that ties the module together. The polysemy problem is well-motivated with concrete examples. The BERT code demonstration is practical (using what students would actually use, not the obsolete ELMo library). The exercises are well-calibrated across difficulty levels. The "What You Built" summary gives students a sense of accomplishment.

**Potential improvements:**
- The ELMo layer explanation (lower layers capture syntax, upper capture semantics) could include a concrete example showing different layer outputs for the same word
- The comparison table (Word2Vec vs. ELMo vs. BERT) is valuable but could note model sizes to give students a sense of scale
- The coding exercise "Word2Vec from scratch in PyTorch" is marked as a challenge but has no scaffolding; a hint or skeleton code reference would help intermediate students

---

## Terminology Standards

These terms should be used consistently throughout the chapter:

| Term | Usage |
|------|-------|
| NLP | Always expand on first use as "Natural Language Processing (NLP)"; thereafter use NLP |
| Embedding | A dense, learned vector representation of a word or token |
| Static embedding | An embedding that assigns one fixed vector per word (Word2Vec, GloVe, FastText) |
| Contextual embedding | An embedding where the same word gets different vectors depending on surrounding words (ELMo, BERT) |
| Sparse vector | A high-dimensional vector with mostly zero entries (BoW, TF-IDF, one-hot) |
| Dense vector | A compact vector where most or all entries are non-zero (word embeddings) |
| Polysemy | A single word having multiple unrelated meanings |
| Distributional hypothesis | The idea that words appearing in similar contexts have similar meanings |
| Cosine similarity | Similarity measure based on the angle between two vectors (range: -1 to 1) |
| Token | A unit of text after tokenization (word, subword, or character depending on method) |
| Pre-training | Training a model on a large unlabeled corpus to learn general language representations |
| Fine-tuning | Adapting a pre-trained model to a specific downstream task |
| OOV (out-of-vocabulary) | A word not seen during training; handled by FastText but not by Word2Vec or GloVe |
| Skip-gram | Word2Vec variant: predicts context words from a center word |
| CBOW | Word2Vec variant: predicts center word from surrounding context words |
| TF-IDF | Term Frequency, Inverse Document Frequency; weights words by distinctiveness |

## Cross-References

**Builds on:**
- Module 00, Section 0.1: Python and NumPy foundations (used in all code examples)
- Module 00, Section 0.2: Neural network basics (needed for understanding Word2Vec architecture, negative sampling loss)
- Module 00, Section 0.3: PyTorch fundamentals (used in the challenge exercise and contextual embedding code)

**Referenced by:**
- Module 02 (Tokenization & Subword Models): FastText's subword approach foreshadows BPE and WordPiece tokenizers; the preprocessing pipeline discussion sets up the question of "how should we split text?"
- Module 03 (Attention Mechanisms): The sequential processing limitation of ELMo/LSTMs motivates why attention was invented
- Module 04 (Transformer Architecture): The embedding layer in transformers is directly descended from Word2Vec; the pre-train/fine-tune paradigm introduced here is central to BERT and GPT
- Module 18 (Vector Databases): Cosine similarity and embedding search concepts from Section 1.3 are directly applied at scale
- Module 19 (RAG Systems): Dense retrieval relies on the same embedding and similarity concepts introduced here

## Content Quality Assessment

### Strengths
1. **Clear narrative arc:** The four-eras framework in Section 1.1 provides a mental model that the rest of the chapter fills in, culminating in the summary diagram in Section 1.4
2. **Strong hands-on content:** Seven distinct code examples across sections 1.2 and 1.3, all runnable and building on each other
3. **Excellent SVG diagrams:** Custom inline SVGs for every major concept (pipeline flows, matrix visualizations, vector space geometry, architecture diagrams)
4. **Effective callout system:** Consistent use of "note," "warning," "insight," and "key-idea" callouts to flag different types of information
5. **Good bridging between sections:** Each section ends by motivating the next (BoW limitations lead to embeddings; static embedding limitations lead to contextual embeddings)
6. **Practical tooling:** Shows both NLTK (for understanding) and spaCy (for production), and uses Gensim and Hugging Face (industry-standard libraries)

### Areas for Improvement
1. **Exercise distribution:** All exercises are concentrated at the end of Section 1.4. Sections 1.1, 1.2, and 1.3 have only inline quick-checks. Consider adding 1 to 2 short exercises at the end of each section.
2. **Missing explicit prerequisite bridge:** Section 1.1 does not reference Module 00 directly; a sentence acknowledging "you built neural networks in Module 00; now we apply them to language" would help returning students orient themselves.
3. **GloVe coverage is thin:** Compared to the detailed Skip-gram walkthrough, GloVe gets only a brief conceptual explanation and one code snippet. A short worked example of the co-occurrence matrix or the factorization objective would bring it closer to parity.
4. **No explicit "common mistakes" section:** Students commonly confuse stemming with lemmatization, mix up CBOW and Skip-gram, or misinterpret t-SNE distances. A short "common pitfalls" callout in each section would be valuable.
5. **Challenge exercise needs scaffolding:** The "Word2Vec from scratch in PyTorch" exercise is a great capstone but may be too open-ended for intermediate students. A link to a starter notebook or skeleton code would help.
6. **Missing quantitative context for ELMo section:** Mentioning approximate model sizes (ELMo: ~94M parameters, BERT-base: ~110M, GPT-3: 175B) would help students grasp the scale progression.

### Consistency Notes
- All four sections use the same CSS styling and callout classes
- Navigation links between sections are consistent (prev/up/next)
- The voice is consistently warm and conversational throughout
- No em dashes or double dashes detected in any section
- Mathematical notation uses inline HTML (not LaTeX/MathJax), which is consistent but limits expressiveness for more complex formulas in later modules

## Estimated Word Counts

| Section | Estimated Words | Status |
|---------|----------------|--------|
| 1.1: Introduction to NLP & the LLM Revolution | ~2,500 | Complete |
| 1.2: Text Preprocessing & Classical Representations | ~3,500 | Complete |
| 1.3: Word Embeddings: Word2Vec, GloVe & FastText | ~4,000 | Complete |
| 1.4: Contextual Embeddings: ELMo & the Path to Transformers | ~3,000 | Complete |
| **Total** | **~13,000** | Within target range (8,000 to 15,000) |
