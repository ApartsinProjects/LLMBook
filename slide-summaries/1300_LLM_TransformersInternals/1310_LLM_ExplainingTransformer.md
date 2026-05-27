# 1310_LLM_ExplainingTransformer — Per-Slide Summary

**Source file:** `1310_LLM_ExplainingTransformer.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/1m5QO6IzmUiZXEK04oMdXK2Ay62I2moRV/view
**Slide count (exact, via python-pptx):** 25
**Extraction:** Local parse + slide PNG render. Bullets carry the conceptual content; code and visualization screenshots illustrate three explanation toolkits (BertViz, SHAP, Captum / Transformer-interpret).

---

## Slide 1 — Explaining Transformer
Title slide for the deck on transformer interpretability.

## Slide 2 — Understanding Transformers
Two motivations: visualize attention to see the influence of each token on the embeddings of other tokens and to manually verify attention sanity (unrelated tokens should not be strongly connected); and measure the importance of tokens for classification to explain why a text was classified into a certain class.

## Slide 3 — Manually fetching attention matrices
Section divider for the subsection on extracting attention matrices from HuggingFace models.

## Slide 4 — Get attention matrix
Two code screenshots showing how to pass an attention mask (binary per token, with padding tokens set to 0) and retrieve the attention weights from the model.

## Slide 5 — Printout attention matrix
Four screenshots printing attention matrices with source as the query token, showing the per-head attention pattern numerically.

## Slide 6 — BertViz
Section divider for BertViz, an interactive attention visualizer for BERT and GPT models.

## Slide 7 — BERT Encode a pair of sentences and visualize
Seven screenshots showing BertViz visualizations of attention for an encoded sentence pair.

## Slide 8 — Visualize all attention heads
Color encodes the attention head within a layer; the default view is mean attention across all heads.

## Slide 9 — Single-head visualization
Two screenshots showing the per-head view with a selected word, revealing what each head is attending to.

## Slide 10 — Model view
An interactive chart with rows for layers and columns for heads, plus an animated GIF showing exploration of the full attention pattern.

## Slide 11 — SHAP
Section divider for SHAP (SHapley Additive exPlanations).

## Slide 12 — Importance by token masking
A naive single-token masking analysis fails to capture interactions. Worked example: "not bad" has positive sentiment; masking "not" leaves "bad" (negative), so "not" appears to push from negative to positive; masking "bad" leaves "not" (negative), so "bad" also appears to push from negative to positive. In reality, "not bad" together is the positive-sentiment marker. The interaction is invisible to single-token masking.

## Slide 13 — Shap Value for specific feature value
SHAP comes from game theory: the average effect of adding a token to all possible subsets of tokens, with absent tokens replaced by the average feature value. Computing all subsets is infeasible, so in practice SHAP samples subsets and averages contributions.

## Slide 14 — SHAP for a single input: Waterfall Plot
For predicting home prices, the waterfall plot shows the contribution of each feature to the difference between the average model output (2.215 over all training data) and the current model output f(x) = 2.846. Read bottom-up: each step continues from where the previous stopped.

## Slide 15 — SHAP of each feature across dataset
A beeswarm plot jitters the SHAP value along X for each input and uses color to encode the normalized feature value. For example, MedInc has high values (red) with a positive impact on X.

## Slide 16 — Measuring Importance
For a classification model, measure contribution to the class logit value (e.g., predicting high income over $500K). A bar plot of absolute mean SHAP value shows overall importance per feature, regardless of sign.

## Slide 17 — Sentence Explanation (Sentiment)
For sentiment classification, red tokens push toward positive and blue tokens push toward negative, ordered by SHAP values. Base is the average logit; f(inputs) is the current logit.

## Slide 18 — Integrated Gradients
Section divider for Integrated Gradients.

## Slide 19 — Gradient
Important features have a significant effect on the model output, reflected in a large gradient. In a well-trained model, gradients become flat (saturation), so plain gradients underestimate importance. Integrated Gradients sums gradients along the entire path from a baseline input (e.g., zeros) to the current input; large positive IG pushes the output (regression or class logit) up. The interpretation is which features help build up the output as you move from baseline to specific input.

## Slide 20 — Transformer-interpret
Transformer-interpret provides IG for HuggingFace transformers.

## Slide 21 — Sequence Classification
Two screenshots showing IG attributions for a sequence classification task; positive numbers are attributed positively for the predicted class.

## Slide 22 — Sequence Classification: Cont'd
Two further screenshots: specify the actual class and visualize attributions against that target.

## Slide 23 — Captum
Captum is the PyTorch library that implements Integrated Gradients (and many more attribution methods).

## Slide 24 — Image Classification Example
Three screenshots showing Captum IG applied to an image classification model.

## Slide 25 — Captum Attribution Algorithms
A figure listing the many feature-importance (attribution) algorithms Captum supports.

---

## Deck-level takeaway
The deck surveys three complementary techniques for explaining transformer predictions. Attention visualization (raw matrices and BertViz) reveals what tokens attend to what, useful for sanity-checking the model. SHAP attributes a class logit's deviation from baseline to each input feature using game-theoretic Shapley values, illustrated on tabular (home prices) and text (sentiment) examples, with the "not bad" walk-through showing why naive single-token masking misses interactions. Integrated Gradients sums gradients along a baseline-to-input path to attribute importance robustly even when individual gradients saturate, with Transformer-interpret and Captum as the canonical HuggingFace and PyTorch libraries.
