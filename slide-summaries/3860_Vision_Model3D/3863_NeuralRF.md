# 3863_NeuralRF — Per-Slide Summary

**Source file:** `3863_NeuralRF.pptx`
**Source folder:** `SlidesPool/3860_Vision_Model3D/`
**Drive link:** https://drive.google.com/file/d/1IEWnzwSWix6UDtHViPL7c-kMKHz3ji4L/view
**Slide count (exact, via python-pptx):** 24
**Extraction:** Local parse + slide PNG render. 3 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — NeRF: Neural Radiance Field
Section divider; the deck transitions to material on nerf: neural radiance field.

## Slide 2 — Introduction
Generate 3D representation from multiple views Need to produce a synthetic view/image of the scene from different angles Parametrize scene using Neural Network Generate a view form from viewing direction Not a light source. The slide includes 1 embedded image alongside the bullets.

## Slide 3 — Volume vs. Surface Rending
Surface Rendering Represents explicit scene surfaces (geometry with reflectance properties) Renders the scene from a given viewpoint under specified illumination Volume Rendering Represents optical properties at every 3D point Model absorption, emission, and (optionally) scattering Renders the scene by integrating light transport through the volume Can render smoke, clouds. The slide includes 2 embedded images alongside the bullets.

## Slide 4 — Radiance Field (Volumetric Rendering)
Specify light coming from every point to every direction Proportion of light reaching the camera Contribution from all pixels along the ray. The slide includes 4 embedded images alongside the bullets.

## Slide 5 — Neural Volume Rendering
Represent Radiance Field By a Neural Network Input: 3D coordinates Notice Lighting is fixed in the network. The slide includes 2 embedded images alongside the bullets.

## Slide 6 — Training NeRF model
Training data Set of images with known camera poses Loss function Use volume rendering to regenerate training images Compare with ground truth using L2 Loss. The slide includes 1 embedded image alongside the bullets.

## Slide 7 — NeRF MLP Network
Fully Connected Layers with ReLU activation Inpit Pixel position(x) View Direction (d) Output Color(RGB) Volume Density. The slide includes 1 embedded image alongside the bullets.

## Slide 8 — Spectral Bias in Fully-Connected Networks
MLP is a composition of smooth functions Each layer acts as a low-pass Difficult to model sharp changes Sharp output change with a small input change Gradient Descent favors smoothness Stable propagation Spectral bias also exists in other architectures Convolution, Transformers NeRF Difficult to learn sharp edges/object bondaries.

## Slide 9 — NeRF Position Encoding
Re-encode the input so sharp changes in input becomes slow varying. The slide includes 2 embedded images alongside the bullets.

## Slide 10 — NeRF: Position Encoding
Transform low-dimensional input into high-dimensional. The slide includes 1 embedded image alongside the bullets.

## Slide 11 — Hierarchical Volume Sampling
Conventional ray marching is inefficient Sample many empty space points or points of occluded regions Use two neural models, same architecture Coarse model to sample space uniformly Used to estimate high volume density (density on larger segments) Fine model, sample based on the estimated PDF of density Trained jointly(fine model on samples from coarse models). The slide includes 2 embedded images alongside the bullets.

## Slide 12 — Training Details
Train fine/coarse models simultaneously 64 points per ray with coarse network, 192 with fine network Total training points per ray: 256 762K rays per image, 200M queries per image 560K learned parameters. The slide includes 1 embedded image alongside the bullets.

## Slide 13 — Pose Estimation
Training NeRF requires multiple views with known camera poses Use SfM backbone for estimating camera poses. The slide includes 1 embedded image alongside the bullets.

## Slide 14 — Pose Estimation
COLMAP SfM package Backbone for pose estimation. The slide includes 1 embedded image alongside the bullets.

## Slide 15 — Tools
COLMAP. Backbone for pose estimation from multiple images. NERFSTUDIO. Train from images with COLMAP-estimated poses, generate novel views. The slide includes 2 embedded images alongside the bullets.

## Slide 16 — Typical Image Requirements
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Typical Image Requirements'.

## Slide 17 — Capturing from Video
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Capturing from Video'.

## Slide 18 — Rendering Model Output
[TABLE] Signal / Label | How It Is Rendered | Primary Uses Depth | Expected distance along ray | Depth estimation, 3D reconstruction Normals | Gradient of density field | Shape learning, robotics Accumulation / Opacity | Sum of ray weights | Foreground masks Point Cloud / Geometry | Backproject depth using intrinsics | Mapping, simulation Multi-View Correspondence | Render same 3D point from multiple cameras | Matching, triangulation Optical Flow | Reproject 3D points between poses | Motion networks Occlusion Mask | Depth comparison across views | Tracking, segmentation Stereo Pairs | Render two cameras with fixed baseline | Stereo training Disparity | Inverse depth difference | Depth-from-stereo Scale-Consistent Trajectories | Move camera in metric steps | Robotics, VO Semantic Masks | Train NeRF with class supervision | Scene understanding Instance Segmentation | Object-aware radiance fields | Detection pipelines. The slide includes 1 table alongside the bullets.

## Slide 19 — Volume Rendering Math
Section divider; the deck transitions to material on volume rendering math.

## Slide 20 — Ray Equation
For each image pixel, cast a ray from the camera through the volume If the ray “hits” a particle at distance t, we return its color C(t). The slide includes 1 embedded image alongside the bullets.

## Slide 21 — Probabilistic Interpretation
Probability of hitting the point Probability of reaching a point (transmittance) : T(t) Not blocked by previous points along the ray (“hits the point”) that are closer to the camera Overall. The slide includes 2 embedded images alongside the bullets.

## Slide 22 — Taylor Expansion for finding transmittance
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Taylor Expansion for finding transmittance'.

## Slide 23 — Rendering
Probability(PDF) that a point hits a point (small volume around it) Accumulated Color Contribution Change probabilistic interpretation to mixture. The slide includes 2 embedded images alongside the bullets.

## Slide 24 — Ray Marching
Discreet evaluation of the integral. The slide includes 5 embedded images alongside the bullets.

---

## Deck-level takeaway
The deck spans 24 slides, opening with "NeRF: Neural Radiance Field" and closing with "Ray Marching". Body-text coverage is 79%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include NeRF Position Encoding, NeRF: Position Encoding, Hierarchical Volume Sampling, Training Details.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3860_Vision_Model3D/3863_NeuralRF/slides/`.
