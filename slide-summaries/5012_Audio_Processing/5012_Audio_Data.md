# 5012_Audio_Data — Per-Slide Summary

**Source file:** `5012_Audio_Data.pptx`
**Source folder:** `SlidesPool/5012_Audio_Processing/`
**Drive link:** https://drive.google.com/file/d/1__SuawZhpgPrSNy4RvlwSoZ439rX_6Vc/view
**Slide count (exact, via python-pptx):** 21
**Extraction:** Local parse + slide PNG render. Many slides combine code screenshots with rendered plots (waveforms, spectrograms, Mel filter banks, MFCC pipeline), visually inspected.

---

## Slide 1 — Audio Processing
Title slide for the chapter on classical audio representations that feed neural pipelines.

## Slide 2 — Audio Tasks
A three-row diagram lays out the canonical I/O signatures: automatic speech recognition takes a waveform and returns a transcript; text-to-speech inverts that; voice enhancement is waveform-to-waveform. A caption reminds the reader that audio extends beyond voice into music completion, style transfer, music from text, and ambient audio from text.

## Slide 3 — Audio Data
Section divider before the digital audio primer.

## Slide 4 — Audio Data
Digital audio is parameterized by sampling rate (samples per second, in Hz) and bit depth (bits per sample). The illustration shows a continuous waveform S(t) being sampled at integer indices to produce discrete samples S_i, demonstrating how the analog signal is captured at uniform time intervals.

## Slide 5 — Example
A librosa demo: `librosa.load(librosa.ex("trumpet"))` returns the sample array and sampling rate, and `librosa.display.waveshow` plots the amplitude envelope. The rendered figure shows a six-second trumpet waveform with high-amplitude attack-decay cycles before silence at the end, making the time-domain representation concrete.

## Slide 6 — Reminder: Frequency Domain
Three panels recap the time-versus-frequency duality. A sinusoid is parameterized as A sin(omega_0 t - phi); a table of single-frequency tones (1, 2, 4, 8, 16 Hz plus a mixed signal) pairs each waveform with its single-spike spectrum; a 3D plot decomposes a complex time-domain signal into the sum of its frequency-domain components, the standard Fourier intuition.

## Slide 7 — Reminder Decibel Scale
The decibel scale converts power to a logarithmic dB value via N_dB = 10 log10(P / 10^-12), with 10^-12 W as the reference threshold of human hearing. A real-world dB ladder (silence at 0 dB, normal speech around 60 dB, rock concert near 150 dB, jet engine at 180 dB) anchors the abstract formula in familiar sounds.

## Slide 8 — Frequency Spectrum, DFT in dB
A code snippet windows the first 4096 samples with a Hanning window, runs `np.fft.rfft`, then converts magnitude to decibels with `librosa.amplitude_to_db`. The resulting plot shows amplitude in dB on a logarithmic frequency axis from about 10 Hz to 10 kHz, with strong harmonic peaks characteristic of a trumpet's overtone series.

## Slide 9 — Short-Time Fourier Transform
The STFT is built by sliding overlapping windows along the signal (window length and hop length annotated), windowing each segment, and applying the FFT to produce a sequence of local spectra. The companion panel pairs the time-domain waveform of "twinkle twinkle little star" with its STFT spectrogram, showing how syllable boundaries align with energy bands across frequency.

## Slide 10 — Audio Spectrograms
A side-by-side example pairs the waveform with the spectrogram for the same "twinkle twinkle" utterance, emphasizing that the spectrogram preserves time on the horizontal axis while exposing how spectral energy redistributes across the vertical (frequency) axis for each syllable.

## Slide 11 — Spectrogram: STFT
The librosa idiom: `D = librosa.stft(array)` followed by `librosa.amplitude_to_db(np.abs(D), ref=np.max)` and `librosa.display.specshow(S_db, x_axis="time", y_axis="hz")`. The rendered spectrogram with a colorbar shows energy in dB across time, the standard input format for many ASR models before the move to log-mel.

## Slide 12 — Mel Spectrum
The mel scale warps the frequency axis non-linearly to match human perception: the ear is more sensitive to changes at low frequencies, so 500 vs 1000 Hz is more noticeable than 5 kHz vs 5.5 kHz, with sensitivity decreasing logarithmically. The plot shows a bank of overlapping triangular mel filters covering 0 to 4 kHz, denser at low frequency and broader at high frequency.

## Slide 13 — Log-Mel spectrogram
Adding a logarithmic amplitude scale on top of the mel spectrogram yields the log-mel-spectrogram. The librosa pipeline `librosa.feature.melspectrogram(...)` followed by `librosa.power_to_db` produces the canonical input representation for Whisper, wav2vec, and most modern ASR models. The rendered figure shows energy on a mel axis from 0 to roughly 4 kHz over several seconds.

## Slide 14 — MFCC features
Mel-frequency Cepstral Coefficients (MFCCs) are obtained by applying a Discrete Cosine Transform to the log-mel-spectrum and keeping only the first few coefficients. The pipeline diagram walks through speech frame, FFT, spectrum, mel-scale triangular filters, integration and data reduction, log, DCT, MFCC, encoding the classical front-end that dominated ASR before deep learning.

## Slide 15 — Audio Datasets
Section divider before the HuggingFace `datasets` walkthrough.

## Slide 16 — Load datasets
`load_dataset("PolyAI/minds14", name="en-AU", split="train")` returns a Dataset object with features path, audio, transcription, english_transcription, intent_class, lang_id, num_rows 654. The example shows a single record where transcription "I would like to pay my electricity bill using my card can you please assist" maps via `id2label = minds.features["intent_class"].int2str` to intent class "pay_bill", the textbook MINDS-14 intent-classification setup.

## Slide 17 — Visualize speech
Code reads `example["audio"]["array"]` and `["sampling_rate"]` and plots the waveform via `librosa.display.waveshow`. The rendered figure shows eight seconds of speech with distinct breath-group bursts separated by pauses, the typical look of a single spoken utterance.

## Slide 18 — Preprocessing Audio
Section divider before resampling and feature extraction.

## Slide 19 — Resampling
`minds.cast_column("audio", Audio(sampling_rate=16_000))` resamples every clip to 16 kHz on access. The accompanying panel contrasts 1D nearest-neighbour, linear, and cubic interpolation, illustrating why higher-order interpolation preserves the underlying waveform shape better than naive nearest-neighbour when changing sample rates.

## Slide 20 — Extract Features
A two-step Whisper feature extraction pipeline: `WhisperFeatureExtractor.from_pretrained("openai/whisper-small")` constructs the extractor; a `prepare_dataset` function applies it to each audio array with padding=True; `minds.map(prepare_dataset)` precomputes features for the whole dataset. The slide reminds the reader that Whisper expects 30-second chunks converted to log-mel-spectrograms.

## Slide 21 — Visualize Features
The final code block plots the extracted log-mel input features via `librosa.display.specshow` with mel axis and the feature extractor's sampling_rate and hop_length. The rendered spectrogram shows mel energy bands up to 4096 mel with a colorbar from -0.5 to 1.25, confirming the input is correctly shaped for ingestion by the Whisper encoder.

---

## Deck-level takeaway
The deck is the classical audio-preprocessing primer that has to precede any deep-audio chapter. It builds the signal-processing stack readers need before encountering wav2vec, HuBERT, or Whisper: time-domain sampling and bit depth, Fourier and STFT, the perceptual mel warp, log-mel spectrograms as the de-facto neural input, and MFCCs as the legacy front-end. The second half pivots from theory to the HuggingFace `datasets` workflow (MINDS-14), demonstrating the load, resample, extract, visualize loop that turns raw waveforms into the tensors a Whisper-style ASR model consumes. The deck pairs every formula with a librosa one-liner so the reader leaves with both intuition and a reproducible toolchain.
