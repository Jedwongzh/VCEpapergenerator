# VCE Exam Paper Generator - Quick Start Guide

## Prerequisites

1. **Python 3.8+** installed
2. **Gemini API Key** - Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Tesseract OCR** (optional, for scanned PDFs) - [Download here](https://github.com/tesseract-ocr/tesseract)

## Setup Instructions

### 1. Install Dependencies

```bash
cd c:/Users/jedwo/Desktop/VCE_AI/VCEpapergenerator
pip install -r requirements.txt
```

### 2. Set Up Gemini API Key

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

To make it permanent, add to your system environment variables.

### 3. Process Your PDF Data (First Time Only)

Place your VCE exam PDFs in the `data/raw` folder, then run:

```bash
python -m vce_paper_generator.data_preparation.embed_data
```

This will:
- Extract text from PDFs
- Clean and chunk the content
- Store embeddings in ChromaDB (creates `chroma_db` folder)

## Running the Backend API

### Start the FastAPI Server

```bash
cd c:/Users/jedwo/Desktop/VCE_AI/VCEpapergenerator
python -m vce_paper_generator.backend.main
```

Or using uvicorn directly:
```bash
uvicorn vce_paper_generator.backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

### API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Using the API

### Generate an Exam Paper

**Request:**
```bash
curl -X POST "http://localhost:8000/api/generate-paper" \
  -H "Content-Type: application/json" \
  -d '{
    "year_level": "12",
    "topics": ["Calculus", "Functions"],
    "difficulty": "Hard",
    "num_questions": 5
  }'
```

**Response:**
```json
{
  "pdf_url": "/download/exam_abc123.pdf",
  "questions": [...]
}
```

### Download the PDF

Visit: `http://localhost:8000/download/exam_abc123.pdf`

### Explain a Question

**Request:**
```bash
curl -X POST "http://localhost:8000/api/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "Find the derivative of f(x) = x^2 + 3x"
  }'
```

## Testing

Run the test suite:

```bash
# Test data pipeline
python tests/test_pipeline.py

# Test backend API
python tests/test_backend.py
```

## Project Structure

```
VCEpapergenerator/
├── data/
│   ├── raw/              # Place your PDF files here
│   └── processed_images/ # Extracted diagrams
├── chroma_db/            # Vector database (auto-created)
├── generated_papers/     # Output PDFs (auto-created)
├── vce_paper_generator/
│   ├── backend/
│   │   ├── main.py           # FastAPI app
│   │   ├── gemini_service.py # Gemini integration
│   │   └── pdf_generator.py  # PDF creation
│   ├── common/
│   │   └── vector_db.py      # ChromaDB wrapper
│   └── data_preparation/
│       ├── processing.py     # PDF processing
│       └── embed_data.py     # Data ingestion
└── tests/
```

## Next Steps: Frontend Integration

To integrate with your website (jtutes.com):

1. **Option A - Iframe Embed:**
   ```html
   <iframe src="http://your-server:8000" width="100%" height="800px"></iframe>
   ```

2. **Option B - Direct API Calls:**
   Use JavaScript to call the API endpoints from your website.

3. **Option C - Deploy as Subdomain:**
   Deploy the backend to `vce.jtutes.com` and build a custom frontend.

## Troubleshooting

### "No module named 'fitz'"
```bash
pip install PyMuPDF
```

### "GEMINI_API_KEY not found"
Make sure you've set the environment variable (see Step 2).

### "No data in ChromaDB"
Run the embed_data script to process your PDFs (see Step 3).

### Port 8000 already in use
Change the port: `uvicorn ... --port 8001`

## Support

For issues or questions, check the logs or run with debug mode:
```bash
uvicorn vce_paper_generator.backend.main:app --reload --log-level debug
```
