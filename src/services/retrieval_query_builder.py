def build_search_query(sections: dict) -> str:
    summary = sections.get("summary", "")
    skills = sections.get("skills", "")
    experience = sections.get("experience", "")
    education = sections.get("education", "")
    query = f"""
    Resume analysis standards for the following candidate profile.
    Candidate Summary:
    {summary}
    Technical Skills:
    {skills}
    Experience:
    {experience}
    Education:
    {education}
    Retrieve guidance related to:
    - ATS optimization
    - Resume best practices
    - Resume formatting standards
    - Content effectiveness
    - Resume section
    - Content effectiveness
    - Resume section quality
    - Technical resume evaluation
    - Skill presentation
    """
    return query.strip()