# 5031_Audio_Classification — Per-Slide Summary

**Source file:** `5031_Audio_Classification.pptx`
**Source folder:** `SlidesPool/5030_Audio_Classifiers/`
**Drive link:** https://drive.google.com/file/d/1AQUwUq6I2k2eLi7sZk85ncU9QqA_UX1O/view
**Slide count (exact, via python-pptx):** 13
**Extraction:** Local parse + slide PNG render. HuggingFace code screenshots and the AST architecture diagram were visually inspected.

---

## Slide 1 — Audio Classification
Title slide for the chapter on audio classification with pretrained transformers.

## Slide 2 — Audio Spectrogram Transformer
AST treats the spectrogram as an image, slicing it into partially overlapped 16x16 patches, embedding them, and feeding the sequence to an encoder-only transformer. Any transformer becomes a classifier by adding a classification head and training with cross-entropy loss. The architecture diagram echoes the one from the audio-transformers deck so the reader recognizes the building block.

## Slide 3 — Pretrained Models for Audio Classification
Section divider before three off-the-shelf classification examples.

## Slide 4 — Keyword Spotting
Keyword spotting (KWS) identifies a small, closed vocabulary like "stop", "play", or "Hello Google", which is simpler than full ASR. The Speech Commands dataset is loaded via `load_dataset("speech_commands", "v0.02", split="validation", streaming=True)`. The HuggingFace pipeline `audio-classification` with model `MIT/ast-finetuned-speech-commands-v2` returns top predictions like 0.999 for "backward" and smaller probabilities for "happy", "follow", "stop", "up".

## Slide 5 — Pretrained Audio Classification
For intent classification on MINDS-14, the recipe loads `load_dataset("PolyAI/minds14", name="en-AU", split="train")` and applies `pipeline("audio-classification", model="anton-l/xtreme_s_xlsr_300m_minds14")`. The visible output assigns 0.963 to "pay_bill" with much smaller mass on "freeze", "card_issues", "abroad", and "high_value_payment".

## Slide 6 — Language Identification
Language identification on FLEURS (Google's low-resource benchmark) labels each clip with a language. The pipeline uses `model="sanchit-gandhi/whisper-medium-fleurs-lang-id"` on a sample from `google/fleurs`. The example output assigns 0.999 to "Afrikaans" with much smaller probabilities on "Northern-Sotho", "Icelandic", "Danish", "Cantonese Chinese".

## Slide 7 — Zero-Shot Classification
Section divider before CLAP-based zero-shot audio classification.

## Slide 8 — CLAP
A reminder slide that CLAP (Contrastive Language-Audio Pretraining) projects audio and text into a shared embedding space so that unseen classes can be classified by their textual descriptions, exactly like CLIP for images.

## Slide 9 — Zero-Shot Audio Classification
Code shows the `task="zero-shot-audio-classification"` pipeline with `model="laion/clap-htsat-unfused"` and `candidate_labels=["Sound of a dog", "Sound of vacuum cleaner"]`. On a sample from `ashraq/esc50` the classifier returns the dog label with the higher similarity score, demonstrating that classification of previously unseen classes works without any task-specific fine-tuning.

## Slide 10 — Fine-Tuning Models
Section divider introducing music-genre classification on GTZAN as the fine-tuning example.

## Slide 11 — GTZAN Dataset
The classic GTZAN music-genre dataset is loaded via `load_dataset("marsyas/gtzan", "all")`, returning 999 records with features file, audio, genre. The dataset is split with `gtzan["train"].train_test_split(seed=42, shuffle=True, test_size=0.1)` to give 899 training and 100 test items. Genre integers map to names through `gtzan["train"].features["genre"].int2str`, returning labels like "pop".

## Slide 12 — Base model and feature extractor
The fine-tuning starts from DistilHuBERT (`model_id = "ntu-spml/distilhubert"`). An `AutoFeatureExtractor.from_pretrained(model_id, do_normalize=True, return_attention_mask=True)` handles preprocessing; `AutoModelForAudioClassification.from_pretrained(model_id, num_labels=num_labels, label2id=label2id, id2label=id2label)` adds the classification head. A `preprocess_function` runs the feature extractor on each batch with truncation and a max length of feature_extractor.sampling_rate * max_duration.

## Slide 13 — Training Arguments and Trainer
Standard HuggingFace `TrainingArguments` set output_dir, eval_strategy=epoch, learning_rate, per_device_train/eval_batch_size, gradient_accumulation_steps, num_train_epochs, warmup_ratio, logging_steps, metric_for_best_model="accuracy", and push_to_hub=True. A `compute_metrics` callback uses `evaluate.load("accuracy")` on argmaxed predictions. `Trainer(model, training_args, train_dataset=gtzan_encoded["train"], eval_dataset=gtzan_encoded["test"], tokenizer=feature_extractor, compute_metrics=compute_metrics)` and `trainer.train()` finish the fine-tune.

---

## Deck-level takeaway
The deck is the practical "how to classify audio with HuggingFace" walkthrough that brings together AST, wav2vec2/XLS-R, Whisper, CLAP, and HuBERT under one consistent API. The first half (slides 1 to 9) demonstrates that for many tasks (keyword spotting, intent classification, language ID, zero-shot recognition) the right model already exists on the Hub and the `audio-classification` or `zero-shot-audio-classification` pipeline is a three-line call. The second half (slides 10 to 13) shows the canonical fine-tuning loop for the case where no exact pretrained model exists: load a dataset, instantiate a feature extractor plus `AutoModelForAudioClassification`, write a preprocess function, and let the standard `Trainer` do the rest. The unifying message is that audio classification has been commoditized: the reader's job is to choose a backbone (AST for events, wav2vec2 for speech, CLAP for zero-shot, HuBERT/DistilHuBERT for fine-tuning) and let the HuggingFace ecosystem handle preprocessing, training, and evaluation.
