import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Get absolute path to the models directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, "models", "ai_models")

MODEL_REGISTRY = {
    "resume_parser": {
        "name": "Resume Parser Model",
        "model": AutoModelForSequenceClassification.from_pretrained(
            os.path.join(model_path, "extended_distilBERT-finetuned-resumes-sections"),
            local_files_only=True
        ),
        "tokenizer": AutoTokenizer.from_pretrained(
            os.path.join(model_path, "extended_distilBERT-finetuned-resumes-sections"),
            local_files_only=True
        )
    }
}