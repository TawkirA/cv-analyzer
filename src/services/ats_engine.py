import re
from src.schemas.ats_schema import (ATSCategoryScore, ATSReport)

REQUIRED_SECTIONS = ["summary", "experience", "skills", "education"]
OPTIONAL_SECTIONS = ["projects", "certifications"]
ATS_KEYWORDS = [
    "python",
    "aws",
    "docker",
    "sql",
    "ci/cd",
    "git",
    "kubernetes",
    "microservices",
    "javascript",
    "typescript",
    "html",
    "react",
    "angular",
    "nodejs",
    "express",
    "nextjs",
    "gen ai",
    "agentic ai",
    "ai"
]

# "python",
#     "aws",
#     "azure",
#     "docker",
#     "sql",
#     "ci/cd",
#     "git",
#     "kubernetes",
#     "api",
#     "microservices",
#     "javascript",
#     "typescript",
#     "html",
#     "reaat",
#     "angular",
#     "nodejs",
#     "express",
#     "nextjs",
#     "gen ai",
#     "agentic ai",
#     "ai",
#     "java",
#     ".net",
#     "springboot",
#     "sql",
#     "mongodb",
#     "postgresql"

def score_section_completeness(sections: dict):
    score = 0
    reasons = []
    for section in REQUIRED_SECTIONS:
        if section in sections and sections[section].strip():
            score += 5
        else:
            reasons.append(
                f"Missing required section: {section}"
            )
    
    for section in OPTIONAL_SECTIONS:
        if section in sections and sections[section].strip():
            score += 2.5
    
    return ATSCategoryScore(
        category = "Section Completeness",
        score=score,
        max_score=25,
        reason=(
            "All required sections present"
            if not reasons
            else ", ".join(reasons)
        )
    )
    
def score_keyword_optimization(sections: dict):
    combined_text = " ".join(sections.values()).lower()
    matched_keywords = []
    for keyword in ATS_KEYWORDS:
        if keyword in combined_text:
            matched_keywords.append(keyword)
            score = (len(matched_keywords) / len(ATS_KEYWORDS) * 25)
    missing_keywords = [
        kw for kw in ATS_KEYWORDS if kw not in matched_keywords
    ]
    return ATSCategoryScore(
        category="Keyword Optimization",
        score=round(score, 2),
        max_score=25,
        reason=(
            f"Matched keywords: {', '.join(matched_keywords)}. "
            f"Missing: {', '.join(missing_keywords)}"
        )
    )
    
def score_readability(sections: dict):
    combined_text = " ".join(sections.values())
    avg_sentence_len = (
        len(combined_text.split()) / max(len(re.findall(r"[.!?]", combined_text)), 1)
    )
    if avg_sentence_len <= 20:
        score = 15
        reason = "Sentence readability is ATS friendly"
    elif avg_sentence_len <= 30:
        score = 10
        reason = "Moderate readability"
    else:
        score = 5
        reason = "Sentences are too lengthy"
    
    return ATSCategoryScore(
        category="Readability",
        score=score,
        max_score=15,
        reason=reason
    )
    
def score_formatting(sections: dict):
    issues = []
    score = 20
    for section, content in sections.items():
        if len(content.split()) > 400:
            issues.append(
                f"{section} section is excessively long"
            )
            score -= 5
        if "|" in content:
            issues.append(
                f"{section} may contain table formatting"
            )
            score -= 5
    score = max(score, 0)
    return ATSCategoryScore(
        category="Formatting Compatibility",
        score=score,
        max_score=20,
        reason=(
            "ATS-compatible formatting detected"
            if not issues
            else ", ".join(issues)
        )
    )
    
def score_skills_clarity(sections: dict):
    skills = sections.get("skills", "")
    if not skills:
        return ATSCategoryScore(
            category="Skills Clarity",
            score=0,
            max_score=15,
            reason="Skills section missing"
        )  
    skills_count = len(
        [s.strip() for s in skills.split(",")]
    )
    if skills_count >= 10:
        score = 15
    elif skills_count >= 5:
        score = 10
    else:
        score = 5
    
    return ATSCategoryScore(
        category="Skills Clarity",
        score=score,
        max_score=15,
        reason=(
            f"Detected {skills_count} skills"
        )
    )
    
def generate_ats_report(sections: dict):
    breakdown = [
        score_section_completeness(sections),
        score_keyword_optimization(sections),
        score_readability(sections),
        score_formatting(sections),
        score_skills_clarity(sections)
    ]
    
    total_score = sum(
        item.score for item in breakdown
    )
    issues = []
    recommendations = []
    for item in breakdown:
        if item.score < (item.max_score * 0.6):
            issues.append(
                f"Weakness in {item.category}"
            )
            recommendations.append(
                item.reason
            )
    return ATSReport(
        total_score=round(total_score, 2),
        breakdown=breakdown,
        issues=issues,
        recommendations=recommendations
    )
    
    