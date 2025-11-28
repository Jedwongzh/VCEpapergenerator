import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_exam_pdf(questions, filename, subject="General", year_level="12"):
    """
    Generates a PDF exam paper.
    
    Args:
        questions (list): List of dicts with 'question' and 'topic'.
        filename (str): Output filename.
        subject (str): Subject name.
        year_level (str): Year level.
        
    Returns:
        str: Path to the generated PDF.
    """
    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='QuestionBody', parent=styles['Normal'], spaceAfter=12, leading=14))
    styles.add(ParagraphStyle(name='QuestionTitle', parent=styles['Heading2'], spaceAfter=6))
    
    story = []
    
    # Cover Page
    story.append(Paragraph(f"VICTORIAN CERTIFICATE OF EDUCATION", styles['Title']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(f"{subject.upper()} - YEAR {year_level}", styles['Heading1']))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("STUDENT NAME: _________________________________", styles['Normal']))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("INSTRUCTIONS:", styles['Heading2']))
    story.append(Paragraph("1. Answer all questions in the spaces provided.", styles['Normal']))
    story.append(Paragraph("2. A formula sheet is provided.", styles['Normal']))
    story.append(PageBreak())
    
    # Questions
    for i, q_data in enumerate(questions):
        q_text = q_data.get("question", "")
        topic = q_data.get("topic", "")
        
        # Format the question text (handle newlines)
        q_text = q_text.replace("\n", "<br/>")
        
        story.append(Paragraph(f"Question {i+1} ({topic})", styles['QuestionTitle']))
        story.append(Paragraph(q_text, styles['QuestionBody']))
        story.append(Spacer(1, 1*cm))
        
        # Add space for answer
        story.append(Paragraph("Answer:", styles['Normal']))
        story.append(Spacer(1, 4*cm)) # Space for writing
        
    doc.build(story)
    return filename

if __name__ == "__main__":
    # Test
    qs = [
        {"question": "Find the derivative of f(x) = x^2.", "topic": "Calculus"},
        {"question": "Solve for x: 2x + 5 = 10.", "topic": "Algebra"}
    ]
    create_exam_pdf(qs, "test_exam.pdf")
    print("Created test_exam.pdf")
