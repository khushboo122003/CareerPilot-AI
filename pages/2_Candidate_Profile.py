import streamlit as st
import sqlite3
# Connect to database
conn = sqlite3.connect("careerpilot.db", check_same_thread=False)
cursor = conn.cursor()

st.set_page_config(
    page_title="Candidate Profile",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Candidate Profile")

st.write("Fill in the candidate details below.")
with st.form("candidate_form"):

    name = st.text_input("Candidate Name")

    email = st.text_input("Email")

    phone = st.text_input("Phone Number")

    college = st.text_input("College")

    skills = st.text_area("Skills")

    submit = st.form_submit_button("Save Candidate")

if submit:

    cursor.execute(
        """
        INSERT INTO candidates (name, email, phone, college, skills)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, phone, college, skills)
    )

    conn.commit()

    st.success("Candidate Saved Successfully!")
 