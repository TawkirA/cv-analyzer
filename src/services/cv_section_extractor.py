import re

SECTION_PATTERNS = {
    "summary": r"^(summary|professional summary|executive summary|profile|professional profile|career summary|career objective|objective|about me|personal profile|profile summary|summary of qualifications|professional overview|overview|career profile|personal statement|summary profile|professional objective)$",
    "experience": r"^(experience|work experience|employment history|professional experience|work history|career history|relevant experience|professional background|internship experience|internships)$",
    "education": r"^(education|academic background|educational qualifications|academic history|degrees|qualifications|academic qualifications|education & credentials)$",
    "skills": r"^(skills|technical skills|core competencies|technologies|tools & technologies|tech stack|key skills|areas of expertise|competencies|skills & competencies|technical expertise|skills & tools)$",
    "projects": r"^(projects|project experience|project details|key projects|selected projects|personal projects|academic projects)$",
    "certifications": r"^(certifications|licenses|certifications & licenses|certifications & trainings|trainings|courses|accreditations|awards|achievements|certifications and achievements|achievements & extracurricular activities)$",
    "languages": r"^(languages|language proficiencies|languages known)$",
    "additional": r"^(additional information|interests|hobbies & interests|hobbies|activities|volunteer experience|volunteering)$"
}

# Sections where sub-category labels (e.g. "Languages:", "Cloud Platforms:") are
# common and must NOT be treated as top-level section headers.
_INLINE_HEADER_BLOCKED_SECTIONS = {"skills", "experience", "projects", "education"}

# Bullet / list-marker prefix — lines starting with these are content, not headers.
_BULLET_PREFIX_RE = re.compile(r"^[\-\•\*\–\—\>✓►▸▪◦·]+\s")


def _clean_header_candidate(line: str) -> str:
    """Strip markdown symbols, numbers, bullets, and trailing punctuation."""
    # Remove markdown headers and emphasis (#, ##, **, __, *)
    cleaned = re.sub(r"^[#*_~\s\d\.\-\•\*\>\–\—]+", "", line).strip()
    # Remove trailing colons, dashes, pipes, etc.
    cleaned = re.sub(r"[:\-\–\—\|]+$", "", cleaned).strip()
    return cleaned.lower()


def _match_section(header_text: str) -> str | None:
    """Matches a cleaned header candidate against SECTION_PATTERNS."""
    for section_name, pattern in SECTION_PATTERNS.items():
        if re.search(pattern, header_text):
            return section_name
    return None


# Patterns that identify a line as contact / metadata rather than prose.
_CONTACT_LINE_RE = re.compile(
    r"(@|linkedin\.com|github\.com|http[s]?://|www\.|"
    r"\+\d|\(\d{3}\)|\d{3}[-.\s]\d{3}|\|)",
    re.IGNORECASE,
)


def _looks_like_prose(text: str) -> bool:
    """
    Returns True when a block of text reads like a prose paragraph (summary-like)
    rather than contact / header metadata.
    Heuristics:
      - At least one non-contact line with >= 8 words
      - Contains common summary / professional verbs or descriptors
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    # Exclude lines that are clearly contact / location metadata
    prose_candidates = [
        l for l in lines
        if len(l.split()) >= 8 and not _CONTACT_LINE_RE.search(l)
    ]
    if not prose_candidates:
        return False
    combined = " ".join(prose_candidates).lower()
    summary_signals = (
        r"\b(experience|expertise|professional|seeking|developer|engineer|manager|"
        r"passionate|motivated|skilled|background|proven|results|speciali[sz]|"
        r"years of|accomplished|deliver|drive|lead|build|architect)\b"
    )
    return bool(re.search(summary_signals, combined))


def extract_sections(text: str) -> dict:
    lines = text.split("\n")
    sections = {}
    current_section = "header"

    for line in lines:
        line_stripped = line.strip()

        if not line_stripped:
            continue

        # Stop processing if metadata/evaluation separator in test files is reached
        if re.match(r"^={4,}", line_stripped):
            break

        # Check for inline header pattern like "SKILLS: Python, SQL..." or "OBJECTIVE: Seeking..."
        # Guard 1: skip if the line starts with a bullet/list marker — it's content, not a header.
        # Guard 2: skip if we are inside a section where sub-labels are expected (e.g. skills).
        if ":" in line_stripped and not _BULLET_PREFIX_RE.match(line_stripped):
            if current_section not in _INLINE_HEADER_BLOCKED_SECTIONS:
                parts = line_stripped.split(":", 1)
                candidate = _clean_header_candidate(parts[0])
                matched_sec = _match_section(candidate)
                if matched_sec and len(candidate.split()) <= 6:
                    current_section = matched_sec
                    inline_body = parts[1].strip()
                    if inline_body:
                        sections.setdefault(current_section, []).append(inline_body)
                    continue

        # Check standalone header candidate
        candidate = _clean_header_candidate(line_stripped)

        # Guard: standalone headers are generally short (< 60 chars and <= 6 words)
        if len(candidate) <= 60 and len(candidate.split()) <= 6:
            matched_sec = _match_section(candidate)
            if matched_sec:
                current_section = matched_sec
                sections.setdefault(current_section, [])
                continue

        sections.setdefault(current_section, []).append(line_stripped)

    # --- Implicit summary promotion ---
    # If a "header" bucket contains prose paragraphs (no recognised summary header
    # was found), promote that prose to "summary" and flag the missing header.
    if "header" in sections and "summary" not in sections:
        header_lines = [l for l in sections["header"] if l.strip()]
        # A line is "contact/name" if it matches contact patterns OR is short (≤ 6 words).
        # Prose lines are long AND don't look like contact metadata.
        contact_lines = [
            l for l in header_lines
            if len(l.split()) <= 6 or _CONTACT_LINE_RE.search(l)
        ]
        prose_lines = [
            l for l in header_lines
            if len(l.split()) > 6 and not _CONTACT_LINE_RE.search(l)
        ]
        prose_block = "\n".join(prose_lines).strip()
        if prose_block and _looks_like_prose(prose_block):
            # Keep only contact / name lines in header
            sections["header"] = contact_lines
            # Promote prose to summary and tag it
            sections["summary"] = prose_lines
            sections["_missing_summary_header"] = ["true"]

    # --- Languages are not analysed ---
    # The "languages" bucket is only used to stop a preceding section from
    # absorbing its lines. Any prose that ended up inside it (e.g. a summary
    # placed after a LANGUAGES block) is rescued into "summary"; the rest is dropped.
    if "languages" in sections:
        lang_lines = sections.pop("languages")
        rescued = [
            l for l in lang_lines
            if len(l.split()) >= 8 and not _CONTACT_LINE_RE.search(l)
        ]
        if rescued and _looks_like_prose("\n".join(rescued)):
            sections.setdefault("summary", []).extend(rescued)

    # Filter out empty sections
    result = {}
    for key, value in sections.items():
        content = "\n".join(value).strip()
        if content:
            result[key] = content

    return result