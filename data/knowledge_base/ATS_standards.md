# ATS Standards - Technical Requirements and Compliance
## Overview
This document defines technical standards and compliance requirements for Applicant Tracking Systems, ensuring resumes are properly parsed, indexed, and ranked.
## 1. ATS Market Overview
### Major ATS Platforms and Market Share
**Enterprise Systems (Large Companies):**
- **Workday** - 25% market share
- **Oracle Taleo** - 20% market share
- **SAP SuccessFactors** - 15% market share
- **iCIMS** - 12% market share
**Mid-Market Systems:**
- **Greenhouse** - 8% market share
- **Lever** - 6% market share
- **JazzHR** - 4% market share
- **BambooHR** - 3% market share
**Small Business Systems:**
- **Zoho Recruit** - 3% market share
- **Freshteam** - 2% market share
- **Breezy HR** - 2% market share
### System Capabilities by Platform
**Workday:**
- Strong AI/ML parsing
- Good PDF support
- Keyword matching algorithm
- Skills taxonomy integration
- Mobile-optimized
- Parsing accuracy: 85-90%
**Oracle Taleo:**
- Strict parsing rules
- Prefers .docx format
- Basic keyword matching
- Legacy system architecture
- Parsing accuracy: 70-80%
- Known for parsing issues with complex formatting
**Greenhouse:**
- Modern parsing engine
- Excellent PDF support
- Advanced keyword algorithms
- Developer-friendly
- Parsing accuracy: 88-92%
**SAP SuccessFactors:**
- Enterprise-grade parsing
- Multi-language support
- Complex rule engine
- Integration with SAP ecosystem
- Parsing accuracy: 80-85%
**Lever:**
- Modern, intuitive parsing
- Good format flexibility
- Candidate relationship focus
- Parsing accuracy: 85-90%
**iCIMS:**
- Reliable parsing
- Standard format support
- Configurable by employer
- Parsing accuracy: 82-87%
## 2. Technical Parsing Standards
### Document Structure Recognition
**Header Detection:**
Standard Headers Recognized:
Contact Information / Personal Details / Contact
Professional Summary / Summary / Profile / Objective
Work Experience / Professional Experience / Employment / Experience
Education / Academic Background / Academic Qualifications
Skills / Technical Skills / Core Competencies / Expertise
Certifications / Licenses / Professional Certifications
Projects / Key Projects / Notable Projects
Awards / Honors / Achievements / Recognition
Publications / Research / Papers
Languages / Language Proficiency
Volunteer / Community Service / Volunteer Experience
**Non-Standard Headers (May Not Parse):**
- "What I Do" instead of "Experience"
- "My Journey" instead of "Professional Summary"
- "Toolbox" instead of "Skills"
- "Wins" instead of "Achievements"
- "Learning" instead of "Education"
### Field Extraction Standards
**Name Extraction:**
- Must be at top of document
- Largest or bold text
- Separate from contact information
- Format: First Name + Last Name
- Middle names/initials acceptable
- Suffixes (Jr., Sr., III) recognized
**Email Extraction:**
- Must contain @ symbol
- Standard email format
- Clickable hyperlink acceptable
- Multiple emails: first one used
- Must be valid format (name@domain.com)
**Phone Number Extraction:**
Recognized Formats:
    (555) 123-4567
    555-123-4567
    555.123.4567
    +1 555 123 4567
    +1-555-123-4567
    1 (555) 123-4567
Not Recognized:
    5551234567 (no separators)
    Random number without context
    Phone numbers in middle of text
**Location Extraction:**
Recognized Formats:
City, State
City, ST
City, State ZIP
City, Country
Remote
City, ST (Willing to relocate)
Examples:
✓ San Francisco, CA
✓ New York, NY 10001
✓ London, United Kingdom
✓ Remote - US Based
✗ SF (too abbreviated)
✗ Bay Area (too vague)
**Date Extraction:**
Recognized Formats:
    January 2020 - Present
    Jan 2020 - Dec 2022
    01/2020 - 12/2022
    2020 - 2022
    2020 - Current
Not Recognized:
    "Two years ago"
    "Recently"
    "2020ish"
    Incomplete dates without context
### Content Parsing Rules
**Job Title Extraction:**
- First bold text in experience section
- Followed by company name
- May include "at [Company]" or "|" separator
- Seniority level recognized (Senior, Junior, Lead, etc.)
- Hyphenated titles accepted
**Company Name Extraction:**
- Typically after job title
- May be separated by |, -, or new line
- Legal suffixes recognized (Inc., LLC, Ltd.)
- Must be distinct from job title
- Location typically follows company name
**Skills Extraction:**
Recognition Methods:
    Dedicated Skills section
    Skills mentioned in experience bullets
    Technical proficiencies section
    Tools and technologies lists
    Certifications section
Extraction Rules:
    Comma-separated lists parsed
    Bullet points parsed
    Skills in parentheses extracted
    Skills in job descriptions weighted lower
    Skills section weighted highest
**Education Parsing:**
Required Elements:
    Degree type (BS, BA, MS, MBA, PhD, etc.)
    Major/Field of study
    Institution name
    Graduation date or expected date
Optional Elements:
    GPA
    Honors
    Location
    Relevant coursework
Degree Recognition:
    Associate's Degree / Associate of Arts (AA) / Associate of Science (AS)
    Bachelor's Degree / Bachelor of Arts (BA) / Bachelor of Science (BS)
    Master's Degree / Master of Arts (MA) / Master of Science (MS) / MBA
    Doctoral Degree / PhD / Doctorate
    Professional Degrees (JD, MD, DDS, etc.)
## 3. Keyword Matching Algorithms
### Exact Match vs. Fuzzy Match
**Exact Match (Strict):**
Job Requirement: "Project Management"
Resume Must Contain: "Project Management" (exact phrase)
Matches:
✓ "Project Management Professional"
✓ "Experience in Project Management"
✓ "Project Management certification"
Does Not Match:
✗ "Managed projects"
✗ "PM experience"
✗ "Project Manager" (different form)
**Fuzzy Match (Flexible):**
Job Requirement: "Project Management"
May Match:
    ✓ "Project Manager"
    ✓ "Managed projects"
    ✓ "PM" (if algorithm includes acronyms)
    ✓ "Programme Management" (UK spelling)
Confidence Scores:
    Exact match: 100%
    Close variant: 80-90%
    Related term: 60-70%
    Distant relation: 40-50%
### Keyword Weighting
**High Weight (Critical):**
- Required qualifications
- Technical skills (hard skills)
- Certifications and licenses
- Years of experience
- Education requirements
- Industry-specific terminology
**Medium Weight (Important):**
- Preferred qualifications
- Soft skills mentioned
- Specific tools/technologies
- Company types/industries
- Job titles
**Low Weight (Nice to Have):**
- General business terms
- Common action verbs
- Soft skills (generic)
- Industry buzzwords
### Synonym Recognition
**Standard Synonyms Recognized:**
Job Title Synonyms:
Software Engineer = Software Developer = Programmer
Sales Representative = Sales Rep = Account Executive
HR Manager = Human Resources Manager = People Manager
Project Manager = PM = Programme Manager
Skill Synonyms:
JavaScript = JS
Search Engine Optimization = SEO
Customer Relationship Management = CRM
Artificial Intelligence = AI = Machine Learning (partial)
Education Synonyms:
Bachelor's = BS = BA = Undergraduate Degree
Master's = MS = MA = Graduate Degree
MBA = Master of Business Administration
**System Limitations:**
- Not all synonyms recognized
- Context matters
- Acronyms must be defined first time
- Industry-specific terms may not have synonyms mapped
### Boolean Search Logic
**AND Logic (All Required):**
"Python AND Machine Learning AND AWS"
Resume must contain ALL three terms
Strictest matching
**OR Logic (Any Acceptable):**
"Python OR Java OR C++"
Resume must contain AT LEAST ONE term
More flexible matching
**NOT Logic (Exclusion):**
"Marketing NOT Intern"
Resume must contain Marketing but NOT Intern
Used to filter out unwanted results
**Complex Queries:**
"(Python OR Java) AND (AWS OR Azure) AND NOT Intern"
Resume must have:
Either Python or Java
Either AWS or Azure
Must not contain Intern
## 4. Scoring and Ranking Systems
### Standard Scoring Components
**Keyword Match Score (40-50% weight):**
Calculation:
Count matched keywords from job description
Weight by importance (required vs preferred)
Calculate percentage match
Example:
Job has 20 keywords (15 required, 5 preferred)
Resume matches 12 required, 3 preferred
Score: (12/15 × 0.7) + (3/5 × 0.3) = 74%
**Experience Match Score (25-30% weight):**
Factors:
    Years of experience vs requirement
    Relevant job titles
    Industry experience
    Company size/type match
    Career progression
Scoring:
    Exact match: 100%
    Close match (±1 year): 90%
    Somewhat relevant: 70%
    Tangentially related: 50%
    Not relevant: 0%
**Education Match Score (15-20% weight):**
Factors:
Degree level (matches requirement)
Field of study relevance
Institution prestige (some systems)
GPA (if specified in requirements)
Certifications
Scoring:
Exact degree + relevant field: 100%
Exact degree + related field: 85%
Higher degree: 90%
Lower degree: 50-70%
No degree (if required): 0%
**Skills Match Score (10-15% weight):**
Factors:
Technical skills match
Years of experience with each skill
Proficiency level (if indicated)
Number of required skills possessed
Scoring:
All required skills: 100%
Most required skills (80%+): 85%
Some required skills (50-79%): 60%
Few required skills (<50%): 30%
**Recency Score (5-10% weight):**
Factors:
How recent is experience
Employment gaps
Current employment status
Last updated date
Scoring:
Currently employed in relevant role: 100%
Recently employed (<6 months): 90%
Gap 6-12 months: 75%
Gap 1-2 years: 60%
Gap 2+ years: 40%
### Overall Score Calculation
**Weighted Average Method:**
Total Score =
(Keyword Match × 0.45) +
(Experience Match × 0.30) +
(Education Match × 0.15) +
(Skills Match × 0.10)
Example:
Keyword: 80% × 0.45 = 36
Experience: 90% × 0.30 = 27
Education: 100% × 0.15 = 15
Skills: 85% × 0.10 = 8.5
Total: 86.5% (Strong Match)
**Score Interpretation:**
90-100%: Excellent Match (Top 5%)
80-89%: Strong Match (Top 15%)
70-79%: Good Match (Top 30%)
60-69%: Moderate Match (Top 50%)
50-59%: Weak Match (Bottom 50%)
<50%: Poor Match (Likely Rejected)
### Ranking Factors
**Primary Ranking Factors:**
1. Overall match score
2. Required qualifications met
3. Years of relevant experience
4. Education level
5. Key skills present
**Secondary Ranking Factors:**
6. Career stability (low turnover)
7. Career progression (promotions)
8. Company reputation
9. Certifications
10. Location match
**Tiebreaker Factors:**
11. Application date (earlier = better)
12. Profile completeness
13. Custom screening questions
14. Referral status
15. Internal candidate status
## 5. Screening Question Standards
### Question Types
**Knockout Questions (Disqualifying):**
Examples:
"Do you have a valid driver's license?" (Required: Yes)
"Are you authorized to work in the US?" (Required: Yes)
"Do you have Bachelor's degree?" (Required: Yes)
"Do you have 5+ years of experience?" (Required: Yes)
Impact:
Wrong answer = Automatic rejection
No manual review
Cannot proceed in process
**Scoring Questions (Weighted):**
Examples:
"How many years of Python experience?" (0-10+ years)
"What is your proficiency with Excel?" (Basic/Intermediate/Advanced)
"How many years of management experience?" (0-20+ years)
Impact:
Adds to overall score
Higher/better answer = higher score
Considered with other factors
**Preference Questions (Informational):**
Examples:
"What is your salary expectation?"
"When can you start?"
"Are you willing to relocate?"
"What is your preferred work arrangement?"
Impact:
Used for filtering/sorting
Not typically disqualifying
Helps recruiter prioritize
### Answer Validation
**Expected Answer Formats:**
Yes/No Questions:
Boolean (True/False)
Radio buttons (Yes/No)
Must select one
Numeric Questions:
Number input
Dropdown with ranges
Validation for reasonable numbers
Text Questions:
Short answer (50-200 characters)
Long answer (500-1000 characters)
Free form text
Multiple Choice:
Single select
Multi-select
Dropdown menu
**Common Validation Rules:**
Years of Experience:
Must be numeric
Must be ≥ 0
Must be ≤ 50 (reasonable maximum)
Decimal acceptable (2.5 years)
Salary:
Must be numeric
Must be > 0
Must be < 1,000,000 (typical cap)
Currency format accepted
Dates:
Must be valid date format
Start date < End date
Not in future (for past experience)
Reasonable range (not 100 years ago)
## 6. Data Extraction Standards
### Contact Information Fields
**Standard Database Fields:**
Personal Information:
First Name (required)
Middle Name (optional)
Last Name (required)
Suffix (optional)
Preferred Name (optional)
Contact Details:
Email Address (required)
Phone Number (required)
Phone Type (Mobile/Home/Work)
Secondary Phone (optional)
Address Line 1 (optional)
Address Line 2 (optional)
City (recommended)
State/Province (recommended)
Postal Code (optional)
Country (required for international)
Online Presence:
LinkedIn URL (recommended)
Portfolio Website (optional)
GitHub Profile (optional for tech)
Other Professional Links (optional)
### Experience Data Fields
**Per Job Entry:**
Required Fields:
Job Title
Company Name
Start Date (Month/Year minimum)
End Date or "Present"
Location (City, State minimum)
Optional Fields:
Employment Type (Full-time, Part-time, Contract, Internship)
Company Industry
Company Size
Reporting Structure
Team Size Managed
Job Description/Responsibilities
Key Achievements
Technologies/Tools Used
Projects
**Data Normalization:**
Job Titles:
Standardized to common variants
Seniority levels extracted (Junior, Senior, Lead, etc.)
Mapped to job family categories
Company Names:
Matched against company database
Legal entities normalized (Inc., LLC removed)
Subsidiaries linked to parent company
Industry classification applied
Dates:
Converted to standard format (YYYY-MM)
Duration calculated automatically
Gaps identified and flagged
Overlap detection
### Education Data Fields
**Per Education Entry:**
Required Fields:
Degree Type (Associate, Bachelor's, Master's, Doctorate)
Major/Field of Study
Institution Name
Graduation Date (or Expected Date)
Optional Fields:
Minor/Concentration
GPA
Honors/Awards
Relevant Coursework
Thesis/Dissertation Title
Activities/Organizations
Location
Accreditation Status
**Degree Standardization:**
Common Variations Normalized:
BS/B.S./Bachelor of Science → Bachelor's Degree
MBA/M.B.A. → Master of Business Administration
PhD/Ph.D./Doctorate → Doctoral Degree
AA/A.A. → Associate Degree
Field of Study Mapping:
Computer Science → Technology/Engineering
Marketing → Business/Marketing
Biology → Science/Healthcare
English → Liberal Arts/Humanities
### Skills Data Fields
**Skills Extraction:**
Skill Categories:
Technical Skills (Hard Skills)
Software/Tools
Programming Languages
Methodologies/Frameworks
Certifications
Soft Skills
Language Proficiency
Per Skill Entry:
Skill Name (standardized)
Proficiency Level (if indicated)
Years of Experience (if calculable)
Last Used Date
Context (where mentioned)
Frequency (how many times mentioned)
**Skills Taxonomy:**
Standardization Examples:
"Javascript" → "JavaScript"
"MS Office" → "Microsoft Office"
"Photoshop" → "Adobe Photoshop"
"AWS" → "Amazon Web Services (AWS)"
Categorization:
JavaScript → Programming Languages → Technology
Leadership → Soft Skills → Management
PMP → Certifications → Project Management
Spanish → Languages → Communication
## 7. Compliance and Legal Standards
### EEOC Compliance
**Protected Information (Must NOT Influence Scoring):**
- Race/Ethnicity
- Gender/Sex
- Age/Date of Birth
- Religion
- National Origin
- Disability Status
- Marital Status
- Pregnancy Status
- Genetic Information
- Military/Veteran Status (with exceptions)
**ATS Requirements:**
Must:
Exclude protected information from scoring algorithms
Provide equal opportunity to all candidates
Avoid discriminatory keyword filtering
Document selection criteria
Allow for reasonable accommodations
Must Not:
Filter by age-related terms ("recent graduate," "digital native")
Require unnecessary physical characteristics
Discriminate based on name ethnicity
Penalize employment gaps without context
Use biased language in job descriptions
### GDPR Compliance (EU)
**Data Protection Requirements:**
Candidate Rights:
Right to access their data
Right to rectification
Right to erasure ("right to be forgotten")
Right to data portability
Right to object to processing
Right to withdraw consent
ATS Obligations:
Obtain explicit consent for data storage
Specify data retention period
Allow data export in standard format
Enable data deletion on request
Provide privacy policy
Secure data storage and transmission
Limit data access to authorized personnel
**Retention Policies:**
Standard Retention:
Active candidates: Duration of hiring process
Rejected candidates: 6-12 months (with consent)
Hired candidates: Duration of employment + legal requirement
EU candidates: Explicit consent required beyond 6 months
Deletion Requirements:
Automatic deletion after retention period
Manual deletion on candidate request
Secure deletion methods
Confirmation of deletion provided
### CCPA Compliance (California)
**California Consumer Privacy Act Requirements:**
Candidate Rights:
Right to know what data is collected
Right to know if data is sold/shared
Right to opt-out of data sale
Right to deletion
Right to non-discrimination
ATS Requirements:
Provide privacy notice
Disclose data collection practices
Allow opt-out mechanisms
Process deletion requests within 45 days
Verify identity before data disclosure
### Accessibility Standards (ADA)
**WCAG 2.1 Compliance:**
Level AA Requirements:
Keyboard navigation support
Screen reader compatibility
Sufficient color contrast (4.5:1 minimum)
Text resizing up to 200%
Clear form labels
Error identification and suggestions
Consistent navigation
Descriptive link text
Application Process:
Alternative format acceptance (not just online)
Reasonable accommodation requests
Accessible document formats
Compatible with assistive technologies
No time limits (or generous extensions)
## 8. Integration Standards
### API Standards
**Data Exchange Formats:**
Accepted Formats:
JSON (most common)
XML
CSV (for bulk imports)
Plain text
Standard API Endpoints:
POST /candidates (submit application)
GET /candidates/{id} (retrieve candidate)
PUT /candidates/{id} (update candidate)
DELETE /candidates/{id} (remove candidate)
GET /jobs (list open positions)
GET /jobs/{id} (job details)

### Webhook and Event Standards
**Standard Webhook Events:**
- candidate.applied — New application submitted
- candidate.reviewed — Recruiter has viewed application
- candidate.advanced — Candidate moved to next stage
- candidate.rejected — Application declined
- candidate.hired — Candidate accepted offer
- job.opened — New job requisition posted
- job.closed — Position filled or cancelled

**Webhook Payload Format (JSON):**
    {
      "event": "candidate.applied",
      "timestamp": "2024-01-15T10:30:00Z",
      "candidate_id": "12345",
      "job_id": "67890",
      "data": { ... }
    }

### Authentication Standards
**Supported Methods:**
- OAuth 2.0 (recommended for enterprise integrations)
- API Key (header-based: X-API-Key)
- Bearer Token (Authorization: Bearer <token>)
- Basic Auth (legacy systems only — not recommended)

**Security Requirements:**
- All API calls must use HTTPS (TLS 1.2+)
- API keys must be rotated every 90 days
- Rate limiting: 1,000 requests/hour (standard tier)
- IP allowlisting available for enterprise accounts
- All tokens expire after 24 hours of inactivity

### Error Handling Standards
**HTTP Status Codes:**
- 200 OK — Request successful
- 201 Created — Resource created (new application submitted)
- 400 Bad Request — Invalid request format or missing required fields
- 401 Unauthorized — Invalid or expired credentials
- 403 Forbidden — Insufficient permissions
- 404 Not Found — Candidate or job not found
- 422 Unprocessable Entity — Valid format but failed business validation
- 429 Too Many Requests — Rate limit exceeded
- 500 Internal Server Error — Server-side parsing failure

**Standard Error Response Body:**
    {
      "error": {
        "code": "PARSE_ERROR",
        "message": "Unable to extract contact information from submitted document",
        "field": "contact.email",
        "suggestion": "Ensure email address is in standard format (name@domain.com)"
      }
    }

**Retry Strategy:**
- Retry on 429 and 5xx errors with exponential backoff
- Initial retry delay: 1 second
- Maximum retries: 3
- Maximum backoff: 30 seconds
- Do not retry on 4xx errors (client errors)

## 9. ATS Testing and Validation Standards
### Resume Parsing Validation
**Accuracy Benchmarks (Minimum Acceptable):**
- Contact information extraction: 95%+
- Job title extraction: 90%+
- Company name extraction: 90%+
- Date extraction: 88%+
- Education extraction: 85%+
- Skills extraction: 80%+

**Test Cases Required:**
- Standard chronological resume (.docx)
- Standard chronological resume (PDF)
- Functional/skills-based resume
- Resume with career gaps
- Recent graduate resume (education-first)
- Executive resume (2+ pages)
- International resume (non-US address format)
- Resume with only partial dates (year only)

### Keyword Matching Validation
**Test Protocol:**
1. Create a baseline job description with 20 known keywords
2. Submit resume with 15/20 keywords in various placements
3. Verify system reports 70-80% keyword match
4. Submit resume with 0/20 keywords
5. Verify system reports <10% keyword match
6. Test synonym recognition: submit "JS" for "JavaScript" — verify matching

**Expected Match Accuracy:**
- Exact keyword match detection: 99%+
- Synonym/acronym resolution: 70%+
- Fuzzy match (minor variations): 80%+
- False positive rate: <5%

### Scoring System Validation
**Validation Criteria:**
- Identical resumes must produce identical scores (deterministic)
- Score must not change based on candidate name, age, or gender
- Score recalculation on profile update must reflect changes within 60 seconds
- Score must be explainable — each component traceable to resume content

### Regression Testing
**Mandatory Test Suite:**
- Run after every parsing engine update
- Minimum 500 anonymized real-world resumes in test corpus
- Score variance after update must be < 2% for unchanged resumes
- Any parsing regression must block deployment
- Monthly accuracy reporting against manual-review ground truth

## 10. ATS Implementation Summary
### Critical Requirements Checklist
**Parsing:**
- [ ] Supports .docx, PDF (text-based), .txt input formats
- [ ] Extracts all 6 standard contact fields
- [ ] Parses multiple work experience entries correctly
- [ ] Handles present/current end dates
- [ ] Extracts education with degree normalization
- [ ] Skills taxonomy applied to extracted skills
- [ ] Handles functional and chronological formats

**Scoring:**
- [ ] Keyword match score calculated (40-50% weight)
- [ ] Experience match score calculated (25-30% weight)
- [ ] Education match score calculated (15-20% weight)
- [ ] Skills match score calculated (10-15% weight)
- [ ] Overall weighted score produced (0-100%)
- [ ] Score interpretation thresholds configured

**Compliance:**
- [ ] EEOC-protected fields excluded from scoring
- [ ] GDPR consent and deletion mechanisms in place (EU)
- [ ] CCPA privacy notice and opt-out available (California)
- [ ] WCAG 2.1 Level AA accessibility verified
- [ ] Data retention policy configured and enforced
- [ ] Audit log maintained for all scoring decisions

**Integration:**
- [ ] REST API endpoints available and documented
- [ ] Webhook events firing for all candidate status changes
- [ ] OAuth 2.0 or API key authentication active
- [ ] HTTPS enforced on all endpoints
- [ ] Rate limiting configured
- [ ] Error responses follow standard schema

### Top 10 ATS Compatibility Rules for Resume Submissions
1. Use .docx or text-based PDF — avoid scanned images
2. Place contact information at the top in simple linear format
3. Use standard section headers recognized by all major platforms
4. Avoid tables, columns, text boxes, and graphics
5. Use standard fonts (Arial, Calibri, Times New Roman)
6. Include both full terms and acronyms for key skills
7. Use consistent date format throughout the document
8. Match job description language as closely as possible
9. Keep formatting simple — prioritize parsability over design
10. Test with a plain-text extraction before submitting

---
*End of ATS Standards Document*
*Version: 1.0*
*Last Updated: 2024*
