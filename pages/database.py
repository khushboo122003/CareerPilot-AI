import sqlite3

# Connect to database
conn = sqlite3.connect("careerpilot.db", check_same_thread=False)

# Create cursor
cursor = conn.cursor()

# Create Candidate Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    college TEXT,
    skills TEXT
)
""")

# Create Recruiter Feedback Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS recruiter_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER,
    technical_skills INTEGER,
    communication INTEGER,
    problem_solving INTEGER,
    confidence INTEGER,
    decision TEXT,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id)
)
""")

conn.commit()
# --------------------------------------------------
# AI JOB SCREENING RESULTS
# --------------------------------------------------

conn = sqlite3.connect(
    "careerpilot.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS job_screening_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    match_score REAL,
    decision TEXT,
    matching_skills TEXT,
    missing_skills TEXT,
    relevant_experience TEXT,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

conn.close()