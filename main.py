"""
main.py
---------
End-to-end ML pipeline for student dropout risk prediction.

WHAT THIS FILE DOES:
1. Generates synthetic student data
2. Stores it in SQLite database
3. Trains a Logistic Regression model
4. Evaluates the model
5. Saves model + metadata for dashboard use

RUN THIS FIRST:
    python main.py
"""

import json
import sqlite3
import numpy as np
import pandas as pd
import pickle
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# --------------------------------------------------
# Load configuration
# --------------------------------------------------
with open("config.json", "r") as f:
    config = json.load(f)

DB_NAME = config["database"]["name"]
NUM_STUDENTS = config["data_generation"]["num_students"]
SEED = config["data_generation"]["random_seed"]
MODEL_PATH = config["model_storage"]["model_path"]

np.random.seed(SEED)


# --------------------------------------------------
# Generate synthetic student data
# --------------------------------------------------
def generate_student_data(n):
    """
    Generates realistic university student data.
    Dropout risk increases with:
    - Low attendance
    - Low academic scores
    - High course difficulty
    """

    attendance = np.random.uniform(40, 100, n)
    assignment_score = np.random.uniform(35, 100, n)
    midsem_score = np.random.uniform(30, 100, n)
    semester = np.random.randint(1, 9, n)
    course_difficulty = np.random.randint(1, 6, n)

    # Risk score logic
    risk_score = (
        (100 - attendance) * 0.4 +
        (100 - assignment_score) * 0.3 +
        (100 - midsem_score) * 0.2 +
        course_difficulty * 5
    )

    dropout_risk = (risk_score > 60).astype(int)

    return pd.DataFrame({
        "attendance": attendance,
        "assignment_score": assignment_score,
        "midsem_score": midsem_score,
        "semester": semester,
        "course_difficulty": course_difficulty,
        "dropout_risk": dropout_risk
    })


# --------------------------------------------------
# Store data in SQLite
# --------------------------------------------------
def store_data(df):
    conn = sqlite3.connect(DB_NAME)
    df.to_sql("students", conn, if_exists="replace", index=False)
    conn.close()


# --------------------------------------------------
# Load data from SQLite
# --------------------------------------------------
def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df


# --------------------------------------------------
# Train and evaluate model
# --------------------------------------------------
def train_model(df):
    X = df.drop("dropout_risk", axis=1)
    y = df["dropout_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config["model"]["test_size"],
        random_state=config["model"]["random_state"]
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 3),
        "precision": round(precision_score(y_test, y_pred), 3),
        "recall": round(recall_score(y_test, y_pred), 3),
        "f1_score": round(f1_score(y_test, y_pred), 3)
    }

    return model, metrics


# --------------------------------------------------
# Save model artifact
# --------------------------------------------------
def save_model(model, metrics):
    artifact = {
        "model": model,
        "metrics": metrics,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(artifact, f)


# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    print("\n--- STUDENT DROPOUT ML PIPELINE STARTED ---\n")

    print("Generating student data...")
    df = generate_student_data(NUM_STUDENTS)

    print("Saving data to database...")
    store_data(df)

    print("Loading data from database...")
    df_loaded = load_data()

    print("Training model...")
    model, metrics = train_model(df_loaded)

    print("\nModel Evaluation Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\nSaving model...")
    save_model(model, metrics)

    print("\nPipeline completed successfully.")
