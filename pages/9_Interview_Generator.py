import streamlit as st

from pages.utils.interview_generator import (
    generate_interview_questions
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CareerPilot AI - Interview Generator",
    page_icon="🎤",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎤 AI Interview Generator")

st.write(
    "Generate personalized technical and HR interview "
    "questions based on the candidate's resume and the job description."
)

st.divider()

# --------------------------------------------------
# CANDIDATE RESUME
# --------------------------------------------------

st.subheader("📄 Candidate Resume Analysis")

resume_analysis_text = st.text_area(
    "Paste the candidate's resume analysis here",
    height=250,
    placeholder="Paste the AI resume analysis here..."
)

# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=250,
    placeholder="Paste the complete job description here..."
)

# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

if st.button(
    "🎤 Generate Interview Questions",
    type="primary",
    use_container_width=True
):

    if not resume_analysis_text.strip():

        st.warning(
            "⚠️ Please provide the candidate's resume analysis."
        )

    elif not job_description.strip():

        st.warning(
            "⚠️ Please provide the job description."
        )

    else:

        with st.spinner(
            "🤖 Generating personalized interview questions..."
        ):

            try:

                analysis = resume_analysis_text

                result = generate_interview_questions(
                    analysis,
                    job_description
                )

                st.session_state[
                    "interview_questions"
                ] = result

                st.success(
                    "🎉 Interview questions generated successfully!"
                )

            except Exception as e:

                st.error(
                    "❌ Something went wrong while generating questions."
                )

                st.exception(e)


# --------------------------------------------------
# DISPLAY QUESTIONS
# --------------------------------------------------

if "interview_questions" in st.session_state:

    result = st.session_state[
        "interview_questions"
    ]

    st.divider()

    # --------------------------------------------------
    # TECHNICAL QUESTIONS
    # --------------------------------------------------

    st.subheader("🛠️ Technical Interview Questions")

    technical_questions = result.get(
        "technical_questions",
        []
    )

    for i, question in enumerate(
        technical_questions,
        start=1
    ):

        st.markdown(
            f"**{i}. {question}**"
        )

    # --------------------------------------------------
    # HR QUESTIONS
    # --------------------------------------------------

    st.subheader("👥 HR Interview Questions")

    hr_questions = result.get(
        "hr_questions",
        []
    )

    for i, question in enumerate(
        hr_questions,
        start=1
    ):

        st.markdown(
            f"**{i}. {question}**"
        )