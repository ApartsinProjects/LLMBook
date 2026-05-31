# Incremental indexing with content hashing
import hashlib
import json
from typing import Dict, List, Optional
from pathlib import Path


class IncrementalIndexer:
    """
    Tracks document versions to enable incremental re-indexing.
    Only processes documents that have changed since the last run.
    """

    def __init__(self, state_file: str = "indexer_state.json"):
        self.state_file = Path(state_file)
        self.state: Dict[str, str] = {}
        if self.state_file.exists():
            self.state = json.loads(self.state_file.read_text())

    def content_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()

    def get_changes(
        self, documents: Dict[str, str]
    ) -> Dict[str, List[str]]:
        """
        Compare current documents against stored state.

        Args:
            documents: dict of {doc_id: content}

        Returns:
            {"added": [...], "modified": [...], "deleted": [...]}
        """
        current_ids = set(documents.keys())
        stored_ids = set(self.state.keys())
        added = current_ids - stored_ids
        deleted = stored_ids - current_ids
        modified = set()
        for doc_id in current_ids & stored_ids:
            new_hash = self.content_hash(documents[doc_id])
            if new_hash != self.state[doc_id]:
                modified.add(doc_id)
        return {
            "added": list(added),
            "modified": list(modified),
            "deleted": list(deleted),
        }

    def update_state(self, documents: Dict[str, str]):
        """Update stored hashes after successful indexing."""
        for doc_id, content in documents.items():
            self.state[doc_id] = self.content_hash(content)
        self.state_file.write_text(json.dumps(self.state, indent=2))

    def process_changes(self, documents: Dict[str, str]):
        """Main entry point for incremental processing."""
        changes = self.get_changes(documents)
        print(f"Added: {len(changes['added'])} documents")
        print(f"Modified: {len(changes['modified'])} documents")
        print(f"Deleted: {len(changes['deleted'])} documents")
        # For added/modified: chunk, embed, upsert
        to_process = changes["added"] + changes["modified"]
        if to_process:
            print(f"Processing {len(to_process)} documents...")
            # chunk_and_embed(to_process)
            # vector_db.upsert(chunks)
        # For deleted: remove from vector DB
        if changes["deleted"]:
            print(f"Removing {len(changes['deleted'])} documents...")
            # vector_db.delete(filter={"doc_id": {"$in": changes["deleted"]}})
        # For modified: also remove old chunks before upserting new ones
        if changes["modified"]:
            print(f"Replacing chunks for {len(changes['modified'])} documents...")
            # vector_db.delete(filter={"doc_id": {"$in": changes["modified"]}})
            # vector_db.upsert(new_chunks)
        self.update_state(documents)


# Usage
indexer = IncrementalIndexer()
docs = {
    "report_2024.pdf": "Full text of the 2024 report...",
    "manual_v3.pdf": "Updated product manual content...",
    "faq.md": "Frequently asked questions...",
}
indexer.process_changes(docs)
