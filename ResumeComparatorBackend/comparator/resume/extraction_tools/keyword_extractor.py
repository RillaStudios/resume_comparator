from pathlib import Path

import spacy
from django.conf import settings

model_path = Path(settings.BASE_DIR) / 'ai_models' / 'en_Resume_Matching_Keywords'

# Load the trained spaCy model
nlp = spacy.load(model_path)


def extract_keywords(text: str, target_labels=None):
    """Extracts unique named entities (keywords) from text using the trained NER model."""
    doc = nlp(text)

    if target_labels is None:
        target_labels = set(ent.label_ for ent in doc.ents)

    extracted_data = {label: set() for label in target_labels}  # Use sets to avoid duplicates

    for ent in doc.ents:
        if ent.label_ in target_labels:
            extracted_data[ent.label_].add(ent.text.lower().strip())  # Convert to lowercase and strip spaces

    return extracted_data