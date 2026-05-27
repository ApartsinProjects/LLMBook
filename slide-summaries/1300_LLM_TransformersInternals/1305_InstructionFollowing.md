# 1305_InstructionFollowing — Per-Slide Summary

**Source file:** `1305_InstructionFollowing.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/1i9BOIRs56ajLPRnZyPsxDyOcv6SJcj1f/view
**Slide count (exact, via python-pptx):** 10
**Extraction:** Local parse + slide PNG render. Bullets and code screenshots carry the conceptual content.

---

## Slide 1 — Instruction fine-tuning
Title slide for the lecture on instruction-tuning generative LLMs.

## Slide 2 — Reminder: Unsupervised Pretraining
GPT is pretrained for next-token prediction on text completion, with no explicit notion of instructions.

## Slide 3 — Major GPT use case: Instruction Following
The dominant downstream use of GPT-style models is instruction following, which requires fine-tuning on instruction / response pairs (supervised fine-tuning, SFT).

## Slide 4 — Training Data: Instruction Datasets
A figure illustrating the structure of an instruction-following dataset (instruction, optional input, expected response).

## Slide 5 — Instruction following datasets
A figure listing several well-known instruction-following datasets used to fine-tune base models.

## Slide 6 — Format data instructions into documents
Each example is rendered into a flat document by separating fields with special tokens or headers; the choice is model-specific, and inference must use exactly the same format that was used during fine-tuning.

## Slide 7 — When to stop the generation process
The special token <|endoftext|> signals generation to stop. It is attached at the end of the response during training so that the model learns to emit it after completing the answer; at inference, autoregressive generation halts when this token is produced.

## Slide 8 — Training data: Batches, Padding, Ignore Tokens
Training data are pairs of input and output sequences; for short instructions, the example is a document plus its shifted version, and the model does not cross document boundaries. Batches are formed by padding to the longest sequence. The loss ignores certain tokens (instruction tokens and padding tokens) by replacing them in the target with the special ignore token -100.

## Slide 9 — Reminder: Parallel Next Token Prediction
Recap of parallel token prediction during training (predict every prefix simultaneously and aggregate loss) and last-token prediction during generation, using the toy "User clicked mouse" example.

## Slide 10 — Prompt dampening
The default approach masks the prompt entirely (instruction tokens replaced with -100). An alternative, prompt dampening, reduces the relative weight of the prompt-token prediction loss rather than zeroing it; the rationale is that learning a proper representation of the prompt might also help response generation.

---

## Deck-level takeaway
The deck explains how to turn a next-token-pretrained GPT into an instruction-following model through supervised fine-tuning on instruction / response pairs. The mechanics center on three practical choices: a model-specific document format that flattens instruction, input, and response fields and is reused at inference; the <|endoftext|> stop token attached during training; and a loss that ignores prompt and padding positions via the -100 sentinel (with prompt dampening as a softer alternative that reduces, rather than zeroes, the prompt's contribution to the loss).
