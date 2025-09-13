# import streamlit as st

# st.set_page_config(page_title="Welcome", layout="wide")

# st.markdown(
#     """
#     <style>
#     .landing-title {
#         font-size: 42px;
#         font-weight: bold;
#         color: #4CAF50;
#     }
#     .landing-sub {
#         font-size: 24px;
#         color: #333333;
#     }
#     .landing-note {
#         font-size: 18px;
#         color: #555555;
#         line-height: 1.6;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.markdown('<div class="landing-title">🎯 Moderator Score Adjustment App</div>', unsafe_allow_html=True)
# st.markdown('<div class="landing-sub">An intelligent tool to adjust and standardize scores across sessions.</div>', unsafe_allow_html=True)

# # st.image("https://images.unsplash.com/photo-1635339821940-2ba8f33fae3e", use_container_width=True)

# st.markdown("### 👋 What This App Does")
# st.markdown(
#     """
#     <div class="landing-note">
#     This app helps academic moderators adjust scores where necessary, ensuring fairness for students who may have just missed the pass mark due to slight variations in assessment combinations.

#     Simply upload your CSV file, filter by session, select the score columns, and the app will do the rest – including:
#     - Calculating totals
#     - Making threshold-based adjustments
#     - Visualizing outcomes
#     - Enabling easy CSV download

#     <br>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# st.markdown("### 🔧 How to Use")
# st.markdown(
#     """
#     1. Upload a valid CSV file containing students’ scores.
#     2. Select the cohort or session you're working on.
#     3. Choose the score columns used to compute the total score.
#     4. Set the minimum pass threshold (e.g., 40).
#     5. View the adjustments, statistics, and download your updated file.
#     """
# )

# st.success("🎉 Ready to get started? Click on the main app page from the sidebar!")

# st.markdown(
#     """
#     <style>
#     .main-footer {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         right: 0;
#         background-color: #f0f2f6;
#         padding: 10px 0;
#         font-size: 13px;
#         text-align: center;
#         color: #444;
#         border-top: 1px solid #ddd;
#         z-index: 9999;
#     }
#     .main-footer a {
#         text-decoration: none;
#         margin: 0 8px;
#         color: #0366d6;
#     }
#     .main-footer a:hover {
#         text-decoration: underline;
#     }
#     .footer-icons {
#         margin-top: 5px;
#     }
#     .footer-icons a {
#         text-decoration: none;
#         color: #444;
#         margin: 0 10px;
#         font-size: 16px;
#     }
#     </style>
#     <div class="main-footer">
#         Design, Developed and Deployed by <strong>Nnamdi A. Isichei</strong> &copy; 2025 <br/>
#         <div class="footer-icons">
#             <a href="https://github.com/isichei-nnamdi" target="_blank">GitHub</a> |
#             <a href="https://www.linkedin.com/in/nnamdi-isichei/" target="_blank">LinkedIn</a> |
#             <a href="mailto:augustus@miva.university" target="_blank">Email</a>
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )


# st.sidebar.markdown(
#     """
#     <style>
#     .sidebar-footer {
#         margin-top: 30px;
#         font-size: 12px;
#         color: #666;
#         text-align: center;
#     }
#     .sidebar-footer a {
#         text-decoration: none;
#         color: #0366d6;
#         margin: 0 4px;
#     }
#     .sidebar-footer a:hover {
#         text-decoration: underline;
#     }
#     </style>
#     <div class="sidebar-footer">
#         &copy; 2025 <br/>
#         <strong>Nnamdi A. Isichei</strong><br/>
#         <a href="https://github.com/isichei-nnamdi" target="_blank">GitHub</a> |
#         <a href="https://www.linkedin.com/in/nnamdi-isichei/" target="_blank">LinkedIn</a> |
#         <a href="mailto:augustus@miva.university" target="_blank">Email</a>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

import streamlit as st
st.set_page_config(page_title="Moderator App", layout="centered", initial_sidebar_state="collapsed")

# HIDE DEFAULT STREAMLIT NAVIGATION
hide_nav_style = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_nav_style, unsafe_allow_html=True)


# Sidebar Navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🎯 Moderation on Canvas", "📝 Moderation on Moodle", "📘 Documentation"])

# Sidebar Footer
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

# Optional: Use switch_page if using multipage structure
if page == "🎯 Moderation on Canvas":
    st.switch_page("pages/Moderate.py")
elif page == "📝 Moderation on Moodle":
    st.switch_page("pages/Moodle_moderation.py")
elif page == "📘 Documentation":
    st.switch_page("pages/Documentation.py")
elif page == "🏠 Home":
    st.markdown(
        """
        <style>
        .landing-title {
            font-size: 42px;
            font-weight: bold;
            color: #4CAF50;
        }
        .landing-sub {
            font-size: 24px;
            color: #333333;
        }
        .landing-note {
            font-size: 18px;
            color: #555555;
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # st.markdown('<div class="landing-title">🎯 Moderator Score Adjustment App</div>', unsafe_allow_html=True)
    # st.markdown('<div class="landing-sub">An intelligent tool to adjust and standardize scores across sessions.</div>', unsafe_allow_html=True)

    # st.markdown("### 👋 What This App Does")
    # st.markdown(
    #     """
    #     <div class="landing-note">
    #     This app helps academic moderators adjust scores where necessary, ensuring fairness for students who may have just missed the pass mark due to slight variations in assessment combinations.

    #     Simply upload your CSV file, filter by session, select the score columns, and the app will do the rest – including:
    #     - Calculating totals
    #     - Making threshold-based adjustments
    #     - Visualizing outcomes
    #     - Enabling easy CSV download

    #     <br>
    #     </div>
    #     """,
    #     unsafe_allow_html=True,
    # )

    # st.markdown("### 🔧 How to Use")
    # st.markdown(
    #     """
    #     1. Upload a valid CSV file containing students’ scores.
    #     2. Select the cohort or session you're working on.
    #     3. Choose the score columns used to compute the total score.
    #     4. Set the minimum pass threshold (e.g., 40).
    #     5. View the adjustments, statistics, and download your updated file.
    #     """
    # )

    # st.success("🎉 Ready to get started? Click on the 'Moderate' page from the sidebar!")

    # 🎯 App Title
    st.markdown('<div class="landing-title">🎯 Moderator Score Adjustment App</div>', unsafe_allow_html=True)
    st.markdown('<div class="landing-sub">An intelligent tool to adjust and standardize scores across sessions.</div>', unsafe_allow_html=True)

    # ============================
    # MOODLE MODERATION
    # ============================
    st.markdown("#### 🖥️ Moderation on Moodle")

    st.markdown("##### 👋 What This App Does")
    st.markdown(
        """
        <div class="landing-note">
        This section is designed for datasets exported from <b>Moodle LMS</b>.  
        It ensures fairness for students whose scores are close to the pass mark by applying threshold-based adjustments.  

        The Moodle moderation process automatically:  
        - Uploads and reads student score exports  
        - Computes <b>Raw Totals</b> from selected assessments  
        - Applies <b>boundary adjustments</b> (e.g., 39 → 40, 44 → 45)  
        - Allows <b>further moderation</b> for scores between a set threshold and 40  
        - Recomputes <b>Grades</b> and <b>Status</b> (Pass, Fail, Incomplete, No Score)  
        - Provides <b>before vs after comparisons</b> in tables and charts  
        - Enables <b>download of moderated results</b>  

        <br>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#####🔧 How to Use (Moodle)")
    st.markdown(
        """
        1. Upload a Moodle-exported CSV/Excel file with student scores.  
        2. Select the relevant session or cohort.  
        3. Choose the score columns used to calculate totals.  
        4. Set the pass threshold (default = 40).  
        5. Review moderated scores, statistics, and grade distributions.  
        6. Download the adjusted dataset.  
        """
    )

    # ============================
    # CANVAS MODERATION
    # ============================
    st.markdown("#### 🎓 Moderation on Canvas")

    st.markdown("##### 👋 What This App Does")
    st.markdown(
        """
        <div class="landing-note">
        This section is tailored for grade exports from <b>Canvas LMS</b>.  
        It adapts to Canvas grading structures while applying the same fairness principle.  

        The Canvas moderation process automatically:  
        - Uploads and processes Canvas gradebook exports  
        - Computes <b>Overall Totals</b> from chosen assessments  
        - Applies <b>boundary adjustments</b> to borderline scores  
        - Allows <b>further moderation</b> to raise some failed scores to 40  
        - Reassigns <b>Grades</b> and <b>Status</b> consistently  
        - Provides <b>visual insights</b> with clustered bar charts (before vs after)  
        - Enables <b>download of moderated results</b>  

        <br>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("##### 🔧 How to Use (Canvas)")
    st.markdown(
        """
        1. Upload a Canvas gradebook export file.  
        2. Select the assessment columns used to compute totals.  
        3. Set the moderation threshold (e.g., 40).  
        4. Review moderated scores, statistics, and grade distributions.  
        5. Download the adjusted dataset for departmental use.  
        """
    )

    # ============================
    # FOOTER MESSAGE
    # ============================
    st.success("🎉 Ready to get started? Select either 'Moodle Moderation' or 'Canvas Moderation' from the sidebar!")


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