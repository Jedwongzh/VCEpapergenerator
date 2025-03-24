import os
import argparse
import aspose.pdf as ap
from preprocessing import preprocessing_function  # Adjust the import based on the actual function name

def convert_pdf_to_latex(pdf_path, tex_path):
    """
    Converts a PDF file to a LaTeX (.tex) file using Aspose.PDF.
    """
    try:
        # Open the PDF document
        document = ap.Document(pdf_path)
        # Create LaTeX save options
        save_options = ap.LaTeXSaveOptions()
        # Save the document as a .tex file
        document.save(tex_path, save_options)
        print(f"Successfully created LaTeX file: {tex_path}")
    except Exception as e:
        print(f"Error converting {pdf_path} to LaTeX: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF file to a LaTeX (.tex) file using Aspose.PDF."
    )
    parser.add_argument("--pdf", required=True, help="Path to the PDF file to convert (e.g. 'test.pdf')")
    args = parser.parse_args()
    
    pdf_file = args.pdf
    # If a relative path is provided, make it relative to this script's directory
    if not os.path.isabs(pdf_file):
        pdf_file = os.path.join(os.path.dirname(__file__), pdf_file)
    
    # Call the preprocessing function and print the result
    preprocessing_result = preprocessing_function(pdf_file)
    print(f"Preprocessing result: {preprocessing_result}")
    
    # Create output TEX file with the same basename as the input PDF
    base_name = os.path.splitext(os.path.basename(pdf_file))[0]
    tex_file = os.path.join(os.path.dirname(pdf_file), base_name + ".tex")
    
    convert_pdf_to_latex(pdf_file, tex_file)

if __name__ == "__main__":
    main()
