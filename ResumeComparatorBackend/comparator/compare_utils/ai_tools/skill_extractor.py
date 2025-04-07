import os
from typing import Dict

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from django.conf import settings
from comparator.compare_utils.ai_tools.device import get_device


def extract_skills(text: str) -> dict[str, list[dict[str, str | float]]]:
    """Extracts unique named entities (keywords) from text using the trained NER model."""

    model_path = os.path.join(
        settings.BASE_DIR, 'ai_models', 'lm-ner-linkedin-skills-recognition')

    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(model_path)

    # Create a pipeline for NER with an aggregation strategy
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple",
                   device=get_device())

    # Use the NER pipeline to identify hard skills
    ner_results = nlp(text)

    # Group results by entity_group
    grouped_results = {}
    for ent in ner_results:
        entity_group = ent['entity_group']
        if entity_group not in grouped_results:
            grouped_results[entity_group] = []

        # Add word and score to the entity info
        grouped_results[entity_group].append({
            "word": ent['word'],
            "score": ent['score']
        })

    return grouped_results