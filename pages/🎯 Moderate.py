import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO
import plotly.express as px

st.set_page_config(page_title="Score Adjustment App", layout="centered")
st.title("🎯 Moderator Score Adjustment App")

uploaded_file = st.file_uploader("📤 Step 1: Upload CSV File", type="csv")

original_filename = uploaded_file.name if uploaded_file else "uploaded_file.csv"
base_name, ext = os.path.splitext(original_filename)
new_filename = f"{base_name}_updated{ext}"

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("✅ File uploaded successfully!")

    # Display unique sessions for selection
    sessions = df["Section"].dropna().unique()
    selected_session = st.selectbox("Step 2: Select a Session to Filter", sorted(sessions))

    score_columns = st.multiselect("Step 3: Select columns used for total score calculation:", df.columns, max_selections=3)

    column_to_be_adjusted = st.selectbox("Select the column to be updated", sorted(score_columns))

    threshold = st.number_input("Step 4: Set the Minimum Threshold Score", min_value=0, value=40)

    if score_columns and selected_session and threshold is not None:
        st.subheader("Processed Results")

        # Filter dataframe based on selected session
        session_df = df[df["Section"] == selected_session].copy()

        # Keep only rows that have values in all selected score_columns
        valid_rows_mask = session_df[score_columns].notna().all(axis=1)
        valid_df = session_df[valid_rows_mask].copy()

        def adjust_row(row):
            values = row[score_columns].fillna(0)
            total = values.sum()
            if (total >= threshold and total < 40):
                shortfall = 40 - total
                values.iloc[-1] = min(values.iloc[-1] + shortfall, 40)  # Cap to 100 if needed
                adjusted_total = values.sum()
                return pd.Series([adjusted_total, f"Adjusted by {shortfall}"])
            else:
                return pd.Series([total, "No adjustment needed"])

        # Convert selected columns to numeric
        valid_df[score_columns] = valid_df[score_columns].apply(pd.to_numeric, errors='coerce')

        try:
            # Apply adjustment only to valid rows
            valid_df[["Adjusted Total", "Adjustment Note"]] = valid_df.apply(adjust_row, axis=1)

            # Merge back into original dataframe
            updated_df = df.copy()
            updated_df.loc[session_df.index, "Adjusted Total"] = valid_df["Adjusted Total"]
            updated_df.loc[session_df.index, "Adjustment Note"] = valid_df["Adjustment Note"]

            st.dataframe(updated_df)

            final_df = updated_df.copy()
            score_columns_without_selected = [col for col in score_columns if col != column_to_be_adjusted]

            result_series = updated_df["Adjusted Total"] - updated_df[score_columns_without_selected].apply(pd.to_numeric, errors='coerce').sum(axis=1)

            # Convert to a DataFrame with column name "New_Scores"
            new_df = pd.DataFrame({"New_Scores": result_series})

            updated_df[column_to_be_adjusted] = pd.to_numeric(updated_df[column_to_be_adjusted], errors='coerce')
            adjusted_total_numeric = pd.to_numeric(updated_df["Adjusted Total"], errors='coerce')

            # Data for summary statistics
            conditions = [
                updated_df["Adjustment Note"].str.contains(r'^Adjusted\s+by', case=False, na=False),  # Check if "Adjust by" exists
                (updated_df["Adjustment Note"].str.contains(r'\bNo\s+adjustment\s+needed\b', case=False, na=False)) & 
                (adjusted_total_numeric > 40),
                updated_df[score_columns].isna().any(axis=1)
            ]

            # Corresponding values for the conditions
            choices = ['Adjusted', 'Pass', 'Assessment not taken']

            # Default value if none of the conditions match
            default_choice = 'Fail'
            
            # Apply the conditions to create the new column
            updated_df['comment'] = np.select(conditions, choices, default=default_choice)

            # Dashboard: Display count of adjusted, pass, and assessment not taken
            session_counts = updated_df[updated_df["Section"] == selected_session]['comment'].value_counts()
            st.subheader("Dashboard: Summary of Results")

            # # Number of candidates who didn't write either of the assessments
            # number_of_candidates_who_did_not_write_either_assessment = updated_df[updated_df["Section"] == selected_session][score_columns].isna().sum().sum()
            # st.write(f"Candidates who didn't write either assessment: {number_of_candidates_who_did_not_write_either_assessment}")

            # Show metrics as cards
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric(label="Total Reg. Candidates", value=session_counts.sum())
            with col2:
                st.metric(label="Adjusted", value=session_counts.get('Adjusted', 0))
            with col3:
                st.metric(label="Pass", value=session_counts.get('Pass', 0))
            with col4:
                st.metric(label="Fail", value=session_counts.get('Fail', 0))
            with col5:
                st.metric(label="Assessment not taken", value=session_counts.get('Assessment not taken', 0))

            updated_df[updated_df["Section"] == selected_session][score_columns].isna().sum()

            
            # Pie chart of the breakdown of results
            fig = px.pie(session_counts, names=session_counts.index, values=session_counts.values, title="Results Breakdown")
            st.plotly_chart(fig)

            # Breakdown of adjusted and non-adjusted students
            st.subheader("Details of Adjusted Students")
            filtered_df = updated_df[
                (updated_df["Adjustment Note"].str.contains(r'^Adjusted\s+by', case=False, na=False)) |
                (updated_df["Section"] == selected_session) &
                (updated_df["comment"] == "Fail")
            ]
            st.dataframe(filtered_df)


            # Display the new scores column adjustment
            updated_df[column_to_be_adjusted] = np.where(
                new_df['New_Scores'] > updated_df[column_to_be_adjusted],
                new_df['New_Scores'].map(lambda x: f"{x:.2f}" if pd.notnull(x) else x).astype(object),
                updated_df[column_to_be_adjusted].map(lambda x: f"{x:.2f}" if pd.notnull(x) else x).astype(object)
            )

            st.subheader("Number of Students Who Didn't Take Assessment")
            # Calculate missing values per assessment
            missing_counts = updated_df[updated_df["Section"] == selected_session][score_columns].isna().sum()

            # Convert to DataFrame with descriptive column names
            missing_df = pd.DataFrame({
                "Assessment Type": missing_counts.index,
                "Number of Students": missing_counts.values
            })

            # Display
            st.dataframe(missing_df)


            st.info("If you're satisfied with the moderation, click the button below 👇 to download the moderated result 🤗 and refresh the page to moderate another exams.")
            # Downloadable Excel
            updated_df_download = updated_df.drop(columns=["Adjusted Total", "Adjustment Note"])
            output = BytesIO()
            updated_df_download.to_csv(output, index=False)
            st.download_button(
                label="📥 Download Updated CSV",
                data=output.getvalue(),
                file_name=new_filename,
                mime="text/csv"
            )
        except ValueError as e:
            # If the ValueError is raised, print a custom error message
            st.info("I think you've made a mistake🤔: Kindly choose the correct Cohort/Session and Score Columns.")
    else:
        st.info("Please make sure you've selected a session and score columns.")


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