import os
import json
import re

import google.generativeai as genai
from dotenv import load_dotenv


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please add your Gemini API key to the .env file."
    )


# --------------------------------------------------
# CONFIGURE GEMINI
# --------------------------------------------------

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-3.6-flash"
)


# --------------------------------------------------
# RECRUITER SHORTLISTING
# --------------------------------------------------

def evaluate_candidate_for_job(
    resume_text,
    job_description
):
    """
    Evaluate one candidate against one specific
    job description.
    """

    prompt = f"""
You are CareerPilot AI's Recruiter Screening Engine.

Evaluate ONE candidate for ONE specific job.

Your decision must be based ONLY on:
1. The candidate's actual resume
2. The supplied job description

CANDIDATE RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add explanations outside the JSON.

Use EXACTLY this structure:

{{
    "candidate_name": "",
    "match_score": 0,
    "decision": "",
    "matching_skills": [],
    "missing_skills": [],
    "relevant_experience": [],
    "reason": ""
}}

SCORING RULES:

1. match_score:
   Give a realistic score from 0 to 100.

   Base the score on the actual relationship between
   the candidate's resume and the job requirements.

   Do NOT use a fixed score.

   Do NOT automatically give 80, 90, or any other value.

2. decision:

   If match_score is 80 or higher:
   "SHORTLIST"

   If match_score is between 60 and 79:
   "MAYBE"

   If match_score is below 60:
   "NOT SUITABLE"

3. candidate_name:
   Extract the candidate's name from the resume.

   If the name cannot be identified, return:
   "Unknown Candidate"

4. matching_skills:
   List skills that are BOTH:
   - actually present in the resume
   - relevant to the job description

5. missing_skills:
   List important skills or requirements from the job
   description that are missing or insufficiently demonstrated
   in the resume.

6. relevant_experience:
   List actual projects, internships, education,
   certifications, achievements, or work experience
   that are relevant to the job.

   Never invent experience.

7. reason:
   Give a concise recruiter-friendly explanation
   for the decision.

IMPORTANT:

- Different candidates MUST receive different evaluations
  when their resumes differ.
- The same candidate can receive different evaluations
  for different jobs.
- Never invent skills or experience.
- Do not judge based on the candidate's name.
- Do not discriminate based on age, gender, religion,
  nationality, race, or other protected characteristics.
- Focus only on job-relevant qualifications.
- Treat internship and entry-level candidates fairly.
"""

    response = model.generate_content(prompt)

    raw_text = response.text.strip()


    # --------------------------------------------------
    # CLEAN POSSIBLE MARKDOWN
    # --------------------------------------------------

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


    # --------------------------------------------------
    # CONVERT RESPONSE TO JSON
    # --------------------------------------------------

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
                "Gemini returned an invalid candidate evaluation."
            )

        result = json.loads(
            match.group(0)
        )


    # --------------------------------------------------
    # VALIDATE SCORE
    # --------------------------------------------------

    result["match_score"] = float(
        result.get(
            "match_score",
            0
        )
    )

    result["match_score"] = max(
        0,
        min(
            100,
            result["match_score"]
        )
    )


    # --------------------------------------------------
    # VALIDATE DECISION
    # --------------------------------------------------

    score = result["match_score"]

    if score >= 80:

        result["decision"] = "SHORTLIST"

    elif score >= 60:

        result["decision"] = "MAYBE"

    else:

        result["decision"] = "NOT SUITABLE"


    # --------------------------------------------------
    # DEFAULT CANDIDATE NAME
    # --------------------------------------------------

    if not result.get("candidate_name"):

        result["candidate_name"] = (
            "Unknown Candidate"
        )


    return result