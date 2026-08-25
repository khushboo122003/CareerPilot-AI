import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Recruiter Intelligence | CareerPilot AI",
    page_icon="🎯",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================

st.title("🎯 Recruiter Intelligence")

st.write(
    "AI-powered candidate evaluation for smarter internship hiring."
)

st.divider()

# ============================================================
# CANDIDATE SELECTION
# ============================================================

# =========================================================
# CANDIDATE SELECTION
# =========================================================

import sqlite3

st.subheader("👤 Candidate")

conn = sqlite3.connect("careerpilot.db", check_same_thread=False)

candidates = conn.execute("""
    SELECT id, name, email, phone, college, skills
    FROM candidates
    ORDER BY id DESC
""").fetchall()

if not candidates:
    st.warning("No candidates found in the database.")
    st.stop()

candidate_options = {
    f"{row[1]} • Candidate #{row[0]}": row
    for row in candidates
}

selected_candidate = st.selectbox(
    "Select Candidate",
    list(candidate_options.keys())
)

candidate = candidate_options[selected_candidate]

candidate_id = candidate[0]
candidate_name = candidate[1]
candidate_email = candidate[2]
candidate_phone = candidate[3]
candidate_college = candidate[4]
candidate_skills = candidate[5]

# ============================================================
# CANDIDATE PROFILE
# ============================================================

st.write("")
# =========================================================
# CANDIDATE SELECTION
# =========================================================

import sqlite3

# Connect to CareerPilot database
conn = sqlite3.connect("careerpilot.db", check_same_thread=False)

# Get all candidates
candidates = conn.execute("""
    SELECT id, name, email, phone, college, skills
    FROM candidates
    ORDER BY id DESC
""").fetchall()

# Check if candidates exist
if not candidates:
    st.warning("No candidates found in the database.")
    st.stop()

# Create readable names for dropdown
candidate_options = {
    f"{candidate[1]}  •  Candidate #{candidate[0]}": candidate
    for candidate in candidates
}

# Candidate dropdown
selected_candidate_label = st.selectbox(
    "🎯 Select Candidate",
    list(candidate_options.keys())
)

# Get selected candidate information
selected_candidate = candidate_options[selected_candidate_label]

candidate_id = selected_candidate[0]
candidate_name = selected_candidate[1]
candidate_email = selected_candidate[2]
candidate_phone = selected_candidate[3]
candidate_college = selected_candidate[4]
candidate_skills = selected_candidate[5]

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "📧 Email\n\n"
        "khushbookushwaha012@gmail.com"
    )

with col2:
    st.info(
        "📱 Phone\n\n"
        "7080857210"
    )

with col3:
    st.info(
        "🎓 College\n\n"
        "Galgotias University"
    )

# ============================================================
# AI RESUME ANALYSIS
# ============================================================

st.divider()

st.subheader("🤖 AI Resume Analysis")

st.caption(
    "Candidate insights generated from the resume analysis."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "ATS Score",
        "87%"
    )

with col2:
    st.metric(
        "Technical Skills",
        "4 / 5"
    )

with col3:
    st.metric(
        "Communication",
        "4 / 5"
    )

with col4:
    st.metric(
        "Overall Match",
        "Strong"
    )

# ============================================================
# AUTOMATIC EVALUATION
# ============================================================

st.divider()

st.subheader("⭐ Candidate Evaluation")

st.caption(
    "The system automatically evaluates the candidate. "
    "The recruiter does not need to write feedback."
)

# These values represent the current AI evaluation.
# Later we will connect these directly to your resume analyzer.
# Get AI scores from the latest resume analysis
analysis = st.session_state.get("resume_analysis", {})

technical_score = float(analysis.get("technical_skills", 0))
communication_score = float(analysis.get("communication", 0))
problem_solving_score = float(analysis.get("problem_solving", 0))
confidence_score = float(analysis.get("confidence", 0))

# ============================================================
# SCORE DISPLAY
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.write("### 💻 Technical Skills")
    st.progress(technical_score / 5)
    st.write(f"**{technical_score}/5**")

    st.write("### 🗣️ Communication")
    st.progress(communication_score / 5)
    st.write(f"**{communication_score}/5**")


with col2:

    st.write("### 🧠 Problem Solving")
    st.progress(problem_solving_score / 5)
    st.write(f"**{problem_solving_score}/5**")

    st.write("### 💪 Confidence")
    st.progress(confidence_score / 5)
    st.write(f"**{confidence_score}/5**")

# ============================================================
# OVERALL SCORE
# ============================================================

overall_score = round(
    (
        technical_score
        + communication_score
        + problem_solving_score
        + confidence_score
    ) / 4,
    1
)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Overall Evaluation",
        f"{overall_score} / 5"
    )

with col2:
    st.metric(
        "Candidate Level",
        "Strong"
    )

with col3:
    st.metric(
        "Hiring Stage",
        "Internship"
    )

# ============================================================
# AUTOMATIC RECRUITER FEEDBACK
# ============================================================

st.divider()

st.subheader("🤖 AI-Generated Recruiter Feedback")

st.caption(
    "This assessment is automatically generated from the "
    "candidate's evaluation data."
)

# ============================================================
# AUTOMATIC FEEDBACK LOGIC
# ============================================================

if overall_score >= 4.5:

    feedback_title = "Excellent Candidate"

    feedback_summary = (
        "The candidate demonstrates excellent overall potential "
        "and is highly suitable for an internship opportunity."
    )

    strengths = [
        "Strong technical foundation",
        "Excellent problem-solving potential",
        "Good communication ability",
        "Strong overall internship readiness"
    ]

    improvements = [
        "Continue developing advanced technical skills",
        "Gain additional real-world project experience"
    ]

    ai_recommendation = "Strongly Recommend"


elif overall_score >= 4.0:

    feedback_title = "Strong Candidate"

    feedback_summary = (
        "The candidate demonstrates strong technical and "
        "problem-solving potential and appears suitable for "
        "the next stage of the internship hiring process."
    )

    strengths = [
        "Good technical foundation",
        "Good problem-solving ability",
        "Good communication potential",
        "Relevant internship skills"
    ]

    improvements = [
        "Strengthen advanced technical concepts",
        "Gain additional practical project experience"
    ]

    ai_recommendation = "Recommend"


elif overall_score >= 3.0:

    feedback_title = "Promising Candidate"

    feedback_summary = (
        "The candidate shows promising potential but may "
        "benefit from additional evaluation before proceeding."
    )

    strengths = [
        "Shows relevant foundational skills",
        "Demonstrates learning potential",
        "Has potential for internship development"
    ]

    improvements = [
        "Improve technical depth",
        "Strengthen problem-solving skills",
        "Gain more practical experience"
    ]

    ai_recommendation = "Consider"


else:

    feedback_title = "Needs Further Development"

    feedback_summary = (
        "The candidate currently requires additional development "
        "before being considered for the next hiring stage."
    )

    strengths = [
        "Shows basic potential",
        "Has opportunities for skill development"
    ]

    improvements = [
        "Improve technical skills",
        "Improve problem-solving ability",
        "Gain practical project experience",
        "Improve interview readiness"
    ]

    ai_recommendation = "Do Not Recommend"

# ============================================================
# OVERALL ASSESSMENT
# ============================================================

if ai_recommendation == "Strongly Recommend":
    st.success(
        f"### 🟢 {feedback_title}\n\n"
        f"{feedback_summary}"
    )

elif ai_recommendation == "Recommend":
    st.success(
        f"### 🟢 {feedback_title}\n\n"
        f"{feedback_summary}"
    )

elif ai_recommendation == "Consider":
    st.warning(
        f"### 🟡 {feedback_title}\n\n"
        f"{feedback_summary}"
    )

else:
    st.error(
        f"### 🔴 {feedback_title}\n\n"
        f"{feedback_summary}"
    )

# ============================================================
# AUTOMATIC STRENGTHS & IMPROVEMENTS
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 💪 Identified Strengths")

    for strength in strengths:
        st.write(f"✅ {strength}")


with col2:

    st.markdown("### 📈 Areas for Improvement")

    for improvement in improvements:
        st.write(f"• {improvement}")

# ============================================================
# AI RECOMMENDATION
# ============================================================

st.divider()

st.subheader("🎯 AI Hiring Recommendation")

if ai_recommendation == "Strongly Recommend":

    st.success(
        f"**{ai_recommendation}**\n\n"
        "The candidate is highly suitable for the internship "
        "and should proceed to the next hiring stage."
    )

elif ai_recommendation == "Recommend":

    st.success(
        f"**{ai_recommendation}**\n\n"
        "The candidate appears suitable for the internship "
        "and should be considered for the next stage."
    )

elif ai_recommendation == "Consider":

    st.warning(
        f"**{ai_recommendation}**\n\n"
        "The candidate should undergo additional evaluation "
        "before a final decision."
    )

else:

    st.error(
        f"**{ai_recommendation}**\n\n"
        "The candidate currently requires further development "
        "before proceeding."
    )

# ============================================================
# RECRUITER FINAL DECISION
# ============================================================

st.divider()

st.subheader("👔 Recruiter Final Decision")

st.caption(
    "The AI provides the assessment. The recruiter makes "
    "the final hiring decision."
)

decision = st.radio(
    "Select final decision",
    [
        "Hire",
        "Hold",
        "Reject"
    ],
    horizontal=True
)

# ============================================================
# SAVE RECRUITER EVALUATION
# ============================================================

st.write("")

if st.button(
    "💾 Save Recruiter Evaluation",
    type="primary",
    use_container_width=True
):

    try:
        import sqlite3

        # ----------------------------------------------------
        # CANDIDATE INFORMATION
        # ----------------------------------------------------

        candidate_id = candidate[0]
        candidate_name = candidate[1]

        # ----------------------------------------------------
        # GET RECRUITER RATINGS
        # ----------------------------------------------------

        technical_skills_value = int(
            globals().get("technical_skills", 0)
        )

        communication_value = int(
            globals().get("communication", 0)
        )

        problem_solving_value = int(
            globals().get("problem_solving", 0)
        )

        confidence_value = int(
            globals().get("confidence", 0)
        )

        # ----------------------------------------------------
        # GET COMMENTS / FEEDBACK
        # ----------------------------------------------------

        comments_value = globals().get("comments", "")

        if not comments_value:
            comments_value = globals().get("feedback", "")

        if comments_value is None:
            comments_value = ""

        # ----------------------------------------------------
        # RECRUITER DECISION
        # ----------------------------------------------------

        decision_value = decision

        # ----------------------------------------------------
        # CONNECT TO DATABASE
        # ----------------------------------------------------

        conn = sqlite3.connect(
            "careerpilot.db",
            check_same_thread=False
        )

        cursor = conn.cursor()

        # ----------------------------------------------------
        # FIX EXISTING DATABASE
        # ----------------------------------------------------
        # The old recruiter_feedback table may not have
        # the comments column. Add it automatically.

        cursor.execute(
            "PRAGMA table_info(recruiter_feedback)"
        )

        existing_columns = [
            row[1]
            for row in cursor.fetchall()
        ]

        if "comments" not in existing_columns:

            cursor.execute(
                """
                ALTER TABLE recruiter_feedback
                ADD COLUMN comments TEXT
                """
            )

        # ----------------------------------------------------
        # SAVE EVALUATION
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO recruiter_feedback
            (
                candidate_id,
                technical_skills,
                communication,
                problem_solving,
                confidence,
                decision,
                comments
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
           (
    candidate_id,
    technical_score,
    communication_score,
    problem_solving_score,
    confidence_score,
    decision_value,
    comments_value
)
        )

        conn.commit()
        conn.close()

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        st.success(
            f"✅ Recruiter evaluation saved successfully for {candidate_name}."
        )

        st.balloons()

    except Exception as e:

        st.error(
            f"❌ Unable to save recruiter evaluation: {e}"
        )


# ============================================================
# EVALUATION SUMMARY
# ============================================================

st.divider()

st.subheader("📋 Evaluation Summary")

col1, col2, col3 = st.columns(3)

# ------------------------------------------------------------
# AI RECOMMENDATION
# ------------------------------------------------------------

with col1:

    st.write(
        f"**AI Recommendation:** {ai_recommendation}"
    )


# ------------------------------------------------------------
# OVERALL SCORE
# ------------------------------------------------------------

with col2:

    scores = [
        globals().get("technical_skills", 0),
        globals().get("communication", 0),
        globals().get("problem_solving", 0),
        globals().get("confidence", 0)
    ]

    valid_scores = [
        score
        for score in scores
        if isinstance(score, (int, float))
    ]

    if valid_scores:
        overall_score = sum(valid_scores) / len(valid_scores)
    else:
        overall_score = 0


# ------------------------------------------------------------
# RECRUITER DECISION
# ------------------------------------------------------------

with col3:

    st.write(
        f"**Recruiter Decision:** {decision}"
    )