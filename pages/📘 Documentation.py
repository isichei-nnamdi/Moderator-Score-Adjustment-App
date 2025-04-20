import streamlit as st

st.set_page_config(page_title="📘 Moderator Score Adjustment App - Documentation", layout="wide")

st.title("📘 Moderator Score Adjustment App - Documentation")

st.markdown("""
## 🎯 Overview
The **Moderator Score Adjustment App** is designed to help faculty and course moderators seamlessly adjust candidate scores for assessments based on a predefined threshold. It ensures fairness and consistency in scoring, especially for borderline pass cases. The app allows moderators to update scores within reasonable limits, providing a transparent record of adjustments made.

---

## 🔄 Workflow

### 1. **File Upload**
- Accepts a `.csv` file containing the assessment results.
- The file must contain at least:
  - A **'Section'** column for filtering by session/cohort.
  - At least **2-3 columns** with assessment scores (e.g., CA1, CA2, Exam).

### 2. **Session Selection**
- Displays a list of unique values from the **'Section'** column.
- Moderator selects a cohort/session to work on.

### 3. **Score Column Selection**
- Moderator selects up to **3 score columns** that contribute to the total score.
- One of these columns will be designated as the **adjustable column** (e.g., Exam).

### 4. **Threshold Setting**
- Moderator sets the minimum acceptable score (e.g., 40).
- Students whose total score is **below the threshold** but close enough (e.g., between 37 and 39) may have their score adjusted.

---

## 🛠️ Adjustment Logic

- **Calculation**:
  - The app computes the total score by summing the selected score columns.
  - If a student's total score is **below the threshold** (e.g., 39) but greater than or equal to a predefined lower threshold (e.g., 37), the app adjusts the **last selected score column**.
  - The adjustment is capped so that no score exceeds 100.
  - The app displays a note in the adjusted column, e.g., "Adjusted by X."

---

## 📊 Outputs

### 📋 Updated Table
- Displays a table of all students with their updated total scores and adjustment notes.

### 📈 Dashboard Summary
- The app presents a summary dashboard that shows:
  - **Adjusted Students**: Candidates whose scores were adjusted to meet the threshold.
  - **Pass**: Candidates who passed without needing adjustments.
  - **Fail**: Candidates who failed and could not be adjusted.
  - **Assessment Not Taken**: Candidates with missing scores in any of the selected columns.

### 🧾 Comments Column
- **Adjusted**: Scores modified to meet the threshold.
- **Pass**: Students who passed without adjustments.
- **Fail**: Students who failed and were not adjusted.
- **Assessment not taken**: Students with missing assessment data.

### 📉 Missing Scores Table
- Lists each assessment and the number of students who did not take it.

---

## 📥 Downloadable Result

- After review, moderators can download the updated CSV file with the adjusted scores.
- The downloaded file will exclude internal adjustment notes, showing only the final moderated results.

---

## ⚙️ Example Use Case

### Example Column Setup

| Matric No | Section | CA1 | CA2 | Exam |
|-----------|---------|-----|-----|------|
| AB123     | 2023A   | 10  | 10  | 15   |
| XY234     | 2023A   | 15  | 15  | 10   |
| CD456     | 2023B   | 20  |     | 15   |

For this example:
1. The moderator uploads the result file.
2. The **Section "2023A"** is selected for moderation.
3. The **CA1, CA2, and Exam** columns are selected for total score calculation.
4. The **threshold of 40** is set.
5. The **Exam** column is selected for adjustments.
6. Students with a total score of 39.5 or below are adjusted by adding the shortfall to their Exam score.

---

## ❗ Error Handling
- If selected columns or sessions do not match the expected structure, the app will display user-friendly error messages and guide the user to correct their selection.

---

## 📂 How It Works

### 1. **Upload CSV File**
- Click the file uploader and upload your result sheet (CSV format).
- Ensure the sheet contains a **'Section'** column for filtering by session/cohort.

### 2. **Session Selection**
- From the dropdown, choose the specific session (e.g., cohort or class) to work on.

### 3. **Score Column Selection**
- Select **2 or 3 score columns** that contribute to the total score (e.g., CA, Exam, Project).

### 4. **Set Minimum Threshold**
- Enter the minimum acceptable score (typically 40). This sets the cutoff for adjustments.

### 5. **Column to Adjust**
- Choose which column among the selected scores should be updated to meet the threshold.

---

## 📈 Charts & Tables

- **Pie Chart**: Visualizes the distribution of Pass/Fail/Adjusted/Not Taken.
- **Missing Scores Table**: Shows how many students didn’t take each assessment.
- **Adjusted Students Table**: Filters only those who were adjusted.

---

## 📞 Contact / Support
For help or feature requests, please contact: **augustus@miva.university**

Happy moderating! 🎓
""")

st.markdown(
    """
    <style>
    .main-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f0f2f6;
        padding: 10px 0;
        font-size: 13px;
        text-align: center;
        color: #444;
        border-top: 1px solid #ddd;
        z-index: 9999;
    }
    .main-footer a {
        text-decoration: none;
        margin: 0 8px;
        color: #0366d6;
    }
    .main-footer a:hover {
        text-decoration: underline;
    }
    .footer-icons {
        margin-top: 5px;
    }
    .footer-icons a {
        text-decoration: none;
        color: #444;
        margin: 0 10px;
        font-size: 16px;
    }
    </style>
    <div class="main-footer">
        Design, Developed and Deployed by <strong>Nnamdi A. Isichei</strong> &copy; 2025 <br/>
        <div class="footer-icons">
            <a href="https://github.com/isichei-nnamdi" target="_blank">GitHub</a> |
            <a href="https://www.linkedin.com/in/nnamdi-isichei/" target="_blank">LinkedIn</a> |
            <a href="mailto:augustus@miva.university" target="_blank">Email</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <style>
    .sidebar-footer {
        margin-top: 30px;
        font-size: 12px;
        color: #666;
        text-align: center;
    }
    .sidebar-footer a {
        text-decoration: none;
        color: #0366d6;
        margin: 0 4px;
    }
    .sidebar-footer a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="sidebar-footer">
        &copy; 2025 <br/>
        <strong>Nnamdi A. Isichei</strong><br/>
        <a href="https://github.com/isichei-nnamdi" target="_blank">GitHub</a> |
        <a href="https://www.linkedin.com/in/nnamdi-isichei/" target="_blank">LinkedIn</a> |
        <a href="mailto:augustus@miva.university" target="_blank">Email</a>
    </div>
    """,
    unsafe_allow_html=True
)