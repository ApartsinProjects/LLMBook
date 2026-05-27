# 5021_MultimodalAudio — Per-Slide Summary

**Source file:** `5021_MultimodalAudio.pptx`
**Source folder:** `SlidesPool/5025_Audio_Multimodal/`
**Drive link:** https://drive.google.com/file/d/1QN7S5CicyRu01JNi0FJLX1Bo8VzMdNEE/view
**Slide count (exact, via python-pptx):** 5
**Extraction:** Local parse + slide PNG render. CLAP architecture diagrams and the InfoNCE formula were visually inspected.

---

## Slide 1 — Multimodal Audio Models
Title slide introducing CLAP as the audio counterpart to CLIP.

## Slide 2 — CLAP: Contrastive Language-Audio Pretraining
CLAP learns a joint embedding space for text and audio. Training pairs are short audio clips with their textual description (e.g., "sad piano music"). The audio side uses a CNN-based encoder; the text side uses a BERT-like transformer. Both encoders are trained with an InfoNCE contrastive objective whose loss is L = -1/N sum_i [ log( exp(sim(a_i, t_i)/tau) / sum_j exp(sim(a_i, t_j)/tau) ) + log( exp(sim(t_i, a_i)/tau) / sum_j exp(sim(t_i, a_j)/tau) ) ], a symmetric audio-to-text and text-to-audio matching loss.

## Slide 3 — CLAP: Audio Encoder
To handle variable-length audio, clips longer than 10 seconds are processed with a chunk-and-fuse trick. Three random 10-second chunks are sampled from the long clip and a fourth down-sampled global representation is computed. Each branch passes through a mel-filterbank and Conv2D; the chunks are merged via attention feature fusion and combined with the global view before entering the rest of the audio encoder and a final MLP layer. Clips shorter than 10 seconds are simply repeated and padded.

## Slide 4 — CLAP
The text encoder must handle two data formats. Some training examples have sentence captions; others have only keyword labels. The pipeline routes keyword-only examples through a T5-based keyword-to-sentence augmentation step that synthesizes a natural-language caption before passing the result to the text encoder. The diagram shows audio waveforms going through the audio-encoder stack and text data going through the text encoder, with the resulting embedding matrix exposing the diagonal alignment between matched audio (E^a_1..n) and text (E^t_1..n) pairs.

## Slide 5 — CLAP: Zero-Shot Audio Classification
At inference, CLAP classifies unseen classes by embedding the audio sample and a textual description of each candidate class, then ranking by embedding similarity. The HuggingFace pipeline `task="zero-shot-audio-classification"` with model `laion/clap-htsat-unfused` accepts `candidate_labels=["Sound of a dog", "Sound of vacuum cleaner"]` and returns per-label probabilities, picking "Sound of a dog" with the higher score on the dog clip from `ashraq/esc50`.

---

## Deck-level takeaway
The short deck reuses the CLIP recipe but in the audio modality. The reader learns that contrastive language-audio pretraining requires two design choices on top of the standard contrastive loss: an audio encoder that can ingest variable-length clips (handled by the three-chunk plus down-sampled-global fusion) and a text encoder that can absorb both captioned and keyword-labeled data (handled by a T5-based keyword-to-sentence augmentation step). The payoff is the same as CLIP: a single joint embedding space that supports zero-shot classification of arbitrary sound categories, retrieval, and conditioning for downstream audio-generation models like TANGO and AudioLDM.
