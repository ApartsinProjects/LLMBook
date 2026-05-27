# 5014_AudioSpeechTransformers — Per-Slide Summary

**Source file:** `5014_AudioSpeechTransformers.pptx`
**Source folder:** `SlidesPool/5018_Audio_Transformer/`
**Drive link:** https://drive.google.com/file/d/1qRyArpWv1vRlxdZDsmJeNpApgoUEmEWr/view
**Slide count (exact, via python-pptx):** 4
**Extraction:** Local parse + slide PNG render. The AST architecture diagram and code screenshots were visually inspected.

---

## Slide 1 — Audio Transformers
Title slide for the short sub-chapter that introduces the Audio Spectrogram Transformer (AST).

## Slide 2 — AST: Audio Spectrogram Transformer
AST treats the log-mel-spectrogram as an image. It splits the spectrogram into partially overlapped 16x16 patches, applies a linear projection plus positional embeddings, and passes the patch sequence to an encoder-only transformer (the same architecture as ViT). A [CLS] token aggregates global information and is fed to a linear classification head. The model is trained on AudioSet (527 audio event classes), making it a strong general-purpose audio classifier. The diagram shows the input spectrogram, the patch-split-with-overlap step, the linear projection, the transformer encoder stack, and the final linear classifier head.

## Slide 3 — Audio Classification
A label dictionary illustrates the kind of coarse audio classes AST learns to discriminate: 0 Speech, 1 Animal, 2 Natural sounds, 3 Musical instrument, 4 Music, 5 Human sounds, 6 Singing, 7 Tools, 8 Engine, 9 Other. The slide motivates why a strong general-purpose audio backbone is useful as a feature extractor for many downstream tasks.

## Slide 4 — Pretrained representation model with classification head
The HuggingFace recipe loads `AutoFeatureExtractor.from_pretrained("MIT/ast-finetuned-audioset-10-10-0.4593")` and `ASTForAudioClassification.from_pretrained(...)` with the same checkpoint. The feature extractor turns `dataset[0]["audio"]["array"]` at the given `sampling_rate` into tensors; the model returns logits; `torch.argmax(logits, dim=-1).item()` picks the top class, which is mapped to a human-readable label through `model.config.id2label`. The code shows the canonical three-line inference pattern for any AST classifier checkpoint.

---

## Deck-level takeaway
The short deck makes a single but important point: by the time the reader encounters this section they already know ViT, and AST is just ViT applied to log-mel spectrograms instead of natural images. The transferable mental model (patchify, linearly project, add positional embeddings, run encoder-only transformer, classify with [CLS]) means the reader can immediately use AudioSet-pretrained backbones via HuggingFace with the familiar `AutoFeatureExtractor` plus `AutoModelForAudioClassification` idiom. It also sets up later material on multimodal audio-text models like CLAP, which use AST-style encoders on the audio side.
