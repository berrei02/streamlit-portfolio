import streamlit as st

about_page = st.Page("content/about.py", title="About Stefan")

tennis_dashboard = st.Page(
    "content/tennis_dashboard.py", title="Tennis Analytics", icon=":material/dashboard:")

next_project = st.Page("content/next.py", title="Upcoming ...", icon=":material/bug_report:")


pg = st.navigation(
    {
        "About": [about_page],
        "Apps": [tennis_dashboard, next_project],
    }
)
pg.run()