# 5015_PretrainedAudioModels — Per-Slide Summary

**Source file:** `5015_PretrainedAudioModels.pptx`
**Source folder:** `SlidesPool/5015_Audio_FM/`
**Drive link:** https://drive.google.com/file/d/1UpKYG9qLFK6VgxhPUrJehrVuPNn4o43n/view
**Slide count (exact, via python-pptx):** 19
**Extraction:** Local parse + slide PNG render. Code-screenshot slides for HuggingFace pipelines and the TANGO architecture diagram were visually inspected.

---

## Slide 1 — Pretrained Audio Models
Title slide introducing the survey of off-the-shelf audio models available through HuggingFace.

## Slide 2 — Audio Classification
Section divider before the classification examples.

## Slide 3 — Keyword Spotting
Keyword spotting (KWS) identifies a small, finite vocabulary like "stop", "play", or "Hello Google" in spoken utterances. Because the vocabulary is closed, it is simpler than full ASR. The deck loads the Speech Commands dataset, applies the `audio-classification` pipeline with model `MIT/ast-finetuned-speech-commands-v2` (an Audio Spectrogram Transformer), and shows the top predictions with scores like 0.999 for "backward", 0.5 for "happy", and similar.

## Slide 4 — Pretrained Audio Classification: Intent
A wav2vec2-based backbone is used for intent classification on the MINDS-14 dataset via the HuggingFace `audio-classification` pipeline. The code screenshots show loading, applying the pipeline to one example, and a result mapping the utterance to an intent label like "pay_bill" with a soft-max probability.

## Slide 5 — Language Identification
Language identification on the FLEURS dataset (notable for its coverage of low-resource languages) labels each clip as English, German, Hebrew, and so on. The model is built on top of Whisper, whose ASR pretraining is repurposed as a language-ID head. The code snippets show pipeline construction and a top-1 language prediction.

## Slide 6 — Automatic Speech recognition
Section divider before the ASR walk-through.

## Slide 7 — Transcription
The Whisper code idiom: `WhisperProcessor.from_pretrained("openai/whisper-small")` and `WhisperForConditionalGeneration.from_pretrained(...)` build processor and model. The processor turns the array plus sampling rate into tensors (the preprocessor computes log-mel-spectrum features), and `whisper_model.generate(**inputs)` returns token ids that `batch_decode` turns into text. The visible output transcript reads "The second in importance is as follows. Sovereignty may be defined to be" surrounded by Whisper's `<|startoftranscript|>`, `<|en|>`, `<|transcribe|>`, `<|notimestamps|>`, `<|endoftext|>` control tokens.

## Slide 8 — Representation Model
Section divider before self-supervised audio encoders.

## Slide 9 — Representation Models
A representation model produces a frame-level embedding that can be mean-pooled into a clip-level feature. HuBERT (a CNN plus transformer) is loaded via `Wav2Vec2Processor` and `HubertModel.from_pretrained("facebook/hubert-base-ls960")`, frozen, and used inside an `extract_embedding(file)` helper that resamples to 16 kHz, runs the model, and mean-pools `last_hidden_state` over time to a single vector. The slide notes HuBERT's MLM-style pretraining where masked frames must predict their cluster id (a quantized pseudo-label).

## Slide 10 — Simple classification head
A small classification head is stacked on the frozen HuBERT embedding to train a downstream classifier. The code shows train and predict calls with the standard PyTorch loop pattern, illustrating the linear-probe recipe that turns a self-supervised audio encoder into a task-specific model with minimal compute.

## Slide 11 — Multimodal Encoder
A one-line divider introduces CLAP, the audio analogue of CLIP.

## Slide 12 — CLAP: Zero-Shot Audio Classification
CLAP embeds text and audio into a shared latent space, enabling zero-shot classification of previously unseen classes. The pipeline is `pipeline(task="zero-shot-audio-classification", model="laion/clap-htsat-unfused")`. Given an audio sample from `ashraq/esc50` and `candidate_labels=["Sound of a dog", "Sound of vacuum cleaner"]`, the classifier scores each by embedding similarity and returns "Sound of a dog" with the higher score.

## Slide 13 — Speech Generation
Section divider before TTS and vocoders.

## Slide 14 — Create Speaker Embedding
A pretrained speaker-encoder model produces a fixed-length vector that captures a target speaker's timbre and style. The code screenshot shows loading the speaker-embedding model and applying it to a reference clip to obtain a vector that downstream TTS will use to clone the voice.

## Slide 15 — Example: TTS
`SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")` and `SpeechT5ForTextToSpeech.from_pretrained(...)` form the TTS stack. The speaker embedding (separately extracted) is passed to `model.generate_speech(inputs["input_ids"], speaker_embeddings)`, producing a mel-spectrogram (visible as a rendered figure). The slide flags that the spectrogram alone is phaseless, so a vocoder is required to reconstruct an audible waveform.

## Slide 16 — VOCODERS: Reconstructing Speech from Spectrogram
Neural vocoders synthesize waveforms from mel-spectrograms. Modern choices are GAN-based: MelGAN and HiFi-GAN. The code loads `SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")` and calls `vocoder(spectrogram)` to obtain the final speech array. A commented-out alternative shows `model.generate_speech(input_ids, speaker_embeddings, vocoder=vocoder)` as a single-step call.

## Slide 17 — Sound Generation
Section divider before text-to-audio diffusion.

## Slide 18 — Generate audio events
Text-to-audio diffusion generates non-speech events from prompts like "techno music" or "Flying mosquito". The architecture encodes the text with CLAP and runs latent audio diffusion conditioned on that embedding. The code uses `AudioLDMPipeline.from_pretrained("cvssp/audioldm-s-full-v2", torch_dtype=torch.float16)` with prompt "Techno music with a strong, upbeat tempo and high melodic riffs", `num_inference_steps=10`, `audio_length_in_s=5.0`, and saves the result via `scipy.io.wavfile.write`.

## Slide 19 — TANGO: Diffusion-Based
TANGO is shown as a full text-to-audio diffusion architecture. The system diagram threads a prompt (e.g., "A dog is barking and growling, as a siren is blaring") through a frozen FLAN-T5 text encoder, into a diffusion model that denoises latents in a VAE-compressed audio space. The audio decoder reconstructs a mel-spectrogram, which a HiFi-GAN vocoder turns into a waveform. The legend distinguishes inference-only, train-only, and inference+train paths, plus frozen versus trainable modules. The code box (`from tango import Tango`) demonstrates that the whole pipeline is a single `tango.generate(prompt)` call.

---

## Deck-level takeaway
The deck is a guided tour through the HuggingFace audio model zoo and the role each component plays in a production audio stack. The first half (slides 2 to 12) covers discriminative tasks: closed-vocabulary keyword spotting with AST, intent classification with wav2vec2, language ID with Whisper, ASR with Whisper, embedding extraction with HuBERT plus linear probes, and zero-shot classification with CLAP. The second half (slides 13 to 19) shifts to generation: SpeechT5 for TTS combined with speaker embeddings, HiFi-GAN as the neural vocoder that supplies phase, and finally text-to-audio diffusion with AudioLDM and TANGO. The throughline is that almost every modern audio capability is a few lines of HuggingFace pipeline code on top of a small set of pretrained backbones (Whisper, wav2vec2, HuBERT, CLAP, AST), and that the reader can mix and match them to build classification, ASR, TTS, or sound-effects generation systems.
