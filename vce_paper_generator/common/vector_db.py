import chromadb
from chromadb.utils import embedding_functions
import os

class VectorDB:
    def __init__(self, collection_name="vce_papers", path="./chroma_db"):
        """
        Initialize the VectorDB with a persistent client.
        :param collection_name: Name of the collection to use.
        :param path: Path to the local ChromaDB storage.
        """
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )

    def add_documents(self, documents, metadatas=None, ids=None):
        """
        Adds documents to the collection.
        """
        if not documents:
            return

        if not ids:
            # Generate deterministic IDs based on content hash or simple index if not provided
            # For now, using simple index is risky for persistence, so let's use a simple counter 
            # or rely on caller to provide IDs. 
            # If caller doesn't provide, we'll generate them.
            current_count = self.collection.count()
            ids = [f"doc_{current_count + i}" for i in range(len(documents))]

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} documents to the collection '{self.collection.name}'.")

    def query_documents(self, query_texts, n_results=5, where=None):
        """
        Queries the collection for similar documents.
        """
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where
        )

if __name__ == "__main__":
    # Example usage
    vector_db = VectorDB(path="./test_chroma_db")

    # Example documents
    docs = [
        "This is a sample document about VCE Methods.",
        "This document covers Specialist Maths topics.",
        "Physics is another important VCE subject."
    ]
    metadatas = [
        {"subject": "Methods"},
        {"subject": "Specialist"},
        {"subject": "Physics"}
    ]

    vector_db.add_documents(docs, metadatas=metadatas)

    # Query for documents related to "Maths"
    results = vector_db.query_documents(["Maths"], n_results=2)
    print("Query results:", results)
