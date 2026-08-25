import os
import json
import re

import google.generativeai as genai
from dotenv import load_dotenv


# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please add your Gemini API key to the .env file."
    )


# -----------------------------
# Configure Gemini
# -----------------------------

genai.configure(api_key=api_key)


# -----------------------------
# Create Gemini Model
# -----------------------------

model = genai.GenerativeModel(
    "gemini-3.6-flash"
)


# -----------------------------
# Resume Analyzer
# -----------------------------

def analyze_resume(resume_text):

    prompt = f"""
You are CareerPilot AI, an expert AI career coach, resume reviewer,
and internship recruiter.

Analyze the following resume carefully.

RESUME:
{resume_text}

Return ONLY valid JSON.
Do not use markdown.
Do not use ```json.
Do not add any explanation outside the JSON.

Use exactly this JSON structure:

{{
    "resume_score": 0,
    "technical_skills": 0,
    "communication": 0,
    "problem_solving": 0,
    "confidence": 0,
    "professional_summary": "",
    "key_strengths": [],
    "areas_for_improvement": [],
    "suggested_job_roles": [],
    "missing_skills": [],
    "learning_roadmap": [],
    "technical_interview_questions": [],
    "hr_interview_questions": [],
    "final_career_advice": []
}}

SCORING RULES:

1. resume_score:
   Give an overall resume score from 0 to 100.

2. technical_skills:
   Score from 0 to 5 based ONLY on the technical skills,
   tools, technologies, projects, certifications, and experience
   actually present in the resume.

3. communication:
   Score from 0 to 5 based on the clarity, organization,
   writing quality, and presentation of the resume.

4. problem_solving:
   Score from 0 to 5 based on evidence of projects,
   problem-solving work, achievements, implementation,
   analytical work, or practical experience in the resume.

5. confidence:
   Score from 0 to 5 based on evidence of ownership,
   achievements, leadership, project responsibility,
   initiative, internships, or other demonstrated experience.

IMPORTANT:
- Do NOT automatically give 4.
- Do NOT give the same score to every candidate.
- Scores must be based on the actual resume.
- Use decimal scores when appropriate, such as 3.5 or 4.5.
- If there is little or no evidence for a category, give a lower score.
- Never invent experience or skills that are not present in the resume.

CONTENT RULES:

professional_summary:
Write a concise 3-4 sentence summary based on the resume.

key_strengths:
List the strongest technical and professional strengths found in the resume.

areas_for_improvement:
List specific weaknesses or areas that need improvement.

suggested_job_roles:
Suggest suitable job roles based on the actual resume.

missing_skills:
Identify important skills relevant to the candidate's likely career direction
that are missing or insufficiently demonstrated.

learning_roadmap:
Give a personalized learning roadmap.

technical_interview_questions:
Create exactly 5 technical interview questions based on the resume.

hr_interview_questions:
Create exactly 5 HR interview questions relevant to the candidate.

final_career_advice:
Give 4-5 specific and actionable recommendations.
Avoid generic advice.
Base the recommendations on the actual resume.
"""

    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    # -----------------------------
    # Clean possible JSON formatting
    # -----------------------------

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

    # -----------------------------
    # Convert AI response to JSON
    # -----------------------------

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        # Try to extract the JSON object if Gemini
        # returned extra text around it.
        match = re.search(
            r"\{.*\}",
            raw_text,
            re.DOTALL
        )

        if not match:
            raise ValueError(
                "Gemini returned an invalid analysis format."
            )

        result = json.loads(match.group(0))

    # -----------------------------
    # Make sure scores are numbers
    # -----------------------------

    result["resume_score"] = float(
        result.get("resume_score", 0)
    )

    result["technical_skills"] = float(
        result.get("technical_skills", 0)
    )

    result["communication"] = float(
        result.get("communication", 0)
    )

    result["problem_solving"] = float(
        result.get("problem_solving", 0)
    )

    result["confidence"] = float(
        result.get("confidence", 0)
    )

    # Keep scores inside their allowed ranges
    result["resume_score"] = max(
        0,
        min(100, result["resume_score"])
    )

    result["technical_skills"] = max(
        0,
        min(5, result["technical_skills"])
    )

    result["communication"] = max(
        0,
        min(5, result["communication"])
    )

    result["problem_solving"] = max(
        0,
        min(5, result["problem_solving"])
    )

    result["confidence"] = max(
        0,
        min(5, result["confidence"])
    )

    return result