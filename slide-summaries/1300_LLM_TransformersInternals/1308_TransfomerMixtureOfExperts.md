# 1308_TransfomerMixtureOfExperts — Per-Slide Summary

**Source file:** `1308_TransfomerMixtureOfExperts.pptx`
**Source folder:** `SlidesPool/1300_LLM_TransformersInternals/`
**Drive link:** https://drive.google.com/file/d/1wYaHTSg-r36p3KjabNh3po8tfw42QvDB/view
**Slide count (exact, via python-pptx):** 18
**Extraction:** Local parse + slide PNG render. Body bullets carry the conceptual content; the parameter-count arithmetic is preserved verbatim.

---

## Slide 1 — Mixture of Experts
Title slide announcing MoE as an advanced addition to the transformer architecture.

## Slide 2 — Reminder: Transformer Architecture
Reminder of the canonical transformer block, with the note that the feed-forward sublayer (FFNN) provides nonlinearity and mixes the concatenated context vectors from multiple heads; attention itself is almost a linear operation (apart from the attention matrix).

## Slide 3 — Original FFNN: Dense Layer
The original FFNN with hidden dimension 2048 and embedding dimension 512 has 2048*512 + 512*2048 = approximately 2M parameters.

## Slide 4 — Mixture of Experts: Illustration
In MoE, a single expert (a specialist in a specific domain) is activated per token. Assume 16 experts: split the hidden dimension of 2048 into 16 disjoint subsets of 128 each. Each expert then has 512*128 + 128*512 = 130K weights. A routing or gating network decides which experts to activate, in either a dense variant (activate one or a few with hard selection) or a sparse variant (activate all with router-assigned weights).

## Slide 5 — Text passes through multiple experts
Two diagrams illustrating different tokens being routed to different experts during a forward pass.

## Slide 6 — Sparse vs. Dense Mixture of Experts
Sparse MoE selects a single or a few experts; dense MoE selects all with weighting.

## Slide 7 — Router
Section divider for the router (gating network).

## Slide 8 — Router
The router selects experts for each input. Soft routing assigns weights to a few selected experts. Switch Transformer is the special case of selecting a single expert.

## Slide 9 — Router / Gating Network: Architecture
A simple linear layer followed by softmax produces the routing weights.

## Slide 10 — Transformer Block with MoE Layer
A diagram showing the transformer block with the dense FFNN replaced by an MoE layer driven by the router.

## Slide 11 — Special Case: Switch Transformer
The Switch Transformer uses a top-1 selection MoE layer.

## Slide 12 — Routing Strategy: KeepTopK
KeepTopK always routes to all of the top-K experts.

## Slide 13 — MoE Training
Section divider for MoE training considerations.

## Slide 14 — Training Challenges
A particular expert may learn faster and end up being selected for nearly all tokens, starving the others. Load balancing prevents this collapse.

## Slide 15 — Load Balancing: Noisy Gating
Adding noise to router logits encourages exploration so that all experts get tokens during training.

## Slide 16 — Other load balancing methods
Load balancing loss penalizes uneven expert usage; capacity constraints cap the number of tokens per expert per batch; additional noise and temperature adjustment add exploration during training.

## Slide 17 — DeepSeek
Section divider introducing DeepSeek as an MoE example.

## Slide 18 — DeepSeek-R1
DeepSeek-R1 uses MoE transformer blocks. It has 671B parameters total, with only 37B active per token, illustrating the parameter-efficiency advantage of MoE at scale.

---

## Deck-level takeaway
The deck explains Mixture of Experts as a replacement for the dense FFNN sublayer that trades a single big network for many smaller specialists routed per token, dramatically reducing active compute while increasing total parameter capacity. It walks through the parameter arithmetic, the sparse vs. dense routing trade-off, the gating-network architecture (linear plus softmax, or top-1 for Switch Transformer), and the unavoidable training challenges (expert collapse) with their fixes (noisy gating, load balancing loss, capacity constraints). The DeepSeek-R1 example anchors the discussion: 671B total parameters with only 37B active per token.
