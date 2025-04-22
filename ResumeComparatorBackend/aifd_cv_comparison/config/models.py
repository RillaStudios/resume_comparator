import os
import spacy
import torch
from llama_cpp import Llama
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoModelForCausalLM, pipeline

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
    },
    "spacy": {
        "name": "spaCy NER Model",
        "model": spacy.load("en_core_web_sm"),
        "tokenizer": None,
    },
    "spacy_lg": {
        "name": "spaCy Large NER Model",
        "model": spacy.load("en_core_web_lg"),
        "tokenizer": None,
    },
    "doc2vec": {
        "name": "Doc2Vec Model",
        "model": os.path.join(model_path, "cv_job_maching.model"),
        "tokenizer": None,
    },
    "phi": {
        "name": "Phi Model",
        "model": Llama(model_path=os.path.join(model_path, "Phi-4-mini-instruct-Q3_K_L.gguf"), n_threads=4),
        "tokenizer": None,
    }
}