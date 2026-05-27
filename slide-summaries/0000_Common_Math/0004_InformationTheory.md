# 0004_InformationTheory — Per-Slide Summary

**Source file:** `0004_InformationTheory.pptx`
**Source folder:** `SlidesPool/0000_Common_Math/`
**Drive link:** https://drive.google.com/file/d/1T-_FQ3uAcSjgvO13Oj1CErfqKU-xyevb/view
**Slide count (exact, via python-pptx):** 42
**Extraction:** Local parse + slide PNG render. Visually inspected 13 image-bearing slides (dividers, encoder block diagrams, formula plates, and image-entropy worked examples) where math, matrices, and curves carry the meaning that the text body alone cannot convey.

---

## Slide 1 — ELEMENTS OF INFORMATION THEORY
Title divider opening the deck on the elements of information theory.

## Slide 2 — IMAGE COMPRESSION MODELS
Section divider introducing image compression as the application driving the information-theoretic machinery.

## Slide 3 — General Model For Image Encoding
The slide presents the canonical communication chain for image transmission. A block diagram traces the signal $f(x,y)$ through a source encoder, then a channel encoder, across the channel, and back through a channel decoder and source decoder to produce the reconstruction $\hat{f}(x,y)$. The two bullets summarize the division of labor: the source encoder removes redundancy to compress the data, while the channel encoder injects controlled redundancy to fight noise. This duality between compression and protection is the conceptual scaffold the rest of the deck builds on.

## Slide 4 — Source Encoder and Decoder
The slide is dominated by a two-row block diagram that decomposes each side of the source codec. The encoding pipeline is Mapper, Quantizer, Symbol encoder, while the decoder mirrors it with Symbol decoder and Inverse mapper that reproduces $\hat{f}(x,y)$. The decomposition isolates three distinct compression mechanisms: spatial decorrelation by the mapper, irreversible precision loss in the quantizer, and entropy coding in the symbol encoder. No prose accompanies the figure, leaving the diagram to carry the architectural argument.

## Slide 5 — Channel Encoder and Decoder
The channel codec injects a controlled form of redundancy to reduce the impact of noise. A simple illustration is appending parity bits to the transmitted data so that the minimum Hamming distance between valid codewords grows. Increasing this minimum distance is what allows the receiver to detect and correct bit flips. The slide frames coding-theoretic protection as deliberately enlarging the gap between legitimate messages.

## Slide 6 — Example: 7-bit Hamming code
The slide makes the parity-bit idea concrete with the classic (7,4) Hamming code. Four information bits $b_0, b_1, b_2, b_3$ are augmented with three parity bits $h_1, h_2, h_4$ computed as XORs of selected information bits, while $h_3, h_5, h_6, h_7$ carry the data through directly. The displayed equations show $h_1 = b_3 \oplus b_2 \oplus b_0$, $h_2 = b_3 \oplus b_1 \oplus b_0$, and $h_4 = b_2 \oplus b_1 \oplus b_0$. The take-away is that this overhead of three extra bits suffices to detect and correct any single-bit error in the seven-bit codeword.

## Slide 7 — Measuring Information
The slide opens the entropy thread by asking how few data are actually needed to represent an image without loss. Two boundary examples set intuition. A source that emits 0 or 1 with probability one half delivers exactly one bit of information per arrival. A source that emits 0 with probability one carries no information at all, because the observer already knew what would arrive. Information, therefore, must be measured against the uncertainty the receiver had before the symbol came.

## Slide 8 — Measuring Information
The slide formalizes the previous intuition. For a random event $E$ occurring with probability $p(E)$, the self-information is $I(E) = -\log_2 p(E)$, measured in bits. The functional form ensures that almost-sure events contribute almost zero information, while rare events deliver large surprise. The slide commits to a logarithmic definition without yet justifying why the logarithm is the natural choice.

## Slide 9 — Why log?
The slide explains the logarithm by appealing to additivity over independent experiments. A single die with $n=6$ outcomes requires $\log n$ bits to describe its uncertainty. Two independent dice with $n$ and $m$ outcomes can be encoded either separately, costing $\log n + \log m$ bits, or jointly across $nm$ combined outcomes, costing $\log(nm)$. The identity $\log(mn) = \log m + \log n$ is precisely what makes the two views consistent, so the logarithm is the unique well-behaved measure that captures additivity of independent uncertainties.

## Slide 10 — The Information Channel
The slide introduces the channel as the physical medium that links source and user. The driving question is how much information the channel can transfer, which the deck calls its capacity. This sets up the formal definitions of source, output alphabet, and conditional probabilities that follow.

## Slide 11 — The source
The source is modeled as a discrete random variable producing letters from a finite set of source symbols, with probabilities that sum to one. This minimal setup is enough to begin computing per-symbol information content. It also gives the receiver a probability model that is the precondition for any compression argument.

## Slide 12 — Average Information
The slide derives the per-symbol average information by frequency counting. If the source emits $k$ symbols, each symbol appears on average $k \cdot P(a_j)$ times. Summing the self-information contributions and dividing by $k$ yields the average information per source output, which is the entropy. The argument shows that entropy emerges naturally from sample-average self-information as the sequence grows long.

## Slide 13 — Uncertainty or Entropy of the Source
The slide names the resulting quantity. Entropy $H(z) = -\sum_j P(a_j) \log P(a_j)$ is the average information in bits transferred by a single source symbol. This is the same uncertainty interpretation Shannon adopted and is the central scalar of the deck.

## Slide 14 — Channel Alphabet
The slide turns to the channel output. Output symbols take values from a separate alphabet, and the probability of each output is computed by the complete probability formula $P(b_k) = \sum_j P(b_k \mid a_j) P(a_j)$. This links the input distribution and the channel transitions into the marginal distribution observed at the receiver.

## Slide 15 — Forward Channel Transition Matrix
The slide displays the forward transition matrix $Q$ whose entry in row $k$, column $j$ is the conditional probability $P(b_k \mid a_j)$ of receiving output $b_k$ given input $a_j$. Stacking input probabilities as $z = \{P(a_1), \dots, P(a_J)\}$ and output probabilities as $v = \{P(b_1), \dots, P(b_K)\}$, the channel acts linearly as $v = Q z$. This compact algebraic form is the workhorse for all subsequent capacity and mutual-information arguments.

## Slide 16 — Conditional Entropy
The slide asks how much information about the source symbol remains uncertain after observing a particular output $b_k$. The conditional entropy function $H(z \mid b_k) = -\sum_j P(a_j \mid b_k) \log P(a_j \mid b_k)$ measures that residual. Averaging over all output symbols $b_k$ produces the global conditional entropy $H(z \mid v)$. This is the formal hook for the equivocation concept that follows.

## Slide 17 — Equivocation
Equivocation is the average information still missing about a source symbol once the corresponding output has been observed. It is the receiver's residual uncertainty about what was sent. The cleaner the channel, the smaller the equivocation.

## Slide 18 — Mutual Information
The slide defines mutual information as the difference between what the receiver wants and what it still lacks. $H(z)$ is the average information per source symbol, $H(z \mid v)$ is the average information still missing after observation, and the difference $I(z, v) = H(z) - H(z \mid v)$ is the average information that actually crossed the channel. Mutual information thus measures effective communication, not raw source entropy.

## Slide 19 — Mutual Information
The slide reinforces the formula $I(z, v) = H(z) - H(z \mid v)$ and expands both pieces in coordinates. The conditional entropy is written as $H(z \mid v) = -\sum_{k=1}^{K} \sum_{j=1}^{J} P(a_j, b_k) \log P(a_j \mid b_k)$ alongside $H(z) = -\sum_{j=1}^{J} P(a_j) \log P(a_j)$. The transition matrix $Q$ is shown a second time, and a final form expresses mutual information directly in terms of the input probabilities and the matrix entries $q_{kj}$: $I(z, v) = \sum_{j=1}^{J} \sum_{k=1}^{K} P(a_j) q_{kj} \log \frac{q_{kj}}{\sum_i P(a_i) q_{ki}}$. The reader is invited to prove the algebraic identity at home.

## Slide 20 — Channel Capacity
Channel capacity is the maximum amount of information the channel can transmit per use, where the maximum is taken over all admissible input distributions. Capacity sets the upper limit on the transmission rate. It is a property of the channel alone because it depends only on the conditional probabilities defining the channel, not on the actual source statistics.

## Slide 21 — Example: Binary Source
The slide instantiates entropy for a binary source $A = \{0, 1\}$ with $P(a_1) = p_{bs}$ and $P(a_2) = 1 - p_{bs} = \bar{p}_{bs}$. The entropy then collapses to a single-parameter function $H(z) = H(p_{bs}) = -p_{bs} \log_2 p_{bs} - \bar{p}_{bs} \log_2 \bar{p}_{bs}$. The accompanying chart plots this binary entropy versus $p_{bs}$, showing the familiar symmetric arch peaking at 1 bit per symbol at $p_{bs} = 0.5$ and falling to zero at the deterministic endpoints. Maximum uncertainty sits at the fair coin.

## Slide 22 — Example
The slide assumes a noisy binary channel known as the Binary Symmetric Channel, where 0 and 1 each flip to the other with equal probability $p_e$. Given the input distribution, the output probabilities follow directly from the complete probability formula. The BSC is the canonical toy channel used to expose capacity calculations.

## Slide 23 — Example: Mutual Information
The slide gives the closed-form mutual information for the BSC. The displayed identity is $I(z, v) = H(z) - H(z \mid v) = H_{bs}(p_e p_{bs} + \bar{p}_e \bar{p}_{bs}) - H_{bs}(p_e)$, again with the proof left as a home exercise. A chart of mutual information versus the source probability $p_{bs}$ at fixed error probability is overlaid. The curve is a flattened arch capped well below 1 bit per symbol, with the dashed horizontal asymptote labeled $1 - H_{bs}(p_e)$ marking the ceiling that can be reached by choosing the optimal input distribution.

## Slide 24 — Channel Capacity
The slide identifies the capacity of the BSC. The mutual information is maximized at the equiprobable input $p_{bs} = 1/2$, and the resulting capacity is $C = 1 - H_{bs}(p_e)$. The plot shows capacity as a function of the bit-flip probability $p_e$: a U-shape that reaches its maximum of 1 bit at $p_e = 0$ and $p_e = 1$, the two noiseless extremes, and collapses to zero at $p_e = 0.5$, where the channel destroys all information.

## Slide 25 — FUNDAMENTAL CODING THEOREMS
Section divider opening the second half of the deck, devoted to Shannon's coding theorems.

## Slide 26 — Example
The slide motivates entropy coding with a worked example. A source emits 0 with probability 2/3 and 1 with probability 1/3, giving entropy $H(z) = 0.918$. A single-bit code wastes capacity, costing $L = 1 > H(z)$. Encoding the four length-two sequences 00, 01, 11, 10 with the variable-length codewords 0, 10, 110, 111 yields an average code length of 1.89 bits for a pair, or 0.945 bits per symbol, much closer to the entropy bound. Block coding lowers the per-symbol cost.

## Slide 27 — Noiseless Coding Theorem
The slide states Shannon's first theorem under idealized assumptions: no noise in the channel so that $Q$ is a zero-one matrix, a zero-memory source where the next symbol does not depend on previous ones, and an $n$-symbol alphabet with entropy $H(z)$. The theorem guarantees that the average bits per symbol can be brought arbitrarily close to the source entropy by encoding sufficiently long blocks of symbols. Block codes saturate the entropy bound in the limit.

## Slide 28 — Noisy Coding Theorem
A simple way to cope with noise is repetition: send each symbol several times (111 instead of 1) and decode by majority vote. The receiver treats some patterns such as 101 or 010 as invalid codewords, which signals an error and triggers correction. The slide foreshadows the more general block-coding framework with rate $R$ and capacity $C$.

## Slide 29 — Noisy Coding Theorem
The slide generalizes repetition into block coding. Sequences of length $n$ are encoded into longer codewords of length $r > n$, and only $2^n$ of the $2^r$ possible codewords are valid. The code rate $R = n/r$ measures information bits per transmitted bit. This trade between rate and protection is what the noisy coding theorem will optimize.

## Slide 30 — Noisy Coding Theorem
The slide states Shannon's second theorem. For any rate $R$ strictly less than capacity $C$, there exists a code of rate $R$ whose block decoding error probability can be made arbitrarily small. Reliable communication is achievable below capacity and impossible above it.

## Slide 31 — The source coding theorem
The slide pivots to lossy compression by repurposing the channel model. Each symbol $a_j$ is encoded and decoded into some output $b_k$ with probability $q_{kj}$, and a distortion measure assigns a cost to representing $a_j$ by $b_k$. The original message is allowed to be distorted in exchange for fewer bits, which is the essence of lossy image coding.

## Slide 32 — Average Distortion
Average distortion depends on the encoding matrix $Q$ and the chosen distortion measure. The design problem is to find the best $Q$ subject to the constraint that average distortion stays below a given budget $D$. The matrix $Q$ then plays a dual role as both an encoding and decoding scheme.

## Slide 33 — Rate Distortion Function
The slide defines the rate distortion function. Among all encoding schemes that meet the distortion budget $D$, $R(D)$ is the minimum value of the mutual information $I(z, v) = H(z) - H(z \mid v)$. Mutual information here counts the information that the lossy encoder actually transmits, since $H(z)$ is the source information and $H(z \mid v)$ is what remains hidden after the encoded output is seen. $R(D)$ is a property of the source alone and tells the designer how few bits per symbol suffice to achieve distortion no worse than $D$.

## Slide 34 — Example: Find Rate Distortion Function
The slide sets up a worked rate-distortion problem for a simple binary source with equally probable symbols 0 and 1 and a simple distortion measure. The optimization minimizes $I(z, v)$ subject to $K+1 = 3$ constraints, and Lagrange multipliers are introduced as the natural tool. The example previews the general technique before plunging into the algebra.

## Slide 35 — Example
The slide outlines the mechanics of the constrained optimization. An augmented criterion function is formed, four partial derivatives with respect to the entries of $q$ are set to zero, and the result is a system of seven equations in seven unknowns (four from the derivatives plus three from the constraints). The reader is told to solve the system at home or consult the textbook.

## Slide 36 — Example: Solution
The slide reports the answer: the rate distortion function for the binary source is $R(D) = 1 - H_{bs}(D)$. A chart of $R(D)$ versus $D$ shows a monotonically decreasing convex curve starting at 1 bit per symbol when $D = 0$ and falling to zero at $D_{\max} = 0.5$. The endpoints are interpreted directly: with zero distortion the source needs at least one bit per symbol, while at distortion 0.5 no bits are needed because the decoder can simply toss a coin.

## Slide 37 — Source Coding Theorem
The slide states the lossy source coding theorem. For any tolerance, there exists a block length $r$ and a code whose rate is arbitrarily close to $R(D)$ and whose average per-symbol distortion stays within budget. The slide then closes the loop with the information transmission theorem: if channel capacity exceeds the rate distortion function, the source can be recovered with arbitrarily small probability of failure, joining lossy compression and noisy transmission into a single sufficient condition.

## Slide 38 — Summary
The slide collects Shannon's four theorems in one place. The first (noiseless, lossless) says entropy $H(z)$ is the floor of bits per symbol and that long codewords approach this floor. The second (noisy, lossless) shows that channel capacity $C$ bounds reliable rate and that long codewords drive the error rate to zero as long as $R < C$. The third (source coding, lossy, noiseless) introduces the rate distortion function $R(D)$ as the bit-cost floor at a given distortion budget. The fourth (information transmission, lossy, noisy) combines both regimes, allowing distortion and noise simultaneously and guaranteeing nearly perfect recovery up to distortion $D$ whenever $R(D) < C$.

## Slide 39 — Example: Computing The Entropy of an Image
The slide computes a first-order entropy for a small toy image. Assuming independent gray levels with a uniform distribution at each pixel gives a maximum-entropy estimate of $H(z) = 8$ bits per pixel. An 8x4 pixel grid is displayed with values stepping through 21, 21, 21, 95, 169, 243, 243, 243 across each row, making clear that the uniform-pixel assumption ignores the strong repetition visible in the data.

## Slide 40 — Example
The slide refines the estimate by computing the empirical histogram of gray levels from the same image. The table lists gray levels 21, 95, 169, 243 with counts 12, 4, 4, 12 and probabilities 3/8, 1/8, 1/8, 3/8. Plugging these into the entropy formula yields $H(z) = 1.81$ bits per pixel, or about 58 bits total for the 32-pixel image. Honest probability estimation has already shrunk the bit budget by more than a factor of four.

## Slide 41 — Example
The slide pushes further by treating horizontal pixel pairs as the unit of analysis, capturing dependence between adjacent pixels. A table enumerates the six observed gray-level pairs (21, 21), (21, 95), (95, 169), (169, 243), (243, 243), (243, 21) with counts 8, 4, 4, 4, 8, 4 and probabilities 1/4, 1/8, 1/8, 1/8, 1/4, 1/8. The resulting block entropy is 2.5 bits per pair, giving 1.25 bits per pixel as a second-order estimate. Modeling spatial correlation strips out yet more redundancy.

## Slide 42 — Example: Difference Encoding
The slide demonstrates predictive coding by replacing each pixel with the difference from its left neighbor (the first column is kept as is). Side by side, the original gray values 21, 21, 21, 95, 169, 243, 243, 243 become the residuals 21, 0, 0, 74, 74, 74, 0, 0, producing a much more skewed distribution. The histogram of residuals collapses to three symbols (0, 21, 74) with probabilities 1/2, 1/8, 3/8 and yields $H(z) = 1.44$ bits per pixel. Decorrelation by a linear predictor is shown to be a powerful and almost free way to lower the entropy of natural-looking image data.

---

## Deck-level takeaway
The deck builds Shannon's information theory from the ground up with a steady eye on image coding as the application. It starts with the duality of source compression and channel protection, defines self-information and entropy with a careful justification of the logarithm, then formalizes the channel through transition matrices, conditional entropy, equivocation, mutual information, and capacity. The Binary Symmetric Channel runs as a worked example throughout, producing the iconic binary entropy curve, the mutual information arch, and the capacity formula $C = 1 - H_{bs}(p_e)$.

The second half lays out all four Shannon coding theorems in a unified picture: noiseless coding hits the entropy bound, noisy coding hits capacity, source coding hits the rate distortion function $R(D)$, and information transmission joins them with the condition $R(D) < C$. The closing image examples make the abstract bounds tangible by showing how naive uniform models cost 8 bits per pixel while honest histograms, block modeling, and a one-step predictive difference encoder drive that cost down to 1.81, 1.25, and 1.44 bits per pixel respectively on the same toy image. The deck is a compact bridge from information-theoretic first principles to the practical levers behind real image compressors.
