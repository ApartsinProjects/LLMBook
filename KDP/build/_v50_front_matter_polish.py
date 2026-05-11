"""v5.0: Front matter audit polish.

  1. Delete section-fm.1.html (44-word redirect stub; content lives in
     fm.1a + fm.1b which the redirect points to)
  2. Shorten Alexander Apartsin bio: drop patents claim, reduce to ~2
     paragraphs from the current 4
  3. Shorten Yehudit Aperstein bio similarly to ~2 paragraphs
  4. Strip any remaining redirect-stub patterns
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent


def safe_read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def delete_fm_1_stub() -> None:
    p = ROOT / "front-matter/section-fm.1.html"
    if p.exists():
        # Verify it's a stub
        text = safe_read(p)
        plain = re.sub(r"<[^>]+>", " ", text)
        if "redirected automatically" in plain.lower() or "page reorganized" in plain.lower():
            words = len(plain.split())
            p.unlink()
            print(f"  rm section-fm.1.html (redirect stub, {words} words)")
        else:
            print(f"  [skip] section-fm.1.html doesn't look like a stub")


def shorten_alexander_bio() -> None:
    p = ROOT / "front-matter/about-authors.html"
    text = safe_read(p)
    original = text
    # Match Alexander's 4-paragraph bio block and replace with shorter 2-paragraph version
    new_alex = '''<p><strong>Alexander (Sasha) Apartsin</strong> is a faculty member in the School of Computer Science at the Holon Institute of Technology. He holds a Ph.D. in Computer Science from Tel Aviv University, M.Sc. degrees from the Weizmann Institute and NYU Polytechnic, and a B.Sc. from the Technion. His research focuses on deep generative models for synthetic data generation in education, healthcare, and defense, where labeled data is scarce.</p>

            <p>Before academia, he led data science and research teams across the technology sector (automotive AI, telecommunications innovation, financial services). He has designed and taught graduate and undergraduate AI courses spanning large language models, agents, generative AI, NLP, computer vision, and deep learning, and uses an Innovation-First Learning pedagogy that integrates theory and practical tools from day one.</p>'''

    # Match the existing bio (4 paragraphs) starting at <p><strong>Alexander..., ending before <div class="author-links">
    pat = re.compile(
        r'<p><strong>Alexander \(Sasha\) Apartsin</strong>.*?(?=\s*<div class="author-links">)',
        re.DOTALL,
    )
    new_text = pat.sub(new_alex + "\n\n            ", text, count=1)
    if new_text != text:
        text = new_text
        print("  Shortened Alexander bio (4 paragraphs -> 2; patents claim dropped)")

    # Shorten Yehudit too
    new_yehudit = '''<p><strong>Yehudit Aperstein</strong> is a faculty member in the Department of Intelligent Systems at Afeka Academic College of Engineering. She holds a Ph.D. in Mathematical Economics from the Weizmann Institute and an M.Sc. in Game Theory from the Technion, with postdoctoral work in Financial Mathematics at Bar-Ilan. She has been on the Afeka faculty since 2008.</p>

            <p>She founded and directed the M.Sc. Program in Intelligent Systems at Afeka (2016-2023), and in 2024 founded ICSGen.AI, the Afeka Interdisciplinary Center for Social Good and Generative AI. She has led numerous collaborative research projects with defense organizations and industry partners, with focus on intelligent systems applied to healthcare, finance, and signal processing.</p>'''

    pat = re.compile(
        r'<p><strong>Yehudit Aperstein</strong>.*?(?=\s*<div class="author-links">)',
        re.DOTALL,
    )
    new_text = pat.sub(new_yehudit + "\n\n            ", text, count=1)
    if new_text != text:
        text = new_text
        print("  Shortened Yehudit bio (3 paragraphs -> 2)")

    if text != original:
        p.write_text(text, encoding="utf-8")


def main() -> int:
    delete_fm_1_stub()
    shorten_alexander_bio()
    return 0


if __name__ == "__main__":
    sys.exit(main())
