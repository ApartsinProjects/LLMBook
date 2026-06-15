# Graduate-Depth Audit: Part 5 (Multimodal LLMs)

| Section | Title (short) | Verdict | Missing piece (only if not COURSE-READY) |
|---|---|---|---|
| 20.0 | Audio Task Landscape | CATALOG-OK | Intentional chapter map / taxonomy of pipelines. |
| 20.0.1 | Audio Data and Representations | COURSE-READY | |
| 20.0.2 | Audio Codecs and Vector Quantization | COURSE-READY | |
| 20.0.3 | Audio/Speech Transformer Architectures | COURSE-READY | |
| 20.0.4 | Self-Supervised Audio Encoders | COURSE-READY | |
| 20.0.5 | Audio Classification (CLAP, SFT) | COURSE-READY | |
| 20.1 | Text-to-Speech: VITS, Bark, F5-TTS | COURSE-READY | |
| 20.2 | Voice Cloning, Zero-Shot TTS | COURSE-READY | |
| 20.3 | Music Generation: MusicGen, Suno | COURSE-READY | |
| 20.4 | Audio Editing: Stems, Style Transfer | DEPTH-GAP | Demucs/BS-RoFormer separation loss and masking math sketched only verbally; no worked SI-SDR objective or band-split mechanism. |
| 20.5 | Speech Recognition (Whisper) | COURSE-READY | |
| 20.6 | Video Diffusion Transformers (DiT) | COURSE-READY | |
| 20.7 | Leading Video Models (Sora, Veo) | CATALOG-OK | Intentional commercial-frontier capability survey. |
| 20.8 | Camera/Motion Control, ControlNet for Video | COURSE-READY | |
| 20.9 | Video Editing (inpaint, interp, upscale) | DEPTH-GAP | Optical-flow warping and RIFE/FILM interpolation named but not derived; no flow-consistency loss or warp mechanics. |
| 20.10 | Multi-Shot Consistency / AI Cinema | CATALOG-OK | Intentional production-workflow survey; mechanism (character tokens) recapped adequately. |
| 21.1 | Modern OCR: TrOCR, Donut | COURSE-READY | |
| 21.2 | Layout-Aware Models: LayoutLM | COURSE-READY | |
| 21.3 | VLM-Based Document Understanding | CATALOG-OK | Intentional frontier-VLM-for-docs survey with cost matrix. |
| 21.4 | Building Document AI Pipelines | CATALOG-OK | Intentional reference-architecture / stage-decomposition survey. |
| 22.1 | Visual Tokenization (ViT) | COURSE-READY | |
| 22.2 | Contrastive VL: CLIP, SigLIP | COURSE-READY | |
| 22.3 | Generative VLMs: LLaVA, BLIP, Qwen-VL | COURSE-READY | |
| 22.4 | Frontier VLMs: GPT-4V, Gemini, Claude | CATALOG-OK | Intentional closed-API vendor comparison; architecture recapped by reference. |
| 22.5 | Evaluating Multimodal Reasoning (MMMU) | CATALOG-OK | Intentional benchmark survey. |
| 22.6 | Pipeline vs Native Multimodal | COURSE-READY | |
| 22.7 | Fusion: Early, Mid, Late | COURSE-READY | |
| 22.8 | Any-to-Any Generation | COURSE-READY | |
| 22.9 | Frontier Omni Models | CATALOG-OK | Intentional frontier-model capability survey. |
| 23.1 | 3D Gaussian Splatting Fundamentals | COURSE-READY | |
| 23.2 | Dynamic Splats (4D) | COURSE-READY | |
| 23.3 | Image-to-3D: Zero123, Multi-View Diffusion | COURSE-READY | |
| 23.4 | Direct 3D Diffusion: Trellis | COURSE-READY | |
| 23.5 | Relighting and 3D Editing | DEPTH-GAP | Inverse-rendering BRDF factorization and IC-Light prior stated but the optimization (how geometry/material/illumination are jointly solved) not worked through. |
| 24.1 | VLA Architecture in One Equation | COURSE-READY | |
| 24.2 | OpenVLA-7B Reference Implementation | COURSE-READY | |
| 24.3 | Physical Intelligence pi-0 / pi-0.5 | COURSE-READY | |
| 24.4 | RT-2-X and Data-Scaling | COURSE-READY | |
| 24.5 | Comparing VLA Models | CATALOG-OK | Intentional capability-matrix / decision-tree survey. |
| 24.6 | VLA Limitations | COURSE-READY | |
| 24.7 | SayCan (affordance grounding) | COURSE-READY | |
| 24.8 | Code-as-Policies | COURSE-READY | |
| 24.9 | VoxPoser (spatial cost field) | COURSE-READY | |
| 24.10 | Multi-Robot Dispatch | COURSE-READY | |
| 24.11 | ROS 2 Integration | COURSE-READY | |
| 24.12 | Comparing Planners | CATALOG-OK | Intentional planner-paradigm comparison matrix. |
| 24.13 | Sim-to-Real Gap | COURSE-READY | |
| 25.1 | Platforms and APIs | CATALOG-OK | Tools-of-the-trade by design. |
| 25.2 | Libraries and Frameworks | CATALOG-OK | Tools-of-the-trade by design. |
| 25.3 | Datasets and Benchmarks | CATALOG-OK | Tools-of-the-trade by design. |
| 25.4 | Model Zoo | CATALOG-OK | Tools-of-the-trade by design. |
| 25.5 | External Reading and Communities | CATALOG-OK | Tools-of-the-trade by design. |

## Summary
- COURSE-READY: 33 | DEPTH-GAP: 3 | NOT-SELF-CONTAINED: 0 | CATALOG-OK: 16
- Top sections most worth enriching:
  1. 20.4 (Audio Editing): add the source-separation objective explicitly (SI-SDR loss + band-split / masking math for Demucs and BS-RoFormer) so separation is derived, not just named.
  2. 20.9 (Video Editing): derive optical-flow warping and the RIFE/FILM interpolation mechanism with a flow-consistency loss, instead of listing the tools.
  3. 23.5 (Relighting/3D Editing): work through the inverse-rendering optimization (joint geometry/material/illumination fit under the rendering equation) and how the IC-Light prior regularizes the ill-posed decomposition.
