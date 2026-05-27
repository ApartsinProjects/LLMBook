# 5013_Audio_VectorQuant — Per-Slide Summary

**Source file:** `5013_Audio_VectorQuant.pptx`
**Source folder:** `SlidesPool/5012_Audio_Processing/`
**Drive link:** https://drive.google.com/file/d/1ENFzS3dpRxiAfj-n2bHlc1yfY5fYd508/view
**Slide count (exact, via python-pptx):** 13
**Extraction:** Local parse + slide PNG render. Several slides carry diagrams (Voronoi cells, RVQ layouts, Gumbel softmax curves, Wav2Vec 2.0 quantization module) that were visually inspected.

---

## Slide 1 — Vector Quantization
Title slide for the vector quantization sub-chapter on turning continuous audio into discrete tokens.

## Slide 2 — Vector Quantization
Vector quantization represents audio samples with a finite codebook so the network can treat audio as tokens. The worked example uses a 20 ms window at a 4 kHz sampling rate, yielding an 80-dimensional real-valued vector, then maps it through a codebook of size 1024, which compresses the chunk to a 10-bit index. The accompanying scatter plot visualizes Voronoi cells: each codeword is the centroid of all points closer to it than to any other codeword.

## Slide 3 — RVQ: Residual Vector Quantization
Residual vector quantization stacks several codebooks so the signal is encoded at multiple resolutions. The first codebook captures the coarse approximation; subsequent codebooks quantize the residual error of the previous stage. The diagrams contrast a single VQ stage with a cascade of RVQ stages where each block subtracts its quantized output from the input before passing the residual to the next quantizer.

## Slide 4 — RVQ and autoregressive generative tasks
For autoregressive generation with RVQ, the deck contrasts four token-layout patterns: flattening, parallel, VALL-E, and delay. Generating "entire code from all codebooks in a single step" trades fidelity for speed; running multiple steps per token gives higher fidelity at higher latency; the delay pattern starts predicting the coarse next token while still refining the previous one. A side panel adds the codebook projection step where sinusoidal positional embeddings corresponding to t=1..k1 are summed before the decoder.

## Slide 5 — Product Quantization
Product quantization splits the input vector into chunks and quantizes each chunk independently with its own codebook. With G groups and K codewords per group, the effective vocabulary grows multiplicatively to K^G, which is far cheaper than maintaining one giant codebook.

## Slide 6 — Encoder
The neural encoder applies residual quantization end to end, using a 1024-entry codebook (10 bits) and a 13 ms window. The diagram shows the audio waveform passing through convolutional layers and being projected onto the RVQ codebook stack to produce the discrete token stream.

## Slide 7 — Differentiable Quantization
Section divider introducing the trick that makes codebooks learnable by gradient descent rather than by k-means.

## Slide 8 — Conventional Quantization
Conventional quantization selects the codeword closest in Euclidean distance to the input vector. The codebook entries are parameters, but the argmax selector is not differentiable, so a standard backpropagation pipeline cannot train the codebook from a downstream loss.

## Slide 9 — Plan
The slide outlines three tricks that together make codebook selection differentiable. Trick 1 reformulates selection as multiplication by a one-hot vector. Trick 2 relaxes the one-hot to a SoftMax that, with a small temperature, looks almost one-hot. Trick 3 samples from the SoftMax over logits rather than averaging, and uses the Gumbel-Max trick (adding Gumbel noise before a low-temperature SoftMax) to make sampling itself differentiable.

## Slide 10 — Background: Reparameterization Trick
The reparameterization trick samples from a continuous distribution through a differentiable operation, so a network can learn the distribution parameters. The Gaussian example writes z = mu + sigma * epsilon with epsilon drawn from N(0,1), keeping mu and sigma in the gradient path while leaving randomness in a frozen noise source.

## Slide 11 — Background: Gumbel-Max Trick
The Gumbel-Max trick is the categorical analogue: instead of multinomial sampling, the model adds Gumbel noise to the logits and takes the argmax. The argmax itself is not differentiable, so a low-temperature SoftMax relaxation is used, producing almost-one-hot vectors whose probabilities can be learned by backpropagation. The Gumbel variables stay random, but the categorical logits become trainable. The slide also notes the pronunciation as "gum-bal".

## Slide 12 — Example
Two density plots compare plain SoftMax with Gumbel SoftMax over the same logits. The plain SoftMax curve is smooth, while the Gumbel SoftMax draws sharp, near-one-hot samples whose mass concentrates on the argmax category, illustrating how the trick approximates discrete sampling while remaining differentiable.

## Slide 13 — Differentiable Quantization Layer (Wav2Vec 2.0)
The Wav2Vec 2.0 quantization module is shown as a concrete instance. It uses product quantization with two groups and two codebooks. Multiplying the latent feature by the quantization matrix produces logits over three candidate codewords in each codebook; a Gumbel SoftMax converts these logits into almost-one-hot selection vectors. A second multiplication by a projection matrix maps the selected IDs back to feature-vector centroids. Both the quantization and projection matrices are trainable parameters, so the codebook itself is learned end to end.

---

## Deck-level takeaway
The deck explains how raw audio is compressed into a discrete token stream for downstream transformer models. It moves from plain vector quantization through residual and product variants used in modern codecs like EnCodec and SoundStream, then tackles the central training obstacle: argmax codeword selection is not differentiable. The solution layered across the second half (one-hot reformulation, SoftMax relaxation, Gumbel-Max sampling, reparameterization trick) produces the Gumbel-SoftMax quantizer that powers Wav2Vec 2.0 and similar self-supervised audio encoders, allowing the codebook to be learned jointly with the rest of the network. The concluding Wav2Vec 2.0 module ties theory to a familiar production architecture and makes the connection between codebook design, autoregressive token layout (relevant to AudioLM, VALL-E, MusicGen), and end-to-end training.
