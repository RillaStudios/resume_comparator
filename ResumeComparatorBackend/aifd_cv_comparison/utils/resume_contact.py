import re
from aifd_cv_comparison.models.model_loader import get_model
from spacy.lang.en import English

class ResumeContact:

    name: str | None
    email: str | None
    phone: str | None

    def __init__(self, resume_text: str | None = None):

        # Initialize with default empty values
        self.name = ""
        self.email = ""
        self.phone = ""

        if resume_text:
            # Extract contact information
            extracted_info = extract_contact_info(resume_text)

            # Update instance attributes with extracted info
            self.name = extracted_info.get('name', None)
            self.email = extracted_info.get('email', None)
            self.phone = extracted_info.get('phone', None)


def extract_contact_info(resume_text: str) -> dict[str, str]:
    """
    Extract contact information from resume text.
    """
    # Initialize empty results
    result = {
        'name': '',
        'email': '',
        'phone': '',
        'address': '',
        'socials': [],
    }

    # Name extraction - keeping existing logic
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]

    if lines:
        first_line = lines[0]
        name_part = first_line.split(',')[0]

        for separator in [' - ', ' | ', ' — ', ' – ']:
            if separator in name_part:
                name_part = name_part.split(separator)[0]

        name_part = name_part.strip()
        words = [word.strip() for word in name_part.split() if word.strip()]

        if (1 <= len(words) <= 4 and
                all(word[0].isupper() for word in words) and
                all(all(c.isalpha() or c == '-' for c in word) for word in words)):
            result["name"] = format_name(words)
        else:
            # Fallback to spaCy NER
            nlp = get_model('spacy').model

            original_token_match = English.Defaults.token_match

            def custom_token_match(text):
                if re.match(r'^[A-Z][a-z]+(-[A-Z][a-z]+)+$', text):
                    return True
                return original_token_match(text) if original_token_match else None

            nlp.tokenizer.token_match = custom_token_match

            doc = nlp('\n'.join(lines[:10]))

            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    # Properly format the name
                    name = ent.text.strip()
                    words = [word.strip() for word in name.split() if word.strip()]
                    formatted_name = format_name(words)
                    result["name"] = formatted_name
                    break

    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.findall(email_pattern, resume_text)
    if email_matches:
        result["email"] = email_matches[0]

    # Extract phone
    phone_patterns = [
        r'\b(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}\b',
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        r'\b\d{10,11}\b'
    ]

    for pattern in phone_patterns:
        phones = re.findall(pattern, resume_text)
        if phones:
            # Strip all non-numeric characters, keeping only digits
            cleaned_phone = re.sub(r'\D', '', phones[0])
            result['phone'] = cleaned_phone
            break

    return result

def format_name(words: list[str]) -> str:
    # Format name to title case (first letter of each word capitalized)
    formatted_name = []
    for word in words:
        if '-' in word:
            # Handle hyphenated names like "Ford-Dow"
            subwords = word.split('-')
            formatted_word = '-'.join(sw.capitalize() for sw in subwords)
            formatted_name.append(formatted_word)
        else:
            formatted_name.append(word.capitalize())

    return ' '.join(formatted_name)