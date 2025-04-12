import re
from aifd_cv_comparison.config.resume_headers import RESUME_HEADER_KEYWORDS

def regex_classifier(text: str) -> dict[str, str]:

    sections = {}
    current_label = "other"
    current_lines = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        matched = False
        for pattern, label in RESUME_HEADER_KEYWORDS.items():
            if re.match(rf"^{pattern}[:\s]*$", line.lower()):
                if current_lines:
                    sections[current_label] = "\n".join(current_lines).strip()
                    current_lines = []
                current_label = label
                matched = True

                break

        if not matched:
            current_lines.append(line)

    if current_lines:
        sections[current_label] = "\n".join(current_lines).strip()

    return sections
