from src.services.ats_engine import (
    generate_ats_report
)

sample_sections = {
    "summary": """
    Python backend developer with cloud experience.
    """,
    "skills": """
    Python, FastAPI, AWS, SQL, FastAPI, AWS, SQL, Docker
    """,
    "experience": """
    Built APIs and cloud solutions.
    """,
    "education": """
    of Technology
    """,
    "certifications": """
    aws certified
    """
}

report = generate_ats_report(sample_sections)
print(
    report.model_dump_json(indent=2)
)