from src.graph.workflow import build_workflow

sections =  {
"summary": """
Python backend developer with AI experience.
""",
"skills": """
Python, FastAPI, LangChain, AWS, SQL
""",
"experience": """
Developed AI-powered systems and APIs.
Worked on scalable backend services.
""",
"education": """
Bachelor of in Computer Science
"""
}

app = build_workflow()

initial_state = {
    "cv_sections": sections
}

result = app.invoke(initial_state)

print("\n")
print("=" * 80)
print("FINAL WORKFLOW OUTPUT")
print("=" * 80)
print(result["analysis_report"])