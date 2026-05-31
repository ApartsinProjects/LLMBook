# API cost estimation utility
import tiktoken


def estimate_cost(
    text: str,
    model: str = "gpt-4",
    input_cost_per_1k: float = 0.01,
    output_cost_per_1k: float = 0.03,
    estimated_output_ratio: float = 1.5,
):
    """Estimate API cost for a single request.

    Note: Pricing is shown per 1K tokens for readability.
    Real APIs typically quote prices per million tokens.

    Args:
        text: The input prompt text.
        model: Model name for tokenizer selection.
        input_cost_per_1k: Cost per 1,000 input tokens.
        output_cost_per_1k: Cost per 1,000 output tokens.
        estimated_output_ratio: Expected output tokens as a
            multiple of input tokens.

    Returns:
        dict with token counts and cost estimates.
    """
    enc = tiktoken.encoding_for_model(model)
    input_tokens = len(enc.encode(text))
    est_output_tokens = int(input_tokens * estimated_output_ratio)
    input_cost = (input_tokens / 1000) * input_cost_per_1k
    output_cost = (est_output_tokens / 1000) * output_cost_per_1k
    total_cost = input_cost + output_cost
    return {
        "input_tokens": input_tokens,
        "est_output_tokens": est_output_tokens,
        "input_cost": f"${input_cost:.4f}",
        "output_cost": f"${output_cost:.4f}",
        "total_cost": f"${total_cost:.4f}",
        "monthly_cost_at_1k_req_per_day": f"${total_cost * 1000 * 30:.2f}",
    }


# Example: estimate cost for a RAG prompt
prompt = """You are a helpful assistant. Use the following context to answer.
Context: [imagine 500 words of retrieved document text here]
Question: What are the key benefits of subword tokenization?
Answer:"""

result = estimate_cost(prompt, model="gpt-4")
for key, val in result.items():
    print(f"  {key}: {val}")
