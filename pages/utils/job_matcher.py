import json
import re
import google.generativeai as genai


def match_candidate_to_job(resume_analysis, job_description):
    """
    Compare a candidate's resume analysis with a specific
    job description and generate a personalized job match.
    """

    prompt = f"""
You are CareerPilot AI's Job Description Matching Engine.

Your task is to compare ONE candidate's actual resume analysis
against ONE specific job description.

Do NOT recommend a generic job.

The recruiter has provided a specific job description.
Your job is to determine how well THIS candidate matches THIS job.

CANDIDATE RESUME ANALYSIS:
{json.dumps(resume_analysis, indent=2)}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add explanations outside the JSON.

Use EXACTLY this structure:

{{
    "job_title": "",
    "match_score": 0,
    "matching_skills": [],
    "missing_skills": [],
    "relevant_experience": [],
    "match_summary": "",
    "recommendation": ""
}}

SCORING RULES:

1. match_score:
   Give a realistic score from 0 to 100.

   The score must be based on how well the candidate's
   demonstrated skills, projects, education, certifications,
   and experience match the actual job description.

   Do NOT automatically give 80, 90, or any fixed score.

   A candidate with many strong matches should score higher.

   A candidate with many missing requirements should score lower.

2. job_title:
   Extract the job title from the supplied job description.

   If no clear title exists, create a short appropriate title
   based on the job description.

3. matching_skills:
   List ONLY skills that are both:
   - actually demonstrated by the candidate
   - relevant to the supplied job description

   Do NOT invent skills.

4. missing_skills:
   Identify important skills or requirements from the job
   description that are missing or insufficiently demonstrated
   in the candidate's resume.

5. relevant_experience:
   List projects, internships, certifications, education,
   achievements, or other experience from the resume that
   directly relates to this job.

   Do NOT invent experience.

6. match_summary:
   Give a concise explanation of the candidate's overall
   suitability for this specific job.

   Mention both strong matches and important gaps.

7. recommendation:
   Give ONE clear recommendation.

   Examples:
   - "Strong match - recommend for interview"
   - "Good match - shortlist for further review"
   - "Moderate match - review skill gaps"
   - "Weak match - candidate needs more relevant skills"

IMPORTANT:

- This must be candidate-specific AND job-specific.
- Do NOT use a fixed match score.
- Do NOT recommend the same result for every candidate.
- Do NOT invent skills, projects, experience, or qualifications.
- Use ONLY information available in the candidate analysis
  and job description.
- Consider internship/entry-level candidates fairly.
"""

    response = genai.GenerativeModel(
        "gemini-3.6-flash"
    ).generate_content(prompt)

    raw_text = response.text.strip()

    # Remove possible markdown formatting
    raw_text = re.sub(
        r"^```json\s*",
        "",
        raw_text,
        flags=re.IGNORECASE
    )

    raw_text = re.sub(
        r"^```\s*",
        "",
        raw_text
    )

    raw_text = re.sub(
        r"\s*```$",
        "",
        raw_text
    )

    # Convert AI response to JSON
    try:
        result = json.loads(raw_text)

    except json.JSONDecodeError:

        match = re.search(
            r"\{.*\}",
            raw_text,
            re.DOTALL
        )

        if not match:
            raise ValueError(
                "Gemini returned an invalid job match format."
            )

        result = json.loads(match.group(0))

    # Keep match score between 0 and 100
    result["match_score"] = float(
        result.get("match_score", 0)
    )

    result["match_score"] = max(
        0,
        min(100, result["match_score"])
    )

    return result