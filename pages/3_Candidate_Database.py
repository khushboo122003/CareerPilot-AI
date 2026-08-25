import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Candidate Database",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Candidate Database")

conn = sqlite3.connect("careerpilot.db")

df = pd.read_sql_query(
    "SELECT * FROM candidates",
    conn
)

st.dataframe(df, use_container_width=True)
