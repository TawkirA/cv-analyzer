import os
import tempfile
from typing import Any, Dict

from src.tools.pdf_parser import extract_pdf_text
from src.tools.docx_parser import extract_docx_text
from src.tools.cleaner import clean_text
from src.services.cv_section_extractor import extract_sections

SUPPORTED_EXTENSIONS = ("pdf", "docx")


class InvalidCVError(ValueError):
    """Raised when the uploaded CV is unsupported, empty or unreadable."""


def get_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def parse_cv_bytes(filename: str, content: bytes) -> Dict[str, str]:
    """Same steps as the Streamlit 'Process Document' button:
    temp file -> extract text -> clean -> split into sections."""
    ext = get_extension(filename)
    if ext not in SUPPORTED_EXTENSIONS:
        raise InvalidCVError("Unsupported file type. Please upload a PDF or DOCX file.")
    if not content:
        raise InvalidCVError("Uploaded file is empty.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as temp_file:
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        try:
            raw_text = extract_pdf_text(temp_path) if ext == "pdf" else extract_docx_text(temp_path)
        except Exception as e:
            raise InvalidCVError(f"Could not read the uploaded file: {e}") from e
        cleaned_text = clean_text(raw_text)
        if not cleaned_text.strip():
            raise InvalidCVError("No text could be extracted from the uploaded file.")
        return extract_sections(cleaned_text)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def public_sections(sections: Dict[str, Any]) -> Dict[str, str]:
    """Strip internal sentinel keys (prefixed with _), as the Streamlit UI does."""
    return {k: v for k, v in sections.items() if not k.startswith("_")}
