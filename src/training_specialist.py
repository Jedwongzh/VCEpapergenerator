import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from src.preprocessing import load_and_preprocess_data
from src.config import DATA_DIR, MODEL_DIR

def train_specialist_model():
    # Load and preprocess the data
    processed_data = load_and_preprocess_data(os.path.join(DATA_DIR, 'processed', 'specialist'))
    if not processed_data:
        print("No processed data found for Specialist Maths. Exiting.")
        return

    # Split the data into training and validation sets
    train_data = processed_data[:int(len(processed_data) * 0.8)]
    val_data = processed_data[int(len(processed_data) * 0.8):]

    # Prepare the model and tokenizer
    model_name = "gpt2"  # You can choose a different model if needed
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Tokenize the data
    train_encodings = tokenizer([item['text'] for item in train_data], truncation=True, padding=True)
    val_encodings = tokenizer([item['text'] for item in val_data], truncation=True, padding=True)

    # Create a PyTorch dataset
    class MathDataset(torch.utils.data.Dataset):
        def __init__(self, encodings):
            self.encodings = encodings

        def __getitem__(self, idx):
            return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

        def __len__(self):
            return len(self.encodings.input_ids)

    train_dataset = MathDataset(train_encodings)
    val_dataset = MathDataset(val_encodings)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=os.path.join(MODEL_DIR, 'specialist'),  # Output directory
        num_train_epochs=3,  # Number of training epochs
        per_device_train_batch_size=4,  # Batch size per device during training
        per_device_eval_batch_size=4,  # Batch size for evaluation
        warmup_steps=500,  # Number of warmup steps for learning rate scheduler
        weight_decay=0.01,  # Strength of weight decay
        logging_dir='./logs',  # Directory for storing logs
        logging_steps=10,
        evaluation_strategy="steps",  # When to evaluate
        eval_steps=20,
        save_steps=100,
        load_best_model_at_end=True,
    )

    # Create a Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    # Train the model
    trainer.train()

    # Save the model
    model.save_pretrained(os.path.join(MODEL_DIR, 'specialist'))
    tokenizer.save_pretrained(os.path.join(MODEL_DIR, 'specialist'))

if __name__ == "__main__":
    train_specialist_model()