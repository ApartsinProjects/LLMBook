# 3641a_Compression_ErrorFree — Per-Slide Summary

**Source file:** `3641a_Compression_ErrorFree.pptx`
**Source folder:** `SlidesPool/3640_Vision_ImageCompression/`
**Drive link:** https://drive.google.com/file/d/1P-GwQUIVYT2BP8HAexltW-it2g1u9sph/view
**Slide count (exact, via python-pptx):** 11
**Extraction:** Local parse + slide PNG render. 1 slides are primarily visual (no body text) and are summarized from titles and rendered figures.

---

## Slide 1 — ERROR-FREE COMPRESSION
Section divider; the deck transitions to material on error-free compression.

## Slide 2 — Variable –Length Coding
Reduce coding redundancy only Assign shortest possible codewords to most probable gray levels Example: Huffman Coding.

## Slide 3 — Huffman Coding
It’s an optimal code (achieve noiseless coding theorem bound when symbols are coded individually) Sort probabilities of symbols, combine lowest probabilities(review at home). The slide includes 1 embedded image alongside the bullets.

## Slide 4 — Huffman Coding
Assign codes Average code length Entropy is 2.14bps (efficiency 0.973). The slide includes 2 embedded images alongside the bullets.

## Slide 5 — Lempel-Ziv-Welch(LZW) Coding
No a priori knowledge on the probabilities of symbols Build dictionary “on-the-fly” Dictionary contains a sequence of gray levels The codeword for a sequence is its index in the dictionary (row number).

## Slide 6 — Encoding
Initialize the dictionary to contain all strings of length one Find the longest string W in the dictionary that match the current input Emit dictionary index W to output and remove W from input Add W followed by the next symbol in the input to the dictionary Go to step 2.

## Slide 7 — LZW Example
Homework assignment: read Wikipedia or textbook example.

## Slide 8 — Bit-Plane Coding
Represent gray values using the base 2 polynomial Rational: neighboring pixels have similar values different only at high-order bits(almost) Encode each bit plane (binary image) individually Binary image compression methods in few slides.

## Slide 9 — Gray code
Problem: two close values 127, 128 have very different binary representation 127 (01111111), 128 (1000000) Use gray codes Property: successive code words differ in only a single bit 127 (11000000),128 (0100000).

## Slide 10 — Example: Most-Significant Bits
Gray-coded have less complexity (right column). The slide includes 2 embedded images alongside the bullets.

## Slide 11 — High-order bits
Visual slide containing 2 embedded figures with no body text; the visual carries the content of the topic 'High-order bits'.

---

## Deck-level takeaway
The deck spans 11 slides, opening with "ERROR-FREE COMPRESSION" and closing with "High-order bits". Body-text coverage is 82%, so a meaningful fraction of the content lives in the rendered slide images. Representative middle topics include Huffman Coding, Lempel-Ziv-Welch(LZW) Coding, Encoding, LZW Example.

Together the slides build a self-contained module that should be read in the order presented; the visual content (diagrams, figures, code screenshots, results) carries a significant portion of the message and is best appraised by opening the rendered slide PNGs under the work directory `_downloads/3640_Vision_ImageCompression/3641a_Compression_ErrorFree/slides/`.
