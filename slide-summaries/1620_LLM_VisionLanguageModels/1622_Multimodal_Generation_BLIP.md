# 1622_Multimodal_Generation_BLIP — Per-Slide Summary

**Source file:** `1622_Multimodal_Generation_BLIP.pptx`
**Source folder:** `SlidesPool/1620_LLM_VisionLanguageModels/`
**Drive link:** https://drive.google.com/file/d/1LmrTByWV-xndAv58dfkiDvsCY2u_UPPK/view
**Slide count (exact, via python-pptx):** 13
**Extraction:** Local parse + slide PNG render. Bullets and code screenshots cover the Q-Former architecture and the two-stage BLIP-2 training recipe.

---

## Slide 1 — BLIP-2
Title slide; sub-title "Multimodal text generation using adapters".

## Slide 2 — Chatting with images
CLIP embeds text and images into a shared semantic space. BLIP-2 generates text and dialog from a combined image-plus-text prompt.

## Slide 3 — Soft Prompt
BLIP-2 starts from frozen pretrained models (a vision encoder and an encoder-decoder language model) and trains a Q-Former to translate the image into soft tokens. Q-Former outputs a fixed number of dense embedding tokens regardless of image, capturing image semantics. These soft tokens are prefixed to the text prompt for the language model. The Q-Former starts from learnable query vectors that are enriched with the image through cross-attention with encoded image tokens; the fine-tuned encoder-decoder language model then generates the response.

## Slide 4 — Architecture
Three components. Frozen pretrained vision encoder (e.g., CLIP), maps an image to a sequence of context vectors; any pretrained vision encoder works. Frozen pretrained LLM (e.g., Flan-T5), maps language and vision tokens to generated text; any pretrained LLM works. Q-Former (query transformer) translates image representation into the LLM token embedding space.

## Slide 5 — Q-Former Queries
In cross-attention, queries say what the tokens want to know and keys / values supply that. The Q-Former learns good query vectors that, applied to any image's ViT patch embeddings, extract a fixed-size summary. The Q-Former's parameters are both its model weights and its learned queries.

## Slide 6 — Q-former training
Stage 1, Bootstrapping: train the Q-Former independently of the language generator on text-image pairs. A temporary text encoder is attached and the model is trained on proxy tasks; the attention layer of text and image encoders interacts in a uni- or bi-directional fashion.

## Slide 7 — Q-Former Proxy Tasks for stage 1
Three proxy tasks. ITM (Image-Text Matching) is a binary classification loss on the pooled or [CLS] embeddings. ITC (Image-Text Contrastive) is InfoNCE loss maximizing similarity between correct pairs in a batch. ITG (Image-Grounded Text Generation) attaches an autoregressive next-token prediction head.

## Slide 8 — Q-former training: stage 2
Stage 2: project visual query embeddings into the LLM space (a different frozen LLM than the one used in Q-Former stage-1 training), learning to project tokens to LLM space as soft tokens.

## Slide 9 — BLIP2 Examples
Section divider for examples.

## Slide 10 — Preprocessing Image
Six screenshots preprocessing the image for BLIP-2.

## Slide 11 — Task 1: generate Image Captioning
Four screenshots showing the model.generate flow for captioning: ViT embeds patches, Q-Former transforms its query vectors using the patch embeddings, the transformed queries are projected into the LLM input space, and the LLM generates text.

## Slide 12 — Task 2: Multimodal Chat Prompting
Four screenshots demonstrating a multimodal chat-prompting task with image plus text input.

## Slide 13 — Task 2: Chat over image
Three screenshots showing multi-turn chat over an image, with chat history provided in the prompt.

---

## Deck-level takeaway
BLIP-2 keeps both the vision encoder and the LLM frozen and learns only a lightweight adapter, the Q-Former, that turns any image into a fixed-size sequence of soft tokens consumable as a prompt prefix by the LLM. The Q-Former starts from learnable query vectors and pulls visual information in through cross-attention with the vision encoder's patch embeddings. Training is two-stage: first bootstrap Q-Former independently with ITM, ITC, and ITG objectives, then project its output into the target LLM's token space. The result is a multimodal model that does both image captioning and multi-turn chat over images without retraining the heavy vision or language backbones.
