import torch
import numpy as np
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

LABEL_MAP = {
    0: "Neutral",
    1: "Positive",
    2: "Negative"
}


def load_base_models(model_paths):
    loaded_models = {}

    for name, path in model_paths.items():
        tokenizer = AutoTokenizer.from_pretrained(path)
        model = AutoModelForSequenceClassification.from_pretrained(path)
        model.to(DEVICE)
        model.eval()

        loaded_models[name] = {
            "tokenizer": tokenizer,
            "model": model
        }

    return loaded_models


def load_boosting_model(path):
    return joblib.load(path)


def ensemble_predict(texts, loaded_models, boosting_model):
    all_logits = []

    for model_info in loaded_models.values():
        tokenizer = model_info["tokenizer"]
        model = model_info["model"]

        inputs = tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        ).to(DEVICE)

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits.cpu().numpy()
            all_logits.append(logits)

    ensemble_logits = np.array(all_logits)

    n_models, n_samples, n_classes = ensemble_logits.shape
    X_boost = ensemble_logits.transpose(1, 0, 2).reshape(n_samples, n_models * n_classes)

    preds = boosting_model.predict(X_boost)
    probs = boosting_model.predict_proba(X_boost)

    sentiments = [LABEL_MAP[p] for p in preds]
    confidence = probs.max(axis=1)

    return sentiments, confidence