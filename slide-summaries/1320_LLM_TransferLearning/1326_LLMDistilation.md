# 1326_LLMDistilation — Per-Slide Summary

**Source file:** `1326_LLMDistilation.pptx`
**Source folder:** `SlidesPool/1320_LLM_TransferLearning/`
**Drive link:** https://drive.google.com/file/d/1jEExeWbNfbrj3oMD-GQ1V70P_Al-KcM7/view
**Slide count (exact, via python-pptx):** 5
**Extraction:** Local parse + slide PNG render. A compact deck on knowledge distillation with DistilBERT as the worked example.

---

## Slide 1 — Knowledge Distilation
Title slide for the deck on knowledge distillation.

## Slide 2 — Motivation
A large generic model (GPT) can solve a domain-specific task but is heavy, costly, and slow. Knowledge distillation trains a smaller, faster, cheaper model (BERT-like) to solve a specific task using knowledge from the big model.

## Slide 3 — Knowledge Distillation
A big trained model provides helpful information for training equivalent smaller models. The student uses soft classification labels (the teacher's full softmax distribution) instead of hard training-data labels, which carry richer information about class similarity.

## Slide 4 — DistilBERT
DistilBERT has 6 transformer blocks (BERT has 12) and 66M parameters (BERT has 110M). The loss combines three terms: MLM (no NSP), minimize the teacher-student softmax difference at each token position, and minimize the cosine difference between the teacher's and student's token representations.

## Slide 5 — DistilBERT
A diagram of the DistilBERT teacher-student training setup, with the frozen BERT teacher producing soft targets and hidden states that the smaller DistilBERT student is trained to imitate.

---

## Deck-level takeaway
A five-slide primer on knowledge distillation that frames it as the standard way to compress a large model into a small one without losing most of its capability. DistilBERT is the canonical example: half the transformer layers, about 60% of the parameters, trained on MLM plus a token-level softmax-matching loss plus a cosine-similarity loss on representations against frozen BERT as teacher. The recurring intuition is that the teacher's soft probabilities are a much richer training signal than one-hot labels because they encode inter-class similarity.
