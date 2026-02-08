# Future Plans

================

This document outlines **small, realistic, incremental improvements** to the current **student dropout risk prediction pipeline**.
The goal is to improve **data reliability, model clarity, and decision usefulness** without turning the project into an over-engineered system.

Each task is designed to be achievable in **~15 minutes per day**, enabling consistent and low-stress progress.

---

## Current Pipeline (Baseline)

Right now, the system does:

* **Extract**: Generate reproducible student data using Python scripts
* **Transform**: Clean and encode academic and engagement features
* **Load**: Store student records and model artifacts in a local database
* **Train**: Train multiple ML models and select the best one
* **Serve**: Predict dropout risk via an interactive dashboard

This is a solid foundation. The improvements below build on this **without increasing complexity**.

---

## Week 1 — Data Quality & ETL Improvements

**Goal:** Make the data pipeline more reliable and easier to inspect.

Small changes:

* Add a **data validation step**:

  * Check for missing or invalid values (attendance, GPA, engagement, label)
  * Print warnings for dropped or corrected rows

* Add a **simple dataset summary log**:

  * Total number of students
  * Number of students per course / department
  * Dropout vs non-dropout distribution

* Add a **“last updated” timestamp** for student records in the database

* Add a CLI option:

  ```bash
  python scripts/train.py --show-stats
  ```

  to display dataset statistics in the terminal

Why this helps:

* Improves trust in training data
* Makes ETL steps easier to explain in reports
* Helps catch data issues early

---

## Week 2 — Better Feature Engineering (Still Simple)

**Goal:** Improve feature quality while keeping transformations interpretable.

Small changes:

* Bucket continuous features:

  * Attendance → Low / Medium / High
  * Engagement score → Low / Medium / High

* Add derived features:

  * `is_low_attendance`
  * `is_first_year_student`
  * `is_academic_risk` (based on GPA threshold)

* Store **feature versioning** in model metadata:

  ```json
  "feature_version": "v2"
  ```

* Log the list of features used during training (file or DB)

Why this helps:

* Demonstrates feature engineering clearly
* Improves model interpretability
* Keeps transformations explainable to non-technical audiences

---

## Week 3 — Training & Evaluation Improvements

**Goal:** Make model comparison and evaluation more transparent.

Small changes:

* Store **metrics for all trained models**, not just the best one:

  * Accuracy
  * Precision
  * Recall
  * F1-score

* Add a **model comparison table** in the dashboard

* Add **3-fold cross-validation** for one model (e.g., Random Forest)

* Add a CLI option:

  ```bash
  python scripts/train.py --list-models
  ```

  to show all trained models and their metrics

Why this helps:

* Reflects a realistic ML workflow
* Improves evaluation credibility
* Helps explain model selection decisions

---

## Week 4 — Prediction & UX Improvements

**Goal:** Improve how predictions are presented and understood.

Small changes:

* Add **prediction explanations**:

  * “High dropout risk due to low attendance and engagement”

* Add **confidence labels**:

  * High / Medium / Low confidence

* Add dashboard filters:

  * Show only **High Risk** students
  * Filter by course or semester

* Add sorting options:

  * By risk probability
  * By attendance
  * By academic performance

Why this helps:

* Improves interpretability and trust
* Makes the dashboard more useful for administrators
* Enhances demo and presentation quality

---

## Small Technical Cleanup Tasks (Any Time)

These can be done whenever you want quick, low-effort improvements:

* Add docstrings to all major functions
* Improve variable and function naming
* Add inline comments to complex logic
* Add `requirements.txt`
* Add graceful error handling for:

  * Empty database
  * Missing trained model
  * Invalid dashboard inputs

---

## Long-Term (Optional, After One Month)

Only if you want to extend the project further:

* Add **time-based tracking** (semester-wise risk trends)
* Add **simple feedback input**:

  * “Was this prediction helpful? Yes / No”
* Store feedback for future analysis
* Add a **small synthetic data expander** to simulate larger cohorts

---

## Guiding Principles

* Keep changes **small and reversible**
* Prefer **clarity over complexity**
* Improve **one pipeline stage at a time**
* Always keep the project:

  * Easy to run
  * Easy to explain
  * Easy to maintain

---

## Summary

Over one month, with **~15 minutes per day**, this project can evolve from:

> A basic academic ML prediction system
> to
> A clean, realistic, and well-structured student risk prediction pipeline

— without ever becoming fragile or over-engineered.
