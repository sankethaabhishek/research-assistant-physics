import re

def split_into_sections(text):
    # Define possible headings in physics research papers
    section_titles = [
        "abstract",
        "introduction",
        "background",
        "related work",
        "methodology",
        "methods",
        "experiments",
        "results",
        "discussion",
        "conclusion",
        "references"
    ]

    # Create a regex pattern to find section headings (case-insensitive)
    pattern = r"(?i)(?<=\n)(" + "|".join(section_titles) + r")\s*\n"

    # Find all matches
    matches = list(re.finditer(pattern, text))

    if not matches:
        return {"full_text": text}  # Fallback if no matches

    sections = {}
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        title = matches[i].group(0).strip().lower()
        content = text[start:end].strip()
        sections[title] = content

    return sections
