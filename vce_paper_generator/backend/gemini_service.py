import os
import google.generativeai as genai

# Configure Gemini
# Assumes GEMINI_API_KEY is set in environment variables
if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_model():
    """
    Returns the configured Gemini model.
    """
    return genai.GenerativeModel('gemini-1.5-flash')

def generate_question(context_chunks, topic, difficulty):
    """
    Generates a VCE-style question using Gemini and provided context.
    
    Args:
        context_chunks (list): List of strings containing similar questions/content.
        topic (str): The topic to generate for.
        difficulty (str): Difficulty level (Easy, Medium, Hard).
        
    Returns:
        str: The generated question text.
    """
    model = get_model()
    
    context_str = "\n\n".join(context_chunks)
    
    prompt = f"""
    You are an expert VCE (Victorian Certificate of Education) exam writer.
    
    Your task is to write a NEW {difficulty} difficulty question for the topic: {topic}.
    
    Here are some examples of previous VCE questions for this topic to guide the STYLE and FORMATTING:
    
    --- EXAMPLES START ---
    {context_str}
    --- EXAMPLES END ---
    
    INSTRUCTIONS:
    1. Write a completely new question that mimics the style, terminology, and structure of the examples.
    2. Ensure the difficulty matches '{difficulty}'.
    3. Do NOT copy the examples directly.
    4. Provide the question text clearly.
    5. If the question requires a diagram, describe the diagram in [brackets] like [Diagram: description...].
    6. Provide a marking scheme/solution at the end, separated by "--- SOLUTION ---".
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating question with Gemini: {e}")
        return "Error generating question."

def explain_question(question_text, context_chunks):
    """
    Explains a question using Gemini and provided context.
    """
    model = get_model()
    
    context_str = "\n\n".join(context_chunks)
    
    prompt = f"""
    You are an expert VCE tutor.
    
    Please explain the following question step-by-step to a student.
    
    QUESTION:
    {question_text}
    
    RELEVANT CONTEXT (Formulas, similar examples):
    {context_str}
    
    INSTRUCTIONS:
    1. Break down the problem into clear steps.
    2. Explain the reasoning for each step.
    3. Reference relevant formulas or concepts from the context if applicable.
    4. Highlight common mistakes students make.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error explaining question with Gemini: {e}")
        return "Error generating explanation."
