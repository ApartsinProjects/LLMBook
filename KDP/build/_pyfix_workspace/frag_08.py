import numpy as np
import torch
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class PageResult:
    page_id: str
    score: float
    source_doc: str
    page_number: int


class TwoStageRetriever:
    """
    Two-stage retrieval: fast first stage + ColQwen2 rescoring.
    Stage 1: Use single-vector embeddings (mean-pooled patch embeddings)
    stored in a standard vector DB for fast ANN search.
    Stage 2: Rerank top-K candidates using full MaxSim scoring
    against stored patch embeddings.
    """

    def __init__(self, model, processor, vector_db, patch_store):
        self.model = model
        self.processor = processor
        self.vector_db = vector_db        # Standard vector DB (single vectors)
        self.patch_store = patch_store    # Storage for full patch embeddings

    def index_page(self, page_id: str, image, metadata: dict):
        """Index a page for both retrieval stages."""
        # Generate patch embeddings
        batch = self.processor.process_images([image]).to(self.model.device)
        with torch.no_grad():
            patch_embs = self.model(**batch)[0]  # (n_patches, dim)
        # Stage 1: Store mean-pooled vector in standard vector DB
        mean_vector = patch_embs.mean(dim=0).cpu().numpy()
        self.vector_db.upsert(
            ids=[page_id],
            vectors=[mean_vector.tolist()],
            metadata=[metadata],
        )
        # Stage 2: Store full patch embeddings for rescoring
        self.patch_store.save(page_id, patch_embs.cpu())

    def retrieve(
        self,
        query: str,
        first_stage_k: int = 100,
        final_k: int = 10,
    ) -> List[PageResult]:
        """
        Two-stage retrieval with ColQwen2 rescoring.

        Args:
            query: Text query
            first_stage_k: Candidates from first stage
            final_k: Final results after rescoring
        """
        # Stage 1: Fast candidate generation
        query_batch = self.processor.process_queries([query])
        query_batch = query_batch.to(self.model.device)
        with torch.no_grad():
            query_embs = self.model(**query_batch)[0]  # (n_tokens, dim)
        # Mean-pool query for first-stage ANN search
        query_vector = query_embs.mean(dim=0).cpu().numpy()
        candidates = self.vector_db.query(
            vector=query_vector.tolist(),
            top_k=first_stage_k,
        )
        # Stage 2: MaxSim rescoring on candidates
        results = []
        for candidate in candidates:
            page_patches = self.patch_store.load(candidate.id)
            page_patches = page_patches.to(self.model.device)
            # MaxSim: for each query token, max similarity over patches
            sim_matrix = torch.matmul(
                query_embs, page_patches.T
            )  # (n_tokens, n_patches)
            max_sims = sim_matrix.max(dim=1).values  # (n_tokens,)
            score = max_sims.sum().item()
            results.append(PageResult(
                page_id=candidate.id,
                score=score,
                source_doc=candidate.metadata.get("source", ""),
                page_number=candidate.metadata.get("page", 0),
            ))
        # Sort by MaxSim score and return top results
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:final_k]


# Usage pattern
# retriever = TwoStageRetriever(model, processor, vector_db, patch_store)
# results = retriever.retrieve("quarterly revenue by product line", final_k=5)
# for r in results:
#     print(f"  {r.source_doc} p.{r.page_number}: {r.score:.1f}")
