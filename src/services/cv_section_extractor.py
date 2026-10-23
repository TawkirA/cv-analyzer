import re
SECTION_PATTERNS = {
    "summary": r"^(summary|professional summary|profile|professional profile)$",
    "experience": r"^(experience|work experience|employment history|professional experience)$",
    "education": r"^(education|academic background|dducational qualifications)$",
    "skills": r"^(skills|technical skills|core competencies)$",
    "projects": r"^(projects|project experience|project details)$",
    "certifications": r"^(certifications|licenses|trainings|achievements)$"
}

def extract_sections(text: str) -> dict:
    lines = text.split("\n")
    sections = {}
    current_section = "unknown"
    
    for line in lines:
        line_clean = line.strip().lower()
        
        if not line_clean:
            continue
        
        matched = False
        for section_name, pattern in SECTION_PATTERNS.items():
            if re.search(pattern, line_clean):
                current_section = section_name
                sections.setdefault(current_section, [])
                matched = True
                break
            
        if not matched:
            sections.setdefault(current_section, []).append(line)
            
    return {
        key: "\n".join(value).strip()
        for key, value in sections.items()
    }