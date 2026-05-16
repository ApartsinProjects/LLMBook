# Ch 31 / Ch 32 Duplicate Resolution

## Per-pair decisions
- 31.5 vs 32.1: 32.1 is canonical-replacement. 32.1 has current 2026 framing (OpenVLA-7B, pi-0/pi-0.5 with flow matching, cross-embodiment transfer, late-2025 reference table). 31.5 has older, more verbose code-heavy treatment with stale "26.5.x" section numbering, lacks pi-0.5/flow-matching coverage, and frames the field at the RT-2/OpenVLA/Octo era. Action: direct-delete. The detailed action-tokenizer code and domain-randomization snippet in 31.5 are conceptually superseded by 32.1's tighter "LM head emits motor tokens" presentation and 32.2's sim-to-real treatment.
- 31.6 vs 32.2: 32.2 is canonical-replacement. 32.2 covers SayCan / Code-as-Policies / VoxPoser plus the 2025 multi-robot dispatcher pattern (Claude Haiku 4.5, Gemini Flash, Covariant/Amazon fleets), ROS 2 integration, and the cost-vs-reliability layering principle. 31.6 covers SayCan, Code-as-Policies, Inner Monologue, LM-Nav, edge deployment on Jetson, safety verification - some unique sub-topics (Inner Monologue, edge / Jetson, safety verification) but with stale "26.6.x" numbering and pre-multi-robot-LLM-dispatcher framing. Action: direct-delete. Edge deployment + safety-monitor pattern is already implicit in 32.2.5 ROS 2 + 32.2.6 cost trade-off callout.
- 31.7 vs 32.3: 32.3 is canonical-replacement. 32.3 has the current 2026 framing (3DGS displaces NeRFs everywhere, InstantSplat for few-view, 4DGS / Spacetime Gaussians, RD-GS compression, NVIDIA splat backgrounds for sim-to-real). 31.7 has older "From NeRFs to 3DGS" exposition plus text-to-3D (DreamGaussian, GaussianDreamer, SDS) which 32.3 omits, but with stale "26.7.x" numbering. Text-to-3D is covered separately in Chapter 32.5 (3D Asset Generation). Action: direct-delete.

## Content merged into Ch 32 (if any)
- None. All three 32.x sections were judged complete and current as the canonical home. The 31.x files contained conceptually redundant material with stale section numbering. Topical sub-areas not explicitly mirrored in 32.x (Inner Monologue feedback loops, edge / Jetson deployment specifics, text-to-3D / SDS, aerial-ground systems) either appear elsewhere in Ch 32 (32.5 covers 3D asset generation including text-to-3D; 32.8 covers robotics / scientific discovery) or are out of scope for the current revision pass.

## Cross-refs rewritten
- 3 files book-wide updated (section-31.{5,6,7}.html -> section-32.{1,2,3}.html):
  - `part-12-frontiers/module-61-frontier-architectures/section-61.4.html` (VLA / robotic-planning cross-ref)
  - `part-10-idea-to-product/module-43-vibe-coding/section-43.2.html` (robotics-applications cross-ref)
  - `appendices/appendix-g-problem-solution-key/index.html` (robotics row of problem-solution table)
- Internal Ch 31 navigation: `section-31.4.html` chapter-nav next + "What Comes Next" prose updated to point at `module-32-embodied-world-models/section-32.1.html`.
- Note: `section-47.4.html` and `section-61.2.html` matched the `section-31.[567]` pattern but they reference `module-31-strategy-product-roi/section-31.5.html` (the Part 9 strategy/ROI chapter, different namespace). Not in scope.

## Files deleted
- part-7-multimodal-generation/module-31-multimodal/section-31.5.html
- part-7-multimodal-generation/module-31-multimodal/section-31.6.html
- part-7-multimodal-generation/module-31-multimodal/section-31.7.html

## Chapter 31 index updates
- Section-card list trimmed from 7 to 4 entries (31.1 Image / VLM, 31.2 Audio-Music-Video, 31.3 Document / OCR, 31.4 Unified omni-architectures).
- "Looking Back" callout rewritten to scope Ch 31 to the generative half and point at Ch 32 for the embodied half.
- Chapter Overview's last paragraph rewritten to drop "embodied AI with VLA, LLM-powered robotics, and 3D neural scene representation" and add an explicit pointer to Chapter 32.
- Learning Objectives trimmed: 3 embodied / robotics / 3DGS bullets removed.
- "What's Next?" prose rewritten - previously misnamed Chapter 27 - now correctly points to Chapter 32: Embodied AI, World Models & Multimodal Reasoning with current scope.
- Part VII index (`part-7-multimodal-generation/index.html`): Ch 31 card section list trimmed from 7 to 4 entries.
- Section 31.4 chapter-nav next link and "What Comes Next" prose updated to point at Section 32.1.
- `toc.html` Part VII count updated from "3 chapters · 20 sections" to "3 chapters · 17 sections" (Ch 31 lost 3 sections; Ch 32 has 8; Ch 33 has 5; 4+8+5=17).
