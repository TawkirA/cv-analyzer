# Scoring Rubrics - CV Analyzer Evaluation Criteria
## Overview
This document defines the structured scoring rubrics used by the CV analyzer/optimizer application to evaluate each section of a resume objectively, generate an overall quality score, and produce actionable feedback. All scores are on a 0-100 scale unless otherwise noted.

## 1. Overall Score Architecture
### Score Components and Weights
| Component | Weight | Description |
|---|---|---|
| Contact Information | 5% | Completeness and professionalism |
| Professional Summary | 10% | Quality, relevance, and impact |
| Work Experience | 35% | Depth, achievements, and relevance |
| Education | 10% | Completeness and relevance |
| Skills Section | 15% | Match rate, completeness, and format |
| Keyword Match (JD) | 20% | Alignment with target job description |
| Formatting / ATS Compatibility | 5% | Parsability and professional presentation |

### Overall Score Thresholds
| Score Range | Rating | Recommendation |
|---|---|---|
| 90-100 | Excellent | Ready to submit; minor polish only |
| 80-89 | Strong | 1-2 targeted improvements recommended |
| 70-79 | Good | 3-5 improvements needed; competitive with revisions |
| 60-69 | Fair | Significant revisions recommended |
| 50-59 | Weak | Major rework needed |
| 0-49 | Poor | Complete rewrite recommended |

## 2. Contact Information Rubric (Max 100 → weighted 5%)
### Scoring Criteria
| Element | Points | Deduction Triggers |
|---|---|---|
| Full name present | 20 | Missing or only first name |
| Professional email address | 20 | Missing; unprofessional email (hotgirl@..., birthdayboy@...) |
| Phone number present | 15 | Missing |
| Phone number properly formatted | 5 | No separators; unrecognizable format |
| Location (city/state minimum) | 15 | Missing entirely |
| LinkedIn URL (optional but valuable) | 10 | Award 10 if present and well-formatted |
| No inappropriate information | 15 | Photo included (-10); DOB included (-10); SSN (-15); full home address (-5) |

### Deductions
- Photo included: -10 points (US/UK/Canada market context)
- Date of birth included: -10 points
- Marital status included: -10 points
- Full street address (not just city/state): -5 points
- Unprofessional email domain (e.g., aol.com): -5 points
- Unprofessional email handle: -10 points

## 3. Professional Summary Rubric (Max 100 → weighted 10%)
### Scoring Criteria
| Element | Points | Guidance |
|---|---|---|
| Summary present | 20 | 0 if entirely absent |
| Mentions years of experience | 10 | "5+ years of experience in..." |
| Mentions primary specialization | 10 | Industry or functional area named |
| Contains at least 1 quantified achievement | 20 | Specific metric or result |
| Includes 2-3 key competencies | 15 | Relevant to target role |
| Forward-looking value proposition | 10 | Answers "what value do I bring?" |
| Appropriate length (3-5 lines) | 10 | Deduct 5 for <2 lines; deduct 5 for >6 lines |
| Free of personal pronouns | 5 | Deduct 5 if "I," "me," "my" present |

### Score Modifiers
- Generic / not tailored to any specific role: -15 points
- Contains outdated buzzwords only ("dynamic team player"): -10 points
- Career objective instead of summary (for experienced candidates): -10 points
- Reads as a paragraph of duties (not achievements): -10 points

### Summary Score Band
- 85-100: Excellent — compelling, specific, and results-driven
- 70-84: Good — strong but could add more impact or specificity
- 55-69: Fair — present but vague; needs quantification and tailoring
- 0-54: Poor — missing, extremely generic, or objective-only

## 4. Work Experience Rubric (Max 100 → weighted 35%)
### Section-Level Scoring
| Element | Points | Notes |
|---|---|---|
| At least one role present | 10 | 0 if no experience at all |
| Reverse chronological order | 5 | Deduct if not in order |
| Consistent date formatting | 5 | Deduct if mixed formats present |
| Each role has: title, company, dates, location | 10 | Deduct 2 per missing element per role (up to 10) |

### Per-Role Bullet Quality Scoring (averaged across all roles)
| Element | Points per Role | Notes |
|---|---|---|
| Bullets start with action verbs | 10 | Deduct 2 per non-action-verb bullet |
| At least 1 quantified achievement per role | 20 | Specific number, %, $, or scale mentioned |
| Bullets describe outcomes, not just duties | 20 | "Managed X" vs. "Managed X, resulting in Y" |
| Appropriate number of bullets (3-6) | 10 | Deduct 5 for <2; deduct 5 for >8 |
| No personal pronouns | 5 | Deduct 1 per instance |
| Relevant to target role (if JD provided) | 20 | Scored relative to JD keyword presence |

### Experience Recency and Depth
| Situation | Score Modifier |
|---|---|
| Most recent role is current or ended <6 months ago | +5 |
| Gap of 6-12 months unexplained | -10 |
| Gap of 12+ months unexplained | -20 |
| Job hopping (>3 roles in 2 years, each <6 months) | -15 |
| Clear career progression evident | +10 |
| Consistent industry experience | +5 |

### Work Experience Score Band
- 85-100: Excellent — achievement-focused, quantified, relevant
- 70-84: Good — strong but some duties-only bullets; add more metrics
- 55-69: Fair — mostly duties-focused; needs achievement reframing
- 0-54: Poor — sparse, duty-only, or no quantification at all

## 5. Education Rubric (Max 100 → weighted 10%)
### Scoring Criteria
| Element | Points | Notes |
|---|---|---|
| Degree type present | 25 | BS, BA, MS, MBA, PhD, etc. |
| Field of study present | 20 | Major or concentration listed |
| Institution name present | 20 | Full name, not abbreviated |
| Graduation year present | 20 | Year is sufficient; month optional |
| GPA present (if 3.5+ and recent) | 15 | Only award if GPA >= 3.5; penalize if <3.0 shown |

### Deductions
- High school listed when degree is present: -10
- GPA below 3.0 included: -15
- Degree listed without institution: -15
- Expected graduation date without "Expected:" label: -5
- Education section missing entirely (for roles requiring degree): -40

### Education Placement Check
- For candidates with <3 years experience: Education should appear before Experience (+5 if correct)
- For candidates with 3+ years experience: Education should appear after Experience (+5 if correct)
- Wrong placement for experience level: -5 points

## 6. Skills Section Rubric (Max 100 → weighted 15%)
### Scoring Criteria
| Element | Points | Notes |
|---|---|---|
| Skills section present | 20 | 0 if no dedicated skills section |
| Contains 8+ skills | 15 | Deduct 2 per skill below 8 |
| Mix of technical and domain skills | 15 | Not all soft skills |
| No obvious outdated technologies | 10 | Deduct for obsolete tools unless contextual |
| No skill rating bars or graphics | 10 | ATS incompatible; deduct if present |
| Skills are specific (not vague) | 15 | "Microsoft Office" better than "computer skills" |
| Categorized appropriately (optional) | 10 | Award if Technical/Soft/Languages split present |
| No soft-skill-only section | 5 | "Hardworking, team player" only = -5 |

### Skills-to-JD Match (if JD provided)
- 80%+ of Tier 1 required skills present in skills section: +20 bonus
- 60-79% of Tier 1 skills present: +10 bonus
- Below 60% of Tier 1 skills present: no bonus; flag as gap

### Skills Section Score Band
- 85-100: Excellent — comprehensive, specific, ATS-friendly
- 70-84: Good — mostly complete; expand technical specificity
- 55-69: Fair — thin or too generic; needs targeted expansion
- 0-54: Poor — absent, all soft skills, or ATS-incompatible format

## 7. Keyword Match Rubric (Max 100 → weighted 20%)
### Requires JD Input
This section scores only when a job description is provided. Without a JD, this component is redistributed to Work Experience (35% → 45%) and Skills (15% → 20%).

### Scoring Methodology
**Tier 1 Keywords (Required) — 70% of keyword score:**
- Each Tier 1 keyword present in CV: +70 / (number of Tier 1 keywords) points
- Partial match (synonym or acronym): 75% credit
- Missing: 0 credit

**Tier 2 Keywords (Preferred) — 30% of keyword score:**
- Each Tier 2 keyword present in CV: +30 / (number of Tier 2 keywords) points
- Partial match: 75% credit
- Missing: 0 credit

### Keyword Placement Bonus
- Keyword appears in professional summary: +2 per keyword (cap: +10 total)
- Keyword appears in skills section: standard credit
- Keyword only appears once in experience bullets: 90% credit
- Keyword appears 0 times: 0 credit

### Keyword Match Score Band
- 85-100: Excellent — strong keyword alignment; ATS should rank highly
- 70-84: Good — solid match; add 2-3 missing Tier 1 terms
- 55-69: Fair — several key terms missing; targeted additions needed
- 0-54: Poor — major gaps; significant resume tailoring needed

## 8. Formatting / ATS Compatibility Rubric (Max 100 → weighted 5%)
### Scoring Criteria
| Element | Points | Deduction Triggers |
|---|---|---|
| No tables detected | 20 | Deduct 20 if tables present |
| No text boxes detected | 15 | Deduct 15 if text boxes present |
| No multi-column layout detected | 15 | Deduct 15 if multi-column present |
| Standard section headers used | 15 | Deduct 3 per non-standard header |
| No images or graphics detected | 10 | Deduct 10 if images present |
| Consistent bullet style | 10 | Deduct 5 if mixed bullets |
| Appropriate page length | 10 | Deduct 10 if >3 pages for standard resume |
| File format appropriate | 5 | Award 5 for .docx or text-based PDF |

### ATS Risk Flags (Flag but do not necessarily deduct twice)
- Table in experience section: HIGH risk
- Text box with contact info: HIGH risk
- Columns (2 or more): MEDIUM risk
- Headers/footers with critical info: MEDIUM risk
- Non-standard font: LOW risk
- Image-based PDF: CRITICAL — no text extractable

## 9. Bonus Score Factors
### Positive Bonuses (added to overall score, max +10 total)
- LinkedIn URL present and matches resume name: +2
- Portfolio or GitHub URL present (for relevant roles): +2
- Certifications listed with issuing body and year: +2
- Clear career progression visible (promotions, increasing scope): +2
- Quantified achievement in every role listed: +2

### Penalty Factors (subtracted from overall score)
- Spelling errors detected (per error): -2 (max -10)
- Grammatical errors detected (per error): -1 (max -5)
- Personal pronouns used: -3
- "References Available Upon Request" present: -2
- Salary history included: -3
- Photo included (US/UK/Canada): -5
- Date of birth included: -5
- Completely generic / unrelated to any role: -15

## 10. Score Reporting Format
### Output Structure for Each Resume Evaluation
    {
      "overall_score": 74,
      "rating": "Good",
      "section_scores": {
        "contact_information": { "score": 90, "weighted": 4.5 },
        "professional_summary": { "score": 65, "weighted": 6.5 },
        "work_experience": { "score": 78, "weighted": 27.3 },
        "education": { "score": 85, "weighted": 8.5 },
        "skills": { "score": 70, "weighted": 10.5 },
        "keyword_match": { "score": 60, "weighted": 12.0 },
        "formatting_ats": { "score": 95, "weighted": 4.75 }
      },
      "bonus_points": 4,
      "penalty_points": -3,
      "top_issues": [
        "Low keyword match: 8 Tier 1 keywords missing from JD",
        "Professional summary lacks quantified achievements",
        "3 roles have only duty-based bullets with no metrics"
      ],
      "top_strengths": [
        "Strong formatting — ATS compatible",
        "Education section complete and well-placed",
        "Contact information professional and complete"
      ]
    }

## 11. Score Change Tracking
### Before / After Optimization Comparison
When a resume is re-submitted after AI suggestions:
- Track delta score per section
- Highlight which sections improved and by how much
- Show estimated ATS ranking improvement (percentile)
- Flag any sections that regressed

### Improvement Benchmarks
| Score Delta | Interpretation |
|---|---|
| +20 or more | Major improvement — significantly more competitive |
| +10 to +19 | Strong improvement — recommended to submit |
| +5 to +9 | Moderate improvement — good progress |
| +1 to +4 | Marginal improvement — consider more targeted edits |
| 0 | No improvement — suggestions not applied or ineffective |
| Negative | Regression — review changes made |

---
*End of Scoring Rubrics Document*
*Version: 1.0*
*Last Updated: 2024*
