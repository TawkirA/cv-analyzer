from src.services.retrieval_query_builder import (build_search_query)
from src.rag.retriever import retrieve_context
from src.agents.analyzer_agent import analyze_cv
from src.services.ats_engine import generate_ats_report
from src.services.report_merger import merge_reports

def ats_analysis_node(state):
    ats_report = generate_ats_report(state["cv_sections"])
    state["ats_report"] = ats_report.model_dump()
    return state

def build_query_node(state):
    query = build_search_query(state["cv_sections"])
    state["retrieval_query"] = query
    return state

def retrieve_context_node(state):
    context = retrieve_context(state["retrieval_query"])
    state["rag_context"] = context
    return state

def llm_analysis_node(state):
    report = analyze_cv(
        cv_sections=state["cv_sections"],
        rag_context=state["rag_context"],
        llm_config=state.get("llm_config")
    )
    state["llm_analysis"] = report.model_dump()
    return state

def report_merger_node(state):
    final_report = merge_reports(
        ats_report = state["ats_report"],
        llm_report = state["llm_analysis"]
    )
    state["final_report"] = final_report
    return state

def analyze_cv_node(state):
    report = analyze_cv(
        cv_sections=state["cv_sections"],
        rag_context=state["rag_context"],
        llm_config=state.get("llm_config")
    )
    state["analysis_report"] = report.model_dump()
    return state