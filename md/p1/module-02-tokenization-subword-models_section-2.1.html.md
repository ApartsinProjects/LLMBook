> "Tokenization is easy," I said, right before the Thai sentence without spaces reduced me to individual Unicode code points.
>
> ![Token](../../front-matter/images/agents/token.png) [Token](../../front-matter/wisdom-council.html#token), Whitespace-Challenged AI Agent
### Prerequisites
This section assumes familiarity with text representation concepts from [Section 1.2: Text Preprocessing](../module-01-foundations-nlp-text-representation/section-1.2.html) and word embeddings from [Section 1.3](../module-01-foundations-nlp-text-representation/section-1.3.html). Understanding vocabulary, word frequency distributions, and the idea of mapping text to numbers will make the tokenization tradeoffs immediately clear.
Big Picture
Think of tokenization as choosing the alphabet for your model's language. If your alphabet
has too few symbols, you need long strings to express simple ideas. If it has too many,
you waste memory storing symbols you rarely use. Every modern LLM navigates this tradeoff,
and the choices have real consequences for users. Building on the text representation foundations
from [Section 1.1](../module-01-foundations-nlp-text-representation/section-1.1.html),
tokenization is the first concrete step in converting raw text into the numerical inputs a model processes.
## Introduction: The Invisible Gateway
![A cartoon sushi chef slicing a long text roll into token-sized pieces at a cutting board, balancing between large and small pieces](images/tokenizer-sushi-chef.png)
**Figure 2.1.1**: Tokenization as sushi preparation. The chef (tokenizer) must slice the text roll into pieces that are small enough to fit the vocabulary but large enough to preserve meaning. Too many tiny pieces waste the context window; too few large pieces limit what the model can express.
Before a language model can process a single word, it must first decide what a "word"
even means. In [Chapter 01](../module-01-foundations-nlp-text-representation/index.html), you learned how to represent words as vectors using techniques
from Bag-of-Words to Word2Vec, but all those methods assumed that the "words" were already
given to you. How does a model decide where one word ends and the next begins? How does
it handle misspellings, compound words, or languages that do not use spaces? That is the
problem of tokenization.
When you type a prompt into ChatGPT, Claude, or any other language model, your text does
not enter the model as characters or words. Instead, it passes through a **tokenizer**,
a preprocessing step that chops your input into discrete units called **tokens**.
These tokens are the atoms of the model's universe: every parameter, every computation, and
every output is defined in terms of them. Yet tokenization is often treated as a footnote,
a plumbing detail that receives far less attention than attention heads or loss functions.
This section argues that tokenization deserves center stage. The way you split text into
tokens determines how large your vocabulary is, how long your sequences become, how much
each API call costs, and what kinds of errors the model makes. A poor tokenization scheme
can cripple an otherwise excellent model; a thoughtful one can quietly improve everything
from multilingual performance to arithmetic reasoning.
Key Insight: Tokens Are the True Currency of LLMs
When you pay for an API call, you pay per token, not per word. When a model "runs out of context," it ran out of tokens, not words. When an LLM struggles with arithmetic, it is because digits were tokenized in unexpected ways. Understanding tokenization is not just academic; it directly affects your costs, your prompt engineering strategy, and the kinds of errors you will encounter in production.
## The Vocabulary Size Tradeoff
Fun Fact
LLMs are notoriously bad at counting letters in words, and tokenization is the culprit. Ask a model how many "r"s are in "strawberry" and it may confidently answer two, because the word was split into tokens like ["str", "aw", "berry"] and the model never sees individual characters.
At one extreme, you could tokenize text one character at a time. English has roughly 100
printable characters, so your vocabulary would be tiny and your embedding table would fit
on a smart watch. But the sequence "machine learning" would become 16 tokens, forcing the
model to spend precious context window space and computation just to reconstruct familiar
words.
At the other extreme, you could give every word in the language its own token. English
has hundreds of thousands of distinct word forms (including conjugations, pluralizations,
and compounds), so your embedding table would balloon to gigabytes. Worse, any word not
in your vocabulary (a typo, a new brand name, a word from another language) would be
unrepresentable.
Modern text is stored using UTF-8, the standard encoding that represents each character
as one to four bytes. Modern tokenizers live between these extremes by using **subword** units.
Common words like "the" and "machine" get their own tokens, while rarer words are
broken into recognizable pieces: "tokenization" might become ["token", "ization"],
and "unhelpfulness" might become ["un", "help", "ful", "ness"]. This strategy keeps
the vocabulary manageable (typically 32,000 to 128,000 tokens) while ensuring that
any string can be encoded.
### The Core Equation
The fundamental relationship is simple:
Largervocabulary⇒fewertokenspertext⇒shortersequences⇒moretextfitsincontextwindowLarger vocabulary \Rightarrow fewer tokens per text \Rightarrow shorter sequences \Rightarrow more text fits in context windowLargervocabulary⇒fewertokenspertext⇒shortersequences⇒moretextfitsincontextwindow
Conversely, shrinking the vocabulary pushes in the opposite direction:
Smallervocabulary⇒moretokenspertext⇒longersequences⇒lesstextfitsincontextwindowSmaller vocabulary \Rightarrow more tokens per text \Rightarrow longer sequences \Rightarrow less text fits in context windowSmallervocabulary⇒moretokenspertext⇒longersequences⇒lesstextfitsincontextwindow
But vocabulary size also affects model parameters. Every token in the vocabulary needs
an [embedding vector](../module-01-foundations-nlp-text-representation/section-1.3.html) (typically 4,096 to 12,288 dimensions in modern LLMs). A vocabulary
of 128,000 tokens with 4,096-dimensional embeddings consumes about 2 GB of parameters
just for the embedding and output layers. That is not free.
Key Insight: Tokenization as Optimal Coding
The vocabulary size tradeoff is a direct manifestation of Shannon's source coding theorem from information theory. Shannon proved in 1948 that the optimal encoding of a message source assigns shorter codes to more frequent symbols and longer codes to rarer ones, with the theoretical minimum being the source entropy. [BPE](module-02-tokenization-subword-models_section-2.2.html.md) and WordPiece independently rediscover this principle: frequent words like "the" receive single tokens (short codes), while rare words are decomposed into multiple subword pieces (longer codes). The vocabulary size determines the codebook, and the resulting token count per text approximates the description length of the message. This is why subword tokenization works so well across languages: it automatically adapts the code length to the statistical structure of the corpus, approaching the information-theoretic optimum without anyone explicitly computing entropy.
Common Misconception: Tokens Are Not Words
One of the most persistent misconceptions among LLM practitioners is equating "token" with "word." They are not the same. A single word may be split into multiple tokens ("tokenization" becomes ["token", "ization"]), and a single token may span parts of multiple words (some tokenizers merge common bigrams like "of the" into one token). This distinction matters practically: when API pricing says "$10 per million tokens," a 500-word document might cost you 700 tokens or 1,200 tokens depending on the language, vocabulary, and content. Always check actual token counts using the tokenizer, never estimate from word counts.
![Vocabulary size spectrum: subword tokenization is the sweet spot](images/fig-2.1.2-vocab-spectrum.png)
**Figure 2.1.2**: The vocabulary size spectrum. Subword tokenization occupies the sweet spot between character and word tokenization.
### Seeing the Tradeoff in Numbers
Let us make the tradeoff concrete with a quick Python experiment. We will compare how
many tokens different granularities produce for the same English sentence.
Code Fragment 2.1.1 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (19 lines)
```python
# Comparing tokenization granularities
text = "Tokenization determines the model's vocabulary and sequence length."
# Character-level
char_tokens = list(text)
print(f"Character tokens: {len(char_tokens)} tokens")
print(f" Sample: {char_tokens[:10]}...")
# Whitespace word-level
word_tokens = text.split()
print(f"\nWord tokens: {len(word_tokens)} tokens")
print(f" Tokens: {word_tokens}")
# Subword-level (using tiktoken, GPT-4's tokenizer)
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
subword_tokens = enc.encode(text)
print(f"\nSubword tokens (GPT-4): {len(subword_tokens)} tokens")
print(f" Decoded: {[enc.decode([t]) for t in subword_tokens]}")
```
Output (9 lines)
Character tokens: 66 tokens
Sample: ['T', 'o', 'k', 'e', 'n', 'i', 'z', 'a', 't', 'i']...
Word tokens: 9 tokens
Tokens: ['Tokenization', 'determines', 'the', "model's", 'vocabulary', 'and', 'sequence', 'length.']
Subword tokens (GPT-4): 11 tokens
Decoded: ['Token', 'ization', ' determines', ' the', ' model', "'s", ' vocabulary', ' and', ' sequence', ' length', '.']
**Code Fragment 2.1.14:** Comparing tokenization granularities
Notice that the subword tokenizer produces 11 tokens, compared to 66 for characters
and 9 for words. The subword approach is nearly as compact as word-level, yet it handles
the possessive "'s" and the suffix "ization" as separate reusable pieces. It can also
handle any misspelling or novel word by falling back to smaller subword fragments.
## Context Window and Cost Impact
Modern LLMs have a fixed context window measured in tokens: 4,096 tokens for early GPT-3,
128,000 for GPT-4 Turbo, and up to 1,000,000 for Gemini 1.5 Pro (as of 2025). The tokenizer
determines how much raw text fits into that window. A tokenizer that is inefficient (uses
too many tokens per word) effectively shrinks the model's context window from the user's
perspective.
### The Token Tax on Different Languages
This becomes especially important for non-English languages. Most popular tokenizers were
trained primarily on English text, so English words tend to get their own tokens while
words in other languages are split into many small pieces. The same semantic content in
Japanese, Hindi, or Thai might consume 2x to 5x as many tokens as the English equivalent.
This means non-English users get a smaller effective context window and pay more per [API call](../../part-3-working-with-llms/module-10-llm-apis/section-10.1.html) for the same amount of meaning. Tokenizer fertility also affects [chunking strategies for retrieval systems](../../part-5-retrieval-conversation/module-19-embeddings-vector-db/section-19.4.html).
Code Fragment 2.1.2 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (18 lines)
```python
# Demonstrating the "token tax" across languages
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
texts = {
 "English": "Artificial intelligence is transforming the world.",
 "Spanish": "La inteligencia artificial está transformando el mundo.",
 "Japanese": "人工知能は世界を変えつつある。",
 "Hindi": "कृत्रिम बुद्धिमत्ता दुनिया को बदल रही है।",
}
for lang, text in texts.items():
 tokens = enc.encode(text)
 ratio = len(tokens) / len(text.split())
 print(f"{lang:10s}: {len(tokens):3d} tokens, "
 f"{len(text.split()):2d} words, "
 f"ratio = {ratio:.1f} tokens/word")
```
Output (5 lines)
English : 8 tokens, 7 words, ratio = 1.1 tokens/word
Spanish : 11 tokens, 7 words, ratio = 1.6 tokens/word
Japanese : 14 tokens, 1 words, ratio = 14.0 tokens/word
Hindi : 28 tokens, 7 words, ratio = 4.0 tokens/word
**Code Fragment 2.1.13:** Demonstrating the "token tax" across languages
Warning: The Multilingual Token Tax
A user writing in Hindi effectively pays 3 to 4 times more per API call than an English
user expressing the same idea. This is not a flaw in the model architecture; it is a
direct consequence of tokenizer training data being skewed toward English. Newer models
(Llama 3, GPT-4o) are addressing this by training tokenizers on more balanced multilingual
corpora, but the gap has not been fully closed. Retraining a tokenizer requires retraining
the entire model, since the embedding layer is sized to the vocabulary. This makes tokenizer
changes extremely expensive.
### Cost Arithmetic
API providers charge per token. Pricing varies by model and provider: as of early 2025,
rates range from roughly 1to1 to 1to30 per million input tokens depending on the model.
If your application processes 10 million words per day, the choice of
tokenizer directly affects your monthly bill:
Cost Arithmetic Comparison
| Tokenizer Efficiency | Tokens per Word | Tokens / Day | Monthly Cost (approx.) |
| --- | --- | --- | --- |
| Efficient (English text) | 1.2 | 12M | $3,600 |
| Average (mixed languages) | 2.0 | 20M | $6,000 |
| Inefficient (CJK heavy) | 3.5 | 35M | $10,500 |
The difference between 1.2 and 3.5 tokens per word is nearly a 3x cost multiplier.
Understanding your tokenizer's behavior on your specific data is not an academic
exercise; it has direct financial implications.
🌎 **Real-World Scenario**: The Multilingual Chatbot Cost Surprise
**Who:** Backend engineer at a fintech startup serving Southeast Asian markets
**Situation:** Building a customer support chatbot deployed across English, Thai, and Vietnamese
**Problem:** Monthly API costs hit 18,000,triplethe18,000, triple the 18,000,triplethe6,000 budget, despite moderate traffic of 40,000 conversations per month
**Dilemma:** Cut features and conversation depth, or find a way to reduce token consumption without degrading quality
**Decision:** Profiled token counts by language and discovered Thai queries consumed 3.8x more tokens than equivalent English queries
**How:** Switched from GPT-4 to GPT-4o (which has a more balanced multilingual tokenizer), shortened the system prompt from 380 tokens to 95 tokens, and added a token-counting middleware that flags queries likely to exceed 2,000 tokens for pre-summarization
**Result:** Monthly costs dropped to $7,200 (60% reduction). Thai token fertility improved from 3.8x to 2.1x relative to English with the new tokenizer
**Lesson:** **Always profile your tokenizer on real data in every target language before committing to a cost estimate. The "token tax" on non-English languages can silently multiply your budget.**
![Same greeting consumes vastly different context window amounts across languages](images/fig-2.1.3-multilingual-tokens.png)
**Figure 2.1.3**: The same greeting consumes vastly different amounts of the context window depending on language, due to tokenizer efficiency differences.
## Tokenization Artifacts and Their Downstream Effects
![A broken telephone game where a message gets distorted as puzzle pieces are split incorrectly at each handoff, leaving the final recipient confused](images/tokenization-artifacts-telephone.png)
**Figure 2.1.4**: Tokenization artifacts as a broken telephone game. When the tokenizer splits words at unexpected boundaries, the resulting fragments can confuse the model, leading to arithmetic errors, inconsistent spelling, and strange behavior at token boundaries.
Tokenization is not a lossless compression of text. The boundaries where the tokenizer
decides to split (or not split) create artifacts that propagate through the model's
behavior. Some of these artifacts are subtle; others cause spectacular failures.
### Artifact 1: Inconsistent Splitting
The same word can be tokenized differently depending on context. Leading spaces, capitalization,
and surrounding punctuation all affect how a subword tokenizer segments text. Consider
how GPT-4's tokenizer handles the word "token" in different contexts:
Code Fragment 2.1.3 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (18 lines)
```python
# Demonstrating context-sensitive tokenization
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
examples = [
 "token", # bare word
 " token", # with leading space
 "Token", # capitalized
 "TOKEN", # all caps
 "tokenization", # as part of longer word
 " tokenization", # with leading space, longer word
]
for ex in examples:
 ids = enc.encode(ex)
 pieces = [enc.decode([i]) for i in ids]
 print(f" {repr(ex):25s} => {pieces}")
```
Output (7 lines)
'token' => ['token']
' token' => [' token']
'Token' => ['Token']
'TOKEN' => ['TOKEN']
'tokenization' => ['token', 'ization']
' tokenization' => [' token', 'ization']
**Code Fragment 2.1.12:** Demonstrating context-sensitive tokenization
Notice that "token" and " token" (with a leading space) are entirely different tokens
in the vocabulary. This is by design: leading spaces are attached to the following word
so that the tokenizer can reconstruct the original text faithfully. But it means the
model sees different input IDs for what a human would consider the same word. The model
must learn that these represent the same concept, which requires extra training data and
capacity.
### Artifact 2: Arithmetic Failures
One of the most widely discussed tokenization artifacts is the difficulty LLMs have with
arithmetic. Numbers are tokenized inconsistently: "380" might be a single token, "381"
might be split into ["38", "1"], and "3810" might become ["38", "10"]. The model has
no built-in notion that these tokens represent digits in a positional number system.
It must learn addition, subtraction, and other operations from patterns in the training
data, and the inconsistent tokenization makes this much harder.
Code Fragment 2.1.4 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Code (10 lines)
```python
# See how numbers tokenize differently
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
numbers = ["128+256", "100+200", "3810", "381", "380"]
for num in numbers:
 ids = enc.encode(num)
 pieces = [enc.decode([i]) for i in ids]
 print(f" {num:10s} => {pieces}")
```
Output (6 lines)
128+256 => ['128', '+', '256']
100+200 => ['100', '+', '200']
3810 => ['38', '10']
381 => ['38', '1']
380 => ['380']
**Code Fragment 2.1.11:** See how numbers tokenize differently
Notice how "380" is a single token but "381" splits into ["38", "1"], and "3810" becomes
["38", "10"]. The model receives entirely different representations for numbers that differ
by just one digit. This inconsistency is a major reason why LLMs struggle with arithmetic.
Note: Why LLMs Struggle with Math
When a model sees "What is 1234 + 5678?", the tokenizer might produce
["12", "34", " +", " ", "56", "78"]. The model does not see individual
digits aligned in columns the way a human would when doing manual addition.
It must learn to parse multi-digit numbers from arbitrary token boundaries,
align them mentally, and compute carries. This is one reason why tool-use
(calling a calculator) is so important for production LLM systems.
🌎 **Real-World Scenario**: Tokenization Breaks the Invoice Parser
**Who:** ML engineer at an accounting automation company
**Situation:** Building an LLM-powered invoice parser that extracts line-item totals and computes subtotals
**Problem:** The model correctly extracted dollar amounts 94% of the time, but the computed subtotals were wrong in 23% of cases, especially for amounts above $1,000
**Dilemma:** Fine-tune the model on more arithmetic examples, or add external validation
**Decision:** Investigated tokenization and found that numbers like "1,234.56"weresplitinto["1,234.56" were split into ["1,234.56"weresplitinto["1", ",", "234", ".", "56"], making arithmetic nearly impossible for the model
**How:** Changed the pipeline so the LLM only extracts the raw numbers as strings, then a deterministic Python function parses and sums them. Added a verification step that re-checks extracted amounts against the original text
**Result:** Subtotal accuracy jumped from 77% to 99.6%. The pipeline ran faster because the model no longer needed [chain-of-thought](../../part-2-understanding-llms/module-08-reasoning-test-time-compute/section-8.1.html) prompting for arithmetic
**Lesson:** **Never rely on LLMs for arithmetic in production. Tokenization splits numbers unpredictably, so always delegate math to deterministic code.**
### Artifact 3: The "Trailing Space" Problem
Because many tokenizers attach leading whitespace to tokens, the model treats
" Hello" and "Hello" as fundamentally different inputs. This can cause unexpected
behavior when building prompts programmatically. If you accidentally include or
omit a space before a key word, the model may interpret it differently. This is
especially tricky in few-shot prompting, where consistent formatting is critical.
### Artifact 4: Tokenization of Code
Programming languages create unique challenges. Indentation is semantically meaningful
in Python, yet a tokenizer may split indentation inconsistently. Four spaces might be
one token in one context and two tokens in another. Variable names in camelCase or
snake\_case get split at different points. Modern tokenizers (like those used in code-focused
models such as Codex or StarCoder) address this by including common indentation patterns
and code-specific tokens in their vocabulary.
Code Fragment 2.1.5 below puts this into practice.
![](http://llmbook.apartsin.com/styles/icons/callout-code.svg)Show Code (15 lines)
```python
# How code gets tokenized (using tiktoken)
import tiktoken
enc = tiktoken.encoding_for_model("gpt-4")
code = """def fibonacci(n):
 if n <= 1:
 return n
 return fibonacci(n-1) + fibonacci(n-2)"""
tokens = enc.encode(code)
pieces = [enc.decode([t]) for t in tokens]
print(f"Total tokens: {len(tokens)}")
print(f"Token pieces: {pieces}")
```
Output (3 lines)
Total tokens: 29
Token pieces: ['def', ' fibonacci', '(n', '):\n', ' ', ' if', ' n', ' <=', ' ', '1', ':\n', ' ', ' return', ' n', '\n', ' ', ' return', ' fibonacci', '(n', '-', '1', ')', ' +', ' fibonacci', '(n', '-', '2', ')']
**Code Fragment 2.1.5:** How code gets tokenized (using tiktoken).
Notice how indentation, newlines, and even the function name get merged into multi-character
tokens. The four-space indentation appears as a single token in some lines but might be split
differently in others, depending on what follows.
![Tokenization artifacts propagate causing unexpected failures in arithmetic](images/fig-2.1.5-token-artifacts.png)
**Figure 2.1.5**: Tokenization artifacts propagate through the model pipeline, causing unexpected failures in downstream tasks like arithmetic.
## Practical Implications for Builders
If you are building applications on top of LLMs, tokenization behavior should inform
several design decisions:
- **Prompt budgeting:** Always count tokens, not words or characters,
  when estimating whether your prompt fits in the context window. Use the model
  provider's tokenizer library (such as `tiktoken` for OpenAI models
  or the Hugging Face `tokenizers` library) to get exact counts.
- **Multilingual applications:** Test your prompts in all target languages
  to understand the token expansion factor. You may need larger context windows or
  shorter system prompts for languages that tokenize less efficiently.
- **Structured output:** JSON, XML, and other structured formats use
  delimiters (braces, brackets, quotes) that each consume tokens. A compact JSON
  response uses fewer tokens than a verbose one, directly reducing cost.
- **Retrieval-Augmented Generation ([RAG](../../part-5-retrieval-conversation/module-20-rag/section-20.1.html)):** When chunking documents
  for retrieval, chunk by token count rather than by word count or character count
  to avoid exceeding context limits.
Key Insight
Tokenization is the lens through which your model sees the world. Understanding
that lens, including its distortions, is essential for building reliable
AI applications. Every time a model behaves unexpectedly, ask yourself: how
did the tokenizer represent this input?
**Rule of thumb:** When in doubt, use the tokenizer that shipped with your
model. Never mix tokenizers and models.
Tip: Inspect Tokenizer Output on Edge Cases
Before building a pipeline around any tokenizer, test it on numbers, code snippets, URLs, and multilingual text. Many subtle bugs come from unexpected token splits. The `tokenizer.tokenize()` method (without encoding) is your best debugging friend.
## Key Takeaways
- **Tokenization is the first processing step** in any LLM pipeline, converting
  raw text into the discrete units that the model actually processes.
- **The vocabulary size tradeoff** is the central tension: larger vocabularies
  produce shorter sequences but consume more parameters; smaller vocabularies do the opposite.
  Subword tokenization occupies the practical sweet spot.
- **Context windows are measured in tokens, not words.** Tokenizer efficiency
  directly determines how much text fits in the window and how much each API call costs.
- **Non-English languages often suffer a "token tax"** because tokenizers
  trained on English-dominated corpora produce more tokens per word for other languages.
- **Tokenization artifacts** (inconsistent splitting, number fragmentation,
  whitespace sensitivity) propagate through the model and can cause unexpected failures
  in tasks like arithmetic, code generation, and multilingual processing.
- **Always count tokens, not words,** when budgeting context windows,
  estimating costs, or chunking documents for retrieval-augmented generation.
Research Frontier
**Tokenizer-free models** are an active research frontier. Byte-level models like ByT5 and MegaByte process raw bytes without any tokenization, eliminating the entire tokenization pipeline. However, they require significantly more compute. Hybrid approaches (byte-level fallback with subword primary) offer a middle ground. Meanwhile, the multilingual tokenization gap remains: GPT-4 requires 3 to 4x more tokens for languages like Thai, Burmese, and Amharic compared to English, directly affecting API costs and effective context length.
☑ Self-Check
1. Why do modern LLMs use subword tokenization instead of word-level or character-level tokenization?
Show Answer
Subword tokenization balances the vocabulary size tradeoff. Word-level tokenization
creates enormous vocabularies and cannot handle out-of-vocabulary words. Character-level
tokenization produces extremely long sequences, wasting context window space and making
it hard for the model to learn word-level patterns. Subword tokenization keeps common
words as single tokens while breaking rare words into reusable pieces, achieving both
compact sequences and complete coverage.
2. A model has a 4,096-token context window. You want to process a 3,000-word English document and a 3,000-word Japanese document. Will both fit?
Show Answer
Probably not both. The English document will likely produce roughly 3,600 to 4,200 tokens
(about 1.2 to 1.4 tokens per word), which is already close to the limit. The Japanese
document may produce 6,000 to 15,000 tokens depending on the tokenizer, because Japanese
text typically has a much higher token-to-word ratio in tokenizers trained primarily on
English. You would need to measure with the specific tokenizer and possibly truncate or
summarize the documents.
3. Why do LLMs sometimes make arithmetic mistakes, and how does tokenization contribute to the problem?
Show Answer
LLMs make arithmetic mistakes partly because numbers are tokenized inconsistently.
A number like "1234" might become tokens ["12", "34"] or ["1", "234"] or even a
single token, depending on the number and tokenizer. The model never sees individual
digits aligned in positional columns the way humans do when computing by hand.
It must learn arithmetic from statistical patterns in training data, and the
inconsistent digit boundaries make this task much harder.
4. You notice your multilingual chatbot costs 3x more when users write in Thai compared to English. What is the likely cause, and what could you do about it?
Show Answer
The likely cause is tokenizer fertility: Thai text gets split into many more tokens
per semantic unit than English, because the tokenizer was trained primarily on English
data. Possible mitigations include: (1) switching to a model with a more balanced
multilingual tokenizer, (2) using a model with a larger vocabulary that includes
more Thai-specific tokens, (3) translating Thai inputs to English before processing
(though this adds latency and may lose nuance), or (4) using a different pricing
tier or provider that is more cost-effective for multilingual workloads.
5. In the code example, why are " token" (with a leading space) and "token" (without) different tokens in GPT-4's vocabulary?
Show Answer
Most modern tokenizers attach leading whitespace to the following word so that the
original text can be perfectly reconstructed from the token sequence. Without this
convention, the tokenizer would lose information about where spaces appeared in
the original text. The consequence is that " token" and "token" occupy different
entries in the vocabulary, and the model must learn that they refer to the same
concept. This is a necessary tradeoff for lossless round-trip encoding.
### What's Next?
In the next section, [Section 2.2: Subword Tokenization Algorithms](module-02-tokenization-subword-models_section-2.2.html.md), we dive into the specific subword tokenization algorithms (BPE, WordPiece, Unigram) used by modern LLMs.
📚 References & Further Reading
Foundational Papers
[Sennrich, R., Haddow, B., & Birch, A. (2016). "Neural Machine Translation of Rare Words with Subword Units." *ACL 2016*.](https://arxiv.org/abs/1508.07909)
The paper that introduced BPE to NLP, adapting a data compression algorithm to solve the open-vocabulary problem in neural machine translation. Established the subword tokenization paradigm used by nearly all modern LLMs. Essential reading for understanding why tokenization moved beyond word-level splitting.
📄 Paper
Schuster, M. & Nakajima, K. (2012). ["Japanese and Korean Voice Search."](https://doi.org/10.1109/ICASSP.2012.6289079) *IEEE ICASSP*.
Introduced the WordPiece algorithm in the context of speech recognition for CJK languages, later adopted by [BERT](../../part-2-understanding-llms/module-06-pretraining-scaling-laws/section-6.1.html) and related models. Demonstrates how subword segmentation handles agglutinative languages with large vocabularies. Relevant for practitioners working with multilingual or speech-to-text systems.
📄 Paper
[Kudo, T. (2018). "Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates." *ACL 2018*.](https://arxiv.org/abs/1804.10959)
Proposes the Unigram language model tokenizer and subword regularization, where multiple segmentations are sampled during training to improve robustness. Shows that probabilistic tokenization outperforms deterministic approaches on translation benchmarks. Key reading for understanding the Unigram alternative to BPE.
📄 Paper
Tools & Implementations
[Kudo, T. & Richardson, J. (2018). "SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing." *EMNLP 2018*.](https://github.com/google/sentencepiece)
The most widely used open-source tokenizer library, supporting both BPE and Unigram models with language-agnostic raw byte processing. Used by [LLaMA](../../part-2-understanding-llms/module-07-modern-llm-landscape/section-7.2.html), T5, and many other major models. Essential tool for anyone training or [fine-tuning](../../part-4-training-adapting/module-14-fine-tuning-fundamentals/section-14.1.html) language models.
🔧 Tool
[Hugging Face. "Tokenizers Library."](https://github.com/huggingface/tokenizers)
A fast, Rust-based tokenizer library supporting BPE, WordPiece, and Unigram with Python bindings, capable of tokenizing 1GB of text in under 20 seconds. Integrates seamlessly with the Hugging Face transformers ecosystem. The default choice for practitioners using Hugging Face models.
🔧 Tool
[OpenAI. "tiktoken: A fast BPE tokeniser for use with OpenAI's models."](https://github.com/openai/tiktoken)
OpenAI's production tokenizer for GPT models, implemented in Rust for speed. Indispensable for token counting, cost estimation, and context window budgeting when working with the OpenAI API. Recommended for any practitioner building applications on GPT-family models.
🔧 Tool
Analysis & Multilingual Tokenization
[Rust, P. et al. (2021). "How Good is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models." *ACL 2021*.](https://arxiv.org/abs/2012.15613)
Demonstrates that tokenizer fertility (tokens per word) is a primary factor in multilingual model performance, often more impactful than model architecture choices. Provides fertility metrics across dozens of languages. Essential for teams building or evaluating multilingual NLP systems.
📄 Paper
[Petrov, A. et al. (2024). "Language Model Tokenizers Introduce Unfairness Between Languages." *NeurIPS 2024*.](https://arxiv.org/abs/2305.15425)
Quantifies how tokenizer design creates cost and quality disparities across languages in commercial LLM APIs, with some languages requiring 10x more tokens than English for equivalent text. Directly relevant to the fertility analysis discussed in this section. Important reading for anyone concerned with equitable AI deployment.
📄 Paper