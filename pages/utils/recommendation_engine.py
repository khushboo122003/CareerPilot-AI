import json
import re
import google.generativeai as genai


def generate_recommendation(resume_analysis):
    """
    Generate a personalized, resume-based career recommendation.
    """

    prompt = f"""
You are CareerPilot AI's personalized career recommendation engine.

Your task is to analyze ONE candidate's resume analysis and recommend
the SINGLE BEST-FIT job role for that specific candidate.

Do NOT recommend the same role to every candidate.

The recommendation MUST change according to the candidate's:
- Technical skills
- Projects
- Experience
- Strengths
- Missing skills
- Career direction
- Resume score
- Technical skills score
- Communication score
- Problem-solving score
- Confidence score

CANDIDATE RESUME ANALYSIS:
{json.dumps(resume_analysis, indent=2)}

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add any explanation outside the JSON.

Use EXACTLY this structure:

{{
    "best_fit_role": "",
    "match_score": 0,
    "career_direction": "",
    "matching_skills": [],
    "skills_to_improve": [],
    "why_this_role": "",
    "recommended_actions": []
}}

RULES:

1. BEST-FIT ROLE

Choose the SINGLE job role that best matches this candidate's
actual resume.

Examples of possible roles include:
- Data Analyst Intern
- Python Developer Intern
- Frontend Developer Intern
- Backend Developer Intern
- Full Stack Developer Intern
- Java Developer Intern
- Machine Learning Intern
- Software Developer Intern
- Business Analyst Intern
- UI/UX Design Intern
- Cybersecurity Intern
- Cloud/DevOps Intern

These are ONLY examples.

You may recommend another role if the candidate's resume
supports it.

Do NOT force the candidate into one of these examples.

2. MATCH SCORE

Give a realistic score from 0 to 100.

The score must represent how strongly the candidate's
current resume matches the recommended role.

Do NOT automatically give 80, 90, or any other fixed score.

Different candidates MUST receive different scores when
their resumes differ.

3. CAREER DIRECTION

Give a short explanation of the career direction that would
be most suitable for this candidate.

4. MATCHING SKILLS

List the skills that are actually present in the resume and
directly support the recommended role.

Do NOT invent skills.

5. SKILLS TO IMPROVE

List the most important skills the candidate should improve
to become stronger for the recommended role.

Use the missing skills and weaker areas from the resume analysis.

6. WHY THIS ROLE

Explain specifically why this job role fits the candidate.

Mention evidence from the resume analysis such as:
- skills
- projects
- experience
- education
- certifications
- achievements

Do not give generic explanations.

7. RECOMMENDED ACTIONS

Give EXACTLY 4 practical actions.

The actions should help the candidate become more competitive
for the recommended role.

Examples:
- Build a relevant project
- Improve a missing technical skill
- Practice interview questions
- Improve the resume
- Complete a relevant certification

Only recommend actions that make sense for THIS candidate.

IMPORTANT:

- Do NOT give the same job recommendation to every candidate.
- Base everything on the supplied candidate analysis.
- Do NOT invent experience.
- Do NOT invent skills.
- Do NOT assume skills that are not demonstrated.
- Be realistic for an internship or early-career candidate.
- Prefer a specific internship/job role rather than a broad career field.
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
        recommendation = json.loads(raw_text)

    except json.JSONDecodeError:

        match = re.search(
            r"\{.*\}",
            raw_text,
            re.DOTALL
        )

        if not match:
            raise ValueError(
                "Gemini returned an invalid recommendation format."
            )

        recommendation = json.loads(match.group(0))

    # Keep match score within 0-100
    recommendation["match_score"] = float(
        recommendation.get("match_score", 0)
    )

    recommendation["match_score"] = max(
        0,
        min(100, recommendation["match_score"])
    )

    return recommendation