import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re
import os


st.set_page_config(page_title="Moodle Gradebook Resolver", layout="wide")

def normalize_col(col):
    col = col.strip()
    col = re.sub(r"\.\d+$", "", col)  # remove .1, .2, .3
    return col

col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.write("")
with col2:
    st.title("📊 Moodle Gradebook Duplicate Column Resolver")

    st.write(
        """
        This app helps resolve duplicated assessment columns from Moodle gradebooks.
        
        **Logic used:**
        - If a student has **no score in all selected duplicate columns** → result is empty
        - If a student has **scores in one or more columns** → highest score is used
        """
    )

    # -------------------------------
    # File Upload
    # -------------------------------
    uploaded_file = st.file_uploader(
        "Upload Gradebook (CSV or Excel)",
        type=["csv", "xlsx"]
    )

    if uploaded_file:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully!")

        st.subheader("📄 Raw Data Preview")
        st.dataframe(df.head())

        
        # Extracting the uploaded file to name the Resolved filename
        original_filename = uploaded_file.name
        base_filename = os.path.splitext(original_filename)[0]
        safe_name = re.sub(r"[^\w\s-]", "", base_filename)
        resolved_filename = f"{safe_name}_resolved_gradebook"
        # resolved_filename = f"{base_filename}_resolved_gradebook"


        st.subheader("⚙️ Duplicate Column Detection")

        mode = st.radio(
            "Choose how to identify duplicated assessments:",
            ["Automatically detect duplicates", "Manually select columns"]
        )

        column_groups = {}

        # -------------------------------
        # AUTO DETECT MODE
        # -------------------------------
        if mode == "Automatically detect duplicates":

            normalized_map = {}

            for col in df.columns:
                base = normalize_col(col)
                normalized_map.setdefault(base, []).append(col)

            auto_duplicates = {
                base: cols for base, cols in normalized_map.items() if len(cols) > 1
            }

            if not auto_duplicates:
                st.info("No duplicated columns detected automatically.")
            else:
                st.subheader("🔁 Detected Duplicate Groups")

                for base_col, cols in auto_duplicates.items():
                    resolved_name = f"{base_col} (Resolved)"

                    with st.expander(f"{base_col}"):
                        st.write("Columns to be merged:")
                        st.write(cols)

                        column_groups[base_col] = {
                            "selected": cols,
                            "resolved_name": resolved_name
                        }

        # -------------------------------
        # MANUAL MODE
        # -------------------------------
        else:
            st.subheader("✋ Manual Selection")

            selected_cols = st.multiselect(
                "Select columns to merge",
                options=df.columns.tolist()
            )

            if selected_cols:
                base_name = normalize_col(selected_cols[0])
                resolved_name = f"{base_name} (Resolved)"

                st.info(f"Resolved column will be named: **{resolved_name}**")

                column_groups["manual"] = {
                    "selected": selected_cols,
                    "resolved_name": resolved_name
                }
        # -------------------------------
        # Analyze Button
        # -------------------------------
        if st.button("🔍 Analyze"):
            resolved_df = df.copy()

            for group in column_groups.values():
                cols = group["selected"]
                resolved_name = group["resolved_name"]

                # Convert to numeric safely
                temp = resolved_df[cols].apply(pd.to_numeric, errors="coerce")

                # Row-wise resolution
                def resolve_row(row):
                    if row.isna().all():
                        return np.nan
                    return row.max()

                resolved_df[resolved_name] = temp.apply(resolve_row, axis=1)



            st.subheader("👀 Preview: With Duplicates + Resolved Columns")
            st.dataframe(resolved_df.head(20))

            # -------------------------------
            # Prepare final download version
            # -------------------------------
            drop_cols = []
            keep_cols = []

            for group in column_groups.values():
                drop_cols.extend(group["selected"])
                keep_cols.append(group["resolved_name"])

            final_df = resolved_df.drop(columns=drop_cols)

            st.subheader("✅ Final Sheet (Duplicates Dropped)")
            st.dataframe(final_df.head(20))

            # -------------------------------
            # Download Section
            # -------------------------------
            st.subheader("⬇️ Download Resolved Gradebook")

            col1, col2 = st.columns(2)

            with col1:
                csv = final_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download as CSV",
                    data=csv,
                    file_name=f"{resolved_filename}.csv",
                    mime="text/csv"
                )


            with col2:
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    final_df.to_excel(writer, index=False, sheet_name="Resolved")
                st.download_button(
                    "Download as Excel",
                    data=output.getvalue(),
                    file_name=f"{resolved_filename}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    else:
        st.info("👆 Upload a CSV or Excel gradebook to begin.")
with col3:
    st.write("")
