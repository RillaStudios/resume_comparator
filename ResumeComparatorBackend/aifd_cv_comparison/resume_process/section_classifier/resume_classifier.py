from aifd_cv_comparison.config.ai_res_label_map import AI_RESUME_LABEL_MAP
from aifd_cv_comparison.models.model_loader import get_model
from aifd_cv_comparison.resume_process.section_classifier import regex_classifier
from aifd_cv_comparison.resume_process.section_classifier.utils.ai_classifier import ai_classifier
from aifd_cv_comparison.utils.chunk_text import chunk_text
from aifd_cv_comparison.utils.resume import Resume, ResumeContact
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

def classify_resume(resume: Resume) -> dict[str | list[str], str]:
    """
    Classifies the sections of a resume using regex patterns.

    Args:
        resume (Resume): The resume text to classify.

    Returns:
        dict: A dictionary containing classified sections of the resume.
    """
    # Use regex_classifier to classify the resume sections
    sections = regex_classifier(resume.raw_text)

    revised_sections = {}

    #Tokenizer
    tokenizer = get_model('resume_parser').tokenizer

    for section_key, section_content in sections.items():
        # Only apply AI classification if section is labeled as "other"
        if section_key == "other":
            # Handle long content with chunking
            chunks = chunk_text(section_content, max_chunk_size=512, tokenizer=tokenizer)

            # Classify each chunk
            votes = {}

            section_labels = ["awards", "certificates", "contact/name/title", "education",
                              "interests", "languages", "para", "professional_experiences",
                              "projects", "skills", "soft_skills", "summary"]

            for chunk in chunks:
                classifier_output = ai_classifier(chunk)
                logits = classifier_output.logits[0]
                predicted_class_idx = logits.argmax().item()
                predicted_label = section_labels[predicted_class_idx]
                votes[predicted_label] = votes.get(predicted_label, 0) + 1

            # Determine best section label based on votes
            if votes:
                winning_label = max(votes, key=votes.get)

                # Get the mapped label first
                revised_label = AI_RESUME_LABEL_MAP.get(winning_label)

                # Add to sections dict, appending if label already exists
                if revised_label in revised_sections:
                    revised_sections[revised_label] += "\n\n" + section_content
                else:
                    revised_sections[revised_label] = section_content

        else:
            # For non-"other" sections, keep the original label
            revised_sections[section_key] = section_content

    confidence_score = _check_class_confidence(revised_sections)

    resume.contact = ResumeContact(resume.raw_text)

    if confidence_score < 0.65:
        resume.bad_format = True
        fail_message = 'Resume was either badly formatted or unparsable. Will not continue with comparison.'
        resume.failing_list.append(fail_message)
    else:
        section_names = ['skills', 'education', 'experience', 'awards', 'certifications',
                         'hobbies', 'projects', 'summary', 'unknown']

        # Load NLTK resources
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))

        for section_name in section_names:
            section_text = revised_sections.get(section_name)
            if section_text:
                section_text = normalize_text(section_text, lemmatizer, stop_words)
            setattr(resume, section_name, section_text)

    # Return the classified sections
    return revised_sections

def _check_class_confidence(sections: dict[str | list[str], str]) -> float:
    """
    Calculate confidence score based on section coverage and content.

    Args:
        sections: Dictionary of classified sections

    Returns:
        float: Confidence score between 0.0 and 1.0

    @Author: IFD
    @Date: 2025-04-12
    """
    if not sections:
        print("No sections found, confidence = 0.0")
        return 0.0

    # Get all possible section labels from the map
    expected_sections = set(AI_RESUME_LABEL_MAP.values())
    # print(f"Expected sections: {expected_sections} (total: {len(expected_sections)})")

    # Remove "unknown" as it's not a real section type
    if "unknown" in expected_sections:
        expected_sections.remove("unknown")
        # print(f"Removed 'unknown', remaining: {len(expected_sections)}")

    # Count existing sections with content
    sections_with_content = 0
    found_sections = []
    for section_key, content in sections.items():
        if section_key in expected_sections:
            has_content = False
            if content and (isinstance(content, str) and content.strip() or
                            isinstance(content, list) and any(c.strip() for c in content)):
                sections_with_content += 1
                found_sections.append(section_key)
                has_content = True
            # print(f"Section '{section_key}': {'has content' if has_content else 'empty'}")

    # Show which sections are missing
    # missing_sections = expected_sections - set(found_sections)
    # print(f"Missing sections: {missing_sections}")

    # Calculate coverage ratio (how many expected sections exist with content)
    coverage_ratio = sections_with_content / len(expected_sections) if expected_sections else 0.0
    # print(f"Coverage ratio: {sections_with_content}/{len(expected_sections)} = {coverage_ratio:.2f}")

    # Add weight to important sections
    important_sections = {"education", "experience", "skills", "summary"}
    found_important = [s for s in important_sections if s in sections and sections[s]]
    # print(f"Important sections found: {found_important}")

    important_sections_coverage = len(found_important) / len(important_sections)
    # print(
    #     f"Important sections coverage: {len(found_important)}/{len(important_sections)} = {important_sections_coverage:.2f}")

    # Final confidence is weighted average of overall coverage and important section coverage
    confidence = (0.3 * coverage_ratio) + (0.7 * important_sections_coverage)
    # print(
    #     f"Final confidence: (0.3 * {coverage_ratio:.2f}) + (0.7 * {important_sections_coverage:.2f}) = {confidence:.2f}")

    return min(1.0, max(0.0, confidence))

def normalize_text(text, lemmatizer, stop_words):
    # Lowercase the text
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Lemmatize words
    text = ' '.join(lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words)
    return text