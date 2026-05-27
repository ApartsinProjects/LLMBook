# 2225_VisionGeneration — Per-Slide Summary

**Source file:** `2225_VisionGeneration.pptx`
**Source folder:** `SlidesPool/2220_GAI_VisionFM/`
**Drive link:** https://drive.google.com/file/d/1bChQXcJMNv9vB7o8P4mKNM8CKAvdMQ5y/view
**Slide count (exact, via python-pptx):** 22
**Extraction:** Local parse + slide PNG render. Many gallery slides without body text were inspected visually.

---

## Slide 1 — Stable Diffusion Models
Title slide framing the goal: showcase what is possible with Stable Diffusion before drilling into how it works and how it is trained or fine-tuned.

## Slide 2 — Text2Image
A three-panel gallery of text-to-image generations illustrates the core capability driven by a textual prompt.

## Slide 3 — Text2Image: Negative Prompt
Two panels compare outputs from the same prompt with and without a negative prompt, demonstrating how negative prompts steer the model away from unwanted features.

## Slide 4 — Image2Image
A four-panel gallery shows image-to-image generation where a reference image is iterated under a new prompt to produce variations preserving structure.

## Slide 5 — Inpainting
A four-panel gallery demonstrates inpainting: a mask is drawn on an image and the masked region is regenerated under a prompt while the rest of the image is preserved.

## Slide 6 — ControlNet
Section-header slide introducing ControlNet as the family of structural-control mechanisms.

## Slide 7 — ControlNet: Pose Guidance
Four panels show pose-conditioned generation: a stick-figure skeleton from a reference image drives the body posture of multiple stylized characters generated from text.

## Slide 8 — Extracting Skeleton
The slide shows the OpenPose-style preprocessor turning a real photograph into the skeleton signal that feeds the pose ControlNet.

## Slide 9 — ControlNet: Depth guidance
Six panels demonstrate depth-conditioned generation where a depth map locks the scene layout while text changes the style and appearance.

## Slide 10 — Extract Depth
The slide shows MiDaS-style depth estimation that produces the depth control signal from an arbitrary input image.

## Slide 11 — ControlNet: Canny Image
Three panels show Canny edge-conditioned generation where a black-and-white edge map dictates contours while the prompt fills in style and content.

## Slide 12 — ControlNet: Canny Image
Three more Canny-conditioned variations on a different reference image, illustrating the strong silhouette adherence the edge map enforces.

## Slide 13 — More Controls
A schematic enumerates the broader catalog of control signals (scribble, segmentation, normal map) handled by community ControlNets.

## Slide 14 — Multi-ControlNet
Three panels show stacking multiple ControlNets (for example pose plus depth) simultaneously, with the model honoring both structural constraints.

## Slide 15 — Outpainting
Five panels walk through outpainting: an original image is placed inside a larger canvas with a surrounding mask, and Stable Diffusion fills the new area consistent with the original.

## Slide 16 — LoRA Adapters
Section-header slide that introduces LoRA adapters as the parameter-efficient fine-tuning route.

## Slide 17 — LoRA: Fine-tune by composition
Two panels demonstrate composing multiple LoRA adapters (for example a style LoRA with a character LoRA) at inference time without retraining.

## Slide 18 — Personalized Generation
Section-header slide that transitions to personalization techniques.

## Slide 19 — Dream Booth
DreamBooth is described as fine-tuning on 3-5 images of a specific object or subject, associating a unique trigger word (example: `sks herge_style`, referencing Hergé, a Belgian comic artist). Three panels show personalized outputs in the trained style.

## Slide 20 — Textual Inversion
Textual Inversion is similarly described as fine-tuning on 3-5 images of a specific concept with a learned trigger word such as `<gta5_artwork>`; three panels show outputs in the inverted style.

## Slide 21 — Diffusion Model UI Tool: ComfyUI
The slide presents ComfyUI as a node-based graphical UI for orchestrating diffusion pipelines, showing a typical pipeline graph.

## Slide 22 — Model Hubs
Two panels highlight the Hugging Face Hub and Civitai as community model hubs that distribute base models, LoRAs, ControlNets, and textual-inversion concepts.

---

## Deck-level takeaway
This is a capabilities tour of the Stable Diffusion ecosystem. It first showcases text-to-image, image-to-image, and inpainting, then walks through ControlNet variants (pose, depth, Canny, multi-control) and outpainting, and finally introduces personalization through LoRA, DreamBooth, and Textual Inversion plus the ComfyUI orchestration tool and the model hubs that distribute everything. Each technique covered here is unpacked in the dedicated decks that follow.
