import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from src.schemas.report_schema import CVAnalysisReport
from src.prompts.analysis_prompt import ANALYSIS_PROMPT
from src.services.llm_factory import get_structured_llm

load_dotenv()

def analyze_cv(
    cv_sections: dict,
    rag_context: str,
    llm_config: Optional[Dict[str, Any]] = None
) -> CVAnalysisReport:
    """
    Analyzes CV sections against retrieved RAG guidelines using the user-specified LLM model.
    """
    structured_llm = get_structured_llm(llm_config, schema=CVAnalysisReport)
    
    # Build CV content, skipping internal sentinel keys (prefixed with _).
    # When a summary was detected without an explicit header, append a note so
    # the LLM can flag it in its recommendations.
    missing_summary_header = cv_sections.get("_missing_summary_header", "").strip() == "true"

    cv_content = "\n\n".join(
        [
            f"{section.upper()}:\n{content}"
            for section, content in cv_sections.items()
            if not section.startswith("_")
        ]
    )

    if missing_summary_header:
        cv_content += (
            "\n\n[SYSTEM NOTE]: A summary/profile paragraph was detected in this CV "
            "but it has NO section header (e.g. 'Professional Summary', 'Profile', "
            "'Objective'). In your analysis, highlight this under weaknesses and "
            "recommend adding a clear Summary section header."
        )
    
    prompt = ANALYSIS_PROMPT.format(
        context=rag_context,
        cv_content=cv_content
    )
    
    result = structured_llm.invoke(prompt)
    return result