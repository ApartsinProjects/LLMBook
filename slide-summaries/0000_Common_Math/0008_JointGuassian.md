# 0008_JointGuassian — Per-Slide Summary

**Source file:** `0008_JointGuassian.pptx`
**Source folder:** `SlidesPool/0000_Common_Math/`
**Drive link:** https://drive.google.com/file/d/15k6pA3IpRysId4WIhQnbsIMcd4PHXAyq/view
**Slide count (exact, via python-pptx):** 9
**Extraction:** Local parse + slide PNG render. Most slides combine a short bulleted skeleton with several rasterized LaTeX equation snippets, so each PNG was visually inspected to recover the underlying mathematics.

---

## Slide 1 — Jointly Gaussian Random Vectors
Title divider that opens the module on jointly Gaussian random vectors.

## Slide 2 — Jointly Gaussian Random Vector
This slide introduces the construction of a jointly Gaussian random vector. A vector entry is defined as the affine combination $X_i = \mu_i + \sum_{j=1}^{m} a_{ij} W_j$ for $i = 1, \dots, n$, where each $W_j \sim \mathcal{N}(0,1)$ is an independent standard normal. The construction is then rewritten in matrix form as $X = AW + \mu$ with $W = [W_1\ W_2\ \cdots\ W_m]^T$. The resulting distribution is the multivariate normal $X \sim \mathcal{N}(\mu, \Sigma)$ with covariance $\Sigma = AA^T \in \mathbb{R}^{n \times n}$. The density appears at the bottom as $f_X(x_1, \dots, x_n) = (2\pi)^{-n/2} |\Sigma|^{-1/2} \exp\!\left(-\tfrac{1}{2}(x-\mu)^T \Sigma^{-1}(x-\mu)\right)$, providing the canonical pdf used throughout the rest of the deck.

## Slide 3 — Jointly Gaussian Vector Pair
This slide extends the definition from a single vector to a pair. Two vectors $X \in \mathbb{R}^n$ and $Y \in \mathbb{R}^m$ are said to be jointly Gaussian when each one is itself jointly Gaussian and their stacked combination $[X\ Y]^T \in \mathbb{R}^{n+m}$ is also jointly Gaussian. The resulting joint law is given block-wise as $\begin{bmatrix} X \\ Y \end{bmatrix} \sim \mathcal{N}\!\left(\begin{bmatrix} \mu_X \\ \mu_Y \end{bmatrix}, \begin{bmatrix} \Sigma_X & \Sigma_{XY} \\ \Sigma_{YX} & \Sigma_Y \end{bmatrix}\right)$. The block-partitioned mean and covariance set up the notation needed for the conditional-distribution formulas that follow.

## Slide 4 — Conditional distribution formula
This slide states the headline result of the deck without proof. Starting from the block-partitioned joint law from Slide 3, the conditional distribution of $X$ given $Y = y$ is also multivariate Gaussian, with shifted mean $\bar{\mu} = \mu_X + \Sigma_{XY} \Sigma_Y^{-1}(y - \mu_Y)$ and reduced covariance $\bar{\Sigma} = \Sigma_X - \Sigma_{XY} \Sigma_Y^{-1} \Sigma_{YX}$. These two formulas are the workhorses behind Gaussian linear regression, Kalman filtering, and Gaussian-process inference. The remainder of the deck reconstructs them from first principles.

## Slide 5 — Conditional Distribution: Proof
This slide begins the derivation by reducing the problem to zero-mean variables and introducing a decorrelating linear transform. The centered versions are $\tilde{x} = x - \mu_x$ and $\tilde{y} = y - \mu_y$. A new zero-mean variable $z \triangleq \tilde{x} - A\tilde{y}$ is defined, with $\mathbb{E}[z] = 0$ by construction. The matrix $A$ is then chosen so that $z$ and $\tilde{y}$ are uncorrelated, which under jointly Gaussian assumptions also implies independence. The decorrelation requirement is captured by $\mathrm{Cov}(z, \tilde{y}) = \mathbb{E}[z\tilde{y}] = 0$, which the next slide solves for $A$.

## Slide 6 — Find Matrix A
This slide solves the decorrelation equation for $A$. Expanding the covariance gives $\mathbb{E}[z\tilde{y}^T] = 0 = \mathbb{E}[(\tilde{x} - A\tilde{y})\tilde{y}^T] = \mathbb{E}[\tilde{x}\tilde{y}^T] - A\,\mathbb{E}[\tilde{y}\tilde{y}^T] = \Sigma_{xy} - A\Sigma_y$. Rearranging produces the closed-form $A = \Sigma_{xy} \Sigma_y^{-1}$, which is exactly the regression coefficient matrix that maps an observed $\tilde{y}$ into the conditional mean shift of $\tilde{x}$.

## Slide 7 — Find conditional expectation
This slide assembles the conditional mean from the previous result. Since $\tilde{x} = z + A\tilde{y}$ and $z$ is independent of $\tilde{y}$ with zero mean, $\mathbb{E}[\tilde{x} \mid \tilde{y}] = A\tilde{y} + \mathbb{E}[z] = \Sigma_{xy}\Sigma_y^{-1}\tilde{y} + 0 = \Sigma_{xy}\Sigma_y^{-1}\tilde{y}$. Adding back the mean gives $\mathbb{E}[x \mid \tilde{y}] = \mathbb{E}[\tilde{x} \mid \tilde{y}] + \mu_x$, and substituting the centered $\tilde{y} = y - \mu_y$ recovers the headline conditional-mean formula $\mathbb{E}[x \mid y] = \mu_x + \Sigma_{xy} \Sigma_y^{-1}(y - \mu_y)$. This matches the $\bar{\mu}$ asserted on Slide 4.

## Slide 8 — Find Conditional Variance
This slide derives the conditional covariance through a similar route. By independence, $\mathrm{Cov}(x \mid y) = \mathrm{Cov}(\tilde{x} \mid \tilde{y}) = \mathrm{Cov}(z) = \mathbb{E}[zz^T]$. Expanding $z = \tilde{x} - A\tilde{y}$ and distributing yields $\mathbb{E}[\tilde{x}\tilde{x}^T - \tilde{x}\tilde{y}^T A^T - A\tilde{y}\tilde{x}^T + A\tilde{y}\tilde{y}^T A^T] = \Sigma_x - \Sigma_{xy}A^T - A\Sigma_{yx} + A\Sigma_y A^T$. Substituting $A = \Sigma_{xy}\Sigma_y^{-1}$ produces $\Sigma_x - \Sigma_{xy}\Sigma_y^{-1}\Sigma_{xy}^T - \Sigma_{xy}\Sigma_y^{-1}\Sigma_{yx} + \Sigma_{xy}\Sigma_y^{-1}\Sigma_y\Sigma_y^{-1}\Sigma_{xy}^T$, and the cross terms cancel to leave the Schur-complement form $\Sigma_x - \Sigma_{xy}\Sigma_y^{-1}\Sigma_{xy}^T$.

## Slide 9 — Conditional distribution
This closing slide consolidates the mean and covariance results into a single statement. The conditional law is $x \mid y \sim \mathcal{N}\!\left(\mu_x + \Sigma_{xy}\Sigma_y^{-1}(y - \mu_y),\ \Sigma_x - \Sigma_{xy}\Sigma_y^{-1}\Sigma_{xy}^T\right)$. This boxed equation is the takeaway result of the deck and the foundation for Gaussian conditioning across signal processing, Bayesian inference, and Gaussian-process machine learning.

---

## Deck-level takeaway
The deck is a self-contained derivation of the Gaussian conditional distribution. It starts by defining a jointly Gaussian vector through an affine map of standard normals, lifts the definition to a pair of vectors with a block-partitioned mean and covariance, and then states the conditional mean and conditional covariance formulas as the target results.

The proof relies on a single clean trick: construct $z = \tilde{x} - A\tilde{y}$ and pick $A = \Sigma_{xy}\Sigma_y^{-1}$ so that $z$ and $\tilde{y}$ are uncorrelated and therefore independent under Gaussianity. From there, the conditional mean falls out as a regression on the observation and the conditional covariance reduces to the Schur complement $\Sigma_x - \Sigma_{xy}\Sigma_y^{-1}\Sigma_{xy}^T$. These formulas underlie linear minimum mean-square-error estimation, Kalman filtering, and posterior inference for Gaussian processes.
