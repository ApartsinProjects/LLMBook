# Practical strategies for mitigating lost-in-the-middle
from typing import List, Dict


def reorder_context_for_retrieval(
    query: str,
    retrieved_passages: List[Dict],
    strategy: str = "important_first_last"
) -> List[Dict]:
    """Reorder passages to mitigate the lost-in-the-middle effect."""
    if strategy == "important_first_last":
        # Place the most relevant passages at the start and end
        # Less relevant passages go in the middle
        sorted_passages = sorted(
            retrieved_passages,
            key=lambda p: p["relevance_score"],
            reverse=True
        )
        n = len(sorted_passages)
        reordered = [None] * n
        # Alternate between start and end positions
        left, right = 0, n - 1
        for i, passage in enumerate(sorted_passages):
            if i % 2 == 0:
                reordered[left] = passage
                left += 1
            else:
                reordered[right] = passage
                right -= 1
        return reordered
    elif strategy == "reverse_rank":
        # Put least relevant first, most relevant last
        # (recency bias helps with last items)
        return sorted(
            retrieved_passages,
            key=lambda p: p["relevance_score"]
        )
    return retrieved_passages


# Example: 10 passages ranked by relevance
passages = [
    {"text": f"Passage {i}", "relevance_score": 1.0 - i * 0.1}
    for i in range(10)
]
reordered = reorder_context_for_retrieval("query", passages)
positions = [(p["text"], f"score={p['relevance_score']:.1f}") for p in reordered]
for i, (text, score) in enumerate(positions):
    position_label = "START" if i < 2 else "END" if i >= 8 else "middle"
    print(f"  Position {i:2d} [{position_label:6s}]: {text} ({score})")
