"""v5.8: Generate the missing Code Fragment 4.2.8 (training loop).

Section 4.2 ("Building a Mini Transformer From Scratch") section 4.2.4
is titled "The Training Loop" but contains only the caption — no code.
The caption says "Complete training loop with learning rate warmup,
gradient clipping, and periodic evaluation. The DataLoader handles
batching and shuffling of character sequences."

We insert a complete, runnable training loop that:
  - Sets up an optimizer (AdamW) with a linear warmup -> cosine decay schedule
  - Iterates over a DataLoader of (input, target) char sequences
  - Computes cross-entropy loss
  - Clips gradients to a fixed L2 norm
  - Periodically evaluates validation loss
  - Saves checkpoints

Code style follows the existing 4.2 chapter conventions (PyTorch + bare
training loop, no Lightning, no HF Trainer — that's the whole point of
the "mini Transformer from scratch" chapter).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SECTION = ROOT / "part-1-foundations/module-04-transformer-architecture/section-4.2.html"


# Generated <pre> block (Pygments-highlighted-style classes match what html2pub
# produces during build, but we emit a plain <pre><code class="lang-python">...
# block; the build pipeline's pygments hook will re-highlight on next publish.
NEW_CODE_BLOCK = '''<div class="code-block-wrapper">
<pre><code class="lang-python"># --- Complete training loop with warmup, gradient clipping, and periodic eval ---
import math
import torch
from torch.utils.data import DataLoader

def train(
    model,
    train_loader: DataLoader,
    val_loader: DataLoader,
    *,
    epochs: int = 5,
    base_lr: float = 3e-4,
    warmup_steps: int = 100,
    grad_clip: float = 1.0,
    eval_every: int = 200,
    device: str = "cuda",
):
    """A from-scratch training loop that demonstrates every piece you need:
    AdamW + warmup-then-cosine LR schedule, gradient clipping, and periodic
    validation. No Lightning, no Trainer — every line is yours to read.
    """
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=base_lr, betas=(0.9, 0.95))
    total_steps = epochs * len(train_loader)

    def lr_at(step: int) -> float:
        # Linear warmup, then cosine decay to 10% of base_lr
        if step < warmup_steps:
            return base_lr * (step + 1) / warmup_steps
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return base_lr * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * progress)))

    step = 0
    history = []
    for epoch in range(epochs):
        model.train()
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)

            # Forward + cross-entropy over the vocabulary
            logits = model(x)                                 # (B, T, V)
            loss = torch.nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)), y.view(-1)
            )

            # Backward + grad clipping + step
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            for g in optimizer.param_groups:
                g["lr"] = lr_at(step)
            optimizer.step()

            # Periodic validation
            if step % eval_every == 0:
                val_loss = evaluate(model, val_loader, device)
                history.append((step, loss.item(), val_loss))
                print(f"step {step:>5} | train {loss.item():.3f} | val {val_loss:.3f} | "
                      f"lr {lr_at(step):.2e}")
            step += 1

    # Final checkpoint
    torch.save(model.state_dict(), "mini_transformer.pt")
    return history


@torch.no_grad()
def evaluate(model, loader: DataLoader, device: str) -> float:
    """Compute mean cross-entropy on a held-out loader; returns avg loss."""
    model.eval()
    losses = []
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        losses.append(torch.nn.functional.cross_entropy(
            logits.view(-1, logits.size(-1)), y.view(-1)
        ).item())
    model.train()
    return sum(losses) / len(losses)


# --- Run training ---
# train_loader, val_loader = build_loaders(...)   # from Section 4.2.3
# model = MiniTransformer(...)                    # from Section 4.2.2
# history = train(model, train_loader, val_loader, epochs=5)
</code></pre>
</div>'''


def main() -> int:
    text = SECTION.read_text(encoding="utf-8")

    # Anchor: section "4.2.4 The Training Loop" header. Insert the code block
    # AFTER any intro paragraph that follows the h2, BEFORE the existing
    # Code Fragment 4.2.8 caption.
    pat = re.compile(
        r'(<h2>4\.2\.4 The Training Loop</h2>'
        r'(?:.|\n)*?)'
        r'(<div class="code-caption"><strong>Code Fragment 4\.2\.8:</strong>)',
        re.DOTALL,
    )
    m = pat.search(text)
    if not m:
        print('  ERROR: could not locate insertion anchor')
        return 1

    # Check if a <pre> already exists in the captured group — if yes, code
    # was already inserted; idempotent skip.
    if '<pre><code' in m.group(1):
        # Look more narrowly — between h2 and caption, is there a <pre>?
        intro = m.group(1)
        if '<pre><code class="lang-python">' in intro and 'def train(' in intro:
            print('  Code Fragment 4.2.8 already has code; skipping (idempotent).')
            return 0

    new_text = text[:m.start(2)] + NEW_CODE_BLOCK + '\n' + text[m.start(2):]
    SECTION.write_text(new_text, encoding="utf-8")
    print(f'  Inserted Code Fragment 4.2.8 ({len(NEW_CODE_BLOCK)} chars) before its caption.')
    return 0


if __name__ == "__main__":
    sys.exit(main())
