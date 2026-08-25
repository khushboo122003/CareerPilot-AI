import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please add your Gemini API key to the .env file."
    )

genai.configure(api_key=api_key)


def generate_interview_questions(
    resume_analysis,
    job_description
):
    """
    Generate candidate-specific and job-specific
    technical and HR interview questions.
    """

    prompt = f"""
You are CareerPilot AI's Interview Generation Engine.

Generate personalized interview questions for ONE candidate
applying to ONE specific job.

You must use BOTH:
1. The candidate's actual resume analysis
2. The specific job description

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
    "technical_questions": [],
    "hr_questions": []
}}

RULES:

TECHNICAL QUESTIONS:
- Generate exactly 5 questions.
- Questions must be relevant to the specific job.
- Questions must be based on the candidate's actual skills,
  projects, technologies, education, or experience.
- Include questions that test whether the candidate
  actually understands the skills shown on the resume.
- Include job-specific technical requirements where relevant.
- Do NOT invent projects or technologies for the candidate.
- Do NOT ask generic questions unrelated to the resume or job.

HR QUESTIONS:
- Generate exactly 5 questions.
- Questions must be relevant to the candidate and the job.
- Use the candidate's projects, education, experience,
  achievements, or career direction when appropriate.
- Include questions that could realistically be asked
  during an internship/job interview.
- Do NOT invent candidate experience.

IMPORTANT:

The questions must change when the candidate's resume changes.

The questions must also change when the job description changes.

Do NOT return the same fixed questions for every candidate.

Return exactly 5 technical questions and exactly 5 HR questions.
"""

    response = genai.GenerativeModel(
        "gemini-3.6-flash"
    ).generate_content(prompt)

    raw_text = response.text.strip()

    # --------------------------------------------------
    # Remove possible markdown formatting
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
    # Convert AI response to JSON
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
                "Gemini returned an invalid interview format."
            )

        result = json.loads(
            match.group(0)
        )

    # --------------------------------------------------
    # Validate question lists
    # --------------------------------------------------

    technical_questions = result.get(
        "technical_questions",
        []
    )

    hr_questions = result.get(
        "hr_questions",
        []
    )

    if not isinstance(
        technical_questions,
        list
    ):

        technical_questions = []

    if not isinstance(
        hr_questions,
        list
    ):

        hr_questions = []

    # --------------------------------------------------
    # Keep exactly 5 questions
    # --------------------------------------------------

    result["technical_questions"] = (
        technical_questions[:5]
    )

    result["hr_questions"] = (
        hr_questions[:5]
    )

    return result