import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.graph.workflow import build_workflow
from src.rag.retriever import warm_up_vectordb


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Same startup pattern as the Streamlit app: pre-load the vector DB in the
    # background and build the LangGraph workflow once.
    threading.Thread(target=warm_up_vectordb, daemon=True).start()
    app.state.workflow = build_workflow()
    yield


app = FastAPI(
    title="CV Analyzer API",
    version="1.0.0",
    description="Upload a CV (PDF/DOCX) and receive an ATS + LLM analysis report as JSON.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(router, prefix="/api/v1")
