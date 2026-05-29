# MathML rendering in Kindle Previewer 3: research notes

Compiled 2026-05-16. All web evidence drawn from the official Amazon Kindle Publishing Guidelines (Mar 2026 build), the Kindle Previewer 3 User Guide v3.104.0 (Apr 2026), the EPUB 3 Content Documents specification, KaTeX docs, DAISY best-practices pages, KDP Community threads, and MobileRead forum reports.

## 1. Summary (headline)

Our `content.opf` already declares `properties="mathml"` on the 59 chapters that contain math, the package is `version="3.0"` reflowable, and every `<math>` element carries `xmlns="http://www.w3.org/1998/Math/MathML"` plus `display="block"` for block equations, which matches Amazon's documented requirements. The most likely reasons KPV3 still mis-renders are: (a) we use only KaTeX's MathML output without retaining any `alttext`/`semantics` annotation that helps Kindle's KFX renderer position scripts, (b) the markup leans heavily on `msub`/`msup`/`msubsup`/`mover` patterns that are known to drift offscreen on KPV3 device profiles (a long-standing community complaint, not fixed in any release-note entry through v3.104.0), and (c) Amazon's renderer reportedly behaves differently on tablet vs. e-ink simulations even when the Previewer claims Enhanced Typesetting is enabled. The concrete next steps are to emit KaTeX with `output: "mathml"` and an `<annotation encoding="application/x-tex">` fallback under `<semantics>`, to add `alttext` on every `<math>`, and to test a build that ships an embedded math-capable font (STIX Two Math) so KPV3 has glyphs available for the operators it currently drops.

## 2. Kindle's documented MathML support

Authoritative source: **Amazon Kindle Publishing Guidelines** (PDF), creation/mod date `D:20260330110848Z` (March 30, 2026), 126 pages, hosted at `https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf`.

### Section 10.6, "MathML Support" (page 46-47), verbatim:

> "Enhanced Typesetting supports MathML.
> 
> Supported Tags:
> maligngroup, mrow, semantics, malignmark, ms, math, mspace, menclose, msqrt, mfenced, mstyle, mfrac, msub, mi, msubsup, mlabeledtr, msup, mmultiscripts, mtable, mn, mtd, mo, mtext, mover, mtr, mpadded, munder, mphantom, munderover, mroot, annotation.
> 
> Unsupported Tags:
> maction, mglyph, mlongdiv, msgroup, mstack.
> 
> Troubleshooting:
> Open the HTML page with MathJax. If MathML is displayed without any issues, then it will be supported in Enhanced Typesetting."

The same guide, **Appendix A** (page 87), lists MathML in the bullet list of features delivered by Enhanced Typesetting and cross-references section 10.6.

### Enhanced Typesetting requirements (page 87 and KDP help):

- Enhanced Typesetting is automatic for reflowable books; there is no publisher-side toggle, but the file must be reflowable and meet other criteria (see [KDP Help: Enhanced Typesetting](https://kdp.amazon.com/en_US/help/topic/G202087570)). The reader cannot disable it; it is applied during KDP ingestion if eligible.
- The Kindle Previewer User Guide v3.104.0 (PDF created `D:20260417143423Z`, April 17, 2026, hosted at `https://kindlepreviewer3.s3.amazonaws.com/UserGuide320_EN.pdf`) confirms in section 2.1 that an Enhanced Typesetting label appears in the Preview and Navigation Options pane when the book qualifies. It does **not** add any MathML-specific rendering notes.
- The Kindle Previewer release notes (`https://s3.amazonaws.com/kindlepreviewer/UG_ReleaseNotes_EN.txt`) contain **no entries that mention "MathML", "math", or "equation"** through v3.104.0; only generic Enhanced Typesetting refinements appear. Treat KPV3 MathML behavior as effectively unchanged since 2018-2019.

## 3. Required EPUB metadata

Cross-checked against [EPUB 3 Content Documents](https://idpf.org/epub/30/spec/epub30-contentdocs.html) and the [EPUB Manifest Properties Vocabulary](https://idpf.github.io/epub-vocabs/package/item/).

1. **Reflowable layout**: the package must declare `<meta property="rendition:layout">reflowable</meta>` (or simply not declare fixed-layout). Our `content.opf` already has this. Enhanced Typesetting is **not applied to fixed-layout**.
2. **Manifest property `properties="mathml"`**: required by EPUB 3.0 on every Content Document that embeds MathML. Quoted definition: "The mathml property of the manifest item element indicates that an XHTML Content Document contains embedded MathML." Our OPF lists 47 items as `properties="mathml"`, 12 as `properties="svg mathml"`, plus 80 `svg`-only. Coverage matches the chapters that contain `<math>` (verified: 59 chapter files contain `<math>` and 59 manifest items declare `mathml`).
3. **MathML namespace** on each `<math>` element: `xmlns="http://www.w3.org/1998/Math/MathML"`. The EPUB 3 spec requires correct namespace; the DAISY MathML Best Practices ([daisy.github.io/transitiontoepub/best-practices/mathML](https://daisy.github.io/transitiontoepub/best-practices/mathML/mathMLBestPractices.html)) recommends declaring it locally on each `<math>` element rather than at the document root, which is what our markup already does.
4. **No spine `properties="mathml"`** is required or defined; the property is only valid on manifest `item`, not on `itemref`. Do not add it to the spine.
5. **MIME type**: the XHTML document carries `application/xhtml+xml`. There is no separate `application/mathml+xml` registration needed because the `<math>` element is embedded in XHTML. **Unverified**: whether Kindle's converter accepts a standalone `application/mathml+xml` document in the manifest. Recommended to keep MathML inline in XHTML.
6. **xmlns:epub** on the html element ("http://www.idpf.org/2007/ops") is the usual EPUB 3 convention; our chapters already declare it. No MathML-specific epub: properties are required.

### Restrictions from EPUB 3 spec

- Only **Presentation MathML** is allowed in the main `<math>` content. Content MathML may appear only inside `<annotation-xml>`.
- "Elements and attributes marked as deprecated in [MATHML] must not be included."
- External MathML DTDs must not be referenced from inside the EPUB archive; named entities like `&InvisibleTimes;` must be replaced with numeric entities or rewritten with `<mo>&#x2062;</mo>`. KaTeX already emits numeric entities for these, which is fine.

## 4. Required HTML/CSS structure

- The `<math>` element must declare the MathML namespace on itself (Amazon, DAISY, IDPF all agree). Done.
- `display="block"` on standalone equations and `display="inline"` (or omitted) on inline math. Recommended by DAISY; KaTeX writes `display="block"` for `displayMode: true`. Done.
- DAISY explicitly recommends **against** `alttext`/`altimg` for accessibility reasons (they cause duplicate readings under assistive tech). However, the **Amazon supported tag table includes `annotation`** as a supported element, implying a `<semantics><mrow>...</mrow><annotation encoding="application/x-tex">...</annotation></semantics>` wrapper is allowed and may help Kindle's renderer. KaTeX's `output: "mathml"` mode can emit `<annotation>` blocks when its `annotate: true` option is on (see [KaTeX options](https://katex.org/docs/options.html)).
- No specific math fonts are mandated, but Kindle E-readers do not ship STIX, Cambria Math, or Latin Modern Math. **Unverified, but plausibly load-bearing**: KPV3 falls back to its built-in fonts (Bookerly, Caecilia) for math glyphs, which lack proper "math italic" and operator metrics. Several MobileRead and KDP threads describe operator drift, missing stretchy fences, and offscreen scripts that match the symptoms we see. Embedding a math font (e.g. STIX Two Math `.otf`) in the EPUB `fonts/` directory and binding it via `@font-face` for `math, math *` selectors is the documented workaround for this.
- CSS for `<math>` elements should be minimal. KaTeX wraps its MathML in a `<span class="katex">` shell; this is harmless on Kindle, but the shell carries no styling responsibility.

## 5. Working open-source EPUB examples

### turesheim/epub-examples (GitHub, MIT)
File [`mathml/math.xhtml`](https://raw.githubusercontent.com/turesheim/epub-examples/master/mathml/math.xhtml). Verbatim head:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0 plus SVG 1.1//EN"
    "http://www.w3.org/Math/DTD/mathml2/xhtml-math11-f.dtd" >
<html lang="en">
  ...
  <math xmlns="http://www.w3.org/1998/Math/MathML">
    <mrow>
      <mi>a</mi>
      <mo>&InvisibleTimes;</mo>
      <msup><mi>x</mi><mn>2</mn></msup>
      <mo>+</mo>
      ...
    </mrow>
  </math>
```

Note this example references an **external MathML DTD** which is **not** EPUB 3 compliant; ignore the DOCTYPE for our purposes. The relevant pattern is the per-element `xmlns` and the strictly Presentation-MathML body.

### 99nyorituryo blog post (Japanese, 2018-07-27)

Source: [99nyorituryo.hatenablog.com](https://99nyorituryo.hatenablog.com/entry/2018/07/27/235051). Working OPF item:

```xml
<item href="201305211138.xhtml" id="id201305211138"
      media-type="application/xhtml+xml" properties="mathml"/>
```

Working math element:

```xml
<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline">
  ...
</math>
```

The author reports that adding `properties="mathml"` to the OPF item resolved the EPUBcheck error and that the resulting EPUB rendered correctly in Kindle Previewer 3 after the 2018 KFX update. Same author warns that `annotation`, `maction`, `mglyph`, `mlongdiv`, `msgroup`, `mstack`, and `semantics` were unreliable; note that Amazon's 2026 published guidance has since added `annotation` and `semantics` to the **supported** list, but `maction`/`mglyph`/`mlongdiv`/`msgroup`/`mstack` remain unsupported.

## 6. Known bugs and pitfalls

### KPV3 vs. real Kindle devices

The KDP Community thread "MathML shows well on Kindle Previewer 3 but not elsewhere" (`https://kdpcommunity.com/s/question/0D52T00005bqbBzSAI`) is the most-cited symptom report. We could not retrieve the body of the thread (KDP Community returned a CSS error), but the existence of the title at all in a long-lived KDP forum is corroboration that the divergence between KPV3 and shipped Kindle clients is widespread. A sister thread "Simple fraction using MATHML does not render on Kindle Desktop but works on phone and Kindle Previewer" (`https://kdpcommunity.com/s/question/0D58V00008KT0I7SAL`) describes the same class of bug for `mfrac`. Both threads are listed in active Google search results as of May 2026. **Unverified specifics** (could not load body): exact KDP responses.

### KaTeX-specific msub/msup positioning

KaTeX issue [#2219 "Display mode doesn't work for MathML output"](https://github.com/KaTeX/KaTeX/issues/2219) documents that with `{displayMode: true, output: 'mathml'}` the resulting MathML does not request displaystyle, so renderers (including KPV3) lay out the equation as inline-style with cramped scripts. PR #2220 ostensibly fixed this. **Action**: re-check that our installed KaTeX version emits `displaystyle="true"` on display math; older KaTeX 0.11.x does not.

KaTeX issues [#820](https://github.com/KaTeX/KaTeX/issues/820) and [#593](https://github.com/KaTeX/KaTeX/issues/593) describe how KaTeX's default `htmlAndMathml` output hides MathML for screen readers via CSS, which means many EPUB toolchains take the HTML branch instead of the MathML branch unless explicitly told to emit MathML only. We use `output: "mathml"` per our html2epub configuration (verified in test EPUB), so this is fine, but is worth double-checking.

### "Enhanced Typesetting required" toggle

There is **no publisher-side toggle** to turn MathML on. Enhanced Typesetting is enabled automatically by KDP ingestion if the source file is reflowable, conforms to the supported HTML/CSS subset, and is not blacklisted. Readers cannot disable it either; per the 2026 guidelines (page 87), it is a property of the book entry on Amazon's servers. The "Enhanced Typesetting" label shown in KPV3 reflects the same eligibility check. If the label is present in our Previewer session, MathML support is "on" as far as Amazon is concerned.

### epubcheck

[EPUBcheck](https://github.com/w3c/epubcheck) flags missing `properties="mathml"` on a manifest item that embeds `<math>` (error code `OPF-014`); the inverse, declaring `mathml` on an item that contains no MathML, is `OPF-015`. Our manifest passes both. epubcheck also flags non-namespaced `<math>` elements as malformed. **Unverified**: whether KDP rejects books on these errors specifically; the consensus in MobileRead threads is that KDP ingests the book and simply renders math poorly rather than rejecting it.

### Font fallback

Kindle E-readers (Paperwhite, Voyage, Oasis) and the iOS/Android Kindle apps **do not ship a Unicode math font** with stretchy bracket coverage, blackboard bold, or script italics. Operators like `&Sum;` (U+2211), `&Nabla;` (U+2207), `&Integral;` (U+222B), and stretchy parens often fall back to the next available glyph, which causes misalignment that looks identical to layout bugs. Embedding STIX Two Math or Latin Modern Math via `@font-face` is a documented workaround on MobileRead.

## 7. Recommended next steps

Three concrete experiments, ranked by expected impact and ease:

### Experiment A: re-emit MathML with `<semantics>` + `<annotation encoding="application/x-tex">`

Switch the KaTeX call in our html2epub pipeline to enable annotation, e.g.:

```js
katex.renderToString(tex, {
  output: "mathml",
  displayMode: isBlock,
  trust: false,
  strict: "ignore",
  annotate: true,            // emits <annotation encoding="application/x-tex">
});
```

This wraps the Presentation MathML in `<semantics>...</semantics>` and adds the TeX source as an annotation child. Amazon explicitly lists `semantics` and `annotation` as supported tags (Kindle Publishing Guidelines 2026, p. 46), and several published Kindle math textbooks rely on this wrapping. Add an `alttext` attribute on each `<math>` carrying the raw TeX for redundancy:

```xml
<math xmlns="http://www.w3.org/1998/Math/MathML"
      display="block"
      alttext="\\sigma(x) = \\frac{1}{1 + e^{-x}}">
  ...
</math>
```

Verify the resulting EPUB in KPV3 across all three device profiles (tablet, phone, e-reader).

### Experiment B: embed STIX Two Math and bind it to `<math>` elements

Drop `STIX2Math.otf` (SIL OFL) into `temp_epub/EPUB/fonts/`, add the manifest entry with `media-type="application/vnd.ms-opentype"`, and append the binding to a stylesheet:

```css
@font-face {
  font-family: "STIXMath";
  src: url("../fonts/STIX2Math.otf") format("opentype");
  font-weight: normal;
  font-style: normal;
}
math, math * {
  font-family: "STIXMath", "Cambria Math", serif;
}
```

This sidesteps the glyph-fallback failure mode where Kindle's default Bookerly drops operator characters or substitutes a non-math italic for `mi` letters. Re-run quality checks to confirm no font-licensing rejection. If our EPUB size budget is tight, an alternative is the subsetted "Latin Modern Math" `.otf` (around 700 KB).

### Experiment C: simplify the script structure that triggers KPV3 offscreen drift

For the specific msub/msup base-atom drift we observed, the patterns that most often fail are nested `msub`/`msup` where the base is itself an `mover` accent (e.g. `\hat{y}_i`). KaTeX emits `<msub><mover>...</mover><mi>i</mi></msub>`; some renderers mis-measure the base width. Try wrapping such constructs in an explicit `<mrow>` and forcing baseline alignment:

```xml
<msub>
  <mrow><mover accent="true"><mi>y</mi><mo>^</mo></mover></mrow>
  <mi>i</mi>
</msub>
```

This is a post-processing step on the KaTeX output (one regex substitution in the build). If it visibly fixes the rendering in KPV3, file a KaTeX issue upstream.

### Sanity check (do first)

Before any of the above, run `kindlepreviewer test_math.epub -convert -output ./out/` (test EPUB exists at `E:\Projects\BookBlogsHome\LLMBook\KDP\output\test_math.epub`) and inspect `out/Logs/`. Any `WARNING-1024` or `ERROR-2003` lines about MathML are the most direct evidence of what Amazon's converter is complaining about and should drive the priority among A/B/C above.

---

## Sources cited

- [Amazon Kindle Publishing Guidelines (PDF, March 2026 build)](https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf) — sections 10.6 (p. 46-47) and Appendix A (p. 87).
- [Kindle Previewer 3 User Guide v3.104.0 (PDF, April 2026)](https://kindlepreviewer3.s3.amazonaws.com/UserGuide320_EN.pdf).
- [Kindle Previewer release notes](https://s3.amazonaws.com/kindlepreviewer/UG_ReleaseNotes_EN.txt).
- [KDP Help: Enhanced Typesetting](https://kdp.amazon.com/en_US/help/topic/G202087570).
- [KDP Community: MathML shows well on Kindle Previewer 3 but not elsewhere](https://kdpcommunity.com/s/question/0D52T00005bqbBzSAI/mathml-shows-well-on-kindle-previewer-3-but-not-elsewhere) (could not retrieve body, May 2026).
- [KDP Community: Simple fraction using MATHML does not render on Kindle Desktop](https://kdpcommunity.com/s/question/0D58V00008KT0I7SAL).
- [EPUB 3 Content Documents (IDPF)](https://idpf.org/epub/30/spec/epub30-contentdocs.html) - MathML restrictions and namespace.
- [EPUB Manifest Properties Vocabulary - mathml property](https://idpf.github.io/epub-vocabs/package/item/).
- [DAISY Best Practices for Authoring MathML in EPUB](https://daisy.github.io/transitiontoepub/best-practices/mathML/mathMLBestPractices.html).
- [DAISY Old EPUB 3 Support Grid: MathML](https://daisy.github.io/old-epub3-support-grid/testsuite/epub3/feature/mathml/) - Kindle 0/12 tests passed (historical).
- [KaTeX Options documentation](https://katex.org/docs/options.html).
- [KaTeX Issue #2219: Display mode doesnt work for MathML output](https://github.com/KaTeX/KaTeX/issues/2219).
- [KaTeX Issue #593: Should we drop MathML rendering?](https://github.com/KaTeX/KaTeX/issues/593).
- [turesheim/epub-examples: math.xhtml](https://raw.githubusercontent.com/turesheim/epub-examples/master/mathml/math.xhtml).
- [Lapiz Digital: Including MathML in Publications (2016)](https://lapizdigi.wordpress.com/2016/03/22/including-mathml-in-publications/).
- [99nyorituryo blog: Kindle now supports MathML (Japanese, 2018-07-27)](https://99nyorituryo.hatenablog.com/entry/2018/07/27/235051).
- [The Digital Reader: Amazon KFX Format Updated With Support for MathML](https://the-digital-reader.com/amazon-kfx-format-updated-with-support-for-mathml/) - reported 2018 rollout.
- [MobileRead: How to view math equations on Kindle (2020)](https://www.mobileread.com/forums/showthread.php?t=334462).
- [Leanpub: Methods for Writing and Displaying Math in Ebooks](https://help.leanpub.com/en/articles/6116789-methods-for-writing-and-displaying-math-in-ebooks-and-html) - PNG-only stance.
- [PreTeXt EPUB conversion guide](https://pretextbook.org/doc/guide/html/epub.html) - "for Kindle, MathML is the best format".
- [Calibre: Typesetting Mathematics](https://manual.calibre-ebook.com/typesetting_math.html).
