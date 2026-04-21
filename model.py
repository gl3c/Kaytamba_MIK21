from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "cointegrated/rubert-tiny2"  # маленькая и быстрая русская модель

def load_model_and_tokenizer(num_labels=1):  # 1 = regression (оценка 0-10)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=num_labels, problem_type="regression"
    )
    return model, tokenizer