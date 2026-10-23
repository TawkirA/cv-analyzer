import re

def clean_text(text: str) -> str:
    # 1. Standardise all vertical spaces (newlines) down to a single newline
    text = re.sub(r"\n+", "\n", text)
    # 2. Standardise other consecutive spaces (tabs, inline spaces) down to a single space
    text = re.sub(r"[ \t]+", " ", text)
    # 3. Strip any leading/trailing spaces or newlines
    return text.strip()