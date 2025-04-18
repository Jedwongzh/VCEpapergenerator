import os
import re
import PyPDF2

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

def clean_text(text):
    """
    Cleans the extracted text by removing extraneous characters,
    handling common OCR errors, and standardizing formatting.
    """
    if not text:
        return ""

    # Remove headers, footers, page numbers (basic example - adjust as needed)
    text = re.sub(r"^\s*Page\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[A-Za-z]+\s*$", "", text, flags=re.MULTILINE)

    # Correct common OCR errors
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff")
    text = text.replace("l ", "1 ").replace("I ", "1 ")
    text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)
    text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)

    # Standardize formatting
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text

def process_pdf_files(data_dir, output_dir):
    """
    Processes all PDF files in the specified directory and saves the cleaned text
    to the output directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Processing directory: {data_dir}")
    for filename in os.listdir(data_dir):
        if filename.lower().endswith(".pdf"):
            print(f"Found PDF: {filename}")
            pdf_path = os.path.join(data_dir, filename)
            text = extract_text_from_pdf(pdf_path)
            cleaned_text = clean_text(text)

            # Save cleaned text to a file
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(cleaned_text)
    print(f"Finished processing {data_dir}")

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    m1_raw_data_dir = os.path.join(project_root, "data", "raw", "methods", "Exam1")
    s1_raw_data_dir = os.path.join(project_root, "data", "raw", "spesh", "Exam1")
    m2_raw_data_dir = os.path.join(project_root, "data", "raw", "methods", "Exam2")
    s2_raw_data_dir = os.path.join(project_root, "data", "raw", "spesh", "Exam2")
    
    # Output directory for processed Methods data
    processed_methods_dir_1 = os.path.join(project_root, "data", "processed", "proc_methods", "m1")
    processed_methods_dir_2 = os.path.join(project_root, "data", "processed", "proc_methods", "m2")
    
    # Output directory for processed Specialist data
    processed_specialist_dir_1 = os.path.join(project_root, "data", "processed", "proc_specialist", "s1")
    processed_specialist_dir_2 = os.path.join(project_root, "data", "processed", "proc_specialist", "s2")
    
    # Process PDF files for both Methods and Specialist
    process_pdf_files(m1_raw_data_dir, processed_methods_dir_1)
    process_pdf_files(m2_raw_data_dir, processed_methods_dir_2)
    
    process_pdf_files(s1_raw_data_dir, processed_specialist_dir_1)
    process_pdf_files(s2_raw_data_dir, processed_specialist_dir_2)

if __name__ == "__main__":
    main()