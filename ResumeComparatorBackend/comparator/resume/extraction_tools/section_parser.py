import re


def split_into_sections(resume_text: str) -> dict[str, str]:
    """
    Splits resume text by known section headers and then relocates any education content
    found under 'experience' into its own 'education_' section if a dedicated header is missing.
    """

    section_titles = [
        "awards", "certifications", "education", "experience", "projects", "skills", "skills & abilities",
        "summary", "training", "hobbies", "references", "tech skills", "soft skills", "profile",
        "personal projects", "exp", "edu", "professional experience", "work history", "employment history",
        "career history", "publications", "languages", "volunteer experience", "leadership", "achievements",
        "affiliations", "professional affiliations", "internships", "research", "coursework", "honors",
        "courses", "activities", "qualifications", "interests", "objective", "career objective",
        "technical skills", "professional skills", "core competencies", "key skills", "areas of expertise",
        "academic background", "educational qualifications", "professional development",
        "highlights of qualifications"
    ]

    # Create regex pattern
    section_pattern = re.compile(r"(?i)^(?:{}):?".format("|".join(section_titles)))

    sections = {}
    current_section = None
    section_content = []

    # Process each line
    for line in resume_text.split("\n"):
        line = line.strip()

        # Check if the line is a section header
        if section_pattern.match(line):
            if current_section:
                sections[current_section] = "\n".join(section_content).strip()

            current_section = line
            section_content = []
        elif current_section:
            section_content.append(line)

    # Store last section
    if current_section:
        sections[current_section] = "\n".join(section_content).strip()

    return sections