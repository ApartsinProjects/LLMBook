# 0006_GibbsSampling — Per-Slide Summary

**Source file:** `0006_GibbsSampling.pptx`
**Source folder:** `SlidesPool/0000_Common_Math/`
**Drive link:** https://drive.google.com/file/d/1-0cuyM93akqpdYvipgmoBmanyUTOeiFD/view
**Slide count (exact, via python-pptx):** 50
**Extraction:** Local parse + slide PNG render. Visually inspected the title slide, two Plate Diagram slides, the State-space walk pseudocode, and several image-heavy math slides (Beta, Dirichlet, Monte Carlo, Sampling and Approximation, MAP/MLE/Expectation) where image-only equations carry the meaning.

---

## Slide 1 — Gibbs Sampling
The title slide of the deck, with the words "Gibbs Sampling" set on the standard cream-on-brown title layout used throughout the lecture. No body content; the slide serves as the opening cover for the lecture on the Gibbs Sampling algorithm.

## Slide 2 — Approximating the value of an integral
The slide positions Gibbs sampling within the Markov Chain Monte Carlo (MCMC) family of methods and motivates why a computer scientist should care about it. It promises to keep the theory to a necessary minimum (no theorems) and to jump to algorithms as soon as possible, illustrating ideas on a text-mining application. The core motivation given is that integrals are needed when estimating probabilities from data, which Gibbs sampling will let us approximate by simulation.

## Slide 3 — Estimating the probabilities
Using the toy example of a biased coin tossed ten times with the observed sequence HHHHTTTTTT, the slide poses the question of estimating the probability of heads. It then writes the Maximum Likelihood Estimation answer as four heads out of ten tosses, giving an estimate of 0.4. This sets up the recurring single-parameter Bernoulli example used to motivate MLE, MAP, and full Bayesian expectation in the slides that follow.

## Slide 4 — Maximum Likelihood Estimator
The slide gives the one-line conceptual definition of MLE: find a value of the parameter p that is most likely to generate the observed data. The accompanying image carries the formal argmax expression for the MLE of p. It frames MLE as a point-estimate that picks the parameter maximising the likelihood of the data.

## Slide 5 — MLE Model
The slide spells out the generative model behind the coin example. A single trial is Bernoulli with parameter p, a sequence of trials is therefore binomial, and the embedded equations give the likelihood of the observed data and the predicted probability of the next outcome y. This establishes the explicit probabilistic model that MLE is operating on.

## Slide 6 — MAP: Maximum a posteriori estimation
Maximum a posteriori estimation is introduced as the most likely value of the parameter given the observed data, in contrast to MLE which conditions on the parameter. The slide notes that MAP can incorporate prior knowledge or beliefs, for example a belief about how far the coin is from unbiased. The embedded equation shows the MAP argmax over the posterior.

## Slide 7 — Information Loss
The slide critiques both MLE and MAP for predicting y using a single "best" value of the parameter, which throws away information contained in the full posterior distribution. The proposed alternative is to take the whole distribution into account and predict y as an expected value given the data. For a binary random variable (1 for heads, 0 for tails) this expectation is exactly the probability of heads.

## Slide 8 — Using the expectation
The slide formalises the expected-value approach: the expected value of a function on a random variable z, specialised to the coin example. Four embedded equation images show the general expectation, the coin-specific form, the conditional expectation given all unknown parameters, and an application of Bayes rule to rewrite the posterior in terms of likelihood and prior. The slide is the bridge from "use a point estimate" to "integrate over the parameter".

## Slide 9 — MAP, MLE, Expectation
A summary slide side by side comparing the three estimators. The image at the top shows MLE as argmax of P(X|pi), MAP as argmax of P(pi|X) (expanded via Bayes into P(X|pi)P(pi)/P(X)), and the predictive distribution P(y|X) computed via the integral over pi of P(y|pi) P(pi|X) dpi. These are labelled as "exact solutions", followed by the warning that the integral is difficult to compute and an approximation is needed; this is exactly the gap Gibbs sampling will fill.

## Slide 10 — Monte Carlo Sampling
Monte Carlo sampling is introduced as obtaining a desired value by simulations involving probabilistic choices. The canonical example given is estimating pi by scattering rice grains uniformly into a square enclosing a circle and counting how many fall inside the circle versus inside the square. The small icon shows the square with its inscribed circle and the formulas C/S approximately equal to pi (d/2)^2 / d^2 and pi approximately 4C/S, illustrating that Monte Carlo gives an approximation of an integral (here the area).

## Slide 11 — Sampling and Approximation
The slide states the central idea that an expectation under a distribution can be approximated by drawing samples from that distribution. An embedded sequence z^(0), z^(1), ..., z^(N) labels the draws, and two equations show the law of large numbers form (the expectation equals the limit as N goes to infinity of the sample mean) and its finite-T approximation. A small inline figure plots p(z) and an overlaid curve f(z) at several sample points z_1...z_4, visualising how samples concentrate where p(z) is large.

## Slide 12 — Walking the right walk
The slide reframes the samples z as points in a state space and casts sampling as a "walk" that jumps from state to state. The goal is stated cleanly: make the likelihood of state z proportional to p(z) so that the empirical visit frequency reproduces the target distribution. This is the conceptual leap from independent Monte Carlo sampling to MCMC.

## Slide 13 — MCMC
MCMC is described as a function g that makes a probabilistic choice of the next state based on the current state, a first-order Markov model. The open design question stated on the slide is how to define the transition probability so that the resulting walk is a "good" sample, where the long-run probability of visiting state z equals p(z). The embedded equations carry the formal transition kernel and stationary-distribution conditions.

## Slide 14 — The Gibbs Sampling Algorithm
The slide states the core idea of Gibbs sampling: the state must have at least two dimensions, and the sampler probabilistically changes one coordinate at a time, conditioned on all other coordinates (both their new and old values). This one-coordinate-at-a-time update conditioned on the rest defines the Gibbs sweep that the rest of the deck will instantiate on the text-mining model.

## Slide 15 — Conditional probability
The slide highlights the structural difference between the numerator and the denominator of the Gibbs conditional probability: the variable being resampled is "missing" in the denominator. The embedded equation shows the full conditional p(z_i | z_{-i}) written as the joint over the marginal of all other coordinates. This is the form that will be evaluated for each variable in the text-mining model.

## Slide 16 — Next
A roadmap divider. It announces that the next part will work an NLP/text-mining problem, defining the data and the task, applying Gibbs sampling to walk through the state space, and finally using the samples to evaluate expectations.

## Slide 17 — Text Mining and Gibbs Sampling
The application is specified as classifying a set of unlabelled documents into two classes (positive and negative) without supervised examples. The modelling assumption is that the two classes use different language models. A language model is then defined either simply as a probability distribution over a fixed vocabulary of V words, or in more complicated forms involving word combinations and sentences. The simple bag-of-words language model is what the rest of the deck will use.

## Slide 18 — Definition
The task is restated formally: assign class labels (encoded by the two embedded variables) and denote the set of documents with a given label. The "best" labelling is defined as the most probable one. The slide also asks the reader to think of the model as a generative story: given a label, what probabilistic process generates the document.

## Slide 19 — The generative story for a document
The generative story is laid out in three steps. First, pick a document label with probability given by the embedded distribution. Second, for every position in the document pick a word from the vocabulary according to a multinomial distribution, with words chosen independently (the Naive Bayes assumption). Third, repeat for N positions in each document. This is the data-generating model the Gibbs sampler will reason about.

## Slide 20 — Plate Diagram
A plate diagram of the Naive Bayes mixture model with no body text. The graph shows a hyperparameter node gamma_pi feeding into a Bernoulli prior pi, which in turn feeds into a per-document label L_j; L_j and a per-class word distribution theta together generate the observed word W_jk (shaded as observed). The inner plate is over R_j words in document j, the outer plate is over N documents, and a separate plate around theta indicates two class-conditional word distributions. A second hyperparameter gamma_theta feeds theta, completing the prior structure.

## Slide 21 — Priors
The slide enumerates the model's two sets of parameters: the scalar pi (probability of label 1) and the two word-distribution vectors (one per class). It then asks where these come from, answering that they are drawn randomly from uninformed priors in which every combination is equiprobable subject to the constraint that the multinomial sums to one. To enforce this conveniently, the slide introduces the special distributions Beta and Dirichlet that the next two slides will detail.

## Slide 22 — Beta Distribution
The slide presents the Beta distribution as the prior for the scalar pi. The embedded image carries the notation Beta(gamma_pi1, gamma_pi0) and notes that the uninformed prior Beta(1,1) is just the uniform distribution. The math panel shows the density f(x; alpha, beta) = const * x^(alpha-1) * (1-x)^(beta-1), the explicit normalising constant written both as an integral and using the Gamma-function identity Gamma(alpha+beta) / (Gamma(alpha)Gamma(beta)), and the compact form 1 / B(alpha, beta), together with the definitions of the Beta function B(x,y) and the Gamma function Gamma(t). An accompanying plot illustrates the shape of Beta(alpha, beta) for several parameter pairs (0.5/0.5, 5/1, 1/3, 2/2, 2/5). The slide closes with the justification "Why Beta": it can encode uninformed priors and is convenient via the conjugate prior trick.

## Slide 23 — Dirichlet Distribution
The slide introduces the Dirichlet distribution as the multivariate generalisation of the Beta, used as the prior on the per-class word distributions. The embedded support is x_1, ..., x_K with x_i in (0,1) and the sum equal to one. The density is given as f(x_1, ..., x_K; alpha_1, ..., alpha_K) = (1 / B(alpha)) * product of x_i^(alpha_i - 1). Hyperparameters are highlighted, with gamma_theta a V-dimensional vector. Uniform priors correspond to all ones (every probability distribution over words is equally likely), and the slide closes by noting that Dirichlet is also convenient (foreshadowing conjugacy with the multinomial).

## Slide 24 — Plate Diagram
Re-shows the same plate diagram as slide 20 (hyperparameters gamma_pi and gamma_theta, the Bernoulli prior pi, per-document label L_j, per-class word distribution theta on a plate of size 2, and the observed word W_jk inside an R_j-by-N nested plate). The slide reuses the figure now that the specific Beta and Dirichlet priors have been named, so the reader can re-read the graphical model with the priors fully understood.

## Slide 25 — State space initialization
The slide enumerates what counts as an unknown in the state space and what counts as an observable. Unknowns are the scalar pi, the two word-distribution vectors, and one binary label per document. The observables are the documents themselves, encoded as a vector of word indices treated as a bag of words (so word order does not matter). This catalog is what the Gibbs sampler will resample one coordinate at a time.

## Slide 26 — Initialization
The initialisation recipe is given step by step. Draw pi from Beta(1,1) under uninformed priors. For each document, flip a coin with probability pi and assign the resulting label. Finally, sample each per-class word distribution from Dirichlet(1) under uninformed priors. The embedded equations show the corresponding draws explicitly.

## Slide 27 — Derive the joint distribution
The slide previews what comes next: deriving the joint distribution of the model (recalled at the top) so that the Gibbs conditionals can be read off later. It also flags that pseudocode for the walk in the parameter space will follow. The two embedded equations show the joint we want to factor and the conditional form we will eventually compute.

## Slide 28 — Joint Distribution
The slide writes the joint probability of the entire collection conditioned on the hyperparameters and decomposes it via the generative story. The embedded equation breaks the joint into six factors of four types, which the next four slides will examine one type at a time.

## Slide 29 — Factors: Type #1
The first factor type captures the choices of the label distribution pi. The four embedded images give the prior over pi, its Beta density expressed in terms of the hyperparameters, the normalising constant (a constant that does not depend on the variables being resampled), and the resulting product form. The takeaway is that this factor is just the Beta prior on pi.

## Slide 30 — Factors: Type #2
The second factor type is the probability of a specific sequence of labels L given pi. The embedded equations give the product over documents of pi^(L_j) * (1 - pi)^(1 - L_j), the Bernoulli likelihood of the label assignment under pi.

## Slide 31 — Factors: Type #3
The third factor type captures the choices of the per-class word distributions theta_0 and theta_1. The embedded equations show their Dirichlet priors, each a product of theta_k^(gamma_theta_k - 1) divided by the Dirichlet normalising constant.

## Slide 32 — Factors: Type #4
The fourth factor type is the probability of generating the actual document content given the label and the word distribution. The slide writes it first for a single document as a bag of words (a product over vocabulary words of theta^(W_ni) where W_ni is the count of word i), then for the whole collection. Four embedded images carry these expressions.

## Slide 33 — Simplifying the Joint probability
The slide foreshadows the simplification that the conjugate priors (Beta and Dirichlet) make possible. The embedded equation collects the six factors into a more compact joint form, with the conjugacy structure visible.

## Slide 34 — Step #1: Factor1+2
Multiplying the Beta prior on pi by the Bernoulli likelihood of the labels yields, by conjugacy, another Beta distribution. The embedded equations show how the normalising factor updates and how the updated Beta parameters are obtained simply by adding the relevant label counts. The slide formally introduces the conjugate-prior idea: the posterior is in the same family as the prior, and Beta is the conjugate prior for the Bernoulli/binomial.

## Slide 35 — Step #2: Factor 3+4
The same conjugacy argument is now applied to the word distributions. For a single document, the Dirichlet prior on theta times the multinomial likelihood of the words is again a Dirichlet (with parameters updated by word counts). Extending the product to the entire collection gives the analogous expression. The slide states the general fact that Dirichlet is the conjugate prior for the multinomial and that the update rule is again "add counters".

## Slide 36 — Simplified Join
The two conjugate-prior simplifications are combined into a single, simplified joint distribution expressed in terms of the hyperparameters. The two embedded equations carry the simplified form that the integration step will operate on.

## Slide 37 — Integrating out
The slide reduces the effective number of parameters by integrating out pi and the theta vectors. The two embedded equations show the integrals over pi and theta that need to be evaluated to leave a joint only over the labels L and the observed data given the hyperparameters.

## Slide 38 — Integrating: cont'd
The slide finishes the integration analytically. It notes that the integrand is a Beta distribution missing its normalising constant, so the integral is just that normalising constant (referenced as available on Wikipedia). The three embedded equations carry the per-factor result and the combined form, replacing the integrals with ratios of Gamma functions.

## Slide 39 — Joint distribution
The slide presents the joint distribution after integration. The embedded equation shows the closed form involving Gamma functions and counters over labels and words. A side note remarks that the Gamma functions will almost entirely cancel when the Gibbs sampler is taking ratios, and recalls that the remaining state space is just the document labels L.

## Slide 40 — Building Gibbs sampler
The slide spells out how to build the Gibbs sampler over the labels. One variable is resampled at a time; in the running example one would, for instance, first resample L_1 by selecting 0 or 1 according to the appropriate conditional probability, effectively forgetting the previous label of document 1 and choosing a new one. The same step is then repeated for L_2, L_3, and so on through the collection. Three embedded equations give the conditional ratios.

## Slide 41 — Sampling for labels
The slide derives the conditional probability of a single label L_j given all others. The three embedded equations show that most factors of the joint cancel out in the ratio, leaving a compact closed-form expression for p(L_j | L_{-j}, W) in terms of counters that can be incrementally maintained.

## Slide 42 — Sampling for labels: Pseudocode
The slide gives the pseudocode for resampling a single document label: using the conditional distribution from the previous slide (referred to as distribution 49 in the source notes) it performs a coin flip with that probability and assigns the new label. The two embedded equations carry the explicit formula and the Bernoulli draw.

## Slide 43 — Sampling for theta
The slide derives the conditional probability for the per-class word distribution theta, showing it is again a Dirichlet distribution but with parameters updated by the observed counts under the current label assignment. The three embedded equations give the conditional and the sampling step from the updated Dirichlet.

## Slide 44 — Documents with labels
The slide handles the semi-supervised case: when some documents already have labels (for example, reviews already marked as positive), their labels should be held fixed and not updated during the Gibbs sweeps. This grounds the otherwise fully unsupervised algorithm in the more practical mixed setting.

## Slide 45 — The algorithm: State-space walk
A complete pseudocode listing of the Gibbs sampler is shown. The outer loop runs for t := 1 to T sweeps. For each document j from 1 to N, if j is not a training document, the algorithm subtracts j's word counts from the total word counts of whatever class it currently belongs to, decrements the document count of class L_j, assigns a new label L_j^(t+1) using the conditional probability derived earlier, increments the document count of class L_j^(t+1), and adds j's word counts back to the class word counts. After the document sweep, the algorithm sets t_0 to the vector of total word counts from class 0 (including pseudocounts), samples theta_0 from Dirichlet(t_0), and does the same for class 1 to obtain theta_1.

## Slide 46 — Producing values from the output of Gibbs sampler
Once the sampler has produced T samples from the joint distribution, the desired value Z is approximated by averaging the relevant statistic across samples (in this example, averaging the T label assignments per document). The slide flags three practical caveats that the next slides will unpack: burn-in, lag, and the use of multiple chains.

## Slide 47 — Convergence and burn-in iterations
Depending on the initialisation, the Markov chain may take some time to converge to its stationary distribution. The standard remedy is to discard the first B iterations as a "burn-in" period and only retain samples after that.

## Slide 48 — Autocorrelation and lag
The expectation approximation assumed independent samples of Z, but Gibbs samples are autocorrelated since each new state is generated from the previous one. The slide names this the autocorrelation problem and prescribes the standard fix: take every L-th value for averaging, where L is the chosen lag.

## Slide 49 — Multiple chains
Because Gibbs sampling is sensitive to the starting point, the slide recommends running multiple chains from different initial states and combining their samples, which protects against being stuck near a single starting region of the state space.

## Slide 50 — Informal Recipe
The closing slide distils the lecture into a step-by-step informal recipe for applying Gibbs sampling to a new problem. Design a generative story with hidden variables and parameters (labels, parameterised distributions). Carefully select priors on the unknown parameters, favouring conjugate distributions. Derive the joint distribution and simplify it using the conjugate priors. Integrate out unneeded variables. Derive the conditional probability needed to update each hidden variable and parameter, keeping known quantities fixed. Run the simulation for T steps, use the samples to approximate the target function or expectation, and apply burn-in, lag, and multiple chains if necessary.

---

## Deck-level takeaway
The deck is a self-contained, algorithm-first introduction to Gibbs sampling that begins from the Bayesian motivation (MLE versus MAP versus expectation under the posterior), explains why exact integrals are intractable, and positions Monte Carlo and then MCMC as the practical workaround. Gibbs sampling is then introduced as the special case that resamples one coordinate at a time from its full conditional, which is tractable whenever conjugate priors (Beta for Bernoulli, Dirichlet for multinomial) make those conditionals closed-form.

The second half of the deck instantiates the recipe on an unsupervised binary document classification task built on a Naive Bayes mixture model with Beta and Dirichlet priors. The reader is walked through the plate diagram, the six-factor joint distribution, the conjugate-prior simplifications, the integration that eliminates pi and the theta vectors, and finally an explicit pseudocode sampler that sweeps over document labels. Practical caveats (burn-in, lag, multiple chains) and a one-slide informal recipe close the lecture, giving the reader a transferable template for applying Gibbs sampling to other latent-variable problems.
