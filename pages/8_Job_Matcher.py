import streamlit as st

from pages.utils.job_matcher import match_candidate_to_job


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CareerPilot AI - Job Matcher",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎯 AI Job Description Matcher")

st.write(
    "Compare a candidate's resume against a specific job "
    "description using AI."
)

st.divider()


# --------------------------------------------------
# CHECK RESUME ANALYSIS
# --------------------------------------------------

if "resume_analysis" not in st.session_state:

    st.warning(
        "⚠️ Please analyze a candidate's resume first."
    )

    st.info(
        "Go to **AI Resume Analyzer**, upload a resume, "
        "and click **Analyze My Resume**."
    )

    st.stop()


# --------------------------------------------------
# CANDIDATE
# --------------------------------------------------

st.subheader("👤 Candidate")

st.success(
    "Resume analysis loaded successfully."
)


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the complete job description below:",
    height=300,
    placeholder=(
        "Example:\n\n"
        "Python Developer Intern\n\n"
        "Requirements:\n"
        "- Python\n"
        "- SQL\n"
        "- REST APIs\n"
        "- Git\n"
        "- Database knowledge\n"
        "- Problem-solving skills"
    )
)


# --------------------------------------------------
# ANALYZE JOB MATCH
# --------------------------------------------------

if st.button(
    "🤖 Analyze Job Match",
    type="primary",
    use_container_width=True
):

    if not job_description.strip():

        st.error(
            "❌ Please enter a job description first."
        )

    else:

        resume_analysis = st.session_state[
            "resume_analysis"
        ]

        with st.spinner(
            "🔍 AI is comparing the candidate with the job..."
        ):

            try:

                result = match_candidate_to_job(
                    resume_analysis,
                    job_description
                )

                st.session_state[
                    "job_match_result"
                ] = result

                st.success(
                    "🎉 Job match analysis completed!"
                )

            except Exception as e:

                st.error(
                    "❌ Unable to analyze the job match."
                )

                st.exception(e)


# --------------------------------------------------
# DISPLAY RESULT
# --------------------------------------------------

if "job_match_result" in st.session_state:

    result = st.session_state[
        "job_match_result"
    ]

    st.divider()

    st.subheader("🎯 Job Match Result")


    # --------------------------------------------------
    # JOB + SCORE
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 💼 Job Role")

        st.info(
            result.get(
                "job_title",
                "Not available"
            )
        )

    with col2:

        match_score = float(
            result.get(
                "match_score",
                0
            )
        )

        st.markdown("### 📊 Match Score")

        st.metric(
            "Candidate Match",
            f"{match_score:.1f}%"
        )

        st.progress(
            int(match_score) / 100
        )


    # --------------------------------------------------
    # MATCHING SKILLS
    # --------------------------------------------------

    st.subheader("✅ Matching Skills")

    matching_skills = result.get(
        "matching_skills",
        []
    )

    if matching_skills:

        for skill in matching_skills:
            st.write(f"• {skill}")

    else:

        st.write(
            "No strong matching skills identified."
        )


    # --------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------

    st.subheader("⚠️ Missing / Required Skills")

    missing_skills = result.get(
        "missing_skills",
        []
    )

    if missing_skills:

        for skill in missing_skills:
            st.write(f"• {skill}")

    else:

        st.success(
            "No major skill gaps identified."
        )


    # --------------------------------------------------
    # RELEVANT EXPERIENCE
    # --------------------------------------------------

    st.subheader("💼 Relevant Candidate Experience")

    relevant_experience = result.get(
        "relevant_experience",
        []
    )

    if relevant_experience:

        for experience in relevant_experience:
            st.write(f"• {experience}")

    else:

        st.write(
            "No directly relevant experience identified."
        )


    # --------------------------------------------------
    # MATCH SUMMARY
    # --------------------------------------------------

    st.subheader("💡 Match Summary")

    st.write(
        result.get(
            "match_summary",
            "No summary available."
        )
    )


    # --------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------

    st.subheader("⭐ AI Recommendation")

    recommendation = result.get(
        "recommendation",
        "No recommendation available."
    )

    st.success(
        recommendation
    )