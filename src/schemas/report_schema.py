from pydantic import BaseModel
from typing import List

class SectionAnalysis(BaseModel):
    section_name: str
    score: float
    findings: List[str]
    suggestions: List[str]

class CVAnalysisReport(BaseModel):
    overall_score: float
    ats_score: float
    strengths: List[str]
    weaknesses: List[str]
    missing_sections: List[str]
    keyword_gaps: List[str]
    section_analysis: List[SectionAnalysis]
    final_recommendations: List[str]