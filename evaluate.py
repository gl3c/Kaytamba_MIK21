from transformers import pipeline
import torch

def evaluate_description(description: str, model_path="models/descscore"):
    pipe = pipeline(
        "text-classification",
        model=model_path,
        tokenizer=model_path,
        function_to_apply="none"  # для regression
    )
    result = pipe(description)[0]
    score = round(torch.sigmoid(torch.tensor(result['score'])).item() * 10, 1)  # приводим к 0-10
    return score