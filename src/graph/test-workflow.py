import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure workspace root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

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
print(result.get("final_report", result.get("analysis_report")))