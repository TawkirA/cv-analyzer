from langchain.tools import tool
from typing import Optional, Type
from pydantic import BaseModel, Field
import pymupdf
import docx

class CVParseInput(BaseModel):
    """Input for CV Parser tool"""
    file_path: str = Field(description="Path to the CV file (PDF or DOCX)")
    
class CVParserTool(BaseModel):
    name: str = "cv_parser"
    description: str = """
    Useful for parsing CV files and extracting structured information.
    Input should be the file path to a CV (PDF or DOCX format).
    Returns structured data including: name, contact, summary, experience, 
    education, skills, certifications, and formatting details.
    """
    args_schema: Type[BaseModel] = CVParseInput
    
    def _run(self, file_path: str) -> dict:
        """Parse CV and extract structured data."""
        try:
            if file_path.endswith('.pdf'):
                return self._parse_pdf(file_path)
            elif file_path.endswith('.docx'):
                return self._parse_docx(file_path)
            else:
                return {"error": "Unsupported file format"}
        except Exception as e:
            return {"error": str(e)}
        
    def _parse_pdf(self, file_path: str) -> dict:
        """Extract text and structure from PDF."""
        doc = pymupdf.open(file_path)
        
        # Extract text with formatting
        full_text = ""
        formatting_info = {
            "fonts": set(),
            "font_sizes": set(),
            "colors": set(),
            "page_count": len(doc)
        }
        
        for page in doc:
            text = page.get_text()
            full_text += text + "\n"
            # Extract formatting details
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            formatting_info["fonts"].add(span["font"])
                            formatting_info["font_sizes"].add(span["size"])
        
        return {
            "raw_text": full_text,
            "formatting": {
                "fonts": list(formatting_info["fonts"]),
                "font_sizes": list(formatting_info["font_sizes"]),
                "page_count": formatting_info["page_count"]
            },
            "file_type": "pdf"
        }
        
    def _parse_docx(self, file_path: str) -> dict:
        """Extract text and structure from DOCX."""
        doc = docx.Document(file_path)
        paragraph = [p.text for p in doc.paragraphs if p.text.strip()]
        return {
            "raw_text": "\n".join(paragraphs),
            "formatting": {
                "sections": len(doc.sections),
                "paragraphs": len(paragraphs)
            },
            "file_type": "docx"
        }       
        
    def _arun(self, file_path: str) -> dict:
        """Async version."""
        return self._run(file_path)
    