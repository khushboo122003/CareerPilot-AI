import streamlit as st

from pages.utils.recommendation_engine import generate_recommendation


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CareerPilot AI - AI Recommendations",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎯 AI Career Recommendations")

st.write(
    "Get a personalized career recommendation based on "
    "your resume and AI analysis."
)

st.divider()


# --------------------------------------------------
# CHECK RESUME ANALYSIS
# --------------------------------------------------

if "resume_analysis" not in st.session_state:

    st.warning(
        "⚠️ Please upload and analyze your resume first."
    )

    st.info(
        "Go to the AI Resume Analyzer, upload your resume, "
        "and click **Analyze My Resume**."
    )

    st.stop()


# --------------------------------------------------
# GENERATE RECOMMENDATION
# --------------------------------------------------

analysis = st.session_state["resume_analysis"]


if st.button(
    "🤖 Generate My Career Recommendation",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "🔍 AI is finding the best career match for you..."
    ):

        try:

            recommendation = generate_recommendation(
                analysis
            )

            st.session_state[
                "career_recommendation"
            ] = recommendation

            st.success(
                "🎉 Personalized career recommendation generated!"
            )

        except Exception as e:

            st.error(
                "❌ Unable to generate recommendation."
            )

            st.exception(e)


# --------------------------------------------------
# DISPLAY RECOMMENDATION
# --------------------------------------------------

if "career_recommendation" in st.session_state:

    recommendation = st.session_state[
        "career_recommendation"
    ]

    st.divider()

    st.subheader("🎯 Your Best-Fit Career")

    # --------------------------------------------------
    # BEST FIT ROLE
    # --------------------------------------------------

    st.markdown(
        f"""
        ### 💼 {recommendation.get("best_fit_role", "Not available")}

        **Match Score:**
        {recommendation.get("match_score", 0):.1f}%
        """
    )

    st.progress(
        int(
            recommendation.get(
                "match_score",
                0
            )
        ) / 100
    )

    # --------------------------------------------------
    # CAREER DIRECTION
    # --------------------------------------------------

    st.subheader("🧭 Career Direction")

    st.write(
        recommendation.get(
            "career_direction",
            "No career direction available."
        )
    )

    # --------------------------------------------------
    # MATCHING SKILLS
    # --------------------------------------------------

    st.subheader("✅ Matching Skills")

    matching_skills = recommendation.get(
        "matching_skills",
        []
    )

    if matching_skills:

        for skill in matching_skills:

            st.write(f"• {skill}")

    else:

        st.write(
            "No matching skills identified."
        )

    # --------------------------------------------------
    # SKILLS TO IMPROVE
    # --------------------------------------------------

    st.subheader("📚 Skills to Improve")

    skills_to_improve = recommendation.get(
        "skills_to_improve",
        []
    )

    if skills_to_improve:

        for skill in skills_to_improve:

            st.write(f"• {skill}")

    else:

        st.write(
            "No major skill gaps identified."
        )

    # --------------------------------------------------
    # WHY THIS ROLE
    # --------------------------------------------------

    st.subheader("💡 Why This Role Fits You")

    st.write(
        recommendation.get(
            "why_this_role",
            "No explanation available."
        )
    )

    # --------------------------------------------------
    # RECOMMENDED ACTIONS
    # --------------------------------------------------

    st.subheader("🚀 Recommended Next Steps")

    actions = recommendation.get(
        "recommended_actions",
        []
    )

    for index, action in enumerate(
        actions,
        start=1
    ):

        st.write(
            f"**{index}.** {action}"
        )