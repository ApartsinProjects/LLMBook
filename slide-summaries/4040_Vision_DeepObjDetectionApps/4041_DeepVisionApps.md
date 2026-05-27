# 4041_DeepVisionApps — Per-Slide Summary

**Source file:** `4041_DeepVisionApps.pptx`
**Source folder:** `SlidesPool/4040_Vision_DeepObjDetectionApps/`
**Drive link:** https://drive.google.com/file/d/1DSRF2pfoNj1Z1vnRl8WbV8CLCIgU_XsM/view
**Slide count (exact, via python-pptx):** 48
**Extraction:** Local parse + slide PNG render. 27 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Applications of Object Detection and Segmentation
Section divider; the deck transitions to material on applications of object detection and segmentation.

## Slide 2 — Fine-tuning object detection
Section divider; the deck transitions to material on fine-tuning object detection.

## Slide 3 — Detectron2 Platform
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Detectron2 Platform'.

## Slide 4 — Fetch subset from Open Images
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Fetch subset from Open Images'.

## Slide 5 — Select Classes To Predict
Fine-tune model trained don COCO data. The slide includes 1 embedded image alongside the bullets.

## Slide 6 — COCO label format
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'COCO label format'.

## Slide 7 — Configure detectron training
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Configure detectron training'.

## Slide 8 — Train the model
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Train the model'.

## Slide 9 — Inference
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'Inference'.

## Slide 10 — Results
Results slide with 1 screenshot showing the output of the previous step. The visual content typically pairs an input image, a model output, and/or a numerical metric.

## Slide 11 — Human pose detection
Section divider; the deck transitions to material on human pose detection.

## Slide 12 — Keypoint R-CNN
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Keypoint R-CNN'.

## Slide 13 — Reuse pretrained pose keypoints detection
Visual slide containing 4 embedded figures with no body text; the visual carries the content of the topic 'Reuse pretrained pose keypoints detection'.

## Slide 14 — Ultralytics Pose Estimation
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Ultralytics Pose Estimation'.

## Slide 15 — Crowd Counting
Section divider; the deck transitions to material on crowd counting.

## Slide 16 — Counting people
Identify center of the head keypoints. The slide includes 1 embedded image alongside the bullets.

## Slide 17 — Sparsity Problem
Most of the pixels are not keypoints Transform into the approximate density of the people #of people per unit of image area, heatmap Transform points to Gaussian and sum at each pixel Predict the actual number of people by summing up all pixels. The slide includes 3 embedded images alongside the bullets.

## Slide 18 — Dataset class
Dataset/sample slide containing 2 figures that visualise the data used at this point of the project pipeline.

## Slide 19 — VGG16-based model
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'VGG16-based model'.

## Slide 20 — Inference
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'Inference'.

## Slide 21 — Image Collarization
Section divider; the deck transitions to material on image collarization.

## Slide 22 — Colorization
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Colorization'.

## Slide 23 — CIFAR-10 Image Colorization
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'CIFAR-10 Image Colorization'.

## Slide 24 — U-Net Architecture
Visual slide containing 3 embedded figures with no body text; the visual carries the content of the topic 'U-Net Architecture'.

## Slide 25 — Input Images
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Input Images'.

## Slide 26 — 3D object detection with point clouds
Detecting pedestrians and vehicles.

## Slide 27 — 3D Object Detection
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic '3D Object Detection'.

## Slide 28 — LiDAR collected point clouds
Time-of-flight (ToF)based distance estimation. The slide includes 2 embedded images alongside the bullets.

## Slide 29 — Input Encoding
x,y,z and the intensity of the reflection. The slide includes 2 embedded images alongside the bullets.

## Slide 30 — Cast an object detection task
Encode 3D input 2D image, use RGB to encode 3D information Output encoding Encode 3D box parameters Start from several anchor 3D boxes Partition into a grid, a cell with a 3D box center owns the box.

## Slide 31 — Projecting Point Cloud to 2D
Generate a bird’s-eye view Project onto the XY plane Grid with 8cm^2 resolution per grid cell RGB Red: the distance to highest(z) point of the cell Greed: the intensity of highest(z) point of the cell Blue: normalized number of points in the cell Intuition Highest point overshadow points below. The slide includes 2 embedded images alongside the bullets.

## Slide 32 — Output Encoding
Predict Length and width and height of the object(in meters) Object class Object orientation(Yaw) Distance to the object Output x,y, l,w, and yaw Regress into intermediate values Relative to the grid cell center Normalize by class (vehicle, pedestrian) average size Offset of box center from cell center: sigma. The slide includes 6 embedded images alongside the bullets.

## Slide 33 — Illustration
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Illustration'.

## Slide 34 — Loss
YOLO loss Object detection loss Euler loss for orientation. The slide includes 2 embedded images alongside the bullets.

## Slide 35 — Sample Ground Truth Data
Dataset/sample slide containing 1 figure that visualise the data used at this point of the project pipeline.

## Slide 36 — Input image and encoding with GT
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Input image and encoding with GT'.

## Slide 37 — Predictions
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Predictions'.

## Slide 38 — Action Recognition From Video
Section divider; the deck transitions to material on action recognition from video.

## Slide 39 — MMAction Toolbox
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'MMAction Toolbox'.

## Slide 40 — CNN for Video Processing
2D Obtain feature maps for each video frame using a backbone VGG16, ResNet50 Pass results through temporal convolution 3D 3D convolution over 4D tensor FxCHW F- number of frames, C-channels, HW dimensions. Temporal convolution: across the temporal dimension Temporal pooling: across temporal dimension (avg, max). The slide includes 1 embedded image alongside the bullets.

## Slide 41 — Video snippets:
A single frame or few frame for computing modalities Result: a single frame. The slide includes 1 embedded image alongside the bullets.

## Slide 42 — Temporal Convolution
Several (not necessary consecutive ) frames. The slide includes 1 embedded image alongside the bullets.

## Slide 43 — Temporal Segmentation Network
Divide the video into segments A few short snippets randomly selected from each segment Score each snippet(spatial) or sequence of snippets(temporal) Aggregate scores for each segment by its snippet consensus Aggregate scores for video by segment score consensus. The slide includes 1 embedded image alongside the bullets.

## Slide 44 — MMA: Pretrained Model
Visual slide containing 6 embedded figures with no body text; the visual carries the content of the topic 'MMA: Pretrained Model'.

## Slide 45 — Training on a custom dataset: Kinetics
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Training on a custom dataset: Kinetics'.

## Slide 46 — Prepare configuration
Dataset/sample slide containing 2 figures that visualise the data used at this point of the project pipeline.

## Slide 47 — Ultralytics Solutions
Section divider; the deck transitions to material on ultralytics solutions.

## Slide 48 — Building solutions with detection and segmentation
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Building solutions with detection and segmentation'.

---

## Deck-level takeaway
The deck spans 48 slides, opening with "Applications of Object Detection and Segmentation" and closing with "Building solutions with detection and segmentation". Body-text coverage is 29%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Sparsity Problem, Dataset class, VGG16-based model, Inference.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/4040_Vision_DeepObjDetectionApps/4041_DeepVisionApps/slides/`.
