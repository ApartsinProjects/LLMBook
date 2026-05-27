# 2506_GAN_Music — Per-Slide Summary

**Source file:** `2506_GAN_Music.pptx`
**Source folder:** `SlidesPool/2500_GAI_GAN/`
**Drive link:** https://drive.google.com/file/d/1kPEVc-6l6LNev_QuS_tNibeAvIAhWZh8/view
**Slide count (exact, via python-pptx):** 20
**Extraction:** Local parse + slide PNG render. Pure-text body bullets carry most semantics; code-screenshot and visualization slides were inspected visually.

---

## Slide 1 — MuseGAN
Title slide for music generation with GANs (MuseGAN).

## Slide 2 — Digital Music Representation
Section-header slide introducing how music is represented numerically.

## Slide 3 — Notes, Octave, Pitch
A figure recaps notes, octaves, and pitch (treated here as note number).

## Slide 4 — Multitrack Music
The slide formalizes multitrack music. A track is a sequence of bars; a bar is a segment defined by beats (typically 4 per bar in 4/4 time). Each beat has a note duration and is subdivided into steps; each step contains a note in the range 0-83, encoded as an 84-dim one-hot. Tempo is set by a metronome mark (BPM). The training dataset is JSB Chorales with 4 tracks per piece (4 vocal parts).

## Slide 5 — MIDI files
MIDI files store digital music; MusicScore software visualizes them as sheet music. Four panels show the sheet-music representation.

## Slide 6 — Piano Rolls
Four panels visualize the same MIDI files as piano rolls (time on x-axis, pitch on y-axis).

## Slide 7 — Music Tensor
Two panels show the tensorized representation: a (bars, steps, pitches, tracks) tensor with one-hot pitch encoding.

## Slide 8 — Latent/Noise Inputs
MuseGAN samples separate noise vectors for melody, chords, style, and groove. A temporal network expands the latent vectors to produce consistent inputs for subsequent bars. Chord noise is shared across tracks while melody noise is independent per track.

## Slide 9 — Melody: Temporal Network noise generation
A schematic shows the per-track temporal-network noise generation for each bar (noise shape 1x4x32).

## Slide 10 — Blueprint: Wasserstein GAN
A panel previews the architecture as a Wasserstein GAN with gradient penalty.

## Slide 11 — Preparing Data
Six code panels prepare the JSB Chorales data, using (-1, 1) instead of (0, 1) for the one-hot encoding to match the tanh-output activation.

## Slide 12 — Create midi file
A code panel reconstructs a MIDI file from generated tensors by accumulating note durations.

## Slide 13 — Background: 1D, 2D and 3D Convolutions
The slide recaps 1D convolution (across features), 2D (features plus area), and 3D (features plus area plus time depth).

## Slide 14 — A critic: return score
Two code panels define the WGAN critic that returns a Wasserstein score for a music tensor.

## Slide 15 — Temporal network: generate consistent noise for the second bar
A code panel implements the temporal network that, given the first-bar noise, produces consistent noise for the next bar.

## Slide 16 — BarGenerator: Generate single bar for a single track
Two code panels implement a BarGenerator module that synthesizes one bar for one track from the noise inputs.

## Slide 17 — MuseGenerator
Two code panels assemble the full MuseGenerator from BarGenerators (one per track per bar) and the temporal network.

## Slide 18 — Gradient Penalty
A code panel implements the WGAN-GP gradient penalty using random interpolations between real and fake music tensors.

## Slide 19 — Train Epoch
Six code panels show the per-epoch training loop alternating critic and generator updates.

## Slide 20 — Generating Music
Four code panels show the inference path: sample chord, style, melody, and groove noise; run the temporal network and BarGenerators; export to MIDI.

---

## Deck-level takeaway
MuseGAN extends the WGAN-GP recipe from images to multitrack music by tensorizing pieces as (bars, steps, pitches, tracks) and decomposing the latent input into chord, melody, style, and groove noise streams. A temporal network injects bar-to-bar consistency while shared BarGenerators synthesize each (track, bar) cell. The same Wasserstein critic plus gradient-penalty machinery that stabilizes face generation here generalizes to symbolic music, with the network's output decoded back into a standard MIDI file via duration accumulation.
