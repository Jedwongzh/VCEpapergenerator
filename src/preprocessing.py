import os
import re
import PyPDF2
import json

def load_im2latex_mapping(mapping_file):
    """
    Loads a mapping of raw math formulas to their LaTeX representation
    from the im2latex-100k dataset.
    Expected JSON format: {"raw_formula": "LaTeX_formula", ...}
    """
    with open(mapping_file, "r", encoding="utf-8") as f:
        mapping = json.load(f)
    return mapping

def convert_formula_to_latex(text, mapping):
    """
    Detects math expressions in the text and replaces them with the LaTeX version
    from the mapping if available.

    This regex attempts to capture formulas typically seen in VCE Mathematics,
    including sequences with digits, letters, underscores, parentheses, exponents,
    and common operators (+, -, *, /, =).
    """
    # This regex captures one or more tokens (letters, digits, underscores, common math symbols)
    # separated by at least one operator with optional spaces.
    pattern = re.compile(r"([A-Za-z0-9\(\)_\^\{\}]+(?:\s*[\+\-\*/=]\s*[A-Za-z0-9\(\)_\^\{\}]+)+)")
    
    def repl(match):
        raw_formula = match.group(1)
        # Return the LaTeX equivalent if found in the mapping, else return the original.
        return mapping.get(raw_formula, raw_formula)
    
    return pattern.sub(repl, text)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyPDF2.
    """
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return text

def clean_text(text, formula_mapping=None):
    """
    Cleans the extracted text by removing extraneous characters,
    correcting OCR errors, standardizing spacing,
    and converting math formulas via the provided mapping.
    """
    if not text:
        return ""
    
    # Remove headers, footers, or isolated page texts.
    text = re.sub(r"^\s*Page\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[A-Za-z]+\s*$", "", text, flags=re.MULTILINE)
    
    # Correct common OCR errors.
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff")
    text = text.replace("l ", "1 ").replace("I ", "1 ")
    text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)
    text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)
    
    # Standardize spacing.
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    
    # Convert math formulas using the provided mapping (if available).
    if formula_mapping:
        text = convert_formula_to_latex(text, formula_mapping)
        
    return text

def process_pdf_files(data_dir, output_dir, formula_mapping=None):
    """
    Processes all PDF files in the specified directory:
      - Extracts text,
      - Cleans it (including math conversion),
      - Saves the cleaned text as a .txt file in the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Processing directory: {data_dir}")
    for filename in os.listdir(data_dir):
        if filename.lower().endswith(".pdf"):
            print(f"Found PDF: {filename}")
            pdf_path = os.path.join(data_dir, filename)
            text = extract_text_from_pdf(pdf_path)
            cleaned_text = clean_text(text, formula_mapping)
            
            # Save the cleaned text to an output file.
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(cleaned_text)
    print(f"Finished processing {data_dir}")

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Load the im2latex mapping file from the project root.
    mapping_path = os.path.join(project_root, "im2latex_mapping.json")
    formula_mapping = load_im2latex_mapping(mapping_path)
    
    # Define raw data directories.
    m1_raw_data_dir = os.path.join(project_root, "data", "raw", "methods", "Exam1")
    s1_raw_data_dir = os.path.join(project_root, "data", "raw", "spesh", "Exam1")
    m2_raw_data_dir = os.path.join(project_root, "data", "raw", "methods", "Exam2")
    s2_raw_data_dir = os.path.join(project_root, "data", "raw", "spesh", "Exam2")
    
    # Define output directories for processed text.
    processed_methods_dir_1 = os.path.join(project_root, "data", "processed", "proc_methods", "m1")
    processed_methods_dir_2 = os.path.join(project_root, "data", "processed", "proc_methods", "m2")
    processed_specialist_dir_1 = os.path.join(project_root, "data", "processed", "proc_specialist", "s1")
    processed_specialist_dir_2 = os.path.join(project_root, "data", "processed", "proc_specialist", "s2")
    
    # Process PDF files for both Methods and Specialist exams.
    process_pdf_files(m1_raw_data_dir, processed_methods_dir_1, formula_mapping)
    process_pdf_files(m2_raw_data_dir, processed_methods_dir_2, formula_mapping)
    process_pdf_files(s1_raw_data_dir, processed_specialist_dir_1, formula_mapping)
    process_pdf_files(s2_raw_data_dir, processed_specialist_dir_2, formula_mapping)

if __name__ == "__main__":
    main()