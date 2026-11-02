# Expose CV Analyzer as a REST API (FastAPI) – Plan

## Top-Level Overview

**Goal:** Expose the existing CV analysis pipeline (currently only reachable through the Streamlit UI) as an HTTP API so that (a) it can be tested from Postman and (b) an independent UI can integrate with it later.

**Approach:**
- Add a new, self-contained FastAPI layer under `src/api/` (currently empty). `fastapi` is already in [`requirements.txt`](requirements.txt:12) but unused.
- **No change to existing working code** (Streamlit app, graph, services, agents, tools, schemas). The API only *imports and calls* existing functions.
- The API reproduces the same flow the Streamlit app performs in [`src/ui/streamlit_app.py`](src/ui/streamlit_app.py:250):
  `upload -> temp file -> extract_pdf_text/extract_docx_text -> clean_text -> extract_sections -> validate_llm_config -> build_workflow().invoke(...) -> final_report`.
- `final_report` returned by the workflow is already a plain dict (nodes call `model_dump()` and `merge_reports` builds a dict). The **dict -> JSON response conversion lives only in the API code** (Pydantic response models in `src/api/`), as requested.

**Endpoints (v1):**
| Method | Path | Input | Output |
|---|---|---|---|
| POST | `/api/v1/analyze` | `multipart/form-data`: `cv` (file, pdf/docx), `provider`, `model_name`, `api_key` | JSON with all report details |
| POST | `/api/v1/report/pdf` | JSON report (the body returned by `/analyze`) + optional filename/model label | `application/pdf` bytes |
| GET | `/api/v1/health` | – | simple status (useful for Postman / UI connectivity check) |
| GET | `/api/v1/providers` | – | supported providers and default models (from `PROVIDER_MODELS`), helps the future UI populate dropdowns |

**Input rules for `/analyze`:**
- `cv` – uploaded file (`.pdf` / `.docx` only), loaded via FastAPI `UploadFile` (Postman: form-data, type *File*).
- `provider` – one of `PROVIDER_MODELS` keys in [`src/services/llm_factory.py`](src/services/llm_factory.py:10) (Google Gemini, OpenAI, Anthropic, IBM watsonx).
- `model_name` – model identifier (falls back to provider default if omitted, matching `get_structured_llm`).
- `api_key` – if omitted/blank, falls back to server `.env` key via `get_default_api_key` (existing behavior of `validate_llm_config`).
- Validation reuses `validate_llm_config` – no new validation logic.

**Response of `/analyze` (JSON):** every key of `final_report` from [`merge_reports`](src/services/report_merger.py:1): `overall_score`, `ats_score`, `ats_breakdown[]`, `ats_issues[]`, `recommendations[]`, `strengths[]`, `weaknesses[]`, `missing_sections[]`, `keyword_gaps[]`, `section_analysis[]`, `final_recommendations[]`; plus API-added metadata: `filename`, `model_used` (`"<provider> - <model>"`, same label Streamlit uses), and the extracted public `sections` (keys not starting with `_`, as Streamlit does).

**Error mapping:** 400 unsupported/empty file or unparsable CV; 422 invalid LLM config (message from `validate_llm_config`); 502/500 for LLM/workflow failure with a JSON `detail` message (Streamlit shows `str(e)` – same here).

**Design notes (from code research):**
- `workflow.invoke` is blocking -> endpoints are plain `def` so FastAPI runs them in a threadpool.
- Workflow (`build_workflow()`) should be built once at startup, and `warm_up_vectordb` started in a background thread (same as Streamlit, lines 154-155). Use FastAPI lifespan.
- Project convention: no `__init__.py` files anywhere (namespace packages); run with `python -m ...`. Run API via `uvicorn src.api.main:app` from repo root (so `data/vectorstore` relative path in `CHROMA_PATH` resolves).
- Streamlit script cannot be imported without side effects, so upload/parse glue is re-implemented (small) in the API layer rather than refactoring existing code.
- Add CORS middleware so a browser-based independent UI can call the API.
- Temp file for the upload must be deleted in `finally` (same as Streamlit).

```
src/api/
  main.py            # FastAPI app, lifespan, CORS, router include
  routes.py          # endpoints
  schemas.py         # API-only Pydantic response/request models (dict -> JSON conversion)
  services.py        # upload->sections helper, thin wrapper around workflow + PDF
```

---

## Sub-Tasks

### 1. API scaffolding and dependencies
**Intent:** Create the FastAPI application skeleton without touching existing code.

**Expected Outcomes:**
- `uvicorn src.api.main:app --reload` starts; `GET /api/v1/health` returns 200; Swagger UI at `/docs` loads.
- Workflow built once at startup; vector DB warm-up runs in background.

**Todo List:**
1. Add `uvicorn` and `python-multipart` (required for `UploadFile`/`Form`) to [`requirements.txt`](requirements.txt).
2. Create `src/api/main.py` with app, lifespan (build workflow, start `warm_up_vectordb` thread), CORS, router include under `/api/v1`.
3. Add `/health` endpoint.
4. Add README run instructions (short section).

**Relevant Context:** [`src/graph/workflow.py`](src/graph/workflow.py) `build_workflow`; [`src/rag/retriever.py`](src/rag/retriever.py) `warm_up_vectordb`; Streamlit lines 150-155 for the cached-workflow/warm-up pattern.

**Status:** [x] done

---

### 2. API schemas (dict -> JSON conversion layer)
**Intent:** Keep all response shaping in the API layer; existing code unchanged.

**Expected Outcomes:**
- Pydantic models in `src/api/schemas.py` describing the analyze response (report fields + `filename`, `model_used`, `sections`) and the PDF request body.
- Swagger shows the full response structure.

**Todo List:**
1. Define response model mirroring `merge_reports` keys (reuse nested shapes of `ATSCategoryScore` / `SectionAnalysis` from [`src/schemas`](src/schemas/report_schema.py) by importing them, not modifying them).
2. Define metadata fields (`filename`, `model_used`, `sections`).
3. Define PDF request model (report + optional `filename`, `model_used`).
4. Make fields tolerant of `None` (merge_reports can emit `None` via `.get`).

**Relevant Context:** [`src/services/report_merger.py`](src/services/report_merger.py), [`src/schemas/ats_schema.py`](src/schemas/ats_schema.py), [`src/schemas/report_schema.py`](src/schemas/report_schema.py).

**Status:** [x] done

---

### 3. `POST /api/v1/analyze`
**Intent:** One-shot CV upload + LLM config -> full JSON report.

**Expected Outcomes:**
- In Postman: form-data with `cv` (File), `provider`, `model_name`, `api_key` returns the JSON report.
- Omitting `api_key` uses `.env` key; invalid config returns 422 with the `validate_llm_config` message; bad file type returns 400.

**Todo List:**
1. Implement helper: validate extension -> write temp file -> `extract_pdf_text` / `extract_docx_text` -> `clean_text` -> `extract_sections`; always delete temp file.
2. Build `llm_config` dict (`provider`, `model_name`, `api_key`) and call `validate_llm_config`.
3. Invoke workflow with `GraphState` (`cv_sections`, `llm_config`) and read `final_report`.
4. Map to response model; add `filename`, `model_used`, public `sections`.
5. Error handling per mapping above.

**Relevant Context:** Streamlit lines 237-271 (parse) and 311-327 (analyze); [`src/tools/pdf_parser.py`](src/tools/pdf_parser.py), [`src/tools/docx_parser.py`](src/tools/docx_parser.py), [`src/tools/cleaner.py`](src/tools/cleaner.py), [`src/services/cv_section_extractor.py`](src/services/cv_section_extractor.py), [`src/services/llm_factory.py`](src/services/llm_factory.py) `validate_llm_config`, [`src/graph/state.py`](src/graph/state.py).

**Status:** [x] done

---

### 4. `POST /api/v1/report/pdf` and `GET /api/v1/providers`
**Intent:** Let the UI/Postman download the PDF for an analysis result and discover supported providers/models.

**Expected Outcomes:**
- Posting the JSON returned by `/analyze` returns `application/pdf` with `Content-Disposition: attachment; filename=CV_Analysis_Report_<name>.pdf`; Postman "Send and Download" yields a valid PDF.
- `/providers` returns provider -> default/available models.

**Todo List:**
1. Convert request model back to a dict and call `generate_pdf_report(report, candidate_filename=..., model_name=...)` unchanged.
2. Return bytes via `Response(media_type="application/pdf")`.
3. Implement `/providers` from `PROVIDER_MODELS` (read-only; never expose env keys).

**Relevant Context:** [`src/services/pdf_report_generator.py`](src/services/pdf_report_generator.py:66) `generate_pdf_report`; Streamlit lines 346-354 for filename convention.

**Status:** [x] done

---

### 5. Verification and Postman usage docs
**Intent:** Prove the API works end-to-end and document how to call it.

**Expected Outcomes:**
- Manual run against a sample CV in `tests/cvs/` (note: those are `.txt`; use a real PDF/DOCX for the test) returns full JSON.
- README section with run command, endpoint table, and Postman setup (form-data keys); optional exported Postman collection.
- Existing Streamlit app still runs unchanged (git diff shows no edits to existing files except `requirements.txt` and README).

**Todo List:**
1. Start server, test `/health`, `/docs`, `/analyze` (valid, missing key, bad extension, corrupt file), `/report/pdf`.
2. Optionally add a lightweight API test (FastAPI `TestClient`, workflow mocked) under `tests/`.
3. Write README API section.

**Relevant Context:** [`README.md`](README.md); [`tests/`](tests/).

**Status:** [x] done
