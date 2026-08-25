import streamlit as st
import pdfplumber
import re
import json
from pages.utils.ai_analyzer import analyze_resume

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CareerPilot AI - Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
.resume-header {
    text-align: center;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
}

.resume-header h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

.resume-header p {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="resume-header">
    <h1>📄 AI Resume Analyzer</h1>
    <p>Upload your resume and get personalized AI-powered career insights</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 20px;
    color: #777;
    margin-bottom: 30px;
}

.upload-box {
    padding: 30px;
    border-radius: 18px;
    border: 1px solid #ddd;
    background-color: #fafafa;
    margin-bottom: 25px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 15px;
}

.score-box {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    text-align: center;
}

.result-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #f8f9fa;
    border: 1px solid #e5e5e5;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🚀 CareerPilot AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Resume & Career Analyzer</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload your resume and let CareerPilot AI analyze your skills, "
    "career opportunities, missing skills, and interview preparation."
)

st.divider()


# --------------------------------------------------
# UPLOAD SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📄 Upload Your Resume</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="upload-box">'
    '<h3>Upload your latest resume</h3>'
    '<p>Supported format: PDF</p>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
">
    <h2>📤 Upload Your Resume</h2>
    <p style="font-size: 17px;">
        Upload your PDF resume and let CareerPilot AI analyze your career profile.
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"],
    help="Upload a PDF resume for AI-powered analysis."
)

# --------------------------------------------------
# FILE INFORMATION
# --------------------------------------------------

if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.write("📄 **File:**", uploaded_file.name)

    with col2:
        size_kb = uploaded_file.size / 1024
        st.write(f"📦 **Size:** {size_kb:.1f} KB")

    st.divider()

    # --------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------

    if st.button(
        "🤖 Analyze My Resume",
        type="primary",
        use_container_width=True
    ):

        with st.spinner("🔍 CareerPilot AI is analyzing your resume..."):

            try:

                resume_text = ""

                # Extract text from PDF
                with pdfplumber.open(uploaded_file) as pdf:

                    for page in pdf.pages:

                        page_text = page.extract_text()

                        if page_text:
                            resume_text += page_text + "\n"

                # Check extracted text
                if not resume_text.strip():

                    st.error(
                        "❌ We couldn't extract text from this PDF. "
                        "Please upload a text-based PDF."
                    )

                else:

                    # AI analysis
                    analysis = analyze_resume(resume_text)

                    st.session_state["resume_analysis"] = analysis
                    st.session_state["resume_text"] = resume_text

                    st.success("🎉 Resume analysis completed!")

            except Exception as e:

                st.error("❌ Something went wrong while analyzing your resume.")

                st.exception(e)


# --------------------------------------------------
# DISPLAY AI RESULTS
# --------------------------------------------------

if "resume_analysis" in st.session_state:

    analysis = st.session_state["resume_analysis"]

    st.divider()

    st.markdown(
        '<div class="section-title">🤖 Your CareerPilot AI Report</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Personalized insights generated from your uploaded resume."
    )

    # --------------------------------------------------
    # AI ANALYSIS
    # --------------------------------------------------

    st.markdown(
        """
        <div class="result-box">
        """,
        unsafe_allow_html=True
    )

    st.json(analysis)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # CAREER ACTION CARDS
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">🎯 Your Next Career Steps</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="result-box">
            <h3>💼 Career Opportunities</h3>
            <p>Explore job roles that match your current skills and experience.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="result-box">
            <h3>📚 Skill Development</h3>
            <p>Identify missing skills and build a focused learning roadmap.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="result-box">
            <h3>🎤 Interview Preparation</h3>
            <p>Practice technical and HR questions based on your resume.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # --------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">📥 Save Your Career Report</div>',
        unsafe_allow_html=True
    )

    st.download_button(
        label="📄 Download AI Career Report",
        data=json.dumps(analysis, indent=4),
        file_name="CareerPilot_AI_Resume_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------
    # NEXT STEPS
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">🎯 What You Can Do Next</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "💼 **Explore Job Roles**\n\n"
            "Find roles that match your current skills."
        )

    with col2:

        st.info(
            "📚 **Build Missing Skills**\n\n"
            "Follow the recommended learning roadmap."
        )

    with col3:

        st.info(
            "🎤 **Prepare for Interviews**\n\n"
            "Practice technical and HR questions."
        )

else:

    st.info(
        "👆 Upload your resume above and click "
        "**Analyze My Resume** to begin."
    )