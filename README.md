# 🎯 Moderator Score Adjustment App

The **Moderator Score Adjustment App** is a user-friendly tool built with [Streamlit](https://streamlit.io) to help automate the moderation of student assessment scores based on a configurable minimum threshold. It provides an interactive dashboard, adjusts scores where necessary, and supports export of the updated dataset.

## 🌟 Features

- 📥 Upload student assessment CSV files
- 🔍 Filter by session/section
- 📊 Select up to 3 score columns to compute total score
- ⚖️ Apply adjustment logic based on minimum threshold (e.g., 40 marks)
- 📈 Visual summary of results (Pie chart & Metrics)
- 🧾 Download moderated results as CSV
- 📉 Summary table of students who didn’t write assessments

## 🚀 Getting Started

### Installation

Clone the repository:

```bash
git clone https://github.com/your-username/moderator-score-adjustment-app.git
cd moderator-score-adjustment-app


moderator-score-adjustment-app/
│
├── .streamlit/
│   └── config.toml
│
├── app.py                    # Main application
├── requirements.txt
└── README.md

## 📌 How It Works
Upload your CSV file with student scores.

Filter by session, select the columns used to compute total score.

Set a threshold (e.g., 40). The app checks and boosts the total if it meets the logic.

The score to be adjusted is boosted and recalculated.

Visual dashboard and summary analytics help track overall performance.

Download the updated dataset once you're satisfied.

## 📊 Visuals
Here’s a glimpse of what the dashboard looks like:

🎨 Metrics cards for total candidates, adjusted scores, passes, fails, and non-attempts

🥧 Pie chart breakdown of result distribution

📋 Table of adjusted students

📈 Bar chart showing missing assessment counts

## ☁️ Deploy on Streamlit Cloud
To deploy:

Push this repo to GitHub

Visit Streamlit Cloud

Connect your GitHub, choose the repo and branch

Set the main file path to app.py and deploy 🎉

## 📄 Sample CSV Format
Your uploaded CSV file should include at least these columns:


Name	Section	Test 1	Test 2	Exam
Jane Doe	Cohort A	10	12	15
John Smith	Cohort B	15	NaN	20
...	...	...	...	...
## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss your idea.

## 📧 Contact
For questions, feedback, or suggestions, please contact [your-email@example.com].
