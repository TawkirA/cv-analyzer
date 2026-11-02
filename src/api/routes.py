import logging
import os
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, Request, Response, UploadFile

from src.api.schemas import (
    AnalyzeResponse,
    PdfRequest,
    ProviderInfo,
    ProvidersResponse,
)
from src.api.services import InvalidCVError, parse_cv_bytes, public_sections
from src.graph.state import GraphState
from src.services.llm_factory import PROVIDER_MODELS, validate_llm_config
from src.services.pdf_report_generator import generate_pdf_report

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/providers", response_model=ProvidersResponse)
def providers():
    return ProvidersResponse(
        providers=[
            ProviderInfo(
                provider=name,
                models=cfg["models"],
                default_model=cfg["default"],
                requires_project_id=(name == "IBM watsonx"),
            )
            for name, cfg in PROVIDER_MODELS.items()
        ]
    )


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(
    request: Request,
    cv: UploadFile = File(..., description="CV file (.pdf or .docx)"),
    provider: str = Form("Google Gemini"),
    model_name: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None, description="Falls back to the server .env key when omitted"),
    project_id: Optional[str] = Form(None, description="IBM watsonx only; falls back to WATSONX_PROJECT_ID"),
):
    filename = cv.filename or "Resume"

    try:
        sections = parse_cv_bytes(filename, cv.file.read())
    except InvalidCVError as e:
        raise HTTPException(status_code=400, detail=str(e))

    model_name = (model_name or "").strip() or PROVIDER_MODELS.get(provider, {}).get("default", "")
    llm_config = {
        "provider": provider,
        "model_name": model_name,
        "api_key": (api_key or "").strip(),
        "project_id": (project_id or "").strip() or os.getenv("WATSONX_PROJECT_ID", ""),
    }

    is_valid, err_msg = validate_llm_config(llm_config)
    if not is_valid:
        raise HTTPException(status_code=422, detail=err_msg)

    try:
        initial_state: GraphState = {"cv_sections": sections, "llm_config": llm_config}
        result = request.app.state.workflow.invoke(initial_state)
    except Exception as e:
        logger.exception("Analysis failed")
        raise HTTPException(status_code=502, detail=f"Analysis failed with {provider}: {e}")

    report = {k: v for k, v in result["final_report"].items() if v is not None}
    return AnalyzeResponse(
        **report,
        filename=filename,
        model_used=f"{provider} - {model_name}",
        sections=public_sections(sections),
    )


@router.post("/report/pdf")
def report_pdf(body: PdfRequest):
    report = body.model_dump(exclude={"filename", "model_used"})
    filename = body.filename or "Resume"
    base_name = filename.rsplit(".", 1)[0]

    try:
        pdf_bytes = generate_pdf_report(report, candidate_filename=filename, model_name=body.model_used)
    except Exception as e:
        logger.exception("PDF generation failed")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="CV_Analysis_Report_{base_name}.pdf"'},
    )
