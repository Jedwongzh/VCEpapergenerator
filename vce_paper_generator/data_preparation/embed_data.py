# vce_paper_generator/data_preparation/embed_data.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.vector_db import VectorDB
from data_preparation.processing import process_single_pdf

def embed_and_store_data(data_dir, vector_db):
    """
    Processes all PDF files in the data directory, extracts chunks,
    and stores them in the vector database.
    """
    for filename in os.listdir(data_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(data_dir, filename)

            # This is a placeholder. In a real implementation, you would
            # process the PDF, extract chunks and metadata, and then
            # add them to the vector database.
            chunks = [f"Content from {filename}"]
            metadatas = [{"source": filename}]

            vector_db.add_documents(chunks, metadatas=metadatas)

if __name__ == "__main__":
    # This is an example of how you would run this script.
    # You would need to have a running ChromaDB instance.

    # data_dir = "path/to/your/processed/data"
    # vector_db = VectorDB()
    # embed_and_store_data(data_dir, vector_db)

    print("Data embedding and storage process would run here.")
