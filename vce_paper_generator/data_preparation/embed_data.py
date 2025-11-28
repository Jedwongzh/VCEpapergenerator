import os
import sys
# Ensure the project root is in the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.vector_db import VectorDB
from data_preparation.processing import process_single_pdf

def embed_and_store_data(data_dir, vector_db, output_dir):
    """
    Processes all PDF files in the data directory, extracts chunks,
    and stores them in the vector database.
    """
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} does not exist.")
        return

    files = [f for f in os.listdir(data_dir) if f.lower().endswith(".pdf")]
    print(f"Found {len(files)} PDF files in {data_dir}.")

    for filename in files:
        pdf_path = os.path.join(data_dir, filename)
        
        try:
            # Process the PDF
            processed_data = process_single_pdf(pdf_path, output_dir)
            
            if not processed_data:
                print(f"No data extracted from {filename}.")
                continue

            chunks = [item[0] for item in processed_data]
            metadatas = [item[1] for item in processed_data]
            
            # Add to Vector DB
            vector_db.add_documents(chunks, metadatas=metadatas)
            print(f"Successfully stored {len(chunks)} chunks from {filename}.")
            
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    # Define paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    raw_data_dir = os.path.join(base_dir, "data", "raw")
    processed_output_dir = os.path.join(base_dir, "data", "processed_images")
    chroma_db_path = os.path.join(base_dir, "chroma_db")
    
    print(f"Processing data from: {raw_data_dir}")
    print(f"Storing vector DB at: {chroma_db_path}")
    
    # Initialize Vector DB
    vector_db = VectorDB(path=chroma_db_path)
    
    # Run embedding
    embed_and_store_data(raw_data_dir, vector_db, processed_output_dir)
