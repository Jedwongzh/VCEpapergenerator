# vce_paper_generator/data_preparation/processing.py

import os
import re
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

def ocr_pdf(pdf_path):
    """
    Performs OCR on a PDF file and extracts text.
    """
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img_bytes = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_bytes))
            text += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error processing {pdf_path} with OCR: {e}")
    return text

def extract_text_from_pdf(pdf_path, use_ocr=False):
    """
    Extracts text from a PDF file, with an option to use OCR.
    """
    if use_ocr:
        return ocr_pdf(pdf_path)

    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return text

def extract_diagrams(pdf_path, output_dir):
    """
    Extracts diagrams and images from a PDF file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            image_list = doc.get_page_images(page_num)
            for image_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = f"image_{page_num+1}_{image_index+1}.{image_ext}"
                with open(os.path.join(output_dir, image_filename), "wb") as f:
                    f.write(image_bytes)
    except Exception as e:
        print(f"Error extracting images from {pdf_path}: {e}")

def clean_text(text):
    """
    Cleans the extracted text.
    """
    # Placeholder for cleaning logic
    return text.strip()

def chunk_text(text):
    """
    Chunks the text into questions, marking schemes, etc.
    """
    # Placeholder for chunking logic
    return [text]

def process_single_pdf(pdf_path, output_dir, use_ocr=False):
    """
    Processes a single PDF file.
    """
    text = extract_text_from_pdf(pdf_path, use_ocr=use_ocr)
    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text)

    # Placeholder for saving chunks and metadata
    print(f"Processed {pdf_path} with {len(chunks)} chunks.")

    diagram_output_dir = os.path.join(output_dir, "diagrams")
    extract_diagrams(pdf_path, diagram_output_dir)

if __name__ == "__main__":
    # Example usage
    pdf_path = "path/to/your/pdf.pdf"
    output_dir = "path/to/output"
    process_single_pdf(pdf_path, output_dir, use_ocr=True)
