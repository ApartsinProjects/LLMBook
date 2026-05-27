# 5021_Audio_Encoders — Per-Slide Summary

**Source file:** `5021_Audio_Encoders.pptx`
**Source folder:** `SlidesPool/5020_Audio_Encoders/`
**Drive link:** https://drive.google.com/file/d/1PUTgaw-JnceL1FmiOG7Deo_y9kWatXwi/view
**Slide count (exact, via python-pptx):** 36
**Extraction:** Local parse + slide PNG render. Architecture diagrams (wav2vec, HuBERT, EnCodec, CTC alignment, RVQ) and code screenshots were visually inspected.

---

## Slide 1 — Speech Encoding
Title slide for the chapter on speech encoders, framed as audio compression plus representation learning.

## Slide 2 — Reminder; Transformer Models
A one-slide recap of canonical transformer roles (encoder, decoder, encoder-decoder) so the reader has the right mental scaffold for the audio variants to come.

## Slide 3 — Transformers for Audio
A taxonomy splits transformer audio systems into two families. Modality-specific models use different encoders, decoders, or encoder-decoders depending on whether input or output is text, speech, or general audio. Multimodal models share a single trunk across modalities. The slide motivates why the chapter needs to discuss input/output token formats before it can compare model families.

## Slide 4 — Representing audio for input and output
Section divider before the input/output representation discussion.

## Slide 5 — Waveform Input Embedding
Wav2Vec2 and HuBERT consume raw waveforms. Preprocessing normalizes the signal to zero mean and unit variance; a small convolutional network gradually downsamples and produces a 512-dimensional embedding per 25 ms frame. The diagram shows the waveform feeding the CNN feature encoder, then being passed (after an addition with positional info) into a transformer encoder.

## Slide 6 — Spectrogram Input
Raw waveforms are inconveniently long: 30 s at 16 kHz is 0.5 M samples, beyond reasonable transformer context. Whisper instead consumes a (3000, 80) log-mel spectrogram per 30 s clip with 80 mel bins and 3000 time steps at ~10 ms per step. The spectrogram trick shortens sequence length by two orders of magnitude while preserving the time-frequency structure the model needs.

## Slide 7 — Spectrogram Output
For generation, the model emits a spectrogram, not a waveform, because waveforms require phase information that the model would have to invent sample by sample. SpeechT5 TTS outputs a sequence of 768-dim vectors, a linear layer projects them to log-mel spectrogram frames, a post-net (linear+CNN) refines the spectrogram, and a vocoder finally produces the waveform. The diagram shows this generate-spectrogram-then-vocode pattern that has become standard across modern TTS.

## Slide 8 — CTC: Connectionist Temporal Classification
Section divider for CTC, the mechanism that lets a model learn sequence-to-sequence tasks without per-frame ground-truth alignment.

## Slide 9 — Sequence-to-sequence tasks
Two task families are contrasted. In aligned seq2seq, ground truth for every token or frame is known and frame-level supervision (correct or incorrect) is trivial. In misaligned seq2seq (the realistic ASR case), only the final transcript is known; alignment between predicted frames and target characters is unknown, but time order is preserved, so the loss has to marginalize over plausible alignments.

## Slide 10 — Training Encoder with an ASR task
The naive recipe: break audio into short windows, encode each window, and add a character prediction head. The challenge is that one phoneme spans multiple windows, so the encoder may emit the same character several times, and there is no per-window label to compare against.

## Slide 11 — CTC Decoding/Model Output
The trick is to predict character sequences containing repetitions, separator tokens, and word breaks. A ground-truth transcript like "CHAPTER SIXTEEN I MIGHT" can correspond to a noisy raw output like "CHAAAAAPTTERRRSSIXTEEEEENIMMMIIGHT...", which collapses to clean text by merging consecutive repeats and removing the separator (`*`) and word-break (`/`) markers, e.g. "CHAAAAAA*PTT*ERRR/SS*IX*T*EE*EEN/I/MMM*II*GHT".

## Slide 12 — CTC Loss
The CTC loss sums probabilities over all valid alignments of labels y and predictions x. Direct enumeration is exponential; a dynamic-programming forward-backward algorithm computes the marginal in polynomial time, making CTC trainable end-to-end with standard gradient descent.

## Slide 13 — CTC Architecture
An encoder-only transformer encodes the audio into context vectors and a linear head predicts characters at every time step. The alignment problem (matching frame-level outputs to a character-level transcript) is solved by the CTC loss rather than by an explicit forced-alignment preprocessing step.

## Slide 14 — Text generation with CTC: Beam Search
At inference, beam search picks the best alignment and corresponding transcript by maintaining the top-k candidate paths through the lattice of frame-level character predictions, optionally re-scored by a language model.

## Slide 15 — Encoders
A comparison table summarizes the three encoders covered next. HuBERT is BERT-like with hardcoded MFCC frame features, pretrained to predict k-means cluster pseudo-labels and fine-tuned with CTC. Wave2Vec is BERT-like with learnable CNN features, pretrained to predict learnable codewords via the Gumbel-Max trick, and fine-tuned with CTC. EnCodec is an encoder-decoder whose decoder is dropped at inference; it consumes raw waveforms, is pretrained self-supervised for reconstruction, has no ASR fine-tune step, and represents audio via residual vector quantization in latent space for a multiscale token stream.

## Slide 16 — HuBERT
One-line divider: HuBERT stands for Hidden Unit BERT.

## Slide 17 — Objective
HuBERT processes audio into a sequence of contextual vectors. Training is BERT-like masked language modeling: a proxy task predicts pseudo-labels for masked segments rather than reconstructing the input. Audio frames are clustered into phoneme-like discrete units, not soft-maxed over reconstruction targets. The model learns both the targets and the encoder so it automatically discovers a lexicon of discrete sound units.

## Slide 18 — HuBERT: Tokenize audio waveform
The audio is segmented into 25 ms windows; MFCC features are extracted per window; an iteratively-built codebook (initially built via k-means on MFCC, later from intermediate BERT layer outputs) assigns each window a cluster id (the pseudo-target, hidden unit, or cluster ID). Each iteration alternates a clustering step (refine codebook) with a prediction step (train BERT to predict the codeword from masked features). The architecture diagram shows the CNN encoder feeding the transformer, with hidden states z1..z7 going into the acoustic unit discovery system above.

## Slide 19 — HuBERT: Clustering step
Vectors are clustered with k-means and assigned to centers. The first iteration uses MFCC features; later iterations cluster intermediate BERT layer outputs. No trainable parameters live in the clustering itself: only a projection from class centers into the output embedding space. At prediction time, projected class centers are compared with the encoder output and the codeword id is picked by cosine similarity.

## Slide 20 — Masked Prediction
50% of input frames are masked and replaced with a trained mask vector. For each output position the loss is a cross-entropy between the ground-truth cluster id and similarity-based logits. The encoder and the cluster embedding layers are trained jointly. The diagram shows masked frames [MSK] flowing through the CNN encoder, the transformer, and into the acoustic-unit discovery target.

## Slide 21 — Fine-Tuning HuBERT for ASR
For ASR, the cluster-prediction head is replaced by a CTC character head (alphabet plus space and separator). The encoder is fine-tuned end-to-end with CTC loss on supervised character targets, using average frame alignment behavior learned during pretraining.

## Slide 22 — Example: HuBERT fine-tuned for ASR
A code screenshot loads `HubertForCTC.from_pretrained("facebook/hubert-large-ls960-ft")` and uses the Wav2Vec2 processor to transcribe an audio clip. Greedy decoding selects the most probable token per window and collapses repeats using the separator character to yield a clean transcript like "The stale shell of old beer linger it takes many to bring out the odor a cold sop restores health and zest a salt pickle tastes fine with ham tacos al pastor are my favorite a zestful food is the hot cross bun".

## Slide 23 — Wave2Vec
Section divider for the wav2vec family.

## Slide 24 — Self-supervised pretraining
Wave2Vec 2.0 has two branches: a transformer-based encoder and a trainable quantizer using Gumbel sampling for differentiable vector quantization. The masked-language objective masks some input segments and reconstructs the quantized target vectors; a linear projection maps reconstructions back into the quantized space. The loss is contrastive: the reconstructed vector should be closer to the true target than to sampled distractors. Formally L_m = -log( exp(sim(c_t, q_t)/k) / sum_{q in Q_t} exp(sim(c_t, q)/k) ). The contrastive formulation is the main contrast with HuBERT's cross-entropy.

## Slide 25 — Wave2Vec Pretraining
The architecture diagram visualizes the masked-language pretraining setup: raw audio enters the CNN feature encoder, latent z vectors flow into the transformer, some positions are masked, and the loss compares context outputs to quantized targets with distractors.

## Slide 26 — Wave2Vec: CTC fine-tuning
Like HuBERT, fine-tuning attaches a character classification head on top of the encoder, supervises with character targets, and trains with CTC loss. The pretraining step gives the model a strong frame embedding before any labeled speech is seen.

## Slide 27 — Transcription
The HuggingFace recipe loads `Wav2Vec2Processor` and `Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")`, resamples the audio to 16 kHz, runs the model, argmaxes the logits, and decodes with `processor.batch_decode`. The slide notes that `Wav2VecForCTC` returns predicted character IDs while `Wav2VecModel` returns encoded vectors, so the same backbone serves both ASR and feature extraction.

## Slide 28 — EnCodec
One-line divider: EnCodec is a neural audio codec.

## Slide 29 — Reminder: RVQ: Residual Vector Quantization
A reminder of residual VQ: multiple codebooks each quantize the residual of the previous stage, yielding a multi-resolution token stream. The diagram revisits the RVQ stack seen in the earlier vector quantization deck.

## Slide 30 — Background: Straight-Through Training (SST)
The straight-through estimator trains a codebook through a non-differentiable nearest-neighbor selection. On the forward pass, each vector is snapped to its nearest codebook entry. On the backward pass, the quantizer is treated as the identity so the gradient flows through unchanged. Centroids are updated from the assigned vectors with exponential moving-average smoothing.

## Slide 31 — Motivation
EnCodec is trained as an autoencoder on 1-second raw audio segments with reconstruction loss. The total loss combines: reconstruction MSE; frequency-domain loss; adversarial loss (a discriminator trained to distinguish reconstructed from source); latent-space quantization error. The key trick is to quantize in the latent space using residual vector quantization with trainable codebook entries, producing a compact multiscale representation. After training, the decoder is dropped when only an encoder is needed.

## Slide 32 — EnCodec
The full EnCodec system diagram shows the convolutional encoder, the quantizer (a stack of LSTM/transformer-based RVQ blocks), the decoder, and the discriminator that supplies adversarial loss l_a alongside losses l_w (waveform), l_l (latent), l_d (discriminator), l_g (generator), and l_t (other targets).

## Slide 33 — Example
A code screenshot uses HuggingFace `EncodecModel.from_pretrained("facebook/encodec_24khz")` and its `AutoProcessor`, encodes a clip from `librispeech_asr_dummy`, and runs `encoder_outputs.audio_codes` and `audio_scales` through `model.decode`. The slide notes the example output shape: 1 s of audio is converted to a sequence of 75 frames of 128-dim vectors using 8 codebooks of 1024 entries each.

## Slide 34 — EnCodec Usage
EnCodec drives three applications: low-bitrate audio compression (6 kbps speech vs Opus at 12 to 16 kbps); generative modeling where downstream LMs predict coarse and fine EnCodec tokens that are decoded into speech (AudioLM, VALL-E, MusicGen); and intermediate representations for multimodal speech-to-speech translation systems.

## Slide 35 — Encoders
A recap of the same comparison from slide 15 (HuBERT vs Wave2Vec vs EnCodec) so the reader leaves with a consolidated cheat-sheet of inputs, pretraining objectives, fine-tuning losses, and representation styles.

## Slide 36 — AST: Audio Spectrogram Transformer
An appendix slide on AST: treat the spectrogram as an image, split into 16x16 patches with overlap, embed and run through an encoder-only transformer, and train with audio event classification on AudioSet (527 classes) using a [CLS] token classifier. The slide reuses the AST diagram from the earlier audio-transformer deck as a pointer that AST belongs in the same family of audio encoders.

---

## Deck-level takeaway
This is the deck where the reader meets the three modern speech encoders that power most ASR, codec, and audio LM pipelines today. The first third (slides 1 to 14) establishes the foundations: how audio is represented as model input (waveform CNN features versus log-mel spectrograms), how it is generated (spectrogram plus vocoder, never raw waveform), and how a model can be trained to predict text without per-frame alignment using CTC. The middle third (slides 15 to 27) is a deep dive into HuBERT (BERT-on-clusters, with iterative k-means re-clustering) and Wave2Vec 2.0 (BERT-on-Gumbel-codewords with a contrastive loss), drawing out the cross-entropy vs contrastive distinction and showing that both fine-tune to ASR via the CTC head. The final third (slides 28 to 36) presents EnCodec as a different beast: a neural audio codec whose RVQ tokens are the input vocabulary for the generative audio models that come later (AudioLM, MusicGen, VALL-E). The closing AST recap rounds out the encoder zoo. The unifying thread is that all three are transformer encoders trained self-supervised on huge unlabeled audio corpora, differing only in input format (waveform vs spectrogram), target (cluster id, codeword, or reconstruction), and loss (cross-entropy, contrastive, or reconstruction+adversarial).
