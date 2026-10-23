# Job Description Analysis - Parsing and Extraction Guide
## Overview
This document defines how to parse, analyze, and extract structured information from job descriptions (JDs) to enable accurate resume-to-job matching, keyword gap analysis, and tailoring recommendations in the CV analyzer/optimizer application.

## 1. Job Description Structure
### Standard JD Sections
Most job descriptions follow a predictable structure:
1. **Job Title** — The role being advertised
2. **Company Overview** — Brief company background (1-3 sentences)
3. **Role Summary / About the Role** — High-level description of the position
4. **Responsibilities / What You'll Do** — Day-to-day duties and ownership areas
5. **Requirements / Qualifications** — Required and preferred candidate attributes
6. **Skills / Technologies** — Specific tools, languages, or platforms required
7. **Education** — Degree and field requirements
8. **Benefits / Compensation** — Salary range, perks (not used for matching)
9. **Location / Work Arrangement** — On-site, remote, hybrid; city/country

### Sections That Drive Resume Matching
Focus extraction efforts on:
- Responsibilities section (reveals required competencies)
- Requirements/Qualifications section (hard requirements and preferences)
- Skills/Technologies section (explicit technical keywords)
- Job title (reveals seniority level and function)

## 2. Keyword Extraction
### Extraction Priority Tiers
**Tier 1 — Critical (Must Match):**
- Keywords that appear in "Required" or "Must Have" language
- Keywords repeated 3+ times across the JD
- Job title keywords
- Certifications explicitly listed as required

**Tier 2 — Important (Should Match):**
- Keywords in "Preferred," "Nice to Have," or "Bonus" language
- Technical tools or platforms mentioned once
- Soft skills mentioned with specific context
- Industry-specific terminology used in responsibilities

**Tier 3 — Contextual (Good to Match):**
- Company values and cultural keywords
- General business terms
- Generic soft skills (communication, teamwork)
- Keywords from the company overview section

### Keyword Categories to Extract
**Technical Skills:**
- Programming languages (Python, Java, SQL, JavaScript)
- Frameworks and libraries (React, Django, Spring Boot)
- Platforms and tools (AWS, Salesforce, SAP, Tableau)
- Methodologies (Agile, Scrum, Six Sigma, ITIL)

**Domain Skills:**
- Industry-specific competencies (HIPAA compliance, GAAP, SEO, PPC)
- Functional expertise (financial modeling, product roadmaps, clinical trials)
- Processes and practices (A/B testing, code review, budget management)

**Soft Skills:**
- Leadership indicators (managed, led, mentored, directed)
- Communication indicators (presented, negotiated, collaborated)
- Analytical indicators (analyzed, evaluated, identified, researched)

**Experience Signals:**
- Years of experience requirements ("5+ years," "minimum 3 years")
- Seniority indicators (Senior, Lead, Principal, Director, Manager)
- Industry background requirements ("experience in healthcare," "B2B SaaS background")

**Education Requirements:**
- Minimum degree level (Bachelor's, Master's, PhD)
- Preferred fields of study (Computer Science, Finance, Engineering)
- Certification requirements (PMP, CPA, AWS Certified)

## 3. Requirement Classification
### Required vs. Preferred Language Patterns
**Signals of Required Qualifications:**
- "Must have," "Required," "Essential," "Minimum qualifications"
- "You must," "Candidates must," "Applicants should have"
- Listed under "Requirements" or "Qualifications" heading
- "X+ years of experience in..." (explicitly stated minimum)
- Degree requirements: "Bachelor's degree required"

**Signals of Preferred Qualifications:**
- "Preferred," "Nice to have," "Bonus," "Plus," "Ideal"
- "Experience with X is a plus"
- "Familiarity with," "Exposure to"
- Listed under "Preferred Qualifications" or "What Would Be Great"
- "X+ years experience preferred"

**Signals of Disqualifying Criteria:**
- "Must be authorized to work in..." (legal requirement)
- "Must have active security clearance"
- "Must be able to lift X pounds" (physical requirement)
- "Must be available for X% travel"

### Classification Decision Tree
1. Does the JD label it "required"? → Tier 1
2. Does it appear 3+ times in the JD? → Tier 1
3. Does the JD label it "preferred"? → Tier 2
4. Is it in the responsibilities section? → Tier 2
5. Is it mentioned once in company overview? → Tier 3

## 4. Seniority Level Extraction
### Title-Based Seniority Mapping
| JD Title Signal | Seniority Level | Expected Experience |
|---|---|---|
| Intern, Student | Entry/Intern | 0-1 years |
| Associate, Junior, Entry-Level | Junior | 0-2 years |
| (No prefix), Analyst, Specialist | Mid-Junior | 1-3 years |
| Senior, Sr. | Senior | 5-8 years |
| Lead, Staff | Lead | 7-10 years |
| Principal, Architect | Principal | 10-15 years |
| Manager, Director | Manager/Director | 5-12 years |
| Vice President, VP | VP | 10-15 years |
| C-Suite (CEO, CTO, CPO) | Executive | 15+ years |

### Experience Requirement Extraction Rules
- Extract numeric experience requirements: "5+ years" → min: 5, no max
- Extract range requirements: "3-5 years" → min: 3, max: 5
- "Recent graduate" or "0-1 years" → min: 0, max: 1
- "Minimum 3 years" → min: 3
- When no years stated, infer from seniority title mapping above

## 5. Skills Gap Analysis
### Gap Analysis Process
1. **Extract all skills from the CV** (technical skills, tools, certifications)
2. **Extract all required skills from the JD** (Tier 1 keywords)
3. **Extract all preferred skills from the JD** (Tier 2 keywords)
4. **Compare CV skills to JD skills** using exact match + synonym resolution
5. **Classify each JD skill** as: Present / Partially Present / Missing
6. **Calculate match scores** per category

### Match Classification Rules
**Present:** Skill appears explicitly in CV (skills section, experience bullets, certifications)
**Partially Present:** Related term or synonym found but not exact match (e.g., JD requires "React"; CV has "ReactJS")
**Missing:** No mention of skill or close synonym anywhere in CV

### Gap Severity Classification
**Critical Gap:** Required (Tier 1) skill is missing entirely
**Significant Gap:** Required skill only partially present
**Minor Gap:** Preferred (Tier 2) skill is missing
**No Gap:** All required skills present; preferred skills mostly present

## 6. Industry and Role Classification
### Industry Detection Keywords
**Technology:**
Software, SaaS, Cloud, API, DevOps, Machine Learning, AI, Cybersecurity, Mobile, Platform

**Finance:**
Banking, Financial Services, Investment, Trading, Compliance, Risk, Audit, Accounting, Tax

**Healthcare:**
Clinical, Patient, Hospital, Medical, Pharmaceutical, HIPAA, EHR, Nursing, Physician, Healthcare

**Marketing:**
Brand, Campaign, Digital Marketing, SEO, PPC, Social Media, Content, PR, Advertising, Growth

**Sales:**
Revenue, Quota, Pipeline, CRM, Account Management, B2B, B2C, Outbound, Inbound, Sales

**Operations:**
Supply Chain, Logistics, Manufacturing, Process Improvement, Lean, Six Sigma, Operations

**Education:**
Curriculum, Teaching, Academic, Instruction, Learning, Students, Higher Education

### Function Classification
**Engineering/Technical:** Engineer, Developer, Architect, DevOps, Data Scientist, Analyst (technical)
**Business/Strategy:** Analyst, Consultant, Manager, Director, Strategist, Operations
**Creative/Design:** Designer, UX, UI, Creative Director, Art Director, Writer, Editor
**People/HR:** Recruiter, HR, Talent, People Operations, Learning & Development
**Finance/Accounting:** Accountant, Controller, Analyst (finance), CFO, Treasurer
**Sales/Marketing:** Account Executive, Sales Manager, Marketing Manager, Growth, Demand Gen

## 7. Compensation and Location Extraction
### Salary Range Extraction
- Extract stated ranges: "$80,000 - $120,000" → min: 80000, max: 120000
- Extract single figures: "Up to $150K" → max: 150000
- Normalize to annual: hourly × 2080 = annual equivalent
- Note currency when non-USD
- Flag "competitive salary" / "market rate" as unspecified

### Work Arrangement Classification
- **On-site / In-office:** "In-person," "on-site required," "must be in [city]"
- **Remote:** "Fully remote," "work from anywhere," "100% remote"
- **Hybrid:** "2 days in office," "hybrid," "flexible work arrangement"
- **Travel Required:** Extract percentage if stated ("25% travel required")

### Location Extraction
- Extract primary city and country/state
- Note multiple locations if listed ("New York or San Francisco")
- Flag "Willing to relocate required"
- Flag "US-based only" or regional restrictions

## 8. JD Quality Assessment
### Red Flags in Job Descriptions
**Vague or Unrealistic Requirements:**
- Require 10+ years experience in a technology less than 10 years old
- Request 5 skills in vastly different domains (likely poorly defined role)
- "Rockstar," "ninja," "wizard" — often signals cultural red flags
- Salary listed far below market rate for stated requirements

**Discriminatory Language Flags:**
- Age-related terms: "digital native," "recent graduate" as hard requirement
- Gendered language: "salesman," "chairman" (non-inclusive)
- Physical requirement without operational justification
- Overly specific cultural fit language

**Signs of a Well-Written JD:**
- Clear separation of required vs. preferred qualifications
- Specific, measurable responsibilities
- Realistic experience range for the seniority level
- Named tools and technologies
- Salary or range disclosed

## 9. Structured Output Format
### Parsed JD Data Structure
After analysis, the extracted JD data should be structured as:

    {
      "job_title": "Senior Data Engineer",
      "seniority_level": "Senior",
      "industry": "Technology",
      "function": "Engineering/Technical",
      "work_arrangement": "Hybrid",
      "location": "New York, NY",
      "experience_required": { "min": 5, "max": null },
      "education_required": { "degree": "Bachelor's", "field": "Computer Science or related" },
      "salary_range": { "min": 130000, "max": 180000, "currency": "USD" },
      "keywords": {
        "tier1_required": ["Python", "SQL", "Apache Spark", "AWS", "ETL pipelines", "dbt"],
        "tier2_preferred": ["Kafka", "Airflow", "Snowflake", "Terraform"],
        "tier3_contextual": ["communication", "collaboration", "data-driven"]
      },
      "certifications_required": [],
      "certifications_preferred": ["AWS Certified Data Engineer"],
      "soft_skills": ["problem-solving", "cross-functional collaboration", "mentoring"]
    }

## 10. JD Analysis Checklist
### Pre-Analysis Validation
- [ ] JD is complete (has title, responsibilities, and requirements sections)
- [ ] JD is for a real, active role (not a template or generic posting)
- [ ] Language is in English (or translation applied if multilingual support enabled)
- [ ] JD is recent (posted within last 90 days preferred for accurate keyword matching)

### Extraction Completeness Checklist
- [ ] Job title extracted and seniority level mapped
- [ ] Industry and function classified
- [ ] All Tier 1 required keywords extracted
- [ ] All Tier 2 preferred keywords extracted
- [ ] Experience minimum extracted or inferred
- [ ] Education requirement extracted
- [ ] Work arrangement classified (remote/hybrid/on-site)
- [ ] Location extracted
- [ ] Salary range extracted (if present)
- [ ] Required certifications identified

### Gap Analysis Readiness
- [ ] JD keyword list complete before resume comparison begins
- [ ] Synonyms and acronyms expanded (JS → JavaScript, etc.)
- [ ] Tier weighting applied before scoring
- [ ] Structured JD object ready for comparison against parsed CV

---
*End of Job Description Analysis Document*
*Version: 1.0*
*Last Updated: 2024*
