"""
dashboard.py
-------------
Streamlit dashboard for:
1. Viewing student dataset
2. Viewing model performance
3. Predicting dropout risk

RUN USING:
    streamlit run dashboard.py
"""

import streamlit as st
import sqlite3
import pandas as pd
import pickle
import json
import os


# --------------------------------------------------
# Load configuration
# --------------------------------------------------
with open("config.json", "r") as f:
    config = json.load(f)

DB_NAME = config["database"]["name"]
MODEL_PATH = config["model_storage"]["model_path"]


# --------------------------------------------------
# Safety checks
# --------------------------------------------------
if not os.path.exists(MODEL_PATH):
    st.error("❌ Model not found. Please run `python main.py` first.")
    st.stop()


# --------------------------------------------------
# Load model
# --------------------------------------------------
with open(MODEL_PATH, "rb") as f:
    artifact = pickle.load(f)

model = artifact["model"]
metrics = artifact["metrics"]
trained_at = artifact["trained_at"]


# --------------------------------------------------
# Load student data
# --------------------------------------------------
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql("SELECT * FROM students", conn)
conn.close()


# --------------------------------------------------
# UI
# --------------------------------------------------
st.set_page_config(page_title="Student Dropout Risk", layout="centered")

st.title("🎓 Student Dropout Risk Prediction")

st.subheader("Model Details")
st.write(f"**Last Trained:** {trained_at}")
st.json(metrics)

st.divider()

st.subheader("Student Dataset (Preview)")
st.dataframe(df.head(10))

st.divider()

st.subheader("Predict Dropout Risk")

attendance = st.slider("Attendance Percentage", 0.0, 100.0, 75.0)
assignment = st.slider("Assignment Average Score", 0.0, 100.0, 70.0)
midsem = st.slider("Mid-Semester Exam Score", 0.0, 100.0, 65.0)
semester = st.selectbox("Semester Number", [1,2,3,4,5,6,7,8])
difficulty = st.selectbox("Course Difficulty (1 = Easy, 5 = Hard)", [1,2,3,4,5])

if st.button("Predict Risk"):
    input_df = pd.DataFrame([{
        "attendance": attendance,
        "assignment_score": assignment,
        "midsem_score": midsem,
        "semester": semester,
        "course_difficulty": difficulty
    }])

    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.error("⚠️ At Risk of Dropout")
    else:
        st.success("✅ Not At Risk")
