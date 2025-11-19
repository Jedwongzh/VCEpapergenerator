# vce_paper_generator/common/vector_db.py

import chromadb
from chromadb.utils import embedding_functions

class VectorDB:
    def __init__(self, collection_name="vce_papers", host="localhost", port="8000"):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )

    def add_documents(self, documents, metadatas=None, ids=None):
        """
        Adds documents to the collection.
        """
        if not ids:
            ids = [f"doc_{i}" for i in range(len(documents))]

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} documents to the collection.")

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
    vector_db = VectorDB()

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
