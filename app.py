import streamlit as st

st.set_page_config(page_title="Stefan Berreiter")

about_page = st.Page("content/about.py", title="About Stefan")

project_foo = st.Page(
    "content/foo.py", title="Foo App", icon=":material/dashboard:")

project_bar = st.Page("content/bar.py", title="Bar app", icon=":material/bug_report:")


pg = st.navigation(
    {
        "About": [about_page],
        "Apps": [project_foo, project_bar],
    }
)

st.write("# Welcome")

main_page_text = """
This will become my portfolio Website.
"""

st.write(main_page_text)
