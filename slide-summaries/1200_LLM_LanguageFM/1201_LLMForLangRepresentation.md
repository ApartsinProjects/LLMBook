# 1201_LLMForLangRepresentation — Per-Slide Summary

**Source file:** `1201_LLMForLangRepresentation.pptx`
**Source folder:** `SlidesPool/1200_LLM_LanguageFM/`
**Drive link:** https://drive.google.com/file/d/1n0ozo6ZnRICLlqALneD--ZC_8BFPO2cY/view
**Slide count (exact, via python-pptx):** 21
**Extraction:** Local parse + slide PNG render. Body text and the inline domain-models table carry the bulk of the conceptual content.

---

## Slide 1 — Text Representation with LLMs
Title slide announcing that the deck covers LLM-based text representation and reviews the surrounding interfaces and libraries (Ollama, HuggingFace, Azure, OpenAI).

## Slide 2 — LLM-based Sentence Embedding
LLM-based sentence embeddings capture the semantics of a whole sentence or text fragment, including context, order, and meaning. The dense vectors range from 300 to 8000 dimensions depending on the model and are produced by LLMs pretrained on the entire internet plus specialized datasets. The slide gives only a taste of what embeddings do and how they are used; internals come later. A key limitation is that embeddings are still suitable only for relatively short text (up to ~500 tokens); compressing a whole book into one vector is impractical.

## Slide 3 — Closed vs. Open LLMs
Contrasts two access patterns: a downloaded local HuggingFace transformer model versus cloud calls to OpenAI or Microsoft Azure via API or Python libraries.

## Slide 4 — OpenAI library and interface
The OpenAI Python library wraps the REST/HTTP interface and is used to access OpenAI plus other hosted models that share the same protocol.

## Slide 5 — Ollama
Ollama hosts open-source models locally on the user's PC and can be driven through the ollama Python library. Crucially, its API is OpenAI-compatible, so the same client library works against either backend. Large models still require generous GPU memory.

## Slide 6 — Sentence Embedding with Ollama
Code screenshot showing how to call the Ollama embeddings endpoint to produce sentence embeddings locally.

## Slide 7 — HF: Representation models with encoder
HuggingFace encoder representation models produce a vector for a short text (typically up to 512 tokens).

## Slide 8 — Azure Foundry
Azure Foundry hosts many models including OpenAI's. Students can register with their student email to receive a $100 free credit.

## Slide 9 — Attaching the classification head to the representation model
The classification stack: input text goes through an LLM representation model (a sentence transformer), then a classification head (logistic regression, SVM, or deep learning), producing a class label. The pretrained embedding serves as the feature vector for the downstream classifier.

## Slide 10 — TwitterEval: Twitter Sentiment Dataset
Introduces the TwitterEval running dataset for sentiment-related experiments.

## Slide 11 — Example: HF twitter sentiment classifier model
Loads a pretrained HF model trained on Twitter data and asks whether it can transfer to Facebook posts or Wikipedia comments. The setup keeps the pretrained representation and classification heads fixed.

## Slide 12 — Inference using Pipelines on Movie Reviews
A pipeline consisting of tokenization and encoding, the transformer representation model, and the logistic classification head returns a list of class labels. The cross-domain experiment trains on TwitterEval and infers on the Movie Review dataset, with the model's three sentiment classes mapped down to the two labels in movie reviews.

## Slide 13 — Classification Report
Five screenshots showing precision, recall, F1, and confusion-matrix metrics produced by sklearn's classification_report on the cross-domain experiment.

## Slide 14 — Training classification head
Section divider for the next subsection on actually training a classification head on the LLM representation.

## Slide 15 — Logistic Regression Classification Head
Four code screenshots showing how to extract LLM embeddings, fit a sklearn LogisticRegression on them, and evaluate on a held-out split.

## Slide 16 — Zero-shot classification
Zero-shot classification assumes no training data and that the class label has semantic meaning ("sport"). The text is embedded along with each class label, and the closest label in embedding space wins. An improvement is to enrich each label with a longer descriptive sentence before embedding ("activities rooted in sport, emphasizing physical skill, competition, teamwork, and personal achievement").

## Slide 17 — Example: Movie Review Sentiment Analysis
Four screenshots applying the zero-shot label-similarity recipe to the movie-review sentiment task.

## Slide 18 — More on classification in the following sections
Previews upcoming material: leveraging text generation models for classification; fine-tuning representation and generation LLMs; how representation and generation models are built and trained; and how to represent long texts.

## Slide 19 — Domain-specific Text Representation Models
A seven-row table of domain-specialized encoders: PubMedBERT (biomedical, trained from scratch on PubMed); ChemBERTa (chemistry, RoBERTa-base over SMILES); FinBERT (finance, BERT-base fine-tuned on financial texts); LegalBERT (legal, BERT-base on contracts and rulings); SciBERT (science, trained from scratch on Semantic Scholar); CodeBERT (computer science, RoBERTa-base on source code and natural language); XBioBERT (multilingual biomed, XLM-R/mBERT adaptation).

## Slide 20 — Multimodal Representation Models
Introduces multimodal representation models with a single illustrative diagram bridging text and image embeddings.

## Slide 21 — Vision Language Models: Zero-Shot Classification
CLIP represents images and text in a shared semantic space as vectors. Zero-shot image classification computes cosine distance between an image representation and each candidate class-label representation, picking the closest.

---

## Deck-level takeaway
The deck introduces LLM-based dense sentence embeddings as the modern alternative to TF-IDF and word-level features, then shows how to consume them through three interchangeable interfaces: the OpenAI library against either OpenAI or local Ollama, and the HuggingFace transformers library locally. With embeddings as feature vectors, three downstream patterns are illustrated: a frozen encoder plus a fine-tunable classification head, a pretrained-but-out-of-domain classifier pipeline applied cross-domain, and label-similarity zero-shot classification (extended via descriptive label expansion). The deck closes with a catalog of domain-specialized encoders (medicine, chemistry, finance, legal, science, code, multilingual biomed) and a multimodal extension showing CLIP doing zero-shot image classification via text-image cosine similarity in a shared embedding space.
