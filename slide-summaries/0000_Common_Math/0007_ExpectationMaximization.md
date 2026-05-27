# 0007_ExpectationMaximization — Per-Slide Summary

**Source file:** `0007_ExpectationMaximization.pptx`
**Source folder:** `SlidesPool/0000_Common_Math/`
**Drive link:** https://drive.google.com/file/d/1UZGLnhs1aPK3iiEhzJlVQnFWUA9cmdsb/view
**Slide count (exact, via python-pptx):** 41
**Extraction:** Local parse + slide PNG render. Ten slides with embedded image regions (formulas, alignment diagrams, worked-example panels) were visually inspected to transcribe equations and ASCII alignment art that python-pptx could not extract.

---

## Slide 1 — Machine Translation

Title slide announcing the topic. The headline reads "Machine Translation" with the subtitle "Expectation Maximization", framing EM as the algorithmic engine that powers the statistical machine translation case study running through the deck.

## Slide 2 — Scope

A four-item agenda listing what the deck will cover: review of basic probability concepts, the machine translation task itself, language modeling, and finally the Expectation Maximization method. The ordering signals a bottom-up build: probability first, application context second, EM as the payoff.

## Slide 3 — Basic Probability

The slide grounds the discussion in translation-flavored probability. It states that an English sentence e may translate into many possible French sentences f, with some translations more likely than others. It introduces p(e) as the a priori probability that a certain person at a certain time will utter e, and p(f|e) as the conditional probability that a perfect translator will produce f given e. These two quantities become the building blocks of the noisy-channel model.

## Slide 4 — Basic probability: Cont'd

The slide extends probability notation to joint distributions. It defines p(f,e) as the chance that f and e are translations of each other, notes that independence would give p(f,e)=p(f)*p(e) (explicitly not the MT case), and writes the product rule p(f,e)=p(f|e)*p(e)=p(e|f)*p(f). Three bullet fragments at the bottom ("Sum over all possible English strings", "Sum over all translation", "Sum over sources") prepare the reader for marginalization arguments used later when summing over alignments.

## Slide 5 — Statistical Machine Translation

The slide states the decoding problem: given a French sentence f, find the English e that maximizes p(e|f), which is the most likely translation. A short pseudocode-style "Program" explains the naive search: for every possible e, score the pair by p(e|f), then choose the e with the maximum score. This sets up the need for tractable factorizations on later slides.

## Slide 6 — Bayesian Reasoning

The slide motivates Bayes by analogy with medical diagnosis: f are symptoms, e is the disease. It is hard to go directly from symptoms to disease, but easy to model how a disease generates symptoms (a generative model where one rolls a disease and then rolls its symptoms). Bayes' rule p(e|f)=p(f|e)*p(e)/p(f) then turns the generative direction into the diagnostic direction, mirroring how MT will invert a model of how English generates French.

## Slide 7 — Word reordering in Translation

The slide explains the two-step noisy-channel reasoning. p(f|e) should be high if the words in f are generally translations of words in e, regardless of order, and this can be computed from a dictionary. p(e) should be high only if e is grammatical, evaluated against a corpus by checking that e is "similar" to other sentences. Scoring with the product p(f|e)*p(e) lets the language model fix the word order that the translation model is allowed to ignore. The generative story is summarized as: first choose e, then choose its translation f.

## Slide 8 — Word Choice in Translation

The slide illustrates why a bag-of-words translation score is insufficient. A dictionary may translate one French word as either "in" or "on", so under p(f|e) alone, the grammatical "She is in the end zone", the awkward "She is on the end zone", and the scrambled "Zone end the in is she" all receive the same translation score. The language model p(e) is what distinguishes the fluent candidate from the rest.

## Slide 9 — Language Modeling

The slide describes how to assign p(e) to a sentence. The simplest approach records every sentence ever said or written, so for example "How's going?" with 76,413 occurrences in 1 billion records yields p="How's going?")=76413/1B. Two problems are noted: many perfectly good sentences would never appear and thus get p(e)=0, and storing and looking up the entire database is impractical, motivating decompositional n-gram models on the next slide.

## Slide 10 — N-grams

The slide defines an n-gram as an n-word substring, with n=2 a bigram, n=3 a trigram, and n=1 a unigram (single word). It sketches the language-model intuition: a sentence containing many reasonable n-grams is likely to itself be a reasonable, reusable string. This is the key approximation that makes p(e) tractable.

## Slide 11 — Bigram model

The slide defines b(y|x) as the probability that word y follows word x, easy to estimate from online text via Count(xy)/Count(x). A formula image below the bullets writes this as b(y|x) = number-of-occurrences("xy") / number-of-occurrences("x") and then walks through a worked decomposition: P(I like snakes that are not poisonous) is approximated as a product b(I | start-of-sentence) * b(like | I) * b(snakes | like) * ... * b(poisonous | not) * b(end-of-sentence | poisonous). This concretely shows how a sentence probability factors into local bigram terms anchored by start- and end-of-sentence tokens.

## Slide 12 — Trigram model

The slide has no bullet text; its content is an embedded formula image. The image defines b(z | x y) = number-of-occurrences("xyz") / number-of-occurrences("xy"), and again walks through the same example sentence: P(I like snakes that are not poisonous) is approximated as b(I | start-of-sentence start-of-sentence) * b(like | start-of-sentence I) * b(snakes | I like) * ... * b(poisonous | are not). Compared to the bigram slide, each factor now conditions on two preceding words, including doubled start-of-sentence padding for the first token.

## Slide 13 — Smoothing

The slide first warns that an n-gram model should still assign a non-zero probability to a sentence whose full n-grams it never saw, otherwise even one unseen n-gram zeros the entire product. An embedded formula image then shows the unsmoothed b(z | x y) = number-of-occurrences("xyz") / number-of-occurrences("xy") and offers a linear-interpolation smoothing alternative: b(z | x y) = 0.95 * (count("xyz")/count("xy")) + 0.04 * (count("yz")/count("z")) + 0.008 * (count("z")/total-words-seen) + 0.002. The fixed weights 0.95, 0.04, 0.008, 0.002 blend the trigram, bigram, unigram, and uniform-floor estimates so that no sentence receives zero probability.

## Slide 14 — Evaluating models

The slide enumerates what defines a model: a generative story (people produce words probabilistically based on the two preceding words), parameter values such as B(z|x y)=0.02, and smoothing coefficients. Training is described as learning these parameters. It then poses the comparison question: how to decide that one model works better than another, which motivates the held-out evaluation on the next slide.

## Slide 15 — Evaluating models

The slide gives a Bayesian recipe for model comparison on test data. By Bayes, P(model|test_data) = p(model) * p(test_data|model) / p(test_data). Since p(model) is treated as the same across candidate models and p(test_data) is identical across models, the best model is simply the one with the highest p(test_data|model), which is straightforward to compute by scoring the held-out data.

## Slide 16 — Perplexity

The slide notes that p(e) is typically a product of many small probabilities, which underflows in floating point. It defines model perplexity as -log(p(e))/N, normalized by length N so that test sets of different lengths produce comparable values. A formula image at the bottom illustrates the log-product identity log(P(e)) = log(f1 * f2 * f3 * ... * fn) = log(f1) + log(f2) + log(f3) + ... + log(fn), the arithmetic trick that turns dangerous multiplications into safe additions.

## Slide 17 — Translation modeling

The slide pivots from language modeling p(e) to the translation model p(f|e). It notes several model families are possible and introduces IBM Model 3 as the running example: each English word is replaced by zero or more French words, and the resulting bag of French words is then permuted into the final French sentence. This two-step rewriting is what subsequent slides formalize.

## Slide 18 — IBM Model 3: Story

The slide narrates the generative story of IBM Model 3 in four steps. First, each English word receives a fertility (the number of French words it will produce), depending only on the English word itself. Second, each word generates that many French words, each chosen independently and depending only on its English source. Third, each generated French word is assigned an absolute "target slot". Fourth, the position of each French word depends solely on the position of the English word that generated it. The story is intentionally cascaded so that each step depends on local information only.

## Slide 19 — Translation as String Rewriting

The bullet says "Generative story as string rewriting" and the slide body is four stacked sentence images that walk a single example through the Model 3 cascade. Starting line is "Mary did not slap the green witch"; the next line shows fertility expansion with the duplicated "Mary not slap slap slap the the green witch" (slap has fertility 3, the has fertility 2, did has fertility 0); the third line shows translation into Spanish "Mary no daba una botefada a la verde bruja"; the final line shows distortion (reordering) into "Mary no daba una botefada a la bruja verde", swapping the adjective and noun. The four lines literally make the four Model 3 steps visible.

## Slide 20 — Parameters of Model 3

The slide lists the Model 3 parameters. t(mansion|house) is the translation probability of French mansion given English house; n(2|house) is the probability that house produces two French words; d(5|2,4,6) is the distortion probability that a French word lands in slot 5 given its English source sat at position 2 with an English sentence of length 4 and a French sentence of length 6. Conflicts between competing slot assignments are deferred. The slide then discusses spurious words (French words without an English source) by assuming a NULL token in position 0; rather than letting longer sentences pull in more spurious words mechanically, the model tosses a spurious word with probability p after each generated word, distributes the "normal" words by d, and randomly fills the leftover slots with spurious words.

## Slide 21 — Other Models

A quick comparison list of the IBM family. Model 1 has neither fertility nor distortion. Model 2 adds distortion probabilities. Model 3 adds fertility, distortion, and spurious words. Models 4 and 5 layer on more dependencies and parameters. This sets up the later transfer-learning trick of training simpler models first.

## Slide 22 — Model 3 parameters

The slide consolidates the four parameter types: t is the translation probability (a large 2-D table), n is the fertility probability (another large 2-D table), d is the distortion probability (a smaller 4-D table), and p is the spurious-word probability (a single scalar). Two open questions are posed: how to train these from data, and how to use them to compute p(f|e) for any sentence pair. These two questions drive the rest of the deck.

## Slide 23 — Word-for-Word Alignment

The slide explains that a full record of step-by-step rewritings is infeasible to count and tabulate, so a compact "world alignment data structure" is used. An ASCII diagram in the slide image shows the English sentence "NULL And the program has been implemented" connected by vertical bars to the French "Le programme a ete mis en application", with "implemented" branching into three lines that fan out to "mis", "en", and "application". The same alignment is represented as the integer vector (2,3,4,5,6,6,6) giving, for each French word, the index of its English source. The slide notes this representation does not preserve every decision, for example whether "mis en application" was generated in this order or permuted afterwards.

## Slide 24 — Parameter Values from Alignment

The slide says that given alignments, t, n, and d can all be estimated by counting. An embedded formula image shows distortion estimation concretely: d(5 | 2, 4, 6) = dc(5 | 2, 4, 6) / sum_{j=1..25} dc(j | 2, 4, 6), the count of times French slot 5 was used for English position 2 in (4,6) sentences, normalized by the total count summed over all possible target slots j. The slide adds that the spurious-word probability p1 is estimated from the ratio of words generated from NULL to words generated from real English words.

## Slide 25 — Bootstrapping

The slide acknowledges that real corpora come with translated sentence pairs but no word-by-word alignments, so parameters must be estimated from data alone. The intuition is that word pairs that frequently co-occur in matched English and French sentences are likely approximate translations, and these approximate alignments can in turn yield approximate distortion estimates, and the process repeats. This incremental, self-improving estimation is named "bootstrapping" and is the conceptual seed of EM.

## Slide 26 — All possible alignments

The slide builds the fractional-count idea. If a sentence pair has two possible alignments, parameters should be collected from both and weighted by certainty. Each sentence pair thus produces fractional counts rather than integer counts, and in general all alignments are considered possible, each with its own weight. This generalizes the bootstrap of the previous slide into a principled weighted-counting scheme.

## Slide 27 — Alignment probabilities

The slide formalizes the weight as an alignment probability p(a|e,f). By Bayes, p(a|e,f) = p(a,f|e) / p(f|e). The numerator p(a,f|e) can be computed from the Model 3 generative story as the product of the probabilities of the various decisions that lead to f under alignment a, while the denominator p(f|e) is the marginalization over all alignments. This is the E-step in disguise.

## Slide 28 — P(a,f|e)

A brief slide noting that Model 3 does not mention alignments explicitly but alignments are a convenient way to summarize the generative choices. Some additional factors are needed to account for spurious words, and the slide explicitly skips the algebraic details.

## Slide 29 — Chicken and Egg Problem

The slide states the circular dependency in one sentence: given parameter values one can compute alignment probabilities, and given alignments one can extract parameter values. The resolution, "Estimation-Maximization Algorithms", names what is coming next.

## Slide 30 — EM algorithms

The slide writes the EM loop in plain language. Start from some parameter values, for example a uniform t(f|e) where any word translates to any word with equal likelihood. Estimate alignment probabilities under the current parameters (E-step). Re-estimate parameters from the alignment probabilities using fractional counts (M-step). Repeat until convergence. This is the heart of the deck.

## Slide 31 — EM example

The slide sets up a minimal worked example. The corpus has two sentence pairs: "bc/xy" and "b/y", where b and c are English words and x and y are French words. There is no NULL token and every word has fertility 1, so only the translation probabilities t are free parameters. The pair "bc/xy" admits two possible alignments while "b/y" admits only one, giving just enough structure to demonstrate the EM iteration without algebraic clutter.

## Slide 32 — Example cont'd

The slide initializes the toy example with uniform translation probabilities. An equation block lists t(x|b)=1/2, t(y|b)=1/2, t(x|c)=1/2, t(y|c)=1/2. A second panel shows the probability of each alignment as a product of t-values: for the straight alignment "b|x c|y" of bc/xy, P(a,f|e) = 1/2 * 1/2 = 1/4; for the crossed alignment of the same pair, P(a,f|e) = 1/2 * 1/2 = 1/4; for the trivial b/y pair with alignment "b|y", P(a,f|e) = 1/2. A formula on the right, p(a,f|e) = product over j of t(f_j | e_{a_j}), gives the general factorization being applied.

## Slide 33 — Example cont'd

The slide shows the E-step normalization. The formula at the top reads p(a|e,f) = p(a,f|e) / p(f|e) = p(a,f|e) / sum_a p(a,f|e). Applied to the toy example, each of the two alignments of bc/xy gets P(a|e,f) = (1/4)/(2/4) = 1/2, and the unique alignment of b/y gets P(a|e,f) = (1/2)/(1/2) = 1, with an annotation noting that with a single alignment the posterior is always 1.

## Slide 34 — Example cont'd

The slide shows the M-step. Fractional counts are collected by weighting each potential (English word, French word) link by its posterior alignment probability, giving tc(x|b)=1/2, tc(y|b)=1/2+1=3/2 (because b/y contributes a full count to (y|b) while the bc/xy alignments contribute fractional ones), tc(x|c)=1/2, tc(y|c)=1/2. Normalizing each row to a proper probability gives t(x|b)=1/2 / 4/2 = 1/4, t(y|b)=3/2 / 4/2 = 3/4, t(x|c)=1/2 / 1 = 1/2, t(y|c)=1/2 / 1 = 1/2. After one EM iteration the model has correctly pulled t(y|b) up because y occurs unambiguously with b in the second sentence.

## Slide 35 — What EM is doing?

The slide takes stock. EM is searching for a local minimum of an optimization criterion, here perplexity -log(p(f|e))/N, and each iteration lowers this criterion. Two practical problems are flagged: the local minimum may not be global, and enumerating all alignments is expensive. Conflicts in distortion are noted as another wrinkle. The slide then jumps ahead to decoding: once parameters are estimated, given e one must find the f that maximizes the score, and enumerating all f is also infeasible, so only a subset of the most probable f sentences is typically explored.

## Slide 36 — Efficient Model 1 training

The slide announces an algebraic speedup for Model 1, which has no fertility and no distortion. It mentions that the denominator (a sum over m, the number of French words) and the rearrangement (with l the number of English words) can be manipulated to avoid summing over all alignments explicitly. The actual algebra lives on the next slide.

## Slide 37 — Expanding and re-arranging

The slide is dominated by three formula panels. At top right is the goal sum_a p(a,f|e) = sum_a product_{j=1..m} t(f_j | e_{a_j}). The left panel writes out the naive expansion: each row corresponds to one alignment a and each column to one French word, so the sum becomes a giant sum-of-products such as t(f1|e0)*t(f2|e0)*...*t(fm|e0) + t(f1|e0)*t(f2|e0)*...*t(fm|e1) + t(f1|e0)*t(f2|e1)*...*t(fm|e2) + ..., enumerating all combinations of English source indices. The middle panel rearranges so that t(f1|e0) factors out across a block of terms, t(f2|e0) plus t(f2|e1) plus ... across the inner block, and so on. The bottom "Until" panel shows the closed form [ t(f1|e0) + t(f1|e1) + ... + t(f1|el) ] * [ t(f2|e0) + t(f2|e1) + ... + t(f2|el) ] * ... * [ t(fm|e0) + t(fm|e1) + ... + t(fm|el) ], turning a sum over exponentially many alignments into a product of m sums of l+1 terms each.

## Slide 38 — Number of operation

The slide summarizes the speedup that the rearrangement bought. Before the rearrangement the cost was exponential in sentence length; after it the cost is quadratic. This makes it tractable to compute p(f|e) for Model 1 on real corpora.

## Slide 39 — Best Alignment for Model 1

The slide notes a second algorithmic gift from Model 1: for a given pair (e, f), the best alignment (maximizing p(a|e,f) or equivalently p(a,f|e)) can be found without iterating over all alignments. Because the choices of source for each French word are independent in Model 1, one just picks the maximizing English source per French word. The catch is that a single English word may then end up generating every French word, which Model 1 cannot penalize but Model 3 does penalize through its fertility probability.

## Slide 40 — Back to Model 3

The slide describes the staged training protocol. Start by running EM under Model 1 to get good translation probabilities. Transition to Model 3 by rescoring the best Model 1 alignment under Model 3 and exploring small variations of it. Continue iterating under Model 3, restricted to a neighborhood of the current best alignment rather than the intractable full alignment space. This is how Model 3 is trained in practice.

## Slide 41 — Model 2

The closing slide notes that Model 2 (distortions but no fertility) provides a stepping stone between Models 1 and 3. Distortion parameters can be learned cheaply under Model 2 and then transferred to Model 3, giving the chain M1 -> M2 -> M3 as the standard parameter-bootstrapping path. Detailed options are left to the original paper.

---

## Deck-level takeaway

The deck uses statistical machine translation as a concrete arena in which to motivate and unpack the EM algorithm. It opens with probability fundamentals (joint, conditional, Bayes), builds a noisy-channel decomposition p(e|f) proportional to p(f|e)*p(e), develops language modeling via n-grams with smoothing and perplexity, and then introduces IBM Model 3 as a layered generative story (fertility, translation, distortion, spurious words). Once parameters and alignments are defined, the chicken-and-egg dependency between them is named explicitly and resolved by EM: initialize uniformly, compute posterior alignment probabilities (E-step), re-estimate parameters as normalized fractional counts (M-step), repeat. A tiny "bc/xy and b/y" example is worked end-to-end with arithmetic on the slides so the reader sees one iteration concretely lift t(y|b) from 1/2 to 3/4.

The pedagogical signature is the deliberate use of Model 1 as both a stepping stone and an algorithmic illustration: an algebraic re-arrangement that collapses an exponential sum over alignments into a quadratic product, and an independence property that makes best-alignment search trivial. The deck then closes the loop by showing how parameters trained under Model 1 and Model 2 are transferred to Model 3, where exact inference is infeasible and EM operates only in the neighborhood of the current best alignment. The whole arc presents EM not as an abstract optimization recipe but as the natural answer to a missing-data problem (the alignments) in a generative model that one would actually want to fit.
