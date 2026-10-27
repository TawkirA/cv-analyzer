from typing import TypedDict, Dict, Any, Optional

class GraphState(TypedDict, total=False):
    cv_sections: Dict[str, str]
    retrieval_query: str
    rag_context: str
    ats_report: Dict[str, Any]
    llm_analysis: Dict[str, Any]
    analysis_report: Dict[str, Any]
    final_report: Dict[str, Any]
    llm_config: Optional[Dict[str, Any]]
    
