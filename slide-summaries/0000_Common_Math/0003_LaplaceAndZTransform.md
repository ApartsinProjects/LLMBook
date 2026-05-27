# 0003_LaplaceAndZTransform — Per-Slide Summary

**Source file:** `0003_LaplaceAndZTransform.pptx`
**Source folder:** `SlidesPool/0000_Common_Math/`
**Drive link:** https://drive.google.com/file/d/10ul-Zs9yE_JdU2Aphl0I1qd0oVk_DJQz/view
**Slide count (exact, via python-pptx):** 31
**Extraction:** Local parse + slide PNG render. Visually inspected 10 slides whose body was empty, whose body contained only equation stubs, or that mixed embedded images with terse text so that the rendered slide carried information missing from the text extraction.

---

## Slide 1 — LAPLACE TRANSFORM AND Z-Transform
Title slide that opens the module on Laplace and Z-transforms with the disclaimer "Intuition only, expect inaccuracies", warning readers that the deck pursues physical and geometric intuition rather than rigorous proofs. It sets the tone for an applied derivation of transforms in the context of LTI signal processing.

## Slide 2 — Unstable Systems
Section divider announcing the first thematic block on unstable systems.

## Slide 3 — Back to LTI Operator
Recap of linear time-invariant (LTI) operators as maps from time series to time series (or functions to functions). In the spatial domain an LTI operator is fully specified by its impulse response h(t), which is meaningful because Dirac and Kronecker deltas form a basis. In the frequency domain the same operator is specified by its complex frequency response H(u), because complex exponentials are eigenfunctions of any LTI operator. The frequency response therefore plays the role of the eigenvalue spectrum of the operator.

## Slide 4 — LTI recap, continued
Reminder that the (inverse) Fourier transform is the change-of-basis tool between the spatial and frequency views of LTI. A signal can be transformed to the frequency domain, the LTI operator can be applied as multiplication there, and the result can be transformed back. h(t) and H(u) constitute a Fourier pair, which is the standard way to swap representations.

## Slide 5 — The Limitation of Fourier Transform
The Fourier transform is well-defined only when the integral converges, which in practice requires finite power, equivalently finite area under the function. While real input signals rarely carry infinite power, the engineer often needs to analyze (or avoid) output signals and impulse responses that do diverge. This motivates a basis broader than pure complex sinusoids.

## Slide 6 — Finite vs. Infinite Impulse Response
Contrasts two LTI operators through their impulse responses. A finite impulse response (FIR) returns to zero after excitation, whereas a recursive LTI such as the integrator with response (..., 0, 1, 1, 1, ...) produces an infinite, yet still stable, impulse response that does not blow up to infinity and carries finite power on each interval. A small table tracking n, x, and h(n) illustrates a unit impulse at n=0 producing h(n)=1 for all n>=0, demonstrating infinite support without divergence.

## Slide 7 — Unstable LTI Systems
Introduces a Fibonacci-like recursive operator T(n) = x_n + y_{n-1} + y_{n-2} and shows that a single bounded input pulse can drive its impulse response sequence to unbounded growth (the table shows h(n) marching 1, 1, 2, 3, 5, 8). A bold-printed take-away states that Fourier basis functions cannot analyze such infinite-power signals, motivating the Laplace transform for continuous signals and the Z-transform for discrete sequences. A small photographic insert of a feedback amplifier in a workshop reinforces the "unstable" theme with a real-world cue.

## Slide 8 — Laplace Transform
Generalizes the LTI eigenbasis beyond pure imaginary exponentials e^{jut} to all complex exponentials g(s) = e^{st} = e^{(r+ju)t} = e^{rt} dot e^{jut}, indexed by an arbitrary complex number s = r + ju. The damped or growing factor e^{rt} multiplied by a sinusoid e^{jut} forms a richer basis of LTI operators and contains the Fourier basis as the special case r=0. The slide is illustrated with three stacked time-domain plots of cos(40t)e^{-1.5t}, cos(40t)e^{0t}, and cos(40t)e^{1.5t}, visualizing decaying, pure oscillating, and exploding eigenfunctions, respectively.

## Slide 9 — Bounded Signals
Repeats the basis function g_s(t) = e^{st} = e^{rt} dot e^{jut} and identifies the "problematic" cases: when r > 0 the magnitude |e^s| = |e^r e^{ju}| exceeds 1, meaning s lies outside the unit circle in the complex plane and the eigenfunction blows up. The same three plot stack from the previous slide reappears on the right to emphasize visually which regions of the s-plane correspond to bounded versus unbounded basis members.

## Slide 10 — Eigenfunctions Check
A two-step proof on a single slide. The first line uses the Dirac-delta sifting identity to write T[f(t)] as the convolution integral of f against the impulse response h, recovering the standard LTI form. The second line substitutes f(t) = e^{st} into that convolution and pulls e^{st} outside the integral, leaving lambda_s = integral e^{-sm} h(m) dm so that T[e^{st}] = lambda_s e^{st}. This shows that every complex exponential is an eigenfunction of any LTI operator with eigenvalue equal to the Laplace integral of the impulse response.

## Slide 11 — Laplace Transform
Presents the two-sided continuous Laplace transform as the natural extension of the Fourier integral to the full complex s-plane. The remark "Need 4D to visualize" reminds the reader that both the input plane (complex s) and the output (complex H(s)) are two-dimensional, so any picture is a projection. The inverse transform is flagged as algebraically tricky because the contour of integration lives in the complex plane.

## Slide 12 — LTI Operator in s-domain
Single-equation slide stating the transform-domain convolution identity: g(t) = T[f(t)] is equivalent to G(s) = H(s) dot F(s). The point is that the Laplace transform turns convolution into multiplication exactly as the Fourier transform does, but on a wider domain that admits unbounded signals.

## Slide 13 — From Laplace to Z-Transform
Section divider that pivots from continuous Laplace theory to the discrete-time Z-transform.

## Slide 14 — Discrete Case
Begins the bridge to discrete time. A continuous signal f(t) is sampled on a uniform grid, producing a sequence; a Dirac comb is introduced as the periodic train of deltas that multiplies f(t) to model this sampling. The resulting "continuous function after sampling" is zero between sample points and equals f at each sample, which sets up the algebraic manipulation on the following slide.

## Slide 15 — Discrete Case, continued
Applies the Laplace transform to the sampled function. Because the sampled signal is a weighted sum of shifted deltas, its Laplace transform collapses to a sum over samples of f(nT) e^{-snT}, which is the starting point for defining the Z-transform.

## Slide 16 — Discrete Case
Performs the change of variable z = e^{sT} on the Laplace integral of the sampled signal. The substitution converts the sum over samples into the Z-transform F(z) = sum f[n] z^{-n}, turning a discrete sequence f[n] into a continuous (complex-valued) function of z. This is presented as the constructive derivation of the Z-transform from the Laplace machinery, not as a separate axiomatic definition.

## Slide 17 — LTI Operator in z-domain
States the Z-domain counterpart of the spatial-domain convolution: in time the LTI output is y[n] = (h * x)[n] with a possibly infinite-support h, while in the Z-domain Y(z) = H(z) X(z). H(z) is named the transfer function of the LTI, the direct discrete analogue of the continuous frequency response.

## Slide 18 — Time-Shifting Property of z-transform
Derives the shift theorem of the Z-transform: shifting a sequence by k samples multiplies its Z-transform by z^{-k}. This is the workhorse identity that lets recursive difference equations be turned into algebraic equations on the next slides.

## Slide 19 — IIR Filters and System Stability
Section divider that opens an optional block on infinite-impulse-response (IIR) filters and stability analysis, marked "Not necessary for the course, optional".

## Slide 20 — Z-transform and Infinite Impulse Response Filters
Reminds the reader that an IIR filter is defined recursively, then writes the general linear difference equation relating current output to past outputs and present and past inputs. The expression is then rearranged so that all output terms are on one side, preparing it for a Z-transform.

## Slide 21 — IIR Filter
Applies the Z-transform to both sides of the recursive equation using the shift property and isolates Y(z)/X(z). The transfer function emerges as a ratio of two polynomials in z^{-1}, with numerator coefficients tied to the input taps and denominator coefficients tied to the feedback taps.

## Slide 22 — Transfer Function and Stability
Defines bounded-input bounded-output (BIBO) stability: an LTI operator is BIBO-stable when |f(t)| <= B implies |g(t)| = |T(f(t))| < D for all t. The slide adds the spectral viewpoint that a bounded signal must have zero coefficient in its Z- or Laplace-transform at every s with |e^s| > 1 (outside the unit circle). The familiar trio of damped, pure, and exploding cos(40t) plots returns at the right margin to remind the reader which transform-domain coordinates correspond to bounded basis functions and which do not.

## Slide 23 — Stability
Restates the stability criterion in operator form: a "good" LTI must not amplify or generate "bad exponents", which means H(s) must remain finite for all s with positive real part and H(z) must remain finite for all |z| > 1. For a recursive (IIR) filter this reduces to the requirement that every zero of the denominator polynomial of H(z), that is, every pole, lies strictly inside the unit circle of the complex z-plane.

## Slide 24 — End of Optional Material
Section divider closing the optional IIR stability block.

## Slide 25 — Upsampling and Downsampling in Z-domain
Section divider opening the final block on multi-rate operations expressed in the Z-domain.

## Slide 26 — Properties of Z-Transform
Reflects on why the Z-transform is worth introducing even though the course mostly deals with bounded signals. The key payoff is that it embeds a discrete sequence into a continuous complex-valued function, which makes many discrete operations (delay, downsampling, upsampling, alternation) expressible as closed-form algebraic operations on z, where continuous-function machinery (polynomial roots, contour integrals, factorization) can be brought to bear.

## Slide 27 — Downsampling in z-domain
Introduces decimation by 2, the operation that keeps every second sample of f[n], and sets up the algebraic question of expressing the Z-transform of the decimated sequence in terms of F(z).

## Slide 28 — Downsampling, continued
Carries out the decimation derivation. The downsampling mask q(n) = (1/2)[(-1)^n + 1] is plugged into the Z-transform sum, which then splits into two geometric sums F(-z^{1/2}) and F(z^{1/2}). The final identity g(k) = T^{down}[f(k)] is equivalent to G(z) = (1/2)[F(-z^{1/2}) + F(z^{1/2})], the standard alias-folding formula that exposes the spectral overlap caused by decimation.

## Slide 29 — Up-sampling (prove at home)
States the dual identity as a homework exercise. Zero-insertion upsampling g(n) = f(n/2) for even n and 0 otherwise is equivalent to G(z) = F(z^2), a clean substitution rule that compresses the spectrum onto the lower half of the unit circle.

## Slide 30 — Down and Up Sampling
Compiles the previous two results into a summary slide and then composes them. Down-then-up sampling g(n) = T^{up}[T^{down}[f(n)]] gives G(z) = F^{down}(z^2) = (1/2)[F(-z) + F(z)], making the lossy nature of the round-trip explicit through the symmetric averaging of F(z) and its reflection F(-z).

## Slide 31 — Alternating Sequence
Final closed-form identity: multiplying a sequence by (-1)^n in time is equivalent to the substitution z -> -z in the Z-transform, that is, g(n) = (-1)^n f(n) is equivalent to G(z) = F(-z). The full algebraic derivation is shown line by line as a worked example of the substitution mechanic emphasized throughout the multi-rate block.

---

## Deck-level takeaway
The deck builds the Laplace and Z-transforms as a controlled generalization of Fourier analysis, motivated by the practical need to reason about unstable and infinite-power signals such as IIR responses. The narrative arc is: complex exponentials e^{st} are eigenfunctions of every LTI operator, so widening the basis from the imaginary axis (Fourier) to the full complex s-plane (Laplace) yields a richer transform that turns convolution into multiplication while supporting growing and decaying modes. Sampling plus the substitution z = e^{sT} then collapses the Laplace machinery onto the discrete Z-transform, where stability translates into pole locations relative to the unit circle.

The second half pivots from theory to operational identities. The shift theorem turns recursive difference equations into ratios of polynomials, BIBO stability becomes a pole-inside-the-unit-circle condition, and decimation, zero-insertion upsampling, their composition, and sign alternation all reduce to clean algebraic substitutions on F(z). The repeated cos(40t)e^{rt} plots and small impulse-response tables keep the abstract complex-plane geometry tethered to concrete time-domain behavior, in line with the deck's opening promise of "intuition only".
