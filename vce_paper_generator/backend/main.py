import os
import sys
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from vce_paper_generator.common.vector_db import VectorDB
from vce_paper_generator.backend import gemini_service

app = FastAPI(title="VCE Exam Paper Generator API")

# Configure CORS for production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Vector DB
# Ensure the path matches where embed_data.py stores it
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
vector_db = VectorDB(path=CHROMA_DB_PATH)

class GeneratePaperRequest(BaseModel):
    year_level: str
    topics: List[str]
    difficulty: str
    num_questions: int = 5

class ExplainRequest(BaseModel):
    question_text: str
    context_id: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "VCE Exam Generator API is running"}

from fastapi.responses import FileResponse
from vce_paper_generator.backend import pdf_generator
import uuid

# ... (imports)

@app.post("/api/generate-paper")
def generate_paper(request: GeneratePaperRequest):
    """
    Generates a PDF exam paper based on topics and difficulty.
    """
    generated_questions = []
    
    for topic in request.topics:
        # Retrieve relevant chunks for the topic
        results = vector_db.query_documents([topic], n_results=3)
        
        context_chunks = []
        if results and results['documents']:
            context_chunks = results['documents'][0]
            
        # Generate question using Gemini
        question = gemini_service.generate_question(
            context_chunks=context_chunks,
            topic=topic,
            difficulty=request.difficulty
        )
        
        generated_questions.append({
            "topic": topic,
            "question": question
        })
    
    # Generate PDF
    output_dir = os.path.join(BASE_DIR, "generated_papers")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    filename = f"exam_{uuid.uuid4()}.pdf"
    file_path = os.path.join(output_dir, filename)
    
    pdf_generator.create_exam_pdf(
        questions=generated_questions,
        filename=file_path,
        subject="VCE Mathematics", # Could be inferred
        year_level=request.year_level
    )
    
    # Return URL (assuming static file serving or just path for now)
    # For a real plugin, we'd serve this file via a static mount or S3
    return {"pdf_url": f"/download/{filename}", "questions": generated_questions}

@app.get("/download/{filename}")
def download_file(filename: str):
    output_dir = os.path.join(BASE_DIR, "generated_papers")
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

@app.post("/api/explain")
def explain_question(request: ExplainRequest):
    """
    Explains a given question.
    """
    # Retrieve context relevant to the question text
    results = vector_db.query_documents([request.question_text], n_results=3)
    
    context_chunks = []
    if results and results['documents']:
        context_chunks = results['documents'][0]
        
    explanation = gemini_service.explain_question(
        question_text=request.question_text,
        context_chunks=context_chunks
    )
    
    return {"explanation": explanation}

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    print("🚀 Starting VCE Exam Generator API...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API docs available at: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
