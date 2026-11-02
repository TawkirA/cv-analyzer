# Weight of the deterministic (rule-based) ATS score in the overall quality score.
ATS_WEIGHT = 0.6
# LLM scores are snapped to this step so small run-to-run differences vanish.
LLM_SCORE_STEP = 10


def compute_overall_score(ats_score, llm_report: dict) -> float:
    """
    Overall quality = weighted blend of the deterministic ATS score and the
    LLM's section scores (averaged, then snapped to bands). The LLM's own
    free-form `overall_score` is not used because it is not reproducible.
    """
    ats_score = float(ats_score or 0)
    section_scores = [
        float(s["score"])
        for s in (llm_report.get("section_analysis") or [])
        if isinstance(s, dict) and s.get("score") is not None
    ]
    if not section_scores:
        return round(ats_score, 1)
    llm_avg = sum(section_scores) / len(section_scores)
    llm_snapped = round(llm_avg / LLM_SCORE_STEP) * LLM_SCORE_STEP
    return round(ATS_WEIGHT * ats_score + (1 - ATS_WEIGHT) * llm_snapped, 1)


def merge_reports(ats_report: dict, llm_report: dict):
    final_report = {
        "overall_score": compute_overall_score(ats_report.get("total_score"), llm_report),
        "ats_score": ats_report.get("total_score"),
        "ats_breakdown": ats_report.get("breakdown"),
        "ats_issues": ats_report.get("issues"),
        "recommendations": ats_report.get("recommendations"),
        "strengths": llm_report.get("strengths"),
        "weaknesses": llm_report.get("weaknesses"),
        "missing_sections": llm_report.get("missing_sections"),
        "keyword_gaps": list(
            set(llm_report.get("keyword_gaps", []))
        ),
        "section_analysis": llm_report.get("section_analysis"),
        "final_recommendations": llm_report.get("final_recommendations")
    }
    return final_report