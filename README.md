# 📈 Video Potential Index (VPI) Diagnostic Report Tool

This Streamlit application provides a sophisticated diagnostic report for video content, moving beyond simple weighted scores to predict viral potential using a tiered, algorithmic-centric methodology (VBS/QSS Gates).

The tool classifies video performance into four distinct VPI Tiers, offering precise, actionable feedback on where a video succeeded or failed relative to platform algorithms.

---

## ✨ Key Features

* **4-Tier VPI Prediction:** Classifies video potential into four tiers (Champion, High Potential, Lottery Ticket, Self-Sabotage).
* **Gate-Based Logic:** Uses a mandatory two-gate system (VBS and QSS-1) to determine viral trajectory.
* **Actionable Diagnosis:** Distinguishes between **Internal Failures** (content flaws) and **External Failures** (distribution/timing issues).
* **Critical ±1 Tolerance:** Prevents misclassifying near-perfect viral hits.
* **Complete Breakdown:** Displays all 15 categories and underlying checklist points.

---

## 🧠 The VPI Tier System: Methodology

The VPI Tier system evaluates content using three core metrics. Tier placement follows sequential mandatory gates.

### 1. Core Metrics

| Metric                          | Score Range | Focus                  | Role                        |
| ------------------------------- | ----------- | ---------------------- | --------------------------- |
| **VBS** (Viral Base Score)      | 0–8         | Topic & Connection     | **Gate 1:** Must be ≥ 7/8   |
| **QSS-1** (Critical Retention)  | 0–13        | Hook & Loop Mechanics  | **Gate 2:** Must be ≥ 10/13 |
| **QSS-Total** (Overall Quality) | 0–51        | Execution & Production | Determines Tier 1–3         |

### 2. VPI Tier Logic

| VPI Tier                      | Logic                                        | Diagnosis                                                 |
| ----------------------------- | -------------------------------------------- | --------------------------------------------------------- |
| **Tier 1: 🏆 Viral Champion** | VBS = 8/8 AND QSS-1 ≥ 10 AND QSS-Total ≥ 80% | Fully optimized. If it fails, it’s external (CTR/timing). |
| **Tier 2: ✨ High Potential**  | VBS ≥ 7 AND QSS-1 ≥ 10 AND QSS-Total ≥ 70%   | Strong contender with minor flaws.                        |
| **Tier 3: 💡 Lottery Ticket** | VBS ≥ 7 AND QSS-1 ≥ 10 AND QSS-Total < 70%   | Outlier success, non-repeatable.                          |
| **Tier 4: 🚫 Self-Sabotage**  | VBS < 7 OR QSS-1 < 10                        | Fatal flaw. Topic or hook must be fixed.                  |

---

## 🚀 Usage

### Prerequisites

Install dependencies:

```bash
pip install streamlit pandas
```

### Files Required

Ensure these two files are in the same directory:

1. `app.py` – Streamlit app containing `display_final_vpi_report`.
2. `scoring.py` – Contains scoring logic and constants.

Required constants inside `scoring.py`:

```python
VBS_PERFECTION_THRESHOLD = 1.0
QSS_HIGH_QUALITY_THRESHOLD = 0.70
QSS_1_RETENTION_THRESHOLD = 0.80
VBS_MIN_PASS_RAW = 7
QSS_1_MIN_PASS_RAW = 10
```

### Run the Application

```bash
streamlit run app/main.py
```

### Generating a Report

The application expects:

* `full_result`: dictionary containing raw scores for all checklist categories.
* `total_frames`: total video length (e.g., 25 seconds).

Example (internal logic):

```python
# display_final_vpi_report(full_result, total_frames)
```

This function calculates:

* VBS
* QSS-1
* QSS-Total

And renders the complete tier-based VPI diagnostic report in the Streamlit interface.

---

## 📌 Summary

This README documents the complete functionality of the VPI Diagnostic Tool—from methodology to running the app—helping you understand, modify, or extend the model for advanced content analysis and algorithm-friendly scoring.
