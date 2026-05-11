"""v5.9: Generate the missing Code Fragment 9.7.4 (FlashAttention in Triton).

Section 9.7 explains FlashAttention's algorithm in detail (online softmax,
SRAM tiling, no materialization of the full N x N attention matrix). It then
ends with a Code Fragment 9.7.4 caption — but no code follows.

The caption says "Simplified FlashAttention forward pass in Triton. The key
ideas are: Q tiles stay in SRAM while iterating over K/V tiles, the online
softmax trick maintains running statistics, and the full N x N attention
matrix is never materialized."

We insert a teaching-grade Triton kernel that demonstrates exactly that:
  - A `@triton.jit` forward kernel with BLOCK_M and BLOCK_N tiles
  - Q tile pinned in registers/SRAM, K/V streamed in
  - Online softmax: running m_i (max) and l_i (denominator)
  - Single-pass output O = sum_j p_ij * V_j

The kernel is intentionally simplified (no causal mask, no dropout, no
multi-head batching) to prioritize readability over feature completeness.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SECTION = ROOT / 'part-2-understanding-llms/module-09-inference-optimization/section-9.7.html'

NEW_CODE_BLOCK = '''<div class="code-block-wrapper">
<pre><code class="lang-python"># --- FlashAttention forward pass in Triton (simplified, single-head) ---
# Key ideas:
#   1. Q tile of shape (BLOCK_M, head_dim) stays in fast SRAM
#   2. We stream K, V tiles of shape (BLOCK_N, head_dim) in turn
#   3. Online softmax: maintain running max m_i and denominator l_i
#      so we never materialize the full N x N attention matrix
import torch
import triton
import triton.language as tl


@triton.jit
def flash_attn_fwd(
    Q_ptr, K_ptr, V_ptr, O_ptr,
    stride_qm, stride_qk,           # Q strides (M, K)
    stride_kn, stride_kk,           # K strides (N, K)
    stride_vn, stride_vk,           # V strides (N, K)
    stride_om, stride_ok,           # O strides (M, K)
    M, N,                           # sequence lengths
    softmax_scale,                  # 1 / sqrt(head_dim)
    BLOCK_M: tl.constexpr,
    BLOCK_N: tl.constexpr,
    HEAD_DIM: tl.constexpr,
):
    # Each program handles ONE Q tile of BLOCK_M rows
    pid_m = tl.program_id(0)

    # Load this Q tile into SRAM (stays here for the entire kernel)
    offs_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offs_k = tl.arange(0, HEAD_DIM)
    q_ptrs = Q_ptr + offs_m[:, None] * stride_qm + offs_k[None, :] * stride_qk
    q = tl.load(q_ptrs, mask=offs_m[:, None] < M, other=0.0)
    q = q * softmax_scale

    # Online-softmax accumulators
    m_i = tl.full((BLOCK_M,), float("-inf"), dtype=tl.float32)   # running max
    l_i = tl.zeros((BLOCK_M,), dtype=tl.float32)                  # running denom
    acc = tl.zeros((BLOCK_M, HEAD_DIM), dtype=tl.float32)         # output accum

    # Stream over K, V tiles
    for start_n in range(0, N, BLOCK_N):
        offs_n = start_n + tl.arange(0, BLOCK_N)
        # Load K, V tile
        k_ptrs = K_ptr + offs_n[:, None] * stride_kn + offs_k[None, :] * stride_kk
        v_ptrs = V_ptr + offs_n[:, None] * stride_vn + offs_k[None, :] * stride_vk
        k = tl.load(k_ptrs, mask=offs_n[:, None] < N, other=0.0)
        v = tl.load(v_ptrs, mask=offs_n[:, None] < N, other=0.0)

        # Compute QK^T for this tile: shape (BLOCK_M, BLOCK_N)
        s = tl.dot(q, tl.trans(k))

        # Online softmax update
        m_new = tl.maximum(m_i, tl.max(s, axis=1))
        alpha = tl.exp(m_i - m_new)             # rescale prev
        p = tl.exp(s - m_new[:, None])          # current tile softmax (unnormalized)
        l_new = alpha * l_i + tl.sum(p, axis=1)

        # Rescale prior accumulator and add this tile's contribution
        acc = acc * alpha[:, None] + tl.dot(p.to(v.dtype), v)
        m_i, l_i = m_new, l_new

    # Final normalization
    o = acc / l_i[:, None]

    # Write output
    o_ptrs = O_ptr + offs_m[:, None] * stride_om + offs_k[None, :] * stride_ok
    tl.store(o_ptrs, o.to(O_ptr.dtype.element_ty), mask=offs_m[:, None] < M)


def flash_attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor,
                    block_m: int = 64, block_n: int = 64) -> torch.Tensor:
    """Wrapper: q/k/v are (M, head_dim), (N, head_dim), (N, head_dim) on CUDA."""
    M, head_dim = q.shape
    N = k.shape[0]
    o = torch.empty_like(q)
    grid = (triton.cdiv(M, block_m),)
    flash_attn_fwd[grid](
        q, k, v, o,
        q.stride(0), q.stride(1),
        k.stride(0), k.stride(1),
        v.stride(0), v.stride(1),
        o.stride(0), o.stride(1),
        M, N,
        softmax_scale=1.0 / (head_dim ** 0.5),
        BLOCK_M=block_m, BLOCK_N=block_n, HEAD_DIM=head_dim,
    )
    return o
</code></pre>
</div>'''


def main() -> int:
    text = SECTION.read_text(encoding='utf-8')
    pat = re.compile(
        r'(<div class="callout note">\s*<div class="callout-title">FlashAttention Memory Savings</div>'
        r'(?:.|\n)*?</div>\s*)'
        r'(<div class="code-caption"><strong>Code Fragment 9\.7\.4:</strong>)',
        re.DOTALL,
    )
    m = pat.search(text)
    if not m:
        print('  ERROR: could not locate insertion point')
        return 1

    # Idempotent skip
    intro = m.group(1)
    if 'flash_attn_fwd' in text[max(0, m.start()-200):m.start(2)]:
        print('  CF 9.7.4 already has Triton code; skipping (idempotent).')
        return 0

    new_text = text[:m.start(2)] + NEW_CODE_BLOCK + '\n' + text[m.start(2):]
    SECTION.write_text(new_text, encoding='utf-8')
    print(f'  Inserted Code Fragment 9.7.4 ({len(NEW_CODE_BLOCK)} chars).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
