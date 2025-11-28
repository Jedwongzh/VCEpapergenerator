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
    Cleans the extracted text by removing headers, footers, and excessive whitespace.
    """
    # Remove common headers/footers (e.g., "VCE MATHEMATICAL METHODS")
    # This is a basic implementation and might need refinement based on actual PDF content
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # heuristic to remove page numbers or short header lines
        if len(line.strip()) < 5 and line.strip().isdigit():
            continue
        cleaned_lines.append(line.strip())
    
    text = '\n'.join(cleaned_lines)
    
    # Normalize whitespace but keep newlines
    # Replace multiple spaces/tabs with single space
    text = re.sub(r'[ \t]+', ' ', text).strip()
    # Replace multiple newlines with max 2 newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text

def chunk_text(text):
    """
    Chunks the text into questions.
    Assumes questions start with "Question X" or just "X." followed by text.
    """
    # Regex to find question starts. 
    # Matches "Question 1" or "1." 
    # We use a lookahead to split but keep the delimiter
    
    # Pattern: (Question \d+|^\d+\.)
    # We need to handle cases where "Question 1" is inside the text.
    
    # Improved regex:
    # Look for "Question <number>" or "<number>." at the start of a line or preceded by newline
    # But re.split doesn't handle lookbehinds easily for variable length.
    
    # Strategy: Use re.finditer to find all start positions, then slice.
    pattern = r"(?:^|\n\s*)(Question\s*\d+|\d+\.)"
    
    matches = list(re.finditer(pattern, text))
    
    if not matches:
        return [text]
        
    chunks = []
    start_idx = 0
    
    # If the first match is not at the beginning, capture the intro text
    if matches[0].start() > 0:
        chunks.append(text[:matches[0].start()].strip())
        
    for i in range(len(matches)):
        current_match = matches[i]
        match_start = current_match.start()
        # If the match started with \n, we want to include the text AFTER the \n as the start of the chunk
        # The group(1) is the actual "Question 1" part.
        # But we want the chunk to start with "Question 1".
        
        # The start of the content is match_start if it was ^, or match_start+1 if it was \n
        content_start = match_start
        if text[match_start] == '\n':
            content_start += 1
            
        # End of this chunk is start of next match
        if i < len(matches) - 1:
            next_match = matches[i+1]
            end_idx = next_match.start()
        else:
            end_idx = len(text)
            
        chunk_content = text[content_start:end_idx].strip()
        chunks.append(chunk_content)
        
    # Filter out very short chunks (likely noise)
    chunks = [c for c in chunks if len(c) > 20]
    
    return chunks

def extract_metadata(pdf_path, text):
    """
    Extracts metadata from the PDF path and content.
    """
    filename = os.path.basename(pdf_path)
    metadata = {
        "source": filename,
        "year": "Unknown",
        "subject": "Unknown",
        "topic": "General"
    }
    
    # Extract Year
    year_match = re.search(r"20\d{2}", filename)
    if year_match:
        metadata["year"] = year_match.group(0)
        
    # Extract Subject
    if "method" in filename.lower():
        metadata["subject"] = "Methods"
    elif "spec" in filename.lower():
        metadata["subject"] = "Specialist"
    elif "phys" in filename.lower():
        metadata["subject"] = "Physics"
        
    return metadata

def process_single_pdf(pdf_path, output_dir, use_ocr=False):
    """
    Processes a single PDF file: Extract -> Clean -> Chunk -> Metadata.
    Returns a list of (chunk_text, metadata) tuples.
    """
    print(f"Processing {pdf_path}...")
    text = extract_text_from_pdf(pdf_path, use_ocr=use_ocr)
    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text)
    base_metadata = extract_metadata(pdf_path, cleaned_text)
    
    processed_data = []
    for i, chunk in enumerate(chunks):
        meta = base_metadata.copy()
        meta["chunk_id"] = i
        # Simple topic detection based on keywords (can be improved with LLM later)
        if "function" in chunk.lower():
            meta["topic"] = "Functions"
        elif "calculus" in chunk.lower() or "derivative" in chunk.lower():
            meta["topic"] = "Calculus"
        elif "probability" in chunk.lower():
            meta["topic"] = "Probability"
            
        processed_data.append((chunk, meta))

    diagram_output_dir = os.path.join(output_dir, "diagrams")
    extract_diagrams(pdf_path, diagram_output_dir)
    
    return processed_data

if __name__ == "__main__":
    # Example usage
    # pdf_path = "path/to/your/pdf.pdf"
    # output_dir = "path/to/output"
    # data = process_single_pdf(pdf_path, output_dir)
    # print(data)
    pass
