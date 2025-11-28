import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vce_paper_generator.backend.main import app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("vce_paper_generator.backend.main.pdf_generator.create_exam_pdf")
    @patch("vce_paper_generator.backend.main.gemini_service.generate_question")
    @patch("vce_paper_generator.backend.main.vector_db.query_documents")
    def test_generate_paper(self, mock_query, mock_generate, mock_create_pdf):
        # Mock VectorDB return
        mock_query.return_value = {'documents': [["Context chunk 1", "Context chunk 2"]]}
        
        # Mock Gemini return
        mock_generate.return_value = "Generated Question 1"
        
        # Mock PDF generation
        mock_create_pdf.return_value = "dummy_path.pdf"
        
        response = self.client.post("/api/generate-paper", json={
            "year_level": "12",
            "topics": ["Calculus"],
            "difficulty": "Hard"
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["questions"]), 1)
        self.assertEqual(data["questions"][0]["question"], "Generated Question 1")
        self.assertTrue("pdf_url" in data)
        self.assertTrue(data["pdf_url"].startswith("/download/"))

    @patch("vce_paper_generator.backend.main.gemini_service.explain_question")
    @patch("vce_paper_generator.backend.main.vector_db.query_documents")
    def test_explain_question(self, mock_query, mock_explain):
        mock_query.return_value = {'documents': [["Context chunk"]]}
        mock_explain.return_value = "Explanation text"
        
        response = self.client.post("/api/explain", json={
            "question_text": "Solve x^2 = 4"
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["explanation"], "Explanation text")

if __name__ == "__main__":
    unittest.main()
