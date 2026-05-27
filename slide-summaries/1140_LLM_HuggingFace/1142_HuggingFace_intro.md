# 1142_HuggingFace_intro — Per-Slide Summary

**Source file:** `1142_HuggingFace_intro.pptx`
**Source folder:** `SlidesPool/1140_LLM_HuggingFace/`
**Drive link:** https://drive.google.com/file/d/1h2o10jgHkVTuwrtDtxc70nO-CQpfdX2X/view
**Slide count (exact, via python-pptx):** 20
**Extraction:** Local parse + slide PNG render. Slide 20 (Audio Generation) had no body or images in the parsed output, so its PNG was inspected and found to contain a code screenshot using AudioLDM2Pipeline.

---

## Slide 1 — Hugging Face
Title slide for the HuggingFace ecosystem tour.

## Slide 2 — What is HuggingFace
Defines HuggingFace as a hub of models and datasets (foundational and task-specific across language, vision, and text), a set of Python libraries (datasets, transformers, pipelines, training and fine-tuning, evaluation), and surrounding services (API endpoints, app hosting).

## Slide 3 — Datasets
Section divider introducing the datasets library and ecosystem.

## Slide 4 — HF Dataset Card
Screenshot of a dataset card on the HF hub showing title, description, splits, columns, license, and citation.

## Slide 5 — HF Dataset library
Code screenshots showing load_dataset usage to download and use a hosted dataset with split selection.

## Slide 6 — HF DatasetDict and Dataset Class
Defines DatasetDict as a dictionary of partitions, with each partition being a Dataset whose rows are feature sets. Four screenshots illustrate the class structure and basic row access.

## Slide 7 — Models
Section divider introducing the models hub.

## Slide 8 — Search Models By Type
Screenshot of the HF model search UI filtered by task and type (text classification, image classification, etc.).

## Slide 9 — HF Model Card
Screenshot of a model card showing description, intended use, training data, evaluation, license, and how-to-use snippets.

## Slide 10 — Transformers and sentence transformers library
Section divider introducing the transformers and sentence-transformers libraries.

## Slide 11 — AutoClasses
AutoClasses guess the model configuration and interface, so the user can load any checkpoint with AutoTokenizer, AutoModel, and AutoProcessor. The example uses ViT-base, where the processor resizes, crops, normalizes, and converts the image into tensors.

## Slide 12 — Specialized model class: Sentence Transformer
Screenshot showing the SentenceTransformer specialized class that returns sentence-level embeddings directly from raw text.

## Slide 13 — Pipelines
A text-generation pipeline is described conceptually: implement the loop of predict-next-token, decode, append to input, and repeat. The default model in the example is GPT-2.

## Slide 14 — Evaluation library
Section divider for the evaluation library.

## Slide 15 — HF evaluate
Screenshot of code using evaluate.load to fetch a metric (e.g., accuracy or BLEU) and compute it on predictions and references.

## Slide 16 — Training and fine-tuning
Section divider for training and fine-tuning APIs.

## Slide 17 — Using HF trainer
Code screenshot showing the standard Trainer setup: TrainingArguments, Trainer construction with model, args, datasets, and compute_metrics, then trainer.train().

## Slide 18 — Diffusers library
Section divider for the diffusers library covering image and audio generation.

## Slide 19 — Image Generation
Four screenshots showing the diffusers image-generation pipeline (StableDiffusionPipeline.from_pretrained, prompt input, generated image preview).

## Slide 20 — Audio Generation
Visual inspection shows a Python code screenshot using AudioLDM2Pipeline from diffusers, loaded with from_pretrained on the cvssp/audioldm2 checkpoint in fp16 on CUDA. The example sets a torch.Generator seed, defines a prompt ("The sound of a hammer hitting a wooden surface") and a negative prompt ("Low quality"), calls the pipeline with num_inference_steps, audio_length_in_s, num_waveforms_per_prompt, and writes the best waveform to a .wav file via scipy.io.wavfile.write at 16 kHz.

---

## Deck-level takeaway
The deck tours the HuggingFace ecosystem layer by layer: hub artifacts (dataset and model cards), the datasets library and its DatasetDict abstraction, the transformers library with AutoClasses and the SentenceTransformer specialization, ready-made pipelines (with text generation as the running example), the evaluate library for metrics, the Trainer for fine-tuning, and finally the diffusers library for image and audio generation. The unifying message is that nearly any modern model, dataset, or metric is one from_pretrained or load call away, and that the same APIs scale from quick prototyping to full fine-tuning loops.
