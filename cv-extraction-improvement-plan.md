# Plan: CV Extraction Pipeline Improvement

## Top-Level Overview
Enhance the CV parsing and section extraction pipeline to reliably handle diverse resume formats, messy layouts, inline headers (e.g., `SKILLS: ...`), trailing punctuation/markdown styling, and multi-column PDF layouts without dropping text into `unknown`.

---

## Sub-Tasks

### Sub-Task 1: Expand Section Patterns and Normalization in Section Extractor
- **Intent**: Enable `cv_section_extractor.py` to recognize a wider range of section header variations, handle trailing colons/dashes, markdown symbols (`#`, `**`), and inline headers.
- **Expected Outcomes**:
  - `OBJECTIVE: ...`, `WORK EXPERIENCE:`, `SKILLS:`, `## Education`, etc. are correctly identified.
  - Inline headers have their header mapped to the section and the trailing inline text appended as content.
  - Typo in existing code (`dducational qualifications`) fixed.
- **Relevant Context**:
  - `src/services/cv_section_extractor.py`
  - `tests/cvs/messy_resumet.txt`
- **Status**: [ ] pending

---

### Sub-Task 2: Upgrade PDF Parser to Layout-Aware Block Extraction
- **Intent**: Prevent multi-column and sidebar text interleaving during PDF text extraction.
- **Expected Outcomes**:
  - `extract_pdf_text` uses PyMuPDF block extraction sorted geometrically (top-to-bottom, left-to-right columns).
  - Clean column separation for two-column resumes.
- **Relevant Context**:
  - `src/tools/pdf_parser.py`
  - `src/tools/cv_parser_tool.py`
- **Status**: [ ] pending

---

### Sub-Task 3: Add Unit Tests & Validation for Section Extraction
- **Intent**: Verify that section extraction works accurately across all test resumes (`messy_resumet.txt`, `senior_resume.txt`, `fresher_resume.txt`, `weak_resume.txt`, `strong_resume.txt`, `junior_resume.txt`).
- **Expected Outcomes**:
  - A test script runs across all sample CVs in `tests/cvs/`.
  - Core sections (`summary`/`objective`, `experience`, `education`, `skills`) are successfully identified with minimal or no orphaned `unknown` content.
- **Relevant Context**:
  - `tests/cvs/`
  - `src/services/test_ats_engine.py`
  - `src/graph/test-workflow.py`
- **Status**: [ ] pending
