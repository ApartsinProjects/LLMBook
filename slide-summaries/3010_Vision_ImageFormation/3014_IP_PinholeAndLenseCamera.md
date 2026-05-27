# 3014_IP_PinholeAndLenseCamera — Per-Slide Summary

**Source file:** `3014_IP_PinholeAndLenseCamera.pptx`
**Source folder:** `SlidesPool/3010_Vision_ImageFormation/`
**Drive link:** https://drive.google.com/file/d/1uZSultj7i_Df2FWqfaEjFqNdLNQqdQsm/view
**Slide count (exact, via python-pptx):** 32
**Extraction:** Local parse + slide PNG render. 8 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — Pinhole & Lens Camera
Section divider; the deck transitions to material on pinhole & lens camera.

## Slide 2
Let’s design a camera. Put a piece of film(sensor array) in front of an object - do we get a reasonable image? Blurring - need to be more selective! The slide includes 1 embedded image alongside the bullets.

## Slide 3
Let’s design a camera (cont’d). Add a barrier (aperture) with a small opening to block off most of the rays. The slide includes 1 embedded image alongside the bullets. Speaker notes: It gets inverted

## Slide 4 — Pinhole cameras
Abstract camera model - box with a small hole in it. Pinhole cameras work in practice. The slide includes 1 embedded image alongside the bullets. Speaker notes: The point to make here is that each point on the image plane sees light from only one direction, the one that passes through the pinhole.

## Slide 5 — Mathematic Model
Same geometry if the image plane is before the pinhole (“center f projection”). The slide includes 1 embedded image alongside the bullets.

## Slide 6 — Camera Obscura
Mo Tzu, 470-390BCE. The slide includes 1 embedded image alongside the bullets.

## Slide 7 — Distant objects are smaller
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Distant objects are smaller'.

## Slide 8 — Parallel lines meet
Common to draw film plane in front of the focal point. Moving the film plane merely scales the image. The slide includes 1 embedded image alongside the bullets.

## Slide 9 — Vanishing points and lines
Parallel lines in the world intersect in the image at a “vanishing point”. The slide includes 1 embedded image alongside the bullets. Speaker notes: Go to board, sketch out various properties of vanishing points/lines

## Slide 10 — Vanishing points and lines
Section divider; the deck transitions to material on vanishing points and lines.

## Slide 11 — The equation of projection
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'The equation of projection'.

## Slide 12 — Projection can be tricky…
Slide source: Seitz. The slide includes 1 embedded image alongside the bullets.

## Slide 13 — Projection can be tricky…
Slide source: Seitz. The slide includes 1 embedded image alongside the bullets.

## Slide 14 — Projective Geometry
What is lost? Length. Which is closer? Who is taller? The slide includes 1 embedded image alongside the bullets.

## Slide 15 — Projective Geometry
What is lost? Length Angles. Perpendicular? Parallel? The slide includes 1 embedded image alongside the bullets.

## Slide 16 — Projective Geometry
What is preserved? Straight lines are still straight. The slide includes 1 embedded image alongside the bullets.

## Slide 17 — Other Planar Transformations
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Other Planar Transformations'.

## Slide 18 — Homogeneous Coordinates
Planar transformation becomes matrix multiplication (Linear operator) Can ignore third coordinate (2x3 matrix) or define equivalence (x,y,z)<-> (x/a, y/a, z/a). The slide includes 1 embedded image alongside the bullets.

## Slide 19 — 2D Planar Transformation
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic '2D Planar Transformation'.

## Slide 20 — 3D Transformation
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic '3D Transformation'.

## Slide 21 — LENS CAMERA
Section divider; the deck transitions to material on lens camera.

## Slide 22 — Problems with pinhole camera
Need a very small aperture to allow light only from a single direction Large aperture makes images blurry Small aperture Very little light is passing (dark images) Diffraction effect. The slide includes 1 embedded image alongside the bullets.

## Slide 23 — Diffraction
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'Diffraction'.

## Slide 24
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic ''.

## Slide 25 — The reason for the lenses
Circle of confusion. The slide includes 1 embedded image alongside the bullets.

## Slide 26 — Thin lens
Visual slide containing 1 embedded figure with no body text; the visual carries the content of the topic 'Thin lens'.

## Slide 27 — Thin lens equation (cont’d)
f u v image. f,  focal distance (lens property) u- distance to the scene point v, where all the rays from the point meet. Speaker notes: And the set of all such points forms a plane parallel to the image (plane of focus).

## Slide 28 — Thin lens equation (cont’d)
The thin lens equation implies that only points at distance u from the lens are “in focus” (i.e., focal point lies on image plane). Other points project to a “blur circle” or “circle of confusion” in the image (i.e., blurring occurs). “circle of confusion”. The slide includes 1 embedded image alongside the bullets.

## Slide 29 — Depth of Field
The range of depths over which the world is approximately sharp (i.e., in focus). The slide includes 2 embedded images alongside the bullets. Speaker notes: Depth of field is the range of distance within the subject that is acceptably sharp.

## Slide 30 — How can we control depth of field?
The size of the blur circle is proportional to the aperture size. The slide includes 1 embedded image alongside the bullets.

## Slide 31 — How can we control depth of field? (cont’d)
Section divider; the deck transitions to material on how can we control depth of field? (cont’d).

## Slide 32 — Depth of field
Changing the aperture size or focal length affects depth of field. f / 5.6. f / 32. The slide includes 3 embedded images alongside the bullets.

---

## Deck-level takeaway
The deck spans 32 slides, opening with "Pinhole & Lens Camera" and closing with "Depth of field". Body-text coverage is 62%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Projection can be tricky…, Projection can be tricky…, Projective Geometry, Projective Geometry.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3010_Vision_ImageFormation/3014_IP_PinholeAndLenseCamera/slides/`.
