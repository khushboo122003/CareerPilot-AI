import streamlit as st

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CAREERPILOT AI NAVIGATION
# --------------------------------------------------

pages = {
    "CareerPilot AI": [
        st.Page(
            "pages/1_Dashboard.py",
            title="Dashboard",
            icon="🏠"
        ),
        st.Page(
            "pages/2_Candidate_Profile.py",
            title="Candidate Profile",
            icon="👤"
        ),
        st.Page(
            "pages/3_View_Candidates.py",
            title="View Candidates",
            icon="👥"
        ),
        st.Page(
            "pages/3_Candidate_Database.py",
            title="Candidate Database",
            icon="🗄️"
        ),
        st.Page(
            "pages/6_Candidate_History.py",
            title="Candidate History",
            icon="📋"
        ),
        st.Page(
            "pages/7_AI_Recommendations.py",
            title="AI Recommendations",
            icon="🤖"
        ),
        st.Page(
            "pages/8_Job_Matcher.py",
            title="Job Matcher",
            icon="🎯"
        ),
        st.Page(
            "pages/9_Interview_Generator.py",
            title="Interview Generator",
            icon="🎤"
        ),
        st.Page(
            "pages/10_Recruiter_Shortlisting.py",
            title="Recruiter Shortlisting",
            icon="👥"
        ),
        st.Page(
            "pages/11_Candidate_Interview.py",
            title="Candidate Interview",
            icon="💼"
        ),
    ]
}

pg = st.navigation(pages)

pg.run()