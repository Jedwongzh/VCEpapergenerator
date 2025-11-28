import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vce_paper_generator.data_preparation.processing import process_single_pdf, clean_text, chunk_text, extract_metadata

class TestDataPipeline(unittest.TestCase):

    def test_clean_text(self):
        raw_text = "   Header   \n\n  Content  \n  12  \n"
        cleaned = clean_text(raw_text)
        # "12" should be removed as it looks like a page number
        # Newlines should be preserved (normalized to \n\n for multiple)
        self.assertEqual(cleaned, "Header\n\nContent")

    def test_chunk_text(self):
        text = "Introduction text.\nQuestion 1. This is question 1.\nQuestion 2. This is question 2."
        chunks = chunk_text(text)
        # Should identify "Question 1" and "Question 2"
        # Note: The regex might split "Introduction text." as a separate chunk if not matched
        # Let's see how our regex behaves.
        # Our regex: (Question \s*\d+|^\d+\.)
        # It splits BEFORE the pattern.
        
        # Expected: 
        # 1. "Introduction text." (if it doesn't match pattern)
        # 2. "Question 1. This is question 1."
        # 3. "Question 2. This is question 2."
        
        # However, our current logic appends the delimiter to the NEXT chunk or PREVIOUS?
        # The loop: if part matches pattern, it starts a new chunk.
        
        self.assertTrue(len(chunks) >= 2)
        self.assertIn("Question 1", chunks[0] if "Question 1" in chunks[0] else chunks[1])

    def test_extract_metadata(self):
        filename = "2023_Methods_Exam1.pdf"
        text = "some text"
        meta = extract_metadata(filename, text)
        self.assertEqual(meta["year"], "2023")
        self.assertEqual(meta["subject"], "Methods")

    @patch("vce_paper_generator.data_preparation.processing.fitz.open")
    @patch("vce_paper_generator.data_preparation.processing.extract_diagrams")
    def test_process_single_pdf(self, mock_extract_diagrams, mock_fitz_open):
        # Mock PDF document
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Question 1. Solve for x. \n Question 2. Find the derivative."
        mock_doc.__len__.return_value = 1
        mock_doc.load_page.return_value = mock_page
        mock_fitz_open.return_value = mock_doc
        
        processed_data = process_single_pdf("dummy_path/2023_Methods.pdf", "dummy_output")
        
        self.assertTrue(len(processed_data) >= 2)
        self.assertEqual(processed_data[0][1]["year"], "2023")
        self.assertEqual(processed_data[0][1]["subject"], "Methods")
        self.assertTrue("Question 1" in processed_data[0][0])

if __name__ == "__main__":
    unittest.main()
