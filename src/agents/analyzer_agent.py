import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from src.schemas.report_schema import CVAnalysisReport
from src.prompts.analysis_prompt import ANALYSIS_PROMPT

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model='gemini-3.5-flash-lite',
    temperature=0
)

structured_llm = llm.with_structured_output(CVAnalysisReport)

def analyze_cv(cv_sections: dict, rag_context: str) -> CVAnalysisReport:
    cv_content = "\n\n".join(
        [
            f"{section.upper()}:\n{content}" for section, content in cv_sections.items()
        ]
    )
    
    prompt = ANALYSIS_PROMPT.format(
        context = rag_context,
        cv_content = cv_content
    )
    
    result = structured_llm.invoke(prompt)
    
    return result