from langgraph.graph import StateGraph
from langgraph.graph import END
from src.graph.state import GraphState
from src.graph.nodes import (
    ats_analysis_node,
    build_query_node,
    retrieve_context_node,
    llm_analysis_node,
    report_merger_node,
    analyze_cv_node
)

def build_workflow():
    workflow = StateGraph(GraphState)
    workflow.add_node("ats_analysis", ats_analysis_node)
    workflow.add_node("build_query", build_query_node)
    workflow.add_node("retrieve_context", retrieve_context_node)
    workflow.add_node("llm_analysis", llm_analysis_node)
    workflow.add_node("merge_reports", report_merger_node)
    workflow.add_node("analyze_cv", analyze_cv_node)
    
    # workflow.set_entry_point("build_query")
    workflow.set_entry_point("ats_analysis")
    workflow.add_edge("ats_analysis", "build_query")
    workflow.add_edge("build_query", "retrieve_context")
    workflow.add_edge("retrieve_context", "llm_analysis")
    workflow.add_edge("llm_analysis", "merge_reports")
    workflow.add_edge("merge_reports", END)
    # workflow.add_edge("analyze_cv", END)
    
    return workflow.compile()
    
