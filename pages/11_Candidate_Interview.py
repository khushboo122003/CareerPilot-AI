import streamlit as st
import pdfplumber

from pages.utils.interview_generator import (
    generate_interview_questions
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CareerPilot AI - Candidate Interview",
    page_icon="🎤",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎤 Candidate Interview Generator")

st.write(
    "Generate personalized interview questions for a candidate "
    "based on their resume and the job they are applying for."
)

st.divider()

# --------------------------------------------------
# CANDIDATE RESUME
# --------------------------------------------------

st.subheader("👤 Candidate Resume")

uploaded_file = st.file_uploader(
    "Upload candidate resume",
    type=["pdf"],
    help="Upload the candidate's PDF resume."
)

resume_text = ""

if uploaded_file is not None:

    st.success(
        f"✅ Resume uploaded: {uploaded_file.name}"
    )

    try:

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    resume_text += page_text + "\n"

    except Exception as e:

        st.error(
            "❌ Could not read the resume."
        )

        st.exception(e)


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description",
    height=300,
    placeholder=(
        "Paste the complete job description here..."
    )
)


# --------------------------------------------------
# GENERATE INTERVIEW
# --------------------------------------------------

if st.button(
    "🎤 Generate Candidate Interview",
    type="primary",
    use_container_width=True
):

    if not resume_text.strip():

        st.warning(
            "⚠️ Please upload a candidate resume first."
        )

    elif not job_description.strip():

        st.warning(
            "⚠️ Please enter the job description first."
        )

    else:

        with st.spinner(
            "🤖 Generating personalized interview questions..."
        ):

            try:

                result = generate_interview_questions(
                    resume_text,
                    job_description
                )

                st.session_state[
                    "candidate_interview"
                ] = result

                st.success(
                    "🎉 Candidate interview generated successfully!"
                )

            except Exception as e:

                st.error(
                    "❌ Something went wrong while generating the interview."
                )

                st.exception(e)


# --------------------------------------------------
# DISPLAY INTERVIEW QUESTIONS
# --------------------------------------------------

if "candidate_interview" in st.session_state:

    result = st.session_state[
        "candidate_interview"
    ]

    st.divider()

    # --------------------------------------------------
    # TECHNICAL QUESTIONS
    # --------------------------------------------------

    st.subheader(
        "🛠️ Technical Interview Questions"
    )

    technical_questions = result.get(
        "technical_questions",
        []
    )

    for index, question in enumerate(
        technical_questions,
        start=1
    ):

        st.markdown(
            f"**{index}. {question}**"
        )


    # --------------------------------------------------
    # HR QUESTIONS
    # --------------------------------------------------

    st.subheader(
        "👥 HR Interview Questions"
    )

    hr_questions = result.get(
        "hr_questions",
        []
    )

    for index, question in enumerate(
        hr_questions,
        start=1
    ):

        st.markdown(
            f"**{index}. {question}**"
        )
# --------------------------------------------------
# DOWNLOAD INTERVIEW REPORT
# --------------------------------------------------

if "candidate_interview" in st.session_state:

    result = st.session_state["candidate_interview"]

    report = "CAREERPILOT AI - CANDIDATE INTERVIEW REPORT\n"
    report += "=" * 60 + "\n\n"

    report += "TECHNICAL INTERVIEW QUESTIONS\n"
    report += "-" * 40 + "\n\n"

    technical_questions = result.get(
        "technical_questions",
        []
    )

    for index, question in enumerate(
        technical_questions,
        start=1
    ):
        report += f"{index}. {question}\n"

    report += "\n\n"

    report += "HR INTERVIEW QUESTIONS\n"
    report += "-" * 40 + "\n\n"

    hr_questions = result.get(
        "hr_questions",
        []
    )

    for index, question in enumerate(
        hr_questions,
        start=1
    ):
        report += f"{index}. {question}\n"

    st.download_button(
        label="📥 Download Interview Report",
        data=report,
        file_name="CareerPilot_AI_Interview_Report.txt",
        mime="text/plain",
        use_container_width=True
    )