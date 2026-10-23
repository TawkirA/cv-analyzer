import streamlit as st
import tempfile
import os
from src.tools.pdf_parser import extract_pdf_text
from src.tools.docx_parser import extract_docx_text
from src.tools.cleaner import clean_text
from src.services.cv_section_extractor import extract_sections
from src.graph.workflow import build_workflow

st.set_page_config(
    page_title="CV Analyzer",
    layout="wide"
)

st.title("CV Analyzer")
workflow = build_workflow()

uploaded_file = st.file_uploader(
    "Upload CV",
    type=["pdf", "docx"]
)

if uploaded_file:
    suffix = uploaded_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{suffix}"
    ) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name
        
    try:
        with st.spinner("Processing CV content..."):
            if suffix == "pdf":
                raw_text = extract_pdf_text(temp_path)
            else:
                raw_text = extract_docx_text(temp_path)
            
            cleaned_text = clean_text(raw_text)
            sections = extract_sections(cleaned_text)
            print(sections)
        st.success("CV processed successfully!")
        st.divider()
        st.subheader("Extracted Sections")
        for section, content in sections.items():
            with st.expander(section.upper()):
                st.write(content[:3000])
        st.divider()
        if st.button("Analyze CV"):
            with st.spinner("Running CV analysis...."):
                initial_state = {
                    "cv_sections": sections
                }
                result = workflow.invoke(initial_state)
                # FOR DEBUGGING
                # st.write(type(result))
                # st.write(result)
                # st.write(type(result["analysis_report"]))
                # st.write(result["analysis"])
                # FOR DEBUGGING END
                
                report = result["final_report"]
                
                # FOR DEBUGGING
                # st.json(report)
                # st.write(report.keys())  
                # FOR DEBUGGING END  
                
            st.success("Analysis completed...")
            st.divider()
            # print('*'*80)
            # print("RERPOT")
            # st.json(report)
            # print('*'*80)
            st.header("Overall Assessment")
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Overall Score",
                    report["overall_score"]
                )
            with col2:
                st.metric(
                    "ATS Score",
                    report["ats_score"]
                )
            st.divider()
            st.header("ATS Score Breakdown")
            for item in report["ats_breakdown"]:
                with st.expander(item["category"]):
                    st.metric(
                        "Score", f"{item['score']} / {item['max_score']}"
                    )
                    st.write(item["reason"])
            st.divider()
            st.header("ATS Issues")
            for item in report["ats_issues"]:
                st.warning(item)
            st.header("ATS Recommendations")
            for item in report["recommendations"]:
                st.write(f"- {item}")
            st.divider()
            st.header("Strengths")
            for item in report["strengths"]:
                st.success(item)
            st.header("Weaknesses")
            for item in report["weaknesses"]:
                st.warning(item)
            st.divider()
            st.header("Missing Sections")
            if report["missing_sections"]:
                for item in report["missing_sections"]:
                    st.error(item)
            else:
                st.success("No major sections missing")
            if report["keyword_gaps"]:
                st.header("Keyword Gaps")
                for item in report["keyword_gaps"]:
                    st.write(f"- {item}")
            st.divider()
            st.header("Section Analysis")
            for section in report["section_analysis"]:
                with st.expander(
                    f"{section['section_name']} Analysis"
                ):
                    st.write(
                        f"Score: {section['score']}"
                    )
                    st.markdown("### Findings")
                    for finding in section["findings"]:
                        st.write(f"- {finding}")
                    st.markdown("### Suggestions")
                    for suggestion in section["suggestions"]:
                        st.write(f"- {suggestion}")
            st.divider()
            st.header("Final Recommendations")
            for item in report["final_recommendations"]:
                st.write(f"- {item}")
    finally:
        # Since delete=False was used, we manually clean up the file here
        if os.path.exists(temp_path):
            os.unlink(temp_path)