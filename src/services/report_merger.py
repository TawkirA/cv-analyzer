def merge_reports(ats_report: dict, llm_report: dict):
    final_report = {
        "overall_score": llm_report.get("overall_score"),
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