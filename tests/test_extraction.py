import os
import sys
from pathlib import Path

# Ensure workspace root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.tools.cleaner import clean_text
from src.services.cv_section_extractor import extract_sections

def run_tests():
    cv_dir = Path("tests/cvs")
    test_files = list(cv_dir.glob("*.txt"))
    
    print(f"Found {len(test_files)} test files to validate:\n")
    
    for file_path in test_files:
        print(f"--- Testing: {file_path.name} ---")
        raw_text = file_path.read_text(encoding="utf-8")
        cleaned = clean_text(raw_text)
        sections = extract_sections(cleaned)
        
        print(f"Extracted {len(sections)} sections:")
        for sec_name, content in sections.items():
            first_line = content.split('\n')[0][:50]
            print(f"  - [{sec_name}]: ({len(content)} chars) -> {first_line}...")
        print()
        
        # Verify core sections are extracted
        has_summary_or_exp = "summary" in sections or "experience" in sections
        assert has_summary_or_exp, f"Failed to extract summary/experience from {file_path.name}"
        assert "unknown" not in sections, f"Found 'unknown' section in {file_path.name}"

if __name__ == "__main__":
    run_tests()
    print("All extraction tests passed successfully!")
