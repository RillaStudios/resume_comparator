import os

import torch
from django.conf import settings
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from comparator.resume.extraction_tools.section_parser import split_into_sections

def classify_sections(resume_text: str) -> dict[str, str]:
    """
    Uses DistilBERT to classify extracted sections into predefined labels.
    """
    # Load the DistilBERT model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(os.path.join(
        settings.BASE_DIR, 'ai_models', 'distilbert-resume-parts-classify'))
    model = AutoModelForSequenceClassification.from_pretrained(os.path.join(
        settings.BASE_DIR, 'ai_models', 'distilbert-resume-parts-classify'))

    label_map = {
        0: 'awards',
        1: 'certifications',
        2: 'education_',
        3: 'exp_',
        4: 'extra',
        5: 'hobbies',
        6: 'personal_',
        7: 'projects_',
        8: 'references',
        9: 'skills',
        10: 'summary',
        11: 'training'
    }

    raw_sections = split_into_sections(resume_text)
    classified_sections = {}

    for section, text in raw_sections.items():
        # Skip empty sections
        if not text.strip():
            continue

        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            logits = model(**inputs).logits
            predicted_label = torch.argmax(logits, dim=1).item()

        section_name = label_map.get(predicted_label, "unknown")

        # If we already have content in this section, append rather than replace
        if section_name in classified_sections:
            classified_sections[section_name] += "\n\n" + text
        else:
            classified_sections[section_name] = text

    return classified_sections