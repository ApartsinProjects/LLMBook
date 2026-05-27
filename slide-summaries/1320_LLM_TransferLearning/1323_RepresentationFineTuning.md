# 1323_RepresentationFineTuning — Per-Slide Summary

**Source file:** `1323_RepresentationFineTuning.pptx`
**Source folder:** `SlidesPool/1320_LLM_TransferLearning/`
**Drive link:** https://drive.google.com/file/d/1iBrpEM3REGhpW5KGlQyBM_-lIBC3bItm/view
**Slide count (exact, via python-pptx):** 36
**Extraction:** Local parse + slide PNG render. Body bullets carry the conceptual content for four representation fine-tuning recipes.

---

## Slide 1 — Domain adaptation of representation models
Title slide announcing how to create sentence-embedding models tailored to your own data.

## Slide 2 — Reminder
Reminds the reader that BERT uses MLM plus NSP pretraining (NSP on sentence pairs, MLM on both single sentences and pairs), uses [CLS] ... [SEP] for single sentences, takes the [CLS] token as the sentence embedding, and operates as a cross-encoder.

## Slide 3 — Reminder: SBERT
Reminder of SBERT's siamese / bi-encoder architecture trained on NLI with tied weights, where each tower receives a single sentence and similar sentences cluster together.

## Slide 4 — Motivation
The goal is to fine-tune sentence representations to capture the specifics of a target domain (chemistry, medicine). Labeled sentence-pair data is hard to obtain, while unlabeled domain pairs are easy by sampling the corpus. Two regimes follow: semi-supervised fine-tuning when a small portion is labeled, and unsupervised fine-tuning when no labels exist.

## Slide 5 — 1. Finetuning with bootstrapping
Section divider for semi-supervised fine-tuning.

## Slide 6 — Assumptions
Assume a small domain-specific labeled "gold" sentence-pair dataset with binary similarity labels, plus a large corpus of unlabeled individual sentences.

## Slide 7 — Bootstrapping
The recipe: fine-tune a generic cross-encoder BERT on the gold dataset to predict similarity. Use it to sample and label a "silver" dataset from the unlabeled corpus, then train SBERT (siamese / bi-encoder) on the silver dataset.

## Slide 8 — Generation of balanced silver dataset
Naive random pair sampling produces mostly "unrelated" pairs once labeled. Instead, embed all candidates with the gold-tuned BERT and, for each sample, pair it with its 10 closest candidates, then label those pairs with the gold-tuned BERT.

## Slide 9 — Implementation
Section divider for the implementation walkthrough.

## Slide 10 — Simulating Gold Dataset
Two screenshots showing how to simulate a gold dataset using 10K MNLI rows, mapping contradiction or neutral to 0 (unrelated) and entailment to 1 (related).

## Slide 11 — Prepare the silver dataset
Three screenshots: fine-tune BERT on the gold dataset, create the silver dataset by nearest-neighbor sampling, and label the silver pairs with the gold-tuned BERT.

## Slide 12 — Fine-tune using silver dataset
Five screenshots training SBERT on the silver dataset with cosine-similarity contrastive loss.

## Slide 13 — 2. Finetuning with Sequential Denoising Autoencoder (SDAE)
Section divider for SDAE, which requires no labels at all.

## Slide 14 — Assumption
Assume no labeled data and a large domain corpus. A good representation should allow robust reconstruction: drop some tokens (not mask), encode the noisy sentence, and reconstruct the complete sentence. Unlike MLM, reconstruction starts from the sentence embedding rather than from each token's embedding.

## Slide 15 — Denoising autoencoder
Attach a transformer-based decoder with cross-attention to the sentence representation; discard it after training. The loss is masked token reconstruction at the decoder output.

## Slide 16 — Preparing noisy dataset
Code screenshot showing how to drop tokens from sentences to form the noisy training inputs.

## Slide 17 — Create Evaluator
Code screenshot showing an evaluator that, when called, receives the model and returns a score.

## Slide 18 — Prepare encoder/decoder
Two screenshots: the decoder is included in the DenoisingAutoEncoderLoss (the loss carries trainable weights), the encoder is BERT plus [CLS] pooling, and the SentenceTransformer object is composed from individual modules. The training loss scores how well the pristine input sequence appears in the predicted output.

## Slide 19 — Training
Two screenshots running the SDAE training loop.

## Slide 20 — 3. Simple Contrastive Sentence Embeddings (SimCSE)
Section divider for SimCSE.

## Slide 21 — Smart way to generate positive/negative pairs
Inject random noise into the processing (via dropout). Two passes of the same sentence with different dropout masks should produce similar embeddings (positive pair). Two different sentences should produce dissimilar embeddings (negative pair).

## Slide 22 — Reminder: Dropout
Dropout randomly disables activations per sample. Different dropout configurations on the same sentence should still yield similar representations.

## Slide 23 — BERT Encoder: Dropout layers
BERT's dropout sits after the token-and-position embedding, after each self-attention (before adding to the residual), and after each feed-forward (before adding to the residual).

## Slide 24 — SimCSE: Simple Contrastive Sentence Embeddings
SimCSE generates a positive pair by passing the same sentence through BERT with different dropout masks and forms negative pairs from different sentences.

## Slide 25 — Contrastive loss with implicit negative pairs
The built-in sentence-transformers loss accepts only positive pairs and treats all other in-batch combinations as negatives.

## Slide 26 — Training SimCSE
Code screenshot training SimCSE: each sentence is duplicated in the batch and different dropout is applied to the two copies.

## Slide 27 — Continued Pretraining with Masked Language Modeling
Section divider for the fourth recipe: continued MLM pretraining on domain data.

## Slide 28 — Reminder
BERT has MLM and NSP losses. Continual pretraining trains with MLM on domain-specific data and combines with later supervised fine-tuning.

## Slide 29 — Fine-tuning: 2 steps
Two figures contrasting the two regimes: MLM pretraining on a generic dataset then classification fine-tuning on domain data, versus MLM pretraining on a generic dataset, then MLM fine-tuning (self-supervised) on domain data, then classification fine-tuning.

## Slide 30 — Organizational finetuning workflow
The organizational workflow starts from generic BERT (trained on all web data), continues pretraining on corporate data to adapt to the business domain, then fine-tunes per application (semantic search, customer service).

## Slide 31 — Type of masking
Token masking is used here (the figure surveys other masking variants in passing).

## Slide 32 — (no title)
Six code screenshots showing the data collator with token masking and saving a copy under the mlm name.

## Slide 33 — Evaluate on MLM task
Two screenshots evaluating MLM perplexity on the web corpus and after continued pretraining on movie reviews.

## Slide 34 — Summary
Section header for the closing summary.

## Slide 35 — DAPT: Domain-Adaptive Pretraining
DAPT (Domain-Adaptive Pretraining) is the formal name for continuing MLM training on a domain corpus.

## Slide 36 — TAPT: Task-Specific Pretraining
TAPT (Task-Adaptive Pretraining) does task-specific MLM-style or supervised fine-tuning for a specific task, typically after DAPT.

---

## Deck-level takeaway
The deck covers four ways to adapt sentence-embedding models to a specific domain. (1) Semi-supervised bootstrapping: fine-tune a cross-encoder on a small gold pair dataset, use it to label a smartly sampled "silver" dataset from the unlabeled corpus, then train SBERT on the silver data with contrastive loss. (2) Sequential Denoising Autoencoder: drop tokens from sentences and force the encoder to recover the original from the sentence-level embedding (no labels needed). (3) SimCSE: exploit dropout noise as data augmentation, treating two dropout-masked passes of the same sentence as a positive pair and other in-batch sentences as implicit negatives. (4) Continued MLM pretraining (DAPT) on domain data followed by task-adaptive pretraining (TAPT), the standard workflow for adapting BERT to a corporate corpus before per-application fine-tuning.
