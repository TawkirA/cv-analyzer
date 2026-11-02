from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from src.schemas.ats_schema import ATSCategoryScore
from src.schemas.report_schema import SectionAnalysis


class ReportBody(BaseModel):
    """Final merged report, mirrors the keys produced by merge_reports()."""
    overall_score: Optional[float] = None
    ats_score: Optional[float] = None
    ats_breakdown: List[ATSCategoryScore] = Field(default_factory=list)
    ats_issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    missing_sections: List[str] = Field(default_factory=list)
    keyword_gaps: List[str] = Field(default_factory=list)
    section_analysis: List[SectionAnalysis] = Field(default_factory=list)
    final_recommendations: List[str] = Field(default_factory=list)


class AnalyzeResponse(ReportBody):
    """JSON returned by POST /analyze: the report plus request metadata."""
    filename: str
    model_used: str
    sections: Dict[str, str] = Field(default_factory=dict)


class PdfRequest(ReportBody):
    """Body for POST /report/pdf. The /analyze response can be posted as-is
    (extra keys such as `sections` are ignored)."""
    filename: Optional[str] = None
    model_used: Optional[str] = None


class ProviderInfo(BaseModel):
    provider: str
    models: List[str]
    default_model: str
    requires_project_id: bool = False


class ProvidersResponse(BaseModel):
    providers: List[ProviderInfo]
