from transformers import Trainer, TrainingArguments, DataCollatorWithPadding
from data import load_and_prepare_data
from model import load_model_and_tokenizer
import torch

def train():
    print("🔄 Загружаем данные...")
    raw_data = load_and_prepare_data()
    
    model, tokenizer = load_model_and_tokenizer()
    
    def tokenize(examples):
        return tokenizer(examples["text"], truncation=True, max_length=256, padding=True)
    
    # Преобразуем в нужный формат
    tokenized = {"text": [item["text"] for item in raw_data],
                 "labels": [item["quality_score"] for item in raw_data]}
    
    tokenized = tokenize(tokenized)  # применяем токенизатор
    
    training_args = TrainingArguments(
        output_dir="models/descscore",
        num_train_epochs=2,
        per_device_train_batch_size=8,
        learning_rate=3e-5,
        weight_decay=0.01,
        logging_steps=10,
        save_strategy="no",
        report_to="none",
        fp16=False,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        data_collator=DataCollatorWithPadding(tokenizer),
    )
    
    print("🚀 Начинаем обучение модели...")
    trainer.train()
    
    model.save_pretrained("models/descscore")
    tokenizer.save_pretrained("models/descscore")
    print("✅ МОДЕЛЬ УСПЕШНО ОБУЧЕНА И СОХРАНЕНА!")
    return model, tokenizer