from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
import os
from src.utils import load_processed_data, save_model

def prepare_model(model_name="gpt2"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        model.resize_token_embeddings(len(tokenizer))

    return model, tokenizer

def train_model(model, tokenizer, train_data, val_data, output_dir):
    train_encodings = tokenizer([item['text'] for item in train_data], truncation=True, padding=True)
    val_encodings = tokenizer([item['text'] for item in val_data], truncation=True, padding=True)

    class MathDataset(torch.utils.data.Dataset):
        def __init__(self, encodings):
            self.encodings = encodings

        def __getitem__(self, idx):
            return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

        def __len__(self):
            return len(self.encodings.input_ids)

    train_dataset = MathDataset(train_encodings)
    val_dataset = MathDataset(val_encodings)

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="steps",
        eval_steps=20,
        save_steps=100,
        load_best_model_at_end=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )

    trainer.train()
    save_model(model, output_dir)

def main():
    data_dir = "./data/processed/methods"
    output_dir = "./models/methods"
    
    train_data = load_processed_data(os.path.join(data_dir, "train.json"))
    val_data = load_processed_data(os.path.join(data_dir, "val.json"))

    model, tokenizer = prepare_model()
    train_model(model, tokenizer, train_data, val_data, output_dir)

if __name__ == "__main__":
    main()