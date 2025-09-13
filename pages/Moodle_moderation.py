import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import os
from io import BytesIO

st.set_page_config(page_title="Moderation on Moodle", layout="centered", initial_sidebar_state="collapsed")

# HIDE DEFAULT STREAMLIT NAVIGATION
hide_nav_style = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_nav_style, unsafe_allow_html=True)

st.page_link("app.py", label="Back to Home", icon="🏠")


# --- Helper functions ---
def round_boundary(score):
    if score in [39, 44, 49, 59, 69]:
        return score + 1
    return score

def assign_grade(score):
    if score < 40:
        return "F"
    elif score < 45:
        return "E"
    elif score < 50:
        return "D"
    elif score < 60:
        return "C"
    elif score < 70:
        return "B"
    else:
        return "A"

# --- App Layout ---
st.title("📊 Exam Moderation Tool")

# Initialize session state if not already
def init_session():
    if "df" not in st.session_state:
        st.session_state.df = None

init_session()

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file and st.session_state.df is None:
    if uploaded_file.name.endswith("csv"):
        st.session_state.df = pd.read_csv(uploaded_file)
    else:
        st.session_state.df = pd.read_excel(uploaded_file)

if st.session_state.df is not None:
    df = st.session_state.df.copy()

    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Step 1: Select columns
    st.subheader("Step 1: Choose Columns for Moderation")
    columns = st.multiselect(
        "Select columns to include in score calculation",
        df.columns
    )

    # Step 2: Choose update field
    st.subheader("Step 2: Choose Field to Update After Moderation")
    update_field = st.selectbox(
        "Select the column that will be updated with the moderated score",
        df.columns
    )

    # Step 3: Threshold input
    threshold = st.number_input(
        "Enter threshold for further moderation (leave at 0 for none)",
        min_value=0, max_value=100, step=1, value=0
    )

    # --- When user clicks the moderate button, do all moderation in one pass ---
if st.button("Moderate Result"):

    if not columns:
        st.warning("⚠️ Please select at least one column to proceed.")
    else:
        # ---------- IMPORTANT: Work on a numeric copy that preserves NaNs ----------
        # numeric_raw has NaN where scores were not recorded — we will use this
        selected_data = df[columns]
        numeric_raw = selected_data.apply(pd.to_numeric, errors="coerce")  # NaNs preserved
        

        # For arithmetic we will create a filled version when needed:
        numeric_filled = numeric_raw.fillna(0)

        # ---------- Initial moderation (boundary) ----------
        df["RawScore"] = numeric_filled.sum(axis=1)
        df["ModeratedTotalScore"] = df["RawScore"].apply(round_boundary)

        # assign grade only for students who attempted ALL selected assessments (use numeric_raw)
        df["Grade"] = np.where(
            numeric_raw.notna().all(axis=1),
            df["ModeratedTotalScore"].apply(assign_grade),
            np.nan
        )

        # Keep a copy BEFORE further moderation for comparisons
        df_before = df.copy()
        numeric_raw_before = numeric_raw.copy()

        try:
            # ---------- Further moderation (optional) ----------
            further_count = 0
            moderated_40_list = pd.DataFrame()
            if threshold > 0:
                # Only consider failed students who had a value recorded in the selected update_field
                # (this prevents turning previously-missing cells into recorded attempts)
                pre_mask = (
                    (df["Grade"] == "F") &
                    (df["ModeratedTotalScore"] >= threshold) &
                    (df["ModeratedTotalScore"] < 40) &
                    (numeric_raw[update_field].notna())   # must have had an actual recorded value
                )

                if pre_mask.any():
                    # compute how much to add to bring each student's ModeratedTotalScore to 40
                    diff = 40 - df.loc[pre_mask, "ModeratedTotalScore"]
                    # apply the diff to the numeric_raw (not to df directly)
                    numeric_raw.loc[pre_mask, update_field] = numeric_raw.loc[pre_mask, update_field].fillna(0) + diff

                    further_count = int(pre_mask.sum())

                    # After changing numeric_raw we must recompute filled sums and moderated total
                    numeric_filled = numeric_raw.fillna(0)
                    df["RawScore"] = numeric_filled.sum(axis=1)
                    df["ModeratedTotalScore"] = df["RawScore"].apply(round_boundary)

                    # Reassign grade only to those who attempted all assessments
                    df["Grade"] = np.where(
                        numeric_raw.notna().all(axis=1),
                        df["ModeratedTotalScore"].apply(assign_grade),
                        np.nan
                    )

            # ---------- Compute ModeratedExamScore (final moderated value for the update_field) ----------
            # Only compute ModeratedExamScore for students who originally had a recorded value in the update_field
            df["ModeratedExamScore"] = np.where(
                numeric_raw[update_field].notna(),                               # True if user originally had a value
                numeric_raw[update_field] + (df["ModeratedTotalScore"] - df["RawScore"]),
                np.nan  # keep NaN for those with no score recorded in the selected update_field
            )

            # update the dataframe column used for download / final output without destroying NA info for the others:
            # We want the moderated column to contain the final moderated value where applicable, and preserve original blanks
            df[update_field] = df["ModeratedExamScore"].combine_first(df[update_field])

            # ---------- Status classification using numeric_raw (preserves No Score / Incomplete) ----------
            def classify_status_row(r):
                nr = numeric_raw.loc[r.name]
                if nr.isna().all():
                    return "No Score"
                elif nr.isna().any():
                    return "Incomplete"
                else:
                    return "Pass" if r["ModeratedTotalScore"] >= 40 else "Fail"

            df["Status"] = df.apply(classify_status_row, axis=1)

            # ---------- Build summary using numeric_raw (so attempted counts are correct) ----------
            total_students = len(df)
            attempted_all = numeric_raw.notna().all(axis=1).sum()
            boundary_count = df["RawScore"].apply(lambda x: x in [39, 44, 49, 59, 69]).sum()

            summary_rows = [
                ["Total enrolled", total_students, "100%"],
                ["Attempted all selected assessments", attempted_all, f"{attempted_all/total_students:.1%}"],
                [f"Attempted {update_field} only (missed others)",
                    ((numeric_raw[update_field].notna()) & (numeric_raw.drop(columns=[update_field]).isna().any(axis=1))).sum(),
                    f"{((numeric_raw[update_field].notna()) & (numeric_raw.drop(columns=[update_field]).isna().any(axis=1))).sum()/total_students:.1%}"
                ],
                ["Boundary adjustments (+1)", boundary_count, f"{boundary_count/total_students:.1%}"],
            ]
            if threshold > 0:
                summary_rows.append(["Further moderated to 40", further_count, f"{further_count/total_students:.1%}"])

            # Per-assessment attempt counts (use numeric_raw)
            for col in columns:
                cnt = numeric_raw[col].notna().sum()
                summary_rows.append([f"Attempted {col}", cnt, f"{cnt/total_students:.1%}"])

            # Status distribution
            for st_label in ["Pass", "Fail", "Incomplete", "No Score"]:
                cnt = (df["Status"] == st_label).sum()
                summary_rows.append([st_label, cnt, f"{cnt/total_students:.1%}"])

            # Grade distribution (exclude NaN)
            for grade, cnt in df["Grade"].dropna().value_counts().sort_index().items():
                summary_rows.append([f"Grade {grade}", int(cnt), f"{cnt/total_students:.1%}"])

            summary_df = pd.DataFrame(summary_rows, columns=["Metric", "Count", "Percentage"])
            st.subheader("📋 Summary Table")
            st.dataframe(summary_df, use_container_width=True)

            # ---------- Preview moderated results (final) ----------
            st.subheader("Moderated Results Preview")
            show_cols = ["First name", "Last name", update_field, "ModeratedExamScore", "RawScore", "ModeratedTotalScore", "Grade", "Status"]
            available_show_cols = [c for c in show_cols if c in df.columns]
            st.dataframe(df[available_show_cols])

        
            moderated_40_list = df.loc[pre_mask].copy()

            # Add the "ExamScoreBefore" column
            moderated_40_list["ExamScoreBefore"] = numeric_raw_before.loc[pre_mask, update_field]

            # Reorder columns to your desired layout
            required_cols = [
                "First name", "Last name", "ExamScoreBefore",
                "ModeratedExamScore", "ModeratedTotalScore",
                "Grade", "Status"
            ]

            # Only keep those columns (in the exact order)
            moderated_40_list = moderated_40_list[[c for c in required_cols if c in moderated_40_list.columns]]

            # Filter out Incomplete
            moderated_40_list = moderated_40_list[moderated_40_list["Status"] != "Incomplete"]

            # ---------- If further moderation happened: show list ----------
            if threshold > 0 and further_count > 0 and not moderated_40_list.empty:
                st.subheader("🔄 Students Moderated to 40")
                st.dataframe(moderated_40_list.head(100), use_container_width=True)


                # ---- Overall before vs after summary (status & grade) ----
                st.subheader("📊 Overall Before vs After Summary")
                import matplotlib.pyplot as plt
                import numpy as np

                # ==============================
                # STATUS DISTRIBUTION
                # ==============================
                if "Status" not in df_before.columns:
                    df_before["Status"] = df_before.apply(classify_status_row, axis=1)

                if "Status" not in df.columns:
                    df["Status"] = df.apply(classify_status_row, axis=1)

                # Define all possible statuses
                all_statuses = ["Pass", "Fail", "Incomplete", "No Score"]

                # Count values and reindex to include all statuses (fill missing with 0)
                before_counts = df_before["Status"].value_counts().reindex(all_statuses, fill_value=0)
                after_counts = df["Status"].value_counts().reindex(all_statuses, fill_value=0)

                # ==============================
                # GRADE DISTRIBUTION
                # ==============================
                grade_fig = None
                if "Grade" in df_before.columns and "Grade" in df.columns:
                    grades_all = sorted(
                        set(df_before["Grade"].dropna().astype(str).unique()) |
                        set(df["Grade"].dropna().astype(str).unique())
                    )

                    before_grade = df_before["Grade"].astype(str).value_counts().reindex(grades_all, fill_value=0)
                    after_grade = df["Grade"].astype(str).value_counts().reindex(grades_all, fill_value=0)

                    # Build grade chart
                    xg = np.arange(len(grades_all))
                    width = 0.35

                    grade_fig, axg = plt.subplots(figsize=(6, 5))
                    bars1 = axg.bar(xg - width/2, before_grade, width, label="Before")
                    bars2 = axg.bar(xg + width/2, after_grade, width, label="After")

                    for bar in bars1 + bars2:
                        height = bar.get_height()
                        axg.annotate(f"{height}",
                                    xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 3),
                                    textcoords="offset points",
                                    ha="center", va="bottom")

                    axg.set_title("🎓 Grade Distribution Change")
                    axg.set_xticks(xg)
                    axg.set_xticklabels(grades_all)
                    axg.legend()

                else:
                    st.warning("⚠️ 'Grade' column not found in one of the dataframes. Skipping grade comparison.")

                # ==============================
                # SHOW SIDE BY SIDE
                # ==============================
                col1, col2 = st.columns(2)

                # Status chart
                with col1:
                    xs = np.arange(len(all_statuses))
                    width = 0.35
                    status_fig, axs = plt.subplots(figsize=(6, 5))
                    bars1 = axs.bar(xs - width/2, before_counts, width, label="Before")
                    bars2 = axs.bar(xs + width/2, after_counts, width, label="After")

                    for bar in bars1 + bars2:
                        height = bar.get_height()
                        axs.annotate(f"{height}",
                                    xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 3),
                                    textcoords="offset points",
                                    ha="center", va="bottom")

                    axs.set_title("📊 Status Distribution Change")
                    axs.set_xticks(xs)
                    axs.set_xticklabels(all_statuses)
                    axs.legend()

                    st.pyplot(status_fig)

                # Grade chart
                with col2:
                    if grade_fig:
                        st.pyplot(grade_fig)
        except Exception as e:
            st.error(f"No charts to be generated for this moderation.")


        # ---------- Prepare downloadable file ----------
        # df_download = df.copy()
        # # Ensure the moderated final score is in the selected column (but preserve blanks if they were blanks)
        # df_download[update_field] = df["ModeratedExamScore"].combine_first(df_download[update_field])

        # # drop helper cols that you don't want in final export (optional)
        # helper_cols = ["RawScore", "ModeratedTotalScore", "ModeratedExamScore", "BoundaryAdjusted", "Status", "Grade"]
        # to_drop = [c for c in helper_cols if c in df_download.columns]
        # df_download_export = df_download.drop(columns=to_drop)

        # st.success("✅ Moderation complete — download below.")
        # csv = df_download_export.to_csv(index=False).encode("utf-8")
        # st.download_button("Download CSV", csv, "moderated_results.csv", "text/csv")

        # ---------- Prepare downloadable file ----------
        df_download = df.copy()
        # Ensure the moderated final score is in the selected column (but preserve blanks if they were blanks)
        df_download[update_field] = df["ModeratedExamScore"].combine_first(df_download[update_field])

        # drop helper cols that you don't want in final export (optional)
        helper_cols = ["RawScore", "ModeratedTotalScore", "ModeratedExamScore", "BoundaryAdjusted", "Status", "Grade"]
        to_drop = [c for c in helper_cols if c in df_download.columns]
        df_download_export = df_download.drop(columns=to_drop)

        st.success("✅ Moderation complete — download below.")

        if uploaded_file is not None:
            base_name, _ = os.path.splitext(uploaded_file.name)

            # Let the user choose the output format
            download_format = st.radio(
                "📂 Choose download format:",
                ("CSV", "Excel (.xlsx)"),
                horizontal=True
            )

            if download_format == "Excel (.xlsx)":
                file_name = f"{base_name}_ModeratedResults.xlsx"

                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df_download_export.to_excel(writer, index=False, sheet_name="Moderated Results")
                processed_data = output.getvalue()

                st.download_button(
                    label="⬇️ Download Moderated Excel",
                    data=processed_data,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

            else:  # CSV
                file_name = f"{base_name}_ModeratedResults.csv"

                csv_data = df_download_export.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Download Moderated CSV",
                    data=csv_data,
                    file_name=file_name,
                    mime="text/csv",
                )
