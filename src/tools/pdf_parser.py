import pymupdf

def extract_pdf_text(file_path: str) -> str:
    """Extract text from PDF preserving layout and reading order."""
    document = pymupdf.open(file_path)
    full_text = []
    for page in document:
        # get_text("blocks", sort=True) sorts blocks in reading order (top-down, left-to-right)
        blocks = page.get_text("blocks", sort=True)
        page_text = []
        for block in blocks:
            # block[4] contains the text content, block[6] is 0 for text blocks (1 for image)
            if len(block) > 6 and block[6] == 0:
                text = block[4].strip()
                if text:
                    page_text.append(text)
            elif len(block) > 4:
                text = block[4].strip()
                if text:
                    page_text.append(text)
        if page_text:
            full_text.append("\n".join(page_text))
    document.close()
    return "\n\n".join(full_text)