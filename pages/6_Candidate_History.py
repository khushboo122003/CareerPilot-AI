import streamlit as st
import sqlite3
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Candidate History | CareerPilot AI",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# DATABASE
# ============================================================

DB_PATH = "careerpilot.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# GET ALL CANDIDATES
# ============================================================

def get_candidates():

    conn = get_connection()

    try:
        df = pd.read_sql_query(
            """
            SELECT
                id,
                name,
                email
            FROM candidates
            ORDER BY id DESC
            """,
            conn
        )

    except Exception:
        df = pd.DataFrame(
            columns=["id", "name", "email"]
        )

    finally:
        conn.close()

    return df


# ============================================================
# GET RECRUITER HISTORY
# ============================================================

def get_candidate_history(candidate_id):

    conn = get_connection()

    try:
        df = pd.read_sql_query(
            """
            SELECT
                technical_skills,
                communication,
                problem_solving,
                confidence,
                decision,
                comments,
                created_at
            FROM recruiter_feedback
            WHERE candidate_id = ?
            ORDER BY created_at DESC
            """,
            conn,
            params=(candidate_id,)
        )

    except Exception:
        df = pd.DataFrame()

    finally:
        conn.close()

    return df


# ============================================================
# PAGE HEADER
# ============================================================

st.title("📋 Candidate History")

st.write(
    "View previous recruiter evaluations and hiring decisions "
    "for candidates across recruitment cycles."
)

st.divider()


# ============================================================
# LOAD CANDIDATES
# ============================================================

candidates = get_candidates()


if candidates.empty:

    st.warning("No candidates found.")

    st.info(
        "Please add a candidate first from the Candidate Profile page."
    )

    st.stop()


# ============================================================
# SELECT CANDIDATE
# ============================================================

st.subheader("👤 Select Candidate")

candidate_names = candidates["name"].fillna(
    "Unknown Candidate"
).tolist()

selected_name = st.selectbox(
    "Choose a candidate",
    candidate_names
)


selected_candidate = candidates[
    candidates["name"] == selected_name
].iloc[0]


candidate_id = int(selected_candidate["id"])


st.divider()


# ============================================================
# CANDIDATE PROFILE
# ============================================================

st.subheader("👤 Candidate Profile")


col1, col2, col3 = st.columns(3)


with col1:

    st.caption("Candidate")

    st.markdown(
        f"### {selected_candidate['name']}"
    )


with col2:

    st.caption("Candidate ID")

    st.markdown(
        f"### #{candidate_id}"
    )


# Get history before showing status
history = get_candidate_history(candidate_id)


with col3:

    st.caption("Status")

    if history.empty:

        st.markdown("### No History")

    else:

        st.markdown("### History Available")


# Email
email = selected_candidate["email"]

if pd.notna(email) and str(email).strip():

    st.write(f"📧 {email}")


st.divider()


# ============================================================
# RECRUITER EVALUATION HISTORY
# ============================================================

st.subheader("📊 Recruiter Evaluation History")


if history.empty:

    st.info(
        "No recruiter evaluations have been recorded "
        "for this candidate yet."
    )

else:

    # ========================================================
    # LATEST EVALUATION
    # ========================================================

    latest = history.iloc[0]


    technical = latest["technical_skills"]
    communication = latest["communication"]
    problem_solving = latest["problem_solving"]
    confidence = latest["confidence"]


    # ========================================================
    # SCORE CARDS
    # ========================================================

    st.markdown("### ⭐ Latest Evaluation")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        if pd.notna(technical):

            st.metric(
                "Technical Skills",
                f"{technical}/5"
            )

        else:

            st.metric(
                "Technical Skills",
                "N/A"
            )


    with col2:

        if pd.notna(communication):

            st.metric(
                "Communication",
                f"{communication}/5"
            )

        else:

            st.metric(
                "Communication",
                "N/A"
            )


    with col3:

        if pd.notna(problem_solving):

            st.metric(
                "Problem Solving",
                f"{problem_solving}/5"
            )

        else:

            st.metric(
                "Problem Solving",
                "N/A"
            )


    with col4:

        if pd.notna(confidence):

            st.metric(
                "Confidence",
                f"{confidence}/5"
            )

        else:

            st.metric(
                "Confidence",
                "N/A"
            )


    # ========================================================
    # OVERALL SCORE
    # ========================================================

    scores = []

    for value in [
        technical,
        communication,
        problem_solving,
        confidence
    ]:

        if pd.notna(value):

            try:

                scores.append(
                    float(value)
                )

            except:

                pass


    if scores:

        overall_score = sum(scores) / len(scores)

    else:

        overall_score = 0


    st.write("")


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Overall Score",
            f"{overall_score:.1f}/5"
        )


    # ========================================================
    # LATEST DECISION
    # ========================================================

    decision = latest["decision"]


    with col2:

        st.write("**Latest Hiring Decision**")


        if decision == "Hire":

            st.success("✅ Hire")

        elif decision == "Hold":

            st.warning("⏸️ Hold")

        elif decision == "Reject":

            st.error("❌ Reject")

        else:

            st.info(
                str(decision)
            )


    st.divider()


    # ========================================================
    # RECRUITER COMMENTS
    # ========================================================

    comments = latest["comments"]


    if pd.notna(comments) and str(comments).strip():

        st.subheader("💬 Recruiter Comments")

        st.info(
            str(comments)
        )


    # ========================================================
    # COMPLETE HISTORY
    # ========================================================

    st.subheader("📚 Complete Evaluation History")


    display_history = history.copy()


    display_history.columns = [
        "Technical Skills",
        "Communication",
        "Problem Solving",
        "Confidence",
        "Decision",
        "Comments",
        "Date"
    ]


    st.dataframe(
        display_history,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CareerPilot AI • Candidate Intelligence & Recruitment Management"
)