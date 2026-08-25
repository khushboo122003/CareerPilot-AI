import streamlit as st
import pdfplumber

from pages.utils.recruiter_shortlisting import (
    evaluate_candidate_for_job
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CareerPilot AI - Recruiter Shortlisting",
    page_icon="🧑‍💼",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧑‍💼 AI Recruiter Shortlisting")

st.write(
    "Evaluate multiple candidates against a specific job "
    "description using AI-powered resume screening."
)

st.divider()


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the complete job description",
    height=300,
    placeholder=(
        "Paste the job title, responsibilities, "
        "required skills, qualifications, and experience "
        "requirements here."
    )
)


# --------------------------------------------------
# CANDIDATE RESUMES
# --------------------------------------------------

st.subheader("📄 Candidate Resumes")

uploaded_files = st.file_uploader(
    "Upload candidate resumes",
    type=["pdf"],
    accept_multiple_files=True,
    help="You can upload multiple candidate PDF resumes."
)


# --------------------------------------------------
# DISPLAY UPLOADED CANDIDATES
# --------------------------------------------------

if uploaded_files:

    st.write(
        f"📌 {len(uploaded_files)} candidate(s) uploaded."
    )

    for file in uploaded_files:
        st.write(f"• {file.name}")


# --------------------------------------------------
# SHORTLIST BUTTON
# --------------------------------------------------

if st.button(
    "🤖 Evaluate & Shortlist Candidates",
    type="primary",
    use_container_width=True
):

    if not job_description.strip():

        st.warning(
            "⚠️ Please enter a job description first."
        )

    elif not uploaded_files:

        st.warning(
            "⚠️ Please upload at least one candidate resume."
        )

    else:

        results = []

        progress = st.progress(0)

        status = st.empty()

        total_candidates = len(
            uploaded_files
        )

        # --------------------------------------------------
        # PROCESS EACH CANDIDATE
        # --------------------------------------------------

        for index, uploaded_file in enumerate(
            uploaded_files
        ):

            status.write(
                f"🔍 Analyzing candidate "
                f"{index + 1} of {total_candidates}: "
                f"{uploaded_file.name}"
            )

            try:

                resume_text = ""

                # ------------------------------------------
                # EXTRACT RESUME TEXT
                # ------------------------------------------

                with pdfplumber.open(
                    uploaded_file
                ) as pdf:

                    for page in pdf.pages:

                        page_text = (
                            page.extract_text()
                        )

                        if page_text:

                            resume_text += (
                                page_text + "\n"
                            )

                # ------------------------------------------
                # CHECK TEXT
                # ------------------------------------------

                if not resume_text.strip():

                    results.append(
                        {
                            "candidate_name":
                                uploaded_file.name,

                            "match_score":
                                0,

                            "decision":
                                "NOT SUITABLE",

                            "matching_skills":
                                [],

                            "missing_skills":
                                [],

                            "relevant_experience":
                                [],

                            "reason":
                                "Could not extract text "
                                "from this PDF."
                        }
                    )

                else:

                    # --------------------------------------
                    # AI EVALUATION
                    # --------------------------------------

                    result = (
                        evaluate_candidate_for_job(
                            resume_text,
                            job_description
                        )
                    )

                    # Keep filename available
                    result["file_name"] = (
                        uploaded_file.name
                    )

                    results.append(result)
                    


            except Exception as e:

                results.append(
                    {
                        "candidate_name":
                            uploaded_file.name,

                        "match_score":
                            0,

                        "decision":
                            "ERROR",

                        "matching_skills":
                            [],

                        "missing_skills":
                            [],

                        "relevant_experience":
                            [],

                        "reason":
                            f"Unable to analyze "
                            f"this candidate: {str(e)}"
                    }
                )

            progress.progress(
                (index + 1) / total_candidates
            )

        status.success(
            "🎉 Candidate evaluation completed!"
        )

        st.session_state[
            "shortlisting_results"
        ] = results


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "shortlisting_results" in st.session_state:

    results = st.session_state[
        "shortlisting_results"
    ]

    st.divider()

    st.subheader(
        "📊 Candidate Screening Results"
    )

    # --------------------------------------------------
    # SORT BY MATCH SCORE
    # --------------------------------------------------

    results = sorted(
        results,
        key=lambda x: float(
            x.get("match_score", 0)
        ),
        reverse=True
    )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    shortlist_count = sum(
        1
        for result in results
        if result.get("decision")
        == "SHORTLIST"
    )

    maybe_count = sum(
        1
        for result in results
        if result.get("decision")
        == "MAYBE"
    )

    not_suitable_count = sum(
        1
        for result in results
        if result.get("decision")
        == "NOT SUITABLE"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🟢 Shortlisted",
            shortlist_count
        )

    with col2:

        st.metric(
            "🟡 Maybe",
            maybe_count
        )

    with col3:

        st.metric(
            "🔴 Not Suitable",
            not_suitable_count
        )


    st.divider()


    # --------------------------------------------------
    # INDIVIDUAL CANDIDATE RESULTS
    # --------------------------------------------------

    for rank, result in enumerate(
        results,
        start=1
    ):

        candidate_name = result.get(
            "candidate_name",
            "Unknown Candidate"
        )

        match_score = float(
            result.get(
                "match_score",
                0
            )
        )

        decision = result.get(
            "decision",
            "NOT SUITABLE"
        )

        # ----------------------------------------------
        # DECISION DISPLAY
        # ----------------------------------------------

        if decision == "SHORTLIST":

            decision_text = (
                "🟢 SHORTLIST"
            )

        elif decision == "MAYBE":

            decision_text = (
                "🟡 MAYBE"
            )

        else:

            decision_text = (
                "🔴 NOT SUITABLE"
            )

        with st.expander(
            f"#{rank} — {candidate_name} "
            f"| {match_score:.1f}% | "
            f"{decision_text}",
            expanded=(rank == 1)
        ):

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "📊 Match Score",
                    f"{match_score:.1f}%"
                )

            with col2:

                st.metric(
                    "🎯 Decision",
                    decision_text
                )


            st.progress(
                int(match_score) / 100
            )


            # ------------------------------------------
            # MATCHING SKILLS
            # ------------------------------------------

            st.markdown(
                "### ✅ Matching Skills"
            )

            matching_skills = result.get(
                "matching_skills",
                []
            )

            if matching_skills:

                for skill in matching_skills:

                    st.write(
                        f"• {skill}"
                    )

            else:

                st.write(
                    "No strong matching skills identified."
                )


            # ------------------------------------------
            # MISSING SKILLS
            # ------------------------------------------

            st.markdown(
                "### ⚠️ Missing Skills"
            )

            missing_skills = result.get(
                "missing_skills",
                []
            )

            if missing_skills:

                for skill in missing_skills:

                    st.write(
                        f"• {skill}"
                    )

            else:

                st.success(
                    "No major skill gaps identified."
                )


            # ------------------------------------------
            # RELEVANT EXPERIENCE
            # ------------------------------------------

            st.markdown(
                "### 💼 Relevant Experience"
            )

            relevant_experience = result.get(
                "relevant_experience",
                []
            )

            if relevant_experience:

                for experience in (
                    relevant_experience
                ):

                    st.write(
                        f"• {experience}"
                    )

            else:

                st.write(
                    "No directly relevant experience identified."
                )


            # ------------------------------------------
            # AI REASON
            # ------------------------------------------

            st.markdown(
                "### 💡 AI Screening Reason"
            )

            st.write(
                result.get(
                    "reason",
                    "No reason available."
                )
            )
# --------------------------------------------------
# DOWNLOAD SHORTLISTING REPORT
# --------------------------------------------------

if "shortlisting_results" in st.session_state:

    results = st.session_state["shortlisting_results"]

    report = "CAREERPILOT AI - RECRUITER SHORTLISTING REPORT\n"
    report += "=" * 60 + "\n\n"

    for index, result in enumerate(results, start=1):

        report += f"Candidate {index}\n"
        report += "-" * 40 + "\n"

        report += (
            f"Name: "
            f"{result.get('candidate_name', 'Unknown Candidate')}\n"
        )

        report += (
            f"Match Score: "
            f"{float(result.get('match_score', 0)):.1f}%\n"
        )

        report += (
            f"Decision: "
            f"{result.get('decision', 'NOT SUITABLE')}\n"
        )

        report += "\nMatching Skills:\n"

        for skill in result.get("matching_skills", []):
            report += f"- {skill}\n"

        report += "\nMissing Skills:\n"

        for skill in result.get("missing_skills", []):
            report += f"- {skill}\n"

        report += "\nRelevant Experience:\n"

        for experience in result.get(
            "relevant_experience", []
        ):
            report += f"- {experience}\n"

        report += "\nAI Screening Reason:\n"

        report += (
            result.get(
                "reason",
                "No reason available."
            )
            + "\n"
        )

        report += "\n" + "=" * 60 + "\n\n"


    st.download_button(
        label="📥 Download Shortlisting Report",
        data=report,
        file_name="CareerPilot_AI_Shortlisting_Report.txt",
        mime="text/plain",
        use_container_width=True
    )