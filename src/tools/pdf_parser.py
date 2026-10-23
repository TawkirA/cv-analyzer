import pymupdf

def extract_pdf_text(file_path: str) -> str:
    document = pymupdf.open(file_path)
    full_text = []
    for page in document:
        text = page.get_text()
        full_text.append(text)
    document.close()
    return "\n".join(full_text)