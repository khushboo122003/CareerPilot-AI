import streamlit as st
import sqlite3

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)
# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

conn = sqlite3.connect("careerpilot.db")

candidate_count = conn.execute(
    "SELECT COUNT(*) FROM candidates"
).fetchone()[0]

feedback_count = conn.execute(
    "SELECT COUNT(*) FROM recruiter_feedback"
).fetchone()[0]

resume_count = candidate_count

ai_match_count = feedback_count

conn.close()

st.title("🚀 CareerPilot AI")
st.subheader("AI-Powered Recruitment & Candidate Intelligence Platform")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
   st.metric("👤 Candidates", candidate_count)

with col2:
   st.metric("📄 Resumes", resume_count)

with col3:
   st.metric("💬 Feedback", feedback_count)

with col4:
   st.metric("🤖 AI Matches", ai_match_count)

st.divider()

st.subheader("⚡ Quick Actions")

col1, col2 = st.columns(2)

with col1:
    st.button("➕ Add Candidate")

with col2:
    st.button("📄 Analyze Resume")

st.divider()
st.subheader("📋 Recent Candidates")

conn = sqlite3.connect("careerpilot.db")

recent_candidates = conn.execute("""
    SELECT name, email, college, skills
    FROM candidates
    ORDER BY id DESC
    LIMIT 5
""").fetchall()

conn.close()

if recent_candidates:

    for candidate in recent_candidates:

        name, email, college, skills = candidate

        with st.container(border=True):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"👤 **{name or 'Unknown'}**")

            with col2:
                st.write(f"📧 {email or 'No email'}")

            with col3:
                st.write(f"🎓 {college or 'Not provided'}")

            if skills:
                st.caption(
                    f"🛠️ Skills: {skills}"
                )

else:

    st.info(
        "No candidates added yet."
    )
# ---------------------------------------------------------
# CANDIDATE INTELLIGENCE
# ---------------------------------------------------------

st.divider()

st.subheader("📊 Candidate Intelligence")

conn = sqlite3.connect("careerpilot.db")

feedback_stats = conn.execute("""
    SELECT
        AVG(technical_skills),
        AVG(communication),
        AVG(problem_solving),
        AVG(confidence)
    FROM recruiter_feedback
""").fetchone()

conn.close()

technical_avg = feedback_stats[0]
communication_avg = feedback_stats[1]
problem_solving_avg = feedback_stats[2]
confidence_avg = feedback_stats[3]

if technical_avg is not None:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🛠️ Technical Skills",
            f"{technical_avg:.1f} / 5"
        )

    with col2:
        st.metric(
            "💬 Communication",
            f"{communication_avg:.1f} / 5"
        )

    with col3:
        st.metric(
            "🧠 Problem Solving",
            f"{problem_solving_avg:.1f} / 5"
        )

    with col4:
        st.metric(
            "💪 Confidence",
            f"{confidence_avg:.1f} / 5"
        )

else:

    st.info(
        "No recruiter feedback available yet."
    )