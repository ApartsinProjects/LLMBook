# 5041_Audio_Speech2Text — Per-Slide Summary

**Source file:** `5041_Audio_Speech2Text.pptx`
**Source folder:** `SlidesPool/5040_Audio_Speech2Text/`
**Drive link:** https://drive.google.com/file/d/14H2dsaLm2ugwZYAREaKCCXEOq4ffT8Vm/view
**Slide count (exact, via python-pptx):** 14
**Extraction:** Local parse + slide PNG render. The Whisper architecture diagram, the multitask training format, and chunked long-form transcription were visually inspected.

---

## Slide 1 — Speech2Text
Title slide for the chapter on sequence-to-sequence speech recognition with Whisper.

## Slide 2 — Whisper transformer: encoder-decoder
OpenAI's Whisper was trained on 680 K hours of audio (compared to 60 K hours for wav2vec), covering 96 languages. It is an encoder-decoder transformer: the encoder ingests the log-mel-spectrogram of the input clip; the decoder predicts the next text token autoregressively. Unlike HuBERT or wav2vec there is no quantization or pseudo-target stage; supervision is direct on text. A single model handles multiple tasks (transcription in the same language, translation to English, language identification) by conditioning on special task, language, and timestamp tokens.

## Slide 3 — Whisper Architecture
The diagram shows the full architecture. A log-mel spectrogram passes through 2x Conv1D + GELU with sinusoidal positional encoding into a stack of encoder blocks. The decoder is a stack of decoder blocks with cross-attention to the encoder output and learned positional encoding on the textual side. Generation is autoregressive: the decoder starts from SOT (start-of-transcript), then emits language and task tokens (e.g., EN, TRANSCRIBE), a no-timestamp marker (0.0), and finally text tokens until an end-of-text token. Training uses token-level cross-entropy; evaluation reports Word Error Rate (counting substitutions, insertions, and deletions between output and ground truth).

## Slide 4 — Speech2Text with transformers
A simpler view of the sequence-to-sequence setup highlights how task tokens (Language, Task Type) control behavior. The HuggingFace `pipeline("automatic-speech-recognition", model="openai/whisper-small", max_new_tokens=200)` reduces the whole flow to a single function call: `pipe(array)` returns `{'text': ' The second in importance is as follows. Sovereignty may be defined to be'}`.

## Slide 5 — Multitask Training Format (text output)
The Whisper multitask training format is drawn as a directed graph over special tokens. From the Start-of-transcript token the model branches: a Language tag activates language identification, then either Transcribe (X to X transcription) or Translate (X to English translation). A "No speech" branch handles Voice Activity Detection. Inside transcription, the choice between time-aligned tokens (Begin time, Text tokens, End time) and text-only output is controlled by another switch, finally reaching EOT. The same vocabulary describes every task the model performs.

## Slide 6 — Example
A short code snippet (single screenshot) shows the canonical Whisper invocation pattern, anchoring the multitask format in a runnable call.

## Slide 7 — Transcription
The lower-level API: `WhisperProcessor.from_pretrained("openai/whisper-small")` and `WhisperForConditionalGeneration.from_pretrained(...)`. The processor turns the audio array and sampling rate into tensors; `model.generate(**inputs)` returns ids; `processor.batch_decode(generated_ids, skip_special_tokens=False)` produces the string with all control tokens visible: `<|startoftranscript|><|en|><|transcribe|><|notimestamps|> The second in importance is as follows. Sovereignty may be defined to be<|endoftext|>`.

## Slide 8 — Transcription with Pipeline
The model has a 30-second duration limit, so long audio must be chunked. The pipeline accepts `chunk_length_s=5`, `batch_size=8`, and `return_timestamps=True` to chunk with overlap for long clips and to support live inference with short chunks. The example uses `generate_kwargs={"task": "transcribe"}` to force the transcribe task.

## Slide 9 — Multilingual ASR
Whisper covers 96 languages out of the box. Code screenshots show loading multilingual data, applying the pipeline, and switching language by changing the language task token in `generate_kwargs`.

## Slide 10 — Results
The chunked pipeline returns a dictionary with `chunks` (a list of {text, timestamp} pairs) and a final concatenated `text`. The visible example shows chunks at timestamps (0.0, 3.0), (3.0, 6.33), (6.33, 16.89), (16.89, 36.61), (36.61, 59.75), (59.75, 67.09), (67.09, 70.43) for a 70-second passage from a political theory text, demonstrating how Whisper aligns transcript spans to audio time.

## Slide 11 — Fine-Tuning
Section divider for the fine-tuning recipe.

## Slide 12 — Finetuning ASR
Fine-tuning uses `Seq2SeqTrainingArguments` (output_dir="./whisper-small-dv", per_device_train_batch_size, gradient_accumulation_steps, learning_rate, lr_scheduler_type="constant_with_warmup", warmup_steps, max_steps=4000, gradient_checkpointing=True, fp16, evaluation_strategy="steps", per_device_eval_batch_size, predict_with_generate=True, generation_max_length=225, save_steps, eval_steps, logging_steps, report_to=["tensorboard"], load_best_model_at_end=True, metric_for_best_model="wer", greater_is_better=False, push_to_hub=True) and the `Seq2SeqTrainer(args=training_args, model=model, train_dataset=common_voice["train"], eval_dataset=common_voice["test"], data_collator=data_collator, compute_metrics=compute_metrics, tokenizer=processor)`. This is the textbook recipe for Whisper fine-tuning on Common Voice.

## Slide 13 — Longform Transcription
Section divider before the chunking-and-stitching trick for very long audio.

## Slide 14 — Long-Form Transcription
Whisper natively handles 30-second windows, so very long audio must be chunked into overlapped segments (e.g., `chunk_length_s=30`, with stride at both ends), each processed independently (potentially in parallel) and stitched together. The diagram visualizes chunk1 and chunk2 with shared stride regions: overlapping tokens like "HHELLLM P" and "ME LLO O" are reconciled at the boundary so the final transcript reads continuously. The `pipe(long_audio, max_new_tokens=256, generate_kwargs={"task": "transcribe"}, chunk_length_s=30, batch_size=8)` call wraps the entire procedure.

---

## Deck-level takeaway
The deck presents Whisper as the modern reference architecture for ASR and the natural endpoint of the audio-encoder progression that began with wav2vec and HuBERT. The key architectural differences (encoder-decoder vs encoder-only, direct text supervision vs cluster-id pseudo-targets, multitask special-token conditioning vs single-task CTC head) are made concrete with the architecture diagram and the multitask training-format graph. The HuggingFace API ladder is presented in full: a one-line `pipeline` call for simple use, a lower-level processor/model pair for control over generation parameters, the `Seq2SeqTrainer` recipe for fine-tuning on Common Voice, and the chunk-and-stitch pattern for transcripts longer than Whisper's native 30-second window. The reader leaves with both the conceptual story of why a seq2seq transformer trained on 680 K hours of multilingual audio dominates classical pipelines, and the practical code to deploy or fine-tune it.
