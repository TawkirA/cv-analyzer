from pydantic import BaseModel
from typing import List

class ATSCategoryScore(BaseModel):
    category: str
    score: float
    max_score: float
    reason: str
    
class ATSReport(BaseModel):
    total_score: float
    breakdown: List[ATSCategoryScore]
    issues: List[str]
    recommendations: List[str]
    
    
    