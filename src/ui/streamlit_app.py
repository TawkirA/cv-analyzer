import streamlit as st
import tempfile
import os
import threading
from src.tools.pdf_parser import extract_pdf_text
from src.tools.docx_parser import extract_docx_text
from src.tools.cleaner import clean_text
from src.services.cv_section_extractor import extract_sections
from src.services.pdf_report_generator import generate_pdf_report
from src.services.llm_factory import (
    PROVIDER_MODELS,
    get_default_api_key,
    validate_llm_config
)
from src.graph.workflow import build_workflow
from src.graph.state import GraphState
from src.rag.retriever import warm_up_vectordb

st.set_page_config(
    page_title="CV Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional styling & button theme overrides
st.markdown("""
<style>
    /* Extra room below the report so the last content isn't clipped */
    .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-bottom: 6rem !important;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #6c757d;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .strength-item {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 0.7rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .weakness-item {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 0.7rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .keyword-pill {
        display: inline-block;
        background-color: #f1f5f9;
        border: 1px solid #cbd5e1;
        color: #334155;
        padding: 0.25rem 0.65rem;
        border-radius: 20px;
        font-size: 0.88rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    .action-step {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.8rem 1.1rem;
        margin-bottom: 0.6rem;
    }

    /* Primary Analyze Button Styling (Modern Royal Blue / Indigo instead of Red) */
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.2rem !important;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.35) !important;
        transform: translateY(-1px);
    }

    /* PDF Download Button Styling (Teal / Emerald Gradient) */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.2rem !important;
        box-shadow: 0 2px 4px rgba(5, 150, 105, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
        box-shadow: 0 4px 10px rgba(5, 150, 105, 0.35) !important;
        transform: translateY(-1px);
    }

    /* Secondary / Reset Button Styling */
    div.stButton > button[kind="secondary"],
    div.stButton > button[data-testid="baseButton-secondary"] {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out !important;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="main-title">📄 CV Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Intelligent resume diagnostics, ATS scoring, and actionable career feedback</div>', unsafe_allow_html=True)

# Initialize Session State
if "sections" not in st.session_state:
    st.session_state.sections = None
if "report" not in st.session_state:
    st.session_state.report = None
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None
if "used_model" not in st.session_state:
    st.session_state.used_model = None
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "last_seen_file" not in st.session_state:
    st.session_state.last_seen_file = None

def reset_all_state():
    """Completely resets parsed sections, generated report, and uploaded file widget."""
    st.session_state.sections = None
    st.session_state.report = None
    st.session_state.uploaded_filename = None
    st.session_state.used_model = None
    st.session_state.last_seen_file = None
    st.session_state.uploader_key = st.session_state.get("uploader_key", 0) + 1

@st.cache_resource
def get_workflow():
    # Pre-load the embedding model / vector store in the background so the UI
    # renders immediately and the first analysis doesn't pay the full load cost.
    threading.Thread(target=warm_up_vectordb, daemon=True).start()
    return build_workflow()

workflow = get_workflow()

# Sidebar for Model Configuration, API Key & Document Upload
with st.sidebar:
    st.header("🤖 Model Configuration")
    
    selected_provider = st.selectbox(
        "AI Provider",
        options=list(PROVIDER_MODELS.keys()),
        index=0,
        help="Select the AI provider for analysis"
    )
    
    provider_info = PROVIDER_MODELS[selected_provider]
    model_options = provider_info["models"] + ["Custom Model..."]
    
    selected_model_option = st.selectbox(
        "Model",
        options=model_options,
        index=0,
        help=f"Select an {selected_provider} model or provide custom model name"
    )
    
    if selected_model_option == "Custom Model...":
        selected_model = st.text_input(
            "Custom Model Name",
            value=provider_info["default"],
            help="Enter exact model identifier"
        )
    else:
        selected_model = selected_model_option
        
    env_key = get_default_api_key(selected_provider)
    has_env_key = bool(env_key)
    
    api_key_input = st.text_input(
        f"{provider_info['key_label']}",
        type="password",
        placeholder=provider_info["key_placeholder"],
        help=f"Enter your {selected_provider} API key" + (" (Found key in environment)" if has_env_key else "")
    )
    
    if has_env_key and not api_key_input:
        st.caption("🔒 *API key auto-detected from environment*")
    elif not has_env_key and not api_key_input:
        st.caption("⚠️ *API key required to run analysis*")
        
    project_id_input = ""
    watsonx_url_input = "https://us-south.ml.cloud.ibm.com"
    if selected_provider == "IBM watsonx":
        env_proj = os.getenv("WATSONX_PROJECT_ID", "")
        project_id_input = st.text_input(
            "Watsonx Project ID",
            value=env_proj,
            placeholder="e.g. 1a2b3c4d-...",
            help="Watsonx.ai Project ID"
        )
        watsonx_url_input = st.text_input(
            "Watsonx API URL",
            value=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
            help="IBM Cloud region endpoint URL"
        )
        
    llm_config = {
        "provider": selected_provider,
        "model_name": selected_model,
        "api_key": api_key_input.strip() if api_key_input else env_key,
        "project_id": project_id_input.strip() if project_id_input else os.getenv("WATSONX_PROJECT_ID", ""),
        "watsonx_url": watsonx_url_input.strip()
    }
    
    st.divider()
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a CV file",
        type=["pdf", "docx"],
        key=f"file_uploader_{st.session_state.uploader_key}",
        help="Upload your PDF or DOCX format resume for instant evaluation"
    )
    
    if uploaded_file:
        # Detect a newly dropped file and immediately clear stale sections so the
        # old CV data doesn't linger on screen while the user hasn't processed yet.
        if uploaded_file.name != st.session_state.last_seen_file:
            with st.spinner("⏳ Uploading CV..."):
                st.session_state.last_seen_file = uploaded_file.name
                st.session_state.sections = None
                st.session_state.report = None
                uploaded_file.getvalue()  # fully read the uploaded bytes

        st.caption(f"**Filename:** `{uploaded_file.name}`")
        st.info("📋 File ready — click **Process Document** to extract sections.", icon=None)

        if st.button("Process Document", use_container_width=True, type="secondary"):
            suffix = uploaded_file.name.split(".")[-1]
            with st.spinner("⏳ Loading CV..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_path = temp_file.name

            try:
                with st.spinner("⏳ Extracting & parsing resume sections..."):
                    if suffix == "pdf":
                        raw_text = extract_pdf_text(temp_path)
                    else:
                        raw_text = extract_docx_text(temp_path)

                    cleaned_text = clean_text(raw_text)
                    st.session_state.sections = extract_sections(cleaned_text)
                    st.session_state.report = None
                    st.session_state.uploaded_filename = uploaded_file.name
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            st.rerun()
                    
    if st.session_state.sections or st.session_state.report:
        st.divider()
        if st.button("🔄 Reset / Start New", use_container_width=True, type="secondary", help="Clear document, parsed sections, and generated analysis"):
            reset_all_state()
            st.rerun()

if st.session_state.sections:
    # Public sections only — strip internal sentinel keys (prefixed with _)
    public_sections = {
        k: v for k, v in st.session_state.sections.items()
        if not k.startswith("_")
    }

    # Extracted Sections Preview
    with st.expander("📑 View Extracted Resume Sections", expanded=False):
        section_cols = st.columns(min(len(public_sections), 4))
        for idx, (sec_name, sec_content) in enumerate(public_sections.items()):
            col = section_cols[idx % len(section_cols)]
            with col:
                st.caption(f"**{sec_name.upper()}** ({len(sec_content)} chars)")
        st.divider()
        selected_preview = st.selectbox(
            "Inspect raw section content:",
            options=list(public_sections.keys()),
            format_func=lambda s: s.upper()
        )
        st.text_area(
            "Content",
            public_sections[selected_preview],
            height=150,
            disabled=True,
            label_visibility="collapsed"
        )
    
    # Analysis Trigger (if report not yet generated)
    if not st.session_state.report:
        col_btn, col_info = st.columns([1.3, 2.7])
        with col_btn:
            if st.button("🚀 Run Comprehensive Analysis", type="primary", use_container_width=True):
                is_valid, err_msg = validate_llm_config(llm_config)
                if not is_valid:
                    st.error(f"❌ {err_msg}")
                else:
                    try:
                        with st.spinner(f"Analyzing resume using {selected_provider} ({selected_model})..."):
                            initial_state: GraphState = {
                                "cv_sections": st.session_state.sections,
                                "llm_config": llm_config
                            }
                            result = workflow.invoke(initial_state)
                            st.session_state.report = result["final_report"]
                            st.session_state.used_model = f"{selected_provider} - {selected_model}"
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ Analysis failed with {selected_provider}: {str(e)}")
        with col_info:
            st.caption(f"Selected: **{selected_provider}** (`{selected_model}`)")

# Render Report if Available
if st.session_state.report:
    report = st.session_state.report
    safe_fname = st.session_state.get("uploaded_filename") or "Resume"
    base_name = safe_fname.rsplit(".", 1)[0]
    used_model = st.session_state.get("used_model") or f"{selected_provider} - {selected_model}"
    
    st.divider()
    
    # Top Action Bar: Title & Model badge, Download PDF button, Reset Report button
    head_col, dl_col, reset_col = st.columns([2, 1.2, 0.8])
    with head_col:
        st.subheader("📊 Analysis Results & Diagnostics")
        st.caption(f"Evaluated with **{used_model}**")
    with dl_col:
        pdf_bytes = generate_pdf_report(report, candidate_filename=safe_fname, model_name=used_model)
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"CV_Analysis_Report_{base_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
            help="Download complete diagnostic report as a formatted PDF"
        )
    with reset_col:
        if st.button("🔄 Reset Report", use_container_width=True, help="Clear report and extracted resume data"):
            reset_all_state()
            st.rerun()
    
    # Executive Score Dashboard (Top Cards)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(
            label="Overall Score",
            value=f"{report.get('overall_score', 0)} / 100",
            delta="Overall Quality"
        )
    with c2:
        st.metric(
            label="ATS Compatibility",
            value=f"{report.get('ats_score', 0)} / 100",
            delta="Parser Match"
        )
    with c3:
        strengths_count = len(report.get("strengths", []))
        st.metric(
            label="Key Strengths",
            value=f"{strengths_count} Identified"
        )
    with c4:
        issues_count = len(report.get("ats_issues", [])) + len(report.get("weaknesses", []))
        st.metric(
            label="Areas for Improvement",
            value=f"{issues_count} Areas"
        )

    st.write("") # Spacing

    # Organize Report Sections in Tabs
    tab_summary, tab_ats, tab_sections, tab_action_plan = st.tabs([
        "📋 Executive Summary",
        "⚙️ ATS Diagnostics & Rubrics",
        "🔍 Section-by-Section Review",
        "🎯 Strategic Action Plan"
    ])
    
    # --- TAB 1: EXECUTIVE SUMMARY ---
    with tab_summary:
        st.markdown("#### Strengths & Improvement Opportunities")
        col_str, col_weak = st.columns(2)
        
        with col_str:
            st.markdown("##### ✅ Core Strengths")
            if report.get("strengths"):
                for item in report["strengths"]:
                    st.markdown(f'<div class="strength-item">✓ {item}</div>', unsafe_allow_html=True)
            else:
                st.info("No standout strengths detected.")
                
        with col_weak:
            st.markdown("##### ⚠️ Key Weaknesses")
            if report.get("weaknesses"):
                for item in report["weaknesses"]:
                    st.markdown(f'<div class="weakness-item">! {item}</div>', unsafe_allow_html=True)
            else:
                st.success("No critical weaknesses found.")
                
        st.divider()
        
        # Missing Sections & Keyword Gaps in 2 Columns
        col_miss, col_keys = st.columns(2)
        with col_miss:
            st.markdown("##### 📌 Section Completeness Check")
            if report.get("missing_sections"):
                for item in report["missing_sections"]:
                    st.error(f"Missing Section: **{item}**")
            else:
                st.success("✅ All core resume sections are present!")
                
        with col_keys:
            st.markdown("##### 🔑 Keyword Gaps")
            if report.get("keyword_gaps"):
                st.write("Consider incorporating these relevant target keywords:")
                pills_html = " ".join([f'<span class="keyword-pill">{kw}</span>' for kw in report["keyword_gaps"]])
                st.markdown(pills_html, unsafe_allow_html=True)
            else:
                st.success("✅ Strong keyword coverage across key domains!")

    # --- TAB 2: ATS DIAGNOSTICS & RUBRICS ---
    with tab_ats:
        st.markdown("#### Automated ATS Engine Rubric Breakdown")
        
        # Progress and cards for each ATS category
        if report.get("ats_breakdown"):
            for item in report["ats_breakdown"]:
                cat_score = item.get("score", 0)
                cat_max = item.get("max_score", 100)
                pct = int((cat_score / cat_max) * 100) if cat_max > 0 else 0
                
                with st.container():
                    st.markdown(f"**{item['category']}** — `{cat_score} / {cat_max} pts` ({pct}%)")
                    st.progress(pct / 100.0)
                    st.caption(f"**Notes:** {item.get('reason', '')}")
                    st.write("")
        
        st.divider()
        col_ats_iss, col_ats_rec = st.columns(2)
        
        with col_ats_iss:
            st.markdown("##### ⚠️ ATS Parsing & Formatting Issues")
            if report.get("ats_issues"):
                for issue in report["ats_issues"]:
                    st.warning(issue)
            else:
                st.success("✅ No critical ATS formatting issues detected.")
                
        with col_ats_rec:
            st.markdown("##### 💡 ATS Optimization Recommendations")
            if report.get("recommendations"):
                for rec in report["recommendations"]:
                    st.info(f"• {rec}")
            else:
                st.write("No additional ATS recommendations needed.")

    # --- TAB 3: SECTION-BY-SECTION REVIEW ---
    with tab_sections:
        st.markdown("#### Detailed Section Analysis")
        section_analyses = report.get("section_analysis", [])
        
        if section_analyses:
            for sec in section_analyses:
                sec_name = sec.get("section_name", "Section")
                sec_score = sec.get("score", "N/A")
                
                with st.expander(f"📌 {sec_name.upper()} — Score: {sec_score}/100", expanded=False):
                    f_col, s_col = st.columns(2)
                    with f_col:
                        st.markdown("##### 🔍 Findings & Observations")
                        findings = sec.get("findings", [])
                        if findings:
                            for f in findings:
                                st.markdown(f"- {f}")
                        else:
                            st.write("No specific findings reported.")
                            
                    with s_col:
                        st.markdown("##### 💡 Targeted Suggestions")
                        suggestions = sec.get("suggestions", [])
                        if suggestions:
                            for s in suggestions:
                                st.markdown(f"- {s}")
                        else:
                            st.write("No suggestions for this section.")
        else:
            st.info("No detailed section-by-section analysis data available.")

    # --- TAB 4: STRATEGIC ACTION PLAN ---
    with tab_action_plan:
        st.markdown("#### Prioritized Final Recommendations")
        final_recs = report.get("final_recommendations", [])
        
        if final_recs:
            for idx, rec in enumerate(final_recs, 1):
                st.markdown(
                    f'<div class="action-step">'
                    f'<strong>Step {idx}:</strong> {rec}'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.success("Resume is fully optimized! No immediate changes required.")

    # Bottom Actions Bar
    st.divider()
    bot_col1, bot_col2, _ = st.columns([1.5, 1, 2])
    with bot_col1:
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=f"CV_Analysis_Report_{base_name}.pdf",
            mime="application/pdf",
            key="download_pdf_bottom",
            use_container_width=True
        )
    with bot_col2:
        if st.button("🔄 Reset Report", key="reset_report_bottom", use_container_width=True, help="Clear report and extracted resume data"):
            reset_all_state()
            st.rerun()
    st.markdown('<div style="height: 4rem;"></div>', unsafe_allow_html=True)
else:
    if not uploaded_file:
        st.info("👈 Upload a resume (PDF or DOCX) in the sidebar to begin analysis.")
