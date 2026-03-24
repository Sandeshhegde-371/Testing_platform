"""
app/ai/rag/vector_store.py

ChromaDB vector store wrapper for the RAG pipeline.

Responsibilities:
    - Initialise and persist a ChromaDB collection for test case embeddings
    - Upsert new test cases into the vector store (after generation)
    - Expose a search interface for similarity queries
    - Support batch upsert for initial data loading

Usage:
    store = VectorStore()
    await store.upsert(doc_id="TC-001", text="...", metadata={})
    results = await store.search("user login validation", top_k=5)
"""


class VectorStore:
    """
    Wraps ChromaDB for persistent test case embedding storage.

    Collection name: "test_cases"
    Embedding model : specified in settings.EMBEDDING_MODEL
    """

    def __init__(self):
        """
        Initialise ChromaDB client and embedding function.
        Loads or creates the "test_cases" collection.
        """
        pass

    async def upsert(self, doc_id: str, text: str, metadata: dict = None) -> None:
        """
        Add or update a document in the vector store.

        Args:
            doc_id   : Unique document identifier (TestCase ID).
            text     : Text content to embed (title + description + BDD).
            metadata : Optional metadata dict stored alongside the vector.
        """
        pass

    async def upsert_batch(self, documents: list) -> None:
        """
        Bulk upsert for initial data loading or re-indexing.

        Args:
            documents: List of {doc_id, text, metadata} dicts.
        """
        pass

    async def search(self, query: str, top_k: int = 5) -> list:
        """
        Find the most semantically similar documents to a query.

        Args:
            query  : Query string to embed and search.
            top_k  : Number of top results to return.

        Returns:
            list[dict]: [{doc_id, text, metadata, score}]
        """
        pass

    async def delete(self, doc_id: str) -> None:
        """Remove a document from the vector store (called on test case delete)."""
        pass
