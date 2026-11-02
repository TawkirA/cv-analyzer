TO RUN ANY FILE FROM A FOLDER RUN THE COMMAND AS BELOW.
python -m src.<folder_name>.<file_name>
Example - python -m src.agents.test_analyzer
Do not specify file extension


## REST API (FastAPI)

Run from the repo root (so `data/vectorstore` resolves):

    uvicorn src.api.main:app --reload

Swagger UI: http://127.0.0.1:8000/docs

| Method | Path | Input | Output |
|---|---|---|---|
| GET | /api/v1/health | - | `{"status": "ok"}` |
| GET | /api/v1/providers | - | supported providers and models |
| POST | /api/v1/analyze | form-data: `cv` (File: pdf/docx), `provider`, `model_name`, `api_key` (optional, falls back to `.env`), `project_id` (watsonx only) | JSON report |
| POST | /api/v1/report/pdf | JSON body = the `/analyze` response (optional `filename`, `model_used`) | `application/pdf` |

Postman: POST `/api/v1/analyze` -> Body -> form-data; set `cv` key type to *File*, others as *Text*.
For the PDF, POST the JSON from `/analyze` as raw JSON to `/api/v1/report/pdf` and use *Send and Download*.
