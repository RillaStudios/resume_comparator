import spacy
import re
from typing import Dict

def get_applicant_details(contact_info: str) -> Dict[str, str]:
    """
    Extract applicant's name and email from resume text.
    """
    result = {
        'name': '',
        'email': '',
        'phone': '',
        'address': '',
        'socials': [],
    }

    # Extract email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_matches = re.findall(email_pattern, contact_info)
    if email_matches:
        result["email"] = email_matches[0]

    # Get non-empty lines from the beginning
    lines = [line.strip() for line in contact_info.split('\n') if line.strip()]

    # First line handling with improved name extraction
    if lines:
        first_line = lines[0]

        # Remove common title indicators
        name_part = first_line.split(',')[0]  # Split by comma to remove titles

        # If there are other title separators like "|" or "-", remove them too
        for separator in [' - ', ' | ', ' — ', ' – ']:
            if separator in name_part:
                name_part = name_part.split(separator)[0]

        # Clean the name: remove extra spaces and format properly
        name_part = name_part.strip()
        words = [word.strip() for word in name_part.split() if word.strip()]

        if (1 <= len(words) <= 4 and  # Names typically have 1-4 words
                all(word[0].isupper() for word in words) and
                all(all(c.isalpha() or c == '-' for c in word) for word in words)):
            formatted_name = format_name(words)
            result["name"] = formatted_name
            return result

    # Fallback to spaCy NER with hyphen handling
    nlp = spacy.load("en_core_web_sm")

    # Add hyphenated name handling
    from spacy.lang.en import English
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