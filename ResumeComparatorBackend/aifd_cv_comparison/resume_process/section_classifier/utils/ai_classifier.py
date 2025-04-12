from aifd_cv_comparison.models.model_loader import get_model


def ai_classifier(section: str):

    model = get_model('resume_parser')

    inputs = model.tokenizer(section, return_tensors="pt", truncation=True, padding=True)
    outputs = model.model(**inputs)

    return outputs