def evaluate_model(model, tokenizer, test_data):
    """
    Evaluates the trained model on the test data.
    """
    model.eval()  # Set the model to evaluation mode
    total_questions = len(test_data)
    correct_math_count = 0
    generated_questions = []

    for item in test_data:
        # Prepare the input text
        input_text = item['text']

        # Generate output from the model
        inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=200, num_return_sequences=1)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract the generated question
        generated_question_text = generated_text

        # Generate math expression (if any)
        generated_expression = generate_math_expression(item['expressions'][0])

        # Combine question and expression
        final_generated_question = generated_question_text.replace("MATH_EXPR", generated_expression)
        generated_questions.append(final_generated_question)

        # Basic Math Correctness Check
        if item['expressions'] and generated_expression.strip():
            try:
                sympy.parsing.mathematica.parse_mathematica(generated_expression)
                correct_math_count += 1
            except Exception:
                pass

    # Print some results
    print(f"Evaluated on {total_questions} questions.")
    print(f"Correctly generated math expressions: {correct_math_count}/{total_questions}")
    for i in range(3):  # print first 3 generated questions
        print(f"Generated Question {i+1}: {generated_questions[i]}")
    return generated_questions

def main():
    """
    Main function to evaluate both models.
    """
    # Load the tokenizer and model for VCE Methods
    methods_model, methods_tokenizer = prepare_llm(model_path='./models/methods/model.pt')
    # Load the test data for VCE Methods
    methods_test_data = load_test_data('./data/processed/methods')

    # Evaluate the VCE Methods model
    print("Evaluating VCE Methods Model:")
    evaluate_model(methods_model, methods_tokenizer, methods_test_data)

    # Load the tokenizer and model for VCE Specialist
    specialist_model, specialist_tokenizer = prepare_llm(model_path='./models/specialist/model.pt')
    # Load the test data for VCE Specialist
    specialist_test_data = load_test_data('./data/processed/specialist')

    # Evaluate the VCE Specialist model
    print("Evaluating VCE Specialist Model:")
    evaluate_model(specialist_model, specialist_tokenizer, specialist_test_data)

if __name__ == "__main__":
    main()